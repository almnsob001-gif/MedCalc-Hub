import os
import json
import traceback
from datetime import datetime, timedelta

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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "health_app_data.json")
STARTUP_LOG = os.path.join(BASE_DIR, "startup_log.txt")

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

# ============================================================
# ==================  Custom Rules  =========================
# ============================================================

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

# ============================================================
# ==================  Screens  ==============================
# ============================================================

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
            Color:
                rgba: 1, 1, 1, 0.05
            Ellipse:
                pos: -dp(90), self.height - dp(150)
                size: dp(240), dp(240)
            Color:
                rgba: 1, 1, 1, 0.05
            Ellipse:
                pos: self.width - dp(100), -dp(60)
                size: dp(180), dp(180)
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
                        rgba: 1, 1, 1, 0.08
                    Ellipse:
                        pos: self.pos
                        size: self.size
                    Color:
                        rgba: 1, 1, 1, 0.18
                    Ellipse:
                        pos: self.x + dp(16), self.y + dp(16)
                        size: dp(108), dp(108)
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
            BoxLayout:
                size_hint_y: None
                height: dp(78)
                spacing: dp(6)
                BoxLayout:
                    orientation: "vertical"
                    BoxLayout:
                        canvas.before:
                            Color:
                                rgba: 1, 1, 1, 0.1
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size
                                radius: [dp(12)]
                        MDIcon:
                            icon: "calculator"
                            font_size: "22sp"
                            theme_text_color: "Custom"
                            text_color: 1, 1, 1, 0.9
                            pos_hint: {"center_x": .5, "center_y": .5}
                    MDLabel:
                        text: "BMI"
                        halign: "center"
                        font_size: "9sp"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 0.6
                        size_hint_y: None
                        height: dp(14)
                BoxLayout:
                    orientation: "vertical"
                    BoxLayout:
                        canvas.before:
                            Color:
                                rgba: 1, 1, 1, 0.1
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size
                                radius: [dp(12)]
                        MDIcon:
                            icon: "heart-pulse"
                            font_size: "22sp"
                            theme_text_color: "Custom"
                            text_color: 1, 1, 1, 0.9
                            pos_hint: {"center_x": .5, "center_y": .5}
                    MDLabel:
                        text: "BP"
                        halign: "center"
                        font_size: "9sp"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 0.6
                        size_hint_y: None
                        height: dp(14)
                BoxLayout:
                    orientation: "vertical"
                    BoxLayout:
                        canvas.before:
                            Color:
                                rgba: 1, 1, 1, 0.1
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size
                                radius: [dp(12)]
                        MDIcon:
                            icon: "water"
                            font_size: "22sp"
                            theme_text_color: "Custom"
                            text_color: 1, 1, 1, 0.9
                            pos_hint: {"center_x": .5, "center_y": .5}
                    MDLabel:
                        text: "Sugar"
                        halign: "center"
                        font_size: "9sp"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 0.6
                        size_hint_y: None
                        height: dp(14)
                BoxLayout:
                    orientation: "vertical"
                    BoxLayout:
                        canvas.before:
                            Color:
                                rgba: 1, 1, 1, 0.1
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size
                                radius: [dp(12)]
                        MDIcon:
                            icon: "pill"
                            font_size: "22sp"
                            theme_text_color: "Custom"
                            text_color: 1, 1, 1, 0.9
                            pos_hint: {"center_x": .5, "center_y": .5}
                    MDLabel:
                        text: "Meds"
                        halign: "center"
                        font_size: "9sp"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 0.6
                        size_hint_y: None
                        height: dp(14)
            MDRaisedButton:
                text: "GET STARTED"
                size_hint_y: None
                height: dp(52)
                size_hint_x: 1
                md_bg_color: 1, 1, 1, 1
                text_color: 0.05, 0.33, 0.62, 1
                on_release: app.sm.current = "disclaimer"
            MDLabel:
                text: "v1.0.0"
                halign: "center"
                font_size: "10sp"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 0.4
                size_hint_y: None
                height: dp(18)

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
                    height: dp(240)
                    BoxLayout:
                        size_hint: None, None
                        size: dp(72), dp(72)
                        pos_hint: {"center_x": .5}
                        canvas.before:
                            Color:
                                rgba: 1.0, 0.60, 0.0, 0.15
                            Ellipse:
                                pos: self.pos
                                size: self.size
                        MDIcon:
                            icon: "alert"
                            font_size: "38sp"
                            theme_text_color: "Custom"
                            text_color: 1.0, 0.60, 0.0, 1
                            pos_hint: {"center_x": .5, "center_y": .5}
                    MDLabel:
                        text: "Please Read Carefully"
                        halign: "center"
                        font_size: "17sp"
                        bold: True
                        size_hint_y: None
                        height: dp(28)
                    MDLabel:
                        text: "This app is for informational purposes only and does not replace professional medical advice."
                        halign: "center"
                        text_size: self.width, None
                        font_size: "13sp"
                        theme_text_color: "Secondary"
                        size_hint_y: None
                        height: dp(80)
                Card:
                    height: dp(190)
                    BoxLayout:
                        size_hint_y: None
                        height: dp(36)
                        spacing: dp(10)
                        MDIcon:
                            icon: "check"
                            font_size: "20sp"
                            theme_text_color: "Custom"
                            text_color: 0.20, 0.65, 0.32, 1
                            size_hint: None, None
                            size: dp(24), dp(24)
                            pos_hint: {"center_y": .5}
                        MDLabel:
                            text: "Results are not a diagnosis"
                            font_size: "12sp"
                            size_hint_y: None
                            height: dp(20)
                            pos_hint: {"center_y": .5}
                    BoxLayout:
                        size_hint_y: None
                        height: dp(36)
                        spacing: dp(10)
                        MDIcon:
                            icon: "check"
                            font_size: "20sp"
                            theme_text_color: "Custom"
                            text_color: 0.20, 0.65, 0.32, 1
                            size_hint: None, None
                            size: dp(24), dp(24)
                            pos_hint: {"center_y": .5}
                        MDLabel:
                            text: "Not a medical prescription"
                            font_size: "12sp"
                            size_hint_y: None
                            height: dp(20)
                            pos_hint: {"center_y": .5}
                    BoxLayout:
                        size_hint_y: None
                        height: dp(36)
                        spacing: dp(10)
                        MDIcon:
                            icon: "check"
                            font_size: "20sp"
                            theme_text_color: "Custom"
                            text_color: 0.20, 0.65, 0.32, 1
                            size_hint: None, None
                            size: dp(24), dp(24)
                            pos_hint: {"center_y": .5}
                        MDLabel:
                            text: "Always consult your doctor first"
                            font_size: "12sp"
                            size_hint_y: None
                            height: dp(20)
                            pos_hint: {"center_y": .5}
        BoxLayout:
            size_hint_y: None
            height: dp(84)
            padding: dp(16), dp(16)
            canvas.before:
                Color:
                    rgba: 1, 1, 1, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
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
            BoxLayout:
                size_hint: None, None
                size: dp(56), dp(56)
                pos_hint: {"center_y": .5}
                canvas.before:
                    Color:
                        rgba: 1, 1, 1, 0.2
                    Ellipse:
                        pos: self.pos
                        size: self.size
                MDIcon:
                    icon: "heart-pulse"
                    font_size: "30sp"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1
                    pos_hint: {"center_x": .5, "center_y": .5}
            BoxLayout:
                orientation: "vertical"
                pos_hint: {"center_y": .5}
                MDLabel:
                    text: "Health App"
                    font_size: "20sp"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1
                    size_hint_y: None
                    height: dp(26)
                MDLabel:
                    text: "Track your health daily"
                    font_size: "12sp"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 0.85
                    size_hint_y: None
                    height: dp(20)
            Button:
                size_hint: None, None
                size: dp(44), dp(44)
                pos_hint: {"center_y": .5}
                background_normal: ""
                background_down: ""
                background_color: 0, 0, 0, 0
                on_release: app.reset_welcome()
                MDIcon:
                    icon: "refresh"
                    font_size: "22sp"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 0.85
                    pos_hint: {"center_x": .5, "center_y": .5}
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
                    subtitle_text: "Track BP readings"
                    icon_color: 0.91, 0.30, 0.24, 1
                    icon_bg_color: 0.91, 0.30, 0.24, 0.15
                    on_release: app.sm.current = "bp"
                FeatureCard:
                    icon_name: "water"
                    title_text: "Blood Sugar"
                    subtitle_text: "Log glucose levels"
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
                    subtitle_text: "Reminders and schedule"
                    icon_color: 0.60, 0.30, 0.90, 1
                    icon_bg_color: 0.60, 0.30, 0.90, 0.15
                    on_release: app.sm.current = "medication"

