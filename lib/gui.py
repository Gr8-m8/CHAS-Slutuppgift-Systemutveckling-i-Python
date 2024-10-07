import tkinter as tk
import time
#from ..main import *

class GUI:
    def __init__(self, title, elements, func) -> None:
        self.func = func
        self.screen = tk.Tk(className=title)
        for element in elements:
            element.master = self.screen
            element.pack()

    NAME = "Monitor"


def Gui_Clear(gui):
    for widget in gui.winfo_children():
        widget.destroy()

def Gui_Exit(gui):
    gui.destroy()

def Gui_MonitorStart(gui, monitor, logger = None):
    status = ""
    if not monitor.monitor:
        monitor.monitor_start()
        status = "Monitor is ON"
    else:
        status = "Failed. Monitor is already ON"

    Gui_Clear(gui)

    textStatus = tk.Label(gui, text=status)
    button_Back = tk.Button(gui, text="Back",command=lambda:Gui_Main(gui, monitor, logger),width=20, height=1)

    textStatus.pack()
    button_Back.pack()

def Gui_MonitorList(gui, monitor = None, logger = None):
    cpu, ram, disk = monitor.monitor_snapshot_list()

    Gui_Clear(gui) 

    textStatus = tk.Label(gui, text=f"Failed. Monitor is not ON")
    cpuStatus = tk.Label(gui, text=f"cpu: {cpu}%") if cpu else None
    ramStatus = tk.Label(gui, text=f"ram: {ram.percent if ram else None}%") if ram else None
    diskStatus = tk.Label(gui, text=f"disk: {disk.percent if disk else None}%") if disk else None
    button_Back = tk.Button(gui, text="Back",command=lambda:Gui_Main(gui, monitor, logger),width=20, height=1)

    if monitor.monitor:
        cpuStatus.pack() if cpu else None
        ramStatus.pack() if ram else None
        diskStatus.pack() if disk else None
    else:
        textStatus.pack()
    button_Back.pack()

def Gui_MonitorDisplay(gui, monitor = None, logger = None):
    cpu, ram, disk = monitor.monitor_snapshot_list()
    cpua, rama, diska = monitor.monitor_snapshot_alarm_list()
    timeE = 0

    Gui_Clear(gui) 

    textStatus = tk.Label(gui, text=f"Failed. Monitor is not ON")
    button_Back = tk.Button(gui, text="Back",command=lambda:Gui_Main(gui, monitor, logger),width=20, height=1)
    
    timeElapsed = tk.Label(gui, text=f"Time Elapsed: {timeE}s")
    
    cpuStatus = tk.Label(gui, text=f"cpu: {cpu}%") if cpu else None
    ramStatus = tk.Label(gui, text=f"ram: {ram.percent if ram else None}%") if ram else None
    diskStatus = tk.Label(gui, text=f"disk: {disk.percent if disk else None}%") if disk else None
    
    cpuaStatus = tk.Label(gui, text=f"cpua: {cpua}") if cpua and cpua[1]>0 else None
    ramaStatus = tk.Label(gui, text=f"rama: {rama}") if rama and rama[1]>0 else None
    diskaStatus = tk.Label(gui, text=f"diska: {diska}") if diska and diska[1]>0 else None
    
    

    
    if monitor.monitor:
        timeElapsed.pack()
        cpuStatus.pack() if cpu else None
        ramStatus.pack() if ram else None
        diskStatus.pack() if disk else None
        cpuaStatus.pack() if cpua and cpua[1]>0 else None
        ramaStatus.pack() if rama and rama[1]>0 else None
        diskaStatus.pack() if diska and diska[1]>0 else None
    else:
        textStatus.pack()
    button_Back.pack()

    if monitor.monitor:
        while True:
                timeE=timeE+1
                cpu, ram, disk = monitor.monitor_snapshot_list()
                cpua, rama, diska = monitor.monitor_snapshot_alarm_list()
                gui.update()
                time.sleep(1)
    

    


