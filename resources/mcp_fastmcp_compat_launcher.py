#!/usr/bin/env python3
"""Compatibility launcher for MCP Python SDK 1.x servers running on SDK 2.x.

Problem
-------
In ``mcp`` 2.x the high-level server class ``FastMCP`` was renamed to
``MCPServer`` and the module was moved from ``mcp.server.fastmcp`` to
``mcp.server.mcpserver``. The old import path was *removed*, not deprecated,
so an unmodified 1.x server dies at import time with::

    ModuleNotFoundError: No module named 'mcp.server.fastmcp'

Clients usually report only "Connection closed" because the server crashes
before it can log a traceback.

What this file does
-------------------
It installs a lightweight shim into ``sys.modules`` that:

* makes ``mcp.server.fastmcp`` (and all of its submodules) importable again;
* maps ``FastMCP`` to ``MCPServer`` (with 1.x positional-argument order
  preserved);
* maps ``FastMCPError`` to ``MCPServerError``;
* adds ``Context.fastmcp`` as an alias of ``Context.mcp_server``;
* restores a working ``get_context()`` for tool/resource/prompt handlers;
* lets 1.x constructor transport arguments (``host``, ``port``, ``sse_path``,
  ``streamable_http_path``, ...) keep working by forwarding them to
  ``run()`` / the app factories at call time;
* tolerates 1.x ``mcp.settings.<transport_field> = ...`` assignments.

Usage
-----
1. Import a server module and call a function on it (the form used in
   ``mcp.json`` for the clangd and JVM servers)::

       python mcp_fastmcp_compat_launcher.py <module> <callable>

   For example::

       {"command": "/home/user/venv/bin/python",
        "args": ["/home/user/mcp_fastmcp_compat_launcher.py",
                 "clangd_mcp.server", "main"]}

   ``<callable>`` defaults to ``main`` when omitted. Extra arguments are
   passed to the callable, and an async callable is awaited automatically.
   The module is imported under its real name, so ``if __name__ ==
   "__main__":`` guards do *not* fire — the explicit callable is what starts
   the server. This is why ``jvm_mcp_server.__main__`` works here.

2. As a launcher for an existing 1.x server script::

       python mcp_fastmcp_compat_launcher.py /path/to/server.py [args...]
       python mcp_fastmcp_compat_launcher.py -m mypackage.server [args...]

3. As an in-process shim. Put this at the *very top* of your 1.x server,
   before any ``mcp`` import::

       import mcp_fastmcp_compat_launcher
       mcp_fastmcp_compat_launcher.install()

4. Via ``PYTHONPATH`` / ``sitecustomize.py`` if you want the shim in every
   Python process.

Nothing is patched until :func:`install` is called (or the launcher's
``main()`` runs), so importing this file is side-effect free.

Notes
-----
The shim is intentionally a *bridge*, not a full reimplementation of 1.x.
It covers the class/module renames and the argument moves that break a
decorator-built server at startup. It does not attempt to restore removed
low-level APIs (``request_ctx``, ``streamablehttp_client``, ambient
``Server.request_context``, etc.) — servers using those still need a real
migration.

Tested against ``mcp==2.3.0``. Safe to call ``install()`` more than once.
"""

from __future__ import annotations

import contextvars
import importlib
import inspect
import os
import runpy
import sys
import types
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from mcp.server.mcpserver import Context, MCPServer

__all__ = ["install", "is_installed", "main"]

_MARKER = "_mcp_fastmcp_compat_installed"

# 1.x FastMCP positional order after ``name``. In 2.x the second positional
# argument is ``title``, so a bare positional remap is required to avoid a
# silent mis-assignment of ``instructions`` -> ``title``.
_V1_POSITIONAL_AFTER_NAME = ("instructions", "website_url", "icons")

# Constructor arguments that 2.x moved to run()/app factories. 1.x code
# commonly passed these to FastMCP(...); we stash them and replay them later.
_TRANSPORT_KWARGS = frozenset(
    {
        "host",
        "port",
        "sse_path",
        "message_path",
        "streamable_http_path",
        "json_response",
        "stateless_http",
        "max_request_body_size",
        "event_store",
        "retry_interval",
        "transport_security",
        "session_idle_timeout",
        "max_sessions",
        "mount_path",
    }
)

