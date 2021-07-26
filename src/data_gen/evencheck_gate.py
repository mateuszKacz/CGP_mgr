#
#   Script generates data for gate that
#    should check if inputs are even
# ---------------------------------------- #

import os

import numpy as np


# 1 0 1 0 1 is not even because sum of those '1' is 3
# 1 0 1 0 0 is even because sum of those '1' is 2

data_in = []
data_out = []
gate_var = [0, 1]
func_set = []

for elem_1 in gate_var:
    for elem_2 in gate_var:
        for elem_3 in gate_var:
            for elem_4 in gate_var:
                for elem_5 in gate_var:

                    elems = [elem_1, elem_2, elem_3, elem_4, elem_5]

                    if sum(elems) % 2 == 0:
                        elems.append(1)
                        data_out.append(elems)
                    else:
                        elems.append(0)
                        data_out.append(elems)

data_out = np.array(data_out)

path = (
    os.path.abspath(
        os.path.join(os.path.abspath(os.path.join(__file__, os.pardir)), os.pardir)
    )
) + "/user_inputs/input_even_check_gate.txt"

np.savetxt(path, data_out, delimiter=",")
