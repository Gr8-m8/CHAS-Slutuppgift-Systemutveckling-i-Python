import psutil
import datetime
import os

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

    #print new line
    @staticmethod
    def nl():
        print("")

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

    #print and prompt user input
    @staticmethod
    def input(content = ""):
        if content or content != "":
            content +='\n'
        print(f"{text.YELLOW}"); contentout = input(f"{content}> ").lower(); print(f"{text.END}")
        return contentout
    
    #print error and reason
    @staticmethod
    def fail(content = "", contentfail = ""):
        print(f"{content}: '{text.RED}{text.UNDERLINE}{contentfail}{text.END}'")
        return f"{content}: '{contentfail}'"

#simplify log prints
class Logger:
    def __init__(self):
        self.session = Logger.datetime()
        self.path_action = f"data/log/{self.session} action.log"
        open(file=self.path_action, mode="x")
        #self.path_

    #add to logfile
    def appendlog(self, path, content):
        log = open(path, "a")
        log.write(f"[{Logger.datetime()}] {content}\n")
        log.close()

    #formated date time str
    @staticmethod
    def datetime():
        return f"{datetime.datetime.now().strftime('%Y-%m-%d_[%H-%M-%S]')}"

#simplify json save/load
class Saver:
    pass

#manage program functions
class Monitor:
    def __init__(self):
        self.monitor = False
        self.alarms = []

#main menu
class Menu_Main:
    def __init__(self):
        self.cmds = Menu_Main.cmdsf()

        self.main()

    def main(self):
        try:
            main_loop=True
            while(main_loop):
                logger.appendlog(logger.path_action, text.title("Menu"))
                text.option(1, "Start Monitor")
                text.option(2, "Monitor List")
                text.option(3, "Set Alarm")
                text.option(4, "List Alarm")
                text.option(5, "Start Monitor Mode")
                text.option(0, "Exit")
                cmd = text.input()
                logger.appendlog(logger.path_action, f"> {cmd}")
                
                cmd_activate=False
                for i in range(len(self.cmds)):
                    if cmd in self.cmds[i][1]:
                        cmd_activate = True
                        self.cmds[i][0](self)

                if not cmd_activate:
                    logger.appendlog(logger.path_action, text.fail("Invalid option", cmd))
                    text.nl()
        except KeyboardInterrupt:
            logger.appendlog(logger.path_action, "KeyboardInterrupt")
            print(text.END)
            exit(1)

    def exit(self):
        logger.appendlog(logger.path_action, text.title("Exit"))
        exit(0)

    def start_monitor(self):
        logger.appendlog(logger.path_action, text.title("Start Monitor"))
        if not monitor.monitor:
            monitor.monitor = True
            logger.appendlog(logger.path_action, "Monitor Mode ON")
            text.text(f"Monitor Mode: {text.GREEN}ON{text.END}")
        else:
            logger.appendlog(logger.path_action, text.fail("Start Monitor Failed", "Monitor Mode already ON"))
            
        text.nl()

    def list_monitor(self):
        logger.appendlog(logger.path_action, text.title("List Monitor"))

    def set_alarm(self):
        logger.appendlog(logger.path_action, text.title("Set Alarm"))

    def list_alarm(self):
        logger.appendlog(logger.path_action, text.title("Lsit Alarm"))

    def start_monitor_display(self):
        logger.appendlog(logger.path_action, text.title("Start Monitor Display"))
    
    @staticmethod
    def cmdsf():
        return [
        [Menu_Main.exit, ['0', "exit", "e", "x"]],
        [Menu_Main.start_monitor, ['1', "start monitor"]],
        [Menu_Main.list_monitor, ['2', "monitor list", "ml"]],
        [Menu_Main.set_alarm, ['3', "set alarm", 'sa']],
        [Menu_Main.list_alarm, ['4', "list alarm", "la"]],
        [Menu_Main.start_monitor_display, ['5', "start monitor display", "smd"]]
        ]

saver = Saver()
logger = Logger()
monitor = Monitor()
menu_main = Menu_Main()