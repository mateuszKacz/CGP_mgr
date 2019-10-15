###################################################
#####    Main script executing crucial        #####
#####  procedures and initializing simulation #####
#####                                         #####
###################################################

from parameters import Parameters
from net import Net2D, Net1D


def main():
    """Main function"""

    params = Parameters(['AND', 'OR'], 15, [1, 2, 3, 4, 5], [15], 5, pdb_link_change=0.35,
                        pdb_gate_operations_change=0.2)

    net = Net1D(params)
    net.show_net()
    net.show_output()

main()
