from flask import Flask, render_template, abort, redirect, url_for, session, request
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


def guard_check(id_user, level_guard=0):
    user_role = dbc.show_role(id_user)
    print('User Role: ' + str(user_role) + " Level guard: " + str(level_guard))
    access_dict = {'1': "123", '2': "13", '3': "1"}

    for i in list(access_dict.get(str(level_guard))):
        if int(i) == user_role:
            return True
    return False


def account_enter(_login, _pass):
    result = dbc.show_table("users")
    for row in result:
        if row['login'] == _login and row['pass'] == _pass:
            session['id_user'] = row['id_user']
            session['username'] = row['login']
            return True
    return False


@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return abort(401)


@app.route('/admin/')
def ad_panel():
    if 'username' in session:
        return render_template('adminPanel.html', username=session['username'])
    return abort(401)


@app.route('/journal/')
def journal():
    if 'username' in session:
        return render_template('journal.html', username=session['username'])
    return abort(401)


@app.route('/login/', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        if account_enter('admin', 'admin'):
            print(account_enter('admin', 'admin'))
            #session['username'] = request.json['nick']
            return url_for('index')
        abort(401)
    return render_template('login.html')


@app.route('/personal/')
def personal_area():
    if 'username' in session:
        return render_template('personalArea.html', username=session['username'])
    return abort(401)


@app.route('/exit/')
def exit_account():
    session.pop('username', None)
    session.pop('id_user', None)
    return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error404.html'), 404
    # return "Error 404. Такой страницы нет", 404


@app.errorhandler(401)
def page_login(error):
    return redirect(url_for('login'))


app.secret_key = str(os.urandom(24))
