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

def dvi2png(dvi_file, png_file, log_file):
    """ Convert the DVI file with the equation to PNG.
    The log is saved in the specified file.
    """
    with open(log_file, "wt") as flog:
        subprocess.call(["dvipng", "-T", "tight", "-D", "500",
                         "-bg", "Transparent",
                         "-o", png_file, dvi_file], stdout=flog)

def eq2png(eq, directory, fname=None):
    """ Create a png from a equation, returns the filename of the PNG image.

    The user specify the dir where it will be created and the name of the
    image (without extension). If the filename is not specified it is assumed
    that the directory is temporal and this function will not clean the
    directory of auxiliary files that it will create.
    """

    # If directory does not exist, raise exception
    if not os.path.exists(directory):
        raise ValueError('Directory does not exist.')
        #os.makedirs(directory)

    # If the user want a png, put the rest in a temporal dir
    # (it prevents overwriting things in a place where you are invited)
    if fname == None:
        fname = 'foo'
        aux_dir = directory
        rm_aux_files = False
    else:
        aux_dir = tempfile.mkdtemp()
        rm_aux_files = True

    template_file = "eq_template.tex"
    latex_ext = ".tex"
    log_ext = ".log"
    dvi_ext = ".dvi"
    png_ext = ".png"

    latex_f = os.path.join(aux_dir, fname + latex_ext)
    latex2dvi_log_f = os.path.join(aux_dir, fname + '_latex2dvi' + log_ext)
    dvi2png_log_f = os.path.join(aux_dir, fname + '_div2png' + log_ext)
    dvi_f = os.path.join(aux_dir, fname + dvi_ext)
    png_f = os.path.join(directory, fname + png_ext)
    eq2latex_file(eq, latex_f, template_file)
    latex_file2dvi(latex_f, aux_dir, latex2dvi_log_f)
    dvi2png(dvi_f, png_f, dvi2png_log_f)

    if rm_aux_files:
        shutil.rmtree(aux_dir)

    return png_f
