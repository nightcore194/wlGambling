import os

BASE_DIR = os.path.abspath(os.getcwd()) # starts with / and ends with foldername without .
DB_ROOT = BASE_DIR + '/instance'
DB_DESTINITION = DB_ROOT + "/linkBuyersDB.db"