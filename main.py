from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from random import randint

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [
    {"title": "title of post 1", "content": "123", "id": 1},
    {"title": "favourite food", "content": "pizza", "id": 2}
]


@app.get("/posts")
def get_posts():
    return my_posts


@app.get("/posts/{post_id}")
def get_post(post_id: int):
    try:
        [data] = list(filter(lambda x: x['id'] == post_id, my_posts))
    except ValueError:
        data = "Post not found"

    return {"data": data}


@app.post("/posts")
def create_posts(post: Post):
    data = post.dict()
    data['id'] = randint(1, 1000000000)
    my_posts.append(data)
    return {"data": data}
