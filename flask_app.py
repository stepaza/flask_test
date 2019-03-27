# -*- coding: utf-8 -*-
"""
This module contains the actual Flask application, including the global variable ``TASKS`` containing all
tasks added or removed with calls to the API. Upon start, the app contains 2 tasks:

::

    TASKS = [
        {
            'id':           1,
            'title':        'Buy groceries',
            'description':  'Milk, Cheese, Pizza Ätna, Fruit, Tylenol',
            'done':         False,
        },
        {
            'id':           2,
            'title':        'Find cute French names',
            'description':  'Which is better - Charlotte or Geneviève?',
            'done':         False,
        }
    ]


The application itself is actually simple: a user can alter specific tasks stored in the ``TASKS`` variable using one
of the 5 API methods:

 + ``GET``
 + ``PUT``
 + ``POST``
 + ``DELETE``
 + ``PATCH``

Each task has 4 attributes:

================    =========================================================
Attribute           Description  
================    =========================================================
``id``              continuous integer, serves as a unique identifier for tasks.
``title``           task title.
``description``     more detailed description of each task.
``done``            boolean, one of ``True`` or ``False``.
================    =========================================================

Authentication is done using Flask's built-in ``HTTPBasicAuth()``.

In addition to the ``TASKS`` variable, all tasks are written to file, where that file is named ``<task_id>.txt``. The
path to that file is extracted from an environment variable called ``TASK_PATH``.

Example
    Assuming that ``TASK_PATH`` is set to ``D:/SomeFolder/FlaskTasks``, the contents of a newly created task (e.g.
    via the POST method) with some ``id`` <task_id> will be written to the file
    ``D:/SomeFolder/FlaskTasks/<task_id>.txt``. Similarly, if the DELETE method is invoked, the corresponding
    ``<task_id>.txt`` file will be deleted.

Deployment of applications in IDSC projects is largely based on Docker containerization. Since environmental variables
are an excellent choice for controlling docker, apps should be built accordingly.

-----

"""

from flask import Flask, abort, make_response, request
from flask_httpauth import HTTPBasicAuth
import os
import flask_functions as ff
from pathlib import PurePath

###############################################################################
#  Setup the "Database" of tasks
###############################################################################
TASKS = [
    {
        'id':           1,
        'title':        'Buy groceries',
        'description':  'Milk, Cheese, Pizza Ätna, Fruit, Tylenol',
        'done':         False,
    },
    {
        'id':           2,
        'title':        'Find cute French names',
        'description':  'Which is better - Charlotte or Geneviève?',
        'done':         False,
    }
]

# Write these tasks to file



###############################################################################
#  Code for flask_app.py
###############################################################################

app = Flask(__name__)

###############################################################################
#  Setup Authentication
###############################################################################
auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    """Obtains a password for *username* in case the user exists.

    Args:
        username (str): username passed to this function in the context of authenticating with the app.

    Returns:
        str or None:    user's password if the user is explicitly specified in this function, None otherwise.
    """
    if username == 'miguel':
        return 'python'
    return None


@auth.error_handler
def unauthorized():
    """Returns a JSON-formatted ``Unauthorized Access`` message.

    Returns:
        : JSON representation of the error ``Unauthorized Access``
    """

    return make_response(ff.convert_json({'error': 'Unauthorized Access'}), 401)

print(os.environ['TASK_PATH'])
###############################################################################
#  GET Methods
###############################################################################
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
@auth.login_required
def get_task(task_id):
    """Method for retrieving the task with *task_id*.

    Args:
        task_id (int): task id passed in the ``/todo/api/v1.0/tasks/<int:task_id>`` url

    Returns:
        : JSON representation of the task with *task_id*, Error 404 otherwise
    """
    # print(task_id) # For testing purposes
    task = [task for task in TASKS if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return ff.convert_json({'task': task[0]})


################################################################################################################
#  POST Methods
################################################################################################################
@app.route('/todo/api/v1.0/tasks', methods=['POST'])
@auth.login_required
def create_task():
    """Function to create a new task using the POST method.

    Returns:
        : tuple of (*JSON representation of the task created*, *201*) if task is created successfully, HTML code 400
        otherwise
    """
    html_code_dict = {'Created': 201, 'Bad_Request': 400} # Maps messages to HTML codes

    if not request.json or 'title' not in request.json:
        abort(html_code_dict['Bad_Request'])
    task = {
        'id': TASKS[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    TASKS.append(task)

    # Write task to file
    task_nbr = task['id']
    file_path = PurePath(os.environ['TASK_PATH'], f"T{task_nbr}.txt")
    with open(file_path, 'w') as taskfile:
        taskfile.write(f'id = {task["id"]}\n')
        taskfile.write(f"title = {task['title']}\n")
        taskfile.write(f"Description = {task['description']}\n")
        taskfile.write(f"Done = {task['done']}\n")
    return ff.convert_json({'task': task}), html_code_dict['Created']


################################################################################################################
#  DELETE Methods
################################################################################################################
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
@auth.login_required
def delete_task(task_id):
    """Deletes a specific task.

    Args:
        task_id (int): ID of task to be deleted.

    Returns:
        : JSON representation of ``Successfully deleted task [task_id]``, HTML Code 400 otherwise.
    """
    task = [task for task in TASKS if task['id'] == task_id] # this list will always be of length 1
    if len(task) == 0:
        abort(404)
    TASKS.remove(task[0])
    # Delete the task file if it exists
    try:
        file_path = PurePath(os.environ['TASK_PATH'], f"T{task[0]['id']}.txt")
        os.remove(file_path)
    except Exception as e:
        do_nothing = ''
    return ff.convert_json({'result': True, 'Message from the API' : 'Successfully deleted task ' + str(task_id)})

################################################################################################################
###  PUT Methods
################################################################################################################
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
@auth.login_required

def update_task(task_id):
    """Function to update a task in the database.

    Args:
        task_id (int):  ID of task to update.

    Returns:
        : JSON representation of ``Successfully updated task [task_id]``, corresponding HTML error code otherwise.
    """
    task = [task for task in TASKS if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    # if 'title' in request.json and type(request.json['title']) != unicode: # unicode testing currently not implemented (is it really necessary? >> default encoding for python 3)
    #     abort(400)
    # if 'description' in request.json and type(request.json['description']) is not unicode:
    #     abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return ff.convert_json({'task': task[0], 'Message from the API': 'Successfully updated task ' + str(task_id)})

################################################################################################################
###  Global Error Handling
################################################################################################################
@app.errorhandler(404) # improve the error handler, as ERROR 404 returns an HTML string by default from Flask

def not_found(error):
    """Function for formatting error messages in JSON.

    Args:
        error (str): Unused variable

    Returns:
        : JSON representation of ``Not found``
    """
    return make_response(ff.convert_json({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(host = '0.0.0.0')

