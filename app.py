import os
import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
JSON_FILE = 'jewellery.json'

def get_bot_reply(user_msg, jewellery):
    msg = user_msg.lower()
    if "choker" in msg or "kundan" in msg:
        return f"Sir {msg} collection me kafi designs hain, koi price range bataen?"
    return "Welcome Sir / Welcome Madam, hukum karen apko kya chahiye?"

@app.route('/')
def index():
    jewellery_data = {}
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r') as f:
            try:
                jewellery_data = json.load(f)
            except:
                jewellery_data = {}
    return render_template('index.html', jewellery=jewellery_data)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    
    jewellery_data = {}
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r') as f:
            try:
                jewellery_data = json.load(f)
            except:
                pass
                
    reply = get_bot_reply(user_message, jewellery_data)
    return jsonify({"reply": reply})

@app.route("/admin")
def admin():
    jewellery_data = {}
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r') as f:
            try:
                jewellery_data = json.load(f)
            except:
                jewellery_data = {}
    return render_template('admin.html', jewellery=jewellery_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)