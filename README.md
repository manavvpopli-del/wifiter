# WiFi Skaner

Kali Linux üçün yaxınlıqdakı Wi-Fi şəbəkələrinin SSID, BSSID, kanal, tezlik, siqnal gücü və təhlükəsizlik növünü göstərən kiçik Python aləti. Yalnız şəbəkələri aşkarlayır; parol sındırma, deauth və paket inyeksiyası etmir.

## Tələblər

- Python 3.10 və ya daha yeni
- Tövsiyə olunur: NetworkManager (`nmcli`)
- Alternativ: `iw` (scan üçün root/sudo tələb oluna bilər)
- Wi-Fi adapteri

Əlavə Python paketi lazım deyil.

## Quraşdırma

```bash
git clone https://github.com/USERNAME/wifi-skaner.git
cd wifi-skaner
chmod +x wifi_skaner.py
```

Kali-də `nmcli` yoxdursa, `iw` istifadə edə bilərsiniz:

```bash
sudo apt update
sudo apt install iw
```

## İstifadə

```bash
python3 wifi_skaner.py
```

Seçilmiş interfeys və çıxış formatları:

```bash
python3 wifi_skaner.py --interface wlan0
python3 wifi_skaner.py --backend iw --interface wlan0
python3 wifi_skaner.py --json
python3 wifi_skaner.py --csv networks.csv
python3 wifi_skaner.py --watch 5
```

`iw` mühərriki ilə icazə xətası alsanız, `sudo python3 wifi_skaner.py --backend iw --interface wlan0` işlədin. Monitor mode tələb olunmur. Yalnız istifadə etməyə icazəniz olan cihaz və mühitlərdə skan edin.

## Windows PowerShell

Windows versiyası əlavə quraşdırma tələb etmir; Windows-un daxili `netsh` WLAN əmrindən istifadə edir:

```powershell
.\wifi_skaner.ps1
.\wifi_skaner.ps1 -Json
.\wifi_skaner.ps1 -Csv networks.csv
.\wifi_skaner.ps1 -Watch 5
```

Skript işlətmə siyasəti buna mane olsa, yalnız cari PowerShell pəncərəsi üçün icazə verib başladın:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\wifi_skaner.ps1
```

Windows əmri `netsh wlan show networks mode=bssid` görünən şəbəkələrin BSSID, siqnal və kanal məlumatını qaytarır. [Microsoft dokumentasiyası](https://learn.microsoft.com/en-us/troubleshoot/windows-client/networking/wireless-network-connectivity-issues-troubleshooting).

## GitHub-a göndərmə

GitHub-da boş repository yaradandan sonra:

```bash
git init
git add .
git commit -m "Initial WiFi scanner"
git branch -M main
git remote add origin https://github.com/USERNAME/wifi-skaner.git
git push -u origin main
```

## Lisenziya

MIT. Bax [LICENSE](LICENSE).
