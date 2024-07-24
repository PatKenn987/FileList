import scapy.all as scapy
import argparse

#Goal - Discover clients on the network

# 1. Create arp request directed to broadcast MAC asking for IP
    #a) Create an ARP request to ask who has a target
    #b) Set the destination MAC to broadcast MAC address
# 2. Send packet and receive a response
# 3. Parse the response
# 4. Print the result

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="ip_range", help="Range of IP address's to scan")

    (options) = parser.parse_args()

    #Ensure that the user provided a command line input
    if not options.ip_range:
        parser.error("[-] Please specify an IP address of IP address range, use --help for more info")

    return options
def scan(ip):
    #Create an ARP request packet for a specific IP
    arp_request = scapy.ARP(pdst=ip)
    #Create an Ethernet broadcast request packet
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    #Concatenate the packets together
    arp_request_broadcast = broadcast/arp_request
    #Transmit the packet and receive a response
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    #Create a list
    clients_list=[]
    #Parse the data returned and store client_list
    for element in answered_list:
        client_dict = {"ip":element[1].psrc, "mac":element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list

def print_result(result_list):
    print("IP \t\t\tMAC Address\n-----------------------------------------------")
    for client in result_list:
        print(client["ip"] + "\t\t" + client["mac"])

ip_input = get_arguments()

scan_result = scan(ip_input.ip_range)
print_result(scan_result)


*****************************************

#This is the program that I wrote in section 4 of the course with a bunch of debug comments.  I want to
#clean up the main program so I am going to copy this here.


#!/usr/bin/env python

import scapy.all as scapy


#Goal - Discover clients on the network

# 1. Create arp request directed to broadcast MAC asking for IP
    #a) Create an ARP request to ask who has a target
    #b) Set the destination MAC to broadcast MAC address
# 2. Send packet and receive a response
# 3. Parse the response
# 4. Print the result
def scan(ip):

    #Create an ARP request packet for a specific IP
    arp_request = scapy.ARP(pdst=ip)
    #Debug - arp_request.show()
    #Debug - scapy.ls(scapy.ARP)
    #Debug - print(arp_request.summary())

    #Create an Ethernet broadcast request packet
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")

    #Debug - print(broadcast.summary())
    #Debug - scapy.ls(scapy.Ether())
    #Debug - broadcast.show()

    #Concatenate the packets together
    arp_request_broadcast = broadcast/arp_request

    #Debug - print(arp_request_broadcast.summary())
    #Debug - arp_request_broadcast.show()

    #Transmit the packet and receive a response
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    #Create a list
    clients_list=[]

    #Parse the response

    for element in answered_list:
        client_dict = {"ip":element[1].psrc, "mac":element[1].hwsrc}
        clients_list.append(client_dict)
        #Debug - print(element[1].psrc+"\t\t"+element[1].hwsrc)

    return  clients_list

    #Debug - answered_list, unanswered_list = scapy.srp(arp_request_broadcast, timeout=1)
    #Debug - print(answered_list.summary())
    #Debug - print(unanswered_list.summary())


    #Parse the answered_list and retrieve the relevant data.
    #scapy.ls(scapy.ARP)


def print_result(result_list):
    print("IP \t\t\tMAC Address\n-----------------------------------------------")
    for client in result_list:
        print(client["ip"] + "\t\t" + client["mac"])


scan_result = scan("192.168.1.1/24")
print_result(scan_result)
