import sqlite3

class DBCursor:
    def __init__(self):
        self.db_name = 'PhoneBooks.db'
        self.db_table_name = 'Names'
        self.db_connector = sqlite3.connect(self.db_name)
        self.db_cursor = self.db_connector.cursor()

    def add_to_db(self, id, first, second, phone):
        query_add = """INSERT INTO TABLE `%s` (`ID`, `First Name`, `Surname` ,`Phone Number`)
                        VALUES (%s, %s, %s, %s)""" % (self.db_table_name, id, first, second, phone) 

        self.db_cursor.execute(query_add)
        self.db_connector.commit()

    def delete_from_db(self, id):
        query_delete = """DELETE FROM `%s` WHERE `ID` = %s """ % (self.db_table_name, id)

        self.db_cursor.execute(query_delete)
        self.db_connector.commit()

    def search_in_db(self, surname):
        query_search = """SELECT * FROM `%s` WHERE `Surname` = `%s`""" % (self.db_table_name, surname)

        self.db_cursor.execute(query_search)

        return self.db_cursor.fetchall()

    def view_all_data(self):
        query_all_data = """SELECT * FROM `%s`""" % (self.db_table_name)

        self.db_cursor.execute(query_all_data)

        return self.db_cursor.fetchall()
