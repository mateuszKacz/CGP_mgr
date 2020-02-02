###################################################
#####    Main script executing crucial        #####
#####  procedures and initializing simulation #####
#####                                         #####
###################################################

import random as rnd
import tkinter as tk

from gui import GUI
from parameters import Parameters
from simulation import Simulation


def main():
    """Main function"""

    input_size = 5
    number_of_inputs = 20

    data = [[rnd.randint(0, 10) for x in range(input_size)] for y in range(number_of_inputs)]

    data_sum = [sum(data[i]) for i in range(len(data))]

    params = Parameters(_operations=['+', '-', '*'], _size_1d=15, _inputs=data, _output=data_sum, _num_copies=4,
                        _pdb_link_change=0.9, _pdb_gate_operation_change=0.9)

    simulation = Simulation(params)

    # GUI creation
    root = tk.Tk()
    gui = GUI(params, simulation, _master=root)
    gui.mainloop()


if __name__ == "__main__":
    main()
