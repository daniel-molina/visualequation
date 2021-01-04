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

import functools
from PIL import Image, ImageQt
from PyQt5.QtGui import QPixmap, QBrush, QColor, QImage
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene

from visualequation.eqlib.edeq import EdEq
from visualequation.eqlib.conversions import EqRender, SubeqFamily


# LCARET = Op(r"\left\lvert {0} \right.", char_class=CCls.INNER)
# RCARET = Op(r"\left. {0} \right\rvert", char_class=CCls.INNER)
# OCARET = Op(r"\begingroup\color{{red}}\left\lvert {0} \right.\endgroup",
#             char_class=CCls.INNER)
# LH = Op(r"\begingroup\color{{blue}}\left\lvert {0} \right.\endgroup",
#         char_class=CCls.INNER)
# RH = Op(r"\begingroup\color{{blue}}\left. {0} \right\rvert\endgroup",
#         char_class=CCls.INNER)
#
#
# def subeq4display(eq):
#     """Return an equation with selection represented by an Op.
#
#     Output will be ready to be transformed into LaTeX and be displayed.
#     """
#     s2disp = deepcopy(Subeq(eq))
#     if eq.is_lcur() and eq.ovrwrt:
#         s2disp(eq.idx)[:] = [OCARET, eq(eq.idx[:])]
#     elif eq.is_lcur():
#         s2disp(eq.idx)[:] = [LCARET, eq(eq.idx[:])]
#     elif eq.is_rcur():
#         s2disp(eq.idx)[:] = [RCARET, eq(eq.idx[:])]
#     elif eq.is_lhl():
#         s2disp(eq.idx)[:] = [LH, eq(eq.idx[:])]
#     else:
#         s2disp(eq.idx)[:] = [RH, eq(eq.idx[:])]
#     return s2disp

def image_differences(im1: Image, im2: Image):
    min_width = min(im1.width, im2.width)
    min_height = min(im1.height, im2.height)
    max_width = max(im1.width, im2.width)
    max_height = max(im1.height, im2.height)
    im1 = im1.load()
    im2 = im2.load()
    artifacts = Image.new('RGBA', (max_width, max_height), (255, 255, 255, 0))
    # Print excess of pixels in blue
    for i in range(min_width, max_width):
        for j in range(0, min_height):
            artifacts.putpixel((i, j), (0, 0, 255, 255))
    for j in range(min_height, max_height):
        for i in range(0, min_width):
            artifacts.putpixel((i, j), (0, 0, 255, 255))
    for i in range(min_width, max_width):
        for j in range(min_height, max_height):
            artifacts.putpixel((i, j), (0, 0, 255, 255))
    # Mark differences in red
    for i in range(min_width):
        for j in range(min_height):
            if im1[i,j] != im2[i,j]:
                artifacts.putpixel((i, j), (255, 0, 0, 255))
    return ImageQt.ImageQt(artifacts)


def _setscene(deq: 'DisplayedEq'):
    deq.scene = QGraphicsScene(deq)
    deq.render.r(deq.eq)
    refpngfile = deq.render.r_debug(deq.eq)
    deq.scene.addPixmap(QPixmap(deq.render.png_filename))
    if refpngfile is not None:
        png = Image.open(deq.render.png_filename)
        refpng = Image.open(refpngfile)
        deq.scene.addPixmap(QPixmap.fromImage(image_differences(png, refpng)))
    deq.rects = []
    redbrush = QBrush(QColor(255, 0, 0, 50))
    greenbrush = QBrush(QColor(0, 255, 0, 50))
    bluebrush = QBrush(QColor(0, 0, 255, 50))
    for idx, sf, x1, y1, x2, y2 in deq.render.info():
        deq.rects.append(deq.scene.addRect(x1, y1, x2-x1, y2-y1))
        if sf is SubeqFamily.VOID:
            deq.rects[-1].setBrush(greenbrush)
        elif sf is SubeqFamily.JB:
            deq.rects[-1].setBrush(bluebrush)
        else:
            deq.rects[-1].setBrush(redbrush)
    deq.setScene(deq.scene)


