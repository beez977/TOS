import getpass
import webview
import os
import time
from cryptography.fernet import Fernet
from colorama import init, Fore, Style

# Init colorama
init(autoreset=True)

# ========== Retro Style Print ==========
def type_out(text, delay=0.05):
    for char in text:
        print(Fore.GREEN + Style.BRIGHT + char, end="", flush=True)
        time.sleep(delay)
    print()

# ========== Key Management ==========
def load_key(filename):
    if not os.path.exists(filename):
        key = Fernet.generate_key()
        with open(filename, "wb") as f:
            f.write(key)
        return key
    else:
        with open(filename, "rb") as f:
            return f.read()

ukey = load_key("ukey.key")
pkey = load_key("pkey.key")

# ========== Login ==========
def login():
    os.system("cls" if os.name == "nt" else "clear")
    type_out("\n>>> LOGIN MODE ACTIVE")
    username = input(Fore.GREEN + ">> ENTER USERNAME: ").strip()
    pas = getpass.getpass(Fore.GREEN + ">> ENTER PASSWORD: ")

    if not os.path.exists("userf.txt") or not os.path.exists("passf.txt"):
        type_out("!! NO ACCOUNTS FOUND. CREATE ONE FIRST.")
        return False

    try:
        with open("userf.txt", "rb") as f:
            enc_user = f.read()
        with open("passf.txt", "rb") as f:
            enc_pass = f.read()

        dec_user = Fernet(ukey).decrypt(enc_user).decode()
        dec_pass = Fernet(pkey).decrypt(enc_pass).decode()

        if username == dec_user and pas == dec_pass:
            type_out(">>> ACCESS GRANTED")
            return True
        else:
            type_out("!! LOGIN FAILED. INCORRECT CREDENTIALS.")
            return False
    except Exception:
        type_out("!! DECRYPTION ERROR - POSSIBLE KEY MISMATCH OR CORRUPTION.")
        return False

# ========== Create Account ==========
def make_acc():
    os.system("cls" if os.name == "nt" else "clear")
    type_out("\n>>> ACCOUNT CREATION MODE")
    username = input(Fore.GREEN + ">> NEW USERNAME: ").strip()
    pas = getpass.getpass(Fore.GREEN + ">> NEW PASSWORD: ")

    enc_user = Fernet(ukey).encrypt(username.encode())
    enc_pass = Fernet(pkey).encrypt(pas.encode())

    with open("userf.txt", "wb") as f:
        f.write(enc_user)
    with open("passf.txt", "wb") as f:
        f.write(enc_pass)

    type_out(">>> ACCOUNT CREATED SUCCESSFULLY")

# ========== Applications ==========
def terminal():
    while True:
        cmd = input(Fore.GREEN + Style.BRIGHT + "TERMINAL >> ")
        if cmd.lower() in ["exit", "quit"]:
            break
        os.system(cmd)

def code():
    print(Fore.YELLOW + ">> Code editor not implemented.")

def browser():
    web = input(Fore.GREEN + Style.BRIGHT + ">> ENTER A URL (include http/https): ")
    try:
        webview.create_window("Browser", web)
        webview.start()
    except Exception as e:
        print(Fore.RED + f"!! ERROR OPENING BROWSER: {e}")

def chat():
    print(Fore.YELLOW + ">> Chat not implemented.")

def games():
    print(Fore.YELLOW + ">> Games not implemented.")

def calc():
    print(Fore.YELLOW + ">> Calculator not implemented.")

# ========== Options Screen ==========
def options():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        type_out(">>> SYSTEM ONLINE", 0.03)
        print(Fore.GREEN + Style.BRIGHT + """
        ================================
        ||  WELCOME TO THE OS         ||
        ================================
        ||  1. Terminal               ||
        ||  2. Code Editor            ||
        ||  3. Browser                ||
        ||  4. Text Chat              ||
        ||  5. Games                  ||
        ||  6. Calculator             || 
        ||  7. Shutdown               ||
        ================================
        """)
        choice = input(Fore.GREEN + Style.BRIGHT + "CHOOSE AN APPLICATION [1-7]: ").strip()

        if choice == "1":
            terminal()
        elif choice == "2":
            code()
        elif choice == "3":
            browser()
        elif choice == "4":
            chat()
        elif choice == "5":
            games()
        elif choice == "6":
            calc()
        elif choice == "7":
            type_out("SHUTTING DOWN...")
            break    
        else:
            print(Fore.RED + "!! INVALID OPTION. TRY AGAIN.")
        input(Fore.GREEN + ">> PRESS ENTER TO RETURN TO MENU...")

# ========== Entry Point ==========
def main():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        type_out(">>> WELCOME TO TERMINAL OS v1.0 <<<", 0.03)
        a_check = input(Fore.GREEN + ">> DO YOU HAVE AN ACCOUNT? (yes/no): ").strip().lower()

        if a_check == "yes":
            if login():
                options()
                break  # Exit after logout or shutdown
        elif a_check == "no":
            make_acc()
        else:
            print(Fore.RED + "!! INVALID INPUT. PLEASE TYPE 'yes' OR 'no'.")
        input(Fore.GREEN + ">> PRESS ENTER TO TRY AGAIN...")

if __name__ == "__main__":
    main()
