from sqlmodel import SQLModel, Relationship, Field
from typing import List, Optional

class Poll(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    question: str
    owner_id: Optional[int] = Field(foreign_key="user.id")
    owner: Optional['User'] = Relationship(back_populates='polls')
    choices: List['Choice'] = Relationship(back_populates="poll")

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    password: str
    polls: Optional[Poll] = Relationship(back_populates='owner', sa_relationship_kwargs={"lazy": "selectin"})

class Choice(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    poll_id: Optional[Poll] = Field(foreign_key="poll.id")
    text: str
    poll: Optional[Poll] = Relationship(back_populates='choices')
    votes: List['Vote'] = Relationship(back_populates="choice")

class Vote(SQLModel, table=True):
    user_id: Optional[User] = Field(foreign_key="user.id")
    choice_id: Optional[Choice] = Field(foreign_key="choice.id")
    user: Optional["User"] = Relationship(back_populates='votes')
    choice: Optional[Choice] = Relationship(back_populates="votes")
    