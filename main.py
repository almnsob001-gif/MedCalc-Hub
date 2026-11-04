import os
import json
import traceback
from datetime import datetime, timedelta

# ========= سجل تشخيصي مبكر =========
def write_diag(msg):
    try:
        msg_full = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
        for p in [
            "/storage/emulated/0/Download/healthapp_diag.txt",
            "/sdcard/Download/healthapp_diag.txt",
            "/storage/emulated/0/healthapp_diag.txt",
            "/sdcard/healthapp_diag.txt",
        ]:
            try:
                with open(p, "a", encoding="utf-8") as f:
                    f.write(msg_full + "\n")
                return
            except Exception:
                continue
        print(msg_full)
    except Exception:
        pass

write_diag("=" * 40)
write_diag("APP START")

try:
    import kivy
    write_diag(f"Kivy: {kivy.__version__}")
except Exception as e:
    write_diag(f"Kivy import failed: {e}")

try:
    import kivymd
    write_diag(f"KivyMD: {kivymd.__version__}")
except Exception as e:
    write_diag(f"KivyMD import failed: {e}")

from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import StringProperty, ListProperty, BooleanProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.toast import toast

try:
    from kivymd.uix.screenmanager import MDScreenManager
    ScreenMgrClass = MDScreenManager
except ImportError:
    from kivy.uix.screenmanager import ScreenManager
    ScreenMgrClass = ScreenManager

write_diag("Imports OK")

# =========================================================
# ============ إجبار الوضع العمودي على Android =========
# =========================================================
from kivy.utils import platform

if platform == "android":
    try:
        from android import config
        config.orientation = ["portrait"]
        write_diag("Android orientation set to portrait")
    except Exception as e:
        write_diag(f"orientation (config) err: {e}")

    try:
        from android.runnable import run_on_ui_thread
        from jnius import autoclass

        @run_on_ui_thread
        def _force_portrait():
            try:
                PythonActivity = autoclass("org.kivy.android.PythonActivity")
                activity = PythonActivity.mActivity
                activity.setRequestedOrientation(1)
                write_diag("setRequestedOrientation(1) OK")
            except Exception as e:
                write_diag(f"setRequestedOrientation err: {e}")

        Clock.schedule_once(lambda dt: _force_portrait(), 0.5)
    except Exception as e:
        write_diag(f"orientation (jnius) err: {e}")

# =========================================================
# ============ مسار آمن على Android =====================
# =========================================================
def get_data_file():
    try:
        app = MDApp.get_running_app()
        if app is not None:
            return os.path.join(app.user_data_dir, "health_app_data.json")
    except Exception:
        pass
    return os.path.join(os.path.expanduser("~"), "health_app_data.json")

write_diag(f"Initial data path: {get_data_file()}")

# =========================================================
# ============ Custom Python Classes ====================
# =========================================================
class FeatureCard(ButtonBehavior, BoxLayout):
    icon_name = StringProperty("")
    title_text = StringProperty("")
    subtitle_text = StringProperty("")
    icon_color = ListProperty([0.13, 0.59, 0.95, 1])
    icon_bg_color = ListProperty([0.13, 0.59, 0.95, 0.15])

class Card(BoxLayout):
    pass

class PageHeader(BoxLayout):
    title_text = StringProperty("")
    subtitle_text = StringProperty("")
    show_back = BooleanProperty(True)
    header_color = ListProperty([0.09, 0.42, 0.74, 1])
    icon_name = StringProperty("")

class HistoryRow(BoxLayout):
    date_text = StringProperty("")
    value_text = StringProperty("")
    category_text = StringProperty("")
    status_color = ListProperty([0.13, 0.59, 0.95, 1])

