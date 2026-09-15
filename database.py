from sqlalchemy  import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from dotenv import find_dotenv,load_dotenv
import os 

find_dotenv()
load_dotenv()

db_url=os.getenv("DATABASE_URL")
print(db_url)


engine=create_engine(db_url)
SessionLocal=sessionmaker(bind=engine)
Base=declarative_base()