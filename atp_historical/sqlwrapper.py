import sqlite3
import pandas as pd
from typing import List, Optional, Union
from uuid import uuid4


class SQLConnection:

    def __init__(self, db_name: str = None) -> None:
        self.current_cursor = str(uuid4())
        if db_name is None:
            self.db_name = f'.student_{self.current_cursor}.db'
        else:
            self.db_name = db_name

    def q(self, query: str) -> Optional[List[str]]:
        """Executes a query and returns the result"""
        res = None
        with sqlite3.connect(self.db_name) as con:
            cur = con.cursor()
            for q in query.split(';'):
                try:
                    res = pd.read_sql_query(q.strip(), con)
                except (TypeError, ValueError):
                    pass
        return res

    def connect(self):
        return sqlite3.connect(self.db_name)