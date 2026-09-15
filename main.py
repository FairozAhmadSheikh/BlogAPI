from fastapi import FastAPI,Depends,HTTPException
import models,schemas
from database import engine,SessionLocal
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app=FastAPI()


#DB Session
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return{
        "message":"Workig "
    }

# Create blog
@app.post("/blogs",response_model=schemas.BlogResponse)
def create_blog(blog:schemas.BlogCreate,db:Session=Depends(get_db)):
    new_blog=models.Blog(title=blog.title,content=blog.content)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

# Get all blogs
@app.get("/get_blogs",response_model=list[schemas.BlogResponse])
def get_all_blogs(db:Session=Depends(get_db)):
    all_blogs=db.query(models.Blog).all()
    if not all_blogs:
        raise HTTPException(
            status_code=404,
            detail="No blog Found"
        )
    return all_blogs

# Get on the basis of id
@app.get("/blog/{id}",response_model=schemas.BlogResponse)
def get_blog_id(id:int,db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(
            status_code=404,
            detail="Blog not found"
        )
    return blog

# Update on the basis of id 
@app.put("/blog/{id}",response_model=schemas.BlogResponse)
def update_blog(id:int,blog:schemas.BlogCreate,db:Session=Depends(get_db)):
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

