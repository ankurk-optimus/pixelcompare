from flask import Flask, make_response, send_file, session, request, redirect
import os
import json
import api.api as api
import api.prjinit as prjinit

app = Flask(__name__)

@app.route("/")
def index():
    return send_file("templates/index.html")

@app.route("/create_project", methods=['POST'])
def create_project():
    request_data = json.loads(request.data)
    config_data = request_data['config']
    devices_data= request_data['devices']
    resp_code = prjinit.create_project(config_data, devices_data, './projects')
    if resp_code == 0:
        return api.create_json_response({"status":"success", "error_code":0, "message":"Project created."});
    else:
        return api.create_json_response({"status":"failure", "error_code":-1, "message":"Project cannot be created."});

@app.route("/projects", methods=['GET'])
def get_projects():
    projects = [];
    for filename in os.listdir('./projects'):
        if os.path.isdir(os.path.join('./projects', filename)):
            projects.append(filename)
    return api.create_json_response({"status":"success", "error_code":0, "data":projects})

if __name__ == '__main__':
    app.run(debug=True)
