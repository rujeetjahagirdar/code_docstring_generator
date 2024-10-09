import ast
import os

from flask import Flask, request, jsonify
from openai import OpenAI
# Load model directly
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch

from holoviews.operation import method

app = Flask(__name__)

client = OpenAI(
api_key = os.getenv('OPENAI_API_KEY'),
)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!@@@@'


def parse_code_snippet(code_data):
    function_list = []
    parsd_code = ast.parse(code_data)
    for node in ast.walk(parsd_code):
        if(isinstance(node, ast.FunctionDef)):
            function_list.append(node.name)
    return function_list

def generate_docstring(fun):
    prompt = f"Generate a detailed Python docstring for the following function:\n\n{fun}. Do not add your comments just \
    give the docstring such that i can directly process the response. Give output in Markdown."

    response = client.beta.chat.completions.parse(
        messages= [
            {"role" : "user",
             "content":prompt},
        ],
        model = 'gpt-4o-mini',
        # response_format=similar
    )

    docStr = response.choices[0].message.content
    print(docStr)
    return docStr


@app.route('/generate_doc', methods=['POST'])
def generate_doc():
    code_data = request.json.get('code')
    functions = parse_code_snippet(code_data)
    print(functions)
    doc_string = {}
    for f in functions:
        doc_string[f] = generate_docstring(f)
    print(doc_string)
    return jsonify(doc_string)

if __name__ == '__main__':
    app.run(debug=True)
