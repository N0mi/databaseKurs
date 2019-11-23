from sqlalchemy import create_engine, exc

engine = create_engine('postgresql+psycopg2://postgres:root@localhost/pansionat')


# result = engine.execute("SELECT * FROM corps;")

def show_table(name_table):
    result = engine.execute("SELECT * FROM %s;" % name_table)
    return result


def show_role(id_user):
    result = engine.execute("SELECT id_user, id_role FROM users WHERE id_user = %s;" % id_user)
    user_role = result.fetchone()['id_role']

    return user_role


def add_room(id_status, id_type, id_corp, num_room):
    result = engine.execute("INSERT INTO rooms(id_status, id_type, id_corp, num_room)"
                            " VALUES ('%s', '%s', '%s', '%s');" % (id_status, id_type, id_corp, num_room))
    return "Success"


def add_corp(name_corp):
    result = engine.execute("INSERT INTO corps(name_corp) VALUES ('%s');" % name_corp)
    return "Success"


def add_type_rooms(name_type, place_amount, price):
    result = engine.execute("INSERT INTO type_rooms(name_type, place_amount, price)"
                            " VALUES ('%s', '%s', '%s');" % (name_type, place_amount, price))
    return "Success"


def add_status(name_status):
    result = engine.execute("INSERT INTO statuses(name_status)"
                            " VALUES ('%s');" % name_status)
    return "Success"


def add_request(id_room, date_start, date_end, id_status):
    pass


def new_ticket(id_user, id_request):
    pass


def change_role(id_user, id_role):
    pass


def delete_corp(id_corp):
    pass


def delete_room(id_room):
    try:
        result = engine.execute('CALL delete_corp(1);')
        print("Успешно")
    except exc.IntegrityError as e:
        print("Невозможно удалить статус. Удалить комнаты сэтим статусом?")


def delete_request(id_request):
    pass


def delete_type_rooms(id_corp):
    pass


def delete_status(id_status):
    pass


def test_method():
    pass
