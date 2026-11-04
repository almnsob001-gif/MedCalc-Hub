[app]
title = Medical Abbreviations
package.name = medicaldict
package.domain = org.med
source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,db,ttf,json,txt
version = 1.0.0
requirements = python3==3.10.12, hostpython3==3.10.12, kivy==2.3.0, kivymd==1.2.0, pillow==9.5.0, sqlite3
android.permissions = INTERNET
android.accept_sdk_license = True
android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a
android.orientation = portrait

[buildozer]
log_level = 2
warn_on_root = 0
