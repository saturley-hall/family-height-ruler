from math import floor
from subprocess import call as terminal_call

def make(footmarker, filename):
    """
    Makes a box with a sliding lid
    @param l length of the box in mm (external)
    @param w width of the box in mm (external)
    @param h height of the box in mm (external)
    @param mat_thickness thickness of the material in mm
    @param tab_size how long each of the tabs in mm
    """
    
    tex_string = "\\documentclass[class=minimal, border=0mm, preview=true]{standalone}\n"
    tex_string += "\\usepackage{amssymb}\n"
    tex_string += "\\usepackage{tikz}\n"
    tex_string += "\\usepackage{xcolor}\n"
    tex_string += "\\begin{document}\n"
    tex_string += "\\thispagestyle{empty}\n"
    tex_string += "\\begin{tikzpicture}[x=1in, y=1in]\n"
    tex_string += "% Debugging grid\n"
    tex_string += "%\\draw[step=0.0625, gray, ultra thin] (0, -3) grid (3, 8.5);\n"

    bar_height = 0.25
    bar_length = 2.0
    circle_diam = 0.1875
    counter_start_pos = 0
    if (footmarker == 1):
        counter_start_pos = bar_height / 2.0 # this is the base case of 1 foot mark
    elif (footmarker % 2 == 0): # if it is even start offset one bar width
        counter_start_pos = -1 * (footmarker - 1) * bar_height + bar_height / 2.0 
    else: # it is odd so align with bar
        counter_start_pos = -1 * (footmarker - 1) * bar_height + bar_height / 2.0

    tex_string += "\\fill[fill=black] (0,0) rectangle ({0}, {1});\n".format(
        bar_length,
        bar_height
    )

    tex_string += "\\draw[white, thin] (0, {0}) -- ({1}, {0});\n".format(
        bar_height / 2.0,
        bar_length
    )

    for i in range(footmarker):
        pos_name = "pos{0}".format(i)
        tex_string += "\\coordinate ({0}) at ({1}, {2});\n".format(
            pos_name,
            bar_length + (bar_height * 1.5),
            counter_start_pos + 2 * i * bar_height
        )
    
        tex_string += "\\fill[color=gray] ({0}) circle ({1});\n".format(
            pos_name,
            circle_diam / 2.0,
        )
        tex_string += "\\fill[color=black] ({0}) circle ({1});\n".format(
            pos_name,
            circle_diam / 10,
        )
    tick_height = 0.0625
    tick_length = 0.5
    # Draw the tick marks
    for inch_counter in range(1, 8):
        tex_string += "\\fill[fill=black!30] (0, {0}) rectangle ({1}, {2});\n".format(
            inch_counter - tick_height / 2.0 + bar_height / 2.0,
            tick_length * 2.0 if inch_counter == 6 else tick_length,
            inch_counter + tick_height / 2.0 + bar_height / 2.0
        )    # lines connecting
        tex_string += "\\draw[white, thin] (0, {0}) -- ({1}, {0});\n".format(
            inch_counter + bar_height / 2.0,
            tick_length * 2.0 if inch_counter == 6 else tick_length
        )
    for inch_counter in range(-3, 0):
        tex_string += "\\fill[fill=black!30] (0, {0}) rectangle ({1}, {2});\n".format(
            inch_counter - tick_height / 2.0 + bar_height / 2.0,
            tick_length,
            inch_counter + tick_height / 2.0 + bar_height / 2.0
        )
        tex_string += "\\draw[white, thin] (0, {0}) -- ({1}, {0});\n".format(
            inch_counter + bar_height / 2.0,
            tick_length * 2.0 if inch_counter == 6 else tick_length
        )

    tex_string += "\\end{tikzpicture}\n"
    tex_string += "\\end{document}"

    with open(filename, "w") as f:
        f.write(tex_string)

for number in range(1, 8):
    # call the pdflatex
    terminal_call(["mkdir", "build"])
    filename = "build/marker-{0}.tex".format(number)
    make(number, filename)
    terminal_call(["latexmk", "-xelatex", "-output-directory=build", filename])
