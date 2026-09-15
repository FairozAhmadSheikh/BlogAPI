from fastapi import FastAPI,Depends,HTTPException,Query
import models,schemas
from database import engine,SessionLocal
from sqlalchemy.orm import Session
from auth import create_token,verify_token

models.Base.metadata.create_all(bind=engine)

app=FastAPI()


#DB Session
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
#Login
@app.post("/login")
def login():
    return{
        "access_token":create_token({"user":"admin"}),
        "token_type":"bearer"
    }

@app.get("/")
def home():
    return{
        "message":"Workig "
    }



# Create blog
@app.post("/blogs",response_model=schemas.BlogResponse)
def create_blog(blog:schemas.BlogCreate,user=Depends(verify_token),db:Session=Depends(get_db)):
    new_blog=models.Blog(title=blog.title,content=blog.content)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

# Get all blogs now with pagination and search
@app.get("/get_blogs")
def get_all_blogs(page:int=1,
                  limit:int=5,
                  search:str=Query(default=""),
                  db:Session=Depends(get_db)):
    query=db.query(models.Blog)
    if search:
        query=query.filter(models.Blog.title.ilike(f"%{search}%"))
    total=query.count()
    start=(page-1)*limit
    all_blogs=query.offset(start).limit(limit).all()
    if not all_blogs:
        raise HTTPException(
            status_code=404,
            detail="No blog Found"
        )
    return {
        "page":page,
        "limit":limit,
        "total":total,
        "data":all_blogs
    }

# Get on the basis of id
@app.get("/blog/{id}",response_model=schemas.BlogResponse)
def get_blog_id(id:int,user=Depends(verify_token),db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(
            status_code=404,
            detail="Blog not found"
        )
    return blog

# Update on the basis of id 
@app.put("/blog/{id}",response_model=schemas.BlogResponse)
def update_blog(id:int,blog:schemas.BlogCreate,db:Session=Depends(get_db),user=Depends(verify_token)):
    existing_blog=db.query(models.Blog).filter(models.Blog.id==id).first()

    if not blog :
        raise HTTPException(
            status_code=404,
            detail="Blog not Found"
        )
    existing_blog.title=blog.title
    existing_blog.content=blog.content

    db.commit()
    
    return existing_blog

# Delete on the basis of id 

@app.delete("/blog/{id}")
def delete_blog(id:int,db:Session=Depends(get_db),user=Depends(verify_token)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).first()

    if not blog:
        raise HTTPException(
            status_code=404,
            detail='Could not find the Blog'
        )
    db.delete(blog)
    db.commit()
    return {
        "message":"Blog Deleted"
    }