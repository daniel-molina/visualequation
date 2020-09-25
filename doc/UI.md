# User Interface

> **Note**: At least part of some operations should be presented
> in some way that a casual user is someway "forced" to know about them.
> An initial window with tips or a dropdown are possibilities.

## Introduction to keybindings
Navigation, edition and other equations-related operations are classified into
desktop-like and terminal-like operations.

Since subequations can be arbitrarily nested, contrary to characters in a
line or document, an equivalence must be set. The concept of mates of a
subequation is a powerful tool to flat its equation. Desktop-like operatios
will be based on that idea, being the subequation of interest current
selection or its supeq.

Previous partition of an equation in mates depends on a chosen subequation
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
Visual Equation, you can equivalently use `M-g`. For example, to introduce 3
ten times you can type: `M-1 0 M-g 3`.

`M--` starts a negative argument. For example, `M-- M-2 C-f` passes argument -2
to operation associated to keybinding `C-f`. If no number is added after
`M--`, -1 is passed implicitly.

## Selection-independent operations

**Saved equations** can be accessed like previous commands on the history of a
shell. In addition, saved equations can have an associated name, categories
and subcategories (arbitrarily nested), but it is not mandatory.

Not to confuse "saved equations" with "exported equations".

Exported equations are equations that can be accessed outside Visual Equation.
Current formats to export equations are PNG, EPS, SVG and PDF. On the contrary,
saved equations are stored in a database which only Visual Equation is
intended to use. There are a lot of different commands to save equations.

Details on shell-like operations.

### Quit (C-q)
Exit Visual Equation with a confirmation dialog.

> **Note**: C-q has a long tradition in many desktops to quit programs, so it
> has been requisitioned to readline. M-q is used instead for that, even if
> the meaning is quite different (except when followed by a number).

### Quit without dialog (C-d)
Exit Visual Equation if equation is a PVOID, discarding the kill ring and the
undo list. It never asks for confirmation to quit.

### Export equation (C-p)
Export an equation (saved or not) to an image, specifying its size, format
and other details.

It is possible to recover equations for further edition from exported equations
in PNG and PDF format.

> **Note**: C-p is a usual keybinding for "printing", so it seems convenient
> for exporting since probably nobody is interested in really printing single
> equations.

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

### New equation (C-n)
This is desktop-like operation but it is placed in this section to help the
reader have a big picture.

It ask the user if it is desired to save current equation. In the positive
case, the usual dialog to save equation is presented. After that, a new empty 
equation is presented for edition.

### Accept line (C-j, C-m)
This a non-windowed version of *Save as...*.
Specify a name and save current equation as a new equation with that name. 
After that, a new empty equation is presented for edition.
It is possible to specify a category in the form
`[category[/subcategory[/...]]/]name`. To accept the name press again C-j or 
C-m or RETURN.
**Note**: C-j acts differently while searching in the history. See below.

### Insert comment (M-#)
Save current equation at the end of the history list (as a new equation)
and start editing a new empty equation. This is a fast accept-line that does
not ask the user for an equation name nor categories to include in the save.
With a numeric argument, it is equivalent to accept_line.

### Save without dialog (S-C-j, S-C-m)
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

### Previous saved equation (PAGEUP)
*Save withoud dialog* displayed equation and fetch the previous equation from
the history list, moving back in the list.

> **Note**: Default readline keybinding is C-p.
### Next saved equation (PAGEDOWN)
save-no-window displayed equation and fetch the next equation from the 
history list, moving forward in the list.

> **Note**: Default readline keybinding is C-n.

### Beginning of history (M-<)
save-no-window displayed equation and fetch the first equation in the
history.
### End of history (M->)
save-no-window displayed equation and fetch the last equation of the history.

### Reverse search history (C-r)
save-no-window current equation and search backward starting at the current
equation and moving up through the history as necessary. This is an 
incremental search. You can introduce part of the name, category or other 
fields (TODO: specify). You can fetch the equation with C-j. Any
other key combination will fetch the equation and then apply the command
to the equation.

### Forward search history (SHIFT-C-r)
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

### Select all (C-a)
This keybinding has a long tradition in graphical applications, so it is
respected even if it collides with an important shortcut of readline.

### Clear screen (C-l)
Remove the whole equation. Undo command would restore previous eq.

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

### Modes

There are three operation modes which, in some cases, operates differently when
the same input is processed by the program. They are:

*   Oriented insertion mode (orimode)
*   Insertion mode (imode)
*   Overwrite mode (ovmode)