KV = r"""
#:import dp kivymd.material_resources.dp

<FeatureCard>:
    orientation: "horizontal"
    size_hint_y: None
    height: dp(88)
    padding: dp(14)
    spacing: dp(14)
    canvas.before:
        Color:
            rgba: 0, 0, 0, 0.06
        RoundedRectangle:
            pos: self.x + dp(1), self.y - dp(4)
            size: self.size
            radius: [dp(14)]
        Color:
            rgba: 1, 1, 1, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(14)]
    BoxLayout:
        size_hint: None, None
        size: dp(56), dp(56)
        pos_hint: {"center_y": .5}
        canvas.before:
            Color:
                rgba: root.icon_bg_color
            Ellipse:
                pos: self.pos
                size: self.size
        MDIcon:
            icon: root.icon_name
            font_size: "26sp"
            theme_text_color: "Custom"
            text_color: root.icon_color
            pos_hint: {"center_x": .5, "center_y": .5}
    BoxLayout:
        orientation: "vertical"
        pos_hint: {"center_y": .5}
        MDLabel:
            text: root.title_text
            font_size: "15sp"
            bold: True
            size_hint_y: None
            height: dp(22)
        MDLabel:
            text: root.subtitle_text
            font_size: "11sp"
            theme_text_color: "Secondary"
            size_hint_y: None
            height: dp(18)
    MDIcon:
        icon: "chevron-right"
        font_size: "20sp"
        theme_text_color: "Secondary"
        size_hint_x: None
        width: dp(22)
        pos_hint: {"center_y": .5}

<Card>:
    orientation: "vertical"
    padding: dp(16)
    spacing: dp(12)
    size_hint_y: None
    canvas.before:
        Color:
            rgba: 0, 0, 0, 0.06
        RoundedRectangle:
            pos: self.x + dp(1), self.y - dp(4)
            size: self.size
            radius: [dp(14)]
        Color:
            rgba: 1, 1, 1, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(14)]

<PageHeader>:
    orientation: "horizontal"
    size_hint_y: None
    height: dp(82)
    padding: dp(4), dp(16)
    spacing: dp(10)
    canvas.before:
        Color:
            rgba: root.header_color
        Rectangle:
            pos: self.pos
            size: self.size
    Button:
        size_hint: None, None
        width: dp(44) if root.show_back else 0
        height: dp(44)
        opacity: 1 if root.show_back else 0
        disabled: not root.show_back
        background_normal: ""
        background_down: ""
        background_color: 0, 0, 0, 0
        pos_hint: {"center_y": .5}
        on_release: app.go_home()
        MDIcon:
            icon: "arrow-left"
            font_size: "24sp"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            size_hint: None, None
            size: dp(24), dp(24)
            pos_hint: {"center_x": .5, "center_y": .5}
    BoxLayout:
        size_hint: None, None
        size: dp(46), dp(46)
        pos_hint: {"center_y": .5}
        canvas.before:
            Color:
                rgba: 1, 1, 1, 0.22
            Ellipse:
                pos: self.pos
                size: self.size
        MDIcon:
            icon: root.icon_name
            font_size: "24sp"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            pos_hint: {"center_x": .5, "center_y": .5}
    BoxLayout:
        orientation: "vertical"
        pos_hint: {"center_y": .5}
        MDLabel:
            text: root.title_text
            font_size: "17sp"
            bold: True
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            size_hint_y: None
            height: dp(22)
        MDLabel:
            text: root.subtitle_text
            font_size: "10sp"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 0.7
            size_hint_y: None
            height: dp(14)

<HistoryRow>:
    orientation: "horizontal"
    size_hint_y: None
    height: dp(64)
    padding: dp(14), dp(10)
    spacing: dp(12)
    canvas.before:
        Color:
            rgba: 0, 0, 0, 0.04
        RoundedRectangle:
            pos: self.x, self.y - dp(2)
            size: self.size
            radius: [dp(12)]
        Color:
            rgba: 1, 1, 1, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(12)]
    Widget:
        size_hint: None, None
        size: dp(4), dp(40)
        pos_hint: {"center_y": .5}
        canvas:
            Color:
                rgba: root.status_color
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [dp(2)]
    BoxLayout:
        orientation: "vertical"
        pos_hint: {"center_y": .5}
        spacing: dp(2)
        MDLabel:
            text: root.date_text
            font_size: "10sp"
            theme_text_color: "Secondary"
            size_hint_y: None
            height: dp(14)
        MDLabel:
            text: root.category_text
            font_size: "13sp"
            bold: True
            theme_text_color: "Custom"
            text_color: root.status_color
            size_hint_y: None
            height: dp(20)
    MDLabel:
        text: root.value_text
        font_size: "20sp"
        bold: True
        halign: "right"
        valign: "center"
        theme_text_color: "Custom"
        text_color: root.status_color
        size_hint_x: None
        width: dp(110)

<GetStartedScreen>:
    AnchorLayout:
        anchor_x: "center"
        anchor_y: "center"
        canvas.before:
            Color:
                rgba: 0.05, 0.33, 0.62, 1
            Rectangle:
                pos: self.pos
                size: self.size
        BoxLayout:
            orientation: "vertical"
            size_hint: None, None
            width: min(root.width - dp(48), dp(380))
            height: self.minimum_height
            padding: dp(24)
            spacing: dp(14)
            BoxLayout:
                size_hint: None, None
                size: dp(140), dp(140)
                pos_hint: {"center_x": .5}
                canvas.before:
                    Color:
                        rgba: 1, 1, 1, 0.18
                    Ellipse:
                        pos: self.pos
                        size: self.size
                MDIcon:
                    icon: "heart-pulse"
                    font_size: "68sp"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1
                    pos_hint: {"center_x": .5, "center_y": .5}
            MDLabel:
                text: "Health App"
                halign: "center"
                font_size: "34sp"
                bold: True
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                size_hint_y: None
                height: dp(48)
            MDLabel:
                text: "Your complete health companion"
                halign: "center"
                font_size: "14sp"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 0.8
                size_hint_y: None
                height: dp(24)
            MDRaisedButton:
                text: "GET STARTED"
                size_hint_y: None
                height: dp(52)
                size_hint_x: 1
                md_bg_color: 1, 1, 1, 1
                text_color: 0.05, 0.33, 0.62, 1
                on_release: app.sm.current = "disclaimer"

<DisclaimerScreen>:
    BoxLayout:
        orientation: "vertical"
        canvas.before:
            Color:
                rgba: 0.97, 0.97, 0.97, 1
            Rectangle:
                pos: self.pos
                size: self.size
        PageHeader:
            title_text: "Disclaimer"
            subtitle_text: "Please read carefully"
            show_back: False
            header_color: 0.85, 0.30, 0.20, 1
            icon_name: "alert"
        ScrollView:
            do_scroll_x: False
            BoxLayout:
                orientation: "vertical"
                padding: dp(16)
                spacing: dp(14)
                size_hint_y: None
                height: self.minimum_height
                Card:
                    height: dp(260)
                    MDLabel:
                        text: "Please Read Carefully"
                        halign: "center"
                        font_size: "17sp"
                        bold: True
                    MDLabel:
                        text: "This app is for informational purposes only and does not replace professional medical advice. Blood pressure uses ESH 2023 guidelines. Blood sugar uses ADA guidelines."
                        halign: "center"
                        text_size: self.width, None
                        font_size: "13sp"
                        theme_text_color: "Secondary"
                        size_hint_y: None
                        height: dp(160)
        BoxLayout:
            size_hint_y: None
            height: dp(84)
            padding: dp(16), dp(16)
            MDRaisedButton:
                text: "I AGREE & CONTINUE"
                pos_hint: {"center_x": .5, "center_y": .5}
                size_hint_x: .85
                on_release: app.accept_disclaimer()

<HomeScreen>:
    BoxLayout:
        orientation: "vertical"
        canvas.before:
            Color:
                rgba: 0.97, 0.97, 0.97, 1
            Rectangle:
                pos: self.pos
                size: self.size
        BoxLayout:
            orientation: "horizontal"
            size_hint_y: None
            height: dp(115)
            padding: dp(20), dp(24)
            spacing: dp(14)
            canvas.before:
                Color:
                    rgba: 0.09, 0.42, 0.74, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
            MDIcon:
                icon: "heart-pulse"
                font_size: "30sp"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                size_hint: None, None
                size: dp(40), dp(40)
                pos_hint: {"center_y": .5}
            BoxLayout:
                orientation: "vertical"
                pos_hint: {"center_y": .5}
                MDLabel:
                    text: "Health App"
                    font_size: "20sp"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1
                MDLabel:
                    text: "Track your health daily"
                    font_size: "12sp"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 0.85
        ScrollView:
            do_scroll_x: False
            BoxLayout:
                orientation: "vertical"
                padding: dp(16)
                spacing: dp(12)
                size_hint_y: None
                height: self.minimum_height
                FeatureCard:
                    icon_name: "calculator"
                    title_text: "BMI Calculator"
                    subtitle_text: "Body mass index"
                    icon_color: 0.13, 0.59, 0.95, 1
                    icon_bg_color: 0.13, 0.59, 0.95, 0.15
                    on_release: app.sm.current = "bmi"
                FeatureCard:
                    icon_name: "heart-pulse"
                    title_text: "Blood Pressure"
                    subtitle_text: "ESH 2023 classification"
                    icon_color: 0.91, 0.30, 0.24, 1
                    icon_bg_color: 0.91, 0.30, 0.24, 0.15
                    on_release: app.sm.current = "bp"
                FeatureCard:
                    icon_name: "water"
                    title_text: "Blood Sugar"
                    subtitle_text: "ADA classification"
                    icon_color: 0.20, 0.65, 0.32, 1
                    icon_bg_color: 0.20, 0.65, 0.32, 0.15
                    on_release: app.sm.current = "sugar"
                FeatureCard:
                    icon_name: "food-apple"
                    title_text: "Calories"
                    subtitle_text: "Daily calorie needs"
                    icon_color: 1.0, 0.60, 0.0, 1
                    icon_bg_color: 1.0, 0.60, 0.0, 0.15
                    on_release: app.sm.current = "calories"
                FeatureCard:
                    icon_name: "pill"
                    title_text: "Medications"
                    subtitle_text: "Reminders with alarm"
                    icon_color: 0.60, 0.30, 0.90, 1
                    icon_bg_color: 0.60, 0.30, 0.90, 0.15
                    on_release: app.sm.current = "medication"

<BMIScreen>:
    BoxLayout:
        orientation: "vertical"
        PageHeader:
            title_text: "BMI Calculator"
            subtitle_text: "Body Mass Index"
            header_color: 0.13, 0.59, 0.95, 1
            icon_name: "calculator"
        ScrollView:
            do_scroll_x: False
            BoxLayout:
                orientation: "vertical"
                padding: dp(16)
                spacing: dp(14)
                size_hint_y: None
                height: self.minimum_height
                Card:
                    height: dp(260)
                    MDTextField:
                        id: weight_input
                        hint_text: "Weight (kg)"
                        input_filter: "float"
                    MDTextField:
                        id: height_input
                        hint_text: "Height (cm)"
                        input_filter: "float"
                    MDRaisedButton:
                        text: "CALCULATE"
                        md_bg_color: 0.13, 0.59, 0.95, 1
                        pos_hint: {"center_x": .5}
                        size_hint_x: .7
                        on_release: root.calculate()
                Card:
                    height: dp(180)
                    MDLabel:
                        id: bmi_result
                        text: "--"
                        halign: "center"
                        font_size: "44sp"
                        bold: True
                    MDLabel:
                        id: bmi_category
                        text: ""
                        halign: "center"
                        font_size: "14sp"

<BPScreen>:
    BoxLayout:
        orientation: "vertical"
        PageHeader:
            title_text: "Blood Pressure"
            subtitle_text: "ESH 2023 Classification"
            header_color: 0.91, 0.30, 0.24, 1
            icon_name: "heart-pulse"
        ScrollView:
            do_scroll_x: False
            BoxLayout:
                orientation: "vertical"
                padding: dp(16)
                spacing: dp(14)
                size_hint_y: None
                height: self.minimum_height
                Card:
                    height: dp(280)
                    MDLabel:
                        text: "NEW READING"
                        font_size: "10sp"
                        bold: True
                        theme_text_color: "Secondary"
                        size_hint_y: None
                        height: dp(18)
                    MDTextField:
                        id: systolic_input
                        hint_text: "Systolic (mmHg)"
                        input_filter: "int"
                    MDTextField:
                        id: diastolic_input
                        hint_text: "Diastolic (mmHg)"
                        input_filter: "int"
                    MDRaisedButton:
                        text: "SAVE RECORD"
                        md_bg_color: 0.91, 0.30, 0.24, 1
                        pos_hint: {"center_x": .5}
                        size_hint_x: .7
                        on_release: root.save_record()
                Card:
                    height: dp(90)
                    MDLabel:
                        text: "ESH 2023 Reference"
                        font_size: "11sp"
                        bold: True
                        theme_text_color: "Secondary"
                    MDLabel:
                        text: "Grade 1: 140-159 / 90-99  •  Grade 2: 160-179 / 100-109  •  Grade 3: ≥180 / ≥110"
                        font_size: "10sp"
                        theme_text_color: "Secondary"
                        text_size: self.width, None
                MDLabel:
                    text: "RECENT RECORDS"
                    font_size: "10sp"
                    bold: True
                    theme_text_color: "Secondary"
                    size_hint_y: None
                    height: dp(24)
                BoxLayout:
                    id: bp_history
                    orientation: "vertical"
                    spacing: dp(8)
                    size_hint_y: None
                    height: self.minimum_height

<SugarScreen>:
    BoxLayout:
        orientation: "vertical"
        PageHeader:
            title_text: "Blood Sugar"
            subtitle_text: "ADA Classification"
            header_color: 0.20, 0.65, 0.32, 1
            icon_name: "water"
        ScrollView:
            do_scroll_x: False
            BoxLayout:
                orientation: "vertical"
                padding: dp(16)
                spacing: dp(14)
                size_hint_y: None
                height: self.minimum_height
                Card:
                    height: dp(200)
                    MDLabel:
                        text: "NEW READING"
                        font_size: "10sp"
                        bold: True
                        theme_text_color: "Secondary"
                        size_hint_y: None
                        height: dp(18)
                    MDTextField:
                        id: sugar_input
                        hint_text: "Random Glucose (mg/dL)"
                        input_filter: "float"
                    MDRaisedButton:
                        text: "SAVE RECORD"
                        md_bg_color: 0.20, 0.65, 0.32, 1
                        pos_hint: {"center_x": .5}
                        size_hint_x: .7
                        on_release: root.save_record()
                Card:
                    height: dp(110)
                    MDLabel:
                        text: "ADA Reference"
                        font_size: "11sp"
                        bold: True
                        theme_text_color: "Secondary"
                    MDLabel:
                        text: "Low <70  •  Normal 70-139  •  Borderline 140-199  •  Suspect Diabetes ≥200 (confirm with doctor)"
                        font_size: "10sp"
                        theme_text_color: "Secondary"
                        text_size: self.width, None
                MDLabel:
                    text: "RECENT RECORDS"
                    font_size: "10sp"
                    bold: True
                    theme_text_color: "Secondary"
                    size_hint_y: None
                    height: dp(24)
                BoxLayout:
                    id: sugar_history
                    orientation: "vertical"
                    spacing: dp(8)
                    size_hint_y: None
                    height: self.minimum_height

<CaloriesScreen>:
    BoxLayout:
        orientation: "vertical"
        PageHeader:
            title_text: "Calories"
            subtitle_text: "Mifflin-St Jeor Formula"
            header_color: 1.0, 0.60, 0.0, 1
            icon_name: "food-apple"
        ScrollView:
            do_scroll_x: False
            BoxLayout:
                orientation: "vertical"
                padding: dp(16)
                spacing: dp(14)
                size_hint_y: None
                height: self.minimum_height
                Card:
                    height: dp(420)
                    MDTextField:
                        id: cal_weight
                        hint_text: "Weight (kg)"
                        input_filter: "float"
                    MDTextField:
                        id: cal_height
                        hint_text: "Height (cm)"
                        input_filter: "float"
                    MDTextField:
                        id: cal_age
                        hint_text: "Age (years)"
                        input_filter: "int"
                    MDRaisedButton:
                        id: gender_btn
                        text: "Gender: Male"
                        size_hint_x: 1
                        on_release: root.cycle_gender()
                    MDRaisedButton:
                        id: activity_btn
                        text: "Activity: Sedentary"
                        size_hint_x: 1
                        on_release: root.cycle_activity()
                    MDRaisedButton:
                        text: "CALCULATE"
                        md_bg_color: 1.0, 0.60, 0.0, 1
                        pos_hint: {"center_x": .5}
                        size_hint_x: .7
                        on_release: root.calculate()
                Card:
                    height: dp(120)
                    MDLabel:
                        id: cal_result
                        text: "--"
                        halign: "center"
                        font_size: "22sp"
                        bold: True

<MedicationScreen>:
    BoxLayout:
        orientation: "vertical"
        PageHeader:
            title_text: "Medications"
            subtitle_text: "Reminders with Alarm"
            header_color: 0.60, 0.30, 0.90, 1
            icon_name: "pill"
        ScrollView:
            do_scroll_x: False
            BoxLayout:
                orientation: "vertical"
                padding: dp(16)
                spacing: dp(14)
                size_hint_y: None
                height: self.minimum_height
                Card:
                    height: dp(320)
                    MDLabel:
                        text: "NEW REMINDER"
                        font_size: "10sp"
                        bold: True
                        theme_text_color: "Secondary"
                        size_hint_y: None
                        height: dp(18)
                    MDTextField:
                        id: med_name
                        hint_text: "Medication name"
                    MDTextField:
                        id: med_time
                        hint_text: "Time (HH:MM) e.g. 14:30"
                    MDRaisedButton:
                        text: "ADD REMINDER (daily)"
                        md_bg_color: 0.60, 0.30, 0.90, 1
                        pos_hint: {"center_x": .5}
                        size_hint_x: .8
                        on_release: root.add_medication()
                    MDRaisedButton:
                        text: "TEST ALARM (5 sec)"
                        md_bg_color: 0.95, 0.55, 0.10, 1
                        pos_hint: {"center_x": .5}
                        size_hint_x: .8
                        on_release: root.test_alarm()
                Card:
                    height: dp(300)
                    MDLabel:
                        text: "SCHEDULED (repeats daily)"
                        font_size: "10sp"
                        bold: True
                        theme_text_color: "Secondary"
                        size_hint_y: None
                        height: dp(18)
                    MDLabel:
                        id: med_list
                        text: "No medications"
                        font_size: "12sp"
                        size_hint_y: None
                        height: dp(240)
                        text_size: self.width, None
                        valign: "top"
"""

