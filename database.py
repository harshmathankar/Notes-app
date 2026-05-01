from typing import Annotated
from fastapi import Depends, HTTPException
from sqlmodel import create_engine, Session, select, SQLModel
from sqlalchemy.exc import NoResultFound

from schemas import CreateUser, UserNote, DbNote
from models import User, Note
from logger import logger
import auth
import os

pg_url = os.getenv("DATABASE_URL")
engine = create_engine(pg_url)

def create_db_and_tables():
    """Creates Tables"""
    SQLModel.metadata.create_all(engine,checkfirst = True)
create_db_and_tables()

def get_session():
    """Creates database session"""
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

# USER UTILS
def get_user_from_db(username: str, session: Session ):
    """Gets user information from database"""
    user =  session.exec(select(User).where(username==User.username)).first()
    if not user:
        return False
    return user

def save_user_in_db(user: CreateUser, session: Session):
    """Saves user details in db"""
    username = user.username
    password = user.password
    if not username or not password:
        raise HTTPException(422,"Incomplete information.")
    hashed_password = auth.hash_password(password)
    db_user = User(username = username, hashed_password= hashed_password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

# NOTE UTILS
def save_note_in_db(note: UserNote, username: str, session:Session):
    """Saves note in DB"""
    db_note = Note(name=note.name,content=note.content, username=username)
    logger.info(f"Saving note: {db_note}")
    session.add(db_note)
    session.commit()
    session.refresh(db_note)
    return db_note

def get_all_notes_from_db(username:str, session:Session):
    """Get all the notes of the user"""
    notes = session.exec(select(Note).where(username==Note.username)).all()
    if not notes:
        raise HTTPException(404, "Notes not found.")
    logger.info(f"Fetched Notes: {notes}")
    return notes

def get_note_from_db(note_id:int, username:str, session:Session):
    """Get the note with the given note id"""
    try:
        note = session.exec(select(Note).where(username==Note.username, note_id == Note.id)).one()
        logger.info(f"Fetched Note: {note}")
        return note
    except NoResultFound:
        raise HTTPException(404, "Note not found.")


def delete_note_from_db(note_id:int, username:str, session: Session):
    """Delete the note from DB with given note id"""
    try:
        note = session.exec(select(Note).where(username==Note.username, note_id==Note.id)).one()
        session.delete(note)
        session.commit()
        return {"message": f"Note with id {note_id} deleted successfully."}
    except NoResultFound:
        raise HTTPException(404, f"No note with Note ID: {note_id} present.")