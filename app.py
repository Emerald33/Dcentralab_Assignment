import os
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, request, redirect, url_for
from rag import rag

api_key = set()
load_dotenv()
if os.path.exists("./.env"):
    openai_api_key = os.getenv("OPENAI_API_KEY")
    api_key.add(openai_api_key)


app = Flask(__name__)

@app.route("/")
def welcome_page():
    return render_template('api_key.html')

@app.route("/rag/llamaindex")
def llamaindex_main():
    return render_template("llamaindex.html")


@app.route("/", methods = ['post'])
def upload_api_page():
    openai_api_key = request.form.get("openai_api_key")
    api_key.add(openai_api_key)
    return redirect(url_for("llamaindex_main"))

@app.route("/rag/llamaindex", methods = ['post'])
def llamaindex_page():
    data = request.form
    api_key_list = list(api_key)
    response = rag(str(api_key_list[0]), data['text_input'])

    return render_template("llamaindex_result.html",
                           generated = response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)