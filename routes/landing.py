from flask import render_template, request, g
from os import environ
from routes import landing
from models.clients.maker_teams_client import MTClient
from models.project import Project

@landing.route('/thankyou', methods=['GET'], strict_slashes=False)
def presignup():
    # let's users know they've pre-signed up
    return render_template('presignup.html', data={})

@landing.route('/', methods=['GET'], strict_slashes=False)
def index():
  """ render landing template """
  data = {}
  from models.project_template import ProjectTemplate
  project_templates = ProjectTemplate.get_all(MTClient)

  data['templates'] = []

  for template in project_templates:
      data['templates'].append(template.to_dict())

  if request.current_user:
    data['current_user'] = request.current_user.to_dict()
    print('template id', [x.get('id') for x in data['templates']])
    return render_template('dash.html', data=data)
  return render_template('landing.html')



@landing.route('/about', methods=['GET'], strict_slashes=False)
def about():
  """ render about template """
  data = {}
  if request.current_user:
    data['current_user'] = request.current_user.to_dict()
  return render_template('about.html', data=data)

@landing.route('/contact', methods=['GET'], strict_slashes=False)
def contact():
  """ render contact template """
  data = {}
  if request.current_user:
    data['current_user'] = request.current_user.to_dict()
  return render_template('contact.html', data=data)


def allProjects():
    """ query all projects in database """
    projects = []

    for _ in range(3):
        projects.append({
            'title': 'Title',
            'link': 'https://www.historicblackwallstreet.com/',
            'author': 'Makers Club',
            'description': 'Me me do things double plus bigly',
            'price': 1.23,
            'preview': 'https://i.redd.it/60h3y9h882h51.jpg',
            'unlocked': False
        })

    return projects
