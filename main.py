import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import socket
import threading
from kivy.clock import Clock
from functools import partial
kivy.require("2.1.0")


class MyRoot(BoxLayout):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def __init__(self):
        super(MyRoot, self).__init__()

    def send_message(self):
        self.client.send(f'{self.nickname_text.text}: {self.message_text.text}'.encode('utf-8'))

    def connect_to_server(self):
        if self.nickname_text != "":
            self.client.connect((self.ip_text.text, 9999))
            message = self.client.recv(1024).decode('utf-8')
            if message == "NICK":
                self.client.send(self.nickname_text.text.encode('utf-8'))
                self.send_btn.disabled = False
                self.message_text.disabled = False
                self.connect_btn.disabled = True
                self.ip_text.disabled = True

                self.make_invisible(self.connection_grid)
                self.make_invisible(self.connect_btn)

                thread = threading.Thread(target=self.receive)
                thread.start()


    def make_invisible(self, widget):
        widget.visible = False
        widget.size_hint_x = None
        widget.size_hint_y = None
        widget.height = 0
        widget.width = 0
        widget.text = ""
        widget.opacity = 0

    def chat(self,message,*args):
        self.chat_text.text += message + "\n"

    def receive(self):
        stop = False
        while not stop :
            try:
                message = self.client.recv(1024).decode('utf-8')
                Clock.schedule_once(partial(self.chat,message))
            except:
                print("ERROR")
                self.client.close()
                stop = True


class Interface(App):
    def build(self):
        return MyRoot()


interface = Interface()
interface.run()
