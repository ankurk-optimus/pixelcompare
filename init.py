import os, sys
import json
import datetime
import getpass
import traceback

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
		
	# Create project folders.
	try:
		os.mkdir(config['projectName'], 0777 );
		os.mkdir(config['projectName'] + "/input" , 0777)
		os.mkdir(config['projectName'] + "/input/source" , 0777)
		os.mkdir(config['projectName'] + "/input/screenshots" , 0777)
		os.mkdir(config['projectName'] + "/output" , 0777)
		for subject in config['subject']:
			os.mkdir(config['projectName'] + "/input/source/" + subject['pageName'] , 0777)	
	except IOError:
		print "Error: Cannot create project folder."
		traceback.print_exc()
		exit()		
	except Exception:
		print "Error: Something unrecoverable happened!"
		traceback.print_exc()
		exit()
	
	
	
	
	
