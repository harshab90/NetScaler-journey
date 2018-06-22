#!/usr/local/bin/python3

import os
import requests
import ipaddress
import argparse
import pprint

def valid_ip(address):
    try:
        ipaddress.ip_network(address)
        return True
    except:
        print ('\n'"Try option -h to know more about the usage. Also check and make sure you enter the correct IP Addr."'\n')
        exit()
        return False

def Diff(a, b):
    return (list(set(a) - set(b)))

def Request(ip,vserver):
    url = 'http://{}:{}@{}/nitro/v1/config/{}'.format(user,password,ip,vserver)
    header = {"Content-Type":"application/vnd.com.citrix.netscaler.config+json"}
    r = requests.get(url, headers=header)
    x = r.json()
    global data
    data = []
    for i in range(0, len(x[vserver])):
        y = (x[vserver][i]['name'], x[vserver][i]['curstate'])
        data.append(y)

parser = argparse.ArgumentParser()
parser.add_argument("--P", help="Please enter the Primary NetScaler IP")
parser.add_argument("--S", help="Please enter the Secondary NetScaler IP")
parser.add_argument("--vserver", help="Please specify the vserver ex: csvserver / lbvserver")

args = parser.parse_args()
ip = args.P
ip2 = args.S
vserver = args.vserver

user = os.environ.get('USR')
password = os.environ.get('PAS')

def IPValidation(ip,ip2):
    global ns1
    global ns2
    ns1 = []
    ns2 = []
    try:
        ipaddress.ip_network(ip)
        Request(ip, vserver)
        ns1 = data
#        print (ns1)
    except:
        print('\n'"It is mandatory to at least enter Primary IP address"'\n')
        pass
    try:
        ipaddress.ip_network(ip2)
        Request(ip2, vserver)
        ns2 = data
#        print (ns2)
    except:
        print('\n'"Try option -h to know more about the usage. Also check and make sure you enter the correct IP Addr."'\n')
        pass
IPValidation(ip,ip2)


out = Diff (ns1, ns2)
if out == []:
    try:
        out2 = Diff(ns2, ns1)
        if out2 == []:
            print ("The NetScaler Vserver's are same and are in SYNC / Please check option -h to see if you are using the script properly"'\n')
        else:
            print("Here are the vserver which are configured/not in SYNC", '\n''\t')
            print(pprint.pprint(out2))
    except:
        pass
else:
    print ("Here are the vserver which are configured/not in SYNC",'\n''\t')
    print (pprint.pprint(out))
