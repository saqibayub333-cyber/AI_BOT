from flask import Flask, render_template, request, redirect, jsonify
import os
import csv
import re

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
    return ""

def get_bot_reply(user_msg, jewellery):
    msg = user_msg.lower()

    # 1. Mehanga wala
    if any(w in msg for w in ['mehenga','mehinga','mehnga','mehngha','expensive','price zyada','bohot mehenga']):
        return "Samajh sakta hun. Ye Indian imported jewellery hai, iski polish aur stone quality local se bohot behtar hai. Long lasting hai, kala nahi hota. Isi wajah se price thoda zyada hai."

    # 2. JazzCash / Payment
    if any(w in msg for w in ['jazz','cash','jazzcash','payment','paisa bhejna','account']):
        return "JazzCash: 03005639461 pe payment kar sakte hain. Payment ke baad screenshot bhej dein."

    # 3. Address / Shop
    if any(w in msg for w in ['address','location','shop kahan','kahan pe','dokan']):
        return "Hamari shop: Shop 1 Momin Market Gami Adda Abbottabad. Online delivery all Pakistan."

    # 4. MJ Code - product dhoondna
    for item in jewellery:
        code = str(item.get('code','')).lower()
        if code and code in msg:
            return f"{item.get('code')} available hai - Price: {item.get('price')} - {item.get('name','')}"

    # 5. Default
    return "Welcome Sir / Welcome Madam, hukum karen apko kya chahiye? Ap MJ code bata dein ya product ka naam."

    # 1. Gali check - NEVER reply with gali
    gali_words = ["bhen","behen","madar","chut","gandu","harami","kutti","kutta","randi","lora","lund"]
    if any(g in msg for g in gali_words):
        return "Welcome, Sir / Welcome, Madam, hukum karen apko kya chahiye?"

    # 2. Mehenga check
    if any(w in msg for w in ["mehenga","mehnga","mehinga","mehnga","price zyada","bohot zyada","bohat mehnga"]):
        return "Sir, ye imported item hai, hum bahir se mangwate hain, quality best hai is liye price ye hai. Welcome Sir."

    # 3. Guarantee / Kala check
    if any(w in msg for w in ["guarantee","kala","kaala","kale","rang","color"]):
        return "Sir, ye artificial hai, tareeqay se istemal karen to kuch nahi hota, long time chalta hai."

    # 4. Order Flow
    if any(w in msg for w in ["order","lena","chahiye","buy","mujhe ye"]):
        return "Sir/Madam, apna complete address bta dein?"

    # 5. Address lag raha hai (lamba msg, ya address likha)
    if len(msg) > 20 and any(w in msg for w in ["abbottabad","house","street","gali","colony","road","city","mohalla"]) or "address" in msg:
        return "Shukriya Sir/Madam, total price 2400 + 200 delivery = 2600. EasyPaisa / JazzCash 03005639461 pe payment kar dein."

    # 6. Payment / Screenshot
    if any(w in msg for w in ["payment","easypaisa","jazzcash","send kar di","kar diya"]):
        return "Payment ka screenshot bhej dein Sir/Madam."

    if any(w in msg for w in ["screenshot","screen shot","bhej diya","done"]):
        return "Shukriya Sir/Madam, apka order 5-6 din me apke address pe pohnch jayega."

    # 7. MJ Code search
    code_match = re.search(r'mj\s?(\d+)', msg)
    if code_match:
        code = f"MJ{code_match.group(1)}"
        if code in jewellery:
            item = jewellery[code]
            return f"{code} - {item['name']} available hai. Price: {item['final']} (Original {item['original']}). Order ke liye address bhej dein Sir."
    
    # 8. Choker / Kundan
    if "choker" in msg or "kundan" in msg:
        return f"Sir {msg} collection me kafi designs hain. Koi MJ code likho MJ1 se MJ122 tak."

    # Default
    return "Welcome Sir / Welcome Madam, hukum karen apko kya chahiye? Koi MJ code bhejein ya apna sawal likhein."

@app.route("/")
def home():
    return render_template("index.html", jewellery=load_data())

@app.route("/chat", methods=["POST"])
def chat():
   
  msg = user_msg.lower()
    if any(w in msg for w in ['mehenga','mehinga','mehnga','expensive','bohot mehenga']):
        return jsonify({"reply": "Samajh sakta hun Sir, ye Indian imported jewellery hai, quality local se bohot behtar hai, kala nahi hota. Original 3500 se discount me Final 3150 me de rahe hain."})
    if 'jazz' in msg or 'cash' in msg or 'payment' in msg:
        return jsonify({"reply": "JazzCash: 03005639461 pe payment kar sakte hain. Address: Shop 1 Momin Market Gami Adda Abbottabad."})  data = request.get_json()
    user_msg = data.get("message","")
    jewellery = load_data()
    reply = get_bot_reply(user_msg, jewellery)
    return jsonify({"reply": reply})

@app.route("/admin", methods=["GET", "POST"])
def admin():
    jewellery = load_data()
    bot_prompt = load_bot_prompt()
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
        new_bot_prompt = request.form.get("bot_prompt", bot_prompt)
        with open(BOT_FILE, 'w', encoding='utf-8') as bf:
            bf.write(new_bot_prompt)
        return redirect("/admin")
    return render_template("admin.html", jewellery=jewellery, bot_prompt=bot_prompt)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)