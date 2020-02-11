import tkinter as tk


class GUI(tk.Frame):

    def __init__(self, _params, _simulation, _master=None):
        super().__init__(_master)
        self.master = _master
        self.params = _params
        self.pack()
        self.create_widgets()

        # Simulation
        self.sim_continue = True
        self.simulation = _simulation

    def create_widgets(self):

        self.start = tk.Button(self, text='Start', command=self.start).pack(side='top')

        self.stop = tk.Button(self, text='Stop', command=self.stop).pack(side='top')

        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy).pack(side='bottom')

    def stop(self):

        self.sim_continue = False

    def start(self):

        print("Start")
        self.sim_continue = True
        self.simulation.net.show_net()
        self.params.temp = 100.
        self.simulation.simulate(self.sim_continue)



