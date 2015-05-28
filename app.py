from flask import Flask, make_response, send_file, session, request, redirect
import os
import json
import api.api as api
import api.prjinit as prjinit
import api.diff as diff
import shutil

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

    if os.path.isdir(PRJ_ROOT + project_name) is False:
        return api.create_json_response("failure", -1, message="Project does not exist.")

    config_data = api.readInputFile(
        api.config_file_path(PRJ_ROOT, project_name))
    devices_data = api.readInputFile(
        api.devices_file_path(PRJ_ROOT, project_name))

    response_data = {
        'projectName': config_data['projectName'],
        'testcases': None
    }
    testcases = []

    for subject in config_data['subject']:
        page_name = subject['pageName']
        page_url = subject['pageUrl']
        testcase = {
            'pageName': page_name,
            'pageUrl': page_url,
            'images': []
        }
        for device in subject['devices']:
            image = {
                'device': device,
                'source': None,
                'screenshot': None,
                'output': {
                    'contourOnSubject': None,
                    'contourOnSource': None,
                    'diff': None
                }
            }

            source_file_path = api.source_file_path(
                PRJ_ROOT, project_name, page_name, device)
            screenshot_file_path = api.screenshot_file_path(
                PRJ_ROOT, project_name, page_name, device)
            contourOnSource_file_path = api.contourOnSource_file_path(
                PRJ_ROOT, project_name, page_name, device)
            contourOnSubject_file_path = api.contourOnSubject_file_path(
                PRJ_ROOT, project_name, page_name, device)
            diff_file_path = api.diff_file_path(
                PRJ_ROOT, project_name, page_name, device)

            if(os.path.isfile(source_file_path)):
                image['source'] = api.source_file_path(
                    PRJ_ROOT, project_name, page_name, device, True)
            if(os.path.isfile(screenshot_file_path)):
                image['screenshot'] = api.screenshot_file_path(
                    PRJ_ROOT, project_name, page_name, device, True)

            if(os.path.isfile(contourOnSource_file_path)):
                image['output']['contourOnSource'] = api.contourOnSource_file_path(
                    PRJ_ROOT, project_name, page_name, device, True)
            if(os.path.isfile(contourOnSubject_file_path)):
                image['output']['contourOnSubject'] = api.contourOnSubject_file_path(
                    PRJ_ROOT, project_name, page_name, device, True)
            if(os.path.isfile(diff_file_path)):
                image['output']['diff'] = api.diff_file_path(
                    PRJ_ROOT, project_name, page_name, device, True)

            testcase['images'].append(image)
        testcases.append(testcase)
    response_data['testcases'] = testcases
    return api.create_json_response("success", 0, data=response_data)


@app.route("/upload/<project_name>", methods=['POST'])
def upload(project_name):
    if os.path.isdir(PRJ_ROOT + project_name) is False:
        return api.create_json_response("failure", -1, message="Project does not exist.")

    img_type = request.form.get('type')
    img_page_name = request.form.get('pageName')
    img_device = request.form.get('device')
    file_path = PRJ_ROOT + project_name + '/input/' + \
        img_type + '/' + img_page_name + '/' + \
        img_device + '.png'

    uploaded_File = request.files['file']

    d = os.path.dirname(file_path)
    if not os.path.exists(d):
        os.makedirs(d)

    uploaded_File.save(file_path)
    if os.path.isfile(file_path):
        output = {
            'path': None
        }

        if img_type == 'source':
            output['path'] = api.source_file_path(
                PRJ_ROOT, project_name, img_page_name, img_device, True)
        else:
            output['path'] = api.screenshot_file_path(
                PRJ_ROOT, project_name, img_page_name, img_device, True)

        return api.create_json_response("success", 0, data=output)
    else:
        return api.create_json_response("failure", -1, message="File cannot be uploaded.")


@app.route("/compare/<project_name>/<page_name>/<device>", methods=['GET'])
def compare(project_name, page_name, device):
    if os.path.isdir(PRJ_ROOT + project_name) is False:
        return api.create_json_response("failure", -1, message="Project does not exist.")
    elif os.path.isfile(api.source_file_path(PRJ_ROOT, project_name, page_name, device)) is False:
        return api.create_json_response("failure", -1, message="Source image does not exist")
    elif os.path.isfile(api.screenshot_file_path(PRJ_ROOT, project_name, page_name, device)) is False:
        return api.create_json_response("failure", -1, message="Screenshot image does not exist")

    diff_img, source_img, subject_img = diff.compare(api.source_file_path(
        PRJ_ROOT, project_name, page_name, device), api.screenshot_file_path(PRJ_ROOT, project_name, page_name, device))

    diff.write(diff_img, api.diff_file_path(
        PRJ_ROOT, project_name, page_name, device))
    diff.write(source_img, api.contourOnSource_file_path(
        PRJ_ROOT, project_name, page_name, device))
    diff.write(subject_img, api.contourOnSubject_file_path(
        PRJ_ROOT, project_name, page_name, device))

    error_code = 0
    error_message = ""
    if os.path.isfile(api.diff_file_path(
            PRJ_ROOT, project_name, page_name, device)) is False:
        error_code = -1
        error_message = error_message + "Difference file could not be created."

    if os.path.isfile(api.contourOnSource_file_path(
            PRJ_ROOT, project_name, page_name, device)) is False:
        error_code = -1
        error_message = error_message + \
            "Countour on source file could not be created."

    if os.path.isfile(api.contourOnSource_file_path(
            PRJ_ROOT, project_name, page_name, device)) is False:
        error_code = -1
        error_message = error_message + \
            "Countour on subject file could not be created."

    if error_code is -1:
        return api.create_json_response("failure", -1, message=error_message)
    else:
        output = {
            'contourOnSubject': None,
            'contourOnSource': None,
            'diff': None
        }
        output['contourOnSource'] = api.contourOnSource_file_path(
            PRJ_ROOT, project_name, page_name, device, True)
        output['contourOnSubject'] = api.contourOnSubject_file_path(
            PRJ_ROOT, project_name, page_name, device, True)
        output['diff'] = api.diff_file_path(
            PRJ_ROOT, project_name, page_name, device, True)

        return api.create_json_response("success", 0, data=output)

