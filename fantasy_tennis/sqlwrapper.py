import sqlite3
import pandas as pd
from typing import Union


class SQLConnection:

    def __init__(self, path) -> None:
        self.conn = sqlite3.connect(path, timeout=1)
        self.cursor = self.conn.cursor()

    def select(self, query: str) -> Union[pd.DataFrame, str]:
        """Takes a query and executes it returning the result of the query

        Args:
            query (str): the query to be executed on the database 

        Returns:
            pd.DataFrame: returns the result of the query 
        """
        try:
            res = self.cursor.execute(query)
            res = pd.read_sql_query(query, self.conn)
            self.conn.commit()
            return res
        except Exception as e:
            return (e)
            # return (f"Error executing {query}")
        
    def q(self, query: str) -> str:
        """Execute a generic query that doesn't need the response as a dataframe 

        Args:
            query (str): the query to the database as a string 

        Returns:
            str: outcome of the query (successful or not?)
        """
        try: 
            self.cursor.execute(query)
            self.conn.commit()
            return (f"Successfully executes {query}")
        except:
            return (f"Error executing {query}")
        
    def append(self, df: pd.DataFrame):
        """Takes the new total points from the most recent week and adds them to the table

        Args:
            df (pd.DataFrame): the pandas dataframe to be added to the table
        """

        try:
            df.to_sql('players_points', self.conn, if_exists='append', index=False)
            self.conn.commit()
            return('Successfully appended new points totals')
        except Exception as e:
            return('Points already added for this week')