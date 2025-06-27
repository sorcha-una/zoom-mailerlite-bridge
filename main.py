from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Fetching from environment variables
MAILERLITE_API_KEY = os.getenv("MAILERLITE_API_KEY")
EARLY_BIRD_GROUP_ID = os.getenv("EARLY_BIRD_GROUP_ID")
OTHER_GROUP_ID = os.getenv("OTHER_GROUP_ID")

# Your Zoom ticket type IDs
EARLY_BIRD_TICKET_ID = "Lrx0nUqCSEeJxwcV5iZCvg"

def add_email_to_mailerlite_group(email, group_id):
    url = f"https://api.mailerlite.com/api/v2/groups/{group_id}/subscribers"
    headers = {
        "Content-Type": "application/json",
        "X-MailerLite-ApiKey": MAILERLITE_API_KEY
    }
    data = {
        "email": email,
        "resubscribe": True
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code in (200, 201):
        print(f"Added {email} to MailerLite group {group_id}")
    else:
        print(f"Failed to add {email}: {response.status_code} - {response.text}")

@app.route("/", methods=["GET"])
def index():
    return "Webhook listener is running."
    
@app.route("/", methods=["POST"])
def zoom_webhook():
    data = request.json
    if not data:
        return jsonify({"error": "No JSON received"}), 400

    event = data.get("event")

    if event == "zoom_events.ticket_created":
        ticket = data["payload"]["object"]
        email = ticket.get("email")
        ticket_type_id = ticket.get("ticket_type_id")

        if not email or not ticket_type_id:
            return jsonify({"error": "Missing email or ticket_type_id"}), 400

        if ticket_type_id == EARLY_BIRD_TICKET_ID:
            group_id = EARLY_BIRD_GROUP_ID
        else:
            group_id = OTHER_GROUP_ID

        add_email_to_mailerlite_group(email, group_id)
        return jsonify({"status": "added to group"}), 200

    # Respond 200 to other events to avoid retries
    return jsonify({"status": "event ignored"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)