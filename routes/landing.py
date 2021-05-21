from flask import render_template, request, g
from os import environ
from routes import landing

@landing.route('/', methods=['GET'], strict_slashes=False)
def index():
  """ render landing template """

  if request.current_user:
    return render_template('dash.html', data=request.current_user.to_dict())
  return render_template('landing.html', data=None)

@landing.route('/about', methods=['GET'], strict_slashes=False)
def about():
  """ render about template """
  return render_template('about.html', data=None)

@landing.route('/contact', methods=['GET'], strict_slashes=False)
def contact():
  """ render contact template """
  return render_template('contact.html', data=None)
