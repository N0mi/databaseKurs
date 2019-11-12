from sqlalchemy import create_engine
import psycopg2

engine = create_engine('postgresql+psycopg2://postgres:root@localhost/pansionat')
result = engine.execute("SELECT * FROM corps;")


def add_room(id_status, id_type, id_corp):
    pass


def add_corp(name_corp):
    pass


def add_type_rooms(name_type, place_amount, price):
    pass


def add_status(name_status):
    pass


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
