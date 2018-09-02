import json
import string

user_db_file = 'Database/user_database.json'

user_db = json.loads(open(user_db_file).read())

def test():
	print('Database Hook Tested Successfully')

def get_hash_for(username):
	for i in range(len(user_db)):
		if(user_db[i]['username'] == username):
			return user_db[i]['password_hash']

def get_perms_for(username):
	for i in range(len(user_db)):
		if(user_db[i]['username'] == username):
			return user_db[i]['privelage']