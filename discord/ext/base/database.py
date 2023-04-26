from typing import Dict, Tuple

import sqlalchemy


class Database:
    def __init__(self, driver: str, tables: Tuple[str, ...]):
        self.engine = sqlalchemy.create_engine(driver)
        self.metadata = sqlalchemy.MetaData()

        self.tableKeys = tables
        self._tables: Dict[str, sqlalchemy.Table] = self._get_tables()

    def get_table(self, name: str) -> sqlalchemy.Table:
        if name.lower() not in self._tables:
            raise KeyError(f"Table {name} does not exist")
        return self._tables[name.lower()]

    def get_engine(self) -> sqlalchemy.Engine:
        return self.engine

    def get_connection(self) -> sqlalchemy.Connection:
        return self.engine.connect()

    def get_metadata(self) -> sqlalchemy.MetaData:
        return self.metadata

    def _get_tables(self) -> Dict[str, sqlalchemy.Table]:
        tables = {}

        for table in self.tableKeys:
            tables[table.lower()] = Table(table, self.metadata, autoload_with=self.engine)

        return tables
