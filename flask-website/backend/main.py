from flask import Flask, render_template
import os

template_dir = os.path.abspath('..')
app = Flask(__name__, template_folder = template_dir)




@app.route('/')
def index():
	return render_template('index.html')

@app.route('/list')
def list():
	return render_template('listRooms.html')

@app.route('/request')
def request():
	return render_template('requestTicket.html')

@app.route('/journal')
def journal():
	return render_template('journal.html')