###################################################
#####    Main script executing crucial        #####
#####  procedures and initializing simulation #####
#####                                         #####
###################################################

from parameters import Parameters
from net import Net2D, Net1D


def main():
    """Main function"""

    params = Parameters()

    net = Net1D(params, operations_types = ['AND', 'OR'])



main()
