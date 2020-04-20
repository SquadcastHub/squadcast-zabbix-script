#!/usr/bin/env python3
#
# Python3 script to post Zabbix alerts to Squadcast.
# This script has been tested with Python 3.6.
#

import sys
import os
import json
import ssl
import urllib.request
import logging

logger = logging.getLogger('sq-zabbix.py')
hdlr = logging.FileHandler('/tmp/sq-zabbix-py.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.WARNING)

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
        gcontext = ssl.SSLContext()
        req = urllib.request.Request(url, data=bytes(json.dumps(payload), "utf-8"))
        req.add_header("Content-Type", "application/json")
        resp = urllib.request.urlopen(req,context=gcontext)
        if resp.status > 299:
           logger.error("[sq-zabbix] Request failed with status code %s : %s" % (resp.status, resp.read()))
    except urllib.request.HTTPError as e:
        if e.code >= 400 and e.code < 500:
            logger.error("[sq-zabbix] Some error occured while processing the event")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print_usage()
        exit(2)
    url = sys.argv[1]
    subject = sys.argv[2]
    data = sys.argv[3]
    logger.error("[sq-zabbix] url:{}".format(url))
    logger.error("[sq-zabbix] subject:{}".format(subject))
    logger.error("[sq-zabbix] data:{}".format(data))
    print("Sending data to squadcast")
    print(form_payload(data, subject))
    post_to_url(url, form_payload(data, subject))
    print("Done.")
