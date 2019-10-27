import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

engine = sa.create_engine('mssql+pyodbc://.\\SQL2005/ULAN_UDE_2019_READY?driver=SQL+Server+Native+Client+11.0')
Session = sessionmaker()
Session.configure(bind=engine)

session = Session()
