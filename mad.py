import argparse
import sys, os
from os import path
import imp
from multiprocessing import Process
import readline
import time
import threading
import signal

from core.database import essential

variables = {}

vars_store = {}

notifications = []
current = ''
processes = []

def print_banner():
	banner = """\n\n
####################################################
####################################################
###### 888b     d888        d8888 8888888b. ########
###### 8888b   d8888       d88888 888  "Y88b #######
###### 88888b.d88888      d88P888 888    888 #######
###### 888Y88888P888     d88P 888 888    888 #######
###### 888 Y888P 888    d88P  888 888    888 #######
###### 888  Y8P  888   d88P   888 888    888 #######
###### 888   "   888  d8888888888 888  .d88P #######
###### 888       888 d88P     888 8888888P" ########
####################################################
########  Promethean Information Security  #########
####################################################
##          Welcome to MAD Active Defense         ##
##             Type 'help' to begin               ##
####################################################\n
"""
	print banner
	return


def print_help():
	print "# Available commands"
	print "#  1) help"
	print "#     A) help <module>"
	print "#     B) help <command>"
	print "#  2) list"
	print "#     A) list modules"
	print "#     B) list variables"
	print "#     C) list commands"
	print "#     D) list jobs"
	print "#  3) module"
	print "#     A) module <module>"
	print "#  4) set"
	print "#     A) set <variable> <value>"
	print "#  5) home"
	print "#  6) query"
	print "#     A) query <sqlite query>"
	print "#  99) exit"

def list_modules():
	print "Available modules"
	
	for root, dirnames, filenames in os.walk("modules"):
		for filename in filenames:
			path = root + "/"
			path = path.split("modules/")[1]
			if not "pyc" in filename and is_module("modules/"+path+filename):
				print "   " + path + filename

def is_module(path_to):
	fi = open(path_to, "rb")
	data = fi.read()
	fi.close()

	if "variables" in data and 'meta' in data and "class commands" in data and "info" in data and "author" in data and "ported_by" in data and 'version' in data:
		return True
	else:
		return False
	
def output_modules():
	modules = []
	for root, dirnames, filenames in os.walk("modules"):
		for filename in filenames:
			path = root + "/"
			path = path.split("modules/")[1]
			if is_module("modules/" + path + filename):
				modules.append(path + filename)
	return modules


def load_module(selection, prev):
	
	if os.path.isfile("modules/"+ selection) and "pyc" not in selection and ".." not in selection and is_module("modules/" + selection):
			return selection
	return prev

def set_var(variable, value, module, required="no", description="Empty"):
	if module != "MAD":
		for key in variables:
			if variable == key:
				if len(variables[variable]) == 3:
					variables[variable][0] = value
				else:
					variables[variable] = [value, required, description]
				return
	elif module == "MAD":
		if variable in variables and len(variables[variable]) == 3:
			variables[variable][0] = value
		else:
			variables[variable] = [value, required, description]
		return
	
	if variable in vars_store and len(vars_store[variable]) == 3:
		vars_store[variable][0] = value
	else:
		vars_store[variable] = [value, required, description]
	
	return
	

def more_variable(v):
	try:
		print v
		print "--------------------"
		print "Value: ", variables[v][0]
		print "Required: ", variables[v][1]
		print "Description: ", variables[v][2]
		print "--------------------"
	except:
		print "invalid variable name"
	return

def signal_handler(signal, frame):
	print "Exiting..."
	sys.exit(0)

