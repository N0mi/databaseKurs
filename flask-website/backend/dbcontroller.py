from sqlalchemy import create_engine, exc

engine = create_engine('postgresql+psycopg2://postgres:root@localhost/pansionat')


# result = engine.execute("SELECT * FROM corps;")

def show_table(name_table):
    result = engine.execute("SELECT * FROM %s;" % name_table)
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
    result = engine.execute("INSERT INTO rooms(id_status, id_type, id_corp, num_room) VALUES (%s, %s, %s, %s);", (id_status, id_type, id_corp, num_room))
    return "Success"


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
    result = engine.execute("INSERT INTO users(login, pass, id_role) VALUES('%s', '%s', '%s');" %(login, password, role))
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


def delete_room(id_room):
    try:
        result = engine.execute("DELETE FROM rooms WHERE id_room = '%s';" % id_room)
        print("Успешно")
    except exc.IntegrityError as e:
        print("Комната связана с журналом")


def delete_type_rooms(id_corp):
    pass


def delete_corp(id_corp):
    pass


def delete_status(id_status):
    pass


def delete_user(id_user):
    pass


def delete_role(id_role):
    pass


def delete_ticket(id_ticket):
    pass


def delete_request(id_request):
    pass


def update_room(id_room, id_type, id_corp, num_room):
    result = engine.execute("UPDATE rooms SET id_type = '%s', id_corp = '%s',"
                            " num_room = '%s'  WHERE id_room = '%s';" % (id_type, id_corp, num_room, id_room))
    return "Success"
