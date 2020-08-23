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

from visualequation.ops import *
from visualequation.dirsel import Dir
from visualequation.idx import Idx
from visualequation.subeqs import Subeq
from visualequation.scriptops import *
from visualequation.eqedit import EditableEq


class Eq(EditableEq):
    """Dummy class to avoid debugging messages."""
    def __init__(self, eq0=None, sel_index0=None, dir0=None):
        super().__init__(eq0, sel_index0, dir0, debug=False)


SCRIPT_OPS_LIST = [op for op in SCRIPT_OP2ID_DICT.keys() if op is not None]
SETSCRIPT_OPS_LIST \
    = [op for op in SETSCRIPT_OP2ID_DICT.keys() if op is not None]
LOSCRIPT_OPS_LIST \
    = [op for op in LOSCRIPT_OP2ID_DICT.keys() if op is not None]


class EqEdit(unittest.TestCase):
    def test_init(self):
        eq = Eq()
        self.assertEqual(eq, Subeq(None))
        self.assertEqual(eq.idx, [])
        self.assertIs(eq.dir, Dir.V)

        eq = Eq(["a"])
        self.assertEqual(eq, ["a"])
        self.assertEqual(eq.idx, [])
        self.assertIs(eq.dir, Dir.R)

        eq = Eq([PJUXT, ["e"], [TVOID]], [2], Dir.O)
        self.assertIsInstance(eq, Subeq)
        self.assertIsInstance(eq, EditableEq)
        self.assertIsInstance(eq(2), Subeq)
        self.assertNotIsInstance(eq(2), EditableEq)
        self.assertEqual(eq.idx, Idx(2))
        self.assertIs(eq.dir, Dir.O)

        eq.idx[:] = [2]
        self.assertIsInstance(eq.idx, Idx)
        eq.idx[0] = 1
        self.assertIsInstance(eq.idx, Idx)

        idx_cp = eq.idx[:]
        # Unintended use
        eq.idx = [1]
        self.assertNotIsInstance(eq.idx, Idx)
        eq.idx = idx_cp[:]

    def test_safe_idx_arg(self):
        eq = Eq([PJUXT, ["e"], ["r"]], [1])
        idx = [1]
        self.assertEqual(eq._safe_idx_arg(idx), idx)
        self.assertIsNot(eq._safe_idx_arg(idx), idx)
        self.assertIsNot(eq._safe_idx_arg(idx), eq.idx)

        self.assertEqual(eq._safe_idx_arg(-1), eq.idx)
        self.assertIsNot(eq._safe_idx_arg(-1), eq.idx)

        self.assertEqual(eq._safe_idx_arg(None), [])
        self.assertIsNot(eq._safe_idx_arg(None), eq.idx)

        self.assertEqual(eq._safe_idx_arg(2), [2])
        self.assertIsNot(eq._safe_idx_arg(None), eq.idx)

    def test_safe_subeq_arg(self):
        eq = Eq([PJUXT, ["e"], ["r"]])

        l_in = [PJUXT, ["1"], ["2"], ["3"]]
        s_out = eq._safe_subeq_arg(l_in)
        self.assertEqual(s_out, l_in)
        self.assertIsNot(s_out, l_in)
        for pos in range(0, 4):
            self.assertIsNot(l_in[pos], s_out[pos])

        eq.idx = []
        for args in ((), (0,), (0, -1), (0, []), (0, None)):
            s_out = eq._safe_subeq_arg(*args)
            self.assertEqual(s_out, eq(eq.idx))
            self.assertIsNot(s_out, eq(eq.idx))
            for pos in range(0, 3):
                self.assertEqual(s_out[pos], eq[pos])
                self.assertIsNot(s_out[pos], eq[pos])

        for idx in ([1], [2]):
            for args in ((), (0,), (0, -1), (0, idx[:])):
                eq.idx[:] = idx
                s_out = eq._safe_subeq_arg(*args)
                self.assertEqual(s_out, eq(eq.idx))
                self.assertIsNot(s_out, eq(eq.idx))

    def test_set(self):
        eq = Eq([PJUXT, ["e"], ["r"]])
        l_in = [PJUXT, ["1"], ["2"], ["3"]]

        eqref = eq
        eqref_1 = eq[1]
        eq._set(l_in)
        self.assertEqual(eq, l_in)
        self.assertIsNot(eq, l_in)
        for pos in range(0, 4):
            self.assertIsNot(eq[pos], l_in[pos])
        self.assertIsInstance(eq, EditableEq)
        self.assertIs(eq, eqref)
        self.assertIsNot(eq[1], eqref_1)
        self.assertNotEqual(eq[1], eqref_1)
        self.assertIsInstance(eq[1], Subeq)
        self.assertNotIsInstance(eq[1], EditableEq)

        eq = Eq([PJUXT, ["e"], ["r"]])
        eqref = eq
        eqref_1 = eq[1]
        eqref_11 = eq(1, 0)
        eq._set(l_in, 1)
        self.assertEqual(eq[1], l_in)
        self.assertIsNot(eq[1], l_in)
        for pos in range(0, 4):
            self.assertEqual(eq(1, pos), l_in[pos])
            self.assertIsNot(eq(1, pos), l_in[pos])
        self.assertNotIsInstance(eq[1], EditableEq)
        self.assertIsInstance(eq[1], Subeq)
        self.assertIs(eq, eqref)
        self.assertIs(eq[1], eqref_1)
        self.assertNotEqual(eq(1, 0), eqref_11)

    def test_safe_dir(self):
        eq = Eq([Op("a", "a", 2), ["e"], [PVOID]])

        eq.idx[:] = []
        eq.dir = Dir.R
        for args in ((), (["h"], -43), (0, -1), (0, [1]), (0, 1), (0, Idx(1))):
            self.assertEqual(eq._safe_dir(0, *args), Dir.R)
            self.assertEqual(eq._safe_dir(1, *args), Dir.R)
            self.assertEqual(eq._safe_dir(-1, *args), Dir.L)
            self.assertEqual(eq._safe_dir(5, *args), Dir.R)
            self.assertEqual(eq._safe_dir(-5, *args), Dir.R)

        eq.dir = Dir.L
        for args in ((), (["h"], -43), (0, -1), (0, [1]), (0, 1), (0, Idx(1))):
            self.assertEqual(eq._safe_dir(0, *args), Dir.L)
            self.assertEqual(eq._safe_dir(1, *args), Dir.R)
            self.assertEqual(eq._safe_dir(-1, *args), Dir.L)
            self.assertEqual(eq._safe_dir(5, *args), Dir.L)
            self.assertEqual(eq._safe_dir(-5, *args), Dir.L)

        for dir in (Dir.R, Dir.L, Dir.V):
            for args in((None, -1), (None, -88), (0, [2]), (0, -1)):
                eq.dir = dir
                if args == (0, -1):
                    eq.idx[:] = [2]
                self.assertEqual(eq._safe_dir(0, *args), Dir.V)
                self.assertEqual(eq._safe_dir(1, *args), Dir.V)
                self.assertEqual(eq._safe_dir(-1, *args), Dir.V)
                self.assertEqual(eq._safe_dir(5, *args), Dir.V)
                self.assertEqual(eq._safe_dir(-5, *args), Dir.V)

        eq.dir = Dir.O
        for idx in ([], [1], [2]):
            eq.idx[:] = idx
            self.assertEqual(eq._safe_dir(0), Dir.O)
            self.assertEqual(eq._safe_dir(1), Dir.O)
            self.assertEqual(eq._safe_dir(-1), Dir.O)
            self.assertEqual(eq._safe_dir(5), Dir.O)
            self.assertEqual(eq._safe_dir(-5), Dir.O)

    def test_condtly_correct_scriptop(self):
        for eq in (Eq(["a"]), Eq(None)):
            for repl in (Subeq(["repl"]), Subeq([Op("", "", 0, "vs")])):
                eq_cp = eq._safe_subeq_arg(0, [])
                eq_cp._condtly_correct_scriptop(repl)
                self.assertEqual(eq, eq_cp)
                eq_cp._condtly_correct_scriptop(repl, [])
                self.assertEqual(eq, eq_cp)

        eq = Eq([PJUXT, ["e"], [Op("q", "q")]])
        for repl in (Subeq(["repl"]), Subeq([Op("", "", 0, "vs")])):
            for idx in ([], [1], [2]):
                eq_cp = eq._safe_subeq_arg()
                eq_cp._condtly_correct_scriptop(repl, idx)
                self.assertEqual(eq, eq_cp)

        n_scripts = 15
        n_setscripts = 3
        n_loscripts = 63
        self.assertEqual(n_scripts, len(SCRIPT_OPS_LIST))
        self.assertEqual(n_setscripts, len(SETSCRIPT_OPS_LIST))
        self.assertEqual(n_loscripts, len(LOSCRIPT_OPS_LIST))

        n_ops = 0
        for repl in (Subeq(["repl"]), Subeq([GOP, [PJUXT, ["d"], ["e"]]])):
            for op in SCRIPT_OPS_LIST + SETSCRIPT_OPS_LIST:
                n_ops += 1
                eq = Eq([op] + [["x"]]*op.n_args)
                eq_cp = eq._safe_subeq_arg()
                eq_cp._condtly_correct_scriptop(repl, [1])
                self.assertEqual(eq, eq_cp)

                eq = Eq([Op("O", "O", 1), [op] + [["x"]]*op.n_args])
                eq_cp = eq._safe_subeq_arg()
                eq_cp._condtly_correct_scriptop(repl, [1, 1])
                self.assertEqual(eq, eq_cp)
            self.assertEqual(n_ops, n_scripts + n_setscripts)
            n_ops = 0
            for op in LOSCRIPT_OPS_LIST:
                n_ops += 1
                eq = Eq([op] + [["x"]]*op.n_args)
                eq_cp = eq._safe_subeq_arg()
                eq_cp._condtly_correct_scriptop(repl, [1])
                self.assertNotEqual(eq, eq_cp)

                eq = Eq([Op("O", "O", 1), [op] + [["x"]]*op.n_args])
                eq_cp = eq._safe_subeq_arg()
                eq_cp._condtly_correct_scriptop(repl, [1, 1])
                self.assertNotEqual(eq, eq_cp)
            self.assertEqual(n_ops, n_loscripts)
            n_ops = 0

        for repl in (Subeq([Op("s", "s", 0, "vs")]),
                     Subeq([GOP, [Op("fa", "", 1, "fun_args"), ["d"]]])):
            for op in SCRIPT_OPS_LIST + SETSCRIPT_OPS_LIST:
                n_ops += 1
                eq = Eq([op] + [["x"]]*op.n_args)
                eq_cp = eq._safe_subeq_arg()
                eq_cp._condtly_correct_scriptop(repl, [1])
                self.assertNotEqual(eq, eq_cp)
                # NON-LO -> LO conserves always all the pars
                self.assertEqual(len(eq), len(eq_cp))


                eq = Eq([Op("O", "O", 1), [op] + [["x"]]*op.n_args])
                eq_cp = eq._safe_subeq_arg()
                eq_cp._condtly_correct_scriptop(repl, [1, 1])
                self.assertNotEqual(eq, eq_cp)
                # NON-LO -> LO conserves always all the pars
                self.assertEqual(len(eq[1]), len(eq_cp[1]))

            self.assertEqual(n_ops, n_scripts + n_setscripts)
            n_ops = 0
            for op in LOSCRIPT_OPS_LIST:
                n_ops += 1
                eq = Eq([op] + [["x"]]*op.n_args)
                eq_cp = eq._safe_subeq_arg()
                eq_cp._condtly_correct_scriptop(repl, [1])
                self.assertEqual(eq, eq_cp)

                eq = Eq([Op("O", "O", 1), [op] + [["x"]]*op.n_args])
                eq_cp = eq._safe_subeq_arg()
                eq_cp._condtly_correct_scriptop(repl, [1, 1])
                self.assertEqual(eq, eq_cp)
            self.assertEqual(n_ops, n_loscripts)
            n_ops = 0

    def test_biggest_subeq_same_urepr(self):
        for eq in (Eq(["a"]), Eq([PJUXT, ["d"], ["e"]]),
                   Eq([GOP, [PJUXT, ["d"], ["e"]]])):
            self.assertIs(eq._biggest_subeq_same_urepr(), eq)
            self.assertIs(eq._biggest_subeq_same_urepr(-1), eq)
            self.assertEqual(eq._biggest_subeq_same_urepr(-1, True), [])

        eq = Eq([GOP, [PJUXT, ["d"], [PJUXT, ["e"], ["f"]]]])
        self.assertEqual(eq._biggest_subeq_same_urepr([1]), eq)
        self.assertEqual(eq._biggest_subeq_same_urepr([1], True), [])
        eq.idx[:] = [1]
        self.assertEqual(eq._biggest_subeq_same_urepr(), eq)
        self.assertEqual(eq._biggest_subeq_same_urepr(-1, True), [])

        for idx in ([1, 1], [1, 2], [1, 2, 1], [1, 2, 2]):
            self.assertEqual(eq._biggest_subeq_same_urepr(idx), eq(idx))
            self.assertEqual(eq._biggest_subeq_same_urepr(idx, True), idx)
            eq.idx[:] = idx
            self.assertEqual(eq._biggest_subeq_same_urepr(), eq(idx))
            self.assertEqual(eq._biggest_subeq_same_urepr(-1, True), idx)

        eq = Eq([PJUXT, ["a"], [GOP, [PJUXT, ["e"], ["f"]]]])
        self.assertEqual(eq._biggest_subeq_same_urepr([2, 1]), eq(2))
        self.assertEqual(eq._biggest_subeq_same_urepr([2, 1], True), [2])
        eq.idx[:] = [2, 1]
        self.assertEqual(eq._biggest_subeq_same_urepr(), eq(2))
        self.assertEqual(eq._biggest_subeq_same_urepr(-1, True), [2])
        for idx in ([], [1], [2], [2, 1, 1], [2, 1, 2]):
            self.assertEqual(eq._biggest_subeq_same_urepr(idx), eq(idx))
            self.assertEqual(eq._biggest_subeq_same_urepr(idx, True), idx)
            eq.idx[:] = idx
            self.assertEqual(eq._biggest_subeq_same_urepr(), eq(idx))
            self.assertEqual(eq._biggest_subeq_same_urepr(-1, True), idx)


if __name__ == '__main__':
    unittest.main()
