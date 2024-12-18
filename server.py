from flask import Flask, request, jsonify
from transformers import pipeline
import json
from typing import List, Dict
import re
import jwt
import datetime
from flask_jwt_extended import JWTManager,jwt_required, create_access_token

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_secret_key'

ner_model = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")

qa_model = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

jwt = JWTManager(app)
def load_json_file(file_path: str) -> List[Dict]:
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def extract_entities_using_ner(query: str):
 
    entities = ner_model(query)
    return entities

def process_query_with_qa(query: str, context: str):
    result = qa_model(question=query, context=context)
    return result

def process_query(query: str, data: List[Dict]):
    
    entities = extract_entities_using_ner(query)
    print(f"Entities extracted: {entities}")

    # Process different types of queries
    if 'invoice' in query:
 
        context = " ".join([str(invoice) for invoice in data])
        answer = process_query_with_qa(query, context)
        return answer
    return {"message": "Unable to process the query."}

data = load_json_file('invoice.json')

@app.route('/query', methods=['POST'])
@jwt_required()
def query_handler():
    try:
        query = request.json.get('question', None)
        if not query:
            return jsonify({"error": "No question provided."}), 400
        query = query.strip()
        if not query:
            return jsonify({"error": "Invalid or empty query."}), 400
        response = process_query(query, data)
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if username == "admin" and password == "password":
        # Create the access token
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

if __name__ == '__main__':
    app.run()