They can be switched by pressing C-\[. INS always set/unset overwrite mode. If
unsetting, it will set the mode that was set before setting overwrite mode.

> **Note**: DEL or BACKSPACE will flat supeq when every parameter of supeq is a
> PVOID. This avoids unexpected results for the inexperienced users and, at the
> same time, allows a naive way to delete the supeq "from inside". Typical use
> of DEL and BACKSPACE is, however, specific of the mode. They are detailed
> below.

#### Oriented insertion mode (orimode)

Characteristics:

*   Subequations are selected in an oriented fashion, unless selected subeq
    is a PVOID.
*   If the cursor is to the right of selected subeq, direction of selection is
    R. If the cursor is to the left of the selected subeq, direction is
    L. If a PVOID is selected, direction is V.
*   Insertion is done to the right of the cursor if R or L. If V,
    insertion is really a replacement in which the VOID is substituted.
*   DEL deletes the subeq to the right of the cursor, if it exists.
*   BACKSPACE deletes subeq to the left of the cursor, if it exists.
*   In both cases deleted subeq can be the selected one, depending on the
    orientation.

#### Insertion mode (imode)

*   Selections cannot be oriented. The cursor is always to the left of 
    selection. Direction is always the same, I.
*   Insertions introduce subeqs to the right of the cursor.
*   DEL deletes selection.
*   BACKSPACE deletes the subeq to the left.


#### Overwrite mode (ovmode)

*   It is equivalent to *insert mode* except for insertions (honoring graphical
    overwrite mode in texts editors, but not readline's version where BACKSPACE
    replaces with a white space).
*   Inserted subeqs substitute selection.

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

## Selection-size operations
Operations in this section act on subequations which sizes are related to the
size of current selection. For example the selection itself, its mates,
1-level subeqs and 1-level supeq. These operations may act on higher level
subeqs or supeqs if a numeric argument is passed.

### Changing selection

#### overwrite-mode (INS)
This command switch from normal mode into overwrite mode and from overwrite
mode into normal mode.

The exact behavior is intuitive but is cumbersome to explain. It involves
decisions regarding directions, TVOIDs and selections.

Overwrite mode is more similar to the behavior of graphical editors than the
one of readline. In particular, backward delete does not create an "empty 
space" but totally removes the previous "character". One difference with any 
common overwrite mode is that inserting without a movement never trespass a 
supeq but in text editors eventually words delimiters are overwritten and
several words become a single one.

#### change_dir (C-()
This is not a readline command.

In orimode, it turns L into R and R into L. If V, it remembers previous 
direction if the next command does not force a direction.

> **Note**: Same effect can be alternatively done with the appropriated cursor
> key *LEFT* or *RIGHT*.
#### change_mode (C-[)
This is not a readline command.

Alternate between modes.

> **Note**: Mode can be alternatively set by clicking in the status bar.

#### Select one more or less juxted (S-LEFT/S-RIGHT):

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

#### Select many more or less juxteds (S-C-LEFT/S-C-RIGHT)
*   If selection is a juxted, select that and all its cojuxteds to the
    left/right, using a TJUXT-block if needed.
*   Else, select supeq. In addition, if orimode, set dir to L/R.

It must be equivalent to use S-LEFT/S-RIGHT once or more times, so
further details may apply.

#### Select usupeq (S-UP, M-p)
Select usupeq if it exists. Do not change dir unless it is V. In that case, set
R. It resembles the GUI notion of using SHIFT to extend current selection.

#### Select first param (S-DOWN, M-a)
Select first 1-ulevel usubeq of selection if it exists and is selectable.

Do not change dir unless required by a PVOID.
It resembles the GUI notion of using SHIFT to shrink current selection and
also that DOWN does not always go to the start of the next line. Of course,
SHIFT-DOWN per se would extend selection and not shrink it in reasonable text
editors.

#### Select last param (M-e)
Select last 1-ulevel usubeq of selection, if it exists and is selectable.
Do not change dir unless required by a PVOID.

#### Select closest mates (C-LEFT/C-RIGHT)
These key bindings are used to navigate between mates.

> **Notes**:
>*  CONTROL is preferred for "word movements" instead of ALT in basic
>   operations because they are commonly used by desktop applications with that
>   meaning.
>
>*  The behavior does more honor to gedit and equivalent readline key 
>   combination than to kwrite (considering that mates are words) because
>   final selection shares orientation with the key. 
>
>*  On the contrary, advanced movements will consider that mates are characters
>   and their supeqs are words.

When using C-LEFT/C-RIGHT:
*   The mate to the left/right of selection is selected without changing dir.
    Marginal case: If selection is the first/last mate, choose the last/first
    mate.
*   Successive keystrokes of these key combinations (valid for an interleaved
    use of them) will remember the N-mate level of the selection before 
    applying the first of these key combinations.

> **Note**: Successive keystrokes of the same class will remember the mate
> ulevel if needed.

#### Create/Delete groups (C-RETURN)

A group makes strict usubeqs of selected block not selectable. It has no
effect if selection is a symbol.

> **Note**: If an existing soft group (see below) is grouped, it will become
> again a soft group if it is ungrouped.

#### Create/Delete soft groups (S-RETURN)

A soft group is a juxt-block that is a juxted of another juxt-block.

To create a soft-group, select together the desired juxteds by using
SHIFT-LEFT or SHIFT-RIGHT before using they key binding.

> **Note**: There may be an option to create soft groups automatically when
> inserting sequences of digits.

#### Selecting further subeqs

> **Note**: Successive keystrokes of the same class will remember the mate
> ulevel if needed.

If selection is the whole eq, do nothing.
Else, consider that supeq of selection is called SUP.

##### Select first par of mate to the right of supeq (TAB)
*   If SUP has a mate to the right RSUP, select the first param of RSUP.
*   Elif SUP has at least one mate to the left, select the first param of the
    first mate of SUP.
*   Else, select the first param of SUP.

##### Select first par of mate to the left of supeq (S-TAB)
*   If selection is not the first param of SUP, select the first param of SUP.
*   Elif SUP has a mate to the left LSUP, select the first param of LSUP.
*   Elif SUP has at least one mate to the right, select the first param of the
    last mate of SUP.
*   Else, do nothing.

##### Select last par of mate to the right of supeq (C-TAB)
*   If selection is not the last param of SUP, select the last param of SUP.
*   Elif SUP has a mate to the right RSUP, select the last param of RSUP.
*   Elif SUP has at least one mate to the left, select the last param of the
    first mate of SUP.
*   Else, do nothing.

##### Select last par of mate to the left of supeq (S-C-TAB)
*   If SUP has a mate to the left LSUP, select the last param of LSUP.
*   Elif SUP has at least one mate to the right, select the last param of the
    last mate of SUP.
*   Else, select the last param of SUP.


### Editing

#### Cut (C-x)

Remove selected subeq and save/overwrite VE's clipboard.
 
This shortcut is a an important key combination for emacs and readline, but by
default the desktop tradition will be respected.

#### Copy (C-c)

Save/overwrite VE's clipboard with selection.

#### Paste (C-v)

Insert VE's clipboard (in overwrite mode, selection is replaced).

#### Undo (C-z)

Undo last manipulation, if it exists.

#### Redo (S-C-z)

Redo last manipulation, if it exists.

#### Crop selection (SHIFT-C-l)
Substitute equation with selection. Undo command would restore previous eq.

#### Delete coparams (C-DEL)
If selection is a juxted remove all the juxteds of the same PJUXT-block to the
right of the cursor.

If selection is not a juxted, substitute pars of lop-block to the right of the
cursor by PVOIDs.

If there is nothing to remove, lop-block is flatted.

Killed subeq is saved on the kill-ring.

> **Note**: Successive keystrokes of the same class will remember the mate
> ulevel if needed.

#### Backward delete coparams (C-BACKSPACE) 

If selection is a juxted remove all the juxteds of the same juxt-block to the 
left of the cursor

If selection is not a juxted, substitute pars of lop-block to the left of the
cursor by PVOIDs.

Killed subeq is saved on the kill-ring (see related shell-like section).

> **Note**: Successive keystrokes of the same class will remember the mate
> ulevel if needed.

#### Transpose forward (M-RIGHT)

Swap positions of current selection and its mate to the right, leaving original
selection selected.

No direction is changed.

Marginal case: If there is no mate to the right, do nothing.

> **Note**: Successive keystrokes of the same class will remember the mate
> ulevel if needed.

#### Transpose backward (M-LEFT)

Swap positions of current selection and mate the left, leaving original
selection selected.

No direction is changed.

Marginal cases:
*   If selection is a TVOID, swap the closest two mates to the left if they 
    exist. Else, do nothing.
*   If there is no mate to the left, do nothing.

> **Note**: Successive keystrokes of the same class will remember the mate
> ulevel if needed.

#### Destroy line (SHIFT-C-DEL)
Delete every mate from the cursor to the right. Those which cannot be totally
removed without flatting blocks will have their lops flatted. Use C-k if you
prefer to keep the structure by replacing subeqs by PVOIDs instead of flatting.

Killed subeq is saved on the kill-ring.

> **Note**: The flattening effect is forced here because it is a complex
> command (three keys involved) instead of two as in C-k.

#### Backward destroy line (S-C-BACKSPACE)
Delete every mate from the cursor to the left. Those which cannot be totally
removed without flatting blocks will have their lops flatted. Use C-u if you
prefer to keep the structure by replacing subeqs by PVOIDs instead of flatting.

Killed subeq is saved on the kill-ring.

> **Note**: The flattening effect is forced here because it is a complex
> command (three keys involved) instead of two as in C-u.

#### Delete usupeq (M-C-w)
If supeq is a juxted, vanish it (with all its subeqs). Else, replace it with a
PVOID.

Killed subeq is saved on the kill-ring (see related shell-like section).

> **Note**: Keybinding is inspired by readline command unix-word-rubout (C-w),
> which is quite related to this action. C-w is in fact a very good option for
> the keybinding due to the simplicity of the keystroke and the operation.
> However it was assigned to M-C-w for the sake of the mnemonic (this command 
> is equivalent to M-w C-w, each one described below). In case of supeq being 
> an empty block, as they are when recently created, command associated to C-w
> achieves the same result than this command.

> **Note**: See also C-BACKSPACE and M-C-?/M-C-h which are more like the
> original command and its alternative, backward-kill-word.

#### Flat block (M-\\)
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

#### Flat supeq (S-C-w)
Identical to *flat block*, but applied to the usupeq of selection instead.

With a positive numeric argument n, it acts on the n-ulevel usupeq of
selection. With a non-positive numerical argument -n, it acts on the n-ulevel 
usubeq of selection (M-0 SHIFT-C-w is identical to M-\\).

#### Recursively flat block (S-BACKSPACE)
Similar to *flat block*, but the procedure is applied before to each parameter
(and before to the parameters of its parameters if they exist, and so on)
of selected block. As a result, selection is replaced by a juxt-block which
contains no blocks at all, only symbols.

#### Recursively flat supeq (C-w)
Identical to *recursively flat block*, but applied to the usupeq of selection
instead.

With a positive numeric argument n, it acts on the n-ulevel usupeq of
selection. With a non-positive numerical argument -n, it acts on the n-ulevel 
usubeq of selection (M-0 C-w is identical to SHIFT-BACKSPACE).

#### Recursively void block (C-\\)
*   If selection is a symbol, do nothing.
*   Else, substitute every symbol of selection (included symbols of parameters
    of selection if they are blocks, and so on) with PVOIDs.

> **Note**: The "recursive" word is used here for the name of the command with
> keybinding including "\\", contrary to the previous case, but it seems the
> most appropriate naming.

#### Recursively void supeq (S-M-w)
Identical to *recursively void block*, but applied to the usupeq of selection
instead.

With a positive numeric argument n, it acts on the n-ulevel usupeq of
selection. With a non-positive numerical argument -n, it acts on the n-ulevel 
usubeq of selection (M-0 SHIFT-M-w is identical to C-\\).

#### Void block (S-DEL)
*   If selection is a symbol, do nothing.
*   Else, substitute every parameter of selection (if selection is a block B,
    it refers to whole B-pars) with a PVOID.

#### Void supeq (M-w)
Identical to *void block*, but applied to the usupeq of selection instead.

With a positive numeric argument n, it acts on the n-ulevel usupeq of
selection. With a non-positive numerical argument -n, it acts on the n-ulevel 
usubeq of selection (M-0 M-w is identical to SHIFT-DEL).

#### Rotate copars to the left (M-UP)
#### Rotate copars to the right (M-DOWN)

> **Note**: First param is chosen instead of first one for symmetry with
> *Select first param* (SHIFT-DOWN).

#### Transmute with subeq (S-C-t)
It is not a readline command.

If selection is a block B and its last parameter is a block BSUB, exchange
lop-B and lop-BSUB, removing excess of parameters and including PVOIDs as 
needed.

#### Transmute with supeq (S-M-t)
It is not a readline command.

If selection is a block B and has a supeq SUP, exchange lop-B and lop-SUP,
removing excess of parameters and including PVOIDs as needed.

#### Upcase word (M-u)
Uppercase every symbol which has sense (Latin and Greek letters) included in
selection and every mate to the right contained in the supeq of selection. If
supeq does not exists, just in selection.
With a numeric argument, certain mates of the supeq of selection are included.

#### Downcase word (M-l)
Counterpart of *Upcase word*.

#### Capitalize word (M-c)
Capitalize the first symbol which has sense of selection.

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
In orimode, direction will be set to L, or V is symbol is a PVOID.

#### Last gsymb (END, C-e)
In orimode, direction will be set to R, or V if symbol is a PVOID.
Any other mode will create and select a TVOID after the last symbol.

#### First gsymb of selection (SHIFT-C-a)
Select the first gsymb of selection. In orimode, set L if it is not a PVOID.

#### Last gsymb of selection (SHIFT-C-e)
Select the last gsymb of selection. If orimode, set R if it is not a PVOID.
Else, it creates a TVOID.

#### Forward char (C-f)
Select the closest gsymb to the right of effsel. Direction will be changed in
orimode when that is necessary to place the cursor correctly. If not orimode,
TVOIDs, will be created when needed.

#### Alternative forward char (SHIFT-C-f)
Equivalent to forward_char but considering that effsel is in the opposite side
of selection.

> To be considered: PBC.
#### Backward char (C-b)
Counter-part of forward_char.

#### Alternative backward char (SHIFT-C-b)
Counter-part of forward_char_sel.

#### Forward word (M-f)
*   If effsel is not the last gsymb of its usupeq LGU, select LGU.
*   Elif usupeq of effsel has a mate to the right, select its last gsymb.

> To be considered: PBC.
>
> **Note**: Mate ulevel will NOT be retained for successive keystrokes of the
> same type.

#### Backward word (M-b)
Counterpart of forward-word.

#### Alternative forward word (SHIFT-M-f)
Equivalent to forward_word but considering that effsel is in the opposite side
of selection.

#### Alternative backward word (SHIFT-M-b)
Counter-part of forward_char_sel.

### Editing

#### Delete char (C-d)
*   If there is no gsymb to the right of the cursor (supposing effsel is
    selected), do nothing.
*   Elif it is a TVOID, do nothing.
*   Elif it is a last juxted and not orimode, replace it with a TVOID.
*   Elif it is a juxted, vanish it.
*   Elif it is not a PVOID, replace it with a PVOID.
*   Else, do nothing.

> **Note**: This is the most conservative deletion command. It cannot join
> different words as readline equivalent can do, but there are plenty of other
> commands for that task.

> **Note**: C-d executes end-of-file if whole equation is a PVOID.

#### Alternative delete char (S-C-d)
Equivalent to *Delete char* but considering that effsel is in the opposite side
of selection.

#### Backward delete char (C-h)
Counterpart of delete-char (not exactly reciprocal, but it has the same
philosophy and is less complex because it avoids some TVOIDs cases).

> **Note**: Readline calls the key used for this command Rubout, usually
> associated to BACKSPACE and C-?. C-h is also used for this command. Because 
> BACKSPACE is being used in Visual Equation for Selection-size operations and
> C-? require SHIFT being pressed in some keyboard layouts, Visual Equation 
> will stick to C-h.

#### Alternative backward delete char (S-C-h)
Equivalent to *Backward delete char* but considering that effsel is in the
opposite side of selection.

#### Transpose chars (C-t)
*   If there is no gsymb to the left of effsel, do nothing.
*   Elif it is the last gsymb and there is only one gsymb in the equation
    excluding effsel if it is a TVOID, do nothing.
*   Elif it is the last gsymb, exchange the positions of last two non-TVOID
    gsymbs. In addition, if orimode, select last gsymb with R; else, select
    a last TVOID, creating it if needed.
*   Else, exchange positions of gsymbs at both sides of the cursor and
    forward_char.
     
> **Temporal note**: Description may have inaccuracies and may be simplified.

#### Transpose words (M-t)
*   If supeq SUP of selection exists and SUP has a mate to the left, transpose
    them.
*   Else, do nothing.

#### Kill line (C-k)
Kill any subequation after cursor. Those which cannot be deleted totally
without flatting their supeqs are substituted by PVOID (as in *Void block*,
so not recursively).

With a negative argument, kill any subequation before cursor.
#### Backward kill line (C-u)
Counter-part of *Kill line*.

> **Note**: Default readline keybinding is undesired (C-x Rubout), so
> keybinding of a very similar command (*Unix line discard*), which is not
> going to be implemented in Visual Equation, is used instead.

#### Alternative kill line (S-C-k)
Equivalent to *Kill line* but considering that effsel is in the opposite side
of selection.

#### Alternative backward kill line (S-C-u)
Equivalent to *Backward kill line* but considering that effsel is in the
opposite side of selection.

#### Unix line discard (Not to be implemented)
Similar to *Backward kill line*. A negative argument has no effect.

#### Kill word (M-d)
If selection is a juxted of a juxt-block JB and there are juxteds of JB
after the cursor different than TVOID (selection itself may be one of them),
delete every juxted satisfying that condition.
Elif selection is a nested juxted and has a quasi-cojuxted QCJ to the right,
remove QCJ and every cojuxted of QCJ to the right.
Else, set to PVOID every 1-level subeq of the supeq of selection to the
right of the cursor.

Read this:-----

*   If there is no gsymb to the right of effsel, do nothing.
*   Elif gsymb to the right of effsel is a non-last juxted, delete juxted to
 the right.
*   Elif next mate exists and it is not a PVOID, move it to the right of
    selection as a juxted or several juxteds if it was a juxt-block. Leave a 
    PVOID in the original position of the mate.
*   Elif there exists a mate to the right which is not a PVOID, replace the
    (PVOID) mate to the left of that mate with it and leave a PVOID in its
    original position.
*   Else, do nothing.

It saves deleted mates on the kill ring (readline do that when a
numeric argument is passed, even if that is not documented).


#### Backward kill word (M-h, M-C-h)
Counter-part of kill-word.

> **Note**: According to Note of *Backward delete char*, Visual equation will
> stick to M-C-h for the keybinding of this command. Alternatively, M-h is also
> associated to this operation.

#### Alternative kill word (S-M-d)
Equivalent to *Kill word* but considering that effsel is in the opposite side
of selection.

#### Alternative backward kill word (S-M-h, S-M-C-h)
Equivalent to *Backward kill word* but considering that effsel is in the
opposite side of selection.

#### Kill region (Considered to be implemented)
Kill the text between the point and  mark  (saved  cursor  posi‐
tion).  This text is referred to as the region.

#### Yank (C-y)
Yank the top of the kill ring after the cursor.
#### Yank pop (M-y)
Rotate the kill ring, and yank the new top. Only works following *Yank* or
 *Yank pop*.
#### Yank nth arg (M-C-y)
Insert the first non-VOID 1-ulevel usubeq of usupeq. With an argument n, insert
the nth non-VOID 1-ulevel usubeq of usupeq. If it is 0, insert the lop of
usupeq with empty pars. If it is negative, insert the nth non-VOID 1-ulevel
usubeq starting from the end and without counting the last non-void 1-ulevel
usubeq.

> **Note**: To insert the last 1-ulevel usubeq, it is possible to use
> *Yank last arg* (see below).
#### Yank last arg (M-.)
Insert the last non-VOID 1-ulevel usubeq of usupeq. With a numeric argument it
is equivalent to yank-nth-arg. Successive calls to yank-last-arg consider
usupeqs of higher level. A negative numeric argument provided to successive
calls invert the nesting direction. It is, first negative argument provided
will result in using the (N-1)-ulevel usupeq instead of the (N+1)-ulevel
usupeq. Next time that a numerical argument is passed the (M+1)-ulevel usupeq
is considered instead of the (M-1)-ulevel usupeq. If no supeqs are available
in requested direction, previous insertion is not modified.

## Shortcuts to insert specific subequations

> **Temporal Note**:
>
> The following key bindings are used by readline and should not be used,
> unless they are marked as requisitioned.
>
>*  C-@, C-], C-\_, C-?
>*  M-C-\[, M-C-], M-C-?
>*  M-SPACE, M-#, M-& (requisitioned), M-\* (requisitioned), M--, M-., M-digit,
>   M-<, M->, M-?, M-\\, M-~ (requisitioned), M-\_ (requisitioned).

