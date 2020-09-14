# User Interface

## Manipulating and navigating an equation
Navigation, edition and other equations-related operations are classified into
basic and advanced.

> **Note**: At least part of some operations should be presented
> in some way that a casual user is someway "forced" to know about them.
> An initial window with tips or a dropdown are possibilities.

There are three operation modes which in some cases operates differently when
the same input is sent to the program. They are:

*   Oriented insertion mode (orimode)
*   Insertion mode (imode)
*   Overwrite mode (ovmode)

They can be switched by pressing C-\[. INS always set/unset overwrite mode. If
unsetting, it will set the mode that was set before setting overwrite mode.

### Modes

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
*   In both cases deleted subeq mey be the selected one depending on the
    orientation.

If DEL or BACKSPACE do not find a juxted to delete and selection is the par of
a lop L, L-block is flatted.

#### Insertion mode (imode)

*   Selections cannot be oriented. The cursor is always to the left of 
    selection. Direction is always the same, I.
*   Insertions introduce subeqs to the right of the cursor.
*   DEL deletes selection.
*   BACKSPACE deletes the subeq to the left (honoring graphical texts editors
    but not readline's behaviour of replacing with a white space).

    
If DEL or BACKSPACE do not find a juxted to delete and selection is the par of
a lop L, L-block is flatted.

#### Overwrite mode (ovmode)

*   It is equivalent to *insert mode* except for insertions.
*   Inserted subeqs substitute selection.

### Basic operations

Basic operations must be intuitive for an user with no experience with emacs
or command-line shortcuts.

The scope of basic operations is everything that can be done only with the
mouse and cursor movement keys, RETURN, BACKSPACE, DEL and some common uses of
CONTROL, ALT and SHIFT.

> **Note**:
>
> Key bindings requiring CONTROL being selected are noted by C-x.
> Key bindings requiring ALT being selected are noted by M-x.
> Key bindings requiring CONTROL and ALT being selected are noted by M-C-x.
>
> In each particular case, instead of "x", the correspondent key which 
> completes the key binding will be used. Lower case will be always used. For
> example, C-s if it is required to press CONTROL and then the S key without
> releasing the CONTROL key.

A limited amount of usual key bindings used in graphical applications that
collide with readline's default key bindings and/or philosophy are honored
in order to be consistent with the fact that Visual Equation is a graphical
application at the end and to help users which are used to shortcuts of
graphical environments but not those of emacs/readline. In the future it may be
possible to choose a "package" of shortcuts or even define them individually.

#### Fundamental movements
Users who do not know any key-bindings, with no previous experience 
with Visual Equation or which will not dedicate time to learn the rest of
movements will likely use these fundamental movements all the time.

Because of that, fundamental movements are intended to satisfy the following
conditions:

*   It must be possible to select any selsubeq by using them.
*   Thye must require very few keystrokes to select selsubeqs which are close 
    to current selection.
*   Navigating far away must not require too many keystrokes.
*   They must be someway reasonable so the user can learn their behaviour soon.
*   They must be a compromise between being practical and not discouraging
    a new user to use the program because they look strange.

##### LEFT (fast movement):

*   If RDIR, set LDIR.
*   Else, move to the closest symbol to the left without changing dir.
    If that symbol is not a selsubeq, select instead its usupeq of lower level.
    
**Marginal case**: If no candidate is found, select the last symbol or its
usupeq of lower lever in the case that it is not a selsubeq.

##### RIGHT (slow, exhaustive and redundant):

*   If LDIR, set RDIR.
*   Navigate equation forward, selecting selsubeqs before entering them and
    before exiting them.
*   In addition, if ODIR, insert a temporal VOID after a subeq before exiting
    it so the user can insert a juxted there.

#### Longer movements

> **Note**: CONTROL is preferred for "words" movements instead of ALT in basic
> commands because they are commonly used by desktop applications.

##### C-LEFT and C-RIGHT
This key bindings are used to navigate between mates.

> **Note**: The behavior does more honor to gedit and equivalent readline
> key combination than to kwrite if considering that mates are words. 
>
> **Note**: Advanced movements will consider that mates are characters and
> their supeqs are words.

When using C-RIGHT/C-LEFT:
*   If LDIR/RDIR, direction will change to RDIR/LDIR.
*   Else, the mate to the right/left of selection is selected when
    C-RIGHT/C-LEFT is used.
    Marginal case: If selection is the last/first mate, choose the first/last
    mate.
*   Successive keystrokes of these key combinations (valid for an interleaved
    use of them) will remember the N-mate level of the selection before 
    applying the first of these key combinations.

#### Increasing and shortening selections

##### SHIFT-LEFT and SHIFT-RIGHT:

When using SHIFT-LEFT/SHIFT-RIGHT:
*   If selection is the representative of a non-first/non-last juxted, include
    in selection the juxted to the left/right. In the case that dir is not
    ODIR, set LDIR/RDIR.
*   If selection is already formed by several juxteds, shrink or extend the
    side matching the direction if that is LDIR or RDIR. If it is ODIR, the
    equivalent direction is determined by which was the first keystroke of the
    sequence. It is possible to change the direction in the LDIR/RDIR case
    by pressing RIGHT/LEFT.
*   If an extension is not possible (no more juxteds in the direction of
    expansion or a non-juxted is selected, select the supeq of selection and
    set LDIR/RDIR.

##### RETURN
Select first 1-ulevel usubeq of selection if it exists and is selectable.
   
##### SHIFT-UP (or M-p)
Select superequation if it exists. Do not change dir unless selection was VDIR.
In that case, RDIR is set. It respects the GUI notion of using SHIFT to
extend current selection.

##### SHIFT-DOWN (or M-n)
Select last 1-ulevel usubeq of selection if it exists and is selectable.
It respects the GUI notion of using SHIFT to shrink current selection.

#### Manipulation of subequations

##### Cut (C-x)
 
Remove selected subeq and save/overwrite VE's clipboard.
 
This shortcut is a an important key combination for emacs and readline, but by
default the desktop tradition will be respected.

##### Copy (C-c)

Save/overwrite VE's clipboard with selection.

##### Paste (C-v)

Insert VE's clipboard (in overwrite mode, selection is replaced).

##### Undo (C-z)

Undo last manipulation, if it exists.

##### Redo (C-SHIFT-z)

Redo last manipulation, if it exists.

#### Complete (TAB)
#### Possible Completions (SHIFT-TAB, M-?)

Allow to specify graphically a new form for current selection. More details
on advanced operations sections.

##### Transpose forward (M-RIGHT)

Swap positions of current selection and its mate to the right, leaving original
selection selected.

No direction is changed.

Marginal case: If there is no mate to the right, do nothing.

##### Transpose backward (M-LEFT)

Swap positions of current selection and mate the left, leaving original
selection selected.

No direction is changed.

Marginal cases:
*   If selection is a TVOID, swap the closest two mates to the left if they 
    exist. Else, do nothing.
*   If there is no mate to the left, do nothing.

##### C-DEL

If selection is a juxted (or combination of them) remove all the juxted of
the same juxt-block to the right of the cursor.

If selection is not a juxted, substitute pars of lop-block to the right of the
cursor by PVOIDs.

##### C-BACKSPACE

If selection is a juxted (or combination of them) remove all the juxted of
the same juxt-block to the left of the cursor

If selection is not a juxted, substitute pars of lop-block to the left of the
cursor.

##### Create/Delete groups (C-RETURN)

A group makes strict usubeqs of selected block not selectable. It has no
effect if selection is a symbol.

> **Note**: If an existing soft group (see below) is grouped, it will become
> again a soft group if it is ungrouped.

##### Create/Delete soft groups (SHIFT-RETURN)

A soft group is a juxt-block that is a juxted of another juxt-block.

To create a soft-group, select together the desired juxteds by using
SHIFT-LEFT or SHIFT-RIGHT before using they key binding.

> **Note**: There may be an option to create soft groups automatically when
> inserting sequences of digits.

#### Shortcuts for inserting symbols and operators

> **Temporal Note**:
>
> The following key bindings are used by readline and should not be used,
> unless they are marked as requisitioned.
>
>*  C-@, C-], C-\_, C-?
>*  M-C-\[, M-C-], M-C-?
>*  M-SPACE, M-#, M-&, M-\* (requisitioned), M--, M-., M-digit, M-<, M->, M-?, 
>   M-\\, M-~ (requisitioned), M-\_ (requisitioned).

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

##### Separate subeqs (SPACE)
Insert or increase a region "without" subequations.
A numeric argument fix the width with precision.

##### Bring subeqs closer (SHIFT-SPACE)
Reduce a region "without" subequations or delete it.

> **Temporal note**: They will be implemented as characters, not operators.
> That way there is no need of a non-user op.
##### Subscripts and superscripts (DOWN and UP)
Include an empty sub/super-script or select it if it is already a script.

The sub/super-script will be the one to the left if dir is L or I. If dir is O,
selection will be replaced with a PVOID at the same time the script is
selected (and created if it did not exist).

TAB an SHIFT-TAB after DOWN or UP will modify the position of the recently
created script, including under/over-sets (see below).
##### Undersets and oversets (C-DOWN and C-UP)
Add an under/over-set (a subequation exactly under/over another subequation).

TAB an SHIFT-TAB after DOWN or UP will modify the position of the recently
created under/over-set, including scripts.
##### Functions (C-,, M-,, M-C-,)
First time is cosinus, then sinus then... The symbol version matches every 
function and the operator versions match functions which can have arguments.

> **Mnemonic**: Arguments of functions are separated by commas where they are
> presented as a list inside parenthesis.
##### Roots (M-%, M-C-%)
First time is a square root, next time is generic.

> **Mnemonic**: '%' looks like a generic root with its arguments, only
> lacking part of the main glyph.
##### Modify subequation with a variant (M-@)
Full details to be defined.  There is more info in *Advanced operations*.
 
> **Mnemonic**: '@' looks like a modified form of 'a'.
##### Summatory (C-+, M-+, M-C-+)
Sucesive keystrokes of the operator versions modify the number and position of
the args.
##### Productory (C-*, M-\*, M-C-\*)
Equivalent to summatory.
##### Integral (C-$, M-$, M-C-$)
Equivalent to summatory.

> **Mnemonic**: '$' looks like an integral if the vertical var is not
> considered.
>
##### Fraction (C-/, M-/, M-C-/)
There are several types of fractions.

The symbol version introduce may introduce a fraction-like symbol.
##### Equal-like symbols (C-=)
##### Multi-line equations (M-=, M-C-=)
Some versions may include equals and other useful things that avoid typing
and provide a visual idea of the possibilities.

> **Mnemonic**: Usually multiline equations are connected with the = sign.
##### "Less than"-like symbol (C-<)
##### "Bigger than"-like symbol (C->) 
##### Pair of delimiters (C-), M-), M-C-))
The symbol version introduces a pair of independent delimiters of the same
size.

It can be accelerated providing a character identified with the delimiter.
##### Matrices (M-(, M-C-()
###### Equation system (M-{, M-C-{)
A digit modifies the number of equations.

> **Mnemonic**: Glyph enclosing equations in a equation system looks like a
> '{'.
###### Brace-like (M-}, M-C-})
> **Mnemonic**: Usual braces looks like a rotated '{'.
###### Arrows (C-~)
> **Mnemonic**: '~' looks like a curved arrow without head.
###### Hat-like decorators of fixed size (M-\_, M-C-\_)
> **Mnemonic**: '_' is straight, which gives an idea of something constant.
###### Hat-like decorators of variable size (M-\~, M-C-\~)
> **Mnemonic**: '~' is curved, which gives an idea of being adaptable.
###### Small operators (C--)
> **Mnemonic**: '+' and '*' stand for big operators. '-' reduces something,
> in this case the size of the operators.
###### Font colors (M-&, M-C-&)
###### Background colors (C-!, M-!)
> **Mnemonic**: '!' indicates something important. Backgroung colors increase
> importance of an equation. 
###### Special text (C-., M-C-.)
It is a symbol-like key biding because a windowed dialog will always appear 
and modification of the text will require a special dialog.
However, M-C-. may be considered with care.

> **Mnemonic**: A dot is used to finish a "text" sentence.

> **Note**: M-. is used for an advanced operation not related with special
> texts.
### Advanced operations

The intention of advance operations is to imitate Readline default
keybindings as much as possible. We will use Readline's command names with
the following equivalence:

*   characters -> selection and its mates
*   words -> 1-ulevel usupeq US of selection and mates of US

In addition, mates are nested in an equation, contrary to words in a
line. That is indicated with the ulevel of the mate. Following the
symbolism of words, 1-ulevel mates would be words of the same
line, 2-ulevel mates would be, for example, lines of the same page,
3-ulevel mates pages of the same book, and so on.

Main difference with respect to equivalent basic commands is that these ones do
not consider so much direction of selection. It is recommended to avoid LDIR 
when using advanced commands to avoid confusion.

VOID is a special character which is understood in different ways by
different commands.

If not specified, any reference to a mate always refer to current selection.

#### Numeric arguments (M-0, M-1, ..., M--)
Add this digit to the argument already being prepared, or start a
new argument. M-- starts a negative argument. If no number is added, -1 is
used.

> **Note**: Numeric arguments can be used in basic operations too.

#### Movements
##### change-dir (C-()
This is not a readline command.

In normal mode, it turns LDIR into RDIR and RDIR into LDIR. If VDIR, it
remembers previous direction when selection was not a VOID and flip it, which
will be appreciated in the case that a sequence of movements not altering
direction selects a non-VOID subeq.
##### change-mode (C-[)
This is not a readline command.

##### beginning-of-line (C-a)
Select the first mate.
##### end-of-line (C-e)
Select the last mate.
##### forward-char (C-f)
Select mate to the right if it is not the last one. Else, do not move.
##### backward-char (C-b)
Select mate to the left if it is not the first one. Else, do not move.
##### forward-word (M-f)
Consider supeq SUP of selection S:
*   If S has at least one mate to the right contained in SUP, select the
    last one satisfying that condition.
*   Elif SUP has a mate RSUP to the right, select last mate of S contained in
    RSUP.
*   Else, do not move.

Successive calls to forward-word and backward-word (also inteleaved) must act
on the mate-ulevel which had seletion before the first call.
##### backward-word (M-b)
Counterpart of forward-word.
##### clear-screen (C-l)
Undecided, but it should be a nice operation.

#### Manipulating and accesing the history

**Saved equations** can be accessed as commands on the history of a shell.
In addition, saved equations can have a name and categories and subcategories
(to any nesting level) associated, but it is not mandatory.

Not to confuse "saved equations" with "exported equations". Exported equations
are equations that can be accessed outside visual equation. Current formats
to export equations are PNG, EPS, SVG and PDF. It is worth mentioning that
it is possible to recover equations for further edition from exported PNGs
and PDFs.

##### save-as (C-SHIFT-s)
This is not a readline command but it is placed in this section to help the
reader have a full view.

Save with a graphical interface current equation as a new equation at
the end of the history, possibly specifying a name and categories.

##### save (C-s)
This is not a readline command but it is placed in this section to help the
reader have a full view.

If equation being edited was never saved, this command is equivalent to
save-as. Else, it overwrites saved equation.
##### open-equation (C-o)
This is not a readline command but it is placed in this section to help the
reader have a full view.

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

##### accept-line (C-j, C-m)
This a non-windowed version of save-as.
Specify a name and save current equation as a new equation with that name. 
After that, a new empty equation is presented for edition.
It is possible to specify a category in the form
`[category[/subcategory[/...]]/]name`. To accept the name press again C-j or 
C-m or RETURN.
**Note**: C-j acts differently while searching in the history. See below.
##### insert-comment (M-#)
Save current equation at the end of the history list (as a new equation)
and start editing a new empty equation. This is a fast accept-line that does
not ask the user for an equation name nor categories to include in the save.
However, the equation will be uniquely identified anyway. With a numeric 
argument, it is equivalent to accept-line.
##### save-no-window (M-C-#)
This is not a readline command but it is placed in this section to help the
reader have a full view.

It acts like command save (C-s) but not allowing the user to add a name or
categories if equation was not saved before. It is:
*   If equation is already part of the history, overwrite its entry.
*   Else, it is equivalent to insert-comment.

In any case, a numeric argument allows the user to specify a name and
categories. If equation already existed:
*   If only a name is provided, equation is renamed but old categories, if
    any, are unmodified.
*   If at least a main category is provided, any category equation had are
    discarded.

To discard previous categories without adding a new one, just precede the name
by a slash as in `/newname`.
##### previous-history (C-p)
save-no-window displayed equation and fetch the previous equation from the
history list, moving back in the list. 
##### next-history (C-n)
save-no-window displayed equation and fetch the next equation from the 
history list, moving forward in the list.
##### beginning-of-history (M-<)
save-no-window displayed equation and fetch the first equation in the
history.
##### end-of-history (M->)
save-no-window displayed equation and fetch the last equation of the history.
##### reverse-search-history (C-r)
save-no-window current equation and search backward starting at the current
equation and moving up through the history as necessary. This is an 
incremental search. You can introduce part of the name, category or other 
fields (TODO: specify). You can fetch the equation with C-j. Any
other key combination will fetch the equation and then apply the command
to the equation.
##### forward-search-history (M-C-r)
Counter part of reverse-search-history.
> **Note**: C-s is not used as key binding because that is a
> shortcut with a long tradition in desktop applications to save files. If
> we allow key-bindings to be configurable, this will be one of the first
> commands supported.

> **Note**: By default, M-C-R is assigned to revert-line along with M-R in
> readline.

##### non-incremental-reverse-search-history (Not implemented!)
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
##### non-incremental-forward-search-history (Not implemented!)
The counterpart of non-incremental-reverse-search-history.

The default readline keybinding for this command, M-n, is used as C-DOWN (see 
basic basic movements).
#### Manipulating subequations
##### end-of-file (C-d)
Exit Visual Equation if equation is a VOID, discarding the kill ring and the
undo list. 
##### delete-char (C-d)
*   If next mate do not exist, do nothing.
*   Elif selectio is a non-last juxted of a juxt-block, delete juxted to the
    right.
*   Elif next mate exists and it is not a VOID, move it to the right of
    selection as a juxted or several juxteds if it was a juxt-block. Leave a 
    VOID in the original position of the mate.
*   Elif there exists a mate to the right which is not a VOID, replace the
    (VOID) mate to the left of that mate with it and leave a VOID in its
    original position.
*   Else, do nothing.

It saves deleted mates on the kill ring (readline do that when a
numeric argument is passed, even if that is not documented).

> **Note**: C-d executes end-of-file if whole equation is a VOID.

##### backward-delete-char (C-?, C-h)
Counterpart of delete-char (not exactly reciprocal, but it has the same
philosophy and is less complex).

##### transpose-chars (C-t)
Equivalent to Transpose backward (M-LEFT). 
##### transpose-words (M-t)
*   If supeq SUP of selection exists and SUP has a mate to the left, transpose
    them.
*   Else, do nothing.

##### upcase-word (M-u)
Uppercase every symbol which has sense (Latin and Greek letters) included in
selection and every mate to the right contained in the supeq of selection. If
supeq does not exists, just in selection.
With a numeric argument, certain mates of the supeq of selection are included.
##### downcase-word (M-l)
Counterpart of upcase-word.
##### capitalize-word (M-c)
Capitalize the first symbol which has sense of selection.
##### overwrite-mode (INSERT, C-[)
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

##### quoted-insert (C-q)
If next input is a number, the number is introduced. (That is useful to 
introduce several times a number. e.g, to introduce 3 ten times type: 
M-1 0 C-q 3).

If next input is a letter, it will introduce an associated Greek letter.
Some capital letters have a greek version, but many cases share a latin
letter. To pass a negative numeric argument is equivalent to pass the
same numeric argument but positive except for some letters which have
a variant. In that case, it is equivalent to pass a positive numeric
argument but the variant is used for the insertion instead.

Not every greek letter can be inserted with this command. For those
cases quoted-insert-extra (M-q) can be used. 

Code equivalence:

> Legend:
>*  (**) means that correspondent greek letters can be obtained with another
>   key combination.
>*  (=) means that previous characters do not have a greek equivalent and
>   they map to themselves.
      
*   a, A -> alpha, A 
*   b, B -> beta, B
*   c, C -> chi, X (**)
*   d, D -> delta, Delta
*   e, E, - -> epsilon, E, varepsilon
*   f, F, - -> phi, Phi, varphi
*   g, G, - -> gamma, Gamma, digamma
*   h, H -> eta, H
*   i, I -> iota, I
*   j, J -> (=)
*   k, K, - -> kappa, K, varkappa
*   l, L -> lambda, Lambda
*   m, M -> mu, M
*   n, N -> nu, N
*   o, O -> omikron, O
*   p, P, - -> pi, Pi, varpi
*   q, Q -> (=)
*   r, R, - -> rho, P, varrho (**)
*   s, S, - -> sigma, Sigma, varsigma
*   t, T -> tau, T
*   u, U -> upsilon, Upsilon (**)
*   v, V -> (=)
*   w, W -> (=)
*   x, X -> chi, X (**)
*   y, Y -> upsilon, Upsilon (**)
*   z, Z -> zeta, Z 

##### quoted-insert-extra (M-C-q):
If next input is a number, the number is introduced.

This command supplies the missing greek letters of quoted-insert (C-q). 
Assigned key combination is not used in readline by default.
If next input is an alphanumeric character not listed in the list below,
the character is considered literally. To pass a negative numeric
argument is equivalent to pass the same numeric argument but positive 
except for some letters which have a variant. In that case, it is
equivalent to pass a positive numeric argument but the variant is used
for the insertion instead.

Code equivalence:

> Legend:
>*  (**) means that correspondent greek letters can be obtained with another
>   key combination.

*   o, O -> omega, Omega
*   p, P -> rho, P, varrho (**)
*   s, S -> psi, Psi
*   t, T , - -> theta, Theta, vartheta
*   x, X -> xi, Xi

##### tab-insert
See shortcuts TAB and SHIFT-TAB in basic operations.

##### self-insert (a, b, A, 1, !, ...)
Insert the character typed. In some cases such as ~ or SPACE, a special
character is inserted instead (TODO: be more specific). In some cases,
quoted-insert may be needed to insert some special symbols.

#### Killing and Yanking
Killed subequations can be yanked at any moment (before quiting the program).
##### kill-line (C-k)
Kill any subequation after current subeq. Those which cannot be deleted totally
without flatting their supeqs are left. It is a compromise so the
"usually desired" command can be executed without selecting exactly the
subeq of interest.
With a negative argument kill any subequation before current subeq.
##### backward-kill-line (C-c C-?, C-c C-h)
Kill selection and any subequation before current subeq. It is a compromise so
a variant of kill-line can be used.
With a negative argument kill selection and any subequation before.
##### unix-line-discard (C-u)
Kill any subequation before current subeq. Those which cannot be deleted
totally without flatting their supeqs are left. It is a compromise so the
"usually desired" command can be executed without selecting exactly the
subeq of interest.
A negative argument has no effect, honoring readline.

##### kill-word (M-d)
If selection is a juxted of a juxt-block JB and there are juxteds of JB
after the cursor different than TVOID (selection itself may be one of them),
delete every juxted satisfying that condition.
Elif selection is a nested juxted and has a quasi-cojuxted QCJ to the right,
remove QCJ and every cojuxted of QCJ to the right.
Else, set to PVOID every 1-level subeq of the supeq of selection to the
right of the cursor.
##### backward-kill-word (M-C-?, M-C-h)
Counter-part of kill-word.
##### unix-word-rubout (C-w)
Kill  the  word behind point, using white space as a word boundary.
The killed text is saved on the kill-ring.
A negative argument has no effect, honoring readline.
##### delete-horizontal-space (M-\\)
If selection is a juxt-block, do nothing. Else, flat the leading
operator of selection. A positive numeric argument n acts on the (n-1)-ulevel
usubeq of selection. A negative numerical argument -n acts on the n-ulevel 
usupeq of selection.
##### massively-delete-horizontal-space (M-C-\\)
It is not a readline command.

It is equivalent to use delete-horizontal-space with every positive numerical
argument until reaching the last subeq of selection. A numerical argument
bigger than 1 acts from the 0-ulevel supeq of selection to the (n-1)-ulevel
subeq of selection. A numerical argument of -1 is equivalent to use 
delete-horizontal-space with every negative numerical argument until reaching
the last supeq. A numerical argument -n smaller than -1 acts from the n-ulevel
usupeq of selection to the 1-ulevel usupeq of selection.

##### create-horizontal-space (C-\\)
It is not a readline command.

If selection is a block, replace every symbol of selected block by a VOID
(it acts recursively on subeqs of selection).

With a negative argument -n, n-ulevel subeqs of selection are replaced by VOIDs
before applying the default command.

##### kill-region (Maybe we bound it even if it is not a default of readline)
Kill the text between the point and  mark  (saved  cursor  posi‐
tion).  This text is referred to as the region.
##### copy-region-as-kill (Maybe we can reserve a key combination)
Copy the text in the region to the kill buffer.
##### yank (C-y)
Yank the top of the kill ring into the buffer at point.
##### yank-pop (M-y)
Rotate  the kill ring, and yank the new top.  Only works follow‐
ing yank or yank-pop.
##### yank-nth-arg (M-C-y)
Insert the first non-VOID 1-ulevel usubeq of usupeq. With an argument n, insert
the nth non-VOID 1-ulevel usubeq of usupeq. If it is 0, insert the lop of
usupeq with empty pars. If it is negative, insert the nth non-VOID 1-ulevel
usubeq starting from the end and without counting the last non-void 1-ulevel
usubeq.

> **Note**: To insert the last 1-ulevel usubeq it is possible to use
> yank-last-arg (see below).
##### yank-last-arg (M-.)
Insert the last non-VOID 1-ulevel usubeq of usupeq. With a numeric argument it
is equivalent to yank-nth-arg. Successive calls to yank-last-arg consider
usupeqs of higher level. A negative numeric argument provided to successive
calls invert the nesting direction. It is, first negative argument provided
will result in using the (N-1)-ulevel usupeq instead of the (N+1)-ulevel
usupeq. Next time that a numerical argument is passed the (M+1)-ulevel usupeq
is considered instead of the (M-1)-ulevel usupeq. If no supeqs are available
in requested direction, previous insertion is not modified.

#### Completing
WIP!!!
##### complete (TAB)
Display a a graphical window equivalent to the one for building the selected
subequation when pressing a button in the pannel. If it is not available,
use possible-completions instead.

> **Note**: > C-i is used by default for 'complete' command in readline. C-i
> is used in VE as an alternative to C-x.
##### possible-completions (SHIFT-TAB, M-?)
List in a graphical window the possible variations of the selected subequation.
You can choose one using the cursor keys and accept it with RETURN, C-j or C-m.
To abort, use ESC or a key binding associated to abort. There will be window
buttons too.
##### insert-completions
Not used.

Default keybing, M-*, is used to introduce productories.
##### menu-complete (M-@)
Replace selection with a variation. Repeated execution of the command steps
through the list of possible variations, inserting each match in turn. At
the end of the list, the original subequation is restored. An argument of
n moves n positions forward in the list of possible variations. A negative
argument moves backward through the list.

> **Note**: This command is unbounded by default in readline.

#### Keyboard Macros
WIP!!!
##### start-kbd-macro (C-i ()
Begin saving the characters  typed  into  the  current  keyboard
macro.
##### end-kbd-macro (C-i ))
Stop saving the characters typed into the current keyboard macro
and store the definition.
##### call-last-kbd-macro (C-i e)
Re-execute the last keyboard macro defined, by making the  char‐
acters  in  the  macro  appear  as  if  typed  at  the keyboard.
print-last-kbd-macro () Print the last keyboard macro defined in
a format suitable for the inputrc file.

#### Miscellaneous
WIP!!!
##### re-read-init-file (C-i C-r)
Read a configuration file.
##### abort (C-g, M-C-g, C-i C-g, ESC)
Abort the current editing command. It does not ring.
##### do-uppercase-version (M-a, M-b, M-x, ...)
If  the  metafied character x is lowercase, run the command that
is bound to the corresponding uppercase character.
##### prefix-meta (Unbounded)
Metafy the next character typed.

ESC is used for abort command.
##### undo (C-_, C-i C-u)
Incremental undo, separately remembered for each equation.
##### revert-line (M-r)
Undo all changes made to this equation.  This is like executing
the undo command enough times to return the equation to its
initial state.
##### set-mark (C-@, M-SPACE)
Set the mark to the point.  If a numeric argument  is  supplied,
the mark is set to that position.
##### exchange-point-and-mark (C-i C-i, C-i C-x)
Swap  the  point  with the mark.  The current cursor position is
set to the saved position, and the old cursor position is  saved
as the mark.
##### character-search (C-])
A character is read and point is moved to the next occurrence of
that character. A negative count searches for  previous  occurrences.
##### character-search-backward (M-C-])
A character  is  read and point is moved to the previous occurrence of that 
character. A negative count searches for subsequent occurrences.
##### emacs-editing-mode
When in vi command mode, this causes a switch to  emacs  editing
mode.

vi-mode not supported by the moment.
##### vi-editing-mode
When  in  emacs editing mode, this causes a switch to vi editing
mode.

vi-mode not supported by the moment.
