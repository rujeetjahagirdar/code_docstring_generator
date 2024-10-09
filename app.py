import ast
import os

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from openai import OpenAI


app = Flask(__name__)
CORS(app)

client = OpenAI(
api_key = os.getenv('OPENAI_API_KEY'),
)

@app.route('/')
def home():
    return render_template('index.html')

def parse_code_snippet(code_data):
    function_list = {}
    parsd_code = ast.parse(code_data)
    for node in ast.walk(parsd_code):
        if(isinstance(node, ast.FunctionDef)):
            f_name = node.name
            f_code = ast.get_source_segment(code_data, node)
            # print("Function name= ",f_name)
            # print(node.body)
            # print("Function code= ",f_code)
            function_list[f_name] = f_code
    return function_list

def generate_docstring(fun_name, fun_code):
    prompt = f'Analyze the following function and Generate a detailed Python docstring based on what is the input to the function, what it is doing and what is the output for the following function:"\n\n{fun_name}\n{fun_code}". Do not add your comments just give the docstring such that i can directly process the response.'

    response = client.chat.completions.create(
        messages= [
            {"role" : "user",
             "content":prompt},
        ],
        model = 'gpt-4-turbo',
        temperature=0.7,
        top_p=1,
        presence_penalty=0.3
    )

    docStr = response.choices[0].message.content
    # print(docStr)
    return docStr


@app.route('/generate_doc', methods=['POST'])
def generate_doc():
    # code_data = request.json.get('code')
    # print("inside gene")
    code_file = request.files['code_file']
    code_data = code_file.read().decode('utf-8')
    functions = parse_code_snippet(code_data)
    # print("functions= ", functions)
    doc_string = {}
    for f_name, f_code in enumerate(functions):
        doc_string[f_name] = generate_docstring(f_name, f_code)
    
    for i in doc_string:
        print(i)
        print(doc_string[i])
        print("##############")

    return jsonify({"docstrings": doc_string})

if __name__ == '__main__':
    app.run(debug=True)
