#
#   Main script executing crucial
#   procedures and initializing simulation
# ---------------------------------------- #

import random as rnd
import tkinter as tk

from src.gui import GUI
from src.parameters import Parameters
from src.simulation import Simulation


def main():
    """Main function"""

    # TODO: fix parameters
    # all the parameters are explained in doc-string in the parameters.py file
    params = Parameters(_operations=['+', '-', '*', '/'], _size_1d=25, _inputs=[[1,1,1,1,1]], _output=[1], _num_copies=4,
                        _pdb_link_change=0.1, _pdb_gate_operation_change=0.1, _pdb_output_change=0.1, _beta_const=100)

    # ['+', '-', '*', '/'] - is the current list of managed functions

    # creating simulation instance
    simulation = Simulation(params)

    # GUI creation
    root = tk.Tk()
    gui = GUI(params, simulation, _master=root)
    gui.mainloop()


if __name__ == "__main__":
    main()
