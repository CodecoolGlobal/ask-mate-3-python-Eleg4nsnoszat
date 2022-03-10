from flask import Flask, render_template, request, redirect, url_for
import data_manager
import os
from werkzeug.utils import secure_filename
import time

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'


def get_filename():
    image = request.files['image']
    timestamp = time.time()
    timestamp = round(timestamp)
    if image.filename:
        filename = secure_filename(str(timestamp) + image.filename)
    else:
        filename = ''
    return filename


def save_image():
    filename = get_filename()
    image = request.files['image']
    if filename:
        image.save(os.path.join(UPLOAD_FOLDER, filename))


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
    if request.method == 'GET':
        latest_questions = data_manager.get_latest_questions('submission_time', 'DESC')
        return render_template('index.html', latest_questions=latest_questions)
    if request.method == 'POST':
        _order_by = request.form['order_by']
        _order_direction = request.form['order_direction']
        latest_questions = data_manager.get_latest_questions(_order_by, _order_direction)
        return render_template('index.html', latest_questions=latest_questions, order_by=_order_by,
                               order_direction=_order_direction)


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def show_question_answers(question_id):
    question = data_manager.get_question_details_by_id(question_id)
    answers = data_manager.get_answers_details_by_question_id(question_id)
    comments = data_manager.get_comments_by_question_id(question_id)
    all_tags_for_question = data_manager.get_tags_by_question_id(question_id)
    if request.method == 'GET':
        data_manager.update_view_number(question_id)
        return render_template('show_id_question.html', question=question, question_id=question_id, answers=answers,
                               comments=comments, all_tags_for_question=all_tags_for_question)


@app.route("/add-question", methods=['GET', 'POST'])
def add_question():
    if request.method == 'GET':
        return render_template('add-question.html')
    elif request.method == 'POST':
        title = request.form['title']
        message = request.form['message']
        image_name = get_filename()
        save_image()
        data_manager.add_question(title, message, image_name)
        question_id = data_manager.get_question_id()
        return redirect('/question/' + str(question_id['id']))


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def add_new_answer(question_id):
    if request.method == 'GET':
        return render_template('new-answer.html', question_id=question_id)
    elif request.method == 'POST':
        image_name = get_filename()
        save_image()
        message = request.form['message']
        data_manager.add_new_answer(question_id, message, image_name)
        return redirect('/question/' + question_id)


@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    question = data_manager.get_question_details_by_id(question_id)
    filename = question['image']
    if filename:
        os.remove(os.path.dirname(__file__) + '/' + UPLOAD_FOLDER + filename)
    data_manager.delete_question(question_id)
    return redirect('/list')


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    question = data_manager.get_question_details_by_id(question_id)
    if request.method == 'GET':
        return render_template('edit.html', question=question)
    if request.method == 'POST':
        title = request.form['title']
        message = request.form['message']
        image = request.files['image']
        if image.filename:
            image_name = get_filename()
            save_image()
        else:
            image_name = question['image']
        data_manager.update_question(question_id, title, message, image_name)
        return redirect('/question/' + str(question['id']))


@app.route('/question/<question_id>/edit/remove-image')
def delete_uploaded_question_image(question_id):
    if request.method == 'GET':
        question = data_manager.get_question_details_by_id(question_id)
        image_name = question['image']
        data_manager.delete_question_image(question_id)
        if image_name:
            os.remove(os.path.dirname(__file__) + '/' + UPLOAD_FOLDER + image_name)
        return redirect('/question/' + str(question_id) + '/edit')


@app.route("/answer/<answer_id>/delete", methods=["GET", "POST"])
def delete_answer(answer_id):
    question_id = data_manager.get_question_by_answer_id(answer_id)
    answer = data_manager.get_answer_by_answer_id(answer_id)
    image_name = answer['image']
    if image_name:
        os.remove(os.path.dirname(__file__) + '/' + UPLOAD_FOLDER + image_name)
    data_manager.delete_answer(answer_id)
    return redirect('/question/' + str(question_id['question_id']))


@app.route("/question/<question_id>/vote-up", methods=['GET', 'POST'])
def vote_up_question(question_id):
    data_manager.upvote_question(question_id)
    return redirect('/list')


