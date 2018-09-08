#!/usr/bin/env python2
"""
Run this script before installing.
It requires the LaTeX system to be installed.
"""
import os
import tempfile
import shutil

import visualequation.symbols as symbols
import visualequation.conversions as conversions
import visualequation.dirs as dirs

def generate_symb_images(menuitemdata, temp_dir):
    """
    Generate the png of the symbols and place them in a given directory.
    A temporal directory must be passed, where auxiliary files are
    generated.
    """
    for symb in menuitemdata.symb_l:
        filename = os.path.join(dirs.SYMBOLS_DIR, symb.tag + ".png")
        conversions.eq2png(symb.expr, menuitemdata.dpi, None, temp_dir,
                           filename)

if __name__ == '__main__':

    os.chdir('visualequation')
    # Prepare a temporal directory to manage all LaTeX files
    temp_dirpath = tempfile.mkdtemp()

    for index, menuitemdata in enumerate(symbols.MENUITEMSDATA):
        print "Generating menu symbols...", index+1, "/", \
            len(symbols.MENUITEMSDATA)
        generate_symb_images(menuitemdata, temp_dirpath)

    print "Generating Tk symbols..."
    for symb in symbols.ADDITIONAL_LS:
        filename = os.path.join(dirs.SYMBOLS_DIR, symb.tag + ".png")
        conversions.eq2png(symb.expr, 200, None, temp_dirpath, filename)

    shutil.rmtree(temp_dirpath)
