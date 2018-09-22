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

class EqHist:
    def __init__(self, init_eq):
        self.eq_hist = [(list(init_eq), 0)]
        self.eq_hist_index = 0

    def save(self, eq, sel_index):
        """
        Save current equation to the historial and delete any future elements
        from this point
        """
        self.eq_hist_index += 1
        self.eq_hist[self.eq_hist_index:] = [(list(eq), sel_index)]

    def get_prev(self):
        """ Recover previous equation from the historial """
        if self.eq_hist_index != 0:
            self.eq_hist_index -= 1
        return self.eq_hist[self.eq_hist_index]

    def get_next(self):
        """ Recover next equation from the historial """
        if self.eq_hist_index != len(self.eq_hist)-1:
            self.eq_hist_index += 1
        return self.eq_hist[self.eq_hist_index]
