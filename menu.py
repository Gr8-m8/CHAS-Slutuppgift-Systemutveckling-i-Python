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
        self.logger: Logger = logger #logger
        self.text:str = text #Menu displaytext
        self.getdata = getdata #function for generating data
        self.data = None #data variable
        self.options:list = [] #menu options
        self.cursor:int = 0 #cursor variable
        self.menu_loop = True #Update loop variable

        #Key inputs as bytes
        self.KEYS_MOVE = [b'H', b'P'] #menu move options
        self.KEYS_MOVE_INDEX= b'1234567890' #menu move options, to index
        self.KEYS_ACTIVATE = [b'\r', b'\n', b' '] #menu activate options
        self.KEYS_ESC = [b'\x1b'] #menu leave menu
        self.KEYS = self.KEYS_MOVE+self.KEYS_ACTIVATE+self.KEYS_ESC

    def Get(self): #load menu, for active menu
        self.logger.appendlog(content=f"In Menu: {self.text}")
        self.loaddata()
        self.cursor = 1 if len(self.options)>1 else 0 #set cursor to item index 1 unless there is only an item 0
        self.menu_loop = True
        self.Draw()
        self.Update()
        return self
    
    def loaddata(self):
        self.data = self.getdata() if self.getdata else None #set data with data get menu
    
    def Drop(self): #stop update
        self.menu_loop = False
        return self

    def Draw(self): #console UI
        text.clear()
        print(f"{self.text}{text.END}") #print text
        print(self.data) if self.data else None #print data i data
        for optionindex in range(1,len(self.options)): #list all menu items, (exept index 0)
            print(f"{text.BGWHITE if optionindex == self.cursor else text.BLUE}[{optionindex}] {self.options[optionindex].text.ljust(len(self.text), " ")}{text.END}")
        print(f"{text.BGWHITE if 0 == self.cursor else text.BLUE}[{0}] {self.options[0].text.ljust(len(self.text), " ")}{text.END}") #draw option index 0 last (used for quit/return/confirm)


    def Update(self): #update on event
        while self.menu_loop:
            key = getch.readkey() #read key in stdin

            if key != b'':
                self.Draw() if self.keyaction(key) else None #if key is valid action draw
     
    
    def keyaction(self, key): #action dependant on keys
        if key in self.KEYS or key in self.KEYS_MOVE_INDEX: #valid keys for action
            if key in self.KEYS_MOVE:
                if key == b'H':
                    self.cursor = (self.cursor-1)%len(self.options)
                if key == b'P':
                    self.cursor = (self.cursor+1)%len(self.options)

            if key in self.KEYS_MOVE_INDEX:
                self.cursor = int(key.decode())%len(self.options)

            if key in self.KEYS_ACTIVATE:
                self.logger.appendlog(content=f"In Menu: {self.text}: selected option {self.cursor} {self.options[self.cursor].text}")
                self.options[self.cursor].Activate() if len(self.options)>0 else None

            if key in self.KEYS_ESC:
                self.logger.appendlog(content=f"In Menu: {self.text}: ESC Menu")
                self.menu_loop = False
            
            return True
        return False


    def PopOption(self, optionindex): #remove menuoptions by index
        self.options.pop(optionindex)
        self.cursor = min(self.cursor, len(self.options)-1)

#
class MenuNonBlocking(Menu): #menu that updates independently from user input
    def __init__(self, text="", getdata=None, logger = None) -> None:
        super().__init__(text, getdata, logger)
        self.interval: float = 0.25 #update interval
        self.streamtime = 0 #variable tracking in menu time

    def Get(self):
        self.streamtime = 0 #reset time in menu
        return super().Get()


    def Update(self):
        while self.menu_loop:
            self.data = self.getdata() if self.getdata else None
            key = getch.readkey()
            
            skipwait = False #variable to skip interval wait (if valid input)
            
            if key != b'':
                skipwait = self.keyaction(key)

            if skipwait:
                self.Draw()
            else:
                self.Draw()
                time.sleep(self.interval)
                self.streamtime+=self.interval
            
            

class MenuInput(Menu):
    def __init__(self, text="", getdata=None, logger = None) -> None:
        super().__init__(text, None, logger)
        self.KEYS_BACKSPACE = [b'\x08', b'\x7f']
        self.KEYS_NUMBERS = b'1234567890'
        self.KEYS_DECIMAL = b',.'
        self.KEYS_INPUT = self.KEYS_NUMBERS+self.KEYS_DECIMAL #keys valid for input
        self.KEYS += self.KEYS_BACKSPACE
    
    def loaddata(self):
        self.data = self.getdata() if self.getdata else "" #set data with data get menu

    def Draw(self):
        text.clear()
        print(f"{self.text}{text.END}")
        print(f"> {self.data if self.data else ""}\033[107m \033[0m")
    
    def keyaction(self, key):
        if key in self.KEYS or key in self.KEYS_INPUT:
            if key in self.KEYS_NUMBERS:
                self.data += key.decode()

            if key in self.KEYS_DECIMAL:
                decimal = '.'
                if not decimal in self.data:
                    self.data += decimal

            if key in self.KEYS_BACKSPACE:
                self.data = self.data[:-1]

            if key in self.KEYS_ESC:
                if self.data:
                    self.data = ""
                else:
                    self.menu_loop = False
                    self.logger.appendlog(content=f"In Menu: {self.text}: ESC Menu")

            if key in self.KEYS_ACTIVATE:
                self.logger.appendlog(content=f"In Menu: {self.text}: input value {self.data} at {self.options[self.cursor].text}")
                self.options[self.cursor].Activate() if len(self.options)>0 else None
                self.menu_loop = False
            
            return True
        return False
