from dotenv import dotenv_values, load_dotenv
from app.server.server_config import Server

_settings = (dotenv_values("./.env")) if (load_dotenv("./.env") == True) else "!token not found"

serverLink = _settings["SERVERLINK"]
endPointDatabase = _settings["ENDPOINTDATABASE"]

endPointTest = "/tests"
link = serverLink + endPointDatabase + "/users.db"

print(
    Server(
        _settings["TOKEN"], "app/core/data/users/data.db", link, viewConnectorSignal = False, dowloadDb='s'
        ).upload_allFiles("test_upload_file.txt", "{}{}/test_upload_file.txt".format(serverLink, endPointTest))
    )