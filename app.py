import os
from flask import Flask, render_template, request, redirect, url_for, session
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev")

def generate_response(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Tu es un expert AutoCAD Mac qui répond avec précision au chemin d'accès via la barre des menus et à la commande de la ligne de commande autoCAD associée, si elle existe."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        keyword = request.form["keyword"]
        prompt = (
            f"L'utilisateur veut accéder à '{keyword}' dans AutoCAD sur Mac. "
            "Donne uniquement le chemin d'accès via la barre des menus, puis la commande texte en français à saisir dans la ligne de commande si elle existe, "
            "en séparant les deux parties par un saut de ligne. "
            "Commence la première partie directement par le chemin, puis à la ligne suivante commence la commande directement, sans texte introductif."
        )
        response = generate_response(prompt)
        parts = response.split('\n', 1)
        session['chemin'] = parts[0].strip() if len(parts) > 0 else ""
        session['commande'] = parts[1].strip() if len(parts) > 1 else ""
        session['keyword'] = keyword
        return redirect(url_for('index'))
    chemin = session.pop('chemin', "")
    commande = session.pop('commande', "")
    keyword = session.pop('keyword', "")
    return render_template("index.html", chemin=chemin, commande=commande, keyword=keyword)

if __name__ == "__main__":
    app.run(debug=True)