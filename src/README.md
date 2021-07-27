# *data_gather*

Here are all the files connected to gathering the data form the simulations.

* *cgp* - contains `.csv` files with data from the classic *CGP* simulations
* *cgpsa - contains `.csv` files with data from the *Simulated Annealing* simulations
* *pt* - contains `.csv` files with data from the *Parallel Tempering* simulations
* *test_data* - test files with the exported data from the simulations
* `data_gathering_automat.py` - script contains functions that automize the procedure of
 gathering data from bunch of simulations.

# *data_gen*

Contains scripts that generate input data for different experiments:
* random gate
* AND gate
* evencheck gate

# *experiments*

Contains all the scripts that were used to gather data from the simulations, optimize
parameters and check various parameters' configurations.

# *user_inputs*

This directory contains all the necessary files to perform a simulation:
* `gate_functions.py` - all the available functions that can be applied to gates are
defined here. Algorithm takes all those and randomly initializes the gates with them.
* `objective_function.py` - evaluation function for the model. Based on that algorithm
measures the success/fitness of the current model's mutation.
* input_*.txt - one of those text files is necessary to perform a simulation, depending
on the need. Here there are couple of them, generated with scripts from `data_gen`
directory.

# *utils*

Helping functions like saving to the `.csv` or JSON files.

# *visualize_network*

Module is used to generate visual representation of the network. An example could be
reached in `solutions.Graphics` folder.

# `cgpsa.py`

Main script that introduces Cartesian Genetic Programming with a possibility to turn on
the Simulated Annealing algorithm, by replacing the `_annealing_scheme` parameter e.g.:
 ```
 None -> ['geom', 0.99]
 ```

To explore all the possible variants check the parameter description, together with
`Parameters` class definition located in `parameters.py`

# `main.py`

An example of CGP with SA run with *evencheck* gate as input.

# `net_1d.py`

Introduced architecture of the CGP network. Net1D class consist of numerous of `Gate`
objects, that split into input gates and the rest. One of those gates at a time is the
**Output** gate - from it's output fitness of the whole network is evaluated.

# `parallel_tempering.py`

Based on previous components *PT* algorithm is implemented here. There are couple of
possible approaches:
* passing one temperature value - therefore the system recognizes it as a starting
temperature, the rest of the values are calculated following the optimal pattern.
* passing a list of values - temperatures of all the copies of the system are defined by
 *User* explicitly.

 There are also two schemes available:
 * *gaussian* - temperature of the system evolves during the simulation following the
 gaussian distribution. Therefore, *User* has to pass the *mean* and *variance* to the
 algorithm.
 * *discrete*/*None* - temperatures are fixed in places. **recommended**

# `parameters.py`

Contains `Parameters` class definition, that holds all the main parameters of the
simulation.

Based on the `scheme` the list of the `annealing_parameter`/`temperature` values are
calculated here.

# `simulation.py`

This component is designed to facilitate mutation, evolution and the whole simulation
procedure of the `CGPSA` component. It contains the simulation`end-conditions`.
