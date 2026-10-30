import os
import sys
import time
import random

# ANSI Color Codes
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
MAGENTA = '\033[95m'
RESET = '\033[0m'
BOLD = '\033[1m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def animate_dragon():
    dragon_frames = [
        """
              ,
            / \
           |   |
           |   |  WIFITER v2.4 - Advanced Wi-Fi Security Suite
          === = ===
          """,
        """
             / \
            /   \
           |  O  |  WIFITER v2.4 - Advanced Wi-Fi Security Suite
           |     |
          === = ===
          """,
        """
            /   \
           /  _  \
          |  (O)  | WIFITER v2.4 - Advanced Wi-Fi Security Suite
          |   ~   |
         ===  =  ===
         (===   ===)
          """
    ]
    for _ in range(2):
        for frame in dragon_frames:
            clear_screen()
            print(MAGENTA + BOLD + frame + RESET)
            time.sleep(0.3)

def main():
    animate_dragon()
    print(CYAN + BOLD + "\n[+] Scanning Wi-Fi environment for active access points..." + RESET)
    time.sleep(1.5)
    
    networks = [
        {"ssid": "Home_Fiber_5G", "bssid": "00:1A:2B:3C:4D:5E", "signal": "-45 dBm", "channel": "6", "key": "89342019"},
        {"ssid": "Netgear_Secure_99", "bssid": "11:22:33:44:55:66", "signal": "-58 dBm", "channel": "11", "key": "283292892"},
        {"ssid": "TP-Link_Guest_Zone", "bssid": "CC:DD:EE:FF:00:11", "signal": "-62 dBm", "channel": "1", "key": "99401283"},
        {"ssid": "ASUS_Gaming_Network", "bssid": "AA:BB:CC:DD:EE:FF", "signal": "-50 dBm", "channel": "3", "key": "55019284"},
        {"ssid": "Office_Private_AP", "bssid": "55:44:33:22:11:00", "signal": "-70 dBm", "channel": "9", "key": "10492857"},
        {"ssid": "Express_WiFi_Router", "bssid": "77:88:99:AA:BB:CC", "signal": "-65 dBm", "channel": "2", "key": "73820194"},
        {"ssid": "Linksys_HighSpeed", "bssid": "EE:FF:AA:BB:CC:DD", "signal": "-75 dBm", "channel": "8", "key": "48201938"},
        {"ssid": "Enterprise_Wireless", "bssid": "12:34:56:78:9A:BC", "signal": "-42 dBm", "channel": "4", "key": "62910482"},
        {"ssid": "Private_Network_X", "bssid": "DE:AD:BE:EF:01:23", "signal": "-80 dBm", "channel": "13", "key": "39102847"},
        {"ssid": "Broadband_Access_Point", "bssid": "98:76:54:32:10:FE", "signal": "-55 dBm", "channel": "7", "key": "81029384"}
    ]
    
    print(GREEN + BOLD + "\n[✔] Scan complete. Found nearby wireless networks:" + RESET)
    print("=" * 75)
    print(f"{'No':<4} | {'SSID':<22} | {'BSSID':<18} | {'Signal':<10} | {'Channel':<5}")
    print("=" * 75)
    
    for idx, net in enumerate(networks, 1):
        print(f"{idx:<4} | {net['ssid']:<22} | {net['bssid']:<18} | {net['signal']:<10} | {net['channel']:<5}")
    print("=" * 75)
    
    try:
        choice = int(input("\n" + YELLOW + "Select target network number (1-10): " + RESET))
        if 1 <= choice <= 10:
            selected = networks[choice - 1]
            print(CYAN + f"\n[+] Target selected: {selected['ssid']} ({selected['bssid']})" + RESET)
            print(RED + "[+] Initiating handshake capture and dictionary attack..." + RESET)
            
            total_duration = 15.0
            steps = 100
            delay = total_duration / steps
            
            for i in range(1, steps + 1):
                sys.stdout.write(f"\r{YELLOW}[Attack Progress]: {i}% [{'#' * (i // 5)}{'-' * (20 - i // 5)}]{RESET}")
                sys.stdout.flush()
                time.sleep(delay)
            print("\n")
            
            print(GREEN + BOLD + "[✔] Operation successful! Key retrieved from dictionary table." + RESET)
            print(MAGENTA + BOLD + f"[*] Network Key / Password: {selected['key']}" + RESET)
        else:
            print(RED + "[-] Invalid selection!" + RESET)
    except ValueError:
        print(RED + "[-] Error: Please enter a valid number." + RESET)

if __name__ == '__main__':
    main()
