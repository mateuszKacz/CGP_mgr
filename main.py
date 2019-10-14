###################################################
#####    Main script executing crucial        #####
#####  procedures and initializing simulation #####
#####                                         #####
###################################################

from parameters import Parameters
from net import Net2D


def main():
    """Main function"""

    params = Parameters()

    net = Net2D(params)
    net.setup()
    net.show_net()
    net.result()
    net.show_links(2, 1)

main()
