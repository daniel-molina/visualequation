# visualequation

Visualequation creates equations visually, in a WYSIWYG (What You See Is What You Get) style. Equations can be exported to PNG, EPS, PDF and SVG. PNG and SVG are transparent. If you want a background you can put a white (or whatever color) colorbox to the whole equation in the editor before exporting. You can recover equations from previously created images in PNG and PDF format and continue editing them!

## Requirements

### Debian 9.0 and Ubuntu 18.04 or derivatives

$ sudo apt-get install python3-pyqt5 texlive-latex-recommended dvipng texlive-font-utils texlive-science libimage-exiftool-perl

### Ubuntu 14.04 and 16.04 or derivatives

$ sudo apt-get install python3-pyqt5 texlive-latex-recommended dvipng texlive-font-utils texlive-math-extra libimage-exiftool-perl

### Microsoft Windows and MacOS

By the moment it has only been tested on GNU/Linux. But it would be interesting to have installation instructions for the dependencies on other operative systems. Volunteers needed!

To run the program successfully, you need:

* python3
* PyQt5
* LaTeX
* Some specific LaTeX packages (you can find them in the preamble of the equation template _visualequation/data/eq_template.tex_).
* Some command-line programs to manipulate LaTeX output (some of them probably come with your LaTeX distribution):
  * dvipng
  * dvips
  * dvisvgm
  * epstopdf
* exiftool
  
## Checking that dependencies are fulfilled

If you have the sources you can see if everything is installed properly running the test:

$ python3 -m tests.test_dependencies

## Installation

I did not package visualequation for any distribution yet. In the case of python, installing software with pip and related tools is almost a standard so I decided to use it first. If you know how to manage pip in your system, perfect, follow your way to install visualequation from source (development version) or PyPI (released versions). If you have no clue and want me to explain all the details about how to install it, I feel that I have certain responsability of telling you something that works. If you use a modern distribution like Debian 9.0 or Ubuntu 18.04/16.04 it worked for me using the tools of the distribution, else, read the next section on how to install a current version of pip.

### Installing pip from your distribution (Debian/Ubuntu case)

If you want to install from sources and you want to use the provided packages by your distribution, do the following (if you are just going to install from PyPI you only need python3-pip)

$ sudo apt-get install python3-pip python3-setuptools python3-wheel

Continue the instructions in "Installing visualequation using pip".

### Installing current version of pip (recommended for old distributions)

I will show here a recipe to install pip in your home directory. It may be necessary because the version that comes in some distributions (like Ubuntu 14.04) does not work totally for the instructions I will give later. Said that, if you want further lecture on the topic, I leave [this well-written link](http://matthew-brett.github.io/pydagogue/installing_on_debian.html).

If you are going to install from sources, I recommend you to remove the package setuptools (if it is installed) of your distribution; else, pip will refuse to install the last version

$ sudo apt-get remove python3-setuptools

Download pip, e.g.:

$ curl -LO https://bootstrap.pypa.io/get-pip.py

Install it locally

$ python3 get-pip.py --user

Now you should be able to run

$ python3 -m pip --version

should give the same valid output (the current last version of pip).

### Installing visualequation

The simplest way is to use the last packaged version of visualequation in PyPI. To download and install, just do the following

$ python3 -m pip install --user --upgrade visualequation

That is all.

On the other hand, if you want to install the development version, follow the next instructions. First, get the sources

$ git clone https://github.com/daniel-molina/visualequation.git

$ cd visualequation

You must first generate the icons (you will need imagemagick, but probably it will be currently installed)

$ python3 setup.py build

Generating the package:

$ python3 setup.py bdist_wheel

After that, you can install the package by

$ cd dist

$ python3 -m pip install --user visualequation-\<version\>-py3-none-any.whl

where you substitute \<version\> by the version number of the file generated in dist/.

## Running visualequation

Add the directory where visualequation is installed to your path. You can do it by writting at the end of your .bashrc the following line

PATH=${PATH}:${HOME}/.local/bin

If you want this change to take effect in the current terminal, run

$ source ~/.bashrc

To execute the program, just run

$ visualequation 

in whatever current directory.

## Usage/Instructions

See Help->'Basic Usage' or read the file visualequation/data/USAGE.html

## Known Issues

* Conversion to SVG fails when the equation contains a Text. The application will wait forever while converting, so the user has to force the exit of the execution.
  * Affected environments: Ubuntu Xenial (16.04) (dvisvgm 1.9.2)
  * It is known to work in Ubuntu 14.04 and 18.04 (dvisvgm 1.2.2 and 2.1.3, respectively)
  * Solutions: There are not so many programs that transform images into a nice SVG, most of them have issues. pdf2svg does normally a good work, but it does an ugly output in the affected system for the so-called Text block. Maybe that shows that the problem is caused by something related with the associated font.

* Several problems when running in Ubuntu 12.04.
  * epstopdf related.
  * This version of Ubuntu is out of support, so we have no interest in these bugs by the moment.

## License

visualequation is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

visualequation is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

## Acknowledgements

* I have been inspired by [Ekee](http://rlehy.free.fr/) features. It is a pity that the program is not mantained (2018).
