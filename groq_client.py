from dotenv import load_dotenv
from groq import Groq
import os


client = Groq(api_key=os.getenv("groq_api_key"))
def get_roast(message : list):
    response = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages = message
    )
    return response.choices[0].message.content
