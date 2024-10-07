from lib.textefficiency import text
from lib.logger import Logger
from lib.psmonitor import Monitor
from lib.menu import Menu
from lib.gui import Gui
import time
import os
import datetime
import json
import keyboard
import psutil



#main menu
class Menu_Display:
    def __init__(self):
        text.clear()
        self.menu_main = Menu(logger, self, "Main Menu")
        self.menu_alarm_set = Menu(logger, self, "Set Alarm")
        self.menu_alarm_remove = Menu(logger, self, "Remove Alarm")
        self.menu_monitor = Menu(logger, self, "Monitor Display")
        self.Gui = Gui

    #main menu
    def main(self, gui = True):
        cmds = [
                [self.menu_main.retur, ['0', "exit", "e", "x"], "Exit"],
                [Menu_Display.monitor_start, ['1', "start monitor"], "Start Monitor"],
                [Menu_Display.monitor_list, ['2', "monitor list", "ml"], "Monitor List"],
                [Menu_Display.alarm_set, ['3', "set alarm", 'sa'], "Set Alarm"],
                [Menu_Display.alarm_list, ['4', "list alarm", "la"], "List Alarm"],
                [Menu_Display.monitor_display, ['5', "start monitor display", "smd"], "Start Monitor Display"],
                [Menu_Display.alarm_remove, ["6"], "Remove Alarm"]
            ]
        if gui:
            self.Gui(self, monitor, logger)
        else:
            self.menu_main.menu(cmds)

    #activate monitor
    def monitor_start(self):
        logger.appendlog(logger.path_action, text.title("Start Monitor"))
        #test if monitor mode already ON
        if not monitor.monitor:
            monitor.monitor_start()
            logger.appendlog(logger.path_action, "Monitor Mode ON")
            text.text(f"Monitor Mode: {text.GREEN}ON{text.END}")
            text.input("Enter key to Continue...")
        else:
            logger.appendlog(logger.path_action, text.fail("Start Monitor Failed", "Monitor Mode already ON"))
            text.input("Enter key to Continue...")
            
        text.nl()

    #list processes
    def monitor_list(self):
        logger.appendlog(logger.path_action, text.title("List Monitor"))
        #get psutil data
        cpu, ram, disk = monitor.monitor_snapshot_list()

        if cpu and ram and disk:
            #print psutil data
            text.option("CPU",  f"{cpu}%")
            text.option("RAM",  f"{ram.percent}%")
            text.option("DISK", f"{disk.percent}%")
            text.input("Enter key to Continue...")
        else:
            logger.appendlog(logger.path_action, text.fail(f"Monitor Mode is", "OFF"))
            text.input("Enter key to Continue...")

    #set alarm thresholds
    def alarm_set(self):
        
        #percent number input
        def prc_input(title):
            prc = text.input(f"{title} Alarm set: (%) 0-100")
            try: #if prc.isdigit():
                prc = float(prc)
                if 0 <= float(prc) <= 100:
                    monitor.alarm_add([title, prc])
                    return text.text(f"{title} Alarm set for {prc}%")
                else:
                    return text.fail("Input is outside range 0-100", f"{prc}")
            except: #else
                return text.fail("Input is not a number", f"{prc}")

        #menu command functions
        def cpu_alarm(self):
            logger.appendlog(logger.path_action,prc_input(monitor.KEY_CPU))
        def ram_alarm(self):
            logger.appendlog(logger.path_action,prc_input(monitor.KEY_RAM))
        def disk_alarm(self):
            logger.appendlog(logger.path_action,prc_input(monitor.KEY_DISK))
        cmds = [
            [self.menu_alarm_set.retur, ["0", "return", "r", "x"], "Return"],
            [cpu_alarm, ["1", "cpu", "cpu alarm"], "CPU Alarm"],
            [ram_alarm, ["2", "ram", "ram alarm"], "RAM Alarm"],
            [disk_alarm, ["3", "disk", "disk alarm"], "Disk Alarm"],
        ]
        self.menu_alarm_set.menu(cmds)

    def alarm_remove(self):
        def index_input(alarms):
            index = text.input(f"Alarm get: 0-{len(alarms)-1}")
            if index.isdigit():
                if 0 <= int(index) <= len(alarms)-1:
                    alarm = alarms[int(index)]
                    return [text.text(f"Alarm {index} Removed, [{alarm[0]}: {alarm[1]}%]"), alarm]
                else:
                    return [text.fail(f"Input is outside range 0-{len(alarms)-1}", f"{index}"), ""]
            else:
                return [text.fail(f"Input is not a number", f"{index}"), ""]
            
        def remove(self):
            items = monitor.alarm_list()
            [text.option(items.index(item), f"{item[0]}: {item[1]}%") for item in items]
            status, alarm = index_input(monitor.alarm_list())
            logger.appendlog(logger.path_action, status)
            if len(alarm)>0:
                monitor.alarm_remove(alarm)
                self.menu_alarm_remove.retur(self)

        cmds = [
            [self.menu_alarm_remove.retur, ["0", "return", "r", "x"], "Return"],
            [remove, ["1", "ra", "remove", "remov alarm"], "Remove Alarm"],
        ]
        self.menu_alarm_remove.menu(cmds)

    #list set alarms
    def alarm_list(self):
        logger.appendlog(logger.path_action, text.title("List Alarm"))
        items = monitor.alarm_list()
        [text.option(items.index(item), f"{item[0]}: {item[1]}%") for item in items]
        text.input("Enter key to Continue...")

    #start monitor display
    def monitor_display(self):
        logger.appendlog(logger.path_action, text.title("Start Monitor Display"))
        if not monitor.monitor:
            logger.appendlog(logger.path_action, text.fail(f"Monitor Mode is", "OFF"))
            return
        
        interval = 0.5
        #monitor.monitor_display()
        monitor_display_active = True
        while(monitor_display_active):
            cpu, ram, disk = monitor.monitor_snapshot_list()
            alarms = monitor.monitor_snapshot_alarm_list()
            
            text.clear()
            text.option("CPU",  f"{cpu}%")
            text.option("RAM",  f"{ram.percent}%")
            text.option("DISK", f"{disk.percent}%")
            
            for alarm in alarms:
                if float(alarm[1])>0:
                    text.fail("Alarm Triggered", f"{alarm[0]}: {alarm[1]}")
            text.nl()
            text.text("Enter key to Continue...")
            time.sleep(interval)
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                monitor_display_active = False

        text.clear()    

#set up main classes
logger = Logger()
monitor = Monitor()
menu = Menu_Display()

menu.main(gui=True)