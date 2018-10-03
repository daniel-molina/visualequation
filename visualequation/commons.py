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
import os, sys, site

VERSION="0.3.5"

# Set the path to common files
# Valid for execution in the sources tree
if os.path.exists(os.path.join(os.path.dirname(__file__), '..', 'data')):
    DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
# Valid for installation in the FHS
elif os.path.exists(os.path.join(sys.prefix, 'share', 'visualequation')):
    DATA_DIR = os.path.join(sys.prefix, 'share', 'visualequation')
# Valid for installation through "pip install --user"
elif os.path.exists(os.path.join(site.USER_BASE, 'share', 'visualequation')):
    DATA_DIR = os.path.join(site.USER_BASE, 'share', 'visualequation')
else:
    raise SystemExit("Could not find where data files are located.")

#DATA_DIR = os.path.dirname(resource_filename(__name__, "visualequation.desktop"))

#print("This is DATA_DIR: ", DATA_DIR, "\n", subprocess.check_output("pwd"),"\n\n")
ICONS_DIR = os.path.join(DATA_DIR, 'icons')
LATEX_TEMPLATE = os.path.join(DATA_DIR, 'eq_template.tex')
ICON = os.path.join(DATA_DIR, 'visualequation.png')
USAGE_FILE = os.path.join(DATA_DIR, 'USAGE.html')
