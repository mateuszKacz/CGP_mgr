#
#   Implementation of Parallel Tempering
#   algorithm for CGP
# ---------------------------------------- #

from math import exp
from src.cgpsa import CGPSA
from random import randint, random
from copy import deepcopy


class PT:
    """
    Class implements Parallel Tempering algorithm for CGP objects. The purpose of this additional method is to
    improve the dynamic properties of Monte Carlo method used in Simulated Annealing algorithm.
    """

    def __init__(self, _cgpsa_object, _num_parallel_copies=4, _scheme=None):
        """
        Init method takes one CGP object initialized by the user and then creates copies following chosen Parallel
        Tempering scheme.

        :param _cgpsa_object: CGPSA initialized object - it is a scheme for other PT copies to follow
        :type _cgpsa_object: CGPSA
        :param _num_parallel_copies: user defines how many copies of the system should be created for the PT alg.
        :type _num_parallel_copies: int
        :param _scheme: this parameter defines the temperatures in the systems - we can use fixed set of temperatures
            for clones ("discrete") or use distributions thus the temperatures in the systems would float ("gaussian").
            Possible values ["discrete", "gaussian"]. Choosing "gaussian" will require additional parameters to add std
            val.
            E. g. ["gaussian", 1] - std = 1, mean would be our system initial temperature so we can skip this parameter.
        :type _scheme: list

        """

        if _scheme is None:
            _scheme = ["discrete"]

        self.num_parallel_copies = _num_parallel_copies
        self.cgpsa = [CGPSA(_gate_func=_cgpsa_object.params.gate_func, _obj_func=_cgpsa_object.params.obj_func,
                            _data=_cgpsa_object.params.data, _input_data_size=_cgpsa_object.params.input_data_size,
                            _size_1d=_cgpsa_object.params.size_1d, _num_copies=_cgpsa_object.params.num_copies,
                            _pdb_mutation=_cgpsa_object.params.pdb_mutation,
                            _annealing_param=_cgpsa_object.params.annealing_param_init_value,
                            _annealing_scheme=_cgpsa_object.params.annealing_scheme, _steps=_cgpsa_object.params.steps)
                      for x in range(self.num_parallel_copies)]

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
                           (1 / self.cgpsa[i].simulation.params.annealing_param_values[self.cgpsa[i].simulation.i] -
                            1 / self.cgpsa[j].simulation.params.annealing_param_values[self.cgpsa[j].simulation.i])))

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
                # TODO: add condition: if sim's are running then switch
                self.cgpsa[i].simulation.net.net, self.cgpsa[j].simulation.net.net = \
                    deepcopy(self.cgpsa[j].simulation.net.net), deepcopy(self.cgpsa[i].simulation.net.net)
