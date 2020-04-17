#
#   Data generation script
#   this is sample data normally
#   user should prepare give data file
# ---------------------------------------- #

from random import randint
import numpy as np

input_size = 5  # number of input data in one set
number_of_inputs = 50  # number of data sets to supply the net

data_out = []

for line in range(number_of_inputs):

    dataset = [randint(0, 1) for x in range(input_size)]
    gate = dataset[0]

    for i in range(1, input_size):
        if dataset[i] == 1 and gate == 1:
            gate = 1
        else:
            gate = 0
    dataset.append(gate)
    data_out.append(dataset)

data_out = np.array(data_out)

np.savetxt('input_data.txt', data_out, fmt='%d', delimiter=',')
