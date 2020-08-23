#utf-8
import requests
import sys
import pprint
from argparse import ArgumentParser

def printBanner():
    sys.stdout.write(CYAN)
    print(  "   _   _   _   _   _   _     _   _   _   _   _   _   _  \n"
            "  / \ / \ / \ / \ / \ / \   / \ / \ / \ / \ / \ / \ / \ \n"
            " ( m | e | t | h | 0 | d ) ( c | h | 3 | c | k | 3 | r )\n"
            "  \_/ \_/ \_/ \_/ \_/ \_/   \_/ \_/ \_/ \_/ \_/ \_/ \_/ \n")

def printTheCat():
    sys.stdout.write(GREEN)
    print(
            "                                            :\n"
            "                                           :::\n"
            "                    '::                   ::::\n"
            "                    '::::.     .....:::.:::::::\n"
            "                    '::::::::::::::::::::::::::::\n"
            "                    ::::::XUWWWWWU:::::XW$$$$$$WX:\n"
            "                    ::::X$$$$$$$$$$W::X$$$$$$$$$$Wh\n"
            "                   ::::t$$$$$$$$$$$$W:$$$$$$P*$$$$M::\n"
            "                   :::X$$$$$$''''$$$$X$$$$$   ^$$$$X:::\n"
            "                  ::::M$$$$$$    ^$$$RM$$$L    <$$$X::::\n"
            "                .:::::M$$$$$$     $$$R:$$$$.   d$$R:::`\n"
            "               '~::::::?$$$$$$...d$$$X$6R$$$$$$$$RXW$X:'`\n"
            "                 '~:WNWUXT#$$$$$$$$TU$$$$W6IBBIW@$$RX:\n"
            "                  `~")

def beautyText(text):
    print("\n#######################################")
    print(text)
    print("#######################################\n")

RED   = "\033[1;31m"
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"

parser = ArgumentParser(description='http methods')
parser.add_argument('-t', '--target', type=str, metavar='',required=False, default=False, help='host:port')
parser.add_argument('-f', '--filename', type=str, metavar='',required=False, default=False, help='hosts from file')
args = parser.parse_args()

def getMethods(target):
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4 Supplemental Update) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15'}

    print('[*] Enviando petición de metodos disponibles .. ')
    verbs = requests.options(target)

    try:
        print('Los metodos habilitados son: %s \n[*] Comenzando pruebas individuales.. \n' % verbs.headers['allow'])
    except KeyError:
        print('[!!] El servidor ha rechadazo nuestra peticion OPTIONS \n[*] Comenzando pruebas individuales en cada método..\n')
        pass


    #get
    conn = requests.get(target, params=headers)
    data = '[!] GET METHOD recived: %s' % (conn.status_code)
    print(data)
    #post
    conn = requests.post(target, params=headers)
    data = '[!] POST METHOD recived: %s' % (conn.status_code)
    print(data)
    #put
    conn = requests.put(target, params=headers)
    data = '[!] PUT METHOD recived: %s' % (conn.status_code)
    print(data)
    #delete
    conn = requests.delete(target, params=headers)
    data = '[!] DELETE METHOD recived: %s' % (conn.status_code)
    print(data)
    #head
    conn = requests.head(target, params=headers)
    data = '[!] HEAD METHOD recived: %s' % (conn.status_code)
    print(data)
    #patch
    conn = requests.patch(target, params=headers)
    data = '[!] PATCH METHOD recived: %s' % (conn.status_code)
    print(data)

def run(target):
    try:
        getMethods(target)
    except Exception as e:
        sys.stdout.write(RED)
        data = '[!] %s: %s' % (e, target)
        print(data)

def runFromFile(filename):
    f = open(filename, 'r')
    for line in f:
        run(line)

printTheCat()
printBanner()

if args.filename != False:
    filelen = open(args.filename, 'r').read()
    if len(filelen) > 0:
        runFromFile(args.filename)
    else:
        sys.stdout.write(RED)
        beautyText('El archivo proporcionado no contiene informacion')
elif args.target != False:
    run(args.target)
if args.filename == False and args.target == False:
    sys.stdout.write(RED)
    beautyText('ERR: Proporciona un objetivo o un archivo con un objetivo por linea')
