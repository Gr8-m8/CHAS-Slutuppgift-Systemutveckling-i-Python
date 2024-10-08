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

    #clear console
    @staticmethod
    def clear():
        print(text.END)
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
        try:
            print(f"{text.YELLOW}"); contentout = input(f"{content}> ").lower(); print(f"{text.END}")
        except KeyboardInterrupt:
            print(f"{text.END}")
            contentout = "0"
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