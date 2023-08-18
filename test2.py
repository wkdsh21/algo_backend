
import requests
from flask import Blueprint, jsonify, request
from flask import Flask
app = Flask(__name__)

@app.route('/',methods=["POST"])
def hello():
    print(request.files)
    return "Hello, client! This is the response from the Flask server."

if __name__ == '__main__':
    app.run()