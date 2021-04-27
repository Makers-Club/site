from flask import Blueprint, render_template, g

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
  data = set_user()
  return render_template('landing.html', data=data)

@landing.route('/about', methods=['GET'], strict_slashes=False)
def about():
  data = set_user()
  return render_template('about.html', data=data)

@landing.route('/auth', methods=['GET'], strict_slashes=False)
def auth_page():
  return render_template('auth.html')

@landing.route('/contact_us', methods=['GET'], strict_slashes=False)
def contact_us():
  return render_template('contact.html')
