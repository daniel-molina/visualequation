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

from visualequation.subeqs import Subeq
from visualequation.idx import Idx
from visualequation.dirsel import Dir
from visualequation.ops import *
from visualequation.eqedit import EditableEq
from visualequation.scriptops import *


class Eq(EditableEq):
    """Dummy class to avoid debugging messages when testing."""
    def __init__(self, eq0=None, sel_index0=None, dir0=None):
        super().__init__(eq0, sel_index0, dir0, debug=False)


SCRIPT_OPS_LIST = [op for op in SCRIPT_OP2ID_DICT.keys() if op is not None]
SETSCRIPT_OPS_LIST \
    = [op for op in SETSCRIPT_OP2ID_DICT.keys() if op is not None]
LOSCRIPT_OPS_LIST \
    = [op for op in LOSCRIPT_OP2ID_DICT.keys() if op is not None]


NO_EQ_MSG = "No Eqs are available for comparison"
NoEqError = ValueError(NO_EQ_MSG)
NON_EQUAL_EQ_MSG = "Eqs are not equal"
NonEqualEqError = ValueError(NON_EQUAL_EQ_MSG)
NON_EQUAL_IDX_MSG = "Indices are not equal"
NonEqualIdxError = ValueError(NON_EQUAL_IDX_MSG)
NON_EQUAL_DIR_MSG = "Dirs are not equal"
NonEqualDirError = ValueError(NON_EQUAL_DIR_MSG)
WRONG_NUMBER_ARGS_MSG = "Wrong number of arguments"
WrongNumberArgsError = TypeError(WRONG_NUMBER_ARGS_MSG)

class CompareEqs:
    def add_pair(self, eq_in, eq_out):
        """Add a pair of input and output eq."""
        if isinstance(eq_in, EditableEq):
            self.eq_in.append(eq_in)
            self.eq_out.append(eq_out)
        else:
            self.eq_in.append(Subeq(eq_in))
            self.eq_out.append(Subeq(eq_out))

    def add_many(self, many_eq_in, many_eq_out):
        """Add many input and output eqs"""
        if isinstance(many_eq_in[0], EditableEq):
            self.eq_in.extend(many_eq_in)
            self.eq_out.extend(many_eq_out)
        else:
            self.eq_in.extend(map(lambda l: Subeq(l), many_eq_in))
            self.eq_out.extend(map(lambda l: Subeq(l), many_eq_out))

    def add_unzipping(self, pairs_iter):
        """"""
        if isinstance(pairs_iter[0][0], EditableEq):
            for e1, e2 in pairs_iter:
                self.add_pair(e1, e2)
        else:
            for e1, e2 in pairs_iter:
                self.add_pair(Subeq(e1), Subeq(e2))

    def __init__(self, *args):
        if len(args) > 2:
            raise WrongNumberArgsError

        self.eq_in = []
        self.eq_out = []
        if len(args) == 1:
            self.add_unzipping(*args)
        elif len(args) == 2:
            self.add_many(*args)

    def assert_equality(self, fun=None, inversely=False,
                exclude_eq=False, exclude_idx=False, exclude_dir=False):
        if not self.eq_in or not self.eq_out:
            raise NoEqError

        if fun is None:
            lhs = self.eq_in
            rhs = self.eq_out
        elif inversely:
            lhs = self.eq_in
            rhs = list(map(fun, self.eq_out))
        else:
            lhs = self.eq_out
            rhs = list(map(fun, self.eq_in))

        if not exclude_eq:
            if not all(map(lambda s, p: s == p, lhs, rhs)):
                raise NonEqualEqError

        if isinstance(lhs[0], EditableEq) and not exclude_idx:
            if not all(map(lambda s, p: s.idx == p.idx, lhs, rhs)):
                raise NonEqualIdxError

        if isinstance(lhs[0], EditableEq) and not exclude_dir:
            if not all(map(lambda s, p: s.dir is p.dir, lhs, rhs)):
                raise NonEqualDirError


