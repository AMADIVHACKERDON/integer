from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from datetime import date

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
        "data": {
            "date": {
                "created_at": str(date.today()),
                "updated_at": str(date.today())
            },
            "descriptions": {
                "app_name": "Telex Legal Assist",
                "app_description": "A chatbot that provides instant legal guidance by refining queries, categorizing them, and offering legal responses or references.",
                "app_logo": "https://upload.wikimedia.org/wikipedia/commons/7/76/Slack_Icon.png",
                "app_url": "https://integer-i9u8.onrender.com/",
                "background_color": "#FFFFFF"
            },
            "integration_category": "Legal Assistance",
            "integration_type": "modifier",
            "is_active": True,
            "output": [],
            "key_features": [
                "Instant legal query refinement and categorization.",
                "Provides relevant legal references and responses.",
                "Fallback to external legal resources if needed.",
                "Seamless API integration for automated legal assistance."
            ],
            "permissions": {
                "legal_assist_user": {
                    "always_online": True,
                    "display_name": "Legal Assist Bot"
                }
            },
            "settings": [
                {
                    "label": "API Endpoint",
                    "type": "text",
                    "required": True,
                    "default": "https://integer-i9u8.onrender.com/webhook"
                },
                {
                    "label": "Fallback Resource URL",
                    "type": "text",
                    "required": True,
                    "default": "https://your-legal-resource.com"
                }
            ],
            "target_url": "https://integer-i9u8.onrender.com/webhook"
        }
    }
    return JSONResponse(content=data)
