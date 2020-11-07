# User Interface

> **Note**: At least part of some operations should be presented
> in some way that a casual user is someway "forced" to know about them.
> An initial window with tips or a dropdown are possibilities.

## Introduction to keybindings
Since subequations can be arbitrarily nested, contrary to characters in a
line or document, an equivalence must be set. The concept of mates of a
subequation is a powerful tool to flat its equation. Desktop-like operations
will be based on that idea, being the subequation of interest current
selection or its supeq.

Previous partition in mates of an equation depends on a chosen subequation
(or, equivalently, on the ulevel of the mates being considered). An alternative
way is to consider the deepest level of the equation: its symbols.
Considering that each symbol is a character and their supeqs are words, the
equation can be flatted locally, even if it does not define consistent
partition of the whole equation. Terminal-like operations will be based on
this.

### Keybindings

Desktop-like operations must be intuitive for a user with no experience with
emacs or command-line shortcuts. Most of common shortcuts used in usual text
editors and graphical applications are set set by default, even if
they collide with defaults of readline. At the end, Visual Equation is a 
graphical application, so users will expect that. Advanced users should have
no problems in setting their own keybindings.
 
> **Note**: A good feature may be to provide "sets" of shortcuts already 
> defined, apart of being able to specify them individually.

The user interaction of desktop-like operations is everything that can be done
with the mouse and also by using cursor keys, RETURN, BACKSPACE, DEL and some
standard uses of CONTROL, ALT and SHIFT and TAB. Main reference will be the
GNOME desktop, but most of the time they will be shared by other desktops, even
from different operative systems.

### Notation for keystrokes

*   When an alphabetic key is required for a keybinding, it is noted always
    lower-case (e.g., in examples below, `X` is noted as `x`), independently of
    whether `SHIFT` key is being used or not.
*   When `CONTROL` key is required for a keybinding, it is noted as `C-` 
    (e.g, `C-x`).
*   When `ALT` key is required for a keybinding, it is noted as `M-` (e.g, 
    `M-x`).
*   When `SHIFT` key is required for a keybinding, it is noted as `S-` (e.g,
    `S-TAB`)
*   The order of precedence when writting a keybinding is, from left to right:
    `S-`, `M-`, `C-` (e.g, `M-C-x` or `S-C-x`). However, when stroking the 
    keybinding the order does not matter as long as the final key (`x` in the
    examples) is pressed the last one, being all the others currently pressed
    at the that happens.
*   It is possible to previously press `ESC` and release it instead of leaving
    `ALT` pressed at the same time than the rest of the keys, so `ESC x` is
    equivalent to `M-x` and `ESC C-x` equivalent to `M-C-x`.


### Numeric arguments (M-0, M-1, ..., M--)
Numeric arguments may modify the next operation indicated to visual equation.
For example, `M-3 f` will introduce three "f" characters instead of only one.
As in the example, by default, a numeric argument will be equivalent to
repeat operation the indicated number of times. If that is not the case, the
description of the operation should indicate details of the effect of a numeric
argument.

Successive numeric arguments add a digit to the argument already being
prepared. For example `M-1 2 h` introduces twelve "h" characters. It is also
possible to introduce every digit with meta, so the following is equally valid
`M-1 M-2 h`. Introducing a number several times using this procedure is
impossible without an additional command. A usual workaround in readline is to
use the command quoted-insert (`C-q` or `C-v` by default) to manage that. In
Visual Equation, you can equivalently use `M-g` which is normally used to
transform Latin letters into Greek, but it also transforms numbers into itself.
For example, to introduce 3 ten times you can type: `M-1 0 M-g 3`.

`M--` starts a negative argument. For example, `M-- M-2 C-f` passes argument -2
to operation associated to keybinding `C-f`. If no number is added after
`M--`, -1 is passed implicitly.

## Global operations

**Saved equations** can be accessed like previous commands on the history of a
shell. In addition, saved equations can have an associated name, categories
and subcategories (arbitrarily nested), but it is not mandatory.

Not to confuse "saved equations" with "exported equations".

Exported equations are equations that can be accessed outside Visual Equation.
Current formats to export equations are PNG, EPS, SVG and PDF. On the contrary,
saved equations are stored in a database which only Visual Equation is
intended to use. There are a lot of different commands to save equations.

Details on shell-like operations.

### Help (F1)
### Select previous/next equation (C-UP/C-DOWN)
Select a contiguous equation.
### Go to first/last equation (C-HOME/C-END)
### Create new eq after current one (RETURN)
### Transpose eq with previous/next equation (M-UP/M-DOWN)
Exchange positions of contiguous equations.
### Move screen up/down (PAGEUP/PAGEDOWN)
### Increase/Decrease size of equations (C-+/C--)

### New tab (C-t)
### Close tab (C-w)
### Close all tabs (S-C-w)

### Quit (C-q)
Exit Visual Equation with a confirmation dialog.

> **Note**: C-q has a long tradition in many desktops to quit programs, so it
> has been requisitioned to readline. M-q is used instead for that, even if
> the meaning is quite different (except when followed by a number).

### Quit without dialog ()
Exit Visual Equation if equation is a PVOID, discarding the kill ring and the
undo list. It never asks for confirmation to quit.

### Open equation (C-o)
This is desktop-like operation but it is placed in this section to help the
reader have a big picture.

This command is managed completely with a graphical interface.
If equation being edited has not saved modifications, the user is asked to
save it as a new equation or, if applicable, overwriting its previous entry
in the history list. In detail:

*   If equation currently has already a place in the history:
    *   The user is asked whether discarding modifications, overwrite or save
        as a new equation.
*   Else:
    *   The user is asked whether discarding the equation or save as a new
        equation.

After that, the user can choose an equation from the history
with different graphical search facilities and fetch it.

