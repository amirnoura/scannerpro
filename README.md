# scannerpro
VLESS IP Scanner &amp; Config Generator - Generate VLESS configs from IP ranges and test latency with V2RayN
# VLESS Config Generator

ابزاری برای ساخت تعداد زیادی کانفیگ VLESS از روی لیست IP و رنج‌های CIDR و تست آن‌ها در V2RayN.

## قابلیت‌ها

- پشتیبانی از IP تکی
- پشتیبانی از رنج CIDR
- تغییر خودکار IP و پورت
- شماره‌گذاری خودکار کانفیگ‌ها
- تقسیم خروجی به دسته‌های 500 تایی
- ایمپورت خودکار به V2RayN
- اجرای Real Delay Test

## پیش‌نیازها

Python 3.10+

نصب کتابخانه‌ها:

```bash
pip install pyautogui pyperclip
```

## فایل‌ها

### config.txt

کانفیگ‌ VLESS ورودی:

```text
vless://...
vless://...
```

### ip-in.txt

IP یا رنج IP:

```text
104.16.0.1
104.16.1.0/24
172.67.0.0/24
```

## تنظیمات

داخل فایل main.py:

```python
NEW_PORT = 443
BATCH_SIZE = 500
PING_WAIT_SECONDS = 120
```

## اجرا

```bash
python scannerpro.py
```

قبل از شروع تست، پنجره V2RayN را باز و فعال کنید.
ترجیحا اول ویتوری رو باز کنید یک ساب گروپ جدید بسازید و فقط براش اسم بزارید
بعد روش کلیک کنید برید توی همون گروه
روی همین صفحه بمونید برید فایل پایتون رو ران کنید اینجا 5 ثانیه فرصت دارید یه کلیک بزنید روی برنامه ویتوری تا بیاد رو صفحه اصلی.
ترجیحا ای پی های مورد تست رو 500 تا 500 تا وارد کنید.
