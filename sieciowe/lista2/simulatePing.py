from scapy.all import IP, ICMP, send
from datetime import datetime
import time

def log_packet(info, logfile="ping_log.txt"):           # write to file with current date
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(logfile, "a") as f:
        f.write(f"[{timestamp}] {info}\n")
    print(f"[{timestamp}] {info}")

def simulate_ping(ip_src, ip_dst, id=1000, seq=1, logfile="ping_log.txt"):
    # Create Echo Request from IP1 -> IP2
    echo_request = IP(src=ip_src, dst=ip_dst) / ICMP(type=8, id=id, seq=seq)

    send(echo_request, verbose=False)

    # log i console and in file
    log_packet(f"Sent ICMP Echo Request from {ip_src} to {ip_dst} (id={id}, seq={seq})", logfile)

    # Simulate network delay, thanks to that we can see a time difference between
    # echo request and echo reply
    time.sleep(1)

    # Create Echo Reply from IP2 -> IP1
    echo_reply = IP(src=ip_dst, dst=ip_src) / ICMP(type=0, id=id, seq=seq)
    send(echo_reply, verbose=False)
    log_packet(f"Sent ICMP Echo Reply from {ip_dst} to {ip_src} (id={id}, seq={seq})", logfile)

if __name__ == "__main__":
    ip1 = "192.168.115.43"  # Spoofed source - the device i pretend to be
    ip2 = "192.168.115.31"  # Spoofed destination - my victim

    for i in range(1, 5):  # Simulate 4 ping attempts
        simulate_ping(ip1, ip2, id=1234, seq=i)
        time.sleep(1)