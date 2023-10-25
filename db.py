import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

engine = sa.create_engine('mssql+pyodbc://.\\SQL2014/RoadsDB_2023_new_done?driver=SQL+Server+Native+Client+11.0')
Session = sessionmaker()
Session.configure(bind=engine)

session = Session()
