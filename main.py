from textefficiency import text
from logger import Logger
from psmonitor import Monitor

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
            text.clear()
            logger.appendlog(logger.path_action, text.text("Exit (KeyboardInterrupt)"))
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
                [Menu.alarm_remove, ["6"], "Remove Alarm"]
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
        cpu, ram, disk = monitor.monitor_list()
        #print psutil data
        text.option("CPU",  f"{cpu[2]}%"+ "\t{cpu}")
        text.option("RAM",  f"{ram[0].percent}%"+ "\t{ram}")
        text.option("DISK", f"{disk[-1].percent}%"+ "\t{disk}")
        text.input("Enter key to Continue...")

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
                Menu.retur(self)

        cmds = [
            [Menu.retur, ["0", "return", "r", "x"], "Return"],
            [remove, ["1", "ra", "remove", "remov alarm"], "Remove Alarm"],
        ]
        self.menu("Remove Alarm", cmds)

    #list set alarms
    def alarm_list(self):
        logger.appendlog(logger.path_action, text.title("List Alarm"))
        items = monitor.alarm_list()
        [text.option(items.index(item), f"{item[0]}: {item[1]}%") for item in items]
        text.input("Enter key to Continue...")

    #start monitor display
    def monitor_display(self):
        logger.appendlog(logger.path_action, text.title("Start Monitor Display"))

#set up main classes
logger = Logger()
monitor = Monitor()
menu = Menu()