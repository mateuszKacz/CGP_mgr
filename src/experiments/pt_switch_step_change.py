#
#   Experiment gathers example data for the simulations
#   with Parallel Tempering algorithm
# ---------------------------------------- #

import pathlib

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

    temperatures = [x * 0.1 for x in range(1, 70, 10)]
    num_sim = 30
    switch_steps = [x for x in range(1, 50, 5)]
    steps = 5000
    annealing_scheme = ["const"]
    pt_scheme = ["gaussian", 1]

    all_data = []
    for switch_step in tqdm(switch_steps, desc="Switch step: "):
        data = gen_cgp_data(
            _gate_func=gate_fun,
            _obj_func=obj_func.obj_func,
            _data=data_even_check_gate,
            _input_data_size=5,
            _steps=steps,
            _annealing_scheme=annealing_scheme,
            _pt_temps=temperatures,
            _algorithm="PT",
            _pt_switch_step=switch_step,
            _pt_scheme=pt_scheme,
            _show_progress=False,
            _num_of_sim=num_sim,
        )

        all_data += data

    save_to_csv(
        all_data,
        MAIN_DATA_GATHER_PATH
        / f"pt_example_numsim{num_sim}_switch_steps1_50_steps{steps}_ptscheme"
        f"{pt_scheme[0]}{pt_scheme[1]}_sa{annealing_scheme[0]}.csv",
    )


if __name__ == "__main__":
    main()
