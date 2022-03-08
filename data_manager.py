import connection


@connection.connection_handler
def get_questions(cursor, order_by, order_direction):
    query = f"""SELECT submission_time, view_number, vote_number, title, message, image FROM question 
    ORDER BY {order_by} {order_direction};"""
    cursor.execute(query)
    return cursor.fetchall()
