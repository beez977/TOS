import os
from colorama import init, Fore, Style

def inp():
  c = input(Fore.GREEN + Style.BRIGHT + "Click 'e' to exit: ")
  return c

def play():

  init(autoreset=True)

  os.system("cls" if os.name == "nt" else "clear")
  print(Fore.GREEN + Style.BRIGHT + "TICTACTOE")
  print("------------------------------------")
  inp()
  

