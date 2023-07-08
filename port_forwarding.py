#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import subprocess
import argparse

if __name__ == '__main__':


    parser = argparse.ArgumentParser()
    # parser.add_argument('-si', '--src-ip', help='変換前のIPアドレス')
    parser.add_argument('-sp', '--src-port', help='変換前のポート')
    parser.add_argument('-di', '--dst-ip', help='変換後のIPアドレス')
    parser.add_argument('-dp', '--dst-port', help='変換後のポート')
    parser.add_argument('-d', '--delete',
                              action="store_true",
                              help='ルールを削除する場合に指定')

    args = parser.parse_args()    # 4. 引数を解析

    if(#(args.src_ip is None) or \
        (args.src_port is None) or \
       (args.dst_ip is None) or (args.dst_port is None) \
       ):
        print("必要な引数が指定されていません！\n")
        parser.print_help()
        sys.exit()

    mode = "-A"

    # 変数名を短くする
    # src_ip = args.src_ip
    src_port = args.src_port
    dst_ip = args.dst_ip
    dst_port = args.dst_port

    # チェイン名は固定
    CHAIN = 'MY_PORTFORWARDING'

    # ポートフォワーディングルールの作成or削除(FORWARD系)
    if(not args.delete):
        subprocess.call(["iptables", "-N", CHAIN])
    else:
        mode = "-D"
    
    subprocess.call(["iptables", mode, "FORWARD", "-j", CHAIN])
    subprocess.call(["iptables", mode, CHAIN, "-p", "tcp", "-d", dst_ip,
                        "--dport", dst_port, "-j", "ACCEPT"])
    subprocess.call(["iptables", mode, CHAIN, "-p", "tcp", r"!", "--syn", "-m", "state",
                        "--state", "ESTABLISHED", "--sport", dst_port, "-s", dst_ip,
                        "-j", "ACCEPT"])

    if(args.delete):
        subprocess.call(["iptables", "-X", CHAIN])

    # ポートフォワーディングルールの作成or削除(NAT系)
    if(not args.delete):
        subprocess.call(["iptables", "-t", "nat", "-N", CHAIN])
    
    subprocess.call(["iptables", "-t", "nat", mode, "PREROUTING", "-j", CHAIN])
    subprocess.call(["iptables", "-t", "nat", mode, "OUTPUT", "-j", CHAIN])
    subprocess.call(["iptables", "-t", "nat", mode, CHAIN, "-p", "tcp", 
                     "--dport", src_port, "-j", "DNAT", 
                     "--to-destination", "{}:{}".format(dst_ip, dst_port)])
    subprocess.call(["iptables", "-t", "nat", mode, "POSTROUTING", "-p", "tcp", 
                    "-d", dst_ip, "--dport", dst_port, "-j", "MASQUERADE"])

    if(args.delete):
        subprocess.call(["iptables", "-t", "nat", "-X", CHAIN])
