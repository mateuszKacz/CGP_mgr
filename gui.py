import tkinter as tk
from simulation import simulate
from net_1d import Net1D


class GUI(tk.Frame):

    def __init__(self, params, master=None):
        super().__init__(master)
        self.master = master
        self.params = params
        self.pack()
        self.create_widgets()

    def create_widgets(self):

        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.start
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def start(self):

        print("Start")
        net_1d = Net1D(self.params)
        net_1d.show_net()
        simulate(net_1d)


