#!/usr/bin/env python3
"""Offline Wi-Fi security simulator. No wireless scanning or attacks are performed."""

from __future__ import annotations

import argparse
import os
import sys
import time


NETWORKS = [
    {"ssid": "HomeNetwork_5G", "bssid": "02:5A:11:00:00:01", "channel": 44, "signal": 92, "band": "5 GHz", "security": "WPA2-Personal", "key": "FICTIONAL-KEY-0001"},
    {"ssid": "TPLink_A47C", "bssid": "02:5A:11:00:00:02", "channel": 6, "signal": 84, "band": "2.4 GHz", "security": "WPA2-Personal", "key": "FICTIONAL-KEY-0002"},
    {"ssid": "ASUS_2.4GHz", "bssid": "02:5A:11:00:00:03", "channel": 11, "signal": 77, "band": "2.4 GHz", "security": "WPA3-Personal", "key": "FICTIONAL-KEY-0003"},
    {"ssid": "NETGEAR_EXT", "bssid": "02:5A:11:00:00:04", "channel": 36, "signal": 69, "band": "5 GHz", "security": "WPA2-Personal", "key": "FICTIONAL-KEY-0004"},
    {"ssid": "DIRECT-8C-HP-Office", "bssid": "02:5A:11:00:00:05", "channel": 1, "signal": 61, "band": "2.4 GHz", "security": "WPA2-Personal", "key": "FICTIONAL-KEY-0005"},
    {"ssid": "Apartment_WiFi", "bssid": "02:5A:11:00:00:06", "channel": 9, "signal": 55, "band": "2.4 GHz", "security": "WPA2-Personal", "key": "FICTIONAL-KEY-0006"},
    {"ssid": "Home-Guest", "bssid": "02:5A:11:00:00:07", "channel": 40, "signal": 48, "band": "5 GHz", "security": "WPA2-Personal", "key": "FICTIONAL-KEY-0007"},
    {"ssid": "Router_5G_91B2", "bssid": "02:5A:11:00:00:08", "channel": 48, "signal": 42, "band": "5 GHz", "security": "WPA3-Personal", "key": "FICTIONAL-KEY-0008"},
    {"ssid": "Pixel_Hotspot", "bssid": "02:5A:11:00:00:09", "channel": 6, "signal": 35, "band": "2.4 GHz", "security": "WPA2-Personal", "key": "FICTIONAL-KEY-0009"},
    {"ssid": "Linksys_2G", "bssid": "02:5A:11:00:00:0A", "channel": 3, "signal": 28, "band": "2.4 GHz", "security": "WPA2-Personal", "key": "FICTIONAL-KEY-0010"},
]


def paint(text: str, code: str) -> str:
    if not sys.stdout.isatty() or os.environ.get("NO_COLOR"):
        return text
    return f"\033[{code}m{text}\033[0m"


def animate_dragon(delay: float) -> None:
    for flame in (".", "..", "...", "🔥", "🔥🔥", "🔥🔥🔥"):
        sys.stdout.write(paint(f"\r  🐉  {flame:<6}  SCANNING THE SIMULATED AIRWAVES", "95"))
        sys.stdout.flush()
        time.sleep(delay)
    print()


def show_banner() -> None:
    banner = [
        "  ╔══════════════════════════════════════════════════════════════════════╗",
        "  ║   /\\_/\\        DRAGON WI-FI SECURITY LAB                     ║",
        "  ║  ( o.o )        OFFLINE SIMULATION • NO RADIO ACTIONS            ║",
        "  ║   > ^ <         FICTIONAL NETWORKS AND KEYS                      ║",
        "  ╚══════════════════════════════════════════════════════════════════════╝",
    ]
    for line in banner:
        print(paint(line, "96"))


def show_networks() -> None:
    print(paint(f"\n  {'#':>2} {'SSID':<23} {'BSSID':<19} {'CH':>4} {'SIGNAL':>8} {'BAND':<10} {'SECURITY':<20}", "97;1"))
    print(paint(f"  {'--':>2} {'─' * 23} {'─' * 19} {'─' * 4} {'─' * 8} {'─' * 10} {'─' * 20}", "90"))
    for number, network in enumerate(NETWORKS, start=1):
        signal = network["signal"]
        signal_color = "92" if signal >= 70 else "93" if signal >= 40 else "91"
        row = (
            paint(f"  {number:>2} ", "95;1")
            + paint(f"{network['ssid']:<23} ", "96")
            + paint(f"{network['bssid']:<19} ", "90")
            + paint(f"{network['channel']:>4} ", "37")
            + paint(f"{signal:>7}% ", signal_color)
            + paint(f"{network['band']:<10} ", "94")
            + paint(f"{network['security']:<20}", "93")
        )
        print(row)
    print(paint(f"\n  {len(NETWORKS)} fictional access points are loaded.\n", "92;1"))


def simulate_attack(number: int, network: dict[str, object], delay: float) -> None:
    print(paint(f"\n  Target selected: [{number}] {network['ssid']}", "96;1"))
    print(paint("  Starting a pretend handshake capture...", "36"))
    for percent in (12, 29, 47, 68, 86, 100):
        filled = percent // 5
        bar = "█" * filled + "░" * (20 - filled)
        sys.stdout.write(paint(f"\r  [{bar}] {percent:3d}%  Simulated process", "92"))
        sys.stdout.flush()
        time.sleep(delay)
    print()
    print(paint("  Pretend attack complete.", "92;1"))
    print(paint(f"  Fictional key: {network['key']}", "93;1"))
    print(paint("  This key is fabricated; no real network or password was accessed.\n", "90"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Offline Wi-Fi security simulation; no real wireless activity.")
    parser.add_argument("--no-animation", action="store_true", help="Skip the animated intro")
    parser.add_argument("--fast", action="store_true", help="Shorten animation delays")
    args = parser.parse_args()
    delay = 0.035 if args.fast else 0.14

    if not args.no_animation:
        animate_dragon(delay)
    show_banner()
    show_networks()

    while True:
        try:
            choice = input(f"  Enter a number (1-{len(NETWORKS)}) to run the simulation, or Q to quit: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Session ended. No Wi-Fi activity was performed.")
            return 0
        if choice.lower() == "q":
            break
        if not choice.isdigit() or not 1 <= int(choice) <= len(NETWORKS):
            print(paint(f"  Choose a number from 1 to {len(NETWORKS)}, or Q.\n", "91"))
            continue
        number = int(choice)
        simulate_attack(number, NETWORKS[number - 1], delay)

    print(paint("  Session ended. No Wi-Fi activity was performed.", "36"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
