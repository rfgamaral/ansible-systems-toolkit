#!/usr/bin/env python

import argparse
import subprocess
import re
import hashlib

# Forked and adapted from original script:
# https://github.com/confirm/edgerouter-dnsmasq-updater

parser = argparse.ArgumentParser(description="Read all static DHCP mappings from EdgeOS and generate a 'dnsmasq' compatible hosts file.")
parser.add_argument('hosts_filename', help="The '/path/filename' to store the generated hosts file")

args = parser.parse_args()

config = subprocess.check_output(['cat', '/config/config.boot'])

static_mappings = re.findall('static-mapping ([^ ]+) \{\s+ip-address ([0-9.]+)[^\}]+\}', config, re.S)

static_mappings_aliases = {
    "RFA-DellLaptop": "BLACKDELL",
    "RFA-DesktopPC": "BLACKBOX",
    "SYN-DiskStation": "HYPERCUBE",
    "SYS-RaspberryPi-1": "POLYMERBOX",
}

hasher  = hashlib.md5('\n'.join([h + i for h, i in static_mappings]))
md5_new_config = hasher.hexdigest()

try:
    with file(args.hosts_filename, 'r') as f:
        md5_current_config = f.readline()[2:].strip()
except IOError:
    md5_current_config = None

if md5_current_config != md5_new_config:
    with file(args.hosts_filename, 'w') as hosts:
        hosts.write('# {md5}\n\n'.format(md5=md5_new_config))

        for hostname, ip in static_mappings:
            hosts.write('{ip:<15s} {hostname}'.format(ip=ip, hostname=hostname))

            try:
                hosts.write(' {alias}\n'.format(alias=static_mappings_aliases[hostname]))
            except:
                hosts.write('\n')

    subprocess.check_call(['pkill', '-HUP', 'dnsmasq'])
