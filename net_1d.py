###################################################
#####    Class contains main class Gate1D     #####
#####     it is a core item                   #####
#####           of the simulation             #####
###################################################

import random as rnd


class Gate1D:
    """Creates 1D Gate with functions"""

    def __init__(self, params, operation_type, gate_index, value=0):

        self.active = True
        self.params = params
        self.operation_type = operation_type
        self.output_val = value
        self.gate_index = gate_index

        # input values
        self.active_input = [0, 0]

    def print_type(self):

        print(self.operation_type)

    def set_activate(self):

        self.active = True

    def set_deactivate(self):

        self.active = False

    def operation(self):
        """Defines gate operations like 'AND' 'OR' etc. """
        if self.operation_type == 'AND':

            if self.active_input[0] and self.active_input[1]:
                self.output_val = 1
            else:
                self.output_val = 0

        elif self.operation_type == 'OR':
            if self.active_input[0] == 0 and self.active_input[1] == 0:
                self.output_val = 0
            else:
                self.output_val = 1


class Net1D:
    """Creates a 1D net of gates"""

    def __init__(self, params):

        self.params = params
        self.net = [Gate1D(self.params, 'input', i, value=self.params.inputs[i]) for i in range(len(self.params.inputs))]
        self.net = self.net + [Gate1D(self.params, rnd.choice(self.params.operations), self.params.inputs_size + i) for i in
                               range(self.params.size_1d)]

        # initiate gates' links
        for gate_index in range(self.params.inputs_size, len(self.net)):

            for gate_input in range(2):
                self.change_input(gate_index, gate_input)

    def show_net(self):
        """Prints net indexes with values"""
        for gate in self.net:
            print(str(gate.gate_index) + '\t' + str(gate.output_val) + '\t' + str(gate.operation_type))

    def show_output(self):
        """Prints output value of last active gate"""

        #for gate in reversed(self.net):
           # if gate.active:
            #    print(gate.output_val)

        print(self.net[-1].output_val)

    @staticmethod
    def output(net):
        """Returns output value of last active gate"""

        for gate in reversed(net):
            if gate.active:
                return gate.output_val

    def rnd_gate(self):

        random_gate = rnd.choice(self.net)

        return random_gate.gate_index

    # random choices for gates
    def change_operation(self, gate_index):

        self.net[gate_index].operation_type = rnd.choice(self.params.operations)
        print('operation changed to: ' + self.net[gate_index].operation_type)

    def change_input(self, gate_index, input_index):

        self.net[gate_index].active_input[input_index] = self.net[rnd.randint(0, max(1, gate_index-1))].output_val
        self.net[gate_index].operation()
