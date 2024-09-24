import psutil
import datetime
import os
import json

#decorate text, simplyfy/unify prints
class text:
    #console text decoration codes
    BGWHITE = '\033[107m'
    BGCYAN = '\033[106m'
    BGPURPLE = '\033[105m'
    BGBLUE = '\033[104m'
    BGYELLOW = '\033[103m'
    BGGREEN = '\033[102m'
    BGRED = '\033[101m'
    BGGRAY = '\033[100m'
    BGBLACK = '\033[40m'
    
    CYAN = '\033[96m'
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    GRAY = '\033[90m'

    STRIKETHROUGH = '\033[28m'
    UNDERLINE = '\033[4m'
    ITALICS = '\033[3m'
    BOLD = '\033[1m'
    END = '\033[0m'

    #clear console
    @staticmethod
    def clear():
        CLEARACTIVE = True
        if CLEARACTIVE:
            os.system('cls')

    #print new line
    @staticmethod
    def nl():
        print("")

    #print and prompt user input
    @staticmethod
    def input(content = ""):
        if content or content != "":
            content +='\n'
        print(f"{text.YELLOW}"); contentout = input(f"{content}> ").lower(); print(f"{text.END}")
        text.clear()
        return contentout
    
    #print text
    @staticmethod
    def text(content = ""):
        print(f"{content}")
        return f"{content}"

    #print list item
    @staticmethod
    def option(id = "", content = ""):
        print(f"{text.BOLD}{text.BLUE}[{id}]{text.END} {content}{text.END}")
        return f"[{id}] {content}"

    #print header
    @staticmethod
    def title(content = ""):
        print(f"\t{text.BOLD}{text.CYAN}=== {content} === {text.END}")
        return f"=== {content} ==="

    #print error and reason
    @staticmethod
    def fail(content = "", contentfail = ""):
        print(f"{content}: '{text.RED}{text.UNDERLINE}{contentfail}{text.END}'")
        return f"{content}: '{contentfail}'"
    

#simplify log prints
class Logger:
    def __init__(self):
        self.LOGACTIVE = True
        self.session = Logger.datetime()
        self.path_action = f"data/log/{self.session} action.log"
        
        if self.LOGACTIVE:
            open(file=self.path_action, mode="x")
        #self.path_

    #add to logfile
    def appendlog(self, path, content):
        if self.LOGACTIVE:
            log = open(path, "a")
            log.write(f"[{Logger.datetime()}] {content}\n")
            log.close()

    #formated date time str
    @staticmethod
    def datetime():
        return f"{datetime.datetime.now().strftime('%Y-%m-%d_[%H-%M-%S]')}"

#simplify json save/load
class Saver:
    def __init__(self):
        pass

    PATH_ALARMS = f"data/save/alarms.json"
    def save(self, path, content):
        try:
            open(path, "x")
        except:
            pass

        try:
            save_file = open(path, "w")
            save_file.write(json.dumps(content))
            save_file.close()
        except:
            pass

    def load(self, path):
        content = None
        try:
            save_file = open(path, "r")
            if save_file:
                content = json.loads(save_file.read())
                save_file.close()
        except:
            try:
                open(path, "x")
            except:
                pass
            
        return content

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
            self.alarms = alarm_save

    def alarm_add(self, alarm):
        self.alarms[alarm[0]].append(alarm)
        saver.save(saver.PATH_ALARMS, self.alarms)

    def alarm_remove(self, alarm):
        self.alarms[alarm[0]].remove(alarm)
        saver.save(saver.PATH_ALARMS, self.alarms)

    def alarm_list(self):
        return monitor.alarms[monitor.KEY_CPU]+monitor.alarms[monitor.KEY_RAM]+monitor.alarms[monitor.KEY_DISK]

    KEY_CPU = 'CPU'
    KEY_RAM = 'RAM'
    KEY_DISK = 'Disk'

