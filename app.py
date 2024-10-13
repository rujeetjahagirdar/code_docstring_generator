import ast
import os
import json

from flask import Flask, request, jsonify, render_template, redirect
from flask_cors import CORS
from openai import OpenAI

from io import StringIO
from pylint.lint import Run
from pylint.reporters import JSONReporter
from pylint.lint import pylinter

app = Flask(__name__)
CORS(app)

client = OpenAI(
api_key = os.getenv('OPENAI_API_KEY'),
)


app.config['FILE_UPLOAD_FOLDER'] = './file_uploads/'

ALLOWED_EXTENSION = ["py"]


def process_file(code_file):
    pylinter.MANAGER.clear_cache()
    print("Processing file")
    pylint_output = StringIO()  # Custom open stream
    result = Run([code_file], reporter=JSONReporter(pylint_output), do_exit=False)
    result_json = json.loads(pylint_output.getvalue())
    # print("process_file result_json= ",result_json)
    issues = [i['message'] for i in result_json]
    return issues

def get_llm_suggestions(code_snippet, code_error):
    print("Getting LLM suggestions....")
    # print(code_snippet)
    issues = ',\n'.join(code_error)
    prompt = "Here is some python code.{code}\n Rewrite this piece of code to fix following issues\n \"{isssues}\". \
    \nDo not add your comments just give the rewritten code such that i can directly process the response.".format(code = code_snippet, isssues = issues)
    # print(prompt)
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "user",
                 "content": prompt},
            ],
            model='gpt-4-turbo',
            temperature=0.5,
            top_p=1,
            presence_penalty=0.3
        )
        print(response)
    except Exception as e:
        print("Error= ", e)
    # print("LLM Response= ",response)
    result = response.choices[0].message.content
    # print("result= ", result)
    return result

def parse_code_snippet(code_data):
    function_list = {}
    parsd_code = ast.parse(code_data)
    for node in ast.walk(parsd_code):
        if(isinstance(node, ast.FunctionDef)):
            f_name = node.name
            f_code = ast.get_source_segment(code_data, node)
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

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/generate_doc', methods=['POST'])
def generate_doc():
    code_file = request.files['code_file']
    code_data = code_file.read().decode('utf-8')
    functions = parse_code_snippet(code_data)
    doc_string = {}
    for f_name, f_code in enumerate(functions):
        doc_string[f_name] = generate_docstring(f_name, f_code)
    
    for i in doc_string:
        print(i)
        print(doc_string[i])
        print("##############")

    return jsonify({"docstrings": doc_string})

@app.route('/analyze_file', methods=['GET','POST'])
def analyze_file():
    if(request.method=='POST'):
        if ("code_file" not in request.files):
            # flash("Please select file!!")
            return redirect(request.url)
        code_file = request.files['code_file']
        #check file extension
        if(code_file.filename.split(".")[-1] not in ALLOWED_EXTENSION):
            # flash("Select valid file!! Only .py file allowed.")
            return redirect(request.url)
        file_path = os.path.join(app.config['FILE_UPLOAD_FOLDER'], code_file.filename)
        if(os.path.exists(file_path)):
            os.remove(file_path)
            print("File already exists!!! Deleting existing file.!!")
        code_file.save(file_path)
        print("File Saved !!!!!!!!")
        code_file.seek(0)
        code_data = code_file.read().decode('utf-8')
        issue_result = process_file(file_path)
        suggested_code = get_llm_suggestions(code_data, issue_result)
        os.remove(file_path)
        print("File Deleted!!!!")
        # print(type(suggested_code))
        return jsonify({"issues":issue_result, "original": code_data , "result": suggested_code})
    return render_template("analyze_file.html")


if __name__ == '__main__':
    app.run(debug=True)
