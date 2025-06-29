import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev")
APP_PASSCODE = os.getenv("APP_PASSCODE")  # Default for dev

def generate_response(keyword):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Expert AutoCAD Mac. Réponds par chemin d'accès puis ligne de commande si elle existe."},
            {"role": "user", "content": f"Pour '{keyword}' dans AutoCAD Mac, donne chemin d'accès puis ligne de commande (s'il y en a une), séparés par un saut de ligne, sans texte introductif."}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        passcode = request.form.get("passcode", "")
        if passcode == APP_PASSCODE:
            session["authenticated"] = True
            return redirect(url_for("index"))
        flash("Code incorrect.")
    return render_template("login.html")

@app.route("/", methods=["GET", "POST"])
def index():
    if not session.get("authenticated"):
        return redirect(url_for("login"))
    if request.method == "POST":
        keyword = request.form["keyword"]
        response = generate_response(keyword)
        parts = response.split('\n', 1)
        session['chemin'] = parts[0].strip() if len(parts) > 0 else ""
        commande = parts[1].strip() if len(parts) > 1 else ""
        if not commande:
            commande = "Commande non trouvée"
        session['commande'] = commande
        session['keyword'] = keyword
        return redirect(url_for('index'))
    chemin = session.pop('chemin', "")
    commande = session.pop('commande', "")
    keyword = session.pop('keyword', "")
    return render_template("index.html", chemin=chemin, commande=commande, keyword=keyword)

if __name__ == "__main__":
    app.run(debug=True)