# =========================================================
# ============ Helper Functions =========================
# =========================================================
def load_data():
    try:
        p = get_data_file()
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        write_diag(f"load_data err: {e}")
    return {}

def save_data(data):
    try:
        p = get_data_file()
        with open(p, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        write_diag(f"save_data err: {e}")

def classify_bp(s, d):
    # ESH 2023 Guidelines
    if s < 140 and d < 90:
        return "Normal", [0.30, 0.69, 0.31, 1]
    if 140 <= s <= 159 or 90 <= d <= 99:
        return "Grade 1 Hypertension", [1.0, 0.76, 0.03, 1]
    if 160 <= s <= 179 or 100 <= d <= 109:
        return "Grade 2 Hypertension", [1.0, 0.60, 0.0, 1]
    if s >= 180 or d >= 110:
        return "Grade 3 Hypertension", [0.96, 0.26, 0.21, 1]
    return "Unknown", [0.62, 0.62, 0.62, 1]

def classify_sugar(v):
    # ADA Guidelines — Random Glucose
    if v < 70:
        return "Low (Hypoglycemia)", [0.13, 0.59, 0.95, 1]
    if v < 140:
        return "Normal", [0.30, 0.69, 0.31, 1]
    if v < 200:
        return "Borderline - Needs Testing", [1.0, 0.60, 0.0, 1]
    return "Suspect Diabetes - Confirm", [0.96, 0.26, 0.21, 1]

def calculate_bmi(w, h):
    if h <= 0:
        return 0, "Error", [0.96, 0.26, 0.21, 1]
    bmi = w / ((h / 100) ** 2)
    if bmi < 18.5:
        return bmi, "Underweight", [0.13, 0.59, 0.95, 1]
    if bmi < 25:
        return bmi, "Normal", [0.30, 0.69, 0.31, 1]
    if bmi < 30:
        return bmi, "Overweight", [1.0, 0.76, 0.03, 1]
    return bmi, "Obese", [0.96, 0.26, 0.21, 1]

def calculate_calories(w, h, age, gender, activity):
    bmr = (10 * w + 6.25 * h - 5 * age + (5 if gender == "male" else -161))
    f = {"sedentary": 1.2, "light": 1.375, "moderate": 1.55,
         "active": 1.725, "very_active": 1.9}
    return bmr * f.get(activity, 1.2)

# =========================================================
# ============ Alarm Sound & Vibration ==================
# =========================================================
def play_alarm_sound():
    """يشغّل نغمة المنبه الافتراضية عبر RingtoneManager."""
    if platform != "android":
        write_diag("play_alarm_sound: non-android (skip)")
        return
    try:
        from jnius import autoclass
        from android import mActivity

        RingtoneManager = autoclass("android.media.RingtoneManager")
        uri = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_ALARM)
        ringtone = RingtoneManager.getRingtone(mActivity, uri)
        if ringtone is None:
            write_diag("Alarm ringtone None, trying notification")
            uri = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION)
            ringtone = RingtoneManager.getRingtone(mActivity, uri)
        if ringtone is None:
            write_diag("Alarm ringtone still None")
            return
        ringtone.play()
        write_diag("Alarm playing")
        Clock.schedule_once(lambda dt: ringtone.stop(), 30)
    except Exception as e:
        write_diag(f"play_alarm err: {e}")