> **Notes**:
>
>*  Every C-... key binding of this section inserts a symbol.
>*  Every M-... key binding of this section inserts an operator with all their
>*  parameters set to VOID.
>*  Every M-C-... key binding of this section replaces selection with an
>   operator which has as first parameter the previous selection and any
>   other it may have set to VOID.
>*  Several keystrokes of the same key binding produce different
>   symbols/operators of common characteristics.

### Complete (double click, right click and select in menu)
Display a a graphical window equivalent to the one for building the selected
subequation when pressing a button in the pannel. If it is not available,
use possible-completions instead.

> **Note**: C-i is used by default for 'complete' command in readline. C-i
> is used in VE as an alternative to C-x.
### Possible completions (M-?, right click and select in menu)
List in a graphical window the possible variations of the selected subequation.
You can choose one using the mouse or cursor keys and RETURN, C-j or C-m.
To abort, use ESC or a key binding associated to abort.

### Insert completions
Not used.

> **Note**: Default keybinding, M-*, is used to introduce productories.
### Menu complete (M-@)
Replace selection with a variation. Repeated execution of the command steps
through the list of possible variations, inserting each match in turn. At
the end of the list, the original subequation is restored. An argument of
n moves n positions forward in the list of possible variations. A negative
argument moves backward through the list.

