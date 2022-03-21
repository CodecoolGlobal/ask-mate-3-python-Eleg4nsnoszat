from psycopg2 import sql

import connection


@connection.connection_handler
def get_questions(cursor, order_by, order_direction):
    query = """SELECT * FROM question  
    ORDER BY {} {};"""
    cursor.execute(sql.SQL(query).format(sql.Identifier(order_by), sql.SQL(order_direction)))
    return cursor.fetchall()


@connection.connection_handler
def add_question(cursor, title, message, image):
    query = """INSERT INTO question
                VALUES (default, CURRENT_TIMESTAMP, 0, 0, %(title)s, %(message)s, NULLIF (%(image)s, ''));"""
    cursor.execute(query, {'title': title, 'message': message, 'image': image})


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
    query = """SELECT * FROM question WHERE id = %(question_id)s"""
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchone()


@connection.connection_handler
def get_answers_details_by_question_id(cursor, question_id):
    query = """SELECT * FROM answer WHERE question_id = %(question_id)s ORDER BY submission_time"""
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchall()


@connection.connection_handler
def update_view_number(cursor, question_id):
    query = """UPDATE question
                SET view_number = view_number + 1
                WHERE id = %(question_id)s"""
    cursor.execute(query, {'question_id': question_id})


@connection.connection_handler
def upvote_question(cursor, question_id):
    query = """UPDATE question
                SET vote_number = vote_number + 1
                WHERE id = %(question_id)s"""
    cursor.execute(query, {'question_id': question_id})


@connection.connection_handler
def upvote_answer(cursor, answer_id):
    query = """UPDATE answer
                SET vote_number = vote_number + 1
                WHERE id = %(answer_id)s"""
    cursor.execute(query, {'answer_id': answer_id})


@connection.connection_handler
def downvote_question(cursor, question_id):
    query = """UPDATE question
                SET vote_number = vote_number - 1
                WHERE id = %(question_id)s"""
    cursor.execute(query, {'question_id': question_id})


@connection.connection_handler
def downvote_answer(cursor, answer_id):
    query = """UPDATE answer
                SET vote_number = vote_number - 1
                WHERE id = %(answer_id)s"""
    cursor.execute(query, {'answer_id': answer_id})


@connection.connection_handler
def update_question(cursor, question_id, title, message, image):
    query = """UPDATE question
                SET title = %(title)s, message = %(message)s, image = %(image)s
                WHERE id = %(question_id)s"""
    cursor.execute(query, {'title': title, 'message': message, 'image': image, 'question_id': question_id})


@connection.connection_handler
def delete_question_image(cursor, question_id):
    query = """UPDATE question
                SET image = NULL
                WHERE id = %(question_id)"""
    cursor.execute(query, {'question_id': question_id})


@connection.connection_handler
def add_new_answer(cursor, question_id, message, image):
    query = """INSERT INTO answer VALUES (DEFAULT, CURRENT_TIMESTAMP, 0,%(question_id)s, %(message)s, 
    NULLIF (%(image)s, ''))"""
    cursor.execute(query, {'question_id': question_id, 'message': message, 'image': image})


@connection.connection_handler
def delete_question(cursor, question_id):
    query = """DELETE FROM question WHERE id = %(question_id)s"""
    cursor.execute(query, {'question_id': question_id})


@connection.connection_handler
def delete_answer(cursor, answer_id):
    query = """DELETE FROM answer WHERE id = %(answer_id)s"""
    cursor.execute(query, {'answer_id': answer_id})


@connection.connection_handler
def get_question_by_answer_id(cursor, answer_id):
    query = """SELECT question_id FROM answer WHERE id = %(answer_id)s"""
    cursor.execute(query, {'answer_id': answer_id})
    return cursor.fetchone()


@connection.connection_handler
def get_answer_by_answer_id(cursor, answer_id):
    query = """SELECT * FROM answer WHERE id = %(answer_id)s"""
    cursor.execute(query, {'answer_id': answer_id})
    return cursor.fetchone()


