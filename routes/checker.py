from flask import jsonify, request, url_for
from requests import post
from routes import api
from os import environ

"""
CHECKER FOR A sample Hello World server.
"""
from os import environ, listdir, path
from flask import Flask, jsonify, request
from flask_cors import (CORS, cross_origin)
from subprocess import run, Popen, PIPE
from time import sleep
from shutil import which

# Define some global attributes
repo = 'hello-world'
check_dir = path.abspath('../checker/checks')

# Get the check files. Sometimes the pytests create __pycache__ folders, so
# just to be safe, we filter those out
check_files = [file for file in listdir(check_dir) if '.' in file]

def delete_repo(repo):
    """use subprocess.run to delete the repository folder""" 
    run(['rm', '-rf', repo])

def clone_repo(user):
    """clone respository from github"""
    link = f'https://github.com/{user}/{repo}'
    cmd = ['git', 'clone', link]
    process = Popen(cmd, stdout=PIPE, stderr=PIPE)
    try:
        print(process.communicate(timeout=5))
    except:
        return {'result': False}

    if process.returncode != 0:
        return {'result': False}

    return {
        'description': 'Github repository exists and is public',
        'result': True,
        'check_id': 0,
        'check_type': 'repo',
        'message': 'Success!'
    }

def run_user_app():
    """
    runs the user's flask app, sleeps to wait for app to begin, returns
    running process
    """
    env = {'FLASK_APP': 'app.py'}
    cmd = [which('flask'), 'run']
    user_app = Popen(cmd, stdout=PIPE, stderr=PIPE, cwd=repo, env=env)
    sleep(2)
    return user_app


def get_check_description(check_file):
    """
    In each check file, the description is the first line of the file as a
    comment.
    This method returns that line, minus the comment part (i.e. '# ')
    """

    check_file_path = path.join(check_dir, check_file)
    with open(check_file_path, 'r') as fp:
        description = fp.readline()[2:]
        fp.close()
    return description

def get_check_id(check_file):
    """
    The check_id is the check number.

    All check files are named <check_type>_<check_id>.<extension>
        e.g. pytest_2.py - Check #2 is a python script to be run with pytest
    """
    return check_file[check_file.find('_') + 1 : check_file.find('.')]

def get_check_type(check_file):
    """
    The check_type is the type of check we're testing (e.g. requirement,
    output, pytest, speed, etc)

    All check files are named <check_type>_<check_id>.<extension>
        e.g. pytest_2.py - Check #2 is a python script to be run with pytest
    """
    return check_file[:check_file.find('_')]

def test_exec(check_file, check_type):
    """
    Executes a test
    """
    if check_type == 'pytest':
        executor = 'pytest'
    else:
        executor = '/bin/bash'
    
    check_file_path = path.join(check_dir, check_file)
    
    command = f'{executor} {check_file_path}'.split()
    return Popen(command, stdout=PIPE, stderr=PIPE, cwd=repo)

def test(check_file):
    """
    parses a check_file and runs the check, returns a disctionary describing
    check results
    """
    check_type = get_check_type(check_file)

    # Returns an instance of a running process
    test_process = test_exec(check_file, check_type)

    out, err = test_process.communicate()
    return {
        'description': get_check_description(check_file),
        'check_id': get_check_id(check_file),
        'check_type': check_type,
        'stdout': out.decode(),
        'stderr': err.decode(), 
        'result': test_process.returncode == 0,
        'message': out.decode().rstrip().splitlines()[-1] # Last line of output
    }

def user_app_crashed(user_app):
    """ checks if a running process crashed """
    return user_app.poll() is not None


def checker_home(user):
    repo_download_result = clone_repo(user)
    results = [repo_download_result]
    if results[0]['result'] is True:
        user_app = run_user_app()
        for check in check_files:
            result = test(check)
            results.append(result)
            if user_app_crashed(user_app):
                user_app.terminate()
                user_app = run_user_app()
        user_app.terminate()
    delete_repo(repo)
    return results



@api.route('/checker', methods=['POST'], strict_slashes=False)
def checker():
    # response = post(environ['CHECKER_API_URL'], data=request.form)
    response = checker_home(request.form.get('user'))
    # if response.status_code != 200:
    #     print('FAILURE: {}'.format(response.text))
    #     return jsonify({'checks': None})
    print(response)
    return jsonify({'checks': response})
