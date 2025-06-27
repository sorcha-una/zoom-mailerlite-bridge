import os
import hmac
import hashlib
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load the Zoom verification token from Replit's environment variables
ZOOM_VERIFICATION_TOKEN = os.getenv("ZOOM_VERIFICATION_TOKEN")

@app.route("/", methods=["GET", "POST"])
def handle_webhook():
    if request.method == "GET":
        return "Zoom Webhook Listener is running."

    try:
        data = request.get_json()
        print("Received Zoom webhook event:", data)

        # Handle Zoom URL validation event
        if data.get("event") == "endpoint.url_validation":
            plain_token = data["payload"]["plainToken"]

            encrypted_token = hmac.new(
                ZOOM_VERIFICATION_TOKEN.encode(),
                msg=plain_token.encode(),
                digestmod=hashlib.sha256
            ).hexdigest()

            return jsonify({
                "plainToken": plain_token,
                "encryptedToken": encrypted_token
            }), 200

        # Handle other webhook events
        # (You can expand this section to handle more event types as needed)
        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print("Error handling webhook:", e)
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)