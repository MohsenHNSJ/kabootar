#!/usr/bin/env python3
import argparse


def cmd_dns_bridge_server():
    from app.dns_bridge import run_dns_bridge_server

    run_dns_bridge_server()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("command", choices=["dns-bridge-server"])
    args, _ = p.parse_known_args()

    if args.command == "dns-bridge-server":
        cmd_dns_bridge_server()


if __name__ == "__main__":
    main()
