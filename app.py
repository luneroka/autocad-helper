import os
from flask import Flask, render_template, request
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

def generate_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Tu es un expert AutoCAD Mac qui répond avec précision au chemin d'accès via la barre des menus et à la commande clavier associée, si elle existe."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message["content"]

@app.route("/", methods=["GET", "POST"])
def index():
    response = ""
    if request.method == "POST":
        user_input = request.form["keyword"]
        prompt = f"L'utilisateur veut accéder à '{user_input}' dans AutoCAD sur Mac. Donne uniquement le chemin dans la barre des menus, puis le raccourci clavier s’il existe."
        response = generate_response(prompt)
    return render_template("index.html", response=response)

if __name__ == "__main__":
    app.run(debug=True)