<BMIScreen>:
    BoxLayout:
        orientation: "vertical"
        canvas.before:
            Color:
                rgba: 0.96, 0.96, 0.97, 1
            Rectangle:
                pos: self.pos
                size: self.size
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
                    height: dp(120)
                    BoxLayout:
                        orientation: "horizontal"
                        spacing: dp(16)
                        BoxLayout:
                            size_hint: None, None
                            size: dp(64), dp(64)
                            pos_hint: {"center_y": .5}
                            canvas.before:
                                Color:
                                    rgba: 0.13, 0.59, 0.95, 0.15
                                Ellipse:
                                    pos: self.pos
                                    size: self.size
                            MDIcon:
                                icon: "calculator"
                                font_size: "30sp"
                                theme_text_color: "Custom"
                                text_color: 0.13, 0.59, 0.95, 1
                                pos_hint: {"center_x": .5, "center_y": .5}
                        BoxLayout:
                            orientation: "vertical"
                            pos_hint: {"center_y": .5}
                            MDLabel:
                                text: "LATEST BMI"
                                font_size: "9sp"
                                bold: True
                                theme_text_color: "Secondary"
                                size_hint_y: None
                                height: dp(14)
                            MDLabel:
                                id: bmi_stat
                                text: "--"
                                font_size: "28sp"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: 0.13, 0.59, 0.95, 1
                                size_hint_y: None
                                height: dp(36)
                            MDLabel:
                                id: bmi_stat_cat
                                text: "Not calculated yet"
                                font_size: "11sp"
                                theme_text_color: "Secondary"
                                size_hint_y: None
                                height: dp(16)
                Card:
                    height: dp(260)
                    MDLabel:
                        text: "MEASUREMENTS"
                        font_size: "9sp"
                        bold: True
                        theme_text_color: "Secondary"
                        size_hint_y: None
                        height: dp(16)
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
                    height: dp(200)
                    MDLabel:
                        text: "BMI SCALE"
                        font_size: "9sp"
                        bold: True
                        theme_text_color: "Secondary"
                        size_hint_y: None
                        height: dp(16)
                    BoxLayout:
                        size_hint_y: None
                        height: dp(26)
                        Widget:
                            canvas:
                                Color:
                                    rgba: 0.13, 0.59, 0.95, 0.6
                                Rectangle:
                                    pos: self.pos
                                    size: self.size
                        Widget:
                            size_hint_x: 1.5
                            canvas:
                                Color:
                                    rgba: 0.30, 0.69, 0.31, 0.6
                                Rectangle:
                                    pos: self.pos
                                    size: self.size
                        Widget:
                            canvas:
                                Color:
                                    rgba: 1.0, 0.76, 0.03, 0.6
                                Rectangle:
                                    pos: self.pos
                                    size: self.size
                        Widget:
                            canvas:
                                Color:
                                    rgba: 0.96, 0.26, 0.21, 0.6
                                Rectangle:
                                    pos: self.pos
                                    size: self.size
                    BoxLayout:
                        size_hint_y: None
                        height: dp(20)
                        MDLabel:
                            text: "Under 18.5"
                            font_size: "8sp"
                            halign: "center"
                        MDLabel:
                            text: "Normal 18.5-25"
                            font_size: "8sp"
                            halign: "center"
                            size_hint_x: 1.5
                        MDLabel:
                            text: "Over 25-30"
                            font_size: "8sp"
                            halign: "center"
                        MDLabel:
                            text: "Obese 30+"
                            font_size: "8sp"
                            halign: "center"
                    MDLabel:
                        id: bmi_result
                        text: "--"
                        halign: "center"
                        font_size: "44sp"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: 0.13, 0.59, 0.95, 1
                        size_hint_y: None
                        height: dp(70)
                    BoxLayout:
                        size_hint_y: None
                        height: dp(40)
                        canvas.before:
                            Color:
                                rgba: 0.13, 0.59, 0.95, 0.1
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size
                                radius: [dp(20)]
                        MDLabel:
                            id: bmi_category
                            text: "Enter your measurements above"
                            halign: "center"
                            valign: "center"
                            font_size: "12sp"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: 0.13, 0.59, 0.95, 1

