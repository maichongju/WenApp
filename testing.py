from conf_basic import database_config

from Object.DataBase import DataBase

db = DataBase(database_config)
db.test()
print("Done")