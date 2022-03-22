import os

import databases
import sqlalchemy


DATABASE_URL = os.getenv('DATABASE_URL')
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
