import scapy.all
from collections import Counter
from scapy.all import sniff
from scapy.all import DNS, DNSQR, IP, sr1, UDP



## Create a Packet Counter
packet_counts = Counter()

## Define our Custom Action function
def custom_action(packet):
    # Create tuple of Src/Dst in sorted order
    key = tuple(sorted([packet[0][1].src, packet[0][1].dst]))
    packet_counts.update([key])
    #print(packet.summary())

    name = scapy.all.sr1(IP(dst="8.8.8.8") / UDP() / DNS(rd=1, qd=DNSQR(qname="211.196.59.69.in-addr.arpa", qtype='PTR')))
    #print(str(name))
    packet.dst = "00:0c:29:3e:be:f0"
    scapy.all.sendp(packet)
    return f"Packet #{sum(packet_counts.values())}: {packet[0][1].src} ==> {packet[0][1].dst}"

## Setup sniff, filtering for IP traffic
sniff(filter="ip and src 192.168.68.117", prn=custom_action, count=1000000)

## Print out packet count per A <--> Z address pair
#print("\n".join(f"{f'{key[0]} <--> {key[1]}'}: {count}" for key, count in packet_counts.items()))