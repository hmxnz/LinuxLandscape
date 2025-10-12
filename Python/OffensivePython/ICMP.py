#!/usr/bin/env python3
import subprocess
import platform
import ipaddress
import argparse
import asyncio

def ping(host):
    """Envía un ping a host y devuelve True si responde"""
    system = platform.system().lower()
    if system == "windows":
        command = ["ping", "-n", "1", "-w", "1000", host]
    else:
        command = ["ping", "-c", "1", "-W", "1", host]
    result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return result.returncode == 0

async def ping_host(host, semaphore):
    async with semaphore:
        loop = asyncio.get_event_loop()
        alive = await loop.run_in_executor(None, ping, host)
        return host, alive

async def scan_network(target, concurrency=100):
    """Acepta IP individual o red completa"""
    semaphore = asyncio.Semaphore(concurrency)

    # Verificar si es red o IP
    try:
        net = ipaddress.ip_network(target, strict=False)
        hosts = [str(ip) for ip in net.hosts()]
    except ValueError:
        # Si no es una red válida, asumimos IP individual
        hosts = [target]

    tasks = [asyncio.create_task(ping_host(host, semaphore)) for host in hosts]

    for coro in asyncio.as_completed(tasks):
        host, alive = await coro
        if alive:
            print(f"{host} está activo")

def main():
    parser = argparse.ArgumentParser(description="Escáner ICMP (ping) de IP o red")
    parser.add_argument("-t", "--target", required=True,
                        help="IP o red a escanear (ej: 192.168.1.10 o 192.168.1.0/24)")
    parser.add_argument("-c", "--concurrency", type=int, default=100,
                        help="Número máximo de pings simultáneos")
    args = parser.parse_args()

    asyncio.run(scan_network(args.target, args.concurrency))

if __name__ == "__main__":
    main()



#todo
"""
Ejemplo de uso:
Escanea la red 192.168.1.0/24 con 100 pings concurrentes
python3 ICMP.py -n 192.168.1.0/24
"""
#todo
#Hecho por Hugo Martínez Segura (hmxnz)