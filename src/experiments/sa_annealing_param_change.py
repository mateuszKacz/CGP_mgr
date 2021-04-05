#
#   Experiment gathers data for the simulations
#   with annealing_param changing
# ---------------------------------------- #

from numpy import genfromtxt
import numpy as np
from ..user_inputs import objective_function as obj_func
from ..user_inputs import gate_functions as gate_func
from tqdm import tqdm
from ..data_gather import data_gathering_automat as data_gather
import pathlib


def main():
    MAIN_DATA_PATH = pathlib.Path().absolute().parent / 'data_gather/'

    gate_fun = [gate_func.bin_and, gate_func.bin_nand, gate_func.bin_or, gate_func.bin_xor]
    data_even_check_gate = genfromtxt('user_inputs/input_even_check_gate.txt', delimiter=',')

    schemes = [{'scheme': ['geom', 0.99], 'annealing_param': [x for x in np.linspace(0.005, 2, 30)]}]

    num_sim = 30
    steps = 3000

    for scheme in tqdm(schemes, desc='Schemes'):

        all_data = []
        for temp in tqdm(scheme['annealing_param'], 'Temperatures done'):
            data = data_gather.gen_cgp_data(_gate_func=gate_fun, _obj_func=obj_func.obj_func,
                                            _data=data_even_check_gate,
                                            _input_data_size=5, _size_1d=15, _num_copies=5, _pdb_mutation=0.06,
                                            _annealing_param=temp, _annealing_scheme=scheme['scheme'], _steps=steps,
                                            _num_of_sim=num_sim)
            all_data = all_data + data

        file_path = MAIN_DATA_PATH / 'even_gate_temp_0005_2_geom.csv'

        data_gather.save_to_csv(all_data, file_path)


if __name__ == "__main__":
    main()
