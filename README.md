# A WorkBuddy Docker image for Computer Science work.

## 1. Introduction
This is a [Docker](https://www.docker.com) image of the [WorkBuddy](https://www.workbuddy.cn) agent with many packages for computer science works installed.
It is based on an [Ubuntu](https://ubuntu.com) [Linux](https://thomasweise.github.io/tags/linux) image.
It is intended for use in particular with [rootless Docker](https://thomasweise.github.io/posts/2026-11-17-installing-rootless-docker-on-ubuntu-in-china) installations.
You can find the image at [`ghcr.io/thomasweise/workbuddy_cs`](https://github.com/thomasWeise/workbuddy_cs/pkgs/container/workbuddy_cs).

The image uses Chinese domestic mirrors where possible, so that you can both build and run it in China.

The image comes with many tools:

- [Lean](https://lean-lang.org) with a cached [mathlib4](https://github.com/leanprover-community/mathlib4),
- the [GNU Compiler Collection](https://gcc.gnu.org) and [clang](https://clang.llvm.org), to enable `C` and `C++` programming, together with the linters [clang-format](https://clang.llvm.org/docs/ClangFormatStyleOptions.html), [clang-tidy](https://clang.llvm.org/extra/clang-tidy), [cppcheck](https://cppcheck.sourceforge.io), [cpplint](https://github.com/cpplint/cpplint), and [uncrustify](https://github.com/uncrustify/uncrustify),
- the [Rust Programming Language](https://rust-lang.org),
- [Python&nbsp;3](https://thomasweise.github.io/programmingWithPython) with a virtual environment `/home/user/venv` hosting many pre-installed packages, such as
  - packages for numeric computation: [numpy](https://pypi.org/project/numpy), [numba](https://pypi.org/project/numba), [mpmath](https://pypi.org/project/mpmath), [intel-cmplr-lib-rt](https://pypi.org/project/intel-cmplr-lib-rt),
  - packages for visualization: [matplotlib](https://pypi.org/project/matplotlib), [seaborn](https://pypi.org/project/seaborn),
  - packages for machine learning, statistics, testing, symbolic computation, optimization algorithms: [scipy](https://pypi.org/project/scipy), [scikit-learn](https://pypi.org/project/scikit-learn), [scikit-image](https://pypi.org/project/scikit-image), [xgboost](https://pypi.org/project/xgboost), [sympy](https://pypi.org/project/sympy), [cmaes](https://pypi.org/project/cmaes),
  - packages for AI, neural networks: [tensorflow-cpu](https://pypi.org/project/tensorflow-cpu),
  - packages for data loading: [defusedxml](https://pypi.org/project/defusedxml), [pandas](https://pypi.org/project/pandas), [openpyxl](https://pypi.org/project/openpyxl), [odfpy](https://pypi.org/project/odfpy), [polars](https://pypi.org/project/polars),
  - packages for network access: [urllib3](https://pypi.org/project/urllib3), [certifi](https://pypi.org/project/certifi),
  - packages for software development, such as linters, type checkers: [autoflake](https://pypi.org/project/autoflake), [bandit](https://pypi.org/project/bandit), [dlint](https://pypi.org/project/dlint), [dodgy](https://pypi.org/project/dodgy), [flake8](https://pypi.org/project/flake8), [flake8-2020](https://pypi.org/project/flake8-2020), [flake8-absolute-import](https://pypi.org/project/flake8-absolute-import), [flake8-bugbear](https://pypi.org/project/flake8-bugbear), [flake8-builtins](https://pypi.org/project/flake8-builtins), [flake8-commas](https://pypi.org/project/flake8-commas), [flake8-comprehensions](https://pypi.org/project/flake8-comprehensions), [flake8-docstrings](https://pypi.org/project/flake8-docstrings), [flake8-eradicate](https://pypi.org/project/flake8-eradicate), [flake8-length](https://pypi.org/project/flake8-length), [flake8-mutable](https://pypi.org/project/flake8-mutable), [flake8-pyi](https://pypi.org/project/flake8-pyi), [flake8-pytest-style](https://pypi.org/project/flake8-pytest-style), [flake8-use-fstring](https://pypi.org/project/flake8-use-fstring), [mypy](https://pypi.org/project/mypy), [pycodestyle](https://pypi.org/project/pycodestyle), [pydocstyle](https://pypi.org/project/pydocstyle), [pyflakes](https://pypi.org/project/pyflakes), [pylint](https://pypi.org/project/pylint), [pyrefly](https://pypi.org/project/pyrefly), [pyroma](https://pypi.org/project/pyroma), [ruff](https://pypi.org/project/ruff), [tryceratops](https://pypi.org/project/tryceratops), [vulture](https://pypi.org/project/vulture),
  - documentation generation: [sphinx](https://pypi.org/project/sphinx), [sphinx-autodoc-typehints](https://pypi.org/project/sphinx-autodoc-typehints), [pygments](https://pypi.org/project/pygments), [myst-parser](https://pypi.org/project/myst-parser), [markdown](https://pypi.org/project/markdown), [minify_html](https://pypi.org/project/minify_html),
  - testing: [coverage](https://pypi.org/project/coverage), [pytest](https://pypi.org/project/pytest), [pytest-timeout](https://pypi.org/project/pytest-timeout),
  - package, setup, and deployment tools: [setuptools](https://pypi.org/project/setuptools), [testresources](https://pypi.org/project/testresources), [twine](https://pypi.org/project/twine), [virtualenv](https://pypi.org/project/virtualenv), [wheel](https://pypi.org/project/wheel), [psutil](https://pypi.org/project/psutil), and
  - our own packages: [pycommons](https://pypi.org/project/pycommons), [moptipy](https://pypi.org/project/moptipy), [moptipyapps](https://pypi.org/project/moptipyapps).
- a full [TeX Live](https://tug.org/texlive) installation,
- a full [LibreOffice](https://www.libreoffice.org) installation,
- an [Inkscape](https://inkscape.org) installation for vector graphics editing, and
- [GIMP](https://www.gimp.org) and [ImageMagick](https://imagemagick.org) for pixel image processing,
- [tesseract-ocr](https://tesseractocr.org) and [ocrmypdf](https://github.com/ocrmypdf/OCRmyPDF) for performing image-to-text actions. 


This should enable you to do lots of things out of the box.


**Notice:** I am totally new to using AI tools.
Therefore, this is really a very very experimental setup.
I cannot guarantee that it will work.


## 2. Run the Image
You can either run this image via the provided script or manually.
Either way, the WorkBuddy login window will pop up.
It would provide you with a link to copy into your browser.
Then, you can authenticate/login via your browser.
After that, WorkBuddy can be used.


### 2.1. Run it via provided Script
Under Ubuntu Linux, you can run it with script [`workbuddy_cs_run.sh`](https://thomasweise.github.io/workbuddy_cs/workbuddy_cs_run.sh).
This script will take three optional parameters:

- The directory to mount into WorkBuddy, by default `"."`
- The version of the image to run, by default `"latest"`
- The mode of the image to use.
  By default, this uses the image [`ghcr.io/thomasweise/workbuddy_cs`](https://github.com/thomasWeise/workbuddy_cs/pkgs/container/workbuddy_cs) from the GitHub package repository.
  If you set this to `"local"`, then you can also run a Docker image that you built locally using, e.g., the scripts [`workbuddy_cs_build.sh`](https://thomasweise.github.io/workbuddy_cs/workbuddy_cs_build.sh) and our [`Dockerfile.sh`](https://thomasweise.github.io/workbuddy_cs/Dockerfile).


## 2.2. Run it by Hand from the Shell
Alternatively, you can run the image by hand.

Notice that in order to run the image properly, you need to first set `xhost +local:docker` on your system.
This is needed so that WorkBuddy can access your screen.
You would do something like

```bash
xhost +local:docker

docker run -it --rm \
  --name workbuddy \
  --network host \
  --cap-add SYS_ADMIN \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v /path/to/folder/you/want/to/mount/into/image:/home/user/workbuddy-data \
  "ghcr.io/thomasweise/workbuddy_cs:latest"
```


## 3. License
Copyright (C) 2026  [Thomas Weise](https://thomasweise.github.io) (汤卫思教授)

Dr. [Thomas Weise](https://thomasweise.github.io) (see [Contact](#12-contact)) holds the copyright of these scripts.
The scripts are provided to the public as open source software under the [GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007](https://thomasweise.github.io/moptipy/LICENSE.html).

**This license only here applies to the scripts in this package.
It obviously does NOT apply to the WorkBuddy software, Docker itself, or anything else contained in the Docker images.
These are obviously under the copyright of their copyright holders.**

All scripts here are free software: you can redistribute them and/or modify them under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
All scripts and programs here are distributed in the hope that they will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with them.
If not, see <https://www.gnu.org/licenses/>.

**If you feel that this repository or image infringes any of your property rights, please contact me.**


## 4. Contact
If you have any questions or suggestions, please contact
Prof. Dr. [Thomas Weise](https://thomasweise.github.io) (汤卫思教授) of the 
School of Artificial Intelligence and Big Data ([人工智能与大数据学院](http://www.hfuu.edu.cn/aibd)) at
[Hefei University](http://www.hfuu.edu.cn/english) ([合肥大学](http://www.hfuu.edu.cn)) in
Hefei, Anhui, China (中国安徽省合肥市) via
email to [tweise@hfuu.edu.cn](mailto:tweise@hfuu.edu.cn) with CC to [tweise@ustc.edu.cn](mailto:tweise@ustc.edu.cn).
