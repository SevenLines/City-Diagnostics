import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

engine = sa.create_engine('mssql+pyodbc://SVPD2018_City_ready')
Session = sessionmaker()
Session.configure(bind=engine)

session = Session()
