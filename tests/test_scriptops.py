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
from collections import OrderedDict

from visualequation.ops import *
from visualequation.dirsel import Dir
from visualequation.idx import Idx
from visualequation.subeqs import Subeq
from visualequation.scriptops import *
from tests.test_utils import *


class ScriptOpsTests(unittest.TestCase):
    def test_equivalent_op(self):
        ops = OrderedDict()
        for lo_op in LOSCRIPT_OPS_LIST:
            nonlo_pair = test_equivalent_op(lo_op)
            self.assertEqual(test_equivalent_op(nonlo_pair[0], nonlo_pair[1]),
                             (lo_op, None))
            if nonlo_pair[1] is not None:
                self.assertEqual(test_equivalent_op(nonlo_pair[1],
                                                    nonlo_pair[0]),
                                 (lo_op, None))
            ops[nonlo_pair] = lo_op
        self.assertEqual(len(ops), 63)

        for t in (pair[1].type_ for pair in ops if pair[1] is not None):
            # External \*script op after transformation, if any, must be script
            # by convention
            self.assertEqual(t, "script")

    def test_update_scriptblock(self):
        def f(eq):
            retval = update_scriptblock(eq(eq.idx), eq, eq.idx, eq.idx)
            eq.idx = retval
            return eq

        db = (
            (Eq(["a"]), Eq(["a"])),
            (Eq([PJUXT, ["d"], ["f"]]), Eq([PJUXT, ["d"], ["f"]])),
            (Eq([PJUXT, ["d"], ["f"]], [1]),
                Eq([PJUXT, ["d"], ["f"]], [1])),
            (Eq([PJUXT, ["d"], ["f"]], [2]),
                Eq([PJUXT, ["d"], ["f"]], [2])),
        )
        ce = CompareEqs(db)
        ce.assert_equality(f, is_method=False)

        def f_lo(eq):
            eq.idx = update_scriptblock([Op("O", "O", 0, "vs")], eq)
            return eq

        def f_nonlo(eq):
            eq.idx = update_scriptblock(["base"], eq)
            return eq

        n_single_ops = 0
        for op in SETSCRIPT_OPS_LIST + SCRIPT_OPS_LIST:
            n_single_ops += 1

            new_op = test_equivalent_op(op)[0]
            db = (
                (Eq(["a"]), Eq(["a"], [])),
                (Eq([op] + [["x"]]*op.n_args),
                    Eq([new_op] + [["x"]]*new_op.n_args)),
            )
            # non-lo -> lo
            ce = CompareEqs(db)
            ce.assert_equality(f_lo, is_method=False)

            # lo ->  non-lo
            ce.assert_equality(f_nonlo, is_method=False, inversely=True)

            # non-lo -> non-lo
            ce.eq_out_bkp = ce.eq_out[:]
            ce.eq_out[:] = ce.eq_in[:]
            ce.assert_equality(f_nonlo, is_method=False)

            # lo -> lo
            ce.eq_out[:] = ce.eq_out_bkp[:]
            ce.eq_in[:] = ce.eq_out_bkp[:]
            ce.assert_equality(f_lo, is_method=False, inversely=True)

        self.assertEqual(n_single_ops, 15+3)

        def f_lo1(eq):
            eq.idx = update_scriptblock([Op("O", "O", 0, "vs")], eq, [1])
            return eq

        def f_nonlo1(eq):
            eq.idx = update_scriptblock(["base"], eq, [1])
            return eq

        ce = CompareEqs()
        ce_reversed = CompareEqs()
        n_combined_ops = 0
        for op1 in SETSCRIPT_OPS_LIST:
            for op2 in SCRIPT_OPS_LIST:
                n_combined_ops += 1
                block1 = [op2] + [["x"]] * op2.n_args
                block_scr_in = [op1] + [block1] + [["x"]] * (op1.n_args - 1)
                block2 = [op1] + [["x"]] * op1.n_args
                block_scr_out = [op2] + [block2] + [["x"]] * (op2.n_args - 1)
                e_op = test_equivalent_op(op1, op2)[0]
                result = [e_op] + [["x"]]*e_op.n_args
                ce.add_pair(block_scr_out, result)
                ce_reversed.add_pair(block_scr_in, result)

                block_correct = f_nonlo(Eq(result))
                self.assertNotEqual(block_scr_in, block_correct)
                self.assertEqual(block_scr_out, block_correct)

        self.assertEqual(n_combined_ops, 15*3)

        # non-lo -> lo
        ce.assert_equality(f_lo1, is_method=False)
        ce_reversed.assert_equality(f_lo1, is_method=False)

        # lo -> non-lo
        ce.assert_equality(f_nonlo, is_method=False, inversely=True)

        # lo -> lo
        ce.eq_in_bkp = ce.eq_in[:]
        ce.eq_in[:] = ce.eq_out[:]
        ce.assert_equality(f_lo, is_method=False)
        ce_reversed.eq_in_bkp = ce_reversed.eq_in[:]
        ce_reversed.eq_in[:] = ce_reversed.eq_out[:]
        ce_reversed.assert_equality(f_lo, is_method=False)

        # non-lo -> non-lo
        ce.eq_in[:] = ce.eq_in_bkp[:]
        ce.eq_out[:] = ce.eq_in_bkp[:]
        ce.assert_equality(f_nonlo1, is_method=False)
        ce_reversed.eq_in[:] = ce_reversed.eq_in_bkp[:]
        ce_reversed.eq_out[:] = ce_reversed.eq_in_bkp[:]
        ce_reversed.assert_equality(f_nonlo1, is_method=False)

    def test_update_scriptblock_retvals_single(self):
        def f_creator(newbase, index):
            def wrapper(eq):
                refidx = eq.idx[:]
                eq.idx[:] = update_scriptblock(newbase, eq, index, refidx)
                return eq
            return wrapper

        flo = f_creator([Op("O", "O", 0, "vs")], [])
        flo1 = f_creator([Op("O", "O", 0, "vs")], [1])
        fnonlo = f_creator(["z"], [])
        fnonlo1 = f_creator(["z"], [1])

        p = [PJUXT, ["a"], ["b"]]
        for op in SETSCRIPT_OPS_LIST + SCRIPT_OPS_LIST:
            e_op = test_equivalent_op(op)[0]

            db = (
                (Eq([PJUXT] + [["x"]] * op.n_args, []),
                 Eq([PJUXT] + [["x"]] * op.n_args, [])),
                (Eq([op] + [["x"]] * op.n_args, []),
                 Eq([e_op] + [["x"]] * op.n_args, [])),
            )
            ce = CompareEqs(db)
            ce.assert_equality(flo, is_method=False)
            ce.assert_equality(fnonlo, is_method=False, inversely=True)

            db = (
                (Eq([PJUXT] + [["x"]] * op.n_args, []),
                 Eq([PJUXT] + [["x"]] * op.n_args, [])),
                (Eq([PJUXT, [op] + [["x"]] * op.n_args, ["y"]], []),
                 Eq([PJUXT, [e_op] + [["x"]] * op.n_args, ["y"]], [])),
                (Eq([PJUXT, [op] + [["x"]] * op.n_args, ["y"]], [1]),
                 Eq([PJUXT, [e_op] + [["x"]] * op.n_args, ["y"]], [1])),
                (Eq([PJUXT, [op] + [["x"]] * op.n_args, ["y"]], [2]),
                 Eq([PJUXT, [e_op] + [["x"]] * op.n_args, ["y"]], [2])),
            )
            ce = CompareEqs(db)
            ce.assert_equality(flo1, is_method=False)
            ce.assert_equality(fnonlo1, is_method=False, inversely=True)

            for n in range(1, op.n_args + 1):
                db = (
                    (Eq([PJUXT] + [["x"]] * op.n_args, [n]),
                     Eq([PJUXT] + [["x"]] * op.n_args, [n])),

                    (Eq([op] + [["x"]] * op.n_args, [n]),
                     Eq([e_op] + [["x"]] * op.n_args, [n])),

                    (Eq([op] + [p] + [["x"]] * (op.n_args - 1), [n]),
                     Eq([e_op] + [p] + [["x"]] * (op.n_args - 1), [n])),

                    (Eq([op] + [["x"]] * op.n_args, [n]),
                     Eq([e_op] + [["x"]] * op.n_args, [n])),
                    (Eq([op] + [p] * op.n_args, [n, 1]),
                     Eq([e_op] + [p] * op.n_args, [n, 1])),
                    (Eq([op] + [p] * op.n_args, [n, 2]),
                     Eq([e_op] + [p] * op.n_args, [n, 2])),
                )
                ce = CompareEqs(db)
                ce.assert_equality(flo, is_method=False)
                ce.assert_equality(fnonlo, is_method=False, inversely=True)

                db = (
                    (Eq([PJUXT] + [["x"]] * op.n_args, [n]),
                     Eq([PJUXT] + [["x"]] * op.n_args, [n])),

                    (Eq([PJUXT, [op] + [p] * op.n_args, ["y"]], [1, n]),
                     Eq([PJUXT, [e_op] + [p] * op.n_args, ["y"]], [1, n])),
                    (Eq([PJUXT, [op] + [p] * op.n_args, ["y"]], [1, n, 1]),
                     Eq([PJUXT, [e_op] + [p] * op.n_args, ["y"]], [1, n, 1])),
                    (Eq([PJUXT, [op] + [p] * op.n_args, ["y"]], [1, n, 2]),
                     Eq([PJUXT, [e_op] + [p] * op.n_args, ["y"]], [1, n, 2])),
                )
                ce = CompareEqs(db)
                ce.assert_equality(flo1, is_method=False)
                ce.assert_equality(fnonlo1, is_method=False, inversely=True)

    # Extensive tests, but code is asking for a serious refactoring
    def test_update_scriptblock_retvals_pairs(self):
        """This test is slower than the rest (~ x10)"""
        def f_creator(newbase, index):
            def wrapper(eq):
                refidx = eq.idx[:]
                eq.idx[:] = update_scriptblock(newbase, eq, index, refidx)
                return eq

            return wrapper

        flo = f_creator([Op("O", "O", 0, "vs")], [])
        flo1 = f_creator([Op("O", "O", 0, "vs")], [1])
        flo11 = f_creator([Op("O", "O", 0, "vs")], [1, 1])
        fnonlo = f_creator(["z"], [])
        fnonlo1 = f_creator(["z"], [1])
        fnonlo11 = f_creator(["z"], [1, 1])

        p = [PJUXT, ["a"], ["b"]]
        for op_set in SETSCRIPT_OPS_LIST:
            for op_scr in SCRIPT_OPS_LIST:
                sb_scr_set = [op_scr] + [[op_set] + [p] * op_set.n_args] \
                              + [p] * (op_scr.n_args - 1)
                sb_set_scr = [op_set] + [[op_scr] + [p] * op_scr.n_args] \
                              + [p] * (op_set.n_args - 1)

                e_op = test_equivalent_op(op_set, op_scr)[0]
                e_op_scr = test_equivalent_op(op_scr)[0]
                e_op_set = test_equivalent_op(op_set)[0]
                sb_e = [e_op] +  [p] * e_op.n_args
                sb_e_scr = [e_op_scr] + [[op_set] + [p] * op_set.n_args] \
                             + [p] * (op_scr.n_args - 1)
                sb_e_set = [e_op_set] + [[op_scr] + [p] * op_scr.n_args] \
                             + [p] * (op_set.n_args - 1)
                # Act on []
                db_scr = (
                    (Eq([PJUXT, sb_scr_set, p], []),
                     Eq([PJUXT, sb_scr_set, p], [])),
                    (Eq([PJUXT, sb_scr_set, p], [1]),
                     Eq([PJUXT, sb_scr_set, p], [1])),
                    (Eq([PJUXT, sb_scr_set, p], [1, 1]),
                     Eq([PJUXT, sb_scr_set, p], [1, 1])),
                    (Eq([PJUXT, sb_scr_set, p], [2]),
                     Eq([PJUXT, sb_scr_set, p], [2])),
                )
                db_set = (
                    (Eq([PJUXT, sb_set_scr, p], []),
                     Eq([PJUXT, sb_set_scr, p], [])),
                    (Eq([PJUXT, sb_set_scr, p], [1]),
                     Eq([PJUXT, sb_set_scr, p], [1])),
                    (Eq([PJUXT, sb_set_scr, p], [1, 1]),
                     Eq([PJUXT, sb_set_scr, p], [1, 1])),
                    (Eq([PJUXT, sb_set_scr, p], [2]),
                     Eq([PJUXT, sb_set_scr, p], [2])),
                )
                ce = CompareEqs(db_scr + db_set)
                ce.assert_equality(flo, is_method=False)
                ce.assert_equality(fnonlo, is_method=False, inversely=True)
                ce.eq_in_bkp = ce.eq_in[:]
                ce.eq_in[:] = ce.eq_out[:]
                ce.assert_equality(flo, is_method=False)
                ce.eq_in[:] = ce.eq_in_bkp[:]
                ce.eq_out[:] = ce.eq_in_bkp[:]
                ce.assert_equality(fnonlo, is_method=False)

                # Act on [1]
                db1_scr = (
                    (Eq([PJUXT, sb_scr_set, p], []),
                     Eq([PJUXT, sb_e_scr,   p], [])),
                    (Eq([PJUXT, sb_scr_set, p], [1]),
                     Eq([PJUXT, sb_e_scr,   p], [1])),
                    (Eq([PJUXT, sb_scr_set, p], [1, 1]),
                     Eq([PJUXT, sb_e_scr,   p], [1, 1])),
                    (Eq([PJUXT, sb_scr_set, p], [2]),
                     Eq([PJUXT, sb_e_scr,   p], [2])),
                )
                db1_set = (
                    (Eq([PJUXT, sb_set_scr, p], []),
                     Eq([PJUXT, sb_e_set,   p], [])),
                    (Eq([PJUXT, sb_set_scr, p], [1]),
                     Eq([PJUXT, sb_e_set,   p], [1])),
                    (Eq([PJUXT, sb_set_scr, p], [1, 1]),
                     Eq([PJUXT, sb_e_set,   p], [1, 1])),
                    (Eq([PJUXT, sb_set_scr, p], [2]),
                     Eq([PJUXT, sb_e_set,   p], [2])),
                )
                ce = CompareEqs(db1_scr + db1_set)
                ce.assert_equality(flo1, is_method=False)
                ce.assert_equality(fnonlo1, is_method=False, inversely=True)
                ce.eq_in_bkp = ce.eq_in[:]
                ce.eq_in[:] = ce.eq_out[:]
                ce.assert_equality(flo1, is_method=False)
                ce.eq_in[:] = ce.eq_in_bkp[:]
                ce.eq_out[:] = ce.eq_in_bkp[:]
                ce.assert_equality(fnonlo1, is_method=False)

                # Act on [1, 1]
                db11_scr = (
                    (Eq([PJUXT, sb_scr_set, p], []),
                     Eq([PJUXT, sb_e,       p], [])),
                    (Eq([PJUXT, sb_scr_set, p], [1]),
                     Eq([PJUXT, sb_e,       p], [1])),
                    (Eq([PJUXT, sb_scr_set, p], [2]),
                     Eq([PJUXT, sb_e,       p], [2])),
                )
                db11_set = (
                    (Eq([PJUXT, sb_set_scr, p], []),
                     Eq([PJUXT, sb_e,       p], [])),
                    (Eq([PJUXT, sb_set_scr, p], [1]),
                     Eq([PJUXT, sb_e,       p], [1])),
                    (Eq([PJUXT, sb_set_scr, p], [2]),
                     Eq([PJUXT, sb_e,       p], [2])),
                )
                ce = CompareEqs(db11_scr + db11_set)
                ce.assert_equality(flo11, is_method=False)
                # Inverse test is done below
                ce.eq_in_bkp = ce.eq_in[:]
                ce.eq_in[:] = ce.eq_out[:]
                ce.assert_equality(flo11, is_method=False)
                ce.eq_in[:] = ce.eq_in_bkp[:]
                ce.eq_out[:] = ce.eq_in_bkp[:]
                ce.assert_equality(fnonlo11, is_method=False)

                ce = CompareEqs(db11_scr)
                # It uses fnonlo1 because it operates inversely, but it refers
                # to the 11 case.
                ce.assert_equality(fnonlo1, is_method=False, inversely=True)
                # Usual tests has been done before

                db11_special = (
                    (Eq([PJUXT, sb_scr_set, p], [1, 1]),
                     Eq([PJUXT, sb_e,       p], [1])),
                    (Eq([PJUXT, sb_set_scr, p], [1, 1]),
                     Eq([PJUXT, sb_e,       p], [1])),
                )
                ce = CompareEqs(db11_special)
                ce.assert_equality(flo11, is_method=False)
                ce.eq_out[:] = ce.eq_in[:]
                ce.assert_equality(fnonlo11, is_method=False)

                db11_special_bis = (
                    (Eq([PJUXT, sb_e, p], [1, 1]),
                     Eq([PJUXT, sb_e, p], [1, 1])),
                )
                ce = CompareEqs(db11_special_bis)
                ce.assert_equality(flo11, is_method=False)

                for n_scr in range(2, op_scr.n_args + 1):
                    # Act on []
                    db = (
                        (Eq([PJUXT, sb_scr_set, p], [1, n_scr]),
                         Eq([PJUXT, sb_scr_set, p], [1, n_scr])),
                        (Eq([PJUXT, sb_scr_set, p], [1, n_scr, 1]),
                         Eq([PJUXT, sb_scr_set, p], [1, n_scr, 1])),
                        (Eq([PJUXT, sb_scr_set, p], [1, n_scr, 2]),
                         Eq([PJUXT, sb_scr_set, p], [1, n_scr, 2])),
                        (Eq([PJUXT, sb_set_scr, p], [1, 1, n_scr]),
                         Eq([PJUXT, sb_set_scr, p], [1, 1, n_scr])),
                        (Eq([PJUXT, sb_set_scr, p], [1, 1, n_scr, 1]),
                         Eq([PJUXT, sb_set_scr, p], [1, 1, n_scr, 1])),
                        (Eq([PJUXT, sb_set_scr, p], [1, 1, n_scr, 2]),
                         Eq([PJUXT, sb_set_scr, p], [1, 1, n_scr, 2])),
                    )
                    ce = CompareEqs(db)
                    ce.assert_equality(flo, is_method=False)
                    ce.assert_equality(fnonlo, is_method=False,
                                       inversely=True)
                    ce.eq_in_bkp = ce.eq_in[:]
                    ce.eq_in[:] = ce.eq_out[:]
                    ce.assert_equality(flo, is_method=False)
                    ce.eq_in[:] = ce.eq_in_bkp[:]
                    ce.eq_out[:] = ce.eq_in_bkp[:]
                    ce.assert_equality(fnonlo, is_method=False)

                    # Act on [1]
                    db1 = (
                        (Eq([PJUXT, sb_scr_set, p], [1, n_scr]),
                         Eq([PJUXT, sb_e_scr,   p], [1, n_scr])),
                        (Eq([PJUXT, sb_scr_set, p], [1, n_scr, 1]),
                         Eq([PJUXT, sb_e_scr,   p], [1, n_scr, 1])),
                        (Eq([PJUXT, sb_scr_set, p], [1, n_scr, 2]),
                         Eq([PJUXT, sb_e_scr,   p], [1, n_scr, 2])),
                        # Unintended use since the base would be modified
                        (Eq([PJUXT, sb_set_scr, p], [1, 1, n_scr]),
                         Eq([PJUXT, sb_e_set,   p], [1, 1, n_scr])),
                    )
                    ce = CompareEqs(db1)
                    ce.assert_equality(flo1, is_method=False)
                    ce.assert_equality(fnonlo1, is_method=False,
                                       inversely=True)
                    ce.eq_in_bkp = ce.eq_in[:]
                    ce.eq_in[:] = ce.eq_out[:]
                    ce.assert_equality(flo1, is_method=False)
                    ce.eq_in[:] = ce.eq_in_bkp[:]
                    ce.eq_out[:] = ce.eq_in_bkp[:]
                    ce.assert_equality(fnonlo1, is_method=False)

                    # Act on [1, 1]
                    # This section trusts in updated eqs but not in retvals

                    # Surface
                    k1 = Subeq([PJUXT, ["k11"], ["k12"]])
                    s1 = deepcopy(Subeq([PJUXT, sb_scr_set, p]))
                    sub1 = s1([1, n_scr])
                    sub1[:] = k1
                    e_s1 = deepcopy(s1)
                    update_scriptblock([Op("O", "O", 0, "vs")], e_s1, [1, 1])
                    e_sub1 = e_s1(1)
                    e_pos_k1 = e_sub1.index(k1)

                    # Deeper
                    k2 = Subeq([PJUXT, ["k21"], ["k22"]])
                    s2 = deepcopy(Subeq([PJUXT, sb_set_scr, p]))
                    sub2 = s2([1, 1, n_scr])
                    sub2[:] = k2
                    e_s2 = deepcopy(s2)
                    update_scriptblock([Op("O", "O", 0, "vs")], e_s2, [1, 1])
                    e_sub2 = e_s2(1)
                    e_pos_k2 = e_sub2.index(k2)

                    db11_scr = (
                        (Eq(s1, [1, n_scr]),
                         Eq(e_s1, [1, e_pos_k1])),
                        (Eq(s1, [1, n_scr, 1]),
                         Eq(e_s1, [1, e_pos_k1, 1])),
                    )
                    db11_set = (
                        (Eq(s2, [1, 1, n_scr]),
                         Eq(e_s2, [1, e_pos_k2])),
                        (Eq(s2, [1, 1, n_scr, 1]),
                         Eq(e_s2, [1, e_pos_k2, 1])),
                    )
                    ce = CompareEqs(db11_scr + db11_set)
                    ce.assert_equality(flo11, is_method=False)
                    # Inverse is done below
                    ce.eq_in_bkp = ce.eq_in[:]
                    ce.eq_in[:] = ce.eq_out[:]
                    ce.assert_equality(flo11, is_method=False)
                    ce.eq_in[:] = ce.eq_in_bkp[:]
                    ce.eq_out[:] = ce.eq_in_bkp[:]
                    ce.assert_equality(fnonlo11, is_method=False)

                    ce = CompareEqs(db11_scr)
                    ce.assert_equality(fnonlo1, is_method=False,
                                       inversely=True)

                for n_set in range(2, op_set.n_args + 1):
                    # Act on []
                    db = (
                        (Eq([PJUXT, sb_set_scr, p], [1, n_set]),
                         Eq([PJUXT, sb_set_scr, p], [1, n_set])),
                        (Eq([PJUXT, sb_set_scr, p], [1, n_set, 1]),
                         Eq([PJUXT, sb_set_scr, p], [1, n_set, 1])),
                        (Eq([PJUXT, sb_scr_set, p], [1, 1, n_set]),
                         Eq([PJUXT, sb_scr_set, p], [1, 1, n_set])),
                        (Eq([PJUXT, sb_scr_set, p], [1, 1, n_set, 1]),
                         Eq([PJUXT, sb_scr_set, p], [1, 1, n_set, 1])),
                    )
                    ce = CompareEqs(db)
                    ce.assert_equality(flo, is_method=False)
                    ce.assert_equality(fnonlo, is_method=False,
                                       inversely=True)
                    ce.eq_in_bkp = ce.eq_in[:]
                    ce.eq_in[:] = ce.eq_out[:]
                    ce.assert_equality(flo, is_method=False)
                    ce.eq_in[:] = ce.eq_in_bkp[:]
                    ce.eq_out[:] = ce.eq_in_bkp[:]
                    ce.assert_equality(fnonlo, is_method=False)

                    # Act on [1]
                    db1 = (
                        (Eq([PJUXT, sb_set_scr, p], [1, n_set]),
                         Eq([PJUXT, sb_e_set,   p], [1, n_set])),
                        (Eq([PJUXT, sb_set_scr, p], [1, n_set, 1]),
                         Eq([PJUXT, sb_e_set,   p], [1, n_set, 1])),
                        # Unintended use since the base would be modified
                        (Eq([PJUXT, sb_scr_set, p], [1, 1, n_set]),
                         Eq([PJUXT, sb_e_scr,   p], [1, 1, n_set])),
                        (Eq([PJUXT, sb_scr_set, p], [1, 1, n_set, 1]),
                         Eq([PJUXT, sb_e_scr, p], [1, 1, n_set, 1])),
                    )
                    ce = CompareEqs(db1)
                    ce.assert_equality(flo1, is_method=False)
                    ce.assert_equality(fnonlo1, is_method=False,
                                       inversely=True)
                    ce.eq_in_bkp = ce.eq_in[:]
                    ce.eq_in[:] = ce.eq_out[:]
                    ce.assert_equality(flo1, is_method=False)
                    ce.eq_in[:] = ce.eq_in_bkp[:]
                    ce.eq_out[:] = ce.eq_in_bkp[:]
                    ce.assert_equality(fnonlo1, is_method=False)

                    # Act on [1, 1]
                    # This section trusts in updated eqs but not in retvals

                    # Surface
                    k1 = Subeq([PJUXT, ["k11"], ["k12"]])
                    s1 = deepcopy(Subeq([PJUXT, sb_set_scr, p]))
                    sub1 = s1([1, n_set])
                    sub1[:] = k1
                    e_s1 = deepcopy(s1)
                    update_scriptblock([Op("O", "O", 0, "vs")], e_s1, [1, 1])
                    e_sub1 = e_s1(1)
                    e_pos_k1 = e_sub1.index(k1)

                    # Deeper
                    k2 = Subeq([PJUXT, ["k21"], ["k22"]])
                    s2 = deepcopy(Subeq([PJUXT, sb_scr_set, p]))
                    sub2 = s2([1, 1, n_set])
                    sub2[:] = k2
                    e_s2 = deepcopy(s2)
                    update_scriptblock([Op("O", "O", 0, "vs")], e_s2, [1, 1])
                    e_sub2 = e_s2(1)
                    e_pos_k2 = e_sub2.index(k2)

                    db11_set = (
                        (Eq(s1, [1, n_set]),
                         Eq(e_s1, [1, e_pos_k1])),
                        (Eq(s1, [1, n_set, 1]),
                         Eq(e_s1, [1, e_pos_k1, 1])),
                    )
                    db11_scr = (
                        (Eq(s2, [1, 1, n_set]),
                         Eq(e_s2, [1, e_pos_k2])),
                        (Eq(s2, [1, 1, n_set, 1]),
                         Eq(e_s2, [1, e_pos_k2, 1])),
                    )
                    ce = CompareEqs(db11_scr + db11_set)
                    ce.assert_equality(flo11, is_method=False)
                    # Inverse is done below
                    ce.eq_in_bkp = ce.eq_in[:]
                    ce.eq_in[:] = ce.eq_out[:]
                    ce.assert_equality(flo11, is_method=False)
                    ce.eq_in[:] = ce.eq_in_bkp[:]
                    ce.eq_out[:] = ce.eq_in_bkp[:]
                    ce.assert_equality(fnonlo11, is_method=False)

                    ce = CompareEqs(db11_scr)
                    ce.assert_equality(fnonlo1, is_method=False,
                                       inversely=True)

    def test_insert_script(self):
        op0vs = [Op("O", "O", 0, "vs")]
        scr_dict = {
            "lsub": (-1, False), "under": (0, False), "sub": (1, False),
            "lsup": (-1, True), "over": (0, True), "sup": (1, True),
        }

        def fnone(eq):
            retval = insert_script(eq.idx, eq, *scr_dict[op_cn])
            self.assertIsInstance(retval, Idx)
            self.assertEqual(eq(retval), [PVOID])
            eq._set(["x"], retval)
            eq.idx[:] = retval
            return eq

        def fy(eq):
            retval = insert_script(eq.idx, eq, *scr_dict[op_cn], ["y"])
            self.assertIsInstance(retval, Idx)
            self.assertEqual(eq(retval), ["y"])
            eq._set(["x"], retval)
            eq.idx[:] = retval
            return eq

        for op_cn in scr_dict:
            # Test insertions from no base
            op = eval(op_cn.upper())
            loop = test_equivalent_op(op)[0]
            s = ["a"]
            fins = [op, ["a"], ["x"]]
            los = op0vs
            finlos = [loop, op0vs, ["x"]]

            db = (
                (Eq(s, []), Eq(fins, [2])),
                (Eq(los, []), Eq(finlos, [2])),
                (Eq([Op("O", "O", 1), s], [1]),
                    Eq([Op("O", "O", 1), fins], [1, 2])),
                (Eq([Op("O", "O", 1), los], [1]),
                    Eq([Op("O", "O", 1), finlos], [1, 2])),
                (Eq([PJUXT, s, ["b"]], [1]),
                    Eq([PJUXT, fins, ["b"]], [1, 2])),
                (Eq([PJUXT, s, ["b"]], [1]),
                    Eq([PJUXT, fins, ["b"]], [1, 2])),
                (Eq([PJUXT, ["b"], s], [2]),
                    Eq([PJUXT, ["b"], fins], [2, 2])),
                (Eq([PJUXT, ["b"], los], [2]),
                    Eq([PJUXT, ["b"], finlos], [2, 2])),
            )
            ce = CompareEqs(db)
            ce.assert_equality(fnone, is_method=False)
            ce.assert_equality(fy, is_method=False)

            for finop in (o for o in ALL_SCRIPT_OPS_LIST
                          if o.n_args > 2 and test_is_scriptop_with(op_cn, o)):
                # Test already scripts-blocks when new script is really
                # inserted
                op = test_downgraded_scriptop_given_codename(finop, op_cn)
                new_script_ord = test_which_ord_is_script(finop, op_cn)
                check = test_downgraded_scriptop_given_n(finop, new_script_ord)
                # Just a consistency check due to the lack of auxiliary tests
                self.assertEqual(op, check)
                if op.type_ == "loscript":
                    s = [op, op0vs] + [["x"]] * (op.n_args - 1)
                    fins = [finop, op0vs] + [["x"]] * (finop.n_args - 1)
                else:
                    s = [op, ["base"]] + [["x"]] * (op.n_args - 1)
                    fins = [finop, ["base"]] + [["x"]] * (finop.n_args - 1)

                db = (
                    (Eq(s, [1]), Eq(fins, [new_script_ord + 1])),
                    (Eq([Op("O", "O", 1), s], [1, 1]),
                        Eq([Op("O", "O", 1), fins], [1, new_script_ord + 1])),
                    (Eq([PJUXT, s, ["a"]], [1, 1]),
                        Eq([PJUXT, fins, ["a"]], [1, new_script_ord + 1])),
                    (Eq([PJUXT, ["a"], s], [2, 1]),
                        Eq([PJUXT, ["a"], fins], [2, new_script_ord + 1])),
                )

                ce = CompareEqs(db)
                ce.assert_equality(fnone, is_method=False)
                ce.assert_equality(fy, is_method=False)

                # Test bases which already have requested script
                # (not exhaustive)
                for i in (i for i in range(1, finop.n_args)
                          if i != new_script_ord):
                    op = test_downgraded_scriptop_given_n(finop, i)
                    prev_script_ord = test_which_ord_is_script(op, op_cn)
                    if op.type_ == "loscript":
                        s = [op, op0vs] + [["x"]] * (op.n_args - 1)
                    else:
                        s = [op, ["base"]] + [["x"]] * (op.n_args - 1)
                    db = (
                        (Eq(s, [1]), Eq(s, [1])),
                        (Eq([Op("O", "O", 1), s], [1, 1]),
                            Eq([Op("O", "O", 1), s], [1, 1])),
                        (Eq([PJUXT, s, ["a"]], [1, 1]),
                            Eq([PJUXT, s, ["a"]], [1, 1])),
                        (Eq([PJUXT, ["a"], s], [2, 1]),
                            Eq([PJUXT, ["a"], s], [2, 1])),
                    )

                ce = CompareEqs(db)

                def f(eq):
                    retval = insert_script(eq.idx, eq, *scr_dict[op_cn])
                    self.assertEqual(retval, prev_script_ord + 1)
                    retval = insert_script(eq.idx, eq, *scr_dict[op_cn], ["y"])
                    self.assertEqual(retval, prev_script_ord + 1)
                    return eq
                ce.assert_equality(f, is_method=False)

        # Tests bases which requested script is not compatible with current lop
        for op in SCRIPT_OPS_LIST:
            for op_cn in ("under", "over"):
                def fnone(eq):
                    retval = insert_script(eq.idx, eq, *scr_dict[op_cn])
                    self.assertIsInstance(retval, Idx)
                    self.assertEqual(eq(retval), [PVOID])
                    eq._set(["x"], retval)
                    eq.idx[:] = retval
                    return eq

                def fy(eq):
                    retval = insert_script(eq.idx, eq, *scr_dict[op_cn], ["y"])
                    self.assertIsInstance(retval, Idx)
                    self.assertEqual(eq(retval), ["y"])
                    eq._set(["x"], retval)
                    eq.idx[:] = retval
                    return eq

                new_op = eval(op_cn.upper())
                s = [op, ["a"]] + [["z"]] * (op.n_args - 1)
                fins = [op, [new_op, ["a"], ["x"]]] + [["z"]] * (op.n_args - 1)
                db = (
                    (Eq(s, [1]), Eq(fins, [1, 2])),
                    (Eq([Op("O", "O", 1), s], [1, 1]),
                        Eq([Op("O", "O", 1), fins], [1, 1, 2])),
                    (Eq([PJUXT, s, ["a"]], [1, 1]),
                        Eq([PJUXT, fins, ["a"]], [1, 1, 2])),
                    (Eq([PJUXT, ["a"], s], [2, 1]),
                        Eq([PJUXT, ["a"], fins], [2, 1, 2])),

                )
                ce = CompareEqs(db)
                ce.assert_equality(fnone, is_method=False)
                ce.assert_equality(fy, is_method=False)

        for op in SETSCRIPT_OPS_LIST:
            for op_cn in ("lsub", "sub", "lsup", "sup"):
                def fnone(eq):
                    retval = insert_script(eq.idx, eq, *scr_dict[op_cn])
                    self.assertIsInstance(retval, Idx)
                    self.assertEqual(eq(retval), [PVOID])
                    eq._set(["x"], retval)
                    eq.idx[:] = retval
                    return eq

                def fy(eq):
                    retval = insert_script(eq.idx, eq, *scr_dict[op_cn], ["y"])
                    self.assertIsInstance(retval, Idx)
                    self.assertEqual(eq(retval), ["y"])
                    eq._set(["x"], retval)
                    eq.idx[:] = retval
                    return eq

                new_op = eval(op_cn.upper())
                s = [op, ["a"]] + [["z"]] * (op.n_args - 1)
                fins = [op, [new_op, ["a"], ["x"]]] + [["z"]] * (op.n_args - 1)
                db = (
                    (Eq(s, [1]), Eq(fins, [1, 2])),
                    (Eq([Op("O", "O", 1), s], [1, 1]),
                        Eq([Op("O", "O", 1), fins], [1, 1, 2])),
                    (Eq([PJUXT, s, ["a"]], [1, 1]),
                        Eq([PJUXT, fins, ["a"]], [1, 1, 2])),
                    (Eq([PJUXT, ["a"], s], [2, 1]),
                        Eq([PJUXT, ["a"], fins], [2, 1, 2])),

                )
                ce = CompareEqs(db)
                ce.assert_equality(fnone, is_method=False)
                ce.assert_equality(fy, is_method=False)

    def test_remove_script_2args(self):
        for op in (op for op in ALL_SCRIPT_OPS_LIST if op.n_args == 2):
            db = (
                (Eq([op] + [["x"]] * op.n_args, [2]), Eq(["x"])),
                (Eq([Op("O", "O", 1), [op] + [["x"]] * op.n_args], [1, 2]),
                    Eq([Op("O", "O", 1), ["x"]], [1])),
                (Eq([PJUXT, [op] + [["x"]] * op.n_args, ["y"]], [1, 2]),
                    Eq([PJUXT, ["x"], ["y"]], [1])),
                (Eq([PJUXT, ["y"], [op] + [["x"]] * op.n_args], [2, 2]),
                    Eq([PJUXT, ["y"], ["x"]], [2])),
            )

        def fsb(eq):
            # Point with refindex to the supeq, which must always exist
            retval = remove_script(eq.idx, eq, eq.idx[:-1])
            eq.idx[:] = retval
            return eq

        def fbase(eq):
            # Point with refindex to the base, which must always exist
            retval = remove_script(eq.idx, eq, eq.idx[:-1] + [1])
            eq.idx[:] = retval
            return eq
        def frem(eq):
            # Refindex pointing to removed script
            retval = remove_script(eq.idx, eq, eq.idx[:-1] + [2])
            # Do check here and do not care about adjusting final idx
            self.assertEqual(retval, -1)
            return eq
        ce = CompareEqs(db)
        ce.assert_equality(fsb, is_method=False)
        ce.assert_equality(fbase, is_method=False)

        for op in (op for op in ALL_SCRIPT_OPS_LIST if op.n_args == 2):
            db = (
                (Eq([op] + [["x"]] * op.n_args, [2]), Eq(["x"])),
                (Eq([Op("O", "O", 1), [op] + [["x"]] * op.n_args], [1, 2]),
                    Eq([Op("O", "O", 1), ["x"]])),
                (Eq([PJUXT, [op] + [["x"]] * op.n_args, ["y"]], [1, 2]),
                    Eq([PJUXT, ["x"], ["y"]])),
                (Eq([PJUXT, ["y"], [op] + [["x"]] * op.n_args], [2, 2]),
                    Eq([PJUXT, ["y"], ["x"]])),
            )
            ce = CompareEqs(db)
            ce.assert_equality(frem, is_method=False, exclude_idx=True)

    def test_remove_script_3argsormore(self):
        for op in (op for op in ALL_SCRIPT_OPS_LIST if op.n_args > 2):
            end = op.n_args + 1
            args = [[str(n)] for n in range(1, end)]
            for arg in range(2, end):
                finop = test_downgraded_scriptop_given_n(op, arg - 1)
                finargs = args[:]
                del finargs[arg - 1]
                for oarg in (a for a in range(2, end) if a != arg):
                    # README!
                    # It will act on [..., arg] and refindex is [..., oarg]
                    # Return value is assigned to eq.idx
                    def foarg(eq):
                        retval = remove_script(eq.idx, eq,
                                               eq.idx[:-1] + [oarg])
                        eq.idx[:] = retval
                        return eq

                    def farg(eq):
                        # Refindex pointing to removed script
                        retval = remove_script(eq.idx, eq, eq.idx[:-1] + [arg])
                        # Do check here and do not care about adjusting
                        # final idx
                        self.assertEqual(retval, -1)
                        return eq
                    finoarg = oarg if oarg < arg else oarg - 1
                    db = (
                        (Eq([op] + args, [arg]),
                            Eq([finop] + finargs, [finoarg])),
                        (Eq([Op("O", "O", 1), [op] + args], [1, arg]),
                            Eq([Op("O", "O", 1), [finop] + finargs],
                                [1, finoarg])),
                        (Eq([PJUXT, [op] + args, ["y"]], [1, arg]),
                            Eq([PJUXT, [finop] + finargs, ["y"]],
                                [1, finoarg])),
                        (Eq([PJUXT, ["y"], [op] + args], [2, arg]),
                            Eq([PJUXT, ["y"], [finop] + finargs],
                                [2, finoarg])),
                    )
                    ce = CompareEqs(db)
                    ce.assert_equality(foarg, is_method=False)
                    ce.assert_equality(farg, is_method=False, exclude_idx=True)

    def test_remove_script_composed(self):
        def fbase(eq):
            retval = remove_script(eq.idx, eq, eq.idx[:-1] + [1])
            eq.idx = retval
            return eq

        nonlo_list = SETSCRIPT_OPS_LIST + SCRIPT_OPS_LIST
        for op_in in (o for o in nonlo_list if o.n_args == 2):
            for op in nonlo_list:
                db = (
                    (Eq([op, [op_in, ["x"], ["x"]]]
                        + [["y"]] * (op.n_args -1), [1, 2]),
                        Eq([op, ["x"]] + [["y"]] * (op.n_args - 1), [1])),
                )

                ce = CompareEqs(db)
                ce.assert_equality(fbase, is_method=False)

        op0vs = Op("O", "O", 0, "vs")
        for loop_in in (o for o in LOSCRIPT_OPS_LIST if o.n_args == 2):
            for op in nonlo_list:
                finloop = test_equivalent_op(op)[0]

                def frem(eq):
                    retval = remove_script(eq.idx, eq, eq.idx[:-1] + [2])
                    self.assertEqual(retval, -1)
                    return eq
                db = (
                    (Eq([op, [loop_in, [op0vs], ["a"]]]
                        + [["y"]] * (op.n_args - 1),
                            [1, 2]),
                        Eq([finloop, [op0vs]]
                           + [["y"]] * (op.n_args - 1), [1])),
                )

                ce = CompareEqs(db)
                ce.assert_equality(fbase, is_method=False)
                ce.assert_equality(frem, is_method=False, exclude_idx=True)
                for arg in range(1, op.n_args + 1):
                    def farg(eq):
                        retval = remove_script(eq.idx, eq, eq.idx[:-2] + [arg])
                        self.assertEqual(retval, eq.idx[:-2] + [arg])
                        return eq
                    ce.assert_equality(farg, is_method=False, exclude_idx=True)

    def test_remove_script_extrefindices(self):
        for op in ALL_SCRIPT_OPS_LIST:
            for i in range(2, op.n_args + 1):
                if op.type_ == "loscript":
                    op0vs = [Op("O", "O", 0, "vs")]
                    if op.n_args == 2:
                        s = [op, op0vs[:], ["x"]]
                        fs = op0vs[:]
                    else:
                        finop = test_downgraded_scriptop_given_n(op, i - 1)
                        s = [op, op0vs[:]] + [["x"]] * (op.n_args - 1)
                        fs = [finop, op0vs[:]] + [["x"]] * (finop.n_args - 1)
                else:
                    if op.n_args == 2:
                        s = [op, ["base"], ["x"]]
                        fs = ["base"]
                    else:
                        finop = test_downgraded_scriptop_given_n(op, i - 1)
                        s = [op, ["base"]] + [["x"]] * (op.n_args - 1)
                        fs = [finop, ["base"]] + [["x"]] * (finop.n_args - 1)
                db = (
                    (Eq([PJUXT, s, ["b"]], [1, i]),
                        Eq([PJUXT, fs,  ["b"]])),
                )

                def f2(eq):
                    self.assertEqual(remove_script(eq.idx, eq, [2]), [2])
                    return eq

                ce = CompareEqs(db)
                ce.assert_equality(f2, is_method=False, exclude_idx=True)

        nonlo_list = SETSCRIPT_OPS_LIST + SCRIPT_OPS_LIST
        for loop_in in (o for o in LOSCRIPT_OPS_LIST if o.n_args == 2):
            for op in nonlo_list:
                finop = test_equivalent_op(op)[0]

                def f2(eq):
                    self.assertEqual(remove_script(eq.idx, eq, [2]), [2])
                    return eq

                op0vs = Op("O", "O", 0, "vs")
                db = (
                    (Eq([op, [loop_in, [op0vs], ["a"]]]
                        + [["y"]] * (op.n_args - 1), [1, 2]),
                        Eq([finop, [op0vs]]
                           + [["y"]] * (finop.n_args - 1))),
                )

                ce = CompareEqs(db)
                ce.assert_equality(f2, is_method=False, exclude_idx=True)

if __name__ == '__main__':
    unittest.main()