### New document (C-n)
This is desktop-like operation but it is placed in this section to help the
reader have a big picture.

It ask the user if it is desired to save current equations. In the positive
case, the usual dialog to save equation is presented. After that, a new empty 
equation is presented for edition.

### Export equations (C-e)
Export all equation (saved or not) to images, specifying its size, format
and other details.

It is possible to recover equations for further edition from exported equations
in PNG and PDF format.

### Export current equation (S-C-e)
Export only equation being edited

### Save as... (S-C-s)
This is desktop-like operation but it is placed in this section to help the
reader have a big picture.

Save with a graphical interface current equation as a new equation at
the end of the history, possibly specifying a name and categories.

### Save (C-s)
This is desktop-like operation but it is placed in this section to help the
reader have a big picture.

If equation being edited was never saved, this command is equivalent to
save_as. Else, it overwrites previously saved version of equation.

### Print (C-p)


### Accept line ()
This a non-windowed version of *Save as...*.
Specify a name and save current equation as a new equation with that name. 
After that, a new empty equation is presented for edition.
It is possible to specify a category in the form
`[category[/subcategory[/...]]/]name`. To accept the name press again C-j or 
C-m or RETURN.
**Note**: C-j acts differently while searching in the history. See below.

### Insert comment ()
Save current equation at the end of the history list (as a new equation)
and start editing a new empty equation. This is a fast accept-line that does
not ask the user for an equation name nor categories to include in the save.
With a numeric argument, it is equivalent to accept_line.

### Save without dialog ()
This is not a readline command but it is placed in this section to help the
reader have a big picture.

It acts like command *Save* (C-s) but not allowing the user to add a name or
categories if equation was not saved before. It is:
*   If equation is already part of the history, overwrite its entry.
*   Else, it is equivalent to insert_comment.

In any case, a numeric argument allows the user to specify a name and
categories. If equation already existed:
*   If only a name is provided, equation is renamed but old categories, if
    any, are unmodified.
*   If at least a main category is provided, any category equation had are
    discarded.

To discard previous categories without adding a new one, just precede the name
by a slash as in `/newname`.

### Previous saved equation ()
*Save without dialog* displayed equation and fetch the previous equation from
the history list, moving back in the list.

> **Note**: Default readline keybinding is C-p.
### Next saved equation ()
save-no-window displayed equation and fetch the next equation from the 
history list, moving forward in the list.

> **Note**: Default readline keybinding is C-n.

### Beginning of history ()
save-no-window displayed equation and fetch the first equation in the
history.
### End of history ()
save-no-window displayed equation and fetch the last equation of the history.

### Reverse search history ()
save-no-window current equation and search backward starting at the current
equation and moving up through the history as necessary. This is an 
incremental search. You can introduce part of the name, category or other 
fields (TODO: specify). You can fetch the equation with C-j. Any
other key combination will fetch the equation and then apply the command
to the equation.

### Forward search history ()
Counter part of reverse-search-history.
> **Note**: C-s is not used as key binding because that is a
> shortcut with a long tradition in desktop applications to save files. If
> we allow key-bindings to be configurable, this will be one of the first
> commands supported.

> **Note**: By default, M-C-R is assigned to revert-line along with M-R in
> readline.

### Non-incremental reverse search history (Not to be implemented)
Replace current equation by some previous equation of the history and
discard any edition information of previous equation (so command undo will 
not work). Equation taken is searched backward through the history starting
at the current equation, using a non-incremental search. To accept the input, 
press RETURN, C-j or C-m. To abort press BACKSPACE, a backward-delete-char
command or an abort command.
> **No-Implementation note**: I cannot find a way to like this command! I do
> not have any reason to implement it (today).

The default readline keybinding for this command, M-p, is used as C-UP (see
 basic
 movements).

### Non incremental forward search history (Not to be implemented)
The counterpart of non-incremental-reverse-search-history.

The default readline keybinding for this command, M-n, is used as C-DOWN (see 
basic basic movements).

## Basics of selection and edition
Users who do not know any key-bindings, with no previous experience 
with Visual Equation or which will not dedicate time to learn the rest of
movements, will likely use the mouse and, likely, LEFT and RIGHT keys.

Because of that, fundamental movements are intended to satisfy the following
conditions:

*   It must be possible to select any selsubeq by using them.
*   It must be required very few fundamental movements to select selsubeqs
    which are close to current selection.
*   Navigating far away must not require too many fundamental movements.
*   Fundamental movements must be someway reasonable so the user can learn
    their behaviour soon.
*   Fundamental movements must be a compromise between being practical and not
    discouraging a new user to use the program because they look strange.

### Modes (Insertion and Delete)

There are two operation modes which, in some cases, operates differently when
the same input is processed by the program. They are:

*   Insertion mode (imode)
*   Overwrite mode (ovmode)

They can be switched by pressing INS.

Noticeable keyboards are `M-v` and `S-M-v` (which can be thought as commands
similar to *Paste* (`C-v`) and *Paste overwriting* (`S-C-v`)). `S-M-v` replaces
current selection by next user input, independently of the mode. `M-v` acts
equivalently if input is a symbol but, if it is an operator, in addition first
parameter is set to previous selection, while any other parameter is still set 
to PVOID.

#### Insertion mode (imode)

*   The cursor is always to the left of selection.
*   Insertions introduce subeqs to the right of the cursor, preserving selected
    subeq and keeping it selected.
*   DEL deletes selection.
*   If selection is a juxted, BACKSPACE deletes the juxted to the left.


#### Overwrite mode (ovmode)

*   It is equivalent to *insert mode* except for insertions (honoring graphical
    overwrite mode in texts editors, but not readline's version where BACKSPACE
    replaces with a white space).
*   Inserted subeqs substitute selection.

### Deletion details

