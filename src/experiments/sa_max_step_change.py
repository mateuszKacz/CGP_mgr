#
#   Experiment gathers data for the simulations
#   with steps parameter changing
# ---------------------------------------- #

import pathlib

from numpy import genfromtxt
from tqdm import tqdm

from ..data_gather import data_gathering_automat as data_gather
from ..user_inputs import gate_functions as gate_func, objective_function as obj_func


def main():
    MAIN_DATA_PATH = pathlib.Path().absolute() / "src/data_gather/cgpsa"
    MAIN_USER_INPUT_PATH = pathlib.Path().absolute() / "src/user_inputs"

    gate_fun = [
        gate_func.bin_and,
        gate_func.bin_nand,
        gate_func.bin_or,
        gate_func.bin_xor,
    ]
    data_even_check_gate = genfromtxt(
        MAIN_USER_INPUT_PATH / "input_random_gate_2.txt", delimiter=","
    )

    max_steps = [10 ** x for x in range(1, 7)]

    schemes = [{"scheme": ["linear"], "max_steps": max_steps}]

    num_sim = 30
    annealing_param = 50

    for scheme in tqdm(schemes, desc="Schemes"):

        all_data = []
        for steps in tqdm(scheme["max_steps"], "Max_steps"):
            data = data_gather.gen_cgp_data(
                _gate_func=gate_fun,
                _obj_func=obj_func.obj_func,
                _data=data_even_check_gate,
                _input_data_size=5,
                _size_1d=15,
                _num_copies=5,
                _pdb_mutation=0.06,
                _annealing_param=annealing_param,
                _annealing_scheme=scheme["scheme"],
                _steps=steps,
                _num_of_sim=num_sim,
            )
            all_data = all_data + data

        file_path = (
            MAIN_DATA_PATH
            / f"random2_gate_max_step_10_10000000_{scheme['scheme'][0]}.csv"
        )

        data_gather.save_to_csv(all_data, file_path)


if __name__ == "__main__":
    main()
