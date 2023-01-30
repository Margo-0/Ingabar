import json

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
import hmac
import hashlib
import requests
from kivy.properties import ObjectProperty, NumericProperty, StringProperty

Window.size = (360, 640)


class InformationPage(MDScreen):
    pass


class SearchIngredientsPage(MDScreen):
    getIngr = StringProperty('')

    def search(self):
        self.getIngr = self.print_ingr_text_input.text
        splitted = self.getIngr.split(',')
        print(splitted[0])
        secretKey = "RiOrjHCoyneB4MNVV3P60ieFrlLaBP6l"
        accessKey = "bdf0a6c6289df4c7"

        for item in splitted:
            unified_item = item.replace(" ", "+")
            print(unified_item)
            path = f"/ingredient/search/{unified_item}?accessKeyId={accessKey}"
            hmac_val = hmac.new(bytes(secretKey, "UTF-8"), path.encode("UTF-8"), hashlib.sha256).hexdigest()
            url = f"http://api.incibeauty.com/ingredient/search/{unified_item}?accessKeyId={accessKey}&hmac={hmac_val}"
            response = requests.get(url)
            parsed = response.json()
            for ingr in parsed['docs']:
                ingr_path = f"/ingredient/{ingr['identifier']}?locale=pl_PL&accessKeyId={accessKey}"
                ingr_hmac = hmac.new(bytes(secretKey, "UTF-8"), ingr_path.encode("UTF-8"), hashlib.sha256).hexdigest()
                ingr_url = f"http://api.incibeauty.com/ingredient/{ingr['identifier']}?locale=pl_PL&accessKeyId={accessKey}&hmac={ingr_hmac}"
                ingr_response = requests.get(ingr_url)
                print(ingr_response.json())


class ScanBarcodePage(MDScreen):
    scannedEAN = ''
    def get_product_by_ean(self, symbols):
        if symbols is not None and len(symbols) > 0:
            symbol = symbols[0]
            data = symbol.data.decode("utf-8")
            if data is not self.scannedEAN:
                self.scannedEAN = data
                self.get_product()

            print(self.scannedEAN)


    def get_product(self):
        secretKey = "RiOrjHCoyneB4MNVV3P60ieFrlLaBP6l"
        path = f"/product/composition/{self.scannedEAN}?locale=pl_PL&accessKeyId=bdf0a6c6289df4c7"
        hmac_val = hmac.new(bytes(secretKey, "UTF-8"), path.encode("UTF-8"), hashlib.sha256).hexdigest()
        url = f"https://api.incibeauty.com/product/composition/{self.scannedEAN}?locale=pl_PL&accessKeyId=bdf0a6c6289df4c7&hmac={hmac_val}"
        response = requests.get(url)
        product = response.json()
        print(response.json())
        print(self.scannedEAN)
        name = f"{product['brand']} {product['name']}"
        self.ids.NameOfThePrdct.text = name


class MainScreen(MDScreen):

    def scan(self):
        print("działa!")


class WindowManager(ScreenManager):
    pass


class MyApp(MDApp):
    def search(self):
        print(self.root.ids.search_ingr_field.text)
    def build(self):
        root = Builder.load_file("main_page.kv")

        return root


if __name__ == '__main__':
    MyApp().run()
