#
#   Experiment gathers data for the simulations with CGP
#   algorithm
# ---------------------------------------- #

import pathlib

from numpy import genfromtxt
from tqdm import tqdm

from src.utils.save_data import save_to_csv

from ..data_gather.data_gathering_automat import gen_cgp_data
from ..user_inputs import gate_functions as gate_func, objective_function as obj_func


def main():
    MAIN_USER_INPUT_PATH = pathlib.Path().absolute() / "src/user_inputs"
    MAIN_DATA_GATHER_PATH = pathlib.Path().absolute() / "src/data_gather/cgp"

    gate_fun = [
        gate_func.bin_and,
        gate_func.bin_nand,
        gate_func.bin_or,
        gate_func.bin_xor,
    ]
    data_even_check_gate = genfromtxt(
        MAIN_USER_INPUT_PATH / "input_even_check_gate.txt", delimiter=","
    )

    num_sim = 99

    retry = 50
    steps = 5000
    annealing_scheme = ["const"]
    all_data = []

    for i in tqdm(range(retry), desc="Retry:"):
        data = gen_cgp_data(
            _gate_func=gate_fun,
            _obj_func=obj_func.obj_func,
            _data=data_even_check_gate,
            _input_data_size=5,
            _steps=steps,
            _annealing_scheme=annealing_scheme,
            _algorithm="SA",
            _show_progress=False,
            _num_of_sim=num_sim,
            _retry=i,
        )
        all_data = all_data + data

    save_to_csv(
        all_data,
        MAIN_DATA_GATHER_PATH
        / f"cgp_alone_pt_comparison_retries{retry}_num_sim_{num_sim}_steps_{steps}.csv",
    )


if __name__ == "__main__":
    main()
