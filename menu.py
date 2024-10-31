from keyboard import getch
from textefficiency import text
from logger import Logger

import os
import time

#Interactable menu options
class MenuOption:
    def __init__(self, text = "", action = None) -> None:
        self.text: str = text
        self.action = action

    def Activate(self):
        return self.action() if self.action else None

#Menu Class
class Menu:
    def __init__(self, text = "", getdata = None, logger = None) -> None:
        self.logger: Logger = logger
        self.text:str = text
        self.getdata = getdata
        self.data = None #self.getdata() if self.getdata else None
        self.options:list = []

        self.cursor:int = 0

        self.menu_loop = True

    def Get(self):
        self.logger.appendlog(content=f"In Menu: {self.text}")
        self.data = self.getdata() if self.getdata else None
        self.cursor = 1 if len(self.options)>1 else 0
        self.menu_loop = True
        self.Draw()
        self.Update()
        return self
    
    def Drop(self):
        self.menu_loop = False
        return self

    def Draw(self):
        text.clear()
        print(f"{self.text}{text.END}")
        print(self.data) if self.data else None
        for optionindex in range(1,len(self.options)):
            print(f"{text.BGWHITE if optionindex == self.cursor else text.BLUE}[{optionindex}] {self.options[optionindex].text.ljust(len(self.text), " ")}{text.END}")
        print(f"{text.BGWHITE if 0 == self.cursor else text.BLUE}[{0}] {self.options[0].text.ljust(len(self.text), " ")}{text.END}")


    def Update(self):
        while self.menu_loop:
            key = getch.readkey()
            
            KEYS_ARROW = [b'H', b'P']
            KEYS_RETURN = [b'\r', b'\n']
            KEYS_ESC = [b'\x1b']
            KEYS_NUMBERS= b'1234567890'
            KEYS = KEYS_ARROW+KEYS_RETURN+KEYS_ESC
            if key != b'':
                if key in KEYS or key in KEYS_NUMBERS:
                    if key in KEYS_ARROW:
                        if key == b'H':
                            self.cursor = (self.cursor-1)%len(self.options)
                        if key == b'P':
                            self.cursor = (self.cursor+1)%len(self.options)
                    
                    if key in KEYS_NUMBERS:
                        self.cursor = int(key.decode())%len(self.options)

                    if key in KEYS_RETURN:
                        self.logger.appendlog(content=f"In Menu: {self.text}: selected option {self.cursor} {self.options[self.cursor].text}")
                        self.options[self.cursor].Activate() if len(self.options)>0 else None

                    if key in KEYS_ESC:
                        self.menu_loop = False


                    self.Draw()

#
class MenuNonBlocking(Menu):
    def __init__(self, text="", getdata=None, logger = None) -> None:
        super().__init__(text, getdata, logger)
        self.interval: float = 0.25
        self.streamtime = 0

    def Get(self):
        self.streamtime = 0
        return super().Get()


    def Update(self):
        while self.menu_loop:
            self.data = self.getdata() if self.getdata else None
            key = getch.readkey()
            
            skipwait = False
            KEYS_ARROW = [b'H', b'P']
            KEYS_RETURN = [b'\r', b'\n']
            KEYS_ESC = [b'\x1b']
            KEYS_NUMBERS= b'1234567890'
            KEYS = KEYS_ARROW+KEYS_RETURN+KEYS_ESC
            if key != b'':
                if key in KEYS or key in KEYS_NUMBERS:
                    if key in KEYS_ARROW:
                        if key == b'H':
                            self.cursor = (self.cursor-1)%len(self.options)
                        if key == b'P':
                            self.cursor = (self.cursor+1)%len(self.options)
                    
                    if key in KEYS_NUMBERS:
                        self.cursor = int(key.decode())%len(self.options)

                    if key in KEYS_RETURN:
                        self.logger.appendlog(content=f"In Menu: {self.text}: selected option {self.cursor} {self.options[self.cursor].text}")
                        self.options[self.cursor].Activate() if len(self.options)>0 else None

                    if key in KEYS_ESC:
                        self.menu_loop = False
                    skipwait = True

            if skipwait:
                self.Draw()
            else:
                self.Draw()
                time.sleep(self.interval)
                self.streamtime+=self.interval
            
            

class MenuInput(Menu):
    def __init__(self, text="", getdata=None, logger = None) -> None:
        super().__init__(text, None, logger)
    
    def Get(self):
        self.logger.appendlog(content=f"In Menu: {self.text}")
        self.data = self.getdata() if self.getdata else ""
        self.cursor = 1 if len(self.options)>1 else 0
        self.menu_loop = True
        self.Draw()
        self.Update()
        return self

    def Draw(self):
        text.clear()
        print(f"{self.text}{text.END}")
        print(f"> {self.data if self.data else ""}\033[107m \033[0m")
    
    def Update(self):
        while self.menu_loop:
            key = getch.readkey()
            KEYS_RETURN = [b'\r', b'\n']
            KEYS_ESC = [b'\x1b']
            KEYS_BACKSPACE = [b'\x08', b'\x7f']
            KEYS_NUMBERS = b'1234567890'
            KEYS_DECIMAL = b',.'
            KEYS = KEYS_RETURN+KEYS_ESC+KEYS_BACKSPACE
            if key != b'':
                if key in KEYS or key in KEYS_NUMBERS or key in KEYS_DECIMAL:
                    if key in KEYS_NUMBERS:
                        self.data += key.decode()

                    if key in KEYS_DECIMAL:
                        decimal = '.'
                        if not decimal in self.data:
                            self.data += decimal

                    if key in KEYS_BACKSPACE:
                        self.data = self.data[:-1]

                    if key in KEYS_ESC:
                        if self.data:
                            self.data = ""
                        else:
                            self.menu_loop = False

                    if key in KEYS_RETURN:
                        self.logger.appendlog(content=f"In Menu: {self.text}: input value {self.data} at {self.options[self.cursor].text}")
                        self.options[self.cursor].Activate() if len(self.options)>0 else None
                        self.menu_loop = False
                
                self.Draw()