<BPScreen>:
    BoxLayout:
        orientation: "vertical"
        canvas.before:
            Color:
                rgba: 0.96, 0.96, 0.97, 1
            Rectangle:
                pos: self.pos
                size: self.size
        PageHeader:
            title_text: "Blood Pressure"
            subtitle_text: "ACC/AHA Classification"
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
                    height: dp(120)
                    BoxLayout:
                        orientation: "horizontal"
                        spacing: dp(16)
                        BoxLayout:
                            size_hint: None, None
                            size: dp(64), dp(64)
                            pos_hint: {"center_y": .5}
                            canvas.before:
                                Color:
                                    rgba: 0.91, 0.30, 0.24, 0.15
                                Ellipse:
                                    pos: self.pos
                                    size: self.size
                            MDIcon:
                                icon: "heart-pulse"
                                font_size: "30sp"
                                theme_text_color: "Custom"
                                text_color: 0.91, 0.30, 0.24, 1
                                pos_hint: {"center_x": .5, "center_y": .5}
                        BoxLayout:
                            orientation: "vertical"
                            pos_hint: {"center_y": .5}
                            MDLabel:
                                text: "LATEST READING"
                                font_size: "9sp"
                                bold: True
                                theme_text_color: "Secondary"
                                size_hint_y: None
                                height: dp(14)
                            MDLabel:
                                id: bp_stat
                                text: "-- / --"
                                font_size: "24sp"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: 0.91, 0.30, 0.24, 1
                                size_hint_y: None
                                height: dp(32)
                            MDLabel:
                                id: bp_stat_cat
                                text: "No records yet"
                                font_size: "11sp"
                                theme_text_color: "Secondary"
                                size_hint_y: None
                                height: dp(16)
                Card:
                    height: dp(260)
                    MDLabel:
                        text: "NEW READING"
                        font_size: "9sp"
                        bold: True
                        theme_text_color: "Secondary"
                        size_hint_y: None
                        height: dp(16)
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
                    height: dp(130)
                    MDLabel:
                        text: "CLASSIFICATION"
                        font_size: "9sp"
                        bold: True
                        theme_text_color: "Secondary"
                        size_hint_y: None
                        height: dp(16)
                    BoxLayout:
                        size_hint_y: None
                        height: dp(44)
                        canvas.before:
                            Color:
                                rgba: 0.91, 0.30, 0.24, 0.1
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size
                                radius: [dp(22)]
                        MDLabel:
                            id: bp_result
                            text: "Enter your readings"
                            halign: "center"
                            valign: "center"
                            font_size: "14sp"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: 0.91, 0.30, 0.24, 1
                BoxLayout:
                    size_hint_y: None
                    height: dp(30)
                    spacing: dp(8)
                    MDIcon:
                        icon: "history"
                        font_size: "16sp"
                        theme_text_color: "Custom"
                        text_color: 0.91, 0.30, 0.24, 1
                        size_hint: None, None
                        size: dp(18), dp(18)
                        pos_hint: {"center_y": .5}
                    MDLabel:
                        text: "RECENT RECORDS"
                        font_size: "10sp"
                        bold: True
                        theme_text_color: "Secondary"
                        valign: "center"
                BoxLayout:
                    id: bp_history
                    orientation: "vertical"
                    spacing: dp(8)
                    size_hint_y: None
                    height: self.minimum_height

