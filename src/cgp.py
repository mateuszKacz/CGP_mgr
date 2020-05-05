#
#
#
# ---------------------------------------- #

from src.parameters import Parameters
from src.simulation import Simulation


class CGP:
    """Main CGP-algorithm object which is initialized by the User."""

    def __init__(self, _gate_func, _obj_func, _data, _input_data_size, _size_1d=15, _num_copies=5, _pdb_link_change=0.1,
                 _pdb_gate_operation_change=0.1, _pdb_output_change=0.1, _annealing_param=100):

        print("Setting Parameters...")
        self.params = Parameters(_gate_func=_gate_func,
                                 _obj_func=_obj_func,
                                 _data=_data,
                                 _input_data_size=_input_data_size,
                                 _size_1d=_size_1d,
                                 _num_copies=_num_copies,
                                 _pdb_link_change=_pdb_link_change,
                                 _pdb_gate_operation_change=_pdb_gate_operation_change,
                                 _pdb_output_change=_pdb_output_change,
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
        :return:
        """
        # Printing initial Net
        print("Initial Network\n")
        self.simulation.net.show_net()
