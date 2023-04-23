from typing import Dict

import sqlalchemy


class Database:
    def __init__(self, driver):
        self.engine = sqlalchemy.create_engine(driver)
        self.metadata = sqlalchemy.MetaData()

        self.tables: Dict[str, sqlalchemy.Table] = self._get_tables()

    def get_engine(self) -> sqlalchemy.Engine:
        return self.engine

    def get_connection(self) -> sqlalchemy.Connection:
        return self.engine.connect()

    def get_metadata(self) -> sqlalchemy.MetaData:
        return self.metadata

    def _get_tables(self) -> Dict[str, sqlalchemy.Table]:
        tables = {}

        for table in self.metadata.tables.keys():
            tables[table] = self.metadata.tables[table]

        return tables
