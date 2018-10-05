from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import TankGame
import re

class TestApp(App):
    def build(self):
        b = BoxLayout(orientation='vertical')
        def on_enter(instance,value):
            if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",value):
                #try to connect
                print(value)
                TankGame.StartGame(value)
                return value
            instance.text = 'invalid ip'
            return value

        def attemptConnection(strAddress):
            Address = strAddress.split(':')
            print(Address[0])
            print(Address[1])
    

        l = Label(text='ERmahGerDd TANKZ!!!!!!!!!!!!! \n\n\n\n\n Enter server IP to join\n      ')
        serverAddress = TextInput(text='127.0.0.1', multiline=False,size_hint_y=None, height = 30)
        i = Button(text='PLAY', height=200)
        i.bind(on_press=lambda x:on_enter(serverAddress,serverAddress.text))  
        b.add_widget(l)
        b.add_widget(serverAddress)
        b.add_widget(i)
        return b

TestApp().run()
