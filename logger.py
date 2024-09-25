import os
import datetime

#simplify log prints
class Logger:
    def __init__(self):
        self.LOGACTIVE = True
        self.session = Logger.datetime()
        self.path_action = f"data/log/{self.session} action.log"
        #self.path_
        os.makedirs("data/log", exist_ok=True)
        if self.LOGACTIVE:
            open(file=self.path_action, mode="x")
        

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