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

import unittest

from copy import deepcopy
from visualequation.dirsel import Dir
from visualequation.ops import *
from visualequation.eqedit import EditableEq
from visualequation.scriptops import *


class Eq(EditableEq):
    DEFAULT_METHOD_RETVAL = 88

    """Dummy class to avoid debugging messages when testing."""
    def __init__(self, eq0=None, sel_index0=None, dir0=None):
        super().__init__(eq0, sel_index0, dir0, debug=False)

    def default_eq(self):
        self[:] = [PVOID]
        self.idx[:] = []
        self.dir = Dir.V
        return self.DEFAULT_METHOD_RETVAL


SCRIPT_OPS_LIST = [op for op in SCRIPT_OP2ID_DICT.keys() if op is not None]
SETSCRIPT_OPS_LIST \
    = [op for op in SETSCRIPT_OP2ID_DICT.keys() if op is not None]
LOSCRIPT_OPS_LIST \
    = [op for op in LOSCRIPT_OP2ID_DICT.keys() if op is not None]
ALL_SCRIPT_OPS_LIST = SCRIPT_OPS_LIST + SETSCRIPT_OPS_LIST + LOSCRIPT_OPS_LIST

NO_EQ_MSG = "No Eqs are available for comparison"
NoEqError = ValueError(NO_EQ_MSG)
NON_EQUAL_EQ_MSG = "Eqs do not match"
NonEqualEqError = ValueError(NON_EQUAL_EQ_MSG)
NON_EQUAL_IDX_MSG = "Indices do not match"
NonEqualIdxError = ValueError(NON_EQUAL_IDX_MSG)
NON_EQUAL_DIR_MSG = "Dirs do not match"
NonEqualDirError = ValueError(NON_EQUAL_DIR_MSG)
NON_EQUAL_RETURN_MSG = "Returned values do not match"
NoneEqualReturnError = ValueError(NON_EQUAL_RETURN_MSG)
WRONG_NUMBER_ARGS_MSG = "Wrong number of arguments"
WrongNumberArgsError = TypeError(WRONG_NUMBER_ARGS_MSG)

