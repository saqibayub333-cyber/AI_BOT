from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

def load_data():
    try:
        with open('jewellery.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def get_bot_reply(user_msg, jewellery):
    msg = user_msg.lower()
    if "choker" in msg or "kundan" in msg:
        return f"Sir {msg} collection me kafi designs hain, koi price range batayen?"
    return "Welcome Sir / Welcome Madam, hukum karen apko kya chahiye?"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message", "")
    msg = user_msg.lower()
    if any(w in msg for w in ['mehenga','mehinga','mehnga','expensive']):
        return jsonify({"reply": "Samajh sakta hun Sir, ye Indian imported jewellery hai, quality local se bohot behtar hai, kala nahi hota. Original 3500 se discount me Final 3150 me de rahe hain."})
    if 'jazz' in msg or 'cash' in msg or 'payment' in msg:
        return jsonify({"reply": "JazzCash: 03005639461 pe payment kar sakte hain. Address: Shop 1 Momin Market Gami Adda Abbottabad."})
    jewellery = load_data()
    reply = get_bot_reply(user_msg, jewellery)
    return jsonify({"reply": reply})

@app.route("/admin")
def admin():
    return render_template("admin.html")