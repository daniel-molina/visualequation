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

from .ops import PseudoSymb, CCls
from visualequation.icons import icon_class


def _class_gen(short_cls_name, enum_class, ccls: CCls = CCls.ORD):
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
            super().__init__(ps.latex(), ccls, **kwargs)

        @classmethod
        def from_json(cls, dct):
            return cls(cls.ENUM_CLASS(dct["n"]), pp=dct["pp"])

        def to_json(self):
            return dict(cls=short_cls_name, n=self.ps.value,
                        pp=self.pp.to_json())
    return PSAux


@icon_class
class AlphabSymbE(Enum):
    COMPLEMENT = auto()
    ELL = auto()
    ETH = auto()
    HBAR = auto()
    HSLASH = auto()
    MHO = auto()
    PARTIAL = auto()
    WP = auto()
    COPYRIGHT = auto()
    CIRCLEDR_N0 = auto()
    CIRCLEDS_N0 = auto()
    BBBK_U0 = auto()
    FINV_U0 = auto()
    GAME_U0 = auto()
    IM_U0 = auto()
    RE_U0 = auto()
    EURO_LI = auto()
    DOLLAR_LI = auto()
    POUNDS = auto()
    YEN = auto()
    P_U0 = auto()
    S_U0 = auto()

    def latex(self):
        if self is self.EURO_LI:
            return r"\text\euro"
        if self is self.DOLLAR_LI:
            return r"\$"
        raise NotImplemented


AlphabSymb = _class_gen("AS", AlphabSymbE)


@icon_class
class MiscSimpleSymbE(Enum):
    NUMBERSIGN_LI = auto()
    AMPERSAND_LI = auto()
    UNDERSCORE_LI = auto()
    DOT_LI = auto()
    PERCENT_LI = auto()
    SLASH_LI = auto()
    VERT_LI = auto()
    PRIME = auto()  # Inserting "'" from keyboard adds \prime as script safely
    BACKSLASH = auto()

    ANGLE = auto()
    BACKPRIME = auto()
    BIGSTAR = auto()
    BLACKLOZENGE = auto()
    BLACKSQUARE = auto()
    BLACKTRIANGLE = auto()
    BLACKTRIANGLEDOWN = auto()
    BOT = auto()
    CHECKMARK = auto()
    CLUBSUIT = auto()
    DIAGDOWN = auto()
    DIAGUP = auto()
    DIAMONDSUIT = auto()
    DAG = auto()
    DDAG = auto()
    EMPTYSET = auto()
    EXISTS = auto()
    FLAT = auto()
    FORALL = auto()
    HEARTSUIT = auto()
    INFTY = auto()
    LOZENGE = auto()
    MALTESE = auto()
    MEASUREDANGLE = auto()
    NABLA = auto()
    NATURAL = auto()
    NEG = auto()
    NEXISTS = auto()
    SHARP = auto()
    SPADESUIT = auto()
    SPHERICALANGLE = auto()
    SQUARE = auto()
    SURD = auto()
    TOP = auto()
    TRIANGLE = auto()
    TRIANGLEDOWN = auto()
    VARNOTHING = auto()

    def latex(self):
        if self is self.NUMBERSIGN_LI:
            return r"\&"
        if self is self.AMPERSAND_LI:
            return r"\#"
        if self is self.UNDERSCORE_LI:
            return r"\_"
        if self is self.DOT_LI:
            return r"."
        if self is self.PERCENT_LI:
            return r"\%"
        if self is self.SLASH_LI:
            return r"/"
        if self is self.VERT_LI:
            return r"|"
        raise NotImplemented


MiscSimpleSymb = _class_gen("MS", MiscSimpleSymbE)


