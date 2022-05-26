from flask import Flask
from .nope import KEY

app = Flask(__name__)

app.secret_key = KEY