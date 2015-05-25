from flask import Flask, make_response, send_file, session, request, redirect
import os
import json
import api.api as api
import api.prjinit as prjinit

app = Flask(__name__)

PRJ_ROOT = './static/projects/'

@app.route("/")
def index():
    return send_file("templates/index.html")

@app.route("/create_project", methods=['POST'])
def create_project():
    request_data = json.loads(request.data)
    config_data = request_data['config']
    devices_data = request_data['devices']
    resp_code = prjinit.create_project(
        config_data, devices_data, PRJ_ROOT)
    if resp_code == 0:
        return api.create_json_response("success", 0, message="Project Created.")
    else:
        return api.create_json_response("failure", -1, message="Project cannot be created.")


@app.route("/projects", methods=['GET'])
def get_projects():
    projects = []
    for filename in os.listdir(PRJ_ROOT):
        if os.path.isdir(PRJ_ROOT + filename):
            projects.append(filename)
    return api.create_json_response("success", 0, data=projects)


@app.route("/testcases/<project_name>", methods=['GET'])
def getTestCases(project_name):
    config_data = api.readInputFile(api.config_file_path(PRJ_ROOT, project_name))
    devices_data = api.readInputFile(api.devices_file_path(PRJ_ROOT, project_name))

    response_data={
        'projectName': config_data['projectName'],
        'testcases': None
    }
    testcases=[]

    for subject in config_data['subject']:
        page_name=subject['pageName']
        page_url=subject['pageUrl']
        testcase={
            'pageName': page_name,
            'pageUrl': page_url,
            'images': []
        }
        for device in subject['devices']:
            image={
                'device': device,
                'source': None,
                'screenshot': None,
                'output': {
                    'contourOnSubject': None,
                    'contourOnSource': None,
                    'diff': None
                }
            }

            source_file_path=api.source_file_path(
                PRJ_ROOT, project_name, page_name, device)
            screenshot_file_path=api.screenshot_file_path(
                PRJ_ROOT, project_name, page_name, device)
            contourOnSource_file_path=api.contourOnSource_file_path(
                PRJ_ROOT, project_name, page_name, device)
            contourOnSubject_file_path=api.contourOnSubject_file_path(
                PRJ_ROOT, project_name, page_name, device)
            diff_file_path=api.diff_file_path(
                PRJ_ROOT, project_name, page_name, device)

            if(os.path.isfile(source_file_path)):
                image['source']=api.source_file_path(
                    PRJ_ROOT, project_name, project_name, device, True)
            if(os.path.isfile(screenshot_file_path)):
                image['screenshot']=api.screenshot_file_path(
                    PRJ_ROOT, project_name, page_name, device, True)

            if(os.path.isfile(contourOnSource_file_path)):
                image['output']['contourOnSource']=api.contourOnSource_file_path(
                    PRJ_ROOT, project_name, page_name, device, True)
            if(os.path.isfile(contourOnSubject_file_path)):
                image['output']['contourOnSubject']=api.contourOnSubject_file_path(
                    PRJ_ROOT, project_name, page_name, device, True)
            if(os.path.isfile(diff_file_path)):
                image['output']['diff']=api.diff_file_path(
                    PRJ_ROOT, project_name, page_name, device, True)

            testcase['images'].append(image)
        testcases.append(testcase)
    response_data['testcases']=testcases
    return api.create_json_response("success", 0, data=response_data)


# @app.route("/upload/<project_name>", methods=['POST'])
# def upload(project_name):
#     request_data = json.loads(request.data)
#     file_path = PRJ_ROOT + project_name + '/input/' +
#         request_data['type'] + '/' + request_data['pageName']


if __name__ == '__main__':
    app.run(debug=True)
