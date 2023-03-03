import sqlite3
import pandas as pd


class SQLConnection:

    def __init__(self, path) -> None:
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()

    def q(self, query: str) -> tuple:
        """Takes a query and executes it returning the result of the query

        Args:
            query (str): the query to be executed on the database 

        Returns:
            tuple: returns the result of the query 
        """
        try:
            res = self.cursor.execute(query)
            self.conn.commit()
            return res
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
        except:
            return('Failed to append to table')