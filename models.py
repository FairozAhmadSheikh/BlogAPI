from sqlalchemy import Column, Integer,String,Text
from database import Base

class Blog(Base):
    __tablename__="blogs"
    id=Column(Integer,index=True,primary_key=True)
    title=Column(String)
    content=Column(Text)