@app.route("/question/<question_id>/vote-down", methods=['GET', 'POST'])
def vote_down_question(question_id):
    data_manager.downvote_question(question_id)
    return redirect('/list')


@app.route("/answer/<answer_id>/vote-down", methods=['GET', 'POST'])
def vote_down_answer(answer_id):
    question_id = data_manager.get_question_by_answer_id(answer_id)
    data_manager.downvote_answer(answer_id)
    return redirect('/question/' + str(question_id['question_id']))


@app.route("/answer/<answer_id>/vote-up", methods=['GET', 'POST'])
def vote_up_answer(answer_id):
    question_id = data_manager.get_question_by_answer_id(answer_id)
    data_manager.upvote_answer(answer_id)
    return redirect('/question/' + str(question_id['question_id']))


@app.route("/question/<question_id>/new-comment", methods=['GET', 'POST'])
def add_comment_to_question(question_id):
    if request.method == 'GET':
        return render_template("new-comment.html", question_id=question_id)
    if request.method == 'POST':
        message = request.form['message']
        data_manager.add_new_comment_to_question(question_id, message)
        return redirect('/question/' + str(question_id))


@app.route("/answer/<answer_id>/new-comment", methods=['GET', 'POST'])
def add_comment_to_answer(answer_id):
    question_id = data_manager.get_question_by_answer_id(answer_id)
    if request.method == 'GET':
        return render_template("new-comment-answer.html", answer_id=answer_id)
    if request.method == 'POST':
        message = request.form['message']
        data_manager.add_new_comment_to_answer(answer_id, message)
        return redirect('/question/' + str(question_id['question_id']))


@app.route("/show-answer-comments/<answer_id>", methods=['GET'])
def show_answer_comments(answer_id):
    comments = data_manager.get_comments_by_answer(answer_id)
    question_id = data_manager.get_question_by_answer_id(answer_id)
    if request.method == 'GET':
        return render_template("show-answer-comments.html", comments=comments,
                               question_id=question_id, answer_id=answer_id)


@app.route("/comment/<comment_id>/edit", methods=['GET', 'POST'])
def edit_comment(comment_id):
    comment = data_manager.get_comment_by_id(comment_id)
    question_id = comment['question_id']
    answer_id = comment['answer_id']
    if request.method == 'GET':
        return render_template("edit-comment.html", comment=comment, comment_id=comment_id)
    if request.method == 'POST':
        message = request.form['message']
        data_manager.update_comment(comment_id, message)
        if question_id:
            return redirect('/question/' + str(question_id))
        else:
            question = data_manager.get_question_by_answer_id(answer_id)
            question_id = question['question_id']
            return redirect('/question/' + str(question_id))


@app.route("/comments/<comment_id>/delete", methods=["GET", "POST"])
def delete_comment(comment_id):
    comment = data_manager.get_comment_by_id(comment_id)
    question_id = comment['question_id']
    answer_id = comment['answer_id']

    data_manager.delete_comment(comment_id)
    if answer_id:
        question = data_manager.get_question_by_answer_id(answer_id)
        question_id = question['question_id']

    return redirect("/question/" + str(question_id))


@app.route("/question/<question_id>/new-tag", methods=["GET", "POST"])
def add_tag(question_id):
    all_tags = data_manager.get_all_tags()
    if request.method == 'GET':
        return render_template('add-tag.html', question_id=question_id, all_tags=all_tags)
    if request.method == 'POST':
        name = request.form['name']
        data_manager.add_tag_for_tag(name)
        data_manager.add_tag_for_question_tag(question_id)
        return redirect("/question/" + str(question_id))


@app.route("/question/<question_id>/tag/<tag_id>/delete", methods=["GET", "POST"])
def delete_tag(question_id, tag_id):
    data_manager.delete_tag(tag_id)
    return redirect("/question/" + str(question_id))


@app.route("/answer/<answer_id>/edit", methods=["GET", "POST"])
def edit_answer(answer_id):
    answer = data_manager.get_answer_by_answer_id(answer_id)
    if request.method == 'GET':
        return render_template("edit-answer.html", answer_id=answer_id, answer=answer)
    question_id = data_manager.get_question_by_answer_id(answer_id)
    message = request.form['message']
    data_manager.update_answer(message, answer_id)
    return redirect("/question/" + str(question_id['question_id']))


if __name__ == "__main__":
    app.run()