When DEL or BACKSPACE act on an existing subeq S and it is not PVOID, if S is
a juxted it is vanished and if it is a non-juxted it is substituted by a PVOID.
If they act on a PVOID and it is a script, the script is completely removed
(consequently downgrading the script op). If it is a PVOID and some copar it
has is not a PVOID, nothing is done. If it is a PVOID which has no copars or
all of them are also PVOIDs, supeq is deleted.

> **Note**: Flatting a supeq only when every par is a PVOID avoids unexpected 
> results for the inexperienced users and, at the same time, allows a naive way
> to delete the supeq "from inside".

### Left click (arbitrary distance movement)

Most intuitive movement. However, it may be possible that not all usubeqs
sharing the same area when displayed are able to be selected this way. For
example, a usubeq giving color to its only parameter.

### LEFT/RIGHT cursor keys (short, exhaustive and redundant movements):

These keys, even if in the desktop-like category, provide a different approach.
These are bullet-proof, meaning that every selsubeq can be selected by using
them exclusively, even only one of them. They are handy to select a random
subeq which is close to current selection. Redundancy is useful when the
user is introducing subeqs and needs to select a related subeq.

Description:

Effect of pressing LEFT/RIGHT:
*   If R/L, set L/R.
*   Else, navigate equation backward/forward, selecting selsubeqs before
    entering them and before exiting them.
*   In addition, if O or I, insert a TVOID after a subeq before entering from/
    exiting to the right, so the user can insert everywhere also when using
    imode or ovmode.

### UP/DOWN cursor keys
They change selection according to specific subeq being selected. Typical case
is to move from numerator to denominator (and the other way around).

## Selection-size operations
Operations in this section act on subequations which sizes are related to the
size of current selection. For example the selection itself, its mates,
1-level subeqs and 1-level supeq. These operations may act on higher level
subeqs or supeqs if a numeric argument is passed.

> **Reasoning about main advanced keybindings**:
>
> In common graphical text editor:
>
>*  S-TAB/TAB are used to increase/remove indentation, but it is also commonly 
>   associated to navigate through different fields.
>*  M-LEFT/M-RIGHT are used to transpose words.
>*  C-LEFT/C-RIGHT are used to move between word boundaries.
>*  S-C-LEFT/S-C-RIGHT are used in graphical text editors to select from cursor
>   to word boundaries.
>*  C-BACKSPACE/C-DEL are used in graphical text editors to delete from the
>   cursor to word boundaries.
>*  S-C-BACKSPACE/S-C-DEL are used in graphical text editors to delete from the
>   cursor to line boundaries.
>
> In Visual equation:
>
>*  TAB is associated to mates. S-TAB/TAB select them and S-C-TAB/C-TAB
>   transpose them.
>*  M-LEFT/M-RIGHT push and pull subeqs to the boundaries of juxt-blocks or
>   inside/outside blocks.
>*  CONTROL-LEFT/RIGHT are associated to word boundaries.
>*  C-LEFT/C-RIGHT selects first/last param.
>*  S-C-LEFT/S-C-RIGHT increases selection until first/last param.
>*  C-BACKSPACE/C-DEL deletes from cursor to first/last param.
>*  S-C-BACKSPACE/S-C-DEL delete from cursor to line boundaries, voiding any
>   subeq that cannot be vanished.
>
> In addition:
>
>*  S-BACKSPACE/S-DEL flats/voids blocks.
>
>
> Main disparity is that S-C-TAB/C-TAB would fit better M-LEFT/M-RIGHT common
> usage in graphical text editors.
> However, it is a good feature that all commands using TAB are associated to
> the same idea (mates) while ALT, which only has two cursor commands
> involved because other keybindings may collide with the desktop keybindings,
> performs an unusual action in text editors.

### Changing selection

#### Toggle overwrite mode (INS)
This command switch from normal mode into overwrite mode and from overwrite
mode into normal mode.

Overwrite mode is more similar to the behavior of graphical editors than the
one of readline. In particular, backward delete does not create an "empty 
space" but totally removes the previous "character". One difference with any 
common overwrite mode is that inserting without a movement never trespass a 
supeq but in text editors eventually words delimiters are overwritten and
several words become a single one.

#### Selecting further subeqs

> **Note**: Successive keystrokes of the same class will remember the mate
> ulevel.

If selection is the whole eq, do nothing.
Else, consider that supeq of selection is called SUP.

##### Forward select first par of supeq (Unbounded)
*   If SUP has a mate to the right RSUP, select the first param of RSUP.
*   Elif SUP has at least one mate to the left, select the first param of the
    first mate of SUP.
*   Else, select the first param of SUP.

##### Select first par of supeq (C-LEFT)
*   If selection is not the first param of SUP, select the first param of SUP.
*   Elif SUP has a mate to the left LSUP, select the first param of LSUP.
*   Elif SUP has at least one mate to the right, select the first param of the
    last mate of SUP.
*   Else, do nothing.

##### Select last par of supeq (C-RIGHT)
*   If selection is not the last param of SUP, select the last param of SUP.
*   Elif SUP has a mate to the right RSUP, select the last param of RSUP.
*   Elif SUP has at least one mate to the left, select the last param of the
    first mate of SUP.
*   Else, do nothing.

##### Backward select last par of supeq (Unbounded)
*   If SUP has a mate to the left LSUP, select the last param of LSUP.
*   Elif SUP has at least one mate to the right, select the last param of the
    last mate of SUP.
*   Else, select the last param of SUP.

#### Backward/Forward modify selection (S-LEFT/S-RIGHT):

When using S-LEFT/S-RIGHT:
*   If a non-juxted is selected:
    *   If previous keystroke was of a different class, select supeq of 
        selection. In orimode, in addition set dir to direction matching the
        key combination.
    *   Elif keystroke coincides with first keystroke of the sequence, select
        supeq.
    *   Elif selection is a symbol or GOP-par:
        *   If not orimode or V, select supeq and consider direction of
            current keystroke to be a new first one from now on.
        *   Else (L or R) set the opposite direction and consider current
            keystroke to be the first one of the sequence from now on.
    *   Else, select the last/first param.
