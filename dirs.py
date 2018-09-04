"""This modules indicates the directories of the program."""
import os

# Set the path to main directories
PROGRAM_DIR = os.path.join(os.path.expanduser('~'), '.visualequation')
SYMBOLS_DIR = os.path.join(PROGRAM_DIR, 'data')
LATEX_TEMPLATE = 'eq_template.tex' # Install me!!
