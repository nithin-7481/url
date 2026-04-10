from flask import Flask, request, jsonify, redirect
import json
import os
import string
import random

app = Flask(__name__)

FILE_NAME = "urls.json"
BASE_URL = "http://127.0.0.1:5000/"

# Load data
def load_urls():
    if not os.path.exists(FILE_NAME):
        return {}
    with open(FILE_NAME, "r") as f:
        return json.load(f)

# Save data
def save_urls(data):
    with open(FILE_NAME, "w") as f:
        json.dump(data, f, indent=4)

# Generate short code
def generate_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

# Home
@app.route("/")
def home():
    return jsonify({"message": "URL Shortener API Running 🚀"})

# Create short URL
@app.route("/shorten", methods=["POST"])
def shorten_url():
    data = request.json
    long_url = data.get("url")

    if not long_url:
        return jsonify({"error": "URL is required"}), 400

    urls = load_urls()

    code = generate_code()

    while code in urls:
        code = generate_code()

    urls[code] = long_url
    save_urls(urls)

    short_url = BASE_URL + code

    return jsonify({
        "short_url": short_url,
        "code": code
    })

# Redirect
@app.route("/<code>")
def redirect_url(code):
    urls = load_urls()

    if code in urls:
        return redirect(urls[code])
    else:
        return jsonify({"error": "Invalid URL"}), 404

# List all URLs
@app.route("/urls", methods=["GET"])
def list_urls():
    return jsonify(load_urls())

# Delete URL
@app.route("/delete/<code>", methods=["DELETE"])
def delete_url(code):
    urls = load_urls()

    if code in urls:
        del urls[code]
        save_urls(urls)
        return jsonify({"message": "Deleted successfully"})
    else:
        return jsonify({"error": "Code not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)