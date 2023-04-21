import ast
import pandas as pd
import random

from typing import List
from kivy.uix.screenmanager import Screen

from app.components.poettoggle.poettogle import PoetToggle


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)
        self.in_game_poets = []
        self.bag_of_words = []

    def populate_screen(self) -> None:
        poets = pd.read_csv("assets/data/poets_data.csv")

        for poet_name in poets["full_name"].unique():
            poet_data = poets.loc[poets["full_name"] == poet_name]
            poet_bio = poet_data["bio"].values[0]

            poet_toggle = PoetToggle(poet_name=poet_name)
            self.ids["poets_menu"].add_widget(poet_toggle)

    def get_selected_poets(self) -> List:
        selected_poets = []

        for poet in self.ids["poets_menu"].children:
            if poet.state == "down":
                selected_poets.append(poet.poet_name)
            else:
                pass

            if len(selected_poets) > 4:
                print("Can't select more than 4 poets")

        return selected_poets

    def start_game(self) -> None:
        poems = pd.read_csv("assets/data/poems_data.csv", usecols=[1, 2, 3, 4])
        selected_poets = self.get_selected_poets()

        bag_of_words = list()

        for poet in selected_poets:
            filtered_poem = poems.loc[poems["full_name"] == poet].sample(1)

            poem_text = filtered_poem["poem"].apply(ast.literal_eval)
            poem_text = list(poem_text.tolist()[0])

            stop_words = filtered_poem["stop_words"].apply(ast.literal_eval)
            stop_words = list(stop_words.tolist()[0])

            try:
                selected_words = random.sample(poem_text, 25)
            except ValueError:
                selected_words = poem_text

            try:
                selected_stop = random.sample(stop_words, 25)
            except ValueError:
                selected_stop = stop_words

            poem_words = selected_words + selected_stop
            bag_of_words += poem_words

            random.shuffle(bag_of_words)

            self.in_game_poets.append({"poet": poet, "poem": filtered_poem["title"]})

        self.bag_of_words = bag_of_words
        self.manager.current = "game_screen"
        self.manager.ids["game_screen"].populate_screen(bag_of_words)
