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

from . import eqqueries
from .symbols import utils

"""This is the module to manage groups.

There are 3 kind of groups, all of them being 1-argument operators:

    * Temporal groups.
    * Groups (permeable).
    * Solid groups.
    
Temporal group (utils.TEMPGROUP):

    It is an invisible operator intended to be used to temporally select more 
    than one contiguous co-citizen. When selection changes, if that is not
    done with the intention of extending or shrinking the TEMPGROUP, the group
    is removed.
    
    Properties:
        *   The argument of a TEMPGROUP is always the current selection of
            the equation.
        *   There can only be one TEMPGROUP in the equation at the same time.
        *   It does not care about if subequations of its argument are
            selectable or not.
    
    The argument of a TEMPGROUP makes sense to be:
    
        *   A JUXT-ublock.
    That is because symbols and any other kind of block can be selected without
    the need of a group, regardless of whether they are usubeq or citizens. 
    However, it is intentionally forbidden for a JUXT-ublock to be a citizen 
    due to JUXT composition rules. GROUPS and TEMPGROUPS are the available 
    mechanism to have JUXT-ublocks inside a another JUXT-ublock without being
    part of a "visible" operator.

    A temporal group makes sense to be:
    
        *   A citizen.
    That is because usubeqs (subeqs which are not argument of a JUXT) can be 
    always selected without the need of a TEMPGROUP.
     
    Implementation to create a temporal group must be equivalent to:
    
        *   Extract the citizens which are going to be selected from an 
            original JUXT-ublock.
        *   Create a new JUXT-ublock with all of them, respecting their order.
        *   Replace extracted citizens with a TEMPGROUP which argument is the
            new JUXT-ublock. TEMPGROUP is then *one* citizen of the original
            JUXT-ublock.

    Equation methods that cares about TEMPGROUPS:
        * Methods that modify the equation.
        * Methods that change the current selection.
    It is their responsibility to check if current selection is the argument of
    a TEMPGROUP and delete it or replace it if reasonable. 
    
Group (utils.GROUP):

    It is an invisible operator that protects a JUXT-ublock so all its 
    citizens will be always selectable as a whole (apart from individually), 
    even if it results being part of another JUXT-ublock.

    Properties:
    
        *   Subequations that starts with a GROUP are not selsubeqs, but its
            argument, a JUXT-ublock, always is.
        *   It does not care if subequations of itself strictly smaller than 
            its argument are selectable or not.
        *   There can be many GROUPs in the equation at the same time and some
            of them can be subequations of other GROUPs.
          
    The argument of a GROUP makes sense to be:
    
        *   A JUXT-ublock.
    Reasons are exactly the same than for TEMPGROUPs.
    
    A group makes sense to be:
    
        *   A citizen or ublock (including the whole equation).
    That is because a a block which is an usubeq (always selectable) 
    can become a citizen after later equation edition. As a consequence, a 
    group makes sense everywhere.

    Implementation to create a group:
    
    To introduce a GROUP is usually trivial because it is an action typically
    executed due to an explicit petition from the user, who previously need
    to select the subequation which will be the argument of the GROUP. That
    implies that, if needed, a TEMPGROUP has been previously created, and then
    it is just a matter of substituting the TEMPGROUP by a GROUP.

    Equation methods that cares about TEMPGROUPs:
    
        *   Methods that modify the equation.
    It is their responsibility to check if an edited JUXT-ublock is the 
    argument of a GROUP and delete or replace the GROUP if reasonable.

Solid group (utils.SOLIDGROUP):

    It is an invisible operator which argument is guaranteed to be selected as 
    as a whole but none of its subequations are allowed to be selected.

    Properties:
    
        *   Subequations that start with SOLIDGROUPs are not selsubeqs, but
            its argument always is.
        *   Subequations of itself strictly smaller than its argument cannot
            be selected.
        *   There can be many SOLIDGROUPs in the equation at the same time, and
            some of them can be subequations of other SOLIDGROUPs.
          
    The argument of a SOLIDGROUP makes sense to be:
    
        *   A block.
    The argument of a SOLIDGROUP must be selectable as a whole, so symbols
    and operators with no arguments already have that property and they do 
    not have arguments susceptible to be selected.
    
    A solid group makes sense to be:
    
        *   A citizen or ublock (including the whole equation).
    User is free to set any selectable block to be a solid group.

    Implementation of a solid group:
    
        Just putting a SOLIDBLOCK in front of a block would be sufficient, but 
        it would be needed to check if an element is part of a solidblock 
        each time.
        
        Another option is to implement tags for operators. Then every 
        every element of the argument(s) of the argument of the solid block 
        would carry a tag "unselectable". Symbols would be promoted to 
        operators with no arguments so they can have tags.

    Equation methods that cares about SOLIDGROUPs:
    
        *   Methods that change the current selection.
    It is their responsibility to not select any subequation of a SOLIDGROUP
    different than its argument.
"""


def remove_nonsense_group(eq, idx):
    """Remove group in idx-1 if it exists and eq[idx] is not a JUXT.
    Return the corrected index of element that was pointed by idx.
    """
    if idx > 0 and eq[idx - 1] == utils.GROUP and eq[idx] != utils.JUXT:
        eq.pop(idx - 1)
        return idx - 1
    return idx


def ungroup(eq, idx):
    """Remove an existing group or temporary group if existing it exists.

    :eq: Equation of interest.
    :idx: Index of the *argument* of the group or temporary group.
    """
    # Let us always use the group index from now on
    g_idx = idx - 1
    if not idx or eq[g_idx] not in [utils.TEMPGROUP, utils.GROUP]:
        # Case: No group at all
        return

    assert eq[g_idx-1] == utils.JUXT

    juxt_idx, arg2_idx = eqqueries.other_juxt_arg(eq, g_idx)
    if juxt_idx < 0 or arg2_idx < g_idx:
        # Easy cases: Group is an usubeq or last citizen
        eq.pop(g_idx)
    else:
        # Complex case: Group is a citizen and not the last one
        group_last_citizen = eqqueries.last_citizen(eq, g_idx + 2)
        eq.insert(group_last_citizen, utils.JUXT)
        eq[g_idx:g_idx + 2] = []


def group(eq, idx):
    """Protect subequation with a group operator or transform a temporary
    group to a group.

    If subequation is already the argument of a group or idx does not point
    to a parent JUXT, do nothing.

    Requirement: Do not send me :idx: pointing to descendant JUXTs!

    :eq: Equation of interest.
    :idx: Index in :eq: of the subequation which will be protected.
    """
    if eq[idx] == utils.JUXT:
        if idx and eq[idx-1] == utils.TEMPGROUP:
            eq[idx-1] = utils.GROUP
        elif not idx or eq[idx-1] != utils.GROUP:
            eq.insert(idx, utils.GROUP)
