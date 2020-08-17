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

class Op:
    """Class for primitive elements of an equation."""

    def __init__(self, name, latex_code, n_args = 0, type_=None):
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
        return "Op(" + repr(self.name) + ", " + repr(self.n_args) \
               + ", " + repr(self.latex_code) + ", " + repr(self.type_) + ")"

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(repr(self))


SELARG = Op("selarg", r'\cdots')
VOID = Op("void", r'\begingroup\color{purple}\oblong\endgroup')
TVOID = Op("tvoid", r'\begingroup\color{lightgray}\oblong\endgroup')

REDIT = Op("redit", r'\left\lmoustache {0} \right\rgroup', 1)  # right
LEDIT = Op("ledit", r'\left\lgroup {0} \right\rmoustache', 1)  # left
NEDIT = Op("nedit", r'\left\lmoustache {0} \right\rmoustache', 1)  # new
SEDIT = Op("sedit", r'\left\rmoustache {0} \right\lmoustache', 1)  # substitute
JUXT = Op("juxt", r'J', -1)
TJUXT = Op("tjuxt", r'T', -1)
GOP = Op("gop", r'{0}', 1)

NONUOPS = (GOP,)
