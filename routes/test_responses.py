"""
Test that routes return the correct format and status code.
"""
from flask import jsonify
from main import client


def is_valid_html(response):
    """
    True if the response is valid html.
    """
    try:
        jsonify(response)
        # if it can be jsonified,
        # must be an error message
        return False
    except:
        return True

def test_landing_should_return_html(client):
    """
    The landing page is public, so it should always return valid html.
    """
    response = client.get("/").data.decode()
    assert(is_valid_html(response))

def test_about_us_should_return_html(client):
    """
    The About Us page is public, so it should always return valid html.
    """
    response = client.get("/about").data.decode()
    assert(is_valid_html(response))

def test_contact_us_should_return_html(client):
    """
    The Contact Us page is public, so it should return valid html.
    """
    response = client.get("/contact").data.decode()
    assert(is_valid_html(response))

def test_landing_should_return_status_code_200(client):
    """
    The landing page is public, so it should always return a status code of 200.
    """
    response = client.get("/")
    assert(response.status_code == 200)

def test_about_us_should_return_status_code_200(client):
    """
    The About Us page is publis, so it should always return a status code of 200.
    """
    response = client.get("/about")
    assert(response.status_code == 200)

def test_contact_us_should_return_status_code_200(client):
    """
    The Conatct Us page is public, so it should always return a status code of 200.
    """
    response = client.get("/contact")
    assert(response.status_code == 200)



