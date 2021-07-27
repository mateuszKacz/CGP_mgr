#
#   Experiment gathers data for the simulations
#   with Simulated Annealing algorithm - geometric scheme with
#   logarithmic annealing parameter scale
# ---------------------------------------- #
import math
import pathlib

import numpy as np
from numpy import genfromtxt
from tqdm import tqdm

from src.utils.save_data import save_to_csv
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
        MAIN_USER_INPUT_PATH / "input_even_check_gate.txt", delimiter=","
    )

    # PARAMETERS
    schemes = [["geom", 0.99], ["linear"]]
    annealing_param = [
        x for x in np.logspace(math.log(0.005), math.log(200), 10, base=math.e)
    ]
    max_steps = 3000
    num_sim = 200

    for scheme in tqdm(schemes, desc="Scheme:"):
        all_data = []
        for temp in tqdm(annealing_param, desc="Temperatures done"):
            data = data_gather.gen_cgp_data(
                _gate_func=gate_fun,
                _obj_func=obj_func.obj_func,
                _data=data_even_check_gate,
                _input_data_size=5,
                _size_1d=15,
                _num_copies=5,
                _pdb_mutation=0.06,
                _annealing_param=temp,
                _annealing_scheme=scheme,
                _steps=max_steps,
                _num_of_sim=num_sim,
            )
            all_data = all_data + data

        file_path = MAIN_DATA_PATH / f"even_gate_temp_log_scale_0005_200_{scheme}.csv"

        save_to_csv(all_data, file_path)

    if __name__ == "__main__":
        main()


if __name__ == "__main__":
    main()
