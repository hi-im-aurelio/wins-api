import sqlite3

cursor = sqlite3.connect("./app/domain/data/users/data.db").cursor()

# for datas in cursor.execute(("SELECT name FROM sqlite_master WHERE type='table';")).fetchall():
#     print(datas)

for datas in cursor.execute(("SELECT * FROM Users")).fetchall():
    print(datas)