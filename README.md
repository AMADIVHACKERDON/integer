📡 Telex Slack Bridge Integration

This is a Slack Bridge Output Integration for Telex. It forwards alerts from monitoring tools (e.g., Datadog, New Relic, Prometheus, Sentry) to a Slack channel using Slack's Incoming Webhooks API.

🚀 Features

✅ Receives alerts via webhook from various monitoring services.

🔄 Processes and formats alert messages for clarity and readability.

📩 Forwards alerts to a designated Slack channel using Slack’s Incoming Webhooks.

⚙️ Configurable settings for Slack webhook URL and message formatting.

📊 Enhances incident response workflows by ensuring critical alerts reach the right teams instantly.

📦 Installation & Setup

1️⃣ Clone the Repository

 git clone https://github.com/your-username/telex-slack-bridge.git
 cd telex-slack-bridge

2️⃣ Install Dependencies

Ensure you have Python installed, then run:

pip install -r requirements.txt

3️⃣ Configure Slack Webhook

Create a .env file in the project root and add your Slack webhook URL:

SLACK_WEBHOOK_URL=https://hooks.slack.com/services/your/webhook/url

4️⃣ Run the Integration

Start the FastAPI server using Uvicorn:

uvicorn main:app --reload

📜 API Endpoints

🔹 Receive Alert (POST /webhook)

Accepts JSON payloads from monitoring tools and forwards them to Slack.

Request Example:

{
  "service": "Prometheus",
  "alert": "High CPU Usage",
  "severity": "critical",
  "timestamp": "2025-02-23T10:30:00Z"
}

Response Example:

{
  "status": "success",
  "message": "Alert forwarded to Slack"
}

🛠 Development & Testing

Running Tests

pytest tests/

Ensure all tests pass before making any changes.

Linting Code

flake8 .

Maintain clean and readable code.

🚀 Deployment

Using Docker

Build and run the container:

docker build -t telex-slack-bridge .
docker run -p 8000:8000 --env-file .env telex-slack-bridge

Deploying to a Cloud Provider

You can deploy this integration on any cloud platform that supports Python and FastAPI, such as:

AWS Lambda (via API Gateway)

DigitalOcean App Platform

Vercel or Render

📄 License

This project is licensed under the MIT License. See LICENSE for details.

🙌 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.
