from flask import render_template, g
from os import environ
from routes import landing

@landing.route('/', methods=['GET'], strict_slashes=False)
def index():
  """ render landing template """
  return render_template('landing.html', data=None)

@landing.route('/about', methods=['GET'], strict_slashes=False)
def about():
  """ render about template """
  return render_template('about.html', data=None)

@landing.route('/contact_us', methods=['GET'], strict_slashes=False)
def contact_us():
  """ render contact template """
  return render_template('contact.html', data=None)