class CompareEqs:
    """A class to compare equations.

    By default it converts subeqs to EditableEqs if they are already not
    EditableEq. That can be avoided by passing the keyword force_subeq=True. In
    that case Subeqs are created. Every subeq passed should belong to the same
    class: This class is not intended to be bullet-proof by the moment, so take
    care.

    'Input equations' will be transformed by a function or method in a call
    to the assert_equality method and compared with 'output equations'.
    Input and output equations to be compared must be previously provided
    through the constructor or the rest of the methods available, not
    necessarily at once or strictly before a first assert_equality call.

    If 'retvals' are provided and assert_equality's comparison refers to a
    method, returned values of the methods are compared with it.

    Other specific comparison options can be set with assert_equality keywords.

    If a comparison reveals a non-equality, a specific error is raised.
    """
    def add_pair(self, eq_in, eq_out, retval=None, force_subeq=False):
        """Add a pair of input and output eq."""
        if retval is not None:
            self.expected_retvals.append(retval)

        if force_subeq:
            self.eq_in.append(Subeq(eq_in))
            self.eq_out.append(Subeq(eq_out))
        elif not isinstance(eq_in, EditableEq):
            self.eq_in.append(Eq(eq_in))
            self.eq_out.append(Eq(eq_out))
        else:
            # Current EditableEq-ctor would remove idx and dir info if a
            # member of its class is passed as argument
            self.eq_in.append(eq_in)
            self.eq_out.append(eq_out)

    def add_many(self, many_eq_in, many_eq_out, retvals=None,
                 force_subeq=False):
        """Add many input and output eqs"""
        if retvals is not None:
            self.expected_retvals.extend(retvals)

        if force_subeq:
            self.eq_in.extend((Subeq(e) for e in many_eq_in))
            self.eq_out.extend((Subeq(e) for e in many_eq_out))
        elif not isinstance(many_eq_in[0], EditableEq):
            self.eq_in.extend((Eq(e) for e in many_eq_in))
            self.eq_out.extend((Eq(e) for e in many_eq_out))
        else:
            # Current EditableEq-ctor would remove idx and dir info if a
            # member of its class is passed as argument
            self.eq_in.extend(many_eq_in)
            self.eq_out.extend(many_eq_out)

    def add_unzipping(self, eq_iter, force_subeq=False):
        """It accepts an iterable which elements are 2-tuples or 3-tuples."""
        for e in eq_iter:
            self.add_pair(*e, force_subeq=force_subeq)

    def __init__(self, *args, **kwargs):
        """It accepts 2 or 3 iterables or a block of 2-tuples or 3 tuples."""
        self.eq_in = []
        self.eq_out = []
        self.expected_retvals = []

        if len(args) == 1:
            self.add_unzipping(*args, **kwargs)
        elif len(args) > 1:
            self.add_many(*args, **kwargs)

    @staticmethod
    def print_debug_message(l_pos, l_val, l_correct, eqs1, eqs2, inversely):
        terminal_cols = 79
        arrow_len = 8

        def eq2text(eq):
            eq_srepr = str(eq)
            if isinstance(eq, EditableEq):
                tail_str = str(eq.idx) + ", " + eq.dir.name
            else:
                tail_str = ""

            others_len = 1  # ","
            data_len = len(eq_srepr + tail_str)

            free_space = terminal_cols - arrow_len - others_len - data_len
            if free_space > 1:
                retval = "\n\033[93m" + (arrow_len - 1) * ">" + "\033[0m "
                retval += "\033[1m" + eq_srepr + "\033[0m"
                if tail_str:
                    retval += "," + free_space * " " + tail_str
                return retval

            retval = "\n\033[93m" + (arrow_len - 1) * ">" + "\033[0m "
            retval += "\033[1m" + eq_srepr + "\033[0m\n"
            if tail_str:
                retval += (terminal_cols - len(tail_str)) * " " + tail_str
            return retval

        if inversely:
            eqs1, eqs2 = eqs2, eqs1

        print("\n\033[93m>>>>>>>\033[0m",
              "Position of offending equation:\033[93m", l_pos,
              "\033[0m(positions start at 0, not 1)",
              eq2text(eqs1[l_pos]), eq2text(eqs2[l_pos]),
              "\n\033[91m" + (arrow_len - 1) * ">" \
              + "\033[0m Offending value:\033[91m", l_val,
              "\n\033[92m>>>>>>>\033[0m Expected value: \033[92m",
              l_correct, "\033[0m")

    def assert_equality(self, fun=None, is_method=True, inversely=False,
                        exclude_eq=False, exclude_idx=False, exclude_dir=False,
                        exclude_retvals=False, debug=True):
        if not self.eq_in or not self.eq_out:
            raise NoEqError

        retvals = []
        # A function or method can modify an equation: do not allow that to
        # modify self.eq_in nor self.eq_out.
        if fun is None:
            other_eqs = self.eq_in      # eqs not being compared
            correct_eqs = self.eq_in    # eqs used as reference
            calc_eqs = self.eq_out      # eqs being compared
        elif inversely:
            other_eqs = self.eq_out
            correct_eqs = self.eq_in
            if is_method:
                calc_eqs = deepcopy(self.eq_out)
                for eq in calc_eqs:
                    retvals.append(fun(eq))
            else:
                calc_eqs = list(map(fun, deepcopy(self.eq_out)))
        else:
            other_eqs = self.eq_in
            correct_eqs = self.eq_out
            if is_method:
                calc_eqs = deepcopy(self.eq_in)
                for eq in calc_eqs:
                    retvals.append(fun(eq))
            else:
                calc_eqs = list(map(fun, deepcopy(self.eq_in)))

        if not exclude_eq:
            if correct_eqs != calc_eqs:
                if debug:
                    e = next((i, s) for i, s in enumerate(calc_eqs)
                             if s != correct_eqs[i])
                    self.print_debug_message(e[0], e[1], correct_eqs[e[0]],
                                             other_eqs, correct_eqs, inversely)
                raise NonEqualEqError

        if isinstance(correct_eqs[0], EditableEq) and not exclude_idx:
            if not all(map(lambda s, p: s.idx == p.idx,
                           correct_eqs, calc_eqs)):
                if debug:
                    e = next((i, s) for i, s in enumerate(calc_eqs) \
                          if s.idx != correct_eqs[i].idx)
                    self.print_debug_message(e[0], e[1].idx,
                                             correct_eqs[e[0]].idx,
                                             other_eqs, correct_eqs, inversely)
                raise NonEqualIdxError

        if isinstance(correct_eqs[0], EditableEq) and not exclude_dir:
            if not all(map(lambda s, p: s.dir is p.dir,
                           correct_eqs, calc_eqs)):
                if debug:
                    e = next((i, s) for i, s in enumerate(calc_eqs) \
                         if s.dir != correct_eqs[i].dir)
                    self.print_debug_message(e[0], e[1].dir,
                                             correct_eqs[e[0]].dir,
                                             other_eqs, correct_eqs, inversely)
                raise NonEqualDirError

        if is_method and not exclude_retvals and self.expected_retvals:
            if self.expected_retvals != retvals:
                if debug:
                    a = self.expected_retvals
                    b = retvals
                    e = next((i, v) for i, v in enumerate(b) if v != a[i])
                    self.print_debug_message(e[0], e[1], a[e[0]],
                                             other_eqs, correct_eqs, inversely)
                raise NoneEqualReturnError


