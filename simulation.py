###################################################
#####        Class contains the main          #####
#####              algorythm                  #####
#####           of the simulation             #####
###################################################
import time as t
import random as rnd


def init(net, ngates):
    """Randomly select ngates and actives them building links"""
    for i in range(ngates):

        index = net.rnd_gate()
        net.net[index].set_activate()


def simulate(net):

    for i in range(1000):

        t.sleep(0.1)

        if net.params.pdb_gate_operations_change >= rnd.uniform(0, 1.):

            net.change_operation(net.rnd_gate())

        if net.params.pdb_link_change >= rnd.uniform(0, 1.):

            net.change_input(net.rnd_gate(), rnd.randint(0, 1))

        net.show_output()



