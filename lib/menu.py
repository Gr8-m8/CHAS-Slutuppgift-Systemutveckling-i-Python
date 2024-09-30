from lib.textefficiency import text

class Menu:
    def __init__(self, logger, menu_display, title):
        self.logger = logger
        self.menu_display = menu_display
        self.title = title

        self.menu_active=True

    def retur(self, status):
        self.logger.appendlog(self.logger.path_action, text.text(status))
        self.menu_active=False

    def menu(self, commands):
        try:
            #main menu options: [function, activate commands, description]
            cmds = commands
            #main loop
            self.menu_active = True
            while(self.menu_active):
                #print menu
                self.logger.appendlog(self.logger.path_action, text.title(self.title))
                #list main menu options, by index and description
                for i in range(len(cmds)-1):
                    text.option(i+1, cmds[i+1][-1])
                text.option(0, cmds[0][-1])
                #read user input
                cmd = text.input()
                self.logger.appendlog(self.logger.path_action, f"> {cmd}")

                cmd_activate=False
                #match input with menu exit
                if not cmd in cmds[0][1]:
                    #match input with commnds, if match: run function
                    for i in range(0, len(cmds)):
                        if cmd in cmds[i][1]:
                            cmd_activate = True
                            cmds[i][0](self.menu_display)
                else:
                    cmd_activate = True
                    cmds[0][0](cmds[0][-1])
                    break
                
                #if invalid input
                if not cmd_activate:
                    self.logger.appendlog(self.logger.path_action, text.fail("Invalid option", cmd))
                    text.nl()
        #allow keybordinterrupt (ctrl+c)
        except KeyboardInterrupt:
            text.clear()
            self.logger.appendlog(self.logger.path_action, text.text("Exit (KeyboardInterrupt)"))
            print(text.END)
            exit(1)