#main menu
class Menu:
    def __init__(self):
        text.clear()
        self.menu_main()

    def menu(self, title, commands):
        try:
            #main menu options: [function, activate commands, description]
            cmds = commands
            #main loop
            main_loop_active=True
            while(main_loop_active):
                #print menu
                logger.appendlog(logger.path_action, text.title(title))
                #list main menu options, by index and description
                for i in range(len(cmds)-1):
                    text.option(i+1, cmds[i+1][-1])
                text.option(0, cmds[0][-1])
                #read user input
                cmd = text.input()
                logger.appendlog(logger.path_action, f"> {cmd}")

                cmd_activate=False
                #match input with menu exit
                if not cmd in cmds[0][1]:
                    #match input with commnds, if match: run function
                    for i in range(0, len(cmds)):
                        if cmd in cmds[i][1]:
                            cmd_activate = True
                            cmds[i][0](self)
                else:
                    cmd_activate = True
                    cmds[0][0](self, cmds[0][-1])
                    break
                
                #if invalid input
                if not cmd_activate:
                    logger.appendlog(logger.path_action, text.fail("Invalid option", cmd))
                    text.nl()
        #allow keybordinterrupt (ctrl+c)
        except KeyboardInterrupt:
            logger.appendlog(logger.path_action, "exit(KeyboardInterrupt)")
            print(text.END)
            exit(1)

    #main menu
    def menu_main(self):
        cmds = [
                [Menu.retur, ['0', "exit", "e", "x"], "Exit"],
                [Menu.monitor_start, ['1', "start monitor"], "Start Monitor"],
                [Menu.monitor_list, ['2', "monitor list", "ml"], "Monitor List"],
                [Menu.alarm_set, ['3', "set alarm", 'sa'], "Set Alarm"],
                [Menu.alarm_list, ['4', "list alarm", "la"], "List Alarm"],
                [Menu.monitor_display, ['5', "start monitor display", "smd"], "Start Monitor Display"],
            ]
        self.menu("Main Menu", cmds)

    #exit program
    def retur(self, status = "Return"):
        logger.appendlog(logger.path_action, text.text(status))
        #exit(0)

    #activate monitor
    def monitor_start(self):
        logger.appendlog(logger.path_action, text.title("Start Monitor"))
        #test if monitor mode already ON
        if not monitor.monitor:
            monitor.monitor = True
            logger.appendlog(logger.path_action, "Monitor Mode ON")
            text.text(f"Monitor Mode: {text.GREEN}ON{text.END}")
        else:
            logger.appendlog(logger.path_action, text.fail("Start Monitor Failed", "Monitor Mode already ON"))
            
        text.nl()

    #list processes
    def monitor_list(self):
        logger.appendlog(logger.path_action, text.title("List Monitor"))
        #get psutil data
        cpu = [psutil.cpu_count(), psutil.cpu_freq() ,psutil.cpu_percent(), psutil.cpu_stats(), psutil.cpu_times(), psutil.cpu_times_percent()]
        ram = [psutil.swap_memory(), psutil.virtual_memory()]
        disk = [psutil.disk_io_counters(), psutil.disk_partitions(), psutil.disk_usage("C:")]
        #print psutil data
        text.option("CPU",  f"{cpu[2]}%"+ "\t{cpu}")
        text.option("RAM",  f"{ram[0].percent}%"+ "\t{ram}")
        text.option("DISK", f"{disk[-1].percent}%"+ "\t{disk}")
        text.input("Any key to Continue...")

    #set alarm thresholds
    def alarm_set(self):
        
        #percent number input
        def prc_input(title):
            prc = text.input(f"{title} Alarm set: (%) 0-100")
            if prc.isdigit():
                if 0 <= int(prc) <= 100:
                    monitor.alarm_add([title, prc])
                    return text.text(f"{title} Alarm set for {prc}%")
                else:
                    return text.fail("Input is outside range 0-100", f"{prc}")
            else:
                return text.fail("Input is not a number", f"{prc}")

        #menu command functions
        def cpu_alarm(self):
            logger.appendlog(logger.path_action,prc_input(monitor.KEY_CPU))
        def ram_alarm(self):
            logger.appendlog(logger.path_action,prc_input(monitor.KEY_RAM))
        def disk_alarm(self):
            logger.appendlog(logger.path_action,prc_input(monitor.KEY_DISK))
        cmds = [
            [Menu.retur, ["0", "return", "r", "x"], "Return"],
            [cpu_alarm, ["1", "cpu", "cpu alarm"], "CPU Alarm"],
            [ram_alarm, ["2", "ram", "ram alarm"], "RAM Alarm"],
            [disk_alarm, ["3", "disk", "disk alarm"], "Disk Alarm"],
        ]
        self.menu("Alarm Set", cmds)

    def alarm_remove(self):
        cmds = [
            [Menu.retur, ["0", "return", "r", "x"], "Return"],
        ]
        self.menu("Remove Alarm", cmds)

    #list set alarms
    def alarm_list(self):
        logger.appendlog(logger.path_action, text.title("List Alarm"))
        items = monitor.alarm_list()
        [text.option(items.index(item), f"{item[0]}: {item[1]}%") for item in items]
        text.input("Any key to Continue...")

    #start monitor display
    def monitor_display(self):
        logger.appendlog(logger.path_action, text.title("Start Monitor Display"))

#set up main classes
logger = Logger()
saver = Saver()
monitor = Monitor()
menu = Menu()