[![https://thomasweise.github.io](https://shields.io/badge/home-thomasweise.github.io-009000)](https://thomasweise.github.io)

# A WorkBuddy Docker image for Computer Science work.

## 1. Introduction
This is a [Docker](https://www.docker.com) image of the [WorkBuddy](https://www.workbuddy.cn) agent with many packages for computer science works installed.
It is intended as a pipeline for using AI for computer science research.
For example, we can use [Lean](https://lean-lang.org) for mathematical proofs,
[TeX Live](https://tug.org/texlive) for writing papers in LaTeX, and
[Python&nbsp;3](https://thomasweise.github.io/programmingWithPython) with many scientific packages pre-installed for experiments.

The image is based on our [plain WorkBuddy image](https://thomasweise.github.io/workbuddy_plain).
It is intended for use in particular with [rootless Docker](https://thomasweise.github.io/posts/2026-11-17-installing-rootless-docker-on-ubuntu-in-china) installations.
You can find the image at [`ghcr.io/thomasweise/workbuddy_cs`](https://github.com/thomasWeise/workbuddy_cs/pkgs/container/workbuddy_cs).

WorkBuddy normally runs in a Chrome Sandbox. 
However, here we put it *additionally* into a Docker container.
So it runs in a sandbox inside a container.
This has the two advantages that we are *(a)*&nbsp;less likely to make errors that could mess up with our local data or systems configuration and *(b)*&nbsp;can have consistent installations of several tools directly contained in the image.
(We did have to weaken the inner sandbox in some places to make it work, as explained in the [`workbuddy_plain` documentation](https://thomasweise.github.io/workbuddy_plain), though, so this weakens point *(a)* a bit&hellip;)

**Notice:** I am totally new to using AI tools.
Therefore, this is really a very very experimental setup.
I cannot guarantee that it will work.


## 2. Additional Tools Provided by this Image
This image here uses Chinese domestic mirrors where possible, so that you can both build and run it in China.
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
- Java [OpenJDK](https://openjdk.org) and [Maven](https://maven.apache.org) for Java development,
- a full [TeX Live](https://tug.org/texlive) installation,
- a full [LibreOffice](https://www.libreoffice.org) installation,
- an [Inkscape](https://inkscape.org) installation for vector graphics editing, and
- [GIMP](https://www.gimp.org) and [ImageMagick](https://imagemagick.org) for pixel image processing,
- [tesseract-ocr](https://tesseractocr.org) and [ocrmypdf](https://github.com/ocrmypdf/OCRmyPDF) for performing image-to-text actions,
- [git](https://git-scm.com), [curl](https://curl.se), and [wget](https://www.gnu.org/software/wget) for downloading data. 


Additionally, we have pre-configured several Python-based MCP actions:

- [lean-mcp](https://pypi.org/project/lean-mcp) for working with Lean4 + Mathlib,
- [latex-server](https://github.com/RobertoDure/mcp-latex-server) for TeX&nbsp;Live interaction,
- [clangd-mcp](https://github.com/ibuildrun/clangd-mcp) for C/C++ coding,
- [jvm-mcp-server](https://pypi.org/project/jvm-mcp-server) for analyzing Java projects,
- [maven-decoder-mcp](https://pypi.org/project/maven-decoder-mcp) for Maven interaction, and
- [mcp-server-git](https://pypi.org/project/mcp-server-git) for interactions with git.

This should enable you to do lots of things out of the box.


## 3. Run the Image
You can either run this image via the provided script or manually.
Either way, after starting the container, you can log in as described in [Section&nbsp;4.1](#41-logging-in).
After that, you can use WorkBuddy as discussed in [Section&nbsp;4.2](#42-using-workbuddy).

**Connection Issues:**
If your internet connection is unstable, it may take a few attempts to download the image.
The image is not small.
This download issue only occurs during the first launch of the image&nbsp;(or if you update it later on).
If you experience connection issues, you can combine the [script-based execution](#31-run-it-via-provided-script) with our [`tryForever.sh`](https://thomasweise.github.io/posts/2026-03-09-repeating-until-success-linux) shell script.


### 3.1. Run it via provided Script
Under Ubuntu Linux, you can run the container with script [`workbuddy_cs_run.sh`](https://thomasweise.github.io/workbuddy_cs/workbuddy_cs_run.sh).
This script will take three optional parameters:

- The directory to mount into WorkBuddy, by default `"/tmp/workbuddy"`.
  This folder will be created if it does not exist.
  You can point this to some folder with data in it that you want to share.
  The default setting just uses a temporary folder, where nothing important should be in.
  This directory should have reading and writing permissions for the container.
  The easiest way to do this is to `chmod 777 directory`.
  The files created by WorkBuddy will have read permissions for you only, so you can tell it to give all files read/write permissions for everyone.
- The version of the image to run, by default `"latest"`
- The mode of the image to use.
  By default, this uses the image [`ghcr.io/thomasweise/workbuddy_cs`](https://github.com/thomasWeise/workbuddy_cs/pkgs/container/workbuddy_cs) from the GitHub package repository.
  If you set this to `"local"`, then you can also run a Docker image that you built locally using, e.g., the scripts [`workbuddy_cs_build.sh`](https://thomasweise.github.io/workbuddy_cs/workbuddy_cs_build.sh) and our [`Dockerfile.sh`](https://thomasweise.github.io/workbuddy_cs/Dockerfile).


## 3.2. Run it by Hand from the Shell
Alternatively, you can run the image by hand.
This will also download the image if it is not downloaded yet.

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
  --add-host=update.codebuddy.cn:127.0.0.1 \
  --add-host=update.workbuddy.cn:127.0.0.1 \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v /path/to/folder/you/want/to/mount/into/image:/home/user/workbuddy-data \
  "ghcr.io/thomasweise/workbuddy_cs:latest"
```


## 4. Usage
After you have started the container as described above, a WorkBuddy window will pop up.

### 4.1. Logging In
When you start the container, you first need to log in.
For this, you should ideally have a [WeChat](https://www.wechat.com/en) account.

<figure>
<img src="https://thomasweise.github.io/workbuddy_plain/images/workbuddy_sign_in_1.png" style="width:80%;border:2px solid black;border-radius:8px" alt='The log in window appears. You click "Sign in" in the login screen.' />
<figcaption>The log in window appears. You click "Sign in" in the login screen.</figcaption>
</figure>

<figure>
<img src="https://thomasweise.github.io/workbuddy_plain/images/workbuddy_sign_in_2.png" style="width:80%;border:2px solid black;border-radius:8px" alt="After the click, it may take a second until the container-internal browser pops up." />
<figcaption>After the click, it may take a second until the container-internal browser pops up.</figcaption>
</figure>

<figure>
<img src="https://thomasweise.github.io/workbuddy_plain/images/workbuddy_sign_in_3.png" style="width:80%;border:2px solid black;border-radius:8px" alt=">It shows you a WeChat confirmation QR-code&nbsp;(here blotted out by the gray rectangle)." />
<figcaption>It shows you a <a href="https://www.wechat.com/en">WeChat</a> confirmation QR-code&nbsp;(here blotted out by the gray rectangle).</figcaption>
</figure>

<figure>
<img src="https://thomasweise.github.io/workbuddy_plain/images/workbuddy_sign_in_4.png" style="width:80%;border:2px solid black;border-radius:8px" alt="Using WeChat on your phone, you scan this QR code&hellip;" />
<figcaption>Using <a href="https://www.wechat.com/en">WeChat</a> on your phone, you scan this QR code&hellip;</figcaption>
</figure>

<figure>
<img src="https://thomasweise.github.io/workbuddy_plain/images/workbuddy_sign_in_5.png" style="width:80%;border:2px solid black;border-radius:8px" alt="&hellip;and allow it to use your information." />
<figcaption>&hellip;and allow it to use your information.</figcaption>
</figure>

<figure>
<img src="https://thomasweise.github.io/workbuddy_plain/images/workbuddy_sign_in_6.png" style="width:80%;border:2px solid black;border-radius:8px" alt="The browser will change to a confirmation. After the browser content has changed, you can close it." />
<figcaption>The browser will change to a confirmation. After the browser content has changed, you can close it.</figcaption>
</figure>

<figure>
<img src="https://thomasweise.github.io/workbuddy_plain/images/workbuddy_sign_in_7.png" style="width:80%;border:2px solid black;border-radius:8px" alt="You are now logged into WorkBuddy." />
<figcaption>You are now logged into WorkBuddy.</figcaption>
</figure>


### 4.2. Using WorkBuddy
Now you can now use WorkBuddy.

<figure>
<img src="https://thomasweise.github.io/workbuddy_plain/images/workbuddy_example_1.png" style="width:80%;border:2px solid black;border-radius:8px" alt="Here I instruct WorkBuddy to create a simple Python file, run it, store its output in the mounted folder, and set all permissions to the generated files so that I can edit them."/>
<figcaption>Here I instruct WorkBuddy to create a simple Python file, run it, store its output in the mounted folder, and set all permissions to the generated files so that I can edit them.</figcaption>
</figure>

<figure>
<img src="https://thomasweise.github.io/workbuddy_plain/images/workbuddy_example_2.png" style="width:80%;border:2px solid black;border-radius:8px" alt="WorkBuddy begins to work." />
<figcaption>WorkBuddy begins to work.</figcaption>
</figure>

<figure>
<img src="https://thomasweise.github.io/workbuddy_plain/images/workbuddy_example_3.png" style="width:80%;border:2px solid black;border-radius:8px" alt="It shows me the contents of the file it created." />
<figcaption>It shows me the contents of the file it created.</figcaption>
</figure>

<figure>
<img src="https://thomasweise.github.io/workbuddy_plain/images/workbuddy_example_4.png" style="width:80%;border:2px solid black;border-radius:8px" alt="And it explains what it did." />
<figcaption>And it explains what it did.</figcaption>
</figure>

<figure>
<img src="https://thomasweise.github.io/workbuddy_plain/images/workbuddy_example_5.png" style="width:80%;border:2px solid black;border-radius:8px" alt="And the files appear indeed in the mounted folder." />
<figcaption>And the files appear indeed in the mounted folder.</figcaption>
</figure>


### 4.3. Using the Computer Science Tool Chain
Now let's do a more advanced example.
We will ask WorkBuddy to prove that `1+x <= exp(x)` for all real-valued `x`.
We will ask it to draw the two functions into a diagram next to each other.
We will ask it put all the proof, description, maths, artifacts, and plots into one LaTeX document and compile it to PDF.

<figure>
<img src="https://thomasweise.github.io/workbuddy_cs/images/workbuddy_cs_example_01.png" style="width:80%;border:2px solid black;border-radius:8px" alt="We tell WorkBuddy to store all the artifacts into the folder that we mounted into its container. Then we give it the task to do the proof. For this, we advise it to use Lean, which is pre-installed in the image." />
<figcaption>We tell WorkBuddy to store all the artifacts into the folder that we mounted into its container. Then we give it the task to do the proof. For this, we advise it to use [Lean](https://lean-lang.org), which is pre-installed in the image.</figcaption>
</figure>

<figure>
<img src="https://thomasweise.github.io/workbuddy_cs/images/workbuddy_cs_example_02.png" style="width:80%;border:2px solid black;border-radius:8px" alt="WorkBuddy does this quickly. The text on the right-hand side is the Lean output, telling us that everything is OK." />
<figcaption>WorkBuddy does this quickly. The text on the right-hand side is the Lean output, telling us that everything is OK. The Lean proof is in file <a href="https://thomasweise.github.io/workbuddy_cs/images/proof.lean">proof.lean</a>.</figcaption>
</figure>

<figure>
<img src="https://thomasweise.github.io/workbuddy_cs/images/workbuddy_cs_example_03.png" style="width:80%;border:2px solid black;border-radius:8px" alt="It has created both files." />
<figcaption>It has created both files.</figcaption>
</figure>

<figure>
<img src="https://thomasweise.github.io/workbuddy_cs/images/workbuddy_cs_example_04.png" style="width:80%;border:2px solid black;border-radius:8px" alt="I can see both files in the mounted folder." />
<figcaption>I can see both files in the mounted folder.</figcaption>
</figure>

<figure>
<img src="https://thomasweise.github.io/workbuddy_cs/images/workbuddy_cs_example_05.png" style="width:80%;border:2px solid black;border-radius:8px" alt="This is the content of the Lean file." />
<figcaption>This is the content of the Lean file The Lean proof is in file <a href="https://thomasweise.github.io/workbuddy_cs/images/proof.lean">proof.lean</a>..</figcaption>
</figure>

<figure>
<img src="https://thomasweise.github.io/workbuddy_cs/images/workbuddy_cs_example_06.png" style="width:80%;border:2px solid black;border-radius:8px" alt="And here we have the output of the proof checker." />
<figcaption>And here we have the output of the proof checker in file <a href="https://thomasweise.github.io/workbuddy_cs/images/proof_results.txt">proof_results.txt</a>.</figcaption>
</figure>

<figure>
<img src="https://thomasweise.github.io/workbuddy_cs/images/workbuddy_cs_example_07.png" style="width:80%;border:2px solid black;border-radius:8px" alt="Now I instruct WorkBuddy to create a Python program plotting the two functions into one diagram. The diagram is to be stored as PDF file." />
<figcaption>Now I instruct WorkBuddy to create a Python program plotting the two functions into one diagram. The diagram is to be stored as PDF file.</figcaption>
</figure>

<figure>
<img src="https://thomasweise.github.io/workbuddy_cs/images/workbuddy_cs_example_08.png" style="width:80%;border:2px solid black;border-radius:8px" alt="It completes the task and also presents me with the diagram." />
<figcaption>It completes the task and also presents me with the <a href="https://thomasweise.github.io/workbuddy_cs/images/plot.pdf">diagram</a>.</figcaption>
</figure>

<figure>
<img src="https://thomasweise.github.io/workbuddy_cs/images/workbuddy_cs_example_09.png" style="width:80%;border:2px solid black;border-radius:8px" alt="" />
<figcaption>Both the <a href="https://thomasweise.github.io/workbuddy_cs/images/plot.py">Python script</a> and the <a href="https://thomasweise.github.io/workbuddy_cs/images/plot.pdf">PDF</a> it generates appear inside the mounted folder.</figcaption>
</figure>

<figure>
<img src="https://thomasweise.github.io/workbuddy_cs/images/workbuddy_cs_example_10.png" style="width:80%;border:2px solid black;border-radius:8px" alt="The Python script looks quite reasonable." />
<figcaption>The <a href="https://thomasweise.github.io/workbuddy_cs/images/plot.py">Python script</a> looks quite reasonable.</figcaption>
</figure>

<figure>
<img src="https://thomasweise.github.io/workbuddy_cs/images/workbuddy_cs_example_11.png" style="width:80%;border:2px solid black;border-radius:8px" alt="Now I ask WorkBuddy to write a summary document in LaTeX. I instruct it to include and explain everything that was done and to compile the LaTeX to PDF." />
<figcaption>Now I ask WorkBuddy to write a summary document in LaTeX. I instruct it to include and explain everything that was done and to compile the LaTeX to PDF.</figcaption>
</figure>

<figure>
<img src="https://thomasweise.github.io/workbuddy_cs/images/workbuddy_cs_example_12.png" style="width:80%;border:2px solid black;border-radius:8px" alt="It even realizes the limitations of some LaTeX packages&hellip;" />
<figcaption>It even realizes the limitations of some LaTeX packages&hellip;</figcaption>
</figure>

<figure>
<img src="https://thomasweise.github.io/workbuddy_cs/images/workbuddy_cs_example_13.png" style="width:80%;border:2px solid black;border-radius:8px" alt="It creates the LaTeX document and presents me with the compiled result." />
<figcaption>It creates the <a href="https://thomasweise.github.io/workbuddy_cs/images/summary.tex">LaTeX document</a> and presents me with the <a href="https://thomasweise.github.io/workbuddy_cs/summary.pdf">compiled result</a>.</figcaption>
</figure>

<figure>
<img src="https://thomasweise.github.io/workbuddy_cs/images/workbuddy_cs_example_14.png" style="width:80%;border:2px solid black;border-radius:8px" alt="Here are all the files that were generated during this session." />
<figcaption>Here are all the files that were generated during this session.</figcaption>
</figure>

<figure>
<img src="https://thomasweise.github.io/workbuddy_cs/images/workbuddy_cs_example_15.png" style="width:80%;border:2px solid black;border-radius:8px" alt="This is the front page of the generated document." />
<figcaption>This is the front page of the <a href="https://thomasweise.github.io/workbuddy_cs/summary.pdf">generated document</a>.</figcaption>
</figure>

<figure>
<img src="https://thomasweise.github.io/workbuddy_cs/images/workbuddy_cs_example_16.png" style="width:80%;border:2px solid black;border-radius:8px" alt="A part of page 2 of the generated document." />
<figcaption>A part of page 2 of the <a href="https://thomasweise.github.io/workbuddy_cs/summary.pdf">generated document</a>.</figcaption>
</figure>

<figure>
<img src="https://thomasweise.github.io/workbuddy_cs/images/workbuddy_cs_example_17.png" style="width:80%;border:2px solid black;border-radius:8px" alt="A part of pages 2 and 3 of the generated document." />
<figcaption>A part of page 2 and 3 of the <a href="https://thomasweise.github.io/workbuddy_cs/summary.pdf">generated document</a>.</figcaption>
</figure>

<figure>
<img src="https://thomasweise.github.io/workbuddy_cs/images/workbuddy_cs_example_18.png" style="width:80%;border:2px solid black;border-radius:8px" alt="A part of page 3 of the generated document." />
<figcaption>A part of page 3 of the <a href="https://thomasweise.github.io/workbuddy_cs/summary.pdf">generated document</a>.</figcaption>
</figure>

<figure>
<img src="https://thomasweise.github.io/workbuddy_cs/images/workbuddy_cs_example_19.png" style="width:80%;border:2px solid black;border-radius:8px" alt="The last page of the generated document." />
<figcaption>The last page of the <a href="https://thomasweise.github.io/workbuddy_cs/summary.pdf">generated document</a>.</figcaption>
</figure>

During the course of the example, WorkBuddy created the following files:

- [proof.lean](https://thomasweise.github.io/workbuddy_cs/images/proof.lean)
- [proof_results.txt](https://thomasweise.github.io/workbuddy_cs/images/proof_results.txt)
- [plot.py](https://thomasweise.github.io/workbuddy_cs/images/plot.py)
- [plot.pdf](https://thomasweise.github.io/workbuddy_cs/images/plot.pdf)
- [summary.tex](https://thomasweise.github.io/workbuddy_cs/images/summary.tex)
- [summary.pdf](https://thomasweise.github.io/workbuddy_cs/images/summary.pdf)

If you read [summary.pdf](https://thomasweise.github.io/workbuddy_cs/images/summary.pdf), you will find that the proof that it created does make sense.
All the files are of surprisingly high quality.


## 5. License
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


## 6. Contact
If you have any questions or suggestions, please contact
Prof. Dr. [Thomas Weise](https://thomasweise.github.io) (汤卫思教授) of the 
School of Artificial Intelligence and Big Data ([人工智能与大数据学院](http://www.hfuu.edu.cn/aibd)) at
[Hefei University](http://www.hfuu.edu.cn/english) ([合肥大学](http://www.hfuu.edu.cn)) in
Hefei, Anhui, China (中国安徽省合肥市) via
email to [tweise@hfuu.edu.cn](mailto:tweise@hfuu.edu.cn) with CC to [tweise@ustc.edu.cn](mailto:tweise@ustc.edu.cn).
