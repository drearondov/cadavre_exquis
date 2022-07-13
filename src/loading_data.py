import json
import requests
import re

from bs4 import BeautifulSoup as BSoup


def get_poet_bio(bio_link: str) -> str:
    """Gets poet's bio fron Poetrysoup

    Args:
        bio_link (str): Link to request poet's bio

    Returns:
        poet_bio str: Sting containing the poet's bio
    """
    bio_page = requests.get(bio_link)


def get_poet_poems(poems_link: str) -> list:
    """Gets poets poems from Poetrtysoup

    Args:
        poems_link (str): Link to request poet's poems

    Returns:
        poet_poems (list): List containing th poet's poems
    """
    poems_page = requests.get(poems_link)
    poems_soup = BSoup(poems_page.content, "html.parser")

    poems_table = poems_soup.find(id="ContentPane_GridView1")
    poems = poems_table.find_all("tr", class_=re.compile("rowstyle"))

    poem_list = []

    for poem in poems:
        poem_title_element = poem.find("h2")
        poem_text_element = poem.find("pre")

        poem_list.append(dict(title=poem_title_element.text, poem=poem_text_element.text))

    return poem_list


def get_poet_quotes(quotes_link: str) -> list:
    """Gets poets poems from Poetrtysoup

    Args:
        poems_link (str): Link to request poet's poems

    Returns:
        poet_poems (list): List containing th poet's poems
    """
    quotes_page = requests.get(quotes_link)
    quotes_soup = BSoup(quotes_page.content, "html.parser")

    quotes_table = quotes_soup.find(id="ContentPane_GridView1")
    quotes = quotes_table.find_all("tr", class_=re.compile("rowstyle"))

    if quotes == []:
        return []

    quotes_list = []

    for quote in quotes:
        quote_element = quote.find("em")

        quotes_list.append(quote_element.text)

    return quotes_list

if __name__ == "__main__":

    ## Getting Web Page Data
    POETS_URL = "https://www.poetrysoup.com/famous/poets/best_poets_all_time.aspx"

    poets_page = requests.get(POETS_URL)


    ## Scrapping each poet's basic data
    poets_soup = BSoup(poets_page.content, "html.parser")

    poets_table = poets_soup.find(id="ContentPane_GridView1")

    poets = poets_table.find_all("tr", class_=re.compile("rowstyle"))

    poet_list = []

    for poet in poets:
        poet_name_element = poet.find("b")
        poet_bio_element = poet.find("p")

        poet_name = poet_name_element.text
        poet_name = poet_name.split(", ")
        
        new_poet_first_name = poet_name[1]
        new_poet_last_name = poet_name[0]

        BIO_URL = f"https://www.poetrysoup.com/{new_poet_first_name.lower().replace(' ','_')}_{new_poet_last_name.lower().replace(' ', '_')}/biography"
        POEMS_URL = f"https://www.poetrysoup.com/famous/poems/best/{new_poet_first_name.lower().replace(' ','_')}_{new_poet_last_name.lower().replace(' ', '_')}"
        QUOTES_URL = f"https://www.poetrysoup.com/quotes/{new_poet_first_name.lower().replace(' ','_')}_{new_poet_last_name.lower().replace(' ', '_')}"

        new_poet_bio = poet_bio_element.text
        new_poet_poems = get_poet_poems(POEMS_URL)
        new_poet_quotes = get_poet_quotes(QUOTES_URL)

        new_poet = dict(
            first_name=new_poet_first_name,
            last_name=new_poet_last_name,
            bio=new_poet_bio,
            poems=new_poet_poems,
            quotes=new_poet_quotes
        )

        poet_list.append(new_poet)

    with open("assets/data/raw_data.json", "a") as file:
        json.dump(poet_list, file)
    