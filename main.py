from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session
from database import engine,get_db
from system_prompt import SYSTEM_PROMPT
from groq_client import get_roast
from models import Message
from schemas import ChatRequest,ChatResponse
import uuid


app = FastAPI()


@app.post("/chat")
def chat(request : ChatRequest, db : Session = Depends(get_db)):
    session_id = request.session_id
    if session_id is None:
        session_id = str(uuid.uuid4())

    else:
        session_id = request.session_id

    old_messages = db.query(Message).filter(Message.session_id == session_id).all()

    conversation = []
    conversation.append({"role" : "system", "content" : SYSTEM_PROMPT})

    for msgs in old_messages:
        conversation.append({"role": "user", "content": request.message})


    bot_reply = get_roast(conversation)

    UserMsg = Message(session_id = session_id,role = "user",content = request.message)
    BotReply = Message(session_id = session_id, role = "assistant",content = bot_reply)
    db.add(UserMsg)
    db.add(BotReply)
    db.commit()

    return ChatResponse(session_id = session_id ,  response = bot_reply)