_SSE_KWARGS = frozenset(
    {
        "host",
        "port",
        "sse_path",
        "message_path",
        "max_request_body_size",
        "transport_security",
    }
)

_HTTP_KWARGS = frozenset(
    {
        "host",
        "port",
        "streamable_http_path",
        "json_response",
        "stateless_http",
        "event_store",
        "retry_interval",
        "max_request_body_size",
        "session_idle_timeout",
        "max_sessions",
        "transport_security",
    }
)

# Ambient context, restored for get_context() in handler code.
_current_context: contextvars.ContextVar["Context[Any, Any] | None"] = contextvars.ContextVar(
    "mcp_fastmcp_compat_current_context", default=None
)


def is_installed() -> bool:
    """Return True when the compatibility shim is already active."""
    server_pkg = sys.modules.get("mcp.server")
    return bool(server_pkg and getattr(server_pkg, _MARKER, False))


def _get_context() -> "Context[Any, Any]":
    """1.x-compatible ``get_context()``.

    Works inside tool/resource/prompt handlers because the wrapper records the
    ``Context`` passed by the 2.x dispatcher in a ContextVar.
    """
    ctx = _current_context.get()
    if ctx is None:
        raise RuntimeError(
            "mcp_fastmcp_compat_launcher: get_context() is only available inside a "
            "tool/resource/prompt handler. Prefer declaring a `ctx: Context` "
            "parameter in the 2.x API."
        )
    return ctx


class _SettingsProxy:
    """Delegate to the real Settings, but redirect 1.x transport fields.

    In 1.x, code often did ``mcp.settings.port = 9000``. In 2.x Settings is a
    Pydantic model that rejects those fields. The proxy keeps them in the
    server's transport stash instead.
    """

    __slots__ = ("_settings", "_stash")

    def __init__(self, settings: Any, stash: dict[str, Any]) -> None:
        object.__setattr__(self, "_settings", settings)
        object.__setattr__(self, "_stash", stash)

    def __getattr__(self, name: str) -> Any:
        return getattr(object.__getattribute__(self, "_settings"), name)

    def __setattr__(self, name: str, value: Any) -> None:
        if name in _TRANSPORT_KWARGS:
            object.__getattribute__(self, "_stash")[name] = value
            return
        setattr(object.__getattribute__(self, "_settings"), name, value)

    def __repr__(self) -> str:  # pragma: no cover - cosmetic
        return f"<compat SettingsProxy {object.__getattribute__(self, '_settings')!r}>"


