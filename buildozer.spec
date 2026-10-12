[app]

# عنوان اپلیکیشن
title = Card Switch Manager

# نام پکیج و دامنه
package.name = cardswitchapp
package.domain = org.test

# دایرکتوری سورس کد
source.dir = .

# فرمت‌های قابل قبول در پروژه
source.include_exts = py,png,jpg,kv,atlas

# نسخه اپلیکیشن
version = 1.0

# پکیج‌ها و وابستگی‌های پایتون (شامل کتابخانه‌های لازم برای درخواست‌های شبکه و API)
requirements = python3,kivy==2.3.0,certifi,urllib3,idna,charset-normalizer,requests

# جهت صفحه نمایش
orientation = portrait

# حالت تمام صفحه (۰ یعنی غیرفعال و ۱ یعنی فعال)
fullscreen = 0

# دسترسی‌های مورد نیاز اندروید (اینترنت و وضعیت شبکه)
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# نسخه‌های API و NDK برای پایداری بیلد
android.api = 33
android.minapi = 21
android.ndk = 25b

# پذیرش خودکار لایسنس SDK
android.accept_sdk_license = True

# معماری‌های پشتیبانی شده پردازنده
android.archs = arm64-v8a,armeabi-v7a

[buildozer]

# سطح لاگ‌برداری (۲ برای نمایش جزئیات کامل جهت عیب‌یابی)
log_level = 2

# هشدار عدم اجرا با دسترسی روت
warn_on_root = 1
