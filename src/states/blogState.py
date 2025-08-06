from typing import TypedDict 
from pydantic import BaseModel , Field

class Blog(BaseModel):
    title : str = Field(description="The title of the blog post")
    content : str = Field(description="The main content of the blog Post")

class BlogState(TypedDict):
    """State of Blog generation Graph"""
    topic : str
    blog: Blog
    current_language : str