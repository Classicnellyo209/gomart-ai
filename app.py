import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- AUTO-CREATE TEMPLATES FOLDER AND FILES ---
# This will fix the error forever
if not os.path.exists('templates'):
    os.makedirs('templates')

# Create welcome.html automatically if missing
welcome_path = 'templates/welcome.html'
if not os.path.exists(welcome_path):
    with open(welcome_path, 'w', encoding='utf-8') as f:
        f.write("""<!DOCTYPE html>
<html><head><title>Go Mart Welcome</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:Segoe UI}
body{background:#0A5C36;height:100vh;display:flex;align-items:center;justify-content:center;overflow:hidden}
.container{text-align:center;color:white}
.logo{font-size:100px;animation:bounce 2s infinite}
@keyframes bounce{0%,20%,50%,80%,100%{transform:translateY(0)}40%{transform:translateY(-30px)}60%{transform:translateY(-15px)}}
h1{font-size:36px;margin-top:10px}h1 span{color:#8CFF8C}
p{font-size:14px;margin-top:10px;opacity:0.9}
.btn{background:white;color:#0A5C36;padding:14px 40px;border-radius:30px;border:none;font-size:16px;font-weight:bold;margin-top:30px;cursor:pointer;display:inline-block;text-decoration:none;box-shadow:0 5px 15px rgba(0,0,0,0.3)}
</style></head>
<body><div class="container"><div class="logo">🛒</div><h1>GO MART <span>SUPERMARKET</span></h1><p>AI CUSTOMER SUPPORT</p><a href="/chat" class="btn">Start Chatting →</a><p style="font-size:11px;margin-top:15px">● Online 24/7</p></div></body></html>
""")

# Create index.html automatically if missing
index_path = 'templates/index.html'
if not os.path.exists(index_path):
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write("""<!DOCTYPE html>
<html><head><title>Go Mart Chat</title><meta name="viewport" content="width=device-width, initial-scale=1">
<style>*{margin:0;padding:0;box-sizing:border-box;font-family:Segoe UI}body{height:100vh;display:flex;flex-direction:column}.header{background:#0A5C36;color:white;padding:12px 20px;display:flex;justify-content:space-between}.main{flex:1;display:flex;overflow:hidden}.left{width:200px;background:#fff;border-right:1px solid #ddd;padding:10px}.center{flex:1;background:#F2F5F3;display:flex;flex-direction:column}.chat-box{flex:1;overflow:auto;padding:15px}.msg{display:flex;gap:8px;margin:10px 0}.msg.user{justify-content:flex-end}.bubble{background:white;padding:10px;border-radius:10px;max-width:75%;font-size:13px}.user .bubble{background:#FFF9C4}.input-area{display:flex;gap:8px;padding:10px;background:white;border-top:1px solid #ddd}.input-area input{flex:1;padding:12px;border-radius:20px;border:1px solid #ccc}.input-area button{background:#0A5C36;color:white;border:none;padding:10px 20px;border-radius:20px}</style></head>
<body><div class="header"><b>GO MART</b><span>● Online</span></div><div class="main"><div class="left">Chat with AI</div><div class="center"><div class="chat-box" id="chatBox"><div class="msg"><div class="bubble">Hello! Welcome to Go Mart. How can I help?</div></div></div><div class="input-area"><input id="userInput" placeholder="Type message..."><button onclick="sendMessage()">Send</button></div></div><div class="right">Milo - N4,200<br>Coke - N600<br>Indomie - N100</div></div>
<script>async function sendMessage(){let input=document.getElementById('userInput');let msg=input.value.trim();if(!msg)return;let box=document.getElementById('chatBox');box.innerHTML+=`<div class="msg user"><div class="bubble">${msg}</div></div>`;input.value='';let res=await fetch('/get_response',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:msg})});let data=await res.json();box.innerHTML+=`<div class="msg"><div class="bubble">${data.response}</div></div>`;box.scrollTop=box.scrollHeight}document.getElementById('userInput').addEventListener('keypress',e=>{if(e.key==='Enter')sendMessage()})</script></body></html>
""")

# --- YOUR ORIGINAL WORKING LOGIC ---
products = {
    "milo": {"name": "Milo 400g", "price": 4200, "stock": 30},
    "coca-cola": {"name": "Coca-Cola 50cl", "price": 600, "stock": 80},
    "indomie": {"name": "Indomie Noodles", "price": 100, "stock": 100},
}

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/chat')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    msg = request.json.get('message','').lower()
    if "milo" in msg:
        return jsonify({"response": "Milo 400g is N4,200. 30 in stock."})
    if "available" in msg:
        return jsonify({"response": "We have Milo, Coke, Indomie, Spaghetti, Peak Milk."})
    return jsonify({"response": "Hello! Welcome to Go Mart. How can I help you?"})

if __name__ == '__main__':
    print("Templates folder fixed! Now opening...")
    app.run(debug=True)