#
#   Script generates data for random gate
#    from possible provided gate functions
# ---------------------------------------- #

from random import choice
import numpy as np
import os.path
import user_inputs.gate_functions as gate_func

input_size = 5  # number of input data in one set
number_of_inputs = 300  # number of data sets to supply the net

data_out = []
gate_var = [0, 1]
gate_functions = [gate_func.bin_and, gate_func.bin_nand, gate_func.bin_or, gate_func.bin_xor]
func_set = []

for i in range(4):
    func = choice(gate_functions)
    func_set.append(func)

for elem_1 in gate_var:
    for elem_2 in gate_var:
        for elem_3 in gate_var:
            for elem_4 in gate_var:
                for elem_5 in gate_var:

                    dataset = [elem_1, elem_2, elem_3, elem_4, elem_5]
                    gate = dataset[0]

                    for i in range(1, len(dataset)):
                        gate = func_set[i-1]((gate, dataset[i]))

                    dataset.append(gate)
                    data_out.append(dataset)


data_out = np.array(data_out)

path = (os.path.abspath(os.path.join(os.path.abspath(os.path.join(__file__, os.pardir)), os.pardir))) + "/user_inputs/input_random_gate_2.txt"

np.savetxt(path, data_out, fmt='%d', delimiter=',')

print(func_set)
