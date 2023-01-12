from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.screen import MDScreen
from Barcode_Scanner import Barcode_Scanner_Label
from kivymd.uix.button.button import MDRaisedButton
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.metrics import Metrics

Window.size = (360, 640)


class MainScreen(MDScreen):

    def scan(self):
        print("działa!")


class WindowManager(ScreenManager):
    pass


class MyApp(MDApp):

    def build(self):
        root = Builder.load_file("main_page.kv")

        return root


if __name__ == '__main__':
    MyApp().run()
