#
#   Class contains main parameteters
#   and initial values
# ---------------------------------------- #

from numpy import genfromtxt
import src.user_inputs.gate_functions as gate_functions


class Parameters:
    """Class contains main initial values and parameters of the simulation"""

    def __init__(self, _gate_func, _obj_func, _data, _input_data_size, _size_1d, _num_copies, _pdb_mutation=0.03,
                 _annealing_param=100):
        """
        :param _gate_func: list of functions (gate operations)
        :type _gate_func: list
        :param _obj_func: user-defined method fro Net evaluation
        :type _obj_func: object
        :param _data: list of values to feed the net
        :type _data: ndarray
        :param _input_data_size: number of input values to the Net
        :type _input_data_size: int
        :param _size_1d: number of gates to create in the network
        :type _size_1d: int
        :param _num_copies: number of copies created and mutated every step of the simulation
        :type _num_copies: int
        :param _pdb_mutation: Probability of mutation (link change, operation change, output gate change)
        :type _pdb_mutation: float
        :param _annealing_param: control parameter which is a representation of cooling (simulated anealing)
        :type _annealing_param: float
        """

        # User files
        self.data = _data
        self.gate_func = _gate_func
        self.obj_func = _obj_func

        # Input Data
        self.output = [int(x[_input_data_size]) for x in self.data]

        # Probabilities
        self.pdb_mutation = _pdb_mutation

        # 1D Net Params
        self.size_1d = _size_1d  # number of calculating Gates in the Net
        self.input_length = _input_data_size  # number of input Gates
        self.total_size = self.size_1d + self.input_length  # total number of Gates in the Net (including input Gates)

        # Other parameters
        self.num_copies = _num_copies  # number of Net copies created every step of the mutation

        # Annealing parameter
        self.annealing_param = _annealing_param
