# visualequation is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# visualequation is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
A module to manage creation of LaTeX templates, generations of DVI and
conversions to other formats
"""
from functools import wraps
from enum import Enum, auto
import hashlib
import os
import shutil
import subprocess
import json
import ctypes
from collections import namedtuple
from typing import List, Optional

from visualequation import commons
from .idx import Idx
from .ops import JSON_ABBREVIATIONS, Style, Juxt, CCls
from .constructs import MathConstruct
from .subeqs import Subeq

from visualequation.errors import ShowError


LatexPkg = namedtuple("LatexPkg", "opts name")

LATEX_ERROR_MSG = "Error while compiling LaTeX code.\n" \
              + "If required LaTeX packages are installed and you did not " \
              + "manually introduce invalid LaTeX code, it must be a bug." \
              + "Feel free to report it in that case.\n\nFinishing execution."


def command_not_found_msg(command: str):
    return f"Command {command} was not found, which is essential for current" \
           f"operation.\n\nFinishing execution."


def unknown_error_msg(command: str):
    return f"Unknown error reported by {command}.\n\nFinishing execution."


class SubeqEncoder(json.JSONEncoder):
    def default(self, o):
        return o.to_json()


def from_json(json_o):
    return JSON_ABBREVIATIONS[json_o["cls"]].from_json(json_o)


class LatexDoc:
    MANDATORY_PACKAGES = [
        LatexPkg("T1", "fontenc"),
        LatexPkg("latin1", "inputenc"),
        LatexPkg("", "xcolor"),
        LatexPkg("", "amsmath"),
        LatexPkg("", "amsfonts"),
        LatexPkg("", "amssymb"),
        LatexPkg("", "eurosym"),
        LatexPkg("only,oblong,bignplus,nplus,bigsqcap", "stmaryrd"),
        LatexPkg("", "esint"),
        LatexPkg("", "tensor"),
        LatexPkg("", "mathtools")
    ]

    def __init__(self, tmpdir: str,
                 extra_pkgs: Optional[List[LatexPkg]] = None,
                 extra_pre_code = ""):
        self.docclass = "article"
        self.mathenv = "displaymath"
        self.content = None

        if not os.path.exists(tmpdir):
            ShowError('Temporal directory does not exist.', True)

        self.tmpdir = tmpdir
        self.extra_pkgs = [] if extra_pkgs is None else extra_pkgs
        self.extra_pre_code = extra_pre_code

    def _pkgs_text(self):
        ret_str = ""
        for pkg in self.extra_pkgs + self.MANDATORY_PACKAGES:
            if pkg.opts:
                ret_str += "\\usepackage[" + pkg.opts + "]{" + pkg.name + "}\n"
            else:
                ret_str += "\\usepackage{" + pkg.name + "}\n"
        return ret_str

    def preamble(self):
        return "\\documentclass{" + self.docclass \
            + "}\n\\pagestyle{empty}\n" \
            + self._pkgs_text() + self.extra_pre_code

    def start(self):
        """Return the first part of a LaTeX document."""
        return self.preamble() + "\\begin{document}\n"

    @staticmethod
    def end():
        """Return the last part of a LaTeX document, starting with \n."""
        return "\n\\end{document}\n"

    def math_begin(self):
        return "\\begin{" + self.mathenv + "}\n"

    def math_end(self):
        return "\n\\end{" + self.mathenv + "}\n"

    def create_format(self, format_name: str):
        """Preload LaTeX packages in a dump.

         A format saves ~50% of compilation time, specially important for
         user interaction or exporting to images many times.
         """

        try:
            subprocess.run(
                ["etex",
                 "-ini",
                 "-output-directory=" + self.tmpdir,
                 "-jobname=" + format_name,
                 "&latex",
                 "mylatexformat.ltx"],
                input=self.start() + self.end(),
                stdout=subprocess.DEVNULL,
                text=True)
        except subprocess.CalledProcessError:
            ShowError(unknown_error_msg("etex"), True)
        except OSError:
            ShowError(command_not_found_msg("etex"), True)


def throughdvi(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        self._dvi()
        func(self, *args, **kwargs)
    return wrapper


class EqExport(LatexDoc):
    def __init__(self, eq: Subeq, tmpdir: str,
                 extra_pkgs: Optional[List[LatexPkg]] = None):
        super().__init__(tmpdir, extra_pkgs=extra_pkgs)
        self.eq = eq
        self.format_name = "export_fmt"
        self.intermediate_name = "export"
        self.dvi_file = os.path.join(self.tmpdir,
                                     self.intermediate_name + ".dvi")
        self.latex_complete = self.start() + self.math_begin() \
                              + self.eq.latex() \
                              + self.math_end() + self.end()
        self.create_format(self.format_name)

    def latex_complete(self):
        return self.latex_complete

    def latex_file(self, file_path: str):
        with open(file_path, "w") as flatex:
            flatex.write(self.latex_complete())

    def _dvi(self):
        try:
            subprocess.run(
                ["latex",
                 "-halt-on-error",
                 "-no-shell-escape",
                 "-jobname=" + self.intermediate_name,
                 "-fmt=" + self.format_name,
                 "-output-directory=" + self.tmpdir],
                input=self.latex_complete,
                #stdout=subprocess.DEVNULL,
                text=True)
        except subprocess.CalledProcessError:
            ShowError(LATEX_ERROR_MSG, True)
        except OSError:
            ShowError(command_not_found_msg("latex"), True)

    @throughdvi
    def dvi(self, output_file: str):
        shutil.move(self.dvi_file, output_file)

    @throughdvi
    def png(self, output_file: str, dpi: int = 300):
        try:
            subprocess.run(
                ["dvipng",
                 "-T", "tight",
                 "-D", str(dpi),
                 "-bg", "Transparent",
                 "-o", output_file,
                 self.dvi_file],
                stdout=subprocess.DEVNULL)
        except OSError:
            ShowError(command_not_found_msg("dvipng"), True)

        try:
            subprocess.run(
                ["exiftool",
                 "-overwrite_original",
                 "-description=" + json.dumps(self.eq, cls=SubeqEncoder),
                 output_file],
                stdout=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            msg = "Exiftool related error. Probably saved equation data was " \
                  "corrupted."
            ShowError(msg, False)
        except OSError:
            ShowError(command_not_found_msg("exiftool"), True)

    @throughdvi
    def svg(self, output_file: str, scale: int = 5):
        try:
            subprocess.run(
                ["dvisvgm",
                 "--no-fonts",
                 "--scale=" + str(scale) + "," + str(scale),
                 "-o", output_file,
                 self.dvi_file],
                stderr=subprocess.DEVNULL)
        except OSError:
            ShowError(command_not_found_msg("dvisvgm"), True)

    @throughdvi
    def eps(self, output_file: str, dpi: int = 600):
        try:
            subprocess.call(
                ["dvips",
                 "-E",
                 "-D", str(dpi),
                 "-Ppdf",
                 "-o", output_file,
                 self.dvi_file],
                stderr=subprocess.DEVNULL)
        except OSError:
            ShowError(command_not_found_msg("dvips"), True)

    def pdf(self, output_file: str, dpi: int = 600):
        eps_file = os.path.join(self.tmpdir, self.intermediate_name + ".eps")
        self.eps(eps_file, dpi)
        try:
            subprocess.call(
                ["epstopdf",
                 "--outfile", output_file,
                 eps_file])
        except OSError:
            ShowError(command_not_found_msg("epstopdf"), True)

        try:
            subprocess.run(
                ["exiftool",
                 "-overwrite_original",
                 "-description=" + json.dumps(self.eq, cls=SubeqEncoder),
                 output_file],
                stdout=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            msg = "Exiftool related error. Probably saved equation data was " \
                  "corrupted."
            ShowError(msg, False)
        except OSError:
            ShowError(command_not_found_msg("exiftool"), True)


class SubeqFamily(Enum):
    """An enum for different types of subeqs according to the their regions
    of selectivity.

    Implementation note:
        Using strings as values to save time. Just call me premature
        optimization.
    """
    VOID = auto()
    ORDINARY = auto()
    JB = auto()

    @classmethod
    def get_family(cls, s: Subeq):
        if s.is_void():
            return cls.VOID
        if s.is_jb():
            return cls.JB
        return cls.ORDINARY


class EqRender(LatexDoc):
    # Macro for juxts or symbols which are not juxteds
    PRIMARY_MACRO = r"\VEPri" # {idxkey}{idxref}{head}{formula_and_pops}
    # Macro for juxteds which are simple enough. Mandatory for contiguous
    # letters
    SECONDARY_MACRO = r"\VESec"  # {idxkey}{idxref}
    # Macro for subeqs which need a box to correctly determine their dimensions
    # They need an idxref so they can adjust dimensions of their juxt (if any)
    BOX_MACRO = r"\VEBox"  # {idxkey}{idxref}{mathstyle}{mathclass}{formula}
    # Include only classes for symbols, the rest is avoided by design
    BOX_MANDATORY_CLASSES = ()
    POP_MACRO = r"\special{subeq pop}"
    EXTRA_PRE_CODE = (r"""
        \makeatletter
        \def""" + PRIMARY_MACRO + r"""#1#2#3#4{
            #3
            \special{subeq push pri #1 #2}
            #4"""
            + POP_MACRO + r"""
        }
        \def""" + SECONDARY_MACRO + r"""#1#2{
            \special{subeq push sec #1 #2}
        }
        \def""" + BOX_MACRO + r"""#1#2#3#4#5{
            \setbox\z@\hbox{$#3 #5$}
            #4{
                {
                    \special{subeq push box #1 #2}
                    \color@block{\wd\z@}{\ht\z@}{\dp\z@}"""
                    + POP_MACRO + r"""
                }
                \box\z@
            }
        }
        \makeatother  
        """)

    def __init__(self, tmpdir: str, dpi: int = 300,
                 eq0: Optional[Subeq] = None,
                 extra_pkgs: Optional[List[LatexPkg]] = None):
        super().__init__(tmpdir, extra_pkgs=extra_pkgs,
                         extra_pre_code=self.EXTRA_PRE_CODE)
        self.format_name = "render_fmt"
        self.filename = "render"
        self.create_format(self.format_name)

        self.dpi = dpi
        self.eq = Subeq() if eq0 is None else eq0

        self.slib_filename = "/home/daniel/PycharmProjects/visualequation/vedvipng/vedvipng.so"
        self.dvi_filename = os.path.join(self.tmpdir, self.filename + ".dvi")
        self.png_filename = os.path.join(self.tmpdir, self.filename + ".png")

        self.slib = ctypes.CDLL(self.slib_filename)
        self.slib_f = self.slib.vedvipng
        self._slib_file_b = ctypes.c_char_p.in_dll(self.slib, "vedvipngpath")
        self._slib_file_b.value = self.slib_filename.encode("utf8")
        self._dvi_file_b = ctypes.c_char_p.in_dll(self.slib, "veinputfile")
        self._dvi_file_b.value = self.dvi_filename.encode("utf8")
        self._png_file_b = ctypes.c_char_p.in_dll(self.slib, "veoutputfile")
        self._png_file_b.value = self.png_filename.encode("utf8")

        self.l1 = "\\begin{document}\n" + self.math_begin()
        self.l2 = self.math_end() + self.end()
        self.idxlist = None
        self.pixels = None

    def _pri_macro(self, id, refid, s_latex, head=""):
        return self.PRIMARY_MACRO + "{%d}{%d}{%s}{%s}" % (id, refid,
                                                          head, s_latex)

    def _sec_macro(self, id, refid):
        """Add a secondary macro."""
        return self.SECONDARY_MACRO + "{%d}{%d}" % (id, refid)

    def _box_macro_start(self, s, id, refid, style):
        return self.BOX_MACRO \
               + "{%d}{%d}{%s}{%s}" \
               % (id, refid, style.latex(), s[0].ccls().latex())

    def _add_macro2block(self, s: Subeq, idx, prevstyle: Style, id, refid):
        """Auxiliary function to help _add_macros."""
        pars_latex = (self._add_macros(s[n], idx + [n], prevstyle)
                      for n in range(1, len(s)))

        return self._box_macro_start(s, id, refid, prevstyle) \
               + "{" + s[0]._latex_code.format(*pars_latex) + "}"

    def _add_macros(self, s: Subeq, idx, prevstyle: Style):
        """Return latex code to display a subequation.

        Returned string will contain the "magic" LaTeX code so vedvipng will
        be able to set self.pixels.
        """

        # Set current style and Idx key (the rest needs more info)

        idxkey = len(self.idxlist)
        self.idxlist.append((idx, SubeqFamily.get_family(s)))

        if len(s) == 1:
            # It includes symbols which are not juxteds
            if type(s[0]) in self.BOX_MANDATORY_CLASSES:
                return self._box_macro_start(s, idxkey, idxkey, prevstyle) \
                    + "{" + s[0].latex() + "}"
            return self._pri_macro(idxkey, idxkey, s.latex())

        if isinstance(s[0], Juxt):
            head_str = ""
            formula_str = ""
            sec_list = []
            for n in range(1, len(s)):
                juxtedkey = len(self.idxlist)
                self.idxlist.append((idx + [n],
                                     SubeqFamily.get_family(s[n])))
                if len(s[n]) != 1:
                    formula_str += self._add_macro2block(s[n], idx + [n],
                                                         prevstyle,
                                                         juxtedkey, idxkey)
                elif type(s[n]) in self.BOX_MANDATORY_CLASSES:
                    formula_str += self._box_macro_start(s[n],
                                                         juxtedkey, idxkey,
                                                         prevstyle) \
                                   + "{" + s[n].latex() + "}"
                else:
                    sec_list += [juxtedkey]
                    formula_str += s[n].latex()

            if not sec_list:
                return self._pri_macro(idxkey, idxkey, formula_str)
            # Specify the references.
            for j, id in enumerate(sec_list[:-1]):
                head_str += self._sec_macro(sec_list[j], sec_list[j+1])
                formula_str += self.POP_MACRO
            head_str += self._sec_macro(sec_list[-1], sec_list[-1])
            formula_str += self.POP_MACRO
            return self._pri_macro(idxkey, sec_list[0], formula_str, head_str)

        return self._add_macro2block(s, idx, prevstyle, idxkey, idxkey)

    def r_debug(self, eq: Subeq, exit_if_false: bool = False):
        """Return whether previously rendered image is correct."""
        reffilename = "ref" + self.filename
        refdvi_filename = os.path.join(self.tmpdir, reffilename + ".dvi")
        refpng_filename = os.path.join(self.tmpdir, reffilename + ".png")
        try:
            subprocess.run(
                ["latex",
                 "-halt-on-error",
                 "-no-shell-escape",
                 "-jobname=" + reffilename,
                 "-fmt=" + self.format_name,
                 "-output-directory=" + self.tmpdir],
                input=self.l1 + eq.latex() + self.l2,
                stdout=subprocess.DEVNULL,
                text=True)
        except subprocess.CalledProcessError:
            ShowError(LATEX_ERROR_MSG, True)
        except OSError:
            ShowError(command_not_found_msg("latex"), True)

        # Run vedvipng and obtain the pixels
        self._dvi_file_b.value = refdvi_filename.encode("utf8")
        self._png_file_b.value = refpng_filename.encode("utf8")
        self.slib_f(self.dpi, 0, self.pixels, 1)
        self._dvi_file_b.value = self.dvi_filename.encode("utf8")
        self._png_file_b.value = self.png_filename.encode("utf8")

        md5 = hashlib.md5(open(self.png_filename, 'rb').read()).hexdigest()
        refmd5 = hashlib.md5(open(refpng_filename, 'rb').read()).hexdigest()
        if exit_if_false:
            if md5 != refmd5:
                raise Exception("EqRender.r produced an incorrect image.")
        return None if md5 == refmd5 else refpng_filename

    def r(self, eq: Subeq):
        """Render passed Subeq. Information can be retrieved with self.info."""
        self.idxlist = []
        # It fills self.idxlist
        decorated_latex_eq = self._add_macros(eq, [], Style.DISPLAY)

        self.pixels = ((ctypes.c_int * 4) * len(self.idxlist))()
        try:
            subprocess.run(
                ["latex",
                 "-halt-on-error",
                 "-no-shell-escape",
                 "-jobname=" + self.filename,
                 "-fmt=" + self.format_name,
                 "-output-directory=" + self.tmpdir],
                input=self.l1 + decorated_latex_eq + self.l2,
                stdout=subprocess.DEVNULL,
                text=True)
        except subprocess.CalledProcessError:
            ShowError(LATEX_ERROR_MSG, True)
        except OSError:
            ShowError(command_not_found_msg("latex"), True)

        # Run vedvipng and obtain the pixels
        self.slib_f(self.dpi, len(self.idxlist), self.pixels, 0)

    def info(self):
        """Return a generator with info about rectangles associated to Idxs.

        Pixels start counting from top left. Returned values include totally
        the rectangles. They can be considered as real (number) coordinates,
        even if ints are returned. For example, the rectangle filling a whole
        pixmap of WxH pixels would be (0, 0, W, H).

        .. note::
            Consider, however, that symbols are allowed to slightly surpass
            their bounding boxes according to LaTeX rules.

            *   Idx,
            *   SubeqFamily
            *   Horizontal coordinate of left side of the rectangle
            *   Vertical coordinate of top side of the rectangle
            *   Horizontal coordinate of right side of the rectangle
            *   Vertical coordinate of bottom side of the rectangle
        """
        return ((self.idxlist[n][0], self.idxlist[n][1],
                 coords[0], coords[1], coords[2], coords[3])
                for n, coords in enumerate(self.pixels))


def get_eq_from_file(parent, filename=None):
    """Return equation inside a file."""
    try:
        eq_str = subprocess.check_output(
            ["exiftool",
             "-b",
             "-s3",
             "-description",
             filename]).decode('utf8')

    except subprocess.CalledProcessError:
        msg = "Error by exiftool when trying to extract equation from file."
        ShowError(msg, False, parent)
        return
    except OSError:
        ShowError(command_not_found_msg("exiftool"), False, parent)
        return
    except ValueError as error:
        msg = _("Error parsing metadata.\n"
                "ValueError: %s\n"
                "Was the file created with your version of Visual Equation?"
                ) % str(error)
        ShowError(msg, False, parent)
        return

    if eq_str:
        return json.JSONDecoder(object_hook=from_json).decode(eq_str)
    msg = _("No equation inside provided file.")
    ShowError(msg, False, parent)
