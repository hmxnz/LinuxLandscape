#!/usr/bin/env python3
import socket
import argparse
import sys
import asyncio
from termcolor import colored  

#! OBTENER ARGUMENTOS
def get_args():
    parser = argparse.ArgumentParser(
        description='Escáner TCP de puertos (asíncrono con asyncio)'
    )
    parser.add_argument(
        "-H", "--host", dest="host",
        help="Dirección IP o nombre del objetivo (si no se pasa, se pedirá por consola)",
        type=str
    )
    parser.add_argument(
        "-p", "--puertos", dest="ports",
        help="Puertos a escanear. Ejemplos: 1-100 | 22,80,443 | 80",
        required=True,
        type=str
    )
    parser.add_argument(
        "-c", "--concurrency", dest="concurrency",
        help="Número máximo de conexiones simultáneas (default=500)",
        type=int,
        default=500
    )
    return parser.parse_args()

#! PARSEAR PUERTOS
def parse_ports(ports_str):
    ports_str = ports_str.strip()
    if '-' in ports_str:  # rango 1-100
        start, end = map(int, ports_str.split('-', 1))
        return range(start, end + 1)
    elif ',' in ports_str:  # lista 22,80,443
        return [int(p.strip()) for p in ports_str.split(',') if p.strip()]
    else:  # único puerto
        return [int(ports_str)]

#! ESCÁNER ASÍNCRONO DE PUERTO
async def scan_port(host, port, timeout=1.0):
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port),
            timeout=timeout
        )
        writer.close()
        try:
            await writer.wait_closed()
        except Exception:
            pass
        return port, True
    except Exception:
        return port, False

#! ESCÁNER DE RANGO DE PUERTOS
async def scan_ports(host, ports, concurrency=500, timeout=1.0):
    sem = asyncio.Semaphore(concurrency)

    async def sem_scan(port):
        async with sem:
            return await scan_port(host, port, timeout)

    tasks = [asyncio.create_task(sem_scan(p)) for p in ports]
    open_ports = []

    for coro in asyncio.as_completed(tasks):
        port, is_open = await coro
        if is_open:
            try:
                print(colored(f"Puerto {port} -> ABIERTO", "green"))
            except Exception:
                print(f"Puerto {port} -> ABIERTO")
            open_ports.append(port)
        # Si quieres ver cerrados, descomenta:
        # else:
        #     print(f"Puerto {port} -> cerrado")

    return open_ports

#! MAIN
def main():
    args = get_args()

    # Si no se pasa host por argumentos, se pide con input
    host = args.host if args.host else input("\n[?] INTRODUCE LA DIRECCION IP: ")

    try:
        ports = parse_ports(args.ports)
    except ValueError:
        print("Formato de puertos inválido. Usa 1-100 o 22,80,443 o 80")
        sys.exit(1)

    print(f"\nEscaneando {host} ...\n")
    open_ports = asyncio.run(scan_ports(host, ports, args.concurrency))

    print("\nResumen:")
    if open_ports:
        print("Puertos abiertos:", ", ".join(map(str, open_ports)))
    else:
        print("No se encontraron puertos abiertos en el rango indicado.")

if __name__ == "__main__":
    main()

#todo
""" 

Ejemplo de uso:
$ python3 PortScanner.py -H <Dirección IP> -p <Rango de puertos>

"""
#todo
# Hecho por Hugo Martínez Segura (hmxnz)