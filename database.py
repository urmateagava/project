import psycopg2
import creds
from datetime import date, timedelta, datetime
conn = psycopg2.connect(host=creds.host, dbname=creds.database,
                        user=creds.user, password=creds.password)
cur = conn.cursor()

def check_period(user_id):
    cur.execute(f"SELECT day_end_sub FROM subs WHERE user_id ='{user_id}';")
    try:
        now=cur.fetchone()[0]
    except TypeError:
        return None
    return datetime.strptime(now,"%Y-%m-%d").date()

def insert_or_update_user(user_id, username, firstname, lastname, dayss, dayes):
    if check_period(user_id) is None:
        cur.execute(f"INSERT INTO subs (user_id, username, firstname, lastname, day_start_sub, day_end_sub)"
                    f"VALUES ('{user_id}', '{username}', '{firstname}', '{lastname}', '{dayss}','{dayes}');")
        conn.commit()
    else:
        cur.execute(f"UPDATE subs SET day_end_sub = '{dayes}' WHERE user_id = '{user_id}';")
        conn.commit()


def open_order(user_id, payment, username, firstname, lastname):
    dayss = date.today()

    if payment == 39000:
        try:
            if check_period(user_id) >= dayss:
                dayes = check_period(user_id) + timedelta(days=30)
                insert_or_update_user(user_id, username, firstname, lastname, dayss, dayes)
            else:
                dayes = date.today() + timedelta(days=30)
                insert_or_update_user(user_id, username, firstname, lastname, dayss, dayes)
        except TypeError:
            dayes = date.today() + timedelta(days=30)
            insert_or_update_user(user_id, username, firstname, lastname, dayss, dayes)

    elif payment == 100000:
        try:
            if check_period(user_id) >= dayss:
                dayes = check_period(user_id) + timedelta(days=90)
                insert_or_update_user(user_id, username, firstname, lastname, dayss, dayes)
            else:
                dayes = date.today() + timedelta(days=90)
                insert_or_update_user(user_id, username, firstname, lastname, dayss, dayes)

        except TypeError:
            dayes = date.today() + timedelta(days=90)
            insert_or_update_user(user_id, username, firstname, lastname, dayss, dayes)

    elif payment == 170000:
        try:
            if check_period(user_id) >= dayss:
                dayes = check_period(user_id) + timedelta(days=150)
                insert_or_update_user(user_id, username, firstname, lastname, dayss, dayes)
            else:
                dayes = date.today() + timedelta(days=150)
                insert_or_update_user(user_id, username, firstname, lastname, dayss, dayes)

        except TypeError:
            dayes = date.today() + timedelta(days=150)
            insert_or_update_user(user_id, username, firstname, lastname, dayss, dayes)

    elif payment == 270000:
        try:
            if check_period(user_id) >= dayss:
                dayes = check_period(user_id) + timedelta(days=210)
                insert_or_update_user(user_id, username, firstname, lastname, dayss, dayes)
            else:
                dayes = date.today() + timedelta(days=210)
                insert_or_update_user(user_id, username, firstname, lastname, dayss, dayes)

        except TypeError:
            dayes = date.today() + timedelta(days=210)
            insert_or_update_user(user_id, username, firstname, lastname, dayss, dayes)

    elif payment == 400000:
        try:
            if check_period(user_id) >= dayss:
                dayes = check_period(user_id) + timedelta(days=360)
                insert_or_update_user(user_id, username, firstname, lastname, dayss, dayes)
            else:
                dayes = date.today() + timedelta(days=360)
                insert_or_update_user(user_id, username, firstname, lastname, dayss, dayes)

        except TypeError:
            dayes = date.today() + timedelta(days=360)
            insert_or_update_user(user_id, username, firstname, lastname, dayss, dayes)

def daily_check():
    cur.execute(f"SELECT user_id, day_end_sub FROM subs;")
    users=cur.fetchall()
    return users

def delete_from_table(user_id):
    cur.execute(f"DELETE FROM subs WHERE user_id = '{user_id}';")
    conn.commit()

