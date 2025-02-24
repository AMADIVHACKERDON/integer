import httpx
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from datetime import date
import logging

app = FastAPI()

TELEX_WEBHOOK_URL = "https://ping.telex.im/v1/webhooks/0195398f-142c-7bb1-8c3c-887c4cc8c133"

# Set up logging
logging.basicConfig(level=logging.INFO)

@app.get("/")
def home():
    return {"message": "Welcome to the Legal Assist Chatbot"}

@app.post("/webhook")
async def receive_message(request: Request):
    try:
        # Read JSON request
        body = await request.json()
        logging.info(f"Received payload: {body}")

        # Validate required fields
        required_fields = ["event_name", "username", "status", "message"]
        missing_fields = [field for field in required_fields if field not in body]

        if missing_fields:
            return JSONResponse(
                status_code=400, 
                content={"error": f"Missing required fields: {', '.join(missing_fields)}"}
            )

        # Extract data
        event_name = body["event_name"]
        username = body["username"]
        status = body["status"]
        message = body["message"]

        # Process the legal query
        response_text = process_legal_query(message)

        # Forward to Telex
        async with httpx.AsyncClient() as client:
            telex_response = await client.post(
                TELEX_WEBHOOK_URL, 
                json={"event_name": event_name, "username": username, "status": status, "message": response_text}
            )

        if telex_response.status_code != 200:
            logging.error(f"Telex Error: {telex_response.text}")
            return JSONResponse(
                status_code=500, 
                content={"error": "Failed to forward message to Telex", "details": telex_response.text}
            )

        return {"response": response_text, "telex_status": "Forwarded to Telex"}

    except Exception as e:
        logging.error(f"Error processing webhook: {str(e)}")
        return JSONResponse(status_code=500, content={"error": str(e)})

def process_legal_query(text: str) -> str:
    """Processes legal queries and returns responses."""
    text = text.lower()
    
    if "contract" in text:
        return "A contract is a legally binding agreement. Need more details?"
    elif "divorce" in text:
        return "Divorce laws vary by country. Do you need guidance on filing?"
    
    return "Sorry, I couldn't find relevant legal info. Try rephrasing."

@app.get("/telex.json")
def get_json():
    """Serves Telex integration JSON for webhook configuration."""
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
            "integration_category": "Communication & Collaboration",
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
