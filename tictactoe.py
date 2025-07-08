import os
from colorama import init, Fore, Style

def play():

  init(autoreset=True)

  os.system("cls" if os.name == "nt" else "clear")
  print(Fore.GREEN + Style.BRIGHT + "TICTACTOE")
  print("------------------------------------")
  c = input(Fore.GREEN + Style.BRIGHT + "Play or Exit: ").strip()
  
  
