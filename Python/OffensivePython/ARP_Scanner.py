from scapy.all import ARP, Ether, srp

def arp_scan(target_ip):
    # Create an ARP request packet
    arp_request = ARP(pdst=target_ip)
    # Create an Ethernet frame to broadcast the ARP request
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    # Combine the Ethernet frame and ARP request
    arp_request_broadcast = broadcast / arp_request
    # Send the packet and receive the response
    answered_list = srp(arp_request_broadcast, timeout=2, verbose=False)[0]

    # Parse the responses
    clients = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients.append(client_dict)
    return clients

def print_results(clients):
    print("IP Address\t\tMAC Address")
    print("-----------------------------------------")
    for client in clients:
        print(f"{client['ip']}\t\t{client['mac']}")

# Example usage
target_ip = "192.168.18.1/24"  # Adjust to your network range
clients = arp_scan(target_ip)
print_results(clients)