@icon_class
class BinOpSymbE(Enum):
    ASTERISK_LI = auto()
    PLUS_LI = auto()
    MINUS_LI = auto()
    AMALG = auto()
    AST = auto()  # completely equivalent to ASTERISK_LI ("*")
    BARWEDGE = auto()
    BIGCIRC = auto()
    BIGTRIANGLEDOWN = auto()
    BIGTRIANGLEUP = auto()
    BOXDOT = auto()
    BOXMINUS = auto()
    BOXPLUS = auto()
    BOXTIMES = auto()
    BULLET = auto()
    CAP = auto()
    CAP_U0 = auto()
    CDOT = auto()
    CENTERDOT = auto()
    CIRC = auto()
    CIRCLEDAST = auto()
    CIRCLEDCIRC = auto()
    CIRCLEDDASH = auto()
    CUP = auto()
    CUP_U0 = auto()
    CURLYVEE = auto()
    DAGGER = auto()
    DDAGGER = auto()
    DIAMOND = auto()
    DIV = auto()
    DIVIDEONTIMES = auto()
    DOTPLUS = auto()
    DOUBLEBARWEDGE = auto()
    GTRDOT = auto()
    INTERCAL = auto()
    LEFTTHREETIMES = auto()
    LESSDOT = auto()
    LTIMES = auto()
    MP = auto()
    NPLUS = auto()  # stmaryrd
    ODOT = auto()
    OMINUS = auto()
    OPLUS = auto()
    OSLASH = auto()
    OTIMES = auto()
    PM = auto()
    RIGHTTHREETIMES = auto()
    RTIMES = auto()
    SETMINUS = auto()
    SMALLSETMINUS = auto()
    SQCAP = auto()
    SQCUP = auto()
    STAR = auto()
    TIMES = auto()
    TRIANGLELEFT = auto()
    TRIANGLERIGHT = auto()
    UPLUS = auto()
    VEE = auto()
    WEDGE = auto()
    WR = auto()

    def latex(self):
        if self is self.ASTERISK_LI:
            return r"*"
        if self is self.PLUS_LI:
            return r"+"
        if self is self.MINUS_LI:
            return r"-"
        raise NotImplemented


BinOpSymb = _class_gen("BO", BinOpSymbE, CCls.BIN)


@icon_class
class RelationCompE(Enum):
    LESSTHAN_LI = auto()
    EQUAL_LI = auto()
    GREATERTHAN_LI = auto()
    APPROX = auto()
    APPROXEQ = auto()
    ASYMP = auto()
    BACKSIM = auto()
    BACKSIMEQ = auto()
    BUMPEQ = auto()
    BUMPEQ_U0 = auto()
    CIRCEQ = auto()
    CONG = auto()
    CURLYEQPREC = auto()
    CURLYEQSUCC = auto()
    DOTEQ = auto()
    DOTEQDOT = auto()
    EQCIRC = auto()
    EQSIM = auto()
    EQSLANTGTR = auto()
    EQSLANTLESS = auto()
    EQUIV = auto()
    FALLINGDOTSEQ = auto()
    GEQ = auto()
    GEQQ = auto()
    GEQSLANT = auto()
    GG = auto()
    GGG = auto()
    GNAPPROX = auto()
    GNEQ = auto()
    GNEQQ = auto()
    GNSIM = auto()
    GTRAPPROX = auto()
    GTREQLESS = auto()
    GTREQQLESS = auto()
    GTRLESS = auto()
    GTRSIM = auto()
    GVERTNEQQ = auto()
    LEQ = auto()
    LEQQ = auto()
    LEQSLANT = auto()
    LESSAPPROX = auto()
    LESSEQGTR = auto()
    LESSEQQGTR = auto()
    LESSGTR = auto()
    LESSSIM = auto()
    LL = auto()
    LLL = auto()
    LNAPPROX = auto()
    LNEQ = auto()
    LNEQQ = auto()
    LNSIM = auto()
    LVERTNEQQ = auto()
    NCONG = auto()
    NEQ = auto()
    NGEQ = auto()
    NGEQQ = auto()
    NGEQSLANT = auto()
    NGTR = auto()
    NLEQ = auto()
    NLEQQ = auto()
    NLEQSLANT = auto()
    NLESS = auto()
    NPREC = auto()
    NPRECEQ = auto()
    NSIM = auto()
    NSUCC = auto()
    NSUCCEQ = auto()
    PREC = auto()
    PRECAPPROX = auto()
    PRECCURLYEQ = auto()
    PRECEQ = auto()
    PRECNAPPROX = auto()
    PRECNEQQ = auto()
    PRECNSIM = auto()
    PRECSIM = auto()
    RISINGDOTSEQ = auto()
    SIM = auto()
    SIMEQ = auto()
    SUCC = auto()
    SUCCAPPROX = auto()
    SUCCCURLYEQ = auto()
    SUCCEQ = auto()
    SUCCNAPPROX = auto()
    SUCCNEQQ = auto()
    SUCCNSIM = auto()
    SUCCSIM = auto()
    THICKSIM = auto()
    TRIANGLEQ = auto()

    def latex(self):
        if self is self.LESSTHAN_LI:
            return r"<"
        if self is self.EQUAL_LI:
            return r"="
        if self is self.GREATERTHAN_LI:
            return r">"
        raise NotImplemented


