import getpass
import webview
import os
import time
from cryptography.fernet import Fernet
from colorama import init, Fore, Style
import sqlite3
import stat
import platform

# Creates SQL Database
conn = sqlite3.connect('Data.db')
cursor = conn.cursor()

# Init colorama
init(autoreset=True)

# ========== Retro Style Print ==========
def type_out(text, delay=0.05):
    for char in text:
        print(Fore.GREEN + Style.BRIGHT + char, end="", flush=True)
        time.sleep(delay)
    print()

# ========== Secure Permissions ==========
def set_secure_permissions(filename):
    if platform.system() != "Windows":
        os.chmod(filename, 0o600)
    else:
        os.chmod(filename, stat.S_IREAD | stat.S_IWRITE)

# ========== Key Management ==========
def load_key(filename):
    if not os.path.exists(filename):
        key = Fernet.generate_key()
        with open(filename, "wb") as f:
            f.write(key)
        set_secure_permissions(filename) 
        return key
    else:
        set_secure_permissions(filename)  
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

    set_secure_permissions("userf.txt")
    set_secure_permissions("passf.txt")

    type_out(">>> ACCOUNT CREATED SUCCESSFULLY")

# ========== Applications ==========
def terminal():
    while True:
        cmd = input(Fore.GREEN + Style.BRIGHT + "TERMINAL >> ")
        if cmd.lower() in ["exit", "quit"]:
            break
        os.system(cmd)

def code():
    print(Fore.GREEN + ">> Code editor not implemented.")
def notes():
    # Create table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()

    while True:
        os.system("cls" if os.name == "nt" else "clear")
        type_out(">>> NOTES APP", 0.02)
        print(Fore.GREEN + Style.BRIGHT + """
        1. Add a Note
        2. View Notes
        3. Delete Note(s)
        4. Return to Main Menu
        """)
        choice = input(Fore.GREEN + "Choose an option: ").strip()
        
        if choice == '1':
            title = input("Enter a note title: ").strip()
            note = input("Enter a note: ").strip()
            cursor.execute('INSERT INTO notes (title, content) VALUES (?, ?)', (title, note))
            conn.commit()
            print(Fore.GREEN + "Note added successfully!")
            input(Fore.GREEN + "Press Enter to continue...")
        
        elif choice == '2':
            view_notes()
        elif choice == '3':
            delete_notes()
        elif choice == '4':
            break
        
        else:
            print(Fore.RED + "Invalid choice. Try again.")
            time.sleep(1)

def view_notes():
    cursor.execute('SELECT id, title, content, created_at FROM notes ORDER BY created_at DESC')
    rows = cursor.fetchall()
    os.system("cls" if os.name == "nt" else "clear")
    type_out(">>> YOUR NOTES", 0.02)
    if not rows:
        print(Fore.YELLOW + "No notes found.")
    else:
        for row in rows:
            print(Fore.CYAN + f"ID: {row[0]} | Title: {row[1]} | Created: {row[3]}")
            print(Fore.GREEN + f"Content: {row[2]}")
            print("-" * 40)
    input(Fore.GREEN + "Press Enter to return to notes menu...")

def delete_notes():
    note_id = input("Enter the ID of the note to view: ").strip()
    cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
    note = cursor.fetchone()
    if note:
        cursor.execute("DELETE FROM notes WHERE id = ?", (note_id))
        print(Fore.GREEN + "Note Deleted")
        
    else:
        print(Fore.RED + "No note found with that ID.")
    input("Press Enter to continue...")
def browser():
    web = input(Fore.GREEN + Style.BRIGHT + ">> ENTER A URL (include http/https): ")
    try:
        webview.create_window("Browser", web)
        webview.start()
    except Exception as e:
        print(Fore.RED + f"!! ERROR OPENING BROWSER: {e}")

def chat():
    print(Fore.GREEN + ">> Chat not implemented.")

def games():
    print(Fore.GREEN + ">> Games not implemented.")

def calc():
    print(Fore.GREEN + ">> Calculator not implemented.")

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
        ||  3. Notes                  || 
        ||  4. Browser                ||
        ||  5. Text Chat              ||
        ||  6. Games                  ||
        ||  7. Calculator             || 
        ||  8. Shutdown               ||
        ================================
        """)
        choice = input(Fore.GREEN + Style.BRIGHT + "CHOOSE AN APPLICATION [1-8]: ").strip()

        if choice == "1":
            terminal()
        elif choice == "2":
            code()
        elif choice == "3":
            notes()
        elif choice == "4":
            browser()
        elif choice == "5":
            chat()
        elif choice == "6":
            games()
        elif choice == "7":
            calc()
        elif choice == "8":
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
                break 
        elif a_check == "no":
            make_acc()
        else:
            print(Fore.RED + "!! INVALID INPUT. PLEASE TYPE 'yes' OR 'no'.")
            input(Fore.GREEN + ">> PRESS ENTER TO TRY AGAIN...")

if __name__ == "__main__":
    main()
