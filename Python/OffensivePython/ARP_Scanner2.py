import requests
from scapy.all import ARP, Ether, srp

def get_vendor(mac_address):
    try:
        response = requests.get(f"https://api.macvendors.com/{mac_address}", timeout=2)
        if response.status_code == 200:
            return response.text
        else:
            return "Unknown"
    except:
        return "Unknown"

def arp_scan(target_ip):
    print(f"[+] Scanning {target_ip}...")
    arp_request = ARP(pdst=target_ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = srp(arp_request_broadcast, timeout=2, verbose=False)[0]

    clients = []
    for element in answered_list:
        mac = element[1].hwsrc
        vendor = get_vendor(mac)
        client_dict = {
            "ip": element[1].psrc,
            "mac": mac,
            "vendor": vendor
        }
        clients.append(client_dict)
    return clients

def print_results(clients):
    if not clients:
        print("[-] No devices found.")
    else:
        print("IP Address\t\tMAC Address\t\tVendor")
        print("--------------------------------------------------------------")
        for client in clients:
            print(f"{client['ip']}\t\t{client['mac']}\t\t{client['vendor']}")

# Example usage
target_ip = "192.168.18.1/24"  # Adjust to your network
clients = arp_scan(target_ip)
print_results(clients)