def list_variables():
	TOO_LONG = False
	LONG_ERR = "too long, to view type 'more <variable>'"
	name = 5
	value = 6
	required = 9
	desc = 0
	for v in variables:
		if len(variables[v]) == 3:
			if len(v) > name:
				name = len(v)
			if len(variables[v][0]) > value:
				value = len(variables[v][0])
			if len(variables[v][2]) > desc:
				desc = len(variables[v][2])

	if desc > 50:
		TOO_LONG = True
		desc = len(LONG_ERR)
	total = 3 + name + value + required + desc

	print "Variables"
        sys.stdout.write("Name")
	for i in range(name - 3):
		sys.stdout.write(" ")
        sys.stdout.write("Value")
	for i in range(value - 4):
		sys.stdout.write(" ")
        sys.stdout.write("Required")
	sys.stdout.write("  ")
        sys.stdout.write("Description\n")
        for i in range(total):
		sys.stdout.write("-")
	print

	for variable in variables:
		if len(variables[variable]) == 3:
			sys.stdout.write(variable)
			for i in range(name - len(variable) + 1):
				sys.stdout.write(" ")
			sys.stdout.write(variables[variable][0])
			for i in range(value - len(variables[variable][0]) + 1):
				sys.stdout.write(" ")
			sys.stdout.write(variables[variable][1])
			for i in range(required - len(variables[variable][1]) + 1):
				sys.stdout.write(" ")
			if not len(variables[variable][2]) > 50:
				print variables[variable][2]
			else:
				print LONG_ERR
		elif len(variables[variable]) == 1:
			print variable, variables[variable]
		else:
			print "variable %s is corrupt" % (variable)
	for i in range(total):
		sys.stdout.write("-")
	print

def mash_dictionaries(current):
	global variables
	global vars_store

	vars_store.update(variables)
	
	variables.update(vars_store)
	
	del_list = []
	temp = current.variables.copy()
	temp.update(variables)
	for key in temp:
		if key not in current.variables:
			del_list.append(key)
	for key in del_list:
		del temp[key]

	variables = temp

def list_commands(current):
	for command in dir(current.commands):
		if not "__" in command:
			print command
			if command == "run":
				print "run -j (run in background)"

def com_exec(method, current, debug=False):
	to_e = getattr(current.commands, method)
	if required_set(variables):
		if debug:
			return to_e(current.commands, variables)
		else:
			try:
				return to_e(current.commands, variables)
			except:
				print "Exiting module..."
				return None
	else:
		return "required variables not set"

def com_exec_background(method, current):
	to_e = getattr(current.commands, method)
	if required_set(variables):
		p = Process(target=to_e, args=(current.commands, variables,))
		p.daemon = True
		p.start()
		processes.append(p)
		return True
	else:
		return "required variables not set"	

def required_set(variables):
	for variable in variables:
		if variables[variable][1] == "yes":
			if len(variables[variable][0]) <= 0:
				return False
	return True

def list_jobs(current):
	print "Threads \n--------------------"
	try: 
		for thread in current.threads:
			print thread
	except:
		print "no current threads"
	
	print "Processes \n--------------------"
	try:
		if len(processes) > 0:
			for process in processes:
				print type(process)
		else:
			print "no current processes"
	except:
		print "no current processes"
	return

def help_module(module):
	try:
		help_me = imp.load_source("*","modules/%s" % (module))
	except:
		return False
	
	
	try:
		minfo = help_me.meta['info']
	except:
		print "No help data for module"
		return True

	try:
		mauthor = help_me.meta['author']
		mported_by = help_me.meta['ported_by']
		mversion = help_me.meta['version']
	except:
		print "module is missing some meta elements"
		mauthor = "Blank"
		mversion = "Blank"
		mported_by = "Blank"

	print module
	print 'Author: ', mauthor
	print 'Ported by: ', mported_by
	print 'version: ', mversion
	print "-----------------------------------"
	print minfo
	print "-----------------------------------"
	return True

def help_command(command):
	help_texts = {
			'help':'Lists general help',
			'help <module>':'Help for module',
			'help <command>':'Help for command',
			'list modules':'List available modules',
			'list variables':'List current variables',
			'list commands':'List module specific commands',
			'list jobs':'List currently spawned threads and processes',
			'module':'Load a module by name',
			'set':'Set a variable to a value',
			'home':'Unload all modules',		
			'exit':'Exit MAD'}

	if command in help_texts:
		print help_texts[command]
		return True
	print "No such module or command"
	return False

