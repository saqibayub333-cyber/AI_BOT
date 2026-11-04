from flask import Flask, render_template, request, jsonify
import datetime
import os

app = Flask(__name__)

# ===== MJ JEWELLERY - SETTINGS =====
MALIK_NUMBER = "03005639461"
JAZZCASH_NUMBER = "03005639461"
EASYPAISA_NUMBER = "03005639461"
SHOP_NAME = "MJ Jewellery Shop"

# ===== DESIGNS - Yahan apne design add karo =====


# AUTO LOAD - MJ1 se MJ99 tak
import os

jewellery = {}
for i in range(1, 100):
    code = f"MJ{i}"
    fname = f"MJ{i}.jpg"
    if os.path.exists(os.path.join("static", fname)):
        jewellery[code] = {
            "name": f"Design {code}",
            "img": fname,
            "price": 52000,
            "original": 65000
        }

ORDERS = []

# ===== HOME PAGE - TAB WALA DESIGN =====
HTML = """
<!DOCTYPE html>
<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<title>MJ Jewellery Shop</title>
<style>
body{font-family:Arial;background:#fff8e1;text-align:center;padding:20px}
h1{color:#b8860b} .card{background:white;padding:15px;margin:10px;border-radius:15px;box-shadow:0 0 10px #ddd}
button{background:#b8860b;color:white;border:none;padding:12px 20px;border-radius:10px;font-size:16px;width:100%;margin-top:10px}
select,input{width:100%;padding:12px;margin:5px 0;border-radius:10px;border:1px solid #ccc;font-size:16px}
</style></head>
<body>
<h1>💎 MJ Jewellery Shop 💎</h1>
<p>Assalam-o-Alaikum! Khushamdeed</p>

<h3>Design Select Karein</h3>
{% for d in designs %}
<div class="card">
<b>{{d.code}} - {{d.name}}</b><br>
Price: Rs {{d.price}}<br>
Stock: {{d.stock}} Available<br>
<button onclick="selectDesign('{{d.code}} - {{d.name}} - Rs {{d.price}}')">Ye Wala Select Karein</button>
</div>
{% endfor %}

<div class="card">
<h3>Order Final Karein</h3>
<input id="design" placeholder="Design yahan aa jayega" readonly>
<input id="name" placeholder="Aapka Naam">
<input id="address" placeholder="Poora Address">
<select id="payment">
<option>Cash - Shop Pe</option>
<option>JazzCash - 03005639461</option>
<option>EasyPaisa - 03005639461</option>
</select>
<button onclick="finalOrder()">Order Final Karein</button>
<p id="msg" style="color:green;font-weight:bold"></p>
</div>

<script>
function selectDesign(d){ document.getElementById('design').value=d; }
function finalOrder(){
  let data={design:document.getElementById('design').value, name:document.getElementById('name').value, address:document.getElementById('address').value, payment:document.getElementById('payment').value};
  fetch('/order',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)})
  .then(r=>r.json()).then(r=>{ document.getElementById('msg').innerText=r.message; });
}
</script>
<p>Payment: JazzCash / EasyPaisa - <b>0300 5639461</b><br>Malik Number: <b>0300 5639461</b></p>
</body></html>
"""

@app.route('/')
def home():
    return render_template("index.html", jewellery=jewellery)

# ===== BOT KI BAAT-CHEET - IKHLAQ WALA =====
def get_bot_reply(msg):
    msg = msg.lower().strip()

    # Salam
    if "salam" in msg or "hi" in msg or "hello" in msg:
        return "Walaikum Salam Sahb, kaunsa design dekhna hai? MJ code bata den."

    # JazzCash / EasyPaisa
    if "jazz" in msg or "easypaisa" in msg or "payment" in msg or "paisa" in msg:
        return "JazzCash / EasyPaisa: 03005639461 hai Sahb. Send karke screenshot bhej den."

    # Delivery
    if "delivery" in msg or "dc" in msg or "kab" in msg or "pohanch" in msg:
        return "All Pakistan Delivery hai Sahb, 2-3 din me pohanch jayega."

    # Address / Shop
    if "shop" in msg or "address" in msg or "kahan" in msg or "dukhan" in msg:
        return "Shop No 1, Momin Market, Gami Adda, Abbottabad."

    # Price
    if "price" in msg or "rate" in msg or "kimat" in msg:
        return "Kaunsa code hai Sahb? MJ code likhen, mai price bata deta hun."

    # MJ Code - MJ1 se MJ98
    for code in jewellery:
        if code.lower() in msg:
            item = jewellery[code]
            return f"{code} available hai, Price {item['price']} hai. Order ke liye WhatsApp kar den."

    # Choker / Kundan
    if "choker" in msg:
        return "Choker wale MJ12, MJ25, MJ40 me hain. Kaunsa dekhna hai?"
    if "kundan" in msg:
        return "Kundan wale MJ8, MJ9 me hain. Price 65000 hai."

    # Na samajh aaye to
    return "Samajh nahi aaya Sahb, MJ code likhen ya JazzCash likhen."

# ===== WHATSAPP / FACEBOOK / INSTA / TIKTOK SE AANE WALA MESSAGE =====
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json or {}
    user_msg = data.get("message", "")
    reply=get_bot_reply(user_msg)
    # Yahan se order Malik ke number pe jayega - Phase 2 me WhatsApp API lagegi
    print(f"Customer: {user_msg} | Bot: {reply} | Malik ko bhejna hai: {MALIK_NUMBER}")
    return jsonify({"reply": reply, "send_to_malik": MALIK_NUMBER})

# ===== TAB SE ORDER - MALIK KI SCREEN PE JAYEGA =====
@app.route('/order', methods=['POST'])
def order():
    data = request.json or {}
    data["time"] = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
    ORDERS.append(data)
    print(f"NEW ORDER FOR MALIK {MALIK_NUMBER}: {data}")
    return jsonify({"message": f"Shukriya {data.get('name','')}! Aapka order final ho gaya. Payment {data.get('payment')} pe karein - 0300 5639461. Malik ko aapka order mil gaya hai."})

# ===== MALIK KI SCREEN - SAARE ORDERS =====
@app.route('/malik')
def malik_orders():
    html = "<h1>Malik - Saare Orders</h1>"
    for o in ORDERS:
        html += f"<p>{o.get('time')} | {o.get('name')} | {o.get('design')} | {o.get('payment')} | {o.get('address')}</p>"
    if not ORDERS:
        html += "<p>Abhi koi order nahi hai.</p>"
    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
