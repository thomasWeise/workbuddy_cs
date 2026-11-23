FROM ghcr.io/thomasweise/workbuddy_plain:v2026.11.23

USER root

ARG GITHUB_PROXY="https://ghproxy.net/"

RUN echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Beginning with first build step under root." &&\
    echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Making frontend non-interactive." &&\
    export DEBIAN_FRONTEND=noninteractive &&\
    echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Updating the package cache." &&\
    apt-get update &&\
    echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Now installing LaTeX and the requirements of Lean4." &&\
	apt-get install -y --fix-missing \
        biber \
        build-essential \
        cargo \
        clang \
        clangd \
        clang-format \
        clang-tidy \
        cmake \
        cppcheck \
        cpplint \
        curl \
        default-jdk-headless \
        default-jre-headless \
        gcc \
        gettext-base \
        ghostscript \
        gimp \
        git \
        gnuplot \
        imagemagick \
        inkscape \
        latex-cjk-all \
        latex-cjk-common \
        latex-cjk-chinese \
        libgmp-dev \
        libreoffice-core-nogui \
        libssl-dev \
        libuv1-dev \
        libxcb-dri3-0 \
        linux-headers-7.3.0-11-generic \
        maven \
        musl-dev \
        ocrmypdf \
        pkg-config \
        python3 \
        python3-dev \
        python3-pip \
        python3-venv \
        qpdf \
        rust-all \
        tesseract-ocr \
        tesseract-ocr-chi-sim \
        tesseract-ocr-deu \
        tesseract-ocr-eng \
        texlive-full \
        texlive-lang-chinese \
        texlive-lang-cjk \
        texlive-pictures \
        uncrustify \
        wget &&\
    echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Cleaning apt caches." &&\
    apt-get -y clean &&\
    echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Deleting useless cached files." &&\
	rm -rf /var/cache/apt/archives/ &&\
    echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Cleaning useless TeX Live files." &&\
    (rm -rf /usr/share/texmf/source || true) &&\
    (rm -rf /usr/share/texlive/texmf-dist/source || true) &&\
    find /usr/share/texlive -type f -name "readme*.*" -delete &&\
    find /usr/share/texlive -type f -name "README*.*" -delete &&\
    (rm -rf /usr/share/texlive/release-texlive.txt || true) &&\
    (rm -rf /usr/share/texlive/doc.html || true) &&\
    (rm -rf /usr/share/texlive/index.html || true) &&\
    echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Now updating fonts cache, because maybe new fonts came in with TeX Live." &&\
    fc-cache -fv &&\
    echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Printing TeX Life version." &&\
    tex --version &&\
    echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Printing Python version." &&\
    python3 --version &&\
    echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Cleaning up useless stuff." &&\
    rm -rf /usr/share/groff/* /usr/share/info/* &&\
    rm -rf /usr/share/lintian/* /usr/share/linda/* /var/cache/man/* &&\
    rm -rf /usr/share/man &&\
    mkdir -p /usr/share/man &&\
    find /usr/share/doc -depth -type f ! -name copyright -delete &&\
    find /usr/share/doc -type f -name "*.pdf" -delete &&\
    find /usr/share/doc -type f -name "*.gz" -delete &&\
    find /usr/share/doc -type f -name "*.tex" -delete &&\
    (find /usr/share/doc -type d -empty -delete || true) &&\
    mkdir -p /usr/share/doc &&\
    mkdir -p /usr/share/info &&\
    echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Finished first build step under 'root'."

USER user
ENV LEAN_VERSION="v4.37.0-rc1"

