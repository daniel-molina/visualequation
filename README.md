# visualequation

Visualequation creates equations visually, in a WYSIWYG (What You See Is What You Get) style. Equations can be exported to PNG, EPS, PDF and SVG. PNG and SVG are transparent. If you want a background you can put a white (or whatever color) colorbox to the whole equation in the editor before exporting. You can recover equations from previously created images in PNG and PDF format and continue editing them!

## Requirements

To run the program successfully, you need:

* python2
* pygame
* Tkinter
* LaTeX
* Some specific LaTeX packages (you can find them in the preamble of the equation template _visualequation/data/eq_template.tex_).
* Some command-line programs to manipulate LaTeX output:
  * dvipng
  * dvips
  * dvisvgm
  * epstopdf
* exiftool

### Microsoft Windows and MacOS

By the moment it has only been tested on GNU/Linux. But it would be interesting to have installation instructions for the dependencies on other operative systems. Volunteers needed!
  
### Debian 9.0 and Ubuntu 18.04 or derivatives

$ sudo apt-get install python-pygame python-tk texlive-latex-recommended dvipng texlive-font-utils texlive-science libimage-exiftool-perl

### Ubuntu 14.04 and 16.04 or derivatives

$ sudo apt-get install python-pygame python-tk texlive-latex-recommended dvipng texlive-font-utils texlive-math-extra libimage-exiftool-perl

## Checking that dependencies are fulfilled

If you have the sources you can see if everything is installed properly running the test:

$ python2 -m tests.test_dependencies

## Installation

I did not package visualequation for any distribution yet. In the case of python, installing software with pip and related tools is almost a standard so I decided to use it first. If you know how to manage pip in your system, perfect, follow your way to install visualequation from source (development version) or PyPI (released versions). If you have no clue and want me to explain all the details about how to install it, I feel that I have certain responsability of telling you something that works. If you use Debian 9.0 or Ubuntu 18.04/16.04 it worked for me to install the provided packages (if you install are going to install from PyPI you only need python-pip)

$ sudo apt-get install python-pip python-setuptools python-wheel

add the pip path to your ~/.bashrc

PATH=${PATH}:${HOME}/.local/bin

apply the changes to your current terminal

$ source ~/.bashrc

and continue the instructions in "Installing visualequation locally".


### Installing pip locally (recommended for old distributions)

I will show a recipe to install locally pip because the version that comes in some distributions (like Ubuntu 14.04) does not work totally for the instructions I will give later. Said that, if you want further lecture, I just leave [this well-written link](http://matthew-brett.github.io/pydagogue/installing_on_debian.html).

Download it

$ curl -LO https://bootstrap.pypa.io/get-pip.py

Install it locally

$ python2 get-pip.py --user

Add to your path the directory where pip is installed and where it will install the other programs. You can do it by writting at the end of your .bashrc the following line

PATH=${PATH}:${HOME}/.local/bin

If you want this change to take effect in the current terminal, run

$ source ~/.bashrc

Both

$ pip --version

and

$ python2 -m pip --version

should give the same valid output (the current last version of pip).

If you are going to install from the sources, I recommend now to remove the package setuptools (if it is installed) of your distribution and install it with pip

$ sudo apt-get remove python-setuptools

$ python2 -m pip install --user setuptools

### Installing visualequation using pip

The fastest way is to download it and install from PyPI, just

$ python2 -m pip install --user --upgrade visualequation

On the other hand, if you have the sources, the first step is to generate the LaTeX symbols used by the program:

$ python2 populate_symbols.py

It will late a bit.

After that, you can generate a package

$ python2 setup.py bdist_wheel

and install it

$ python2 -m pip install --user dist/visualequation-\<version\>-py2-none-any.whl

where you substitute <version> by the version number of the file generated in dist/.

## Running visualequation

To execute the program, just run

$ visualequation 

in whatever current directory. It should work if you included ~/.local/bin in your PATH as indicated above.

## Usage/Instructions

This program is expected to be user-friendly and intuitive, so it should not be difficult to use.

Instead of a cursor, you navigate with a box that surrounds blocks of the equation, from a single symbol to the entire equation. Insert characters at the right of the box by pressing keys on the keyboard or clicking symbols in the above panel. If the box surrounds a square, as when you open the program, you overwrite the square.

The following key combinations work: (They can be changed or extended in the future)

* LEFT and RIGHT (or TAB or clicking the equation):
Change the selection box.

* UP and DOWN (or clicking in the menu items of the panel below):
Change the symbols and operators showed in the panel above.

* DELETE or BACKSPACE:
Remove current selection. If it was the entire argument of an operator, a square will remain so you can select it and add something in the future. There is no way to remove those squares without deleting the entire operator.

* ^ and _:
Put a superindex or subindex.

* CTRL+z:
Recover the equation as it was before last change. You can use it all the times that you need.

* CTRL+y:
The opposite of CTR+z. If you change the equation after using CTRL+z, the future history from that point will not be accessible by Ctrl+y anymore.

* CTRL+c:
Copy the current selection.

* CTRL+x:
Cut the current selection.

* CTRL+v:
Paste the last copied or cut selection.

* CTRL+s:
Save the equation to PNG, PDF, EPS or SVG format. If format is either PNG or PDF, you will be able to recover the equation (see CTR+o).

* CTR+o:
Open an equation from a PNG or PDF previously created with this program (see CTR+s). The current equation being edited will be lost.

* CTR+p:
Create a square at the left of the selection box, ready to be overwritten. It is useful if you forgot to write something at the left of a block and you do not want to delete the first symbol/operator until you write the missing part.

* SHIFT+click on an element of the panel above:
If the element is a symbol, the selection is replaced by the symbol. If it is an operator, the selection is replaced by the operator and the first argument of it is set to the selection. (The first argument is the one represented by dots instead of a square)

## Known Issues

* Conversion to SVG fails when the equation contains a Text. The application will wait forever while converting, so the user has to force the exit of the execution.
  * Affected environments: Ubuntu Xenial (16.04) (dvisvgm 1.9.2)
  * It is known to work in Ubuntu 14.04 and 18.04 (dvisvgm 1.2.2 and 2.1.3, respectively)
  * Solutions: There are not so many programs that transform images into a nice SVG, most of them have issues. pdf2svg does normally a good work, but it does an ugly output in the affected system for the so-called Text block. Maybe that shows that the problem is caused by something related with the associated font.

* Several problems when running in Ubuntu 12.04.
  * Tk and epstopdf related.
  * This version of Ubuntu is out of support, so we are not going have no interest in these bugs by the moment.

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
