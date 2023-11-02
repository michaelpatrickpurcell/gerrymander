import tikz
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist
from itertools import product

from pylatex import Document, TikZ
from pylatex import Package, Command
from pylatex.utils import italic, bold, NoEscape
from pylatex.basic import NewLine

def generate_locations(seed=None):
    n_colors = 6
    n_copies = 6

    locations = [0.33 * (np.array([i,j]) - 2.5) for i in range(n_colors) for j in range(n_copies)]

    if seed is None:
        seed = np.random.randint(2**31)
    print('Initial seed = %i' % seed)
    np.random.seed(seed)

    np.random.shuffle(locations)

    return locations, seed


def generate_electorate_grid(locations):
    # color_list = ['Red', 'Orange', 'Yellow', 'Green', 'Blue', 'Purple']
    color_list = ['black'] * 6

    pic = tikz.Picture()
    pic.usetikzlibrary('shapes.geometric')

    for location in locations[:6]:
        point = '(%fin, %fin)' % (location[0], location[1])
        pic.node(r'\phantom{.}', at=point, minimum_width='0.33in', minimum_height='0.33in')#, fill=color_list[0])
        # pic.node(r'\contour{black}{\textcolor{white}{1}}', at=point)
        pic.node(r'\phantom{1}', at=point, draw=color_list[0], circle=True, inner_sep='0.75pt', line_width='0.9mm')

    for location in locations[6:12]:
        point = '(%fin, %fin)' % (location[0], location[1])
        pic.node(r'\phantom{.}', at=point, minimum_width='0.33in', minimum_height='0.33in')#, fill=color_list[1])
        # pic.node(r'\contour{black}{\textcolor{white}{2}}', at=point)
        pic.node(r'\rule{6mm}{1mm}', at=point, text=color_list[1], rotate=45, inner_sep='0pt')
        pic.node(r'\rule{6mm}{1mm}', at=point, text=color_list[1], rotate=-45, inner_sep='0pt')

    for location in locations[12:18]:
        point = '(%fin, %fin)' % (location[0], location[1])
        point2 = '(%fin, %fin)' % (location[0], location[1]-0.035)
        pic.node(r'\phantom{.}', at=point, minimum_width='0.33in', minimum_height='0.33in')#, fill=color_list[2])
        # pic.node(r'\contour{black}{\textcolor{white}{3}}', at=point)
        pic.node(r'\phantom{.}', at=point2, regular_polygon=True, regular_polygon_sides=3, fill=color_list[2], inner_sep='1.65pt')

    for location in locations[18:24]:
        point = '(%fin, %fin)' % (location[0], location[1])
        pic.node(r'\phantom{.}', at=point, minimum_width='0.33in', minimum_height='0.33in')#, fill=color_list[3])
        # pic.node(r'\contour{black}{\textcolor{white}{4}}', at=point)
        pic.node(r'\phantom{.}', at=point, draw=color_list[3], diamond=True, inner_sep='2.35pt', line_width='0.9mm')

    for location in locations[24:30]:
        point = '(%fin, %fin)' % (location[0], location[1])
        point2 = '(%fin, %fin)' % (location[0], location[1]-0.005)
        pic.node(r'\phantom{.}', at=point, minimum_width='0.33in', minimum_height='0.33in')#, fill=color_list[4])
        # pic.node(r'\contour{black}{\textcolor{white}{5}}', at=point)
        pic.node(r'\phantom{.}', at=point2, star=True, star_points=5, star_point_ratio=2, fill=color_list[4], inner_sep='1.6pt')

    for location in locations[30:36]:
        point = '(%fin, %fin)' % (location[0], location[1])
        pic.node(r'\phantom{.}', at=point, minimum_width='0.33in', minimum_height='0.33in')#, fill=color_list[5])
        # pic.node(r'\contour{black}{\textcolor{white}{6}}', at=point)
        pic.node(r'\phantom{.}', at=point, regular_polygon=True, regular_polygon_sides=6, fill=color_list[5], inner_sep='3.2pt')

    x_locs = np.arange(-0.99, 1, 0.33/3)
    y_locs = np.arange(-0.99, 1, 0.33)
    dot_locations = product(x_locs, y_locs)
    for i,j in dot_locations:
        point = '(%fin, %fin)' % (i,j)
        pic.node(r'\phantom{}', at=point, inner_sep='0.25pt', fill='black', circle=True)

    dot_locations = product(y_locs, x_locs)
    for i,j in dot_locations:
        point = '(%fin, %fin)' % (i,j)
        pic.node(r'\phantom{}', at=point, inner_sep='0.25pt', fill='black', circle=True)

    pic.node(r'\phantom{}', at='(0in,0in)', draw=True, line_width='0.25mm', minimum_width='1.99in', minimum_height='1.99in')

    tikzpicture = pic.code()
    return tikzpicture

