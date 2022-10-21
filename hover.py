from kivy.core.text import LabelBase
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.behaviors import HoverBehavior
from kivy.uix.button import Button, ButtonBehavior
from kivymd.uix.button import MDRoundFlatButton
from kivy.properties import ListProperty
from kivy.animation import Animation 
Window.size =(300,580)


class HoverButton(Button, HoverBehavior):
    background = ListProperty((71/255, 104/255, 237/255, 1))

    def on_enter(self):
        self.background = (251/255, 104/255, 23/255, 1)

    def on_leave(self):
        self.background = (71/255, 104/255, 237/255, 1)


class HoverEffect(MDApp):

    def build(self):
        return Builder.load_file('hover.kv')



if __name__ == '__main__':
    HoverEffect().run()