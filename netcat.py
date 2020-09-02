#!/usr/bin/env python

from scapy.all import sendp, TCP, IP



print(sendp(TCP(dport=9001) / IP(dst="127.0.0.1")))

import socket
from scapy.all import StreamSocket, Raw

s = socket.socket()
s.connect(("127.0.0.1", 9001))

ss = StreamSocket(s, Raw)
ss.sr1(Raw("Hello and welcome.\nYou can start to send some command lines\nTry to send \"help\" if you need it and \"stop\" to quit the connection.\n"), timeout=0.5)
boole=0
while (boole==0):
    txt=input("Try Something:\n")
    test=ss.sr1(Raw(txt+"\n"), timeout=0.5)
    if (txt=="stop"):
        boole=1