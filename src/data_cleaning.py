import pandas as pd
import re
import spacy
import string


def clean_poems(poem_list: list)-> list:
    """Returns clan poems list

    Args:
        poem_list (list): Raw poem List

    Returns:
        list: Clean poem list without extra characters. Title and text
    """

    for poem in poem_list:
        poem["title"] = poem["title"].replace("\r\n", "")
        poem["poem"] = poem["poem"].replace("\r\n", " ")
        poem["poem"] = poem["poem"].replace("\n\n", "\n")
        poem["poem"] = poem["poem"].replace("  ", " ")
        poem["poem"] = poem["poem"].replace("\r", "")

    return poem_list


def token_poems(poem_list:list) -> list:
    """Tokenize the poems

    Args:
        poem_list (list): List of poems in corpus form

    Returns:
        list: Tokenized list
    """
    nlp = spacy.load("en_core_web_sm")

    token_poems = []

    for poem in poem_list:
        poem_text = poem["poem"]
        poem_doc = nlp(poem_text)

        filtered_poem = [token.text for token in poem_doc if not token.is_stop]
        poem_stop = [token.text for token in poem_doc if token.is_stop]

        token_poems.append({"title": poem["title"] ,"poem": set(filtered_poem), "stop_words": set(poem_stop)})

    return token_poems


def clean_text(poem_list: list) -> list:
    """Make poem_text lowercase, remove poem text in square brackets, remove punctuation and remove words containing numbers

    Args:
        poem_list (list): List of poems in corpus form

    Returns:
        list:  List with clean text
    """
    clean_poems = []

    for poem in poem_list:
        poem_text = poem["poem"]

        poem_text = poem_text.lower()
        poem_text = re.sub("[%s]" % re.escape(string.punctuation), "", poem_text)
        poem_text = re.sub("[“”…]", "", poem_text)
        poem_text = re.sub("\n", " ", poem_text)

        clean_poems.append({"title": poem["title"] ,"poem": poem_text})

    return clean_poems


if __name__ == "__main__":
    
    raw_data = pd.read_json("../assets/data/raw_data.json")

    raw_data["quotes"] = raw_data["quotes"].apply(lambda quote_list: [text.replace("\r\n", "") for text in quote_list])
    raw_data["bio"] = raw_data["bio"].apply(lambda bio: bio.replace("\r\n", ""))
    raw_data["poems"] = raw_data["poems"].apply(lambda x: clean_poems(x))

    data = raw_data
    data["full_name"] = data.apply(lambda x: f"{x['first_name']} {x['last_name']}", axis=1)
    data["clean_poems"] = data["poems"].apply(lambda x: clean_text(x))


    data["token_poems"] = data["clean_poems"].apply(lambda x: token_poems(x))
    data.to_csv("../assets/data/clean_data.csv")

    poems_data = data[["full_name", "token_poems"]]
    poems_data = poems_data.explode("token_poems", ignore_index=True)
    poems_data = pd.concat([poems_data.drop(["token_poems"], axis=1), poems_data["token_poems"].apply(pd.Series)], axis=1).drop([0], axis=1)

    poems_data.to_csv("../assets/data/poems_data.csv")

    poets_data = data[["full_name", "bio", "poems", "quotes"]]

    poets_data.to_csv("../assets/data/poets_data.csv")
