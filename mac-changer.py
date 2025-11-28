#!/usr/bin/env python3

# Script to change the MAC address of an interface (linux) by RSKR

# ----------------------------------------
#               IMPORTS
# ----------------------------------------
# Built-In
import os
import sys
import re
import random
import argparse
import subprocess

# ----------------------------------------
#               FUNCTIONS 
# ----------------------------------------
def root_permission() -> bool:
    return os.getuid() == 0

def is_valid_file(file_path: str) -> bool:
    return os.path.isfile(os.path.abspath(file_path))

def is_valid_mac(mac_address: str) -> bool:
    pattern = re.compile(r'''
        ^(
            ([0-9A-Fa-f]{2}[:]){5}[0-9A-Fa-f]{2} |     
            ([0-9A-Fa-f]{4}\.){2}[0-9A-Fa-f]{4}         
        )$
    ''', re.VERBOSE)
    return bool(pattern.match(mac_address))

def get_current_mac(interface):
    try:
        output = subprocess.check_output(['ip', 'link', 'show', interface], text=True)
        mac_match = re.search(r'link/ether\s([0-9a-fA-F:]{17})', output)
        if mac_match:
            return mac_match.group(1)
    except subprocess.CalledProcessError:
        return None
    
    return None

def change_mac(mac_address, interface):
    mac_address = mac_address.strip()

    try:
        subprocess.run(['ip', 'link', 'set', 'dev', interface, 'down'], check=True)
        subprocess.run(['ip', 'link', 'set', 'dev', interface, 'address', mac_address], check=True)
        subprocess.run(['ip', 'link', 'set', 'dev', interface, 'up'], check=True)

        current_mac = get_current_mac(interface)
        if current_mac and current_mac.lower() == mac_address.lower():
            print(f"[+] MAC address successfully changed to {current_mac} on {interface}")
        else:
            print(f"[-] MAC change failed. Current MAC: {current_mac}")
    except subprocess.CalledProcessError as e:
        print(f"[-] Error changing MAC address: {e}")

def arguments():
    parser = argparse.ArgumentParser(description='Python script to change MAC address (Linux)',
        epilog=f"""
        Change MAC address manually:
            sudo python3 {sys.argv[0]} -i eth0 -m AA:BB:CC:DD:EE:FF
        
        Random selection:
            sudo python3 {sys.argv[0]} -i eth0 -r ./mac_list.txt
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-i', '--interface', help='Destination interface to change MAC address.', type=str, required=True)

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-m', '--mac', help='New MAC address', type=str)
    group.add_argument('-r', '--random', help='MAC address file for random selection', type=str)
    return parser.parse_args()

# ----------------------------------------
#               MAIN
# ----------------------------------------
def main():
    if not root_permission():
        print('[-] Root permission is required')
        sys.exit(1)

    args = arguments()

    # MAC comes from parameter
    if args.mac:
        mac_address = args.mac.strip()

    # MAC comes from file
    elif args.random:
        if not is_valid_file(args.random):
            print(f"[-] Invalid file: {args.random}")
            sys.exit(1)

        try:
            with open(args.random, 'r') as file:
                mac_address = random.choice(file.readlines()).strip()
        except FileNotFoundError:
            print(f"[-] File not found: {args.random}")
            sys.exit(1)
        except Exception as e:
            print(f"[-] Error reading file {args.random}: {e}")
            sys.exit(1)

    # Validate MAC format
    if not is_valid_mac(mac_address):
        print(f"[-] Invalid MAC address: {mac_address}")
        sys.exit(1)

    change_mac(mac_address, args.interface.strip())

# ----------------------------------------
#               ENTRY POINT
# ----------------------------------------
if __name__ == '__main__':
    main()