<SugarScreen>:
    BoxLayout:
        orientation: "vertical"
        canvas.before:
            Color:
                rgba: 0.96, 0.96, 0.97, 1
            Rectangle:
                pos: self.pos
                size: self.size
        PageHeader:
            title_text: "Blood Sugar"
            subtitle_text: "Glucose Tracking"
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
                    height: dp(120)
                    BoxLayout:
                        orientation: "horizontal"
                        spacing: dp(16)
                        BoxLayout:
                            size_hint: None, None
                            size: dp(64), dp(64)
                            pos_hint: {"center_y": .5}
                            canvas.before:
                                Color:
                                    rgba: 0.20, 0.65, 0.32, 0.15
                                Ellipse:
                                    pos: self.pos
                                    size: self.size
                            MDIcon:
                                icon: "water"
                                font_size: "30sp"
                                theme_text_color: "Custom"
                                text_color: 0.20, 0.65, 0.32, 1
                                pos_hint: {"center_x": .5, "center_y": .5}
                        BoxLayout:
                            orientation: "vertical"
                            pos_hint: {"center_y": .5}
                            MDLabel:
                                text: "LATEST READING"
                                font_size: "9sp"
                                bold: True
                                theme_text_color: "Secondary"
                                size_hint_y: None
                                height: dp(14)
                            MDLabel:
                                id: sugar_stat
                                text: "-- mg/dL"
                                font_size: "22sp"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: 0.20, 0.65, 0.32, 1
                                size_hint_y: None
                                height: dp(32)
                            MDLabel:
                                text: "Blood glucose level"
                                font_size: "11sp"
                                theme_text_color: "Secondary"
                                size_hint_y: None
                                height: dp(16)
                Card:
                    height: dp(200)
                    MDLabel:
                        text: "NEW READING"
                        font_size: "9sp"
                        bold: True
                        theme_text_color: "Secondary"
                        size_hint_y: None
                        height: dp(16)
                    MDTextField:
                        id: sugar_input
                        hint_text: "Value (mg/dL)"
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
                        text: "CURRENT READING"
                        font_size: "9sp"
                        bold: True
                        theme_text_color: "Secondary"
                        halign: "center"
                        size_hint_y: None
                        height: dp(16)
                    BoxLayout:
                        size_hint_y: None
                        height: dp(44)
                        canvas.before:
                            Color:
                                rgba: 0.20, 0.65, 0.32, 0.1
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size
                                radius: [dp(22)]
                        MDLabel:
                            id: sugar_result
                            text: "Enter your reading"
                            halign: "center"
                            valign: "center"
                            font_size: "14sp"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: 0.20, 0.65, 0.32, 1
                BoxLayout:
                    size_hint_y: None
                    height: dp(30)
                    spacing: dp(8)
                    MDIcon:
                        icon: "history"
                        font_size: "16sp"
                        theme_text_color: "Custom"
                        text_color: 0.20, 0.65, 0.32, 1
                        size_hint: None, None
                        size: dp(18), dp(18)
                        pos_hint: {"center_y": .5}
                    MDLabel:
                        text: "RECENT RECORDS"
                        font_size: "10sp"
                        bold: True
                        theme_text_color: "Secondary"
                        valign: "center"
                BoxLayout:
                    id: sugar_history
                    orientation: "vertical"
                    spacing: dp(8)
                    size_hint_y: None
                    height: self.minimum_height

