#
#   Class contains main logic
#      of the simulation.
# ---------------------------------------- #

from copy import deepcopy
from math import exp
from random import random
from src.net_1d import Net1D
import json

NUM_SIM = 10000


class Simulation:
    """Main object of the simulation"""

    def __init__(self, _params, _load=False):
        """
        :param _params: parameters of the simulation
        :type _params: Parameters
        """

        self.params = _params

        self.annealing_step = float((self.params.annealing_param-1)/NUM_SIM)
        # initialize first net
        self.net = Net1D(self.params, _load=_load)

    def multiply_net(self):
        """Method creates n copies of the parent Net."""

        copies = [deepcopy(self.net) for x in range(self.params.num_copies)]

        return copies

    def calc_acceptance_probability(self, _new_net_potential, _net_potential):
        """Method calculates probability of acceptance new not optimal state.
        Function: e(-  delta_E / Beta)

        :param _new_net_potential: potential of the mutated (child) Net
        :type _new_net_potential: double
        :param _net_potential: potential of the parent Net
        :type _net_potential: double
        :return pdb(0,1)
        """

        return exp(-(abs(_new_net_potential-_net_potential))/self.params.annealing_param)

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

    def save_data(self, _data_to_viz):
        """
        Method saves momentum data of the simulation to _data_to_viz dictionary.
        :param _data_to_viz: dict
        :return: None
        """
        net = []
        for gate in self.net.net:
            if gate.gate_index < self.params.input_length:
                net.append({
                    'gate_index': gate.gate_index,
                    'active_input_index': gate.active_input_index,
                    'active_input_value': gate.active_input_value,
                    'output_value': gate.output_val,
                    'gate_func': gate.gate_func,
                })
            else:
                net.append({
                    'gate_index': gate.gate_index,
                    'active_input_index': gate.active_input_index,
                    'active_input_value': gate.active_input_value,
                    'output_value': gate.output_val,
                    'gate_func': gate.gate_func.__name__,
                })
        _data_to_viz['net'].append(net)
        _data_to_viz['params'].append({'output_gate_index': self.net.output_gate_index,
                                       'output': self.net.output,
                                       'potential': self.net.potential,
                                       'temperature': self.params.annealing_param
                                       })

    def simulate(self):
        """Method runs net mutation on all Gates"""

        data_to_viz = {'params': [], 'net': []}

        i = 0
        while self.params.annealing_param >= 0.1:

            i += 1  # simulation iterator
            self.params.annealing_param -= self.annealing_step

            potentials = []
            copies = self.multiply_net()  # makes n_copies of Net

            for copy in copies:
                copy.mutate()  # makes mutation of the copy
                potentials.append(copy.calculate_total_potential())

            # choose best copy
            best_copy_index = potentials.index(min(potentials))

            if copies[best_copy_index].potential < self.net.potential:
                self.net = deepcopy(copies[best_copy_index])
            else:
                acc_pdb = self.calc_acceptance_probability(copies[best_copy_index].potential, self.net.potential)

                if random() <= acc_pdb:
                    self.net = copies[best_copy_index]

            # export local state of the net
            if i % 10 == 0:
                self.save_data(data_to_viz)

            # print control params
            if i % 200 == 0:
                print(f'Sim iter: {i}')
                print('Obj func: {:.3f} \t Annealing param value: {:.2f}'.format(self.net.potential, self.params.annealing_param))

            # simulation's end conditions
            if i % NUM_SIM == 0:  # quit if initial number of simulation steps is reached
                self.show_final_solution()
                break

            if self.net.potential == 0.:
                self.show_final_solution()
                break

        # save final state
        self.save_data(data_to_viz)

        with open("net_viz/viz_data.txt", 'w') as file:
            json.dump(data_to_viz, file)

        print("Data to viz save complete")
