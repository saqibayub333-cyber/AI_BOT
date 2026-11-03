from flask import Flask, render_template, request, redirect
import os
import csv

app = Flask(__name__)

CSV_FILE = "jewellery_data.csv"
BOT_FILE = "bot_prompt.txt"

def load_data():
    jewellery = {}
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                code = row['code'].strip()
                if not code: continue
                jewellery[code] = {
                    "name": row['name'],
                    "original": int(row['original']),
                    "final": int(row['final']),
                    "img": f"{code}.jpg",
                    "category": row.get('category','mix')
                }
    for i in range(1, 501):
        code = f"MJ{i}"
        if os.path.exists(f"static/{code}.jpg") and code not in jewellery:
            jewellery[code] = {"name": f"Item {code}", "original": 3500, "final": 2400, "img": f"{code}.jpg", "category": "mix"}
    return jewellery

def load_bot_prompt():
    if os.path.exists(BOT_FILE):
        with open(BOT_FILE, 'r', encoding='utf-8') as f:
            return f.read()
    return """You are MJ Collection Bot - Polite & Respectful.
If customer says mehanga hai, say: Sir imported hai bahir se mangwate hain.
If guarantee, say: Artificial hai tareeqay se use karen to kuch nahi hota.
Ask for address, then price, then EasyPaisa/JazzCash 03005639461.
Ask for payment screenshot, then say order 5-6 days me pohnch jayega.
If gali, say Welcome Sir/Madam."""

@app.route("/")
def home():
    return render_template("index.html", jewellery=load_data())

@app.route("/admin", methods=["GET", "POST"])
def admin():
    jewellery = load_data()
    bot_prompt = load_bot_prompt()
    if request.method == "POST":
        # 1. Save jewellery CSV
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['code','name','original','final','category'])
            for code in jewellery:
                name = request.form.get(f"name_{code}", jewellery[code]['name'])
                orig = request.form.get(f"orig_{code}", jewellery[code]['original'])
                final = request.form.get(f"final_{code}", jewellery[code]['final'])
                cat = request.form.get(f"cat_{code}", jewellery[code]['category'])
                writer.writerow([code, name, orig, final, cat])
        
        # 2. Save Bot Prompt
        new_bot_prompt = request.form.get("bot_prompt", bot_prompt)
        with open(BOT_FILE, 'w', encoding='utf-8') as bf:
            bf.write(new_bot_prompt)
            
        return redirect("/admin")
    return render_template("admin.html", jewellery=jewellery, bot_prompt=bot_prompt)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)