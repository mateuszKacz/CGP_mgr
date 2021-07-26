#
#   Class contains main logic
#      of the simulation.
# ---------------------------------------- #

from copy import deepcopy
from math import exp
from random import random

from src.data_gather.data_gathering_automat import dump_data
from src.net_1d import Net1D


# from src.data_gather.data_gathering_automat import dump_data


class Simulation:
    """Main object of the simulation"""

    def __init__(self, _params, _data_to_viz_filename=None, _load_file=False):
        """
        :param _params: parameters of the simulation
        :type _params: Parameters
        """

        self.params = _params
        self.sim_end = False

        self.i = 0
        self.data_to_viz = {"params": [], "net": []}
        self.data_to_viz_filename = _data_to_viz_filename

        # initialize first net
        self.net = Net1D(self.params, _load_file=_load_file)

    def multiply_net(self):
        """Method creates n copies of the parent Net.

        :return: None
        """

        copies = [deepcopy(self.net) for x in range(self.params.num_copies)]

        return copies

    def calc_acceptance_probability(self, _new_net_potential, _net_potential):
        """Method calculates probability of acceptance new not optimal state. Returns
        float in range (0,1) which is in fact probability.

        Function: exp(-  delta_E / Beta)

        :param _new_net_potential: potential of the mutated (child) Net
        :type _new_net_potential: double
        :param _net_potential: potential of the parent Net
        :type _net_potential: double
        :return: float
        """

        return exp(
            -(abs(_new_net_potential - _net_potential))
            / self.params.annealing_param_values[self.i]
        )

    def show_final_solution(self):
        """
        Method prints all crucial parameters of the final solution

        :return: None
        """

        print("Final solution")
        self.net.show_whole_net()
        self.net.calculate_all_outputs()
        self.net.show_output()
        print("Data outputs:")
        print(self.params.output)
        print("Net output")
        print(self.net.prediction)
        print("Obj function value:")
        print(self.net.potential)

    def show_control_params(self):
        """
        Method prints control parameters of current iteration

        :return: None
        """

        print(f"Sim iter: {self.i}")
        print(
            "Obj func: {:.3f} \t Annealing param value: {:.2f}".format(
                self.net.potential, self.params.annealing_param_values[self.i]
            )
        )

    def save_data(self, _data_to_viz):
        """
        Method saves momentum data of the simulation to _data_to_viz dictionary.

        :param _data_to_viz: dict
        :return: None
        """
        net = []
        for gate in self.net.net:
            if gate.gate_index < self.params.input_data_size:
                net.append(
                    {
                        "gate_index": gate.gate_index,
                        "active_input_index": gate.active_input_index,
                        "active_input_value": gate.active_input_value,
                        "output_value": gate.output_val,
                        "gate_func": gate.gate_func,
                    }
                )
            else:
                net.append(
                    {
                        "gate_index": gate.gate_index,
                        "active_input_index": gate.active_input_index,
                        "active_input_value": gate.active_input_value,
                        "output_value": gate.output_val,
                        "gate_func": gate.gate_func.__name__,
                    }
                )
        _data_to_viz["net"].append(net)
        _data_to_viz["params"].append(
            {
                "output_gate_index": self.net.output_gate_index,
                "output": self.net.output,
                "potential": self.net.potential,
                "temperature": self.params.annealing_param_values[self.i],
            }
        )

    def get_params_history(self):
        """
        Method returns all params as a list of dictionaries.

        :return: dict
        """

        potential = [step["potential"] for step in self.data_to_viz["params"]]
        steps = [i for i in range(len(self.data_to_viz["params"]))]
        param_history = {"potential": potential, "step": steps}

        return param_history

    def run_step(self, n=1):
        """
        Method runs n steps of the simulation.

        :param n: how many steps of the simulation should be performed by the method
        :type n: int
        :return: None
        """

        for i in range(n):

            self.i += 1  # increment step indicator

            potentials = []  # stores momentum potentials of all net-clones
            copies = self.multiply_net()  # makes n_copies of Net

            for copy in copies:
                copy.mutate()  # makes mutation of the copy
                potentials.append(copy.calculate_total_potential())

            # choose best copy
            best_copy_index = potentials.index(min(potentials))

            if copies[best_copy_index].potential < self.net.potential:
                self.net = deepcopy(copies[best_copy_index])
            else:
                if self.params.annealing_scheme:
                    acc_pdb = self.calc_acceptance_probability(
                        copies[best_copy_index].potential, self.net.potential
                    )

                    if random() <= acc_pdb:
                        self.net = deepcopy(copies[best_copy_index])

            if self.net.potential == 0.0:
                self.sim_end = True
                break

    def run(self, show_progress=False):
        """Method runs net mutation on all Gates"""

        # save first initial state of the system
        if self.params.data_gather_interval:
            self.save_data(self.data_to_viz)

        while self.params.annealing_param_values[self.i] > 0.0:

            # essential algorithm step
            self.run_step()

            # save local state of the net
            if self.params.data_gather_interval:
                if self.i % self.params.data_gather_interval == 0:
                    self.save_data(self.data_to_viz)

            # print control params
            if show_progress:
                if self.i % 200 == 0:
                    self.show_control_params()

            # simulation's end conditions
            if (
                self.i % (self.params.steps - 1) == 0
            ):  # quit if initial number of simulation steps is reached
                if show_progress:
                    self.show_final_solution()
                self.save_data(self.data_to_viz)
                break

            if self.net.potential == 0.0:
                if show_progress:
                    self.show_final_solution()
                self.save_data(self.data_to_viz)
                break

        self.sim_end = True

        # Dump simulation data to json file
        if self.data_to_viz_filename:

            dump_data(self.data_to_viz, self.data_to_viz_filename)
