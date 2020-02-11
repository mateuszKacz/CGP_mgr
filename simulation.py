#   Class contains main logic
#      of the simulation.
# ------------------------------------ #

from copy import deepcopy
from math import exp
from random import random
from net_1d import Net1D
from pandas import DataFrame


class Simulation:
    """Main object of the simulation"""

    def __init__(self, params):

        self.params = params

        # initialize first net
        self.net = Net1D(self.params)

    def multiply_net(self):
        """Method creates n copies of the parent Net."""

        copies = [deepcopy(self.net) for x in range(self.params.num_copies)]

        return copies

    def calc_acceptance_probability(self, new_net_potential, net_potential):
        """Method calculates probability of acceptance new not optimal state.
        Function: e(-k * d_E/T)

        :param new_net_potential: potential of the mutated (child) Net
        :type new_net_potential: double
        :param net_potential: potential of the parent Net
        :type net_potential: double
        :return pdb(0,1)
        """

        return exp(- self.params.k_const * (abs(new_net_potential-net_potential))/self.params.temp)

    def simulate(self, _sim_continue):
        """Method runs net mutation on all Gates"""
        acc_pdb_data = []
        i = 0
        while _sim_continue:

            i += 1  # iterator
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
                acc_pdb_data.append(acc_pdb)
                if random() <= acc_pdb:
                    self.net = copies[best_copy_index]

            # controls
            if i % 100 == 0:
                print(i)
                print(f'{self.net.potential} \t {self.params.temp}')
                if self.params.temp > 15:

                    self.params.temp -= 1
                else:
                    self.params.temp -= 0.1


            # end simulation
            if i % 100000 == 0:
                _sim_continue = False
                self.net.show_whole_net()
                self.net.calculate_all_outputs()
                self.net.show_output()
                print(self.net.output)
                print(self.params.output)
                print(self.net.potential)

                data = DataFrame(acc_pdb_data)
                data.to_csv('data.txt')

            if self.net.potential < 0.1:
                _sim_continue = False
                self.net.show_whole_net()
                self.net.calculate_all_outputs()
                self.net.show_output()
                print(self.net.output)
                print(self.params.output)
                print(self.net.potential)
                print(i)


