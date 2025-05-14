import pymol
from pymol import cmd, stored

def get_center(selection = 'sele'):
    """
    DESCRIPTION
    Get the center coordinates of a selection in PyMOL.

    USAGE
    get_center [selection]

    ARGUMENTS
    selection = string: PyMOL selection {default: (all)}

    EXAMPLE
    get_center
    get_center chain A
    get_center resi 10-20
    """
    model = cmd.get_model(selection)
    center = [0, 0, 0]
    n = 0
    for a in model.atom:
        center = [center[i] + a.coord[i] for i in range(3)]
        n += 1
    center = [center[i]/n for i in range(3)]
    print(f"Center of '{selection}': ({center[0]:.2f}, {center[1]:.2f}, {center[2]:.2f})")
    return center

cmd.extend('get_center', get_center)
