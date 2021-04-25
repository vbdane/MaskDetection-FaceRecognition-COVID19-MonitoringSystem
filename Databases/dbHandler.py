import sqlite3
from datetime import datetime

'''
A class to interact with the locally stored sqlite database which contains data about unmasked identified persons.
'''
class DbHandler:
    def __init__(self, id, name):
        self.ID = str(id)
        self.NAME = name
        self.conn = sqlite3.connect(r'Databases/MainDB.db')


    def create_table(self):

        query = "USE MainDB CREATE TABLE NoMaskList(ID INT PRIMARY KEY,NAME TEXT NOT NULL,DATE DATETIME NOT NULL,TIME DATETIME NOT NULL)"

        self.conn.execute(query)
        self.conn.commit()

        self.conn.close()

    def write_db(self):

        i = "(" + self.ID + ","
        n = "'" + self.NAME + "',"
        t = "'" + str(datetime.now().time())[:8] + "',"
        d = "'" + str(datetime.now().date()) + "')"

        query = "INSERT INTO NoMaskList VALUES" + i + n + t + d

        self.conn.execute(query)
        self.conn.commit()

        self.conn.close()

    def displayDb(self):

        myCursor = self.conn.cursor()
        myCursor.execute("SELECT * FROM 'NoMaskList'")

        return myCursor.fetchall()

    def deleteall(self):

        self.conn.execute("DELETE FROM NoMaskList")
        self.conn.commit()
        self.conn.close()