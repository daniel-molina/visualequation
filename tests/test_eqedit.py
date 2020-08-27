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

from visualequation.ops import *
from visualequation.dirsel import Dir
from visualequation.idx import Idx
from visualequation.subeqs import Subeq
from visualequation.scriptops import *
from visualequation.eqedit import EditableEq
from tests.test_utils import *


class EqEditTests(unittest.TestCase):
    """Tests for EditableEq methods.

    .. note::
        EditableEq manages well-built equations. Do not use shorter
        invalid equations in these tests as [GOP, ["a"]].
    """
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

        eq = Eq([GOP, [PJUXT, ["e"], [Op("o", "o")]]])
        self.assertEqual(eq.idx, [1])
        self.assertEqual(eq.dir, Dir.R)
        eq = Eq([GOP, [PJUXT, ["e"], [Op("o", "o")]]], None, Dir.O)
        self.assertEqual(eq.idx, [1])
        self.assertEqual(eq.dir, Dir.O)

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

    def test_rinsert(self):

        for s in (["2"], [Op("2", "2")], [SUP, ["x"], ["a"]],
                  [GOP,  [SUP, ["x"], ["a"]]], [GOP,  [PJUXT, ["1"], ["2"]]]):
            eq = Eq(["C"])
            self.assertEqual(eq._rinsert(s, []), [2])
            self.assertEqual(eq, [PJUXT, ["C"], s])
            # Testing index == -1
            eq.idx[:] = [1]
            self.assertEqual(eq._rinsert(["D"], -1), [2])
            self.assertEqual(eq, [PJUXT, ["C"], ["D"], s])
            eq.idx[:] = [3]
            self.assertEqual(eq._rinsert(["F"]), [4])
            self.assertEqual(eq, [PJUXT, ["C"], ["D"], s, ["F"]])

        eq = Eq([PJUXT, ["1"], ["2"]])
        self.assertEqual(eq._rinsert(["3"], []), [3])
        self.assertEqual(eq, [PJUXT, ["1"], ["2"], ["3"]])

        eq = Eq([PJUXT, ["1"], ["2"]])
        self.assertEqual(eq._rinsert(["3"], [2]), [3])
        self.assertEqual(eq, [PJUXT, ["1"], ["2"], ["3"]])
        self.assertEqual(eq._rinsert(["4"], [3]), [4])
        self.assertEqual(eq, [PJUXT, ["1"], ["2"], ["3"], ["4"]])
        self.assertEqual(eq._rinsert(["1.5"], [1]), [2])
        self.assertEqual(eq, [PJUXT, ["1"], ["1.5"], ["2"], ["3"], ["4"]])
        self.assertEqual(eq._rinsert(["1.7"], [2]), [3])
        self.assertEqual(eq,
                         [PJUXT, ["1"], ["1.5"], ["1.7"], ["2"], ["3"], ["4"]])
        eq = Eq([PJUXT, ["1"], ["2"]])
        with self.assertRaises(IndexError):
            eq._rinsert(["e"], [3])

        eq = Eq([PJUXT, ["1"], ["2"]])
        self.assertEqual(eq._rinsert([SUP, ["x"], ["a"]], []), [3])
        self.assertEqual(eq, [PJUXT, ["1"], ["2"], [SUP, ["x"], ["a"]]])

        eq = Eq([PJUXT, ["1"], ["2"]])
        self.assertEqual(eq._rinsert([SUP, ["x"], ["a"]], [1]), [2])
        self.assertEqual(eq, [PJUXT, ["1"], [SUP, ["x"], ["a"]], ["2"]])
        self.assertEqual(eq._rinsert([SUB, ["y"], ["0"]], [3]), [4])
        self.assertEqual(eq, [PJUXT, ["1"], [SUP, ["x"], ["a"]], ["2"],
                              [SUB, ["y"], ["0"]]])

        for s in (["2"], [Op("2", "2")], [SUP, ["x"], ["a"]],
                  [GOP, [SUP, ["x"], ["a"]]], [GOP, [PJUXT, ["1"], ["2"]]]):
            eq = Eq(s)
            self.assertEqual(eq._rinsert([PJUXT, ["g"], ["h"]], []), [2])
            self.assertEqual(eq, [PJUXT, s, [TJUXT, ["g"], ["h"]]])

        eq = Eq([PJUXT, ["1"], ["2"]])
        self.assertEqual(eq._rinsert([PJUXT, ["g"], ["h"]], []), [3])
        self.assertEqual(eq, [PJUXT, ["1"], ["2"], [TJUXT, ["g"], ["h"]]])

        eq = Eq([PJUXT, ["1"], ["2"]])
        self.assertEqual(eq._rinsert([PJUXT, ["g"], ["h"]], [1]), [2])
        self.assertEqual(eq, [PJUXT, ["1"], [TJUXT, ["g"], ["h"]], ["2"]])
        eq = Eq([PJUXT, ["1"], ["2"]])
        self.assertEqual(eq._rinsert([PJUXT, ["g"], ["h"]], [2]), [3])
        self.assertEqual(eq, [PJUXT, ["1"], ["2"], [TJUXT, ["g"], ["h"]]])

        eq = Eq([PJUXT, ["1"], ["2"], [PJUXT, ["3,1"], ["3,2"]]])
        # If pointed subeq is a juxted, it does not matter if it is also a
        # juxt-block
        self.assertEqual(eq._rinsert([PJUXT, ["g"], ["h"]], [3]), [4])
        self.assertEqual(eq, [PJUXT, ["1"], ["2"], [PJUXT, ["3,1"], ["3,2"]],
                              [TJUXT, ["g"], ["h"]]])

        eq = Eq([PJUXT, ["1"], ["2"], [PJUXT, ["3,1"], ["3,2"]]])
        self.assertEqual(eq._rinsert([PJUXT, ["g"], ["h"]], [3, 1]), [3, 2])
        self.assertEqual(eq, [PJUXT, ["1"], ["2"], [PJUXT, ["3,1"],
                              [TJUXT, ["g"], ["h"]], ["3,2"]]])

        eq = Eq([PJUXT, ["1"], ["2"], [PJUXT, ["3,1"], ["3,2"]]])
        self.assertEqual(eq._rinsert([PJUXT, ["g"], ["h"]], [3, 2]), [3, 3])
        self.assertEqual(eq, [PJUXT, ["1"], ["2"], [PJUXT, ["3,1"], ["3,2"],
                              [TJUXT, ["g"], ["h"]]]])

    def test_linsert(self):

        for s in (["2"], [Op("2", "2")], [SUP, ["x"], ["a"]],
                  [GOP,  [SUP, ["x"], ["a"]]], [GOP,  [PJUXT, ["1"], ["2"]]]):
            eq = Eq(["C"])
            self.assertEqual(eq._linsert(s, []), [1])
            self.assertEqual(eq, [PJUXT, s, ["C"]])
            # Testing index == -1
            eq.idx[:] = [1]
            self.assertEqual(eq._linsert(["A"], -1), [1])
            self.assertEqual(eq, [PJUXT, ["A"], s, ["C"]])
            eq.idx[:] = [3]
            self.assertEqual(eq._linsert(["B"]), [3])
            self.assertEqual(eq, [PJUXT, ["A"], s, ["B"], ["C"]])

        eq = Eq([PJUXT, ["1"], ["2"]])
        self.assertEqual(eq._linsert(["0"], []), [1])
        self.assertEqual(eq, [PJUXT, ["0"], ["1"], ["2"]])

        eq = Eq([PJUXT, ["1"], ["2"]])
        self.assertEqual(eq._linsert(["1.5"], [2]), [2])
        self.assertEqual(eq, [PJUXT, ["1"], ["1.5"], ["2"]])
        self.assertEqual(eq._linsert(["1.7"], [3]), [3])
        self.assertEqual(eq, [PJUXT, ["1"], ["1.5"], ["1.7"], ["2"]])
        self.assertEqual(eq._linsert(["0.5"], [1]), [1])
        self.assertEqual(eq, [PJUXT, ["0.5"], ["1"], ["1.5"], ["1.7"], ["2"]])
        self.assertEqual(eq._linsert(["0.7"], [2]), [2])
        self.assertEqual(eq, [PJUXT, ["0.5"], ["0.7"], ["1"],
                             ["1.5"], ["1.7"], ["2"]])
        eq = Eq([PJUXT, ["1"], ["2"]])
        with self.assertRaises(IndexError):
            eq._linsert(["e"], [3])

        eq = Eq([PJUXT, ["1"], ["2"]])
        self.assertEqual(eq._linsert([SUP, ["x"], ["a"]], []), [1])
        self.assertEqual(eq, [PJUXT, [SUP, ["x"], ["a"]], ["1"], ["2"]])

        eq = Eq([PJUXT, ["1"], ["2"]])
        self.assertEqual(eq._linsert([SUP, ["x"], ["a"]], [1]), [1])
        self.assertEqual(eq, [PJUXT, [SUP, ["x"], ["a"]], ["1"], ["2"]])
        self.assertEqual(eq._linsert([SUB, ["y"], ["0"]], [3]), [3])
        self.assertEqual(eq, [PJUXT, [SUP, ["x"], ["a"]], ["1"],
                              [SUB, ["y"], ["0"]], ["2"]])

        for s in (["2"], [Op("2", "2")], [SUP, ["x"], ["a"]],
                  [GOP, [SUP, ["x"], ["a"]]], [GOP, [PJUXT, ["1"], ["2"]]]):
            eq = Eq(s)
            self.assertEqual(eq._linsert([PJUXT, ["g"], ["h"]], []), [1])
            self.assertEqual(eq, [PJUXT, [TJUXT, ["g"], ["h"]], s])

        eq = Eq([PJUXT, ["1"], ["2"]])
        self.assertEqual(eq._linsert([PJUXT, ["g"], ["h"]], []), [1])
        self.assertEqual(eq, [PJUXT, [TJUXT, ["g"], ["h"]], ["1"], ["2"]])

        eq = Eq([PJUXT, ["1"], ["2"]])
        self.assertEqual(eq._linsert([PJUXT, ["g"], ["h"]], [1]), [1])
        self.assertEqual(eq, [PJUXT, [TJUXT, ["g"], ["h"]], ["1"], ["2"]])
        eq = Eq([PJUXT, ["1"], ["2"]])
        self.assertEqual(eq._linsert([PJUXT, ["g"], ["h"]], [2]), [2])
        self.assertEqual(eq, [PJUXT, ["1"], [TJUXT, ["g"], ["h"]], ["2"]])

        eq = Eq([PJUXT, ["1"], ["2"], [PJUXT, ["3,1"], ["3,2"]]])
        # If pointed subeq is a juxted, it does not matter if it is also a
        # juxt-block
        self.assertEqual(eq._linsert([PJUXT, ["g"], ["h"]], [3]), [3])
        self.assertEqual(eq, [PJUXT, ["1"], ["2"], [TJUXT, ["g"], ["h"]],
                              [PJUXT, ["3,1"], ["3,2"]]])

        eq = Eq([PJUXT, ["1"], ["2"], [PJUXT, ["3,1"], ["3,2"]]])
        self.assertEqual(eq._linsert([PJUXT, ["g"], ["h"]], [3, 1]), [3, 1])
        self.assertEqual(eq, [PJUXT, ["1"], ["2"], [PJUXT,
                              [TJUXT, ["g"], ["h"]], ["3,1"], ["3,2"]]])

        eq = Eq([PJUXT, ["1"], ["2"], [PJUXT, ["3,1"], ["3,2"]]])
        self.assertEqual(eq._linsert([PJUXT, ["g"], ["h"]], [3, 2]), [3, 2])
        self.assertEqual(eq, [PJUXT, ["1"], ["2"], [PJUXT, ["3,1"],
                              [TJUXT, ["g"], ["h"]], ["3,2"]]])

    def test_replace_integrating(self):
        # _replace_integrating only modifies eq, nor the index nor dir

        # Replace a non-PJUXT block
        for repl in (["r"], [Op("O", "O")], [GOP, [SUP, ["x"], ["b"]]],
                     [TJUXT, ["x"], ["y"], ["z"]]):
            # This equation is invalid in some cases, preparing it here
            r1 = Eq(repl)
            r1.idx = [1]
            db = (
                (Eq(["a"]), Eq(repl, []), []),
                (Eq([PVOID], [], Dir.V), Eq(repl, [], Dir.V), []),
                (Eq([Op("O", "O")]), Eq(repl, []), []),
                (Eq([PJUXT, ["f"], ["s"]]), Eq(repl, []), []),
                (Eq([PJUXT, ["f"], ["s"]], [1]),
                    Eq([PJUXT, repl, ["s"]], [1]), [1]),
                (Eq([GOP, [PJUXT, ["a"], ["b"]]], [1]), r1, []),
                (Eq([PJUXT, [PJUXT, ["a"], ["b"]], ["c"]], [1]),
                    Eq([PJUXT, repl, ["c"]], [1]), [1]),
                (Eq([PJUXT, [PJUXT, ["a"], ["b"]], ["c"]], [1, 1]),
                    Eq([PJUXT, [PJUXT, repl, ["b"]], ["c"]], [1, 1]), [1, 1]),
                (Eq([PJUXT, [PJUXT, ["a"], ["b"]], ["c"]], [1, 2]),
                    Eq([PJUXT, [PJUXT, ["a"], repl], ["c"]], [1, 2]), [1, 2]),
                (Eq([PJUXT, [PJUXT, ["a"], ["b"]], ["c"]], [2]),
                    Eq([PJUXT, [PJUXT, ["a"], ["b"]], repl], [2]), [2]),
            )
            ce = CompareEqs(db)
            f = lambda eq: Eq._replace_integrating(eq, repl)
            ce.assert_equality(f)

        # Replacing a PJUXT-block
        db = (
            (Eq(["a"]), Eq([PJUXT, ["x"], ["y"]]), []),
            (Eq([PVOID], [], Dir.V), Eq([PJUXT, ["x"], ["y"]], [], Dir.V), []),
            (Eq([Op("O", "O")]), Eq([PJUXT, ["x"], ["y"]]), []),
            (Eq([PJUXT, ["f"], ["s"]]), Eq([PJUXT, ["x"], ["y"]]), []),
            (Eq([PJUXT, ["f"], ["s"]], [1]),
                Eq([PJUXT, ["x"], ["y"], ["s"]], [1]), [1]),
            (Eq([GOP, [PJUXT, ["a"], ["b"]]], [1]),
                Eq([PJUXT, ["x"], ["y"]], [1]), []),
            (Eq([PJUXT, [PJUXT, ["a"], ["b"]], ["c"]], [1]),
                Eq([PJUXT, ["x"], ["y"], ["c"]], [1]), [1]),
            (Eq([PJUXT, [PJUXT, ["a"], ["b"]], ["c"]], [1, 1]),
                Eq([PJUXT, [PJUXT, ["x"], ["y"], ["b"]], ["c"]], [1, 1]),
                [1, 1]),
            (Eq([PJUXT, [PJUXT, ["a"], ["b"]], ["c"]], [1, 2]),
                Eq([PJUXT, [PJUXT, ["a"], ["x"], ["y"]], ["c"]], [1, 2]),
                [1, 2]),
            (Eq([PJUXT, [PJUXT, ["a"], ["b"]], ["c"]], [2]),
                Eq([PJUXT, [PJUXT, ["a"], ["b"]], ["x"], ["y"]], [2]), [2]),
        )
        ce = CompareEqs(db)
        f = lambda eq: Eq._replace_integrating(eq, [PJUXT, ["x"], ["y"]])
        ce.assert_equality(f)

    def test_replace(self):
        # Replace a non-GOP block
        for repl in (["r"], [Op("O", "O")], [PJUXT, ["x"], ["y"]],
                     [TJUXT, ["x"], ["y"], ["z"]], [SUP, ["x"], ["y"]]):
            # This equation is invalid in some cases, preparing it here
            r1 = Eq(repl)
            r1.idx = [1]
            db = (
                (Eq(["a"]), Eq(repl), []),
                (Eq([PVOID], [], Dir.V), Eq(repl, [], Dir.V), []),
                (Eq([Op("O", "O")]), Eq(repl), []),
                (Eq([PJUXT, ["f"], ["s"]]), Eq(repl), []),
                (Eq([PJUXT, ["f"], ["s"]], [1]),
                    Eq([PJUXT, repl, ["s"]], [1]), [1]),
                (Eq([GOP, [PJUXT, ["a"], ["b"]]], [1]), r1, []),
                (Eq([PJUXT, [PJUXT, ["a"], ["b"]], ["c"]], [1]),
                    Eq([PJUXT, repl, ["c"]], [1]), [1]),
                (Eq([PJUXT, [PJUXT, ["a"], ["b"]], ["c"]], [1, 1]),
                    Eq([PJUXT, [PJUXT, repl, ["b"]], ["c"]], [1, 1]), [1, 1]),
                (Eq([PJUXT, [PJUXT, ["a"], ["b"]], ["c"]], [1, 2]),
                    Eq([PJUXT, [PJUXT, ["a"], repl], ["c"]], [1, 2]), [1, 2]),
                (Eq([PJUXT, [PJUXT, ["a"], ["b"]], ["c"]], [2]),
                    Eq([PJUXT, [PJUXT, ["a"], ["b"]], repl], [2]), [2]),
            )
            ce = CompareEqs(db)
            f = lambda eq: Eq._replace(eq, repl)
            ce.assert_equality(f)

        # Replace a non-GOP block
        for repl in ([GOP, [PJUXT, ["x"], ["y"]]], [GOP, [SUP, ["x"], ["y"]]],
                     [GOP, [PJUXT, [GOP, [SUP, ["x"], ["y"]]], ["y"]]]):
            db = (
                (Eq(["a"]), Eq(repl, []), [1]),
                (Eq([PVOID], [], Dir.V), Eq(repl, [], Dir.V), [1]),
                (Eq([Op("O", "O")]), Eq(repl, []), [1]),
                (Eq([PJUXT, ["f"], ["s"]]), Eq(repl, []), [1]),
                (Eq([PJUXT, ["f"], ["s"]], [1]),
                    Eq([PJUXT, repl, ["s"]], [1]), [1, 1]),
                (Eq([GOP, [PJUXT, ["a"], ["b"]]], [1]), Eq(repl), [1]),
                (Eq([PJUXT, [PJUXT, ["a"], ["b"]], ["c"]], [1]),
                    Eq([PJUXT, repl, ["c"]], [1]), [1, 1]),
                (Eq([PJUXT, [PJUXT, ["a"], ["b"]], ["c"]], [1, 1]),
                    Eq([PJUXT, [PJUXT, repl, ["b"]], ["c"]], [1, 1]), [1, 1, 1]),
                (Eq([PJUXT, [PJUXT, ["a"], ["b"]], ["c"]], [1, 2]),
                    Eq([PJUXT, [PJUXT, ["a"], repl], ["c"]], [1, 2]), [1, 2, 1]),
                (Eq([PJUXT, [PJUXT, ["a"], ["b"]], ["c"]], [2]),
                    Eq([PJUXT, [PJUXT, ["a"], ["b"]], repl], [2]), [2, 1]),
            )
        ce = CompareEqs(db)
        f = lambda eq: Eq._replace(eq, repl)
        ce.assert_equality(f, debug=True)

    def test_empty(self):
        # Replace a non-GOP block
        # Invalid eqs
        ipvoid = Eq([PVOID], [], Dir.R)
        ipvoid1 = Eq([PVOID], [], Dir.R)
        ipvoid1.idx[:] = [1]
        # Many cases are not intended to be used
        db = (
            (Eq(["a"]), ipvoid, []),
            (Eq([PVOID]), Eq([PVOID]), []),
            (Eq([Op("O", "O")]), ipvoid, []),
            (Eq([PJUXT, ["f"], ["s"]]), ipvoid, []),
            (Eq([PJUXT, ["f"], ["s"]], [1]),
                Eq([PJUXT, [PVOID], ["s"]], [1], Dir.R), [1]),
            (Eq([GOP, [PJUXT, ["a"], ["b"]]], [1]), ipvoid1, []),
            (Eq([PJUXT, [PJUXT, ["a"], ["b"]], ["c"]], [1]),
                Eq([PJUXT, [PVOID], ["c"]], [1], Dir.R), [1]),
            (Eq([PJUXT, [PJUXT, ["a"], ["b"]], ["c"]], [1, 1]),
                Eq([PJUXT, [PJUXT, [PVOID], ["b"]], ["c"]], [1, 1], Dir.R),
                [1, 1]),
            (Eq([PJUXT, [PJUXT, ["a"], ["b"]], ["c"]], [1, 2]),
                Eq([PJUXT, [PJUXT, ["a"], [PVOID]], ["c"]], [1, 2], Dir.R),
                [1, 2]),
            (Eq([PJUXT, [PJUXT, ["a"], ["b"]], ["c"]], [2]),
                Eq([PJUXT, [PJUXT, ["a"], ["b"]], [PVOID]], [2], Dir.R), [2]),
        )
        ce = CompareEqs(db)
        ce.assert_equality(Eq._empty, debug=True)

    def test_remove_eq(self):
        # Replace a non-GOP block
        db = (
            (Eq(["a"]), Eq()),
            (Eq([PVOID]), Eq()),
            (Eq([Op("O", "O")]), Eq()),
            (Eq([PJUXT, ["f"], ["s"]]), Eq()),
            (Eq([PJUXT, ["f"], ["s"]], [1]), Eq()),
            (Eq([GOP, [PJUXT, ["a"], ["b"]]], [1]), Eq()),
            (Eq([PJUXT, [PJUXT, ["a"], ["b"]], ["c"]], [1]), Eq()),
            (Eq([PJUXT, [PJUXT, ["a"], ["b"]], ["c"]], [1, 1]), Eq()),
            (Eq([PJUXT, [PJUXT, ["a"], ["b"]], ["c"]], [1, 2]), Eq()),
            (Eq([PJUXT, [PJUXT, ["a"], ["b"]], ["c"]], [2]), Eq()),
        )
        ce = CompareEqs(db)
        ce.assert_equality(Eq.remove_eq, debug=True)

    def test_set_ovrwrt_pvoid(self):
        for args in (([PVOID], []), ([SUP, ["x"], [PVOID]], [2])):
            eq = Eq(*args, Dir.O)
            eq_cp = deepcopy(eq)
            eq_cp.ovrwrt(True)
            self.assertEqual(eq, eq_cp)
            self.assertEqual(eq.idx, eq_cp.idx)
            self.assertEqual(eq.dir, eq_cp.dir)

            eq = Eq(*args, Dir.O)
            eq_cp = deepcopy(eq)
            eq_cp.ovrwrt(False)
            self.assertEqual(eq, eq_cp)
            self.assertEqual(eq.idx, eq_cp.idx)
            self.assertNotEqual(eq.dir, eq_cp.dir)
            self.assertEqual(eq_cp.dir, Dir.V)

            eq = Eq(*args, Dir.V)
            eq_cp = deepcopy(eq)
            eq_cp.ovrwrt(True)
            self.assertEqual(eq, eq_cp)
            self.assertEqual(eq.idx, eq_cp.idx)
            self.assertNotEqual(eq.dir, eq_cp.dir)
            self.assertEqual(eq_cp.dir, Dir.O)

            eq = Eq(*args, Dir.V)
            eq_cp = deepcopy(eq)
            eq_cp.ovrwrt(False)
            self.assertEqual(eq, eq_cp)
            self.assertEqual(eq.idx, eq_cp.idx)
            self.assertEqual(eq.dir, eq_cp.dir)

    def test_set_ovrwrt_L2O(self):
        for args in ((["2"], []), ([Op("2", "2")], []),
                     ([SUP, ["x"], ["a"]], []),
                     ([SUP, ["x"], ["a"]], [1]), ([SUP, ["x"], ["a"]], [2]),
                     ([PJUXT, ["d"], ["d"]], []), ([PJUXT, ["d"], ["d"]], [1]),
                     ([PJUXT, ["d"], ["d"]], [2]),
                     ([GOP,  [SUP, ["x"], ["a"]]], [1]),
                     ([Op("O", "O", 1), [SUP, ["x"], ["a"]]], []),
                     ([Op("O", "O", 1), [SUP, ["x"], ["a"]]], [1]),
                     ([Op("O", "O", 1), [SUP, ["x"], ["a"]]], [1, 1]),
                     ([Op("O", "O", 1), [SUP, ["x"], ["a"]]], [1, 2]),
                     ([Op("O", "O", 1), [PJUXT, ["1"], ["2"]]], [1]),
                     ([Op("O", "O", 1), [PJUXT, ["1"], ["2"]]], [1, 1]),
                     ([Op("O", "O", 1), [PJUXT, ["1"], ["2"]]], [1, 2])):
            eq = Eq(*args, Dir.L)
            eq_cp = deepcopy(eq)
            eq_cp.ovrwrt(True)
            self.assertEqual(eq, eq_cp)
            self.assertEqual(eq.idx, eq_cp.idx)
            self.assertNotEqual(eq.dir, eq_cp.dir)
            self.assertEqual(eq_cp.dir, Dir.O)

    def test_set_ovrwrt_R2O(self):
        for args in (([PJUXT, ["d"], ["d"]], [1]),
                     ([PJUXT, ["d"], ["d"], ["d"]], [1]),
                     ([PJUXT, ["d"], ["d"], ["d"]], [2]),
                     ([Op("O", "O", 1), [PJUXT, ["1"], ["2"]]], [1, 1])):
            eq = Eq(*args, Dir.R)
            eq_cp = deepcopy(eq)
            eq_cp.ovrwrt(True)
            self.assertEqual(eq, eq_cp)
            self.assertEqual(eq_cp.idx, eq.idx[:-1] + [eq.idx[-1] + 1])
            self.assertEqual(eq_cp.dir, Dir.O)

            db = (
                ((["x"], []),
                 ([PJUXT, ["x"], [TVOID]], [2])),

                ((["x"], []),
                 ([PJUXT, ["x"], [TVOID]], [2])),

                (([SUP, ["x"], ["a"]], []),
                 ([PJUXT, [SUP, ["x"], ["a"]], [TVOID]], [2])),

                (([SUP, ["x"], ["a"]], [1]),
                 ([SUP, [PJUXT, ["x"], [TVOID]], ["a"]], [1, 2])),

                (([SUP, ["x"], ["a"]], [2]),
                 ([SUP, ["x"], [PJUXT, ["a"], [TVOID]]], [2, 2])),

                (([PJUXT, ["d"], ["d"]], []),
                 ([PJUXT, ["d"], ["d"], [TVOID]], [3])),

                (([PJUXT, ["d"], ["d"]], [2]),
                 ([PJUXT, ["d"], ["d"], [TVOID]], [3])),

                (([GOP, [SUP, ["x"], ["a"]]], [1]),
                 ([PJUXT, [GOP, [SUP, ["x"], ["a"]]], [TVOID]], [2])),

                (([Op("O", "O", 1), [SUP, ["x"], ["a"]]], []),
                 ([PJUXT, [Op("O", "O", 1), [SUP, ["x"], ["a"]]],
                          [TVOID]], [2])),

                (([Op("O", "O", 1), [SUP, ["x"], ["a"]]], [1]),
                 ([Op("O", "O", 1), [PJUXT, [SUP, ["x"], ["a"]],
                                            [TVOID]]], [1, 2])),

                (([Op("O", "O", 1), [SUP, ["x"], ["a"]]], [1, 1]),
                 ([Op("O", "O", 1), [SUP, [PJUXT, ["x"], [TVOID]],
                                          ["a"]]], [1, 1, 2])),

                (([Op("O", "O", 1), [SUP, ["x"], ["a"]]], [1, 2]),
                 ([Op("O", "O", 1), [SUP, ["x"],
                                    [PJUXT, ["a"], [TVOID]]]], [1, 2, 2])),

                (([Op("O", "O", 1), [PJUXT, ["x"], ["y"]]], [1]),
                 ([Op("O", "O", 1), [PJUXT, ["x"], ["y"], [TVOID]]], [1, 3])),

                (([Op("O", "O", 1), [PJUXT, ["x"], ["y"]]], [1, 2]),
                 ([Op("O", "O", 1), [PJUXT, ["x"], ["y"], [TVOID]]], [1, 3]))
            )

            for args_in, args_out in db:
                eq1 = Eq(*args_in, Dir.R)
                eq2 = Eq(*args_out, Dir.O)
                self.assertNotEqual(eq1, eq2)
                self.assertNotEqual(eq1.idx, eq2.idx)

                eq_test = deepcopy(eq1)
                eq_test.ovrwrt(True)
                self.assertEqual(eq_test, eq2)
                self.assertEqual(eq_test.idx, eq2.idx)
                self.assertEqual(eq_test.dir, Dir.O)

                eq_test = deepcopy(eq2)
                eq_test.ovrwrt(False)
                self.assertEqual(eq_test, eq1)
                self.assertEqual(eq_test.idx, eq1.idx)
                self.assertEqual(eq_test.dir, Dir.R)



if __name__ == '__main__':
    unittest.main()
