import hashlib as hsh
import database_hook as dbh
import string
import random

salt_charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

'''
returns:
* success    : true if creds were good, false otherwise
* privelige  : number in range (0-9) if creds were good, number -1 otherwise
'''
def verify_passphrase(user, passwd):
	success = False
	privilage = -1
	dbhsh = dbh.get_hash_for(user)
	salt = dbh.get_salt_for(user)
	hashed_passwd = hash(passwd, salt)

	if(dbhsh == None):
			print ('No such user: "' + user + '"')
	else:
		if (hashed_passwd == dbhsh):
			success = True
			privilage = dbh.get_perms_for(user)
		else:
			print ('Incorrect password for user "' + user + '"')

	return {'success':success, 'privilage': privilage}

def register_user(username, passphrase, privilage):
	# crypto stuff
	salt = gen_salt()
	pass_hash = hash(passphrase, salt)
	# /crypto stuff

	dbh.register_user(username, pass_hash, salt, privilage)

def gen_salt():
	salt = ''
	for i in range(1, 6):
		salt = salt + random.choice(salt_charset)
	return salt

def hash(data, salt):
	h = hsh.sha256()
	h.update(bytes(data+salt, 'ascii'))
	return (str(h.hexdigest()))