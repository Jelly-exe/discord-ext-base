from typing import Dict

import sqlalchemy


class Database:
    def __init__(self, driver):
        self.engine = sqlalchemy.create_engine(driver)
        self.metadata = sqlalchemy.MetaData()

        self.tables: Dict[str, sqlalchemy.Table] = self._get_tables()

    def get_table(self, name: str) -> sqlalchemy.Table:
        if name.lower() not in self.tables:
            raise KeyError(f"Table {name} does not exist")
        return self.tables[name.lower()]

    def get_engine(self) -> sqlalchemy.Engine:
        return self.engine

    def get_connection(self) -> sqlalchemy.Connection:
        return self.engine.connect()

    def get_metadata(self) -> sqlalchemy.MetaData:
        return self.metadata

    def _get_tables(self) -> Dict[str, sqlalchemy.Table]:
        tables = {}

        for table in self.metadata.tables.keys():
            tables[table.lower()] = Table(table, self.metadata, autoload_with=self.engine)

        return tables
