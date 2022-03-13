from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.properties import NumericProperty, BooleanProperty, StringProperty
from kivy.config import Config
import requests
import os

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

def call_api_save_image(email):
    r = requests.get("http://127.0.0.1:5000/api/v1/set_image/"+email)
    data = r.content
    url = r.request.url
    image_name = url.rsplit('/', 1)[-1]
    image_type = url.rsplit(".",1)[-1]
    with open(image_name, 'wb') as x:
        x.write(data)
    os.rename(image_name, 'set_image' + '.' + image_type)
    return ('set_image' + '.' + image_type)

class MainWindow(Screen):
    def on_pre_enter(self):
        Window.size = (750,400)
        Window.clearcolor = (1, 1, 1, 1)

    def checkbox_click(self, instance, value):
        return value

    def checkbox_click_mode(self, instance, value):

        return value

    def checkbox_click_stretch(self, instance, value):
        return value

    def disable_button(self):
        if self.ids.checkbox_confirm_email.active == False:
            self.ids.submit_button.disabled = True
        else:
            self.ids.submit_button.disabled = False

class SecondWindow(Screen):
    angle = NumericProperty(0)
    allow_strech = BooleanProperty(False)
    sources = StringProperty('set_image.jpg')
    user_input_email = StringProperty('troy@gmail.com')
    def on_pre_enter(self):
        screen = self.manager.get_screen("main")
        angle_value = screen.ids.checkbox_confirm_mode.active
        stretch_value = screen.ids.checkbox_confirm_stretch.active
        user_input_email = screen.ids.user_email_input.text.strip()
        shown_image = call_api_save_image(user_input_email)
        self.sources = shown_image
        self.angle = 90*angle_value # Less calculation.
        self.allow_strech = stretch_value # Less calculation.
        Window.fullscreen = 'auto'
        Window.clearcolor = (0,0,0,0)


class WindowManager(ScreenManager):
    pass

class MyMainApp(App):
    def build(self):
        return kv

kv = Builder.load_file("my.kv")

if __name__ == "__main__":
    MyMainApp().run()