*   Elif (a juxted is selected and) previous keystroke was of a different
    class:
    *   If there is a cojuxted in direction of keystroke, include it in
        selection by using a TJUXT-block in the case that there are cojuxteds 
        that are not being selected. Else, just select the whole PJUXT-block. 
        In addition, if orimode, in any case set dir to direction of keystroke.
    *   Else, select the while PJUXT-block of the juxted. In addition, if
        orimode, set dir to direction of keystroke.
*   Elif keystroke coincides with the first one of the sequence:
    *   If there is a cojuxted in the requested direction, include it in
        selection, using a TJUXT-block if there are no selected cojuxteds.
    *   Else, select its PJUXT-block.
*   Elif selection is a juxt-block, shrink selection excluding the juxted in 
    the opposite side of keystroke direction, using TJUXT-blocks if needed.
*   Elif not orimode, flip direction and consider current keystroke the first
    one.
*   Else, select supeq and consider current keystroke the first one of the
    sequence from now on.

#### Backward/Forward greatly modify selection (S-C-LEFT/S-C-RIGHT)
*   If selection is a juxted, include in selection all its cojuxteds to the
    left/right, using a TJUXT-block if needed.
*   Else, select supeq.

It must be equivalent to use S-LEFT/S-RIGHT once or more times, so
further details may apply.

#### Select all (C-a)
This keybinding has a long tradition in graphical applications, so it is
respected even if it collides with an important shortcut of readline.

#### Select usupeq (M-a)
Select usupeq if it exists. Do not change dir unless it is V. In that case, set
R. It resembles the GUI notion of using SHIFT to extend current selection.

#### Select first param ()
Select first 1-ulevel usubeq of selection if it exists and is selectable.

Do not change dir unless required by a PVOID.
It resembles the GUI notion of using SHIFT to shrink current selection and
also that DOWN does not always go to the start of the next line. Of course,
SHIFT-DOWN per se would extend selection and not shrink it in reasonable text
editors.

#### Select last param ()
Select last 1-ulevel usubeq of selection, if it exists and is selectable.
Do not change dir unless required by a PVOID.

#### Select juxted to the left of usupeq ()
Select juxted to the left of usupeq. If it does not exist, select usupeq.

#### Select juxted to the right of usupeq ()
Select juxted to the right of usupeq. If it does not exist, create a TVOID.


#### Select mate to the left/right (S-TAB/TAB)
These key bindings are used to navigate between mates.

> **Notes**:
>*  TAB is used for mate operations (select and transpose).
>
>*  The behavior does more honor to kwrite than to equivalent readline or gedit
>   keybindings (considering that mates are words) because final selection does
>   not set orientation depending on the key. The reasoning is that it was
>   decided that operations will not change direction unless strictly needed,
>   it is explicitly requested (*Change dir*) or by use of the basic selection
>   commands (LEFT/RIGHT).

When using S-TAB/TAB:
*   The mate to the left/right of selection is selected without changing dir.
    Marginal case: If selection is the first/last mate, choose the last/first
    mate.
*   Successive keystrokes of these key combinations (valid for an interleaved
    use of them) will remember the N-mate level of the selection before 
    applying the first of these key combinations.

> **Note**: Successive keystrokes of the same class will remember the mate
> ulevel.


### Editing

#### Cut (C-x, S-DEL)
#### Cut special (S-C-x)

Remove selected subeq and save/overwrite VE's clipboard.
 
This shortcut is a an important key combination for emacs and readline, but by
default the desktop tradition will be respected.

#### Crop selection (M-x)
Substitute equation with selection. Undo command would restore previous eq.

#### Copy (C-c)
#### Copy special (S-C-c)
Set VE's clipboard to selection.

#### Overwrite with next input (S-M-o)
Next input will overwrite instead of being inserted. If Dir.R and selection is
a non-last juxted, juxted to the right of selection is the one overwritten.

#### Overwrite with next input integrating selection (M-o)
Overwrite selection with next input and set first PVOID of the input, if any,
to previous selection.

#### Paste (C-v)
Insert content of clipboard.

#### Paste special (S-C-v)

Insert content of current clipboard or previous subeqs copied or cut with a
specific format.

#### Paste overwriting (S-M-v)
#### Paste overwriting integrating selection (M-v)
Overwrite selection with VE's clipboard and set first PVOID of replacement,
if any, to previous selection.

> **Note**: M-C-v is known to be used in KDE for clipboard management.

> **Note**: M-v is equivalent to M-o C-v and S-M-v to S-M-o C-v.

#### Undo (C-z)
Undo last edition, if it exists.

#### Local undo (M-z)
Undo last edition in current equation, if it exists.

#### Complete local undo (S-M-z)
Undo all changes made to current equation. This is like executing *local undo*
command enough times to return the equation to its initial state.

#### Redo (S-C-z, C-y)
Redo last edition, if it exists.

#### Local redo (M-y)
Redo last edition in current equation, if it exists.

#### Complete local redo (S-M-y)
Redo all changes made to current equation. This is like executing *local redo*
command enough times to return the equation to its final state.

#### Complete undo (S-M-C-z)
Undo all changes made to all equations. This is like executing *undo*
command enough times to return to the initial void equation.

#### Complete redo (S-C-y)
Redo all changes made to all equations. This is like executing *redo*
command enough times to return the equations to their final state.

#### Delete and select mate (C-d)
If selection is a juxted, it is equivalent to DEL.
Else, after deleting selection, the mate to right is selected.

#### Backward delete and select mate (S-C-d)
If selection is a juxted, it is equivalent to BACKSPACE.
Else, the mate to left is selected and deleted as if DEL was pressed.

