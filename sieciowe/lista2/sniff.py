from scapy.all import sniff

def sniff_icmp_reply(filter_ip):
    sniff(filter=f"icmp and host {filter_ip}", count=1, prn=lambda x: x.summary())