import psutil
import datetime

class Log:
    def __init__(self):
        self.session = datetime.datetime.now()
        self.log = open(f"data/log/log_{self.session}")

    def appendlog(path, content):
        log = open(path)
        log.writelines(f"[{datetime.datetime.now()}] {content}")
        log.close()

class Monitor:
    def __init__(self):
        self.logger = Log()

    @staticmethod
    def main():
        main_loop=True
        while(main_loop):
            print(
                f"[1] Start Monitor\n"
                f"[2] Monitor list\n"
                f"[3] Set Alarm\n"
                f"[4] List Alarm\n"
                f"[5] Start Monitor Mode\n"
                f"[0] Exit\n"

            )
            cmd = input(">").lower()

            if cmd in ['0', "exit", "e", "x"]:
                main_loop=False
                #exit(0)

            if cmd in ['1', "start monitor"]:
                main_loop=False

            if cmd in ['2', "monitor list", "ml"]:
                main_loop=False

            if cmd in ['3', "set alarm", 'sa']:
                main_loop=False  

            if cmd in ['4', "list alarm", "la"]:
                main_loop=False  

            if cmd in ['5', "start monitor display", "smd"]:
                main_loop=False  

mon = Monitor()
mon.main()