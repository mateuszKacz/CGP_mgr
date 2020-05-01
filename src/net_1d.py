#
#   Class contains classes Gate1D and Net1D - those
#   are the main objects of the simulation.
# ---------------------------------------- #

import random as rnd
import src.user_inputs.objective_function as obj_func
from src.user_inputs import gate_functions


class Gate1D:
    """Creates 1D Gate with functions."""

    def __init__(self, _params, _gate_func, _gate_index, _value=0.):

        """
        :param _params: parmeters of the simulation
        :type _params: Parameters
        :param _gate_func: one of the func_names listed in _params.func_names
        :type _gate_func: str
        :param _gate_index: index of the gate in net
        :type _gate_index: int
        :param _value: initial output_val of the gate
        :type _value: double
        """

        self.params = _params
        self.gate_func = _gate_func
        self.output_val = _value
        self.gate_index = _gate_index

        # input values
        self.active_input_index = [0, 0]
        self.active_input_value = [0., 0.]

    def print_type(self):
        """Prints gate's current operation."""

        print(self.gate_func)

    def change_operation(self):
        """Randomly changes gate operation."""

        if rnd.random() <= self.params.pdb_gate_operation_change:

            self.gate_func = rnd.randint(0, len(self.params.func_names) - 1)
            self.run_operation()

    def run_operation(self):
        """Calculates gate output_val."""

        self.output_val = eval('gate_functions.' + self.params.func_names[self.gate_func])(self.active_input_value)


def rnd_gate(stop, start=0):
    """Chooses random gate from the Net.

    :param stop: gate index in the net to stop random choice
    :type stop: int
    :param start: gate index to start random choice
    :type start: int
    :return random gate index in range(start, stop) of type int
    """

    return rnd.randint(start, stop - 1)


class Net1D:
    """Creates a 1D net of gates"""

    def __init__(self, params):

        """
        :param params: parameters of the simulation
        :type params: Parameters
        """

        self.params = params
        self.net = [Gate1D(self.params, 'input', i, _value=0) for i in range(self.params.input_length)]
        self.net = self.net + [Gate1D(self.params, rnd.randint(0, len(self.params.func_names) - 1),
                                      self.params.input_length + i) for i in range(self.params.size_1d)]

        # Net Output
        self.output_gate_index = rnd_gate(self.params.total_size)
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
                rand_gate = rnd_gate(gate_index)
                self.net[gate_index].active_input_index[link] = rand_gate
                self.net[gate_index].active_input_value[link] = self.net[rand_gate].output_val

    # Print methods
    def show_net(self):
        """Prints net indexes with values"""

        for gate in self.net[:self.params.input_length]:
            print(str(gate.gate_index) + '\t' + str(gate.output_val) + '\t' + gate.gate_func)

        for gate in self.net[self.params.input_length:]:
            print(str(gate.gate_index) + '\t' + str(gate.output_val) + '\t' + self.params.func_names[gate.gate_func])

    def show_output(self):
        """Prints output of the Net"""

        print(f'Output gate: {self.output_gate_index}  Output _value: {self.net[self.output_gate_index].output_val}')

    def show_whole_net(self):
        """Prints all Gates indexes, func_names and links"""

        for gate in self.net[:self.params.input_length]:
            print(str(gate.gate_index) + '\t' + str(gate.output_val) + '\t' + gate.gate_func)

        for gate in self.net[self.params.input_length:]:
            print('Gate: ' + str(gate.gate_index) + '   \t' + 'Output: ' + str(gate.output_val) + '   \t' + 'InIndex: ' + str(gate.active_input_index) + '   \t' + self.params.func_names[gate.gate_func])

    # Random methods
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
            self.net[gate_index].active_input_index[0] = rnd_gate(gate_index)
        # Atempt to mutate second link
        if rnd.random() <= self.params.pdb_link_change:
            self.net[gate_index].active_input_index[1] = rnd_gate(gate_index)

    # Update methods
    def update_gate_value(self, gate_index):
        """Method updates input values of the Gate and runs operation on it

        :param gate_index: index of the gate in the net to update _value in
        :type gate_index: int
        """
        self.net[gate_index].active_input_value[0] = self.net[self.net[gate_index].active_input_index[0]].output_val
        self.net[gate_index].active_input_value[1] = self.net[self.net[gate_index].active_input_index[1]].output_val
        self.net[gate_index].run_operation()

    # Calculation methods
    def run_data(self, _input_set):
        """Method takes one input set of data _input_set and it's iterable to extract coresponding output"""

        for x in range(self.params.input_length): # set input values in input gates
            self.net[x].output_val = _input_set[x]

        self.calculate_all_outputs()

        return self.net[self.output_gate_index].output_val

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
        prediction = []

        # Calculates differences between outputs in all data sets
        for i in range(len(self.params.data)):
            prediction.append(self.run_data(self.params.data[i][:self.params.input_length]))

        self.potential = obj_func.obj_func(self.params.data[:][self.params.input_length:], prediction)

        return self.potential
