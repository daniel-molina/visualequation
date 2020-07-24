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

    * Temporal groups (TEMPGROUPs).
    * Permeable groups (GROUPs).
    * Solid groups (SOLIDGROUPs).

Notation:

    *   When using the word "group" in lowercase, it can refer to any of them.
    *   The uppercase always refer to a particular operator.
    *   group block refer to the subequation defined by some group operator.
    *   GROUP-block refer to the subequation defined by a permeable group and
        equivalently for TEMPGROUP-block and SOLIDGROUP-block.
    *   Sometimes, "temporal block" or "solid block" terms can be used as an
        alternative to TEMPGROUP-block and SOLIDGROUP-block, respectively.

Note that an argument of any group is classified as uarg.

Temporal group (TEMPGROUP):

    It is an invisible operator intended to be used to temporally select more 
    than one contiguous co-citizen. When selection changes, if that is not
    done with the intention of extending or shrinking the TEMPGROUP, the
    temporal group must be removed.
    
    Properties:
        *   The argument of a TEMPGROUP is always the current selection of
            the equation.
        *   There can only be one TEMPGROUP in the equation at the same time.
        *   TEMPGROUPS do not care whether subequations of its argument are
            selectable or not.
    
    The argument of a TEMPGROUP makes sense to be:
    
        *   A JUXT-ublock.
    That is because symbols and any other kind of block can be selected without
    the need of a group, regardless of whether they are usubeqs or citizens. 
    However, it is intentionally forbidden for a JUXT-ublock to be a citizen 
    due to JUXT composition rules. GROUPS and TEMPGROUPS are the available 
    mechanism to have a selected JUXT-ublock inside a another JUXT-ublock,
    without being part of any "visible" operator for the user.

    A temporal group makes sense to be:
    
        *   A citizen.
    That is because uargs or the whole eq can be always selected without the
    need of a TEMPGROUP.
     
    Implementation to create a temporal group must be equivalent to:
    
        *   Choose the subeqs which are going to be citizens of the JUXT-ublock
            argument of the TEMPGROUP.
        *   Create a JUXT-ublock with all of them, respecting the intended 
            order when placing the citizens.
        *   Preceed the JUXT-ublock with at TEMPGROUP and place it as a 
            citizen of certain JUXT-ublock.

    Equation methods which must care about TEMPGROUPS:
    
        *   Methods which modify subeq currently selected if it is a 
            JUXT-ublock.
        *   Methods which change current selection if it is a JUXT-ublock.
    It is their responsibility to check if current selection is the argument of
    a TEMPGROUP and delete it if reasonable. 
    
Permeable group (GROUP):

    It is an invisible operator that protects a JUXT-ublock so it is assured 
    that all its citizens are selectable as a whole (apart from individually).
    They are important to be left in the equation even when they are not 
    needed because the user can edit the equation later so it can finally be 
    part of another JUXT-ublock.

    Properties:
    
        *   Blocks which leading op is a GROUP are not selsubeqs, but its
            argument, a JUXT-ublock, always is.
        *   GROUPs do not care if subequations of itself strictly smaller 
            than its argument are selectable or not.
        *   There can be many GROUPs in the equation at the same time and some
            of them can belong to other GROUPs.
          
    The argument of a GROUP makes sense to be:
    
        *   A JUXT-ublock.
    Reasons are exactly the same than for TEMPGROUPs.
    
    A group makes sense to be:
    
        *   An usubeq.
    That is because an uarg or the whole eq can become a citizen after later
    equation edition. As a consequence, a group makes sense everywhere.

    Implementation to create a permeable group:
    
    To introduce a GROUP is usually trivial because it is an action typically
    executed due to an explicit petition from the user, who previously needed
    to select the subequation which will be the argument of the GROUP. That
    implies that, if needed, a TEMPGROUP has been previously created, and then
    it is just a matter of substituting the TEMPGROUP by a GROUP. Else, it is
    only needed to insert a GROUP before the the usubeq.

    Equation methods that cares about GROUPs:
    
        *   Methods which manipulate JUXT-ublocks.
        
            It is their responsibility to check if a deleted JUXT-ublock is the
            argument of a GROUP and then delete it if the JUXT-ublock stop
            being a JUXT-ublock.
    
        *   Methods which manipulate JUXT-ublocks as a whole (copy, move, 
            delete...).
        
            It is their responsibility to check if they are the argument of a 
            GROUP and perform the operation with the permeable group instead of with 
            its argument.
        

