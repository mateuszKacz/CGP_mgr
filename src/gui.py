#
#   GUI generator script
#   creates components and widgets
# ---------------------------------------- #

from tkinter import Frame, Button, Label
from tkinter.filedialog import askopenfilename
from src.simulation import Simulation
from src.parameters import Parameters

# TODO: Add rest of parameters to set


class GUI(Frame):

    def __init__(self, _master=None):
        super().__init__(_master)
        self.master = _master
        self.master.title("CGP")
        self.create_widgets()

        # Simulation
        self.sim_continue = True

        # Input paths
        self.user_input_paths = {'data_file': '', 'gate_func': '', 'gate_func_names': '', 'obj_func': ''}

    def create_widgets(self):

        self.master.maxsize(width=800, height=600)
        
        # make GUI

        #main frame
        self.main_frame = Frame(self.master, height=800, width=1280)
        self.main_frame.pack_propagate(0)
        self.main_frame.grid()


        self.left_frame = Frame(self.main_frame, relief='groove', bd=3)
        self.right_frame = Frame(self.main_frame, relief='groove', bd=3)
        self.control_frame = Frame(self.main_frame, relief='groove', bd=3)

        self.left_frame.grid(row=0, column=0, pady=10, padx=5, sticky='nswe')
        self.right_frame.grid(row=0, column=1, pady=10, padx=5, sticky='nswe')
        self.control_frame.grid(row=0, column=2, pady=10, padx=5, sticky='nswe')

        # Buttons

        self.button_choose_data_path = Button(self.left_frame, text='Choose Data File', relief='groove',
                                                   command=self.choose_data_file)
        self.button_choose_data_path.grid(row=0, column=0, pady=10, padx=5, sticky='nswe')

        self.button_choose_gate_func_path = Button(self.left_frame, text='Choose Gate Functions', relief='groove',
                                        command=self.choose_gate_func_file)
        self.button_choose_gate_func_path.grid(row=1, column=0, pady=10, padx=5, sticky='nswe')

        self.button_choose_gate_func_names_path = Button(self.left_frame, text='Choose Gate Func Names', relief='groove',
                                                   command=self.choose_gate_func_names)
        self.button_choose_gate_func_names_path.grid(row=2, column=0, pady=10, padx=5, sticky='nswe')

        self.button_choose_obj_func_path = Button(self.left_frame, text='Choose Obj Function', relief='groove',
                                                   command=self.choose_obj_func)
        self.button_choose_obj_func_path.grid(row=3, column=0, pady=10, padx=5, sticky='nswe')

        self.start = Button(self.control_frame, text='Start', command=self.start).grid(row=0, column=0, pady=10, padx=5, sticky='nswe')

        self.stop = Button(self.control_frame, text='Stop', command=self.stop).grid(row=1, column=0, pady=10, padx=5, sticky='nswe')

        self.reset = Button(self.control_frame, text='Reset', command=self.reset).grid(row=2, column=0, pady=10, padx=5,
                                                                                    sticky='nswe')

        self.quit = Button(self.control_frame, text="QUIT", fg="red", command=self.master.destroy).grid(row=3, column=0, pady=10, padx=5, sticky='nswe')

        # Labels

        self.label_choose_data = Label(self.right_frame, text='~/')
        self.label_choose_data.grid(row=0, column=0, pady=10, padx=5, sticky='nswe')

        self.label_choose_gate_func = Label(self.right_frame, text='~/')
        self.label_choose_gate_func.grid(row=1, column=0, pady=10, padx=5, sticky='nswe')

        self.label_choose_gate_func_names = Label(self.right_frame, text='~/')
        self.label_choose_gate_func_names.grid(row=2, column=0, pady=10, padx=5, sticky='nswe')

        self.label_choose_obj_func = Label(self.right_frame, text='~/')
        self.label_choose_obj_func.grid(row=3, column=0, pady=10, padx=5, sticky='nswe')

    # Buttons' on-click functions
    def stop(self):
        """Stops the simulation"""
        self.sim_continue = False

    def start(self):
        """Starts the simulation"""
        print("Initiating components...")
        # Creating simulation objects

        params = Parameters(_paths=self.user_input_paths, _input_data_size=5, _size_1d=25, _num_copies=4,
                            _pdb_link_change=0.1, _pdb_gate_operation_change=0.1, _pdb_output_change=0.1, _beta_const=100)
        print("simulation object...")
        simulation = Simulation(params)

        # Printing initial Net
        print("Initial Network\n")
        simulation.net.show_net()

        # Starting simulation
        print("Start")
        self.sim_continue = True
        # Printing initial Net
        simulation.net.show_net()

        # Setting Anealing initial parameter
        params.beta_const = 100.

        # starting main simulation loop
        simulation.simulate(self.sim_continue)

    def reset(self):
        """Resets chosen paths to default _value"""

        for key in self.user_input_paths:
            self.user_input_paths[key] = ''

        self.label_choose_obj_func.config(text='~/')
        self.label_choose_gate_func_names.config(text='~/')
        self.label_choose_data.config(text='~/')
        self.label_choose_gate_func.config(text='~/')

    def choose_data_file(self):
        """Function runs when button is pressed"""

        filename = askopenfilename()
        self.user_input_paths['gate_func'] = filename

        if filename != '':
            self.label_choose_data.config(text=filename)

    def choose_gate_func_file(self):
        """Function runs when button is pressed"""

        filename = askopenfilename()
        self.user_input_paths['gate_func'] = filename

        if filename != '':
            self.label_choose_gate_func.config(text=filename)

    def choose_gate_func_names(self):
        """Function runs when button is pressed"""

        filename = askopenfilename()
        self.user_input_paths['gate_func_names'] = filename

        if filename != '':
            self.label_choose_gate_func_names.config(text=filename)

    def choose_obj_func(self):
        """Function runs when button is pressed"""

        filename = askopenfilename()
        self.user_input_paths['obj_func'] = filename

        if filename != '':
            self.label_choose_obj_func.config(text=filename)
