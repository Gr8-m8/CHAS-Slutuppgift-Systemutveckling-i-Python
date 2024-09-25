import psutil
import time
from textefficiency import text
from saver import Saver

saver = Saver()
#manage program functions
class Monitor:
    def __init__(self):
        self.monitor = False
        self.alarms = {
            self.KEY_CPU:[],
            self.KEY_RAM:[],
            self.KEY_DISK:[],
            }
        
        alarm_save = saver.load(saver.PATH_ALARMS)
        if alarm_save:
            text.text("Loading Previously Configured Alarms...")
            time.sleep(0.5)
            self.alarms = alarm_save

    def monitor_start(self):
        self.monitor = True
        return self.monitor

    def monitor_list(self):
        #get psutil data
        cpu = [psutil.cpu_count(), psutil.cpu_freq() ,psutil.cpu_percent(), psutil.cpu_stats(), psutil.cpu_times(), psutil.cpu_times_percent()]
        ram = [psutil.swap_memory(), psutil.virtual_memory()]
        disk = [psutil.disk_io_counters(), psutil.disk_partitions(), psutil.disk_usage("C:")]
        return [cpu, ram, disk]

    def alarm_add(self, alarm):
        self.alarms[alarm[0]].append(alarm)
        saver.save(saver.PATH_ALARMS, self.alarms)
        return alarm

    def alarm_remove(self, alarm):
        self.alarms[alarm[0]].remove(alarm)
        saver.save(saver.PATH_ALARMS, self.alarms)
        return alarm

    def alarm_list(self):
        return self.alarms[self.KEY_CPU]+self.alarms[self.KEY_RAM]+self.alarms[self.KEY_DISK]
    
    def monitor_display(self):
        pass

    KEY_CPU = 'CPU'
    KEY_RAM = 'RAM'
    KEY_DISK = 'Disk'

