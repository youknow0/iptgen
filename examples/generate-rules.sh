#!/bin/bash
# example script for rule creation

IPTGEN="../iptgen.py"

# this generates the rules for the filter table
cat <<PROLOG
*filter
-P FORWARD DROP
-P INPUT DROP
-P OUTPUT ACCEPT

# allow everything on the loopback interface
-A INPUT -i lo -j ACCEPT

# deny everything that looks like loopback traffic, but is not on the loopback interface
-A INPUT ! -i lo -d 127.0.0.0/8 -j REJECT

# accept all established inbound connections
-A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
-A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT
-A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# allow icmp from everywhere
-A INPUT -p icmp -j ACCEPT

PROLOG

$IPTGEN --generate "rules" --config config-filter.py

cat <<INTERLOG
COMMIT
*nat
INTERLOG

$IPTGEN --generate "rules" --config config-nat.py

cat <<POSTLOG
COMMIT
POSTLOG

