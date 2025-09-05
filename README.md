# 🤖 Data Science Assistant - Jupyter Notebook Extension

A powerful browser extension that brings AI-powered code generation directly to your Jupyter Notebook environment. Get instant help with data science tasks, code suggestions, and automated code insertion.

![Extension Demo](https://img.shields.io/badge/Status-Ready-brightgreen)
![Chrome Extension](https://img.shields.io/badge/Chrome-Extension-blue)
![Jupyter Compatible](https://img.shields.io/badge/Jupyter-Compatible-orange)

## ✨ Features

- **🎯 Context-Aware AI**: Reads your current cell content and imports for smarter suggestions
- **📝 Direct Code Insertion**: Insert generated code directly into active Jupyter cells
- **🔄 Retractable Sidebar**: Toggle with button or `Ctrl+Shift+A` keyboard shortcut
- **📋 Copy Functionality**: Copy code to clipboard with one click
- **🧪 Mock Testing**: Test without API keys using the included mock server
- **🔧 Jupyter Compatible**: Works with both JupyterLab and Classic Notebook
- **⚡ Real-time Generation**: Get instant code suggestions as you type

## 🚀 Quick Start

### 1. Backend Setup
```bash
# Clone the repository
git clone https://github.com/ShubhamP1028/DS_Assistant.git
cd DS_Assistant

# Install dependencies
pip install -r requirements.txt

# Option A: Use with real Gemini API
echo "GEMINI_API_KEY=your_actual_api_key_here" > .env
python app.py

# Option B: Use mock server for testing
python mock_server.py
```

### 2. Extension Setup
1. Open Chrome/Edge browser
2. Go to `chrome://extensions/`
3. Enable "Developer mode" (top right toggle)
4. Click "Load unpacked"
5. Select the `extension/` folder from this project
6. The extension should appear in your extensions list

### 3. Using the Extension
1. Start your Flask server (`python app.py` or `python mock_server.py`)
2. Open any Jupyter Notebook (localhost or JupyterHub)
3. Look for the "≡" button on the right side of the page
4. Click it to open the Data Science Assistant sidebar
5. Ask questions and generate code directly in your notebook!

## 📁 Project Structure

```
DS_Assistant/
├── extension/                 # Browser extension files
│   ├── manifest.json         # Extension configuration
│   ├── content.js           # Main extension logic
│   ├── content.css          # Sidebar styling
│   └── popup.html           # Extension popup
├── templates/                # Flask templates
│   ├── index.html           # Main web interface
│   └── data_science_assistant.html
├── app.py                   # Flask server with Gemini AI
├── mock_server.py           # Mock server for testing
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🎯 Usage Examples

### Basic Queries
- "Create a simple plot with matplotlib"
- "Merge two DataFrames on column id"
- "Remove duplicates from DataFrame"
- "Handle missing values in dataset"
- "Create a histogram of column age"

### Advanced Features
- **Context Awareness**: The extension reads your current cell content
- **Import Detection**: Automatically detects existing imports
- **Smart Suggestions**: Provides relevant code based on your notebook context

## 🔧 API Endpoints

- `GET /extension/health` - Check if backend is running
- `POST /ask` - Generate code (used by extension)
- `GET /test` - Test endpoint

## 🛠️ Development

### Running Tests
```bash
# Start mock server
python mock_server.py

# Test API endpoints
curl http://127.0.0.1:5050/extension/health
```

### Extension Development
1. Make changes to files in `extension/` folder
2. Reload the extension in Chrome (`chrome://extensions/`)
3. Test on Jupyter Notebook pages

## 📋 Requirements

- Python 3.7+
- Chrome/Edge browser
- Flask and dependencies (see `requirements.txt`)
- Gemini API key (optional, mock server available)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/)
- AI powered by [Google Gemini](https://ai.google.dev/)
- Extension framework by [Chrome Extensions API](https://developer.chrome.com/docs/extensions/)

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/ShubhamP1028/DS_Assistant/issues) page
2. Create a new issue with detailed description
3. Include browser version and error messages

---

**Made with ❤️ for the Data Science community**
