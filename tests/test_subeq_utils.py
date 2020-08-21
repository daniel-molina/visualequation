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

from visualequation.subeqs import *
from visualequation.idx import *

class SubeqTests(unittest.TestCase):
    def test_latex(self):
        with self.assertRaises(IndexError):
            Subeq.subeq2latex(Subeq())
        with self.assertRaises(IndexError):
            Subeq().latex()
        self.assertEqual(Subeq.subeq2latex(Subeq(["a"])), "a")
        self.assertEqual(Subeq(["a"]).latex(), "a")

        self.assertEqual(Subeq([ops.PVOID]).latex(), ops.PVOID.latex_code)
        self.assertEqual(Subeq([ops.PJUXT, ["a"], ["b"]]).latex(), "a b")
        self.assertEqual(Subeq([ops.TJUXT, ["a"], ["b"]]).latex(), "a b")
        self.assertEqual(Subeq([ops.Op("", "\\frac{{{0}}}{{{1}}}", 2),
                                ["a"], ["b"]]).latex(), "\\frac{a}{b}")

    def test_call(self):
        s = Subeq([ops.GOP, ["dd"]])
        self.assertIsInstance(s(), Subeq)
        self.assertEqual(s(), [ops.GOP, ["dd"]])
        self.assertEqual(s([]), [ops.GOP, ["dd"]])
        self.assertEqual(s(Idx()), [ops.GOP, ["dd"]])
        self.assertEqual(s(Idx([])), [ops.GOP, ["dd"]])
        self.assertEqual(s(), s[:])

        self.assertNotEqual(s(0), [ops.GOP, ["dd"]])
        self.assertIsInstance(s(0), ops.Op)
        self.assertEqual(s(0), ops.GOP)
        self.assertIsInstance(s(1, 0), str)
        self.assertEqual(s(1, 0), "dd")
        self.assertEqual(s(1, 0, 0), "d")

        s = Subeq([ops.PJUXT, ["a"], ["b"]])
        self.assertIsInstance(s(1), Subeq)
        self.assertIsInstance(s(2), Subeq)
        self.assertEqual(s(1), s[1])
        self.assertEqual(s(2), s[2])

        self.assertEqual(s([1]), ["a"])
        self.assertEqual(s([2]), ["b"])

        self.assertEqual(s(Idx(1)), ["a"])
        self.assertEqual(s(Idx(2)), ["b"])

        self.assertEqual(s(Idx([1])), ["a"])
        self.assertEqual(s(Idx([2])), ["b"])

        s = Subeq([ops.GOP, [ops.PJUXT, ["a"], ["b"]]])
        self.assertEqual(s(1, 1), ["a"])
        self.assertEqual(s([1, 1]), ["a"])
        self.assertEqual(s(Idx(1, 1)), ["a"])
        self.assertEqual(s(Idx([1, 1])), ["a"])
        self.assertEqual(s(1, 1), s[1][1])

        with self.assertRaises(TypeError) as cm:
            s("1")
        self.assertEqual(cm.exception.args[0], IDX_TYPE_ERROR_MSG)
        with self.assertRaises(TypeError) as cm:
            s(3.4)
        self.assertEqual(cm.exception.args[0], IDX_TYPE_ERROR_MSG)
        with self.assertRaises(ValueError) as cm:
            s(-1)
        self.assertEqual(cm.exception.args[0], IDX_VALUE_ERROR_MSG)
        with self.assertRaises(IndexError):
            s(233)
        with self.assertRaises(IndexError):
            s(1, 321)
        with self.assertRaises(TypeError):
            s(0, 321)

    def test_supeq(self):
        self.assertEqual(Subeq(["d"]).supeq(None), -2)
        self.assertEqual(Subeq(["d"]).supeq([]), -2)
        self.assertEqual(Subeq(["d"]).supeq(Idx()), -2)
        self.assertEqual(Subeq(["d"]).supeq(NOIDX), -2)
        s = Subeq([ops.GOP, [ops.PJUXT, ["f"], [ops.TVOID]]])
        self.assertEqual(s.supeq([]), -2)
        self.assertIs(s.supeq(1), s)
        self.assertIs(s.supeq([1, 1]), s[1])
        self.assertIs(s.supeq([1, 2]), s[1])

        # Should it raise an error?
        self.assertEqual(Subeq().supeq(None), -2)
        s = Subeq()

        with self.assertRaises(IndexError) as cm:
            s.supeq(42)

        s = Subeq(["d"])
        with self.assertRaises(TypeError) as cm:
            s.supeq(0)
        self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)

        s = Subeq([ops.PVOID])
        with self.assertRaises(TypeError) as cm:
            s.supeq(0)
        self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)

        s = Subeq([ops.GOP, [ops.PJUXT, ["f"], [ops.TVOID]]])
        with self.assertRaises(TypeError) as cm:
            s.supeq([1, 1, 0])
        self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)


    def test_ispvoid(self):
        self.assertTrue(Subeq([ops.PVOID]).is_pvoid())
        self.assertFalse(Subeq([ops.TVOID]).is_pvoid())
        self.assertFalse(Subeq().is_pvoid())
        self.assertFalse(Subeq(["e"]).is_pvoid())
        self.assertFalse(Subeq(["e"]).is_pvoid(0))
        self.assertFalse(Subeq([ops.GOP, [ops.PVOID]]).is_pvoid())
        self.assertTrue(Subeq([ops.GOP, [ops.PVOID]]).is_pvoid(1))

    def test_istvoid(self):
        self.assertFalse(Subeq([ops.PVOID]).is_tvoid())
        self.assertTrue(Subeq([ops.TVOID]).is_tvoid())
        self.assertFalse(Subeq().is_tvoid())
        self.assertFalse(Subeq(["e"]).is_tvoid())
        self.assertFalse(Subeq([ops.GOP, [ops.TVOID]]).is_tvoid())
        self.assertTrue(Subeq([ops.GOP, [ops.TVOID]]).is_tvoid(1))

    def test_isvoid(self):
        self.assertTrue(Subeq([ops.PVOID]).is_void())
        self.assertTrue(Subeq([ops.TVOID]).is_void())
        self.assertFalse(Subeq().is_void())
        self.assertFalse(Subeq(["e"]).is_void())
        self.assertFalse(Subeq(["e"]).is_void(0))

    def test_isb(self):
        self.assertFalse(Subeq([ops.PVOID]).isb())
        self.assertFalse(Subeq([ops.TVOID]).isb())
        self.assertFalse(Subeq(["eeee"]).isb())
        self.assertTrue(Subeq([ops.PJUXT, ["d"], ["f"]]).isb())
        self.assertFalse(Subeq([ops.PJUXT, ["d"], ["f"]]).isb(0))
        self.assertFalse(Subeq([ops.PJUXT, ["d"], ["f"]]).isb(1))
        self.assertTrue(Subeq([ops.GOP, ["d"]]).isb())
        self.assertTrue(Subeq([ops.GOP, [ops.PJUXT, ["d"], ["f"]]]).isb())
        self.assertTrue(Subeq([ops.GOP, [ops.PJUXT, ["d"], ["f"]]]).isb(1))
        self.assertFalse(Subeq([ops.GOP,
                                [ops.PJUXT, ["d"], ["f"]]]).isb([1, 1]))

        # Unintended use
        self.assertFalse(Subeq([ops.PJUXT]).isb())
        self.assertFalse(Subeq([ops.PJUXT]).isb(0))
        self.assertFalse(Subeq(["eeee"]).isb(0))
        self.assertFalse(Subeq([ops.PVOID]).isb(0))
        self.assertFalse(Subeq().isb())

    def test_isusubeq(self):
        self.assertTrue(Subeq([ops.PVOID]).isusubeq())
        self.assertTrue(Subeq([ops.TVOID]).isusubeq())
        self.assertTrue(Subeq(["eeee"]).isusubeq())
        self.assertTrue(Subeq([ops.PJUXT, ["d"], ["f"]]).isusubeq())
        self.assertFalse(Subeq([ops.PJUXT, ["d"], ["f"]]).isusubeq(0))
        self.assertTrue(Subeq([ops.PJUXT, ["d"], ["f"]]).isusubeq(1))
        self.assertFalse(Subeq([ops.GOP, ["d"]]).isusubeq())
        self.assertFalse(Subeq([ops.GOP,
                                [ops.PJUXT, ["d"], ["f"]]]).isusubeq())
        self.assertTrue(Subeq([ops.GOP,
                               [ops.PJUXT, ["d"], ["f"]]]).isusubeq(1))
        self.assertTrue(Subeq([ops.GOP,
                                [ops.PJUXT, ["d"], ["f"]]]).isusubeq([1, 1]))

        self.assertFalse(Subeq([ops.PJUXT]).isusubeq(0))
        self.assertFalse(Subeq(["eeee"]).isusubeq(0))
        self.assertFalse(Subeq([ops.PVOID]).isusubeq(0))
        # Unintended use
        self.assertTrue(Subeq([ops.PJUXT]).isusubeq())
        with self.assertRaises(IndexError):
            Subeq().isusubeq()

    def test_is_perm_jb(self):
        self.assertFalse(Subeq([ops.PVOID]).is_perm_jb())
        self.assertFalse(Subeq([ops.TVOID]).is_perm_jb())
        self.assertFalse(Subeq(["eeee"]).is_perm_jb())
        self.assertTrue(Subeq([ops.PJUXT, ["d"], ["f"]]).is_perm_jb())
        self.assertFalse(Subeq([ops.PJUXT, ["d"], ["f"]]).is_perm_jb(0))
        self.assertFalse(Subeq([ops.PJUXT, ["d"], ["f"]]).is_perm_jb(1))
        self.assertFalse(Subeq([ops.GOP, ["d"]]).is_perm_jb())
        self.assertFalse(Subeq([ops.GOP,
                                [ops.PJUXT, ["d"], ["f"]]]).is_perm_jb())
        self.assertTrue(Subeq([ops.GOP,
                               [ops.PJUXT, ["d"], ["f"]]]).is_perm_jb(1))
        self.assertFalse(Subeq([ops.GOP,
                                [ops.PJUXT, ["d"], ["f"]]]).is_perm_jb([1, 1]))

        self.assertFalse(Subeq([ops.PJUXT]).is_perm_jb(0))
        self.assertFalse(Subeq(["eeee"]).is_perm_jb(0))
        self.assertFalse(Subeq([ops.PVOID]).is_perm_jb(0))
        with self.assertRaises(IndexError):
            Subeq().is_perm_jb()
        with self.assertRaises(IndexError):
            Subeq([ops.PVOID]).is_perm_jb(32)
        with self.assertRaises(IndexError):
            Subeq([ops.PVOID]).is_perm_jb([1, 43])

        # Unintended use
        self.assertTrue(Subeq([ops.PJUXT]).is_perm_jb())

    def test_is_juxted(self):
        self.assertFalse(Subeq(["d"]).is_juxted([]))
        self.assertFalse(Subeq([ops.PJUXT, ["d"], [ops.PVOID]]).is_juxted([]))
        self.assertFalse(Subeq([ops.PJUXT, ["d"], [ops.PVOID]]).is_juxted(0))
        self.assertTrue(Subeq([ops.PJUXT, ["d"], [ops.PVOID]]).is_juxted(1))
        self.assertTrue(Subeq([ops.PJUXT, ["d"], [ops.PVOID]]).is_juxted(2))
        self.assertFalse(Subeq([ops.GOP, ["d"]]).is_juxted([]))
        self.assertFalse(Subeq([ops.GOP, ["d"]]).is_juxted(1))
        s = Subeq([ops.PJUXT, ["3"], [ops.PJUXT, ["4"], ["2"]], [ops.TVOID]])
        self.assertFalse(s.is_juxted([]))
        self.assertFalse(s.is_juxted(0))
        self.assertTrue(s.is_juxted(1))
        self.assertTrue(s.is_juxted(2))
        self.assertTrue(s.is_juxted(3))
        self.assertFalse(s.is_juxted([2, 0]))
        self.assertTrue(s.is_juxted([2, 1]))
        self.assertTrue(s.is_juxted([2, 2]))

        with self.assertRaises(IndexError):
            s.is_juxted(4)
        with self.assertRaises(IndexError):
            s.is_juxted([2, 3])

    def test_is_gopb(self):
        self.assertFalse(Subeq(["d"]).is_gopb())
        self.assertFalse(Subeq(["d"]).is_gopb([]))
        self.assertFalse(Subeq([ops.PJUXT, ["d"], [ops.PVOID]]).is_gopb())
        self.assertFalse(Subeq([ops.PJUXT, ["d"], [ops.PVOID]]).is_gopb(0))
        self.assertFalse(Subeq([ops.PJUXT, ["d"], [ops.PVOID]]).is_gopb(1))
        self.assertFalse(Subeq([ops.PJUXT, ["d"], [ops.PVOID]]).is_gopb(2))
        self.assertTrue(Subeq([ops.GOP, ["d"]]).is_gopb())
        self.assertTrue(Subeq([ops.GOP, ["d"]]).is_gopb([]))
        self.assertFalse(Subeq([ops.GOP, ["d"]]).is_gopb(1))
        s = Subeq([ops.PJUXT, ["d"], [ops.GOP, ["d"]]])
        self.assertFalse(s.is_gopb())
        self.assertFalse(s.is_gopb(0))
        self.assertFalse(s.is_gopb(1))
        self.assertTrue(s.is_gopb(2))
        self.assertFalse(s.is_gopb([2, 1]))
        s = Subeq([ops.GOP, [ops.PJUXT, ["d"], [ops.GOP, ["d"]]]])
        self.assertTrue(s.is_gopb())
        self.assertFalse(s.is_gopb(0))
        self.assertFalse(s.is_gopb(1))
        self.assertFalse(s.is_gopb([1, 1]))
        self.assertTrue(s.is_gopb([1, 2]))
        self.assertFalse(s.is_gopb([1, 2, 0]))
        self.assertFalse(s.is_gopb([1, 2, 1]))

        with self.assertRaises(IndexError):
            s.is_gopb(89)
        with self.assertRaises(IndexError):
            s.is_gopb([1, 34])
        with self.assertRaises(IndexError):
            s.is_gopb([1, 2, 43])

    def test_is_goppar(self):
        self.assertFalse(Subeq(["d"]).is_goppar([]))
        self.assertFalse(Subeq([ops.PJUXT, ["d"], [ops.PVOID]]).is_goppar([]))
        self.assertFalse(Subeq([ops.PJUXT, ["d"], [ops.PVOID]]).is_goppar(0))
        self.assertFalse(Subeq([ops.PJUXT, ["d"], [ops.PVOID]]).is_goppar(1))
        self.assertFalse(Subeq([ops.PJUXT, ["d"], [ops.PVOID]]).is_goppar(2))
        self.assertFalse(Subeq([ops.GOP, ["d"]]).is_goppar([]))
        self.assertTrue(Subeq([ops.GOP, ["d"]]).is_goppar(1))
        s = Subeq([ops.PJUXT, ["d"], [ops.GOP, ["d"]]])
        self.assertFalse(s.is_goppar([]))
        self.assertFalse(s.is_goppar(0))
        self.assertFalse(s.is_goppar(1))
        self.assertFalse(s.is_goppar(2))
        self.assertTrue(s.is_goppar([2, 1]))
        s = Subeq([ops.GOP, [ops.PJUXT, ["d"], [ops.GOP, ["d"]]]])
        self.assertFalse(s.is_goppar([]))
        self.assertFalse(s.is_goppar(0))
        self.assertTrue(s.is_goppar(1))
        self.assertFalse(s.is_goppar([1, 1]))
        self.assertFalse(s.is_goppar([1, 2]))
        self.assertFalse(s.is_goppar([1, 2, 0]))
        self.assertTrue(s.is_goppar([1, 2, 1]))

        with self.assertRaises(IndexError):
            s.is_goppar(89)
        with self.assertRaises(IndexError):
            s.is_goppar([1, 34])
        with self.assertRaises(IndexError):
            s.is_goppar([1, 2, 43])

    def test_outlop(self):
        self.assertEqual(Subeq(["d"]).outlop([]), -2)
        self.assertEqual(Subeq(["d"]).outlop([], True), -2)
        self.assertEqual(Subeq([ops.PVOID]).outlop([]), -2)
        self.assertEqual(Subeq([ops.PVOID]).outlop([], True), -2)

        s = Subeq([ops.PJUXT, ["d"], [ops.PVOID]])
        self.assertEqual(s.outlop([]), -2)
        self.assertEqual(s.outlop([], True), -2)
        self.assertIs(s.outlop(1), s[0])
        self.assertEqual(s.outlop(1, True), Idx([0]))
        self.assertEqual(s.outlop(1, True), [0])
        self.assertIs(s.outlop(1), ops.PJUXT)
        self.assertIs(s.outlop(2), s[0])
        self.assertEqual(s.outlop(2, True), [0])

        s = Subeq([ops.GOP, [ops.PJUXT, ["d"], [ops.GOP, ["d"]]]])
        self.assertEqual(s.outlop([]), -2)
        self.assertEqual(s.outlop([], True), -2)
        self.assertIs(s.outlop(1), s[0])
        self.assertIs(s.outlop(1), ops.GOP)
        self.assertEqual(s.outlop(1, True), [0])
        self.assertIs(s.outlop([1, 1]), s(1, 0))
        self.assertIs(s.outlop([1, 1]), ops.PJUXT)
        self.assertEqual(s.outlop([1, 1], True), [1, 0])
        self.assertIs(s.outlop([1, 2]), s(1, 0))
        self.assertEqual(s.outlop([1, 2], True), [1, 0])
        self.assertIs(s.outlop([1, 2, 1]), s(1, 2, 0))
        self.assertIs(s.outlop([1, 2, 1]), ops.GOP)
        self.assertEqual(s.outlop([1, 2, 1], True), [1, 2, 0])

        for cond in (True, False):
            with self.assertRaises(IndexError):
                Subeq().outlop(0, cond)
            with self.assertRaises(TypeError) as cm:
                Subeq(["d"]).outlop(0, cond)
            self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)
            with self.assertRaises(TypeError) as cm:
                Subeq([ops.PVOID]).outlop(0, cond)
            self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)

            s = Subeq([ops.PJUXT, ["d"], [ops.PVOID]])
            with self.assertRaises(TypeError) as cm:
                s.outlop(0, cond)
            self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)
            with self.assertRaises(TypeError) as cm:
                s.outlop([1, 0], cond)
            self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)
            with self.assertRaises(TypeError) as cm:
                s.outlop([2, 0], cond)
            self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)

    def test_inlop(self):
        self.assertEqual(Subeq(["d"]).inlop(), -3)
        self.assertEqual(Subeq(["d"]).inlop(NOIDX, True), -3)
        self.assertEqual(Subeq([ops.PVOID]).inlop([]), -3)
        self.assertEqual(Subeq([ops.PVOID]).inlop(None, True), -3)

        s = Subeq([ops.PJUXT, ["d"], [ops.PVOID]])
        self.assertIs(s.inlop([]), ops.PJUXT)
        self.assertEqual(s.inlop([], True), Idx(0))
        self.assertEqual(s.inlop([], True), [0])
        self.assertEqual(s.inlop(1), -3)
        self.assertEqual(s.inlop(1, True), -3)
        self.assertEqual(s.inlop(1, True), -3)
        self.assertEqual(s.inlop(2), -3)
        self.assertEqual(s.inlop(2, True), -3)

        s = Subeq([ops.GOP, [ops.PJUXT, ["d"], [ops.GOP, ["d"]]]])
        self.assertIs(s.inlop(), ops.GOP)
        self.assertEqual(s.inlop([], True), Idx(0))
        self.assertIs(s.inlop(1), ops.PJUXT)
        self.assertEqual(s.inlop(1, True), [1, 0])
        self.assertIs(s.inlop([1, 1]), -3)
        self.assertEqual(s.inlop([1, 1], True), -3)
        self.assertIs(s.inlop([1, 2]), ops.GOP)
        self.assertEqual(s.inlop([1, 2], True), [1, 2, 0])
        self.assertIs(s.inlop([1, 2, 1]), -3)
        self.assertEqual(s.inlop([1, 2, 1], True), -3)

        for cond in (True, False):
            with self.assertRaises(ValueError) as cm:
                Subeq().inlop([], cond)
            self.assertEqual(cm.exception.args[0], EMPTY_SUBEQ_ERROR_MSG)
            with self.assertRaises(IndexError):
                Subeq().inlop(0, cond)
            with self.assertRaises(TypeError) as cm:
                Subeq(["d"]).inlop(0, cond)
            self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)
            with self.assertRaises(TypeError) as cm:
                Subeq([ops.PVOID]).inlop(0, cond)
            self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)

            s = Subeq([ops.PJUXT, ["d"], [ops.PVOID]])
            with self.assertRaises(TypeError) as cm:
                s.inlop(0, cond)
            self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)
            with self.assertRaises(TypeError) as cm:
                s.inlop([1, 0], cond)
            self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)
            with self.assertRaises(TypeError) as cm:
                s.inlop([2, 0], cond)
            self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)

if __name__ == "__main__":
    unittest.main()
