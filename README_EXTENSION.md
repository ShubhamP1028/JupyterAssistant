# Data Science Assistant - Jupyter Notebook Extension

## Setup Instructions

### 1. Backend Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Create .env file with your Gemini API key:
echo "GEMINI_API_KEY=your_actual_api_key_here" > .env

# Start the Flask server
python app.py
```

### 2. Extension Setup
1. Open Chrome/Edge browser
2. Go to `chrome://extensions/`
3. Enable "Developer mode" (top right toggle)
4. Click "Load unpacked"
5. Select the `extension/` folder from this project
6. The extension should appear in your extensions list

### 3. Using the Extension
1. Start your Flask server (`python app.py`)
2. Open any Jupyter Notebook (localhost or JupyterHub)
3. Look for the "≡" button on the right side of the page
4. Click it to open the Data Science Assistant sidebar
5. Ask questions and generate code directly in your notebook!

## Features
- **Context-Aware**: Reads current cell content and imports
- **Direct Insertion**: Insert generated code directly into active cell
- **Copy Function**: Copy code to clipboard
- **Keyboard Shortcut**: Ctrl+Shift+A to toggle sidebar
- **Jupyter Compatible**: Works with both Classic Notebook and JupyterLab

## API Endpoints
- `GET /extension/health` - Check if backend is running
- `POST /ask` - Generate code (used by extension)

## Troubleshooting
- Make sure Flask server is running on port 5050
- Check browser console for any errors
- Verify your Gemini API key is correct in .env file
- Ensure extension has proper permissions
