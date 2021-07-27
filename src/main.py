#
#   Main script executing crucial
#   procedures and initializing simulation
# ---------------------------------------- #

from numpy import genfromtxt

from src.cgpsa import CGPSA
from src.user_inputs import gate_functions as gate_func, objective_function as obj_func


def main():
    """Main function"""
    gate_fun = [
        gate_func.bin_and,
        gate_func.bin_nand,
        gate_func.bin_or,
        gate_func.bin_xor,
    ]

    data_even_check_gate = genfromtxt(
        "user_inputs/input_even_check_gate.txt", delimiter=","
    )

    cgpsa = CGPSA(
        _gate_func=gate_fun,
        _obj_func=obj_func.obj_func,
        _data=data_even_check_gate,
        _input_data_size=5,
        _steps=1000,
        _load_file="data_gather/test_data/cgp_test.txt",
    )

    cgpsa.show_net()


if __name__ == "__main__":
    main()
