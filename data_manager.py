import connection


@connection.connection_handler
def get_questions(cursor, order_by, order_direction):
    query = f"""SELECT * FROM question 
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


@connection.connection_handler
def get_answer_id(cursor):
    query = f"""SELECT id FROM answer ORDER BY id DESC LIMIT 1"""
    cursor.execute(query)
    return cursor.fetchone()


@connection.connection_handler
def get_question_details_by_id(cursor, question_id):
    query = f"""SELECT * FROM question WHERE id = '{question_id}'"""
    cursor.execute(query)
    return cursor.fetchone()


@connection.connection_handler
def get_answers_details_by_question_id(cursor, question_id):
    query = f"""SELECT * FROM answer WHERE question_id = '{question_id}'"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def update_view_number(cursor, question_id):
    query = f"""UPDATE question
                SET view_number = view_number + 1
                WHERE id = '{question_id}'"""
    cursor.execute(query)


@connection.connection_handler
def update_question(cursor, question_id, title, message, image):
    query = f"""UPDATE question
                SET title = '{title}', message = '{message}', image = '{image}'
                WHERE id = '{question_id}'"""
    cursor.execute(query)


@connection.connection_handler
def add_new_answer(cursor, question_id, message, image):
    query = f"""INSERT INTO answer VALUES (DEFAULT,CURRENT_TIMESTAMP, 0,'{question_id}', '{message}', '{image}' )"""
    cursor.execute(query)


@connection.connection_handler
def delete_question(cursor, question_id):
    query = f"""DELETE FROM question WHERE id = '{question_id}'"""
    cursor.execute(query)


@connection.connection_handler
def delete_answer(cursor, answer_id):
    query = f"""DELETE FROM answer WHERE id = '{answer_id}'"""
    cursor.execute(query)


@connection.connection_handler
def get_question_by_answer_id(cursor, answer_id):
    query = f"""SELECT question_id FROM answer WHERE id = '{answer_id}'"""
    cursor.execute(query)
    return cursor.fetchone()
