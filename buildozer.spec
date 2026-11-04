[app]
# (str) عنوان التطبيق الذي سيظهر تحت الأيقونة
title = Medical Abbreviations

# (str) اسم الحزمة (بدون مسافات)
package.name = medicaldict

# (str) اسم النطاق
package.domain = org.med

# (str) مسار الكود المصدري
source.dir = .

# (list) امتدادات الملفات التي سيتم تضمينها (أضفنا html و db)
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,json,txt,html,db

# (str) مسار الأيقونة (تأكد من وجود ملف icon.png في المجلد)
icon.filename = %(source.dir)s/icon.png

# (str) إصدار التطبيق
version = 1.0.0

# (list) المتطلبات (أضفنا kivy_garden.webview و pyjnius لعرض صفحة الويب)
requirements = python3==3.10.12, hostpython3==3.10.12, kivy==2.3.0, kivy_garden.webview, pyjnius, pillow==9.5.0

# (str) اتجاه الشاشة (طولي)
orientation = portrait

# (bool) ملء الشاشة
fullscreen = 0

# (list) صلاحيات التطبيق
android.permissions = INTERNET, WAKE_LOCK

# (bool) الموافقة التلقائية على تراخيص أندرويد
android.accept_sdk_license = True

# (int) إصدار أندرويد المستهدف
android.api = 33

# (int) الحد الأدنى لإصدار أندرويد
android.minapi = 24

# (str) إصدار NDK
android.ndk = 25b

# (list) معماريات المعالج (arm64-v8a يغطي 99% من الهواتف الحديثة)
android.archs = arm64-v8a

[buildozer]
# (int) مستوى السجلات أثناء البناء
log_level = 2

# (int) التحذير عند التشغيل كـ root
warn_on_root = 0
