from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    Published: bool
    rating: Optional[int] = None # Optional allows us to not have to fill in the rating field if we do not want to.
    
    
my_posts = [{"title": "Post 1", "content": "Content of post 1", "id": 1},
            {"title": "Post 2", "content": "Content of post 2", "id": 2},
            {"title": "Post 3", "content": "Content of post 3", "id": 3}]   

def find_post(id):
    for i in my_posts:
        if i["id"] == id:
            return i
      

@app.get("/posts")
async def root():
    return {"message": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)# By referencing the post variable our program returns to the "class post" pydantic model and retrives our posts/data
def createpost(post: Post): 
    post_dict = post.dict()# This converts the post variable to a dictionary from pydantic dictionary.
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)#Hapa ni kwamba tuna add the input (post created on the frot end ) to our storage variable my_posts.
    return {"data": post_dict}

@app.get("/posts/{id}")
def get_posts(id: int, response: Response):# that int keyword int the parameter helps us ensure that the id is an integer,as a path is a always a string
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was no found")
       # response.status_code = status.HTTP_404_NOT_FOUND
       #return {"Message": f"Post with id {id} was no found"}
    return{"post_detail": post}
