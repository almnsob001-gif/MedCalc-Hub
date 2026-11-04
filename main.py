from kivy.config import Config
# إيقاف ميزات الرسم المتقدمة التي تسبب مشكلة تكرار الشاشة في Pydroid
Config.set('graphics', 'multisamples', '0')
Config.set('graphics', 'window_state', 'maximized')

# باقي الكود يبدأ من هنا...
import sqlite3
import os
from kivy.lang import Builder
# ... (باقي الكود كما هو)

import sqlite3
import os

from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
from kivy.metrics import dp
from kivy.core.window import Window

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard

# إجبار الخلفية على اللون الفاتح لمنع مشكلة تكرار الشاشة في Pydroid
Window.clearcolor = (0.96, 0.96, 0.96, 1)

def get_base_dir():
    return os.path.dirname(os.path.abspath(__file__))

def get_db_path():
    return os.path.join(get_base_dir(), 'medical_terms.db')

# تجنب تحميل الملف مرتين إذا كان محملاً مسبقاً
try:
    Builder.load_file(os.path.join(get_base_dir(), 'medical.kv'))
except:
    pass

CATEGORY_COLORS = {
    "Cardiology":         [0.898, 0.263, 0.208, 1],
    "Pulmonology":        [0.129, 0.588, 0.953, 1],
    "Neurology":          [0.611, 0.153, 0.690, 1],
    "Endocrinology":      [0.980, 0.596, 0.000, 1],
    "Gastroenterology":   [0.302, 0.686, 0.290, 1],
    "Nephrology":         [0.000, 0.737, 0.831, 1],
    "Urology":            [0.000, 0.588, 0.533, 1],
    "Hematology":         [0.827, 0.184, 0.184, 1],
    "Infectious Disease": [0.671, 0.278, 0.737, 1],
    "Rheumatology":       [0.976, 0.545, 0.192, 1],
    "Dermatology":        [0.937, 0.388, 0.561, 1],
    "Ophthalmology":      [0.259, 0.475, 0.867, 1],
    "ENT":                [0.337, 0.522, 0.804, 1],
    "Obstetrics":         [0.902, 0.494, 0.659, 1],
    "Gynecology":         [0.800, 0.400, 0.600, 1],
    "Pediatrics":         [0.129, 0.745, 0.608, 1],
    "Psychiatry":         [0.545, 0.467, 0.737, 1],
    "Orthopedics":        [0.451, 0.451, 0.451, 1],
    "Emergency":          [0.855, 0.267, 0.216, 1],
    "Critical Care":      [0.973, 0.373, 0.165, 1],
    "Surgery":            [0.325, 0.400, 0.522, 1],
    "Imaging":            [0.376, 0.490, 0.545, 1],
    "Diagnostics":        [0.396, 0.463, 0.545, 1],
    "Labs":               [0.000, 0.612, 0.647, 1],
    "Vital Signs":        [0.808, 0.255, 0.290, 1],
    "Pharmacology":       [0.667, 0.333, 0.667, 1],
    "Route":              [0.427, 0.596, 0.267, 1],
    "Frequency":          [0.522, 0.502, 0.267, 1],
    "Orders":             [0.545, 0.451, 0.337, 1],
    "Documentation":      [0.333, 0.420, 0.545, 1],
    "Ventilation":        [0.286, 0.549, 0.690, 1],
    "Vascular":           [0.698, 0.204, 0.220, 1],
    "Anatomy":            [0.518, 0.408, 0.325, 1],
}
DEFAULT_COLOR = [0.412, 0.412, 0.412, 1]


class ResultCard(MDCard):
    abbr = StringProperty("")
    full_name = StringProperty("")
    category = StringProperty("")
    accent_color = ListProperty(DEFAULT_COLOR)

    def on_category(self, instance, value):
        self.accent_color = CATEGORY_COLORS.get(value, DEFAULT_COLOR)


class MedicalRoot(MDBoxLayout):
    status_text = StringProperty("Type an abbreviation and press Search")
    stats_text = StringProperty("Loading...")

    def on_kv_post(self, base_widget):
        self.check_database()

    def check_database(self):
        try:
            conn = sqlite3.connect(get_db_path())
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM abbreviations")
            n = cur.fetchone()[0]
            cur.execute("SELECT COUNT(DISTINCT category) FROM abbreviations WHERE category != ''")
            cats = cur.fetchone()[0]
            conn.close()
            self.status_text = "Type an abbreviation and press Search"
            self.stats_text = str(n) + " abbreviations  ·  " + str(cats) + " specialties"
            self.show_welcome()
        except Exception as e:
            self.status_text = "Database error: " + str(e)
            self.stats_text = "Error"

    def show_welcome(self):
        from kivymd.uix.label import MDLabel
        container = self.ids.results_container
        container.clear_widgets()
        container.add_widget(MDLabel(
            text="[size=80][color=aaaaaa]medical-bag[/color][/size]",
            markup=True,
            halign="center",
            size_hint_y=None,
            height=dp(120),
        ))
        container.add_widget(MDLabel(
            text="Search for medical abbreviations",
            halign="center",
            font_style="H6",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(40),
        ))

    def search_abbr(self, query):
        from kivymd.uix.label import MDLabel
        q = query.strip().upper()
        if not q:
            self.status_text = "Please enter an abbreviation"
            return

        try:
            conn = sqlite3.connect(get_db_path())
            cur = conn.cursor()
            cur.execute(
                "SELECT abbr, full_name, category FROM abbreviations "
                "WHERE UPPER(abbr) LIKE ? "
                "ORDER BY (CASE WHEN UPPER(abbr) = ? THEN 0 ELSE 1 END), abbr",
                ('%' + q + '%', q)
            )
            rows = cur.fetchall()
            conn.close()

            container = self.ids.results_container
            container.clear_widgets()

            if not rows:
                self.status_text = "No results for '" + q + "'"
                container.add_widget(MDLabel(
                    text='No expansion found for [b]"' + q + '"[/b]',
                    markup=True,
                    halign="center",
                    font_style="H6",
                    theme_text_color="Secondary",
                    size_hint_y=None,
                    height=dp(60),
                ))
                return

            for abbr, full_name, category in rows:
                container.add_widget(ResultCard(
                    abbr=abbr,
                    full_name=full_name,
                    category=category or "",
                ))
            count = len(rows)
            self.status_text = str(count) + (" result found" if count == 1 else " results found")

        except Exception as e:
            self.status_text = "Error: " + str(e)

    def clear_search(self):
        self.ids.search_input.text = ""
        self.check_database()


class MedicalApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.primary_hue = "700"
        self.theme_cls.theme_style = "Light"
        return MedicalRoot()


if __name__ == '__main__':
    MedicalApp().run()
