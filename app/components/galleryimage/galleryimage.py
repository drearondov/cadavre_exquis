from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout


class GalleryImage(BoxLayout):
    image_source = StringProperty("")
    image_title = StringProperty("")

    def __init__(self, **kwargs):
        super(GalleryImage, self).__init__(**kwargs)