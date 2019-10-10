###################################################
#####    Main script executing crucial        #####
#####  procedures and initializing simulation #####
#####                                         #####
###################################################

from parameters import Parameters
from net import Net


def main():
    """Main function"""

    params = Parameters()

    net = Net(params)
    net.activate(1, 1)
    net.activate(3, 1)
    net.setup()
    net.show_net()
    net.result()


main()
