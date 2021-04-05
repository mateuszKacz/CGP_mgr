#
#   Experiment gathers data for the simulations
#   with Simulated Annealing algorithm - geometric scheme with best params
# ---------------------------------------- #

from numpy import genfromtxt
from ..user_inputs import objective_function as obj_func
from ..user_inputs import gate_functions as gate_func
import pathlib
from ..data_gather import data_gathering_automat as data_gather


def main():
    MAIN_DATA_PATH = pathlib.Path().absolute() / 'src/data_gather/cgpsa'
    MAIN_USER_INPUT_PATH = pathlib.Path().absolute() / 'src/user_inputs'

    gate_fun = [gate_func.bin_and, gate_func.bin_nand, gate_func.bin_or, gate_func.bin_xor]
    data_even_check_gate = genfromtxt(MAIN_USER_INPUT_PATH / 'input_even_check_gate.txt', delimiter=',')

    # PARAMETERS
    scheme = ['geom', 0.99]
    annealing_param = 25
    max_steps = 4000
    num_sim = 300

    data = data_gather.gen_cgp_data(_gate_func=gate_fun, _obj_func=obj_func.obj_func,
                                    _data=data_even_check_gate,
                                    _input_data_size=5, _size_1d=15, _num_copies=5, _pdb_mutation=0.06,
                                    _annealing_param=annealing_param, _annealing_scheme=scheme,
                                    _steps=max_steps, _num_of_sim=num_sim)

    file_path = MAIN_DATA_PATH / f"evencheck_gate_best_params_{scheme[0]}.csv"

    data_gather.save_to_csv(data, file_path)


if __name__ == "__main__":
    main()
