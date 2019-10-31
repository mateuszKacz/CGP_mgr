###################################################
#####    Main script executing crucial        #####
#####  procedures and initializing simulation #####
#####                                         #####
###################################################

from parameters import Parameters
import tkinter as tk
from gui import GUI


def main():
    """Main function"""

    params = Parameters(['AND', 'OR'], 15, [1, 0, 1, 0, 1], [1], 5, pdb_link_change=0.9,
                        pdb_gate_operations_change=0.7)

    root = tk.Tk()
    gui = GUI(params, master=root)
    gui.mainloop()


if __name__ == "__main__":
    main()
