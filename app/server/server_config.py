from dotenv import dotenv_values, load_dotenv # Importando dotenv para variavei de ambiente como o serverLink...
_settings = (dotenv_values("./.env")) if (load_dotenv("./.env") == True) else "!token not found"

import os 
import dropbox
import sqlite3 as sqlite
from pathlib import Path
from cockroach import developing_cockroach as dev
from local_changes_value import local_changes

serverLink = _settings["SERVERLINK"]
endPointDatabase = _settings["ENDPOINTDATABASE"]
link = serverLink + endPointDatabase + "/.db"

class Server:
    '''Class responsible for server calls and provision of some services, such as returning user data on the server.
     REQUIRED PARAMETERS: token (server access token. set it in .env)
                             yourLocalForlder (your data writing location. Where it will be stored)
                             link (serverlink and endpoint)
     These are the minimum parameters for script execution.
     Some parameters like:
                             viewConnectorSignal (Receives True or False. Responsible for showing the CONNECTOR sign, if it is equal to 1 or equal to 0)
                             dowloadDb (receives "n" or something different like "y" from yes and no. Responsible for handling the CONNETOR error equal to 0.)
    '''
    def __init__(self, token, yourLocalFolder, link, viewConnectorSignal = True, dowloadDb = 'n', function = None) -> None:
        self.dowloadDb = dowloadDb # parameter responsible for checking if a succession of CONNECTOR = 0 occurs, that it tries to correct such error by itself.
        self.token = token # server access token.
        self.yourLocalFolder = yourLocalFolder # your writing location.
        self.link = link # server link and endpoint.
        self.dbx = dropbox.Dropbox(self.token) # creating a dropbox object called dbx.

        self.connect = False # initializing self.connect, responsible for handling and returning some exceptions.
        self.localHost = "./app/core/data/users/.db" # setting my recording location. (standard)
        
        if Path(r"{}".format(self.localHost)).is_file():# checking if such a file exists and returning a Boolean, True or False value and based on that making a decision.
            self.__newDataBaseInstance = sqlite.connect(self.localHost)
            self.__cursor = self.__newDataBaseInstance.cursor() # creating a cursor instance.
            self.__commit = self.__newDataBaseInstance.commit
            self.connect = True 
            if viewConnectorSignal: dev.log(name = "CONNECTED", message= "CONNECTOR RETORNANDO SINAL 1")
        
        else: # if the return of the "if" condition equals False, then it will take that path.
            if self.dowloadDb != 'n':

                # if viewConnectorSignal is True, print/print connector log.
                if viewConnectorSignal: dev.log(name = "CONNECTION FAIL", message= "CONNECTOR RETORNANDO SINAL 0")  
                self.tryToDownloadTheDatabase = input("\nThe connector returned the 0 signal, it can be the case that you do not have a " + "\033[33m{}\033[0m".format(self.localHost) + " file on your local machine with the required iformatio. To try to solve the problem, download the file to the remote server? (y/n): ")

                if self.tryToDownloadTheDatabase == "y": # If a CONNECTOR exception of 0 occurs, ask if you want to download the .db file.
                    
                    # download sqlite database file.
                    self.get_dataBase(yourLocalFolder)
                else: 
                    ...
    # removing database file.
    def remove_dataBase(self, local):
        try: 
            os.remove(local) 
        except FileNotFoundError as error:
            print("ARQUIVO DE BASE DE DADOS NÃO ENCOTRADO.")

    # method responsible for getting file .db on the server.
    def get_dataBase(self, yourLocalFolder):
        with open(yourLocalFolder, "wb") as file:
            metadata, res = self.dbx.files_download(path= self.link)
            file.write(res.content)
            dev.log('successfully downloaded.')

    # method responsible for getting users on the server.
    def get_users(self):
        self.get_dataBase(self.yourLocalFolder) # donwload data file to server.
        if self.connect: # by checking the connector value first.
            users = []
            for user in self.__cursor.execute("SELECT * FROM Users").fetchall():
                users.append(user)
            return users
        else: 
            return "\nSOMETHING UNEXPECTED HAPPENED."
    
    # method responsible for getting one user on the server.
    #def get_user(self, userName):

    # method responsible for returning the names of tables in the database.
    def get_tables(self):
        self.get_dataBase(self.yourLocalFolder) # donwload data file to server.
        if self.connect: # by checking the connector first.
            tables = []
            for data in self.__cursor.execute(("SELECT name FROM sqlite_master WHERE type='table';")).fetchall():
                tables.append(data)
            return tables
        else:
            return "\nSOMETHING UNEXPECTED HAPPENED."

    # whereIsTheFile = 'upload/new_image_test.png'. File on your local machine
    # pointThePathOnTheServer = serverPath/... . Path on server. [serverLink + endPoint/nameOfYourFile.exemple]
    #method responsible for uploading some file to the server.
    def upload_allFiles(self, whereIsTheFile, pointThePathOnTheServer):
        self.dbx.files_upload(open(whereIsTheFile, 'rb').read(), pointThePathOnTheServer)
        return "done..."   
    
    # Metodo responsavel por atualizar os dados da minha maquina caso hajam alterações no banco de dados remoto.  (Caso um usuário tenha feito um push no banco de dados remoto) Tente usar essa fução como uma comparação de arquivos no seu sistema.
    def pull(self):
        
        # irá abrir um arquivo CMPdatas.db que é banco de dados remoto com as alteraçõs ou não.
        with open("app/core/data/users/CMPdatas.db", "wb") as file:
            metadata, res = self.dbx.files_download(path= self.link)
            file.write(res.content)
            dev.log('Comparison database download...')
        
        
        # apos isso faremos uma verifição de alterações antes de altualizar, para, se enxistir realmente uma alteração no banco de dados remoto, haja então essa atualização localmente.
        remote_changes = len(sqlite3.connect("app/core/data/users/CMPdatas.db").cursor.execute("SELECT * FROM Users"))
        
        # o local_changes é o lenght dos dados locail. Não verificamos as alterações feitas, mas sim o valor inteiro das alterações feitas e com isso, se for diferente da local, então haverá uma atualização dos dados locais.
        if local_changes != remote_changes:
            self.get_dataBase(yourLocalFolder) # Chamndo uma fução de download do banco de dados remoto: 
        else:
            dev.log(name = 'Pull message', message = 'Está tudo atualizado. Sem alterações encotradas')
            
    # Metodo para a atualização do novo banco de dados com as novas informações locails.
    def push(self):
        # "link" é o caminho exato do meu banco de dados remoto.
        # "locaHost" é o caminho exato do meu banco de dados local.
        self.upload_allFiles(self.localHost,  link) # chamando a o metodo `upload_allFile` com a função de envio de arquivos ao servidor. 
        dev.log('banco de dados atualizado com sucesso')
        
    # Metodo para envio de mensagens ao servidor. Use uma outra funcao para a recuperaçao delas, como o metodo `get_users`.
    def sendMessage(self,nameUser, sender, subject, message, recipient):
        self.__cursor.execute("INSERT INTO Users (nameUser, sender, subject, message, recipient) VALUES ({},{}, {}, {}, {})".format(nameUser, sender, subject, message, recipient)) # query
        
        self.__commit() # commitando as novas alterações que estão no nivel do python ainda para o banco de dados local.
        self.dbx.files_delete(link) # apagando o arquivo antes de atualizaló. Por motivos de retornar o erro de arquivo já existente...
        
        self.push() # Fazendo commit no servidor remoto.
        
        dev.log('done to send message...')
# ...