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
Run this script before packaging or installing.
It requires the LaTeX system and imagemagick to be installed.
"""
import sys
import os
import tempfile
import shutil
import subprocess
import configparser

DPI = 200
ICONS_DEF = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                         'data', 'icons-def.ini'))
ICONS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                         'data', 'icons'))
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
    try:
        subprocess.call(["mogrify", "-chop", "5x0", filename])
    except OSError:
        raise SystemExit("Command mogrify was not found. "
                         + " You need installed imagemagick.")


def code2icon(code, file_output, temp_dir):
    # Create LaTeX file
    latex_file = os.path.join(temp_dir, 've.tex')
    dvi_file = os.path.join(temp_dir, 've.dvi')
    log_file = os.path.join(temp_dir, 've.log')
    with open(LATEX_TEMPLATE, "r") as ftempl:
        with open(latex_file, "w") as flatex:
            for line in ftempl:
                flatex.write(line.replace('%EQ%', edit_expr(code)))
    # Generate the DVI
    try:
        subprocess.check_output(["latex", "-interaction=nonstopmode",
                                 "-halt-on-error",
                                 "-output-directory=" + temp_dir,
                                 latex_file])
    except subprocess.CalledProcessError as error:
        msg = "Error reported by latex. The equation cannot be generated.\n" \
              + "If you have installed the required packages, it could be " \
              + "an internal error.\nCode:" + code
        raise SystemExit(msg)
    except OSError:
        raise SystemExit("Command latex was not found.")
    # Generate the icon
    with open(log_file, "w") as flog:
        try:
            subprocess.call(["dvipng", "-T", "tight", "-D", str(DPI),
                             "-bg", "Transparent",
                             "-o", file_output, dvi_file], stdout=flog)
        except OSError:
            raise SystemExit("Command dvipng was not found.")
    postprocess(file_output)


if __name__ == '__main__':

    # Prepare a temporal directory to manage all LaTeX files
    temp_dirpath = tempfile.mkdtemp()

    if not os.path.exists(ICONS_DIR):
        os.makedirs(ICONS_DIR)

    config = configparser.ConfigParser(delimiters=(' ',))
    config.read(ICONS_DEF)

    for index, section in enumerate(config):
        print("Generating icons...", index + 1, "/", len(config))
        for tag, code in config[section].items():
            png_filepath = os.path.join(ICONS_DIR, tag + '.png')
            if not os.path.exists(png_filepath):
                code2icon(code, png_filepath, temp_dirpath)

    shutil.rmtree(temp_dirpath)