#### Delete coparams to the right (C-DEL)
If selection is a juxted remove all the juxteds of the same PJUXT-block to the
right of the cursor.

If selection is not a juxted, substitute pars of lop-block to the right of the
cursor by PVOIDs.

If there is nothing to remove, lop-block is flatted (?).

> **Note**: Successive keystrokes of the same class will remember the mate
> ulevel if needed.

#### Delete coparams to the left (C-BACKSPACE) 

If selection is a juxted remove all the juxteds of the same juxt-block to the 
left of the cursor

If selection is not a juxted, substitute pars of lop-block to the left of the
cursor by PVOIDs.

If there is nothing to remove, lop-block is flatted (?).

> **Note**: Successive keystrokes of the same class will remember the mate
> ulevel if needed.

#### Transpose mate (C-TAB/S-C-TAB)

Swap positions of current selection and its mate to the right/left, leaving
original selection selected.

No direction is changed.

Marginal case: If there is no mate in the asked direction, do nothing.

> **Note**: Successive keystrokes of the same class will remember the mate
> ulevel if needed.

#### Transpose supeq ()
#### Backward transpose supeq ()

#### Push right (M-RIGHT)
Probably to be changed just to move subeq where RIGHT would go if pressed.

*   If selection is a last mate, do nothing.
*   Elif selection is a juxted and has a cojuxted to the right which is a
    gsymb:
    *   If there is at least one cojuxted to the right of selection which is
        not a gsymb, move selection just before that juxted.
    *   Else, move selection so it becomes the last juxted.
*   Else:
    *   If mate to the right of selection is a PVOID, substitute PVOID with
        selection and remove original selection (by vanishing or substituting
        by PVOID, depending whether it is a juxted or not).
    *   Else, move selection to the left of its mate to the right as a juxted.

#### Push left (M-LEFT)
Counter-part of *Push*.

#### Transmute with supeq ()
If selection is a block B and has a supeq SUP, exchange lop-B and lop-SUP,
removing excess of parameters and including PVOIDs as needed.

#### Transmute with first par ()
If selection is a block B and its first parameter is a block BSUB, exchange
lop-B and lop-BSUB, removing excess of parameters and including PVOIDs as 
needed.

#### Transmute with last par ()
If selection is a block B and its last parameter is a block BSUB, exchange
lop-B and lop-BSUB, removing excess of parameters and including PVOIDs as 
needed.

#### Rotate copars to the left ()
#### Rotate copars to the right ()

#### Delete equation (C-k)
Remove the whole equation. Undo command would restore previous eq.

#### Delete usupeq (M-k)
If supeq is a juxted, vanish it (with all its subeqs). Else, replace it with a
PVOID.

#### Delete last param (C-u)
Delete last param.

#### Delete first param (M-u)
Delete first param.

#### Kill line restricted ()
If whole equation E is a juxt-block, remove every juxted of E to the right
of the cursor. Killed juxteds are saved on the kill-ring.

With a negative argument, kill any subequation before cursor.
#### Backward kill line restricted ()
Counter-part of *Kill line restricted*.

> **Note**: Default readline keybinding is undesired (C-x Rubout), so
> keybinding of a very similar command (*Unix line discard*), which is not
> going to be implemented in Visual Equation, is used instead.

#### Unix line discard (Not to be implemented)
Similar to *Backward kill line restricted*, but a negative argument has no
effect.

#### Delete from selection (S-C-DEL)
1. Perform *Kill line restricted*.
2. Remove every subeq to the right of the cursor using PVOIDs if needed to
keep intact the structure of supeqs of selection (no flat).

> **Note**: Destroying equation structure is quite unrelated to simple notion
> of "kill line" so it has been avoided.

#### Delete before selection (S-C-BACKSPACE)
1. Perform *Backward kill line restricted*.
2. Remove every subeq to the right of the cursor using PVOIDs if needed to
keep intact the structure of supeqs of selection (no flat).

#### Flat block (C-j)
*   If selection is a symbol, do nothing.
*   Else, let selection be a block B:
    *   If every param of B is a PVOID:
        *   If B is juxted, vanish B.
        *   Else, substitute B with a PVOID.
    *   Elif B has one and only one non-PVOID par, substitute B with that par.
    *   Else:
        *   If B is a juxted, join every non-PVOID B-param in a TJUXT-block
            and substitute B with it.
        *   Else, join every non-PVOID B-param in a PJUXT-block and substitute
            B with it.

#### Flat supeq (M-j)
Identical to *flat block*, but applied to the usupeq of selection instead.

With a positive numeric argument n, it acts on the n-ulevel usupeq of
selection. With a non-positive numerical argument -n, it acts on the n-ulevel 
usubeq of selection (M-0 SHIFT-C-w is identical to M-\\).

#### Recursively flat block (S-C-j)
Similar to *flat block*, but the procedure is applied before to each parameter
(and before to the parameters of its parameters if they exist, and so on)
of selected block. As a result, selection is replaced by a juxt-block which
contains no blocks at all, only symbols.

#### Recursively flat supeq (S-M-j)
Identical to *recursively flat block*, but applied to the usupeq of selection
instead.

With a positive numeric argument n, it acts on the n-ulevel usupeq of
selection. With a non-positive numerical argument -n, it acts on the n-ulevel 
usubeq of selection (M-0 C-h is identical to SHIFT-BACKSPACE).

#### Recursively void block (S-C-u)
*   If selection is a symbol, do nothing.
*   Else, substitute every juxt-block or non-juxted symbols of selection with
    PVOIDs, starting from the highest nesting level.

> **Note**: The "recursive" word is used here for the name of the command with
> keybinding including "\\", contrary to the previous case, but it seems the
> most appropriate naming.

