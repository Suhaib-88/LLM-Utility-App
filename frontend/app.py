# frontend/app.py (Flask)
from flask import Flask, render_template, request, jsonify
from app.utils.config_loader import load_component

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        model_option = request.form["model"]
        embedding_option = request.form["embedding"]
        vector_store_option = request.form["vector_store"]
        chain_option = request.form["chain"]
        input_text = request.form["input_text"]

        model = load_component(model_option, component_type="model")
        embedding = load_component(embedding_option, component_type="embedding")
        vector_store = load_component(vector_store_option, component_type="vector_store")
        chain = load_component(chain_option, component_type="chain", model=model, embedding=embedding, vector_store=vector_store)

        response = chain.run(input_text)
        return jsonify({"response": response})
    return render_template("index.html")