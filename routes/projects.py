from flask import render_template, request
from routes import projects
from models.auth import auth_client

@projects.route('/', methods=['GET', 'POST'], strict_slashes=False)
@auth_client.login_required
def index():
    project = setProject()
    data = {
        'current_user': request.current_user.to_dict(),
        'project': project
    }
    return render_template('project.html', data=data)

@projects.route('/<project_id>/<sprint_id>/<task_id>', methods=['GET'], strict_slashes=False)
def sprint_task_by_id(project_id, sprint_id, task_id):
    data = {
        'current_user': request.current_user.to_dict(),
        'project': setProject(),
        'task': setTask()
    }
    return render_template('task.html', data=data)


def setProject():
    project = {
        'title': 'Historic Black Wallstreet Business Directory',
        'repository': 'hello-world',
        'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam accumsan quam sed euismod tempus. \
                        Quisque auctor feugiat quam hendrerit ullamcorper. Nulla interdum risus vel sodales iaculis. Donec \
                        semper nisi at vestibulum condimentum. Maecenas non gravida purus. Praesent bibendum sit amet lacus auctor pellentesque.',
        'preview_images': ['https://i.imgur.com/4Eso2sc.png', 'https://i.imgur.com/KR33ftT.png', 'https://i.imgur.com/tpGOXfD.png'],
        'videos': ['https://www.youtube.com/embed/hRFUZBXOWZI', 'https://www.youtube.com/embed/GAlKHqcnKTw'],
        'resources': [{'link':'https://www.azlyrics.com/n/nickelback.html', 'name': "The Meaning of Life"}],
        'quizes': ['#THEREARENOQUIZESYET'],
        'goals': ['Put your left foot in', 'Your left foot out', 'Your left foot in',
                    'And shake it all about', 'You do the hokey pokey', 'And turn yourself around'],
        'dependencies': ['Python 3.8', 'Flask', 'The Will to Live'],
        'progress': '0',
        'sprints': ['Sprint 1', 'Sprint 2', 'Sprint 3']
    }

    return project

def setTask():
    task = {
        'description': 'Time to make computer go burr',
        'code': "function wasteTime() {\n  setTimeout(\n    () => {\n      console.log('Are we there yet');\n      wasteTime();\n    }, 1000\n  );\n}",
        'completed': False
    }
    return task