def _display_init(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        func(self, *args, **kwargs)
        _setscene(self)
    return wrapper


def _display(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        eq_state = func(self, *args, **kwargs)
        _setscene(self)
        return eq_state
    return wrapper


class DisplayedEq(QGraphicsView):
    @_display_init
    def __init__(self, parent, tempdir=None, eq0=None, idx0=None, debug=False):
        QGraphicsView.__init__(self, parent)
        self.tempdir = parent.tempdir if tempdir is None else tempdir
        self.eq = EdEq(eq0, idx0, ovrwrt=False, debug=debug)
        self.render = EqRender(self.tempdir, 800, self.eq)
        #self.setAcceptDrops(True)
        self.scene = None  # To be set in decorator


    # @_display
    # def display_orig(self):
    #     self.eq.ltx = self.eq.latex
    #
    # @_display
    # def display_new(self):
    #     self.eq.ltx = self.eq.latex4display

    # def mouseMoveEvent(self, event):
    #     if event.buttons() != Qt.LeftButton:
    #         return
    #     self.setAcceptDrops(False)
    #     base = "eq" + str(random.randint(0, 999999))
    #     eq_png = eq2png(
    #         self.maineq.eq,
    #         dpi=None, bg=None, directory=self.maineq.temp_dir,
    #         png_fpath=os.path.join(self.maineq.temp_dir, base +'.png'),
    #         add_metadata=True)
    #     mimedata = QMimeData()
    #     mimedata.setImageData(QImage(eq_png)) # does not work for web browser
    #     #mimedata.setText(eq_png) # text-editor and console
    #     #mimedata.setUrls([QUrl.fromLocalFile(eq_png)]) # nautilus
    #     drag = QDrag(self)
    #     drag.setPixmap(QPixmap(eq_png))
    #     drag.setMimeData(mimedata)
    #     drag.exec_()
    #     self.setAcceptDrops(True)
    #
    # def dragEnterEvent(self, event):
    #     if event.mimeData().hasUrls():
    #         event.acceptProposedAction()
    #     else:
    #         super().dragEnterEvent(event)
    #
    # def dropEvent(self, event):
    #     if event.mimeData().hasUrls():
    #         url = event.mimeData().urls()[0]
    #         self.maineq.open_eq(str(url.toLocalFile()))
    #         event.acceptProposedAction()
    #     else:
    #         super().dropEvent(event)
    #
    @_display
    def zoom_in(self):
        if self.render.dpi < 1000:
            self.render.dpi += 50

    @_display
    def zoom_out(self):
        if self.render.dpi >= 100:
            self.render.dpi -= 50

    def get_latex_sel(self): return self.eq.latex(self.eq.idx)
    def get_latex_eq(self): return self.eq.latex()
    def get_sel(self): return self.eq.get_subeq()
    def get_eq(self): return self.eq.get_subeq(None)
    def get_idx(self): return self.eq.idx
    def get_hist(self): return self.eq.hist

    @_display
    def select_all(self): return self.eq.select_all()

    @_display
    def select_rmate(self): return self.eq.move2mate(right=True, pbc=True)

    @_display
    def select_lmate(self): return self.eq.move2mate(right=False, pbc=True)

    @_display
    def select_lmove(self): return self.eq.lmove()

    @_display
    def select_rmove(self): return self.eq.rmove()

    @_display
    def select_umove(self): return self.eq.umove()

    @_display
    def select_dmove(self): return self.eq.dmove()

    @_display
    def clean_eq(self): return self.eq.delete_eq()

    @_display
    def reset(self, new_eq=None): return self.eq.reset_eq()

    @_display
    def insert_latex(self, latex_code):
        return self.eq.insert_subeq([latex_code])

    @_display
    def insert_subeq(self, subeq):
        return self.eq.insert_subeq(subeq)

    @_display
    def insert_from_callable(self, op_class, *args, **kwargs):
        return self.eq.insert_from_callable(op_class, *args, **kwargs)

    @_display
    def add_scripts(self, *args):
        return self.eq.add_scripts(*args)

    @_display
    def add_greek(self, *args):
        return self.eq.add_greek(*args)

    @_display
    def replace_with_latex(self, latex_code):
        return self.eq.insert_subeq([latex_code])

    @_display
    def replace_with_subeq(self, subeq):
        return self.eq.insert_subeq(subeq)

    @_display
    def delete_forward(self):
        return self.eq.delete_subeq(True)

    @_display
    def delete_backward(self):
        return self.eq.delete_subeq(False)

    @_display
    def undo(self): return self.eq.undo()

    @_display
    def redo(self): return self.eq.redo()