#I want a more powerful alias system to handle simple typos
#Also, autocomplete.. but that's different.
def alias(command):
	aliases = {
			'use':'module',
			'dir':'list variables',
			'ls':'list variables',
			'load':'module',
			'unload':'home',
			'show options':'list variables',
			'list options':'list variables',
			'show':'list',
			'quit':'exit',
			'run j':'run -j',
			':q':'exit',
			':q!':'exit',
			'q':'exit',
			'exit()':'exit',
			'q!':'exit',
			'exot':'exit'
		}
	if command.strip() in aliases:
		return aliases[command.strip()]
	if len(command.split()) > 1:
		temp = []
		for word in command.split():
			if word in aliases:
				temp.append(aliases[word])
			else:
				temp.append(word)
		return " ".join(temp)
	return command

#I need to make this hierarchical
def complete(text, state):
	#options = [f for f in output_modules() if f.startswith(text)]
	com_buffer = readline.get_line_buffer()
	
	loaders = ["module ","load ","use ", "help "]
	coms = ['read','unload ','home ','show ','list ','quit','exit','run ','set ']
	seconds = ['notifications','options','variables','commands','modules']
	
	loader = False
	first = False
	for com in coms:
		if com in com_buffer:
			first = True
	for l in loaders:
		if l in com_buffer:
			loader = True
	
	if first:
		options = [f for f in seconds if f.startswith(text)]
	elif loader:
		options = [f for f in output_modules() if f.startswith(text)]
	else:
		options = [f for f in coms if f.startswith(text)] + [f for f in loaders if f.startswith(text)]
	
	
	if state < len(options):
		return options[state]
	else:
		return None
def initialize():
	#Init log file if not there.
	#Otherwise update it
	os.system("touch logs/notify.log")
	
	return
	
def load_log_unread(log):
	fi = open("logs/"+log,'r')
	data = fi.read()
	fi.close()

	temp = data.split("\n")
	data = []
	for line in temp:
		if len(line) > 0 and line[0] != "#":
			data.append(line)
	return data

def mark_log_read(log, line):
	line = line.replace("/","\/")
	os.system("sed -i 's/%s/#%s/' logs/%s" % (line, line, log))
	return

def read_old():
	fi = open("logs/notify.log",'r')
	data = fi.read().split("\n")
	for line in data:
		print line

#add thread safe locking once everything is finalized
def read_notifications():
	global notifications

	temp = notifications
	notifications = []
	if len(temp) > 0:
		for line in temp:
			print line
			mark_log_read("notify.log",line)
	return

def log_notification(msg):
	fi = open("logs/notify.log", "a")
	fi.write(datetime.datetime.now()+":"+msg)
	fi.close()

#Thread safe locking once finalized
def mon_log(log):
	global notifications
	while True:
		bef = len(notifications)
		notifications = load_log_unread(log)
		if bef != len(notifications):
			if (len(notifications) - bef) != 1:
				s = "s"
			else:
				s = ""
			print "\nYou have received %s new notification%s" % (len(notifications) - bef, s)
			print "%s total unread notifications" % (len(notifications))
			sys.stdout.write( "command is: read notifications\n%s>>> %s" % (module, readline.get_line_buffer()) )
			sys.stdout.flush()		

		time.sleep(120)
			
	

