import os
import subprocess

import latex

def eq2latex_file(eq, latex_file, template_file):
    """ Create equation in LaTeX """
    s = latex.eq2latex_code(eq)
    with open(template_file, "rt") as ftempl:
        with open(latex_file, "wt") as flatex:
            for line in ftempl:
                flatex.write(line.replace('%EQ%', s))

def latex_file2dvi(latex_file, output_dir, log_file):
    with open(log_file, "wt") as flog:
        subprocess.call(["latex", "-interaction=nonstopmode",
                         "-output-directory=" + output_dir,
                         latex_file], stdout=flog)

def dvi2png(dvi_file, png_file, log_file):
    with open(log_file, "wt") as flog:
        subprocess.call(["dvipng", "-T", "tight", "-D", "500",
                         "-bg", "Transparent",
                         "-o", png_file, dvi_file], stdout=flog)

def eq2png(eq, f_base):
    """ Create a png from a equation. Returns the filename.

    It allocates generated files in temporal directory (TODO).
    By now it is used in a known dir in the path of execution, 'dir'.
    """
    directory = 'dir'
    template_file = "eq_template.tex"
    latex_ext = ".tex"
    log_ext = ".log"
    dvi_ext = ".dvi"
    png_ext = ".png"

    latex_f = os.path.join(directory, f_base + latex_ext)
    latex2dvi_log_f = os.path.join(directory, f_base + '_latex2dvi' + log_ext)
    dvi2png_log_f = os.path.join(directory, f_base + '_div2png' + log_ext)
    dvi_f = os.path.join(directory, f_base + dvi_ext)
    png_f = os.path.join(directory, f_base + png_ext)
    eq2latex_file(eq, latex_f, template_file)
    latex_file2dvi(latex_f, directory, latex2dvi_log_f)
    dvi2png(dvi_f, png_f, dvi2png_log_f)
    return png_f
