from flask import Flask, render_template
import sqlalchemy
import psycopg2
import os

print(sqlalchemy.__version__)
conn = psycopg2.connect(dbname='pansionat', user='postgres',
						password = 'root', host='localhost')

cursor = conn.cursor()



template_dir = os.path.abspath('../templates/')
app = Flask(__name__, template_folder = template_dir)




@app.route('/')
def index():
	return render_template('index.html')

@app.route('/list')
def list():	
	cursor.execute('SELECT * FROM corps')
	for row in cursor:
		print(row)
	return render_template('listRooms.html')

@app.route('/request')
def request():
	return render_template('requestTicket.html')

@app.route('/journal')
def journal():
	return render_template('journal.html')

