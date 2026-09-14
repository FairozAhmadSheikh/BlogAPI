from sqlalchemy  import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from dotenv import find_dotenv
import os 

find_dotenv()

db_url=os.getenv("DATBASE_URL")



engine=create_engine(os.getenv("DATBASE_URL"))
SessionLocal=sessionmaker(bind=engine)
Base=declarative_base()