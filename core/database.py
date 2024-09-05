from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('mysql+mysqldb://pascal:pascal@localhost:3308/ecom_db')

session = sessionmaker(bind=engine)