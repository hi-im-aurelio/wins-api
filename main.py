from dotenv import dotenv_values, load_dotenv
from app.server.server_config import Server

_settings = (dotenv_values("./.env")) if (load_dotenv("./.env") == True) else "!token not found"

serverLink = _settings["SERVERLINK"]
endPointDatabase = _settings["ENDPOINTDATABASE"]

endPointTest = "/tests"
link = serverLink + endPointDatabase + "/.db"

print(
    Server(
         _settings["TOKEN"], "app/core/data/users/.db", link, viewConnectorSignal = True, dowloadDb='s'
    ).pull()
)
