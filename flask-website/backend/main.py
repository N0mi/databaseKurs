from flask import Flask, render_template, abort, redirect, url_for, session, request, jsonify
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
app.config['JSON_AS_ASCII'] = False


def guard_check(id_user, level_guard_temp=0):
    level_user = dbc.show_role(id_user)
    if level_guard_temp < level_user:
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


def create_request(id_user, data_start, data_end, id_type):
    pass


def data_change():
    pass


@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html')
    return abort(401)


@app.route('/admin/')
def ad_panel():
    if 'username' in session:
        return render_template('adminPanel.html')
    return abort(401)


@app.route('/journal/')
def journal():
    if 'username' in session:
        return render_template('journal.html')
    return abort(401)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if account_enter(request.json['login'], request.json['pass']):
            return jsonify(message=url_for('index'))
        return jsonify(message='False')
    return render_template('login.html', level=0)


@app.route('/personal/')
def personal_area():
    if 'username' in session:
        return render_template('personalArea.html')
    return abort(401)


@app.route('/exit/')
def exit_account():
    session.pop('username', None)
    session.pop('id_user', None)
    return redirect(url_for('login'))


@app.route('/take_level/')
def take_level():
    if 'username' in session:
        return jsonify(message=int(dbc.show_role(session['id_user'])))

    return jsonify(message=0)


@app.route('/take_model/<namemodel>')
def take_model(namemodel):
    return jsonify(dbc.show_table(namemodel))


@app.route('/add/<name_object>', methods=['POST'])
def add_to_model(name_object):
    if name_object == "room":
        dbc.add_room(request.json['type'], request.json['corp'], request.json['num'])
    if name_object == "type":
        dbc.add_type_rooms(request.json['name'], request.json['amount'], request.json['price'])
    if name_object == "corp":
        dbc.add_corp(request.json['name'])
    if name_object == "status":
        dbc.add_status(request.json["name"])
    if name_object == "user":
        dbc.add_user(request.json["login"], request.json["pass"], request.json["role"])
    if name_object == "role":
        dbc.add_role(request.json["name"], request.json["level"])
    if name_object == "ticket":
        dbc.add_ticket(request.json["id_user"])
    if name_object == "request":
        dbc.add_request(request.json["room"], request.json["start"], request.json["end"], request.json["status"],
                        request.json["ticket"])
    return jsonify(message="true")


@app.route('/delete/<name_object>', methods=['POST'])
def delete_element(name_object):
    if name_object == "room":
        return jsonify(message=(dbc.delete_room(request.json['id'], request.json['cascade'])))
    if name_object == "type":
        return jsonify(message=(dbc.delete_type_rooms(request.json['id'], request.json['cascade'])))
    if name_object == "corp":
        return jsonify(message=(dbc.delete_corp(request.json['id'], request.json['cascade'])))
    if name_object == "status":
        return jsonify(message=(dbc.delete_status(request.json['id'], request.json['cascade'])))
    if name_object == "user":
        return jsonify(message=(dbc.delete_user(request.json['id'], request.json['cascade'])))
    if name_object == "role":
        return jsonify(message=(dbc.delete_role(request.json['id'], request.json['cascade'])))
    if name_object == "ticket":
        return jsonify(message=(dbc.delete_ticket(request.json['id'], request.json['cascade'])))
    if name_object == "request":
        return jsonify(message=(dbc.delete_request(request.json['id'], request.json['cascade'])))

    return jsonify(message="true")


@app.route('/update/<name_object>', methods=['POST'])
def update_element(name_object):
    if name_object == "room":
        # print(str(request.json['num']),str(request.json['corp']),str(request.json['type']), str(request.json['id']))
        dbc.update_room(request.json['id'], request.json['type'], request.json['corp'], request.json['num'])
    if name_object == "type":
        dbc.update_type_rooms(request.json['id'], request.json['name'], request.json['amount'], request.json['price'])
    if name_object == "corp":
        dbc.update_corp(request.json['id'], request.json['name'])
    if name_object == "status":
        dbc.update_status(request.json['id'], request.json['name'])
    if name_object == "user":
        dbc.update_user(request.json['id'], request.json['login'], request.json['pass'], request.json['role'])
    if name_object == "role":
        dbc.update_role(request.json['id'], request.json['name'], request.json['level'])
    if name_object == "ticket":
        dbc.update_ticket(request.json['id'], request.json['user'])
    if name_object == "request":
        dbc.update_request(request.json['id'], request.json['room'], request.json['start'],
                           request.json['end'], request.json['ticket'], request.json['status'])
    return jsonify(message="true")


@app.route('/buy_ticket/', methods=['POST'])
def buy_ticket():
    id_status = 2
    id_room = dbc.find_room(request.json['id_type'], request.json['date_start'], request.json['date_end'])
    if False:
        dbc.add_ticket(session['id_user'])
        id_ticket = dbc.show_table('tickets')[-1]['id_ticket']
        # dbc.add_request(id_room, date_start, date_end, id_status, id_ticket)!!!!!!!!!!!
        return jsonify(message="true")
    else:
        return jsonify(message="false")


@app.route('/registration/', methods=['POST'])
def registration():
    dbc.add_user(request.json['login'], request.json['pass'], request.json['role'])
    return jsonify(message="true")


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error404.html'), 404
    # return "Error 404. Такой страницы нет", 404


@app.errorhandler(401)
def page_login(error):
    return redirect(url_for('login'))


app.secret_key = str(os.urandom(24))
