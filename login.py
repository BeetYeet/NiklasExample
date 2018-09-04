import login_core as core
import database_hook as dbh
import string

helpfile = 'help.txt'
helptext = open(helpfile).read()
logged_in = False
username = ''
stop = False

'''
privs are as follows:
-1 : failed to log in, can only try to log in
0  : administrated account, ie: cant do anything except be logged in
1-8: can run any command that requires n privilage or less
9  : admin rights, ie: can do anything
'''
user_privilage = -1


def try_login():

	user = input ('Please enter your username: ')
	passphrase = input ('Please enter your passphrase: ')
	response = try_login_as(user, passphrase)

def try_login_as(user, passwd):

	global username
	global logged_in
	global user_privilage

	response = core.verify_passphrase(user, passwd)
	
	success = response['success']
	if(success):
		logged_in = True
		username = user
		user_privilage = response['privilage']
		print ('\nWelcome ' + username + '!')
		print ('You have privilage ' + str(user_privilage))
	return response

def try_register():
	user = input ('Please enter your desired username: ')
	passphrase = input ('Please enter your desired passphrase: ')
	priv = input ('Please enter your desired privilage: ')
	try_register_as(user, passphrase, priv)

def try_register_automatic():
	user = input ('Please enter your desired username: ')
	passphrase = input ('Please enter your desired passphrase: ')
	priv = input ('Please enter your desired privilage: ')
	try_register_as(user, passphrase, priv)
	try_login_as(user, passphrase)

def try_register_as_automatic(user, passphrase, priv):
	try_register_as(user, passphrase, priv)
	try_login_as(user, passphrase)

def try_register_as(user, passwd, priv):
	num_priv = int(priv)
	if(num_priv < 0):
		print('you can\'t register a user with privilage under 0')
		return
	else:
		if(num_priv > user_privilage):
			print('you\'re not allowed to register a user above privilage ' + user_privilage)
			return
	core.register_user(user, passwd, num_priv)

def display_help_prompt():
	print ('Type help to list avalible commands')

def display_help_page():
	print (helptext)

def list_users():
	users = dbh.get_user_list()

	print('Users:\n\n')
	for i in range(len(users)):
		u = users[i]
		print('\t' + u['username'] + '\n\t  Privilage: ' + str(u['privilage']) + '\n')

'''
errorcodes for function display_wrong_command():
0 - no such command
1 - invalid parameters
2 - insufficient permissions
'''
def display_wrong_command(errorcode):
	if (errorcode == 0):
		print ('no such command\nmake sure you spelled it correctly and\ndidn\'t capitalize the command')
	if (errorcode == 1):
		print ('invalid arguments\nmake sure the command takes those arguments and\nthat you passed them in the right order')

def proccess_input():
	global stop
	global user_privilage
	global username
	global logged_in
	fail_on_exit = True

	response = ''

	
	response = input ('<#> ')
	
	if (len(response) < 3 ):
		print('inproper command!')
		return

	proccessed = response.split(' ')
	n = len(proccessed)
	if (n > 0):
		# all following if statements check if proccessed[0] fits said command,
		# and since a string cant be two diffrent strings we dont need to do a long if else thing
		if(proccessed[0] == 'login'):
			fail_on_exit = False
			if(logged_in):
				print('you are already logged in\ntype "logout" to logout')
				return
			else:
				if (n == 1):
					try_login()
				else:
					if (n == 3):
						try_login_as(proccessed[1], proccessed[2])
					else:
						# trigger inproper command with errorcode for "wrong arguments"
						display_wrong_command(1)
		if (logged_in and proccessed[0] == 'logout'):
			print('Goodbye ' + username + '!')
			username = ''
			user_privilage = -1
			logged_in = False
			fail_on_exit = False
		if(proccessed[0] == 'register'):
			fail_on_exit = False
			if(not logged_in):
				print('you are not logged in\ntype "login" to login')
				return
			else:
				if(user_privilage < 2):
					display_wrong_command(2)
				else:
					if (n == 1):
						try_register()
					else:
						if (n == 4):
							try_register_as(proccessed[1], proccessed[2], proccessed[3])
						else:
							if (n == 5 and proccessed[4] == '-a'):
								try_register_as_automatic(proccessed[1], proccessed[2], proccessed[3])
							else:
								if (n == 2 and proccessed[1] == '-a'):
									try_register_automatic()
								else:
									# trigger inproper command with errorcode for "wrong arguments"
									display_wrong_command(1)
		if (proccessed[0] == 'exit'):
			stop = True
			print('Goodbye!')
			fail_on_exit = False
		if (proccessed[0] == 'list'):
			list_users()
			fail_on_exit = False
		if (proccessed[0] == 'help'):
			display_help_page()
			fail_on_exit = False
		if (proccessed[0] == 'run'):
			print ('Yet to be inplemented')
			fail_on_exit = False
		if (proccessed[0] == 'whoami'):
			if (user_privilage == -1 or not logged_in):
				print ('You are not logged in')	
			else:
				if (user_privilage == 9):
					print ('You are root\nas ' + username)
				else:
					print ('You are ' +  username + '\nwith privilage ' + str(user_privilage))
			fail_on_exit = False
	if(fail_on_exit):
		# no known command was used
		# trigger inproper command with errorcode for "no such command"
		display_wrong_command(0)


display_help_prompt()
while (stop == False):
	proccess_input()