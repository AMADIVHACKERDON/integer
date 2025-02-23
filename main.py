from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to the Legal Assist Chatbot"}

@app.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()
    message = data.get("text", "")

    # Process legal query
    response = process_legal_query(message)

    return {"response": response}

def process_legal_query(text):
    # Basic legal query processor (Example)
    if "contract" in text.lower():
        return "A contract is a legally binding agreement. Need more details?"
    elif "divorce" in text.lower():
        return "Divorce laws vary by country. Do you need guidance on filing?"
    return "Sorry, I couldn't find relevant legal info. Try rephrasing."

# Serve Telex integration JSON
@app.get("/telex.json")
def get_json():
    data = {
        "name": "telex-legal-assist",
        "type": "modifier",
        "description": {
            "app_name": "Telex Legal Assist",
            "app_description": "A chatbot that provides instant legal guidance by refining queries, categorizing them, and offering legal responses or references.",
            "app_logo": "https://your-logo-url.com/logo.png",
            "app_url": "https://your-app-url.com",
            "background_color": "#FFFFFF"
        },
        "settings": {
            "api_url": {
                "type": "string",
                "required": True,
                "description": "The API endpoint for processing legal queries and retrieving responses."
            },
            "fallback_resource_url": {
                "type": "string",
                "required": True,
                "description": "A default legal resource URL to use if no precise answer is found."
            }
        },
        "data": {
            "api_url": "https://your-deployed-url.com/webhook",
            "fallback_resource_url": "https://your-legal-resource.com"
        },
        "modifies": {
            "input": True,
            "output": False
        },
        "commands": [
            {
                "command": "/legal",
                "description": "Ask a legal question and get an instant response."
            }
        ],
        "permissions": {
            "allow_public": False,
            "allow_private_channels": True
        }
    }
    return JSONResponse(content=data)
