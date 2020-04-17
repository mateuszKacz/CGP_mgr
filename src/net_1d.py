#
#   Class contains classes Gate1D and Net1D - those
#   are the main objects of the simulation.
# ---------------------------------------- #

import random as rnd
from math import sqrt


class Gate1D:
    """Creates 1D Gate with functions."""

    def __init__(self, params, operation_type, gate_index, value=0.):

        """
        :param params: parmeters of the simulation
        :type params: Parameters
        :param operation_type: one of the operations listed in params.operations
        :type operation_type: str
        :param gate_index: index of the gate in net
        :type gate_index: int
        :param value: initial output_val of the gate
        :type value: double
        """

        self.params = params
        self.operation_type = operation_type
        self.output_val = value
        self.gate_index = gate_index

        # input values
        self.active_input_index = [0, 0]
        self.active_input_value = [0., 0.]

    def print_type(self):
        """Prints gate's current operation."""

        print(self.operation_type)

    def change_operation(self):
        """Randomly changes gate operation."""

        if rnd.random() <= self.params.pdb_gate_operation_change:

            self.operation_type = self.params.operations[rnd.randint(0, len(self.params.operations)-1)]
            self.run_operation()

    def run_operation(self):
        """Calculates gate output_val."""

        if self.operation_type == '+':

            self.output_val = sum(self.active_input_value)

        elif self.operation_type == '-':

            self.output_val = self.active_input_value[0] - self.active_input_value[1]

        elif self.operation_type == '*':

            self.output_val = self.active_input_value[0] * self.active_input_value[1]

        elif self.operation_type == '/':
            if self.active_input_value[1] > 0:
                self.output_val = self.active_input_value[0] / self.active_input_value[1]
            elif self.active_input_value[0] > 0:
                self.output_val = self.active_input_value[1] / self.active_input_value[0]
            else:
                self.output_val = 0


class Net1D:
    """Creates a 1D net of gates"""

    def __init__(self, params):

        """
        :param params: parmeters of the simulation
        :type params: Parameters
        """

        self.params = params
        self.net = [Gate1D(self.params, 'input', i, value=self.params.inputs[0][i]) for i in range(self.params.input_length)]
        self.net = self.net + [Gate1D(self.params, rnd.choice(self.params.operations), self.params.input_length + i) for i in
                               range(self.params.size_1d)]

        # Net Output
        self.output_gate_index = self.rnd_gate(self.params.total_size)
        self.output = self.net[self.output_gate_index].output_val
        self.potential = self.calculate_total_potential()

        # inits
        self.init_gates_links()  # sets initial links
        self.calculate_all_outputs()  # sets initial output_val in the gates

    # Init methods
    def init_gates_links(self):
        """Method randomly initiates gates' input links"""

        for gate_index in range(self.params.input_length, len(self.net)):
            for link in range(2):
                rand_gate = self.rnd_gate(gate_index)
                self.net[gate_index].active_input_index[link] = rand_gate
                self.net[gate_index].active_input_value[link] = self.net[rand_gate].output_val

    # Print methods
    def show_net(self):
        """Prints net indexes with values"""

        for gate in self.net:
            print(str(gate.gate_index) + '\t' + str(gate.output_val) + '\t' + str(gate.operation_type))

    def show_output(self):
        """Prints output of the Net"""

        print(f'Output gate: {self.output_gate_index}  Output value: {self.net[self.output_gate_index].output_val}')

    def show_whole_net(self):
        """Prints all Gates indexes, operations and links"""

        for gate in self.net:
            print('Gate: ' + str(gate.gate_index) + '   \t' + 'Output: ' + str(gate.output_val) + '   \t' + 'InIndex: ' + str(gate.active_input_index) + '   \t' + str(gate.operation_type))

    # Random methods
    def rnd_gate(self, stop, start=0):
        """Chooses random gate from the Net.

        :param stop: gate index in the net to stop random choice
        :type stop: int
        :param start: gate index to start random choice
        :type start: int
        :return random gate index in range(start, stop) of type int
        """

        return rnd.randint(start, stop - 1)

    def rnd_output_gate(self):
        """Chooses random gate from the net"""

        if rnd.random() <= self.params.pdb_output_change:

            self.output_gate_index = rnd.randint(0, self.params.total_size - 1)

        self.output = self.net[self.output_gate_index].output_val

    def rnd_link_change(self, gate_index):
        """Method randomly changes the link fo the chosen Gate.

        :param gate_index: index of the gate in the net to change link in
        :type gate_index: int
        """
        # Atempt to mutate first link
        if rnd.random() <= self.params.pdb_link_change:
            self.net[gate_index].active_input_index[0] = self.rnd_gate(gate_index)
        # Atempt to mutate second link
        if rnd.random() <= self.params.pdb_link_change:
            self.net[gate_index].active_input_index[1] = self.rnd_gate(gate_index)

    # Update methods
    def update_gate_value(self, gate_index):
        """Method updates input values of the Gate and runs operation on it

        :param gate_index: index of the gate in the net to update value in
        :type gate_index: int
        """
        self.net[gate_index].active_input_value[0] = self.net[self.net[gate_index].active_input_index[0]].output_val
        self.net[gate_index].active_input_value[1] = self.net[self.net[gate_index].active_input_index[1]].output_val
        self.net[gate_index].run_operation()

    # Calculation methods
    def run_data(self, _input_set, i):
        """Method takes one input set of data _input_set and it's iterable to extract coresponding output"""

        for x in range(self.params.input_length): # set input values in input gates
            self.net[x].output_val = _input_set[x]

        self.calculate_all_outputs()

        return pow((self.params.output[i] - self.net[self.output_gate_index].output_val), 2)

    def calculate_all_outputs(self):
        """Method recalculates all values in gates - all net"""

        for gate_index in range(self.params.input_length, self.params.total_size):

            self.update_gate_value(gate_index)

    def mutate(self):
        """Method tries to mutate every gate from the Net - it's operation and links with probability"""

        for gate_index in range(self.params.input_length, self.params.total_size):
            self.rnd_link_change(gate_index)  # atempts to change the links and recalc if needed
            self.net[gate_index].change_operation()  # atempts to change the operation and recalc output if needed
            self.rnd_output_gate()  # atempts to change output gate and sets new output if needed

    def calculate_total_potential(self):
        """Method checks how close the net is to real answer.
        Function used is quadratic length. sqrt(sum([output-data_output]^2))
        """
        diff_list = []

        # Calculates differences between outputs in all data sets
        for i in range(len(self.params.inputs)):
            diff_list.append(self.run_data(self.params.inputs[i], i))

        self.potential = sqrt(sum(diff_list))

        return self.potential
