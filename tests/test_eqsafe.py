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
from visualequation.dirsel import Dir
from visualequation.idx import Idx
from visualequation.subeqs import Subeq
from visualequation.scriptops import *
from visualequation.eqsafe import EditableEq
from tests.test_utils import *


class SEq(EditableEq):
    """Dummy class to avoid debugging messages when testing."""
    def __init__(self, eq0=None, sel_index0=None, dir0=None):
        super().__init__(eq0, sel_index0, dir0, debug=False)


class SafeEqTests(unittest.TestCase):
    def test_repr(self):
        self.assertEqual(repr(SEq(["a"])), "UserEq(['a'], [], Dir.R, False)")
        self.assertEqual(repr(SEq([PJUXT, ["a"], ["b"]], [2], Dir.I)),
                         "UserEq([" + repr(PJUXT) +
                         ", ['a'], ['b']], [2], Dir.I, False)")

    def test_change_sel(self):
        def f(eq, new_index, current_index=-1):
            eq.idx = eq._change_sel(new_index, current_index)
            return eq

        db = (
            # Usual cases
            (f(SEq([PJUXT, ["a"], ["b"]], [1], Dir.O), [1]),
             SEq([PJUXT, ["a"], ["b"]], [1], Dir.O)),
            (f(SEq([PJUXT, ["a"], ["b"]], [1]), [2]),
             SEq([PJUXT, ["a"], ["b"]], [2])),
            (f(SEq([PJUXT, ["a"], [PJUXT, ["x"], ["y"]]], [2]), [1]),
             SEq([PJUXT, ["a"], [PJUXT, ["x"], ["y"]]], [1])),
            # TVOIDs
            (f(SEq([PJUXT, ["a"], ["b"], [TVOID]], [3], Dir.O), [3]),
             SEq([PJUXT, ["a"], ["b"], [TVOID]], [3], Dir.O)),
            (f(SEq([PJUXT, ["a"], ["b"], [TVOID]], [3], Dir.O), [2]),
             SEq([PJUXT, ["a"], ["b"]], [2], Dir.O)),
            (f(SEq([PJUXT, ["a"], ["b"], [TVOID]], [3], Dir.I), [1]),
             SEq([PJUXT, ["a"], ["b"]], [1], Dir.I)),
            (f(SEq([PJUXT, ["a"], [TVOID]], [2], Dir.I), [1]),
             SEq(["a"], [], Dir.I)),

            (f(SEq([RSUP, [PJUXT, PS_LO, [TVOID]], ["f"]], [1, 2], Dir.O),
               [1, 2]),
             SEq([RSUP, [PJUXT, PS_LO, [TVOID]], ["f"]], [1, 2], Dir.O)),
            (f(SEq([RSUP, [PJUXT, PS_LO, [TVOID]], ["f"]], [1, 2], Dir.O),
               [1, 1]),
             SEq([LORSUP, PS_LO, ["f"]], [1], Dir.O)),
            (f(SEq([RSUP, [PJUXT, PS_LO, [TVOID]], ["f"]], [1, 2], Dir.I),
               [2]),
             SEq([LORSUP, PS_LO, ["f"]], [2], Dir.I)),
            # TJUXTs
            (f(SEq([PJUXT, ["a"], [TJUXT, ["b"], ["c"]]], [2]), [2]),
             SEq([PJUXT, ["a"], [TJUXT, ["b"], ["c"]]], [2])),
            (f(SEq([PJUXT, ["a"], [TJUXT, ["b"], ["c"]]], [2]), [1]),
             SEq([PJUXT, ["a"], ["b"], ["c"]], [1])),
            (f(SEq([PJUXT, ["a"], [TJUXT, ["b"], ["c"]]], [2]), [2, 1]),
             SEq([PJUXT, ["a"], ["b"], ["c"]], [2])),
            (f(SEq([PJUXT, ["a"], [TJUXT, ["b"], ["c"]]], [2]), [2, 2]),
             SEq([PJUXT, ["a"], ["b"], ["c"]], [3])),
        )
        ce = CompareEqs(db)
        ce.assert_equality(inversely=True)

    def test_select_mate_wholeeq(self):
        def f(eq: EditableEq, right, pbc, n_in=1, n_out=0):
            retval = eq.move2mate(n_in, right)
            self.assertEqual(n_out, retval)
            return eq

        for s in (["a"], [PJUXT, ["v"], PS_LO], [SUBSUP, ["a"], ["b"], ["c"]]):
            for dir in (Dir.O, Dir.I, Dir.L, Dir.R):
                for n in range(0, 6):
                    db = (
                        (f(SEq(s, [], dir), True, True, n, 0),
                         SEq(s, [], dir)),
                        (f(SEq(s, [], dir), False, True, n, 0),
                         SEq(s, [], dir)),
                        (f(SEq(s, [], dir), True, False, n, abs(n)),
                         SEq(s, [], dir)),
                        (f(SEq(s, [], dir), False, False, n, abs(n)),
                         SEq(s, [], dir)),
                    )
                    ce = CompareEqs(db)
                    ce.assert_equality(inversely=True)


    def test_select_mate_strictsubeqs(self):
        #
        def rs(start, right, n_in):
            """Return final param ord and remaining steps if not pbc.

            It is assumed that there are 3 mates and some of them are possibly
            GOP-pars.

            *start* is the ordinal of the mate, from 1 to 3 (it is not a Idx
            nor list). If mate is a GOP-par, use the index of its supeq, the
            GOP-block.
            """
            n_mates = 3
            if n_in < 0:
                right = not right
                n_in = -n_in

            if right:
                max_n = n_mates - start
                aux = start + n_in
                return (aux, 0) if n_in <= max_n else (max_n, n_in - max_n)
            else:
                max_n = start - 1
                aux = start - n_in
                return (aux, 0) if n_in <= max_n else (1, n_in - max_n)

        def fidx(index, s):
            # It assumes that index list has only one element
            return index if s[index[0]][0] != GOP else index + [1]

        def f(eq, right, pbc, n_in=1, n_out=0):
            retval = eq.move2mate(right, pbc)
            self.assertEqual(n_out, retval)
            return eq

        for s in ([PJUXT, ["v"], PS_LO, ["h"]],
                  [SUBSUP, ["a"], ["b"], ["c"]],
                  [PJUXT, ["v"], [PJUXT, ["a"], PS_LO], PS_LO],
                  [SUBSUP, ["a"], [PJUXT, ["x"], ["y"]], ["c"]],
                  [SUBSUP, ["a"], [PJUXT, ["x"], ["y"]],
                   [GOP, [PJUXT, ["x"], ["y"]]]],
                  [SUBSUP, ["a"], [GOP, [PJUXT, ["x"], ["y"]]], ["c"]],
                  [SUBSUP, [GOP, [PJUXT, ["x"], ["y"]]], ["b"],
                   [PJUXT, ["x"], ["y"]]],
                  [SUBSUP, [GOP, [PJUXT, ["x"], ["y"]]], ["b"],
                   [GOP, [PJUXT, ["x"], ["y"]]]],
                  [SUBSUP, [GOP, [PJUXT, ["x"], ["y"]]],
                   [GOP, [PJUXT, ["x"], ["y"]]],
                   [GOP, [PJUXT, ["x"], ["y"]]]],
                  ):
            for n in range(0, 6):
                for i in (1, 2, 3):
                    for dir in (Dir.O, Dir.I, Dir.L, Dir.R):
                        db = (
                            # pbc == TRUE
                            (f(SEq(s, fidx([i], s), dir), True, True, n, 0),
                             SEq(s, fidx([(n + i - 1) % 3 + 1], s), dir)),
                            (f(SEq(s, fidx([i], s), dir), True, True, -n, 0),
                             SEq(s, fidx([(-n + i - 1) % 3 + 1], s), dir)),
                            (f(SEq(s, fidx([i], s), dir), False, True, n, 0),
                             SEq(s, fidx([(-n + i - 1) % 3 + 1], s), dir)),
                            (f(SEq(s, fidx([i], s), dir), False, True, -n, 0),
                             SEq(s, fidx([(n + i - 1) % 3 + 1], s), dir)),
                            # pbc == False
                            (f(SEq(s, fidx([i], s), dir), True, False, n,
                               rs(i, True, n)[1]),
                             SEq(s, fidx([rs(i, True, n)[0]], s), dir)),
                            (f(SEq(s, fidx([i], s), dir), True, False, -n,
                               rs(i, True, -n)[1]),
                             SEq(s, fidx([rs(i, True, -n)[0]], s), dir)),
                            (f(SEq(s, fidx([i], s), dir), False, False, n,
                               rs(i, False, n)[1]),
                             SEq(s, fidx([rs(i, False, n)[0]], s), dir)),
                            (f(SEq(s, fidx([i], s), dir), False, False, -n,
                               rs(i, False, -n)[1]),
                             SEq(s, fidx([rs(i, False, -n)[0]], s), dir)),
                        )
                    ce = CompareEqs(db)
                    ce.assert_equality(inversely=True)


    def test_select_mate_marginalsels(self):
        def f(eq, right, strict, n_in=1, n_out=0):
            retval = eq.move2mate(right, strict)
            self.assertEqual(n_out, retval)
            return eq

        # Empty eq
        for dir in (Dir.V, Dir.O, Dir.I):
            for n_in in range(1, 5):
                for right in (True, False):
                    db = (
                        (f(SEq([PVOID], [], dir), right, True, n_in, n_in),
                         SEq([PVOID], [], dir)),
                        (f(SEq([PVOID], [], dir), right, True, -n_in, n_in),
                         SEq([PVOID], [], dir)),
                        (f(SEq([PVOID], [], dir), right, False, n_in, 0),
                         SEq([PVOID], [], dir)),
                        (f(SEq([PVOID], [], dir), right, False, -n_in, 0),
                         SEq([PVOID], [], dir)),
                    )
                    ce = CompareEqs(db)
                    ce.assert_equality(inversely=True)

        # PVOIDs with possibly previous preference
        s = [SUBSUP, ["y"], [PVOID], ["z"]]
        for k in (1, -1):
            db = (
                # Go Dir.R
                (f(SEq(s, [1], Dir.R), k > 0, False, k * 2), SEq(s, [3], Dir.R)),
                (f(SEq(s, [1], Dir.L), k > 0, False, k * 3), SEq(s, [3], Dir.R)),
                (f(SEq(s, [1], Dir.R), k > 0, True, k * 2), SEq(s, [3], Dir.R)),
                (f(SEq(s, [1], Dir.L), k > 0, True, k * 2), SEq(s, [3], Dir.L)),
                (f(SEq(s, [1], Dir.O), k > 0, False, k * 2), SEq(s, [3], Dir.O)),
                (f(SEq(s, [1], Dir.O), k > 0, False, k * 2), SEq(s, [3], Dir.O)),
                (f(SEq(s, [1], Dir.I), k > 0, True, k * 2), SEq(s, [3], Dir.I)),
                (f(SEq(s, [1], Dir.I), k > 0, True, k * 2), SEq(s, [3], Dir.I)),
                # Go Dir.L
                (f(SEq(s, [3], Dir.L), k < 0, False, k * 2), SEq(s, [1], Dir.L)),
                (f(SEq(s, [3], Dir.R), k < 0, False, k * 3), SEq(s, [1], Dir.L)),
                (f(SEq(s, [3], Dir.L), k < 0, True, k * 2), SEq(s, [1], Dir.L)),
                (f(SEq(s, [3], Dir.R), k < 0, True, k * 2), SEq(s, [1], Dir.R)),
                (f(SEq(s, [3], Dir.O), k < 0, False, k * 2), SEq(s, [1], Dir.O)),
                (f(SEq(s, [3], Dir.O), k < 0, False, k * 2), SEq(s, [1], Dir.O)),
                (f(SEq(s, [3], Dir.I), k < 0, True, k * 2), SEq(s, [1], Dir.I)),
                (f(SEq(s, [3], Dir.I), k < 0, True, k * 2), SEq(s, [1], Dir.I)),

            )
        ce = CompareEqs(db)
        ce.assert_equality(inversely=True)

        s1 = [RSUP, [PVOID], ["y"]]
        s2 = [RSUP, ["y"], [PVOID]]
        for strict in (True, False):
            db = (
                # PVOIDs with no previous preference
                # Only positive n_in: behavior for negative values to be
                # decided yet when starting from PVOID in orimode
                (f(SEq(s1, [1], Dir.V), True, strict), SEq(s1, [2], Dir.R)),
                (f(SEq(s1, [2], Dir.L), False, strict), SEq(s1, [1], Dir.V)),
                (f(SEq(s1, [1], Dir.O), True, strict), SEq(s1, [2], Dir.O)),
                (f(SEq(s1, [2], Dir.O), False, strict), SEq(s1, [1], Dir.O)),
                (f(SEq(s1, [1], Dir.I), True, strict), SEq(s1, [2], Dir.I)),
                (f(SEq(s1, [2], Dir.I), False, strict), SEq(s1, [1], Dir.I)),

                (f(SEq(s2, [1], Dir.R), True, strict), SEq(s2, [2], Dir.V)),
                (f(SEq(s2, [2], Dir.V), False, strict), SEq(s2, [1], Dir.L)),
                (f(SEq(s2, [1], Dir.O), True, strict), SEq(s2, [2], Dir.O)),
                (f(SEq(s2, [2], Dir.O), False, strict), SEq(s2, [1], Dir.O)),
                (f(SEq(s2, [1], Dir.I), True, strict), SEq(s2, [2], Dir.I)),
                (f(SEq(s2, [2], Dir.I), False, strict), SEq(s2, [1], Dir.I)),
                # TVOIDs
                (f(SEq([PJUXT, ["a"], [TVOID]], [2], Dir.O), False, strict),
                 SEq(["a"], [], Dir.O)),
                (f(SEq([PJUXT, ["a"], [TVOID]], [2], Dir.I), False, strict),
                 SEq(["a"], [], Dir.I)),
                # TJUXTs
                (f(SEq([PJUXT, ["a"], [TJUXT, ["x"], ["y"]]], [2], Dir.O),
                   False, strict),
                 SEq([PJUXT, ["a"], ["x"], ["y"]], [1], Dir.O)),
                (f(SEq([PJUXT, ["a"], [TJUXT, ["x"], ["y"]]], [2], Dir.I),
                   False, strict),
                 SEq([PJUXT, ["a"], ["x"], ["y"]], [1], Dir.I)),
                (f(SEq([PJUXT, ["a"], [TJUXT, ["x"], ["y"]]], [2], Dir.L),
                   False, strict),
                 SEq([PJUXT, ["a"], ["x"], ["y"]], [1], Dir.L)),
                (f(SEq([PJUXT, ["a"], [TJUXT, ["x"], ["y"]]], [2], Dir.R),
                   False, strict=True),
                 SEq([PJUXT, ["a"], ["x"], ["y"]], [1], Dir.R)),
                (f(SEq([PJUXT, ["a"], [TJUXT, ["x"], ["y"]]], [2], Dir.R),
                   False, strict=False),
                 SEq([PJUXT, ["a"], [TJUXT, ["x"], ["y"]]], [2], Dir.L)),
            )
            ce = CompareEqs(db)
            ce.assert_equality(inversely=True)

    def test_select_pseudosymbol_eqissymbol(self):
        def f(eq: EditableEq, right, strict, n_in=1, n=0):
            retval = eq.select_pseudosymbol(right, strict, n_in)
            self.assertEqual(retval, n)
            return eq

        for right in (True, False):
            # n_in == 0
            for dir in (Dir.R, Dir.L, Dir.O, Dir.I):
                db = (
                    (f(SEq(["a"], [], dir), right, False, 0),
                     SEq(["a"], [], dir)),
                    (f(SEq(["a"], [], dir), right, True, 0),
                     SEq(["a"], [], dir)),
                )
                ce = CompareEqs(db)
                ce.assert_equality(inversely=True)
            for n_in in range(1, 5):
                # strict == False
                db = (
                    (f(SEq(["a"], [], Dir.R), right, False, n_in, 0),
                     SEq(["a"], [], Dir.R if right else Dir.L)),
                    (f(SEq(["a"], [], Dir.R), right, False, -n_in, 0),
                     SEq(["a"], [], Dir.L if right else Dir.R)),
                    (f(SEq(["a"], [], Dir.L), right, False, n_in, 0),
                     SEq(["a"], [], Dir.R if right else Dir.L)),
                    (f(SEq(["a"], [], Dir.L), right, False, -n_in, 0),
                     SEq(["a"], [], Dir.L if right else Dir.R)),
                    (f(SEq(["a"], [], Dir.O), right, False, n_in, 0),
                     SEq(["a"], [], Dir.O)),
                    (f(SEq(["a"], [], Dir.O), right, False, -n_in, 0),
                     SEq(["a"], [], Dir.O)),
                    (f(SEq(["a"], [], Dir.I), right, False, n_in, 0),
                     SEq(["a"], [], Dir.I)),
                    (f(SEq(["a"], [], Dir.I), right, False, -n_in, 0),
                     SEq(["a"], [], Dir.I)),
                )
                ce = CompareEqs(db)
                ce.assert_equality(inversely=True)

                for k in (1, -1):
                    for dir in (Dir.R, Dir.L, Dir.O, Dir.I):
                        # strict == True
                        db = (
                            (f(SEq(["a"], [], dir), right, True, k * n_in, n_in),
                             SEq(["a"], [], dir)),
                            (f(SEq(["a"], [], dir), right, True, k * n_in, n_in),
                             SEq(["a"], [], dir)),
                            (f(SEq(["a"], [], dir), right, True, k * n_in, n_in),
                             SEq(["a"], [], dir)),
                            (f(SEq(["a"], [], dir), right, True, k * n_in, n_in),
                             SEq(["a"], [], dir)),
                        )
                        ce = CompareEqs(db)
                        ce.assert_equality(inversely=True)

    def test_group(self):
        op1 = Op("O", "O", 1)
        db = (
            (Eq(["a"]), Eq(["a"]), False),
            (Eq([op1, ["a"]], [1]),
                Eq([op1, ["a"]], [1]), False),
            (Eq([op1, ["a"]], []),
                Eq([GOP, [op1, ["a"]]], [1]), True),
            (Eq([PJUXT, ["a"], ["b"]], [1]),
                Eq([PJUXT, ["a"], ["b"]], [1]), False),
            (Eq([PJUXT, ["a"], ["b"]], [2]),
                Eq([PJUXT, ["a"], ["b"]], [2]), False),
            (Eq([PJUXT, ["a"], ["b"]], []),
                Eq([GOP, [PJUXT, ["a"], ["b"]]], [1]), True),
            (Eq([PJUXT, ["a"], ["b"]], []),
                Eq([GOP, [PJUXT, ["a"], ["b"]]], [1]), True),
            (Eq([op1, [PJUXT, ["a"], ["b"]]], [1, 1]),
                Eq([op1, [PJUXT, ["a"], ["b"]]], [1, 1]), False),
            (Eq([op1, [PJUXT, ["a"], ["b"]]], [1]),
                Eq([op1, [GOP, [PJUXT, ["a"], ["b"]]]], [1, 1]), True),
            (Eq([op1, [PJUXT, ["a"], ["b"]]], []),
             Eq([GOP, [op1, [PJUXT, ["a"], ["b"]]]], [1]), True)
        )
        ce = CompareEqs(db)
        ce.assert_equality(Eq.group)

    def test_set_ovrwrt_pvoid(self):
        db = (
            (Eq([PVOID]), Eq([PVOID], [], Dir.O)),
            (Eq([RSUP, ["x"], [PVOID]], [2]),
                Eq([RSUP, ["x"], [PVOID]], [2], Dir.O)),
        )
        # V->O
        ce = CompareEqs(db)
        ce.assert_equality(Eq.ovrwrt)

        # O->O
        def f(eq):
            eq.dir = Dir.O
            eq.ovrwrt()
        ce.assert_equality(f)

        # V->O
        def f(eq): eq.ovrwrt(False)
        ce.assert_equality(f, inversely=True)

        # V->V
        def f(eq): eq.ovrwrt(False)
        ce.assert_equality(f, inversely=True)

    def test_set_ovrwrt_fromL(self):
        eqs = (
            Eq(["2"], []),
            Eq([Op("2", "2")], []),
            Eq([RSUP, ["x"], ["a"]], []),
            Eq([RSUP, ["x"], ["a"]], [1]),
            Eq([RSUP, ["x"], ["a"]], [2]),
            Eq([PJUXT, ["d"], ["d"]], []),
            Eq([PJUXT, ["d"], ["d"]], [1]),
            Eq([PJUXT, ["d"], ["d"]], [2]),
            Eq([GOP, [RSUP, ["x"], ["a"]]], [1]),
            Eq([Op("O", "O", 1), [RSUP, ["x"], ["a"]]], []),
            Eq([Op("O", "O", 1), [RSUP, ["x"], ["a"]]], [1]),
            Eq([Op("O", "O", 1), [RSUP, ["x"], ["a"]]], [1, 1]),
            Eq([Op("O", "O", 1), [RSUP, ["x"], ["a"]]], [1, 2]),
            Eq([Op("O", "O", 1), [PJUXT, ["1"], ["2"]]], [1]),
            Eq([Op("O", "O", 1), [PJUXT, ["1"], ["2"]]], [1, 1]),
            Eq([Op("O", "O", 1), [PJUXT, ["1"], ["2"]]], [1, 2])
        )

        def ret_oriented(eqs, dir):
            eqs_cp = deepcopy(eqs)
            for eq in eqs_cp:
                eq.dir = dir
            return eqs_cp

        ce = CompareEqs(ret_oriented(eqs, Dir.L), ret_oriented(eqs, Dir.O))
        ce.assert_equality(Eq.ovrwrt)

        for eq in ce.eq_out:
            eq.dir = Dir.L
        f = lambda eq: eq.ovrwrt(False)
        ce.assert_equality(f)

    def test_set_ovrwrt_RO(self):
        db = (
            (Eq(["x"], []),
                Eq([PJUXT, ["x"], [TVOID]], [2])),
            (Eq([PJUXT, ["d"], ["d"]], [1]),
                Eq([PJUXT, ["d"], ["d"]], [2])),
            (Eq([PJUXT, ["d"], ["d"]], [2]),
                Eq([PJUXT, ["d"], ["d"], [TVOID]], [3])),
            (Eq([PJUXT, ["d"], ["d"], ["d"]], [1]),
                Eq([PJUXT, ["d"], ["d"], ["d"]], [2])),
            (Eq([PJUXT, ["d"], ["d"], ["d"]], [2]),
                Eq([PJUXT, ["d"], ["d"], ["d"]], [3])),
            (Eq([PJUXT, ["d"], ["d"], ["d"]], [3]),
                Eq([PJUXT, ["d"], ["d"], ["d"], [TVOID]], [4])),

            (Eq([Op("O", "O", 1), [PJUXT, ["1"], ["2"]]], [1, 1]),
                Eq([Op("O", "O", 1), [PJUXT, ["1"], ["2"]]], [1, 2])),
            (Eq([Op("O", "O", 1), [PJUXT, ["1"], ["2"]]], [1, 2]),
                Eq([Op("O", "O", 1), [PJUXT, ["1"], ["2"], [TVOID]]], [1, 3])),

            (Eq([RSUP, ["x"], ["a"]], []),
                Eq([PJUXT, [RSUP, ["x"], ["a"]], [TVOID]], [2])),
            (Eq([RSUP, ["x"], ["a"]], [1]),
                Eq([RSUP, [PJUXT, ["x"], [TVOID]], ["a"]], [1, 2])),
            (Eq([RSUP, ["x"], ["a"]], [2]),
                Eq([RSUP, ["x"], [PJUXT, ["a"], [TVOID]]], [2, 2])),
            (Eq([GOP, [RSUP, ["x"], ["a"]]], [1]),
                Eq([PJUXT, [GOP, [RSUP, ["x"], ["a"]]], [TVOID]], [2])),

            (Eq([Op("O", "O", 1), [RSUP, ["x"], ["a"]]], []),
                Eq([PJUXT, [Op("O", "O", 1), [RSUP, ["x"], ["a"]]], [TVOID]],
                   [2])),
            (Eq([Op("O", "O", 1), [RSUP, ["x"], ["a"]]], [1]),
                Eq([Op("O", "O", 1), [PJUXT, [RSUP, ["x"], ["a"]], [TVOID]]],
                   [1, 2])),
            (Eq([Op("O", "O", 1), [RSUP, ["x"], ["a"]]], [1, 1]),
                Eq([Op("O", "O", 1), [RSUP, [PJUXT, ["x"], [TVOID]], ["a"]]],
                   [1, 1, 2])),
            (Eq([Op("O", "O", 1), [RSUP, ["x"], ["a"]]], [1, 2]),
                Eq([Op("O", "O", 1), [RSUP, ["x"], [PJUXT, ["a"], [TVOID]]]],
                   [1, 2, 2])),

            (Eq([Op("O", "O", 1), [PJUXT, ["x"], ["y"]]], [1, 2]),
                Eq([Op("O", "O", 1), [PJUXT, ["x"], ["y"], [TVOID]]], [1, 3])),
        )
        ce = CompareEqs(db)

        # R->O
        for eq in ce.eq_out:
            eq.dir = Dir.O
        ce.assert_equality(Eq.ovrwrt)

        def f(eq): eq.ovrwrt(False)

        # O->R
        ce.assert_equality(f, inversely=True)

        # R->R
        ce.eq_out[:] = ce.eq_in
        ce.assert_equality(f)

    def test_set_ovrwrt_O2L(self):
        (Eq([TJUXT, ["d"], ["d"]], []),
            Eq([TJUXT, ["d"], ["d"], [TVOID]], [3]))

    def test_remove_eq(self):
        # Replace a non-GOP block
        db = (
            (Eq(["a"]), Eq()),
            (Eq([PVOID]), Eq()),
            (Eq([Op("O", "O")]), Eq()),
            (Eq([PJUXT, ["f"], ["s"]]), Eq()),
            (Eq([PJUXT, ["f"], ["s"]], [1]), Eq()),
            (Eq([GOP, [PJUXT, ["a"], ["b"]]], [1]), Eq()),
            (Eq([PJUXT, [PJUXT, ["a"], ["b"]], ["c"]], [1]), Eq()),
            (Eq([PJUXT, [PJUXT, ["a"], ["b"]], ["c"]], [1, 1]), Eq()),
            (Eq([PJUXT, [PJUXT, ["a"], ["b"]], ["c"]], [1, 2]), Eq()),
            (Eq([PJUXT, [PJUXT, ["a"], ["b"]], ["c"]], [2]), Eq()),
        )
        ce = CompareEqs(db)
        ce.assert_equality(Eq.remove_eq)
        def f(eq):
            eq.dir = Dir.O
            eq.remove_eq()
        for eq1, eq2 in db:
            eq2.dir = Dir.O
        ce.assert_equality(f)


if __name__ == '__main__':
    unittest.main()
