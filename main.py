from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy_garden.webview import WebView
import os

class MedicalApp(App):
    def build(self):
        self.title = "Medical Abbreviations"
        layout = BoxLayout()
        html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html')
        self.webview = WebView(url=f"file://{html_path}")
        layout.add_widget(self.webview)
        return layout

if __name__ == '__main__':
    MedicalApp().run()
