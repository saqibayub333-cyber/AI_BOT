from flask import Flask, request, jsonify, render_template
import json
import csv
import os

app = Flask(__name__)

CSV_FILE = 'jewellery_data.csv'

@app.route('/')
def home():
    return "MJ BOT is Live!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    return jsonify({"status": "ok"})

@app.route('/admin')
def admin():
    jewellery_data = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            jewellery_data = list(reader)
    return render_template('admin.html', jewellery=jewellery_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)