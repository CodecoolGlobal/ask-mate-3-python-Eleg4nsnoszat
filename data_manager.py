from psycopg2 import sql
import connection
import bcrypt


def hash_password(plain_text_password):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    if hashed_password is None:
        return False
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


@connection.connection_handler
def get_questions(cursor, order_by, order_direction):
    query = """SELECT * FROM question  
    ORDER BY {} {};"""
    cursor.execute(sql.SQL(query).format(sql.Identifier(order_by), sql.SQL(order_direction)))
    return cursor.fetchall()


@connection.connection_handler
def get_usernames(cursor):
    query = """SELECT username FROM users;"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def add_question(cursor, title, message, image, author_id, username):
    query = """INSERT INTO question
                VALUES (default, CURRENT_TIMESTAMP, 0, 0, %(title)s, %(message)s, NULLIF (%(image)s, ''),
                %(author_id)s, %(username)s);"""
    cursor.execute(query, {'title': title, 'message': message, 'image': image, 'author_id': author_id,
                           'username': username})


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
    WHERE question.id = %(question_id)s"""
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
def add_new_answer(cursor, question_id, message, image, author_id, username):
    query = """INSERT INTO answer VALUES (DEFAULT, CURRENT_TIMESTAMP, 0,%(question_id)s, %(message)s, 
    NULLIF (%(image)s, ''), %(author_id)s, %(username)s)"""
    cursor.execute(query, {'question_id': question_id, 'message': message, 'image': image,
                           'author_id': author_id, 'username': username})


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
def get_all_tags_by_question(cursor):
    query = """SELECT tag.name, COUNT(question_tag.question_id) as number_of_questions
    FROM question_tag
    JOIN tag
    ON question_tag.tag_id = tag.id
    GROUP BY tag.name"""
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def get_answer_by_answer_id(cursor, answer_id):
    query = """SELECT * FROM answer WHERE id = %(answer_id)s"""
    cursor.execute(query, {'answer_id': answer_id})
    return cursor.fetchone()


@connection.connection_handler
def add_new_comment_to_question(cursor, question_id, message, author_id, username):
    query = """INSERT INTO comment VALUES (default, %(question_id)s, NULL, %(message)s, CURRENT_TIMESTAMP, 0, 
    %(author_id)s, %(username)s)"""
    cursor.execute(query, {'question_id': question_id, 'message': message,
                           'author_id': author_id, 'username': username})


@connection.connection_handler
def get_comments_by_question_id(cursor, question_id):
    query = """SELECT id, message, submission_time, edited_count, username FROM comment 
    WHERE question_id = %(question_id)s"""
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchall()


@connection.connection_handler
def add_new_comment_to_answer(cursor, answer_id, message, author_id, username):
    query = """INSERT INTO comment VALUES (default, NULL, %(answer_id)s, %(message)s, CURRENT_TIMESTAMP, 0,
     %(author_id)s, %(username)s)"""
    cursor.execute(query, {'answer_id': answer_id, 'message': message,
                           'author_id': author_id, 'username': username})


@connection.connection_handler
def get_comments_by_answer(cursor, answer_id):
    query = """SELECT id, message, submission_time, username FROM comment WHERE answer_id = %(answer_id)s"""
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


@connection.connection_handler
def registration(cursor, username, password):
    query = """INSERT INTO users VALUES (default, %(username)s, %(password)s, CURRENT_TIMESTAMP, 0)"""
    cursor.execute(query, {'username': username, 'password': password})


@connection.connection_handler
def get_hashed_password(cursor, username):
    query = """SELECT password FROM users WHERE username = %(username)s"""
    cursor.execute(query, {'username': username})
    query_result = cursor.fetchone()
    return query_result["password"] if query_result is not None else query_result



@connection.connection_handler
def get_user_id_by_username(cursor, username):
    query = """SELECT user_id FROM users WHERE username = %(username)s"""
    cursor.execute(query, {'username': username})
    return cursor.fetchone()


@connection.connection_handler
def check_registration(cursor, username):
    query = """SELECT username FROM users WHERE username = %(username)s"""
    cursor.execute(query, {'username': username})
    return cursor.fetchone()


@connection.connection_handler
def get_all_user_data(cursor, user_id):
    query = """SELECT * FROM users WHERE user_id = %(user_id)s"""
    cursor.execute(query, {'user_id': user_id})
    return cursor.fetchone()


@connection.connection_handler
def get_num_of_asked_questions_by_user_id(cursor, user_id):
    query = """SELECT COUNT(author_id) AS user_questions FROM question WHERE author_id = %(user_id)s"""
    cursor.execute(query, {'user_id': user_id})
    return cursor.fetchone()


@connection.connection_handler
def get_asked_questions_by_user_id(cursor, user_id):
    query = """SELECT * FROM question WHERE author_id = %(user_id)s"""
    cursor.execute(query, {'user_id': user_id})
    return cursor.fetchall()


@connection.connection_handler
def get_num_of_user_answers(cursor, user_id):
    query = """SELECT COUNT(author_id) AS user_answers FROM answer WHERE author_id = %(user_id)s"""
    cursor.execute(query, {'user_id': user_id})
    return cursor.fetchone()


@connection.connection_handler
def get_user_answers_by_user_id(cursor, user_id):
    query = """SELECT * FROM answer WHERE author_id = %(user_id)s"""
    cursor.execute(query, {'user_id': user_id})
    return cursor.fetchall()


@connection.connection_handler
def get_num_of_user_comments(cursor, user_id):
    query = """SELECT COUNT(author_id) AS user_comments FROM comment WHERE author_id = %(user_id)s"""
    cursor.execute(query, {'user_id': user_id})
    return cursor.fetchone()


@connection.connection_handler
def get_user_comments_by_user_id(cursor, user_id):
    query = """SELECT * FROM comment WHERE author_id = %(user_id)s"""
    cursor.execute(query, {'user_id': user_id})
    return cursor.fetchall()


def get_username_by_user_id(cursor, user_id):
    query = """SELECT username FROM users WHERE user_id = %(user_id)s"""
    cursor.execute(query, {'user_id': user_id})
    return cursor.fetchone()


@connection.connection_handler
def users_info(cursor):
    query = """select users.user_id, users.username,
                        users.registration_date, users.reputation, 
                        count(distinct answer.id)   as number_of_answers,
                        count(distinct question.id) as number_of_questions,
                        count(distinct comment.id)  as number_of_comments
                    from users
                        left join answer on users.user_id = answer.author_id
                        left join question on users.user_id = question.author_id
                        left join comment on users.user_id = comment.author_id
                    group by users.user_id"""

    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def lose_reputation(cursor, author_id, points):
    query = """UPDATE users
    SET reputation = reputation - %(points)s
    WHERE user_id = %(author_id)s"""
    cursor.execute(query, {'author_id': author_id, 'points': points})


@connection.connection_handler
def gain_reputation(cursor, author_id, points):
    query = """UPDATE users
    SET reputation = reputation + %(points)s
    WHERE user_id = %(author_id)s"""
    cursor.execute(query, {'author_id': author_id, 'points': points})
