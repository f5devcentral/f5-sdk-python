#!/bin/bash

adminUsername='${admin_username}'
adminPassword='${admin_password}'

# disable 1nic auto configuration
/usr/bin/setdb provision.1nicautoconfig disable

# wait for mcpd ready before attempting any tmsh command(s)
source /usr/lib/bigstart/bigip-ready-functions
wait_bigip_ready

# create external VLAN, self IP
tmsh create net vlan external interfaces replace-all-with { 1.1 }
tmsh create net self externalSelf address ${external_self} vlan external allow-service default

# create user
tmsh create auth user $${adminUsername} password $${adminPassword} shell bash partition-access replace-all-with { all-partitions { role admin } }

# create ltm pool and virtual server
tmsh create ltm pool http_pool1
tmsh create ltm virtual http_virtual1 destination 10.0.1.10:80 ip-protocol tcp profiles add { http tcp } pool http_pool1

# create gtm datacenter, server, pool
tmsh create gtm datacenter dns_datacenter1 dns_datacenter2
tmsh create gtm server gtm_server1 devices add { sdkbigipvm0 { addresses add { 10.10.90.1 } } } datacenter dns_datacenter1 virtual-server-discovery enabled
tmsh create gtm create gtm pool a gtm_pool1 members add { gtm_server1:/Common/http_virtual1 }

# save config
tmsh save sys config