<CaloriesScreen>:
    BoxLayout:
        orientation: "vertical"
        canvas.before:
            Color:
                rgba: 0.96, 0.96, 0.97, 1
            Rectangle:
                pos: self.pos
                size: self.size
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
                    height: dp(120)
                    BoxLayout:
                        orientation: "horizontal"
                        spacing: dp(16)
                        BoxLayout:
                            size_hint: None, None
                            size: dp(64), dp(64)
                            pos_hint: {"center_y": .5}
                            canvas.before:
                                Color:
                                    rgba: 1.0, 0.60, 0.0, 0.15
                                Ellipse:
                                    pos: self.pos
                                    size: self.size
                            MDIcon:
                                icon: "food-apple"
                                font_size: "30sp"
                                theme_text_color: "Custom"
                                text_color: 1.0, 0.60, 0.0, 1
                                pos_hint: {"center_x": .5, "center_y": .5}
                        BoxLayout:
                            orientation: "vertical"
                            pos_hint: {"center_y": .5}
                            MDLabel:
                                text: "DAILY CALORIES"
                                font_size: "9sp"
                                bold: True
                                theme_text_color: "Secondary"
                                size_hint_y: None
                                height: dp(14)
                            MDLabel:
                                id: cal_stat
                                text: "-- kcal"
                                font_size: "22sp"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: 1.0, 0.60, 0.0, 1
                                size_hint_y: None
                                height: dp(32)
                            MDLabel:
                                text: "Based on your profile"
                                font_size: "11sp"
                                theme_text_color: "Secondary"
                                size_hint_y: None
                                height: dp(16)
                Card:
                    height: dp(420)
                    MDLabel:
                        text: "YOUR INFO"
                        font_size: "9sp"
                        bold: True
                        theme_text_color: "Secondary"
                        size_hint_y: None
                        height: dp(16)
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
                        md_bg_color: 1.0, 0.60, 0.0, 0.15
                        text_color: 1.0, 0.60, 0.0, 1
                        size_hint_x: 1
                        on_release: root.cycle_gender()
                    MDRaisedButton:
                        id: activity_btn
                        text: "Activity: Sedentary"
                        md_bg_color: 1.0, 0.60, 0.0, 0.15
                        text_color: 1.0, 0.60, 0.0, 1
                        size_hint_x: 1
                        on_release: root.cycle_activity()
                    MDRaisedButton:
                        text: "CALCULATE"
                        md_bg_color: 1.0, 0.60, 0.0, 1
                        pos_hint: {"center_x": .5}
                        size_hint_x: .7
                        on_release: root.calculate()
                Card:
                    height: dp(140)
                    MDLabel:
                        text: "YOUR RESULT"
                        font_size: "9sp"
                        bold: True
                        theme_text_color: "Secondary"
                        halign: "center"
                        size_hint_y: None
                        height: dp(16)
                    BoxLayout:
                        size_hint_y: None
                        height: dp(90)
                        BoxLayout:
                            size_hint: None, None
                            size: dp(90), dp(90)
                            pos_hint: {"center_x": .5, "center_y": .5}
                            canvas.before:
                                Color:
                                    rgba: 1.0, 0.60, 0.0, 0.12
                                Ellipse:
                                    pos: self.pos
                                    size: self.size
                            MDLabel:
                                id: cal_result
                                text: "--"
                                halign: "center"
                                valign: "center"
                                font_size: "20sp"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: 1.0, 0.60, 0.0, 1

