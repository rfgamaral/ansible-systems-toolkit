#!/bin/vbash

# Forked and adapted from original script:
# https://kriegsman.io/2016/10/configuring-a-ubiquiti-edgerouter-to-automatically-update-static-route-for-kpn-iptv-platform/

OLD_ROUTER_IP=\$(cat /config/config.boot | grep 'table 105' -A2 | grep 'next-hop' | awk '{print \$2}')

NEW_ROUTER_IP=\$(cat /var/run/dhclient_eth9.105_lease | grep 'new_routers' | awk -F= '{print \$2}' | tr -d \')

if [ "\$OLD_ROUTER_IP" = "\$NEW_ROUTER_IP" ]; then
   exit 0
fi

source /opt/vyatta/etc/functions/script-template

configure
delete protocols static table 105 route 0.0.0.0/0 next-hop \$OLD_ROUTER_IP
set protocols static table 105 route 0.0.0.0/0 next-hop \$NEW_ROUTER_IP
set protocols static table 105 route 0.0.0.0/0 next-hop \$NEW_ROUTER_IP description "IPTV subnet routing"
commit
save
exit
