from fastapi import FastAPI, Request

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
