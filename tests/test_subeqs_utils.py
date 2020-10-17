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

OP = Op("O", "O")
ps = PseudoSymb("omega", r"\omega")


class SubeqTests(unittest.TestCase):
    def test_latex(self):
        with self.assertRaises(IndexError):
            Subeq.subeq2latex(Subeq())
        with self.assertRaises(IndexError):
            Subeq().latex()
        self.assertEqual(Subeq.subeq2latex(Subeq(["a"])), "a")
        self.assertEqual(Subeq(["a"]).latex(), "a")

        self.assertEqual(Subeq([PVOID]).latex(), PVOID._latex_code)
        self.assertEqual(Subeq([PJuxt(), ["a"], ["b"]]).latex(), "a b")
        self.assertEqual(Subeq([TJuxt(), ["a"], ["b"]]).latex(), "a b")
        self.assertEqual(Subeq([Op("", "\\frac{{{0}}}{{{1}}}", 2),
                                ["a"], ["b"]]).latex(), "\\frac{a}{b}")

    def test_call(self):
        s = Subeq([OP, ["dd"]])
        self.assertIsInstance(s(), Subeq)
        self.assertEqual(s(), [OP, ["dd"]])
        self.assertEqual(s([]), [OP, ["dd"]])
        self.assertEqual(s(Idx()), [OP, ["dd"]])
        self.assertEqual(s(Idx([])), [OP, ["dd"]])
        self.assertEqual(s(), s[:])

        self.assertNotEqual(s(0), [OP, ["dd"]])
        self.assertIsInstance(s(0), Op)
        self.assertEqual(s(0), OP)
        self.assertIsInstance(s(1, 0), str)
        self.assertEqual(s(1, 0), "dd")
        self.assertEqual(s(1, 0, 0), "d")

        s = Subeq([PJuxt(), ["a"], ["b"]])
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

        s = Subeq([OP, [PJuxt(), ["a"], ["b"]]])
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

    def test_isb(self):
        self.assertFalse(Subeq([PVOID]).isb())
        self.assertFalse(Subeq([ps]).isb())
        self.assertFalse(Subeq(["eeee"]).isb())
        self.assertTrue(Subeq([PJuxt(), ["d"], ["f"]]).isb())
        self.assertFalse(Subeq([PJuxt(), ["d"], ["f"]]).isb(0))
        self.assertFalse(Subeq([PJuxt(), ["d"], ["f"]]).isb(1))
        self.assertTrue(Subeq([OP, ["d"]]).isb())
        self.assertTrue(Subeq([OP, [PJuxt(), ["d"], ["f"]]]).isb())
        self.assertTrue(Subeq([OP, [PJuxt(), ["d"], ["f"]]]).isb(1))
        self.assertFalse(Subeq([OP,
                                [PJuxt(), ["d"], ["f"]]]).isb([1, 1]))

        # Unintended use
        self.assertFalse(Subeq([PJuxt()]).isb())
        self.assertFalse(Subeq([PJuxt()]).isb(0))
        self.assertFalse(Subeq(["eeee"]).isb(0))
        self.assertFalse(Subeq([PVOID]).isb(0))
        self.assertFalse(Subeq().isb())

    def test_supeq(self):
        self.assertEqual(Subeq(["d"]).supeq(None), -2)
        self.assertEqual(Subeq(["d"]).supeq([]), -2)
        self.assertEqual(Subeq(["d"]).supeq(Idx()), -2)
        s = Subeq([OP, [PJuxt(), ["f"], [ps]]])
        self.assertEqual(s.supeq([]), -2)
        self.assertIs(s.supeq(1), s)
        self.assertIs(s.supeq([1, 1]), s[1])
        self.assertIs(s.supeq([1, 2]), s[1])

        # Should it raise an error?
        self.assertEqual(Subeq().supeq(None), -2)
        s = Subeq()

        with self.assertRaises(IndexError):
            s.supeq(42)

        s = Subeq(["d"])
        with self.assertRaises(TypeError) as cm:
            s.supeq(0)
        self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)

        s = Subeq([PVOID])
        with self.assertRaises(TypeError) as cm:
            s.supeq(0)
        self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)

        s = Subeq([OP, [PJuxt(), ["f"], [ps]]])
        with self.assertRaises(TypeError) as cm:
            s.supeq([1, 1, 0])
        self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)

    def test_ispvoid(self):
        self.assertTrue(Subeq([PVOID]).is_pvoid())
        self.assertFalse(Subeq([ps]).is_pvoid())
        self.assertFalse(Subeq().is_pvoid())
        self.assertFalse(Subeq(["e"]).is_pvoid())
        self.assertFalse(Subeq(["e"]).is_pvoid(0))
        self.assertFalse(Subeq([OP, [PVOID]]).is_pvoid())
        self.assertTrue(Subeq([OP, [PVOID]]).is_pvoid(1))

    def test_allpvoid(self):
        self.assertEqual(Subeq([ps]).all_pvoid(), -1)
        self.assertEqual(Subeq([PVOID]).all_pvoid(), -1)
        self.assertEqual(Subeq(["eeee"]).all_pvoid(), -1)
        with self.assertRaises(TypeError):
            Subeq(["eeee"]).all_pvoid(0)
        self.assertEqual(Subeq([PJuxt(), ["d"], ["f"]]).all_pvoid(), False)
        self.assertEqual(Subeq([PJuxt(), ["d"], ["f"]]).all_pvoid(1), -1)
        self.assertEqual(Subeq([PJuxt(), ["d"], ["f"]]).all_pvoid(2), -1)

        self.assertEqual(Subeq([OP, [PVOID]]).all_pvoid(), True)
        self.assertEqual(Subeq([Op("O", "O", 2), [PVOID], ["d"]]).all_pvoid(),
                         False)
        self.assertEqual(
            Subeq([Op("O", "O", 2), [PVOID], [PVOID]]).all_pvoid(), True)
        self.assertEqual(
            Subeq([Op("O", "O", 3), [PVOID], ["d"], [PVOID]]).all_pvoid(),
                         False)
        self.assertEqual(
            Subeq([Op("O", "O", 3), [PVOID], ["d"], ["g"]]).all_pvoid(),
                         False)
        self.assertEqual(
            Subeq([Op("O", "O", 3), [PVOID], [PVOID], [PVOID]]).all_pvoid(),
                         True)

        # Unintended
        self.assertEqual(Subeq([PJuxt(), [PVOID], [PVOID]]).all_pvoid(), True)
        self.assertTrue(Subeq([PJuxt(), [PVOID], [PVOID]]).all_pvoid(1), -1)

    def test_isusubeq(self):
        self.assertTrue(Subeq([PVOID]).isusubeq())
        self.assertTrue(Subeq([ps]).isusubeq())
        self.assertTrue(Subeq(["eeee"]).isusubeq())
        self.assertFalse(Subeq(["eeee"]).isusubeq(0))
        self.assertFalse(Subeq([PJuxt(), ["d"], ["f"]]).isusubeq())
        self.assertFalse(Subeq([PJuxt(), ["d"], ["f"]]).isusubeq(0))
        self.assertTrue(Subeq([PJuxt(), ["d"], ["f"]]).isusubeq(1))
        self.assertTrue(Subeq([OP, ["d"]]).isusubeq())
        self.assertTrue(Subeq([OP,
                                [PJuxt(), ["d"], ["f"]]]).isusubeq())
        self.assertFalse(Subeq([OP,
                               [PJuxt(), ["d"], ["f"]]]).isusubeq(1))
        self.assertTrue(Subeq([OP,
                               [PJuxt(), ["d"], ["f"]]]).isusubeq([1, 1]))

        self.assertFalse(Subeq([PJuxt()]).isusubeq(0))
        self.assertFalse(Subeq(["eeee"]).isusubeq(0))
        self.assertFalse(Subeq([PVOID]).isusubeq(0))
        # Unintended use
        self.assertFalse(Subeq([PJuxt()]).isusubeq())
        with self.assertRaises(IndexError):
            Subeq().isusubeq()

    def test_is_perm_jb(self):
        self.assertFalse(Subeq([PVOID]).is_perm_jb())
        self.assertFalse(Subeq([ps]).is_perm_jb())
        self.assertFalse(Subeq(["eeee"]).is_perm_jb())
        self.assertTrue(Subeq([PJuxt(), ["d"], ["f"]]).is_perm_jb())
        self.assertFalse(Subeq([TJuxt(), ["d"], ["f"]]).is_perm_jb())
        self.assertFalse(Subeq([PJuxt(), ["d"], ["f"]]).is_perm_jb(0))
        self.assertFalse(Subeq([PJuxt(), ["d"], ["f"]]).is_perm_jb(1))
        self.assertFalse(Subeq([TJuxt(), ["d"], ["f"]]).is_perm_jb(1))
        self.assertFalse(Subeq([OP, ["d"]]).is_perm_jb())
        self.assertFalse(Subeq([OP,
                                [PJuxt(), ["d"], ["f"]]]).is_perm_jb())
        self.assertTrue(Subeq([OP,
                               [PJuxt(), ["d"], ["f"]]]).is_perm_jb(1))
        self.assertFalse(Subeq([OP,
                                [PJuxt(), ["d"], ["f"]]]).is_perm_jb([1, 1]))

        self.assertFalse(Subeq([PJuxt()]).is_perm_jb(0))
        self.assertFalse(Subeq(["eeee"]).is_perm_jb(0))
        self.assertFalse(Subeq([PVOID]).is_perm_jb(0))
        with self.assertRaises(IndexError):
            Subeq().is_perm_jb()
        with self.assertRaises(IndexError):
            Subeq([PVOID]).is_perm_jb(32)
        with self.assertRaises(IndexError):
            Subeq([PVOID]).is_perm_jb([1, 43])

        # Unintended use
        self.assertTrue(Subeq([PJuxt()]).is_perm_jb())

    def test_is_temp_jb(self):
        self.assertFalse(Subeq([PVOID]).is_temp_jb())
        self.assertFalse(Subeq([ps]).is_temp_jb())
        self.assertFalse(Subeq(["eeee"]).is_temp_jb())
        self.assertTrue(Subeq([TJuxt(), ["d"], ["f"]]).is_temp_jb())
        self.assertFalse(Subeq([PJuxt(), ["d"], ["f"]]).is_temp_jb())
        self.assertFalse(Subeq([TJuxt(), ["d"], ["f"]]).is_temp_jb(0))
        self.assertFalse(Subeq([TJuxt(), ["d"], ["f"]]).is_temp_jb(1))
        self.assertFalse(Subeq([PJuxt(), ["d"], ["f"]]).is_temp_jb(1))
        self.assertFalse(Subeq([OP, ["d"]]).is_temp_jb())
        self.assertFalse(Subeq([OP,
                                [TJuxt(), ["d"], ["f"]]]).is_temp_jb())
        self.assertTrue(Subeq([OP,
                               [TJuxt(), ["d"], ["f"]]]).is_temp_jb(1))
        self.assertFalse(Subeq([OP,
                                [TJuxt(), ["d"], ["f"]]]).is_temp_jb([1, 1]))

        self.assertFalse(Subeq([TJuxt()]).is_temp_jb(0))
        self.assertFalse(Subeq(["eeee"]).is_temp_jb(0))
        self.assertFalse(Subeq([PVOID]).is_temp_jb(0))
        with self.assertRaises(IndexError):
            Subeq().is_temp_jb()
        with self.assertRaises(IndexError):
            Subeq([PVOID]).is_temp_jb(32)
        with self.assertRaises(IndexError):
            Subeq([PVOID]).is_temp_jb([1, 43])

        # Unintended use
        self.assertTrue(Subeq([TJuxt()]).is_temp_jb())

    def test_is_jb(self):
        self.assertFalse(Subeq([PVOID]).is_jb())
        self.assertFalse(Subeq([ps]).is_jb())
        self.assertFalse(Subeq(["eeee"]).is_jb())
        self.assertTrue(Subeq([TJuxt(), ["d"], ["f"]]).is_jb())
        self.assertTrue(Subeq([PJuxt(), ["d"], ["f"]]).is_jb())
        self.assertFalse(Subeq([TJuxt(), ["d"], ["f"]]).is_jb(0))
        self.assertFalse(Subeq([TJuxt(), ["d"], ["f"]]).is_jb(1))
        self.assertFalse(Subeq([PJuxt(), ["d"], ["f"]]).is_jb(1))
        self.assertFalse(Subeq([OP, ["d"]]).is_jb())
        self.assertFalse(Subeq([OP,
                                [TJuxt(), ["d"], ["f"]]]).is_jb())
        self.assertTrue(Subeq([OP,
                               [TJuxt(), ["d"], ["f"]]]).is_jb(1))
        self.assertFalse(Subeq([OP,
                                [TJuxt(), ["d"], ["f"]]]).is_jb(
            [1, 1]))

        self.assertFalse(Subeq([TJuxt()]).is_jb(0))
        self.assertFalse(Subeq(["eeee"]).is_jb(0))
        self.assertFalse(Subeq([PVOID]).is_jb(0))
        with self.assertRaises(IndexError):
            Subeq().is_jb()
        with self.assertRaises(IndexError):
            Subeq([PVOID]).is_jb(32)
        with self.assertRaises(IndexError):
            Subeq([PVOID]).is_jb([1, 43])

        # Unintended use
        self.assertTrue(Subeq([TJuxt()]).is_jb())

    def test_is_juxted(self):
        self.assertFalse(Subeq(["d"]).is_juxted([]))
        self.assertFalse(Subeq([PJuxt(), ["d"], [PVOID]]).is_juxted([]))
        self.assertFalse(Subeq([PJuxt(), ["d"], [PVOID]]).is_juxted(0))
        self.assertTrue(Subeq([PJuxt(), ["d"], [PVOID]]).is_juxted(1))
        self.assertTrue(Subeq([PJuxt(), ["d"], [PVOID]]).is_juxted(2))
        self.assertFalse(Subeq([OP, ["d"]]).is_juxted([]))
        self.assertFalse(Subeq([OP, ["d"]]).is_juxted(1))
        s = Subeq([PJuxt(3), ["3"], [PJuxt(), ["4"], ["2"]], [ps]])
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

    def test_last_par_ord(self):
        self.assertEqual(Subeq(["s"]).last_par_ord(), -3)
        with self.assertRaises(TypeError):
            Subeq(["s"]).last_par_ord(0)
        s = Subeq([PJuxt(3), ["3"], [PJuxt(), ["4"], ["2"]], [ps]])
        self.assertEqual(s.last_par_ord(), 3)
        self.assertEqual(s.last_par_ord([]), 3)
        self.assertEqual(s.last_par_ord(1), -3)
        self.assertEqual(s.last_par_ord([1]), -3)
        self.assertEqual(s.last_par_ord(2), 2)
        with self.assertRaises(TypeError):
            s.last_par_ord([2, 0])
        self.assertEqual(s.last_par_ord([2, 1]), -3)
        self.assertEqual(s.last_par_ord([2, 2]), -3)
        self.assertEqual(s.last_par_ord(3), -3)
        self.assertEqual(s.last_par_ord([3]), -3)

    def test_is_lastpar(self):
        self.assertEqual(Subeq(["s"]).is_lastpar([]), False)
        with self.assertRaises(TypeError):
            Subeq(["s"]).is_lastpar(0)
        s = Subeq([PJuxt(3), ["3"], [PJuxt(), ["4"], ["2"]], [ps]])
        self.assertEqual(s.is_lastpar(None), False)
        self.assertEqual(s.is_lastpar([]), False)
        self.assertEqual(s.is_lastpar(1), False)
        self.assertEqual(s.is_lastpar([1]), False)
        self.assertEqual(s.is_lastpar(2), False)
        with self.assertRaises(TypeError):
            s.is_lastpar([2, 0])
        self.assertEqual(s.is_lastpar([2, 1]), False)
        self.assertEqual(s.is_lastpar([2, 2]), True)
        self.assertEqual(s.is_lastpar(3), True)
        self.assertEqual(s.is_lastpar([3]), True)

    def test_is_lastjuxted(self):
        self.assertEqual(Subeq(["s"]).is_lastjuxted([]), False)
        with self.assertRaises(TypeError):
            Subeq(["s"]).is_lastjuxted(0)
        s = Subeq([PJuxt(3), ["3"], [PJuxt(), ["4"], ["2"]], [ps]])
        self.assertEqual(s.is_lastjuxted(None), False)
        self.assertEqual(s.is_lastjuxted([]), False)
        self.assertEqual(s.is_lastjuxted(1), False)
        self.assertEqual(s.is_lastjuxted([1]), False)
        self.assertEqual(s.is_lastjuxted(2), False)
        with self.assertRaises(TypeError):
            s.is_lastjuxted([2, 0])
        self.assertEqual(s.is_lastjuxted([2, 1]), False)
        self.assertEqual(s.is_lastjuxted([2, 2]), True)
        self.assertEqual(s.is_lastjuxted(3), True)
        self.assertEqual(s.is_lastjuxted([3]), True)

        s = Subeq([PJuxt(3), ["3"], [Op("O", "O", 2), ["4"], ["2"]], [ps]])
        self.assertEqual(s.is_lastjuxted(None), False)
        self.assertEqual(s.is_lastjuxted([]), False)
        self.assertEqual(s.is_lastjuxted(1), False)
        self.assertEqual(s.is_lastjuxted([1]), False)
        self.assertEqual(s.is_lastjuxted(2), False)
        with self.assertRaises(TypeError):
            s.is_lastjuxted([2, 0])
        self.assertEqual(s.is_lastjuxted([2, 1]), False)
        self.assertEqual(s.is_lastjuxted([2, 2]), False)
        self.assertEqual(s.is_lastjuxted(3), True)
        self.assertEqual(s.is_lastjuxted([3]), True)

        s = Subeq([Op("O", "O", 3), ["3"], [PJuxt(2), ["4"], ["2"]], [ps]])
        self.assertEqual(s.is_lastjuxted(None), False)
        self.assertEqual(s.is_lastjuxted([]), False)
        self.assertEqual(s.is_lastjuxted(1), False)
        self.assertEqual(s.is_lastjuxted([1]), False)
        self.assertEqual(s.is_lastjuxted(2), False)
        with self.assertRaises(TypeError):
            s.is_lastjuxted([2, 0])
        self.assertEqual(s.is_lastjuxted([2, 1]), False)
        self.assertEqual(s.is_lastjuxted([2, 2]), True)
        self.assertEqual(s.is_lastjuxted(3), False)
        self.assertEqual(s.is_lastjuxted([3]), False)

    def test_is_nonlastjuxted(self):
        self.assertEqual(Subeq(["s"]).is_nonlastjuxted([]), False)
        with self.assertRaises(TypeError):
            Subeq(["s"]).is_nonlastjuxted(0)
        s = Subeq([PJuxt(3), ["3"], [PJuxt(), ["4"], ["2"]], [ps]])
        self.assertEqual(s.is_nonlastjuxted(None), False)
        self.assertEqual(s.is_nonlastjuxted([]), False)
        self.assertEqual(s.is_nonlastjuxted(1), True)
        self.assertEqual(s.is_nonlastjuxted([1]), True)
        self.assertEqual(s.is_nonlastjuxted(2), True)
        with self.assertRaises(TypeError):
            s.is_nonlastjuxted([2, 0])
        self.assertEqual(s.is_nonlastjuxted([2, 1]), True)
        self.assertEqual(s.is_nonlastjuxted([2, 2]), False)
        self.assertEqual(s.is_nonlastjuxted(3), False)
        self.assertEqual(s.is_nonlastjuxted([3]), False)

        s = Subeq([PJuxt(3), ["3"], [Op("O", "O", 2), ["4"], ["2"]], [ps]])
        self.assertEqual(s.is_nonlastjuxted(None), False)
        self.assertEqual(s.is_nonlastjuxted([]), False)
        self.assertEqual(s.is_nonlastjuxted(1), True)
        self.assertEqual(s.is_nonlastjuxted([1]), True)
        self.assertEqual(s.is_nonlastjuxted(2), True)
        with self.assertRaises(TypeError):
            s.is_nonlastjuxted([2, 0])
        self.assertEqual(s.is_nonlastjuxted([2, 1]), False)
        self.assertEqual(s.is_nonlastjuxted([2, 2]), False)
        self.assertEqual(s.is_nonlastjuxted(3), False)
        self.assertEqual(s.is_nonlastjuxted([3]), False)

        s = Subeq([Op("O", "O", 3), ["3"], [PJuxt(2), ["4"], ["2"]], [ps]])
        self.assertEqual(s.is_nonlastjuxted(None), False)
        self.assertEqual(s.is_nonlastjuxted([]), False)
        self.assertEqual(s.is_nonlastjuxted(1), False)
        self.assertEqual(s.is_nonlastjuxted([1]), False)
        self.assertEqual(s.is_nonlastjuxted(2), False)
        with self.assertRaises(TypeError):
            s.is_nonlastjuxted([2, 0])
        self.assertEqual(s.is_nonlastjuxted([2, 1]), True)
        self.assertEqual(s.is_nonlastjuxted([2, 2]), False)
        self.assertEqual(s.is_nonlastjuxted(3), False)
        self.assertEqual(s.is_nonlastjuxted([3]), False)

    def test_lopsup(self):
        self.assertEqual(Subeq(["d"]).lopsup([]), -2)
        self.assertEqual(Subeq(["d"]).lopsup([], True), -2)
        self.assertEqual(Subeq([PVOID]).lopsup([]), -2)
        self.assertEqual(Subeq([PVOID]).lopsup([], True), -2)

        s = Subeq([PJuxt(), ["d"], [ps]])
        self.assertEqual(s.lopsup([]), -2)
        self.assertEqual(s.lopsup([], True), -2)
        self.assertIs(s.lopsup(1), s[0])
        self.assertEqual(s.lopsup(1, True), Idx(0))
        self.assertEqual(s.lopsup(1, True), [0])
        self.assertEqual(s.lopsup(1), PJuxt())
        self.assertNotEqual(s.lopsup(1), PJuxt(3))
        self.assertNotEqual(s.lopsup(1), PJuxt(color=4))
        self.assertIs(s.lopsup(2), s[0])
        self.assertEqual(s.lopsup(2, True), [0])

        s = Subeq([OP, [PJuxt(), ["d"], [OP, ["d"]]]])
        self.assertEqual(s.lopsup([]), -2)
        self.assertEqual(s.lopsup([], True), -2)
        self.assertIs(s.lopsup(1), s[0])
        self.assertIs(s.lopsup(1), OP)
        self.assertEqual(s.lopsup(1, True), [0])
        self.assertIs(s.lopsup([1, 1]), s(1, 0))
        self.assertEqual(s.lopsup([1, 1]), PJuxt())
        self.assertEqual(s.lopsup([1, 1], True), [1, 0])
        self.assertIs(s.lopsup([1, 2]), s(1, 0))
        self.assertEqual(s.lopsup([1, 2], True), [1, 0])
        self.assertIs(s.lopsup([1, 2, 1]), s(1, 2, 0))
        self.assertIs(s.lopsup([1, 2, 1]), OP)
        self.assertEqual(s.lopsup([1, 2, 1], True), [1, 2, 0])

        for cond in (True, False):
            with self.assertRaises(IndexError):
                Subeq().lopsup(0, cond)
            with self.assertRaises(TypeError) as cm:
                Subeq(["d"]).lopsup(0, cond)
            self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)
            with self.assertRaises(TypeError) as cm:
                Subeq([PVOID]).lopsup(0, cond)
            self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)

            s = Subeq([PJuxt(), ["d"], [PVOID]])
            with self.assertRaises(TypeError) as cm:
                s.lopsup(0, cond)
            self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)
            with self.assertRaises(TypeError) as cm:
                s.lopsup([1, 0], cond)
            self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)
            with self.assertRaises(TypeError) as cm:
                s.lopsup([2, 0], cond)
            self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)

    def test_lop(self):
        self.assertEqual(Subeq(["d"]).lop(), -3)
        self.assertEqual(Subeq(["d"]).lop(Idx(), True), -3)
        self.assertEqual(Subeq([PVOID]).lop([]), -3)
        self.assertEqual(Subeq([PVOID]).lop(None, True), -3)

        s = Subeq([PJuxt(), ["d"], [PVOID]])
        self.assertEqual(s.lop([]), PJuxt())
        self.assertNotEqual(s.lop([]), PJuxt(4))
        self.assertNotEqual(s.lop([]), PJuxt(font=5))
        self.assertEqual(s.lop([], True), Idx(0))
        self.assertEqual(s.lop([], True), [0])
        self.assertEqual(s.lop(1), -3)
        self.assertEqual(s.lop(1, True), -3)
        self.assertEqual(s.lop(1, True), -3)
        self.assertEqual(s.lop(2), -3)
        self.assertEqual(s.lop(2, True), -3)

        s = Subeq([OP, [PJuxt(), ["d"], [OP, ["d"]]]])
        self.assertIs(s.lop(), OP)
        self.assertEqual(s.lop([], True), Idx(0))
        self.assertEqual(s.lop(1), PJuxt())
        self.assertEqual(s.lop(1, True), [1, 0])
        self.assertIs(s.lop([1, 1]), -3)
        self.assertEqual(s.lop([1, 1], True), -3)
        self.assertIs(s.lop([1, 2]), OP)
        self.assertEqual(s.lop([1, 2], True), [1, 2, 0])
        self.assertIs(s.lop([1, 2, 1]), -3)
        self.assertEqual(s.lop([1, 2, 1], True), -3)

        for cond in (True, False):
            with self.assertRaises(ValueError) as cm:
                Subeq().lop([], cond)
            self.assertEqual(cm.exception.args[0], EMPTY_SUBEQ_ERROR_MSG)
            with self.assertRaises(IndexError):
                Subeq().lop(0, cond)
            with self.assertRaises(TypeError) as cm:
                Subeq(["d"]).lop(0, cond)
            self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)
            with self.assertRaises(TypeError) as cm:
                Subeq([PVOID]).lop(0, cond)
            self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)

            s = Subeq([PJuxt(), ["d"], [PVOID]])
            with self.assertRaises(TypeError) as cm:
                s.lop(0, cond)
            self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)
            with self.assertRaises(TypeError) as cm:
                s.lop([1, 0], cond)
            self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)
            with self.assertRaises(TypeError) as cm:
                s.lop([2, 0], cond)
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

        s = Subeq([PJuxt(), ["a"], [OP, ["f"]], [ps]])
        for n in range(1, 4):
            for cond in (False, True):
                self.assertEqual(s.nthpar(), s[-1])
                self.assertIs(s.nthpar([], n), s[n])
                self.assertEqual(s.nthpar([], n, True), Idx([n]))
                self.assertEqual(s.nthpar([], -1), s[3])
                self.assertEqual(s.nthpar([], -1, True), Idx(3))
                self.assertEqual(s.nthpar([], 3 + n, cond), -1)
                with self.assertRaises(IndexError) as cm:
                    s.nthpar([], 0, cond)
                self.assertEqual(cm.exception.args[0],
                                 NON_EXISTENT_SUBEQ_ERROR_MSG)
                with self.assertRaises(IndexError) as cm:
                    s.nthpar([], -1 - n, cond)
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
                  Subeq([PJuxt(), ["d"], [ps]])):
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

        s = Subeq([PJuxt(), ["a"], [OP, ["f"]], [ps]])
        for n in range(0, 3):
            for cond in (False, True):
                self.assertEqual(s.relpar([], n, cond), -2)
                self.assertEqual(s.relpar([], -n, cond), -2)
                self.assertEqual(s.relpar([1], n), s[1 + n])
                self.assertEqual(s.relpar([1], n, True), Idx([1 + n]))
                self.assertEqual(s.relpar([2], -1), s[2 - 1])
                self.assertEqual(s.relpar([2], -1, True), Idx(2 - 1))
                self.assertEqual(s.relpar([2], +1), s[2 + 1])
                self.assertEqual(s.relpar([2], +1, True), Idx(2 + 1))
                self.assertEqual(s.relpar([3], n - 2), s[1 + n])
                self.assertEqual(s.relpar([3], n - 2, True), [1 + n])
                self.assertEqual(s.relpar([1], -1 - n, cond), -1)
                self.assertEqual(s.relpar([2], -2 - n, cond), -1)
                self.assertEqual(s.relpar([3], -3 - n, cond), -1)
                self.assertEqual(s.relpar([1], 3 + n, cond), -1)
                self.assertEqual(s.relpar([2], 2 + n, cond), -1)
                self.assertEqual(s.relpar([3], 1 + n, cond), -1)
                self.assertEqual(s.relpar([2, 1], 0), s(2, 1))
                self.assertEqual(s.relpar([2, 1], 0, True), [2, 1])
                self.assertEqual(s.relpar([2, 1], 1 + n, cond), -1)
                self.assertEqual(s.relpar([2, 1], -1 - n, cond), -1)
                with self.assertRaises(TypeError) as cm:
                    s.relpar([1, 0], n, cond)
                self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)
                with self.assertRaises(IndexError) :
                    s.relpar([80], n, cond)

    def test_ulevel_wholeeq(self):
        for s in (Subeq(["a"]), Subeq(None),
                  Subeq([PJuxt(), ["d"], [ps]]),
                  Subeq([PJuxt(),
                         [OP, [PJuxt(), ["3"], [ps]]], ["d"]]),
                  Subeq([PJuxt(), [Op("w", "w", 1), ["t"]],
                         [OP, [PJuxt(), ["3"], [ps]]]]),
                  Subeq([PJuxt(), ["d"], [Op("e", "e")],
                         [OP, [PJuxt(), ["3"], [ps]]]]),
                  Subeq([OP, [PJuxt(), ["a"], [ps]]]),
                  Subeq([OP, [Op("d", "d", 1), ["a"]]]),
                  Subeq([OP, [Op("f", "f", 3), ["a"],
                                   [ps], ["f"]]])):
            self.assertEqual(s.ulevel([]), 0)

    def test_ulevel_strict_subeq(self):
        for s in (Subeq(["a"]), Subeq(None), Subeq([ps])):
            with self.assertRaises(TypeError) as cm:
                s.ulevel([0])
            self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)
            with self.assertRaises(IndexError):
                s.ulevel([32])

        for pos, s in enumerate(
                (Subeq([PJuxt(), [OP, [PJuxt(), ["3"], [ps]]], ["d"]]),
                 Subeq([PJuxt(), [Op("w", "w", 1), ["t"]],
                        [OP, [PJuxt(), ["3"], [ps]]]]),
                 Subeq([PJuxt(), ["d"], [Op("e", "e")],
                        [OP, [PJuxt(), ["3"], [ps]]]]))):
            with self.assertRaises(TypeError) as cm:
                s.ulevel([0])
            self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)
            with self.assertRaises(IndexError):
                s.ulevel([32])

            self.assertEqual(s.ulevel(pos + 1), 0)
            self.assertEqual(s.ulevel([pos + 1, 1]), -1)
            self.assertEqual(s.ulevel([pos + 1, 1, 1]), +1)
            self.assertEqual(s.ulevel([pos + 1, 1, 2]), +1)

            for idx in ([pos+1, 0], [pos+1, 1, 0], [pos+1, 1, 1, 0]):
                with self.assertRaises(TypeError) as cm:
                    s.ulevel(idx)
                self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)

        for s in (Subeq([PJuxt(), [Op("O", "O", 2), ["a"], [ps]]]),
                  Subeq([PJuxt(), [Op("d", "d", 1), ["a"]]]),
                  Subeq([PJuxt(), [Op("f", "f", 3), ["a"],
                                   [ps], ["f"]]])):
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
                  Subeq([Op("O", "O", 2), ["d"], [ps]])):
            self.assertEqual(s.selectivity(), 1)
            with self.assertRaises(TypeError) as cm:
                s.selectivity(0)
            self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)
            with self.assertRaises(IndexError):
                s.selectivity(43)

        for pos, s in enumerate(
                (Subeq([PJuxt(),
                        [OP, [Op("O", "O", 2), ["3"], [ps]]], ["d"]]),
                 Subeq([PJuxt(), [Op("w", "w", 1), ["t"]],
                        [OP, [Op("O", "O", 2), ["3"], [ps]]]]),
                 Subeq([PJuxt(3), ["d"], [ps],
                        [OP, [Op("O", "O", 2), ["3"], [ps]]]]))):
            self.assertEqual(s.selectivity(), -1)
            self.assertEqual(s.selectivity(1 + pos), 0)
            self.assertEqual(s.selectivity([1 + pos, 1]), 1)
            self.assertEqual(s.selectivity([1 + pos, 1, 1]), 1)
            self.assertEqual(s.selectivity([1 + pos, 1, 2]), 1)

            for idx in ([pos+1, 0], [pos+1, 1, 0], [pos+1, 1, 1, 0]):
                with self.assertRaises(TypeError) as cm:
                    s.ulevel(idx)
                self.assertEqual(cm.exception.args[0], NOT_SUBEQ_ERROR_MSG)

    def test_mate_1symbol_eq(self):
        for s in (Subeq(["s"]), Subeq(None), Subeq([ps])):
            for right in (True, False):
                for uld in range(0, 4):
                    for retidx in (True, False):
                        self.assertEqual(s.mate([], right, uld, retidx), -1)
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

    def test_mate_juxtopjuxt(self):
        for pos, s in enumerate(
                (Subeq([Op("O", "O", 2),
                        [OP, [PJuxt(), ["3"], [ps]]], ["d"]]),
                 Subeq([Op("O", "O", 2), [Op("w", "w", 1), ["t"]],
                        [OP, [PJuxt(), ["3"], [ps]]]]),
                 Subeq([Op("O", "O", 3), ["d"], [Op("e", "e")],
                        [OP, [PJuxt(), ["3"], [ps]]]]))):
            for right in (True, False):
                for retidx in (True, False):
                    self.assertEqual(s.mate([], right, 0, retidx), -1)
                    for uld in (0, 4):
                        # 0-level subeqs
                        with self.assertRaises(ValueError) as cm:
                            s.mate([], right, 1 + uld, retidx)
                        self.assertEqual(cm.exception.args[0],
                                         NOT_AIDE_ERROR_MSG)

                        # Some 1-level subeqs
                        with self.assertRaises(ValueError) as cm:
                            s.mate([1 + pos, 1], right, uld, retidx)
                        self.assertEqual(cm.exception.args[0],
                                         NOT_USUBEQ_ERROR_MSG)

        s = Subeq([PJuxt(), [OP, [PJuxt(), ["3"], [ps]]], ["d"]])
        self.assertEqual(s.mate([2], True, 0), -1)
        self.assertEqual(s.mate([2], True, 0, True), -1)
        self.assertEqual(s.mate([2], False, 0), (s(1), 0))
        self.assertEqual(s.mate([2], False, 0, True), ([1], 0))

        self.assertEqual(s.mate([1, 1, 1], False, 0), -1)
        self.assertEqual(s.mate([1, 1, 1], False, 0, True), -1)
        self.assertEqual(s.mate([1, 1, 1], True, 0), (s(1, 1, 2), 0))
        self.assertEqual(s.mate([1, 1, 1], True, 0, True), ([1, 1, 2], 0))

        self.assertEqual(s.mate([1, 1, 2], False, 0), (s(1, 1, 1), 0))
        self.assertEqual(s.mate([1, 1, 2], False, 0, True), ([1, 1, 1], 0))
        self.assertEqual(s.mate([1, 1, 2], True, 0), (s[2], 1))
        self.assertEqual(s.mate([1, 1, 2], True, 0, True), ([2], 1))

    def test_mate_opjuxtopjuxt(self):
        for pos, s in enumerate(
                (Subeq([OP,
                        [PJuxt(), [OP, [PJuxt(), ["d"], [PVOID]]], ["h"]]]),
                 Subeq([OP,
                        [PJuxt(), ["h"], [OP, [PJuxt(), ["d"], [PVOID]]]]]))):
            for right in (True, False):
                for uld in (1, 4):
                    for retidx in (True, False):
                        # 0-level subeqs
                        with self.assertRaises(ValueError) as cm:
                            s.mate([], right, uld, retidx)
                        self.assertEqual(cm.exception.args[0],
                                         NOT_AIDE_ERROR_MSG)

                        # 1-level subeqs
                        with self.assertRaises(ValueError) as cm:
                            s.mate([1], right, uld, retidx)
                        self.assertEqual(cm.exception.args[0],
                                         NOT_USUBEQ_ERROR_MSG)

                        # 3-level subeqs
                        with self.assertRaises(ValueError) as cm:
                            s.mate([1, 1 + pos, 1], right, uld, retidx)
                        self.assertEqual(cm.exception.args[0],
                                         NOT_USUBEQ_ERROR_MSG)

    def test_mate_nojuxts(self):
        op2 = Op("O2", "O2", 2)
        op3 = Op("O3", "O3", 3)

        op_0 = op3
        op_2 = op3
        op_22 = op2
        op_3 = op2
        s = Subeq(
            [op_0, ["1"],
             [op_2, ["2-1"], [op_22, ["2-2-1"], ["2-2-2"]], ["2-3"]],
             [op_3, ["3-1"], ["3-2"]]])
        # 1-mates from the left
        self.assertEqual(s.mate(1, True), (s[2], 0))
        self.assertEqual(s.mate(2, True), (s[3], 0))
        self.assertEqual(s.mate(3, True), -1)
        self.assertEqual(s.mate(3, False), (s[2], 0))
        self.assertEqual(s.mate(2, False), (s[1], 0))
        self.assertEqual(s.mate(1, False), -1)
        # 2-mates from the right
        self.assertEqual(s.mate([3, 2], False), (s(3, 1), 0))
        self.assertEqual(s.mate([3, 1], False), (s(2, 3), 0))
        self.assertEqual(s.mate([2, 3], False), (s(2, 2), 0))
        self.assertEqual(s.mate([2, 2], False), (s(2, 1), 0))
        self.assertEqual(s.mate([2, 1], False), (s(1), 1))
        self.assertEqual(s.mate(1, False), -1)
        self.assertEqual(s.mate(1, True, 1), (s(2, 1), 0))
        self.assertEqual(s.mate([2, 1], True), (s(2, 2), 0))
        self.assertEqual(s.mate([2, 2], True), (s(2, 3), 0))
        self.assertEqual(s.mate([2, 3], True), (s(3, 1), 0))
        self.assertEqual(s.mate([3, 1], True), (s(3, 2), 0))
        self.assertEqual(s.mate([3, 2], True), -1)
        # 3-mates from the center
        self.assertEqual(s.mate([2, 2, 1], False), (s(2, 1), 1))
        self.assertEqual(s.mate([2, 1], False, 1), (s(1), 2))
        self.assertEqual(s.mate(1, False, 1), -1)
        self.assertEqual(s.mate([1], True, 2), (s(2, 1), 1))
        self.assertEqual(s.mate([2, 1], True, 1), (s(2, 2, 1), 0))
        self.assertEqual(s.mate([2, 2, 1], True, 0), (s(2, 2, 2), 0))
        self.assertEqual(s.mate([2, 2, 2], True, 0), (s(2, 3), 1))
        self.assertEqual(s.mate([2, 3], True, 1), (s(3, 1), 1))
        self.assertEqual(s.mate([3, 1], True, 1), (s(3, 2), 1))
        self.assertEqual(s.mate([3, 2], True, 1), -1)
        self.assertEqual(s.mate([3, 2], False, 1), (s(3, 1), 1))
        self.assertEqual(s.mate([3, 1], False, 1), (s(2, 3), 1))
        self.assertEqual(s.mate([2, 3], False, 1), (s(2, 2, 2), 0))
        self.assertEqual(s.mate([2, 2, 2], False, 0), (s(2, 2, 1), 0))

    def test_mate_1juxt(self):
        op2 = Op("O2", "O2", 2)
        op3 = Op("O3", "O3", 3)

        op_0 = op3
        op_2 = op3
        op_222 = op2
        op_3 = op2
        op_32 = op2
        s = Subeq(
            [op_0, ["1"],
             [op_2, ["2-1"],
              [PJuxt(), ["2-2-1"],
               [op_222, ["2-2-2-1"], ["2-2-2-2"]]],
              ["2-3"]],
             [op_3, ["3-1"],
              [op_32, ["3-2-1"], ["3-2-2"]]]])
        # 1-mates from the left
        self.assertEqual(s.mate(1, True), (s[2], 0))
        self.assertEqual(s.mate(2, True), (s[3], 0))
        self.assertEqual(s.mate(3, True), -1)
        self.assertEqual(s.mate(3, False), (s[2], 0))
        self.assertEqual(s.mate(2, False), (s[1], 0))
        self.assertEqual(s.mate(1, False), -1)
        # 2-mates from the right
        self.assertEqual(s.mate([3, 2], False), (s(3, 1), 0))
        self.assertEqual(s.mate([3, 1], False), (s(2, 3), 0))
        self.assertEqual(s.mate([2, 3], False), (s(2, 2, 2), 0))
        self.assertEqual(s.mate([2, 2, 2], False), (s(2, 2, 1), 0))
        self.assertEqual(s.mate([2, 2, 1], False), (s(2, 1), 0))
        self.assertEqual(s.mate([2, 1], False), (s(1), 1))
        self.assertEqual(s.mate(1, False), -1)

        self.assertEqual(s.mate(1, True, 1), (s(2, 1), 0))
        self.assertEqual(s.mate([2, 1], True), (s(2, 2, 1), 0))
        self.assertEqual(s.mate([2, 2, 1], True), (s(2, 2 ,2), 0))
        self.assertEqual(s.mate([2, 2, 2], True), (s(2, 3), 0))
        self.assertEqual(s.mate([2, 3], True), (s(3, 1), 0))
        self.assertEqual(s.mate([3, 1], True), (s(3, 2), 0))
        self.assertEqual(s.mate([3, 2], True), -1)
        # 3-mates from the right
        self.assertEqual(s.mate([3, 2, 2], False), (s(3, 2, 1), 0))
        self.assertEqual(s.mate([3, 2, 1], False), (s(3, 1), 1))
        self.assertEqual(s.mate([3, 1], False, 1), (s(2, 3), 1))
        self.assertEqual(s.mate([2, 3], False, 1), (s(2, 2, 2, 2), 0))
        self.assertEqual(s.mate([2, 2, 2, 2], False), (s(2, 2, 2, 1), 0))
        self.assertEqual(s.mate([2, 2, 2, 1], False), (s(2, 2, 1), 1))
        self.assertEqual(s.mate([2, 2, 1], False, 1), (s(2, 1), 1))
        self.assertEqual(s.mate([2, 1], False, 1), (s(1), 2))
        self.assertEqual(s.mate(1, False, 2), -1)

        self.assertEqual(s.mate(1, True, 2), (s(2, 1), 1))
        # ...

    def test_boundary_mate(self):
        for s in (Subeq(["s"]), Subeq(None), Subeq([ps])):
            for ul in range(0, 3):
                self.assertIs(s.boundary_mate(ul, last=False), s)
                self.assertEqual(
                    s.boundary_mate(ul, last=False, retindex=True), [])
                self.assertIs(s.boundary_mate(ul, last=True), s)
                self.assertEqual(
                    s.boundary_mate(ul, last=True, retindex=True), [])
                with self.assertRaises(ValueError) as cm:
                    s.boundary_mate(-1 - ul, last=False)
                self.assertEqual(cm.exception.args[0], NEGATIVE_UL_ERROR_MSG)
                with self.assertRaises(ValueError) as cm:
                    s.boundary_mate(-1 - ul, last=False, retindex=True)
                self.assertEqual(cm.exception.args[0], NEGATIVE_UL_ERROR_MSG)

        s = Subeq([PJuxt(), [OP, [PJuxt(), ["3"], [ps]]], ["d"]])
        self.assertIs(s.boundary_mate(0, last=False), s[1])
        self.assertIs(s.boundary_mate(0, last=True), s[2])
        self.assertIs(s.boundary_mate(1, last=False), s(1, 1, 1))
        self.assertIs(s.boundary_mate(1, last=True), s(2))
        self.assertIs(s.boundary_mate(2, last=False), s(1, 1, 1))
        self.assertIs(s.boundary_mate(2, last=True), s(2))

        self.assertEqual(s.boundary_mate(0, last=False, retindex=True), [1])
        self.assertEqual(s.boundary_mate(0, last=True, retindex=True), [2])
        self.assertEqual(s.boundary_mate(1, last=False, retindex=True),
                         [1, 1, 1])
        self.assertEqual(s.boundary_mate(1, last=True, retindex=True), [2])
        self.assertEqual(s.boundary_mate(2, last=False, retindex=True),
                         [1, 1, 1])
        self.assertEqual(s.boundary_mate(2, last=True, retindex=True), [2])

        s = Subeq([OP, [PJuxt(), ["3"], [ps]]])
        self.assertIs(s.boundary_mate(0, last=False), s)
        self.assertIs(s.boundary_mate(0, last=True), s)
        self.assertIs(s.boundary_mate(1, last=False), s(1, 1))
        self.assertIs(s.boundary_mate(1, last=True), s(1, 2))
        self.assertIs(s.boundary_mate(2, last=False), s(1, 1))
        self.assertIs(s.boundary_mate(2, last=True), s(1, 2))

        s = Subeq([PJuxt(), [Op("w", "w", 1), ["t"]], [OP, [PJuxt(), ["3"],
                                                           [ps]]]])
        self.assertIs(s.boundary_mate(0, last=False), s(1))
        self.assertIs(s.boundary_mate(0, last=True), s(2))
        self.assertIs(s.boundary_mate(1, last=False), s(1, 1))
        self.assertIs(s.boundary_mate(1, last=True), s(2, 1, 2))
        self.assertIs(s.boundary_mate(2, last=False), s(1, 1))
        self.assertIs(s.boundary_mate(2, last=True), s(2, 1, 2))
        self.assertIs(s.boundary_mate(3, last=False), s(1, 1))
        self.assertIs(s.boundary_mate(3, last=True), s(2, 1, 2))

        s = Subeq([PJuxt(3), ["d"], [Op("e", "e")], [OP, [PJuxt(), ["3"],
                                                            [ps]]]])
        self.assertIs(s.boundary_mate(0, last=False), s(1))
        self.assertIs(s.boundary_mate(0, last=True), s(3))
        self.assertIs(s.boundary_mate(1, last=False), s(1))
        self.assertIs(s.boundary_mate(1, last=True), s(3, 1, 2))
        self.assertIs(s.boundary_mate(2, last=False), s(1))
        self.assertIs(s.boundary_mate(2, last=True), s(3, 1, 2))

        s = Subeq([OP, [PJuxt(), [OP, [TJuxt(), ["d"], [PVOID]]], ["h"]]])
        self.assertIs(s.boundary_mate(0, last=False), s)
        self.assertIs(s.boundary_mate(0, last=True), s)
        self.assertIs(s.boundary_mate(1, last=False), s(1, 1))
        self.assertIs(s.boundary_mate(1, last=True), s(1, 2))
        self.assertIs(s.boundary_mate(2, last=False), s(1, 1, 1))
        self.assertIs(s.boundary_mate(2, last=True), s(1, 2))
        self.assertIs(s.boundary_mate(3, last=False), s(1, 1, 1, 1))
        self.assertIs(s.boundary_mate(3, last=True), s(1, 2))

    def test_boundary_symbol(self):
        for s in (Subeq(["s"]), Subeq(None), Subeq([ps])):
            for last in (True, False):
                self.assertIs(s.boundary_symbol(last), s)
                self.assertEqual(
                    s.boundary_symbol(last, retindex=True), [])

        s = Subeq([PJuxt(), [OP, [PJuxt(), ["3"], [ps]]], ["d"]])
        self.assertIs(s.boundary_symbol(last=False),
                      s(1, 1, 1))
        self.assertIs(s.boundary_symbol(last=True), s(2))
        self.assertEqual(s.boundary_symbol(last=False, retindex=True),
                         [1, 1, 1])
        self.assertEqual(s.boundary_symbol(last=True, retindex=True), [2])


if __name__ == "__main__":
    unittest.main()