@connection.connection_handler
def add_new_comment_to_question(cursor, question_id, message):
    query = """INSERT INTO comment VALUES (default, %(question_id)s, NULL, %(message)s, CURRENT_TIMESTAMP, 0)"""
    cursor.execute(query, {'question_id': question_id, 'message': message})


@connection.connection_handler
def get_comments_by_question_id(cursor, question_id):
    query = """SELECT id, message, submission_time, edited_count FROM comment WHERE question_id = %(question_id)s"""
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchall()


@connection.connection_handler
def add_new_comment_to_answer(cursor, answer_id, message):
    query = """INSERT INTO comment VALUES (default, NULL, %(answer_id)s, %(message)s, CURRENT_TIMESTAMP, 0)"""
    cursor.execute(query, {'answer_id': answer_id, 'message': message})


@connection.connection_handler
def get_comments_by_answer(cursor, answer_id):
    query = """SELECT id, message, submission_time FROM comment WHERE answer_id = %(answer_id)s"""
    cursor.execute(query, {'answer_id': answer_id})
    return cursor.fetchall()


@connection.connection_handler
def get_comment_by_id(cursor, comment_id):
    query = """SELECT * FROM comment WHERE id = %(comment_id)s"""
    cursor.execute(query, {'comment_id': comment_id})
    return cursor.fetchone()


@connection.connection_handler
def update_comment(cursor, comment_id, message):
    query = """UPDATE comment
                SET message = %(message)s, submission_time = CURRENT_TIMESTAMP, edited_count = edited_count + 1 
                WHERE id = %(comment_id)s"""
    cursor.execute(query, {'message': message, 'comment_id': comment_id})


@connection.connection_handler
def delete_comment(cursor, comment_id):
    query = """DELETE FROM comment WHERE id = %(comment_id)s"""
    cursor.execute(query, {'comment_id': comment_id})


@connection.connection_handler
def get_latest_questions(cursor, order_by, order_direction):
    query = """SELECT * FROM question 
    ORDER BY {} {} LIMIT 5;"""
    cursor.execute(sql.SQL(query).format(sql.Identifier(order_by), sql.SQL(order_direction)))
    return cursor.fetchall()


@connection.connection_handler
def add_tag_for_tag(cursor, name):
    query = f"""INSERT INTO tag VALUES (default, %(name)s)"""
    cursor.execute(query, {'name': name})


@connection.connection_handler
def add_tag_for_question_tag(cursor, question_id):
    query = f"""INSERT INTO question_tag VALUES (%(question_id)s, (SELECT id FROM tag ORDER BY id DESC LIMIT 1))"""
    cursor.execute(query, {'question_id': question_id})


@connection.connection_handler
def get_all_tags(cursor):
    query = f"""SELECT * FROM tag"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_tags_by_question_id(cursor, question_id):
    query = """SELECT *
                FROM question_tag
                INNER JOIN tag ON id = tag_id WHERE question_id = %(id)s"""
    cursor.execute(query, {'id': question_id})
    return cursor.fetchall()


@connection.connection_handler
def delete_tag(cursor, tag_id):
    query = """DELETE FROM question_tag WHERE tag_id = %(tag_id)s"""
    cursor.execute(query, {'tag_id': tag_id})


@connection.connection_handler
def update_answer(cursor, message, answer_id):
    query = """UPDATE answer
                SET message = %(message)s
                WHERE id = %(answer_id)s"""
    cursor.execute(query, {'answer_id': answer_id, 'message': message})


@connection.connection_handler
def search_questions(cursor, search_input, order_by, order_direction):
    query = """SELECT * FROM question
                WHERE title ILIKE %(search_input)s ORDER BY {} {}"""
    cursor.execute(sql.SQL(query).format(sql.Identifier(order_by), sql.SQL(order_direction)))
    return cursor.fetchall()
