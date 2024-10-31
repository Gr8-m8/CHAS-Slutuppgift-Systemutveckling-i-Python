import time
import os
import datetime
import json
import psutil
import math

from textefficiency import text
from logger import Logger
from psmonitor import Monitor
from menu import Menu, MenuOption, MenuInput, MenuNonBlocking

class Main():
    def __init__(self):
        self.logger = Logger()
        self.monitor = Monitor()

        self.menuMain:Menu = Menu("Select Option", logger=self.logger)
        self.menuMain.options = [
            MenuOption("Exit", lambda: self.menuMain.Drop()),
            MenuOption("Start Monitor", lambda: self.menuSet(self.menuStartMonitor)) ,
            MenuOption("Monitor Snapshot", lambda: self.menuSet(self.menuMonitorSnapshot)),
            MenuOption("Set Alarm", lambda: self.menuSet(self.menuAlarmSet)),
            MenuOption("List Alarm", lambda: self.menuSet(self.menuAlarmList)),
            MenuOption("Monitor Stream", lambda: self.menuSet(self.menuMonitorStream)),
            MenuOption("Remove Alarm", lambda: self.menuSet(self.menuAlarmRemove)),
            
        ]
        
        def MonitorStart():
            self.logger.appendlog(content="Start Monitor")
            if not self.monitor.monitor: 
                self.logger.appendlog(content="Monitor Is On")
                self.monitor.monitor_start()
                return "Monitor Is ON"
            else:
                self.logger.appendlog(content="Monitor Is Already On")
                return "Monitor Is Already ON"
        self.menuStartMonitor:Menu = Menu("Start Monitor", lambda: MonitorStart(), logger=self.logger)
        self.menuStartMonitor.options = [
            MenuOption("Confirm", lambda: self.menuStartMonitor.Drop()),
        ]

        def MonitorSnapshot():
            self.logger.appendlog(content="Monitor Snapshot")
            if not self.monitor.monitor:
                self.logger.appendlog(content="Monitor Is Not ON")
                return "Monitor Is Not ON"
            
            cpu, ram, disk = self.monitor.monitor_snapshot_list()

            self.logger.appendlog(content=f"CPU at {cpu}% & RAM at {ram}% & Disk at {disk}%")
            return f"CPU at {cpu}%\nRAM at {ram}%\nDisk at {disk}%"

        self.menuMonitorSnapshot: Menu = Menu("Monitor Snapshot", lambda: MonitorSnapshot(), logger=self.logger)
        self.menuMonitorSnapshot.options = [
            MenuOption("Return", lambda: self.menuMonitorSnapshot.Drop()),
        ]
        
        def AddAlarm(key = None, data = None):
            self.logger.appendlog(content="Alarm Set")
            if not (key and data):
                self.logger.appendlog(content=f"Could Not Set Alarm: key is '{key}' data is '{data}'")
                return None
            try:
                data = float(data)
            except:
                self.logger.appendlog(content=f"Could Not Set Alarm: '{data}' is not a number (float)")
                return f"Could Not Set Alarm: '{data}' is not a number (float)"
            if 0<=data<=100:
                self.monitor.alarm_add([key, data])
                self.logger.appendlog(content=f"Set Alarm: {key} at {data}%")
                return f"Set Alarm: {key} at {data}%" 
            else:
                self.logger.appendlog(content=f"Could Not Set Alarm {key} at {data}. Outside Range 0-100 (%)")
                return f"Could Not Set Alarm {key} at {data}. Outside Range 0-100"
            
        self.menuAlarmSetCPU: Menu = MenuInput("Set CPU Alarm: 0-100 (%)", logger=self.logger)
        self.menuAlarmSetCPU.options = [
            MenuOption("Confirm", lambda: self.menuSetData(self.menuAlarmSet, AddAlarm(self.monitor.KEY_CPU, self.menuAlarmSetCPU.data)))
        ]
        self.menuAlarmSetRAM: Menu = MenuInput("Set RAM Alarm: 0-100 (%)", logger=self.logger)
        self.menuAlarmSetRAM.options = [
            MenuOption("Confirm", lambda: self.menuSetData(self.menuAlarmSet, AddAlarm(self.monitor.KEY_RAM, self.menuAlarmSetRAM.data)))
        ]
        self.menuAlarmSetDISK: Menu = MenuInput("Set Disk Alarm: 0-100 (%)", logger=self.logger)
        self.menuAlarmSetDISK.options = [
            MenuOption("Confirm", lambda: self.menuSetData(self.menuAlarmSet, AddAlarm(self.monitor.KEY_DISK, self.menuAlarmSetDISK.data)))
        ]
        self.menuAlarmSet: Menu = Menu("Set Alarm", logger=self.logger)
        self.menuAlarmSet.options = [
            MenuOption("Return", lambda: self.menuAlarmSet.Drop()),
            MenuOption("Set CPU Alarm", lambda: self.menuSet(self.menuAlarmSetCPU)),
            MenuOption("Set RAM Alarm", lambda: self.menuSet(self.menuAlarmSetRAM)),
            MenuOption("Set Disk Alarm", lambda: self.menuSet(self.menuAlarmSetDISK)),
        ]

        def ListAlarm():
            self.logger.appendlog(content=f"List Alarms")
            self.logger.appendlog(content=" & ".join([f"{i[0]} at {i[1]}%" for i in self.monitor.alarm_list()]))
            return "\n".join([f"{i[0]} at {i[1]}%" for i in self.monitor.alarm_list()])
        
        self.menuAlarmList: Menu = Menu("List Alarm", lambda: ListAlarm(), logger=self.logger)
        self.menuAlarmList.options = [
            MenuOption("Return", lambda: self.menuAlarmList.Drop()),
        ]

        self.streamtime = 0
        def MonitorStream():
            self.logger.appendlog(content="Monitor Stream") if self.menuMonitorStream.streamtime == 0 else None
            if not self.monitor.monitor:
                self.logger.appendlog(content="Monitor Is Not ON") if self.menuMonitorStream.streamtime == 0 else None
                return "Monitor Is Not ON"
            
            cpu, ram, disk = self.monitor.monitor_snapshot_list()
            cpua, rama, diska = self.monitor.monitor_snapshot_alarm_list()
            cpua = cpua if cpua[1] != -1 else None
            rama = rama if rama[1] != -1 else None
            diska = diska if diska[1] != -1 else None
            #return f"{cpua}, {rama}, {diska}"
            if cpua: self.logger.appendlog(content=f"CPU Alarm Triggered: {cpua[0]} at {cpua[1]}%, {self.menuMonitorStream.streamtime}s Elapsed")
            if rama: self.logger.appendlog(content=f"RAM Alarm Triggered: {rama[0]} at {rama[1]}%, {self.menuMonitorStream.streamtime}s Elapsed")
            if diska: self.logger.appendlog(content=f"Disk Alarm Triggered: {diska[0]} at {diska[1]}%, {self.menuMonitorStream.streamtime}s Elapsed")
            timeprint = f"Session Time: {int(self.menuMonitorStream.streamtime)}s\n"
            cpuprint = f"CPU at {cpu}% {f"Triggered Alarm: {f"{cpua[0]} at {cpua[1]}%"}" if cpua else ""}\n"

            cpuprintL = text.BGRED+"".ljust(math.floor(cpu), "*")+text.BGGREEN+"".ljust(math.ceil(100-cpu),"-")+f"{text.END}\n"
            ramprint = f"RAM at {ram}% {f"Triggered Alarm: {f"{rama[0]} at {rama[1]}%"}" if rama else ""}\n"
            ramprintL = text.BGRED+"".ljust(math.floor(ram), "*")+text.BGGREEN+"".ljust(math.ceil(100-ram),"-")+f"{text.END}\n"
            diskprint = f"Disk at {disk}% {f"Triggered Alarm: {f"{diska[0]} at {diska[1]}%"}" if diska else ""}\n"
            diskprintL = text.BGRED+"".ljust(math.floor(disk), "*")+text.BGGREEN+"".ljust(math.ceil(100-disk),"-")+f"{text.END}\n"
            return timeprint+cpuprint+cpuprintL+ramprint+ramprintL+diskprint+diskprintL
            
        self.menuMonitorStream: Menu = MenuNonBlocking("Monitor Stream", lambda: MonitorStream(), logger=self.logger)
        self.menuMonitorStream.options = [
            MenuOption("Return", lambda: self.menuMonitorStream.Drop()),
        ]

        def RemoveAlarm(menuindex):
            self.logger.appendlog(content=f"Alarm Removed: {" at".join(str(self.monitor.alarm_list()[menuindex-1])[1:-1].replace("'", "").split(','))}%")
            self.menuAlarmRemove.options.pop(menuindex)
            self.monitor.alarm_remove(self.monitor.alarm_list()[menuindex-1])
            self.menuAlarmRemove.cursor = min(self.menuAlarmRemove.cursor, len(self.menuAlarmRemove.options)-1)
            #self.menuAlarmRemove.Drop()

        def RemoveAlarmData():
            self.menuAlarmRemove.options = [
                MenuOption("Return", lambda: self.menuAlarmRemove.Drop()),
            ]

            for alarm in self.monitor.alarm_list():
                self.menuAlarmRemove.options.append(MenuOption(f"{alarm[0]}, {alarm[1]}", lambda: RemoveAlarm(self.menuAlarmRemove.cursor)))
                self.menuAlarmRemove.Drop()

        self.menuAlarmRemove: Menu = Menu("Remove Alarm", lambda: RemoveAlarmData(), logger=self.logger)
        self.menuAlarmRemove.options = [
            MenuOption("Return", lambda: self.menuAlarmRemove.Drop()),
        ]

        print("\033[?25l")
        self.menu:Menu = self.menuMain.Get()
        text.clear()

    def menuSet(self, menu:Menu):
        self.menu = menu.Get()

    def menuSetData(self, menu: Menu, data):
        menu.data = data

#try:
main = Main()
#except Exception as e: print(e)