After an insertion, it always acts on inserted subeq.

> **Note**: This command is unbounded by default in readline.

> **Mnemonic**: '@' looks like a modified form of 'a'.


### Insert Greek letter (M-g char/M-g C-char)
To insert a Greek letter, press `M-g` and then the Latin letter associated to
requested Greek letter (equivalence table can be found below). For example,
to introduce *alpha*, (typed α), use `M-g a`. If there is an uppercase version
of the Greek letter, it can be introduced by inserting the Latin key uppercase
(by pressing SHIFT at the same time or with CAPSLOCK turned on, as reasonable).
Some Greek letters have a variant. They can be introduced by metafying the
associated Latin letter. For example, to introduce the version of epsilon
similar to a reversed 3 (typed as ε), use `M-g M-e`. If keybinding does not
have a Greek letter associated, nothing is printed. However, if a digit is
passed it is inserted literally (`M-g 3` inserts digit 3). In *Introduction*
it is explained why that is useful for numerical arguments.

> **Note**: Table of equivalence has been designed to maximize the
> similarities between Latin and Greek letters, but it is just an artifact
> to force a useful map between them, sometimes based exclusively in the
> shape of the glyphs.

|   | M-g *locase* | M-g *upcase* | M-g M-         |
|---|--------------|--------------|----------------|
| a | α (alpha)    | A            |                |
| b | β (beta)     | B            |                |
| c | χ (xi)       | X            |                |
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

