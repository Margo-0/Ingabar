import json

from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineListItem
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


class InformationIngredientsPage(MDScreen):
    pass


class InformationProductPage(MDScreen):
    productData = None
    passProductName = StringProperty('')


class SearchIngredientsPage(MDScreen):
    getIngr = StringProperty('')

    def search(self):
        self.getIngr = self.print_ingr_text_input.text.upper()
        if self.getIngr == "":
            self.manager.get_screen('search_ingr_page').ids.search_ingr_field.hint_text =  'Field is empty'
            return

        else:

            self.splitted = self.getIngr.split(',')
            print(self.splitted[0])
            secretKey = "RiOrjHCoyneB4MNVV3P60ieFrlLaBP6l"
            accessKey = "bdf0a6c6289df4c7"

            for item in self.splitted:
                self.unified_item = item.strip().replace("/", " ").replace(" ", "+")
                #print(self.unified_item)
                path = f"/ingredient/search/{self.unified_item}?accessKeyId={accessKey}"
                hmac_val = hmac.new(bytes(secretKey, "UTF-8"), path.encode("UTF-8"), hashlib.sha256).hexdigest()
                url = f"http://api.incibeauty.com/ingredient/search/{self.unified_item}?accessKeyId={accessKey}&hmac={hmac_val}"
                response = requests.get(url)
                parsed = response.json()
                print(parsed)
                parsed_ingr = [x for x in parsed['docs'] if x['inci_name'] == item.strip()]

                for ingr in parsed_ingr:
                    ingr_path = f"/ingredient/{ingr['identifier']}?locale=pl_PL&accessKeyId={accessKey}"
                    ingr_hmac = hmac.new(bytes(secretKey, "UTF-8"), ingr_path.encode("UTF-8"), hashlib.sha256).hexdigest()
                    ingr_url = f"http://api.incibeauty.com/ingredient/{ingr['identifier']}?locale=pl_PL&accessKeyId={accessKey}&hmac={ingr_hmac}"
                    ingr_response = requests.get(ingr_url)
                    getInciName = ingr_response.json().get("inci_name")
                    self.InciDescr = ingr_response.json().get("description")
                    self.manager.get_screen('ingr_inf_page').ids.ingr_show.text += f'{getInciName}:  {self.InciDescr}, \n'



class ScanBarcodePage(MDScreen):
    scannedEAN = ''
    EntermanEan = StringProperty('')

    def get_product_by_ean(self, symbols):
        if symbols is not None and len(symbols) > 0:
            symbol = symbols[0]
            data = symbol.data.decode("utf-8")
            if data is not self.scannedEAN:
                self.scannedEAN = data
                self.get_product()

    def get_product(self):

        self.EntermanEan = self.enter_ean_man.text

        if self.EntermanEan:
            self.scannedEAN = self.EntermanEan
        else:
            if self.scannedEAN == '':
                self.manager.get_screen('second_page').ids.enter_ean.hint_text =  'Field is empty'
                return

        secretKey = "RiOrjHCoyneB4MNVV3P60ieFrlLaBP6l"
        path = f"/product/composition/{self.scannedEAN}?locale=pl_PL&accessKeyId=bdf0a6c6289df4c7"
        hmac_val = hmac.new(bytes(secretKey, "UTF-8"), path.encode("UTF-8"), hashlib.sha256).hexdigest()
        url = f"https://api.incibeauty.com/product/composition/{self.scannedEAN}?locale=pl_PL&accessKeyId=bdf0a6c6289df4c7&hmac={hmac_val}"
        response = requests.get(url)
        product = response.json()
        name = f"{product['brand']} {product['name']}"
        self.ids.NameOfThePrdct.text = name
        self.manager.get_screen('information_prdct_page').ids.product_name.text = name
        ingr = product.get('compositions')[0].get('ingredients')
        list_of_names = [x['official_name'] for x in ingr]
        print(list_of_names)
        self.manager.get_screen('information_prdct_page').ids.ingr_show.text = ', '.join(list_of_names)
        self.manager.get_screen('information_prdct_page').productData = product


class MainScreen(MDScreen):

    def scan(self):
        print("działa!")


class SearchHistoryPage(MDScreen):
    pass


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
