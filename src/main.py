#
#   Main script executing crucial
#   procedures and initializing simulation
# ---------------------------------------- #

import src.user_inputs.objective_function as obj_func
import src.user_inputs.gate_functions as gate_func
from numpy import genfromtxt
from src.cgpsa import CGPSA
from src.parallel_tempering import PT
import src.data_gather.data_gathering_automat as data_gather

# TODO: Travelling Salesman Problem


def main():
    """Main function"""
    # input_random_gate = nand/or/or/and
    gate_fun = [gate_func.bin_and, gate_func.bin_nand, gate_func.bin_or, gate_func.bin_xor]

    data_and_gate = genfromtxt('user_inputs/input_data.txt', delimiter=',')
    data_random_gate = genfromtxt('user_inputs/input_random_gate.txt', delimiter=',')
    data_even_check_gate = genfromtxt('user_inputs/input_even_check_gate.txt', delimiter=',')

    # cgpsa = CGPSA(_gate_func=gate_fun, _obj_func=obj_func.obj_func, _data=data, _input_data_size=5,
    #              _steps=1000, _load_file="data_gather/test_data/cgp_test.txt")

    # cgpsa.show_net()

    # data gather for one simulation
    cgpsa = CGPSA(_gate_func=gate_fun, _obj_func=obj_func.obj_func, _data=data_even_check_gate, _input_data_size=5,
                  _steps=5000, _annealing_scheme=['geom', 0.99])
    cgpsa.start()
    # data_gather.save_to_csv(cgpsa.simulation.get_params_history(), "every_step_momentum_data.txt")

    # cgpsa.show_net()
    # cgpsa.save("cgp_test.txt")

    # data = data_gather.gen_cgp_data(_gate_func=gate_fun, _obj_func=obj_func.obj_func, _data=data, _input_data_size=5,
    #                                 _size_1d=15, _num_copies=5, _pdb_mutation=0.06, _annealing_param=100,
    #                                 _annealing_scheme=None, _steps=5000, _load=False, _num_of_sim=200)
    #
    # data_gather.save_to_csv(data, "args_test.csv")

    # Parallel Tempering

    # cgp_no_sa = CGPSA(_gate_func=gate_fun, _obj_func=obj_func.obj_func, _data=data, _input_data_size=5, _steps=5000)
    # pt_alg = PT(cgp_no_sa, _temperatures=[10*x for x in range(1, 8)], _switch_step=10)
    # pt_alg.run()


if __name__ == "__main__":
    main()
