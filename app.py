from flask import Flask 
from flask import render_template, url_for, request, flash, redirect, json, session
from dr import duplicates, isDirValid, deleteFiles

app = Flask(__name__)
app.secret_key = "b'\x0c\x83\xb9jL\x87\xc9\x9e\x16\xbe\xa2.\xae&\xb6\x1a\xb8\x05E\xd1\xea\x83\x8a\xdf'"

dirPath = ''

@app.route('/')
def Home():
    return render_template('home.html')

@app.route('/', methods=['POST'])
def Home_post():
    dirPath = request.form['folderpath']
    dPath = json.dumps(dirPath)
    session['dPath'] = dPath
    if isDirValid(dirPath):
        return redirect(url_for('DupRem', dPath=dPath))
    else:
        flash('The folder path is invalid.', 'error')
        return redirect(url_for('Home'))

@app.route('/duprem')
def DupRem():
    dPath = request.args['dPath']
    dPath = session['dPath']
    return 'OK'