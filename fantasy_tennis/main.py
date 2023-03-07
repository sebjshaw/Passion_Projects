# Not perfect as there are tournaments that we're discounting as part of the 
# fantasy competition so I'll just have to look out for that but this will definitely
# work for the majority of the time 

from urllib.request import urlopen
import requests 
from bs4 import BeautifulSoup
import bs4
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta, MO
import sqlwrapper

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

def connect_to_database(path: str) -> sqlwrapper.SQLConnection: 
    """Establishes a connection with the local database to allow querying of the data  

    Args:
        path (str): the path to the database

    Returns:
        sqlwrapper.SQLConnection: the connection established with the database
    """

    try:
        db = sqlwrapper.SQLConnection(path)
    except:
        print("Connection failed")
    
    return db

def create_dataframe_of_last_weeks_total_points(db: sqlwrapper.SQLConnection) -> pd.DataFrame:

    week_begin = str((datetime.today() - relativedelta(weekday=MO(-2))).date())

    df = db.select(f"""
    SELECT * 
    FROM players_points
    WHERE week_begin == '{week_begin}'
    """)

    return df

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

    Returns:
        list: a list of the desired values  
    """
    iter = 50

    # changes iterations to 51 to account for the string 'points' being included 
    # in the list when the specified tags are retrieved
    if class_name == CLASSES[1]:
        iter = 51

    for value in soup.find_all("td", class_=class_name)[:iter]:
        values.append(value.text)

    return values 

def create_dataframe_of_this_weeks_total_points(player_names: list, player_points: list) -> pd.DataFrame:
    new_player_names = []
    for name in player_names:
        split_name = name.split(' ') # splits name 
        first_name = split_name[len(split_name) - 1] # takes last word (the players first name)
        last_name = name.replace(f' {first_name}', '') # removes first name from original string to leave last name only 
        new_player_names.append(f"{first_name} {last_name}") # recombines first and last name and adds to new list

    week_begin = str((datetime.today() - relativedelta(weekday=MO(-1))).date())
    week_begin_list = [week_begin for i in range(250)]
    df = pd.DataFrame(list(zip(new_player_names, player_points, week_begin_list)), columns=['player_name', 'player_total_points', 'week_begin'])

    return df

def create_weeks_points_dict(df_last_week: pd.DataFrame, df_current_week: pd.DataFrame) -> dict:
    """Creates a dictionary of the weekly points difference 

    Args:
        df_last_week (pd.DataFrame): the total points of the players last week 
        df_current_week (pd.DataFrame): the total points of the players this week 

    Returns:
        dict: the difference between last weeks points and this weeks 
    """

    difference = {}
    
    for player in df_current_week['player_name']:
        try:
            current_points = df_current_week[df_current_week['player_name'] == player].values[0][1]
            last_week_points = df_last_week[df_last_week['player_name'] == player].values[0][1]
            difference[player] = int(current_points) - int(last_week_points)
        except:
            difference[player] = (f'{player} entered top 250 this week')



    return difference 

def create_team_weeks_points_dict(team: list, weeks_points: dict) -> dict:
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
            team_points[player] = weeks_points[player]
        except:
            team_points[player] = (f"{player} not entered top 250 yet or fallen out of it")
    
    return team_points

def create_team_points_txt(team_points: dict):
    """Print the team and the points one this week in an aesthetic manner

    Args:
        team_difference (dict): Team points difference from last week 
    """

    with open("team_points.txt", "w") as f:
        for player in team_points:
            if isinstance(team_points[player], int): 
                f.write(f"{player} gained {team_points[player]} points \n")
            else:
                f.write(f"{team_points[player]} \n")


if __name__ == "__main__":

    # establish connection with SQLite database 
    db = connect_to_database('./fantasy_tennis/players_points.db')

    current_week_names = []
    current_week_points = []

    # import last weeks points from database
    df_last_week = create_dataframe_of_last_weeks_total_points(db)

    # for 1-50, 51-100 and 101-150, get player names and points
    for url in URLS:
        soup = get_html_soup(URLS[url])
        current_week_names = parse_tags_from_soup(soup, CLASSES[0], current_week_names)
        current_week_points = parse_tags_from_soup(soup, CLASSES[1], current_week_points)
        current_week_points.remove('Points')

    df_current_week = create_dataframe_of_this_weeks_total_points(current_week_names, current_week_points)
    print(db.append(df_current_week))
    
    # create a dictionary of players and weekly points difference 
    weeks_points = create_weeks_points_dict(df_last_week, df_current_week)

    # dictionary of player differences in team 
    team_points = create_team_weeks_points_dict(MY_TEAM, weeks_points)
    
    create_team_points_txt(team_points)
    