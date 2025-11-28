# Mac Changer (Linux)
A simple and functional utility written in Python that allows you to change the MAC address of a network interface on Linux systems.
The script supports both manual MAC address changes and random selection from a file of predefined addresses.

Developed by **RSKR**

---
## Characteristics
- Change the MAC address of any network interface in Linux.
- Allows you to:
    - Set a MAC address manually.
    - Select a MAC address randomly from a file.
- Validate the MAC address format (IEEE 802 standard).

## Requirements
- Python 3.x
- Linux with the `ip` command available
- Root privileges

## Clone this repository
``` shell
git clone https://github.com/0RSKR0/Mac-Changer.git
cd Mac-Changer
```

## Usage
Change the MAC address manually:
```shell
sudo python3 mac_changer.py -i eth0 -m AA:BB:CC:DD:EE:FF
```

Select a random MAC address from a file:
``` shell
sudo python3 mac_changer.py -i eth0 -r ./mac_list.txt
```
The file must contain one MAC address per line.

### Example mac_list.txt
You can provide a list of MAC addresses, and the script will randomly choose one when using the `-r` option.
Your mac_list.txt file may look like this:
``` shell
00:11:22:33:44:55
AA:BB:CC:DD:EE:FF
DE:AD:BE:EF:12:34
02:1A:3C:4B:5D:6F
10:9A:22:BC:7F:81
```
Make sure each MAC address appears on its own line and follows a valid MAC format.

## License
This project is licensed under the MIT License.

You are free to use, modify, and distribute this software as long as the terms of the MIT license are respected.
See the **[MIT LICENSE](LICENSE.md)** file for full details.

## Disclaimer
This tool is meant for **educational and legal security testing purposes only**.
Use it only on systems you own or have permission to test.