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


def equiv_loop(op1: ScriptOp, op2: Optional[ScriptOp] = None):
    """Return an FULL ScriptOp with exactly the same ScriptPos than input
    combined."""
    if op2 is None:
        return ScriptOp(True, *op1.valid_scripts_keys(True))
    return ScriptOp(True, *op1.valid_scripts_keys(True),
                    *op2.valid_scripts_keys(True))


class ScriptOpsTests(unittest.TestCase):
    def test_update_scriptblock(self):
        def f(eq):
            retval = update_scriptblock(eq(eq.idx), eq, eq.idx, eq.idx)
            eq.idx = retval
            return eq

        db = (
            (Eq(["a"]), Eq(["a"])),
            (Eq([PJuxt(), ["d"], ["f"]]), Eq([PJuxt(), ["d"], ["f"]])),
            (Eq([PJuxt(), ["d"], ["f"]], [1]),
                Eq([PJuxt(), ["d"], ["f"]], [1])),
            (Eq([PJuxt(), ["d"], ["f"]], [2]),
                Eq([PJuxt(), ["d"], ["f"]], [2])),
        )
        ce = CompareEqs(db)
        ce.assert_equality(f, is_method=False)

        def f_lo(eq):
            eq.idx = update_scriptblock([PS_LO], eq)
            return eq

        def f_nonlo(eq):
            eq.idx = update_scriptblock(["base"], eq)
            return eq

        n_single_ops = 0
        for op in VERT_SCR_OPS_LIST + CORN_SCR_OPS_LIST:
            n_single_ops += 1

            new_op = ScriptOp(True, *op.valid_scripts_keys(True))
            db = (
                (Eq(["a"]), Eq(["a"], [])),
                (Eq([op] + [["x"]] * op._n_args),
                    Eq([new_op] + [["x"]] * new_op._n_args)),
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
            eq.idx = update_scriptblock([PS_LO], eq, [1])
            return eq

        def f_nonlo1(eq):
            eq.idx = update_scriptblock(["base"], eq, [1])
            return eq

        ce = CompareEqs()
        ce_reversed = CompareEqs()
        n_combined_ops = 0
        for op1 in VERT_SCR_OPS_LIST:
            for op2 in CORN_SCR_OPS_LIST:
                n_combined_ops += 1
                block1 = [op2] + [["x"]] * op2._n_args
                block_scr_in = [op1] + [block1] + [["x"]] * (op1._n_args - 1)
                block2 = [op1] + [["x"]] * op1._n_args
                block_scr_out = [op2] + [block2] + [["x"]] * (op2._n_args - 1)
                e_op = equiv_loop(op1, op2)
                result = [e_op] + [["x"]]*e_op._n_args
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

        flo = f_creator([PS_LO], [])
        flo1 = f_creator([PS_LO], [1])
        fnonlo = f_creator(["z"], [])
        fnonlo1 = f_creator(["z"], [1])

        p = [PJuxt(), ["a"], ["b"]]
        for op in VERT_SCR_OPS_LIST + CORN_SCR_OPS_LIST:
            e_op = ScriptOp(True, *op.valid_scripts_keys(True))

            db = (
                (Eq([PJuxt(op._n_args)] + [["x"]] * op._n_args, []),
                 Eq([PJuxt(op._n_args)] + [["x"]] * op._n_args, [])),
                (Eq([op] + [["x"]] * op._n_args, []),
                 Eq([e_op] + [["x"]] * op._n_args, [])),
            )
            ce = CompareEqs(db)
            ce.assert_equality(flo, is_method=False)
            ce.assert_equality(fnonlo, is_method=False, inversely=True)

            db = (
                (Eq([PJuxt()] + [["x"]] * op._n_args, []),
                 Eq([PJuxt()] + [["x"]] * op._n_args, [])),
                (Eq([PJuxt(), [op] + [["x"]] * op._n_args, ["y"]], []),
                 Eq([PJuxt(), [e_op] + [["x"]] * op._n_args, ["y"]], [])),
                (Eq([PJuxt(), [op] + [["x"]] * op._n_args, ["y"]], [1]),
                 Eq([PJuxt(), [e_op] + [["x"]] * op._n_args, ["y"]], [1])),
                (Eq([PJuxt(), [op] + [["x"]] * op._n_args, ["y"]], [2]),
                 Eq([PJuxt(), [e_op] + [["x"]] * op._n_args, ["y"]], [2])),
            )
            ce = CompareEqs(db)
            ce.assert_equality(flo1, is_method=False)
            ce.assert_equality(fnonlo1, is_method=False, inversely=True)

            for n in range(1, op._n_args + 1):
                db = (
                    (Eq([PJuxt()] + [["x"]] * op._n_args, [n]),
                     Eq([PJuxt()] + [["x"]] * op._n_args, [n])),

                    (Eq([op] + [["x"]] * op._n_args, [n]),
                     Eq([e_op] + [["x"]] * op._n_args, [n])),

                    (Eq([op] + [p] + [["x"]] * (op._n_args - 1), [n]),
                     Eq([e_op] + [p] + [["x"]] * (op._n_args - 1), [n])),

                    (Eq([op] + [["x"]] * op._n_args, [n]),
                     Eq([e_op] + [["x"]] * op._n_args, [n])),
                    (Eq([op] + [p] * op._n_args, [n, 1]),
                     Eq([e_op] + [p] * op._n_args, [n, 1])),
                    (Eq([op] + [p] * op._n_args, [n, 2]),
                     Eq([e_op] + [p] * op._n_args, [n, 2])),
                )
                ce = CompareEqs(db)
                ce.assert_equality(flo, is_method=False)
                ce.assert_equality(fnonlo, is_method=False, inversely=True)

                db = (
                    (Eq([PJuxt()] + [["x"]] * op._n_args, [n]),
                     Eq([PJuxt()] + [["x"]] * op._n_args, [n])),

                    (Eq([PJuxt(), [op] + [p] * op._n_args, ["y"]], [1, n]),
                     Eq([PJuxt(), [e_op] + [p] * op._n_args, ["y"]], [1, n])),
                    (Eq([PJuxt(), [op] + [p] * op._n_args, ["y"]], [1, n, 1]),
                     Eq([PJuxt(), [e_op] + [p] * op._n_args, ["y"]], [1, n, 1])),
                    (Eq([PJuxt(), [op] + [p] * op._n_args, ["y"]], [1, n, 2]),
                     Eq([PJuxt(), [e_op] + [p] * op._n_args, ["y"]], [1, n, 2])),
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

        flo = f_creator([PS_LO], [])
        flo1 = f_creator([PS_LO], [1])
        flo11 = f_creator([PS_LO], [1, 1])
        fnonlo = f_creator(["z"], [])
        fnonlo1 = f_creator(["z"], [1])
        fnonlo11 = f_creator(["z"], [1, 1])

        p = [PJuxt(), ["a"], ["b"]]
        for op_vert in VERT_SCR_OPS_LIST:
            for op_corn in CORN_SCR_OPS_LIST:
                sb_c_v = [op_corn] + [[op_vert] + [p] * op_vert._n_args] \
                         + [p] * (op_corn._n_args - 1)
                sb_v_c = [op_vert] + [[op_corn] + [p] * op_corn._n_args] \
                         + [p] * (op_vert._n_args - 1)

                e_op = ScriptOp(True, *op_vert.valid_scripts_keys(True),
                                *op_corn.valid_scripts_keys(True))
                e_op_vert = ScriptOp(True, *op_vert.valid_scripts_keys(True))
                e_op_corn = ScriptOp(True, *op_corn.valid_scripts_keys(True))

                sb_e = [e_op] + [p] * e_op._n_args
                sb_e_scr = [e_op_corn] + [[op_vert] + [p] * op_vert._n_args] \
                           + [p] * (op_corn._n_args - 1)
                sb_e_set = [e_op_vert] + [[op_corn] + [p] * op_corn._n_args] \
                           + [p] * (op_vert._n_args - 1)
                # Act on []
                db_scr = (
                    (Eq([PJuxt(), sb_c_v, p], []),
                     Eq([PJuxt(), sb_c_v, p], [])),
                    (Eq([PJuxt(), sb_c_v, p], [1]),
                     Eq([PJuxt(), sb_c_v, p], [1])),
                    (Eq([PJuxt(), sb_c_v, p], [1, 1]),
                     Eq([PJuxt(), sb_c_v, p], [1, 1])),
                    (Eq([PJuxt(), sb_c_v, p], [2]),
                     Eq([PJuxt(), sb_c_v, p], [2])),
                )
                db_set = (
                    (Eq([PJuxt(), sb_v_c, p], []),
                     Eq([PJuxt(), sb_v_c, p], [])),
                    (Eq([PJuxt(), sb_v_c, p], [1]),
                     Eq([PJuxt(), sb_v_c, p], [1])),
                    (Eq([PJuxt(), sb_v_c, p], [1, 1]),
                     Eq([PJuxt(), sb_v_c, p], [1, 1])),
                    (Eq([PJuxt(), sb_v_c, p], [2]),
                     Eq([PJuxt(), sb_v_c, p], [2])),
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
                    (Eq([PJuxt(), sb_c_v, p], []),
                     Eq([PJuxt(), sb_e_scr,   p], [])),
                    (Eq([PJuxt(), sb_c_v, p], [1]),
                     Eq([PJuxt(), sb_e_scr,   p], [1])),
                    (Eq([PJuxt(), sb_c_v, p], [1, 1]),
                     Eq([PJuxt(), sb_e_scr,   p], [1, 1])),
                    (Eq([PJuxt(), sb_c_v, p], [2]),
                     Eq([PJuxt(), sb_e_scr,   p], [2])),
                )
                db1_set = (
                    (Eq([PJuxt(), sb_v_c, p], []),
                     Eq([PJuxt(), sb_e_set,   p], [])),
                    (Eq([PJuxt(), sb_v_c, p], [1]),
                     Eq([PJuxt(), sb_e_set,   p], [1])),
                    (Eq([PJuxt(), sb_v_c, p], [1, 1]),
                     Eq([PJuxt(), sb_e_set,   p], [1, 1])),
                    (Eq([PJuxt(), sb_v_c, p], [2]),
                     Eq([PJuxt(), sb_e_set,   p], [2])),
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
                    (Eq([PJuxt(), sb_c_v, p], []),
                     Eq([PJuxt(), sb_e,       p], [])),
                    (Eq([PJuxt(), sb_c_v, p], [1]),
                     Eq([PJuxt(), sb_e,       p], [1])),
                    (Eq([PJuxt(), sb_c_v, p], [2]),
                     Eq([PJuxt(), sb_e,       p], [2])),
                )
                db11_set = (
                    (Eq([PJuxt(), sb_v_c, p], []),
                     Eq([PJuxt(), sb_e,       p], [])),
                    (Eq([PJuxt(), sb_v_c, p], [1]),
                     Eq([PJuxt(), sb_e,       p], [1])),
                    (Eq([PJuxt(), sb_v_c, p], [2]),
                     Eq([PJuxt(), sb_e,       p], [2])),
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
                    (Eq([PJuxt(), sb_c_v, p], [1, 1]),
                     Eq([PJuxt(), sb_e,       p], [1])),
                    (Eq([PJuxt(), sb_v_c, p], [1, 1]),
                     Eq([PJuxt(), sb_e,       p], [1])),
                )
                ce = CompareEqs(db11_special)
                ce.assert_equality(flo11, is_method=False)
                ce.eq_out[:] = ce.eq_in[:]
                ce.assert_equality(fnonlo11, is_method=False)

                db11_special_bis = (
                    (Eq([PJuxt(), sb_e, p], [1, 1]),
                     Eq([PJuxt(), sb_e, p], [1, 1])),
                )
                ce = CompareEqs(db11_special_bis)
                ce.assert_equality(flo11, is_method=False)

                for n_scr in range(2, op_corn._n_args + 1):
                    # Act on []
                    db = (
                        (Eq([PJuxt(), sb_c_v, p], [1, n_scr]),
                         Eq([PJuxt(), sb_c_v, p], [1, n_scr])),
                        (Eq([PJuxt(), sb_c_v, p], [1, n_scr, 1]),
                         Eq([PJuxt(), sb_c_v, p], [1, n_scr, 1])),
                        (Eq([PJuxt(), sb_c_v, p], [1, n_scr, 2]),
                         Eq([PJuxt(), sb_c_v, p], [1, n_scr, 2])),
                        (Eq([PJuxt(), sb_v_c, p], [1, 1, n_scr]),
                         Eq([PJuxt(), sb_v_c, p], [1, 1, n_scr])),
                        (Eq([PJuxt(), sb_v_c, p], [1, 1, n_scr, 1]),
                         Eq([PJuxt(), sb_v_c, p], [1, 1, n_scr, 1])),
                        (Eq([PJuxt(), sb_v_c, p], [1, 1, n_scr, 2]),
                         Eq([PJuxt(), sb_v_c, p], [1, 1, n_scr, 2])),
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
                        (Eq([PJuxt(), sb_c_v, p], [1, n_scr]),
                         Eq([PJuxt(), sb_e_scr,   p], [1, n_scr])),
                        (Eq([PJuxt(), sb_c_v, p], [1, n_scr, 1]),
                         Eq([PJuxt(), sb_e_scr,   p], [1, n_scr, 1])),
                        (Eq([PJuxt(), sb_c_v, p], [1, n_scr, 2]),
                         Eq([PJuxt(), sb_e_scr,   p], [1, n_scr, 2])),
                        # Unintended use since the base would be modified
                        (Eq([PJuxt(), sb_v_c, p], [1, 1, n_scr]),
                         Eq([PJuxt(), sb_e_set,   p], [1, 1, n_scr])),
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
                    k1 = Subeq([PJuxt(), ["k11"], ["k12"]])
                    s1 = deepcopy(Subeq([PJuxt(), sb_c_v, p]))
                    sub1 = s1([1, n_scr])
                    sub1[:] = k1
                    e_s1 = deepcopy(s1)
                    update_scriptblock([PS_LO], e_s1, [1, 1])
                    e_sub1 = e_s1(1)
                    e_pos_k1 = e_sub1.index(k1)

                    # Deeper
                    k2 = Subeq([PJuxt(), ["k21"], ["k22"]])
                    s2 = deepcopy(Subeq([PJuxt(), sb_v_c, p]))
                    sub2 = s2([1, 1, n_scr])
                    sub2[:] = k2
                    e_s2 = deepcopy(s2)
                    update_scriptblock([PS_LO], e_s2, [1, 1])
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

                for n_set in range(2, op_vert._n_args + 1):
                    # Act on []
                    db = (
                        (Eq([PJuxt(), sb_v_c, p], [1, n_set]),
                         Eq([PJuxt(), sb_v_c, p], [1, n_set])),
                        (Eq([PJuxt(), sb_v_c, p], [1, n_set, 1]),
                         Eq([PJuxt(), sb_v_c, p], [1, n_set, 1])),
                        (Eq([PJuxt(), sb_c_v, p], [1, 1, n_set]),
                         Eq([PJuxt(), sb_c_v, p], [1, 1, n_set])),
                        (Eq([PJuxt(), sb_c_v, p], [1, 1, n_set, 1]),
                         Eq([PJuxt(), sb_c_v, p], [1, 1, n_set, 1])),
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
                        (Eq([PJuxt(), sb_v_c, p], [1, n_set]),
                         Eq([PJuxt(), sb_e_set,   p], [1, n_set])),
                        (Eq([PJuxt(), sb_v_c, p], [1, n_set, 1]),
                         Eq([PJuxt(), sb_e_set,   p], [1, n_set, 1])),
                        # Unintended use since the base would be modified
                        (Eq([PJuxt(), sb_c_v, p], [1, 1, n_set]),
                         Eq([PJuxt(), sb_e_scr,   p], [1, 1, n_set])),
                        (Eq([PJuxt(), sb_c_v, p], [1, 1, n_set, 1]),
                         Eq([PJuxt(), sb_e_scr, p], [1, 1, n_set, 1])),
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
                    k1 = Subeq([PJuxt(), ["k11"], ["k12"]])
                    s1 = deepcopy(Subeq([PJuxt(), sb_v_c, p]))
                    sub1 = s1([1, n_set])
                    sub1[:] = k1
                    e_s1 = deepcopy(s1)
                    update_scriptblock([PS_LO], e_s1, [1, 1])
                    e_sub1 = e_s1(1)
                    e_pos_k1 = e_sub1.index(k1)

                    # Deeper
                    k2 = Subeq([PJuxt(), ["k21"], ["k22"]])
                    s2 = deepcopy(Subeq([PJuxt(), sb_c_v, p]))
                    sub2 = s2([1, 1, n_set])
                    sub2[:] = k2
                    e_s2 = deepcopy(s2)
                    update_scriptblock([PS_LO], e_s2, [1, 1])
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
        def fnone_gtor(spos):
            def fnone(eq):
                retval = insert_script(eq.idx, eq, spos)
                self.assertIsInstance(retval, Idx)
                self.assertEqual(eq(retval), [PVOID])
                eq._set(["x"], retval)
                eq.idx[:] = retval
                return eq

            return fnone

        def fy_gtor(spos):
            def fy(eq):
                retval = insert_script(eq.idx, eq, spos, ["y"])
                self.assertIsInstance(retval, Idx)
                self.assertEqual(eq(retval), ["y"])
                eq._set(["x"], retval)
                eq.idx[:] = retval
                return eq
            return fy

        for spos in ScriptPos:
            # Test insertions from no base
            op = ScriptOp(False, spos)
            loop = ScriptOp(True, spos)
            s = ["a"]
            fins1 = [op, ["a"], ["x"]]
            los = [PS_LO]
            finlos = [loop, los, ["x"]]

            db = (
                (Eq(s, []), Eq(fins1, [2])),
                (Eq(los, []), Eq(finlos, [2])),
                (Eq([Op("O", 1), s], [1]),
                    Eq([Op("O", 1), fins1], [1, 2])),
                (Eq([Op("O", 1), los], [1]),
                    Eq([Op("O", 1), finlos], [1, 2])),
                (Eq([PJuxt(), s, ["b"]], [1]),
                    Eq([PJuxt(), fins1, ["b"]], [1, 2])),
                (Eq([PJuxt(), s, ["b"]], [1]),
                    Eq([PJuxt(), fins1, ["b"]], [1, 2])),
                (Eq([PJuxt(), ["b"], s], [2]),
                    Eq([PJuxt(), ["b"], fins1], [2, 2])),
                (Eq([PJuxt(), ["b"], los], [2]),
                    Eq([PJuxt(), ["b"], finlos], [2, 2])),
            )
            ce = CompareEqs(db)
            ce.assert_equality(fnone_gtor(spos), is_method=False)
            ce.assert_equality(fy_gtor(spos), is_method=False)

            # Test scripts-blocks when a new script is (really) inserted
            for finop in (o for o in SCR_OPS_LIST
                          if o._n_args > 2 and o._scripts[spos]):
                op = ScriptOp(finop.is_lo(),
                              *(k for k in finop.valid_scripts_keys(True)
                               if k is not spos))
                new_script_ord = finop.spos2ord(spos)
                if op.is_lo():
                    s = [op, los] + [["x"]] * (op._n_args - 1)
                    fins1 = [finop, los] + [["x"]] * (finop._n_args - 1)
                else:
                    s = [op, ["base"]] + [["x"]] * (op._n_args - 1)
                    fins1 = [finop, ["base"]] + [["x"]] * (finop._n_args - 1)

                db = (
                    (Eq(s, [1]), Eq(fins1, [new_script_ord])),
                    (Eq([Op("O", 1), s], [1, 1]),
                        Eq([Op("O", 1), fins1], [1, new_script_ord])),
                    (Eq([PJuxt(), s, ["a"]], [1, 1]),
                        Eq([PJuxt(), fins1, ["a"]], [1, new_script_ord])),
                    (Eq([PJuxt(), ["a"], s], [2, 1]),
                        Eq([PJuxt(), ["a"], fins1], [2, new_script_ord])),
                )

                ce = CompareEqs(db)
                ce.assert_equality(fnone_gtor(spos), is_method=False)
                ce.assert_equality(fy_gtor(spos), is_method=False)

            # Test bases which already have requested script
            for op in SCR_OPS_LIST:
                if not op._scripts[spos]:
                    continue
                scr_ord = op.spos2ord(spos)
                if op.is_lo():
                    s = [op, los] + [["x"]] * (op._n_args - 1)
                else:
                    s = [op, ["base"]] + [["x"]] * (op._n_args - 1)
                db = (
                    (Eq(s, [1]), Eq(s, [1])),
                    (Eq([Op("O", 1), s], [1, 1]),
                        Eq([Op("O", 1), s], [1, 1])),
                    (Eq([PJuxt(), s, ["a"]], [1, 1]),
                        Eq([PJuxt(), s, ["a"]], [1, 1])),
                    (Eq([PJuxt(), ["a"], s], [2, 1]),
                        Eq([PJuxt(), ["a"], s], [2, 1])),
                )

            ce = CompareEqs(db)

            def f(eq):
                retval = insert_script(eq.idx, eq, spos)
                self.assertEqual(retval, scr_ord)
                retval = insert_script(eq.idx, eq, spos, ["y"])
                self.assertEqual(retval, scr_ord)
                return eq
            ce.assert_equality(f, is_method=False)

        # Tests bases which requested script is not compatible with current lop
        for op in CORN_SCR_OPS_LIST:
            for spos in VERT_SCR_POS_TUPLE:
                def fnone(eq):
                    retval = insert_script(eq.idx, eq, spos)
                    self.assertIsInstance(retval, Idx)
                    self.assertEqual(eq(retval), [PVOID])
                    eq._set(["x"], retval)
                    eq.idx[:] = retval
                    return eq

                def fy(eq):
                    retval = insert_script(eq.idx, eq, spos, ["y"])
                    self.assertIsInstance(retval, Idx)
                    self.assertEqual(eq(retval), ["y"])
                    eq._set(["x"], retval)
                    eq.idx[:] = retval
                    return eq

                new_op = ScriptOp(False, spos)
                s = [op, ["a"]] + [["z"]] * (op._n_args - 1)
                fins1 = [op, [new_op, ["a"],
                              ["x"]]] + [["z"]] * (op._n_args - 1)
                fins0 = [new_op, [op, ["a"]] + [["z"]] * (op._n_args - 1),
                         ["x"]]
                db = (
                    (Eq(s, [1]), Eq(fins1, [1, 2])),
                    (Eq([Op("O", 1), s], [1, 1]),
                        Eq([Op("O", 1), fins1], [1, 1, 2])),
                    (Eq([PJuxt(), s, ["b"]], [1, 1]),
                        Eq([PJuxt(), fins1, ["b"]], [1, 1, 2])),
                    (Eq([PJuxt(), ["b"], s], [2, 1]),
                        Eq([PJuxt(), ["b"], fins1], [2, 1, 2])),

                    (Eq(s, []), Eq(fins0, [2])),
                    (Eq([Op("O", 1), s], [1]),
                        Eq([Op("O", 1), fins0], [1, 2])),
                    (Eq([PJuxt(), s, ["a"]], [1]),
                        Eq([PJuxt(), fins0, ["a"]], [1, 2])),
                    (Eq([PJuxt(), ["a"], s], [2]),
                        Eq([PJuxt(), ["a"], fins0], [2, 2])),
                )
                ce = CompareEqs(db)
                ce.assert_equality(fnone, is_method=False)
                ce.assert_equality(fy, is_method=False)

        for op in VERT_SCR_OPS_LIST:
            for spos in CORN_SCR_POS_TUPLE:
                def fnone(eq):
                    retval = insert_script(eq.idx, eq, spos)
                    self.assertIsInstance(retval, Idx)
                    self.assertEqual(eq(retval), [PVOID])
                    eq._set(["x"], retval)
                    eq.idx[:] = retval
                    return eq

                def fy(eq):
                    retval = insert_script(eq.idx, eq, spos, ["y"])
                    self.assertIsInstance(retval, Idx)
                    self.assertEqual(eq(retval), ["y"])
                    eq._set(["x"], retval)
                    eq.idx[:] = retval
                    return eq

                new_op = ScriptOp(False, spos)
                s = [op, ["a"]] + [["z"]] * (op._n_args - 1)
                fins1 = [op, [new_op, ["a"],
                              ["x"]]] + [["z"]] * (op._n_args - 1)
                fins0 = [new_op, [op, ["a"]] + [["z"]] * (op._n_args - 1),
                         ["x"]]
                db = (
                    (Eq(s, [1]), Eq(fins1, [1, 2])),
                    (Eq([Op("O", 1), s], [1, 1]),
                        Eq([Op("O", 1), fins1], [1, 1, 2])),
                    (Eq([PJuxt(), s, ["a"]], [1, 1]),
                        Eq([PJuxt(), fins1, ["a"]], [1, 1, 2])),
                    (Eq([PJuxt(), ["a"], s], [2, 1]),
                        Eq([PJuxt(), ["a"], fins1], [2, 1, 2])),

                    (Eq(s, []), Eq(fins0, [2])),
                    (Eq([Op("O", 1), s], [1]),
                        Eq([Op("O", 1), fins0], [1, 2])),
                    (Eq([PJuxt(), s, ["a"]], [1]),
                        Eq([PJuxt(), fins0, ["a"]], [1, 2])),
                    (Eq([PJuxt(), ["a"], s], [2]),
                        Eq([PJuxt(), ["a"], fins0], [2, 2])),
                )
                ce = CompareEqs(db)
                ce.assert_equality(fnone, is_method=False)
                ce.assert_equality(fy, is_method=False)

    def test_remove_script_2args(self):
        for op in (op for op in SCR_OPS_LIST if op._n_args == 2):
            db = (
                (Eq([op] + [["x"]] * op._n_args, [2]), Eq(["x"])),
                (Eq([Op("O", 1), [op] + [["x"]] * op._n_args], [1, 2]),
                    Eq([Op("O", 1), ["x"]], [1])),
                (Eq([PJuxt(), [op] + [["x"]] * op._n_args, ["y"]], [1, 2]),
                    Eq([PJuxt(), ["x"], ["y"]], [1])),
                (Eq([PJuxt(), ["y"], [op] + [["x"]] * op._n_args], [2, 2]),
                    Eq([PJuxt(), ["y"], ["x"]], [2])),
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

        for op in (op for op in SCR_OPS_LIST if op._n_args == 2):
            db = (
                (Eq([op] + [["x"]] * op._n_args, [2]), Eq(["x"])),
                (Eq([Op("O", 1), [op] + [["x"]] * op._n_args], [1, 2]),
                    Eq([Op("O", 1), ["x"]])),
                (Eq([PJuxt(), [op] + [["x"]] * op._n_args, ["y"]], [1, 2]),
                    Eq([PJuxt(), ["x"], ["y"]])),
                (Eq([PJuxt(), ["y"], [op] + [["x"]] * op._n_args], [2, 2]),
                    Eq([PJuxt(), ["y"], ["x"]])),
            )
            ce = CompareEqs(db)
            ce.assert_equality(frem, is_method=False, exclude_idx=True)

    def test_remove_script_3argsormore(self):
        for op in (op for op in SCR_OPS_LIST if op._n_args > 2):
            end = op._n_args + 1
            args = [[str(n)] for n in range(1, end)]
            for arg in range(2, end):
                finop = ScriptOp(op.is_lo(),
                                 *(k for k in op.valid_scripts_keys(True)
                                   if arg != op.spos2ord(k)))
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
                        (Eq([Op("O", 1), [op] + args], [1, arg]),
                            Eq([Op("O", 1), [finop] + finargs],
                                [1, finoarg])),
                        (Eq([PJuxt(), [op] + args, ["y"]], [1, arg]),
                            Eq([PJuxt(), [finop] + finargs, ["y"]],
                                [1, finoarg])),
                        (Eq([PJuxt(), ["y"], [op] + args], [2, arg]),
                            Eq([PJuxt(), ["y"], [finop] + finargs],
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

        for op_in in VERT_SCR_OPS_LIST + CORN_SCR_OPS_LIST:
            if op_in._n_args != 2:
                continue
            for op in VERT_SCR_OPS_LIST + CORN_SCR_OPS_LIST:
                db = (
                    (Eq([op, [op_in, ["x"], ["x"]]]
                        + [["y"]] * (op._n_args - 1), [1, 2]),
                        Eq([op, ["x"]] + [["y"]] * (op._n_args - 1), [1])),
                )

                ce = CompareEqs(db)
                ce.assert_equality(fbase, is_method=False)

        for loop_in in LO_SCR_OPS_LIST:
            if loop_in._n_args != 2:
                continue
            for op in VERT_SCR_OPS_LIST + CORN_SCR_OPS_LIST:
                finloop = ScriptOp(True, *op.valid_scripts_keys(True))

                def frem(eq):
                    retval = remove_script(eq.idx, eq, eq.idx[:-1] + [2])
                    self.assertEqual(retval, -1)
                    return eq
                db = (
                    (Eq([op, [loop_in, [PS_LO], ["a"]]]
                        + [["y"]] * (op._n_args - 1),
                        [1, 2]),
                        Eq([finloop, [PS_LO]]
                           + [["y"]] * (op._n_args - 1), [1])),
                )

                ce = CompareEqs(db)
                ce.assert_equality(fbase, is_method=False)
                ce.assert_equality(frem, is_method=False, exclude_idx=True)
                for arg in range(1, op._n_args + 1):
                    def farg(eq):
                        retval = remove_script(eq.idx, eq, eq.idx[:-2] + [arg])
                        self.assertEqual(retval, eq.idx[:-2] + [arg])
                        return eq
                    ce.assert_equality(farg, is_method=False, exclude_idx=True)

    def test_remove_script_extrefindices(self):
        s_lo = [PS_LO]
        for op in SCR_OPS_LIST:
            for i in range(2, op._n_args + 1):
                if op.is_lo():
                    if op._n_args == 2:
                        s = [op, s_lo[:], ["x"]]
                        fs = s_lo[:]
                    else:
                        finop = ScriptOp(op.is_lo(),
                                         *(k for k
                                           in op.valid_scripts_keys(True)
                                           if i != op.spos2ord(k)))
                        s = [op, s_lo[:]] + [["x"]] * (op._n_args - 1)
                        fs = [finop, s_lo[:]] + [["x"]] * (finop._n_args - 1)
                else:
                    if op._n_args == 2:
                        s = [op, ["base"], ["x"]]
                        fs = ["base"]
                    else:
                        finop = ScriptOp(op.is_lo(),
                                         *(k for k
                                           in op.valid_scripts_keys(True)
                                           if i != op.spos2ord(k)))
                        s = [op, ["base"]] + [["x"]] * (op._n_args - 1)
                        fs = [finop, ["base"]] + [["x"]] * (finop._n_args - 1)
                db = (
                    (Eq([PJuxt(), s, ["b"]], [1, i]),
                        Eq([PJuxt(), fs,  ["b"]])),
                )

                def f2(eq):
                    self.assertEqual(remove_script(eq.idx, eq, [2]), [2])
                    return eq

                ce = CompareEqs(db)
                ce.assert_equality(f2, is_method=False, exclude_idx=True)

        for loop_in in (o for o in LO_SCR_OPS_LIST if o._n_args == 2):
            for op in VERT_SCR_OPS_LIST + CORN_SCR_OPS_LIST:
                finop = equiv_loop(op)

                def f2(eq):
                    self.assertEqual(remove_script(eq.idx, eq, [2]), [2])
                    return eq

                db = (
                    (Eq([op, [loop_in, s_lo, ["a"]]]
                        + [["y"]] * (op._n_args - 1), [1, 2]),
                        Eq([finop, s_lo] + [["y"]] * (finop._n_args - 1))),
                )

                ce = CompareEqs(db)
                ce.assert_equality(f2, is_method=False, exclude_idx=True)


if __name__ == '__main__':
    unittest.main()
