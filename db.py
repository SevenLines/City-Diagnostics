import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

engine = sa.create_engine('mssql+pyodbc://.\\SQL2014/RoadsDB2022_ready_2?driver=SQL+Server+Native+Client+11.0')
Session = sessionmaker()
Session.configure(bind=engine)

session = Session()
