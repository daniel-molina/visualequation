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

from visualequation.idx import *
from visualequation import ops
from visualequation.subeqs import Subeq


class IdxCore(unittest.TestCase):

    def test_empty(self):
        idx0 = Idx()
        idx1 = Idx(None)
        idx2 = Idx([])
        idx3 = Idx(Idx())
        self.assertEqual(idx0, idx1)
        self.assertEqual(idx0, idx2)
        self.assertEqual(idx0, idx3)
        self.assertEqual(idx0, NOIDX)
        self.assertEqual(idx0, [])
        self.assertEqual(len(idx0), 0)
        self.assertIsNot(idx0, idx1)
        self.assertIsNot(idx0, NOIDX)

    def test_ctor(self):
        idx1 = Idx([1, 3, 4])
        idx2 = Idx((1, 3, 4))
        idx3 = Idx(1, 3, 4)
        idx4 = Idx(Idx(1, 3, 4))
        self.assertEqual(idx1, idx2)
        self.assertEqual(idx1, idx3)
        self.assertEqual(idx1, idx4)

    def test_type_error_idx(self):
        with self.assertRaises(TypeError) as cm:
            Idx([None])
        self.assertEqual(cm.exception.args[0], IDX_TYPE_ERROR_MSG)
        with self.assertRaises(TypeError) as cm:
            Idx([3, None])
        self.assertEqual(cm.exception.args[0], IDX_TYPE_ERROR_MSG)
        with self.assertRaises(TypeError) as cm:
            Idx([[1]])
        self.assertEqual(cm.exception.args[0], IDX_TYPE_ERROR_MSG)
        with self.assertRaises(TypeError) as cm:
            Idx(9.2)
        self.assertEqual(cm.exception.args[0], IDX_TYPE_ERROR_MSG)
        with self.assertRaises(TypeError) as cm:
            Idx(9.2, 3.2)
        self.assertEqual(cm.exception.args[0], IDX_TYPE_ERROR_MSG)
        with self.assertRaises(TypeError) as cm:
            Idx([""])
        self.assertEqual(cm.exception.args[0], IDX_TYPE_ERROR_MSG)
        with self.assertRaises(TypeError) as cm:
            Idx(["1"])
        self.assertEqual(cm.exception.args[0], IDX_TYPE_ERROR_MSG)
        with self.assertRaises(TypeError) as cm:
            Idx([2, [2], 4])
        self.assertEqual(cm.exception.args[0], IDX_TYPE_ERROR_MSG)
        with self.assertRaises(TypeError) as cm:
            Idx(Subeq(["1"]))
        self.assertEqual(cm.exception.args[0], IDX_TYPE_ERROR_MSG)
        with self.assertRaises(TypeError) as cm:
            Idx([Idx([1, 3])])
        self.assertEqual(cm.exception.args[0], IDX_TYPE_ERROR_MSG)
        with self.assertRaises(TypeError) as cm:
            Idx([2, 4], 3)
        self.assertEqual(cm.exception.args[0], IDX_TYPE_ERROR_MSG)
        with self.assertRaises(TypeError) as cm:
            Idx(3, [2, 4])
        self.assertEqual(cm.exception.args[0], IDX_TYPE_ERROR_MSG)
        with self.assertRaises(TypeError) as cm:
            Idx(3, "3")
        self.assertEqual(cm.exception.args[0], IDX_TYPE_ERROR_MSG)
        Idx(Idx([]))
        Idx(Idx([1, 2]))

    def test_value_error_idx(self):
        with self.assertRaises(ValueError) as cm:
            Idx([-1])
        self.assertEqual(cm.exception.args[0], IDX_VALUE_ERROR_MSG)
        with self.assertRaises(ValueError) as cm:
            Idx(3, -1)
        self.assertEqual(cm.exception.args[0], IDX_VALUE_ERROR_MSG)
        with self.assertRaises(ValueError) as cm:
            Idx([1, -1])
        self.assertEqual(cm.exception.args[0], IDX_VALUE_ERROR_MSG)
        with self.assertRaises(ValueError) as cm:
            Idx([-1, 1])
        self.assertEqual(cm.exception.args[0], IDX_VALUE_ERROR_MSG)
        with self.assertRaises(ValueError) as cm:
            Idx([-99, 3, 5, 7])
        self.assertEqual(cm.exception.args[0], IDX_VALUE_ERROR_MSG)
        with self.assertRaises(ValueError) as cm:
            Idx([1, 3, -53, 7])
        self.assertEqual(cm.exception.args[0], IDX_VALUE_ERROR_MSG)
        Idx([0])
        Idx([1])
        Idx([89])
        Idx([1, 14, 51, 61, 11, 61, 81])
        Idx([1, 14, 51, 61, 11, 61, 81, 0])  # lop
        # Invalid index, but accepted by Idx
        Idx([1, 14, 51, 61, 11, 61, 81, 0, 4])

    def test_add(self):
        with self.assertRaises(TypeError):
            Idx() + (3, 5)
        self.assertIsInstance(Idx() + [], Idx)
        self.assertIsInstance(Idx([1]) + [], Idx)
        self.assertIsInstance(NOIDX + [3], Idx)
        self.assertIsInstance(Idx([5]) + [2], Idx)
        # Idx accepts this even if it is not a valid subeq index
        self.assertIsInstance(Idx([0]) + [2], Idx)
        # If first operand is a list, Idx.__add__ cannot convert list to Idx
        self.assertNotIsInstance([] + Idx(), Idx)
        self.assertNotIsInstance([3] + Idx(), Idx)
        self.assertNotIsInstance([3] + Idx([5]), Idx)

        self.assertEqual(len(Idx([5]) + [2, 5] + Idx([])), 3)
        self.assertEqual(len(NOIDX + [2, 5] + Idx([6])), 3)
        self.assertEqual(len(NOIDX + [] + Idx([6])), 1)

    def test_add_type_error(self):
        with self.assertRaises(TypeError) as cm:
            Idx() + ["asd"]
        self.assertEqual(cm.exception.args[0], IDX_TYPE_ERROR_MSG)
        with self.assertRaises(TypeError) as cm:
            Idx() + [[1]]
        self.assertEqual(cm.exception.args[0], IDX_TYPE_ERROR_MSG)
        with self.assertRaises(TypeError):
            Idx() + 3
        with self.assertRaises(TypeError):
            Idx([1, 4]) + 3
        with self.assertRaises(TypeError) as cm:
            NOIDX + [Subeq()]
        self.assertEqual(cm.exception.args[0], IDX_TYPE_ERROR_MSG)
        with self.assertRaises(TypeError) as cm:
            Idx() + [Subeq([ops.PVOID])]
        self.assertEqual(cm.exception.args[0], IDX_TYPE_ERROR_MSG)

    def test_add_value_error(self):
        with self.assertRaises(ValueError) as cm:
            Idx() + [-1]
        self.assertEqual(cm.exception.args[0], IDX_VALUE_ERROR_MSG)
        with self.assertRaises(ValueError) as cm:
            Idx([-3]) + Idx()
        self.assertEqual(cm.exception.args[0], IDX_VALUE_ERROR_MSG)
        with self.assertRaises(ValueError) as cm:
            Idx([5]) + Idx([-4])
        self.assertEqual(cm.exception.args[0], IDX_VALUE_ERROR_MSG)
        with self.assertRaises(ValueError) as cm:
            Idx([5]) + Idx([-4]) + Idx([0])
        self.assertEqual(cm.exception.args[0], IDX_VALUE_ERROR_MSG)
        with self.assertRaises(ValueError) as cm:
            Idx([5]) + [-1] + Idx([0])
        self.assertEqual(cm.exception.args[0], IDX_VALUE_ERROR_MSG)
        with self.assertRaises(ValueError) as cm:
            NOIDX + Idx([-4]) + Idx([0])
        self.assertEqual(cm.exception.args[0], IDX_VALUE_ERROR_MSG)
        # Left operand is not an Idx so it will not raise an error
        [-31] + Idx([4, 2])
        [] + [-4] + Idx([5])

    def test_getitem_int(self):
        for idx in (Idx([1, 3, 0]), Idx([8, 2, 9])):
            self.assertIsInstance(idx[0], int)
            self.assertIsInstance(idx[1], int)
            self.assertIsInstance(idx[2], int)
            self.assertIsInstance(idx[-1], int)
            self.assertIsInstance(idx[-2], int)
            self.assertIsInstance(idx[-3], int)
            with self.assertRaises(IndexError):
                idx[3]
            with self.assertRaises(IndexError):
                idx[-4]
        with self.assertRaises(IndexError):
            Idx()[0]
        with self.assertRaises(IndexError):
            NOIDX[0]

    def test_getitem_slice(self):
        for idx in (Idx([1, 3, 0]), Idx([8, 2, 9])):
            # Type
            self.assertIsInstance(idx[:], Idx)
            self.assertIsInstance(idx[None:None], Idx)
            self.assertIsInstance(idx[0:], Idx)
            self.assertIsInstance(idx[1:], Idx)
            self.assertIsInstance(idx[2:], Idx)
            self.assertIsInstance(idx[3:], Idx)
            self.assertIsInstance(idx[287:], Idx)
            self.assertIsInstance(idx[-1:], Idx)
            self.assertIsInstance(idx[-2:], Idx)
            self.assertIsInstance(idx[-3:], Idx)
            self.assertIsInstance(idx[-234:], Idx)
            self.assertIsInstance(idx[:], Idx)
            self.assertIsInstance(idx[:0], Idx)
            self.assertIsInstance(idx[:1], Idx)
            self.assertIsInstance(idx[:2], Idx)
            self.assertIsInstance(idx[:3], Idx)
            self.assertIsInstance(idx[:287], Idx)
            self.assertIsInstance(idx[:-1], Idx)
            self.assertIsInstance(idx[:-2], Idx)
            self.assertIsInstance(idx[:-3], Idx)
            self.assertIsInstance(idx[:-234], Idx)

            # Length
            self.assertEqual(len(idx[:]), 3)
            self.assertEqual(len(idx[1:1]), 0)
            self.assertEqual(len(idx[0:3]), 3)
            self.assertEqual(len(idx[0:4123]), 3)
            self.assertEqual(len(idx[-1:]), 1)
            self.assertEqual(len(idx[2:]), 1)
            self.assertEqual(len(idx[3:]), 0)
            self.assertEqual(len(idx[1:1]), 0)

        self.assertIsInstance(NOIDX[:], Idx)
        self.assertIsInstance(NOIDX[-3:532], Idx)
        self.assertEqual(len(NOIDX), 0)

    def test_setitem_int(self):
        nidx = NOIDX[:]
        idx = Idx([5, 2, 3])
        idx[0] = 2
        self.assertIsInstance(idx, Idx)
        self.assertNotIsInstance(idx[0], Idx)
        self.assertIsInstance(idx[0], int)
        idx[0] = 10
        idx[1] = 11
        idx[2] = 12
        self.assertEqual(idx[0], 10)
        self.assertEqual(idx[1], 11)
        self.assertEqual(idx[2], 12)
        idx[-3] = 101
        idx[-2] = 111
        idx[-1] = 121
        self.assertEqual(idx[0], 101)
        self.assertEqual(idx[1], 111)
        self.assertEqual(idx[2], 121)
        with self.assertRaises(TypeError) as cm:
            idx[0] = "3"
        self.assertEqual(cm.exception.args[0], IDX_TYPE_ERROR_MSG)
        with self.assertRaises(TypeError) as cm:
            idx[0] = []
        self.assertEqual(cm.exception.args[0], IDX_TYPE_ERROR_MSG)
        with self.assertRaises(TypeError) as cm:
            idx[0] = [2, 4]
        self.assertEqual(cm.exception.args[0], IDX_TYPE_ERROR_MSG)
        with self.assertRaises(ValueError) as cm:
            idx[1] = -3
        self.assertEqual(cm.exception.args[0], IDX_VALUE_ERROR_MSG)
        with self.assertRaises(IndexError):
            idx[3] = 90
        with self.assertRaises(IndexError):
            idx[-4] = 6
        a = idx
        self.assertEqual(a, idx)
        self.assertIs(a, idx)
        a[0] = 999
        self.assertEqual(idx[0], 999)

    def test_setitem_slice(self):
        for idx in (Idx([1, 2, 3, 0]), Idx([1])):
            a = idx[:]
            self.assertIsInstance(a, Idx)
            self.assertEqual(a, idx)
            self.assertIsNot(a, idx)
            a[1:2] = [1, 3]
            self.assertIsInstance(a, Idx)
            self.assertNotEqual(a, idx)
            self.assertNotEqual(len(a), len(idx))
            a = idx
            self.assertIs(a, idx)
            self.assertEqual(a, idx)
            a[1:1] = [1, 4, 6]
            self.assertIsInstance(a, Idx)
            self.assertEqual(a, idx)
            b = a[None:None]
            b[:] = []
            self.assertIsInstance(b, Idx)
            self.assertEqual(len(b), 0)
            idx[-34242:31313] = [4]
            self.assertEqual(len(idx), 1)
            idx_bkp = idx[:]
            with self.assertRaises(TypeError):
                idx[1:2] = 6
            with self.assertRaises(TypeError) as cm:
                idx[1:2] = Subeq(["d"])
            self.assertEqual(cm.exception.args[0], IDX_TYPE_ERROR_MSG)
            with self.assertRaises(ValueError) as cm:
                idx[1:2] = [-1]
            self.assertEqual(cm.exception.args[0], IDX_VALUE_ERROR_MSG)
            with self.assertRaises(ValueError) as cm:
                idx[1:2] = [3, -1, 6]
            self.assertEqual(cm.exception.args[0], IDX_VALUE_ERROR_MSG)
            with self.assertRaises(ValueError) as cm:
                idx[1:2] = [-1, -4]
            self.assertEqual(cm.exception.args[0], IDX_VALUE_ERROR_MSG)
            self.assertEqual(idx, idx_bkp)

        NOIDX_BKP = NOIDX[:]
        # Do not do this in real code!
        NOIDX[:] = [2, 4]
        self.assertFalse(not NOIDX)
        self.assertTrue(len(NOIDX), 2)
        NOIDX[:] = NOIDX_BKP[:]
        self.assertTrue(not NOIDX)
        self.assertEqual(len(NOIDX), 0)

    def test_iadd(self):
        idx = Idx([2])
        idx += Idx(4, 5)
        self.assertEqual(idx, [2, 4, 5])
        self.assertIsInstance(idx, Idx)

        idx = Idx([2])
        idx += [4, 5]
        self.assertEqual(idx, [2, 4, 5])
        self.assertIsInstance(idx, Idx)

        idx = Idx([2])
        idx += (4, 5)
        self.assertEqual(idx, [2, 4, 5])
        self.assertIsInstance(idx, Idx)

    def test_append(self):
        idx = Idx([])
        idx.append(3)
        idx.append(0)
        self.assertIsInstance(idx, Idx)
        with self.assertRaises(TypeError) as cm:
            idx.append([2])
        self.assertEqual(cm.exception.args[0], IDX_TYPE_ERROR_MSG)
        with self.assertRaises(TypeError) as cm:
            idx.append("1")
        self.assertEqual(cm.exception.args[0], IDX_TYPE_ERROR_MSG)
        with self.assertRaises(ValueError) as cm:
            idx.append(-5)
        self.assertEqual(cm.exception.args[0], IDX_VALUE_ERROR_MSG)
        self.assertEqual(len(idx), 2)

    def test_extend(self):
        idx = Idx()
        idx.extend([1, 3])
        idx.extend((1, 3))
        self.assertIsInstance(idx, Idx)
        with self.assertRaises(TypeError):
            idx.extend(1)
        with self.assertRaises(TypeError) as cm:
            idx.extend("1")
        self.assertEqual(cm.exception.args[0], IDX_TYPE_ERROR_MSG)
        with self.assertRaises(ValueError) as cm:
            idx.append(-5)
        self.assertEqual(cm.exception.args[0], IDX_VALUE_ERROR_MSG)
        self.assertEqual(len(idx), 4)
        idx.extend(Idx([1, 3]))
        idx.extend(idx)
        self.assertIsInstance(idx, Idx)

    def test_insert(self):
        idx = Idx([3, 4])
        idx.insert(0, 9)
        self.assertIsInstance(idx, Idx)
        self.assertEqual(idx, Idx([9, 3, 4]))
        with self.assertRaises(TypeError) as cm:
            idx.insert(5, [1])
        self.assertEqual(cm.exception.args[0], IDX_TYPE_ERROR_MSG)
        with self.assertRaises(TypeError) as cm:
            idx.insert(0, "1")
        self.assertEqual(cm.exception.args[0], IDX_TYPE_ERROR_MSG)
        with self.assertRaises(ValueError) as cm:
            idx.insert(1, -5)
        self.assertEqual(cm.exception.args[0], IDX_VALUE_ERROR_MSG)
        self.assertEqual(len(idx), 3)
        a = NOIDX[:]
        a.insert(3131, 9)
        a.insert(41, 34)
        self.assertEqual(a, Idx([9, 34]))
        a.insert(-1, 0)
        self.assertEqual(a, Idx([9, 0, 34]))
        a.insert(-900, 8)
        self.assertEqual(a, Idx([8, 9, 0, 34]))


if __name__ == "__main__":
    unittest.main()
