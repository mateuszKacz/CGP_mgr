#
#   Implementation of Parallel Tempering
#   algorithm for CGPSA
# ---------------------------------------- #

from math import exp
from src.cgpsa import CGPSA
from random import randint, random
from copy import deepcopy


class PT:
    """
    Class implements Parallel Tempering algorithm for CGPSA objects. The purpose of this additional method is to
    improve the dynamic properties of Monte Carlo method used in Simulated Annealing algorithm.
    """

    def __init__(self, _num_parallel_copies=4):
        # TODO: add parameters of PT

        self.num_parallel_copies = _num_parallel_copies
        # TODO: add CGPSA parameters
        self.cgpsa = [CGPSA() for x in range(self.num_parallel_copies)]
        self.sim_end = [cgpsa.simulation.sim_end for cgpsa in self.cgpsa]

    def calc_switch_probability(self, i, j):
        """
        Method calculates probability of state-exchange between systems. Essentially it follows Metropolis-Hastings
        criterion: p = min(1; exp[ (E_i - E_j) * (1/k*T_i - 1/k*T_j) ])
        where:

        E_i, E_j - potentials of two systems
        T_i, T_j - temperatures of two systems
        k - in my version 'k' parameter is skipped, because we can just use temperature as control parameter (like Beta)
        """

        return min(1., exp((self.cgpsa[i].simulation.net.potential -
                            self.cgpsa[j].simulation.net.potential) *
                           (1/self.cgpsa[i].simulation.params.annealing_param_values[self.cgpsa[i].simulation.i] -
                            1/self.cgpsa[j].simulation.params.annealing_param_values[self.cgpsa[j].simulation.i])))

    def pt_algorithm(self):
        """
        Method implements core Parallel Tempering algorithm
        """

        while sum(self.sim_end) < self.num_parallel_copies:

            # randomly select two systems
            i = randint(0, self.num_parallel_copies)
            j = randint(0, self.num_parallel_copies)

            if random() <= self.calc_switch_probability(i, j):
                # if criterion is met switch systems
                self.cgpsa[i].simulation.net.net, self.cgpsa[j].simulation.net.net = \
                    deepcopy(self.cgpsa[j].simulation.net.net), deepcopy(self.cgpsa[i].simulation.net.net)
