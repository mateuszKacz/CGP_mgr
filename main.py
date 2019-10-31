###################################################
#####    Main script executing crucial        #####
#####  procedures and initializing simulation #####
#####                                         #####
###################################################

from parameters import Parameters
from net_1d import Net1D
from simulation import simulate


def main():
    """Main function"""

    params = Parameters(['AND', 'OR'], 15, [1, 0, 1, 0, 1], [1], 5, pdb_link_change=0.7,
                        pdb_gate_operations_change=0.2)

    net_1d = Net1D(params)
    net_1d.show_net()
    simulate(net_1d)


if __name__ == "__main__":
    main()
