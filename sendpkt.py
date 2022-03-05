#!/usr/bin/env python3
from scapy.all import *
import logging, threading, time, subprocess

sendpkt = Ether(src = src, dst = dst, type = 0x0800) / IP(src = srcip, dst = dstip) / TCP() / Raw("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
sendiface = 'enp179s0f0'
interfaces = ['enp179s0f0', 'enp179s0f1']
procs = []

class color:
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	RED = '\033[91m'
	YELLOW = '\033[93m'
	WHITE = '\033[97m'
	GRAY = '\033[90m'
	BOLD = '\033[1m'
	BOLDEND = '\033[21m'
	END = '\033[0m'

verbose = len(sys.argv) > 1 and sys.argv[1] in ['verbose', '-verbose', '-v', '--verbose']

for iface in interfaces:
	if os.path.isfile('/tmp/{}.pcap'.format(iface)):
		os.remove('/tmp/{}.pcap'.format(iface))
	procs.append(subprocess.Popen(['tcpdump', '-i', iface, '-w', '/tmp/{}.pcap'.format(iface)], stderr = subprocess.DEVNULL))
time.sleep(1)

src = '0a:0b:00:00:00:01'
dst = '0a:0b:00:00:00:02'
srcip = '10.0.0.1'
dstip = '10.0.0.2'

s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
s.bind((sendiface, 0))
s.send(bytes(sendpkt))
print('Sending at', sendiface)

time.sleep(1)
for proc in procs:
	proc.send_signal(2) #sigint
time.sleep(1)

for proc in procs:
	proc.kill()

for iface in interfaces:
	print(color.BOLD + color.YELLOW + '# Interface ' + iface + '' + color.END)
	pkts = rdpcap('/tmp/{}.pcap'.format(iface))
	if len(pkts) == 0:
		print('No packets')
	else:
		i = 1
		for pkt in pkts:
			print(color.GREEN + 'Packet {}: '.format(i) + color.END)
			if verbose:
				pkt.show()
			else:
				hexdump(pkt)
			print()
			i += 1
