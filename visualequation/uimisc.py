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


class UIMisc:
    def __init__(self, mwin):
        self.mwin = mwin

    def copy_sel(self):
        s = self.mwin.deq.get_sel()
        self.mwin.clipb.copy_subeq(s)

    def cut_sel(self):
        s = self.mwin.deq.get_sel()
        self.mwin.deq.delete_forward()
        self.mwin.clipb.copy_subeq(s)

    def paste(self):
        s = self.mwin.clipb.paste_subeq()
        if s is not None:
            self.mwin.deq.insert_subeq(s)
