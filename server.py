from flask import Flask, render_template, request, redirect, url_for
import data_manager

app = Flask(__name__)


@app.route("/")
def list_question_page():
    all_questions = data_manager.get_all_questions()
    for question in all_questions:
        question['submission_time'] = data_manager.get_display_submission_time(int(question['submission_time']))
    return render_template('list.html', all_questions=all_questions)


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def show_question_answers(question_id):
    all_questions = data_manager.get_all_questions()
    question = None
    for question_row in all_questions:
        if question_row.get('id') == question_id:
            question = question_row
    answers = data_manager.get_answers(question_id)
    if request.method == 'GET':
        for answer in answers:
            answer['submission_time'] = data_manager.get_display_submission_time(int(answer['submission_time']))
        return render_template('show_id_question.html', question=question, answers=answers)


@app.route("/add-question", methods=['GET', 'POST'])
def add_question():
    question_id = data_manager.get_new_question_id()
    submission_time = data_manager.get_submission_time()
    view_number = 0
    vote_number = 0
    if request.method == "GET":
        return render_template('add-question.html', question_id=question_id,
                               submission_time=submission_time, view_number=view_number, vote_number=vote_number)
    elif request.method == "POST":
        new_question = {field_name: request.form[field_name] for field_name in data_manager.DATA_HEADER_QUESTION}
        data_manager.add_new_question(new_question)
        return redirect('/question/' + new_question.get('id'))

@app.route("/question/<question_id>/new-answer", methods=['GET', 'POST'])
def add_new_answer(question_id):
    answer_id = data_manager.get_new_answer_id()
    submission_time = data_manager.get_submission_time()
    vote_number = 0
    if request.method == "GET":
        return render_template('new-answer.html', question_id=question_id, id=answer_id,
                               submission_time=submission_time, vote_number=vote_number)
    elif request.method == "POST":
        new_answer = {field_name: request.form[field_name] for field_name in data_manager.DATA_HEADER_ANSWER}
        data_manager.add_new_answer(new_answer)
        return redirect('/question/' + question_id)

@app.route("/question/<question_id>/delete", methods=["GET", "POST"])
def delete_question(question_id):
    data_manager.delete_question(question_id)
    data_manager.delete_answer(question_id)
    return redirect('/')


@app.route("/question/<question_id>/edit", methods=['GET', 'POST'])
def edit_question(question_id):
    all_questions = data_manager.get_all_questions()
    question = None
    for question_row in all_questions:
        if question_row.get('id') == question_id:
            question = question_row
    question['submission_time'] = data_manager.get_submission_time()
    if request.method == "GET":
        return render_template('edit.html', id=question['id'], submission_time=question['submission_time'],
                               vote_number=question['vote_number'], view_number=question['view_number'],
                               question=question)
    elif request.method == "POST":
        data_manager.edit_question(question_id, 'title', request.form['title'])
        data_manager.edit_question(question_id, 'message', request.form['message'])
        return redirect('/question/' + question['id'])


@app.route("/answer/<answer_id>/delete", methods=["GET", "POST"])
def delete_answer(answer_id):
    all_answer = data_manager.get_all_answers()
    answer = None
    for answer_row in all_answer:
        if answer_row.get('id') == answer_id:
            answer = answer_row
    question_id = answer['question_id']
    data_manager.delete_answer(answer_id)
    return redirect('/question/' + question_id)


if __name__ == "__main__":
    app.run()
