import json

from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from app.components.galleryimage.galleryimage import GalleryImage


class GalleryScreen(Screen):
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)

        
    def populate_screen(self):

        with open("private/gallery.json", "r") as gallery_file:
            image_list = json.load(gallery_file)

        if image_list == []:
            scroll_view = self.ids["gallery_scroll"]
            box_layout = scroll_view.parent
            box_layout.remove_widget(scroll_view)
            box_layout.add_widget(Label(text="Nada aún, haz tu primer poema!"))

            return

        for image in image_list:

            gallery_item = GalleryImage(image_source=image["source"], image_title=image["title"])
            self.ids["gallery_list"].add_widget(gallery_item)