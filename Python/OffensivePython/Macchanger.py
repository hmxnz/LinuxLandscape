#!/usr/bin/env python3
import sys
import os
import platform
import random
import subprocess
import argparse
import re

def generate_random_mac():
    """Genera una MAC aleatoria válida localmente administrada"""
    return "02:%02x:%02x:%02x:%02x:%02x" % tuple(random.randint(0x00, 0xFF) for _ in range(5))

def get_current_mac(interface):
    system = platform.system()
    if system == "Linux":
        try:
            output = subprocess.check_output(["cat", f"/sys/class/net/{interface}/address"])
            return output.decode().strip()
        except Exception:
            return None
    elif system == "Windows":
        try:
            output = subprocess.check_output(["getmac", "/v", "/fo", "list"], shell=True).decode()
            pattern = re.compile(r"Physical Address:\s+([0-9A-Fa-f:-]{17})")
            matches = pattern.findall(output)
            if matches:
                # En Windows no podemos asociar fácil la MAC a la interfaz exacta aquí
                return matches[0]
            return None
        except Exception:
            return None
    else:
        print(f"Sistema {system} no soportado")
        return None

def change_mac(interface, new_mac):
    system = platform.system()
    if system == "Linux":
        try:
            subprocess.run(["sudo", "ip", "link", "set", "dev", interface, "down"], check=True)
            subprocess.run(["sudo", "ip", "link", "set", "dev", interface, "address", new_mac], check=True)
            subprocess.run(["sudo", "ip", "link", "set", "dev", interface, "up"], check=True)
            print(f"MAC cambiada a {new_mac} en {interface}")
        except subprocess.CalledProcessError as e:
            print(f"Error cambiando MAC: {e}")
    elif system == "Windows":
        try:
            # En Windows se cambia la MAC mediante registro y netsh, se necesita administrador
            cmd = f'netsh interface set interface "{interface}" admin=disable'
            subprocess.run(cmd, shell=True, check=True)
            cmd = f'reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Class\\{{4d36e972-e325-11ce-bfc1-08002be10318}}\\0001" /v "NetworkAddress" /d "{new_mac.replace(":", "")}" /f'
            subprocess.run(cmd, shell=True, check=True)
            cmd = f'netsh interface set interface "{interface}" admin=enable'
            subprocess.run(cmd, shell=True, check=True)
            print(f"MAC cambiada a {new_mac} en {interface} (Windows)")
        except subprocess.CalledProcessError as e:
            print(f"Error cambiando MAC en Windows: {e}")
    else:
        print(f"Sistema {system} no soportado para cambio de MAC")

def main():
    parser = argparse.ArgumentParser(description="MAC Changer multiplataforma (Linux/Windows)")
    parser.add_argument("-i", "--interface", required=True, help="Interfaz de red (Linux: eth0/wlan0, Windows: nombre exacto)")
    parser.add_argument("-m", "--mac", help="MAC nueva (si no se pasa, se genera aleatoria)")
    args = parser.parse_args()

    interface = args.interface
    new_mac = args.mac if args.mac else generate_random_mac()

    current_mac = get_current_mac(interface)
    if not current_mac:
        print("No se pudo obtener la MAC actual. Revisa la interfaz o ejecuta como administrador/root.")
        sys.exit(1)

    print(f"MAC actual de {interface}: {current_mac}")
    change_mac(interface, new_mac)
    final_mac = get_current_mac(interface)
    print(f"MAC final de {interface}: {final_mac}")

if __name__ == "__main__":
    main()

#todo
"""

!Ejemplo de uso EN LINUX:
sudo python3 macchanger.py -i wlan0       # MAC aleatoria
sudo python3 macchanger.py -i eth0 -m 00:11:22:33:44:55  # MAC específica

!Ejemplo de uso EN WINDOWS (ejecutar CMD como administrador):
python macchanger.py -i "Ethernet"       # MAC aleatoria
python macchanger.py -i "Wi-Fi" -m 00:11:22:33:44:55  # MAC específica

"""
#todo
# Hecho por Hugo Martínez Segura (hmxnz)