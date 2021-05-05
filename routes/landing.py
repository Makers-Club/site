from flask import Blueprint, render_template, g
from os import environ

landing = Blueprint('landing', __name__, url_prefix="")
payload = {
  'authenticated_user': None
}

def set_user(**kwargs) -> dict:
  """ fill in payload w/ user data """
  data = payload.copy()

  data.update(kwargs)
  return data

@landing.route('/', methods=['GET'], strict_slashes=False)
def index():
  """ render landing template """
  print(environ['GITHUB_CLIENT_ID'])
  data = {'func': 'github_login("{}")'.format(environ['GITHUB_CLIENT_ID'])}
  return render_template('landing.html', data=data)

@landing.route('/about', methods=['GET'], strict_slashes=False)
def about():
  """ render about template """
  data = set_user()
  return render_template('about.html', data=data)

@landing.route('/contact_us', methods=['GET'], strict_slashes=False)
def contact_us():
  """ render contact template """
  return render_template('contact.html', data=None)
