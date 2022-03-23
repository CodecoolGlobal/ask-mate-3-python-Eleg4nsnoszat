from flask import Flask, render_template, request, redirect, url_for, session
import data_manager
import os
from werkzeug.utils import secure_filename
import time

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\xec]/'
UPLOAD_FOLDER = 'static/uploads/'

'''Put filename and save image to data manager!'''
'''Remove methods if not used'''
'''Modify data manager queries like question tag(not f string)'''
'''url_for documentation to read'''


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


@app.route('/list', methods=['GET', 'POST'])
def list_question_page():
    if request.method == 'GET':
        all_question = data_manager.get_questions('submission_time', 'DESC')
        return render_template('list.html', all_questions=all_question)
    if request.method == 'POST':
        _order_by = request.form['order_by']
        _order_direction = request.form['order_direction']
        _search = request.form['search']
        if _search:
            all_question = data_manager.search_questions(_search, _order_by, _order_direction)
            return render_template('list.html', all_questions=all_question, search=_search,
                                   order_by=_order_by, order_direction=_order_direction)
        else:
            all_question = data_manager.get_questions(_order_by, _order_direction)
            return render_template('list.html', all_questions=all_question, order_by=_order_by,
                                   order_direction=_order_direction)


@app.route("/", methods=['GET', 'POST'])
def main_page():
    if request.method == 'GET':
        latest_questions = data_manager.get_latest_questions('submission_time', 'DESC')
        if 'username' in session:
            username = session['username']
            user_id = session['user_id']
            user_id = user_id['user_id']
            return render_template('index.html', latest_questions=latest_questions,
                                   username=username, user_id=str(user_id))
        else:
            return render_template('index.html', latest_questions=latest_questions, username='', user_id=None)

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
        if 'username' in session:
            username = session['username']
            return render_template('show_id_question.html', question=question, question_id=question_id, answers=answers,
                                   comments=comments, all_tags_for_question=all_tags_for_question, username=username)
        else:
            return render_template('show_id_question.html', question=question, question_id=question_id, answers=answers,
                                   comments=comments, all_tags_for_question=all_tags_for_question, username='')


@app.route("/add-question", methods=['GET', 'POST'])
def add_question():
    if request.method == 'GET':
        if session.get('username'):
            return render_template('add-question.html')
        else:
            return redirect(url_for("login"))

    elif request.method == 'POST':
        title = request.form['title']
        message = request.form['message']
        image_name = get_filename()
        author = session.get('user_id')
        author_id = author['user_id']
        user = session.get('username')
        save_image()
        data_manager.add_question(title, message, image_name, author_id, user)
        question_id = data_manager.get_question_id()
        return redirect('/question/' + str(question_id['id']))


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def add_new_answer(question_id):
    if request.method == 'GET':
        if session.get('username'):
            return render_template('new-answer.html', question_id=question_id)
        else:
            return redirect(url_for("login"))

    elif request.method == 'POST':
        image_name = get_filename()
        save_image()
        message = request.form['message']
        author = session.get('user_id')
        author_id = author['user_id']
        username = session.get('username')
        data_manager.add_new_answer(question_id, message, image_name, author_id, username)
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
    question = data_manager.get_question_details_by_id(question_id)
    author_id = question['author_id']
    data_manager.upvote_question(question_id)
    data_manager.gain_reputation(author_id, 5)
    return redirect('/list')


@app.route("/question/<question_id>/vote-down", methods=['GET', 'POST'])
def vote_down_question(question_id):
    question = data_manager.get_question_details_by_id(question_id)
    author_id = question['author_id']
    data_manager.downvote_question(question_id)
    data_manager.lose_reputation(author_id, 2)
    return redirect('/list')


@app.route("/answer/<answer_id>/vote-down", methods=['GET', 'POST'])
def vote_down_answer(answer_id):
    question_id = data_manager.get_question_by_answer_id(answer_id)
    answer = data_manager.get_answer_by_answer_id(answer_id)
    author_id = answer['author_id']
    data_manager.downvote_answer(answer_id)
    data_manager.lose_reputation(author_id, 2)
    return redirect('/question/' + str(question_id['question_id']))


