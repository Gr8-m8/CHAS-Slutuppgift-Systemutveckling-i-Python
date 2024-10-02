import tkinter as tk
#from ..main import *

def func_Exit(gui):
    gui.destroy()

def func_MonitorStart(monitor):
    if monitor.monitor:
        monitor.start()

def func_MonitorList(monitor):
    pass

def func_MonitorDisplay(monitor):
    pass

def func_AlarmList(monitor):
    pass

def func_AlarmSet(monitor):
    pass

def func_AlarmRemove(monitor):
    pass



def Gui(main, monitor, logger):
    gui = tk.Tk(screenName="screenName",baseName="baseName",className="Monitor")
    gui.title("Monitor")
    gui.geometry(f'{16*40*2}x{9*40*2}')

    button_Exit = tk.Button(gui, text="Exit",command=lambda:func_Exit(gui))
    button_MonitorStart = tk.Button(gui, text="Start Monitor",command=lambda:func_MonitorStart(monitor=monitor))
    button_MonitorList = tk.Button(gui, text="Monitor List",command=lambda:func_MonitorList(monitor=monitor))
    button_AlarmSet = tk.Button(gui, text="Set Alarm",command=lambda:func_AlarmSet(monitor=monitor))
    button_AlarmList = tk.Button(gui, text="List Alarm",command=lambda:func_AlarmList(monitor=monitor))
    button_MonitorDisplay = tk.Button(gui, text="Monitor Display",command=lambda:func_MonitorDisplay(monitor=monitor))
    button_AlarmRemove = tk.Button(gui, text="Remove Alarm",command=lambda:func_AlarmRemove(monitor=monitor))

    button_MonitorStart.grid(row=1, column=1)
    button_MonitorList.grid(row=2, column=1)
    button_MonitorDisplay.grid(row=3, column=1)
    button_AlarmList.grid(row=4, column=1)
    button_AlarmSet.grid(row=5, column=1)
    button_AlarmRemove.grid(row=6, column=1)
    button_Exit.grid(row=8, column=1)

    gui.mainloop()