RelationComp = _class_gen("Co", RelationCompE, CCls.REL)


@icon_class
class RelationArrowE(Enum):
    CIRCLEARROWLEFT = auto()
    CIRCLEARROWRIGHT = auto()
    CURVEARROWLEFT = auto()
    CURVEARROWRIGHT = auto()
    DOWNDOWNARROWS = auto()
    DOWNHARPOONLEFT = auto()
    DOWNHARPOONRIGHT = auto()
    HOOKLEFTARROW = auto()
    HOOKRIGHTARROW = auto()
    LEFTARROW = auto()
    LEFTARROWTAIL = auto()
    LEFTARROW_U0 = auto()
    LEFTHARPOONDOWN = auto()
    LEFTHARPOONUP = auto()
    LEFTLEFTARROWS = auto()
    LEFTRIGHTARROW = auto()
    LEFTRIGHTARROWS = auto()
    LEFTRIGHTARROW_U0 = auto()
    LEFTRIGHTHARPOONS = auto()
    LEFTRIGHTSQUIGARROW = auto()
    LLEFTARROW_U0 = auto()
    LONGLEFTARROW = auto()
    LONGLEFTARROW_U0 = auto()
    LONGLEFTRIGHTARROW = auto()
    LONGLEFTRIGHTARROW_U0 = auto()
    LONGMAPSTO = auto()
    LONGRIGHTARROW = auto()
    LONGRIGHTARROW_U0 = auto()
    LOOPARROWLEFT = auto()
    LOOPARROWRIGHT = auto()
    LSH_U0 = auto()
    MAPSTO = auto()
    MULTIMAP = auto()
    NEARROW = auto()
    NLEFTARROW = auto()
    NLEFTARROW_U1 = auto()
    NLEFTRIGHTARROW = auto()
    NLEFTRIGHTARROW_U1 = auto()
    NRIGHTARROW = auto()
    NRIGHTARROW_U1 = auto()
    NWARROW = auto()
    RIGHTARROW = auto()
    RIGHTARROWTAIL = auto()
    RIGHTARROW_U0 = auto()
    RIGHTHARPOONDOWN = auto()
    RIGHTHARPOONUP = auto()
    RIGHTLEFTARROWS = auto()
    RIGHTLEFTHARPOONS = auto()
    RIGHTRIGHTARROWS = auto()
    RIGHTSQUIGARROW = auto()
    RRIGHTARROW_U0 = auto()
    RSH_U0 = auto()
    SEARROW = auto()
    SWARROW = auto()
    TWOHEADLEFTARROW = auto()
    TWOHEADRIGHTARROW = auto()
    UPHARPOONLEFT = auto()
    UPHARPOONRIGH = auto()
    UPUPARROWS = auto()


RelationArrow = _class_gen("Ar", RelationArrowE, CCls.REL)


