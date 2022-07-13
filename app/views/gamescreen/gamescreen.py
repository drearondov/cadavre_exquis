from datetime import datetime
import json
from kivy.uix.screenmanager import Screen

from app.components.wordlabel.wordlabel import WordLabel
from app.components.finishmodal.finishmodal import FinishModal

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)

    def populate_screen(self, bag_of_words):
        self.clear_words()
        for word in bag_of_words:
            word_label = WordLabel(text=word, size_hint=(None, 0.05), width=len(word)*40, background_down = "assets/img/button_dark.png")
            self.ids["bag_of_words"].add_widget(word_label)

    def clear_words(self):
        for children in self.ids["bag_of_words"].children:
            self.ids["bag_of_words"].remove_widget(children)
        

    def finish_game(self):
        finsih_modal = FinishModal()
        finsih_modal.open()

    def save_image(self, title):
        path = f"private/img/{title}-{datetime.now()}.png"

        self.ids["bag_of_words"].export_to_png(path)

        with open("private/gallery.json", "r") as gallery_file:
            image_list = json.load(gallery_file)

        image_list.append({"title": title, "source": path})

        with open("private/gallery.json", "w") as gallery_file: 
            json.dump(image_list, gallery_file)

        self.manager.ids["gallery_screen"].populate_screen()
        self.manager.current = "gallery_screen"
