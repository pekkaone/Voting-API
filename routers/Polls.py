from fastapi import APIRouter, HTTPException, Depends
from typing import Optional, List
from pydantic import BaseModel
from db.database import get_session
from db.models import Poll, Vote, Choice, User
from Authentefication import current_user
from sqlmodel import Session, select

router = APIRouter()

class ChoiceCreate(BaseModel):
    text: str

class PollCreate(BaseModel):
    question: str

@router.post("/create-new-poll")
def create_new_poll(questions_raw: ChoiceCreate, poll_raw: PollCreate, session: Session = Depends(get_session), user: User = Depends(current_user)):
    poll = Poll(question=poll_raw.question, owner_id=user.id)
    poll_existance = session.exec(select(Poll).where(Poll.question == poll.question)).first()
    if poll_existance is not None:
        raise HTTPException(status_code=401, detail="the poll is already exist")
    if user is None:
        raise HTTPException(status_code=400, detail="no user, or invalid token")
    session.add(poll)
    session.commit()
    session.refresh(poll)

    questions = Choice(text=questions_raw.text, poll_id=poll.id)
    question_existance = session.exec(select(Choice).where(Choice.text == questions.text)).first()
    if question_existance is not None:
        raise HTTPException(status_code=401, detail="question is already exist")
    session.add(questions)
    session.commit()
    session.refresh(questions)
    
    return {"msg": "post created"}

@router.post("/add-new-choice/{poll_id}")
def add_new_choice(question_raw: ChoiceCreate, poll_id: int, user: User = Depends(current_user), session: Session = Depends(get_session)):
    question = Choice(text=question_raw.text, poll_id=poll_id)
    is_owner = session.exec(select(Poll).where((poll_id == Poll.id) & (user.id == Poll.owner_id))).first()
    if is_owner:
        unique = session.exec(select(Choice).where(Choice.text == question.text)).first()
        if unique is not None:
            raise HTTPException(status_code=401, detail="Choice is already exist")
        question.poll_id = poll_id
        session.add(question)
        session.commit()
        session.refresh(question)
        return {"msg": "choice added"}
    raise HTTPException(status_code=400, detail="unfound or it is not yours")

@router.delete("/delete-post/{poll_id}")
def delete_post(poll_id: int, user: User = Depends(current_user), session: Session = Depends(get_session)):
    user_is_owner = session.exec(select(Poll).where((Poll.id == poll_id) & (user.id == Poll.owner_id))).first()
    if user_is_owner:
        polls_choices = session.exec(select(Choice).where(Choice.poll_id == poll_id)).all()
        for choice in polls_choices:
            session.delete(choice)
        session.delete(user_is_owner)
        session.commit()
        return {"msg": "post is deleted"}
    raise HTTPException(status_code=401, detail="you dont own dis")

@router.delete("/delete-choice/{poll_id}/{choice_id}")
def delete_choice(poll_id: int, choice_id: int, session: Session = Depends(get_session), user: User = Depends(current_user)):
    user_is_owner = session.exec(select(Poll).where((Poll.id == poll_id) & (user.id == Poll.owner_id))).first()
    if user_is_owner:
        poll_to_delete = session.exec(select(Choice).where(choice_id == Choice.id)).first()
        session.delete(poll_to_delete)
        session.commit()
        return {"msg": "choice is deleted"}
    raise HTTPException(status_code=401, detail="incorrect poll or choice id")

@router.get("/me")
def my_profile(user: User = Depends(current_user), session: Session = Depends(get_session)):
    user_Votes = session.exec(select(Vote).where(Vote.user_id == user.id)).all()
    return {"name": user.name, "active polls": user.polls, "votes": user_Votes}

@router.get("/vote/{choice_idd}")
def voting(choice_idd: int, user: User = Depends(current_user), session: Session = Depends(get_session)):
    voted = session.exec(select(Vote).where((Vote.choice_id == choice_idd) & (Vote.user_id == user.id))).first()
    if voted:
        raise HTTPException(status_code=401, detail="Already voted")
    vote = Vote(user_id=user.id, choice_id=choice_idd)
    session.add(vote)
    session.commit()
    return {"msg": "Voted"}

@router.get("/show-votes/{choice_idd}")
def show_votes(choice_idd: int, session: Session = Depends(get_session), user: User = Depends(current_user)):
    existing = session.exec(select(Choice).where(Choice.id == choice_idd)).first()
    if existing is not None:
        votes_count = session.exec(select(Vote).where(Vote.choice_id == choice_idd)).all()
        choice = session.exec(select(Choice).where(Choice.id == choice_idd)).first()
        return {"Votes": len(votes_count), "Text": choice.text}
    raise HTTPException(status_code=400, detail="There is no that choice")