<MedicationScreen>:
    BoxLayout:
        orientation: "vertical"
        canvas.before:
            Color:
                rgba: 0.96, 0.96, 0.97, 1
            Rectangle:
                pos: self.pos
                size: self.size
        PageHeader:
            title_text: "Medications"
            subtitle_text: "Reminders & Schedule"
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
                    height: dp(240)
                    MDLabel:
                        text: "NEW REMINDER"
                        font_size: "9sp"
                        bold: True
                        theme_text_color: "Secondary"
                        size_hint_y: None
                        height: dp(16)
                    MDTextField:
                        id: med_name
                        hint_text: "Medication name"
                    MDTextField:
                        id: med_time
                        hint_text: "Time (HH:MM) - e.g. 14:30"
                    MDRaisedButton:
                        text: "ADD REMINDER"
                        md_bg_color: 0.60, 0.30, 0.90, 1
                        pos_hint: {"center_x": .5}
                        size_hint_x: .7
                        on_release: root.add_medication()
                Card:
                    height: dp(280)
                    MDLabel:
                        text: "SCHEDULED"
                        font_size: "9sp"
                        bold: True
                        theme_text_color: "Secondary"
                        size_hint_y: None
                        height: dp(16)
                    MDLabel:
                        id: med_list
                        text: "No medications"
                        font_size: "12sp"
                        size_hint_y: None
                        height: dp(220)
                        text_size: self.width, None
                        valign: "top"
