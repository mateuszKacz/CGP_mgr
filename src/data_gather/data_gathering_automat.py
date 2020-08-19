#
#   Automatization of data gathering process
#
# ---------------------------------------- #

import pandas as pd
from os import chdir, mkdir
import pathlib
#from src.cgpsa import CGPSA
from multiprocessing import Pool
import json


# TODO: add multi threading
def gen_cgp_data(_gate_func=None, _obj_func=None, _data=None, _input_data_size=0, _size_1d=15, _num_copies=5,
                 _pdb_mutation=0.06, _annealing_param=100, _annealing_scheme=None, _steps=10000, _load_file=False,
                 _num_of_sim=10):
    """
    Function takes CGPSA parameters with some additional variables and perform numerous simulations of CGPSA algorithm.

    :param _gate_func: list of functions (gate operations)
    :type _gate_func: list
    :param _obj_func: function that calculates fitness of the Net
    :type _obj_func: object
    :param _data: list of values to feed the net
    :type _data: ndarray
    :param _input_data_size: number of input values to the Net
    :type _input_data_size: int
    :param _size_1d: number of gates to create in the network
    :type _size_1d: int
    :param _num_copies: number of copies created and mutated every step of the simulation
    :type _num_copies: int
    :param _pdb_mutation: Probability of mutation (link change, operation change, output gate change)
    :type _pdb_mutation: float
    :param _annealing_param: control parameter which is a representation of cooling (simulated anealing)
    :type _annealing_param: float
    :param _annealing_scheme: parameter defines the scheme of annealing_param's reduction; one of
        ['geom', 'linear', 'log']. In 'geom' the next argument is also 'a' parameter, so it would look like ['geom', 0.9]
        if None, then Simulated Annealing is not performed and the annealing_param is constant during the simulation.
    :param _steps: number of steps of the simulation
    :type _steps: int
    :param _load_file: name of the file containing saved Net configuration
    :type _load_file: str
    :param _num_of_sim: number of CGP simulations to perform for the data gathering process
    :type _num_of_sim: int
    :return: list
    """

    gathered_data = []

    for i in range(_num_of_sim):
        cgpsa = CGPSA(_gate_func=_gate_func, _obj_func=_obj_func, _data=_data, _input_data_size=_input_data_size,
                      _size_1d=_size_1d, _num_copies=_num_copies, _pdb_mutation=_pdb_mutation,
                      _annealing_param=_annealing_param, _annealing_scheme=_annealing_scheme, _steps=_steps,
                      _load_file=_load_file)

        cgpsa.start()

        gathered_data.append({'potential': cgpsa.simulation.net.potential, 'iteration': cgpsa.simulation.i})

    return gathered_data

    # with Pool(processes=2) as pool:
    #
    #     multiprocess = [pool.apply_async(cgp_run, kwgs=(_gate_func=None, _obj_func=None, _data=None, _input_data_size=0, _size_1d=15, _num_copies=5,
    #         _pdb_mutation=0.06, _annealing_param=100, _annealing_scheme=None, _steps=10000, _load_file=_load_file, _num_of_sim=10,
    #         _gathered_data=None)) for x in range(10)]
    #     print([res.get(timeout=1) for res in multiprocess])
    #
    #     pool.join()
    #
    # print("Pool stopped - returning values...")
    #
    # return gathered_data


def cgp_run(_gate_func=None, _obj_func=None, _data=None, _input_data_size=0, _size_1d=15, _num_copies=5,
            _pdb_mutation=0.06, _annealing_param=100, _annealing_scheme=None, _steps=10000, _load_file=False,
            _num_of_sim=10, _gathered_data=None):

    cgpsa = CGPSA(_gate_func=_gate_func, _obj_func=_obj_func, _data=_data, _input_data_size=_input_data_size,
                  _size_1d=_size_1d, _num_copies=_num_copies, _pdb_mutation=_pdb_mutation,
                  _annealing_param=_annealing_param, _annealing_scheme=_annealing_scheme, _steps=_steps,
                  _load_file=_load_file)

    cgpsa.start()

    _gathered_data.append({'potential': cgpsa.simulation.net.potential, 'iteration': cgpsa.simulation.i})


def save_to_csv(_data, _filename, _new_dir=None):
    """
    Function exports data to csv file.

    :param _data: list or array - whatever Pandas DataFrame can handle.
    :type _data: list
    :param _filename: name of the exported file
    :type _filename: str
    :param _new_dir: user can create a new directory for the data by passing string
    :type _new_dir: str
    :return: None
    """
    root_path = pathlib.Path(__file__).absolute().parent

    try:
        chdir(root_path)

    except NotADirectoryError:
        raise NotADirectoryError

    if _new_dir is not None:
        try:
            mkdir(_new_dir)
            chdir(_new_dir)
            root_path = root_path / _new_dir

        except NotADirectoryError:
            print(f"Can't make {_new_dir} directory")
            raise NotADirectoryError

    try:
        # make Pandas DF and export to csv
        data_to_export = pd.DataFrame(_data)
        data_to_export.to_csv(_filename)

        print(f'Data exported to: {str(root_path) + "/" + _filename}')

    except NotADirectoryError as err:
        print(err)


def dump_data(data, path):
    """
    Method dumps simulation data to json file

    :param data: data in dictionary
    :param path: path of the file to save
    :return: None
    """

    with open(path, 'w') as file:
        json.dump(data, file)

    print("Data to viz save complete")
