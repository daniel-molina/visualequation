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

"""A module to define Latin, Greek and Hebrew letters. Also digits.

.. note::
    Implementation note: Maybe dicts and tuples could be integrated with icons?
"""

from typing import Union
from enum import Enum, auto

from .ops import PseudoSymb
from visualequation.icons import icon_class


@icon_class
class GreekE(Enum):
    ALPHA = auto()
    BETA = auto()
    CHI = auto()
    DELTA = auto()
    EPSILON = auto()
    PHI = auto()
    GAMMA = auto()
    ETA = auto()
    IOTA = auto()
    KAPPA = auto()
    LAMBDA = auto()
    MU = auto()
    NU = auto()
    OMEGA = auto()
    PI = auto()
    THETA = auto()
    RHO = auto()
    SIGMA = auto()
    TAU = auto()
    UPSILON = auto()
    XI = auto()
    PSI = auto()
    ZETA = auto()


@icon_class
class UGreekE(Enum):
    DELTA_U0 = auto()
    PHI_U0 = auto()
    GAMMA_U0 = auto()
    LAMBDA_U0 = auto()
    OMEGA_U0 = auto()
    PI_U0 = auto()
    THETA_U0 = auto()
    SIGMA_U0 = auto()
    UPSILON_U0 = auto()
    XI_U0 = auto()
    PSI_U0 = auto()


@icon_class
class VGreekE(Enum):
    VAREPSILON = auto()
    VARPHI = auto()
    DIGAMMA = auto()
    VARKAPPA = auto()
    VARPI = auto()
    VARTHETA = auto()
    VARRHO = auto()
    VARSIGMA = auto()


@icon_class
class HebrewE(Enum):
    ALEPH = auto()
    BETH = auto()
    DALETH = auto()
    GIMEL = auto()


# A None value means that Latin letter has no Greek equivalent.
# Second element of the tuple value represents the capital letter of associated
# Greek letter. If it is None, the capital letter of the Latin letter is used.
# Elif it is a str, the string is used instead.
LATIN_DICT = {
    'a': (GreekE.ALPHA, None, None),
    'b': (GreekE.BETA, None, None),
    'c': (GreekE.CHI, 'X', None),
    'd': (GreekE.DELTA, UGreekE.DELTA_U0, None),
    'e': (GreekE.EPSILON, None, VGreekE.VAREPSILON),
    'f': (GreekE.PHI, UGreekE.PHI_U0, VGreekE.VARPHI),
    'g': (GreekE.GAMMA, UGreekE.GAMMA_U0, VGreekE.DIGAMMA),
    'h': (GreekE.ETA, None, None),
    'i': (GreekE.IOTA, None, None),
    'j': None,
    'k': (GreekE.KAPPA, None, VGreekE.VARKAPPA),
    'l': (GreekE.LAMBDA, UGreekE.LAMBDA_U0, None),
    'm': (GreekE.MU, None, None),
    'n': (GreekE.NU, None, None),
    'o': (GreekE.OMEGA, UGreekE.OMEGA_U0, None),
    'p': (GreekE.PI, UGreekE.PHI_U0, VGreekE.VARPI),
    'q': (GreekE.THETA, UGreekE.THETA_U0, VGreekE.VARTHETA),
    'r': (GreekE.RHO, 'P', VGreekE.VARRHO),
    's': (GreekE.SIGMA, UGreekE.SIGMA_U0, VGreekE.VARSIGMA),
    't': (GreekE.TAU, None, None),
    'u': (GreekE.UPSILON, UGreekE.UPSILON_U0, None),
    'v': None,
    'w': None,
    'x': (GreekE.XI, UGreekE.XI_U0, None),
    'y': (GreekE.PSI, UGreekE.PSI_U0, None),
    'z': (GreekE.ZETA, None, None),
}

GREEK_DICT = {v[0]: k for k, v in LATIN_DICT.items() if v is not None}

# Note: To be moved to a test
assert len(GREEK_DICT) == len(GreekE)


def has_greek_equiv(latin_char):
    """Return whether a Latin character has an equivalent Greek character."""
    return latin_char in LATIN_DICT and LATIN_DICT[latin_char] is not None


def has_greek_with_variant(latin_char):
    """Return whether a Latin character has an equivalent Greek letter with
    variant."""
    return has_greek_equiv(latin_char) \
        and LATIN_DICT[latin_char][2] is not None


class Latin(PseudoSymb):
    def __init__(self, char: str, upper=False, **kwargs):
        if not isinstance(char, str):
            raise TypeError("Parameter char must be a str.")
        if char not in LATIN_DICT:
            raise ValueError("Parameter char is not in [a-z].")
        if not isinstance(upper, bool):
            raise TypeError("Parameter upper must be a bool.")

        self._upper = upper
        super().__init__(char.upper() if upper else char, **kwargs)

    @classmethod
    def from_json(cls, dct):
        c = dct["c"]
        return cls(c.lower(), c.isupper(), pp=dct["pp"])

    def to_json(self):
        return dict(cls="L", pp=self.pp.to_json(), c=self._latex_code)

    def upper(self):
        self._latex_code = self._latex_code.upper()
        self._upper = True

    def lower(self):
        self._latex_code = self._latex_code.lower()
        self._upper = False

    @classmethod
    def from_greek(cls, g: 'Greek'):
        """Return an instance of Latin from a Greek instance.

        It is simpler to implement than to_greek."""
        return Latin(g._latin, g._upper, pp=g.pp)