### Greek-lock (M-C-g)
This operation allow to introduce several Greek letters using only one
keystroke instead of two. To unlock it, use the keybinding again, or M-C-u.

For example, to introduce the first four Greek letters and then the first four
Latin letters you can type `M-C-g a b g d M-C-g a b c d`.

### Insert math symbol or operator (M-m)
It is intended to remap letters to symbols and operators. The map has not been
yet defined though. One idea is that Latin (and/or even Greek) letters may be
accessible via some CONTROL/META/SHIFT combinations.

### Math-lock (M-C-m)
This operation allow to introduce math symbols and operators using only one
keystroke instead of two. To unlock it, use the keybinding again, or M-C-u.

### tab_insert
See shortcuts SPACE and SHIFT-SPACE in basic operations.

### self_insert (a, b, A, 1, !, ...)
Insert the character typed. In some cases such as ~ or SPACE, a special
character is inserted instead (TODO: be more specific). In some cases,
quoted-insert may be needed to insert some special symbols.

### Separate subeqs (SPACE)
Insert or increase a region "without" subequations.
A numeric argument fix the width with precision.

### Bring subeqs closer (S-SPACE)
Reduce a region "without" subequations or delete it.

> **Temporal note**: They will be implemented as characters, not operators.
> That way there is no need of a non-user op.
### Subscripts and superscripts (DOWN and UP)
Include an empty sub/super-script or select it if it is already a script.