class CompareEqsTests(unittest.TestCase):
    def test_add_pair(self):
        ce = CompareEqs()
        ce.add_pair(["a"], None, force_subeq=True)
        ce.add_pair(["b"], [PVOID], force_subeq=True)
        self.assertEqual(len(ce.eq_in), 2)
        self.assertEqual(len(ce.eq_out), 2)
        ce.add_pair(["a"], ["3"], force_subeq=True)
        ce.add_pair(["b"], [PVOID], force_subeq=True)
        self.assertEqual(len(ce.eq_in), 4)
        self.assertEqual(len(ce.eq_out), 4)
        for s in ce.eq_in + ce.eq_out:
            self.assertIsInstance(s, Subeq)
            self.assertNotIsInstance(s, EditableEq)

        ce = CompareEqs()
        ce.add_pair(Eq(["a"]), Eq(None))
        ce.add_pair(Eq(["b"]), Eq([PVOID]))
        self.assertEqual(len(ce.eq_in), 2)
        self.assertEqual(len(ce.eq_out), 2)
        ce.add_pair(Eq(["a"]), Eq(["3"]))
        ce.add_pair(Eq(["b"]), Eq([PVOID]))
        self.assertEqual(len(ce.eq_in), 4)
        self.assertEqual(len(ce.eq_out), 4)
        for s in ce.eq_in + ce.eq_out:
            self.assertIsInstance(s, EditableEq)

        ce.add_pair(["b"], [PVOID])
        for s in ce.eq_in + ce.eq_out:
            self.assertIsInstance(s, EditableEq)

    def test_add_many(self):
        ce = CompareEqs()
        l1 = (["a"], ["b"], [PVOID], [PJUXT, ["a"], ["b"]])
        l2 = (["x"], ["y"], [TVOID], [TJUXT, ["x"], ["y"]])
        ce.add_many(l1, l2)
        for eqs in (ce.eq_in, ce.eq_out):
            for pos, s in enumerate(eqs):
                self.assertEqual(ce.eq_in[pos], l1[pos])
                self.assertIsInstance(s, EditableEq)

        ce = CompareEqs()
        ce.add_many(l1, l2, force_subeq=True)
        for eqs in (ce.eq_in, ce.eq_out):
            for pos, s in enumerate(eqs):
                self.assertEqual(ce.eq_in[pos], l1[pos])
                self.assertIsInstance(s, Subeq)
                self.assertNotIsInstance(s, EditableEq)

    def test_add_unzipping(self):
        db = (
            (["q"], ["x"]),
            ([PJUXT, ["a"], [TVOID]], [PVOID]),
            ([SUP, ["x"], ["b"]], [Op("O", "O")]),
        )
        ce = CompareEqs()
        ce.add_unzipping(db)
        for pos, eq_pair in enumerate(db):
            self.assertEqual(ce.eq_in[pos], db[pos][0])
            self.assertEqual(ce.eq_out[pos], db[pos][1])
            self.assertIsInstance(ce.eq_in[pos], EditableEq)
            self.assertIsInstance(ce.eq_out[pos], EditableEq)

        db = (
            (["q"], ["x"]),
            ([PJUXT, ["a"], [TVOID]], [PVOID]),
            ([SUP, ["x"], ["b"]], [Op("O", "O")]),
        )
        ce = CompareEqs()
        ce.add_unzipping(db, force_subeq=True)
        for pos, eq_pair in enumerate(db):
            self.assertEqual(ce.eq_in[pos], db[pos][0])
            self.assertEqual(ce.eq_out[pos], db[pos][1])
            self.assertIsInstance(ce.eq_in[pos], Subeq)
            self.assertIsInstance(ce.eq_out[pos], Subeq)
            self.assertNotIsInstance(ce.eq_in[pos], EditableEq)
            self.assertNotIsInstance(ce.eq_out[pos], EditableEq)

    def test_init(self):
        db = (
            (Eq(["q"]), Eq(["x"])),
            (Eq([PJUXT, ["a"], [TVOID]]), Eq([PVOID])),
            (Eq([SUP, ["x"], ["b"]]), Eq([Op("O", "O")])),
        )
        ce = CompareEqs(db)
        for pos, eq_pair in enumerate(db):
            self.assertEqual(ce.eq_in[pos], db[pos][0])
            self.assertEqual(ce.eq_out[pos], db[pos][1])
            self.assertIsInstance(ce.eq_in[pos], EditableEq)
            self.assertIsInstance(ce.eq_out[pos], EditableEq)

        l1 = (["a"], ["b"], [PVOID], [PJUXT, ["a"], ["b"]])
        l2 = (["x"], ["y"], [TVOID], [TJUXT, ["x"], ["y"]])
        ce = CompareEqs(l1, l2)
        for eqs in (ce.eq_in, ce.eq_out):
            for pos, s in enumerate(eqs):
                self.assertEqual(ce.eq_in[pos], l1[pos])
                self.assertIsInstance(s, EditableEq)

        l1 = (["a"], ["b"], [PVOID], [PJUXT, ["a"], ["b"]])
        l2 = (["x"], ["y"], [TVOID], [TJUXT, ["x"], ["y"]])
        ce = CompareEqs(l1, l2, force_subeq=True)
        for eqs in (ce.eq_in, ce.eq_out):
            for pos, s in enumerate(eqs):
                self.assertEqual(ce.eq_in[pos], l1[pos])
                self.assertIsInstance(s, Subeq)
                self.assertNotIsInstance(s, EditableEq)

    def test_assert_equality(self):
        l1 = ([PJUXT, ["a"], ["f"], ["r"]], [PJUXT, ["a"], ["b"]])
        ce = CompareEqs(l1, l1)
        ce.assert_equality(debug=False, is_method=False)

        l2 = ([PJUXT, ["a"], ["f"], ["r"]], [TJUXT, ["x"], ["y"]])
        ce = CompareEqs(l1, l2)
        with self.assertRaises(ValueError) as cm:
            ce.assert_equality(debug=False, is_method=False)
        self.assertEqual(cm.exception.args[0], NON_EQUAL_EQ_MSG)

        f = lambda s: [PJUXT, s, ["o"]]
        ce = CompareEqs(l1, l2, force_subeq=True)
        with self.assertRaises(ValueError) as cm:
            ce.assert_equality(f, debug=False, is_method=False)
        self.assertEqual(cm.exception.args[0], NON_EQUAL_EQ_MSG)

        ce = CompareEqs(l1, l1)
        ce.assert_equality(debug=False, is_method=False)

        f = lambda eq: Eq(eq, [1])
        ce.assert_equality(f, debug=False, is_method=False, exclude_idx=True)
        with self.assertRaises(ValueError) as cm:
            ce.assert_equality(f, debug=False, is_method=False)
        self.assertEqual(cm.exception.args[0], NON_EQUAL_IDX_MSG)

        f = lambda eq: Eq(eq, eq.idx, Dir.O)
        ce.assert_equality(f, debug=False, is_method=False, exclude_dir=True)
        with self.assertRaises(ValueError) as cm:
            ce.assert_equality(f, debug=False, is_method=False)
        self.assertEqual(cm.exception.args[0], NON_EQUAL_DIR_MSG)

        # Inverses
        ce = CompareEqs(list(map(lambda s: Eq(s, None, Dir.R), l1)),
                        list(map(lambda s: Eq(s, None, Dir.L), l1)))
        f = lambda eq: Eq(eq, eq.idx, Dir.L)
        ce.assert_equality(f, debug=False, is_method=False)
        ce.assert_equality(f, debug=False, inversely=True, is_method=False,
                           exclude_dir=True)
        with self.assertRaises(ValueError) as cm:
            ce.assert_equality(f, debug=False, inversely=True, is_method=False)
        self.assertEqual(cm.exception.args[0], NON_EQUAL_DIR_MSG)

        f = lambda eq: Eq(eq, eq.idx, Dir.R)
        ce.assert_equality(f, debug=False, inversely=True, is_method=False)
        with self.assertRaises(ValueError) as cm:
            ce.assert_equality(f, debug=False, is_method=False)
        self.assertEqual(cm.exception.args[0], NON_EQUAL_DIR_MSG)

    def test_assert_equality_methods(self):
        l1 = ([PJUXT, ["a"], ["f"], ["r"]], [PJUXT, ["a"], ["b"]])
        ce = CompareEqs([Eq(s, None, Dir.R) for s in l1],
                        [Eq()]*len(l1))
        ce.assert_equality(Eq.default_eq, debug=False)

        ce = CompareEqs([Eq(s, None, Dir.R) for s in l1],
                        [Eq()]*len(l1), [12]*len(l1))
        ce.assert_equality(Eq.default_eq, debug=False, exclude_retvals=True)
        with self.assertRaises(ValueError) as cm:
            ce.assert_equality(Eq.default_eq, debug=False)
        self.assertEqual(cm.exception.args[0], NON_EQUAL_RETURN_MSG)

        ce = CompareEqs([Eq(s, None, Dir.R) for s in l1],
                        [Eq()]*len(l1), [Eq.DEFAULT_METHOD_RETVAL]*len(l1))
        ce.assert_equality(Eq.default_eq, debug=False)

        db = (
            [[PJUXT, ["a"], ["f"], ["r"]], [PVOID], 1],
            [[PJUXT, ["a"], ["b"]], [PVOID], 1],
        )
        ce = CompareEqs(db)
        with self.assertRaises(ValueError) as cm:
            ce.assert_equality(Eq.default_eq, debug=False)
        self.assertEqual(cm.exception.args[0], NON_EQUAL_RETURN_MSG)

        for e in db:
            e[2] = Eq.DEFAULT_METHOD_RETVAL
        ce = CompareEqs(db)
        ce.assert_equality(Eq.default_eq, debug=False)
