import os
import subprocess
import tempfile
import shutil

import latex

def eq2latex_file(eq, latex_file, template_file):
    """ Write equation in a LaTeX file according to the template_file.
    It looks for string '%EQ%' in the file and replace it by eq.
    """
    latex_code = latex.eq2latex_code(eq)
    with open(template_file, "rt") as ftempl:
        with open(latex_file, "wt") as flatex:
            for line in ftempl:
                flatex.write(line.replace('%EQ%', latex_code))

def latex_file2dvi(latex_file, output_dir, log_file):
    """ Compile the LaTeX file to DVI image and put the output the given dir.
    The log is saved in the specified file.
    """
    with open(log_file, "wt") as flog:
        subprocess.call(["latex", "-interaction=nonstopmode",
                         "-output-directory=" + output_dir,
                         latex_file], stdout=flog)

def dvi2png(dvi_file, png_file, log_file, dpi):
    """ Convert the DVI file with the equation to PNG.
    The log is saved in the specified file.
    """
    with open(log_file, "wt") as flog:
        subprocess.call(["dvipng", "-T", "tight", "-D", str(dpi),
                         "-bg", "Transparent",
                         "-o", png_file, dvi_file], stdout=flog)

def eq2png(eq, dpi, directory, png_fpath=None):
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
        #os.makedirs(directory)

    fname = 'foo'
    latex_ext = ".tex"
    log_ext = ".log"
    dvi_ext = ".dvi"
    png_ext = ".png"

    template_fpath = "eq_template.tex"
    latex_fpath = os.path.join(directory, fname + latex_ext)
    latex2dvi_log_fpath = os.path.join(directory,
                                       fname + '_latex2dvi' + log_ext)
    dvi2png_log_fpath = os.path.join(directory, fname + '_div2png' + log_ext)
    dvi_fpath = os.path.join(directory, fname + dvi_ext)
    if png_fpath == None:
        png_fpath = os.path.join(directory, fname + png_ext)

    eq2latex_file(eq, latex_fpath, template_fpath)
    latex_file2dvi(latex_fpath, directory, latex2dvi_log_fpath)
    if dpi == None:
        dpi = 300
    dvi2png(dvi_fpath, png_fpath, dvi2png_log_fpath, dpi)

    return png_fpath
