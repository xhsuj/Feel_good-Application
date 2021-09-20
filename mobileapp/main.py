from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager,Screen 
import json,glob,random
from datetime import datetime
from pathlib import Path
from hoverable import HoverBehavior
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
Builder.load_file('design.kv') 

class LoginScreen(Screen): #lowest
    def sign_up(self):
        self.manager.current="sign_up_screen"
    def log_in(self,uname,pword):
        with open("user.json") as file:
            users=json.load(file)
        if uname in users and users[uname]['password']==pword:
            self.manager.current="login_screen_success"
        else:
            self.ids.login_wrong.text="Wrong username/password!"

class RootWidget(ScreenManager): #lower
    pass

class SignUpScreen(Screen):
    def add_user(self,uname,pword):
        with open("user.json") as file:
            users=json.load(file)
        users[uname]={'username':uname,'password':pword,
        "created":datetime.now().strftime("%Y-%m-%d %H-%M-%S")}
        with open("user.json",'w') as file:
            json.dump(users,file)
        self.manager.current="sign_up_screen_success"

class SignUpScreenSuccess(Screen):
    def directmain(self):
        self.manager.transition.direction='right'
        self.manager.current="login_screen"

class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction='right'
        self.manager.current="login_screen"
    def get_quote(self,feel):
        feel=feel.lower()
        print(feel)
        available_feels=glob.glob("quotes/*txt")
        available_feels=[Path(filename).stem for filename in 
                            available_feels]
        if feel in available_feels:
            with open(f"quotes/{feel}.txt") as file:
                quotes=file.readlines()
            self.ids.quote.text=random.choice(quotes)
        else:
            self.ids.quote.text="Try another feeling!"


class ImageButton(ButtonBehavior,HoverBehavior,Image): #ButtonBehavior should be placed first
    pass



class Mainapp(App): #top
    def build(self):
        return RootWidget()


if __name__=="__main__":
    Mainapp().run()

