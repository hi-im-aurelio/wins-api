import sqlite3 as sqlite
from sqlite3.dbapi2 import connect
import dropbox
from cockroach import developing_cockroach as dev


# classe Servidor.
# yourLocalFolder = "donwloads/image-test.png"
# link = "/Documents/favicon2_.png"
class Server:
    def __init__(self, token, yourLocalFolder, link) -> None:
        self.token = token
        self.yourLocalFolder = yourLocalFolder
        self.link = link
        self.dbx = dropbox.Dropbox(self.token)

        self.connect = False
        try:
            self.__cursor = sqlite.connect("./app/domain/data/users/data.db").cursor()
            self.connect = True
        except:
            connect = self.connect
        

        # with open(yourLocalFolder, "wb") as file:
        #     metadata, res = self.dbx.files_download(path= self.link)
        #     file.write(res.content)
        #     dev.log('successfully downloaded.')
        

    def get_users(self, tableName):

        if self.connect:
            users = []
            for user in self.__cursor.execute("SELECT * FROM {}".format(tableName)).fetchall():
                users.append(user)
            return users
        else: 
            return "ERROR DE CONNECTOR"

    def get_tables(self):
        if connect:
            tables = []
            for data in self.__cursor.execute(("SELECT name FROM sqlite_master WHERE type='table';")).fetchall():
                tables.append(data)
            return tables
        else:
            return "ERROR DE CONNECTOR"
    
    
# testing