def vibrate_phone():
    """اهتزاز الهاتف."""
    if platform != "android":
        return
    try:
        from jnius import autoclass
        from android import mActivity

        Context = autoclass("android.content.Context")
        vibrator = mActivity.getSystemService(Context.VIBRATOR_SERVICE)
        if vibrator is not None:
            vibrator.vibrate(2000)
            write_diag("Vibrate OK")
    except Exception as e:
        write_diag(f"vibrate err: {e}")

# =========================================================
# ============ Screens ==================================
# =========================================================
class GetStartedScreen(MDScreen):
    pass

class DisclaimerScreen(MDScreen):
    pass

class HomeScreen(MDScreen):
    pass

class BMIScreen(MDScreen):
    def calculate(self):
        try:
            w = float(self.ids.weight_input.text)
            h = float(self.ids.height_input.text)
            bmi, cat, color = calculate_bmi(w, h)
            self.ids.bmi_result.text = f"{bmi:.1f}"
            self.ids.bmi_category.text = cat
            self.ids.bmi_category.text_color = color
        except ValueError:
            toast("Please enter valid numbers")

class BPScreen(MDScreen):
    def save_record(self):
        try:
            s = int(self.ids.systolic_input.text)
            d_ = int(self.ids.diastolic_input.text)
            if s <= 0 or d_ <= 0 or s > 300 or d_ > 200:
                return toast("Values out of range")
            cat, color = classify_bp(s, d_)
            data = load_data()
            data.setdefault("bp_records", []).append({
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "sys": s, "dia": d_, "category": cat})
            save_data(data)
            self.ids.systolic_input.text = ""
            self.ids.diastolic_input.text = ""
            self.update_history()
            toast(f"Saved: {cat}")
        except ValueError:
            toast("Please enter valid numbers")

    def update_history(self):
        self.ids.bp_history.clear_widgets()
        recs = load_data().get("bp_records", [])
        if not recs:
            self.ids.bp_history.add_widget(MDLabel(
                text="No records yet", halign="center",
                font_size="11sp", theme_text_color="Secondary",
                size_hint_y=None, height=60))
            return
        for r in reversed(recs[-10:]):
            cat, color = classify_bp(r['sys'], r['dia'])
            self.ids.bp_history.add_widget(HistoryRow(
                date_text=r['date'],
                value_text=f"{r['sys']}/{r['dia']}",
                category_text=cat,
                status_color=color))

