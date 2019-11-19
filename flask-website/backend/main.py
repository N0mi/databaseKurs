from flask import Flask, render_template, abort, redirect, url_for, session
import dbcontroller as dbc
import os

class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        variable_start_string='%%',  # Default is '{{', I'm changing this because Vue.js uses '{{' / '}}'
        variable_end_string='%%',
    ))


template_dir = os.path.abspath('../templates/')
app = CustomFlask(__name__, template_folder=template_dir)
app._static_folder = os.path.abspath('../static')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/admin/')
def adPanel():
    return render_template('adminPanel.html')


@app.route('/journal/')
def journal():
    return render_template('journal.html')


@app.route('/login/')
def login():
    return render_template('login.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error404.html'), 404
    # return "Error 404. Такой страницы нет", 404


@app.errorhandler(401)
def page_login(error):
    return redirect(url_for('index'))


app.secret_key = str(os.urandom(24))
