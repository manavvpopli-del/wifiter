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
