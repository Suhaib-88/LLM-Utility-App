from tabulate import tabulate
class Logger():
    def __init__(self) -> None:
        self.MAGENTA='\033[95m' 
        self.END='\033[0m' 
        self.BOLD= '\033[1m'
        self.UNDERLINE= '\033[4m'

    def log(self,message):
        print(f"LOG: {self.MAGENTA}+ {message} + {self.END}")

    def log_table(self,data,headers):
        self.log(tabulate(data, headers= headers, tablefmt='grid'))