def save_tikzpicture(tikzpicture, filename):
    f = open(filename, 'w')
    f.write(tikzpicture)
    f.close()

# def generate_latex_doc(tikzpicture, seed):
#     geometry_options = {'margin': '10mm'}
#     doc = Document(documentclass = 'scrartcl',
#                 document_options = ["paper=a4","parskip=half"],
#                 fontenc=None,
#                 inputenc=None,
#                 lmodern=False,
#                 textcomp=False,
#                 page_numbers=False,
#                 geometry_options=geometry_options)

#     doc.packages.append(Package('tikz'))
#     doc.packages.append(Package('fontspec'))
#     doc.packages.append(Package('enumitem'))
#     doc.packages.append(Package('multicol'))
#     doc.packages.append(Package('booktabs'))
#     doc.packages.append(Package('epsdice'))
#     doc.packages.append(Package('astrollogy'))

#     doc.preamble.append(Command('usetikzlibrary', 'shapes.geometric'))
#     doc.preamble.append(Command('setkomafont', NoEscape(r'section}{\setmainfont{Century Gothic}\LARGE\bfseries\center')))
#     doc.preamble.append(Command('RedeclareSectionCommand', 'section', ([r'runin=false', NoEscape(r'afterskip=0.0\baselineskip'), NoEscape(r'beforeskip=1.0\baselineskip')])))
#     doc.change_length("\columnsep", "10mm")

#     doc.append(Command(NoEscape(r'begin{center}')))
#     doc.append(NoEscape(tikzpicture))
#     doc.append(Command(NoEscape(r'end{center}')))

#     doc.append(Command(r'vspace{-8.5mm}'))

#     doc.append(NoEscape(r'\begin{center}\includegraphics[width=155mm]{Images/ASTROLLOGY_Logo.eps}\end{center}'))

#     doc.append(Command(r'vspace{-1.5mm}'))
#     doc.append(Command(NoEscape(r'setmainfont[Scale=0.95]{Century Gothic}')))
#     doc.append(Command(NoEscape(r'raggedright')))

#     doc.append(Command(r'begin{multicols}{2}'))
#     f = open('astrollogy_rules_text.tex')
#     rules_text = f.read()
#     f.close()
#     doc.append(NoEscape(rules_text))
#     doc.append(Command(r'vfill'))
#     doc.append(NoEscape(r"\textbf{Random Seed:} %i\\\textbf{Game Design:} Michael~Purcell\\\textbf{Graphic Design:} Kyle~``KYNG''~Jarratt\\\textbf{Contact:} ttkttkt@gmail.com\vfill\null" % seed))
#     doc.append(Command(r'end{multicols}'))

#     doc.append(Command(r'vspace{-5mm}'))

#     doc.append(NoEscape(r'{\Huge \dieone{} = \tikz{\pic {onestar}} \hfill \dietwo{} = \tikz{\pic {twostar}} \hfill \diethree{} = \tikz{\pic {threestar}} \hfill \diefour{} = \tikz{\pic {fourstar}} \hfill \diefive{} = \tikz{\pic {fivestar}} \hfill \diesix{} = \tikz{\pic {sixstar}}}'))

#     return doc

# def save_latex_doc(latex_doc, seed):
#     latex_doc.generate_pdf('astrollogy_starfield_%i' % seed, compiler='xelatex')

if __name__ == '__main__':
    seed = None
    seed = 983291822
    locations, seed = generate_locations(seed=seed)
    print(seed)
    tikzpicture = generate_electorate_grid(locations=locations)
    save_tikzpicture(tikzpicture=tikzpicture, filename='electorate_grid.tex')
    # latex_doc = generate_latex_doc(tikzpicture, seed)
    # save_latex_doc(latex_doc, seed)