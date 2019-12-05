from sqlalchemy import create_engine, exc
import datetime
engine = create_engine('postgresql+psycopg2://postgres:root@localhost/pansionat')


# result = engine.execute("SELECT * FROM corps;")

def show_table(name_table):
    result = engine.execute("SELECT * FROM %s ORDER BY 1;" % name_table)
    d, a = {}, []
    for rowproxy in result:
        for column, value in rowproxy.items():
            d = {**d, **{column: value}}
        a.append(d)
    return a


def show_role(id_user):
    result = engine.execute("SELECT roles.level_role FROM users INNER JOIN roles "
                            "ON roles.id_role = users.id_role WHERE id_user = %s;" % id_user)

    return result.fetchone()['level_role']


def add_room(id_type, id_corp, num_room):
    id_status = 1
    result = engine.execute("INSERT INTO rooms(id_status, id_type, id_corp, num_room) VALUES (%s, %s, %s, %s);" %
                            (id_status, id_type, id_corp, num_room))
    return "Success"


def find_room(id_type, date_start, date_end):
    result = engine.execute("SELECT id_room FROM rooms WHERE id_type = '%s'" % id_type)
    for row in result:
        requests = engine.execute("SELECT date_start, date_end FROM journal WHERE id_room = '%s'" % (row['id_room']))
        print(requests.fetchone())


def add_corp(name_corp):
    result = engine.execute("INSERT INTO corps(name_corp) VALUES('%s');" % name_corp)
    return "Success"


def add_type_rooms(name_type, place_amount, price):
    result = engine.execute("INSERT INTO type_rooms(name_type, place_amount, price) VALUES('%s', '%s', '%s');" %
                            (name_type, place_amount, price))
    return "Success"


def add_status(name_status):
    result = engine.execute("INSERT INTO statuses(name_status) VALUES('%s');" % name_status)
    return "Success"


def add_user(login, password, role):
    result = engine.execute("INSERT INTO users(login, pass, id_role) VALUES('%s', '%s', '%s');" %
                            (login, password, role))
    return "Success"


def add_role(name, level):
    result = engine.execute("INSERT INTO roles(name_role, level_role) VALUES('%s', '%s');" %
                            (name, level))
    return "Success"


def add_ticket(id_user):
    result = engine.execute("INSERT INTO tickets(id_user) VALUES('%s');" % id_user)
    return "Success"


def add_request(id_room, date_start, date_end, id_status, id_ticket):
    result = engine.execute("INSERT INTO journal(id_room, date_start, date_end, id_status, id_ticket)"
                            " VALUES ('%s', '%s', '%s', '%s', '%s');" %
                            (id_room, date_start, date_end, id_status, id_ticket))
    return "Success"


def delete_room(id_room, cascade):
    try:
        result = engine.execute("DELETE FROM rooms WHERE id_room = '%s';" % id_room)
        return "true"
    except exc.IntegrityError as e:
        if cascade:
            result = engine.execute("SELECT id_request FROM journal WHERE id_room = '%s';" % id_room)
            for row in result:
                delete_room(row['id_request'], cascade)
            return delete_room(id_room, cascade)
        else:
            return "false"


def delete_type_rooms(id_type, cascade):
    try:
        result = engine.execute("DELETE FROM type_rooms WHERE id_type = '%s';" % id_type)
        return "true"
    except exc.IntegrityError as e:
        if cascade:
            result = engine.execute("SELECT id_room FROM rooms WHERE id_type = '%s';" % id_type)
            for row in result:
                delete_room(row['id_room'], cascade)
            return delete_type_rooms(id_type, cascade)
        else:
            return "false"


def delete_corp(id_corp, cascade):
    try:
        result = engine.execute("DELETE FROM corps WHERE id_corp = '%s';" % id_corp)
        return "true"
    except exc.IntegrityError as e:
        if cascade:
            result = engine.execute("SELECT id_room FROM rooms WHERE id_corp = '%s';" % id_corp)
            for row in result:
                delete_room(row['id_room'], cascade)
            return delete_corp(id_corp, cascade)
        else:
            return "false"


