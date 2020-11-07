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

from copy import deepcopy


class EqHist:
    """Class to manage a history of a Subeq.

    .. note::
        No copies are done for input. Caller should pass always copies of eq
        and index (deep copies for the former). However, output values are
        always copies.
    """
    def __init__(self, eq, index, selm):
        """Init a equation history.

        *eq* must be a Subeq, not an EdEq.
        """
        self.eq_hist_index = 0
        self.eq_hist = [(eq, index, selm)]

    def reset(self, new_eq, index, selm):
        """Reset history, as initially created."""
        self.eq_hist_index = 0
        self.eq_hist[:] = [(new_eq, index, selm)]

    def add(self, eq, index, selm):
        """Add new entry.

        Elements after current hist_index are discarded."""
        self.eq_hist_index += 1
        self.eq_hist[self.eq_hist_index:] = [(eq, index, selm)]

    def ovrwrt_current(self, eq, index, selm):
        """Substitute current entry.

        Elements after current hist_index are discarded."""
        self.eq_hist[self.eq_hist_index:] = [(eq, index, selm)]

    def get_prev(self):
        """Recover previous equation from the history.

        If not possible, None is returned.
        """
        if self.eq_hist_index > 0:
            self.eq_hist_index -= 1
            return deepcopy(self.eq_hist[self.eq_hist_index])

    def get_next(self):
        """Recover next equation from the history.

        If not possible, None is returned.
        """
        if self.eq_hist_index < len(self.eq_hist) - 1:
            self.eq_hist_index += 1
            return deepcopy(self.eq_hist[self.eq_hist_index])
