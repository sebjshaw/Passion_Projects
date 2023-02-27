# Not perfect as there are tournaments that we're discounting as part of the 
# fantasy competition so I'll just have to look out for that but this will definitely
# work for the majority of the time 

from urllib.request import urlopen
import requests 
from bs4 import BeautifulSoup
import bs4
import csv

URLS = {
    "0-50":"https://www.tennisexplorer.com/ranking/atp-men/?t=race", 
    "51-100":"https://www.tennisexplorer.com/ranking/atp-men/?t=race&page=2",
    "101-150":"https://www.tennisexplorer.com/ranking/atp-men/?t=race&page=3",
    "151-200":"https://www.tennisexplorer.com/ranking/atp-men/?t=race&page=4",
    "201-250":"https://www.tennisexplorer.com/ranking/atp-men/?t=race&page=5"
    }

CLASSES = ["t-name", "long-point"]

MY_TEAM = [
    'Casper Ruud', 'Rafael Nadal',
    'Borna Coric', 'Alex De Minaur',
    'Maxime Cressy', 'Sebastian Baez',
    'Jenson Brooksby', 'Adrian Mannarino',
    'Andy Murray', 'Nikoloz Basilashvili'
    ]



def import_csv_as_dict() -> dict:

    last_week_points = {}
    with open('/Users/seb/Desktop/passion_projects/fantasty_tennis/players.csv', 'r') as f:
        for row in f:
            data = row.split(',')
            last_week_points[data[0]] = data[1][:-1]

    return last_week_points

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

def create_current_players_points_dictionary(player_names: list, player_points: list) -> dict:
    """Creates a dictionary of players with key value pairs of player name and player points 

    Args:
        player_names (list): List of all the player names
        player_points (list): List of all the player points 

    Returns:
        dict: key value pairs of names and points  
    """ 
    players = {}

    for name, points in zip(player_names, player_points):
        split_name = name.split(' ') # splits name 
        first_name = split_name[len(split_name) - 1] # takes last word (the players first name)
        last_name = name.replace(f' {first_name}', '') # removes first name from original string to leave last name only 
        name = f"{first_name} {last_name}" # recombines first and last name in usual order
        players[name] = points
    
    return players

def create_points_difference_dict(last_week: dict, current_week: dict) -> dict:
    """Creates a dictionary of the weekly points difference 

    Args:
        last_week (dict): the points of the player last week 
        current_week (dict): the points of the player this week 

    Returns:
        dict: the difference between last weeks points and this weeks 
    """

    difference = {}
    try:
        for player in current_week:
            difference[player] = int(current_week[player]) - int(last_week[player])
    except:
        print(f"{player} not in top 150 for consecutive weeks")

    return difference 

def return_points_difference_for_team(team: list, difference: dict) -> dict:
    """Returns the points difference for the players in the specified fantasy team

    Args:
        team (list): list of players in fantasy team
        difference (dict): the points difference of all players

    Returns:
        dict: the points difference for the players in the fantasy team
    """

    team_points = {}
    for player in team:
        try:
            team_points[player] = difference[player]
        except:
            team_points[player] = 0
            print(f"{player} currently not in top 250 or fallen out of top 250")
    
    return team_points

def print_team_points(team_difference: dict):
    """Print the team and the points one this week in an aesthetic manner

    Args:
        team_difference (dict): Team points difference from last week 
    """

    for player in team_difference:
        print(f"{player} gained {team_difference[player]} points")

def export_dict_to_csv(players_dict: dict):
    """Takes the dictionary of player names and points and saves the data as a csv

    Args:
        players_dict (dict): dictionary of players names and points
    """

    with open('/Users/seb/Desktop/passion_projects/fantasty_tennis/players.csv', 'w') as f:
        for player in players_dict:
            f.write(f"{player},{players_dict[player]}\n")


if __name__ == "__main__":

    # import last weeks points from csv 
    last_week = import_csv_as_dict()
    current_week_names = []
    current_week_points = []

    # for 1-50, 51-100 and 101-150, get player names and points
    for url in URLS:
        soup = get_html_soup(URLS[url])
        current_week_names = parse_tags_from_soup(soup, CLASSES[0], current_week_names)
        current_week_points = parse_tags_from_soup(soup, CLASSES[1], current_week_points)
        current_week_points.remove('Points')

    # parse player names and points into dictionary
    current_week = create_current_players_points_dictionary(current_week_names, current_week_points)

    # create a dictionary of players and weekly points difference 
    difference = create_points_difference_dict(last_week, current_week)

    # dictionary of player differences in team 
    team_difference = return_points_difference_for_team(MY_TEAM, difference)
    
    print_team_points(team_difference)

    # save current weeks points as new csv
    export_dict_to_csv(current_week)
    