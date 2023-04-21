import os

os.environ["KIVY_IMAGE"] = "sdl2"
os.environ["KIVY_VIDEO"] = "ffpyplayer"

import kivy

kivy.require("2.1.0")


from kivy.config import Config

Config.set("graphics", "width", "1080")
Config.set("graphics", "height", "810")

from kivy.app import App

from app.views.homescreen.homescreen import HomeScreen
from app.views.menuscreen.menuscreen import MenuScreen
from app.views.gamescreen.gamescreen import GameScreen
from app.views.aboutscreen.aboutscreen import AboutScreen
from app.views.demoscreen.demoscreen import DemoScreen
from app.views.bioscreen.bioscreen import BioScreen
from app.views.galleryscreen.galleryscreen import GalleryScreen


class MainApp(App):
    def build(self):
        self.title = "Poetas Exquisitos"
        self.icon = "assets/img/logo.png"

    def on_start(self):
        self.root.current = "home_screen"


if __name__ == "__main__":
    MainApp().run()
