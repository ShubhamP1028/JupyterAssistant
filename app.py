from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from flask_cors import CORS
from dotenv import load_dotenv
import re

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)       # by default looks in ./templates for HTML
# Restrict CORS to browser extension and local pages
CORS(
    app,
    resources={r"/*": {"origins": [
        "chrome-extension://*",
        "moz-extension://*",
        "http://localhost:*",
        "http://127.0.0.1:*"
    ]}}
)

# Configure Gemini API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("No GEMINI_API_KEY in .env")
genai.configure(api_key=api_key)

# Initialize model (use one of the supported IDs)
model = genai.GenerativeModel("gemini-2.0-flash")
# — or: genai.GenerativeModel("gemini-2.0-pro")

def extract_code_block(text):
    # 1) Try full fenced block
    full = re.search(r"```(?:python)?[\r\n]+([\s\S]*?)[\r\n]+```", text)
    if full:
        inner = full.group(1).strip()
        return f"```python\n{inner}\n```"
    # 2) Fallback: look for code‑like keywords
    if any(kw in text for kw in ("import ", "def ", "plt.", "np.", "pd.", "__name__")):
        cleaned = text.strip().strip('"').strip("'")
        return f"```python\n{cleaned}\n```"
    # 3) Nothing code‑like → return plain text
    return text.strip()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    q = data.get("question", "").strip()
    if not q:
        return jsonify({"error": "No question provided"}), 400

    prompt = (
        "You are a helpful Data Science assistant. "
        "For each request, provide only the *simplest*, *executable*, "
        "and *properly functioning* Python code snippet that directly solves the task. "
        "Use the most appropriate library and include only necessary imports. "
        "Do NOT include comments or extra examples. "
        "Wrap the code in markdown triple backticks:\n\n"
        "```python\n"
        "# code here\n"
        "```\n\n"
        f"Task: {q}"
    )

    resp = model.generate_content(
        prompt,
        generation_config={
            "max_output_tokens": 2048,
            "temperature": 0.4,
            "top_p": 0.9,
            "top_k": 50
        },
        safety_settings={
            "HARASSMENT": "block_only_high",
            "HATE_SPEECH": "block_only_high",
            "SEXUAL": "block_only_high",
            "DANGEROUS": "block_only_high",
        }
    )

    code = extract_code_block(resp.text)
    return jsonify({"answer": code})

@app.route("/test")
def test():
    return jsonify({"status": "active", "model": model.name})

# Simple endpoint for the extension to verify connectivity
@app.route("/extension/health")
def extension_health():
    return jsonify({
        "status": "ok",
        "model": model.name,
        "ready": True
    })

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5050, use_reloader=False)
