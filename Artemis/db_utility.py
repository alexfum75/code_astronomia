import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn


def parse_nav_field(artemis_nav_field, nav_object):
    if nav_object != 'O':
        artemis_nav_field = artemis_nav_field.replace(" ", "")
    artemis_nav_field = artemis_nav_field.replace(nav_object, "")
    artemis_nav_field = artemis_nav_field.replace("(", "")
    artemis_nav_field = artemis_nav_field.replace(")", "")
    artemis_nav_field = artemis_nav_field.replace(":", "")
    if nav_object == 'O':
        artemis_nav_field = artemis_nav_field.replace(",", "")
        artemis_nav_field = artemis_nav_field.lstrip(' ')
        artemis_nav_field = artemis_nav_field.split(' ')
    else:
        artemis_nav_field = artemis_nav_field.split(',')
    return artemis_nav_field


def db_get_nav_point(conn):
    nav_point_dict = {}

    cur = conn.cursor()
    cur.execute("SELECT timestamp, position, speed, attitude FROM state_vector order by timestamp;")
    rows = cur.fetchall()

    for row in rows:
        artemis_timestamp = row[0]
        artemis_timestamp = artemis_timestamp.replace(" ", "")
        artemis_timestamp = artemis_timestamp.replace("days", ":")
        artemis_timestamp = artemis_timestamp.replace("hrs", ":")
        artemis_timestamp = artemis_timestamp.replace("min", ":")
        date_tokens = artemis_timestamp.split(':')
        day = int(date_tokens[0])
        hour = int(date_tokens[1])
        minute = int(date_tokens[2])
        sec = 0

        artemis_nav_obj = artemis_nav.ArtemisObject()
        artemis_nav_obj.setTimeStamp(datetime.timedelta(days=day, hours=hour, minutes=minute, seconds=sec))

        pos_tokens = parse_nav_field(row[1], 'P')
        tuple_pos = (float(pos_tokens[0]), float(pos_tokens[1]), float(pos_tokens[2]))
        artemis_nav_obj.setPos(tuple_pos)

        speed_tokens = parse_nav_field(row[2], 'V')
        tuple_speed = (float(speed_tokens[0]), float(speed_tokens[1]), float(speed_tokens[2]))
        artemis_nav_obj.setSpeed(tuple_speed)

        attitude_tokens = parse_nav_field(row[3], 'O')
        tuple_attitude = (float(attitude_tokens[0]), float(attitude_tokens[1]), float(attitude_tokens[2]))
        artemis_nav_obj.setAttitude(tuple_attitude)

        nav_point_dict[artemis_nav_obj.getArtemisDate()] = artemis_nav_obj

    nav_point_sort = dict(sorted(nav_point_dict.items()))
    return nav_point_sort
