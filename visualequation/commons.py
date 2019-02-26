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

"""This modules indicates the directories of the program."""
import os
import sys
import site

VERSION="0.3.9"

# Set the path to common files
DATA_DIR = ""
LOCALE_DIR = ""
# Priority 1: Execution in the sources tree (do not fill INSTALL_DIRS)
if os.path.exists(os.path.join(os.path.dirname(__file__), '..', 'data')) \
   and os.path.exists(os.path.join(os.path.dirname(__file__),
                                   '..', 'visualequation')):
    DATA_DIR = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'data'))
    LOCALE_DIR = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'locale'))
# Priority 2: Installation through "pip install --user"
INSTALL_DIRS = []
if os.path.exists(os.path.join(site.USER_BASE, 'share', 'visualequation')):
    if not DATA_DIR and not LOCALE_DIR:
        DATA_DIR = os.path.join(site.USER_BASE, 'share', 'visualequation')
        LOCALE_DIR = os.path.join(site.USER_BASE, 'share', 'locale')
    INSTALL_DIRS.append(os.path.join(site.USER_BASE, 'share'))
# Priority 1.5: Installation through "pip install --target="
if os.path.exists(os.path.join(
        os.path.dirname(__file__), '..', 'share', 'visualequation')):
    _BASE = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..', 'share'))
    if (not DATA_DIR and not LOCALE_DIR) or _BASE not in INSTALL_DIRS:
        # Overwrite variables if it is known that __file__ is not
        # the same than --user installation
        DATA_DIR = os.path.join(_BASE, 'visualequation')
        LOCALE_DIR = os.path.join(_BASE, 'locale')
        INSTALL_DIRS.append(_BASE)
# Priority 3: Installation in the FHS
if os.path.exists(os.path.join(sys.prefix, 'share', 'visualequation')):
    if not DATA_DIR and not LOCALE_DIR:
        DATA_DIR = os.path.join(sys.prefix, 'share', 'visualequation')
        LOCALE_DIR = os.path.join(sys.prefix, 'share', 'locale')
    INSTALL_DIRS.append(os.path.join(sys.prefix, 'share'))

if not DATA_DIR or not LOCALE_DIR:
    # Do not use ShowError here (you would need a QApplication)
    raise SystemExit("Could not find any installation of visualequation.")

#DATA_DIR = os.path.dirname(
#    resource_filename(__name__, "visualequation.desktop"))

if len(INSTALL_DIRS) > 1:
    print("WARNING: Visualequation data seems installed in several locations:")
    for path in INSTALL_DIRS:
        print("\t", path)
    print("Next, we show where visualequation is looking for files:")
    print("Data:       ", DATA_DIR)
    print("Locale:     ", LOCALE_DIR)
    print("Own modules:", os.path.dirname(__file__))
        
#print("This is DATA_DIR: ", DATA_DIR, "\n", subprocess.check_output("pwd"),"\n\n")
ICONS_DIR = os.path.join(DATA_DIR, 'icons')
LATEX_TEMPLATE = os.path.join(DATA_DIR, 'eq_template.tex')
ICON = os.path.join(DATA_DIR, 'visualequation.png')