# We will use https://mirror.sjtu.edu.cn/elan/?mirror_intel_list.
RUN --mount=type=bind,source=resources/python-requirements.txt,target=/tmp/requirements.txt \
    --mount=type=bind,source=resources/python-mcp.txt,target=/tmp/mcp.txt \
    echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Beginning second build step as 'user'." &&\
    echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Making frontend non-interactive." &&\
    export DEBIAN_FRONTEND=noninteractive &&\
    echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Entering temp directory." &&\
    cd "/tmp/" &&\
    echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Now downloading Glean4 from SJTU mirror." &&\
    curl -L "https://s3.jcloud.sjtu.edu.cn/899a892efef34b1b944a19981040f55b-oss01/elan/glean/releases/download/v0.1.19/glean_Linux_x86_64.tar.gz" -o /tmp/glean.tar.gz &&\
    echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Now unpacking glean." &&\
    tar -xf glean.tar.gz &&\
    echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Now updating glean." &&\
    ./glean -update &&\
    echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Now installing elan." &&\
    ./glean -install elan -version v4.2.4 &&\
    echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Updating 'PATH'." &&\
    export PATH="${HOME}/.elan/bin:${PATH}" &&\
    echo "$(date +'%0Y-%0m-%0d %0R:%0S'): PATH is now '$PATH'." &&\
    echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Now updating elan." &&\
    elan self update &&\
    echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Now installing elan toolchain." &&\
    elan toolchain install "${LEAN_VERSION}" &&\
    echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Now setting default tool chain." &&\
    elan default "${LEAN_VERSION}" &&\
    echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Printing versions." &&\
    lean --version &&\
    lake --version &&\
    echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Entering user's home directory." &&\
    cd "/home/user" &&\
    echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Downloading mathlib4 from a domestic git mirror." &&\
    #git clone "https://gitcode.com/GitHub_Trending/ma/mathlib4" &&\
    git clone "${GITHUB_PROXY}https://github.com/leanprover-community/mathlib4" &&\
    cd mathlib4 &&\
    echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Loading cached mathlib4." &&\
    lake exe cache get &&\
    echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Building mathlib4." &&\
    lake build &&\
    echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Done with lean/elan/lake, now doing python; first going to /tmp/." &&\
    cd "/tmp/" &&\
    echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Creating virtual environment directory." &&\
    export venvDir="/home/user/venv" &&\
    mkdir -p "$venvDir" &&\
    echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Setting up virtual environment." &&\
    python3 -m venv --upgrade-deps --symlinks "$venvDir" &&\
    echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Activating virtual environment." &&\
    . "$venvDir/bin/activate" &&\
    echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Installing pip Packages." &&\
    python3 -m pip install --no-input --default-timeout=300 --timeout=300 --retries=100 -r /tmp/requirements.txt &&\
    echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Installing MCP Packages: Resolving Github Proxy." &&\
    envsubst < /tmp/mcp.txt > /tmp/mcp_resolved.txt &&\
    echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Now installing MCP Packages." &&\
    python3 -m pip install --no-input --default-timeout=300 --timeout=300 --retries=100 -r /tmp/mcp_resolved.txt &&\
    echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Now handling MCP-LaTeX-Server directly. First entering site-packages." &&\
    cd /home/user/venv/lib/python3.14/site-packages &&\
    echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Now cloning the server." &&\
    git clone "${GITHUB_PROXY}https://github.com/RobertoDure/mcp-latex-server.git" &&\
    echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Now installing it directly." &&\
    mv mcp-latex-server latex_server &&\
    pip install -e ./latex_server &&\
    echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Deactivating virtual environment." &&\
    deactivate &&\
    echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Ensuring that .workbuddy exists." &&\
    mkdir -p "/home/user/.workbuddy" &&\
    echo "$(date +'%0Y-%0m-%0d %0R:%0S'): Now purging everything." &&\
    rm -rf "/tmp/*" &&\
    echo "$(date +'%0Y-%0m-%0d %0R:%0S'): All is done, we built the image workbuddy_cs."

# Updating path
ENV PATH="/home/user/.elan/bin:/home/user/mathlib4:/home/user/.local/bin:/home/user/venv/bin:${PATH}"
# Permanently activating virtual environment with all installed python packages
ENV VIRTUAL_ENV="/home/user/venv"

# Setting up the MCP files.
COPY --chown=user resources/mcp.json "/home/user/.workbuddy/mcp.json"
COPY --chown=user resources/mcp_fastmcp_compat_launcher.py "/home/user/mcp_fastmcp_compat_launcher.py"
