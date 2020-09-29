import sqlite3

class DBCursor:
    def __init__(self):
        self.db_name = 'PhoneBooks.db'
        # self.db_table_name = 'Names'
        self.db_connector = sqlite3.connect(self.db_name)
        self.db_cursor = self.db_connector.cursor()

    def add_to_db(self, id, first, second, phone):
        query_add = """INSERT INTO Names (`ID`, `First Name`, `Surname` ,`Phone Number`)
                        VALUES (%s, '%s', '%s', '%s')""" % (id, first, second, phone) 

        self.db_cursor.execute(query_add)
        # print('1234')
        if self.db_cursor:
            # print('sdf1234')
            # print(self.db_cursor)
            self.db_connector.commit()
        else:
            print('FUCK')

    def __find_by_id(self, id):
        query_find_id = """SELECT * FROM `Names` WHERE `ID` = '%s' """ % (id,)

        self.db_cursor.execute(query_find_id)
        return self.db_cursor.fetchall()

    def delete_from_db(self, id):
        query_delete = """DELETE FROM `Names` WHERE `ID` = '%s' """ % (id)
        record_by_id = self.__find_by_id(id)

        if record_by_id:
            self.db_cursor.execute(query_delete)
            self.db_connector.commit()
            return ['Sucess', record_by_id]
        else:
            return 'Failure'

    def search_in_db(self, surname):
        query_search = """SELECT * FROM `Names` WHERE `Surname` = '%s'""" % (surname)

        self.db_cursor.execute(query_search)

        return self.db_cursor.fetchall()

    def view_all_data(self):
        query_all_data = """SELECT * FROM `Names`"""

        self.db_cursor.execute(query_all_data)

        return self.db_cursor.fetchall()

    def delete_all_records(self):
        query_delete_records = """DELETE FROM `Names` """

        self.db_cursor.execute(query_delete_records)
        self.db_connector.commit()
        self.db_connector.close()
    
    def drop_table(self):
        query_drop_table = """DROP TABLE `Names`"""

        self.db_cursor.execute(query_drop_table)
        self.db_connector.commit()
        self.db_connector.close()
