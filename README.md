# Roast Memory Bot 🔥🧠

A FastAPI chatbot that combines **persistent conversation memory** with a **sarcastic-but-supportive roast personality**. Built as an independent, from-scratch rebuild of a memory-based chatbot pattern, with an added system-prompt-driven character layer.

## Features

- **Session-based conversation memory** — each conversation is tracked using a UUID `session_id`, with full message history persisted in PostgreSQL.
- **Custom personality via system prompt** — the bot roasts you casually like a friend, but switches to genuine motivation and advice when things get real.
- **Context-aware replies** — every request rebuilds the full conversation (system prompt + history + new message) before calling the LLM, so the bot always "remembers" the flow of the conversation within a session.
- **Groq-powered** — uses `llama-3.3-70b-versatile` for fast inference.

## Tech Stack

- FastAPI
- PostgreSQL + SQLAlchemy (ORM)
- Groq API
- Pydantic (request/response validation)
- python-dotenv

## Project Structure

```
├── main.py            # FastAPI app, /chat route, core request flow
├── models.py           # SQLAlchemy Message model (session_id, role, content, created_at)
├── schemas.py           # Pydantic ChatRequest / ChatResponse models
├── database.py           # DB engine, session, and Base setup
├── groq_client.py         # Groq API call wrapper
├── system_prompt.py        # Bot personality definition
├── requirements.txt
├── .gitignore
└── README.md
```

## How It Works

1. Client sends a `message` and optional `session_id`.
2. If no `session_id` is provided, a new UUID is generated for the session.
3. Previous messages for that session are fetched from PostgreSQL.
4. A conversation list is assembled: `[system prompt] + [past messages] + [new message]`.
5. This list is sent to Groq, and the reply is returned.
6. Both the user's message and the bot's reply are saved to the database under the same `session_id`.

## Setup

1. Clone the repo and install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Create a `.env` file:
   ```
   database_url=postgresql://user:password@localhost:5432/your_db
   groq_api_key=your_groq_api_key
   ```
3. Run the server:
   ```
   uvicorn main:app --reload
   ```
4. Test via `/docs` (Swagger UI) — send a `POST /chat` request with a message. Leave `session_id` as `null` on the first request to start a new conversation.

## Example

**Request:**
```json
{
  "message": "bhai kya haal hai",
  "session_id": null
}
```

**Response:**
```json
{
  "response": "Kya haal hai, dost? Sab theek?",
  "session_id": "1ff6e321-e847-4cec-937e-455dd4b07a88"
}
```

Use the returned `session_id` in subsequent requests to continue the same conversation with full memory.

## Author

Built by Bilal (Dhani Baksh) as part of an ongoing series of FastAPI + AI integration projects, exploring conversation memory, function calling, RAG, streaming, and structured outputs.
