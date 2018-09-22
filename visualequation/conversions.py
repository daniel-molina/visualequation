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
A module to manage creation of LaTeX templatex, generations of DVI and
conversions to other formats
"""
import os
import subprocess
import json

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from . import commons
from . import eqtools
from .symbols import utils

def eq2latex_file(eq, latex_file, template_file):
    """ Write equation in a LaTeX file according to the template_file.
    It looks for string '%EQ%' in the file and replace it by eq.
    """
    if isinstance(eq, str):
        latex_code = eq
    elif isinstance(eq, list):
        latex_code = eqtools.eq2latex_code(eq)
    else:
        raise SystemExit('Internal Error: Cannot understand equation type.')
    with open(template_file, "r") as ftempl:
        with open(latex_file, "w") as flatex:
            for line in ftempl:
                flatex.write(line.replace('%EQ%',
                                          '%' + repr(eq) + "\n" + latex_code))

def latex_file2dvi(latex_file, output_dir):
    """
    Compile the LaTeX file to DVI image and put the output in the given dir.
    The log is saved in the specified file.
    """
    try:
        subprocess.check_output(["latex", "-interaction=nonstopmode",
                                 "-halt-on-error",
                                 "-output-directory=" + output_dir,
                                 latex_file])
    except subprocess.CalledProcessError as error:
        raise SystemExit("Error reported by latex. It can be because:\n"
                         + " * You do not have installed required packages.\n"
                         + "   (Do you success running test test_latex?)\n"
                         + " * An internal error. Please, report it with all "
                         + "the text returned above and the files inside "
                         + "this directory:\n%s" % output_dir)
    except OSError:
        raise SystemExit("Command latex was not found.")

    
def dvi2png(dvi_file, png_file, log_file, dpi, bg):
    """ Convert a DVI file to PNG.
    The log is saved in the specified file.
    """
    if bg == None:
        bg = "Transparent"

    with open(log_file, "w") as flog:
        try:
            subprocess.call(["dvipng", "-T", "tight", "-D", str(dpi),
                             "-bg", bg,
                             "-o", png_file, dvi_file], stdout=flog)
        except OSError:
            raise SystemExit("Command dvipng was not found.")

def dvi2eps(dvi_file, eps_file, log_file):
    """ Convert the DVI file to PostScript. """
    with open(log_file, "w") as flog:
        try:
            subprocess.call(["dvips", "-E", "-D", "600", "-Ppdf", 
                             "-o", eps_file, dvi_file], stderr=flog)
        except OSError:
            raise SystemExit("Command dvips was not found.")
            
def eps2pdf(eps_file, pdf_file):
    try:
        subprocess.call(["epstopdf", "--outfile", pdf_file, eps_file])
    except OSError:
        raise SystemExit("Command epstopdf was not found.")

        
# eps2svg: Ouput SVG has bounding box problems
# In Ekee it seems solved by hand but I am not able to reproduce the fix
#def eps2svg(eps_file, svg_file, log_file):
#    with open(log_file, "w") as flog:
#        subprocess.call(["pstoedit", "-dt", "-ssp", "-f", "plot-svg",
#                         eps_file, svg_file], stderr=flog)

# It does not work so good in some sytems (eps produced),
# specially the \text fields (very bad pixeled)
#def pdf2svg(pdf_file, svg_file):
#    subprocess.call(["pdf2svg", pdf_file, svg_file])

def dvi2svg(dvi_file, svg_file, log_file):
    """
    Convert the DVI file to SVG with dvisvgm (it comes with texlive).
    It is the best option found until now:
    * ps2edit creates does not create the image with a tight bounding box.
    * pdf2svg does not work well with pixeled text that dvips create
      in some systems, even when resolution is high in the pdf.
      (it is an issue of \text{} fields, or whatever outside math environment)
    """
    with open(log_file, "w") as flog:
        try:
            subprocess.call(["dvisvgm", "--no-fonts", "--scale=5,5", 
                             "-o", svg_file, dvi_file], stderr=flog)
        except OSError:
            raise SystemExit("Command dvisvgm was not found.")

class MyEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__

def from_json(json_o):
    if isinstance(json_o, dict):
        return utils.Op(json_o['n_args'], json_o['latex_code'])

def eq2png(eq, dpi, bg, directory, png_fpath=None, add_metadata=False):
    """ Create a png from a equation, returns the path of PNG image.

    The size of the image is specified (dpi).
    The user specify the dir where auxiliary files will be created.
    If the path of the image is not specified, it will be created in the same
    directory (and will be overwritten if this function is called again with
    the same directory)
    """
    # If directory does not exist, raise exception
    if not os.path.exists(directory):
        raise ValueError('Directory does not exist.')
    fname = 've'
    latex_fpath = os.path.join(directory, fname + '.tex')
    dvi2pnglog_fpath = os.path.join(directory, fname + '_div2png.log')
    dvi_fpath = os.path.join(directory, fname + '.dvi')
    if png_fpath == None:
        png_fpath = os.path.join(directory, fname + '.png')
    eq2latex_file(eq, latex_fpath, commons.LATEX_TEMPLATE)
    latex_file2dvi(latex_fpath, directory)
    if dpi == None:
        dpi = 300
    dvi2png(dvi_fpath, png_fpath, dvi2pnglog_fpath, dpi, bg)
    if add_metadata:
        # Save the equation into the file
        eq_str = json.dumps(eq, cls=MyEncoder)
        exiftoollog_fpath = os.path.join(directory, fname + '_exif.log')
        with open(exiftoollog_fpath, "w") as flog:
            try:
                subprocess.call(["exiftool", "-overwrite_original",
                                 "-description=" + eq_str,
                                 png_fpath], stdout=flog)
            except subprocess.CalledProcessError:
                raise SystemExit("Exiftool related error. "
                                 + "Please, report this bug.")
            except OSError:
                raise SystemExit("Command exiftool was not found.")

    return png_fpath

def eq2eps(eq, directory, eps_fpath=None):
    """ Create a eps from a equation, returns the path of eps image.

    The user specify the dir where auxiliary files will be created.
    If the path of the image is not specified, it will be created in the same
    directory (and will be overwritten if this function is called again with
    the same directory)
    """
    # If directory does not exist, raise exception
    if not os.path.exists(directory):
        raise ValueError('Directory does not exist.')
    fname = 've'
    latex_fpath = os.path.join(directory, fname + '.tex')
    dvi2epslog_fpath = os.path.join(directory, fname + '_div2eps.log')
    dvi_fpath = os.path.join(directory, fname + '.dvi')
    if eps_fpath == None:
        eps_fpath = os.path.join(directory, fname + '.ps')
    eq2latex_file(eq, latex_fpath, commons.LATEX_TEMPLATE)
    latex_file2dvi(latex_fpath, directory)
    dvi2eps(dvi_fpath, eps_fpath, dvi2epslog_fpath)
    return eps_fpath

def eq2pdf(eq, directory, pdf_fpath=None):
    """
    Convert equation to pdf file. It always adds the equation to metadata.
    """
    if pdf_fpath == None:
        pdf_fpath = os.path.join(directory, 've.pdf')
        save_eq = False
    else:
        save_eq = True
    eps_fpath = eq2eps(eq, directory)
    eps2pdf(eps_fpath, pdf_fpath)
    if save_eq:
        # Save the equation into the file
        eq_str = json.dumps(eq, cls=MyEncoder)
        exiftoollog_fpath = os.path.join(directory, 've_exif.log')
        with open(exiftoollog_fpath, "w") as flog:
            try:
                subprocess.call(["exiftool", "-overwrite_original",
                                 "-description=" + eq_str,
                                 pdf_fpath], stdout=flog)
            except subprocess.CalledProcessError:
                raise SystemExit("Exiftool error. Please, report it.")
            except OSError:
                raise SystemExit("Command exiftool was not found.")

    return pdf_fpath

def eq2svg(eq, directory, svg_fpath):
    """ Converts the equation to SVG"""

    # If directory does not exist, raise exception
    if not os.path.exists(directory):
        raise ValueError('Directory does not exist.')
    fname = 've'
    latex_fpath = os.path.join(directory, fname + '.tex')
    dvi_fpath = os.path.join(directory, fname + '.dvi')    
    dvi2svglog_path = os.path.join(directory,
                                   fname + '_dvi2svg.log')
    eq2latex_file(eq, latex_fpath, commons.LATEX_TEMPLATE)
    latex_file2dvi(latex_fpath, directory)
    dvi2svg(dvi_fpath, svg_fpath, dvi2svglog_path)

def open_eq(parent, filename = None):
    "Return equation inside a file chosen interactively. Else, None."
    if not filename:
        filename, _ = QFileDialog.getOpenFileName(
            parent, 'Open equation', '', 'Valid formats (*.png *.pdf)')
    if not filename:
        return None
    try:
        eq_str = subprocess.check_output(
            ["exiftool", "-b", "-s3", "-description", filename]).decode('utf8')
        if not eq_str:
            msg = QMessageBox(parent)
            msg.setText("No equation inside this file.")
            msg.setWindowTitle("Warning")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
            return None
        return json.JSONDecoder(object_hook=from_json).decode(eq_str)
    except subprocess.CalledProcessError:
        msg = QMessageBox(parent)
        msg.setText("Error by exiftool when trying to extract equation "
                    + "from file.")
        msg.setWindowTitle("Error")
        msg.setIcon(QMessageBox.Critical)
        msg.exec_()
        return None
    except OSError:
        raise SystemExit("Command exiftool was not found.")
    except ValueError as error:
        raise SystemExit("Error parsing equation: %s" % error)
        
