import sqlite3

db_connector = sqlite3.connect('PhoneBooks.db')
db_cursor = db_connector.cursor()

query_table = """CREATE TABLE IF NOT EXISTS `Names` (
	`ID` integer PRIMARY KEY,
	`First Name` text NOT NULL,
	`Surname` text NOT NULL,
	`Phone Number` text NOT NULL);"""

query_values = """INSERT INTO Names(`ID`, `First Name`, `Surname`, `Phone Number`)
                    VALUES('1', 'Simon', 'Howels', '01223 349752'),
                        ('2', 'Karen', 'Phillips', '01954 295773'),
                        ('3', 'Darren', 'Smith', '01583 749012'),
                        ('4', 'Anne', 'Jones', '01323 567322'),
                        ('5', 'Mark', 'Smith', '01223 85534')"""

query_list = [query_table, query_values]
for i in query_list:
    db_cursor.execute(i)

db_connector.commit()


