# Surch: A Conversational Search Engine
Surch is a conversational search engine that leverages advanced language models to provide accurate and context-aware answers to user queries. This project includes a command-line interface (CLI) and a web interface built with Streamlit.

## Features
- Conversational Search: Engage in a conversation with the search engine to get answers to your questions.
- History Retrieval: Access previous conversations and continue from where you left off.
- Web Interface: Use the Streamlit-based web interface for a more interactive experience.

## Installation
1. Clone the repository:
```bash
git clone https://github.com/aayushjoshi-12/surch.git
cd surch
```

2. Install the required packages and set up environment:
```bash
uv sync
uv venv
source .venv/bin/activate
```

3. Set up your API keys in the Streamlit secrets file (`.streamlit/secrets.toml`):
```
API_KEY = "your_google_api_key"
CSE_ID = "your_custom_search_engine_id"
ACCESS_TOKEN = "your_huggingface_access_token"
GROQ_API_KEY = "your_groq_api_key"
```

## Usage
### Command-Line Interface (CLI)
To start a new conversation or retrieve history, use the CLI:

Start a new conversation:
```bash
python surch-cli.py -u <user_id> -n
```

Retrieve previous conversations:
```bash
python surch-cli.py -u <user_id> -H
```

### Web Interface
To use the web interface, run the Streamlit app:
```bash
streamlit run app.py
```
or visit https://surch-12.streamlit.app

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements
HuggingFace for providing the language models.
Streamlit for the web interface framework.
LangChain for the conversational AI tools.