#### Recursively void supeq (S-M-u)
Identical to *recursively void block*, but applied to the usupeq of selection
instead.

#### Void block (S-C-k)
*   If selection is a symbol, do nothing.
*   Else, substitute every parameter of selection (if selection is a block B,
    it refers to whole B-pars) with a PVOID.

#### Void supeq (S-M-k)
Identical to *void block*, but applied to the usupeq of selection instead.

#### Uppercase (In text mode: C-u)
Uppercase letter to the right of the cursor.

#### Lowercase (In text mode: C-l)
Lowercase letter to the right of the cursor.

#### Uppercase word (In text mode: M-u)
Uppercase every letter in supeq.

#### Lowercase word (In text mode: M-l)
Lowercase every letter in supeq.

#### Capitalize word (In text mode: S-C-u)
Capitalize the first symbol which has sense of selection.

#### Switch case (In text mode: S-C-l)

## Gsymb-size operations
Operations in this section act on subequations which are gsybs of supeqs of
them. These operations may act on higher level supeqs if a numeric argument is 
passed.

The intention of these operations is to imitate Readline default bound
commands as much as possible. We will use Readline's command names with
the following equivalence:

*   characters -> gsymbs
*   words -> 1-ulevel usupeq US of a gsymb and closest mates of US

When a gsymb is selected, operation performed is intended to be similar to the
equivalent one of the readline command. If an equation that is not a gsymb is
selected, the first gsymb of selection is considered, which is known in the
 descriptions as **effsel** (effective selection). Exceptions:
*   If orimode and first gsymb of selection is a PVOID, consider it with dir V.
*   If direction is R, consider last gsymb of selection, dir being V or R
    depending whether the gsymb is a PVOID or not.

Outdated:

There are also some commands which behaves differently. In those cases, full
details are included in their description. For example, commands nouns
ending in "_sel" are variants of another command with the same noun except not 
ending in "_sel". They are never readline commands, but inspired by them. The 
difference with respect to the base command is noticeable when selection is not
a gsymb.

### Changing selection

#### First gsymb (HOME)
Select first gsymb of equation.

#### Last gsymb (END)
Create a TVOID to the right of the last gsymb of equation and select it.

#### Next gsymb (C->)
If selection is not a gsymb, select the first gsymb of selection. Else,
select previous gsymb.

#### Previous gsymb (C-<)
If selection is not a gsymb, select the last gsymb of selection. Else,
select next gsymb.

> To be considered: PBC.

### Editing

#### Transpose gsymbs readline-like ()
*   If there is no gsymb to the left of effsel, do nothing.
*   Elif it is the last gsymb and there is only one gsymb in the equation
    excluding effsel if it is a TVOID, do nothing.
*   Elif it is the last gsymb, exchange the positions of last two non-TVOID
    gsymbs. In addition, if orimode, select last gsymb with R; else, select
    a last TVOID, creating it if needed.
*   Else, exchange positions of gsymbs at both sides of the cursor and
    forward_char.
     
> **Temporal note**: Description may have inaccuracies and may be simplified.

#### Yank nth arg ()
Insert the first non-PVOID 1-ulevel usubeq of usupeq. With an argument n, 
insert the nth non-VOID 1-ulevel usubeq of usupeq. If it is 0, insert the lop
of usupeq with empty pars. If it is negative, insert the nth non-VOID 1-ulevel
usubeq starting from the end and without counting the last non-void 1-ulevel
usubeq.

> **Note**: To insert the last 1-ulevel usubeq, it is possible to use
> *Yank last arg* (see below).
#### Yank last arg ()
Insert the last non-VOID 1-ulevel usubeq of usupeq. With a numeric argument it
is equivalent to yank-nth-arg. Successive calls to yank-last-arg consider
usupeqs of higher level. A negative numeric argument provided to successive
calls invert the nesting direction. It is, first negative argument provided
will result in using the (N-1)-ulevel usupeq instead of the (N+1)-ulevel
usupeq. Next time that a numerical argument is passed the (M+1)-ulevel usupeq
is considered instead of the (M-1)-ulevel usupeq. If no supeqs are available
in requested direction, previous insertion is not modified.

## Shortcuts to insert specific subequations

### Complete (double click, right click and select in menu)
Display a graphical window equivalent to the one for building the selected
subequation when pressing a button in the pannel. If it is not available,
use possible-completions instead.

> **Note**: C-i is used by default for 'complete' command in readline. C-i
> is used in VE as an alternative to C-x.
### Possible completions (C-SPACE/S-C-SPACE, right click and select in menu)
List in a graphical window the possible variations of the selected subequation.
You can choose one using the mouse or cursor keys and RETURN, C-j or C-m.
To abort, use ESC or a key binding associated to abort.

### Insert completions
Not used.

> **Note**: Default keybinding, M-*, is used to introduce productories.
### Menu complete ()
Replace selection with a variation. Repeated execution of the command steps
through the list of possible variations, inserting each match in turn. At
the end of the list, the original subequation is restored. An argument of
n moves n positions forward in the list of possible variations. A negative
argument moves backward through the list.

After an insertion, it always acts on inserted subeq.

> **Note**: This command is unbounded by default in readline.

> **Mnemonic**: '@' looks like a modified form of 'a'.


### Insert Greek letter (C-g letter/C-g S-letter/M-g letter)
To insert a Greek letter, press `C-g` and then the Latin letter associated to
requested Greek letter (equivalence table can be found below). For example,
to introduce *alpha*, (typed α), use `C-g a`. If there is an uppercase version
of the Greek letter, it can be introduced by inserting the Latin key uppercase
(by pressing SHIFT at the same time or with CAPSLOCK turned on, as reasonable).
Some Greek letters have a variant. They can be introduced by metafying the
associated Latin letter. For example, to introduce the version of epsilon
similar to a reversed 3 (typed as ε), use `M-g e`. If keybinding does not
have a Greek letter associated, nothing is printed. However, if a digit is
passed it is inserted literally (`C-g 3` inserts digit 3).

