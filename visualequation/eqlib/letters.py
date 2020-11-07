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

from .ops import PseudoSymb
from visualequation.symbols.utils import *

# If associated tuple has one element, Greek letter has a characteristic
# capital letter.
# Elif second element of associated tuple is None, capital letter of the key
# must be used for the Greek letter.
# Else, capital of the second element must be used as capital of the Greek
# letter.
LATIN_DICT = {
    'a': ('alpha', None),
    'b': ('beta', None),
    'c': ('chi', 'x'),
    'd': ('delta',),
    'e': ('epsilon', None),
    'f': ('phi',),
    'g': ('gamma',),
    'h': ('eta', None),
    'i': ('iota', None),
    'j': None,
    'k': ('kappa', None),
    'l': ('lambda',),
    'm': ('mu', None),
    'n': ('nu', None),
    'o': ('omega',),
    'p': ('pi',),
    'q': ('theta',),
    'r': ('rho', 'p'),
    's': ('sigma',),
    't': ('tau', None),
    'u': ('upsilon',),
    'v': None,
    'w': None,
    'x': ('xi',),
    'y': ('psi',),
    'z': ('zeta', None),
}

GREEK_DICT = {v[0]: k for k, v in LATIN_DICT.items() if v is not None}

VGREEK_TPL = (
    'epsilon',
    'phi',
    'gamma',  # Special case, LaTeX code is prefixed with 'di'
    'kappa',
    'pi',
    'theta',
    'rho',
    'sigma',
)

HEBREW_DICT = {
    'aleph': 'a',
    'beth': 'b',
    'daleth': 'd',
    'gimel': 'g',
}


def has_greek_equiv(c):
    """Return whether a Latin character has an equivalent Greek character."""
    return c in LATIN_DICT and LATIN_DICT[c] is not None


def has_greek_with_variant(c):
    """Return whether a Latin character has an equivalent Greek letter with
    variant."""
    return has_greek_equiv(c) and LATIN_DICT[c][0] in VGREEK_TPL


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
    def __init__(self, greek_letter, upper=False, variant=False, **kwargs):
        if not isinstance(greek_letter, str):
            raise TypeError("Parameter greek_letter must be a str.")
        if greek_letter not in GREEK_DICT:
            raise ValueError("Parameter greek_letter is not valid.")
        if not isinstance(upper, bool):
            raise TypeError("Parameter upper must be a bool.")
        if not isinstance(variant, bool):
            raise TypeError("Parameter variant must be a bool.")
        if variant and (upper or greek_letter not in VGREEK_TPL):
            raise ValueError("Specified Greek letter has not a variant.")

        self._latin = GREEK_DICT[greek_letter]
        self._upper = upper
        self._variant = variant
        if upper:
            latex = self.latex_upper(self._latin)
        elif variant:
            latex = self.latex_variant(self._latin)
        else:
            latex = self.latex_lower(self._latin)
        super().__init__("\\" + latex, **kwargs)

    @classmethod
    def latex_lower(cls, latin_letter: str):
        """Return latex code of the lower case of a Greek letter.

        .. note::
            Backslash is not included.
        """
        v = LATIN_DICT[latin_letter]
        if v is None:
            raise ValueError("Specified letter has not a Greek equivalent.")
        return v[0]

    @classmethod
    def latex_upper(cls, latin_letter: str):
        """Return latex code of the upper case of a Greek letter.

        .. note::
            Backslash is not included.
        """
        v = LATIN_DICT[latin_letter]
        if v is None:
            raise ValueError("Specified letter has not a Greek equivalent.")
        if len(v) == 1:
            return v[0].capitalize()
        elif v[1] is None:
            return latin_letter.upper()
        else:
            return v[1].upper()

    @classmethod
    def latex_variant(cls, latin_letter: str):
        """Return latex code of the variant of a Greek letter.

        .. note::
            Backslash is not included.
        """
        v = LATIN_DICT[latin_letter]
        if v is None:
            raise ValueError("Specified letter has not a Greek equivalent.")
        if v[0] not in VGREEK_TPL:
            raise ValueError("Specified letter does not accept a variant.")
        if latin_letter == "g":
            return "digamma"
        return "var" + v[0]

    def upper(self):
        self._latex_code = "\\" + self.latex_upper(self._latin)
        self._upper = True
        self._variant = False

    def lower(self):
        self._latex_code = "\\" + self.latex_lower(self._latin)
        self._upper = False
        self._variant = False

    def variant(self):
        self._latex_code = "\\" + self.latex_variant(self._latin)
        self._upper = False
        self._variant = True

    def has_variant(self):
        return GREEK_DICT[self._latin][0] in VGREEK_TPL

    @classmethod
    def from_json(cls, dct):
        s = dct["s"]
        return cls(LATIN_DICT[s[0]], s[1:] == "C", s[1:] == "v", pp=dct["pp"])

    def to_json(self):
        s = self._latin
        if self._variant:
            s += "v"
        elif self._upper:
            s += "C"
        return dict(cls="G", s=s, pp=self.pp.to_json())

    @classmethod
    def from_str(cls, lower_letter: str, upper=False, variant=False, **kwargs):
        if lower_letter not in LATIN_DICT:
            raise ValueError("Invalid lower_letter value.")
        v = LATIN_DICT[lower_letter]
        if v is None:
            raise ValueError("Passed lower_letter has not a Greek equivalent.")
        return Greek(v[0], upper, variant, **kwargs)

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


class Hebrew(PseudoSymb):
    def __init__(self, hebrew_letter: str, **kwargs):
        if not isinstance(hebrew_letter, str):
            raise TypeError("Parameter hebrew_letter must be a str.")
        if hebrew_letter not in HEBREW_DICT:
            raise ValueError("Parameter hebrew_letter is not valid.")

        super().__init__("\\" + hebrew_letter, **kwargs)

    @classmethod
    def from_json(cls, dct):
        letter = next(k for k, v in HEBREW_DICT.items() if v == dct["c"])
        return cls(letter, pp=dct["pp"])

    def to_json(self):
        return dict(cls="H", c=HEBREW_DICT[self._latex_code[1:]],
                    pp=self.pp.to_json())


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