def delete_status(id_status, cascade):
    try:
        result = engine.execute("DELETE FROM statuses WHERE id_status = '%s';" % id_status)
        return "true"
    except exc.IntegrityError as e:
        if cascade:
            result = engine.execute("SELECT id_user FROM users WHERE id_status = '%s';" % id_status)
            for row in result:
                delete_user(row['id_user'], cascade)
            result = engine.execute("SELECT id_request FROM journal WHERE id_status = '%s';" % id_status)
            for row in result:
                delete_request(row['id_request'], cascade)
            return delete_status(id_status, cascade)
        else:
            return "false"


def delete_user(id_user, cascade):
    try:
        result = engine.execute("DELETE FROM users WHERE id_user = '%s';" % id_user)
        return "true"
    except exc.IntegrityError as e:
        if cascade:
            result = engine.execute("SELECT id_ticket FROM tickets WHERE id_user = '%s';" % id_user)
            for row in result:
                delete_ticket(row['id_ticket'], cascade)
            return delete_user(id_user, cascade)
        else:
            return "false"


def delete_role(id_role, cascade):
    try:
        result = engine.execute("DELETE FROM roles WHERE id_role = '%s';" % id_role)
        return "true"
    except exc.IntegrityError as e:
        if cascade:
            result = engine.execute("SELECT id_user FROM users WHERE id_role = '%s';" % id_role)
            for row in result:
                delete_user(row['id_user'], cascade)
            return delete_role(id_role, cascade)
        else:
            return "false"


def delete_ticket(id_ticket, cascade):
    try:
        result = engine.execute("DELETE FROM tickets WHERE id_ticket = '%s';" % id_ticket)
        return "true"
    except exc.IntegrityError as e:
        if cascade:
            result = engine.execute("SELECT id_request FROM journal WHERE id_ticket = '%s';" % id_ticket)
            for row in result:
                delete_request(row['id_request'], cascade)
            return delete_ticket(id_ticket, cascade)
        else:
            return "false"


def delete_request(id_request, cascade):
    try:
        result = engine.execute("DELETE FROM journal WHERE id_request = '%s';" % id_request)
        return "true"
    except exc.IntegrityError as e:
        return "Ошибка удаления(Заявка используется)"


def update_room(id_room, id_type, id_corp, num_room):
    result = engine.execute("UPDATE rooms SET id_type = '%s', id_corp = '%s',"
                            " num_room = '%s'  WHERE id_room = '%s';" % (id_type, id_corp, num_room, id_room))
    return "Success"


def update_type_rooms(id_type, name_type, amount, price):
    result = engine.execute("UPDATE type_rooms SET name_type = '%s', place_amount = '%s', price = '%s'"
                            " WHERE id_type = '%s';" % (name_type, amount, price, id_type))
    return "Success"


def update_corp(id_corp, name_corp):
    result = engine.execute("UPDATE corps SET name_corp = '%s' WHERE id_corp = '%s';" % (name_corp, id_corp))
    return "Success"


def update_status(id_status, name_status):
    result = engine.execute("UPDATE statuses SET name_status = '%s' WHERE id_status = '%s';" % (name_status, id_status))
    return "Success"


def update_user(id_user, login, password, id_role):
    result = engine.execute("UPDATE users SET login = '%s', pass = '%s', id_role = '%s'"
                            " WHERE id_user = '%s';" % (login, password, id_role, id_user))
    return "Success"


def update_role(id_role, name_role, level_role):
    result = engine.execute("UPDATE roles SET name_role = '%s', level_role = '%s'"
                            " WHERE id_role = '%s';" % (name_role, level_role, id_role))
    return "Success"


def update_ticket(id_ticket, id_user):
    result = engine.execute("UPDATE tickets SET id_user = '%s' WHERE id_ticket = '%s';" % (id_user, id_ticket))
    return "Success"


def update_request(id_request, id_room, date_start, date_end, id_ticket, id_status):
    result = engine.execute("UPDATE journal SET id_room = '%s', date_start = '%s', date_end = '%s', "
                            "id_ticket = '%s', id_status = '%s' WHERE id_status = '%s';" %
                            (id_room, date_start, date_end, id_ticket, id_status, id_request))
    return "Success"


