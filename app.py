import os
import json import csv
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
csv_FILE="jewellery_data.csv"

def get_bot_reply(user_msg, jewellery):
    msg = user_msg.upper().strip()
    if msg.startswith("MJ"):
        for item in jewellery:
            if item['code'] == msg:
                return f"{item['code']} - {item['name']} - Rs.{item['price']} | Photo: /static/{item['code']}.jpg"
        return "Ye code nahi mila, MJ1 se MJ122 tak likho"
    return "MJ code likho, jaise MJ101"

@app.route('/')
def index():
    jewellery_data = {}
    if os.path.exists(CSV_FILE):
    with open(CSV_FILE, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        jewellery_data = list(reader)
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    
    jewellery_data = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            jewellery_data = list(reader)

@app.route("/admin")
def admin():
  jewellery_data = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            jewellery_data = list(reader)
    return render_template('admin.html', jewellery=jewellery_data)  

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)