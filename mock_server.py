#!/usr/bin/env python3
"""
Mock server for testing the extension without requiring a real Gemini API key.
Run this instead of app.py for testing purposes.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(
    app,
    resources={r"/*": {"origins": [
        "chrome-extension://*",
        "moz-extension://*",
        "http://localhost:*",
        "http://127.0.0.1:*"
    ]}}
)

# Mock responses for common data science queries
MOCK_RESPONSES = {
    "plot": "```python\nimport matplotlib.pyplot as plt\nimport numpy as np\n\n# Create sample data\nx = np.linspace(0, 10, 100)\ny = np.sin(x)\n\n# Create plot\nplt.figure(figsize=(10, 6))\nplt.plot(x, y)\nplt.title('Sample Plot')\nplt.xlabel('X')\nplt.ylabel('Y')\nplt.grid(True)\nplt.show()\n```",
    
    "dataframe": "```python\nimport pandas as pd\n\n# Create sample DataFrame\ndata = {\n    'name': ['Alice', 'Bob', 'Charlie'],\n    'age': [25, 30, 35],\n    'city': ['New York', 'London', 'Tokyo']\n}\ndf = pd.DataFrame(data)\nprint(df)\n```",
    
    "merge": "```python\n# Merge two DataFrames on common column\nresult = pd.merge(df1, df2, on='id')\n\n# Left join\nresult = pd.merge(df1, df2, on='id', how='left')\n\n# Outer join\nresult = pd.merge(df1, df2, on='id', how='outer')\n```",
    
    "default": "```python\n# Data Science template\nimport pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\n\n# Your code here\nprint('Hello Data Science!')\n```"
}

def get_mock_response(query):
    """Generate a mock response based on query keywords."""
    query_lower = query.lower()
    
    if any(word in query_lower for word in ['plot', 'graph', 'chart', 'visualize']):
        return MOCK_RESPONSES['plot']
    elif any(word in query_lower for word in ['dataframe', 'df', 'table']):
        return MOCK_RESPONSES['dataframe']
    elif any(word in query_lower for word in ['merge', 'join', 'combine']):
        return MOCK_RESPONSES['merge']
    else:
        return MOCK_RESPONSES['default']

@app.route("/")
def index():
    return jsonify({"message": "Mock Data Science Assistant API", "status": "running"})

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    query = data.get("question", "").strip()
    
    if not query:
        return jsonify({"error": "No question provided"}), 400
    
    # Simulate API delay
    import time
    time.sleep(1)
    
    answer = get_mock_response(query)
    return jsonify({"answer": answer})

@app.route("/extension/health")
def extension_health():
    return jsonify({
        "status": "ok",
        "model": "mock-model",
        "ready": True
    })

@app.route("/test")
def test():
    return jsonify({"status": "active", "model": "mock-model"})

if __name__ == "__main__":
    print("🚀 Starting Mock Data Science Assistant Server...")
    print("📡 Server will run on http://127.0.0.1:5050")
    print("🔧 This is a mock server - no real API calls will be made")
    print("📝 Use this for testing the extension without a Gemini API key")
    app.run(debug=True, host="127.0.0.1", port=5050, use_reloader=False)
