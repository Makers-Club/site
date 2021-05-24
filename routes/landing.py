from flask import render_template, request, g
from os import environ
from routes import landing

@landing.route('/', methods=['GET'], strict_slashes=False)
def index():
  """ render landing template """
  data = {}
  if request.current_user:
    data['current_user'] = request.current_user.to_dict()
    return render_template('dash.html', data=data)
  return render_template('landing.html', data=data)

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
