from tkinter import *
from tkinter import ttk 
import threading

from pox.core import core 

class UI:
    def __init__(self):
        self.root = Tk()
        self.root.title("firewall thing") 

        self.frame = ttk.Frame(self.root, padding="3") 
        self.frame.grid()

        self.conn = core.openflow.getConnection(1)

        self.disp = ttk.Label(self.frame, text="hmm").grid(column=0, row=0)
        ttk.Button(self.frame, text="quit", command=self.root.destroy).grid(column=0, row=1)


    def _handle_ConnectionUp(self, event):
        self.conn = core.openflow.getConnection(1)
        self.disp.configure(str(dir(self.conn)))

        self.root.mainloop()

        # fuck threading
        #ui_thread = threading.thread(target=self.root.mainloop, args=[])
        #ui_thread.start()
