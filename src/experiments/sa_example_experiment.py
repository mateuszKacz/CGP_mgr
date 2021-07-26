#
#   Experiment gathers example data for the simulations
#   with Simulated Annealing algorithm
# ---------------------------------------- #

import pathlib

from numpy import genfromtxt

from ..cgpsa import CGPSA
from ..data_gather import data_gathering_automat as data_gather
from ..user_inputs import gate_functions as gate_func, objective_function as obj_func


def main():
    MAIN_USER_INPUT_PATH = pathlib.Path().absolute() / "src/user_inputs"
    OUTPUT_PATH = pathlib.Path().absolute() / "src/data_gather/cgp/EVENCHECKgate"

    gate_fun = [
        gate_func.bin_and,
        gate_func.bin_nand,
        gate_func.bin_or,
        gate_func.bin_xor,
    ]
    data_even_check_gate = genfromtxt(
        MAIN_USER_INPUT_PATH / "input_even_check_gate.txt", delimiter=","
    )

    cgpsa = CGPSA(
        _gate_func=gate_fun,
        _obj_func=obj_func.obj_func,
        _data=data_even_check_gate,
        _input_data_size=5,
        _steps=5000,
        _data_gather_interval=1,
    )
    cgpsa.run(show_progress=True)
    data_gather.save_to_csv(
        cgpsa.simulation.get_params_history(),
        OUTPUT_PATH / "every_step_momentum_data_evencheck_gate_cgp_alone_sa.txt",
    )


if __name__ == "__main__":
    main()
