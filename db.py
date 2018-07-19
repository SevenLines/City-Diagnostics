import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

engine = sa.create_engine('mssql+pyodbc://sa@DESKTOP-KG0DNNF\SQLEXPRESS/SVPD2018_City_ready?driver=SQL+Server+Native+Client+11.0')
Session = sessionmaker()
Session.configure(bind=engine)

session = Session()
