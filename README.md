# 📝 Code Docstring Generator

This project is a **Code Docstring Generator** that takes Python code as input and generates docstrings for the functions in the code using **Large Language Models (LLM)**. It is built with a **Flask** backend, utilizes **OpenAI's GPT model** for natural language generation, and demonstrates skills in backend development, Python programming, frontend integration, and modern **LLMs**.

## 🚀 Features

- **Backend Development**: Uses **Flask** to build a robust API that handles code uploads and docstring generation.
- **Code Parsing**: Leverages Python's **AST (Abstract Syntax Tree)** to extract function definitions and their source code.
- **LLM Integration**: Utilizes **OpenAI GPT** models to generate meaningful and descriptive docstrings for Python functions.
- **REST API**: Offers a POST API endpoint that accepts a Python file, processes the functions, and returns generated docstrings in JSON format.
- **Frontend**: A simple **HTML page** to upload Python files, built using **Flask's template engine**.
- **CORS Enabled**: Supports cross-origin requests using **Flask-CORS**, making it easy to integrate with frontend or external applications.

## 📂 Project Structure
. 

├── app.py # Main Flask application 

├── templates/ 

│└── index.html # Frontend HTML page 

├── requirements.txt # Dependencies for the project 

└── README.md # Project documentation (this file)


## 📋 Requirements

- **Python 3.8+**
- **Flask**: A micro web framework for Python.
- **OpenAI Python SDK**: For interaction with OpenAI's API.
- **Transformers**: For managing models and tokenization (if needed for other model usage).
- **Flask-CORS**: To enable cross-origin requests.

Install the necessary dependencies using:

```bash
pip install -r requirements.txt
```
## 🛠️ Key Technologies

- **Backend**: Flask
- **Frontend:** Basic HTML (with index.html in the templates folder)
- **Natural Language Processing (NLP)**: OpenAI's GPT models for generating docstrings.
- **Code Parsing**: Python's built-in `ast` library to analyze and extract function definitions.
- **API Development**: RESTful API to handle file uploads and return responses in JSON.
- **CORS Handling**: Flask-CORS for cross-origin resource sharing.
- **Model Loading**: Using `transformers` for managing models and tokenizers.

## 🧑‍💻 Usage

1. **Set up OpenAI API Key**: Make sure to have an OpenAI API key and set it in your environment variables.

```bash
export OPENAI_API_KEY='your-openai-api-key'
```

2. **Run the Flask App:**
```
python app.py
```
3. **Access the Frontend:**

Once the Flask app is running, open your browser and navigate to:
```
http://127.0.0.1:5000
```
4. **API Endpoint:** 
The application exposes a single POST endpoint:

    /generate_doc: This accepts a .py file, processes the functions, and generates a docstring for each function.

    Example request using curl:
```
curl -X POST -F 'code_file=@your_script.py' http://127.0.0.1:5000/generate_doc
```
The API will return a JSON object containing the function names and the generated docstrings.
