HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'

def log(color, msg):
	print color + msg + ENDC

def log_fail(msg):
	log(FAIL, msg)

def log_ok(msg):
	log(OKGREEN, msg)

def log_progress(msg):
	log(OKBLUE, msg)