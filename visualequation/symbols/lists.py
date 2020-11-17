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

from visualequation.eqlib.constructs import MathConstruct
from visualequation.eqlib.letters import *
from visualequation.eqlib.symbcatalog import *
from .functions import *
from .variablesize import *
from .text import *
from visualequation.eqlib.manylines import *
from .accents import *


def f(cls, *args, **kwargs):
    def g():
        return cls(*args, **kwargs)
    return g


def f_mc(name):
    return name, f(MathConstruct, name)


MATHCONSTRUCTS = [
    PanelIcon('frac', Frac),
    PanelIcon('sqrt', Sqrt),
    PanelIcon('nsqrt', NRoot),
    PanelIcon(*f_mc('overline')),
    PanelIcon(*f_mc('underline')),
    PanelIcon(*f_mc('widehat')),
    PanelIcon(*f_mc('widetilde')),
    PanelIcon(*f_mc('overrightarrow')),
    PanelIcon(*f_mc('overleftarrow')),
    PanelIcon(*f_mc('overleftrightarrow')),
    PanelIcon(*f_mc('underrightarrow')),
    PanelIcon(*f_mc('underleftarrow')),
    PanelIcon(*f_mc('underleftrightarrow')),
    PanelIcon(*f_mc('xrightarrow')),
    PanelIcon(*f_mc('xleftarrow')),
    PanelIcon(*f_mc('overbrace')),
    PanelIcon(*f_mc('underbrace')),
]

LGREEK = [PanelIcon(g.name.lower(), f(Greek, g)) for g in GreekE]
UGREEK = [PanelIcon(g.name.lower(), f(Greek.from_str, UGREEK_DICT[g], True))
          for g in UGreekE]
VGREEK = [PanelIcon(g.name.lower(), f(Greek.from_str, VGREEK_DICT[g],
                                      False, True)) for g in VGreekE]
HEBREW = [PanelIcon(h.name.lower(), f(Hebrew, h)) for h in HebrewE]

MISC = [PanelIcon(e.name.lower(), f(MiscSimpleSymb, e)) for e
        in MiscSimpleSymbE]
ARROWS = [PanelIcon(e.name.lower(), f(RelationArrow, e)) for e
          in RelationArrowE]
BINOPS = [PanelIcon(e.name.lower(), f(BinOpSymb, e))
          for e in BinOpSymbE]

MENUITEMSDATA = []
ADDITIONAL_LS = []

MENUITEMSDATA.append(MenuItemData(
    name="alpha",
    icon_l=LGREEK + UGREEK + VGREEK + HEBREW + MISC))

# MENUITEMSDATA.append(MenuItemData(
#     name="frac",
#     icon_l=MATHCONSTRUCTS))

# ADDITIONAL_LS += SINGLEDELIMITERS
#
# MENUITEMSDATA.append(MenuItemData(
#     name="tab_delimiters",
#     icon_l=DELIMITERS))
#
# MENUITEMSDATA.append(MenuItemData(
#     name="tab_functions",
#     icon_l=FUNCTIONS))
#
# MENUITEMSDATA.append(MenuItemData(
#     name="tab_variablesize",
#     icon_l=VARIABLESIZE))

MENUITEMSDATA.append(MenuItemData(
    name="times",
    icon_l=BINOPS))

MENUITEMSDATA.append(MenuItemData(
    name="rightarrow",
    icon_l=ARROWS))

#ADDITIONAL_LS += COLORS
#
# MENUITEMSDATA.append(MenuItemData(
#     name="tab_text",
#     icon_l=TEXT))
#
# ADDITIONAL_LS += MATRIXTYPES
#
# MENUITEMSDATA.append(MenuItemData(
#     name="tab_manylines",
#     icon_l=MANYLINES))
#
# MENUITEMSDATA.append(MenuItemData(
#     name="tab_accents",
#     icon_l=ACCENTS))