"""

# =========================================================
# ============ Helper Functions =========================
# =========================================================
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def classify_bp(s, d):
    if s < 120 and d < 80:
        return "Normal", [0.30, 0.69, 0.31, 1]
    if 120 <= s <= 129 and d < 80:
        return "Elevated", [1.0, 0.76, 0.03, 1]
    if 130 <= s <= 139 or 80 <= d <= 89:
        return "Stage 1 Hypertension", [1.0, 0.60, 0.0, 1]
    if s >= 140 or d >= 90:
        return "Stage 2 Hypertension", [0.96, 0.26, 0.21, 1]
    return "Unknown", [0.62, 0.62, 0.62, 1]

def classify_sugar(v):
    if v < 70:
        return "Low", [0.13, 0.59, 0.95, 1]
    if v <= 99:
        return "Normal", [0.30, 0.69, 0.31, 1]
    if v <= 125:
        return "Pre-diabetic", [1.0, 0.60, 0.0, 1]
    return "High", [0.96, 0.26, 0.21, 1]

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
            self.ids.bmi_stat.text = f"{bmi:.1f}"
            self.ids.bmi_stat_cat.text = cat
            self.ids.bmi_category.text = cat.upper()
            self.ids.bmi_category.text_color = color
            self.ids.bmi_stat.text_color = color
        except ValueError:
            toast("Please enter valid numbers")

class BPScreen(MDScreen):
    def save_record(self):
        try:
            s = int(self.ids.systolic_input.text)
            d_ = int(self.ids.diastolic_input.text)
            cat, color = classify_bp(s, d_)
            data = load_data()
            data.setdefault("bp_records", []).append({
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "sys": s, "dia": d_, "category": cat})
            save_data(data)
            self.ids.bp_result.text = f"{s}/{d_}  •  {cat}"
            self.ids.bp_result.text_color = color
            self.ids.bp_stat.text = f"{s}/{d_}"
            self.ids.bp_stat_cat.text = cat
            self.ids.bp_stat.text_color = color
            self.ids.systolic_input.text = ""
            self.ids.diastolic_input.text = ""
            self.update_history()
        except ValueError:
            toast("Please enter valid numbers")

    def update_history(self):
        self.ids.bp_history.clear_widgets()
        recs = load_data().get("bp_records", [])
        if not recs:
            self.ids.bp_history.add_widget(MDLabel(
                text="No records yet. Save your first reading above.",
                halign="center",
                font_size="11sp",
                theme_text_color="Secondary",
                size_hint_y=None,
                height=60,
            ))
            return
        last = recs[-1]
        cat, color = classify_bp(last['sys'], last['dia'])
        self.ids.bp_stat.text = f"{last['sys']}/{last['dia']}"
        self.ids.bp_stat_cat.text = cat
        self.ids.bp_stat.text_color = color
        for r in reversed(recs[-10:]):
            cat, color = classify_bp(r['sys'], r['dia'])
            self.ids.bp_history.add_widget(HistoryRow(
                date_text=r['date'],
                value_text=f"{r['sys']}/{r['dia']}",
                category_text=cat,
                status_color=color,
            ))

class SugarScreen(MDScreen):
    def save_record(self):
        try:
            v = float(self.ids.sugar_input.text)
            data = load_data()
            data.setdefault("sugar_records", []).append({
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "value": v})
            save_data(data)
            cat, color = classify_sugar(v)
            self.ids.sugar_result.text = f"{v} mg/dL  •  {cat}"
            self.ids.sugar_result.text_color = color
            self.ids.sugar_stat.text = f"{v} mg/dL"
            self.ids.sugar_stat.text_color = color
            self.ids.sugar_input.text = ""
            self.update_history()
        except ValueError:
            toast("Please enter a valid number")

    def update_history(self):
        self.ids.sugar_history.clear_widgets()
        recs = load_data().get("sugar_records", [])
        if not recs:
            self.ids.sugar_history.add_widget(MDLabel(
                text="No records yet. Save your first reading above.",
                halign="center",
                font_size="11sp",
                theme_text_color="Secondary",
                size_hint_y=None,
                height=60,
            ))
            return
        last = recs[-1]
        cat, color = classify_sugar(last['value'])
        self.ids.sugar_stat.text = f"{last['value']} mg/dL"
        self.ids.sugar_stat.text_color = color
        for r in reversed(recs[-10:]):
            cat, color = classify_sugar(r['value'])
            self.ids.sugar_history.add_widget(HistoryRow(
                date_text=r['date'],
                value_text=f"{r['value']} mg/dL",
                category_text=cat,
                status_color=color,
            ))

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
            self.ids.cal_result.text = f"{cal:.0f}\nkcal/day"
            self.ids.cal_stat.text = f"{cal:.0f} kcal"
        except ValueError:
            toast("Please enter valid values")

class MedicationScreen(MDScreen):
    def add_medication(self):
        name = self.ids.med_name.text.strip()
        tm = self.ids.med_time.text.strip()
        if not name or not tm:
            return toast("Please enter name and time")
        data = load_data()
        data.setdefault("medications", []).append({"name": name, "time": tm})
        save_data(data)
        self.schedule_notification(name, tm)
        self.ids.med_name.text = ""
        self.ids.med_time.text = ""
        self.update_list()

    def schedule_notification(self, name, time_str):
        try:
            h, m = map(int, time_str.split(":"))
            now = datetime.now()
            target = now.replace(hour=h, minute=m, second=0, microsecond=0)
            if target <= now:
                target += timedelta(days=1)
            Clock.schedule_once(lambda dt: self.send_notification(name),
                                (target - now).total_seconds())
        except Exception as e:
            print("schedule err:", e)

    def send_notification(self, name):
        try:
            from plyer import notification
            notification.notify(title="Medication Reminder",
                                message=f"Time to take {name}",
                                app_name="Health App",
                                timeout=10)
        except Exception as e:
            print("notification err:", e)

    def update_list(self):
        meds = load_data().get("medications", [])
        lines = [f"• {m['name']}\n   at {m['time']}" for m in meds]
        self.ids.med_list.text = "\n\n".join(lines) if lines else "No medications"

# =========================================================
# ============ App ======================================
# =========================================================
class HealthApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"

        try:
            Builder.load_string(KV)
        except Exception:
            with open(os.path.join(BASE_DIR, "kv_error.txt"), "w", encoding="utf-8") as f:
                f.write(traceback.format_exc())
            raise

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
            try:
                self.sm.add_widget(cls(name=name))
            except Exception:
                with open(os.path.join(BASE_DIR, "screen_error.txt"), "w", encoding="utf-8") as f:
                    f.write(f"FAILED SCREEN: {name}\n")
                    f.write(traceback.format_exc())
                raise

        data = load_data()
        self.sm.current = "home" if data.get("disclaimer_accepted") else "get_started"

        try:
            with open(STARTUP_LOG, "w", encoding="utf-8") as f:
                f.write(f"BASE_DIR: {BASE_DIR}\n")
                f.write(f"DATA_FILE: {DATA_FILE}\n")
                f.write(f"DATA_FILE exists: {os.path.exists(DATA_FILE)}\n")
                f.write(f"data: {data}\n")
                f.write(f"disclaimer_accepted: {data.get('disclaimer_accepted')}\n")
                f.write(f"initial_screen: {self.sm.current}\n")
        except Exception:
            pass

        Window.bind(on_keyboard=self.on_keyboard)
        return self.sm

    def on_start(self):
        Clock.schedule_once(self._init_screens, 0.2)

    def _init_screens(self, dt):
        try:
            self.sm.get_screen("bp").update_history()
        except Exception:
            pass
        try:
            self.sm.get_screen("sugar").update_history()
        except Exception:
            pass
        try:
            self.sm.get_screen("medication").update_list()
        except Exception:
            pass

    def accept_disclaimer(self):
        data = load_data()
        data["disclaimer_accepted"] = True
        save_data(data)
        self.sm.current = "home"

    def go_home(self):
        self.sm.current = "home"

    def reset_welcome(self):
    # نُعيد فقط حالة الترحيب، ولا نحذف السجلات
          data = load_data()
          data["disclaimer_accepted"] = False
          save_data(data)
          self.sm.current = "get_started"
          toast("Welcome screen restored! Your records are safe.")

    def on_keyboard(self, window, key, *args):
        if key == 27:
            if self.sm.current in ("home", "get_started"):
                return False
            self.sm.current = "home"
            return True
        return False

if __name__ == "__main__":
    try:
        HealthApp().run()
    except Exception:
        with open(os.path.join(BASE_DIR, "error_log.txt"), "w", encoding="utf-8") as f:
            f.write(traceback.format_exc())
        raise