The sub/super-script will be the one to the left if dir is L or I. If dir is O,
selection will be replaced with a PVOID at the same time the script is
selected (and created if it did not exist).

TAB an SHIFT-TAB after DOWN or UP will modify the position of the recently
created script, including under/over-sets (see below).
### Undersets and oversets (C-DOWN and C-UP)
Add an under/over-set (a subequation exactly under/over another subequation).

TAB an SHIFT-TAB after DOWN or UP will modify the position of the recently
created under/over-set, including scripts.
### Functions (C-,, M-,, M-C-,)
First time is cosinus, then sinus then... The symbol version matches every 
function and the operator versions match functions which can have arguments.

> **Mnemonic**: Arguments of functions are separated by commas where they are
> presented as a list inside parenthesis.
### Roots (M-s, M-C-s, M-%, M-C-%)
First time is a square root, next time is generic.

> **Mnemonic**: '%' looks like a generic root with its arguments, only
> lacking part of the main glyph.

### Summatory (C-+, M-+, M-C-+)
Sucesive keystrokes of the operator versions modify the number and position of
the args.
### Productory (C-\*, M-\*, M-C-\*)
Equivalent to summatory.
### Integral (C-$, M-$, M-C-$)
Equivalent to summatory.

> **Mnemonic**: '$' looks like an integral if the vertical var is not
> considered.
>
### Fraction (M-q, M-C-q, C-/, M-/, M-C-/)
There are several types of fractions.

The symbol version introduce may introduce a fraction-like symbol.
### Equal-like symbols (C-=)
### Multi-line equations (M-=, M-C-=)
Some versions may include equals and other useful things that avoid typing
and provide a visual idea of the possibilities.

> **Mnemonic**: Usually multiline equations are connected with the = sign.
### "Less than"-like symbol (C-<)
### "Bigger than"-like symbol (C->) 
### Pair of delimiters (C-), M-), M-C-))
The symbol version introduces a pair of independent delimiters of the same
size.

It can be accelerated providing a character identified with the delimiter.
### Matrices (M-(, M-C-()
### Equation system (M-{, M-C-{)
A digit modifies the number of equations.

