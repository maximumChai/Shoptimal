import sqlite3

class Store:
    def __init__(self, name, db_file="stores.db"):
        self.name = name
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS aisles (
                store TEXT,
                item TEXT,
                aisle INTEGER,
                PRIMARY KEY(store, item)
            )
        """)
        self.conn.commit()

    def get_aisle(self, item):
        self.cursor.execute(
            "SELECT aisle FROM aisles WHERE store=? AND item=?",
            (self.name, item.lower())
        )
        result = self.cursor.fetchone()
        return result[0] if result else None

    def add_item(self, item, aisle):
        self.cursor.execute(
            "INSERT OR REPLACE INTO aisles (store, item, aisle) VALUES (?, ?, ?)",
            (self.name, item.lower(), aisle)
        )
        self.conn.commit()

    def sort_items(self, items, aisle_input_func=None):
        sorted_list = []
        for item in items:
            aisle = self.get_aisle(item)
            if aisle is None:
                if aisle_input_func:
                    aisle = aisle_input_func(item)
                else:
                    aisle = 999
                self.add_item(item, aisle)
            sorted_list.append((item, aisle))
        sorted_list.sort(key=lambda x: x[1])
        return sorted_list
