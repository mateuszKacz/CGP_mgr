#
#   Class carries data upload
#
# ---------------------------------------- #
from numpy import genfromtxt


class Input:
    """Class handles data upload from file """
    def __init__(self, _path_input_data, _path_gate_func, _path_gate_func_names, _path_obj_func):

        self.data = genfromtxt(_path_input_data, delimeter=',')
        self.func_names = genfromtxt(_path_gate_func_names, delimiter='\n')
        self.path_gate_func = _path_gate_func
        self.path_obj_func = _path_obj_func
