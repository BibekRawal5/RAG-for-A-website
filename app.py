from flask import Flask, request, jsonify, render_template
from chatbot_service import retrieve_answer
from vector_store import load_site_into_db

app = Flask(__name__)

SEED_URL = "https://amusetechsolutions.com/" 

load_site_into_db(SEED_URL)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("question")
    if not user_input:
        return jsonify({"error": "No question provided"}), 400
    answer = retrieve_answer(user_input)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)
