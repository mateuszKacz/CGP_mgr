#
#   Experiment gathers example data for the simulations
#   with Parallel Tempering algorithm
# ---------------------------------------- #

from numpy import genfromtxt
from ..user_inputs import objective_function as obj_func
from ..user_inputs import gate_functions as gate_func
from ..cgpsa import CGPSA
from ..parallel_tempering import PT
import pathlib
from ..data_gather.data_gathering_automat import gen_cgp_data


def main():
    MAIN_USER_INPUT_PATH = pathlib.Path().absolute() / 'src/user_inputs'

    gate_fun = [gate_func.bin_and, gate_func.bin_nand, gate_func.bin_or, gate_func.bin_xor]
    data_even_check_gate = genfromtxt(MAIN_USER_INPUT_PATH / 'input_even_check_gate.txt', delimiter=',')

    cgp_no_sa = CGPSA(_gate_func=gate_fun, _obj_func=obj_func.obj_func, _data=data_even_check_gate, _input_data_size=5,
                      _steps=5000, _annealing_scheme=['const'])
    pt_alg = PT(cgp_no_sa, _temperatures=[10*x for x in range(1, 8)], _switch_step=10, _show_progress=True,
                _scheme=['gaussian', 1])
    pt_alg.run()


if __name__ == "__main__":
    main()
