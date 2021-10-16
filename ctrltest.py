from pox.core import core 
import pox.openflow.libopenflow_01 as of
from forwarding.l2_learning import * 

from tkinter import *

from project.firewall import TestFW
from project.ui import UI

def setup():
    top = Toplevel()

    # quit POX when window is killed
    top.protocol("WM_DELETE_WINDOW", core.quit) 

    top.title("firewall thing") 

    frame = Frame(top, padding="3") 
    frame.grid()

    disp = Label(frame, text="hmm").grid(column=0, row=0)
    
    def reload():
        conn = core.openflow.getConnection(1)
        disp.configure(str(dir(conn)))

    b_reload = Button(frame, text="reload", command=reload).grid(column=0, row=1)
    b_quit = Button(frame, text="quit", command=top.destroy).grid(column=0, row=2)


def launch():
    fw_list_dpid = [51, 52] 
    srv_list = {"web" : ['10.0.0.100']}

    # register firewall 
    core.registerNew(TestFW, fw_list_dpid[0], srv_list)

    # just use L2 learning switch for others 
    core.registerNew(l2_learning, False) 

    #core.registerNew(UI)


    def start_ui():
        core.tk.do(setup)
        
    core.call_when_ready(start_ui, ['openflow', 'tk'])