def parse_com(com, module, current):
	
	#help
	if com.strip().lower() == "help":
		print_help()
		return module
	
	#help module || help command
	if len(com.strip().lower().split()) > 1 and com.strip().lower().split()[0] == "help":
		if not help_module(com.strip().lower().split()[1]):
			help_command(str(com.strip().lower().split()[1:]))
		return module

	#list
	if com.strip().lower() == "list":
		print "list what?"
		return module

	#list modules
	if com.strip().lower() == "list modules":
		list_modules()
		return module
	
	#list variables
	if com.strip().lower() == "list variables":
		list_variables()
		return module

	#list commands
	if com.strip().lower() == "list commands":
		if module == "MAD":
			print "no module loaded"
			return module
		else:
			list_commands(current)
			return module

	#list jobs
	if com.strip().lower() == "list jobs":
		if module == "MAD":
			return module
		else:
			list_jobs(current)
			return module

	#module
	if com.strip().lower() == "module":
		print "need to specify module"
		return module

	#module <module>
	if "module" in com.strip().lower() and len(com.strip().lower().split()) == 2:
		return load_module(com.strip().lower().split()[1], module)

	#set
	if com.strip().lower() == "set":
		print "set what?"
		return module
	
	#set <variable> <value>
	if len(com.strip().lower().split()) == 3 and com.strip().lower().split()[0] == "set":
		set_var(com.strip().lower().split()[1],com.strip().lower().split()[2], module)
		return module	
	#set <variable> <value> <required>
	if len(com.strip().lower().split()) == 4 and com.strip().lower().split()[0] == "set":
		set_var(com.strip().lower().split()[1],com.strip().lower().split()[2], module, com.strip().lower().split()[3])
		return module

	#set <variable> <value> <required> <description>
	if len(com.strip().lower().split()) > 4 and com.strip().lower().split()[0] == "set":
		set_var(com.strip().lower().split()[1],com.strip().lower().split()[2], module, com.strip().lower().split()[3], " ".join(com.strip().lower().split()[4:]))
		return module

	#home
	if com.strip().lower() == "home":
		return 'MAD'

	#exit
	if com.strip().lower() == "exit":
		exit(0)

	
	#more <variable>
	if len(com.strip().lower().split()) == 2 and com.strip().lower().split()[0] == "more":
		more_variable(com.strip().split()[1])
		return module
	
	#read notifications
	if com.strip().lower() == "read notifications":
		read_notifications()
		return module
	
	#read old
	if com.strip().lower() == "read old":
		read_old()
		return module

	#query
	if len(com.strip().lower().split()) > 1 and com.strip().lower().split()[0] == "query":
		e = essential()
		e.db_exec(com.strip().lower().split()[1])
		return module

	###parse commands
	if not isinstance(current, str):
		if len(com.strip().lower().split()) < 2:
			if com.strip().lower() in dir(current.commands):
				temp = com_exec(com.strip().lower(), current)
				print temp
				return module
		elif len(com.strip().lower().split()) == 2 and com.strip().lower().split()[1] == "-j":
			print 0.1
			if com.strip().lower().split()[0] in dir(current.commands):
				temp = com_exec_background(com.strip().lower().split()[0], current)
				print temp
				return module
		elif len(com.strip().lower().split()) == 2 and com.strip().lower().split()[1] == '-d':
			print "Running in debug mode"
			if com.strip().lower().split()[0] in dir(current.commands):
				temp = com_exec(com.strip().lower().split()[0], current, True)
				print temp
				return module

	return module


def read_loop(filename=""):
	global module
	global module_history
	global current
	
	if len(filename) > 0:
		fi = open(filename, "r")
		data = fi.read()
		fi.close()
		commands = data.split("\n")
		
		for command in commands:
			if module != module_history[-1]:
				module_history.append(module)
			module = parse_com(alias(str(command)),module,current)
			if module != module_history[-1] and module != "MAD":
				current = imp.load_source('*','modules/%s' % (module))
				mash_dictionaries(current)
		
	
	
	while True:
		if module != module_history[-1]:
			module_history.append(module)
		module = parse_com(alias(str(raw_input("%s>>> " % (module)))), module, current)
		if module != module_history[-1] and module != "MAD":
			current = imp.load_source('*','modules/%s' % (module))
			mash_dictionaries(current) 

if __name__ == "__main__":
	initialize()
	
	parser = argparse.ArgumentParser()
	parser.add_argument("-s","--script", help="A script file to run")
	args = parser.parse_args()
	
	t = threading.Thread(target=mon_log, args=("notify.log",))
	t.daemon = True
	t.start()

	readline.parse_and_bind("tab: complete")
	readline.set_completer(complete)	
	readline.set_completer_delims(" ")

	module = 'MAD'
	module_history = ["MAD"]
	print_banner()
	if args.script:
		read_loop(args.script)
	else:
		read_loop()
