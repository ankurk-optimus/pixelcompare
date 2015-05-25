import sys
import os
import json
from flask import make_response


def correct_path(path):
    """
    Appends a / at the end of the path if not placed already.
    """
    if path[len(path) - 1] == '/':
        return path
    else:
        return path + '/'


def readInputFile(file_name):
    json_data = open(file_name).read()
    data = json.loads(json_data)
    return data


def create_json_response(status, error_code, message=None, data=None):
    """
	Convert result object to a JSON web response.
	"""
    result = None
    if message is not None:
        result = {
            'status': status, 'error_code': error_code, 'message': message}
    else:
        result = {'status': status, 'error_code': error_code, 'data': data}
    response = make_response(json.dumps(result))
    response.headers['Access-Control-Allow-Origin'] = "*"
    response.mimetype = "application/json"
    return response


def config_file_path(root, project_name, relative_path=False):
    if relative_path is False:
        return root + project_name + '/config.json'
    else:
        return project_name + '/config.json'


def devices_file_path(root, project_name, relative_path=False):
    if relative_path is False:
        return root + project_name + '/devices.json'
    else:
        return project_name + '/devices.json'


def source_file_path(root, project_name, page_name, device, relative_path=False):
    if relative_path is False:
        return root + project_name + '/input/source/' + page_name + '/' + device + '.png'
    else:
        return project_name + '/input/source/' + page_name + '/' + device + '.png'


def screenshot_file_path(root, project_name, page_name, device, relative_path=False):
    if relative_path is False:
        return root + project_name + '/input/screenshots/' + page_name + '/' + device + '.png'
    else:
        return project_name + '/input/screenshots/' + page_name + '/' + device + '.png'


def contourOnSource_file_path(root, project_name, page_name, device, relative_path=False):
    if relative_path is False:
        return root + project_name + '/output/' + page_name + '/' + device + '/contours_on_source.png'
    else:
        return project_name + '/output/' + page_name + '/' + device + '/contours_on_source.png'


def contourOnSubject_file_path(root, project_name, page_name, device, relative_path=False):
    if relative_path is False:
        return root + project_name + '/output/' + page_name + '/' + device + '/contours_on_subject.png'
    else:
        return project_name + '/output/' + page_name + '/' + device + '/contours_on_subject.png'


def diff_file_path(root, project_name, page_name, device, relative_path=False):
    if relative_path is False:
        return root + project_name + '/output/' + page_name + '/' + device + '/diff.png'
    else:
        return project_name + '/output/' + page_name + '/' + device + '/diff.png'
