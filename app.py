from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "do*not*tell"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route('/')
def render_root():
    return render_template('begin.html', survey_title = satisfaction_survey.title, survey_instructions = satisfaction_survey.instructions)

@app.route('/survey', methods=["POST"])
def start_survey():
    if not session.get('responses'):
        session['responses'] = []
    n = len(session['responses'])
    return redirect(f'/questions/{n}')

@app.route('/questions/<question_index>')
def question(question_index):
    if len(session['responses']) == len(satisfaction_survey.questions):
        flash('You have answered all of the questions', 'err')
        return render_template('thankyou.html')
    if not int(question_index) == len(session['responses']):
        flash('Please answer all questions in order', 'err')
        question_index = len(session['responses'])
    question = satisfaction_survey.questions[int(question_index)]
    return render_template('question.html', question_number = (int(question_index) + 1), question_text = question.question, question_choices = question.choices)

def pair_q_r(questions, responses):
    q_and_r = []
    for n in range(len(responses)):
        q_and_r.append((questions[n].question, responses[n]))
    return q_and_r

@app.route('/questions/<question_index>', methods=["POST"])
def get_answer(question_index):
    hold = session['responses']
    hold.append(request.form.get("response"))
    session['responses'] = hold
    if int(question_index) < len(satisfaction_survey.questions):
        return redirect(f'/questions/{question_index}')
    else:
        return redirect('/thank_you')

@app.route('/thank_you')
def gratitude():
    q_and_r = pair_q_r(satisfaction_survey.questions, session['responses'])
    return render_template('thankyou.html', q_and_r = q_and_r)