> **Mnemonic**: Glyph enclosing equations in a equation system looks like a
> '{'.
### Brace-like (M-}, M-C-})
> **Mnemonic**: Usual braces looks like a rotated '{'.
### Arrows (C-~)
> **Mnemonic**: '~' looks like a curved arrow without head.
### Hat-like decorators of fixed size (M-\_, M-C-\_)
> **Mnemonic**: '_' is straight, which gives an idea of something constant.
### Hat-like decorators of variable size (M-\~, M-C-\~)
> **Mnemonic**: '~' is curved, which gives an idea of being adaptable.
### Small operators (C--)
> **Mnemonic**: '+' and '*' stand for big operators. '-' reduces something,
> in this case the size of the operators.
### Font colors (M-&, M-C-&)
### Background colors (C-!, M-!)
> **Mnemonic**: '!' indicates something important. Backgroung colors increase
> importance of an equation. 
### Special text (C-., M-C-.)
It is a symbol-like key binding because a windowed dialog will always appear 
and modification of the text will require a special dialog.
However, M-C-. may be considered with care.

> **Mnemonic**: A dot is used to finish a "text" sentence.

> **Note**: M-. is used for an advanced operation not related with special
> texts (yank-last-arg).

## Other operations found in readline
WIP!!!
### start-kbd-macro (C-i ()
Begin saving the characters  typed  into  the  current  keyboard
macro.
### end-kbd-macro (C-i ))
Stop saving the characters typed into the current keyboard macro
and store the definition.
### call-last-kbd-macro (C-i e)
Re-execute the last keyboard macro defined, by making the  char‐
acters  in  the  macro  appear  as  if  typed  at  the keyboard.
print-last-kbd-macro () Print the last keyboard macro defined in
a format suitable for the inputrc file.

### re-read-init-file (C-i C-r)
Read a configuration file.
### abort (C-g)
Abort the current editing command. It does not ring.

> **Note**: Any unrelated key will abort a composed command. In particular,
> ESC. ESC will also abort an incremental search.

> **Note**: M-C-g, a default readline keybinding for *Abort*, has been
> requisitioned.

### prefix-meta (ESC)
Metafy the next character typed.

> **Note**: Any unrelated key will abort a composed command. In particular,
> ESC. ESC will also abort an incremental search.
### undo (C-_, C-i C-u)
Incremental undo, separately remembered for each equation.
### revert-line (M-r)
Undo all changes made to this equation.  This is like executing
the undo command enough times to return the equation to its
initial state.
### set-mark (C-@)
Set the mark to the point. If a numeric argument is supplied,
the mark is set to that position.

> **Note**: M-SPACE is reserved by many desktops, sticking to C-@.
### exchange-point-and-mark (C-i C-i, C-i C-x)
Swap  the  point  with the mark.  The current cursor position is
set to the saved position, and the old cursor position is  saved
as the mark.
### character-search (C-])
A character is read and point is moved to the next occurrence of
that character. A negative count searches for  previous  occurrences.
### character-search-backward (M-C-])
A character  is  read and point is moved to the previous occurrence of that 
character. A negative count searches for subsequent occurrences.
### Default mode (M-C-u)
Set default mode from any other mode (vi mode, Greek-lock, Math-lock...).

> **Mnemonic**: The u stands for *user* mode, because it returns to keybindings
> specified by the user, which are the default ones if they have not been
> modified.
### vi-editing-mode (M-C-j, M-C-m)
When  in  emacs editing mode, this causes a switch to vi editing
mode.

### Copy region as kill (Considered to be implemented)
Copy the text in the region to the kill buffer.

> **Temporal note**: vi-mode functionality is not a priority by the moment.

## Appendix A: Already used keybindings

Legend:
*   X: Used.
*   Y: Used and at least another alternative is provided.
*   U: It auto-inserts upper-case version of character.
*   A: Avoided.
*   S: Left free to avoid collision with desktops/operative system keybindings.
*   ?: Unknown/undecided.

