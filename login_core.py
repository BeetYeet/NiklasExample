import hashlib as hsh
import database_hook as dbh

'''
returns:
* success    : true if creds were good, false otherwise
* privelige  : number in range (0-9) if creds were good, number -1 otherwise
'''
def verify_passphrase(user, passwd):
	success = False
	privelige = -1
	dbhsh = dbh.get_hash_for(user)
	if(dbhsh == None):
			print ('No such user: "' + user + '"')
	else:
		if (passwd == dbhsh):
			success = True
			privelige = dbh.get_perms_for(user)
		else:
			print ('Incorrect password for user "' + user + '"')

	return {'success':success, 'privelige': privelige}