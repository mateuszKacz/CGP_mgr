###################################################
#####    Class contains main class Gate       #####
#####     it is a core item of the core       #####
#####       item of the simulation            #####
###################################################

import random as rnd
import numpy as np


class Gate:
    """Contains a scheme of the logical gate. It is suited for every logical operation
    and it depend on the gate_type"""

    # gate_operations = ['AND', 'OR', 'none']
    # gate_types = in, layer, out or none
    def __init__(self, g_type='layer', operation_type='AND'):

        self.active = False
        self.g_type = g_type
        self.operation_type = operation_type
        self.value = 0

        # list of "coordinates" of gates to connect as touples
        self.connect = []

    def print_type(self):

        print(self.g_type)

    def set_active(self):

        self.active = True

    def set_deactive(self):

        self.active = False

   # def operation(self):


class Net:

    """Contains a net of Gates and main operation functions"""

    def __init__(self, params):

        self.params = params
        self.operation_types_dict = {0: 'AND', 1: 'OR', 2: 'AND', 3: 'OR', 4: 'AND', 5: 'OR'}
        self.net = [[Gate(operation_type=self.operation_types_dict[x]) for x in range(self.params.hidden_layers_height)]
                    for y in range(self.params.hidden_layers_width)]

    def last_active(self):
        """Searches for active gate from the last possible layer"""

        for i in range(self.params.hidden_layers_width):
            for j in range(self.params.hidden_layers_height):
                if self.net[self.params.hidden_layers_width-i-1][j].active:
                    return self.params.hidden_layers_width-i-1, j

    def show_net(self):
        """Prints Net Gates with status"""

        for i in range(self.params.hidden_layers_width):
            for j in range(self.params.hidden_layers_height):
                print('Column: %d \t Row: %d \t Active: %s \t Type: %s \t Val: %d' % (i, j, self.net[i][j].active, self.net[i][j].operation_type, self.net[i][j].value))

    def activate(self, i, j):
        """Activate chosen gate"""

        self.net[i][j].set_active()

    def setup(self):
        """Set random initial state"""

        for j in range(self.params.hidden_layers_height):
            self.net[0][j].value = self.params.input[j]

    def result(self):
        """Indicates current result of the network - output"""
        i, j = self.last_active()
        print(self.net[i][j].value)




