from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Your MailerLite API key and group IDs
MAILERLITE_API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI0IiwianRpIjoiYzBkOTA3MWRhMGU4OTE1YmRhN2I5MjBjMjk3MDE5YTZjZTEwYmI1NGJkMGIyY2U0OTExMjQ0MmJmYmEyMjM5M2U5MjE3MjUxNTAzMDdkYzAiLCJpYXQiOjE3NTEwMTY4NzAuMDM0NDE4LCJuYmYiOjE3NTEwMTY4NzAuMDM0NDIxLCJleHAiOjQ5MDY2OTA0NzAuMDMwNTY1LCJzdWIiOiI1MTc0NTAiLCJzY29wZXMiOltdfQ.BA1LHKyVQf6oAkfmpZ8l1Ruv7h_qw3So3MDr3FpecehXDu-V6MFkedki0nprpHK68V2CghS101jeKhNtUDUZUMHPUrZFq249xhtTKAut4oH2JmqmoXTmCKUMOjQddfuzC6hZboyYhCJLFCOOgdKOaoBW8U0hoIj_kRNzdx8eUiL7UJwem7KDfaIc0UegKuhGBG_QeK70dQw31m2E_0pmFIsQYgNdlCp0sdtwPKAxIuUSFToPDxqYQX_5I7v0dhz76P04OI-fnkVV39zG-k0eu_LA3_nlkAXDZXNnx8rK9cyxye-uNwLXZfuENj3JYg0eC2TUMoNp-vX3ZvEoytJJcijUvQaneKJ1p_0C_gqUL8lbhzkmaelqcAwoIarrKsT3QTR4_O1SwiH5fxu_UNgwWIk0x16jRav37YsXCuuWUtd15-_wtXnLW8EOmxJjLBejt4Svs_o0hlK4qbR07BiKsfeURsUwUAI_5EI9P-doOSkinsSCMHChOcXXnbtPrCJ1hgijB9iPjOUwzt77EnlNjKThSqE41FDlyVyLu8Z8mVtxaq8JotTUEj0bzMSkmvq5c2ZLwTKo89dns04Xm4UqQ5wceFXAXY9soYc11dpFUtAsMxn4rv-tbzOLCOxRQzufJzd2RZQDWkABbBSuzzu1I8M_tYAYKxXcD2tcC2xo8tQ"
EARLY_BIRD_GROUP_ID = "156825160811284049"
OTHER_GROUP_ID = "154267060780663825"

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