class CompareEqsTests(unittest.TestCase):
    def test_add_pair(self):
        ce = CompareEqs()
        ce.add_pair(Subeq(["a"]), Subeq(None))
        ce.add_pair(Subeq(["b"]), Subeq([PVOID]))
        self.assertEqual(len(ce.eq_in), 2)
        self.assertEqual(len(ce.eq_out), 2)
        ce.add_pair(["a"], ["3"])
        ce.add_pair(["b"], [PVOID])
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

    def test_add_many(self):
        ce = CompareEqs()
        l1 = (["a"], ["b"], [PVOID], [PJUXT, ["a"], ["b"]])
        l2 = (["x"], ["y"], [TVOID], [TJUXT, ["x"], ["y"]])
        ce.add_many(l1, l2)
        for eqs in (ce.eq_in, ce.eq_out):
            for pos, s in enumerate(eqs):
                self.assertEqual(ce.eq_in[pos], l1[pos])
                self.assertIsInstance(s, Subeq)
                self.assertNotIsInstance(s, EditableEq)

        ce = CompareEqs()
        ce.add_many(tuple(map(lambda s: Eq(s), l1)),
                    list(map(lambda s: Eq(s), l2)))
        for eqs in (ce.eq_in, ce.eq_out):
            for pos, s in enumerate(eqs):
                self.assertEqual(ce.eq_in[pos], l1[pos])
                self.assertIsInstance(s, EditableEq)

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
            self.assertIsInstance(ce.eq_in[pos], Subeq)
            self.assertIsInstance(ce.eq_out[pos], Subeq)
            self.assertNotIsInstance(ce.eq_in[pos], EditableEq)
            self.assertNotIsInstance(ce.eq_out[pos], EditableEq)

        db = (
            (Eq(["q"]), Eq(["x"])),
            (Eq([PJUXT, ["a"], [TVOID]]), Eq([PVOID])),
            (Eq([SUP, ["x"], ["b"]]), Eq([Op("O", "O")])),
        )
        ce = CompareEqs()
        ce.add_unzipping(db)
        for pos, eq_pair in enumerate(db):
            self.assertEqual(ce.eq_in[pos], db[pos][0])
            self.assertEqual(ce.eq_out[pos], db[pos][1])
            self.assertIsInstance(ce.eq_in[pos], EditableEq)
            self.assertIsInstance(ce.eq_out[pos], EditableEq)

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
                self.assertIsInstance(s, Subeq)
                self.assertNotIsInstance(s, EditableEq)

    def test_assert_equality(self):
        l1 = ([PJUXT, ["a"], ["f"], ["r"]], [PJUXT, ["a"], ["b"]])
        ce = CompareEqs(l1, l1)
        ce.assert_equality()

        l2 = ([PJUXT, ["a"], ["f"], ["r"]], [TJUXT, ["x"], ["y"]])
        ce = CompareEqs(l1, l2)
        with self.assertRaises(ValueError) as cm:
            ce.assert_equality()
        self.assertEqual(cm.exception.args[0], NON_EQUAL_EQ_MSG)

        f = lambda s: Subeq([PJUXT, s, ["o"]])
        ce = CompareEqs(l1, l2)
        with self.assertRaises(ValueError) as cm:
            ce.assert_equality(f)
        self.assertEqual(cm.exception.args[0], NON_EQUAL_EQ_MSG)

        eqs = list(map(lambda s: Eq(s), l1))
        ce = CompareEqs(eqs, eqs)
        ce.assert_equality()

        f = lambda eq: Eq([PJUXT, eq, ["o"]])
        ce.assert_equality(f, exclude_eq=True)
        with self.assertRaises(ValueError) as cm:
            ce.assert_equality(f)
        self.assertEqual(cm.exception.args[0], NON_EQUAL_EQ_MSG)

        f = lambda eq: Eq(eq, [1])
        ce.assert_equality(f, exclude_idx=True)
        with self.assertRaises(ValueError) as cm:
            ce.assert_equality(f)
        self.assertEqual(cm.exception.args[0], NON_EQUAL_IDX_MSG)

        f = lambda eq: Eq(eq, eq.idx, Dir.O)
        ce.assert_equality(f, exclude_dir=True)
        with self.assertRaises(ValueError) as cm:
            ce.assert_equality(f)
        self.assertEqual(cm.exception.args[0], NON_EQUAL_DIR_MSG)

        # Inverses
        ce = CompareEqs(list(map(lambda s: Eq(s, None, Dir.R), l1)),
                        list(map(lambda s: Eq(s, None, Dir.L), l1)))
        f = lambda eq: Eq(eq, eq.idx, Dir.L)
        ce.assert_equality(f)
        ce.assert_equality(f, inversely=True, exclude_dir=True)
        with self.assertRaises(ValueError) as cm:
            ce.assert_equality(f, inversely=True)
        self.assertEqual(cm.exception.args[0], NON_EQUAL_DIR_MSG)

        f = lambda eq: Eq(eq, eq.idx, Dir.R)
        ce.assert_equality(f, inversely=True)
        with self.assertRaises(ValueError) as cm:
            ce.assert_equality(f)
        self.assertEqual(cm.exception.args[0], NON_EQUAL_DIR_MSG)
