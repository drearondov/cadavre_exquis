import pandas as pd

from kivy.uix.screenmanager import Screen

from app.components.bioview.bioview import BioView


class BioScreen(Screen):
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)

        
    def populate_screen(self):
        poets = pd.read_csv("assets/data/poets_data.csv")

        for poet_name in poets["full_name"].unique():
            poet_data = poets.loc[poets["full_name"] == poet_name]
            poet_bio = poet_data["bio"].values[0]

            poet_bio = BioView(poet_name=poet_name, poet_bio=poet_bio)
            self.ids["bio_list"].add_widget(poet_bio)