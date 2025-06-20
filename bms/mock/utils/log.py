class Log:
    class color:
        HEADER = '\033[95m'
        DEBUG = '\33[90m'
        INFO = '\033[96m'
        SUCCESS = '\033[92m'
        WARNING = '\033[93m'
        ERROR = '\033[91m'
        RESET = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

    def error(self, msg):
        symbol = f"\r{self.color.BOLD}[{self.color.ERROR}-{self.color.RESET + self.color.BOLD}]{self.color.RESET}"
        print(f"{symbol} {msg}")

    def warning(self, msg):
        symbol = f"\r{self.color.BOLD}[{self.color.WARNING}!{self.color.RESET + self.color.BOLD}]{self.color.RESET}"
        print(f"{symbol} {msg}")

    def flow(self, msg):
        symbol = f"\r{self.color.BOLD}[{self.color.WARNING}>{self.color.RESET + self.color.BOLD}]{self.color.RESET}"
        print(f"{symbol} {msg}")

    def success(self, msg):
        symbol = f"\r{self.color.BOLD}[{self.color.SUCCESS}+{self.color.RESET + self.color.BOLD}]{self.color.RESET}"
        print(f"{symbol} {msg}")

    def info(self, msg):
        symbol = f"\r{self.color.BOLD}[{self.color.INFO}i{self.color.RESET + self.color.BOLD}]{self.color.RESET}"
        print(f"{symbol} {msg}")

    def debug(self, msg):
        symbol = f"\r{self.color.BOLD + self.color.DEBUG}[#]{self.color.RESET}"
        print(f"{symbol} {msg}")


log = Log()