def _make_fastmcp_compat(MCPServer: type) -> type:  # noqa: N802 - name is intentional
    """Build a FastMCP-compatible subclass of MCPServer."""
    init_params = inspect.signature(MCPServer.__init__).parameters
    constructor_names = set(init_params) - {"self", "kwargs", "args"}

    class FastMCP(MCPServer):  # type: ignore[misc,valid-type]
        """1.x FastMCP facade over the 2.x MCPServer class."""

        def __init__(self, name: str | None = None, *args: Any, **kwargs: Any) -> None:
            if len(args) > len(_V1_POSITIONAL_AFTER_NAME):
                raise TypeError(
                    f"FastMCP() takes at most {len(_V1_POSITIONAL_AFTER_NAME) + 1} "
                    f"positional arguments but {len(args) + 1} were given"
                )

            stash: dict[str, Any] = {}
            constructor: dict[str, Any] = {}

            # Map 1.x positional arguments to their 1.x keywords.
            for key, value in zip(_V1_POSITIONAL_AFTER_NAME, args):
                if key in kwargs:
                    raise TypeError(f"FastMCP() got multiple values for argument '{key}'")
                constructor[key] = value

            # Split keywords: transport settings get stashed, the rest go to MCPServer.
            for key, value in kwargs.items():
                if key in _TRANSPORT_KWARGS:
                    stash[key] = value
                else:
                    if key in constructor:
                        raise TypeError(f"FastMCP() got multiple values for argument '{key}'")
                    constructor[key] = value

            super().__init__(name, **constructor)
            object.__setattr__(self, "_compat_transport_kwargs", stash)
            object.__setattr__(self, "settings", _SettingsProxy(self.settings, stash))

        @property
        def _transport_stash(self) -> dict[str, Any]:
            return object.__getattribute__(self, "_compat_transport_kwargs")

        def _merged(self, allowed: frozenset[str], overrides: dict[str, Any]) -> dict[str, Any]:
            merged = {k: v for k, v in self._transport_stash.items() if k in allowed}
            merged.update(overrides)
            return merged

        def run(self, transport: str = "stdio", **kwargs: Any) -> None:
            if transport == "stdio":
                # 2.x stdio ignores extra kwargs; pass none to stay faithful.
                return super().run(transport)  # type: ignore[arg-type]
            allowed = _SSE_KWARGS if transport == "sse" else _HTTP_KWARGS
            return super().run(transport, **self._merged(allowed, kwargs))  # type: ignore[arg-type]

        def sse_app(self, **kwargs: Any) -> Any:
            return super().sse_app(**self._merged(_SSE_KWARGS, kwargs))

        def streamable_http_app(self, **kwargs: Any) -> Any:
            return super().streamable_http_app(**self._merged(_HTTP_KWARGS, kwargs))

        def get_context(self) -> "Context[Any, Any]":
            """1.x ``mcp.get_context()``."""
            return _get_context()

        def _ensure_context(self, context: Any) -> Any:
            """Mirror MCPServer's implicit Context creation so get_context works."""
            if context is not None:
                return context
            from mcp.server.mcpserver import Context

            return Context(mcp_server=self, subscriptions=self._subscriptions)

        async def call_tool(self, name: str, arguments: dict[str, Any], context: Any = None) -> Any:
            context = self._ensure_context(context)
            token = _current_context.set(context)
            try:
                return await super().call_tool(name, arguments, context)
            finally:
                _current_context.reset(token)

        async def read_resource(self, uri: Any, context: Any = None) -> Any:
            context = self._ensure_context(context)
            token = _current_context.set(context)
            try:
                return await super().read_resource(uri, context)
            finally:
                _current_context.reset(token)

        async def get_prompt(self, name: str, arguments: dict[str, Any] | None = None, context: Any = None) -> Any:
            context = self._ensure_context(context)
            token = _current_context.set(context)
            try:
                return await super().get_prompt(name, arguments, context)
            finally:
                _current_context.reset(token)

    FastMCP.__name__ = "FastMCP"
    FastMCP.__qualname__ = "FastMCP"
    FastMCP.__module__ = "mcp.server.fastmcp"
    FastMCP.__doc__ = "Compatibility alias for mcp.server.mcpserver.MCPServer (mcp 1.x API)."
    return FastMCP


def _alias_module(name: str, target: types.ModuleType) -> types.ModuleType:
    """Register a plain sys.modules alias for a 2.x submodule."""
    alias = types.ModuleType(name, f"Compatibility alias for {target.__name__}.")
    alias.__package__ = name.rpartition(".")[0]
    for key, value in vars(target).items():
        if not key.startswith("__"):
            setattr(alias, key, value)
    sys.modules[name] = alias
    return alias


