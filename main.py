import time
import os
import datetime
import json
import psutil

from textefficiency import text
from logger import Logger
from psmonitor import Monitor
from menu import Menu, MenuOption, MenuInput, MenuNonBlocking

class Main():
    def __init__(self):
        self.logger = Logger()
        self.monitor = Monitor()

        self.menuMain:Menu = Menu("Select Option")
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
            self.logger.appendlog(self.logger.path_action, "Start Monitor")
            if not self.monitor.monitor: 
                self.logger.appendlog(self.logger.path_action, "Monitor Is On")
                self.monitor.monitor_start()
                return "Monitor Is ON"
            else:
                self.logger.appendlog(self.logger.path_action, "Monitor Is Already On")
                return "Monitor Is Already ON"
        self.menuStartMonitor:Menu = Menu("Start Monitor", lambda: MonitorStart())
        self.menuStartMonitor.options = [
            MenuOption("Confirm", lambda: self.menuStartMonitor.Drop()),
        ]

        def MonitorSnapshot():
            self.logger.appendlog(self.logger.path_action, "Monitor Snapshot")
            if not self.monitor.monitor:
                self.logger.appendlog(self.logger.path_action, "Monitor Is Not ON")
                return "Monitor Is Not ON"
            
            cpu, ram, disk = self.monitor.monitor_snapshot_list()

            self.logger.appendlog(self.logger.path_action, f"CPU: {cpu}% & RAM: {ram}% & Disk: {disk}%")
            return f"CPU: {cpu}%\nRAM: {ram}%\nDisk: {disk}%"

        self.menuMonitorSnapshot: Menu = Menu("Monitor Snapshot", lambda: MonitorSnapshot())
        self.menuMonitorSnapshot.options = [
            MenuOption("Return", lambda: self.menuMonitorSnapshot.Drop()),
        ]
        
        def AddAlarm(key = None, data = None):
            self.logger.appendlog(self.logger.path_action, "Alarm Set")
            if not (key and data):
                self.logger.appendlog(self.logger.path_action, f"Could Not Set Alarm: key is '{key}' data is '{data}'")
                return None
            try:
                data = float(data)
            except:
                self.logger.appendlog(self.logger.path_action, "")
                return f"Could Not Set Alarm: '{data}' is not a number (float)"
            if 0<=data<=100:
                self.monitor.alarm_add([key, data])
                self.logger.appendlog(self.logger.path_action, f"Set Alarm {key}: {data}%")
                return f"Set Alarm: {key}: {data}%" 
            else:
                self.logger.appendlog(self.logger.path_action, f"Could Not Set {key} Alarm: {data} Outside Range 0-100")
                return f"Could Not Set {key} Alarm: {data} Outside Range 0-100"
            
        self.menuAlarmSetCPU: Menu = MenuInput("Set CPU Alarm: 0-100 (%)")
        self.menuAlarmSetCPU.options = [
            MenuOption("Confirm", lambda: self.menuSetData(self.menuAlarmSet, AddAlarm(self.monitor.KEY_CPU, self.menuAlarmSetCPU.data)))
        ]
        self.menuAlarmSetRAM: Menu = MenuInput("Set RAM Alarm: 0-100 (%)")
        self.menuAlarmSetRAM.options = [
            MenuOption("Confirm", lambda: self.menuSetData(self.menuAlarmSet, AddAlarm(self.monitor.KEY_RAM, self.menuAlarmSetRAM.data)))
        ]
        self.menuAlarmSetDISK: Menu = MenuInput("Set Disk Alarm: 0-100 (%)")
        self.menuAlarmSetDISK.options = [
            MenuOption("Confirm", lambda: self.menuSetData(self.menuAlarmSet, AddAlarm(self.monitor.KEY_DISK, self.menuAlarmSetDISK.data)))
        ]
        self.menuAlarmSet: Menu = Menu("Set Alarm")
        self.menuAlarmSet.options = [
            MenuOption("Return", lambda: self.menuAlarmSet.Drop()),
            MenuOption("Set CPU Alarm", lambda: self.menuSet(self.menuAlarmSetCPU)),
            MenuOption("Set RAM Alarm", lambda: self.menuSet(self.menuAlarmSetRAM)),
            MenuOption("Set Disk Alarm", lambda: self.menuSet(self.menuAlarmSetDISK)),
        ]

        def ListAlarm():
            self.logger.appendlog(self.logger.path_action, f"List Alarms")
            self.logger.appendlog(self.logger.path_action, " & ".join([f"{i[0]}: {i[1]}%" for i in self.monitor.alarm_list()]))
            return "\n".join([f"{i[0]}: {i[1]}%" for i in self.monitor.alarm_list()])
        
        self.menuAlarmList: Menu = Menu("List Alarm", lambda: ListAlarm())
        self.menuAlarmList.options = [
            MenuOption("Return", lambda: self.menuAlarmList.Drop()),
        ]

        self.streamtime = 0
        def MonitorStream():
            self.logger.appendlog(self.logger.path_action, "Monitor Stream") if self.menuMonitorStream.streamtime == 0 else None
            if not self.monitor.monitor:
                self.logger.appendlog(self.logger.path_action, "Monitor Is Not ON") if self.menuMonitorStream.streamtime == 0 else None
                return "Monitor Is Not ON"
            
            cpu, ram, disk = self.monitor.monitor_snapshot_list()
            cpua, rama, diska = self.monitor.monitor_snapshot_alarm_list()
            cpua = cpua if cpua[1] != -1 else None
            rama = rama if rama[1] != -1 else None
            diska = diska if diska[1] != -1 else None
            #return f"{cpua}, {rama}, {diska}"
            if cpua: self.logger.appendlog(self.logger.path_action, f"CPU Alarm Triggered: {cpua[0]}: {cpua[1]}% at {self.menuMonitorStream.streamtime}s Elapsed")
            if rama: self.logger.appendlog(self.logger.path_action, f"CPU Alarm Triggered: {rama[0]}: {rama[1]}% at {self.menuMonitorStream.streamtime}s Elapsed")
            if diska: self.logger.appendlog(self.logger.path_action, f"CPU Alarm Triggered: {diska[0]}: {diska[1]}% at {self.menuMonitorStream.streamtime}s Elapsed")
            timeprint = f"Session Time: {int(self.menuMonitorStream.streamtime)}s\n"
            cpuprint = f"CPU: {cpu}% {f"Triggered Alarm {f"{cpua[0]}: {cpua[1]}%"}" if cpua else ""}\n"
            ramprint = f"RAM: {ram}% {f"Triggered Alarm {f"{rama[0]}: {rama[1]}%"}" if rama else ""}\n"
            diskprint = f"Disk: {disk}% {f"Triggered Alarm {f"{diska[0]}: {diska[1]}%"}" if diska else ""}\n"
            return timeprint+cpuprint+ramprint+diskprint
            
        self.menuMonitorStream: Menu = MenuNonBlocking("Monitor Stream", lambda: MonitorStream())
        self.menuMonitorStream.options = [
            MenuOption("Return", lambda: self.menuMonitorStream.Drop()),
        ]

        def RemoveAlarm(menuindex):
            self.logger.appendlog(self.logger.path_action, f"Alarm Removed: {self.monitor.alarm_list()[menuindex-1]}")
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

        self.menuAlarmRemove: Menu = Menu("Remove Alarm", lambda: RemoveAlarmData())
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