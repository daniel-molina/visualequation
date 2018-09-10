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

# Set the path to main directories
SYMBOLS_DIR = os.path.join(os.path.dirname(__file__), 'data', 'symbols')
LATEX_TEMPLATE = os.path.join(os.path.dirname(__file__), 'data',
                              'eq_template.tex')
