#  visualequation is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  visualequation is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

#  visualequation is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  visualequation is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

from typing import List, Union, Iterable, Optional

class Op:
    """Class for primitive elements of an equation."""

    def __init__(self, name: str, latex_code: str, n_args = 0,
                 type_: Optional[str] = None):
        self.name = name
        self.latex_code = latex_code
        self.n_args = n_args
        self.type_ = type_ if type_ is not None else ""

    def __eq__(self, other):
        if type(self) is type(other):
            return self.__dict__ == other.__dict__
        else:
            return NotImplemented

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        if self.type_ == '' and not self.n_args:
            return "Op(" + repr(self.name) + ", " + repr(self.latex_code) + ")"
        if self.type_ == '':
            return "Op(" + repr(self.name) + ", " + repr(self.latex_code) \
                   + ", " + repr(self.n_args) + ")"
        return "Op(" + repr(self.name) + ", " + repr(self.latex_code) \
               + ", " + repr(self.n_args) + ", " + repr(self.type_) + ")"

    def __str__(self):
        return self.name.upper()

    def __hash__(self):
        # str(self) would be enough
        return hash(repr(self))


SELARG = Op("selarg", r'\cdots')
PVOID = Op("pvoid", r'\begingroup\color{purple}\oblong\endgroup')
TVOID = Op("tvoid", r'\begingroup\color{lightgray}\oblong\endgroup')

REDIT = Op("redit", r'\left\lmoustache {0} \right\rgroup', 1)  # right
LEDIT = Op("ledit", r'\left\lgroup {0} \right\rmoustache', 1)  # left
NEDIT = Op("nedit", r'\left\lmoustache {0} \right\rmoustache', 1)  # new
SEDIT = Op("sedit", r'\left\rmoustache {0} \right\lmoustache', 1)  # substitute
PJUXT = Op("pjuxt", r'', -1)
TJUXT = Op("tjuxt", r'', -1)
GOP = Op("gop", r'{0}', 1)
