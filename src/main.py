#
#   Main script executing crucial
#   procedures and initializing simulation
# ---------------------------------------- #

import random as rnd
import tkinter as tk

from src.gui import GUI
from src.parameters import Parameters
from src.simulation import Simulation


def main():
    """Main function"""

    # GUI creation
    root = tk.Tk()
    gui = GUI(_master=root)
    gui.mainloop()


if __name__ == "__main__":
    main()
