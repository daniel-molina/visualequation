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

from copy import deepcopy, copy
import unittest

from visualequation.subeqs import *


class SubeqTests(unittest.TestCase):

    def test_empty_subeq(self):
        s1 = Subeq()
        s2 = Subeq([])
        self.assertEqual(s1, s2)
        self.assertEqual(len(s1), 0)

        self.assertEqual(Subeq(None), Subeq([ops.PVOID]))


    def test_ctor_containers(self):
        s0 = Subeq([ops.PJUXT, ["3"], [ops.TJUXT, ["g"], ["t"]]])
        s1 = Subeq((ops.PJUXT, ("3",), (ops.TJUXT, ("g",), ("t",),),))
        s2 = Subeq((ops.PJUXT, ["3"], (ops.TJUXT, ["g"], ("t",),),))
        p1 = Subeq(["3"])
        t1 = Subeq(["g"])
        t2 = Subeq(["t"])
        p2 = Subeq([ops.TJUXT, t1, t2])
        s3 = Subeq([ops.PJUXT, p1, p2])
        self.assertEqual(s0, s1)
        self.assertEqual(s0, s2)
        self.assertEqual(s0, s3)
        for s in (s0, s1, s2, s3):
            self.assertIsInstance(s, Subeq)
            self.assertNotIsInstance(s[0], Subeq)
            self.assertIsInstance(s[1], Subeq)
            self.assertIsInstance(s[2], Subeq)
            self.assertNotIsInstance(s[2][0], Subeq)
            self.assertIsInstance(s[2][1], Subeq)
            self.assertIsInstance(s[2][2], Subeq)
            self.assertNotIsInstance(s[2][2][0], Subeq)

        s3_ctor = Subeq(s3)
        s3_copy = copy(s3)
        s3_ctor_copy = Subeq(copy(s3))
        s3_copy_ctor = copy(Subeq(s3))
        self.assertEqual(s3, s3_ctor)
        self.assertEqual(s3, s3_copy)
        self.assertEqual(s3, s3_ctor_copy)
        self.assertEqual(s3, s3_copy_ctor)
        self.assertIsNot(s3, s3_ctor)
        self.assertIsNot(s3, s3_copy)
        self.assertIsNot(s3, s3_ctor_copy)
        self.assertIsNot(s3, s3_copy_ctor)
        for s in (s3, s3_ctor, s3_copy, s3_ctor_copy, s3_copy_ctor):
            self.assertIs(s[1], p1)
            self.assertIs(s[2], p2)
            self.assertIs(s[2][1], t1)
            self.assertIs(s[2][2], t2)

        s3_dcopy = deepcopy(s3)
        s3_ctor_dcopy = Subeq(deepcopy(s3))
        s3_dcopy_ctor = deepcopy(Subeq(s3))
        self.assertEqual(s3, s3_dcopy)
        self.assertEqual(s3, s3_ctor_dcopy)
        self.assertEqual(s3, s3_dcopy_ctor)
        for s in (s3_dcopy, s3_ctor_dcopy, s3_dcopy_ctor):
            self.assertIsNot(s, s3)
            self.assertIsNot(s[1], p1)
            self.assertIsNot(s[2], p2)
            self.assertIsNot(s[2][1], t1)
            self.assertIsNot(s[2][2], t2)

    def test_ctor_type_error(self):
        # This error is managed by list.__init__
        with self.assertRaises(TypeError):
            Subeq(2)
        with self.assertRaises(TypeError) as cm:
            Subeq("1")
        self.assertEqual(cm.exception.args[0], SUBEQ_CONTAINER_TYPE_ERROR_MSG)
        with self.assertRaises(TypeError) as cm:
            Subeq([1])
        self.assertEqual(cm.exception.args[0], SUBEQ_ELEM_TYPE_ERROR_MSG)
        with self.assertRaises(TypeError) as cm:
            Subeq([ops.PJUXT, ["d"], 2])
        self.assertEqual(cm.exception.args[0], SUBEQ_ELEM_TYPE_ERROR_MSG)
        with self.assertRaises(TypeError) as cm:
            Subeq([ops.PJUXT, ["d"], [2]])
        self.assertEqual(cm.exception.args[0], SUBEQ_ELEM_TYPE_ERROR_MSG)
        with self.assertRaises(TypeError) as cm:
            Subeq([ops.PJUXT, ["3"], [ops.TJUXT, ["g"], [9]]])
        self.assertEqual(cm.exception.args[0], SUBEQ_ELEM_TYPE_ERROR_MSG)
        with self.assertRaises(TypeError) as cm:
            Subeq([ops.PJUXT, ["3"], [ops.TJUXT, ["g"], 9]])
        self.assertEqual(cm.exception.args[0], SUBEQ_ELEM_TYPE_ERROR_MSG)
        s = Subeq(["d"])
        Subeq([ops.PVOID])
        big_s = Subeq([ops.PJUXT, ["d"], [ops.TVOID], s])

    def test_ctor_value_error(self):
        Subeq([ops.PVOID])
        Subeq(["d"])
        with self.assertRaises(ValueError) as cm:
            Subeq([ops.PVOID, ops.PVOID])
        self.assertEqual(cm.exception.args[0], SUBEQ_VALUE_ERROR_MSG)
        with self.assertRaises(ValueError) as cm:
            Subeq(["d", "d"])
        self.assertEqual(cm.exception.args[0], SUBEQ_VALUE_ERROR_MSG)
        with self.assertRaises(ValueError) as cm:
            Subeq([ops.PJUXT, ["d"], "2"])
        self.assertEqual(cm.exception.args[0], SUBEQ_VALUE_ERROR_MSG)
        with self.assertRaises(ValueError) as cm:
            Subeq([ops.PJUXT, ["d"], "2"])
        self.assertEqual(cm.exception.args[0], SUBEQ_VALUE_ERROR_MSG)
        with self.assertRaises(ValueError) as cm:
            Subeq([ops.PJUXT, ops.PVOID, ["d"]])
        self.assertEqual(cm.exception.args[0], SUBEQ_VALUE_ERROR_MSG)
        with self.assertRaises(ValueError) as cm:
            Subeq([ops.PJUXT, ops.PVOID, ["d"]])
        self.assertEqual(cm.exception.args[0], SUBEQ_VALUE_ERROR_MSG)
        with self.assertRaises(ValueError) as cm:
            Subeq([ops.PJUXT, ["3"], [ops.TJUXT, ["g"], "t"]])
        self.assertEqual(cm.exception.args[0], SUBEQ_VALUE_ERROR_MSG)
        with self.assertRaises(ValueError) as cm:
            Subeq([ops.PJUXT, ["3"], [ops.TJUXT, ["g"], ops.PVOID]])
        self.assertEqual(cm.exception.args[0], SUBEQ_VALUE_ERROR_MSG)
        # Unintended use
        Subeq([ops.PJUXT])
        Subeq([ops.TJUXT, ops.GOP])
        Subeq([["d"], ops.PJUXT])
        Subeq([["d"], [ops.PVOID]])

    def test_add(self):
        l = [ops.PJUXT, ["d"], ["e"]]
        self.assertNotIsInstance(l + Subeq([["f"]]), Subeq)
        self.assertIsInstance(Subeq() + l + Subeq([["f"]]), Subeq)
        self.assertIsInstance(Subeq([ops.GOP]) + [l], Subeq)

        s = Subeq(l)
        self.assertIsInstance(s + Subeq([["f"]]), Subeq)
        self.assertIsInstance(s + [["f"]], Subeq)

        s_sum = s + [["f"]]
        self.assertIsNot(s_sum, s)
        self.assertIs(s_sum[1], s[1])

        s_sum = s + []
        self.assertIsNot(s_sum, s)
        self.assertEqual(s_sum, s)
        self.assertIs(s_sum[1], s[1])

        s_sum = deepcopy(s) + [["f"]]
        self.assertIsNot(s_sum, s)
        self.assertIsNot(s_sum[1], s[1])

    def test_mul(self):
        s = Subeq(["x"])
        with self.assertRaises(ValueError) as cm:
            s * 2
        self.assertEqual(cm.exception.args[0], SUBEQ_VALUE_ERROR_MSG)

        s = Subeq([ops.PJUXT, ["x"]])
        p = s[1:] * 3
        for idx in ([], [0], [1], [2]):
            self.assertIsInstance(p(idx), Subeq)
        self.assertEqual(p, [["x"], ["x"], ["x"]])

    def test_rmul(self):
        s = Subeq(["x"])
        with self.assertRaises(ValueError) as cm:
            2 * s
        self.assertEqual(cm.exception.args[0], SUBEQ_VALUE_ERROR_MSG)

        s = Subeq([ops.PJUXT, ["x"]])
        p = 3 * s[1:]
        for idx in ([], [0], [1], [2]):
            self.assertIsInstance(p(idx), Subeq)
        self.assertEqual(p, [["x"], ["x"], ["x"]])

    def test_getitem(self):
        s = Subeq([ops.GOP, [ops.PJUXT, ["d"], [ops.TVOID]]])
        self.assertIsInstance(s[0], ops.Op)
        self.assertIs(s[0], ops.GOP)
        self.assertIsInstance(s[1], Subeq)
        self.assertEqual(s[1], Subeq([ops.PJUXT, ["d"], [ops.TVOID]]))
        self.assertIsNot(s[1], Subeq([ops.PJUXT, ["d"], [ops.TVOID]]))
        self.assertIs(s[1], s[1])
        self.assertIsInstance(s[1][0], ops.Op)
        self.assertIs(s[1][0], ops.PJUXT)
        self.assertIsInstance(s[1][1], Subeq)
        self.assertIsInstance(s[1][2], Subeq)
        self.assertIsInstance(s[1][1][0], str)
        self.assertIs(s[1][1][0], "d")
        self.assertIsInstance(s[1][2][0], ops.Op)
        self.assertIs(s[1][2][0], ops.TVOID)

        with self.assertRaises(IndexError):
            s[233]
        with self.assertRaises(IndexError):
            s[-233]

        for start, end in zip(range(-10, -10 + 15), range(6, 6 - 15, -1)):
            self.assertIsInstance(s[start:end], Subeq)
            self.assertIsInstance(s[1][start:end], Subeq)
            self.assertIsInstance(s[1][1][start:end], Subeq)
            self.assertIsInstance(s[1][2][start:end], Subeq)
        self.assertEqual(s, s[:])
        self.assertIsNot(s, s[:])
        s1 = s[1]
        self.assertIs(s1, s[1])
        self.assertIsNot(s1, s[1][:])
        self.assertEqual(s1, s[1][:])
        self.assertIsNot(s1, deepcopy(s[1]))
        self.assertEqual(s1, deepcopy(s[1]))
        for n in range(-10, 10):
            self.assertIsInstance(s[n:n], Subeq)
            self.assertEqual(len(s[n:n]), 0)
        self.assertEqual(len(s[0:1]), 1)
        self.assertEqual(len(s[-32:33]), 2)

        self.assertEqual(Subeq(["a"]), ["a"])
        self.assertEqual(Subeq([ops.PVOID]), [ops.PVOID])
        self.assertEqual(Subeq([ops.GOP, ["a"]]), [ops.GOP, ["a"]])

        with self.assertRaises(TypeError) as cm:
            s["d"]
        self.assertEqual(cm.exception.args[0],
                         SUBEQ_ORDINARY_INDEXING_ERROR_MSG)
        with self.assertRaises(TypeError) as cm:
            s[Idx([1, 1])]
        self.assertEqual(cm.exception.args[0],
                         SUBEQ_ORDINARY_INDEXING_ERROR_MSG)

    def test_setitem(self):
        s = Subeq(["d"])
        s[0] = "4"
        s[0] = ops.PVOID
        p = Subeq([ops.PJUXT, ["d"], ["e"]])
        p[1][0] = "y"
        p[2][0] = ops.TVOID
        # Unintended use -> [[...]]
        s[0] = [ops.PJUXT, ["d"], [ops.TVOID]]
        s[0] = (ops.PJUXT, ("d",), [ops.TVOID])
        s[0] = Subeq([ops.PJUXT, ["d"], [ops.TVOID]])

        s = Subeq(["d"])
        s[:] = [ops.PJUXT, ["d"], [ops.TVOID]]  # Commonly used
        s[1:] = [["a"], ["b"], ["c"]]
        s[1:] = (["a"], ("b",), ["c"])
        s[1:] = Subeq([["a"], ["b"], ["c"]])

        s = Subeq([ops.PJUXT, ["d"], ["e"]])
        with self.assertRaises(TypeError) as cm:
            s["d"]
        self.assertEqual(cm.exception.args[0],
                         SUBEQ_ORDINARY_INDEXING_ERROR_MSG)
        with self.assertRaises(TypeError) as cm:
            s[Idx([1])]
        self.assertEqual(cm.exception.args[0],
                         SUBEQ_ORDINARY_INDEXING_ERROR_MSG)
        for value in (8, [5], Idx([4, 2]), 2.3):
            with self.assertRaises(TypeError) as cm:
                s[0] = value
            self.assertEqual(cm.exception.args[0], SUBEQ_ELEM_TYPE_ERROR_MSG)
        for pos in range(3):
            with self.assertRaises(ValueError) as cm:
                s[pos] = "a"
            self.assertEqual(cm.exception.args[0], SUBEQ_VALUE_ERROR_MSG)
        s[1][0] = "a"
        for value in ("d", ops.PVOID):
            with self.assertRaises(TypeError) as cm:
                s[0:1] = value
            self.assertEqual(cm.exception.args[0],
                             SUBEQ_CONTAINER_TYPE_ERROR_MSG)

    def test_iadd(self):
        l = [ops.PJUXT, ["d"], ["e"]]

        r = deepcopy(l)
        r += Subeq([["f"]])
        self.assertNotIsInstance(r, Subeq)
        self.assertIsInstance(r[3], Subeq)

        r = Subeq([ops.PJUXT, ["a"], ["b"], ["c"]])
        with self.assertRaises(TypeError) as cm:
            r += l[1:]
        self.assertEqual(cm.exception.args[0], SUBEQ_IADD_TYPE_ERROR_MSG)
        self.assertEqual(r, [ops.PJUXT, ["a"], ["b"], ["c"]])

        r = Subeq([ops.PJUXT, ["a"], ["b"], ["c"]])
        r += Subeq(l[1:])
        self.assertEqual(r, [ops.PJUXT, ["a"], ["b"], ["c"], ["d"], ["e"]])
        self.assertIsInstance(r, Subeq)
        self.assertIsInstance(r[4], Subeq)
        self.assertIsInstance(r[5], Subeq)

        s = Subeq(l)
        s1 = s[1]
        s += [Subeq(["f"])]
        self.assertEqual(s, [ops.PJUXT, ["d"], ["e"], ["f"]])
        self.assertIsInstance(s, Subeq)
        self.assertIsInstance(s[3], Subeq)
        self.assertIs(s[1], s1)

    def test_imul(self):
        s = Subeq(["x"])
        with self.assertRaises(ValueError) as cm:
            s *= 2
        self.assertEqual(cm.exception.args[0], SUBEQ_VALUE_ERROR_MSG)

        s = Subeq([ops.PJUXT, ["x"]])
        s[1:] *= 3
        for idx in ([], [1], [2], [3]):
            self.assertIsInstance(s(idx), Subeq)
        self.assertEqual(s, [ops.PJUXT, ["x"], ["x"], ["x"]])

    def test_str(self):
        self.assertEqual(str(Subeq()), "[]")
        self.assertEqual(str(Subeq(["2"])), "[2]")
        self.assertEqual(str(Subeq([ops.PVOID])), "[PVOID]")
        self.assertEqual(str(Subeq([ops.PJUXT, ["d"], [ops.TVOID]])),
                         "[PJUXT, [d], [TVOID]]")

    def test_repr(self):
        self.assertEqual(repr(Subeq()), "Subeq()")
        self.assertEqual(repr(Subeq([])), "Subeq()")
        self.assertEqual(repr(Subeq(())), "Subeq()")
        self.assertEqual(repr(Subeq(["2"])), "Subeq(['2'])")
        self.assertEqual(repr(Subeq([ops.PVOID])),
                         "Subeq([" + repr(ops.PVOID) + "])")
        self.assertEqual(repr(Subeq([ops.PJUXT, ["d"], [ops.TVOID]])),
                         "Subeq([" + repr(ops.PJUXT) + ", ['d'], "
                         + "[" + repr(ops.TVOID) + "]])")
        # Unintended use
        self.assertEqual(repr(Subeq([ops.PJUXT, ["d"], []])),
                         "Subeq([" + repr(ops.PJUXT) + ", ['d'], []])")
        self.assertEqual(repr(Subeq([ops.PJUXT, ["d"], ()])),
                         "Subeq([" + repr(ops.PJUXT) + ", ['d'], []])")

    def test_srepr(self):
        self.assertEqual(Subeq().srepr(), "Subeq()")
        self.assertEqual(Subeq([]).srepr(), "Subeq()")
        self.assertEqual(Subeq(()).srepr(), "Subeq()")
        self.assertEqual(Subeq(["2"]).srepr(), "Subeq(['2'])")
        self.assertEqual(Subeq([ops.PVOID]).srepr(),
                         "Subeq([PVOID])")
        self.assertEqual(Subeq([ops.PJUXT, ["d"], [ops.TVOID]]).srepr(),
                         "Subeq([PJUXT, ['d'], "
                         + "[TVOID]])")
        # Unintended use
        self.assertEqual(Subeq([ops.PJUXT, ["d"], []]).srepr(),
                         "Subeq([PJUXT, ['d'], []])")
        self.assertEqual(Subeq([ops.PJUXT, ["d"], ()]).srepr(),
                         "Subeq([PJUXT, ['d'], []])")

    def test_subeq_bool(self):
        # __bool__ is not finally overridden
        self.assertFalse(Subeq())
        self.assertFalse(Subeq([]))
        self.assertFalse(Subeq(()))
        self.assertTrue(Subeq([ops.PVOID]))
        self.assertTrue(Subeq([ops.TVOID]))
        self.assertTrue(Subeq([""]))
        self.assertTrue(Subeq(["x"]))
        self.assertTrue(Subeq([ops.Op("x", "x")]))
        self.assertTrue(Subeq([ops.PJUXT, ["d"], [ops.Op("x", "x")]]))

    def test_append(self):
        s = Subeq()
        s.append(ops.PJUXT)
        s.append(Subeq(["a"]))
        s.append(Subeq([ops.TVOID]))
        self.assertEqual(s, Subeq([ops.PJUXT, ["a"], [ops.TVOID]]))
        s.append(Subeq([ops.PJUXT, ["a"], [ops.TVOID]]))
        # Unintended use
        for i in range(5):
            s.append(ops.GOP)

        # This test is crucial to deepcopy correctly
        s = Subeq()
        s.append("a")
        s = Subeq()
        s.append(ops.PVOID)

        s = Subeq()
        with self.assertRaises(TypeError) as cm:
            s.append(["d"])
        self.assertEqual(cm.exception.args[0], SUBEQ_APPEND_TYPE_ERROR_MSG)
        with self.assertRaises(TypeError) as cm:
            s.append(["d", "e"])
        self.assertEqual(cm.exception.args[0], SUBEQ_APPEND_TYPE_ERROR_MSG)
        for value in (1, [2], Idx([3, 4]), 9.6):
            with self.assertRaises(TypeError) as cm:
                s.append(value)
            self.assertEqual(cm.exception.args[0], SUBEQ_APPEND_TYPE_ERROR_MSG)
        self.assertEqual(s, Subeq())
        s = Subeq(["3"])
        for value in ("4", ops.PVOID, ops.TVOID):
            with self.assertRaises(ValueError) as cm:
                s.append(value)
            self.assertEqual(cm.exception.args[0], SUBEQ_VALUE_ERROR_MSG)
        self.assertEqual(s, Subeq(["3"]))

    def test_extend(self):
        for value in ([], (), Subeq()):
            s = Subeq()
            s.extend(value)
            s.extend(value)
            self.assertEqual(s, Subeq())

        for value in ([Subeq(["a"])], (Subeq(["a"]),), Subeq([Subeq(["a"])])):
            s = Subeq()
            s.extend(value)
            s.extend(value)
            self.assertEqual(s, Subeq([["a"], ["a"]]))
            self.assertEqual(s, Subeq(2*[["a"]]))

        for value in ([Subeq([ops.PJUXT, ["a"], [ops.TVOID]])],
                      (Subeq([ops.PJUXT, ["a"], [ops.TVOID]]),),
                      Subeq([Subeq([ops.PJUXT, ["a"], [ops.TVOID]])])):
            s = Subeq()
            s.extend(value)
            s.extend(value)
            self.assertEqual(s, Subeq(2*[[ops.PJUXT, ["a"], [ops.TVOID]]]))

        for value in ([Subeq([ops.GOP]),
                       Subeq([ops.PJUXT, ["a"], [ops.TVOID]])],
                      (Subeq([ops.GOP]),
                       Subeq([ops.PJUXT, ["a"], [ops.TVOID]])),
                      Subeq([Subeq([ops.GOP]),
                             Subeq([ops.PJUXT, ["a"], [ops.TVOID]])])):
            s = Subeq()
            s.extend(value)
            s.extend(value)
            self.assertEqual(s, Subeq(2*[[ops.GOP], [ops.PJUXT, ["a"],
                                        [ops.TVOID]]]))

            # Operators with n_args != 0 can be used to extend a subeq
            s.extend([ops.GOP, Subeq(["d"])])
            # Unintended use
            s.extend([ops.GOP, ops.PJUXT, ops.TJUXT])

            # Unintended use
            for value in ([Subeq()], (Subeq(),), Subeq([Subeq()])):
                s = Subeq()
                s.extend(value)
                self.assertEqual(s, Subeq([[]]))
                s.extend(value)
                self.assertEqual(s, Subeq([[], []]))

            for i in range(5):
                s.extend([Subeq(), Subeq(), Subeq()])

        s = Subeq()
        with self.assertRaises(TypeError) as cm:
            s.extend('f')
        self.assertEqual(cm.exception.args[0], SUBEQ_CONTAINER_TYPE_ERROR_MSG)
        with self.assertRaises(TypeError) as cm:
            s.extend(7)
        self.assertEqual(cm.exception.args[0], SUBEQ_CONTAINER_TYPE_ERROR_MSG)
        with self.assertRaises(TypeError) as cm:
            s.extend(ops.PVOID)
        self.assertEqual(cm.exception.args[0], SUBEQ_CONTAINER_TYPE_ERROR_MSG)

        with self.assertRaises(TypeError) as cm:
            s.extend(["f"])
        self.assertEqual(cm.exception.args[0], SUBEQ_EXTEND_TYPE_ERROR_MSG)
        with self.assertRaises(TypeError) as cm:
            s.extend([ops.PVOID])
        self.assertEqual(cm.exception.args[0], SUBEQ_EXTEND_TYPE_ERROR_MSG)

    def test_insert(self):
        for pos in range(1, 5):
            s = Subeq([ops.GOP])
            s.insert(pos, Subeq(["d"]))
            self.assertEqual(s, Subeq([ops.GOP, ["d"]]))

        s = Subeq([["d"], ["f"]])
        s.insert(0, ops.PJUXT)
        self.assertEqual(s, Subeq([ops.PJUXT, ["d"], ["f"]]))
        s.insert(2, Subeq(["e"]))
        self.assertEqual(s, Subeq([ops.PJUXT, ["d"], ["e"], ["f"]]))

        # Unintended use
        s = Subeq()
        s.insert(0, Subeq())
        s.insert(0, Subeq())
        self.assertEqual(s, Subeq([[], []]))

        s = Subeq()
        for pos in range(-4, 4):
            for value in (1, [2], Idx([3, 4]), ["a"], [ops.PVOID],
                          [ops.PJUXT]):
                with self.assertRaises(TypeError) as cm:
                    s.insert(pos, value)
                self.assertEqual(cm.exception.args[0],
                                 SUBEQ_INSERT_TYPE_ERROR_MSG)

if __name__ == "__main__":
    unittest.main()