class SugarScreen(MDScreen):
    def save_record(self):
        try:
            v = float(self.ids.sugar_input.text)
            if v <= 0 or v > 1000:
                return toast("Value out of range")
            data = load_data()
            data.setdefault("sugar_records", []).append({
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "value": v})
            save_data(data)
            self.ids.sugar_input.text = ""
            self.update_history()
            cat, _ = classify_sugar(v)
            toast(f"Saved: {cat}")
        except ValueError:
            toast("Please enter a valid number")

    def update_history(self):
        self.ids.sugar_history.clear_widgets()
        recs = load_data().get("sugar_records", [])
        if not recs:
            self.ids.sugar_history.add_widget(MDLabel(
                text="No records yet", halign="center",
                font_size="11sp", theme_text_color="Secondary",
                size_hint_y=None, height=60))
            return
        for r in reversed(recs[-10:]):
            cat, color = classify_sugar(r['value'])
            self.ids.sugar_history.add_widget(HistoryRow(
                date_text=r['date'],
                value_text=f"{r['value']} mg/dL",
                category_text=cat,
                status_color=color))

class CaloriesScreen(MDScreen):
    gender = "Male"
    activity = "Sedentary"

    def cycle_gender(self):
        self.gender = "Female" if self.gender == "Male" else "Male"
        self.ids.gender_btn.text = f"Gender: {self.gender}"

    def cycle_activity(self):
        opts = ["Sedentary", "Light", "Moderate", "Active", "Very Active"]
        i = opts.index(self.activity)
        self.activity = opts[(i + 1) % len(opts)]
        self.ids.activity_btn.text = f"Activity: {self.activity}"

    def calculate(self):
        try:
            w = float(self.ids.cal_weight.text)
            h = float(self.ids.cal_height.text)
            age = int(self.ids.cal_age.text)
            gk = "male" if self.gender == "Male" else "female"
            ak = {"Sedentary": "sedentary", "Light": "light",
                  "Moderate": "moderate", "Active": "active",
                  "Very Active": "very_active"}[self.activity]
            cal = calculate_calories(w, h, age, gk, ak)
            self.ids.cal_result.text = f"{cal:.0f} kcal/day"
        except ValueError:
            toast("Please enter valid values")

class MedicationScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scheduled_events = []

    def add_medication(self):
        name = self.ids.med_name.text.strip()
        tm = self.ids.med_time.text.strip()
        if not name or not tm:
            return toast("Please enter name and time")
        try:
            h, m = map(int, tm.split(":"))
            if not (0 <= h <= 23 and 0 <= m <= 59):
                raise ValueError
        except Exception:
            return toast("Use HH:MM format (e.g. 14:30)")

        data = load_data()
        data.setdefault("medications", []).append({"name": name, "time": tm})
        save_data(data)
        self.schedule_notification(name, tm)
        self.ids.med_name.text = ""
        self.ids.med_time.text = ""
        self.update_list()
        toast(f"Reminder set: {name} at {tm}")

    def schedule_notification(self, name, time_str):
        try:
            h, m = map(int, time_str.split(":"))
            now = datetime.now()
            target = now.replace(hour=h, minute=m, second=0, microsecond=0)
            if target <= now:
                target += timedelta(days=1)
            delay = (target - now).total_seconds()
            ev = Clock.schedule_once(
                lambda dt: self.fire_alarm(name, time_str), delay)
            self.scheduled_events.append(ev)
            write_diag(f"Scheduled {name} at {time_str} (in {delay:.0f}s)")
        except Exception as e:
            write_diag(f"schedule err: {e}")

    def fire_alarm(self, name, time_str):
        write_diag(f"ALARM FIRED: {name}")
        play_alarm_sound()
        vibrate_phone()
        try:
            from plyer import notification
            notification.notify(
                title="Medication Reminder",
                message=f"Time to take {name}",
                app_name="Health App",
                timeout=30,
            )
        except Exception as e:
            write_diag(f"notif err: {e}")
        # إعادة الجدولة لليوم التالي (تكرار يومي)
        Clock.schedule_once(
            lambda dt: self.schedule_notification(name, time_str), 5)

    def test_alarm(self):
        name = self.ids.med_name.text.strip() or "Test Medication"
        write_diag("Test alarm scheduled in 5 sec")
        toast("Alarm will ring in 5 seconds...")
        Clock.schedule_once(lambda dt: self.fire_alarm(name, "TEST"), 5)

    def reschedule_all(self):
        """يُعيد جدولة كل المنبهات عند فتح التطبيق."""
        for ev in self.scheduled_events:
            try:
                ev.cancel()
            except Exception:
                pass
        self.scheduled_events.clear()
        meds = load_data().get("medications", [])
        for m in meds:
            self.schedule_notification(m["name"], m["time"])
        write_diag(f"Rescheduled {len(meds)} medications")

    def update_list(self):
        meds = load_data().get("medications", [])
        lines = [f"• {m['name']}\n   at {m['time']} (daily)" for m in meds]
        self.ids.med_list.text = "\n\n".join(lines) if lines else "No medications"

