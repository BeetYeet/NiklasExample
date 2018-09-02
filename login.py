import login_core as core
import database_hook as dbh
import string

descriptive = False
logged_in = False
username = ''
stop = False

'''
privs are as follows:
-1 : failed to log in, can only try to log in
0  : administrated account, ie: cant do anything except be logged in
1-8: can run any app that has n privelige or less
9  : admin rights, ie: can do anything
'''
privilage_level = -1


def accept_passphrase():

	global username
	global descriptive
	global logged_in
	global privilage_level

	if (descriptive): 
		print ('accept_passphrase')
	new_username = input ('Please enter your username: ')
	new_passphrase = input ('Please enter your passphrase: ')
	response = core.verify_passphrase(new_username, new_passphrase)
	
	success = response['success']
	if(success):
		logged_in = True
		username = new_username
		privilage_level = response['privelige']
		print ('\nWelcome ' + username + '!')
		print ('You have privelige ' + str(privilage_level))

def proccess_input():
	global proper_command
	global descriptive
	global stop
	global privilage_level

	proper_command = False

	while (proper_command == False):
		response = ''
		if(logged_in):
			response = input ('Type help to list avalible commands\nWhat do you want to do ' + username + '?\n <#>- ')
		else:
			response = input ('Type help to list avalible commands\nWhat do you want to do?\n <#>- ')
		
		if (len(response) < 3 ):
			print('inproper command!')
			continue

		proccessed = response.split(' ')
		n = len(proccessed)
		if (n > 0):
			if(proccessed[0] == 'login'):
				if(logged_in):
					print('You are already logged in')
				else:
					if (n > 1):
						if (proccessed[1] == '-d'):
							descriptive = True
							proper_command = True
						else:
							print ('inproper command')
							proper_command = False
					else:
						proper_command = True
					accept_passphrase()
			if (logged_in and proccessed[0] == 'logout'):
				proper_command = True
				stop = True
				print('Goodbye ' + username + '!')
			else:
				if (proccessed[0] == 'exit'):
					proper_command = True
					stop = True
					print('Goodbye!')
		else:
			print ('inproper command')
			proper_command = False

while (stop == False):
	proccess_input()