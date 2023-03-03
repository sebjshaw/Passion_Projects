import sqlite3


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