# WiFi Skaner

Kali Linux və Windows üçün rəngli terminal Wi-Fi skaner demosu. Standart rejimdə uydurma Wi-Fi adları, rəngli cədvəl, drakon banneri və alov animasiyası göstərir. `--live` / `-Live` ilə həqiqi şəbəkələri skan edə bilər. Demo məlumatları real şəbəkələri əks etdirmir.

## Tələblər

- Python 3.10 və ya daha yeni
- Tövsiyə olunur: NetworkManager (`nmcli`)
- Alternativ: `iw` (scan üçün root/sudo tələb oluna bilər)
- Wi-Fi adapteri

Əlavə Python paketi lazım deyil.

## Quraşdırma

```bash
git clone https://github.com/manavvpopli-del/wifiter.git
cd wifiter
chmod +x wifi_skaner.py
```

Kali-də `nmcli` yoxdursa, `iw` istifadə edə bilərsiniz:

```bash
sudo apt update
sudo apt install iw
```

## Kali/Linux

```bash
python3 wifi_skaner.py
```

Bu standart demo rejimidir. Həqiqi skan üçün `--live` istifadə et:

```bash
python3 wifi_skaner.py --live
```

Digər seçimlər:

```bash
python3 wifi_skaner.py --live --interface wlan0
python3 wifi_skaner.py --live --backend iw --interface wlan0
python3 wifi_skaner.py --json
python3 wifi_skaner.py --csv networks.csv
python3 wifi_skaner.py --watch 5
python3 wifi_skaner.py --no-animation
```

Həqiqi skanda `iw` icazə xətası versə, `sudo python3 wifi_skaner.py --live --backend iw --interface wlan0` işlədin. Monitor mode tələb olunmur. Yalnız istifadə etməyə icazən olan cihaz və mühitlərdə skan et.

## Windows PowerShell

Standartda simulyasiyadır. Həqiqi skan üçün Windows-un daxili `netsh` əmrindən istifadə edən `-Live` seç:

```powershell
.\wifi_skaner.ps1
.\wifi_skaner.ps1 -Live
.\wifi_skaner.ps1 -Json
.\wifi_skaner.ps1 -Csv networks.csv
.\wifi_skaner.ps1 -Watch 5
.\wifi_skaner.ps1 -NoAnimation
```

Skript işlətmə siyasəti buna mane olsa, yalnız cari PowerShell pəncərəsi üçün icazə verib başladın:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\wifi_skaner.ps1
```

Windows canlı skanında `netsh wlan show networks mode=bssid` istifadə olunur. Demo rejimində şəbəkə adları və MAC ünvanları uydurmadır.

## GitHub repository

Repo: [manavvpopli-del/wifiter](https://github.com/manavvpopli-del/wifiter)

## Lisenziya

MIT. Bax [LICENSE](LICENSE).