@icon_class
class RelationMiscE(Enum):
    COLON_LI = auto()

    BACKEPSILON = auto()
    BECAUSE = auto()
    BETWEEN = auto()
    BLACKTRIANGLELEFT = auto()
    BLACKTRIANGLERIGHT = auto()
    BOWTIE = auto()
    DASHV = auto()
    FROWN = auto()
    IN = auto()
    MID = auto()
    MODELS = auto()
    NI = auto()
    NMID = auto()
    NOTIN = auto()
    NPARALLEL = auto()
    NSHORTMID = auto()
    NSHORTPARALLEL = auto()
    NSUBSETEQ = auto()
    NSUBSETEQQ = auto()
    NSPSETEQ = auto()
    NSUPSETEQQ = auto()
    NTRIANGLELEFT = auto()
    NTRIANGLELEFTEQ = auto()
    NTRIANGLERIGHT = auto()
    NTRIANGLERIGHTEQ = auto()
    NVDASH = auto()
    NVDASH_U2 = auto()
    NVDASH_LI = auto()
    PARALLEL = auto()
    PERP = auto()
    PITCHFORK = auto()
    PROPTO = auto()
    SHORTMID = auto()
    SHORTPARALLEL = auto()
    SMALLFROWN = auto()
    SMALLSMILE = auto()
    SMILE = auto()
    SQSUBSET = auto()
    SQSUBSETEQ = auto()
    SQSUPSET = auto()
    SQSUPSETEQ = auto()
    SUBSET = auto()
    SUBSET_U0 = auto()
    SUBSETEQ = auto()
    SUBSETEQQ = auto()
    SUBSETNEQ = auto()
    SUBSETNEQQ = auto()
    SUPSET = auto()
    SUPSET_U0 = auto()
    SUPSETEQ = auto()
    SUPSETEQQ = auto()
    SUPSETNEQ = auto()
    SUPSETNEQQ = auto()
    THEREFORE = auto()
    TRIANGLELEFTEQ = auto()
    TRIANGLERIGHTEQ = auto()
    VARPROPTO = auto()
    VARSUBSETNEQ = auto()
    VARSUBSETNEQQ = auto()
    VARSUPSETNEQ = auto()
    VARSUPSETNEQQ = auto()
    VARTRIANGLE = auto()
    VARTRIANGLELEFT = auto()
    VARTRIANGLERIGHT = auto()
    VDASH = auto()
    VDASH_U0 = auto()
    VDASH_U1 = auto()
    VVDASH_U0 = auto()

    def latex(self):
        if self is self.COLON_LI:
            return r":"
        if self is self.NVDASH_LI:
            return r"\nVDash"
        raise NotImplemented


RelationMisc = _class_gen("RM", RelationMiscE, CCls.REL)


@icon_class
class DotsInnerE(Enum):
    DOTSC = auto()
    DOTSB = auto()
    DOTSM = auto()
    DOTSI = auto()
    DOTSO = auto()
    DDOTS = auto()


DotsInner = _class_gen("Di", DotsInnerE, CCls.INNER)


@icon_class
class DotsOrdE(Enum):
    VDOTS = auto()


DotsOrd = _class_gen("Do", DotsOrdE, CCls.ORD)


@icon_class
class OpenSymbE(Enum):
    LPAR_LI = auto()
    LBRACE_LI = auto()
    LBRACKET_LI = auto()

    def latex(self):
        if self is self.LPAR_LI:
            return r"("
        if self is self.LBRACE_LI:
            return r"["
        if self is self.LBRACKET_LI:
            return r"\{"
        raise NotImplemented


OpenSymb = _class_gen("Op", OpenSymbE, CCls.OPEN)


@icon_class
class CloseSymbE(Enum):
    RPAR_LI = auto()
    RBRACE_LI = auto()
    RBRACKET_LI = auto()
    EXCL_LI = auto()
    QUEST_LI = auto()

    def latex(self):
        if self is self.RPAR_LI:
            return r")"
        if self is self.RBRACE_LI:
            return r"]"
        if self is self.RBRACKET_LI:
            return r"\}"
        if self is self.EXCL_LI:
            return r"!"
        if self is self.QUEST_LI:
            return r"?"
        raise NotImplemented


CloseSymb = _class_gen("Cl", CloseSymbE, CCls.CLOSE)


@icon_class
class PunctE(Enum):
    COMMA_LI = auto()
    SEMICOLON_LI = auto()
    COLON = auto()

    def latex(self):
        if self is self.COMMA_LI:
            return r","
        if self is self.SEMICOLON_LI:
            return r";"
        raise NotImplemented


Punct = _class_gen("Pu", PunctE, CCls.PUNCT)
