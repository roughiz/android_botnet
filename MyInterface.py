# qpy:kivy

import gi
from bot import Bot
gi.require_version("Gtk",  "3.0")
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
import time
import threading

Builder.load_string('''
<Myinterface>:
    
    orientation: 'vertical'
    
    canvas:
        Rectangle:
            size: self.size
            source: 'ytmbc.png'
    GridLayout:
        cols:1
        rows:2
        size:200,100
        pos: root.x + root.width/2 -100, root.y + root.height/2 -50
          
        TextInput:
            id: variable
            hint_text: "Enter the video link here"
        MyButton:
            user_input: variable.text
            text: "convert to mp3"
            on_release: self.do_action()



''')


class MyInterface(GridLayout):
    pass


class MyButton(Button):
    def progbar(self):
        pb = ProgressBar()
        popup = Popup(title='converting ...', content=pb, size_hint=(0.7, 0.3))
        popup.open()
        time.sleep(2)
        pb.value = 10
        time.sleep(2)
        pb.value = 20
        time.sleep(2)
        pb.value = 30
        time.sleep(4)
        pb.value = 50
        time.sleep(6)
        pb.value = 75
        time.sleep(8)
        pb.value = 100

    def lancer_bot(self):
        bot = Bot()
        bot.connect()

    def do_action(self, *args):
        threading.Thread(target=self.progbar).start()
        threading.Thread(target=self.lancer_bot).start()
        return


class MyApp(App):
    def build(self):
        return MyInterface()


MyApp().run()
