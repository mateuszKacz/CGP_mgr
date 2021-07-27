#   data_gen and gate input/output generation script
#   this is sample data, normally
#   user should prepare this file
# ---------------------------------------- #

import os.path

import numpy as np


input_size = 5  # number of input data in one set
number_of_inputs = 300  # number of data sets to supply the net

data_out = []
gate_var = [0, 1]

for elem_1 in gate_var:
    for elem_2 in gate_var:
        for elem_3 in gate_var:
            for elem_4 in gate_var:
                for elem_5 in gate_var:

                    dataset = [elem_1, elem_2, elem_3, elem_4, elem_5]

                    if elem_1 and elem_2 and elem_3 and elem_4 and elem_5 == 1:
                        dataset.append(1)
                    else:
                        dataset.append(0)

                    data_out.append(dataset)

data_out = np.array(data_out)
path = (
    os.path.abspath(
        os.path.join(os.path.abspath(os.path.join(__file__, os.pardir)), os.pardir)
    )
) + "/user_inputs/input_and_gate.txt"

np.savetxt(path, data_out, fmt="%d", delimiter=",")
