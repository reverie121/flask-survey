from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "do*not*tell"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def render_root():
    return render_template('begin.html', survey_title = satisfaction_survey.title, survey_instructions = satisfaction_survey.instructions)

@app.route('/questions/<question_index>')
def question(question_index):
    if len(responses) == len(satisfaction_survey.questions):
        flash('You have answered all of the questions', 'err')
        return render_template('thankyou.html')
    if not int(question_index) == len(responses):
        flash('Please answer all questions in order', 'err')
        question_index = len(responses)
    question = satisfaction_survey.questions[int(question_index)]
    return render_template('question.html', question_number = (int(question_index) + 1), question_text = question.question, question_choices = question.choices)

@app.route('/questions/<question_index>', methods=["POST"])
def get_answer(question_index):
    responses.append(request.form.get("response"))
    if int(question_index) < len(satisfaction_survey.questions):
        return redirect(f'/questions/{question_index}')
    else:
        return redirect('/thank_you')

@app.route('/thank_you')
def gratitude():
    return render_template('thankyou.html')