> **Note**: Table of equivalence has been designed to maximize the
> similarities between Latin and Greek letters, but it is just an artifact
> to force a useful map between them, sometimes based exclusively in the
> shape of the glyphs.

|   | C-g          | C-g S-       | M-g            |
|---|--------------|--------------|----------------|
| a | α (alpha)    | A            |                |
| b | β (beta)     | B            |                |
| c | χ (chi)      | X            |                |
| d | δ (delta)    | Δ (Delta)    |                |
| e | ϵ (epsilon)  | E            | ε (varepsilon) |
| f | ϕ (phi)      | Φ (Phi)      | φ (varphi)     |
| g | γ (gamma)    | Γ (Gamma)    | Ϝ (digamma)    |
| h | η (eta)      | H            |                |
| i | ι (iota)     | I            |                |
| j |              |              |                |
| k | κ (kappa)    | K            | ϰ (varkappa)   |
| l | λ (lambda)   | Λ (Lambda)   |                |
| m | μ (mu)       | M            |                |
| n | ν (nu)       | N            |                |
| o | ω (omega)    | Ω (Omega)    | (*)            |
| p | π (pi)       | Π (Pi)       | ϖ (varpi)      |
| q | θ (theta)    | Θ (Theta)    | ϑ (vartheta)   |
| r | ρ (rho)      | P            | ϱ (varrho)     |
| s | σ (sigma)    | Σ (Sigma)    | ς (varsigma)   |
| t | τ (tau)      | T            |                |
| u | υ (upsilon)  | Υ (Upsilon)  |                |
| v | v            |              |                |
| w | w            |              |                |
| x | ξ (xi)       | Ξ (Xi)       |                |
| y | ψ (psi)      | Ψ (Psi)      |                |
| z | ζ (zeta)     | Z            |                |

(*) At some point omicron may be introduced as the variant for `o`, but it
does not seem a default in standard LaTeX packages.

An alternative way of inserting Greek letters is to use M-@ to switch between
Latin and Greek alphabet (at least under the same rules than the table above,
but it may be more flexible).

### Greek-lock (S-M-g)
This operation allow to introduce several Greek letters using only one
keystroke instead of two. To unlock it, use the keybinding again, or ESC.

For example, to introduce the first four Greek letters and then the first four
Latin letters you can type `M-C-g a b g d M-C-g a b c d`.

### Insert math element (C-m)
It is intended to remap letters to mathematical symbols and operators. The map
has not been yet defined though. One idea is that Latin (and/or Greek) be
accessible through CONTROL/META/SHIFT combinations.

### Math-lock (S-M-m)
This operation allow to *Insert math element* using only one keystroke instead 
of two. To unlock it, use the keybinding again, or M-C-u.

### Self insert (a, b, A, 1, !, ...)
Insert the character typed. In some cases such as ~ or SPACE, a special
character is inserted instead (TODO: be more specific). In some cases,
quoted-insert may be needed to insert some special symbols.

### Separate subeqs (SPACE)
Insert or increase a region "without" subequations.

### Bring subeqs closer (S-SPACE)
Reduce a region "without" subequations or delete it.

> **Temporal note**: They can be implemented as a symbols, not an operator.
> That way there is no need of a non-user op. It may be also a property as
> color.
>
### Subscripts/superscripts/both (C-l/C-h/S-C-l, S-C-h)
Include an empty subscript or superscript, or select it if it already exists.
If both are specified, the script associated to the key is selected.

> **Note**: 'l' stands for 'low'. 'h' stands for 'high'.

### Backward subscripts/superscripts/both (M-b/M-p/S-M-b, S-M-p)
Include an empty backward sub/super-script, or select it if it already exists.
If both are specified, the script associated to the key is selected.

> **Note**: 'b' stands for 'sub'. 'p' stands for 'sup'.

### Undersets/oversets/both (M-l/M-h/S-M-l, S-M-h)
Add an under or over-set (a subequation exactly under/over another
subequation), or select it if it already exists. If both are specified, the
the set associated to the key is selected.

### Functions (Idea: ,)
First time is cosinus, then sinus then... The symbol version matches every 
function and the operator versions match functions which can have arguments.

> **Mnemonic**: Arguments of functions are separated by commas where they are
> presented as a list inside parenthesis.
### Square root/Generic root (C-r/S-C-r, Idea: %)
First time is a square root, next time is generic.

> **Mnemonic**: '%' looks like a generic root with its arguments, only
> lacking part of the main glyph.

### Summatory (Idea: M-+, M-C-+)
Successive keystrokes of the operator versions modify the number and position 
of the args.

> **Mnemonic**: 'M' looks like a rotated summatory.

### Productory (Idea: C-\*, M-\*, M-C-\*)
Similar to summatory.
### Integral (C-i, Idea: C-$, M-$, M-C-$)
Similar to summatory.

> **Mnemonic**: '$' looks like an integral if the vertical var is not
> considered.
>
### Fraction (C-f, Idea: C-/, M-/, M-C-/)
There are several types of fractions.

The symbol version introduce may introduce a fraction-like symbol.
### Equal-like symbols (Idea: C-=)
### Multi-line equations (Idea: M-=, M-C-=)
Some versions may include equals and other useful things that avoid typing
and provide a visual idea of the possibilities.

> **Mnemonic**: Usually multiline equations are connected with the = sign.
### "Less than"-like symbol (Idea: C-<)
### "Bigger than"-like symbol (Idea: C->) 
### Pair of delimiters (Idea: C-), M-), M-C-))
The symbol version introduces a pair of independent delimiters of the same
size.

