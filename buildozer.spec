[app]
title = Health App
package.name = healthapp
package.domain = org.healthapp
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,json,txt
version = 1.0.0

requirements = python3==3.10.12, hostpython3==3.10.12, kivy==2.3.0, kivymd==0.104.2, plyer

android.permissions = INTERNET, WAKE_LOCK
android.accept_sdk_license = True
android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a
android.orientation = portrait

[buildozer]
log_level = 2
warn_on_root = 0

