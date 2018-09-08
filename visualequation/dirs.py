"""This modules indicates the directories of the program."""
import os

# Set the path to main directories
SYMBOLS_DIR = os.path.join(os.path.dirname(__file__), 'data', 'symbols')
LATEX_TEMPLATE = os.path.join(os.path.dirname(__file__), 'data',
                              'eq_template.tex')
