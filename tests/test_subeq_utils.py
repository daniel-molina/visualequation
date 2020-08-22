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

        self.assertEqual(Subeq([PVOID]).latex(), PVOID.latex_code)
        self.assertEqual(Subeq([PJUXT, ["a"], ["b"]]).latex(), "a b")
        self.assertEqual(Subeq([TJUXT, ["a"], ["b"]]).latex(), "a b")
        self.assertEqual(Subeq([Op("", "\\frac{{{0}}}{{{1}}}", 2),
                                ["a"], ["b"]]).latex(), "\\frac{a}{b}")

    def test_call(self):
        s = Subeq([GOP, ["dd"]])
        self.assertIsInstance(s(), Subeq)
        self.assertEqual(s(), [GOP, ["dd"]])
        self.assertEqual(s([]), [GOP, ["dd"]])
        self.assertEqual(s(Idx()), [GOP, ["dd"]])
        self.assertEqual(s(Idx([])), [GOP, ["dd"]])
        self.assertEqual(s(), s[:])

        self.assertNotEqual(s(0), [GOP, ["dd"]])
        self.assertIsInstance(s(0), Op)
        self.assertEqual(s(0), GOP)
        self.assertIsInstance(s(1, 0), str)
        self.assertEqual(s(1, 0), "dd")
        self.assertEqual(s(1, 0, 0), "d")

        s = Subeq([PJUXT, ["a"], ["b"]])
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

        s = Subeq([GOP, [PJUXT, ["a"], ["b"]]])
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
        s = Subeq([GOP, [PJUXT, ["f"], [TVOID]]])
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

        s = Subeq([PVOID])
        with self.assertRaises(TypeError) as cm:
            s.supeq(0)
        self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)

        s = Subeq([GOP, [PJUXT, ["f"], [TVOID]]])
        with self.assertRaises(TypeError) as cm:
            s.supeq([1, 1, 0])
        self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)


    def test_ispvoid(self):
        self.assertTrue(Subeq([PVOID]).is_pvoid())
        self.assertFalse(Subeq([TVOID]).is_pvoid())
        self.assertFalse(Subeq().is_pvoid())
        self.assertFalse(Subeq(["e"]).is_pvoid())
        self.assertFalse(Subeq(["e"]).is_pvoid(0))
        self.assertFalse(Subeq([GOP, [PVOID]]).is_pvoid())
        self.assertTrue(Subeq([GOP, [PVOID]]).is_pvoid(1))

    def test_istvoid(self):
        self.assertFalse(Subeq([PVOID]).is_tvoid())
        self.assertTrue(Subeq([TVOID]).is_tvoid())
        self.assertFalse(Subeq().is_tvoid())
        self.assertFalse(Subeq(["e"]).is_tvoid())
        self.assertFalse(Subeq([GOP, [TVOID]]).is_tvoid())
        self.assertTrue(Subeq([GOP, [TVOID]]).is_tvoid(1))

    def test_isvoid(self):
        self.assertTrue(Subeq([PVOID]).is_void())
        self.assertTrue(Subeq([TVOID]).is_void())
        self.assertFalse(Subeq().is_void())
        self.assertFalse(Subeq(["e"]).is_void())
        self.assertFalse(Subeq(["e"]).is_void(0))

    def test_isb(self):
        self.assertFalse(Subeq([PVOID]).isb())
        self.assertFalse(Subeq([TVOID]).isb())
        self.assertFalse(Subeq(["eeee"]).isb())
        self.assertTrue(Subeq([PJUXT, ["d"], ["f"]]).isb())
        self.assertFalse(Subeq([PJUXT, ["d"], ["f"]]).isb(0))
        self.assertFalse(Subeq([PJUXT, ["d"], ["f"]]).isb(1))
        self.assertTrue(Subeq([GOP, ["d"]]).isb())
        self.assertTrue(Subeq([GOP, [PJUXT, ["d"], ["f"]]]).isb())
        self.assertTrue(Subeq([GOP, [PJUXT, ["d"], ["f"]]]).isb(1))
        self.assertFalse(Subeq([GOP,
                                [PJUXT, ["d"], ["f"]]]).isb([1, 1]))

        # Unintended use
        self.assertFalse(Subeq([PJUXT]).isb())
        self.assertFalse(Subeq([PJUXT]).isb(0))
        self.assertFalse(Subeq(["eeee"]).isb(0))
        self.assertFalse(Subeq([PVOID]).isb(0))
        self.assertFalse(Subeq().isb())

    def test_isusubeq(self):
        self.assertTrue(Subeq([PVOID]).isusubeq())
        self.assertTrue(Subeq([TVOID]).isusubeq())
        self.assertTrue(Subeq(["eeee"]).isusubeq())
        self.assertTrue(Subeq([PJUXT, ["d"], ["f"]]).isusubeq())
        self.assertFalse(Subeq([PJUXT, ["d"], ["f"]]).isusubeq(0))
        self.assertTrue(Subeq([PJUXT, ["d"], ["f"]]).isusubeq(1))
        self.assertFalse(Subeq([GOP, ["d"]]).isusubeq())
        self.assertFalse(Subeq([GOP,
                                [PJUXT, ["d"], ["f"]]]).isusubeq())
        self.assertTrue(Subeq([GOP,
                               [PJUXT, ["d"], ["f"]]]).isusubeq(1))
        self.assertTrue(Subeq([GOP,
                                [PJUXT, ["d"], ["f"]]]).isusubeq([1, 1]))

        self.assertFalse(Subeq([PJUXT]).isusubeq(0))
        self.assertFalse(Subeq(["eeee"]).isusubeq(0))
        self.assertFalse(Subeq([PVOID]).isusubeq(0))
        # Unintended use
        self.assertTrue(Subeq([PJUXT]).isusubeq())
        with self.assertRaises(IndexError):
            Subeq().isusubeq()

    def test_is_perm_jb(self):
        self.assertFalse(Subeq([PVOID]).is_perm_jb())
        self.assertFalse(Subeq([TVOID]).is_perm_jb())
        self.assertFalse(Subeq(["eeee"]).is_perm_jb())
        self.assertTrue(Subeq([PJUXT, ["d"], ["f"]]).is_perm_jb())
        self.assertFalse(Subeq([PJUXT, ["d"], ["f"]]).is_perm_jb(0))
        self.assertFalse(Subeq([PJUXT, ["d"], ["f"]]).is_perm_jb(1))
        self.assertFalse(Subeq([GOP, ["d"]]).is_perm_jb())
        self.assertFalse(Subeq([GOP,
                                [PJUXT, ["d"], ["f"]]]).is_perm_jb())
        self.assertTrue(Subeq([GOP,
                               [PJUXT, ["d"], ["f"]]]).is_perm_jb(1))
        self.assertFalse(Subeq([GOP,
                                [PJUXT, ["d"], ["f"]]]).is_perm_jb([1, 1]))

        self.assertFalse(Subeq([PJUXT]).is_perm_jb(0))
        self.assertFalse(Subeq(["eeee"]).is_perm_jb(0))
        self.assertFalse(Subeq([PVOID]).is_perm_jb(0))
        with self.assertRaises(IndexError):
            Subeq().is_perm_jb()
        with self.assertRaises(IndexError):
            Subeq([PVOID]).is_perm_jb(32)
        with self.assertRaises(IndexError):
            Subeq([PVOID]).is_perm_jb([1, 43])

        # Unintended use
        self.assertTrue(Subeq([PJUXT]).is_perm_jb())

    def test_is_juxted(self):
        self.assertFalse(Subeq(["d"]).is_juxted([]))
        self.assertFalse(Subeq([PJUXT, ["d"], [PVOID]]).is_juxted([]))
        self.assertFalse(Subeq([PJUXT, ["d"], [PVOID]]).is_juxted(0))
        self.assertTrue(Subeq([PJUXT, ["d"], [PVOID]]).is_juxted(1))
        self.assertTrue(Subeq([PJUXT, ["d"], [PVOID]]).is_juxted(2))
        self.assertFalse(Subeq([GOP, ["d"]]).is_juxted([]))
        self.assertFalse(Subeq([GOP, ["d"]]).is_juxted(1))
        s = Subeq([PJUXT, ["3"], [PJUXT, ["4"], ["2"]], [TVOID]])
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
        self.assertFalse(Subeq([PJUXT, ["d"], [PVOID]]).is_gopb())
        self.assertFalse(Subeq([PJUXT, ["d"], [PVOID]]).is_gopb(0))
        self.assertFalse(Subeq([PJUXT, ["d"], [PVOID]]).is_gopb(1))
        self.assertFalse(Subeq([PJUXT, ["d"], [PVOID]]).is_gopb(2))
        self.assertTrue(Subeq([GOP, ["d"]]).is_gopb())
        self.assertTrue(Subeq([GOP, ["d"]]).is_gopb([]))
        self.assertFalse(Subeq([GOP, ["d"]]).is_gopb(1))
        s = Subeq([PJUXT, ["d"], [GOP, ["d"]]])
        self.assertFalse(s.is_gopb())
        self.assertFalse(s.is_gopb(0))
        self.assertFalse(s.is_gopb(1))
        self.assertTrue(s.is_gopb(2))
        self.assertFalse(s.is_gopb([2, 1]))
        s = Subeq([GOP, [PJUXT, ["d"], [GOP, ["d"]]]])
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
        self.assertFalse(Subeq([PJUXT, ["d"], [PVOID]]).is_goppar([]))
        self.assertFalse(Subeq([PJUXT, ["d"], [PVOID]]).is_goppar(0))
        self.assertFalse(Subeq([PJUXT, ["d"], [PVOID]]).is_goppar(1))
        self.assertFalse(Subeq([PJUXT, ["d"], [PVOID]]).is_goppar(2))
        self.assertFalse(Subeq([GOP, ["d"]]).is_goppar([]))
        self.assertTrue(Subeq([GOP, ["d"]]).is_goppar(1))
        s = Subeq([PJUXT, ["d"], [GOP, ["d"]]])
        self.assertFalse(s.is_goppar([]))
        self.assertFalse(s.is_goppar(0))
        self.assertFalse(s.is_goppar(1))
        self.assertFalse(s.is_goppar(2))
        self.assertTrue(s.is_goppar([2, 1]))
        s = Subeq([GOP, [PJUXT, ["d"], [GOP, ["d"]]]])
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
        self.assertEqual(Subeq([PVOID]).outlop([]), -2)
        self.assertEqual(Subeq([PVOID]).outlop([], True), -2)

        s = Subeq([PJUXT, ["d"], [PVOID]])
        self.assertEqual(s.outlop([]), -2)
        self.assertEqual(s.outlop([], True), -2)
        self.assertIs(s.outlop(1), s[0])
        self.assertEqual(s.outlop(1, True), Idx([0]))
        self.assertEqual(s.outlop(1, True), [0])
        self.assertIs(s.outlop(1), PJUXT)
        self.assertIs(s.outlop(2), s[0])
        self.assertEqual(s.outlop(2, True), [0])

        s = Subeq([GOP, [PJUXT, ["d"], [GOP, ["d"]]]])
        self.assertEqual(s.outlop([]), -2)
        self.assertEqual(s.outlop([], True), -2)
        self.assertIs(s.outlop(1), s[0])
        self.assertIs(s.outlop(1), GOP)
        self.assertEqual(s.outlop(1, True), [0])
        self.assertIs(s.outlop([1, 1]), s(1, 0))
        self.assertIs(s.outlop([1, 1]), PJUXT)
        self.assertEqual(s.outlop([1, 1], True), [1, 0])
        self.assertIs(s.outlop([1, 2]), s(1, 0))
        self.assertEqual(s.outlop([1, 2], True), [1, 0])
        self.assertIs(s.outlop([1, 2, 1]), s(1, 2, 0))
        self.assertIs(s.outlop([1, 2, 1]), GOP)
        self.assertEqual(s.outlop([1, 2, 1], True), [1, 2, 0])

        for cond in (True, False):
            with self.assertRaises(IndexError):
                Subeq().outlop(0, cond)
            with self.assertRaises(TypeError) as cm:
                Subeq(["d"]).outlop(0, cond)
            self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)
            with self.assertRaises(TypeError) as cm:
                Subeq([PVOID]).outlop(0, cond)
            self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)

            s = Subeq([PJUXT, ["d"], [PVOID]])
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
        self.assertEqual(Subeq([PVOID]).inlop([]), -3)
        self.assertEqual(Subeq([PVOID]).inlop(None, True), -3)

        s = Subeq([PJUXT, ["d"], [PVOID]])
        self.assertIs(s.inlop([]), PJUXT)
        self.assertEqual(s.inlop([], True), Idx(0))
        self.assertEqual(s.inlop([], True), [0])
        self.assertEqual(s.inlop(1), -3)
        self.assertEqual(s.inlop(1, True), -3)
        self.assertEqual(s.inlop(1, True), -3)
        self.assertEqual(s.inlop(2), -3)
        self.assertEqual(s.inlop(2, True), -3)

        s = Subeq([GOP, [PJUXT, ["d"], [GOP, ["d"]]]])
        self.assertIs(s.inlop(), GOP)
        self.assertEqual(s.inlop([], True), Idx(0))
        self.assertIs(s.inlop(1), PJUXT)
        self.assertEqual(s.inlop(1, True), [1, 0])
        self.assertIs(s.inlop([1, 1]), -3)
        self.assertEqual(s.inlop([1, 1], True), -3)
        self.assertIs(s.inlop([1, 2]), GOP)
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
                Subeq([PVOID]).inlop(0, cond)
            self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)

            s = Subeq([PJUXT, ["d"], [PVOID]])
            with self.assertRaises(TypeError) as cm:
                s.inlop(0, cond)
            self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)
            with self.assertRaises(TypeError) as cm:
                s.inlop([1, 0], cond)
            self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)
            with self.assertRaises(TypeError) as cm:
                s.inlop([2, 0], cond)
            self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)

    def test_nthpar(self):
        for s in (Subeq(["a"]), Subeq(None)):
            for n in range(-4, 4):
                for cond in (False, True):
                    self.assertEqual(s.nthpar(), -3)
                    self.assertEqual(s.nthpar([], n, cond), -3)
                    with self.assertRaises(TypeError) as cm:
                        s.nthpar([0], n, cond)
                    self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)
                    with self.assertRaises(IndexError):
                        s.nthpar([5], n, cond)
                    with self.assertRaises(ValueError) as cm:
                        s.nthpar([-5], n, cond)
                    self.assertEqual(cm.exception.args[0], IDX_VALUE_ERROR_MSG)

        s = Subeq([PJUXT, ["a"], [GOP, ["f"]], [TVOID]])
        for n in range(1, 4):
            for cond in (False, True):
                self.assertEqual(s.nthpar(), s[-1])
                self.assertIs(s.nthpar([], n), s[n])
                self.assertEqual(s.nthpar([], n, True), Idx([n]))
                self.assertEqual(s.nthpar([], -1), s[3])
                self.assertEqual(s.nthpar([], -1, True), Idx(3))
                self.assertEqual(s.nthpar([], 3+n, cond), -1)
                with self.assertRaises(IndexError) as cm:
                    s.nthpar([], 0, cond)
                self.assertEqual(cm.exception.args[0],
                                 NON_EXISTENT_SUBEQ_ERROR_MSG)
                with self.assertRaises(IndexError) as cm:
                    s.nthpar([], -1-n, cond)
                self.assertEqual(cm.exception.args[0],
                                 NON_EXISTENT_SUBEQ_ERROR_MSG)
                self.assertEqual(s.nthpar([2], 1), s([2, 1]))
                self.assertEqual(s.nthpar([2], -1), s(2, 1))
                self.assertEqual(s.nthpar([2], 1, True), [2, 1])
                self.assertEqual(s.nthpar([2], -1, True), Idx([2, 1]))
                with self.assertRaises(TypeError) as cm:
                    s.nthpar([1, 0], n, cond)
                self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)

    def test_relpar(self):
        for s in (Subeq(["a"]), Subeq(None),
                  Subeq([PJUXT, ["d"], [TVOID]])):
            for n in range(-4, 4):
                for cond in (False, True):
                    self.assertEqual(s.relpar([], n, cond), -2)
                    with self.assertRaises(TypeError) as cm:
                        s.relpar([0], n, cond)
                    self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)
                    with self.assertRaises(IndexError):
                        s.relpar([5], n, cond)
                    with self.assertRaises(ValueError) as cm:
                        s.relpar([-5], n, cond)
                    self.assertEqual(cm.exception.args[0], IDX_VALUE_ERROR_MSG)

        s = Subeq([PJUXT, ["a"], [GOP, ["f"]], [TVOID]])
        for n in range(0, 3):
            for cond in (False, True):
                self.assertEqual(s.relpar([], n, cond), -2)
                self.assertEqual(s.relpar([], -n, cond), -2)
                self.assertEqual(s.relpar([1], n), s[1+n])
                self.assertEqual(s.relpar([1], n, True), Idx([1+n]))
                self.assertEqual(s.relpar([2], -1), s[2-1])
                self.assertEqual(s.relpar([2], -1, True), Idx(2-1))
                self.assertEqual(s.relpar([2], +1), s[2+1])
                self.assertEqual(s.relpar([2], +1, True), Idx(2+1))
                self.assertEqual(s.relpar([3], n-2), s[1+n])
                self.assertEqual(s.relpar([3], n-2, True), [1+n])
                self.assertEqual(s.relpar([1], -1-n, cond), -1)
                self.assertEqual(s.relpar([2], -2-n, cond), -1)
                self.assertEqual(s.relpar([3], -3-n, cond), -1)
                self.assertEqual(s.relpar([1], 3+n, cond), -1)
                self.assertEqual(s.relpar([2], 2+n, cond), -1)
                self.assertEqual(s.relpar([3], 1+n, cond), -1)
                self.assertEqual(s.relpar([2, 1], 0), s(2, 1))
                self.assertEqual(s.relpar([2, 1], 0, True), [2, 1])
                self.assertEqual(s.relpar([2, 1], 1+n, cond), -1)
                self.assertEqual(s.relpar([2, 1], -1-n, cond), -1)
                with self.assertRaises(TypeError) as cm:
                    s.relpar([1, 0], n, cond)
                self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)
                with self.assertRaises(IndexError) :
                    s.relpar([80], n, cond)

    def test_urepr(self):
        for s in (Subeq(["a"]), Subeq(None),
                  Subeq([PJUXT, ["d"], [TVOID]])):
            self.assertIs(s.urepr(), s)
            self.assertEqual(s.urepr([], True), Idx())
            with self.assertRaises(TypeError) as cm:
                s.urepr(0)
            self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)
            with self.assertRaises(TypeError) as cm:
                s.urepr([0], True)
            self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)

        # Let us use valid gop-blocks in this test
        for s in (Subeq([GOP, [PJUXT, ["a"], [TVOID]]]),
                  Subeq([GOP, [Op("d", "d", 1), ["a"]]]),
                  Subeq([GOP, [Op("f", "f", 3), ["a"],
                                   [Op("e", "e", 0)], ["f"]]])):
            for cond in (False, True):
                self.assertIs(s.urepr(), s[1])
                self.assertEqual(s.urepr([], True), Idx(1))
                self.assertIs(s.urepr(1), s[1])
                self.assertEqual(s.urepr(1, True), [1])
                with self.assertRaises(TypeError) as cm:
                    s.urepr(0, cond)
                self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)
                with self.assertRaises(TypeError) as cm:
                    s.urepr([1, 0], cond)
                self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)

        for pos, s in enumerate(
                (Subeq([PJUXT,
                        [GOP, [PJUXT, ["3"], [TVOID]]], ["d"]]),
                 Subeq([PJUXT, [Op("w", "w", 1), ["t"]],
                        [GOP, [PJUXT, ["3"], [TVOID]]]]),
                 Subeq([PJUXT, ["d"], [Op("e", "e")],
                        [GOP, [PJUXT, ["3"], [TVOID]]]]))):
            self.assertIs(s.urepr(), s)
            self.assertEqual(s.urepr([], True), Idx())
            self.assertIs(s.urepr(1+pos), s(1+pos, 1))
            self.assertEqual(s.urepr(1+pos, True), [1+pos, 1])
            self.assertIs(s.urepr([1+pos, 1]), s(1+pos, 1))
            self.assertEqual(s.urepr([1+pos, 1], True), [1+pos, 1])

    def test_biggest_supeq_with_urepr(self):
        for s in (Subeq(["a"]), Subeq(None),
                  Subeq([PJUXT, ["d"], [TVOID]])):
            self.assertIs(s.biggest_supeq_with_urepr(), s)
            self.assertEqual(s.biggest_supeq_with_urepr([], True), Idx())
            with self.assertRaises(TypeError) as cm:
                s.biggest_supeq_with_urepr(0)
            self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)
            with self.assertRaises(TypeError) as cm:
                s.biggest_supeq_with_urepr([0], True)
            self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)

        # Let us use valid gop-blocks in this test
        for s in (Subeq([GOP, [PJUXT, ["a"], [TVOID]]]),
                  Subeq([GOP, [Op("d", "d", 1), ["a"]]]),
                  Subeq([GOP, [Op("f", "f", 3), ["a"],
                                   [Op("e", "e", 0)], ["f"]]])):
            for cond in (False, True):
                self.assertIs(s.biggest_supeq_with_urepr([], cond), -1)
                self.assertIs(s.biggest_supeq_with_urepr(1), s)
                self.assertEqual(s.biggest_supeq_with_urepr(1, True), NOIDX)
                with self.assertRaises(TypeError) as cm:
                    s.biggest_supeq_with_urepr(0, cond)
                self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)
                with self.assertRaises(TypeError) as cm:
                    s.biggest_supeq_with_urepr([1, 0], cond)
                self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)

        for pos, s in enumerate(
                (Subeq([PJUXT,
                        [GOP, [PJUXT, ["3"], [TVOID]]], ["d"]]),
                 Subeq([PJUXT, [Op("w", "w", 1), ["t"]],
                        [GOP, [PJUXT, ["3"], [TVOID]]]]),
                 Subeq([PJUXT, ["d"], [Op("e", "e")],
                        [GOP, [PJUXT, ["3"], [TVOID]]]]))):
            self.assertIs(s.biggest_supeq_with_urepr(), s)
            self.assertEqual(s.biggest_supeq_with_urepr([], True), Idx())
            self.assertIs(s.biggest_supeq_with_urepr(1+pos), -1)
            self.assertEqual(s.biggest_supeq_with_urepr(1+pos, True), -1)
            self.assertIs(s.biggest_supeq_with_urepr([1+pos, 1]), s[1+pos])
            self.assertEqual(s.biggest_supeq_with_urepr([1+pos, 1], True),
                             [1+pos])

    def test_ulevel(self):
        for s in (Subeq(["a"]), Subeq(None),
                  Subeq([PJUXT, ["d"], [TVOID]]),
                  Subeq([PJUXT,
                         [GOP, [PJUXT, ["3"], [TVOID]]], ["d"]]),
                  Subeq([PJUXT, [Op("w", "w", 1), ["t"]],
                         [GOP, [PJUXT, ["3"], [TVOID]]]]),
                  Subeq([PJUXT, ["d"], [Op("e", "e")],
                         [GOP, [PJUXT, ["3"], [TVOID]]]]),
                  Subeq([GOP, [PJUXT, ["a"], [TVOID]]]),
                  Subeq([GOP, [Op("d", "d", 1), ["a"]]]),
                  Subeq([GOP, [Op("f", "f", 3), ["a"],
                                   [Op("e", "e", 0)], ["f"]]])):
            self.assertEqual(s.ulevel([]), 0)

        for s in (Subeq(["a"]), Subeq(None), Subeq([Op("e", "e")])):
            with self.assertRaises(TypeError) as cm:
                s.ulevel([0])
            self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)
            with self.assertRaises(IndexError):
                s.ulevel([32])

        for pos, s in enumerate(
                (Subeq([PJUXT,
                        [GOP, [PJUXT, ["3"], [TVOID]]], ["d"]]),
                 Subeq([PJUXT, [Op("w", "w", 1), ["t"]],
                        [GOP, [PJUXT, ["3"], [TVOID]]]]),
                 Subeq([PJUXT, ["d"], [Op("e", "e")],
                        [GOP, [PJUXT, ["3"], [TVOID]]]]))):
            with self.assertRaises(TypeError) as cm:
                s.ulevel([0])
            self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)
            with self.assertRaises(IndexError):
                s.ulevel([32])

            self.assertEqual(s.ulevel(pos+1), -1)
            self.assertEqual(s.ulevel([pos+1, 1]), +1)
            self.assertEqual(s.ulevel([pos + 1, 1, 1]), +2)
            self.assertEqual(s.ulevel([pos + 1, 1, 2]), +2)

            for idx in ([pos+1, 0], [pos+1, 1, 0], [pos+1, 1, 1, 0]):
                with self.assertRaises(TypeError) as cm:
                    s.ulevel(idx)
                self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)


        for s in (Subeq([GOP, [PJUXT, ["a"], [TVOID]]]),
                  Subeq([GOP, [Op("d", "d", 1), ["a"]]]),
                  Subeq([GOP, [Op("f", "f", 3), ["a"],
                                   [Op("e", "e", 0)], ["f"]]])):
            self.assertEqual(s.ulevel([]), 0)
            self.assertEqual(s.ulevel(1), 0)
            self.assertEqual(s.ulevel([1, 1]), 1)

            for idx in ([0], [1, 0], [1, 1, 0]):
                with self.assertRaises(TypeError) as cm:
                    s.ulevel(idx)
                self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)
                with self.assertRaises(IndexError):
                    s.ulevel(idx[:-1] + [8])

    def test_selectivity(self):
        for s in (Subeq(["a"]), Subeq(None),
                  Subeq([PJUXT, ["d"], [TVOID]])):
            self.assertEqual(s.selectivity(), 2)
            with self.assertRaises(TypeError) as cm:
                s.selectivity(0)
            self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)
            with self.assertRaises(IndexError) as cm:
                s.selectivity(43)

        for pos, s in enumerate(
                (Subeq([PJUXT,
                        [GOP, [PJUXT, ["3"], [TVOID]]], ["d"]]),
                 Subeq([PJUXT, [Op("w", "w", 1), ["t"]],
                        [GOP, [PJUXT, ["3"], [TVOID]]]]),
                 Subeq([PJUXT, ["d"], [Op("e", "e")],
                        [GOP, [PJUXT, ["3"], [TVOID]]]]))):
            self.assertEqual(s.selectivity(), 2)
            self.assertEqual(s.selectivity(1 + pos), 0)
            self.assertEqual(s.selectivity([1 + pos, 1]), 1)
            self.assertEqual(s.selectivity([1 + pos, 1, 1]), -2)
            self.assertEqual(s.selectivity([1 + pos, 1, 2]), -2)

            for idx in ([pos+1, 0], [pos+1, 1, 0], [pos+1, 1, 1, 0]):
                with self.assertRaises(TypeError) as cm:
                    s.ulevel(idx)
                self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)

        for pos, s in enumerate(
                (Subeq([GOP, [PJUXT, [GOP, [TJUXT, ["d"], [PVOID]]], ["h"]]]),
                 Subeq([GOP,
                        [PJUXT, ["h"], [GOP, [TJUXT, ["d"], [PVOID]]]]]))):
            self.assertEqual(s.selectivity(), 0)
            self.assertEqual(s.selectivity(1), +1)
            self.assertEqual(s.selectivity([1, 1 + pos]), -1)
            # Mathematical trick to select the other one
            self.assertEqual(s.selectivity([1, 2 - pos]), -2)
            self.assertEqual(s.selectivity([1, 1 + pos, 1]), -2)
            self.assertEqual(s.selectivity([1, 1 + pos, 1, 1]), -2)
            self.assertEqual(s.selectivity([1, 1 + pos, 1, 2]), -2)

            for idx in ([1, 0], [1, 1+pos, 0], [1, 1+pos, 1, 0],
                        [1, 1+pos, 1, 1, 0], [1, 1+pos, 1, 2, 0]):
                with self.assertRaises(TypeError) as cm:
                    s.ulevel(idx)
                self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)

    def test_mate_1symbol_eq(self):
        for s in (Subeq(["s"]), Subeq(None), Subeq([Op("e", "e")])):
            for right in (True, False):
                for uld in range(0, 4):
                    for retidx in (True, False):
                        self.assertEqual(s.mate([], right, uld, retidx)[0], -1)
                for uld in range(-4, 0):
                    for retidx in (True, False):
                        with self.assertRaises(ValueError) as cm:
                            s.mate([], right, uld, retidx)
                        self.assertEqual(cm.exception.args[0],
                                         NEGATIVE_ULD_ERROR_MSG)
                        with self.assertRaises(ValueError) as cm:
                            s.mate([0], right, uld, retidx)
                        self.assertEqual(cm.exception.args[0],
                                         NEGATIVE_ULD_ERROR_MSG)
                for uld in range(0, 4):
                    for retidx in (True, False):
                        with self.assertRaises(TypeError) as cm:
                            s.mate([0], right, uld, retidx)
                        self.assertEqual(cm.exception.args[0],
                                         NOT_SUBEQ_ERROR_MSG)

    def test_mate_juxtgopjuxt(self):
        for pos, s in enumerate(
                (Subeq([PJUXT,
                        [GOP, [PJUXT, ["3"], [TVOID]]], ["d"]]),
                 Subeq([PJUXT, [Op("w", "w", 1), ["t"]],
                        [GOP, [PJUXT, ["3"], [TVOID]]]]),
                 Subeq([PJUXT, ["d"], [Op("e", "e")],
                        [GOP, [PJUXT, ["3"], [TVOID]]]]))):
            for right in (True, False):
                for uld in (0, 4):
                    for retidx in (True, False):
                        # 0-level subeqs
                        self.assertEqual(s.mate([], right, 0, retidx)[0], -1)
                        with self.assertRaises(ValueError) as cm:
                            s.mate([], right, 1+uld, retidx)
                        self.assertEqual(cm.exception.args[0],
                                         NOT_AIDE_ERROR_MSG)

                        # Some 1-level subeqs
                        with self.assertRaises(ValueError) as cm:
                            s.mate([1+pos], right, uld, retidx)
                        self.assertEqual(cm.exception.args[0],
                                         NOT_USUBEQ_ERROR_MSG)

                        # Some 3-level subeqs
                        with self.assertRaises(ValueError) as cm:
                            s.mate([1+pos, 1, 1], right, uld, retidx)
                        self.assertEqual(cm.exception.args[0],
                                         NOT_MATE_ERROR_MSG)
                        with self.assertRaises(ValueError) as cm:
                            s.mate([1+pos, 1, 2], right, uld, retidx)
                        self.assertEqual(cm.exception.args[0],
                                         NOT_MATE_ERROR_MSG)

        s = Subeq([PJUXT, [GOP, [PJUXT, ["3"], [TVOID]]], ["d"]])
        self.assertIs(s.mate([1, 1], False, 0)[0], -1)
        self.assertEqual(s.mate([1, 1], False, 0, True)[0], -1)
        self.assertIs(s.mate([1, 1], True, 0)[0], s[2])
        self.assertIs(s.mate([1, 1], True, 0)[1], 0)
        self.assertEqual(s.mate([1, 1], True, 0, True), ([2], 0))
        self.assertEqual(s.mate([2], False, 0), (s(1, 1), 0))
        self.assertEqual(s.mate([2], False, 0, True), (Idx(1, 1), 0))
        self.assertIs(s.mate([2], True, 0)[0], -1)
        self.assertIs(s.mate([2], True, 0, True)[0], -1)

    def test_mate_gopjuxtgopjuxt(self):
        for pos, s in enumerate(
                (Subeq([GOP, [PJUXT, [GOP, [TJUXT, ["d"], [PVOID]]], ["h"]]]),
                 Subeq([GOP,
                        [PJUXT, ["h"], [GOP, [TJUXT, ["d"], [PVOID]]]]]))):
            for right in (True, False):
                for uld in (0, 4):
                    for retidx in (True, False):
                        # 0-level subeqs
                        with self.assertRaises(ValueError) as cm:
                            s.mate([], right, uld, retidx)
                        self.assertEqual(cm.exception.args[0],
                                         NOT_USUBEQ_ERROR_MSG)

                        # 1-level subeqs
                        self.assertEqual(s.mate([1], right,
                                                uld, retidx)[0], -1)

                        # 2-level subeqs
                        with self.assertRaises(ValueError) as cm:
                            s.mate([1, 1+pos], right, uld, retidx)
                        self.assertEqual(cm.exception.args[0],
                                         NOT_USUBEQ_ERROR_MSG)
                        with self.assertRaises(ValueError) as cm:
                            s.mate([1, 2-pos], right, uld, retidx)
                        self.assertEqual(cm.exception.args[0],
                                         NOT_MATE_ERROR_MSG)

                        # 3-level subeqs
                        with self.assertRaises(ValueError) as cm:
                            s.mate([1, 1+pos, 1], right, uld, retidx)
                        self.assertEqual(cm.exception.args[0],
                                         NOT_MATE_ERROR_MSG)

                        # 4-level subeqs
                        with self.assertRaises(ValueError) as cm:
                            s.mate([1, 1+pos, 1, 1], right, uld, retidx)
                        self.assertEqual(cm.exception.args[0],
                                         NOT_MATE_ERROR_MSG)
                        with self.assertRaises(ValueError) as cm:
                            s.mate([1, 1+pos, 1, 2], right, uld, retidx)
                        self.assertEqual(cm.exception.args[0],
                                         NOT_MATE_ERROR_MSG)

    def test_mate_nogops(self):
        s = Subeq(
            [PJUXT, ["1"],
             [PJUXT, ["2-1"], [PJUXT, ["2-2-1"], ["2-2-2"]], ["2-3"]],
             [PJUXT, ["3-1"], ["3-2"]]])
        # 1-mates from the left
        self.assertEqual(s.mate(1, True), (s[2], 0))
        self.assertEqual(s.mate(2, True), (s[3], 0))
        self.assertEqual(s.mate(2, False), (s[1], 0))
        self.assertEqual(s.mate(3, False), (s[2], 0))
        # 2-mates from the right
        self.assertEqual(s.mate([3, 2], False), (s(3, 1), 0))
        self.assertEqual(s.mate([3, 1], False), (s(2, 3), 0))
        self.assertEqual(s.mate([2, 3], False), (s(2, 2), 0))
        self.assertEqual(s.mate([2, 2], False), (s(2, 1), 0))
        self.assertEqual(s.mate([2, 1], False), (s(1), 1))
        self.assertEqual(s.mate(1, True, 1), (s(2, 1), 0))
        self.assertEqual(s.mate([2, 1], True), (s(2, 2), 0))
        self.assertEqual(s.mate([2, 2], True), (s(2, 3), 0))
        self.assertEqual(s.mate([2, 3], True), (s(3, 1), 0))
        self.assertEqual(s.mate([3, 1], True), (s(3, 2), 0))
        # 3-mates from the center
        self.assertEqual(s.mate([2, 2, 1], False), (s(2, 1), 1))
        self.assertEqual(s.mate([2, 1], False, 1), (s(1), 2))
        self.assertEqual(s.mate([1], True, 2), (s(2, 1), 1))
        self.assertEqual(s.mate([2, 1], True, 1), (s(2, 2, 1), 0))
        self.assertEqual(s.mate([2, 2, 1], True, 0), (s(2, 2, 2), 0))
        self.assertEqual(s.mate([2, 2, 2], True, 0), (s(2, 3), 1))
        self.assertEqual(s.mate([2, 3], True, 1), (s(3, 1), 1))
        self.assertEqual(s.mate([3, 1], True, 1), (s(3, 2), 1))
        self.assertEqual(s.mate([3, 2], False, 1), (s(3, 1), 1))
        self.assertEqual(s.mate([3, 1], False, 1), (s(2, 3), 1))
        self.assertEqual(s.mate([2, 3], False, 1), (s(2, 2, 2), 0))
        self.assertEqual(s.mate([2, 2, 2], False, 0), (s(2, 2, 1), 0))

    def test_mate_1gop(self):
        s = Subeq(
            [PJUXT, ["1"],
             [PJUXT, ["2-1"],
              [GOP, [PJUXT, ["2-2-1-1"], ["2-2-1-2"]]], ["2-3"]],
             [PJUXT, ["3-1"], ["3-2"]]])
        # 1-mates from the left
        self.assertEqual(s.mate(1, True), (s[2], 0))
        self.assertEqual(s.mate(2, True), (s[3], 0))
        self.assertEqual(s.mate(2, False), (s[1], 0))
        self.assertEqual(s.mate(3, False), (s[2], 0))
        # 2-mates from the right
        self.assertEqual(s.mate([3, 2], False), (s(3, 1), 0))
        self.assertEqual(s.mate([3, 1], False), (s(2, 3), 0))
        self.assertEqual(s.mate([2, 3], False), (s(2, 2, 1), 0))
        self.assertEqual(s.mate([2, 2, 1], False), (s(2, 1), 0))
        self.assertEqual(s.mate([2, 1], False), (s(1), 1))
        self.assertEqual(s.mate(1, True, 1), (s(2, 1), 0))
        self.assertEqual(s.mate([2, 1], True), (s(2, 2, 1), 0))
        self.assertEqual(s.mate([2, 2, 1], True), (s(2, 3), 0))
        self.assertEqual(s.mate([2, 3], True), (s(3, 1), 0))
        self.assertEqual(s.mate([3, 1], True), (s(3, 2), 0))

if __name__ == "__main__":
    unittest.main()
