#
#   Experiment gathers data for the simulations with Parallel Tempering
#   algorithm with optimal temp ratio calculation applied
# ---------------------------------------- #

from numpy import genfromtxt
from tqdm import tqdm

from ..user_inputs import objective_function as obj_func
from ..user_inputs import gate_functions as gate_func
import pathlib
from ..data_gather.data_gathering_automat import gen_cgp_data, save_to_csv


def main():
    MAIN_USER_INPUT_PATH = pathlib.Path().absolute() / 'src/user_inputs'
    MAIN_DATA_GATHER_PATH = pathlib.Path().absolute() / 'src/data_gather/pt'

    gate_fun = [gate_func.bin_and, gate_func.bin_nand, gate_func.bin_or, gate_func.bin_xor]
    data_even_check_gate = genfromtxt(MAIN_USER_INPUT_PATH / 'input_even_check_gate.txt', delimiter=',')

    temperatures = [10. * i for i in range(1, 9)]
    num_sim = 300
    switch_step = 10
    steps = 5000
    annealing_scheme = ['const']
    pt_scheme = ['gaussian', 1]

    data = gen_cgp_data(_gate_func=gate_fun, _obj_func=obj_func.obj_func, _data=data_even_check_gate,
                        _input_data_size=5, _steps=steps, _annealing_scheme=annealing_scheme, _pt_temps=temperatures,
                        _algorithm='PT', _pt_switch_step=switch_step, _pt_scheme=pt_scheme, _show_progress=False,
                        _num_of_sim=num_sim, _pt_num_parallel_copies=7)

    save_to_csv(data, MAIN_DATA_GATHER_PATH / f'pt_evencheck_numsim{num_sim}_switch_step{switch_step}_steps{steps}'
                                              f'_ptscheme_{pt_scheme[0]}{pt_scheme[1]}_sa_{annealing_scheme[0]}_'
                                              f'optimal_temp_calculation_fixed_temps.csv')


if __name__ == "__main__":
    main()
