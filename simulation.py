###################################################
#####        Class contains the main          #####
#####              algorythm                  #####
#####           of the simulation             #####
###################################################
import time as t



def init(net, ngates):
    """Randomly select ngates and actives them building links"""
    for i in range(ngates):

        index = net.rnd_gate()
        net.net[index].set_activate()


def simulate(net):

    for i in range(100):


        t.sleep(0.1)

        net.mutate()

        net.show_output()


