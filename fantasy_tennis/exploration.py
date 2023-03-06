import sqlwrapper
import pandas as pd 

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

db = connect_to_database('./fantasy_tennis/players_points.db')


res = db.select("""
SELECT * FROM players_points
WHERE player_name == 'Andy Murray'
ORDER BY week_begin 
""")

print(res)