#
#   Class contains main parameters
#   and initial values
# ---------------------------------------- #

from numpy import genfromtxt
import src.user_inputs.gate_functions as gate_functions
import numpy as np
from math import log


class Parameters:
    """Class contains main initial values and parameters of the simulation"""

    def __init__(self, _gate_func, _obj_func, _data, _input_data_size, _size_1d, _num_copies, _pdb_mutation=0.03,
                 _annealing_param_init_value=100, _annealing_scheme=None, _steps=10000):
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
        :param _annealing_param_init_value: control parameter which is a representation of cooling (simulated anealing)
        :type _annealing_param_init_value: float
        :param _annealing_scheme: parameter defines the scheme of annealing_param's reduction; one of
        ['geom', 'linear', 'log']. In 'geom' the next argument is also 'a' parameter, so it would look like ['geom', 0.9]
        if None, then Simulated Annealing is not performed.
        :type _annealing_scheme: list
        :param _steps: number of steps of the simulation
        :type _steps: int
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
        self.input_data_size = _input_data_size  # number of input Gates
        self.total_size = self.size_1d + self.input_data_size  # total number of Gates in the Net(including input Gates)

        # Other parameters
        self.num_copies = _num_copies  # number of Net copies created every step of the mutation
        self.steps = _steps

        # Annealing parameter
        self.annealing_param_init_value = _annealing_param_init_value
        self.annealing_scheme = _annealing_scheme
        self.annealing_param_values = self.calc_annealing_param_values()

    def calc_annealing_param_values(self):
        """
        Method calculates set of annealing parameter's values following chosen scheme from ['geom', 'linear', 'log']
        For 'geom' we have additional parameter 'a' [0,1] which shapes the slope of the geometric curve.

        :return: ndarray
        """

        if self.annealing_scheme is None:
            _annealing_param_values = [self.annealing_param_init_value for k in range(self.steps)]

        elif self.annealing_scheme[0] == 'geom':
            _annealing_param_values = [self.annealing_param_init_value*(self.annealing_scheme[1] ** k) for k in
                                       range(self.steps)]

        elif str(self.annealing_scheme[0]) == 'linear':
            _annealing_param_values = [self.annealing_param_init_value/(k + 1) for k in range(self.steps)]

        elif self.annealing_scheme[0] == 'log':
            _annealing_param_values = [self.annealing_param_init_value/(1 + log(k + 1)) for k in range(self.steps)]

        else:
            raise ValueError(f"Wrong annealing scheme {self.annealing_scheme}...choose one from ['geom','linear', 'log']")

        return np.array(_annealing_param_values, dtype='float')
