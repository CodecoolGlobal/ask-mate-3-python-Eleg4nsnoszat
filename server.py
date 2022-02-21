from flask import Flask, render_template, request, redirect, url_for
import data_manager

app = Flask(__name__)


@app.route("/")
def list_question_page():
    all_questions = data_manager.get_all_questions()
    return render_template('list.html', all_questions=all_questions)


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def show_question_answers(question_id):
    all_questions = data_manager.get_all_questions()
    question = all_questions[int(question_id)]
    answers = data_manager.get_answers(question_id)
    if request.method == 'GET':
        return render_template('show_id_question.html', question=question, answers=answers)
    '''if request.method == 'POST':
        user_stories[int(post_id)]["title"] = request.form["title"]
        user_stories[int(post_id)]["user_story"] = request.form["user_story"]
        user_stories[int(post_id)]["acceptance_criteria"] = request.form["acceptance_criteria"]
        user_stories[int(post_id)]["business_value"] = request.form["business_value"]
        user_stories[int(post_id)]["estimation"] = request.form["estimation"]
        user_stories[int(post_id)]["status"] = request.form["status"]
        data_manager.add_new_question(question)
        return redirect("/")'''


if __name__ == "__main__":
    app.run()
