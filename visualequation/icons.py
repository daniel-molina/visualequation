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

ICON_ENUMS = []


def _latex_extended(enum_item):
    if len(enum_item.name) <= 3 or enum_item.name[-3] != "_":
        return "\\" + enum_item.name.lower()
    s_latex, code = enum_item.name[:-3], enum_item.name[-2:]
    if code == "U0":
        return "\\" + s_latex.capitalize()
    if code == "U1":
        return "\\" + s_latex[0].lower() + s_latex[1:].capitalize()
    if code == "U2":
        return "\\" + s_latex[0:2].lower() + s_latex[2:].capitalize()
    if code == "N0":
        return "\\" + s_latex[:-1].lower() + s_latex[-1].capitalize()
    if enum_item._latex is None:
        raise NotImplemented
    return enum_item._latex()


def icon_class(enum_cls):
    """Decorator to register icons and extend latex method."""
    ICON_ENUMS.append(enum_cls)
    # Enums cannot be extended => Trick
    if hasattr(enum_cls, "latex"):
        enum_cls._latex = enum_cls.latex
    else:
        enum_cls._latex = None

    def latex(item): return _latex_extended(item)
    enum_cls.latex = latex
    return enum_cls
