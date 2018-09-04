import json
import string

user_db_file = 'Database/user_database.json'

user_db = None

def get_user_list():
	users_simple = []
	for i in range(len(user_db)):
		u = user_db[i]
		users_simple.append({'username': u['username'], 'privilage': u['privilage']})
	return users_simple

def load_databases():
	global user_db
	user_db = json.loads(open(user_db_file).read())

def get_hash_for(username):
	for i in range(len(user_db)):
		if(user_db[i]['username'] == username):
			return user_db[i]['password_hash']

def get_salt_for(username):
	for i in range(len(user_db)):
		if(user_db[i]['username'] == username):
			return user_db[i]['salt']

def get_perms_for(username):
	for i in range(len(user_db)):
		if(user_db[i]['username'] == username):
			return user_db[i]['privilage']

def register_user(username, passwordhash, salt, privilage):
	with open(user_db_file, 'r+') as f:
		# make sure to use the "data" var instead of the "user_db" var since the database could have changed
		data = json.load(f)
		data.append({'username': username, 'password_hash': passwordhash, 'salt': salt, 'privilage': privilage})
		f.seek(0) # <--- should reset file position to the beginning.
		json.dump(data, f, indent=4)
		f.truncate() # remove remaining part
	print ('created user "' + username + '"')
	load_databases()


load_databases()