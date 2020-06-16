import os
# import gettext
# import locale

from visualequation import commons


def getusage():
    def includeexample(filename):
        return "<center><img src='" \
            + os.path.join(commons.EXAMPLES_DIR, filename) \
            + "'></center>"

    usagestr = _(
        "<h2> Table of Contents </h2>"
        "<ul>"
            "<li> Introduction</li>"
            "<li> Fundamentals</li>"
            "<li> Operators</li>"
                "<ul>"
                    "<li> Definition</li>"
                    "<li> Usage</li>"
                    "<li> Subindices and superindices</li>"
                "</ul>"
            "<li> Navigating the equation</li>"
        "</ul>"  
        "<h2> Introduction </h2>"
        "<p> Visual Equation is a program to edit high-quality equations. "
        "LaTeX produces really good-looking formulas and it is the standard "
        "for scientific communication. However, the language has a steep "
        "learning curve and there are not so many applications which produce "
        "LaTeX-rendered formulas in an intuitive way.</p>" 
        "<p> Visual Equation intends to be as user-friendly as possible "
        "while allowing the user to produce arbitrary complex formulas.</p>"
        "<h2> Fundamentals </h2>"
        "<p> When you start Visual Equation, equation consists of a small "
        "square. That's a special symbol used to indicate an empty place.</p>")
    usagestr += includeexample("oblong.png")
    usagestr += _(
        "<p> You will also find that it is surrounded by a strange pair of "
        "parenthesis. We call them the <b>ghost</b>. The ghost will be "
        "always there, surrounding part or the whole equation. We will use "
        "the terms \"surrounded\" or \"selected\" interchangeably to refer to "
        "the part of the equation currently being embraced by the ghost. We "
        "will say that the ghost looks to the right when it looks like in the "
        "previous image, with the lower extremes of the parenthesis pointing "
        "to the left. The following one looks to the left</p>")
    usagestr += includeexample("ghost_left.png")
    usagestr += _(
        "<p> At the bottom of the equation you can find the symbol panel. It "
        "consists of several sections that can be accessed by clicking "
        "on the tabs. It looks like this when the first tab is selected (as "
        "it is when Visual Equation is just opened).</p>")
    usagestr += includeexample("symbol_panel.png")
    usagestr += _(
        "<p> Just press a valid key in your keyboard or click on an element "
        "of the symbol panel to <b>replace the small square</b>. Let's "
        "suppose that you pressed key \"a\" in your keyboard</p>")
    usagestr += includeexample("a.png")
    usagestr += _(
        "<p> If you continue <b>introducing elements</b>, they will be placed "
        "where the ghost is facing and they will be automatically surrounded "
        "by the ghost. For example, let's introduce now a \"b\"</p>")
    usagestr += includeexample("ab.png")
    usagestr += _(
        "<p> If you want to <b>turn the ghost around</b>, probably because "
        "you forgot to include something, press <b>LEFT</b></p>")
    usagestr += includeexample("ab_left.png")
    usagestr += _(
        "<p> Then, if you introduce a new element, it will be placed to "
        "the left of the ghost. Let's introduce a plus sign by pressing \"+\" "
        "on the keyboard</p>")
    usagestr += includeexample("aplusb.png")
    usagestr += _(
        "<p> After introducing a new element, the ghost will always looks "
        "to the right, as it can be appreciated above. Apart from turning the "
        "ghost around, <b>LEFT</b> and <b>RIGHT</b> (or <b>TAB</b>) keys will "
        "allow you to move the ghost to any place of the equation (See "
        "section \"Navigating the equation\" below). You can always "
        "<b>remove</b> what the ghost is surrounding by pressing "
        "<b>DELETE</b> or <b>BACKSPACE</b>.</p>"
        "<p> There are some advanced manipulations that can be selected "
        "from the \"Edit\" menu. We present here the keyboard shortcuts for "
        "some of them:</p>"
        "<p> If you want to copy or cut the selection use the classical "
        "<b>Ctr+C</b> or <b>Ctr+X</b> and paste it with <b>Ctr+V<b>.</p>"
        "<p>If you did something wrong, press <b>Ctr+Z</b> until you arrive "
        "to the desired previous state of the equation. If after accessing "
        "previous states you didn't modify the equation, you can recover "
        "later states by pressing <b>Ctr+Y</b>.</p>"
        "<h2> Operators </h2>"
        "<h3> Definition</h3>"
        "<p> There are some special elements in the symbol panel which "
        "include three dots. For example, that's the case of the matching "
        "parenthesis</p>")
    usagestr += includeexample("parenthesis.png")
    usagestr += _(
        "<p> Some of them include in addition one small square, as the "
        "fraction</p>")
    usagestr += includeexample("fraction.png")
    usagestr += _(
        "<p> A few ones include also more small squares, as the matrix</p>")
    usagestr += includeexample("matrix.png")
    usagestr += _(
        "<p> We will call them all operators. The difference with respect to "
        "ordinary elements is that they reserve positions in the "
        "equation to be used by other elements. We will call the "
        "set of elements in any of those positions an argument of the "
        "operator. Probably the nicest thing about operators is that they are "
        "resized if needed to beautifully match the size of their "
        "arguments. For example, this is a square root with a single "
        "element in its argument</p>")
    usagestr += includeexample("sqrt_simple.png")
    usagestr += _(
        "<p> And this is a square root with several elements. As you can see, "
        "the dimensions of the square root symbol (and also the horizontal "
        "line of the fraction) perfectly fit the rest of the elements</p>")
    usagestr += includeexample("sqrt_complex.png")
    usagestr += _(
        "<p>Note that classical functions found in the symbol panel such as "
        "\"log\" are not considered operators to give more flexibility to the "
        "user. Sometimes you will probably want to introduce the matching "
        "parenthesis to the right of a function and it would look like "
        "this</p>")
    usagestr += includeexample("function.png")
    usagestr += _(
        "<h3> Usage</h3>"
        "<p> When an operator is introduced, its arguments are set to small "
        "squares by default. For example, if you introduce the fraction "
        "operator, it results in</p>")
    usagestr += includeexample("fraction_oblongs.png")
    usagestr += _(
        "<p> As you can see, the first argument (the one which was "
        "marked with dots) is selected automatically. It is expected that "
        "you will replace the small squares by introducing one or more "
        "elements of your choice in every argument, but you are not forced to "
        "do that. There is a slightly bigger square in the symbol panel if "
        "you need it</p>")
    usagestr += includeexample("fraction_alpha_oblong.png")
    usagestr += _(
        "<p> In this case, we introduced a greek letter alpha from the symbol "
        "panel in the first argument. If you press <b>RIGHT</b> when the "
        "ghost is surrounding a whole argument and facing to the right, it "
        "will select the next argument</p>")
    usagestr += includeexample("fraction_alpha_oblong_variant.png")
    usagestr += _(
        "<p> Then you can introduce and remove elements in that "
        "argument.</p>")
    usagestr += includeexample("fraction_completed.png")
    usagestr += _(
        "<p> If you press <b>RIGHT</b> when the ghost is surrounding the "
        "last argument and facing to the right, the whole operator is "
        "surrounded.</p>")
    usagestr += includeexample("fraction_selected.png")
    usagestr += _(
        "<p> In that state, new elements will be introduced to the right "
        "of the operator, as with ordinary elements. For "
        "example, if you click on the logarithmic function</p>")
    usagestr += includeexample("fraction_log.png")
    # Uncomment and extend when the opposite operator is implemented
    # usagestr += _(
    #     "<p> <b>Note:</b> There is a very handy way to introduce an operator. "
    #     "If you click on it in the symbol panel while pressing <b>SHIFT</b>, "
    #     "then: "
    #     "<ul>"
    #     "<li> The selection is removed and the operator is placed there.</li>"
    #     "<li> The first argument of the operator is filled with the removed "
    #     "selection.</li>"
    #     "<li> The second (empty) argument is selected, if any. Else, the "
    #     "whole operator is selected.</li>"
    #     "</ul>")
    # usagestr += includeexample("fraction_parenthesis.png")
    # usagestr += _(
    #     "<p> Note that if the symbol clicked was not an operator, then the "
    #     "selection is simply removed and the clicked element inserted in its "
    #     "position.</p>")
    usagestr += _(
        "<h3> Subindices and superindices</h3>"
        "<p> There are some important operators that cannot be found in "
        "the symbol panel. They are the subindices and superindices. If "
        "you want to include a subindex, press <b>DOWN</b></p>")
    usagestr += includeexample("fraction_log_sub.png")
    usagestr += _(
        "<p> In this example, the subscript can be used to specify a basis "
        "for the logarithm. Let's say it is 2</p>")
    usagestr += includeexample("fraction_log2.png")
    usagestr += _(
        "<p> Using <b>UP</b> superscripts are introduced.</p>")
    usagestr += includeexample("superscript.png")
    usagestr += _(
        "<p> They are mainly used to specify powers</p>")
    usagestr += includeexample("a_cube.png")
    usagestr += _(
        "<p> But they have other uses. For example, you can write "
        "elements of the periodic table. Let's write an isotope of "
        "the Hydrogen. First, we select the \"Text\" element from the "
        "symbol panel and introduce an \"H\". Then we turn around the "
        "ghost</p>")
    usagestr += includeexample("H_ghost_left.png")
    usagestr += _(
        "<p> Pressing <b>UP</b> when the ghost looks to the left will "
        "introduce a superscript to the left.</p>")
    usagestr += includeexample("H_supleft.png")
    usagestr += _(
        "<p> This way, we can write the symbol of deuterium</p>")
    usagestr += includeexample("deuterium.png")
    usagestr += _(
        "<p> You can combine them all</p>")
    usagestr += includeexample("2F1.png")
    usagestr += _(
        "<p> also recursively!</p>")
    usagestr += includeexample("Amunot.png")
    usagestr += _(
        "<h2> Navigating the equation </h2>"
        "<p> Visualequation's way of editing an equation "
        "just by rendering LaTeX is at the very least, cunning. However, "
        "maybe the most important downside is that it's not possible to "
        "select an arbitrary part of the equation by clicking on it. On "
        "the other hand, navigation has been designed to be as "
        "convenient and intuitive as possible. These are the main ideas "
        "to have in mind:"
        "<ul>"
        "<li> The first and last element of the equation are connected. "
        "For convenience, the whole equation is selected when you cross from "
        "one end of the equation to the other.</li>"
        "<li> Forward navigation (using <b>RIGHT</b> or <b>TAB</b>) is slower "
        "but more precise because whole arguments and operators are "
        "surrounded before entering and exiting them.</li>"    
        "</ul>"
        "<p> Next image illustrate is the result of pressing <b>RIGHT</b> "
        "consecutively, illustrating above points.</p>")
    usagestr += includeexample("forward.png")
    usagestr += _(
        "<ul>"
        "<li> Backward navigation (using <b>LEFT</b>) is faster but "
        "less precise because whole arguments and operators are surrounded "
        "only before exiting them.</li>"
        "<p> Previous point can be observed in the next image, which shows "
        "consecutive selections after pressing <b>LEFT</b>.</p>")
    usagestr += includeexample("backward.png")
    return usagestr
