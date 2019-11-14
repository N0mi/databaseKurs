from flask import Flask, render_template, abort, redirect, url_for, session
import dbcontroller as dbc
import os

template_dir = os.path.abspath('../templates/')
app = Flask(__name__, template_folder=template_dir)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/list/')
def list_rooms():
    abort(401)
    return render_template('listRooms.html')


@app.route('/request/')
def request():
    return render_template('requestTicket.html')


@app.route('/journal/')
def journal():
    return render_template('journal.html')


@app.errorhandler(404)
def page_not_found(error):
    return "Такой страницы нет", 404


@app.errorhandler(401)
def page_login(error):
    return redirect(url_for('index'))


app.secret_key = str(os.urandom(24))
