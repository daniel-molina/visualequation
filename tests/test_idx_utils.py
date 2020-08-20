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


class IdxUtils(unittest.TestCase):
    def test_parord(self):
        self.assertEqual(NOIDX.parord(), -2)
        self.assertEqual(Idx([14]).parord(), 14)
        self.assertEqual(Idx([4, 2]).parord(), 2)
        self.assertEqual(Idx([9, 4, 1]).parord(), 1)
        # Unintended uses
        self.assertEqual(Idx([9, 4, 0]).parord(), 0)

    def test_supeq(self):
        self.assertNotIsInstance(NOIDX.supeq(), Idx)
        self.assertEqual(NOIDX.supeq(), -2)
        sup_idx = Idx([1]).supeq()
        self.assertIsInstance(sup_idx, Idx)
        self.assertEqual(sup_idx, NOIDX)
        self.assertIsInstance(Idx([4, 2]).supeq(), Idx)
        self.assertEqual(Idx([4, 2]).supeq(), Idx([4]))

        idx = Idx([2, 8, 1])
        self.assertIsNone(idx.supeq(set=True))
        self.assertIsInstance(idx, Idx)
        self.assertEqual(idx, Idx([2, 8]))
        idx = Idx()
        with self.assertRaises(IndexError) as cm:
            idx.supeq(set=True)
        self.assertEqual(cm.exception.args[0], SUPEQ_ERROR_MSG)
        self.assertEqual(idx, NOIDX)

        # Unintended use
        self.assertEqual(Idx([4, 0]).supeq(), Idx([4]))
        idx = Idx([2, 8, 0])
        self.assertIsNone(idx.supeq(set=True))
        self.assertIsInstance(idx, Idx)
        self.assertEqual(idx, Idx([2, 8]))

    def test_outlop(self):
        self.assertNotIsInstance(NOIDX.outlop(), Idx)
        self.assertEqual(NOIDX.outlop(), -2)
        self.assertIsInstance(Idx([2]).outlop(), Idx)
        self.assertEqual(Idx([2]).outlop(), Idx([0]))
        self.assertIsInstance(Idx([5, 6]).outlop(), Idx)
        self.assertEqual(Idx([5, 6]).outlop(), Idx([5, 0]))

        idx = Idx()
        with self.assertRaises(IndexError) as cm:
            idx.outlop(set=True)
        self.assertEqual(cm.exception.args[0], SUPEQ_ERROR_MSG)
        self.assertIsInstance(idx, Idx)
        self.assertEqual(idx, NOIDX)
        idx.append(0)
        self.assertIsNone(idx.outlop(set=True))
        self.assertEqual(idx, Idx([0]))
        self.assertIsInstance(idx, Idx)
        idx = Idx([3, 5, 2])
        self.assertIsNone(idx.outlop(set=True))
        self.assertEqual(idx, Idx([3, 5, 0]))
        self.assertIsInstance(idx, Idx)
        # Unintended use
        idx = Idx([3, 5, 0]).outlop()
        self.assertEqual(idx, Idx([3, 5, 0]))
        self.assertIsInstance(idx, Idx)
        idx = Idx([3, 5, 0])
        self.assertIsNone(idx.outlop(set=True))
        self.assertEqual(idx, Idx([3, 5, 0]))
        self.assertIsInstance(idx, Idx)

    def test_prevpar(self):
        self.assertEqual(NOIDX.prevpar(), -2)
        self.assertEqual(Idx([1]).prevpar(), -1)
        self.assertEqual(Idx([4, 1]).prevpar(), -1)
        self.assertEqual(Idx([3, 1, 5, 1]).prevpar(), -1)
        self.assertEqual(Idx([3]).prevpar(), Idx([2]))
        self.assertEqual(Idx([6, 9]).prevpar(), Idx([6, 8]))
        self.assertIsInstance(Idx([6, 9]).prevpar(), Idx)

        idx = Idx()
        with self.assertRaises(IndexError) as cm:
            idx.prevpar(set=True)
        self.assertEqual(cm.exception.args[0], SUPEQ_ERROR_MSG)
        idx = Idx([1])
        with self.assertRaises(IndexError) as cm:
            idx.prevpar(set=True)
        self.assertEqual(cm.exception.args[0], NO_CO_PAR_ERROR_MSG)
        idx = Idx([4, 2, 5, 1])
        with self.assertRaises(IndexError) as cm:
            idx.prevpar(set=True)
        self.assertEqual(cm.exception.args[0], NO_CO_PAR_ERROR_MSG)
        idx = Idx([2])
        self.assertIsNone(idx.prevpar(set=True))
        self.assertIsInstance(idx, Idx)
        self.assertEqual(idx, Idx([1]))
        idx = Idx([8])
        self.assertIsNone(idx.prevpar(set=True))
        self.assertIsInstance(idx, Idx)
        self.assertEqual(idx, Idx([7]))
        idx = Idx([6, 1, 6])
        self.assertIsNone(idx.prevpar(set=True))
        self.assertIsInstance(idx, Idx)
        self.assertEqual(idx, Idx([6, 1, 5]))

        # Unintended use
        self.assertEqual(Idx([6, 0]).prevpar(), -1)
        idx = Idx([6, 0])
        with self.assertRaises(ValueError):
            idx.prevpar(set=True)
        self.assertIsInstance(idx, Idx)
        self.assertEqual(idx, [6, 0])

    def test_level(self):
        self.assertEqual(NOIDX.level(), 0)
        self.assertEqual(Idx([1]).level(), 1)
        self.assertEqual(Idx([1, 5]).level(), 2)
        idx = Idx([1, 5, 1, 2, 5, 5, 1, 2])
        self.assertEqual(idx.level(), len(idx))


if __name__ == "__main__":
    unittest.main()
