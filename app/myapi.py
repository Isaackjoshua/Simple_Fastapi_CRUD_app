from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel): #So this is our schema and what it does is it specifies the data format that our api recieves from the front end.
    title: str
    content: str
    Published:Optional[bool] = True
    rating: Optional[int] = None # Optional allows us to not have to fill in the rating field if we do not want to.
    
    
my_posts = [{"title": "Post 1", "content": "Content of post 1", "id": 1},
            {"title": "Post 2", "content": "Content of post 2", "id": 2},
            {"title": "Post 3", "content": "Content of post 3", "id": 3}]   

def find_post(id):
    for i in my_posts:
        if i["id"] == id:
            return i
      
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i 
        

@app.get("/posts")
async def root():
    return {"message": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)# By referencing the post variable our program returns to the "class post" pydantic model and retrives our posts/data
def createpost(post: Post): 
    post_dict = post.dict()# This converts the post variable to a dictionary from pydantic dictionary.
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/{id}")
def get_posts(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was no found")# raise exception
       # response.status_code = status.HTTP_404_NOT_FOUND
       #return {"Message": f"Post with id {id} was no found"}
    return{"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)#Using a 204 will restrict you from sending any more data
def delete_post(id: int): #passing the int keyword changes the string type id into the interger form.
    #deleting post
    #find the index in the array that has the required ID
    # my_posts.pop(index)
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'post with id {id} does not exist')
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    #print(post)
     index = find_index_post(id)
     if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f'post with id {id} does not exist')
     post_dict = post.dict()
     post_dict['id'] = id
     my_posts[index] = post_dict
     return{'data': post_dict}