# Need a simple web scraper (need to find what class/id i'm looking for in the elements)

# Need to create a MySQL table and set up a connection so I can query it 
# Don't think I need a databse can, just do a csv file that I recreate every time 

from urllib.request import urlopen
import requests 
from bs4 import BeautifulSoup
import bs4

URLS = {
    "0-50":"https://www.tennisexplorer.com/ranking/atp-men/?t=race", 
    "51-100":"https://www.tennisexplorer.com/ranking/atp-men/?t=race&page=2",
    "101-150":"https://www.tennisexplorer.com/ranking/atp-men/?t=race&page=3"
    }

CLASSES = ["t-name", "long-point"]


def get_html_soup(url:str) -> bs4.BeautifulSoup:
    """Takes the link to a website and returns the html in soup format 

    Args:
        url (str): The url of the page 

    Returns:
        bs4.BeautifulSoup: Web page html soup 
    """
    website = requests.get(url)
    soup = BeautifulSoup(website.content, 'html.parser')
    return soup


def parse_tags_from_soup(soup: bs4.BeautifulSoup, class_name: str) -> list:
    """_summary_

    Args:
        soup (bs4.BeautifulSoup): The web page html soup
        class_name (str): The name of the class that is being searched 

    Returns:
        list: a list of the desired values  
    """

    values = []
    for value in soup.find_all("td", class_=class_name)[:50]:
        values.append(value.text)

    return values 

soup = get_html_soup(URLS["0-50"])
player_names = parse_tags_from_soup(soup, CLASSES[0])
player_points = parse_tags_from_soup(soup, CLASSES[1])
print(player_names, player_points)
print(len(player_names), len(player_points))


# Next Steps
    # Add the 51-100 and 101-150 players to the lists of players and points
    # Parse the two lists into one dictionary of key value pairs of player_name and player_points