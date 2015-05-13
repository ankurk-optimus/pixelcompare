import os, sys
import json
import datetime
import getpass
import traceback
from termcolor import colored

def print_usage():
	print "Usage: python init.py <config-file-path> <devices-file-path>"
	
def readInputFile(file_name):
	json_data = open(file_name).read()
	data = json.loads(json_data)
	return data

if __name__=="__main__":
	
	config = None
	devices = None
	
	# Check if we have sufficient number of arguments.
	if len(sys.argv) < 2:
		print "Error: Argument list is less than expected."
		print_usage()
		exit()
	
	# Read config files.
	try:
		config = readInputFile(sys.argv[1]) # The 0th item is the file name itself.
		devices = readInputFile(sys.argv[2])
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
		
	# Check for missing input project folders.
	try:
		for subject in config['subject']:
			devicesKeys = dict(devices).keys()
			for deviceType in subject['devices']:
				if deviceType in devicesKeys:
					fileName = devices[deviceType]['name'] + ".png"
					resolution = str(devices[deviceType]['width']) + "x" + str(devices[deviceType]['width'])
					url = subject['pageUrl']
					if os.path.isfile(config['projectName'] + "/input/source/" + subject['pageName'] + "/" + fileName):
						print colored("Exists: " + subject['pageName'] + "/" + fileName + ".", "green")
					else:
						print colored("Not Exists: " + subject['pageName'] + "/" + fileName  + ".", "red")
						print colored("\t Name: " + subject['pageName'],"magenta")
						print colored("\t Resolution: " + resolution,"magenta")
						print colored("\t Url: " + subject['pageUrl'],"magenta")
						
				else:
					print deviceType  + " not found in valid Devices list. Please check your devices.json file."	
	except Exception:
		print "Error: Something bad happened!"
		traceback.print_exc()
		exit()
	
	
	
	
	
