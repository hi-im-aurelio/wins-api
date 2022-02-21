import sqlite3

# Pegando o lenght dos dados locais.
local_changes = len(sqlite3.connect("app/core/data/users/.db").cursor().execute("SELECT * FROM Users").fetchall())