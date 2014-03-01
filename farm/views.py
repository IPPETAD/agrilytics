from farm import app
from flask import render_template, request

@app.route('/')
def index():
    return render_template('home.html')
    