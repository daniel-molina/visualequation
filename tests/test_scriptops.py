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
            nonlo_pair = equivalent_op(lo_op)
            self.assertEqual(equivalent_op(nonlo_pair[0], nonlo_pair[1]),
                             (lo_op, None))
            if nonlo_pair[1] is not None:
                self.assertEqual(equivalent_op(nonlo_pair[1], nonlo_pair[0]),
                                 (lo_op, None))
            ops[nonlo_pair] = lo_op
        self.assertEqual(len(ops), 63)

        for t in (pair[1].type_ for pair in ops if pair[1] is not None):
            # External \*script op after transformation, if any, must be script
            # by convention
            self.assertEqual(t, "script")

    def test_update_scriptblock(self):
        def f_lo(eq):
            eq.idx = update_scriptblock([Op("O", "O", 0, "vs")], eq)
            return eq

        def f_nonlo(eq):
            eq.idx = update_scriptblock(["base"], eq)
            return eq

        n_single_ops = 0
        for op in SETSCRIPT_OPS_LIST + SCRIPT_OPS_LIST:
            n_single_ops += 1

            new_op = equivalent_op(op)[0]
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
                e_op = equivalent_op(op1, op2)[0]
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
            e_op = equivalent_op(op)[0]

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

                e_op = equivalent_op(op_set, op_scr)[0]
                e_op_scr = equivalent_op(op_scr)[0]
                e_op_set = equivalent_op(op_set)[0]
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


if __name__ == '__main__':
    unittest.main()
