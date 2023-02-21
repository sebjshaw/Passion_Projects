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

def parse_tags_from_soup(soup: bs4.BeautifulSoup, class_name: str, values: list) -> list:
    """Adds the text of the specified tags to a list 

    Args:
        soup (bs4.BeautifulSoup): The web page html soup
        class_name (str): The name of the class that is being searched 
        values (list): The list of values to be added to 

    Returns:
        list: a list of the desired values  
    """

    for value in soup.find_all("td", class_=class_name)[:50]:
        values.append(value.text)

    return values 

def create_current_player_points_dictionary(player_names: list, player_points: list) -> dict:
    """Creates a dictionary of players with key value pairs of player name and player points 

    Args:
        player_names (list): List of all the player names
        player_points (list): List of all the player points 

    Returns:
        dict: key value pairs of names and points  
    """ 
    players = {}

    for name, points in zip(player_names, player_points):
        players[name] = points
    
    return players


if __name__ == "__main__":
    player_names = []
    player_points = []
    for url in URLS:
        soup = get_html_soup(URLS[url])
        player_names = parse_tags_from_soup(soup, CLASSES[0], player_names)
        player_points = parse_tags_from_soup(soup, CLASSES[1], player_points)

    players = create_current_player_points_dictionary(player_names, player_points)
    print(players)