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

from .utils import *

ARROWS = [
    LatexSymb('leftarrow', r'\leftarrow', r'\leftarrow'),
    LatexSymb('longleftarrow', r'\longleftarrow', r'\longleftarrow'),
    LatexSymb('upperleftarrow', r'\Leftarrow', r'\Leftarrow'),
    LatexSymb('upperlongleftarrow', r'\Longleftarrow', r'\Longleftarrow'),
    LatexSymb('rightarrow', r'\rightarrow', r'\rightarrow'),
    LatexSymb('longrightarrow', r'\longrightarrow', r'\longrightarrow'),
    LatexSymb('upperrightarrow', r'\Rightarrow', r'\Rightarrow'),
    LatexSymb('upperlongrightarrow', r'\Longrightarrow', r'\Longrightarrow'),
    LatexSymb('leftrightarrow', r'\leftrightarrow', r'\leftrightarrow'),
    LatexSymb('longleftrightarrow', r'\longleftrightarrow',
              r'\longleftrightarrow'),
    LatexSymb('upperleftrightarrow', r'\Leftrightarrow', r'\Leftrightarrow'),
    LatexSymb('upperlongleftrightarrow', r'\Longleftrightarrow',
              r'\Longleftrightarrow'),
    LatexSymb('uparrow', r'\uparrow', r'\uparrow'),
    LatexSymb('upperuparrow', r'\Uparrow', r'\Uparrow'),
    LatexSymb('downarrow', r'\downarrow', r'\downarrow'),
    LatexSymb('upperdownarrow', r'\Downarrow', r'\Downarrow'),
    LatexSymb('updownarrow', r'\updownarrow', r'\updownarrow'),
    LatexSymb('upperupdownarrow', r'\Updownarrow', r'\Updownarrow'),
    LatexSymb('mapsto', r'\mapsto', r'\mapsto'),
    LatexSymb('longmapsto', r'\longmapsto', '\longmapsto'),
    LatexSymb('nupperrightarrow', r'\nRightarrow', r'\nRightarrow'),
    LatexSymb('nupperleftarrow', r'\nLeftarrow', r'\nLeftarrow'),
    LatexSymb('nupperleftrightarrow', r'\nLeftrightarrow',
              r'\nLeftrightarrow'),
    LatexSymb('nleftarrow', r'\nleftarrow', r'\nleftarrow'),
    LatexSymb('nrightarrow', r'\nrightarrow', r'\nrightarrow'),
    LatexSymb('nleftrightarrow', r'\nleftrightarrow', r'\nleftrightarrow'),
    LatexSymb('nearrow', r'\nearrow', r'\nearrow'),
    LatexSymb('searrow', r'\searrow', r'\searrow'),
    LatexSymb('swarrow', r'\swarrow', r'\swarrow'),
    LatexSymb('nwarrow', r'\nwarrow', r'\nwarrow'),
    LatexSymb('diagup', r'\diagup', r'\diagup'),
    LatexSymb('diagdown', r'\diagdown', r'\diagdown'),
    LatexSymb('cdots', r'\cdots', r'\cdots'),
    LatexSymb('vdots', r'\vdots', r'\vdots'),
    LatexSymb('ldots', r'\ldots', r'\ldots'),
    LatexSymb('ddots', r'\ddots', r'\ddots'),
]
