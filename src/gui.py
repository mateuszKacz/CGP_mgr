#
#   GUI generator script
#   creates components and widgets
# ---------------------------------------- #

from tkinter import Frame, Button, LEFT, RIGHT, TOP, ACTIVE, NORMAL
from tkinter.filedialog import askopenfilename


class GUI(Frame):

    def __init__(self, _params, _simulation, _master=None):
        super().__init__(_master)
        self.master = _master
        self.params = _params
        self.pack()
        self.create_widgets()

        # Simulation
        self.sim_continue = True
        self.simulation = _simulation

        # Input paths
        self.paths = []

    def create_widgets(self):

        self.master.geometry('500x400')

        # TODO: add all PATHS buttons and manage GUI
        
        # make GUI
        self.main_frame = Frame(self.master, height=400, width=500)
        self.main_frame.pack_propagate(0)
        self.main_frame.pack()
        self.left_frame = Frame(self.main_frame, relief='groove', bd=3, height=400, width=100)
        self.right_frame = Frame(self.main_frame, relief='groove', bd=3, height=400, width=500)
        self.right_top_frame = Frame(self.right_frame, relief='groove', bd=1, height=200, width=350)
        self.right_bottom_frame = Frame(self.right_frame, relief='groove', bd=1, height=200, width=350)
        self.left_frame.pack(anchor='n', side=LEFT, fill='x')
        self.right_frame.pack(anchor='n', side=RIGHT)
        self.right_top_frame.pack()
        self.right_bottom_frame.pack()
        self.button_choose_gate_func_path = Button(self.left_frame, text='Add Device', relief='groove',
                                        command=self.choose_file)
        self.button_choose_gate_func_path.pack(side=TOP, expand=True, fill='x')

        self.start = Button(self, text='Start', command=self.start).pack(side='top')

        self.stop = Button(self, text='Stop', command=self.stop).pack(side='top')

        self.quit = Button(self, text="QUIT", fg="red", command=self.master.destroy).pack(side='bottom')

    def stop(self):

        self.sim_continue = False

    def start(self):

        print("Start")
        self.sim_continue = True
        self.simulation.net.show_net()
        self.params.temp = 100.

        # starting main simulation loop
        self.simulation.simulate(self.sim_continue)

    def choose_file(self):
        # TODO: Do this function for all PATHS buttons
        self.button_choose_gate_func_path.config(relief='sunken', state=ACTIVE)
        self.button_choose_gate_func_path.after(200, lambda: self.button_choose_gate_func_path.config(relief='groove', state=NORMAL))
        filename = askopenfilename()
        self.paths.append(filename)
        print(filename)





