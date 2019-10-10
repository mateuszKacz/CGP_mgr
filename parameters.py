###################################################
#####    Class contains main parameteters     #####
#####        and initial values               #####
#####                                         #####
###################################################

class Parameters:
    """Class contains main initial values and parameters of the simulation"""

    def __init__(self):

        self.input = [1, 2, 3, 4, 5]
        self.output = sum(self.input)
        self.hidden_layers_width = 4
        self.hidden_layers_height = 5
        self.objective_function = 'SUM'
