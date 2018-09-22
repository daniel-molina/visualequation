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

from .symbols import *
from .constructs import *
from .delimiters import *
from .functions import *
from .variablesize import *
from .operators import *
from .relations import *
from .arrows import *
from .text import *
from .manylines import *
from .accents import *

MENUITEMSDATA = []
ADDITIONAL_LS = []

MENUITEMSDATA.append(MenuItemData(
    tag="tab_greek_hebrew_symb1",
    symb_l=LOWER_GREEK + UPPER_GREEK + VAR_GREEK + HEBREW + SYMBOLS1,
    expr=r'\alpha\, \infty'))

MENUITEMSDATA.append(MenuItemData(
    tag="tab_mathconstructs",
    symb_l=MATHCONSTRUCTS,
    expr=r'\underbrace{{abc}}'))

ADDITIONAL_LS += SINGLEDELIMITERS

MENUITEMSDATA.append(MenuItemData(
    tag="tab_delimiters",
    symb_l=DELIMITERS,
    expr=r'\left(ab\right)'))

MENUITEMSDATA.append(MenuItemData(
    tag="tab_functions",
    symb_l=FUNCTIONS,
    expr=r'f(x)'))

MENUITEMSDATA.append(MenuItemData(
    tag="tab_variablesize",
    symb_l=VARIABLESIZE,
    expr=r'\sum'))

MENUITEMSDATA.append(MenuItemData(
    tag="tab_someoperators",
    symb_l=SOMEOPERATORS,
    expr=r'\otimes'))

MENUITEMSDATA.append(MenuItemData(
    tag="tab_relations",
    symb_l=RELATIONS,
    expr=r'< \in'))

MENUITEMSDATA.append(MenuItemData(
    tag="tab_arrows",
    symb_l=ARROWS,
    expr=r'\rightarrow'))

ADDITIONAL_LS += COLORS

MENUITEMSDATA.append(MenuItemData(
    tag="tab_text",
    symb_l=TEXT,
    expr=r'\mathbb{R}\,\text{if}'))

ADDITIONAL_LS += MATRIXTYPES

MENUITEMSDATA.append(MenuItemData(
    tag="tab_manylines",
    symb_l=MANYLINES,
    expr=r'\begin{smallmatrix}a&b\\c&d\end{smallmatrix}'))

MENUITEMSDATA.append(MenuItemData(
    tag="tab_accents",
    symb_l=ACCENTS,
    expr=r'\acute{{a}}\;\tilde{{B}}'))
