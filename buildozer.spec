[app]
title = Health App
package.name = healthapp
package.domain = org.healthapp
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,json,txt
icon.filename = %(source.dir)s/icon.png
version = 1.0.0
requirements = python3==3.10.12, hostpython3==3.10.12, kivy==2.3.0, kivymd==0.104.2, pillow==9.5.0, plyer
android.permissions = INTERNET, WAKE_LOCK, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.accept_sdk_license = True
android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a
android.orientation = portrait

[buildozer]
log_level = 2
warn_on_root = 0
