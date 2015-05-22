import sys
import os
import json
from flask import make_response
errors = {
	0:"Error 1",
	1:"Error 2",}

def correct_path(path):
	"""
		Appends a / at the end of the path if not placed already.
	"""
	if path[len(path)-1] == '/':
		return path
	else:
		return path + '/'


def readInputFile(file_name):
	json_data = open(file_name).read()
	data = json.loads(json_data)
	return data

def create_json_response(result):
    """Convert result object to a JSON web response."""
    response = make_response(json.dumps(result))
    response.headers['Access-Control-Allow-Origin'] = "*"
    response.mimetype = "application/json"
    return response
