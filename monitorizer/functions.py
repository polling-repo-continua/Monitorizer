from arguments import *
import subprocess
import platform
import signal
import json
import sys
import os


def osrun(cmd):
	try:
		subprocess.check_call(cmd,stdout=open(os.devnull, 'a+'),stderr=subprocess.STDOUT,shell=True)
	except:
		pass

def first_run():
	if platform.architecture()[0].lower() != '64bit':
		print("You need 64bit Linux system to run this tool")
		sys.exit()

	for dir_name in ['reports','temp']:
		if not os.path.isdir(dir_name):
			os.mkdir(dir_name)

	chmod_tools = ['./ext/amass/amass','./ext/subfinder/subfinder']
	for tool in chmod_tools:
		os.chmod(tool, 777)

def run_and_return_output(cmd,output):
	osrun(cmd)
	return parse( output )
	
def read_config(config_file):
	jconfig = json.loads(open(config_file,'r').read().strip())
	return jconfig

def parse(filepath):
	if not os.path.isfile(filepath): yield ''

	data = open(filepath,'r').readlines()
	if 'amass' in filepath:
		for line in data:
			domain = line.split()[-1].strip()
			if domain: yield domain

	elif 'dnscan' in filepath:
		for line in data:
			if '-' in line:
				domain = line.split()[-1].strip()
				if domain: yield domain

	elif 'subfinder' in filepath:
		for line in data:
			if line[0] != '.':
				yield line.strip()
	elif 'dnsrecon' in filepath:
		for line in data:
			if not 'Name' in line:
				yield line.split(",")[1]

	else:
		for line in data:
			if line.strip():
				yield line.strip()

def signal_handler(sig, frame):
        print('Bye!')
        os._exit(1)

signal.signal(signal.SIGINT, signal_handler)