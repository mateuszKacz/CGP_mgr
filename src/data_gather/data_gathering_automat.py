#
#   Automatization of data gathering process
#
# ---------------------------------------- #

import pandas as pd
from ..cgpsa import CGPSA
import json
from ..parallel_tempering import PT
from tqdm.auto import tqdm


def gen_cgp_data(_gate_func=None, _obj_func=None, _data=None, _input_data_size=0, _size_1d=15, _num_copies=5,
                 _pdb_mutation=0.06, _annealing_param=100, _annealing_scheme=None, _steps=10000, _load_file=False,
                 _num_of_sim=10, _algorithm='SA', _pt_temps=None, _pt_switch_step=None, _pt_scheme=None,
                 _pt_num_parallel_copies=5, _show_progress=False):
    """
    Function takes CGPSA parameters with some additional variables and perform numerous simulations of CGPSA algorithm.

    :param _pt_num_parallel_copies: number of CGP copies for the PT algorithm
    :type _pt_num_parallel_copies: int
    :param _pt_scheme: if set to None then temperatures are set in place
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
    :param _algorithm: specifies if there should be Simulated Annealing performed or ParallelTempering
    :param _pt_temps: list of temperatures for PT algorithm
    :param _pt_switch_step: switch step for PT algorithm
    :param _show_progress: if True - shows Annealing Param Value and Obj Func Value every fixed amount of steps
    :return: list
    """

    gathered_data = []

    if _algorithm == 'SA':

        for i in tqdm(range(_num_of_sim), desc='Gathering data for SA'):

            print(f"Sim #: {i+1} Scheme: {_annealing_scheme} Temp: {_annealing_param}")

            cgpsa = CGPSA(_gate_func=_gate_func, _obj_func=_obj_func, _data=_data, _input_data_size=_input_data_size,
                          _size_1d=_size_1d, _num_copies=_num_copies, _pdb_mutation=_pdb_mutation,
                          _annealing_param=_annealing_param, _annealing_scheme=_annealing_scheme, _steps=_steps,
                          _load_file=_load_file)

            cgpsa.run(show_progress=_show_progress)

            gathered_data.append({'potential': cgpsa.simulation.net.potential,
                                  'iteration': cgpsa.simulation.i,
                                  'max_steps': _steps,
                                  'annealing_param': _annealing_param,
                                  'annealing_scheme': _annealing_scheme,
                                  'net_size': _size_1d,
                                  'num_copies': _num_copies,
                                  'pdb_mutation': _pdb_mutation
                                  })

    elif _algorithm == 'PT':

        for i in tqdm(range(_num_of_sim), desc='Gathering data for PT'):

            cgpsa = CGPSA(_gate_func=_gate_func, _obj_func=_obj_func, _data=_data, _input_data_size=_input_data_size,
                          _size_1d=_size_1d, _num_copies=_num_copies, _pdb_mutation=_pdb_mutation,
                          _annealing_param=_annealing_param, _annealing_scheme=_annealing_scheme, _steps=_steps,
                          _load_file=_load_file)

            pt_alg = PT(cgpsa, _temperatures=_pt_temps, _switch_step=_pt_switch_step, _scheme=_pt_scheme,
                        _num_parallel_copies=_pt_num_parallel_copies, _show_progress=False)
            pt_alg.run()

            gathered_data.append({'potential': pt_alg.best_potential,
                                  'iteration': pt_alg.best_solution_steps,
                                  'switch_ratio': pt_alg.switch_ratio,
                                  'max_steps': _steps,
                                  'switch_step': _pt_switch_step,
                                  'annealing_scheme': _annealing_scheme,
                                  'net_size': _size_1d,
                                  'num_copies': _num_copies,
                                  'pdb_mutation': _pdb_mutation,
                                  'pt_copies': pt_alg.num_parallel_copies,
                                  'pt_scheme': _pt_scheme,
                                  'init_temperatures': pt_alg.temperatures,
                                  })
    else:
        pass

    return gathered_data


def cgp_run(_gate_func=None, _obj_func=None, _data=None, _input_data_size=0, _size_1d=15, _num_copies=5,
            _pdb_mutation=0.06, _annealing_param=100, _annealing_scheme=None, _steps=10000, _load_file=False,
            _num_of_sim=10, _gathered_data=None):

    """
    Function runs one CGP algorithm simulation
    """

    cgpsa = CGPSA(_gate_func=_gate_func, _obj_func=_obj_func, _data=_data, _input_data_size=_input_data_size,
                  _size_1d=_size_1d, _num_copies=_num_copies, _pdb_mutation=_pdb_mutation,
                  _annealing_param=_annealing_param, _annealing_scheme=_annealing_scheme, _steps=_steps,
                  _load_file=_load_file)

    cgpsa.run()

    _gathered_data.append({'potential': cgpsa.simulation.net.potential, 'iteration': cgpsa.simulation.i})


def save_to_csv(_data, _filepath, _new_dir=None):
    """
    Function exports data to csv file.

    :param _data: list or array - whatever Pandas DataFrame can handle.
    :type _data: list
    :param _filepath: name of the exported file
    :type _filepath: str
    :param _new_dir: user can create a new directory for the data by passing string
    :type _new_dir: str
    :return: None
    """

    try:
        # make Pandas DF and export to csv
        data_to_export = pd.DataFrame(_data)
        data_to_export.to_csv(_filepath)

        print(f'Data exported to: {_filepath}')

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
