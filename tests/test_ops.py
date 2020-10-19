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
from json import dumps, loads, JSONEncoder

from visualequation.ops import *


class OpsTests(unittest.TestCase):
    def test_pp_class(self):
        pp = PublicProperties()
        self.assertEqual(pp.keys(), PublicProperties.TYPES.keys())
        for v in pp.values():
            self.assertEqual(v, None)

        with self.assertRaises(TypeError):
            pp = PublicProperties(8)
        with self.assertRaises(TypeError):
            pp = PublicProperties(None)
        with self.assertRaises(KeyError):
            pp = PublicProperties(wrongkw=False)
        with self.assertRaises(KeyError):
            pp = PublicProperties(wrongkw=None)

        pp = PublicProperties(color=None)
        self.assertEqual(pp.keys(), PublicProperties.TYPES.keys())
        self.assertEqual(pp["color"], None)

        pp = PublicProperties(color=8)
        self.assertEqual(pp.keys(), PublicProperties.TYPES.keys())
        self.assertEqual(pp["color"], 8)
        self.assertEqual(pp["style"], None)
        with self.assertRaises(KeyError):
            pp["wrongkw2"]

        pp = PublicProperties(color=8, style=5)
        self.assertEqual(pp.keys(), PublicProperties.TYPES.keys())
        self.assertEqual(pp["color"], 8)
        self.assertEqual(pp["style"], 5)
        self.assertEqual(pp["font"], None)
        with self.assertRaises(KeyError):
            pp["wrongkw3"]

        pp = PublicProperties(color=8, style=5, font=False)
        self.assertEqual(pp.keys(), PublicProperties.TYPES.keys())
        self.assertEqual(pp["color"], 8)
        self.assertEqual(pp["style"], 5)
        self.assertEqual(pp["font"], False)
        with self.assertRaises(KeyError):
            pp["wrongkw4"]

        with self.assertRaises(KeyError):
            pp = PublicProperties(color=8, wrongkw5=5)

        pp = PublicProperties()
        self.assertEqual(pp["color"], None)
        pp["color"] = 8
        self.assertEqual(pp["color"], 8)
        self.assertEqual(pp["style"], None)
        pp["style"] = 9
        self.assertEqual(pp["style"], 9)
        with self.assertRaises(KeyError):
            pp["wrongkw9"] = 3

    def test_pseudo_symb_class(self):
        psymb = PseudoSymb("b")
        self.assertEqual(psymb._latex_code, "b")
        self.assertEqual(psymb.pp["color"], None)
        psymb.pp["color"] = 3
        self.assertEqual(psymb.pp["color"], 3)
        with self.assertRaises(KeyError):
            x = psymb.pp["wrongkw9"]
        with self.assertRaises(KeyError):
            psymb.pp["wrongkw9"] = 3

        psymb1 = PseudoSymb("b")
        psymb2 = PseudoSymb("b", color=None)
        self.assertEqual(psymb1, psymb2)
        self.assertIsNot(psymb1, psymb2)
        psymb3 = PseudoSymb("b", color=3)
        self.assertNotEqual(psymb1, psymb3)

        psymb4 = PseudoSymb("b", PublicProperties())
        self.assertEqual(psymb1, psymb4)
        psymb5 = PseudoSymb("b", PublicProperties(color=3))
        self.assertEqual(psymb3, psymb5)
        psymb4bis = PseudoSymb("b", pp=PublicProperties())
        self.assertEqual(psymb1, psymb4bis)
        psymb5bis = PseudoSymb("b", pp=PublicProperties(color=3))
        self.assertEqual(psymb3, psymb5bis)

        with self.assertRaises(KeyError):
            PseudoSymb("b", PublicProperties(dasd=3))

        with self.assertRaises(KeyError):
            PseudoSymb("b", pp=PublicProperties(dfad=3))

        with self.assertRaises(TypeError) as cm:
            PseudoSymb("b", 43)
        self.assertEqual(cm.exception.args[0],
                         PSEUDOSYMB_WRONG_PP_ARG_ERROR_MSG)

        with self.assertRaises(TypeError) as cm:
            PseudoSymb("b", PublicProperties(color=3), style=4)
        self.assertEqual(cm.exception.args[0], PSEUDOSYMB_PP_MIXED_ERROR_MSG)

        with self.assertRaises(TypeError) as cm:
            PseudoSymb("b", pp=PublicProperties(color=3), style=4)
        self.assertEqual(cm.exception.args[0], PSEUDOSYMB_PP_MIXED_ERROR_MSG)

        with self.assertRaises(TypeError) as cm:
            PseudoSymb("b", PublicProperties(color=3), wrongkw=4)
        self.assertEqual(cm.exception.args[0], PSEUDOSYMB_PP_MIXED_ERROR_MSG)

    def test_pseudo_symb_str(self):
        # Unintended: Strings in practice will be the name of derived classes
        # or certain customization
        psymb = PseudoSymb("b")
        self.assertEqual(str(psymb), "PseudoSymb")
        psymb.pp["color"] = ColorProp.BLACK
        self.assertEqual(str(psymb), "PseudoSymb{BLACK}")
        psymb.pp["font"] = FontProp.MATHTT
        self.assertEqual(str(psymb), "PseudoSymb{BLACK, MATHTT}")

    def test_pseudo_symb_repr(self):
        psymb1 = PseudoSymb("b")
        self.assertEqual(repr(psymb1), "PseudoSymb('b')")
        psymb2 = PseudoSymb("b", font=2)
        self.assertEqual(
            repr(psymb2),
            "PseudoSymb('b', font=2)")
        psymb2.pp["style"] = 4
        self.assertEqual(repr(psymb2), "PseudoSymb('b', font=2, style=4)")

    def test_pseudo_symb_repr_backslashes(self):
        latex_code = r"\omega"
        self.assertEqual(repr(PseudoSymb(latex_code)),
                         r"PseudoSymb('\\omega')")
        self.assertEqual(repr(PseudoSymb(latex_code)),
                         "PseudoSymb('\\\\omega')")
        self.assertEqual(repr(PseudoSymb(latex_code)),
                         "PseudoSymb('" + "\\" + latex_code + "')")

    def test_op_class(self):
        op = Op("B")
        self.assertEqual(op._latex_code, "B")
        self.assertEqual(op._n_args, 1)
        self.assertEqual(op._pref_arg, 1)
        self.assertEqual(op.pp["color"], None)

        op = Op("B", 3)
        self.assertEqual(op._latex_code, "B")
        self.assertEqual(op._n_args, 3)
        self.assertEqual(op._pref_arg, 1)
        self.assertEqual(op.pp["color"], None)

        op = Op("B", n_args=3)
        self.assertEqual(op._latex_code, "B")
        self.assertEqual(op._n_args, 3)
        self.assertEqual(op._pref_arg, 1)
        self.assertEqual(op.pp["color"], None)

        op = Op("B", 3, 2)
        self.assertEqual(op._latex_code, "B")
        self.assertEqual(op._n_args, 3)
        self.assertEqual(op._pref_arg, 2)
        self.assertEqual(op.pp["color"], None)

        op = Op("B", 3, font=9)
        self.assertEqual(op._latex_code, "B")
        self.assertEqual(op._n_args, 3)
        self.assertEqual(op._pref_arg, 1)
        self.assertEqual(op.pp["color"], None)
        self.assertEqual(op.pp["font"], 9)

        op = Op("B", 3, color=8)
        self.assertEqual(op._latex_code, "B")
        self.assertEqual(op._n_args, 3)
        self.assertEqual(op._pref_arg, 1)
        self.assertEqual(op.pp["color"], 8)

        op = Op("B", 3, pp=PublicProperties(color=8))
        self.assertEqual(op._latex_code, "B")
        self.assertEqual(op._n_args, 3)
        self.assertEqual(op._pref_arg, 1)
        self.assertEqual(op.pp["color"], 8)

    def test_op_str(self):
        # Unintended: Strings in practice will be the name of derived classes
        # or certain customization
        op = Op("A")
        self.assertEqual(str(op), "Op")
        op.pp["color"] = ColorProp.BLACK
        self.assertEqual(str(op), "Op{BLACK}")
        op.pp["font"] = FontProp.MATHTT
        self.assertEqual(str(op), "Op{BLACK, MATHTT}")

    def test_op_repr(self):
        op = Op("b")
        self.assertEqual(repr(op), "Op('b')")
        op = Op("b", font=2)
        self.assertEqual(repr(op), "Op('b', font=2)")
        op.pp["style"] = 4
        self.assertEqual(repr(op), "Op('b', font=2, style=4)")

        op = Op("b", n_args=2)
        self.assertEqual(repr(op), "Op('b', n_args=2)")

        op = Op("b", 3, pref_arg=2)
        self.assertEqual(repr(op), "Op('b', n_args=3, pref_arg=2)")

        op = Op("b", lo_base=True)
        self.assertEqual(repr(op), "Op('b', lo_base=True)")

        op = Op("b", lo_base=True, n_args=5)
        self.assertEqual(repr(op), "Op('b', n_args=5, lo_base=True)")

        op = Op("b", n_args=2, style=3)
        self.assertEqual(repr(op), "Op('b', n_args=2, style=3)")

    def test_op_repr_backslashes(self):
        latex_code = r"{0}{1}"
        self.assertEqual(latex_code.format("1", "2"), "12")
        self.assertEqual(repr(Op(r"{0}")), r"Op('{0}')")
        latex_code = r"\frac{{{0}}}{{{1}}}"
        self.assertEqual(repr(Op(latex_code)),
                         r"Op('" + "\\" + latex_code + "')")

        # Proof of concept, not strictly a test for the method
        latex_code_formated = r"\frac{1x^2}{2}"
        self.assertEqual(latex_code.format("1x^2", "2"), latex_code_formated)

    def test_op_rstep(self):
        for n_args in range(1, 6):
            op = Op("b", n_args)

            for sm in SelMode:
                self.assertEqual(op.rstep(sm, None), (SelMode.LCURSOR, 1))
                self.assertEqual(op.rstep(sm, n_args), None)

                for n in range(1, n_args):
                    self.assertEqual(op.rstep(sm, n), (SelMode.LCURSOR, n + 1))

                for n in range(-6, 1):
                    with self.assertRaises(ValueError):
                        op.rstep(sm, n)

                for n in range(n_args+1, n_args+6):
                    with self.assertRaises(ValueError):
                        op.rstep(sm, n)

    def test_op_lstep(self):
        for n_args in range(1, 6):
            op = Op("b", n_args)

            for sm in SelMode:
                self.assertEqual(op.lstep(sm, 1), None)
                self.assertEqual(op.lstep(sm, None), (SelMode.RCURSOR, n_args))

                for n in range(2, n_args+1):
                    self.assertEqual(op.lstep(sm, n), (SelMode.RCURSOR, n - 1))

                for n in range(-6, 1):
                    with self.assertRaises(ValueError):
                        op.lstep(sm, n)

                for n in range(n_args+1, n_args+6):
                    with self.assertRaises(ValueError):
                        op.lstep(sm, n)

    def test_op_ustep_dstep(self):
        for n_args in range(1, 6):
            op = Op("b", n_args)

            for sm in SelMode:
                self.assertIsNone(op.ustep(sm, None))
                self.assertIsNone(op.dstep(sm, None))

                for n in range(1, n_args + 1):
                    self.assertIsNone(op.ustep(sm, n))
                    self.assertIsNone(op.dstep(sm, n))

                for n in range(-6, 1):
                    with self.assertRaises(ValueError):
                        print(op.ustep(sm, n))
                    with self.assertRaises(ValueError):
                        print(op.dstep(sm, n))

                for n in range(n_args + 1, n_args + 6):
                    with self.assertRaises(ValueError):
                        print(op.ustep(sm, n))
                    with self.assertRaises(ValueError):
                        print(op.dstep(sm, n))

    def test_pjuxt(self):
        pj = PJuxt()
        self.assertEqual(pj.current_n, 2)
        self.assertEqual(pj._latex_code, "")
        self.assertEqual(pj._n_args, -1)
        self.assertEqual(pj.pp, PublicProperties())

        pj.current_n = 4
        self.assertEqual(pj.current_n, 4)
        pj2 = PJuxt(4)
        self.assertEqual(pj, pj2)

        pj = PJuxt(pp=PublicProperties(color=3, style=5))
        self.assertEqual(pj.current_n, 2)
        self.assertEqual(pj._latex_code, "")
        self.assertEqual(pj._n_args, -1)
        self.assertEqual(pj.pp, PublicProperties(color=3, style=5))

        with self.assertRaises(TypeError):
            PJuxt(PublicProperties(color=3, style=5))

        for n in range(-5, 2):
            with self.assertRaises(ValueError):
                PJuxt(n)

    def test_pjuxt_rstep(self):
        for n_args in range(2, 6):
            pj = PJuxt(n_args)

            for sm in SelMode:
                self.assertEqual(pj.rstep(sm, None), (SelMode.LCURSOR, 1))
                self.assertEqual(pj.rstep(sm, n_args), None)

                for n in range(1, n_args):
                    self.assertEqual(pj.rstep(sm, n), (SelMode.LCURSOR, n + 1))

                for n in range(-6, 1):
                    with self.assertRaises(ValueError):
                        pj.rstep(sm, n)

                for n in range(n_args + 1, n_args + 6):
                    with self.assertRaises(ValueError):
                        pj.rstep(sm, n)

    def test_pjuxt_lstep(self):
        for n_args in range(2, 6):
            pj = PJuxt(n_args)

            for sm in SelMode:
                self.assertEqual(pj.lstep(sm, 1), None)
                self.assertEqual(pj.lstep(sm, None), (SelMode.RCURSOR, n_args))

                for n in range(2, n_args+1):
                    self.assertEqual(pj.lstep(sm, n), (SelMode.RCURSOR, n - 1))

                for n in range(-6, 1):
                    with self.assertRaises(ValueError):
                        pj.lstep(sm, n)

                for n in range(n_args+1, n_args+6):
                    with self.assertRaises(ValueError):
                        pj.lstep(sm, n)

    def test_pjuxt_repr(self):
        pj = PJuxt()
        self.assertEqual(repr(pj), r"PJuxt()")

        pj = PJuxt(2)
        self.assertEqual(repr(pj), r"PJuxt()")

        pj = PJuxt(color=5)
        self.assertEqual(repr(pj), r"PJuxt(color=5)")

        pj = PJuxt(6)
        self.assertEqual(repr(pj), r"PJuxt(6)")

        pj = PJuxt(6, color=7)
        self.assertEqual(repr(pj), r"PJuxt(6, color=7)")


    def test_pjuxt_tjuxt(self):
        for kw in (PublicProperties(color=4),
                   PublicProperties(style=3, font=5),
                   PublicProperties(style=3, font=3, color=5)):
            pj = PJuxt(2, pp=kw)
            tj = pj.equiv_tjuxt()
            self.assertEqual(pj.__dict__, tj.__dict__)

    def test_pjuxt_json(self):
        class PJEncoder(JSONEncoder):
            def default(self, o):
                return o.to_json()

        def from_json(dct):
            if dct["cls"] == "PP":
                return PublicProperties.from_json(dct)
            if dct["cls"] == "PJ":
                return PJuxt.from_json(dct)
            return dct

        for pj in (PJuxt(2), PJuxt(5), PJuxt(color=ColorProp.BLUE),
                   PJuxt(10, color=ColorProp.PINK),
                   PJuxt(20, color=ColorProp.PINK, font=FontProp.MATHTT)):
            self.assertEqual(pj, loads(dumps(pj, cls=PJEncoder),
                                       object_hook=from_json))

    def test_pjuxt_str(self):
        pj2 = PJuxt()
        self.assertEqual(str(pj2), "PJuxt")
        pj9 = PJuxt(9)
        self.assertEqual(str(pj2), str(pj9))
        pj9.pp["color"] = ColorProp.BLACK
        self.assertEqual(str(pj9), "PJuxt{BLACK}")
        pj9.pp["font"] = FontProp.MATHTT
        self.assertEqual(str(pj9), "PJuxt{BLACK, MATHTT}")

    def test_tjuxt(self):
        pj = TJuxt()
        self.assertEqual(pj.current_n, 2)
        self.assertEqual(pj._latex_code, "")
        self.assertEqual(pj._n_args, -1)
        self.assertEqual(pj.pp, PublicProperties())

        pj.current_n = 4
        self.assertEqual(pj.current_n, 4)
        pj2 = TJuxt(4)
        self.assertEqual(pj, pj2)

        pj = TJuxt(pp=PublicProperties(color=3, style=5))
        self.assertEqual(pj.current_n, 2)
        self.assertEqual(pj._latex_code, "")
        self.assertEqual(pj._n_args, -1)
        self.assertEqual(pj.pp, PublicProperties(color=3, style=5))

        with self.assertRaises(TypeError):
            TJuxt(PublicProperties(color=3, style=5))

        for n in range(-5, 2):
            with self.assertRaises(ValueError):
                TJuxt(n)

    def test_tjuxt_repr(self):
        tj = TJuxt()
        self.assertEqual(repr(tj), r"TJuxt()")

        tj = TJuxt(2)
        self.assertEqual(repr(tj), r"TJuxt()")

        tj = TJuxt(color = 3)
        self.assertEqual(repr(tj), r"TJuxt(color=3)")

        tj = TJuxt(6)
        self.assertEqual(repr(tj), r"TJuxt(6)")

        tj = TJuxt(6, color=2)
        self.assertEqual(repr(tj), r"TJuxt(6, color=2)")

    def test_tjuxt_pjuxt(self):
        for kw in (PublicProperties(color=4),
                   PublicProperties(style=3, font=5),
                   PublicProperties(style=3, font=3, color=5)):
            tj = TJuxt(2, pp=kw)
            pj = tj.equiv_pjuxt()
            self.assertEqual(pj.__dict__, tj.__dict__)

    def test_tjuxt_json(self):
        class TJEncoder(JSONEncoder):
            def default(self, o):
                return o.to_json()

        def from_json(dct):
            if dct["cls"] == "PP":
                return PublicProperties.from_json(dct)
            if dct["cls"] == "TJ":
                return TJuxt.from_json(dct)
            return dct

        for pj in (TJuxt(2), TJuxt(5), TJuxt(color=ColorProp.BLUE),
                   TJuxt(10, color=ColorProp.PINK),
                   TJuxt(20, color=ColorProp.PINK, font=FontProp.MATHTT)):
            self.assertEqual(pj, loads(dumps(pj, cls=TJEncoder),
                                       object_hook=from_json))

    def test_tjuxt_str(self):
        tj2 = TJuxt()
        self.assertEqual(str(tj2), "TJuxt")
        tj9 = TJuxt(9)
        self.assertEqual(str(tj2), str(tj9))
        tj9.pp["color"] = ColorProp.BLACK
        self.assertEqual(str(tj9), "TJuxt{BLACK}")
        tj9.pp["font"] = FontProp.MATHTT
        self.assertEqual(str(tj9), "TJuxt{BLACK, MATHTT}")



if __name__ == '__main__':
    unittest.main()
