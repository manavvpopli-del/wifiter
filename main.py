import os
import sys
import time
import random

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
    print(CYAN + BOLD + "\n[+] Wi-Fi mühiti skan edilir..." + RESET)
    time.sleep(1)
    
    networks = [
        {"ssid": "BakuNet_Fiber_5G", "bssid": "00:1A:2B:3C:4D:5E", "signal": "-45 dBm", "channel": "6", "key": "Baku2026_Secure#"},
        {"ssid": "Aztelekom_WiFi_99", "bssid": "11:22:33:44:55:66", "signal": "-58 dBm", "channel": "11", "key": "aztelekom7788"},
        {"ssid": "Nar_Home_Net", "bssid": "CC:DD:EE:FF:00:11", "signal": "-62 dBm", "channel": "1", "key": "narhome2025!"},
        {"ssid": "Bakcell_Hotspot", "bssid": "AA:BB:CC:DD:EE:FF", "signal": "-50 dBm", "channel": "3", "key": "bakcell9900"},
        {"ssid": "Xirdalan_City_Net", "bssid": "55:44:33:22:11:00", "signal": "-70 dBm", "channel": "9", "key": "xirdalanaz123"},
        {"ssid": "Gence_Express_WiFi", "bssid": "77:88:99:AA:BB:CC", "signal": "-65 dBm", "channel": "2", "key": "gencepasha2026"},
        {"ssid": "SuperOnline_Guest", "bssid": "EE:FF:AA:BB:CC:DD", "signal": "-75 dBm", "channel": "8", "key": "superonline99"},
        {"ssid": "Office_Secure_AP", "bssid": "12:34:56:78:9A:BC", "signal": "-42 dBm", "channel": "4", "key": "EnterpriseSecure#1"},
        {"ssid": "Private_Network_X", "bssid": "DE:AD:BE:EF:01:23", "signal": "-80 dBm", "channel": "13", "key": "secretpassw0rd"},
        {"ssid": "MegaNet_Broadband", "bssid": "98:76:54:32:10:FE", "signal": "-55 dBm", "channel": "7", "key": "meganetfiber88"}
    ]
    
    print(GREEN + BOLD + "\n[✔] Skan tamamlandı. Yaxınlıqdakı şəbəkələr aşkar olundu:" + RESET)
    print("=" * 75)
    print(f"{'No':<4} | {'SSID':<22} | {'BSSID':<18} | {'Siqnal':<10} | {'Kanal':<5}")
    print("=" * 75)
    
    for idx, net in enumerate(networks, 1):
        print(f"{idx:<4} | {net['ssid']:<22} | {net['bssid']:<18} | {net['signal']:<10} | {net['channel']:<5}")
    print("=" * 75)
    
    try:
        choice = int(input("\n" + YELLOW + "Hədəf şəbəkə nömrəsini daxil edin (1-10): " + RESET))
        if 1 <= choice <= 10:
            selected = networks[choice - 1]
            print(CYAN + f"\n[+] Hədəf seçildi: {selected['ssid']} ({selected['bssid']})" + RESET)
            print(RED + "[+] Paketlər ələ keçirilir və Handshake təhlil edilir..." + RESET)
            
            for i in range(101):
                sys.stdout.write(f"\r{YELLOW}[Üstünlük əldə olunur]: {i}% [{'#' * (i // 5)}{'-' * (20 - i // 5)}]{RESET}")
                sys.stdout.flush()
                time.sleep(0.04)
            print("\n")
            
            print(GREEN + BOLD + "[✔] Uğurlu əməliyyat! Şifrə şifrə açılış bazasından tapıldı." + RESET)
            print(MAGENTA + BOLD + f"[*] Şəbəkə Şifrəsi: {selected['key']}" + RESET)
        else:
            print(RED + "[-] Yanlış nömrə daxil edildi!" + RESET)
    except ValueError:
        print(RED + "[-] Xəta: Zəhmət olmasa rəqəm daxil edin." + RESET)

if __name__ == '__main__':
    main()
