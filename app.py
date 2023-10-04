from flask import Flask, render_template, redirect, request, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)


@app.route('/')
def start_page():
    """
    Route to start page survey selection
    """
    return render_template("start_page.html", surveys=surveys)


@app.route('/begin', methods=["POST"])
def choose_survey():
    """
    Directing user to chosen survey
    """
    survey_type = request.form.get('survey_type')
    session['survey_type'] = survey_type
    session[RESPONSES_KEY] = []
    return redirect('/questions/0')


@app.route('/questions/<int:question_id>', methods=['GET', 'POST'])
def question(question_id):
    """
    Question Handeling:
    - Displaying current question specific to survey type
    - Prevent user from skipping ahead or accessing non-existent questions 
    """
    # Define variables
    survey_type = session.get('survey_type')
    num_responses = len(session.get(RESPONSES_KEY, []))
    selected_survey = surveys[survey_type]
    responses = session.get(RESPONSES_KEY)
    current_question = selected_survey.questions[question_id]

    # Checking if the survey is chosen
    if not survey_type:
        return redirect('/')

    # Checking for number of responses
    if question_id != num_responses:
        flash("Invalid question, return to survey.")
        return redirect(f'/questions/{num_responses}')

    # Handling once all questions are answered
    if question_id >= len(selected_survey.questions):
        return redirect('/complete')

    # Process the user's response to a question
    if request.method == 'POST':
        choice = request.form.get('option')

        if choice:
            responses.append(choice)
            session[RESPONSES_KEY] = responses
            next_question_id = question_id + 1

            if next_question_id < len(selected_survey.questions):
                return redirect(f'/questions/{next_question_id}')
            else:
                return redirect('/answers')

    return render_template('questions.html', question=current_question.question, choices=current_question.choices, question_id=question_id)


@app.route('/answers')
def answer():
    """
    Display all the user responses
    """

    return render_template("answers.html", responses=session[RESPONSES_KEY])


@app.route('/finish')
def finish():
    return render_template("finish.html")


if __name__ == '__main__':
    app.debug = True
    app.run()
