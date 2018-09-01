# visualequation

Visualequation creates equations visually, in a WYSIWYG (What You See Is What You Get) style. By the moment, they can be exported to transparent png (CTRL+s). Probably it will be extended to other formats.

## Requirements
By the moment it has only been tested on GNU/Linux. But it would be interesting to have installation instructions for the dependencies on other operative systems.

To run the program successfully, you need:

* pygame
* LaTeX (maybe you need to install separatelly some packages). The command used is
  * latex
* Some commands that are probably installed if you have the others:
  * dvipng
  * python2
  
In debian or derivatives, it should be enough:

\# apt-get install python-pygame dvipng texlive-math-extra

Yes, LaTeX will require around 600 MB, but the quality of the equations is incredible too.

To run the program:

$ python2 visualequation.py

## Usage/Instructions

This program is expected to be user-friendly and intuitive, so it should not be difficult to use.

Instead of a cursor, you navigate with a box that surrounds blocks of the equation, from a single symbol to the entire equation. Insert characters at the right of the box by pressing keys on the keyboard or clicking symbols in the above panel. If the box surrounds a square, as when you open the program, you overwrite the square.

The following key combinations work: (They can be changed or extended in the future)

* LEFT and RIGHT (or clicking the equation):
Change the selection box.

* UP and DOWN (or clicking in the menu items of the panel below):
Change the symbols and operators showed in the panel above.

* DELETE or BACKSPACE:
Remove current selection. If it was the entire argument of an operator, a square will remain so you can select it and add something in the future. There is no way to remove those squares without deleting the entire operator.

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
Save the equation to a transparent PNG file.

* SHIFT+click on an element of the panel above:
If the element is a symbol, the selection is replaced by the symbol. If it is an operator, the selection is replaced by the operator and the first argument of it is set to the selection. (The first argument is the one represented by one dot or three dots instead of a square)

* TAB:
Create a square at the left of the selection box, ready to be overwritten. Useful if you forgot to write something at the left of a block and you do not want to delete the first character/operator until you write the missing part.


## License

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

## Acknowledgements

* The badge was done by SMA-DEV (http://www.supermagicadventure.net/) licensed under the WTFPL.
