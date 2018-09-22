#!/usr/bin/env python2

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

import os
import sys
import unittest
import tempfile
import shutil
import subprocess
import json

from visualequation import commons
from visualequation import conversions

class DependenciesTest(unittest.TestCase):

    def test_latex(self):
        temp_dirpath = tempfile.mkdtemp()
        latex_fpath = os.path.join(temp_dirpath, 'latex.tex')
        latex_code = r"\int_0^1 f(x)\, dx = \sum_{n=0}^\infty a_n"
        with open(commons.LATEX_TEMPLATE, "r") as ftempl:
            with open(latex_fpath, "w") as flatex:
                for line in ftempl:
                    flatex.write(line.replace('%EQ%', latex_code))
        try:
            subprocess.check_output(["latex", "-halt-on-error",
                                     "-output-directory=" + temp_dirpath,
                                     latex_fpath])
        except subprocess.CalledProcessError:
            raise SystemExit("Suggestion: Do you have the AMS LaTeX packages?")
        except OSError:
            raise SystemExit("Suggestion: Do you have command latex?")
        shutil.rmtree(temp_dirpath)

    def test_dvipng(self):
        temp_dirpath = tempfile.mkdtemp()
        dvi_fpath = os.path.join(os.path.dirname(__file__), 'im.dvi')
        png_fpath = os.path.join(temp_dirpath, 'im.png')
        try:
            subprocess.check_output(["dvipng", "-T", "tight", "-D", "600",
                                     "-bg", "Transparent",
                                     "-o", png_fpath, dvi_fpath])
        except subprocess.CalledProcessError:
            raise SystemExit("Was DVI image not found in the directory?")
        except OSError:
            raise SystemExit("Suggestion: Do you have command dvipng?")
        shutil.rmtree(temp_dirpath)

    def test_dvips(self):
        temp_dirpath = tempfile.mkdtemp()
        dvi_fpath = os.path.join(os.path.dirname(__file__), 'im.dvi')
        eps_fpath = os.path.join(temp_dirpath, 'im.ps')
        try:
            subprocess.check_output(["dvips", "-E", "-D", "600", "-Ppdf", 
                                     "-o", eps_fpath, dvi_fpath])
        except subprocess.CalledProcessError:
            raise SystemExit("DVI image not found in the directory?")
        except OSError:
            raise SystemExit("Suggestion: Do you have command dvips?")

        shutil.rmtree(temp_dirpath)

    def test_epstopdf(self):
        temp_dirpath = tempfile.mkdtemp()
        eps_fpath = os.path.join(os.path.dirname(__file__), 'im.ps')
        pdf_fpath = os.path.join(temp_dirpath, 'im.pdf')
        try:
            subprocess.check_output(["epstopdf", "--outfile", pdf_fpath,
                                     eps_fpath])
        except subprocess.CalledProcessError:
            raise SystemExit("EPS image not found in the directory?")
        except OSError:
            raise SystemExit("Suggestion: Do you have command epstopdf?")

        shutil.rmtree(temp_dirpath)

    def test_dvisvgm(self):
        temp_dirpath = tempfile.mkdtemp()
        dvi_fpath = os.path.join(os.path.dirname(__file__), 'im.dvi')
        svg_fpath = os.path.join(temp_dirpath, 'im.svg')
        # dvisgvm does not return error code when file is not found
        try:
            subprocess.call(["dvisvgm", "--no-fonts", "--scale=5,5", 
                             "-o", svg_fpath, dvi_fpath])
        except OSError:
            raise SystemExit("Suggestion: Do you have command dvisvgm?")

        shutil.rmtree(temp_dirpath)

    def test_exiftool_read(self):
        png_fpath = os.path.join(os.path.dirname(__file__), 'im.png')
        pdf_fpath = os.path.join(os.path.dirname(__file__), 'im.pdf')

        def fun(fpath):
            try:
                eq_str_b = subprocess.check_output(["exiftool", "-b", "-s3",
                                                    "-description", fpath])
                eq_str = eq_str_b.decode('utf8')
                if not eq_str:
                    raise SystemExit("No equation inside file %s!" % fpath)
                json.JSONDecoder(object_hook=conversions.from_json
                ).decode(eq_str)
            except subprocess.CalledProcessError:
                raise SystemExit("Error by exiftool when trying to extract"
                                 + "equation from file.")
            except ValueError as error:
                raise SystemExit(error)
            except OSError:
                raise SystemExit("Suggestion: Do you have command exiftool?")
        fun(png_fpath)
        fun(pdf_fpath)

            
    def test_exiftool_write(self):
        temp_dirpath = tempfile.mkdtemp()
        png_fpath = os.path.join(os.path.dirname(__file__), 'im.png')
        pdf_fpath = os.path.join(os.path.dirname(__file__), 'im.pdf')
        def fun(fpath):
            try:
                subprocess.check_output(["exiftool", "-out", temp_dirpath,
                                         "-description=Hi", fpath])
            except subprocess.CalledProcessError:
                raise SystemExit("Exiftool error.")
            except OSError:
                raise SystemExit("Suggestion: Do you have command exiftool?")
        fun(png_fpath)
        fun(pdf_fpath)
        shutil.rmtree(temp_dirpath)

    def test_pyqt5(self):
        try:
            import PyQt5
        except ImportError:
            raise SystemExit("You must have PyQt5 installed.")

if __name__ == "__main__":
    unittest.main()
