#
#
#
# ---------------------------------------- #

from src.parameters import Parameters
from src.simulation import Simulation


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
            self.load()
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
        print("Initial Network\n")
        self.simulation.net.show_net()

    def load(self, _path):
        # TODO: Create working load() function
        """
        Method loads saved Net - once evolved scheme
        :return: None
        """
        with open(_path, 'r') as file:
            size_1d = file.readline()


    def save(self, _path=""):
        # TODO: Create working save() function
        """
        Method saves CGP object in a .csv file
        :param _path: path of the saved file - given by user
        :type _path: str
        :return: None
        """
        if _path == "":
            _path = "cgp_evolved_net.csv"
        with open(_path, 'wb') as file:
            # write size of Net
            file.write(bytearray(len(self.simulation.net.net)))
            file.write(bytearray('\n'))

            # write Gates parameters
            for gate in self.simulation.net.net:
                file.write(bytearray(str(gate.gate_index) + ',' + str(gate.active_input_index) + ',' +
                                     str(gate.active_input_value) + ',' + str(gate.output_val) + ',' +
                                     str(gate.gate_func)))
                file.write(bytearray('\n'))

            # write Parameters
            file.write(bytearray(str(self.simulation.params.gate_func) + ',' +
                                 str(self.simulation.params.input_data_size) + ',' +
                                 str(self.simulation.params.num_copies) + ',' +
                                 str(self.simulation.params.pdb_mutation)))
