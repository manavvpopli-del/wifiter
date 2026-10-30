#!/usr/bin/env python3
"""Read-only nearby Wi-Fi network scanner for Kali Linux."""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class Network:
    ssid: str
    bssid: str
    channel: str
    frequency_mhz: str
    signal: str
    signal_unit: str
    security: str
    in_use: bool = False


class ScanError(RuntimeError):
    pass


def run(command: list[str], timeout: int = 30) -> str:
    try:
        result = subprocess.run(
            command, check=False, capture_output=True, text=True, timeout=timeout
        )
    except FileNotFoundError as exc:
        raise ScanError(f"Komanda tapılmadı: {command[0]}") from exc
    except subprocess.TimeoutExpired as exc:
        raise ScanError("Skan vaxtı bitdi. Yenidən cəhd edin.") from exc
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise ScanError(detail or f"Komanda uğursuz oldu: {' '.join(command)}")
    return result.stdout


def split_nmcli_row(row: str) -> list[str]:
    """Split nmcli's escaped colon-separated output."""
    fields: list[str] = []
    current: list[str] = []
    escaped = False
    for char in row:
        if escaped:
            current.append(char)
            escaped = False
        elif char == "\\":
            escaped = True
        elif char == ":":
            fields.append("".join(current))
            current.clear()
        else:
            current.append(char)
    if escaped:
        current.append("\\")
    fields.append("".join(current))
    return fields


def scan_nmcli(interface: str | None, rescan: bool) -> list[Network]:
    command = [
        "nmcli", "--terse", "--escape", "yes", "--fields",
        "SSID,BSSID,CHAN,FREQ,RATE,SIGNAL,SECURITY,IN-USE", "device", "wifi", "list",
    ]
    if interface:
        command.extend(["ifname", interface])
    command.extend(["--rescan", "yes" if rescan else "no"])
    output = run(command)
    networks: list[Network] = []
    for line in output.splitlines():
        if not line.strip():
            continue
        fields = split_nmcli_row(line)
        if len(fields) < 8:
            continue
        ssid, bssid, channel, frequency, _rate, signal, security, in_use = fields[:8]
        networks.append(Network(
            ssid=ssid or "<gizli SSID>",
            bssid=bssid,
            channel=channel,
            frequency_mhz=re.sub(r"[^0-9.]", "", frequency),
            signal=signal,
            signal_unit="%",
            security=security or "Açıq",
            in_use=in_use.strip() == "*",
        ))
    return networks


