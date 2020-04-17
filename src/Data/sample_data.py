#
#   Data generation script
#   this is sample data normally
#   user should prepare give data file
# ---------------------------------------- #


# TODO: Generate binary data

from random import randint

input_size = 5  # number of input data in one set
number_of_inputs = 50  # number of data sets to supply the net

data_in = [[randint(0, 100) for x in range(input_size)] for y in range(number_of_inputs)]  # randomly generated inputs

data_out = [sum(data_in[i]) for i in range(len(data_in))]  # output data - in this case we're using sum and we expect the Net to "learn" how to add input values. The function can be changed of course
