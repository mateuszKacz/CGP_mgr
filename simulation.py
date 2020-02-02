#   Class contains main logic
#      of the simulation.
# ------------------------------------ #

from copy import deepcopy
from math import exp

from net_1d import Net1D


class Simulation:
    """Main object of the simulation"""

    def __init__(self, params):

        self.params = params

        # initialize first net
        self.net = Net1D(self.params)

    # TODO: main_loop

    def multiply_net(self):
        """Method creates n copies of the parent Net."""

        copies = [deepcopy(self.net) for x in range(self.params.num_copies)]

        return copies

    def calc_acceptance_probability(self, new_net_potential, net_potential):
        """Method calculates probability of acceptance new not optimal state.
        Function: e(-k * d_E/T)

        :param new_net_potential: potential of the mutated (child) Net
        :type new_net_potential: float
        :param net_potential: potential of the parent Net
        :type net_potential: float
        :return pdb(0,1)
        """

        return exp(- self.params.k_const * abs(new_net_potential-net_potential)/self.params.temp)

    def simulate(self):
        """Method runs net mutation on all Gates"""
        # TODO: all the simulation function
