#
#   Implementation of Parallel Tempering
#   algorithm for CGP
# ---------------------------------------- #

from math import exp
from .cgpsa import CGPSA
from random import randint, random, choice
from copy import deepcopy
from tqdm import tqdm


class PT:
    """
    Class implements Parallel Tempering algorithm for CGP objects. The purpose of this additional method is to
    improve the dynamic properties of Monte Carlo method used in Simulated Annealing algorithm.
    """

    def __init__(self, _cgpsa_object, _temperatures, _switch_step=10, _cgp_steps=None, _scheme=None,
                 _show_progress=False):
        """
        Init method takes one CGP object initialized by the user and then creates copies following chosen Parallel
        Tempering scheme.

        Number of copies in the system is specified by the length of the _temperatures list.

        :param _cgpsa_object: CGPSA initialized object - it is a scheme for other PT copies to follow
        :type _cgpsa_object: CGPSA
        :param _temperatures: list of temperatures values to use for the copies of the CGP
        :type _temperatures: list
        :param _switch_step: how many iterations proceed between the systems gave an ability to switch
        :type _switch_step: int
        :param _cgp_steps: total number of CGP steps
        :type _cgp_steps: int
        :param _scheme: this parameter defines the temperatures in the systems - we can use fixed set of temperatures
            for clones ("discrete") or use distributions thus the temperatures in the systems would float ("gaussian").
            Possible values ["discrete", "gaussian"]. Choosing "gaussian" will require additional parameters to add
            Sigma - gaussian deviation parameter.
            E. g. ["gaussian", 1] - std = 1, mean would be our system initial temperature so we can skip this parameter.
        :param _show_progress: if False then control params are not shown during the simulation
        :type _show_progress: boolean
        """

        # if user is giving explicitly how many CGP steps should be performed we have to update it with the CGP object
        if _cgp_steps:
            self.pt_steps = int(_cgp_steps / _switch_step)
            _cgpsa_object.params.steps = _cgp_steps + 1
        else:
            self.pt_steps = int(_cgpsa_object.params.steps / _switch_step)
            _cgpsa_object.params.steps += + 1

        if _scheme in ["discrete", ["discrete"], None]:
            self.scheme = "discrete"
            self.is_gaussian = False

        elif _scheme[0] == "gaussian":
            self.scheme = _scheme[0]
            self.is_gaussian = True
            self.gauss_sigma = _scheme[1]  # set gaussian deviation
        else:
            raise Exception("Wrong scheme! Choose 'gaussian' or 'discrete' ...")

        self.temperatures = sorted(_temperatures)
        self.num_parallel_copies = len(self.temperatures)
        self.show_progress = _show_progress
        self.switch_step = _switch_step
        self.curr_pt_step = 0  # current PT step indicator
        self.total_steps = 0
        self.number_of_switches = 0
        self.switch_ratio = 0.
        self.best_solution_steps = _cgp_steps

        # creating CGP objects with different temperatures
        self.cgp = [CGPSA(_gate_func=_cgpsa_object.params.gate_func, _obj_func=_cgpsa_object.params.obj_func,
                          _data=_cgpsa_object.params.data, _input_data_size=_cgpsa_object.params.input_data_size,
                          _size_1d=_cgpsa_object.params.size_1d, _num_copies=_cgpsa_object.params.num_copies,
                          _pdb_mutation=_cgpsa_object.params.pdb_mutation,
                          _annealing_param=_temperatures[i],
                          _annealing_scheme=_scheme, _steps=_cgpsa_object.params.steps)
                    for i in range(self.num_parallel_copies)]

        self.sim_end = [cgp.simulation.sim_end for cgp in self.cgp]
        self.best_potential = self.calc_best_solution_potential()

    def calc_switch_probability(self, i, j):
        """
        Method calculates probability of state-exchange between systems. Essentially it follows Metropolis-Hastings
        criterion: p = min(1; exp[ (|E_i - E_j|) * (|1/k*T_i - 1/k*T_j|) ])
        where:

        E_i, E_j - potentials of two systems
        T_i, T_j - temperatures of two systems
        k - in my version 'k' parameter is skipped, because we can just use temperature as control parameter (like Beta)
        """

        return min(1., exp(abs(self.cgp[i].simulation.net.potential -
                               self.cgp[j].simulation.net.potential) *
                           abs(1 / self.cgp[i].simulation.params.annealing_param_values[self.cgp[i].simulation.i] -
                               1 / self.cgp[j].simulation.params.annealing_param_values[self.cgp[j].simulation.i])))

    def show_control_params(self):
        """
        Method shows current state of the running systems

        :return: None
        """
        message = f"Simulation #: {self.total_steps} \n"

        for cgp_obj in self.cgp:
            message += f"Copy #: {self.cgp.index(cgp_obj)} \t Temp: {cgp_obj.params.annealing_param_init_value} \t " \
                       f"Pot: {cgp_obj.simulation.net.potential} \n"

        print(message)

    def show_final_solution(self):
        """
        Method prints out the final solutions of the PT algorithm

        :return: None
        """

        print(f"Best solution steps: {self.best_solution_steps} \n Best potential: {self.best_potential}")

    def calc_best_solution_steps(self):
        """Method shows best solution"""
        potentials = [cgp_object.simulation.net.potential for cgp_object in self.cgp]
        steps = [cgp_object.simulation.i for cgp_object in self.cgp]

        return steps[potentials.index(min(potentials))]

    def calc_best_solution_potential(self):
        """Method shows best potential"""
        potentials = [cgp_object.simulation.net.potential for cgp_object in self.cgp]

        return min(potentials)

    def calc_switch_ratio(self):
        """Method calculates the switch ratio after the simulation"""
        return self.number_of_switches / self.pt_steps

    def update_sim_end(self):
        self.sim_end = [cgp.simulation.sim_end for cgp in self.cgp]

    def run(self):
        """
        Method implements core Parallel Tempering algorithm
        """

        for step in tqdm(range(self.pt_steps), desc='PT steps'):

            self.curr_pt_step += 1
            self.total_steps += self.switch_step
            # run # of iterations of CGP mutation alg
            for cgp_instance in self.cgp:
                cgp_instance.simulation.run_step(self.switch_step)

            self.update_sim_end()

            if sum(self.sim_end) > 0:
                self.best_solution_steps = self.calc_best_solution_steps()
                self.best_potential = self.calc_best_solution_potential()
                if self.show_progress:
                    self.show_final_solution()
                break

            # randomly select first system
            i = randint(0, self.num_parallel_copies - 1)

            # switch between systems is not completely random - there can be switch only if the systems are in their
            # neighborhood, thus the second system is chosen less randomly - the first and last object has only one
            # neighbor

            if i == 0:
                j = i + 1
            elif i == self.num_parallel_copies - 1:
                j = i - 1
            else:
                j = choice([i - 1, i + 1])

            proba = self.calc_switch_probability(i, j)

            if random() <= proba:
                # if criterion is met switch systems
                self.cgp[i].simulation.net.net, self.cgp[j].simulation.net.net = \
                    deepcopy(self.cgp[j].simulation.net.net), deepcopy(self.cgp[i].simulation.net.net)
                self.number_of_switches += 1
            else:
                continue

            if self.show_progress:
                print(self.sim_end)
                self.show_control_params()

        self.best_solution_steps = self.calc_best_solution_steps()
        self.best_potential = self.calc_best_solution_potential()
        self.switch_ratio = self.calc_switch_ratio()

        if self.show_progress:
            self.show_final_solution()
