import os, sys
import json
import datetime
import getpass
import traceback
import api

def print_usage():
	print "Usage: python init.py <config-file-path> <devices-file-path> <new-project-path>"

def create_project(config, devices, newprj_path):
	"""
		Create a blank project.

		Parameters:
		-----------
		@config: The config data in the form of a python dictionary.
		@devices: The devices data in the form of a python dictionary.
		@newprj_path: The path where new project is to be created.

		Returns:
		----------
		None
	"""
	try:
		os.mkdir(api.correct_path(newprj_path) + config['projectName'], 0777 );
		os.mkdir(api.correct_path(newprj_path) + config['projectName'] + "/input" , 0777)
		os.mkdir(api.correct_path(newprj_path) + config['projectName'] + "/input/source" , 0777)
		os.mkdir(api.correct_path(newprj_path) + config['projectName'] + "/input/screenshots" , 0777)
		os.mkdir(api.correct_path(newprj_path) + config['projectName'] + "/output" , 0777)
		for subject in config['subject']:
			os.mkdir(api.correct_path(newprj_path) + config['projectName'] + "/input/source/" + subject['pageName'] , 0777)

		f = open(api.correct_path(newprj_path) + config['projectName'] + '/config.json','w')
		f.write(json.dumps(config))
		f.close()

		f = open(api.correct_path(newprj_path) + config['projectName'] + '/devices.json', 'w')
		f.write(json.dumps(devices))
		f.close()
	except IOError:
		print "Error: Cannot create project folder."
		traceback.print_exc()
		return -1
	except Exception:
		print "Error: Something unrecoverable happened!"
		traceback.print_exc()
		return -1
	return 0

if __name__=="__main__":

	config = None
	devices = None
	project_path = None

	# Check if we have sufficient number of arguments.
	if len(sys.argv) < 3:
		print "Error: Argument list is less than expected."
		print_usage()
		exit()

	# Read config files.
	try:
		config = api.readInputFile(sys.argv[1]) # The 0th item is the file name itself.
		devices = api.readInputFile(sys.argv[2])
		project_path = api.correct_path(sys.argv[3])
	except IndexError:
		print "Error: Argument list is less than expected.\n"
		print_usage
		traceback.print_exc()
		exit()
	except ValueError:
		print "Error: There seems to be an error with one of the input files."
		traceback.print_exc()
		exit()
	except KeyError:
		print "Error: There seems to be an error with one of the input files."
		traceback.print_exc()
		exit()
	except IOError:
		print "Error: Cannot read the input files."
		traceback.print_exc()
		exit()
	except Exception:
		print "Error: Something unrecoverable happened!"
		traceback.print_exc()
		exit()

	# Create project folders.
	create_project(config, devices, project_path)
