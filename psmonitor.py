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

    def monitor_snapshot_list(self):
        #get psutil data
        if self.monitor:
            cpu = psutil.cpu_percent() #[psutil.cpu_count(), psutil.cpu_freq() ,psutil.cpu_percent(), psutil.cpu_stats(), psutil.cpu_times(), psutil.cpu_times_percent()]
            ram = psutil.swap_memory() #[psutil.swap_memory(), psutil.virtual_memory()]
            disk = psutil.disk_usage("C:") #[psutil.disk_io_counters(), psutil.disk_partitions(), psutil.disk_usage("C:")]
            return [cpu, ram, disk]
        return [None, None, None]
    
    def monitor_snapshot_alarm_list(self):
        alarms = [[self.KEY_CPU, -1], [self.KEY_RAM, -1], [self.KEY_DISK, -1]]
        alarmkeys = [self.KEY_CPU, self.KEY_RAM, self.KEY_DISK]
        cpu, ram, disk = self.monitor_snapshot_list()
        
        #for alarmindex in range(len(alarmkeys)):
        #    for alarm in self.alarms[alarmkeys[alarmindex]]:
        #        if float(cpu) > float(alarm[1]) and float(alarms[alarmindex][1] < float(alarm[1])):
        #            alarms[alarmindex] = alarm
        valueindex = 1
        alarmindex = 0
        if cpu:
            try:
                for alarm in self.alarms[alarmkeys[alarmindex]]:
                    if float(cpu) > float(alarm[valueindex]) and float(alarms[alarmindex][valueindex] < float(alarm[valueindex])):
                        alarms[alarmindex] = alarm 
            except:
                pass
        alarmindex = 1
        if ram:
            try:
                for alarm in self.alarms[alarmkeys[alarmindex]]:
                    if float(ram.percent) > float(alarm[valueindex]) and float(alarms[alarmindex][valueindex] < float(alarm[valueindex])):
                        alarms[alarmindex] = alarm 
            except:
                pass
        alarmindex = 2
        if disk:
            try:
                for alarm in self.alarms[alarmkeys[alarmindex]]:
                    if float(disk.percent) > float(alarm[valueindex]) and float(alarms[alarmindex][valueindex] < float(alarm[valueindex])):
                        alarms[alarmindex] = alarm 
            except:
                pass

        return alarms

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
        cpu = psutil.cpu_percent()
        ram = psutil.swap_memory()
        disk = psutil.disk_usage("C:")

    KEY_CPU = 'CPU'
    KEY_RAM = 'RAM'
    KEY_DISK = 'Disk'

