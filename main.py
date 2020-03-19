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

    input_size = 5 # number of input data in one set
    number_of_inputs = 50 # number of data sets to supply the net

    data_in = [[rnd.randint(0, 100) for x in range(input_size)] for y in range(number_of_inputs)] # randomly generated inputs

    data_out = [sum(data_in[i]) for i in range(len(data_in))] # output data - in this case we're using sum and we expect the Net to "learn" how to add input values. The function can be changed of course

    # all the parameters are explained in doc-string in the parameters.py file
    params = Parameters(_operations=['+', '-', '*', '/'], _size_1d=25, _inputs=data_in, _output=data_out, _num_copies=4,
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