class Greek(PseudoSymb):
    def __init__(self, greek_letter: GreekE, upper=False, variant=False,
                 **kwargs):
        """Only GreekE are allowed so capital letters with no specific LaTeX
        code can be also managed.
        """
        if not isinstance(greek_letter, GreekE):
            raise TypeError("Parameter greek_letter must be a GreekE.")
        self._latin = GREEK_DICT[greek_letter]
        if not isinstance(upper, bool):
            raise TypeError("Parameter upper must be a bool.")
        if not isinstance(variant, bool):
            raise TypeError("Parameter variant must be a bool.")
        if variant and upper:
            raise ValueError("Parameters variant and upper are "
                             "mutually exclusive.")
        if variant and self.vgreek_latex(self._latin) is None:
            raise ValueError("Specified Greek letter has not a variant.")
        self._upper = upper
        self._variant = variant
        if upper:
            super().__init__(LATIN_DICT[self._latin][1].latex(), **kwargs)
        elif variant:
            super().__init__(LATIN_DICT[self._latin][2].latex(), **kwargs)
        else:
            super().__init__(greek_letter.latex(), **kwargs)

    @classmethod
    def greek_latex(cls, latin_letter: str):
        """Return LaTeX code of Greek letter associated to a lowercase Latin
        letter.

        If such Greek letter does not exist, return None.
        """
        if latin_letter not in LATIN_DICT:
            return
        v = LATIN_DICT[latin_letter]
        if v is not None:
            return v[0].latex()

    @classmethod
    def ugreek_latex(cls, latin_letter: str):
        """Return LaTeX code of the capital Greek letter associated to a
        lowercase Latin letter.

        If such Greek letter does not exist, return None.
        """
        if latin_letter not in LATIN_DICT:
            return
        v = LATIN_DICT[latin_letter]
        if v is None:
            return latin_letter.upper()
        if isinstance(v[1], str):
            return v[1]
        return v[1].latex()

    @classmethod
    def vgreek_latex(cls, latin_letter: str):
        """Return LaTeX code of the variant of a Greek letter associated to a
        lowercase Latin letter.

        If such Greek letter does not exist, return None.
        """
        if latin_letter not in LATIN_DICT:
            return
        v = LATIN_DICT[latin_letter]
        if v is not None and v[2] is not None:
            return v[2].latex()

    def upper(self):
        self._latex_code = self.ugreek_latex(self._latin)
        self._upper = True
        self._variant = False

    def lower(self):
        self._latex_code = self.greek_latex(self._latin)
        self._upper = False
        self._variant = False

    def has_variant(self):
        return self.vgreek_latex(self._latin) is not None

    def variant(self):
        latex_code = self.vgreek_latex(self._latin)
        if latex_code is None:
            raise ValueError("Requested variant does not exist.")
        self._latex_code = latex_code
        self._upper = False
        self._variant = True

    @classmethod
    def from_str(cls, latin_letter: str, upper=False, variant=False,
                 **kwargs):
        """Return an instance of Greek from a string with a lowercase Latin."""
        if latin_letter not in LATIN_DICT:
            raise ValueError("Invalid latin_letter value.")
        v = LATIN_DICT[latin_letter]
        if v is None:
            raise ValueError("Passed latin_letter has not a Greek equivalent.")
        return cls(v[0], upper, variant, **kwargs)

    @classmethod
    def from_latin(cls, latin: Latin, variant=False, **kwargs):
        """Return an instance of Greek from a Latin instance.

        .. note::
            An upper/lower Latin instance will force an upper/lower Greek
            instance.
        """
        v = LATIN_DICT[latin._latex_code.lower()]
        if v is None:
            raise ValueError("Passed Latin has not a Greek equivalent.")
        return Greek(v[0], latin._upper, variant, **kwargs)

    @classmethod
    def from_json(cls, dct):
        s = dct["s"]
        return cls(LATIN_DICT[s[0]], s[1:] == "U", s[1:] == "V", pp=dct["pp"])

    def to_json(self):
        s = self._latin
        if self._variant:
            s += "V"
        elif self._upper:
            s += "U"
        return dict(cls="G", s=s, pp=self.pp.to_json())


class Hebrew(PseudoSymb):
    def __init__(self, hebrew_letter: HebrewE, **kwargs):
        if not isinstance(hebrew_letter, HebrewE):
            raise TypeError("Parameter hebrew_letter must be a HebrewE.")

        self._letter = hebrew_letter
        super().__init__(hebrew_letter.latex(), **kwargs)

    @classmethod
    def from_json(cls, dct):
        return cls(HebrewE(dct["n"]), pp=dct["pp"])

    def to_json(self):
        return dict(cls="H", n=self._letter.value, pp=self.pp.to_json())


class Digit(PseudoSymb):
    def __init__(self, digit_str, **kwargs):
        if not isinstance(digit_str, str):
            raise TypeError("Parameter digit_str must be a str.")
        if digit_str not in (str(n) for n in range(0, 10)):
            raise ValueError("Parameter digit_str is not in [0-9].")
        super().__init__(digit_str, **kwargs)

    @classmethod
    def from_json(cls, dct):
        return cls(str(dct["n"]), pp=dct["pp"])

    def to_json(self):
        return dict(cls="D", n=int(self._latex_code), pp=self.pp.to_json())