@app.route("/answer/<answer_id>/vote-up", methods=['GET', 'POST'])
def vote_up_answer(answer_id):
    question_id = data_manager.get_question_by_answer_id(answer_id)
    answer = data_manager.get_answer_by_answer_id(answer_id)
    author_id = answer['author_id']
    data_manager.upvote_answer(answer_id)
    data_manager.gain_reputation(author_id, 10)
    return redirect('/question/' + str(question_id['question_id']))


@app.route("/question/<question_id>/new-comment", methods=['GET', 'POST'])
def add_comment_to_question(question_id):
    if request.method == 'GET':
        return render_template("new-comment.html", question_id=question_id)
    if request.method == 'POST':
        message = request.form['message']
        author = session.get('user_id')
        author_id = author['user_id']
        username = session.get('username')
        data_manager.add_new_comment_to_question(question_id, message, author_id, username)
        return redirect('/question/' + str(question_id))


@app.route("/answer/<answer_id>/new-comment", methods=['GET', 'POST'])
def add_comment_to_answer(answer_id):
    question_id = data_manager.get_question_by_answer_id(answer_id)
    if request.method == 'GET':
        return render_template("new-comment-answer.html", answer_id=answer_id)
    if request.method == 'POST':
        message = request.form['message']
        author = session.get('user_id')
        author_id = author['user_id']
        username = session.get('username')
        data_manager.add_new_comment_to_answer(answer_id, message, author_id, username)
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
        if question_id is not None:
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


@app.route("/tags")
def show_tags():
    tags = data_manager.get_all_tags_by_question()
    return render_template("show-tags.html", tags=tags)


@app.route("/answer/<answer_id>/edit", methods=["GET", "POST"])
def edit_answer(answer_id):
    answer = data_manager.get_answer_by_answer_id(answer_id)
    if request.method == 'GET':
        return render_template("edit-answer.html", answer_id=answer_id, answer=answer)
    question_id = data_manager.get_question_by_answer_id(answer_id)
    message = request.form['message']
    data_manager.update_answer(message, answer_id)
    return redirect("/question/" + str(question_id['question_id']))


@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "GET":
        return render_template("registration.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if data_manager.check_registration(username) is None:
            hashed_password = data_manager.hash_password(password)
            data_manager.registration(username, hashed_password)
            return redirect("/")
        else:
            return redirect(url_for("registration"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", '')
        hashed_password = data_manager.get_hashed_password(username)
        verify_password = data_manager.verify_password(password, hashed_password)
        if verify_password is True:
            session['username'] = request.form['username']
            session['user_id'] = data_manager.get_user_id_by_username(username)
            return redirect(url_for("main_page"))
        else:
            error = 'Invalid email and/or password. Please try again.'
            return render_template("login.html", error=error)
    else:
        if session.get('username'):
            return redirect("/")
        else:
            return render_template("login.html", error=error)


@app.route('/user/<user_id>')
def user_page(user_id):
    user_data = data_manager.get_all_user_data(user_id)
    asked_questions_num = data_manager.get_num_of_asked_questions_by_user_id(user_id)
    asked_questions_num = asked_questions_num['user_questions']
    asked_questions = data_manager.get_asked_questions_by_user_id(user_id)
    user_answers_num = data_manager.get_num_of_user_answers(user_id)
    user_answers_num = user_answers_num['user_answers']
    user_answers = data_manager.get_user_answers_by_user_id(user_id)
    comments_num = data_manager.get_num_of_user_comments(user_id)
    comments_num = comments_num['user_comments']
    user_comments = data_manager.get_user_comments_by_user_id(user_id)
    print(user_comments)
    return render_template('user-page.html', user_data=user_data, asked_questions_num=asked_questions_num,
                           asked_questions=asked_questions, user_answers_num=user_answers_num,
                           user_answers=user_answers, comments_num=comments_num, user_comments=user_comments)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('main_page'))


@app.route("/users")
def list_users():
    if session.get('username'):
        users_info = data_manager.users_info()
        return render_template("users.html", users_info=users_info)
    else:
        return redirect(url_for("main_page"))


if __name__ == "__main__":
    app.run()
