#!/usr/bin/env python3
#
# Python3 script to post Zabbix alerts to Squadcast.
# This script has been tested with Python 3.6.
#

import sys
import os
import json
import urllib.request

def print_usage():
    """Print the script usage"""
    print("Usage:\n  sq-zabbix <url> <subject> <data>")

def form_payload(data = "", subject = ""):
    """Forms the python representation of the data payload to be sent from the passed configuration"""
    lines = data.split("\n")
    payload_rep = {"subject" : subject}
    for line in lines:
        parts = line.split(":", 1)
        if len(parts) == 1:
            continue
        payload_rep[parts[0].strip()] = parts[1].strip()
    return payload_rep

def post_to_url(url, payload):
    """Posts the formed payload as json to the passed url"""
    try:
        req = urllib.request.Request(url, data=bytes(json.dumps(payload), "utf-8"))
        req.add_header("Content-Type", "application/json")
        resp = urllib.request.urlopen(req)
        if resp.status > 299:
           print("[sq-zabbix] Request failed with status code %s : %s" % (resp.status, resp.read()))
    except urllib.request.URLError as e:
        if e.code >= 400 and e.code < 500:
            print("[sq-zabbix] Some error occured while processing the event")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print_usage()
        exit(2)
    url = sys.argv[1]
    subject = sys.argv[2]
    data = sys.argv[3]
    print("Sending data to squadcast")
    post_to_url(url, form_payload(data, subject))
    print("Done.")