# =========================================================
# ============ App ======================================
# =========================================================
class HealthApp(MDApp):
    def build(self):
        try:
            self.theme_cls.primary_palette = "Blue"
            self.theme_cls.theme_style = "Light"

            write_diag(f"user_data_dir: {self.user_data_dir}")
            write_diag(f"data_file will be: {get_data_file()}")

            Builder.load_string(KV)
            write_diag("KV loaded OK")

            self.sm = ScreenMgrClass()

            screens = [
                ("get_started", GetStartedScreen),
                ("disclaimer", DisclaimerScreen),
                ("home", HomeScreen),
                ("bmi", BMIScreen),
                ("bp", BPScreen),
                ("sugar", SugarScreen),
                ("calories", CaloriesScreen),
                ("medication", MedicationScreen),
            ]
            for name, cls in screens:
                self.sm.add_widget(cls(name=name))
                write_diag(f"Added screen: {name}")

            data = load_data()
            self.sm.current = "home" if data.get("disclaimer_accepted") else "get_started"
            write_diag(f"Initial screen: {self.sm.current}")

            Window.bind(on_keyboard=self.on_keyboard)
            return self.sm
        except Exception:
            write_diag("BUILD FAILED:")
            write_diag(traceback.format_exc())
            raise

    def on_start(self):
        Clock.schedule_once(self._init_screens, 0.2)

    def _init_screens(self, dt):
        try:
            self.sm.get_screen("bp").update_history()
        except Exception as e:
            write_diag(f"bp init err: {e}")
        try:
            self.sm.get_screen("sugar").update_history()
        except Exception as e:
            write_diag(f"sugar init err: {e}")
        try:
            self.sm.get_screen("medication").update_list()
            self.sm.get_screen("medication").reschedule_all()
        except Exception as e:
            write_diag(f"med init err: {e}")

    def accept_disclaimer(self):
        data = load_data()
        data["disclaimer_accepted"] = True
        save_data(data)
        self.sm.current = "home"

    def go_home(self):
        self.sm.current = "home"

    def on_keyboard(self, window, key, *args):
        if key == 27:
            if self.sm.current in ("home", "get_started"):
                return False
            self.sm.current = "home"
            return True
        return False

if __name__ == "__main__":
    try:
        write_diag("Running HealthApp...")
        HealthApp().run()
    except Exception:
        write_diag("MAIN CRASHED:")
        write_diag(traceback.format_exc())
        raise