def install() -> None:
    """Install the 1.x -> 2.x compatibility shim. Idempotent."""
    if is_installed():
        return

    try:
        mcpserver = importlib.import_module("mcp.server.mcpserver")
        server_pkg = importlib.import_module("mcp.server")
        exceptions = importlib.import_module("mcp.server.mcpserver.exceptions")
    except ModuleNotFoundError as exc:  # pragma: no cover - depends on environment
        raise RuntimeError(
            "mcp_fastmcp_compat_launcher requires mcp 2.x with "
            "'mcp.server.mcpserver' available; install/upgrade with "
            "`pip install 'mcp>=2'`."
        ) from exc

    FastMCP = _make_fastmcp_compat(mcpserver.MCPServer)

    # Root module: mcp.server.fastmcp
    root = types.ModuleType("mcp.server.fastmcp", "Compatibility shim for mcp.server.mcpserver (mcp 2.x).")
    root.__package__ = "mcp.server"
    root.__path__ = []  # so submodule imports resolve through sys.modules
    for key, value in vars(mcpserver).items():
        if not key.startswith("__"):
            setattr(root, key, value)
    root.FastMCP = FastMCP
    root.MCPServer = mcpserver.MCPServer  # let new code opt into the real class
    root.FastMCPError = exceptions.MCPServerError
    root.MCPServerError = exceptions.MCPServerError
    root.get_context = _get_context
    sys.modules[root.__name__] = root
    setattr(server_pkg, "fastmcp", root)

    # Submodule aliases. All of these lived under mcp.server.fastmcp in 1.x.
    # Direct sys.modules aliasing keeps exception/class identity intact.
    submodules = (
        "context",
        "exceptions",
        "prompts",
        "prompts.base",
        "resolve",
        "resources",
        "server",
        "tools",
        "utilities",
        "utilities.types",
    )
    for suffix in submodules:
        old = f"mcp.server.fastmcp.{suffix}"
        new = f"mcp.server.mcpserver.{suffix}"
        try:
            target = importlib.import_module(new)
        except ModuleNotFoundError:
            # Newer/older 2.x point releases may not have every submodule.
            continue
        alias = _alias_module(old, target)
        # Expose as attribute on the nearest compat parent.
        parent_name, _, attr = old.rpartition(".")
        parent = sys.modules.get(parent_name)
        if parent is not None:
            setattr(parent, attr, alias)

    # Exception module needs the 1.x base-class name as well. Equivalence of
    # ToolError/ResourceError is preserved because they are the same objects.
    compat_exceptions = sys.modules["mcp.server.fastmcp.exceptions"]
    compat_exceptions.FastMCPError = exceptions.MCPServerError

    # In 1.x, mcp.server.fastmcp.server held the FastMCP class itself.
    compat_server = sys.modules.get("mcp.server.fastmcp.server")
    if compat_server is not None:
        compat_server.FastMCP = FastMCP
        compat_server.MCPServer = mcpserver.MCPServer

    # Context.fastmcp -> Context.mcp_server. Context is a Pydantic model, but a
    # plain property on the class is safe (it is not a model field).
    context_cls = mcpserver.Context
    if not hasattr(context_cls, "fastmcp"):
        context_cls.fastmcp = property(  # type: ignore[attr-defined]
            lambda self: self.mcp_server,
            doc="Compatibility alias for Context.mcp_server (mcp 1.x API).",
        )

    setattr(server_pkg, _MARKER, True)


def _resolve_callable(module: types.ModuleType, dotted_name: str) -> Any:
    """Look up ``main`` or a dotted attribute like ``app.run``."""
    obj: Any = module
    for part in dotted_name.split("."):
        try:
            obj = getattr(obj, part)
        except AttributeError as exc:
            raise AttributeError(
                f"{module.__name__!r} has no callable {dotted_name!r} "
                f"(failed at {part!r})"
            ) from exc
    if not callable(obj):
        raise TypeError(f"{module.__name__}.{dotted_name} is not callable")
    return obj


def main(argv: list[str] | None = None) -> int:
    """Launch a 1.x MCP server with the shim pre-installed.

    Accepted forms::

        launcher.py <module> [callable] [args...]   # import module, call callable
        launcher.py -m <module> [args...]          # run module as __main__
        launcher.py <script.py> [args...]          # run script as __main__
    """
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0 if argv else 2

    install()

    # -- -m module (run as __main__) -------------------------------------
    if argv[0] == "-m":
        argv.pop(0)
        if not argv:
            print("error: -m requires a module name", file=sys.stderr)
            return 2
        target = argv.pop(0)
        sys.argv = [target, *argv]
        try:
            runpy.run_module(target, run_name="__main__", alter_sys=True)
        except KeyboardInterrupt:  # pragma: no cover - interactive
            return 130
        return 0

    target = argv[0]
    rest = argv[1:]

    # -- script path (run as __main__) -----------------------------------
    if target.endswith(".py") or os.path.isfile(target):
        sys.argv = [target, *rest]
        try:
            runpy.run_path(target, run_name="__main__")
        except KeyboardInterrupt:  # pragma: no cover - interactive
            return 130
        return 0

    # -- import module + call named function -----------------------------
    callable_name = rest[0] if rest else "main"
    call_args = rest[1:]
    sys.argv = [target, *call_args]
    try:
        module = importlib.import_module(target)
        fn = _resolve_callable(module, callable_name)
        result = fn(*call_args)
        if inspect.isawaitable(result):
            import anyio

            anyio.run(lambda: result)
    except KeyboardInterrupt:  # pragma: no cover - interactive
        return 130
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