@app.route("/add_test_case/<project_name>", methods=['POST'])
def add_test_case(project_name):
    if os.path.isdir(PRJ_ROOT + project_name) is False:
        return api.create_json_response("failure", -1, message="Project does not exist.")
    request_data = json.loads(request.data)
    config_data = api.readInputFile(api.config_file_path(PRJ_ROOT, project_name))
    new_page = {
        'pageName':request_data['pageName'],
        'pageUrl':request_data['pageUrl'],
        'devices':None
    }
    config_data['subject'].append(new_page)
    f = open(api.config_file_path(PRJ_ROOT, project_name),'w')
    f.write(json.dumps(config_data))
    f.close()
    return api.create_json_response("success", 0, message="Test case added.")

@app.route("/delete_test_case/<project_name>", methods=['POST'])
def delete_test_case(project_name):
    if os.path.isdir(PRJ_ROOT + project_name) is False:
        return api.create_json_response("failure", -1, message="Project does not exist.")
    request_data = json.loads(request.data)
    page_name = request_data['pageName']
    config_data = api.readInputFile(api.config_file_path(PRJ_ROOT, project_name))
    index=0
    print page_name
    for page in config_data['subject']:
        if page['pageName'] == page_name:
            config_data['subject'].pop(index)
            print page['pageName']
            break
        index=index+1
    f = open(api.config_file_path(PRJ_ROOT, project_name),'w')
    f.write(json.dumps(config_data))
    f.close()

    source_folder_path = PRJ_ROOT + project_name + '/input/source/' + page_name
    if os.path.isdir(source_folder_path):
        shutil.rmtree(source_folder_path)

    screenshot_folder_path = PRJ_ROOT + project_name + '/input/screenshots/' + page_name
    if os.path.isdir(screenshot_folder_path):
        shutil.rmtree(screenshot_folder_path)

    output_folder_path = PRJ_ROOT + project_name + '/output/' + page_name
    if os.path.isdir(output_folder_path):
        shutil.rmtree(output_folder_path)

    return api.create_json_response("success", 0, message="Test case deleted.")

@app.route("/delete_test_device/<project_name>", methods=['POST'])
def delete_test_device(project_name):
    if os.path.isdir(PRJ_ROOT + project_name) is False:
        return api.create_json_response("failure", -1, message="Project does not exist.")
    request_data = json.loads(request.data)
    page_name = request_data['pageName']
    device_name = request_data['device']
    config_data = api.readInputFile(api.config_file_path(PRJ_ROOT, project_name))
    for page in config_data['subject']:
        if page['pageName'] == page_name:
            index = 0
            for device in page['devices']:
                if device == device_name:
                    page['devices'].pop(index)
                    break
                index = index+1
    f = open(api.config_file_path(PRJ_ROOT, project_name),'w')
    f.write(json.dumps(config_data))
    f.close()

    source_file_path = api.source_file_path(PRJ_ROOT, project_name, page_name, device_name)
    if os.path.isfile(source_file_path):
        os.remove(source_file_path)

    screenshot_file_path = api.screenshot_file_path(PRJ_ROOT, project_name, page_name, device_name)
    if os.path.isfile(screenshot_file_path):
        os.remove(screenshot_file_path)

    output_folder_path = PRJ_ROOT + project_name + '/output/' + page_name + '/' + device_name
    if os.path.isdir(output_folder_path):
        shutil.rmtree(output_folder_path)
    return api.create_json_response("success", 0, message="Test device deleted.")

@app.route("/add_valid_device/<project_name>", methods=['POST'])
def add_valid_device(project_name):
    if os.path.isdir(PRJ_ROOT + project_name) is False:
        return api.create_json_response("failure", -1, message="Project does not exist.")
    request_data = json.loads(request.data)
    new_device={
        'deviceName':request_data['newDevice'],
        'width':request_data['width'],
        'height':request_data['height']
    }
    devices_data = api.readInputFile(api.devices_file_path(PRJ_ROOT, project_name))
    devices_data[request_data['newDevice']] = new_device
    f = open(api.devices_file_path(PRJ_ROOT, project_name),'w')
    f.write(json.dumps(devices_data))
    f.close()
    return api.create_json_response("success", 0, message="Device added to valid devices list.")

@app.route("/add_test_device/<project_name>", methods=['POST'])
def add_test_device(project_name):
    if os.path.isdir(PRJ_ROOT + project_name) is False:
        return api.create_json_response("failure", -1, message="Project does not exist.")
    request_data = json.loads(request.data)
    device_to_add = request_data['device']
    page_name = request_data['pageName']
    devices_data = api.readInputFile(api.devices_file_path(PRJ_ROOT, project_name))
    if devices_data['device_to_add'] is None:
        return api.create_json_response("failure", -1, message="Not a valid device.")

    config_data = api.readInputFile(api.config_file_path(PRJ_ROOT, project_name))
    for page in config_data['subject']:
        if page['pageName'] == page_name:
            if device_to_add not in page['devices']:
                page['devices'].append(device_to_add)
                break
            else:
                return api.create_json_response("failure", -1, message="Testcase already contains this device.")
    f = open(api.config_file_path(PRJ_ROOT, project_name),'w')
    f.write(json.dumps(config_data))
    f.close()
    return api.create_json_response("success", 0, message="Device added to test case.")


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0')
