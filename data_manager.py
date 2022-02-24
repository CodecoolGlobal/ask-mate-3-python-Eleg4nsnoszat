import time
import datetime
#from datetime import datetime
import connection
import os

DATA_FILE_PATH_QUESTION = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/question.csv'
DATA_FILE_PATH_ANSWER = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/answer.csv'
DATA_HEADER_QUESTION = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
DATA_HEADER_ANSWER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def get_new_question_id():
    return connection.get_new_id(DATA_FILE_PATH_QUESTION)


def get_new_answer_id():
    return connection.get_new_id(DATA_FILE_PATH_ANSWER)


def get_submission_time():
    presentDate = datetime.datetime.now()
    unix_timestamp = time.mktime(presentDate.timetuple())
    return round(unix_timestamp)


def get_display_submission_time(unix_timestamp):
    return datetime.date.fromtimestamp(unix_timestamp)


def get_all_questions():
    return connection.get_all(DATA_FILE_PATH_QUESTION)


def get_answers(question_id):
    all_answers = connection.get_all(DATA_FILE_PATH_ANSWER)
    answers = [answer for answer in all_answers if answer["question_id"] == question_id]
    return answers


def get_all_answers():
    all_answers = connection.get_all(DATA_FILE_PATH_ANSWER)
    return all_answers


def add_new_question(new_question):
    connection.add_new(DATA_FILE_PATH_QUESTION, new_question, DATA_HEADER_QUESTION)


def add_new_answer(new_answer):
    connection.add_new(DATA_FILE_PATH_ANSWER, new_answer, DATA_HEADER_ANSWER)


def delete_question(question_id):
    connection.delete(DATA_FILE_PATH_QUESTION, question_id, DATA_HEADER_QUESTION, 'id')


def delete_answer(answer_id, key_to_delete):
    connection.delete(DATA_FILE_PATH_ANSWER, answer_id, DATA_HEADER_ANSWER, key_to_delete)


def edit_question(question_id, edit_key, edit_value):
    connection.edit(DATA_FILE_PATH_QUESTION, DATA_HEADER_QUESTION, question_id, edit_key, edit_value)


def edit_answer(answer_id, edit_key, edit_value):
    connection.edit(DATA_FILE_PATH_ANSWER, DATA_HEADER_ANSWER, answer_id, edit_key, edit_value)