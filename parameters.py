###################################################
#####    Class contains main parameteters     #####
#####        and initial values               #####
#####                                         #####
###################################################


class Parameters:
    """Class contains main initial values and parameters of the simulation"""

    def __init__(self, operations, size_1d, inputs, output, num_gates_active, pdb_link_change=0.35,
                 pdb_gate_operations_change=0.2):

        self.inputs = inputs
        self.output = output
        self.num_gates_active = num_gates_active
        self.pdb_link_change = pdb_link_change
        self.pdb_gate_operations_change = pdb_gate_operations_change
        self.operations = operations
        # 2D Net params
        self.hidden_layers_width = 4
        self.hidden_layers_height = 5
        # 1D Net Params
        self.size_1d = size_1d
        self.inputs_size = len(self.inputs)
        self.total_size = self.size_1d + self.inputs_size

