#!/bin/sh

_tor_uid=109
_i2p_uid=108

_tor_port=9040
_i2p_port=7679
_i2p_range="10.18.0.0/16"
_dns_port=5354

### flush iptables
iptables -F
iptables -t nat -F

### set iptables *nat
iptables -t nat -A OUTPUT -m owner --uid-owner $_tor_uid -j RETURN
iptables -t nat -A OUTPUT -m owner --uid-owner $_i2p_uid -j RETURN
iptables -t nat -A OUTPUT -p udp --dport 53 -j REDIRECT --to-ports $_dns_port

#allow clearnet access for hosts in $_non_tor
for _clearnet in 127.0.0.0/9 127.128.0.0/10; do
   iptables -t nat -A OUTPUT -d $_clearnet -j RETURN
done

#redirect all other output to i2p's TransPort
iptables -t nat -A OUTPUT -p tcp --syn -d $_i2p_range -j REDIRECT --to-ports $_i2p_port

#redirect all other output to Tor's TransPort
iptables -t nat -A OUTPUT -p tcp --syn -j REDIRECT --to-ports $_tor_port

### set iptables *filter
iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

#allow clearnet access for hosts in $_non_tor
for _clearnet in 127.0.0.0/8; do
   iptables -A OUTPUT -d $_clearnet -j ACCEPT
done

#allow only Tor output
iptables -A OUTPUT -m owner --uid-owner $_tor_uid -j ACCEPT
iptables -A OUTPUT -m owner --uid-owner $_i2p_uid -j ACCEPT
iptables -A OUTPUT -j REJECT

