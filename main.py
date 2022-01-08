from dotenv import dotenv_values, load_dotenv
from app.api.config import Server

_settings = (dotenv_values("./.env")) if (load_dotenv("./.env") == True) else "!token not found"


link = _settings["SERVERLINK"] + _settings["ENDPOINTDATABASE"] + "/users.db"

#getData(_settings["TOKEN"], "app/domain/data/users/data.db", link)
Server(_settings["TOKEN"], _settings["app/domain/data/users/data.db", link]).get_tables()