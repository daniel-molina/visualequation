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

from enum import Enum, unique

@unique
class Dir(Enum):
    I = -2  # insertion mode
    L = -1  # left direction in oriented insertion mode
    V = 0   # overwrite direction in oriented insertion mode
    R = 1   # right direction in oriented insertion mode
    O = 2   # overwrite mode
