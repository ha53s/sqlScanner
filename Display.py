import pyfiglet
from termcolor import colored
from pyfiglet import figlet_format

def toolScreen():
    text = "SQL GUARD"
    ascii_art = pyfiglet.figlet_format(text)
    font = colored(ascii_art, color='magenta')
    print(font)
    print("\033[92m" + "   ~~ Welcome to SQL GUARD ~~" + "\033[0m")
    print("\033[95m" + "---------------------------------------" + "\033[0m")
    print("\033[95m" + " [!] Version :1.0 " + "\033[0m")
    print("\033[95m" + " [!] Copyrights : Students Final Project at IAU " + "\033[0m")
    print("\033[95m" + " [!] Course : CYS 403 Programming for Cybersecurity " + "\033[0m")
    print("\033[95m" + " [!] Instructor : Ms. Reem Alassaf " + "\033[0m")
    print("\033[95m" + "---------------------------------------" + "\033[0m")
    print("\033[92m" + "   Written by: Group[5]" + "\033[0m")
    print("\033[95m" + "---------------------------------------" + "\033[0m")
    
    print("\033[95m" + " [+] Zahrah Aljanabi " + "\033[0m")
    print("\033[95m" + " [+] Hams Almansori" + "\033[0m")
    print("\033[95m" + " [+] Reiman Almohana " + "\033[0m")
    print("\033[95m" + " [+] Sara Khalid Almulla " + "\033[0m")
    print("\033[95m" + " [+] Reem Majed Alotaibi " + "\033[0m")
    print("\033[95m" + "---------------------------------------" + "\033[0m")
    print("\033[93m" + " Options: " + "\033[0m")
    print("\033[95m" + "---------------------------------------" + "\033[0m")
    print("\033[95m" + " [1] Scan Website for SQL injection Vulnrability " + "\033[0m")
    print("\033[95m" + " [2] SQL Injection Payload Genorater " + "\033[0m")
    print("\033[95m" + " [3] Generate Report " + "\033[0m")
    print("\033[95m" + " [4] Quit " + "\033[0m")


  
if __name__ == "__main__":
    toolScreen()