def Gui_AlarmList(gui, monitor = None, logger = None):
    Gui_Clear(gui)
    
    cpu, ram, disk = monitor.alarms

    cpu = tk.Label(gui, text=f"CPU Alarms:\n{monitor.alarms[cpu] if monitor.alarms[cpu] or len(monitor.alarms[cpu])>0 else None}")
    ram = tk.Label(gui, text=f"RAM Alarms:\n{monitor.alarms[ram] if monitor.alarms[ram] or len(monitor.alarms[ram])>0 else None}")
    disk = tk.Label(gui, text=f"Disk Alarms:\n{monitor.alarms[disk] if monitor.alarms[disk] or len(monitor.alarms[disk])>0 else None}")
    button_Back = tk.Button(gui, text="Back",command=lambda:Gui_Main(gui, monitor, logger),width=20, height=1)

    cpu.pack()
    ram.pack()
    disk.pack()
    button_Back.pack()

def Gui_AlarmSet(gui, monitor = None, logger = None):
    Gui_Clear(gui)

    alarmtext = ""

    textStatus = tk.Label(gui, text="Enter value 0-100")
    textinput = tk.Entry(gui, textvariable=alarmtext)
    textSubmit = tk.Button(gui, command=lambda: monitor.alarm_add())
    button_Back = tk.Button(gui, text="Back",command=lambda:Gui_Main(gui, monitor, logger),width=20, height=1)

    textStatus.pack()
    textinput.pack()
    button_Back.pack()

def Gui_AlarmRemove(gui, monitor = None, logger = None):
    Gui_Clear(gui) 

    textStatus = tk.Label(gui, text="status")
    button_Back = tk.Button(gui, text="Back",command=lambda:Gui_Main(gui, monitor, logger),width=20, height=1)

    textStatus.pack()
    button_Back.pack()

def Gui_Main(gui, monitor = None, logger = None):
    Gui_Clear(gui)

    buttonwidth = 20
    buttonheight = 1
    button_Exit = tk.Button(gui, text="Exit",command=lambda:Gui_Exit(gui),width=20, height=1)
    button_MonitorStart = tk.Button(gui, text="Start Monitor",command=lambda:Gui_MonitorStart(gui, monitor=monitor),width=buttonwidth, height=buttonheight)
    button_MonitorList = tk.Button(gui, text="Monitor List",command=lambda:Gui_MonitorList(gui,monitor=monitor),width=buttonwidth, height=buttonheight)
    button_AlarmSet = tk.Button(gui, text="Set Alarm",command=lambda:Gui_AlarmSet(gui,monitor=monitor),width=buttonwidth, height=buttonheight)
    button_AlarmList = tk.Button(gui, text="List Alarm",command=lambda:Gui_AlarmList(gui,monitor=monitor),width=buttonwidth, height=buttonheight)
    button_MonitorDisplay = tk.Button(gui, text="Monitor Display",command=lambda:Gui_MonitorDisplay(gui,monitor=monitor),width=buttonwidth, height=buttonheight)
    button_AlarmRemove = tk.Button(gui, text="Remove Alarm",command=lambda:Gui_AlarmRemove(gui, monitor=monitor),width=buttonwidth, height=buttonheight)

    button_MonitorStart.pack(pady=12)
    button_MonitorList.pack(pady=12)
    button_MonitorDisplay.pack(pady=12)
    button_AlarmList.pack(pady=12)
    button_AlarmSet.pack(pady=12)
    button_AlarmRemove.pack(pady=12)
    button_Exit.pack(pady=12)

def Gui(main, monitor, logger):
    name = "Monitor"
    gui = tk.Tk(className=name)
    gui.titlename = name
    gui.geometry(f'{16*40*2}x{9*40*2}')
    
    Gui_Main(gui, monitor)

    gui.mainloop()