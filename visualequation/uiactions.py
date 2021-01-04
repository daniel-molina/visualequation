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

from string import ascii_lowercase

from PyQt5.QtWidgets import QAction, qApp, QApplication
from PyQt5.QtCore import Qt

from .symbols import utils
from visualequation.eqlib.ops import Frac, Sqrt
from visualequation.eqlib.scriptops import ScriptPos
from visualequation.eqlib.letters import Latin, Greek, Digit


def _g(*args, **kwargs):
    """A slots generator."""
    def decorator(f_in):
        def f_out():
            f_in(*args, **kwargs)
        return f_out
    return decorator


class UIActions(list):
    def add(self, f, tooltip, keyseq, text=None):
        qact = QAction(self.mwin)
        qact.triggered.connect(f)
        if isinstance(keyseq, (str, int)):
            qact.setShortcut(keyseq)
        elif keyseq is not None:
            qact.setShortcuts(keyseq)
        if tooltip is not None:
            qact.setStatusTip(_(tooltip))
        if text is not None:
            qact.setText(_(text))
        self.append(qact)

    def get(self, text):
        counter = 0
        for e in self:
            if e.text() == text:
                counter += 1
                ref = e
        if counter == 1:
            return ref
        if counter == 0:
            raise ValueError("QAction not found.")
        raise ValueError("QAction with specified text is not unique.")

    def __init__(self, mwin):
        """Translations of text and tooltips are managed in self.add."""
        list.__init__(self)
        self.mwin = mwin

        deq = self.mwin.deq
        uid = self.mwin.uid
        misc = self.mwin.uimisc

        # -----------------  DisplayedEq actions ---------------
        # Self-insert (They are not intended to be manipulated)
        for c in ascii_lowercase:
            # Self-insert a-z and A-Z
            self.add(_g(Latin, c)(deq.insert_from_callable),
                     "Self-insert", c.upper())
            self.add(_g(Latin, c, True)(deq.insert_from_callable),
                     "Self-insert", "Shift+" + c.upper())
            # Greek letters
            self.add(_g(c)(deq.add_greek),
                     "Greek-insert", "Ctrl+G," + c.upper())
            self.add(_g(c, True)(deq.add_greek),
                     "Greek-insert", "Ctrl+G,Shift+" + c.upper())
            self.add(_g(c, False, True)(deq.add_greek),
                     "Greek-insert", "Alt+G," + c.upper())

        for n in range(0, 10):
            self.add(_g(Digit, str(n))(deq.insert_from_callable),
                     "Self-insert", str(n))

        # Debug
        # self.add(_g()(deq.display_orig), "Display orig (debug)",
        #          "Space")
        # self.add(_g()(deq.display_new), "Display alt (debug)",
        #          "Return")
        # self.add(_g()(deq.display_both), "Display both (debug)",
        #          "Shift+Return")

        for k, v in utils.ASCII_LATEX_TRANSLATION.items():
            self.add(_g(v)(deq.insert_latex), "Self-insert", k)

        self.add(_g(r'\sim')(deq.insert_latex), "Self-insert",
                 Qt.Key_AsciiTilde)

        self.add(_g(r'\backslash')(deq.insert_latex), "Self-insert",
                 Qt.Key_Backslash)

        self.add(_g(r'\prime')(deq.insert_latex), "Self-insert",
                 Qt.Key_Apostrophe)

        # Note: '^' is not self-inserted because of a lack of a good LaTeX
        # equivalence.

        self.add(_g()(deq.select_rmate), "Select mate to the right",
                 "Tab")
        self.add(_g()(deq.select_lmate), "Select mate to the left",
                 "Shift+Tab")
        self.add(_g()(deq.select_rmove), "Go to the right", "Right")
        self.add(_g()(deq.select_lmove), "Go to the left", "Left")
        self.add(_g()(deq.select_umove), "Go up", "Up")
        self.add(_g()(deq.select_dmove), "Go down", "Down")
        self.add(_g()(deq.delete_forward), "Delete forward", "Del")
        self.add(_g()(deq.delete_backward), "Delete backward",
                 "Backspace")

        self.add(_g()(deq.zoom_in), "Increase apparent size of equation",
                 "Ctrl++", "Zoom in")
        self.add(_g()(deq.zoom_out),
                 "Decrease apparent size of equation",
                 "Ctrl+-", "Zoom out")

        self.add(_g()(deq.select_all),
                 "Select active equation completely",
                 "Ctrl+A", "Select all")
        self.add(_g(ScriptPos.LSUB)(deq.add_scripts),
                 "Insert a subscript (backward)",
                 "Alt+B")
        self.add(_g(ScriptPos.LSUP, ScriptPos.LSUB)(deq.add_scripts),
                 "Insert a superscript and subscript (backward, select "
                 "subscript)",
                 "Alt+Shift+B")
        self.add(_g()(misc.copy_sel), "Copy selected subequation",
                 "Ctrl+C", "Copy")
        self.add(_g()(uid.show_latex),
                 "Read/Copy LaTeX code generating the equation",
                 "Ctrl+Shift+C", "LaTeX code...")
        self.add(_g()(uid.export_eq), "Export active equation",
                 "Ctrl+E",
                 "Export equation")
        self.add(_g(Frac)(deq.insert_from_callable), "Insert a fraction",
                 "Ctrl+F")
        self.add(_g(ScriptPos.RSUP)(deq.add_scripts),
                 "Insert a superscript",
                 "Ctrl+H")
        self.add(_g(ScriptPos.RSUB, ScriptPos.RSUP)(deq.add_scripts),
                 "Insert a superscript and subscript (select superscript)",
                 "Ctrl+Shift+H")
        self.add(_g(ScriptPos.CSUP)(deq.add_scripts),
                 "Insert an overset",
                 "Alt+H")
        self.add(_g(ScriptPos.CSUB, ScriptPos.CSUP)(deq.add_scripts),
                 "Insert an overset and underset (select overset)",
                 "Alt+Shift+H")
        self.add(_g(ScriptPos.RSUB)(deq.add_scripts),
                 "Insert a subscript",
                 "Ctrl+L")
        self.add(_g(ScriptPos.RSUP, ScriptPos.RSUB)(deq.add_scripts),
                 "Insert a superscript and subscript (select subscript)",
                 "Ctrl+Shift+L")
        self.add(_g(ScriptPos.CSUB)(deq.add_scripts),
                 "Insert an underset",
                 "Alt+L")
        self.add(_g(ScriptPos.CSUP, ScriptPos.CSUB)(deq.add_scripts),
                 "Insert an overset and underset (select underset)",
                 "Alt+Shift+L")
        self.add(_g()(deq.reset), "New equation (reset)",
                 "Ctrl+N", "New equation")
        self.add(uid.open_eq, "Open equation (reset)",
                 "Ctrl+O", "Open equation")
        self.add(_g(ScriptPos.LSUP)(deq.add_scripts),
                 "Insert a superscript (backward)",
                 "Alt+P")
        self.add(_g(ScriptPos.LSUB, ScriptPos.LSUP)(deq.add_scripts),
                 "Insert a superscript and subscript (backward, select "
                 "superscript)",
                 "Alt+Shift+P")
        self.add(_g(Sqrt)(deq.insert_from_callable),
                 "Insert a square root",
                 "Ctrl+R", "Sqrt")
        self.add(_g()(qApp.quit), "Exit application", "Ctrl+Q", "Exit")
        self.add(_g()(misc.paste), "Paste into active equation",
                 "Ctrl+V", "Paste")
        self.add(_g()(deq.redo), "Cut selected subequation",
                 "Ctrl+X", "Cut")
        self.add(_g()(deq.redo), "Redo (restricted to active equation)",
                 ("Ctrl+Y", "Ctrl+Shift+Z"), "Redo (local)")
        self.add(_g()(deq.undo), "Undo (restricted to active equation)",
                 "Ctrl+Z", "Undo (local)")

        self.add(_g()(uid.usage), "Usage of the program", "F1", "Help")

        # -----------------  Actions without default keybinding ---------------
        # Retrieving data
        self.add(_g()(uid.edit_latex),
                 "Edit LaTeX code of selected block", None, "Edit Latex block")
        self.add(_g()(uid.about), "About this program", None, "About")
        self.add(QApplication.aboutQt, "About Qt", None, "About Qt")
