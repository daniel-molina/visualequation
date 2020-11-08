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

from enum import Enum, auto

from .ops import PseudoSymb


def _class_gen(short_cls_name, enum_class):
    """Return a class for PseudoSymbols grouped in an Enum.

    It checks if the name of the items finish at "_U" and manages it
    consequently.

    Implementation note:
        When Enums are iterated it is done independently of element values.
        If extending an Enum with new PSs and caring about compatibility of
        JSON in exported equations:

            *   Include new PSs at the bottom, which could be a mess if you
                want it to be represented in another position.
            *   Set values manually, removing the auto().
    """
    class PSAux(PseudoSymb):
        ENUM_CLASS = enum_class

        def __init__(self, ps, **kwargs):
            if not isinstance(ps, self.ENUM_CLASS):
                raise TypeError("Invalid parameter ps.")
            self.ps = ps
            super().__init__(ps.latex(), **kwargs)

        @classmethod
        def from_json(cls, dct):
            return cls(cls.ENUM_CLASS(dct["n"]), pp=dct["pp"])

        def to_json(self):
            return dict(cls=short_cls_name, n=self.ps.value,
                        pp=self.pp.to_json())
    return PSAux


class MiscE(Enum):
    INFTY = auto()
    EMPTYSET = auto()
    VARNOTHING = auto()
    DAGGER = auto()
    DDAGGER = auto()
    WR = auto()
    CLUBSUIT = auto()
    DIAMONDSUIT = auto()
    HEARTSUIT = auto()
    SPADESUIT = auto()
    POUNDS = auto()
    P_U = auto()
    S_U = auto()

    def latex(self):
        if self.name[-2:] == "_U":
            return "\\" + self.name.capitalize()[:-2]
        else:
            return "\\" + self.name.lower()


Misc = _class_gen("MI", MiscE)


class ArrowsE(Enum):
    LEFTARROW = auto()
    LONGLEFTARROW = auto()
    LEFTARROW_U = auto()
    LONGLEFTARROW_U = auto()
    RIGHTARROW = auto()
    LONGRIGHTARROW = auto()
    RIGHTARROW_U = auto()
    LONGRIGHTARROW_U = auto()
    LEFTRIGHTARROW = auto()
    LONGLEFTRIGHTARROW = auto()
    LEFTRIGHTARROW_U = auto()
    LONGLEFTRIGHTARROW_U = auto()
    UPARROW = auto()
    UPARROW_U = auto()
    DOWNARROW = auto()
    DOWNARROW_U = auto()
    UPDOWNARROW = auto()
    UPDOWNARROW_U = auto()
    MAPSTO = auto()
    LONGMAPSTO = auto()
    RIGHTARROW_NU = auto()
    LEFTARROW_NU = auto()
    LEFTRIGHTARROW_NU = auto()
    NLEFTARROW = auto()
    NRIGHTARROW = auto()
    NLEFTRIGHTARROW = auto()
    NEARROW = auto()
    SEARROW = auto()
    SWARROW = auto()
    NWARROW = auto()
    DIAGUP = auto()
    DIAGDOWN = auto()
    CDOTS = auto()
    VDOTS = auto()
    LDOTS = auto()
    DDOTS = auto()

    def latex(self):
        if self.name[-2:] == "_U":
            return "\\" + self.name.capitalize()[:-2]
        elif self.name[-3:] == "_NU":
            return "\\n" + self.name.capitalize()[:-3]
        else:
            return "\\" + self.name.lower()


Arrows = _class_gen("Ar", ArrowsE)


class SomeOperatorsE(Enum):
    NABLA = auto()
    PARTIAL = auto()
    TIMES = auto()
    CDOT = auto()
    CENTERDOT = auto()
    DIV = auto()
    CIRC = auto()
    BIGCIRC = auto()
    BULLET = auto()
    DIAMOND = auto()
    CHECKMARK = auto()
    MALTESE = auto()
    STAR = auto()
    PM = auto()
    MP = auto()
    AMALG = auto()
    ODOT = auto()
    OMINUS = auto()
    OPLUS = auto()
    OSLASH = auto()
    OTIMES = auto()
    SQUARE = auto()
    BOXDOT = auto()
    BOXMINUS = auto()
    BOXPLUS = auto()
    BOXTIMES = auto()
    NPLUS = auto()
    UPLUS = auto()
    CAP = auto()
    CUP = auto()
    SQCAP = auto()
    SQCUP = auto()
    WEDGE = auto()
    VEE = auto()
    FORALL = auto()
    EXISTS = auto()
    NEXISTS = auto()

    def latex(self):
        return "\\" + self.name.lower()


SomeOperators = _class_gen("SO", SomeOperatorsE)


class RelationsE(Enum):
    PERP = auto()
    PARALLEL = auto()
    EQUIV = auto()
    LESS = auto()
    GREATER = auto()
    LEQ = auto()
    GEQ = auto()
    LL = auto()
    GG = auto()
    PREC = auto()
    SUCC = auto()
    PRECEQ = auto()
    SUCCEQ = auto()
    SIM = auto()
    CONG = auto()
    SIMEQ = auto()
    APPROX = auto()
    ASYMP = auto()
    LLL = auto()
    GGG = auto()
    DOTEQ = auto()
    TRIANGLEQ = auto()
    CIRCEQ = auto()
    PROPTO = auto()
    SUBSET = auto()
    SUPSET = auto()
    SUBSETEQ = auto()
    SUPSETEQ = auto()
    SQSUBSET = auto()
    SQSUPSET = auto()
    SQSUBSETEQ = auto()
    SQSUPSETEQ = auto()
    DASHV = auto()
    VDASH = auto()
    MODELS = auto()
    SMILE = auto()
    FROWN = auto()
    IN = auto()
    NI = auto()
    NOTIN = auto()
    NEQ = auto()
    NEG = auto()
    NCONG = auto()
    NSIM = auto()
    NPARALLEL = auto()
    NOTPERP = auto()
    NLESS = auto()
    NGTR = auto()
    NLEQ = auto()
    NGEQ = auto()
    LNEQ = auto()
    GNEQ = auto()
    NSUBSETEQ = auto()
    NSUPSETEQ = auto()
    SUBSETNEQ = auto()
    SUPSETNEQ = auto()
    NPREC = auto()
    NSUCC = auto()
    NPRECEQ = auto()
    NSUCCEQ = auto()

    def latex(self):
        return "\\" + self.name.lower()


Relations = _class_gen("Re", RelationsE)
