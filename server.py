from flask import Flask, render_template, request, redirect, url_for
import data_manager
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)


@app.route("/list", methods=['GET', 'POST'])
def list_question_page():
    if request.method == 'GET':
        all_question = data_manager.get_questions('submission_time', 'DESC')
        return render_template('list.html', all_questions=all_question)
    if request.method == 'POST':
        _order_by = request.form['order_by']
        _order_direction = request.form['order_direction']
        all_question = data_manager.get_questions(_order_by, _order_direction)
        return render_template('list.html', all_questions=all_question, order_by=_order_by,
                               order_direction=_order_direction)


@app.route("/", methods=['GET', 'POST'])
def main_page():
    return redirect("/list")


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def show_question_answers(question_id):
    question = data_manager.get_question_details_by_id(question_id)
    answers = data_manager.get_answers_details_by_question_id(question_id)
    if request.method == 'GET':
        data_manager.update_view_number(question_id)
        return render_template('show_id_question.html', question=question, question_id=question_id, answers=answers)


@app.route("/add-question", methods=['GET', 'POST'])
def add_question():
    if request.method == 'GET':
        return render_template('add-question.html')
    elif request.method == 'POST':
        title = request.form['title']
        message = request.form['message']
        image = request.form['image']
        data_manager.add_question(title, message, image)
        question_id = data_manager.get_question_id()
        return redirect('/question/' + str(question_id['id']))


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def add_new_answer(question_id):
    if request.method == 'GET':
        return render_template('new-answer.html', question_id=question_id)
    elif request.method == 'POST':
        image = request.form['image']
        message = request.form['message']
        data_manager.add_new_answer(question_id, message, image)
        return redirect('/question/' + question_id)


@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    data_manager.delete_question(question_id)
    return redirect('/list')


@app.route("/question/<question_id>/edit", methods=['GET', 'POST'])
def edit_question(question_id):
    question = data_manager.get_question_details_by_id(question_id)
    if request.method == "GET":
        return render_template('edit.html', question=question)
    elif request.method == "POST":
        title = request.form['title']
        message = request.form['message']
        image = request.form['image']
        data_manager.update_question(question_id, title, message, image)
        return redirect('/question/' + str(question['id']))


@app.route("/answer/<answer_id>/delete", methods=["GET", "POST"])
def delete_answer(answer_id):
    question_id = data_manager.get_question_by_answer_id(answer_id)
    data_manager.delete_answer(answer_id)
    return redirect('/question/' + str(question_id['question_id']))


@app.route("/question/<question_id>/vote-up", methods=['GET', 'POST'])
def vote_up_question(question_id):
    all_questions = data_manager.get_all_questions()
    question = None
    for question_row in all_questions:
        if question_row.get('id') == question_id:
            question = question_row
    if request.method == 'GET':
        vote_number = question['vote_number']
        vote_number = int(vote_number)
        vote_number += 1
    question['vote_number'] = vote_number
    data_manager.edit_question(question_id, 'vote_number', vote_number)
    return redirect('/list')


@app.route("/question/<question_id>/vote-down", methods=['GET', 'POST'])
def vote_down_question(question_id):
    all_questions = data_manager.get_all_questions()
    question = None
    for question_row in all_questions:
        if question_row.get('id') == question_id:
            question = question_row
    if request.method == 'GET':
        vote_number = question['vote_number']
        vote_number = int(vote_number)
        if vote_number > 0:
            vote_number -= 1
    question['vote_number'] = vote_number
    data_manager.edit_question(question_id, 'vote_number', vote_number)
    return redirect('/list')


@app.route("/answer/<answer_id>/vote-down", methods=['GET', 'POST'])
def vote_down_answer(answer_id):
    all_answer = data_manager.get_all_answers()
    answer = None
    for answer_row in all_answer:
        if answer_row.get('id') == answer_id:
            answer = answer_row
    if request.method == 'GET':
        vote_number = answer['vote_number']
        vote_number = int(vote_number)
        if vote_number > 0:
            vote_number -= 1
    answer['vote_number'] = vote_number
    data_manager.edit_answer(answer_id, 'vote_number', vote_number)
    question_id = answer['question_id']
    return redirect('/question/' + question_id)


@app.route("/answer/<answer_id>/vote-up", methods=['GET', 'POST'])
def vote_up_answer(answer_id):
    all_answer = data_manager.get_all_answers()
    answer = None
    for answer_row in all_answer:
        if answer_row.get('id') == answer_id:
            answer = answer_row
    if request.method == 'GET':
        vote_number = answer['vote_number']
        vote_number = int(vote_number)
        vote_number += 1
    answer['vote_number'] = vote_number
    data_manager.edit_answer(answer_id, 'vote_number', vote_number)
    question_id = answer['question_id']
    return redirect('/question/' + question_id)



if __name__ == "__main__":
    app.run()
