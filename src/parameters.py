#
#   Class contains main parameteters
#   and initial values
# ---------------------------------------- #

from numpy import genfromtxt


class Parameters:
    """Class contains main initial values and parameters of the simulation

    :param operations: list of possible operations performed by gates
    :type func_names: list
    :param size_1d: number of gates to create in the network
    :type size_1d: int
    :param inputs: array of data entries to put through the net
    :type inputs: list
    :param output: array of answers for the net
    :type output: list
    :param num_copies: number of copies created and mutated every step of the simulation
    :type num_copies: int
    :param pdb_link_change: probability of link changing in the Gate
    :type pdb_link_change: float
    :param pdb_gate_operation_change: probability of operation mutation in the Gate
    :type pdb_gate_operation_change: float
    :param _pdb_output_change: probability of changing the output gate
    :type _pdb_output_change: float
    :param _beta_const: control parameter which is a representation of cooling (simulated anealing)
    :type _beta_const: float
    """

    def __init__(self, _paths, _size_1d, _input_data_size, _num_copies, _pdb_link_change=0.2,
                 _pdb_gate_operation_change=0.2, _pdb_output_change=0.2, _beta_const=1.):

        # User files
        self.data = genfromtxt('user_inputs/input_data.txt', delimiter=',')
        self.path_gate_func = _paths['gate_func']
        self.path_obj_func = _paths['obj_func']
        self.func_names = list(genfromtxt(_paths['gate_func_names'], delimiter='\n'))  # list of possible func_names performed by the Gate (one at a time)

        # Probabilities
        self.pdb_link_change = _pdb_link_change
        self.pdb_gate_operation_change = _pdb_gate_operation_change
        self.pdb_output_change = _pdb_output_change

        # 1D Net Params
        self.size_1d = _size_1d  # number of calculating Gates in the Net
        self.input_length = _input_data_size  # number of input Gates
        self.total_size = self.size_1d + self.input_length  # total number of Gates in the Net (including input Gates)

        # Other parameters
        self.num_copies = _num_copies  # number of Net copies created every step of the mutation

        # Annealing parameter
        self.beta_const = _beta_const
