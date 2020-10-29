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

from tests.test_utils import *


class EqCoreTests(unittest.TestCase):
    """Tests for EqCore methods.

    .. note::
        EqCore should manage well-built equations. Avoid using invalid eqs.
    """
    def test_init(self):
        eq = Eq()
        self.assertEqual(eq, Subeq(None))
        self.assertEqual(eq, Eq([PVOID]))
        self.assertEqual(eq.idx, [])
        self.assertIs(eq.selm, SelMode.LCURSOR)

        eq = Eq(["a"])
        self.assertEqual(eq, ["a"])
        self.assertEqual(eq.idx, [])
        self.assertIs(eq.selm, SelMode.LCURSOR)

        eq = Eq([PJuxt(), ["e"], [PS]])
        self.assertIsInstance(eq, Subeq)
        self.assertIsInstance(eq, EqCore)
        self.assertEqual(eq.idx, Idx(1))
        self.assertIs(eq.selm, SelMode.LCURSOR)

        eq = Eq([PJuxt(), ["e"], [PS]], [2], SelMode.RCURSOR)
        self.assertIsInstance(eq, Subeq)
        self.assertIsInstance(eq, EqCore)
        self.assertIsInstance(eq(2), Subeq)
        self.assertNotIsInstance(eq(2), EqCore)
        self.assertEqual(eq.idx, Idx(2))
        self.assertIs(eq.selm, SelMode.RCURSOR)

        eq = Eq([PJuxt(), ["e"], [PS]], [2], SelMode.LHIGHLIGHTED)
        self.assertIsInstance(eq, Subeq)
        self.assertIsInstance(eq, EqCore)
        self.assertIsInstance(eq(2), Subeq)
        self.assertNotIsInstance(eq(2), EqCore)
        self.assertEqual(eq.idx, Idx(2))
        self.assertIs(eq.selm, SelMode.LHIGHLIGHTED)

        eq = Eq([PJuxt(), ["e"], [PS]], [2], SelMode.RHIGHLIGHTED)
        self.assertIsInstance(eq, Subeq)
        self.assertIsInstance(eq, EqCore)
        self.assertIsInstance(eq(2), Subeq)
        self.assertNotIsInstance(eq(2), EqCore)
        self.assertEqual(eq.idx, Idx(2))
        self.assertIs(eq.selm, SelMode.RHIGHLIGHTED)

        eq = Eq([PJuxt(), ["e"], [PS]], [2], SelMode.LCURSOR)
        self.assertIsInstance(eq, Subeq)
        self.assertIsInstance(eq, EqCore)
        self.assertIsInstance(eq(2), Subeq)
        self.assertNotIsInstance(eq(2), EqCore)
        self.assertEqual(eq.idx, Idx(2))
        self.assertIs(eq.selm, SelMode.LCURSOR)

        eq.idx[:] = [2]
        self.assertIsInstance(eq.idx, Idx)
        eq.idx[0] = 1
        self.assertIsInstance(eq.idx, Idx)

        idx_cp = eq.idx[:]
        # Unintended use
        eq.idx = [1]
        self.assertNotIsInstance(eq.idx, Idx)
        eq.idx = idx_cp[:]

        eq = Eq([OP, [PJuxt(), ["e"], [PS]]])
        self.assertEqual(eq.idx, [])
        self.assertEqual(eq.selm, SelMode.LCURSOR)
        eq = Eq([OP, [PJuxt(), ["e"], [PS]]], [1, 1], SelMode.LCURSOR)
        self.assertEqual(eq.idx, [1, 1])
        self.assertEqual(eq.selm,  SelMode.LCURSOR)

    def test_idx_arg(self):
        idx = [1]
        idx2 = Idx(2)
        eq = Eq([RSUP, ["e"], ["r"]], idx)

        self.assertEqual(eq._idx_arg(idx), idx)
        self.assertIsNot(eq._idx_arg(idx), idx)
        self.assertIsNot(eq._idx_arg(idx), eq.idx)

        self.assertEqual(eq._idx_arg(idx2), idx2)
        self.assertIsNot(eq._idx_arg(idx2), idx2)
        self.assertNotEqual(eq._idx_arg(idx2), eq.idx)

        self.assertEqual(eq._idx_arg(-1), eq.idx)
        self.assertIsNot(eq._idx_arg(-1), eq.idx)

        self.assertEqual(eq._idx_arg(), idx)
        self.assertIsNot(eq._idx_arg(), idx)
        self.assertIsNot(eq._idx_arg(), eq.idx)

        self.assertEqual(eq._idx_arg(None), [])
        self.assertIsNot(eq._idx_arg(None), eq.idx)

        self.assertEqual(eq._idx_arg(2), [2])
        self.assertIsNot(eq._idx_arg(None), eq.idx)

    def test_refidx_arg(self):
        idx = [1]
        idx2 = Idx([2])
        eq = Eq([RSUP, ["e"], ["r"]], idx)

        self.assertEqual(eq._refidx_arg(idx), idx)
        self.assertIsNot(eq._refidx_arg(idx), idx)
        self.assertIsNot(eq._refidx_arg(idx), eq.idx)

        self.assertEqual(eq._refidx_arg(idx2), idx2)
        self.assertIsNot(eq._refidx_arg(idx2), idx2)
        self.assertNotEqual(eq._refidx_arg(idx2), eq.idx)

        self.assertEqual(eq._refidx_arg(-1), eq.idx)
        self.assertIsNot(eq._refidx_arg(-1), eq.idx)

        self.assertEqual(eq._refidx_arg(-1, idx2), eq.idx)
        self.assertIsNot(eq._refidx_arg(-1, idx2), eq.idx)

        self.assertEqual(eq._refidx_arg(), eq.idx)
        self.assertIsNot(eq._refidx_arg(), eq.idx)

        self.assertEqual(eq._refidx_arg(-2, idx2), idx2)
        self.assertIsNot(eq._refidx_arg(-2, idx2), idx2)

        self.assertEqual(eq._refidx_arg(None), [])
        self.assertIsNot(eq._refidx_arg(None), eq.idx)

        self.assertEqual(eq._refidx_arg(None, idx2), [])
        self.assertIsNot(eq._refidx_arg(None, idx2), eq.idx)

        self.assertEqual(eq._refidx_arg(2), [2])

    def test_subeq_arg(self):
        eq = Eq([PJuxt(), ["e"], ["r"]], [1])

        s_in = [PJuxt(3), ["1"], ["2"], ["3"]]
        s_out = eq._subeq_arg(s_in)
        self.assertEqual(s_out, s_in)
        self.assertIsNot(s_out, s_in)
        for pos in range(0, 4):
            self.assertIsNot(s_in[pos], s_out[pos])

        for args in ((), (0,), (0, -1), (0, [1]), (0, 1)):
            s_out = eq._subeq_arg(*args)
            self.assertEqual(s_out, eq(eq.idx))
            self.assertIsNot(s_out, eq(eq.idx))

    def test_set(self):
        eq = Eq([PJuxt(), ["e"], ["r"]])
        l_in = [PJuxt(3), ["1"], ["2"], ["3"]]

        eqref = eq
        eqref_1 = eq[1]
        eq.idx[:] = []
        eq._set(l_in)
        self.assertEqual(eq, l_in)
        self.assertIsNot(eq, l_in)
        for pos in range(0, 4):
            self.assertIsNot(eq[pos], l_in[pos])
        self.assertIsInstance(eq, EqCore)
        self.assertIs(eq, eqref)
        self.assertIsNot(eq[1], eqref_1)
        self.assertNotEqual(eq[1], eqref_1)
        self.assertIsInstance(eq[1], Subeq)
        self.assertNotIsInstance(eq[1], EqCore)

        eq = Eq([PJuxt(), ["e"], ["r"]])
        eqref = eq
        eqref_1 = eq[1]
        eqref_11 = eq(1, 0)
        eq._set(l_in, 1)
        self.assertEqual(eq[1], l_in)
        self.assertIsNot(eq[1], l_in)
        for pos in range(0, 4):
            self.assertEqual(eq(1, pos), l_in[pos])
            self.assertIsNot(eq(1, pos), l_in[pos])
        self.assertNotIsInstance(eq[1], EqCore)
        self.assertIsInstance(eq[1], Subeq)
        self.assertIs(eq, eqref)
        self.assertIs(eq[1], eqref_1)
        self.assertNotEqual(eq(1, 0), eqref_11)

    def test_correctly_point(self):
        for selm in (LH, RH, LC):
            eq = Eq([PJuxt(), ["e"], [PS]], [1], selm)
            for idx in ([], None):
                self.assertEqual(eq._correctly_point(idx, False),
                                 ([1], SelMode.LCURSOR))
                self.assertEqual(eq._correctly_point(idx, True),
                                 ([2], SelMode.RCURSOR))
            for idx in ([1], Idx(1), -1):
                self.assertEqual(eq._correctly_point(idx, False),
                                 ([1], SelMode.LCURSOR))
                self.assertEqual(eq._correctly_point(idx, True),
                                 ([2], SelMode.LCURSOR))

            for idx in ([2], Idx(2)):
                self.assertEqual(eq._correctly_point(idx, False),
                                 ([2], SelMode.LCURSOR))
                self.assertEqual(eq._correctly_point(idx, True),
                                 ([2], SelMode.RCURSOR))

        for selm in SelMode:
            eq = Eq([RSUP, ["e"], [PS]], [], selm)

            for idx in ([], None, -1):
                self.assertEqual(eq._correctly_point(idx, False),
                                 ([], SelMode.LCURSOR))
                self.assertEqual(eq._correctly_point(idx, True),
                                 ([], SelMode.RCURSOR))
            for idx in ([1], Idx(1)):
                self.assertEqual(eq._correctly_point(idx, False),
                                 ([1], SelMode.LCURSOR))
                self.assertEqual(eq._correctly_point(idx, True),
                                 ([1], SelMode.RCURSOR))

            for idx in ([2], Idx(2)):
                self.assertEqual(eq._correctly_point(idx, False),
                                 ([2], SelMode.LCURSOR))
                self.assertEqual(eq._correctly_point(idx, True),
                                 ([2], SelMode.RCURSOR))

            eq = Eq([RSUP, [PVOID], [PVOID]])  # idx == []

            for idx in ([], None, -1):
                self.assertEqual(eq._correctly_point(idx, False),
                                 ([], SelMode.LCURSOR))
                self.assertEqual(eq._correctly_point(idx, True),
                                 ([], SelMode.RCURSOR))
            for idx in ([1], Idx(1)):
                self.assertEqual(eq._correctly_point(idx, False),
                                 ([1], SelMode.LCURSOR))
                self.assertEqual(eq._correctly_point(idx, True),
                                 ([1], SelMode.LCURSOR))

            for idx in ([2], Idx(2)):
                self.assertEqual(eq._correctly_point(idx, False),
                                 ([2], SelMode.LCURSOR))
                self.assertEqual(eq._correctly_point(idx, True),
                                 ([2], SelMode.LCURSOR))

    def test_condtly_correct_scriptop(self):
        for eq in (Eq(["a"]), Eq()):
            for repl in (["repl"], [PS_LO]):
                for idx in ([], Idx(), None):
                    eq_cp = Eq(eq._subeq_arg(0, []))
                    self.assertEqual(
                        eq_cp._condtly_correct_scriptop(repl, idx), [])
                    self.assertEqual(eq, eq_cp)

        eq = Eq([PJuxt(), ["e"], [PS]])
        for repl in (Subeq(["repl"]), Subeq([PS_LO])):
            for idx in ([], [1], [2]):
                for refidx in ([], [1], [2]):
                    eq_cp = Eq(eq._subeq_arg(0, []))
                    self.assertEqual(
                        eq_cp._condtly_correct_scriptop(repl, idx, refidx),
                        refidx)
                    self.assertEqual(eq, eq_cp)

        for repl in (Subeq(["repl"]), Subeq([OP, [PJuxt(), ["d"], ["e"]]])):
            # Change a non-lo base with another non-lo subeq
            for op in CORN_SCR_OPS_LIST + VERT_SCR_OPS_LIST:
                eq = Eq([op] + [["x"]] * op._n_args)
                for i in range(1, op._n_args + 1):
                    eq_cp = Eq(eq._subeq_arg(0, []))
                    self.assertEqual(
                        eq_cp._condtly_correct_scriptop(repl, [1], [i]), [i])
                    self.assertEqual(eq, eq_cp)

                eq = Eq([OP, [op] + [["x"]] * op._n_args])
                for i in range(1, op._n_args + 1):
                    eq_cp = Eq(eq._subeq_arg(0, []))
                    self.assertEqual(eq_cp._condtly_correct_scriptop(
                        repl, [1, 1], [1, i]), [1, i])
                    self.assertEqual(eq, eq_cp)

            for lo_op in LO_SCR_OPS_LIST:
                # Change a lo base with a non-lo subeq
                eq = Eq([lo_op] + [[PS_LO]] * lo_op._n_args)
                eq_cp = Eq(eq._subeq_arg(0, []))
                eq_cp._condtly_correct_scriptop(repl, [1])
                self.assertNotEqual(eq, eq_cp)

                eq = Eq([OP, [lo_op] + [[PS_LO]] * lo_op._n_args])
                eq_cp = Eq(eq._subeq_arg(0, []))
                eq_cp._condtly_correct_scriptop(repl, [1, 1])
                self.assertNotEqual(eq, eq_cp)

        for repl in (Subeq([PS_LO]),
                     Subeq([Op("funargs", 1, lo_base=True), ["d"]])):
            for op in CORN_SCR_OPS_LIST + VERT_SCR_OPS_LIST:
                # Change a non-lo base with a lo subeq
                eq = Eq([op] + [["x"]] * op._n_args)
                for i in range(1, op._n_args + 1):
                    eq_cp = Eq(eq._subeq_arg(0, []))
                    self.assertEqual(
                        eq_cp._condtly_correct_scriptop(repl, [1], [i]), [i])
                    self.assertNotEqual(eq, eq_cp)
                    # NON-LO -> LO only modifies the ScriptOp
                    self.assertEqual(len(eq), len(eq_cp))

                eq = Eq([OP, [op] + [["x"]] * op._n_args])
                for i in range(1, op._n_args + 1):
                    eq_cp = Eq(eq._subeq_arg(0, []))
                    self.assertEqual(
                        eq_cp._condtly_correct_scriptop(repl, [1, 1], [1, i]),
                        [1, i])
                    self.assertNotEqual(eq, eq_cp)
                    # NON-LO -> LO only modifies the ScriptOp
                    self.assertEqual(len(eq[1]), len(eq_cp[1]))

            for lo_op in LO_SCR_OPS_LIST:
                # Change a lo base with a lo subeq
                eq = Eq([lo_op] + [[PS_LO]] * lo_op._n_args)
                for i in range(1, lo_op._n_args + 1):
                    eq_cp = Eq(eq._subeq_arg(0, []))
                    self.assertEqual(
                        eq_cp._condtly_correct_scriptop(repl, [1], [i]), [i])
                    self.assertEqual(eq, eq_cp)

                for i in range(1, lo_op._n_args + 1):
                    eq = Eq([OP, [lo_op] + [[PS_LO]] * lo_op._n_args])
                    eq_cp = Eq(eq._subeq_arg(0, []))
                    self.assertEqual(
                        eq_cp._condtly_correct_scriptop(repl, [1, 1], [1, i]),
                        [1, i])
                    self.assertEqual(eq, eq_cp)

    def test_condtly_correct_scriptop_refs(self):
        # This test just evidences the need of using refindex when calling it
        eq = Eq([RSUP, ["x"], ["y"]])
        eq2 = deepcopy(eq)
        ref1 = eq[1]
        ref2 = eq[2]
        self.assertEqual(eq[0], RSUP)
        self.assertIs(ref1, eq[1])
        self.assertIs(ref2, eq[2])
        eq._condtly_correct_scriptop([PS_LO], [1])
        self.assertNotEqual(eq, eq2)
        eq2[0] = ScriptOp(True, ScriptPos.RSUP)
        self.assertEqual(eq, eq2)
        # Key part
        self.assertIsNot(ref1, eq[1])
        self.assertIsNot(ref2, eq[2])

    def test_rinsert(self):
        for s in (["2"], [PS], [RSUP, ["x"], ["a"]],
                  [OP, [RSUP, ["x"], ["a"]]], [OP, [PJuxt(), ["1"], ["2"]]]):
            eq = Eq(["C"])
            self.assertEqual(eq._rinsert(s, []), [2])
            self.assertEqual(eq, [PJuxt(), ["C"], s])
            # Testing index == -1
            eq.idx[:] = [1]
            self.assertEqual(eq._rinsert(["D"], -1), [2])
            self.assertEqual(eq, [PJuxt(3), ["C"], ["D"], s])
            eq.idx[:] = [3]
            self.assertEqual(eq._rinsert(["F"]), [4])
            self.assertEqual(eq, [PJuxt(4), ["C"], ["D"], s, ["F"]])

        eq = Eq([PJuxt(), ["1"], ["2"]])
        self.assertEqual(eq._rinsert(["3"], [2]), [3])
        self.assertEqual(eq, [PJuxt(3), ["1"], ["2"], ["3"]])
        self.assertEqual(eq._rinsert(["4"], [3]), [4])
        self.assertEqual(eq, [PJuxt(4), ["1"], ["2"], ["3"], ["4"]])
        self.assertEqual(eq._rinsert(["1.5"], [1]), [2])
        self.assertEqual(eq, [PJuxt(5), ["1"], ["1.5"], ["2"], ["3"], ["4"]])
        self.assertEqual(eq._rinsert(["1.7"], [2]), [3])
        self.assertEqual(
            eq, [PJuxt(6), ["1"], ["1.5"], ["1.7"], ["2"], ["3"], ["4"]])
        eq = Eq([PJuxt(), ["1"], ["2"]])
        with self.assertRaises(IndexError):
            eq._rinsert(["e"], [3])

        eq = Eq([RSUB, ["1"], ["2"]])
        self.assertEqual(eq._rinsert([RSUP, ["x"], ["a"]], []), [2])
        self.assertEqual(
            eq, [PJuxt(), [RSUB, ["1"], ["2"]], [RSUP, ["x"], ["a"]]])

        eq = Eq([PJuxt(), ["1"], ["2"]])
        self.assertEqual(eq._rinsert([RSUP, ["x"], ["a"]], [1]), [2])
        self.assertEqual(eq, [PJuxt(3), ["1"], [RSUP, ["x"], ["a"]], ["2"]])
        self.assertEqual(eq._rinsert([RSUB, ["y"], ["0"]], [3]), [4])
        self.assertEqual(eq, [PJuxt(4), ["1"], [RSUP, ["x"], ["a"]], ["2"],
                              [RSUB, ["y"], ["0"]]])

        for s in (["2"], [PS], [RSUP, ["x"], ["a"]],
                  [OP, [RSUP, ["x"], ["a"]]], [OP, [PJuxt(), ["1"], ["2"]]]):
            eq = Eq(s)
            self.assertEqual(eq._rinsert([TJuxt(), ["g"], ["h"]], []), [2])
            self.assertEqual(eq, [PJuxt(), s, [TJuxt(), ["g"], ["h"]]])

        eq = Eq([PJuxt(), ["1"], ["2"]])
        self.assertEqual(eq._rinsert([TJuxt(), ["g"], ["h"]], [2]), [3])
        self.assertEqual(eq, [PJuxt(3), ["1"], ["2"], [TJuxt(), ["g"], ["h"]]])

        eq = Eq([PJuxt(), ["1"], ["2"]])
        self.assertEqual(eq._rinsert([TJuxt(), ["g"], ["h"]], [1]), [2])
        self.assertEqual(eq, [PJuxt(3), ["1"], [TJuxt(), ["g"], ["h"]], ["2"]])
        eq = Eq([PJuxt(), ["1"], ["2"]])
        self.assertEqual(eq._rinsert([TJuxt(), ["g"], ["h"]], [2]), [3])
        self.assertEqual(eq, [PJuxt(3), ["1"], ["2"], [TJuxt(), ["g"], ["h"]]])

        eq = Eq([LORSUP, [PS_LO], ["x"]])
        self.assertEqual(eq._rinsert(["z"], [1]), [1, 2])
        self.assertEqual(eq, [RSUP, [PJuxt(), [PS_LO], ["z"]], ["x"]])

        eq = Eq([LOCSUPRSUP, [PS_LO], ["x"], ["y"]])
        self.assertEqual(eq._rinsert(["z"], [1]), [1, 1, 2])
        self.assertEqual(eq, [RSUP, [CSUP, [PJuxt(), [PS_LO],
                                            ["z"]], ["x"]], ["y"]])

    def test_rinsert_integrating(self):
        for s in ([PJuxt(), ["a"], ["c"]], [TJuxt(3), [PS], ["x"], ["y"]],
                  [PJuxt(4), ["a"], ["b"], ["c"], ["d"]]):
            eq = Eq([PJuxt(), [PS], ["f"]])
            self.assertEqual(eq._rinsert_integrating(s, [1]), [len(s)])
            self.assertEqual(eq, [PJuxt(1 + len(s)), [PS], *s[1:], ["f"]])

        for s in ([PJuxt(), ["a"], ["c"]], [TJuxt(3), [PS], ["x"], ["y"]],
                  [PJuxt(4), ["a"], [PS], ["c"], ["d"]]):

            eq = Eq([PS])
            self.assertEqual(eq._rinsert_integrating(s, []), [len(s)])
            self.assertEqual(eq, [PJuxt(len(s)), [PS], *s[1:]])

            eq = Eq([OP, ["x"]])
            self.assertEqual(eq._rinsert_integrating(s, [1]), [1, len(s)])
            self.assertEqual(eq, [OP, [PJuxt(len(s)), ["x"], *s[1:]]])

            eq = Eq([RSUP, ["a"], ["c"]])
            self.assertEqual(eq._rinsert_integrating(s, [2]), [2, len(s)])
            self.assertEqual(eq, [RSUP, ["a"],
                                  [PJuxt(len(s)), ["c"], *s[1:]]])

    def test_linsert(self):
        for s in (["2"], [PS], [RSUP, ["x"], ["a"]],
                  [OP, [RSUP, ["x"], ["a"]]], [OP, [PJuxt(), ["1"], ["2"]]]):
            eq = Eq(["C"])
            self.assertEqual(eq._linsert(s, []), [2])
            self.assertEqual(eq, [PJuxt(), s, ["C"]])
            # Testing index == -1
            eq.idx[:] = [1]
            self.assertEqual(eq._linsert(["A"], -1), [2])
            self.assertEqual(eq, [PJuxt(3), ["A"], s, ["C"]])
            eq.idx[:] = [3]
            self.assertEqual(eq._linsert(["B"]), [4])
            self.assertEqual(eq, [PJuxt(4), ["A"], s, ["B"], ["C"]])

        eq = Eq([PJuxt(), ["1"], ["2"]])
        self.assertEqual(eq._linsert(["0"], [1]), [2])
        self.assertEqual(eq, [PJuxt(3), ["0"], ["1"], ["2"]])

        eq = Eq([PJuxt(), ["1"], ["2"]])
        self.assertEqual(eq._linsert(["1.5"], [2]), [3])
        self.assertEqual(eq, [PJuxt(3), ["1"], ["1.5"], ["2"]])
        self.assertEqual(eq._linsert(["1.7"], [3]), [4])
        self.assertEqual(eq, [PJuxt(4), ["1"], ["1.5"], ["1.7"], ["2"]])
        self.assertEqual(eq._linsert(["0.5"], [1]), [2])
        self.assertEqual(
            eq, [PJuxt(5), ["0.5"], ["1"], ["1.5"], ["1.7"], ["2"]])
        self.assertEqual(eq._linsert(["0.7"], [2]), [3])
        self.assertEqual(
            eq, [PJuxt(6), ["0.5"], ["0.7"], ["1"], ["1.5"], ["1.7"], ["2"]])
        eq = Eq([PJuxt(), ["1"], ["2"]])
        with self.assertRaises(IndexError):
            eq._linsert(["e"], [3])

        eq = Eq([PJuxt(), ["1"], ["2"]])
        self.assertEqual(eq._linsert([RSUP, ["x"], ["a"]], [1]), [2])
        self.assertEqual(eq, [PJuxt(3), [RSUP, ["x"], ["a"]], ["1"], ["2"]])
        self.assertEqual(eq._linsert([RSUB, ["y"], ["0"]], [3]), [4])
        self.assertEqual(
            eq, [PJuxt(4), [RSUP, ["x"], ["a"]], ["1"], [RSUB, ["y"], ["0"]],
                 ["2"]])

        for s in (["2"], [PS], [RSUP, ["x"], ["a"]],
                  [OP, [RSUP, ["x"], ["a"]]], [OP, [PJuxt(), ["1"], ["2"]]]):
            eq = Eq(s)
            self.assertEqual(eq._linsert([TJuxt(), ["g"], ["h"]], []), [2])
            self.assertEqual(eq, [PJuxt(), [TJuxt(), ["g"], ["h"]], s])

        eq = Eq([LORSUP, [PS_LO], ["x"]])
        self.assertEqual(eq._linsert(["z"], [1]), [1, 2])
        self.assertEqual(eq, [RSUP, [PJuxt(), ["z"], [PS_LO]], ["x"]])

        eq = Eq([LOCSUPRSUP, [PS_LO], ["x"], ["y"]])
        self.assertEqual(eq._linsert(["z"], [1]), [1, 1, 2])
        self.assertEqual(
            eq, [RSUP, [CSUP, [PJuxt(), ["z"], [PS_LO]], ["x"]], ["y"]])

    def test_linsert_integrating(self):
        for s in ([PJuxt(), ["a"], ["c"]], [TJuxt(3), [PS], ["x"], ["y"]],
                  [PJuxt(4), ["a"], ["b"], ["c"], ["d"]]):
            eq = Eq([PJuxt(), [PS], ["f"]])
            self.assertEqual(eq._linsert_integrating(s, [1]), [len(s)])
            self.assertEqual(eq, [PJuxt(1 + len(s)), *s[1:], [PS], ["f"]])

        for s in ([PJuxt(), ["a"], ["c"]], [TJuxt(3), [PS], ["x"], ["y"]],
                  [PJuxt(4), ["a"], [PS], ["c"], ["d"]]):

            eq = Eq([PS])
            self.assertEqual(eq._linsert_integrating(s, []), [len(s)])
            self.assertEqual(eq, [PJuxt(len(s)), *s[1:], [PS]])

            eq = Eq([OP, ["x"]])
            self.assertEqual(eq._linsert_integrating(s, [1]), [1, len(s)])
            self.assertEqual(eq, [OP, [PJuxt(len(s)), *s[1:], ["x"]]])

            eq = Eq([RSUP, ["a"], ["c"]])
            self.assertEqual(eq._linsert_integrating(s, [2]), [2, len(s)])
            self.assertEqual(eq, [RSUP, ["a"],
                                  [PJuxt(len(s)), *s[1:], ["c"]]])

    def test_replace_integrating(self):
        for repl in ([PJuxt(), ["x"], [PS]], [PJuxt(3), ["e"], [PS], [PS_LO]],
                     [TJuxt(3), ["x"], ["y"], ["z"]]):
            # Forcing the juxt-block to be selected (just for testing)
            r1 = Eq(repl)
            r1.idx[:] = []
            def f(eq): return eq._replace_integrating(repl)
            db = (
                (Eq(["a"]), r1, ([], False)),
                (Eq([PVOID]), r1, ([], False)),
                (Eq([PS]), r1, ([], False)),
                (Eq([TJuxt(), ["f"], ["s"]], []), r1, ([], False)),
                (Eq([OP, [PJuxt(), ["a"], ["b"]]], []), r1, ([], False)),
                (Eq([OP, [TJuxt(), ["a"], ["b"]]], [1]),
                    Eq([OP, repl], [1]), ([1], False)),

                (Eq([PJuxt(), ["f"], ["s"]], [1]),
                    Eq([PJuxt(len(repl)), *repl[1:], ["s"]], [1]),
                    ([len(repl) - 1], True)),
                (Eq([PJuxt(), ["f"], ["s"]], [2]),
                    Eq([PJuxt(len(repl)), ["f"], *repl[1:]], [2]),
                    ([len(repl)], True)),

                (Eq([LORSUP, [PS_LO], ["x"]], [1]),
                    Eq([RSUP, repl, ["x"]], [1]),
                    ([1], False)),
                (Eq([LOCSUPRSUP, [PS_LO], ["x"], ["z"]], [1]),
                    Eq([RSUP, [CSUP, repl, ["x"]], ["z"]], [1]),
                    ([1, 1], False)),
            )
            ce = CompareEqs(db)
            ce.assert_equality(f)

    def test_replace(self):
        # Replace a non-GOP block
        for repl in (["r"], [PS], [RSUP, ["x"], ["y"]]):
            def f(eq): return eq._replace(repl)
            hacked_eq = Eq([PJuxt(), ["f"], ["s"]])
            hacked_eq.idx[:] = []
            db = (
                (Eq(["a"]), Eq(repl), []),
                (Eq([PVOID]), Eq(repl), []),
                (Eq([PS]), Eq(repl), []),
                (hacked_eq, Eq(repl), []),
                (Eq([PJuxt(), ["f"], ["s"]], [1]),
                    Eq([PJuxt(), repl, ["s"]], [1]), [1]),
                (Eq([OP, [PJuxt(), ["a"], ["b"]]], [1]),
                    Eq([OP, repl], [1]), [1]),
                (Eq([LORSUP, [PS_LO], ["x"]], [1]),
                    Eq([RSUP, repl, ["x"]], [1]), [1]),
                (Eq([LOCSUPRSUP, [PS_LO], ["x"], ["z"]], [1]),
                    Eq([RSUP, [CSUP, repl, ["x"]], ["z"]], [1]), [1, 1]),
            )
            ce = CompareEqs(db)
            ce.assert_equality(f)

        # Replace a lo-subeq
        def f(eq): return eq._replace([PS_LO])
        hacked_eq = Eq([LOCSUPRSUP, [PS_LO], ["x"], ["z"]])
        hacked_eq.idx[:] = [1, 1]  # Forcing a wrong index
        db = (
            (Eq([RSUP, ["base"], ["x"]], [1]),
             Eq([LORSUP, [PS_LO], ["x"]], [1]), [1]),
            (Eq([RSUP, [CSUP, ["base"], ["x"]], ["z"]], [1]),
             Eq([LORSUP, [PS_LO], ["z"]], [1]), [1]),
            (Eq([RSUP, [CSUP, ["base"], ["x"]], ["z"]], [1, 1]),
                hacked_eq, [1]),
        )
        ce = CompareEqs(db)
        ce.assert_equality(f)

    def test_replace_by_pvoid(self):
        def f(eq): return eq._replace_by_pvoid()
        ipjb = Eq([PJuxt(), ["f"], ["s"]])
        ipjb.idx[:] = []  # Invalid eq
        db = (
            (Eq(["a"]), Eq([PVOID]), []),
            (Eq([PVOID]), Eq([PVOID]), []),
            (Eq([PS]), Eq([PVOID]), []),
            (ipjb, Eq([PVOID]), []),
            (Eq([OP, [PJuxt(), ["a"], ["b"]]], []),
                Eq([PVOID]), []),
            (Eq([OP, [PJuxt(), ["a"], ["b"]]], [1]),
                Eq([OP, [PVOID]], [1]), [1]),
            (Eq([RSUP, ["f"], ["s"]], [1]),
                Eq([RSUP, [PVOID], ["s"]], [1]), [1]),
            (Eq([LORSUP, [PS_LO], ["x"]], [1]),
                Eq([RSUP, [PVOID], ["x"]], [1]), [1]),
            (Eq([LOCSUPRSUP, [PS_LO], ["x"], ["z"]], [1]),
                Eq([RSUP, [CSUP, [PVOID], ["x"]], ["z"]], [1]), [1, 1]),
        )
        ce = CompareEqs(db)
        ce.assert_equality(f)

    def test_vanish_juxted(self):
        def f(eq):
            """Set self.idx and self.selm according to return value."""
            retval = eq._vanish_juxted()
            eq.idx[:], eq.selm = retval
            return retval

        db = (
            (Eq([PJuxt(), ["f"], [PS]], [1], LH), Eq([PS], [], LC)),
            (Eq([PJuxt(), ["f"], [PS]], [1], RH), Eq([PS], [], LC)),
            (Eq([PJuxt(), ["fs"], [PS]], [1], LC), Eq([PS], [], LC)),

            (Eq([PJuxt(), ["f"], [PS]], [2], LH), Eq(["f"], [], RC)),
            (Eq([PJuxt(), ["f"], [PS]], [2], RH), Eq(["f"], [], RC)),
            (Eq([PJuxt(), ["f"], [PS]], [2], LC), Eq(["f"], [], RC)),
            (Eq([PJuxt(), ["f"], [PS]], [2], RC), Eq(["f"], [], RC)),

            (Eq([PJuxt(3), ["f"], ["s"], ["g"]], [1], LH),
                Eq([PJuxt(), ["s"], ["g"]], [1], LC)),
            (Eq([PJuxt(3), ["f"], ["s"], ["g"]], [1], RH),
                Eq([PJuxt(), ["s"], ["g"]], [1], LC)),
            (Eq([PJuxt(3), ["f"], ["s"], ["g"]], [1], LC),
                Eq([PJuxt(), ["s"], ["g"]], [1], LC)),

            (Eq([PJuxt(3), ["f"], ["s"], ["g"]], [2], LH),
                Eq([PJuxt(), ["f"], ["g"]], [2], LC)),
            (Eq([PJuxt(3), ["f"], ["s"], ["g"]], [2], RH),
                Eq([PJuxt(), ["f"], ["g"]], [2], LC)),
            (Eq([PJuxt(3), ["f"], ["s"], ["g"]], [2], LC),
                Eq([PJuxt(), ["f"], ["g"]], [2], LC)),

            (Eq([PJuxt(3), ["f"], ["s"], ["g"]], [3], LH),
                Eq([PJuxt(), ["f"], ["s"]], [2], RC)),
            (Eq([PJuxt(3), ["f"], ["s"], ["g"]], [3], RH),
                 Eq([PJuxt(), ["f"], ["s"]], [2], RC)),
            (Eq([PJuxt(3), ["f"], ["s"], ["g"]], [3], LC),
                Eq([PJuxt(), ["f"], ["s"]], [2], RC)),
            (Eq([PJuxt(3), ["f"], ["s"], ["g"]], [3], RC),
                Eq([PJuxt(), ["f"], ["s"]], [2], RC)),
        )

        ce = CompareEqs(db)
        ce.assert_equality(f)

    def test_vanish_juxted_relpos(self):
        # There are only very few cases of interest. Only those are checked

        # relpos = -1
        def f(eq):
            """Set self.idx and self.selm according to return value."""
            retval = eq._vanish_juxted(-1)
            eq.idx[:], eq.selm = retval
            return retval

        db = (
            (Eq([PJuxt(), ["f"], ["s"]], [2], LC),
                Eq(["s"], [], LC)),
            (Eq([PJuxt(3), ["f"], ["s"], ["g"]], [2], LC),
                Eq([PJuxt(), ["s"], ["g"]], [1], LC)),
            (Eq([PJuxt(3), ["f"], ["s"], ["g"]], [3], LC),
                Eq([PJuxt(), ["f"], ["g"]], [2], LC)),
        )
        ce = CompareEqs(db)
        ce.assert_equality(f)

    def test_vanish_juxted_bases(self):
        def f(eq):
            retval = eq._vanish_juxted()
            eq.idx[:], eq.selm = retval
            return retval

        db = (
            (Eq([RSUP, [PJuxt(), ["x"], ["y"]], ["b"]], [1, 1], LC),
                Eq([RSUP, ["y"], ["b"]], [1], LC)),
            (Eq([RSUP, [PJuxt(), ["x"], ["y"]], ["b"]], [1, 2], LC),
                Eq([RSUP, ["x"], ["b"]], [1], RC)),
            (Eq([RSUP, [PJuxt(), ["x"], ["y"]], ["b"]], [1, 2], RC),
                Eq([RSUP, ["x"], ["b"]], [1], RC)),

            (Eq([RSUP, [PJuxt(), ["x"], [PS_LO]], ["b"]], [1, 1], LC),
                Eq([LORSUP, [PS_LO], ["b"]], [1], LC)),
            (Eq([RSUP, [PJuxt(), [PS_LO], ["y"]], ["b"]], [1, 2], LC),
                Eq([LORSUP, [PS_LO], ["b"]], [1], RC)),
            (Eq([RSUP, [PJuxt(), [PS_LO], ["y"]], ["b"]], [1, 2], RC),
                Eq([LORSUP, [PS_LO], ["b"]], [1], RC)),

            (Eq([RSUP, [PJuxt(3), ["x"], [PS_LO], ["z"]], ["b"]], [1, 1], LC),
                Eq([RSUP, [PJuxt(), [PS_LO], ["z"]], ["b"]], [1, 1], LC)),
            (Eq([RSUP, [PJuxt(3), ["x"], ["y"], [PS_LO]], ["b"]], [1, 2], LC),
                Eq([RSUP, [PJuxt(), ["x"], [PS_LO]], ["b"]], [1, 2], LC)),
        )

        ce = CompareEqs(db)
        ce.assert_equality(f)

        # relpos == - 1
        def f(eq):
            retval = eq._vanish_juxted(-1)
            eq.idx[:], eq.selm = retval
            return retval

        db = (
            (Eq([RSUP, [PJuxt(), ["x"], ["y"]], ["b"]], [1, 2], LC),
                Eq([RSUP, ["y"], ["b"]], [1], LC)),

            (Eq([RSUP, [PJuxt(), ["x"], [PS_LO]], ["b"]], [1, 2], LC),
                Eq([LORSUP, [PS_LO], ["b"]], [1], LC)),

            (Eq([RSUP, [PJuxt(3), ["x"], [PS_LO], ["z"]], ["b"]], [1, 2], LC),
                Eq([RSUP, [PJuxt(), [PS_LO], ["z"]], ["b"]], [1, 1], LC)),
            (Eq([RSUP, [PJuxt(3), ["x"], ["y"], [PS_LO]], ["b"]], [1, 3], LC),
                Eq([RSUP, [PJuxt(), ["x"], [PS_LO]], ["b"]], [1, 2], LC)),
        )

        ce = CompareEqs(db)
        ce.assert_equality(f)

    def test_flat(self):
        def f(self):
            """Output of flat will be assigned to eq.idx."""
            retval = self._flat()
            if retval is not None:
                self.idx[:], self.selm = retval

        # Special cases: RC and tjuxt-block creation/selection
        db = (
            (Eq([Op("O", 3), ["t"], ["x"], ["y"]], [], LH),
                Eq([TJuxt(3), ["t"], ["x"], ["y"]], [], LH)),
            (Eq([Op("O", 3), ["t"], ["x"], ["y"]], [], RH),
                Eq([TJuxt(3), ["t"], ["x"], ["y"]], [], RH)),
            (Eq([Op("O", 3), ["t"], ["x"], ["y"]], [], LC),
                Eq([PJuxt(3), ["t"], ["x"], ["y"]], [1], LC)),
            (Eq([Op("O", 3), ["t"], ["x"], ["y"]], [], RC),
                Eq([PJuxt(3), ["t"], ["x"], ["y"]], [3], RC)),

            (Eq([OP, [RSUP, ["x"], ["y"]]], [], RC),
                Eq([RSUP, ["x"], ["y"]], [], RC)),
            (Eq([OP, [RSUP, ["x"], ["y"]]], [1], LH),
                Eq([OP, [TJuxt(), ["x"], ["y"]]], [1], LH)),
            (Eq([OP, [RSUP, ["x"], ["y"]]], [1], RH),
                Eq([OP, [TJuxt(), ["x"], ["y"]]], [1], RH)),
            (Eq([OP, [RSUP, ["x"], ["y"]]], [1], LC),
                Eq([OP, [PJuxt(), ["x"], ["y"]]], [1, 1], LC)),
            (Eq([OP, [RSUP, ["x"], ["y"]]], [1], RC),
                Eq([OP, [PJuxt(), ["x"], ["y"]]], [1, 2], RC)),

            (Eq([PJuxt(), [RSUP, ["x"], ["y"]], ["a"]], [1], LH),
                Eq([PJuxt(), [TJuxt(), ["x"], ["y"]], ["a"]], [1], LH)),
            (Eq([PJuxt(), [RSUP, ["x"], ["y"]], ["a"]], [1], RH),
                Eq([PJuxt(), [TJuxt(), ["x"], ["y"]], ["a"]], [1], RH)),
            (Eq([PJuxt(), [RSUP, ["x"], ["y"]], ["a"]], [1], LC),
                Eq([PJuxt(3), ["x"], ["y"], ["a"]], [1], LC)),
            (Eq([PJuxt(), ["a"], [RSUP, ["x"], ["y"]]], [2], RC),
                Eq([PJuxt(3), ["a"], ["x"], ["y"]], [3], RC)),

            (Eq([PJuxt(), [TJuxt(), ["x"], ["y"]], ["a"]], [1], LH),
                Eq([PJuxt(), [TJuxt(), ["x"], ["y"]], ["a"]], [1], LH)),
            (Eq([PJuxt(), [TJuxt(), ["x"], ["y"]], ["a"]], [1], RH),
                Eq([PJuxt(), [TJuxt(), ["x"], ["y"]], ["a"]], [1], RH)),
        )

        ce = CompareEqs(db)
        ce.assert_equality(f)

        for sm in (LH, RH, LC):
            db = (
                (Eq([PS], [], sm), Eq([PS], [], sm)),
                (Eq(["a"], [], sm), Eq(["a"], [], sm)),

                (Eq([OP, ["x"]], [], sm), Eq(["x"], [], sm)),
                (Eq([OP, ["x"]], [1], sm), Eq([OP, ["x"]], [1], sm)),

                (Eq([PJuxt(), [OP, ["x"]], ["y"]], [1], sm),
                    Eq([PJuxt(), ["x"], ["y"]], [1], sm)),
                (Eq([PJuxt(), [OP, ["x"]], ["y"]], [2], sm),
                    Eq([PJuxt(), [OP, ["x"]], ["y"]], [2], sm)),

                (Eq([RSUP, [PVOID], ["y"]], [], sm),
                    Eq(["y"], [], sm)),
                (Eq([RSUP, [PVOID], [PVOID]], [], sm),
                    Eq([PVOID], [], LC)),
                (Eq([PJuxt(3),
                        ["a"], [RSUP, [PVOID], [PVOID]], ["c"]], [2], sm),
                    Eq([PJuxt(), ["a"], ["c"]], [2], LC)),
                (Eq([Op("O", 3), ["a"], [RSUP, [PVOID], [PVOID]], ["c"]],
                        [2], sm),
                    Eq([Op("O", 3), ["a"], [PVOID], ["c"]], [2], LC)),
                (Eq([RSUP, [PVOID], ["y"]], [1], sm),
                    Eq([RSUP, [PVOID], ["y"]], [1], sm)),
                (Eq([RSUP, ["x"], [PVOID]], [2], sm),
                    Eq([RSUP, ["x"], [PVOID]], [2], sm)),
            )

            ce = CompareEqs(db)
            ce.assert_equality(f)

    def test_flat_bases(self):
        def f(self):
            """Output of flat will be assigned to eq.idx."""
            retval = self._flat()
            if retval is not None:
                self.idx[:], self.selm = retval

        op_lo = Op("O", 1, lo_base=True)
        for sm in (LH, RH, LC):
            db = (
                (Eq([LORSUP, [op_lo, ["x"]], ["a"]], [1], sm),
                    Eq([RSUP, ["x"], ["a"]], [1], sm)),
                (Eq([LORSUP, [op_lo, ["x"]], ["a"]], [2]),
                    Eq([LORSUP, [op_lo, ["x"]], ["a"]], [2])),
                (Eq([LORSUP, [op_lo, ["x"]], ["a"]], [1, 1], sm),
                    Eq([LORSUP, [op_lo, ["x"]], ["a"]], [1, 1], sm)),

                (Eq([RSUP, [Op("O", 2), [PS_LO], [PVOID]], ["a"]], [1], sm),
                    Eq([LORSUP, [PS_LO], ["a"]], [1], sm)),
                (Eq([RSUP, [CSUP, [Op("O", 2), [PS_LO],
                                   [PVOID]], ["a"]], ["b"]], [1, 1, 1], sm),
                    Eq([RSUP, [CSUP, [Op("O", 2), [PS_LO], [PVOID]],
                                      ["a"]], ["b"]], [1, 1, 1], sm)),
                (Eq([RSUP, [CSUP, [Op("O", 2), [PS_LO],
                                   [PVOID]], ["a"]], ["b"]], [1, 1], sm),
                    Eq([LOCSUPRSUP, [PS_LO], ["a"], ["b"]], [1], sm)),
                (Eq([LOCSUPRSUP, [op_lo, ["x"]], ["a"], ["b"]], [1], sm),
                    Eq([RSUP, [CSUP, ["x"], ["a"]], ["b"]], [1, 1], sm)),
            )
            ce = CompareEqs(db)
            ce.assert_equality(f)

    def test_flat_supeq(self):
        def f(eq):
            """Set idx and selm to output value."""
            retval = eq._flat_supeq()
            if retval is not None:
                eq.idx[:], eq.selm = retval

        # Some particular cases: RC
        db = (
            (Eq([PJuxt(), ["x"], ["y"]], [2], RC),
                Eq([PJuxt(), ["x"], ["y"]], [2], RC)),
            (Eq([RSUP, ["x"], ["y"]], [1], RC),
                Eq([PJuxt(), ["x"], ["y"]], [2], LC)),
            (Eq([PJuxt(), [PVOID], ["y"]], [2], RC),
                Eq(["y"], [], RC)),
            (Eq([PJuxt(3), ["x"], [PVOID], ["y"]], [3], RC),
                Eq([PJuxt(), ["x"], ["y"]], [2], RC)),
            (Eq([PJuxt(), [RSUP, ["x"], ["y"]], ["a"]], [1, 2], RC),
                Eq([PJuxt(3), ["x"], ["y"], ["a"]], [3], LC)),
        )
        ce = CompareEqs(db)
        ce.assert_equality(f)

        for sm in (LH, RH, LC):
            db = (
                (Eq([PVOID], [], sm), Eq([PVOID], [], sm)),
                (Eq(["a"], [], sm), Eq(["a"], [], sm)),
                (Eq([RSUP, ["x"], ["y"]], [], sm),
                    Eq([RSUP, ["x"], ["y"]], [], sm)),
                (Eq([PJuxt(), ["x"], ["y"]], [], sm),
                    Eq([PJuxt(), ["x"], ["y"]], [], sm)),
                (Eq([PJuxt(), ["x"], ["y"]], [1]),
                    Eq([PJuxt(), ["x"], ["y"]], [1])),
                (Eq([PJuxt(), ["x"], ["y"]], [2]),
                    Eq([PJuxt(), ["x"], ["y"]], [2])),

                (Eq([RSUP, ["x"], ["y"]], [1], sm),
                    Eq([PJuxt(), ["x"], ["y"]], [1], sm)),
                (Eq([RSUP, ["x"], ["y"]], [2], sm),
                    Eq([PJuxt(), ["x"], ["y"]], [2], sm)),

                (Eq([PJuxt(), [PVOID], ["y"]], [1], sm),
                    Eq(["y"], [], LC)),
                (Eq([PJuxt(), [PVOID], ["y"]], [2], sm),
                    Eq(["y"], [], sm)),
                (Eq([PJuxt(3), ["x"], [PVOID], ["y"]], [1], sm),
                    Eq([PJuxt(), ["x"], ["y"]], [1], sm)),
                (Eq([PJuxt(3), ["x"], [PVOID], ["y"]], [2], sm),
                    Eq([PJuxt(), ["x"], ["y"]], [2], LC)),
                (Eq([PJuxt(3), ["x"], [PVOID], ["y"]], [3], sm),
                    Eq([PJuxt(), ["x"], ["y"]], [2], sm)),
                (Eq([PJuxt(), [PVOID], [PVOID]], [1], sm),
                    Eq([PVOID], [], LC)),
                (Eq([PJuxt(), [PVOID], [PVOID]], [2], sm),
                    Eq([PVOID], [], LC)),

                (Eq([PJuxt(), [RSUP, ["x"], ["y"]], ["a"]], [1], sm),
                    Eq([PJuxt(), [RSUP, ["x"], ["y"]], ["a"]], [1], sm)),

                (Eq([PJuxt(), [RSUP, ["x"], ["y"]], ["a"]], [1, 1], sm),
                    Eq([PJuxt(3), ["x"], ["y"], ["a"]], [1], sm)),
                (Eq([PJuxt(), [RSUP, ["x"], ["y"]], ["a"]], [1, 2], sm),
                    Eq([PJuxt(3), ["x"], ["y"], ["a"]], [2], sm)),

                (Eq([RSUP, [PVOID], ["y"]], [1], sm),
                    Eq(["y"], [], LC)),
                (Eq([RSUP, [PVOID], ["y"]], [2], sm),
                    Eq(["y"], [], sm)),
                (Eq([RSUP, ["y"], [PVOID]], [1], sm),
                    Eq(["y"], [], sm)),
                (Eq([RSUP, ["y"], [PVOID]], [2], sm),
                    Eq(["y"], [], RC)),

                (Eq([PJuxt(), [RSUP, [PVOID], ["y"]], ["a"]], [1, 1], sm),
                    Eq([PJuxt(), ["y"], ["a"]], [1], LC)),
                (Eq([PJuxt(), [RSUP, [PVOID], ["y"]], ["a"]], [1, 2], sm),
                    Eq([PJuxt(), ["y"], ["a"]], [1], sm)),
                (Eq([PJuxt(), [RSUP, ["x"], [PVOID]], ["a"]], [1, 1], sm),
                    Eq([PJuxt(), ["x"], ["a"]], [1], sm)),
                (Eq([PJuxt(), [RSUP, ["x"], [PVOID]], ["a"]], [1, 2], sm),
                    Eq([PJuxt(), ["x"], ["a"]], [2], LC)),
                (Eq([PJuxt(), ["a"], [RSUP, ["x"], [PVOID]]], [2, 1], sm),
                    Eq([PJuxt(), ["a"], ["x"]], [2], sm)),
                (Eq([PJuxt(), ["a"], [RSUP, ["x"], [PVOID]]], [2, 2], sm),
                    Eq([PJuxt(), ["a"], ["x"]], [2], RC)),

                (Eq([PJuxt(), [Op("O", 3), ["x"], ["y"], ["z"]], ["a"]],
                        [1, 1], sm),
                    Eq([PJuxt(4), ["x"], ["y"], ["z"], ["a"]], [1], sm)),
                (Eq([PJuxt(), [Op("O", 3), ["x"], ["y"], ["z"]], ["a"]],
                        [1, 2], sm),
                    Eq([PJuxt(4), ["x"], ["y"], ["z"], ["a"]], [2], sm)),
                (Eq([PJuxt(), [Op("O", 3), ["x"], ["y"], ["z"]], ["a"]],
                        [1, 3], sm),
                    Eq([PJuxt(4), ["x"], ["y"], ["z"], ["a"]], [3], sm)),

            )

            ce = CompareEqs(db)
            ce.assert_equality(f)

    def test_flat_supeq_bases(self):
        def f(eq):
            """Set idx and selm to output value."""
            retval = eq._flat_supeq()
            if retval is not None:
                eq.idx[:], eq.selm = retval

        op_lo = Op("O", 1, lo_base=True)

        # Particular cases: RC
        db = (
            (Eq([LORSUP, [op_lo, ["x"]], ["a"]], [1, 1], RC),
                Eq([RSUP, ["x"], ["a"]], [1], RC)),
            (Eq([RSUP, [OP, [op_lo, ["x"]]], ["a"]], [1, 1], RC),
                Eq([LORSUP, [op_lo, ["x"]], ["a"]], [1], RC)),
            (Eq([RSUP, [CSUP, [OP, [op_lo, ["x"]]], ["g"]], ["a"]],
                    [1, 1, 1], RC),
                Eq([LOCSUPRSUP, [op_lo, ["x"]], ["g"], ["a"]], [1], RC)),
        )
        ce = CompareEqs(db)
        ce.assert_equality(f)

        for sm in (LH, RH, LC):
            db = (
                (Eq([LORSUP, [op_lo, ["x"]], ["a"]], [1], sm),
                    Eq([PJuxt(), [op_lo, ["x"]], ["a"]], [1], sm)),
                (Eq([LORSUP, [op_lo, ["x"]], ["a"]], [2], sm),
                    Eq([PJuxt(), [op_lo, ["x"]], ["a"]], [2], sm)),
                (Eq([LORSUP, [op_lo, ["x"]], ["a"]], [1, 1], sm),
                    Eq([RSUP, ["x"], ["a"]], [1], sm)),
                (Eq([RSUP, [OP, [op_lo, ["x"]]], ["a"]], [1, 1], sm),
                    Eq([LORSUP, [op_lo, ["x"]], ["a"]], [1], sm)),
                (Eq([RSUP, [CSUP, [OP, [op_lo, ["x"]]], ["g"]], ["a"]],
                        [1, 1, 1], sm),
                    Eq([LOCSUPRSUP, [op_lo, ["x"]], ["g"], ["a"]], [1], sm)),
            )
            ce = CompareEqs(db)
            ce.assert_equality(f)


if __name__ == '__main__':
    unittest.main()
