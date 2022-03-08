import connection
from datetime import datetime
import time

@connection.connection_handler
def get_questions(cursor, order_by, order_direction):
    query = f"""SELECT submission_time, view_number, vote_number, title, message, image FROM question 
    ORDER BY {order_by} {order_direction};"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def add_question(cursor, title, message, image):
    query = f"""INSERT INTO question
                VALUES (default, CURRENT_TIMESTAMP, 0, 0, '{title}', '{message}', '{image}');"""
    cursor.execute(query)



@connection.connection_handler
def get_question_id(cursor):
    query = f"""SELECT id FROM question ORDER BY id DESC LIMIT 1"""
    cursor.execute(query)
    return cursor.fetchone()
