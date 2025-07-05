from sqlmodel import SQLModel, Relationship, Field
from typing import List, Optional

class Poll(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    question: str
    owner_id: Optional[int] = Field(foreign_key="user.id")
    owner: Optional['User'] = Relationship(back_populates='polls')

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    password: str
    polls: Optional[Poll] = Relationship(back_populates='owner', sa_relationship_kwargs={"lazy": "selectin"})

class Choice(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    poll_id: Optional[Poll] = Relationship(back_populates='id')
    text: str

class Vote(SQLModel, table=True):
    user_id: Optional[User] = Relationship(back_populates="id")
    choice_id: Optional[Choice] = Relationship(back_populates='id')
    