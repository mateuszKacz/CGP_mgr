#
#
#
# ---------------------------------------- #

from src.parameters import Parameters
from src.simulation import Simulation
import json


class CGP:
    """Main CGP-algorithm object which is initialized by the User."""

    def __init__(self, _gate_func=None, _obj_func=None, _data=None, _input_data_size=0, _size_1d=15, _num_copies=5,
                 _pdb_mutation=0.06, _annealing_param=100, _load=False):
        """
        :param _gate_func: list of functions (gate operations)
        :type _gate_func: list
        :param _obj_func: function that calculates fitness of the Net
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
        :param _load: flag that indicates in CGP object should be read from saved .csv file
        :type _load: bool
        """

        if _load:
            self.load("cgp_evolved_net.txt")
        else:
            print("Setting Parameters...")
            self.params = Parameters(_gate_func=_gate_func,
                                     _obj_func=_obj_func,
                                     _data=_data,
                                     _input_data_size=_input_data_size,
                                     _size_1d=_size_1d,
                                     _num_copies=_num_copies,
                                     _pdb_mutation=_pdb_mutation,
                                     _annealing_param=_annealing_param)

            print("Creating Simulation components...")
            self.simulation = Simulation(self.params)
            print("CGP object ready")

    def start(self):
        """
        Method starts the simulation
        :return: None
        """

        # Starting simulation
        print("Starting simulation...")

        # starting main simulation loop
        self.simulation.simulate()

    def show_net(self):
        """
        Method prints created Net
        :return: None
        """
        # Printing initial Net
        print("\nPrinting Net \n")
        self.simulation.net.show_whole_net()
        self.simulation.net.show_output()

    def load(self, _path):
        """
        Method loads saved Net - once evolved scheme

        :param _path: path of .txt json saved file - given by user
        :type _path: str
        :return: None
        """

        print(f"Opening the file...{_path}")
        with open(_path, 'r') as file:

            data = json.load(file)

        parameters = data['parameters'][0]
        size_1d = len(data['net']) - parameters['input_length']

        print('Loading Parameters...')
        self.params = Parameters(_gate_func=parameters['gate_func'],
                                 _obj_func=[],
                                 _data=[],
                                 _input_data_size=parameters['input_length'],
                                 _size_1d=size_1d,
                                 _num_copies=parameters['num_copies'],
                                 _pdb_mutation=parameters['pdb_mutation'],
                                 )

        self.simulation = Simulation(self.params, _load=True)
        print('Loading Parameters - completed')
        print("Loading Net...")

        # net params
        self.simulation.net.output_gate_index = data['net_params']['output_gate_index']
        self.simulation.net.output = data['net_params']['output']
        self.simulation.net.potential = data['net_params']['potential']

        # net
        for i in range(len(data['net'])):
            self.simulation.net.net[i].gate_index = data['net'][i]['gate_index']
            self.simulation.net.net[i].active_input_index = data['net'][i]['active_input_index']
            self.simulation.net.net[i].active_input_value = data['net'][i]['active_input_value']
            self.simulation.net.net[i].output_val = data['net'][i]['output_value']
            self.simulation.net.net[i].gate_func = data['net'][i]['gate_func']

        print("Loading Net - completed")
        print("Load complete")

    def save(self, _path=""):
        """
        Method saves CGP object in a .txt json file

        :param _path: path of the file to be saved - given by user
        :type _path: str
        :return: None
        """

        if _path == "":
            _path = "cgp_evolved_net.txt"

        print(f"Saving evolved Net in {_path}")

        data = {'parameters': []}
        data['parameters'].append({
            'gate_func': [func.__name__ for func in self.simulation.params.gate_func],
            'obj_func': self.simulation.params.obj_func.__name__,
            'input_length': self.simulation.params.input_length,
            'num_copies': self.simulation.params.num_copies,
            'pdb_mutation': self.simulation.params.pdb_mutation
        })
        data['net'] = []

        for gate in self.simulation.net.net:

            if gate.gate_index < self.simulation.params.input_length:
                data['net'].append({
                    'gate_index': gate.gate_index,
                    'active_input_index': gate.active_input_index,
                    'active_input_value': gate.active_input_value,
                    'output_value': gate.output_val,
                    'gate_func': gate.gate_func,
                })
            else:
                data['net'].append({
                    'gate_index': gate.gate_index,
                    'active_input_index': gate.active_input_index,
                    'active_input_value': gate.active_input_value,
                    'output_value': gate.output_val,
                    'gate_func': gate.gate_func.__name__,
                })

        data['net_params'] = {'output_gate_index': self.simulation.net.output_gate_index,
                              'output': self.simulation.net.output,
                              'potential': self.simulation.net.potential
                              }

        with open(_path, 'w') as file:
            json.dump(data, file)

        print("Save complete")
