"""
A module to manage creation of LaTeX templatex, generations of DVI and
conversions to other formats
"""
import os
import subprocess

import dirs
import eqtools

def eq2latex_file(eq, latex_file, template_file):
    """ Write equation in a LaTeX file according to the template_file.
    It looks for string '%EQ%' in the file and replace it by eq.
    """
    if isinstance(eq, basestring):
        latex_code = eq
    elif isinstance(eq, list):
        latex_code = eqtools.eq2latex_code(eq)
    else:
        raise ValueError('Cannot understand equation type.')
    with open(template_file, "r") as ftempl:
        with open(latex_file, "w") as flatex:
            for line in ftempl:
                flatex.write(line.replace('%EQ%', latex_code))

def latex_file2dvi(latex_file, output_dir, log_file):
    """ Compile the LaTeX file to DVI image and put the output the given dir.
    The log is saved in the specified file.
    """
    with open(log_file, "w") as flog:
        subprocess.call(["latex", "-interaction=nonstopmode",
                         "-output-directory=" + output_dir,
                         latex_file], stdout=flog)

def dvi2png(dvi_file, png_file, log_file, dpi, bg):
    """ Convert a DVI file to PNG.
    The log is saved in the specified file.
    """
    if bg == None:
        bg = "Transparent"

    with open(log_file, "w") as flog:
        subprocess.call(["dvipng", "-T", "tight", "-D", str(dpi),
                         "-bg", bg,
                         "-o", png_file, dvi_file], stdout=flog)

def dvi2eps(dvi_file, eps_file, log_file):
    """ Convert the DVI file to PostScript. """
    with open(log_file, "w") as flog:
        subprocess.call(["dvips", "-E", "-D", "600", "-Ppdf", 
                         "-o", eps_file, dvi_file], stderr=flog)

def eps2pdf(eps_file, pdf_file):
    subprocess.call(["epstopdf", "--outfile", pdf_file, eps_file])

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
        subprocess.call(["dvisvgm", "-n", "-c5,5", 
                         "-o", svg_file, dvi_file], stderr=flog)

def eq2png(eq, dpi, bg, directory, png_fpath=None):
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
    latex_fpath = os.path.join(directory, fname + '.tex')
    latex2dvilog_fpath = os.path.join(directory,
                                      fname + '_latex2dvi.log')
    dvi2pnglog_fpath = os.path.join(directory, fname + '_div2png.log')
    dvi_fpath = os.path.join(directory, fname + '.dvi')
    if png_fpath == None:
        png_fpath = os.path.join(directory, fname + '.png')
    eq2latex_file(eq, latex_fpath, dirs.LATEX_TEMPLATE)
    latex_file2dvi(latex_fpath, directory, latex2dvilog_fpath)
    if dpi == None:
        dpi = 300
    dvi2png(dvi_fpath, png_fpath, dvi2pnglog_fpath, dpi, bg)
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
        #os.makedirs(directory)
    fname = 'foo'
    latex_fpath = os.path.join(directory, fname + '.tex')
    latex2dvilog_fpath = os.path.join(directory,
                                      fname + '_latex2dvi.log')
    dvi2epslog_fpath = os.path.join(directory, fname + '_div2eps.log')
    dvi_fpath = os.path.join(directory, fname + '.dvi')
    if eps_fpath == None:
        eps_fpath = os.path.join(directory, fname + '.ps')
    eq2latex_file(eq, latex_fpath, dirs.LATEX_TEMPLATE)
    latex_file2dvi(latex_fpath, directory, latex2dvilog_fpath)
    dvi2eps(dvi_fpath, eps_fpath, dvi2epslog_fpath)
    return eps_fpath

def eq2pdf(eq, directory, pdf_fpath=None):
    if pdf_fpath == None:
        pdf_fpath = os.path.join(directory, 'foo.pdf')
    eps_fpath = eq2eps(eq, directory)
    eps2pdf(eps_fpath, pdf_fpath)
    return pdf_fpath

def eq2svg(eq, directory, svg_fpath):

    # If directory does not exist, raise exception
    if not os.path.exists(directory):
        raise ValueError('Directory does not exist.')
    fname = 'foo'
    latex_fpath = os.path.join(directory, fname + '.tex')
    latex2dvilog_fpath = os.path.join(directory,
                                      fname + '_latex2dvi.log')
    dvi_fpath = os.path.join(directory, fname + '.dvi')    
    dvi2svglog_path = os.path.join(directory,
                                   fname + '_dvi2svg.log')
    eq2latex_file(eq, latex_fpath, dirs.LATEX_TEMPLATE)
    latex_file2dvi(latex_fpath, directory, latex2dvilog_fpath)
    dvi2svg(dvi_fpath, svg_fpath, dvi2svglog_path)
