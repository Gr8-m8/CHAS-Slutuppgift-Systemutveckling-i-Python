import psutil
import datetime
import os

class text:
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

    @staticmethod
    def nl():
        print("")

    @staticmethod
    def text(content = ""):
        print(f"{content}")
        return f"{content}"

    @staticmethod
    def option(id = "", content = ""):
        print(f"{text.BOLD}{text.BLUE}[{id}]{text.END} {content}{text.END}")
        return f"[{id}] {content}"

    @staticmethod
    def title(content = ""):
        print(f"\t{text.BOLD}{text.CYAN}=== {content} === {text.END}")
        return f"=== {content} ==="

    @staticmethod
    def input(content = ""):
        if content or content != "":
            content +='\n'
        print(f"{text.YELLOW}"); contentout = input(f"{content}> ").lower(); print(f"{text.END}")
        return contentout
    
    @staticmethod
    def fail(content = "", contentfail = ""):
        print(f"{content}: '{text.RED}{text.UNDERLINE}{contentfail}{text.END}'")
        return f"{content}: '{contentfail}'"

class Log:
    def __init__(self):
        self.sessionraw = datetime.datetime.now()
        self.session = f"{self.sessionraw.year}-{self.sessionraw.month}-{self.sessionraw.day}_[{self.sessionraw.hour}-{self.sessionraw.minute}-{self.sessionraw.second}]"
        self.path_action = f"data/log/{self.session}_action.log"
        open(file=self.path_action, mode="x")
        #self.path_

    def appendlog(self, path, content):
        log = open(path, "a")
        log.writelines(f"[{datetime.datetime.now()}] {content}")
        log.close()

class Monitor:
    def __init__(self):
        self.logger = Log()
        self.cmds = Monitor.cmdsf()

        self.monitor = False

    def main(self):
        try:
            main_loop=True
            while(main_loop):
                self.logger.appendlog(self.logger.path_action, text.title("Menu"))
                text.option(1, "Start monitor")
                text.option(2, "monitor List")
                text.option(3, "Set Alarm")
                text.option(4, "List Alarm")
                text.option(5, "Start Monitor Mode")
                text.option(0, "Exit")
                cmd = text.input()
                self.logger.appendlog(self.logger.path_action, f"> {cmd}")
                
                cmd_activate=False
                for i in range(len(self.cmds)):
                    if cmd in self.cmds[i][1]:
                        cmd_activate = True
                        self.cmds[i][0](self)

                if not cmd_activate:
                    self.logger.appendlog(self.logger.path_action, text.fail("Invalid option", cmd))
                    text.nl()
        except KeyboardInterrupt:
            self.logger.appendlog(self.logger.path_action, "KeyboardInterrupt")
            print(text.END)
            exit(1)

    def exit(self):
        self.logger.appendlog(self.logger.path_action, text.title("Exit"))
        exit(0)

    def start_monitor(self):
        self.logger.appendlog(self.logger.path_action, text.title("Start Monitor"))
        if not self.monitor:
            self.monitor = True
            self.logger.appendlog(self.logger.path_action, "Monitor Mode ON")
            text.text(f"Monitor Mode: {text.GREEN}ON{text.END}")
        else:
            self.logger.appendlog(self.logger.path_action, text.fail("Start Monitor Failed", "Monitor Mode already ON"))
            
        text.nl()

    def list_monitor(self):
        self.logger.appendlog(self.logger.path_action, text.title("List Monitor"))

    def set_alarm(self):
        self.logger.appendlog(self.logger.path_action, text.title("Set Alarm"))

    def list_alarm(self):
        self.logger.appendlog(self.logger.path_action, text.title("Lsit Alarm"))

    def start_monitor_display(self):
        self.logger.appendlog(self.logger.path_action, text.title("Start Monitor Display"))
    
    #@staticmethod
    def cmdsf():
        return [
        [Monitor.exit, ['0', "exit", "e", "x"]],
        [Monitor.start_monitor, ['1', "start monitor"]],
        [Monitor.list_monitor, ['2', "monitor list", "ml"]],
        [Monitor.set_alarm, ['3', "set alarm", 'sa']],
        [Monitor.list_alarm, ['4', "list alarm", "la"]],
        [Monitor.start_monitor_display, ['5', "start monitor display", "smd"]]
        ]

mon = Monitor()
mon.main()