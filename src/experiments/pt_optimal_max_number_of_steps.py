#
#   Experiment gathers data for the simulations with Parallel Tempering
#   algorithm, when number_of_copies of the system varies
# ---------------------------------------- #

import pathlib

import numpy as np
from numpy import genfromtxt
from tqdm import tqdm

from src.utils.save_data import save_to_csv

from ..data_gather.data_gathering_automat import gen_cgp_data
from ..user_inputs import gate_functions as gate_func, objective_function as obj_func


def main():
    MAIN_USER_INPUT_PATH = pathlib.Path().absolute() / "src/user_inputs"
    MAIN_DATA_GATHER_PATH = pathlib.Path().absolute() / "src/data_gather/pt"

    gate_fun = [
        gate_func.bin_and,
        gate_func.bin_nand,
        gate_func.bin_or,
        gate_func.bin_xor,
    ]
    data_even_check_gate = genfromtxt(
        MAIN_USER_INPUT_PATH / "input_even_check_gate.txt", delimiter=","
    )

    num_sim = 50
    switch_step = 40
    steps = [10 ** x for x in range(2, 5)]
    annealing_scheme = ["const"]
    pt_scheme = ["gaussian", 1]
    temperatures = np.linspace(0.01, 150, 7)
    all_data = []

    for max_steps in tqdm(steps, desc="Number of steps value:"):
        data = gen_cgp_data(
            _gate_func=gate_fun,
            _obj_func=obj_func.obj_func,
            _data=data_even_check_gate,
            _input_data_size=5,
            _steps=max_steps,
            _annealing_scheme=annealing_scheme,
            _pt_temps=temperatures,
            _algorithm="PT",
            _pt_switch_step=switch_step,
            _pt_scheme=pt_scheme,
            _show_progress=False,
            _num_of_sim=num_sim,
        )
        all_data = all_data + data

    save_to_csv(
        all_data,
        MAIN_DATA_GATHER_PATH
        / f"pt_evencheck_numsim{num_sim}_switch_step{switch_step}_steps{steps}"
        f"_ptscheme_{pt_scheme[0]}{pt_scheme[1]}_sa_{annealing_scheme[0]}_"
        f"optimal_max_steps_extension.csv",
    )


if __name__ == "__main__":
    main()