It can be accelerated providing a character identified with the delimiter.
### Matrices (Idea: M-(, M-C-()
### Equation system (Idea: M-{, M-C-{)
A digit modifies the number of equations.

> **Mnemonic**: Glyph enclosing equations in a equation system looks like a
> '{'.
### Brace-like (Idea: M-}, M-C-})
> **Mnemonic**: Usual braces looks like a rotated '{'.
### Arrows (Idea: C-~)
> **Mnemonic**: '~' looks like a curved arrow without head.
### Hat-like decorators of fixed size (Idea: M-\_, M-C-\_)
> **Mnemonic**: '_' is straight, which gives an idea of something constant.
### Hat-like decorators of variable size (Idea: M-\~, M-C-\~)
> **Mnemonic**: '~' is curved, which gives an idea of being adaptable.
### Small operators (Idea: M--)
> **Mnemonic**: '+' and '*' stand for big operators. '-' reduces something,
> in this case the size of the operators.
### Font colors (Idea: M-&, M-C-&)
### Bold (C-b, M-b)
Switch bold to symbol (C-b) or supeq (M-b). 
### Mathbb (S-C-b, S-M-b)
Switch mathbb to symbol (S-C-b) or supeq (S-M-b). 
### Background colors (Idea: C-!, M-!)
> **Mnemonic**: '!' indicates something important. Background colors increase
> importance of an equation. 
### Special text (Idea: C-., M-C-.)
It is a symbol-like key binding because a windowed dialog will always appear 
and modification of the text will require a special dialog.

> **Mnemonic**: A dot is used to finish a "text" sentence.

> **Note**: M-. is used for an advanced operation not related with special
> texts (yank-last-arg).

## Other operations found in readline
WIP!!!
### Display keybinding command name ()
Display in the status bar the name of a command associated to next pressed
keybinding.
### start-kbd-macro ()
Begin saving the characters  typed  into  the  current  keyboard
macro.
### end-kbd-macro ()
Stop saving the characters typed into the current keyboard macro
and store the definition.
### call-last-kbd-macro ()
Re-execute the last keyboard macro defined, by making the  char‐
acters  in  the  macro  appear  as  if  typed  at  the keyboard.
print-last-kbd-macro () Print the last keyboard macro defined in
a format suitable for the inputrc file.

### re-read-init-file ()
Read a configuration file.
### abort ()
Abort the current editing command. It does not ring.

> **Note**: Any unrelated key will abort a composed command. In particular,
> ESC. ESC will also abort an incremental search.

> **Note**: M-C-g, a default readline keybinding for *Abort*, has been
> requisitioned.

### prefix-meta ()
Metafy the next character typed.

> **Note**: Any unrelated key will abort a composed command. In particular,
> ESC. ESC will also abort an incremental search.
### undo ()
Incremental undo, separately remembered for each equation.

### set-mark ()
Set the mark to the point. If a numeric argument is supplied,
the mark is set to that position.

> **Note**: M-SPACE is reserved by many desktops, sticking to C-@.
### exchange-point-and-mark ()
Swap  the  point  with the mark.  The current cursor position is
set to the saved position, and the old cursor position is  saved
as the mark.
### character-search ()
A character is read and point is moved to the next occurrence of
that character. A negative count searches for  previous  occurrences.
### character-search-backward ()
A character  is  read and point is moved to the previous occurrence of that 
character. A negative count searches for subsequent occurrences.
### Default mode (Idea: ESC)
Set default mode from any other mode (vi mode, Greek-lock, Math-lock...).

> **Mnemonic**: The u stands for *user* mode, because it returns to keybindings
> specified by the user, which are the default ones if they have not been
> modified.
### vi-editing-mode (Idea: M-C-j, M-C-m)
When  in  emacs editing mode, this causes a switch to vi editing
mode.

> **Temporal note**: vi-mode functionality is not a priority by the moment.

## Appendix A: Shortcuts of desktops/windows managers which should be respected
(**) = "Keybindings similar to the referred one are avoided. By similar
 keybindings it means all those which share what is not enclosed in
 parenthesis or a restricted subset defined after the symbol **."
 
> **Notes**:
>* Many M-MOUSECLICK actions are probably reserved.
>* M-SPACE, M-C-DEL, and keybindings including M-TAB, SUPER, PRINT are not
> included. 
>* F\[1-12\] will not be used as part of any key combinations, only by
> themselves.
 
### XFCE
*   M-C-d (noticeable!)
*   M-C-(UP) (** restricted to cursor keys)
*   M-INS (Insert workspace)
*   M-DEL (Delete workspace)
*   M-C-DEL (Lock screen)
*   S-M-PAGEUP
*   S-M-PAGEDOWN
*   M-C-HOME
*   M-C-END
*   M-C-(1) (** resticted to keys from 1 to 0)

### GNOME
*   SHIFT-M-C-R (noticeable!)
*   M-ESC

### KDE
*   M-C-a (noticeable!! activities-related)
*   M-C-d (noticeable!! show-desktop)
*   M-C-k (noticeable!! keyboard-related)
*   M-C-l (noticeable!! lock-session)
*   M-C-r (noticeable!! clipboard-related)
*   M-C-v (noticeable!! clipboard-related)
*   M-C-x (noticeable!! clipboard-related)
*   C-TAB (noticeable!! It seems used by KDE apps, but I think it is free)
*   C-ESC
*   M-C-ESC
*   M-C-(RIGHT) (** restricted to cursor keys)
*   SHIFT-M-C-DEL
*   SHIFT-M-C-PAGEUP
*   SHIFT-M-C-PAGEDOWN

### LXQT/Openbox
*   M-C-l (noticeable!!)
*   M-C-t (noticeable!!)
*   M-C-(LEFT) (** restricted to cursor keys)
*   SHIFT-M-(LEFT) (** restricted to cursor keys)
*   M-ESC

### Others
*   ...
