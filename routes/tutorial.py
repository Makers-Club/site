from flask import render_template, request
from routes import tutorial
from models.auth import auth_client

@tutorial.route('/', methods=['GET', 'POST'], strict_slashes=False)
@auth_client.login_required
def index():
    """ starting tutorial page """
    data = {
        'quiz': getQuiz(),
        'passed': False,
        'current_user': request.current_user
    }
    if request.method == 'GET':
        return render_template('tutorial.html', data=data)
    else:
        quiz = data['quiz']
        questions = quiz['questions']
        correct_answers = 0

        for question in questions:
            for option in questions[question]['options']:
                user_answer = request.form.get(f'{question}_{option}')

                if user_answer is None:
                    continue

                print("user answer: ", user_answer)
                if user_answer == str(questions[question]['correct_answer']):
                    correct_answers += 1
                    print('Failed on question', question, option)

        data['passed'] = correct_answers == quiz['numberOfCorrectAnswers']
        print("passed ", data['passed'])
        return render_template('tutorial.html', data=data)


class Tutorial:
    def __init__(self, path = ''):
        self.file_path = path
        self.questions = []

    def add_question(self):
        raise NotImplementedError()

    def json(self):
        raise NotImplementedError()

class Question:
    def __init__(self):
        self.answer = None
        self.options = []

    def add_answer(self, answer):
        self.answer = answer

    def add_false_option(self, option):
        self.options.append(option)

def getQuiz():
    """ placeHolder for getting Quiz questions """
    return {
        'numberOfCorrectAnswers': 3,
        'questions': {
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
    }
