from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from auth import authenticate_user, get_user_details
from database import save_user_in_db, SessionDep, save_note_in_db, get_all_notes_from_db, get_note_from_db, \
    delete_note_from_db
from schemas import CreateUser, UserResponse, Token, UserNote
from logger import logger


app = FastAPI()

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected Error: {exc}")
    return JSONResponse( status_code=500, content={"message":"Internal Server Error. Please try again later."})

# Register and user login API
@app.post("/register", response_model = UserResponse)
def register_user(user:CreateUser, session: SessionDep):
    """Registers the user into the database"""
    logger.info(f"Registering user: {user.username}")
    saved_info = save_user_in_db(user, session)
    return UserResponse(id = saved_info.id, username=saved_info.username)

@app.post("/login", response_model=Token)
def login_user(user:CreateUser, session:SessionDep):
    """Logs the user and returns an access token for the user"""
    logger.info(f"Login attempt: {user.username}")
    token = authenticate_user(user.username, user.password, session)
    return token

# Notes API
@app.post("/notes")
def create_note(note: UserNote,  session:SessionDep, username:dict = Depends(get_user_details)):
    """Creates and saves notes in DB"""
    logger.info(f"Create note for user: {username.get('username')}")
    if not note:
        raise HTTPException(400, "Please enter notes title and content.")
    note_saved = save_note_in_db(note,username.get("username"),session)
    if not note_saved:
        raise HTTPException(500, "Could not save the note.")
    return {"message":f"Note {note.name} saved in DB with ID:{note_saved.id}."}

@app.get("/notes")
def get_all_notes(session: SessionDep, username: dict = Depends(get_user_details)):
    """Get all the notes of the user"""
    notes = get_all_notes_from_db(username.get("username"),session)
    return notes

@app.get("/notes/{notes_id}")
def get_note_with_id(notes_id: int,session:SessionDep, username: dict = Depends(get_user_details)):
    """Fetches the note with its id"""
    note = get_note_from_db(note_id = notes_id, username=username.get("username"), session = session)
    logger.info(f"Note {notes_id}: {note}")
    return note

@app.delete("/notes/{notes_id}")
def delete_note_with_id(notes_id:int, session:SessionDep, username: dict = Depends(get_user_details)):
    """Deletes the note with the given note id"""
    note = delete_note_from_db(notes_id, username.get("username"), session)
    return note