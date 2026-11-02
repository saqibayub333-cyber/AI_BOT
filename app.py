from flask import Flask, render_template, request, redirect
import os
import csv

app = Flask(__name__)

CSV_FILE = "jewellery_data.csv"

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

@app.route("/")
def home():
    return render_template("index.html", jewellery=load_data())

@app.route("/admin", methods=["GET", "POST"])
def admin():
    jewellery = load_data()
    if request.method == "POST":
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['code','name','original','final','category'])
            for code in jewellery:
                name = request.form.get(f"name_{code}", jewellery[code]['name'])
                orig = request.form.get(f"orig_{code}", jewellery[code]['original'])
                final = request.form.get(f"final_{code}", jewellery[code]['final'])
                cat = request.form.get(f"cat_{code}", jewellery[code]['category'])
                writer.writerow([code, name, orig, final, cat])
        return redirect("/admin")
    return render_template("admin.html", jewellery=jewellery)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)