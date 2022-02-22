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
    question = all_questions[int(question_id) - 1]
    answers = data_manager.get_answers(question_id)
    if request.method == 'GET':
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
        return redirect('/question/' + question_id) #new_question.get('id'))


if __name__ == "__main__":
    app.run()
