from sqlalchemy import create_engine

engine = create_engine('postgresql+psycopg2://postgres:root@localhost/pansionat')


# result = engine.execute("SELECT * FROM corps;")

def show_table(name_table):
    result = engine.execute("SELECT * FROM %s;" % name_table)
    for row in result:
        print(row)
    return result


def add_room(id_status, id_type, id_corp):
    result = engine.execute("INSERT INTO rooms(id_status, id_type, id_corp)"
                            " VALUES ('%s', '%s', '%s');" % (id_status, id_type, id_corp))
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
    pass


def delete_request(id_request):
    pass


def delete_type_rooms(id_corp):
    pass


def delete_status(id_status):
    pass
