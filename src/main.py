#
#   Main script executing crucial
#   procedures and initializing simulation
# ---------------------------------------- #

import src.user_inputs.objective_function as obj_func
import src.user_inputs.gate_functions as gate_func
from numpy import genfromtxt
import src.data_gather.data_gathering_automat as data_gather

# TODO: gather data - SA
# TODO: implement Parallel Tempering algorithm


def main():
    """Main function"""
    # input_random_gate = nand/or/or/and
    gate_fun = [gate_func.bin_and, gate_func.bin_nand, gate_func.bin_or, gate_func.bin_xor]

    data = genfromtxt('user_inputs/input_data.txt', delimiter=',')
    #
    # cgpsa = CGPSA(_gate_func=gate_fun, _obj_func=obj_func.obj_func, _data=data, _input_data_size=5,
    #             _annealing_scheme=['geom', 0.99], _steps=1000, _load=False)
    # cgpsa.start()

    data = data_gather.gen_cgp_data(_gate_func=gate_fun, _obj_func=obj_func.obj_func, _data=data, _input_data_size=5,
                                    _size_1d=15, _num_copies=5, _pdb_mutation=0.06, _annealing_param=100,
                                    _annealing_scheme=None, _steps=5000, _load=False, _num_of_sim=200)

    data_gather.save_to_csv(data, "cgp_alone_test.csv")


if __name__ == "__main__":
    main()
