# WiFi Security Lab

Windows PowerShell və Kali/Linux üçün interaktiv, tam offline Wi-Fi təhlükəsizlik simulyatoru. Təxminən 10 uydurma şəbəkə adı, rəngli terminal cədvəli və drakon banner/animasiya göstərir. Nömrə seçiləndə saxta “hücum” gedişi və yalnız uydurma açar nümayiş olunur.

**Bu proqram Wi-Fi skan etmir, şəbəkəyə qoşulmur, hücum etmir və real şifrə əldə etmir.** Cədvəldəki SSID, BSSID və açarlar nümunə məlumatlarıdır.

## Windows PowerShell

Repo qovluğunda:

```powershell
.\wifi_skaner.ps1
```

Nömrə seçib Enter bas. Başqa şəbəkə simulyasiyası üçün yenidən seçim edə bilərsən; `Q` ilə çıx.

Animasiya sürətini artırmaq və ya giriş animasiyasını söndürmək:

```powershell
.\wifi_skaner.ps1 -DelayMilliseconds 50
.\wifi_skaner.ps1 -NoAnimation
```

PowerShell skript işə salmağı bloklayarsa, cari pəncərə üçün:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\wifi_skaner.ps1
```

## Kali/Linux

Python 3.10+ kifayətdir; əlavə paket və Wi-Fi adapteri lazım deyil.

```bash
python3 wifi_skaner.py
```

Animasiya sürətini artırmaq və ya söndürmək:

```bash
python3 wifi_skaner.py --fast
python3 wifi_skaner.py --no-animation
```

## GitHub

Repo: [manavvpopli-del/wifiter](https://github.com/manavvpopli-del/wifiter)

## Lisenziya

MIT. Bax [LICENSE](LICENSE).
