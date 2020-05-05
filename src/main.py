#
#   Main script executing crucial
#   procedures and initializing simulation
# ---------------------------------------- #


import tkinter as tk
import src.user_inputs.objective_function as obj_func
import src.user_inputs.gate_functions as gate_func
from src.cgp import CGP
from numpy import genfromtxt


def main():
    """Main function"""
    # input_random_gate = nand/or/or/and
    gate_fun = [gate_func.bin_and, gate_func.bin_nand, gate_func.bin_or, gate_func.bin_xor]

    data = genfromtxt('user_inputs/input_random_gate.txt', delimiter=',')

    cgp = CGP(_gate_func=gate_fun, _obj_func=obj_func.obj_func, _data=data, _input_data_size=5)

    cgp.start()


if __name__ == "__main__":
    main()
