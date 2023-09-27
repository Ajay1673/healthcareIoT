from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

url = "mysql+pymysql://root:ajayKrishna03@localhost/healthcareIoT"
engine = create_engine(url)
Session = sessionmaker(bind=engine)

Base = declarative_base()