from flask import render_template, request
from routes import tutorial

@tutorial.route('/', methods=['GET', 'POST'], strict_slashes=False)
def index():
    """ starting tutorial page """
    data = {
        'quiz': getQuiz(),
        'passed': False
    }
    if request.method == 'GET':
        return render_template('tutorial.html', data=data)
    else:
        quiz = data['quiz']
        for question in quiz:
            for option in quiz[question]['options']:
                user_answer = request.form.get(f'{question}_{option}')

                if user_answer is None:
                    continue

                print("user answer: ", user_answer)
                if user_answer == str(quiz[question]['correct_answer']):
                    data['passed'] = True

        return render_template('tutorial.html', data=data)

def getQuiz():
    """ placeHolder for getting Quiz questions """
    return {
        'question1ID': {
            'text': "This is a question?",
            'options': {
                'option1': 1,
                'option2': 2,
                'option3': 3,
                'option4': 4,
            },
            'correct_answer': 1
            
        },
        'question2ID': {
            'text': "This is a question?",
            'options': {
                'option1': 1,
                'option2': 2,
                'option3': 3,
                'option4': 4,
            },
            'correct_answer': 3
        },
        'question3ID': {
            'text': "This is a question?",
            'options': {
                'option1': 1,
                'option2': 2,
                'option3': 3,
                'option4': 4,
            },
            'correct_answer': 2
        }
    }
