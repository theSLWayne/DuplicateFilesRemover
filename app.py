from flask import Flask 
from flask import render_template, url_for, request, flash
from dr import duplicates, isDirValid, deleteFiles

app = Flask(__name__)

dirPath = ''

@app.route('/')
def Home():
    return render_template('home.html')

@app.route('/', methods=['POST'])
def Home_post():
    dirPath = request.form['text']
    if isDirValid(dirPath):
        flash("Valid Folder Path!")