Solid group (utils.SOLIDGROUP):

    It is an invisible operator which argument is guaranteed to be selected as 
    as a whole but none of its subequations are allowed to be selected.

    Properties:
    
        *   Subequations which leading operator are a SOLIDGROUP are not
            not selsubeqs, but its argument always is.
        *   Subequations of its argument strictly smaller than it cannot
            be selected.
        *   There can be many SOLIDGROUPs in the equation at the same time, and
            some of them can be subequations of other SOLIDGROUPs.
          
    The argument of a SOLIDGROUP makes sense to be:
    
        *   A block.
    The argument of a SOLIDGROUP must be selectable as a whole, so symbols
    and operators with no arguments already have that property and they do 
    not have arguments susceptible to be selected.
    
    A solid group makes sense to be:
    
        *   An ublock.
    Solid groups can be anywhere.

    Implementation of a solid group (not decided yet):
    
        Just putting a SOLIDBLOCK in front of a block would be sufficient, but 
        it would be needed to check if an element is part of a solid block 
        each time. (This is the intended implementation)
        
        Another option is to implement tags for operators. Then every 
        every element of the argument(s) of the argument of the solid block 
        would carry a tag "unselectable". Symbols would be promoted to 
        operators with no arguments so they can have tags.
        
        Another one is to use a terminal zero-arg operator to indicate the end.

    Equation methods that cares about SOLIDGROUPs:
    
        *   Methods that change the current selection.
    It is their responsibility to not select any subequation of a SOLIDGROUP
    different than its argument.
"""
ALLGROUPS = (utils.GROUP, utils.TEMPGROUP, utils.SOLIDGROUP)


def is_group(elem):
    """Return whether primitive passed is a group of some kind."""
    return elem in ALLGROUPS


def is_grouped(eq, idx):
    """Return whether pointed subequation is the argument of a group of some
    kind"""
    return idx != 0 and is_group(eq[idx-1])


def is_pgrouped(eq, idx):
    """Return whether pointed subequation is the argument of a GROUP."""
    return idx != 0 and eq[idx-1] == utils.GROUP


def is_tgrouped(eq, idx):
    """Return whether pointed subequation is the argument of a TEMPGROUP."""
    return idx != 0 and eq[idx-1] == utils.TEMPGROUP


def is_sgrouped(eq, idx):
    """Return whether pointed subequation is the argument of a SOLIDGROUP."""
    return idx != 0 and eq[idx-1] == utils.SOLIDGROUP


def ungroup(eq, idx):
    """Remove an existing group of any kind if it exists.

    Return:

        *   If *idx* points to a JUXT-ublock which is the argument of some
            group which in turn is a not-last citizen of some other
            JUXT-ublock, minus the index of primitive pointed by *idx* in *eq*
            after the call is returned.
        *   Else, the index of primitive pointed by *idx* in *eq* after the
            call is returned.

    .. note::
        If returned value is negative, it means that *idx* pointed to a
        a JUXT-ublock and a JUXT was introduced by this call before its last
        citizen.
        Else (returned value is 0 or positive), every primitive of subeq
        pointed by *idx* can be accessed as expected by using the returned
        value as a corrected primitive's index pointed by *idx*.

    :param eq: Equation of interest.
    :param idx: Index of the **argument** of a group of some kind.
    :return: +/- the index of the primitive pointed by *idx* in *eq* after the
    call.
    """
    if not idx or eq[idx-1] not in ALLGROUPS:
        # Case: No group at all
        return idx

    g_idx = idx - 1

    juxt_idx, arg2_idx = eqqueries.other_juxt_arg(eq, g_idx)
    if juxt_idx < 0 or arg2_idx < g_idx or eq[idx] != utils.JUXT:
        # Easy cases: Group is an uarg, whole eq, last citizen or its argument
        # is not a JUXT-ublock (it can happens for solid groups).
        eq.pop(g_idx)
        return g_idx
    else:
        # Complex case: group-block is a citizen which is not a last one and
        # its argument is a JUXT-ublock
        group_last_citizen = eqqueries.last_citizen(eq, g_idx + 2)
        eq.insert(group_last_citizen, utils.JUXT)
        eq[g_idx-1:g_idx+1] = []
        return -(g_idx-1)


def group(eq, idx, solid=False):
    """If necessary, protect a subequation with a group or transform a group
    to another type.

    .. note::
        A temporal group cannot be set with this function.

    .. note::
        *idx* must not point to a descendant JUXT (that has no sense).


    :param eq: Equation of interest.
    :param idx: Index in *eq* of the subequation which will be protected.
    :return: Updated *idx* in *eq* after the call.
    """
    if isinstance(eq[idx], str) or not eq[idx].n_args:
        return idx

    gop = utils.SOLIDGROUP if solid else utils.GROUP

    if not idx:
        eq.insert(0, gop)
        return 1

    if eq[idx-1] not in ALLGROUPS:
        if not solid and eq[idx] != utils.JUXT:
            return idx
        eq.insert(idx, gop)
        return idx + 1

    # From this point idx points to the arg of a group
    if not solid and eq[idx] != utils.JUXT:
        eq.pop(idx - 1)
        return idx - 1

    eq[idx-1] = gop
    return idx
