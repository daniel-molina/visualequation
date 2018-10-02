#!/usr/bin/env python3

# visualequation is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# visualequation is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Run this script before installing.
It requires the LaTeX system to be installed.
"""
import sys
import os
import tempfile
import shutil
import subprocess

from visualequation.symbols.lists import MENUITEMSDATA, ADDITIONAL_LS
from visualequation.conversions import eq2png

DPI = 200
ICONS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data',
                                         'icons'))
LATEX_TEMPLATE = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                              'data', 'eq_template.tex'))

def edit_expr(latex_code):
    """
    Add a slim and tall character so all the symbols are cut with more or less
    the same height.
    """
    return r"\textcolor{white}{|}" + latex_code

def postprocess(filename):
    """
    Remove the extra added character from the image.
    """
    subprocess.call(["mogrify", "-chop", "5x0", filename])

def generate_icons(menuitemdata, temp_dir):
    """
    Generate the png of the symbols and place them in a given directory.
    A temporal directory must be passed, where auxiliary files are
    generated.
    """
    for symb in menuitemdata.symb_l:
        filename = os.path.join(ICONS_DIR, symb.tag + ".png")
        if not os.path.exists(filename):
            eq2png(edit_expr(symb.expr), DPI, None, temp_dir,
                   filename, latex_template=LATEX_TEMPLATE)
            postprocess(filename)

if __name__ == '__main__':

    os.chdir('visualequation')
    # Prepare a temporal directory to manage all LaTeX files
    temp_dirpath = tempfile.mkdtemp()

    if not os.path.exists(ICONS_DIR):
        os.makedirs(ICONS_DIR)

    for index, menuitemdata in enumerate(MENUITEMSDATA):
        print("Generating tab icons...", index+1, "/", \
            len(MENUITEMSDATA))
        filename = os.path.join(ICONS_DIR, menuitemdata.tag + '.png')
        if not os.path.exists(filename):
            eq2png(edit_expr(menuitemdata.expr), DPI, None, temp_dirpath,
                   filename, latex_template=LATEX_TEMPLATE)
            postprocess(filename)
        generate_icons(menuitemdata, temp_dirpath)

    print("Generating dialog icons...")
    for symb in ADDITIONAL_LS:
        filename = os.path.join(ICONS_DIR, symb.tag + ".png")
        if not os.path.exists(filename):
            eq2png(edit_expr(symb.expr), DPI, None, temp_dirpath, filename,
                   latex_template=LATEX_TEMPLATE)
            postprocess(filename)

    shutil.rmtree(temp_dirpath)
