from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout


class BioView(BoxLayout):
    poet_name = StringProperty("Poet Name")
    poet_bio = StringProperty("Poet Bio")

    def __init__(self, **kwargs):
        super(BioView, self).__init__(**kwargs)