def frequency_to_channel(freq: int) -> str:
    if freq == 2484:
        return "14"
    if 2412 <= freq <= 2472:
        return str((freq - 2407) // 5)
    if 5000 <= freq < 5925:
        return str((freq - 5000) // 5)
    if 5955 <= freq <= 7115:
        return str((freq - 5950) // 5)
    return "?"


def find_interface() -> str:
    output = run(["iw", "dev"])
    match = re.search(r"^\s*Interface\s+(\S+)", output, flags=re.MULTILINE)
    if not match:
        raise ScanError("Wi-Fi interfeysi tapılmadı. 'iw dev' nəticəsini yoxlayın.")
    return match.group(1)


def scan_iw(interface: str | None) -> list[Network]:
    device = interface or find_interface()
    output = run(["iw", "dev", device, "scan"], timeout=60)
    networks: list[Network] = []
    current: dict[str, str] | None = None

    def save() -> None:
        if current is None or not current.get("bssid"):
            return
        networks.append(Network(
            ssid=current.get("ssid") or "<gizli SSID>",
            bssid=current["bssid"],
            channel=current.get("channel", "?"),
            frequency_mhz=current.get("frequency", ""),
            signal=current.get("signal", ""),
            signal_unit="dBm",
            security=current.get("security", "Açıq"),
        ))

    for line in output.splitlines():
        match = re.match(r"BSS\s+([0-9a-fA-F:]{17})", line)
        if match:
            save()
            current = {"bssid": match.group(1).lower(), "security": "Açıq"}
            continue
        if current is None:
            continue
        stripped = line.strip()
        if stripped.startswith("freq:"):
            frequency = re.search(r"\d+", stripped)
            if frequency:
                current["frequency"] = frequency.group(0)
                current["channel"] = frequency_to_channel(int(frequency.group(0)))
        elif stripped.startswith("SSID:"):
            current["ssid"] = stripped.partition(":")[2].strip()
        elif stripped.startswith("signal:"):
            current["signal"] = stripped.partition(":")[2].strip().removesuffix(" dBm")
        elif stripped.startswith("DS Parameter set: channel"):
            channel = re.search(r"channel\s+(\d+)", stripped)
            if channel:
                current["channel"] = channel.group(1)
        elif stripped in {"RSN:", "WPA:", "WPA:"}:
            current["security"] = "WPA/WPA2/WPA3"
        elif stripped.startswith("capability:") and "Privacy" in stripped and current["security"] == "Açıq":
            current["security"] = "WEP və ya qorunan şəbəkə"
    save()
    return networks


def scan(interface: str | None, backend: str, rescan: bool) -> list[Network]:
    if backend in {"auto", "nmcli"} and shutil.which("nmcli"):
        try:
            return scan_nmcli(interface, rescan)
        except ScanError:
            if backend == "nmcli":
                raise
    elif backend == "nmcli":
        raise ScanError("nmcli tapılmadı. NetworkManager quraşdırın və ya --backend iw seçin.")
    if backend in {"auto", "iw"} and shutil.which("iw"):
        return scan_iw(interface)
    raise ScanError("Nə nmcli, nə də iw tapıldı. Kali-də NetworkManager və ya iw quraşdırın.")


def signal_bars(value: str, unit: str) -> str:
    try:
        raw = float(value)
        strength = raw if unit == "%" else (raw + 100) * 2
    except (ValueError, TypeError):
        return "?"
    return "▂▄▆█"[: max(1, min(4, round(strength / 25)))]


def render_table(networks: list[Network]) -> None:
    headers = ["SSID", "BSSID", "Kanal", "MHz", "Siqnal", "", "Təhlükəsizlik", "Qoşulub"]
    rows = [[n.ssid, n.bssid, n.channel, n.frequency_mhz, f"{n.signal} {n.signal_unit}".strip(), signal_bars(n.signal, n.signal_unit), n.security, "*" if n.in_use else ""] for n in networks]
    widths = [min(max(len(headers[i]), *(len(row[i]) for row in rows)) if rows else len(headers[i]), 32) for i in range(len(headers))]
    print("  ".join(headers[i].ljust(widths[i]) for i in range(len(headers))))
    print("  ".join("-" * width for width in widths))
    for row in rows:
        print("  ".join(value[:widths[i]].ljust(widths[i]) for i, value in enumerate(row)))
    print(f"\nCəmi: {len(networks)} şəbəkə")


def save_csv(path: Path, networks: list[Network]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=list(asdict(networks[0]).keys()) if networks else ["ssid", "bssid", "channel", "frequency_mhz", "signal", "signal_unit", "security", "in_use"])
        writer.writeheader()
        writer.writerows(asdict(network) for network in networks)


def main() -> int:
    parser = argparse.ArgumentParser(description="Yaxındakı Wi-Fi şəbəkələrini skan edir (yalnız oxu).")
    parser.add_argument("-i", "--interface", help="Wi-Fi interfeysi, məsələn wlan0")
    parser.add_argument("--backend", choices=["auto", "nmcli", "iw"], default="auto", help="Skan mühərriki (default: auto)")
    parser.add_argument("--json", action="store_true", help="Nəticəni JSON formatında göstər")
    parser.add_argument("--csv", metavar="FAYL", help="Nəticəni CSV faylına yaz")
    parser.add_argument("--watch", type=float, metavar="SANİYƏ", help="Davamlı skan et, verilən intervalda yenilə")
    parser.add_argument("--no-rescan", action="store_true", help="nmcli üçün keşdən istifadə et")
    args = parser.parse_args()
    if args.watch is not None and args.watch < 1:
        parser.error("--watch ən azı 1 saniyə olmalıdır")

    try:
        while True:
            networks = scan(args.interface, args.backend, not args.no_rescan)
            if args.json:
                print(json.dumps({"scanned_at": datetime.now(timezone.utc).isoformat(), "networks": [asdict(n) for n in networks]}, ensure_ascii=False, indent=2))
            else:
                render_table(networks)
            if args.csv:
                save_csv(Path(args.csv), networks)
                if not args.json:
                    print(f"CSV saxlanıldı: {args.csv}")
            if args.watch is None:
                break
            time.sleep(args.watch)
            print("\033[2J\033[H", end="")
    except KeyboardInterrupt:
        print("\nSkan dayandırıldı.")
    except (ScanError, OSError) as exc:
        print(f"Xəta: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
