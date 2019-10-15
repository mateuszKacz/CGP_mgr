###################################################
#####    Main script executing crucial        #####
#####  procedures and initializing simulation #####
#####                                         #####
###################################################

from parameters import Parameters
from net import Net2D, Net1D
from simulation import simulate


def main():
    """Main function"""

    params = Parameters(['AND', 'OR'], 15, [1, 2, 3, 4, 5], [15], 5, pdb_link_change=0.35,
                        pdb_gate_operations_change=0.2)

    net_1d = Net1D(params)
    net_1d.show_net()
    simulate(net_1d.net)


if __name__ == "__main__":
    main()