|              | standalone | C- | M- | S- | M-C- | S-C- | S-M- | S-M-C- |
|--------------|------------|----|----|----|------|------|------|--------|
| a            | X          | X  | Y  | U  | S    | X    |      |        |
| b            | X          | X  | X  | U  |      | X    | X    |        |
| c            | X          | X  | X  | U  |      |      |      |        |
| d            | X          | X  | X  | U  | S    | X    | X    |        |
| e            | Y          | X  | X  | U  |      | X    |      |        |
| f            | X          | X  | X  | U  |      | X    | X    |        |
| g            | X          | X  | X  | U  | X    |      |      |        |
| h            | X          | X  | Y  | U  | Y    | Y    | Y    | Y      |
| i            | X          | X  |    | U  |      |      |      |        |
| j            | X          | Y  |    | U  | X    | X    |      |        |
| k            | X          | X  |    | U  | S    | X    |      |        |
| l            | X          | X  | X  | U  | S    | X    |      |        |
| m            | X          | Y  | X  | U  | X    | X    |      |        |
| n            | X          | X  |    | U  |      |      |      |        |
| o            | X          | X  |    | U  |      |      |      |        |
| p            | X          | X  | Y  | U  |      |      |      |        |
| q            | X          | X  | X  | U  | X    |      |      |        |
| r            | X          | X  | X  | U  | S    | X    |      | S      |
| s            | X          | X  | X  | U  | X    | X    |      |        |
| t            | X          | X  | X  | U  | S    | X    | X    |        |
| u            | X          | X  | X  | U  | X    | X    |      |        |
| v            | X          | X  |    | U  | S    |      |      |        |
| w            | X          | X  | X  | U  | X    | X    | X    |        |
| x            | X          | X  |    | U  | S    |      |      |        |
| y            | X          | X  | X  | U  | X    |      |      |        |
| z            | X          | X  |    | U  |      | X    |      |        |
|              | standalone | C- | M- | S- | M-C- | S-C- | S-M- | S-M-C- |
| SPACE        | X          | X  | S  | X  |      |      |      |        |
| RETURN       | X          | X  |    | X  |      |      |      |        |
| TAB          | X          | X* | S  | X  | S    | X    | S    | S      |
| DEL          | X          | X  | S  | X  | S    | X    |      | S      |
| BACKSPACE    | X          | X  |    | X  |      | X    |      |        |
| LEFT         | X          | X  | X  | X  | S    | X    | S    |        |
| RIGHT        | X          | X  | X  | X  | S    | X    | S    |        |
| UP           | X          | X  | X  | Y  | S    |      | S    |        |
| DOWN         | X          | X  | X  | Y  | S    |      | S    |        |
| PAGEUP       | X          | X  |    |    |      |      | S    | S      |
| PAGEDOWN     | X          | X  |    |    |      |      | S    | S      |
| HOME         | X          |    |    |    | S    |      |      |        |
| END          | Y          |    |    |    | S    |      |      |        |
| INS          | X          |    | S  |    |      |      |      |        |
| ESC          | X          | S  | S  |    | S    |      |      |        |
|              | standalone | C- | M- | S- | M-C- | S-C- | S-M- | S-M-C- |
| !            | X          | X  | X  | A  |      | A    | A    | A      |
| "            | ?          |    |    | A  |      | A    | A    | A      |
| #            | X          | X  | X  | A  |      | A    | A    | A      |
| $            | X          | X  | X  | A  | X    | A    | A    | A      |
| %            | X          | X  | X  | A  | X    | A    | A    | A      |
| &            | X          |    | X  | A  | X    | A    | A    | A      |
| '            | X          |    |    | A  |      | A    | A    | A      |
| (            | X          | X  | X  | A  | X    | A    | A    | A      |
| )            | X          | X  | X  | A  | X    | A    | A    | A      |
| *            | X          | X  | X  | A  | X    | A    | A    | A      |
| +            | X          | X  | X  | A  | X    | A    | A    | A      |
| ,            | X          | X  | X  | A  | X    | A    | A    | A      |
| -            | X          | X  | X  | A  |      | A    | A    | A      |
| .            | X          | X  | X  | A  | X    | A    | A    | A      |
| /            | X          | X  | X  | A  | X    | A    | A    | A      |
| :            | X          | X  |    | A  |      | A    | A    | A      |
| ;            | X          | X  |    | A  |      | A    | A    | A      |
| <            | X          | X  | X  | A  |      | A    | A    | A      |
| =            | X          | X  | X  | A  | X    | A    | A    | A      |
| >            | X          | X  | X  | A  |      | A    | A    | A      |
| ?            | X          |    |    | A  |      | A    | A    | A      |
| @            | X          | X  | X  | A  |      | A    | A    | A      |
| \            | X          | X  | X  | A  |      | A    | A    | A      |
| ^            | X          | X  |    | A  |      | A    | A    | A      |
| _            | X          | X  | X  | A  | X    | A    | A    | A      |
| {            | X          |    | X  | A  | X    | A    | A    | A      |
| ¬            | ?          | A  |    | A  | A    | A    | A    | A      |
| }            | X          |    | X  | A  | X    | A    | A    | A      |
| \|           | X          | X  |    | A  |      | A    | A    | A      |
| [            | X          | X  |    | A  |      | A    | A    | A      |
| ~            | X          | X  | X  | A  | X    | A    | A    | A      |
| ]            | X          | X  |    | A  | X    | A    | A    | A      |
|              | standalone | C- | M- | S- | M-C- | S-C- | S-M- | S-M-C- |
| 1            | X          |    | X  |    | S    |      |      |        |
| 2            | X          |    | X  |    | S    |      |      |        |
| 3            | X          |    | X  |    | S    |      |      |        |
| 4            | X          |    | X  |    | S    |      |      |        |
| 5            | X          |    | X  |    | S    |      |      |        |
| 6            | X          |    | X  |    | S    |      |      |        |
| 7            | X          |    | X  |    | S    |      |      |        |
| 8            | X          |    | X  |    | S    |      |      |        |
| 9            | X          |    | X  |    | S    |      |      |        |
| 0            | X          |    | X  |    | S    |      |      |        |
|              | standalone | C- | M- | S- | M-C- | S-C- | S-M- | S-M-C- |
| Left click   | X          | ?  | S  | X  |      |      |      |        |
| Dbl l. click | X          |    |    |    |      |      |      |        |
| Right click  | X          |    |    |    |      |      |      |        |

## Appendix B: Shortcuts of desktops/windows managers which should be respected
(**) = "Keybindings similar to referred one are being avoided, not listing
similar cases for current desktop. Similar keybindings are those those
 sharing what is not enclosed in parenthesis."
 
> **Notes**:
>* Many M-MOUSECLICK actions are probably reserved.
>* M-SPACE, M-C-DEL, and keybindings including M-TAB, SUPER, PRINT or
> F\[1-12\] are not included.
 
### XFCE
*   M-C-d (noticeable!)
*   M-C-(UP) (** restricted to cursor keys)
*   M-INS
*   M-DELETE
*   SHIFT-M-PAGEUP
*   SHIFT-M-PAGEDOWN
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
