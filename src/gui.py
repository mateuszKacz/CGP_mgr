#
#   GUI generator script
#   creates components and widgets
# ---------------------------------------- #

from tkinter import Frame, Button, Label, Entry, END
from tkinter.filedialog import askopenfilename
from src.simulation import Simulation
from src.parameters import Parameters


class GUI(Frame):

    def __init__(self, _master=None):
        super().__init__(_master)
        self.master = _master
        self.master.title("CGP")

        # Simulation
        self.sim_continue = True

        # Input paths
        self.user_input_paths = {'data_file': '', 'gate_func': '', 'gate_func_names': '', 'obj_func': ''}

        # default parameters values
        self.default_param_val = {'param_input_data_size': 5,
                                  'param_net_size': 15,
                                  'param_num_copies': 4,
                                  'param_pdb_link_change': 0.1,
                                  'param_pdb_gate_operation_change': 0.1,
                                  'param_pdb_output_change': 0.1,
                                  'param_beta_const': 100
                                  }

        self.create_widgets()

    def create_widgets(self):

        self.master.maxsize(width=800, height=600)
        
        # make GUI

        #main frame
        self.main_frame = Frame(self.master, height=800, width=1280)
        self.main_frame.pack_propagate(0)
        self.main_frame.grid()

        self.left_frame = Frame(self.main_frame, relief='groove', bd=3)
        self.center_frame = Frame(self.main_frame, relief='groove', bd=3)
        self.right_frame = Frame(self.main_frame, relief='groove', bd=3)
        self.control_frame = Frame(self.main_frame, relief='groove', bd=3)

        self.left_frame.grid(row=0, column=0, pady=10, padx=5, sticky='nswe')
        self.center_frame.grid(row=0, column=1, pady=10, padx=5, sticky='nswe')
        self.right_frame.grid(row=0, column=2, pady=10, padx=5, sticky='nswe')
        self.control_frame.grid(row=0, column=3, pady=10, padx=5, sticky='nswe')

        # Buttons

        # Left Frame
        self.button_choose_data_path = Button(self.left_frame, text='Choose Data File', relief='groove',
                                                   command=self.choose_data_file)
        self.button_choose_data_path.grid(row=0, column=0, pady=10, padx=5, sticky='nswe')

        self.button_choose_gate_func_path = Button(self.left_frame, text='Choose Gate Functions', relief='groove',
                                                    command=self.choose_gate_func_file)
        self.button_choose_gate_func_path.grid(row=1, column=0, pady=10, padx=5, sticky='nswe')

        self.button_choose_obj_func_path = Button(self.left_frame, text='Choose Obj Function', relief='groove',
                                                   command=self.choose_obj_func)
        self.button_choose_obj_func_path.grid(row=3, column=0, pady=10, padx=5, sticky='nswe')

        # Control Frame
        self.start = Button(self.control_frame, text='Start', command=self.start).grid(row=0, column=0, pady=10, padx=5, sticky='nswe')

        self.stop = Button(self.control_frame, text='Stop', command=self.stop).grid(row=1, column=0, pady=10, padx=5, sticky='nswe')

        self.reset = Button(self.control_frame, text='Reset', command=self.reset).grid(row=2, column=0, pady=10, padx=5,
                                                                                    sticky='nswe')

        self.quit = Button(self.control_frame, text="QUIT", fg="red", command=self.master.destroy).grid(row=3, column=0, pady=10, padx=5, sticky='nswe')

        # Labels

        # Center Frame
        self.label_choose_data = Label(self.center_frame, text='~/')
        self.label_choose_data.grid(row=0, column=0, pady=10, padx=5, sticky='nswe')

        self.label_choose_gate_func = Label(self.center_frame, text='~/')
        self.label_choose_gate_func.grid(row=1, column=0, pady=10, padx=5, sticky='nswe')

        self.label_choose_obj_func = Label(self.center_frame, text='~/')
        self.label_choose_obj_func.grid(row=3, column=0, pady=10, padx=5, sticky='nswe')

        # Right Frame
        self.label_param_input_data_size = Label(self.right_frame, text='Input Data Size:').grid(row=0, column=0, pady=10, padx=5, sticky='nswe')
        self.label_param_net_size = Label(self.right_frame, text='Net Size:').grid(row=1, column=0, pady=10, padx=5, sticky='nswe')
        self.label_param_num_copies = Label(self.right_frame, text='Number Of Copies:').grid(row=2, column=0, pady=10, padx=5, sticky='nswe')
        self.label_param_pdb_link_change = Label(self.right_frame, text='Link change pdb:').grid(row=3, column=0, pady=10, padx=5, sticky='nswe')
        self.label_param_pdb_gate_operation_change = Label(self.right_frame, text='Gate operation change pdb:').grid(row=4, column=0, pady=10, padx=5, sticky='nswe')
        self.label_param_pdb_output_change = Label(self.right_frame, text='Net Output Gate change pdb:').grid(row=5, column=0, pady=10, padx=5, sticky='nswe')
        self.label_param_beta_const = Label(self.right_frame, text='Anealing param(beta):').grid(row=6, column=0, pady=10, padx=5, sticky='nswe')

        # Param Entry

        # Right Frame
        self.entry_param_input_data_size = Entry(self.right_frame)
        self.entry_param_net_size = Entry(self.right_frame)
        self.entry_param_num_copies = Entry(self.right_frame)
        self.entry_param_pdb_link_change = Entry(self.right_frame)
        self.entry_param_pdb_gate_operation_change = Entry(self.right_frame)
        self.entry_param_pdb_output_change = Entry(self.right_frame)
        self.entry_param_beta_const = Entry(self.right_frame)
        # packing
        self.entry_param_input_data_size.grid(row=0, column=1, pady=10, padx=5, sticky='nswe')
        self.entry_param_net_size.grid(row=1, column=1, pady=10, padx=5, sticky='nswe')
        self.entry_param_num_copies.grid(row=2, column=1, pady=10, padx=5, sticky='nswe')
        self.entry_param_pdb_link_change.grid(row=3, column=1, pady=10, padx=5, sticky='nswe')
        self.entry_param_pdb_gate_operation_change.grid(row=4, column=1, pady=10, padx=5, sticky='nswe')
        self.entry_param_pdb_output_change.grid(row=5, column=1, pady=10, padx=5, sticky='nswe')
        self.entry_param_beta_const.grid(row=6, column=1, pady=10, padx=5, sticky='nswe')
        # default variables
        self.entry_param_input_data_size.insert(END, self.default_param_val['param_input_data_size'])
        self.entry_param_net_size.insert(END, self.default_param_val['param_net_size'])
        self.entry_param_num_copies.insert(END, self.default_param_val['param_num_copies'])
        self.entry_param_pdb_link_change.insert(END, self.default_param_val['param_pdb_link_change'])
        self.entry_param_pdb_gate_operation_change.insert(END, self.default_param_val['param_pdb_gate_operation_change'])
        self.entry_param_pdb_output_change.insert(END, self.default_param_val['param_pdb_output_change'])
        self.entry_param_beta_const.insert(END, self.default_param_val['param_beta_const'])

    # Buttons' on-click functions
    def stop(self):
        """Stops the simulation"""
        self.sim_continue = False

    def start(self):
        """Starts the simulation"""
        print("Initiating components...")
        # Creating simulation objects

        params = Parameters(_paths=self.user_input_paths,
                            _input_data_size=int(self.entry_param_input_data_size.get()),
                            _size_1d=int(self.entry_param_net_size.get()),
                            _num_copies=int(self.entry_param_num_copies.get()),
                            _pdb_link_change=float(self.entry_param_pdb_link_change.get()),
                            _pdb_gate_operation_change=float(self.entry_param_pdb_gate_operation_change.get()),
                            _pdb_output_change=float(self.entry_param_pdb_output_change.get()),
                            _beta_const=float(self.entry_param_beta_const.get()))
        print("Simulation object...")
        simulation = Simulation(params)

        # Printing initial Net
        print("Initial Network\n")
        simulation.net.show_net()

        # Starting simulation
        print("Start")
        self.sim_continue = True

        # Setting Anealing initial parameter
        params.beta_const = 100.

        # starting main simulation loop
        simulation.simulate(self.sim_continue)

    def reset(self):
        """Resets chosen paths to default _value"""

        for key in self.user_input_paths:
            self.user_input_paths[key] = ''

        self.label_choose_obj_func.config(text='~/')
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

    def choose_obj_func(self):
        """Function runs when button is pressed"""

        filename = askopenfilename()
        self.user_input_paths['obj_func'] = filename

        if filename != '':
            self.label_choose_obj_func.config(text=filename)
