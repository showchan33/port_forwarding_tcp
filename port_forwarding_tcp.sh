#!/bin/sh
set -eu

configure_iptables_filter() {
  iptables -"$MODE" FORWARD -j "$CHAIN"
  iptables -"$MODE" "$CHAIN" -p tcp -d "$DST_IP" --dport "$DST_PORT" -j ACCEPT
  iptables -"$MODE" "$CHAIN" \
    -p tcp ! --syn -m state --state ESTABLISHED \
    --sport "$DST_PORT" -s "$DST_IP" -j ACCEPT
}

configure_iptables_nat() {
  iptables -t nat -"$MODE" PREROUTING -j "$CHAIN"
  iptables -t nat -"$MODE" OUTPUT -j "$CHAIN"
  iptables -t nat -"$MODE" "$CHAIN" -p tcp \
    --dport "$SRC_PORT" -j DNAT \
    --to-destination "$DST_IP":"$DST_PORT"
  iptables -t nat -"$MODE" POSTROUTING -p tcp \
    -d "$DST_IP" --dport "$DST_PORT" -j MASQUERADE
}

ENVS="CHAIN SRC_PORT DST_IP DST_PORT"
for env in $ENVS; do
  eval value=\$${env}
done

if [ -n "${DELETE+x}" ] && [ ${DELETE} = "true" ]; then
  # Delete iptables settings
  MODE="D"

  configure_iptables_filter
  iptables -X "$CHAIN"

  configure_iptables_nat
  iptables -t nat -X "$CHAIN"
else
  # Add iptables settings
  MODE="A"

  iptables -N "$CHAIN"
  configure_iptables_filter

  iptables -t nat -N "$CHAIN"
  configure_iptables_nat
fi
