#! /usr/bin/python3
########################################################################
# Manage clearing of logs on linux systems
# Copyright (C) 2016  Carl J Smith
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
########################################################################
import sys
########################################################################
# check user arguments to the CLI interface in order to skip the wizard
if '--help' in sys.argv or '-h' in sys.argv:
	print('--help')
	print('  Will display this menu')
	print('--reboot')
	print('  Set logs to be cleared on every reboot.')
	print('--hourly')
	print('  Logs will be cleared once every hour.')
	print('--daily')
	print('  Clear logs once per day.')
	print('--weekly')
	print('  Remove all logs once per week.')
	print('--monthly')
	print('  Clear logs at the end of the month.')
	print('--yearly')
	print('  Remove all logs once per year.')
	print('--never')
	print('  Never clear any logs on the system')
	print('  If you have not ran the program yet this is the default')
	print('  setting after install.')
	# exit the program after displaying help
	exit()
elif '--reboot' in sys.argv:
	userChoice=['','reboot']
	curses=False
elif '--hourly' in sys.argv:
	userChoice=['','hourly']
	curses=False
elif '--daily' in sys.argv:
	userChoice=['','daily']
	curses=False
elif '--monthly' in sys.argv:
	userChoice=['','monthly']
	curses=False
elif '--yearly' in sys.argv:
	userChoice=['','yearly']
	curses=False
elif '--never' in sys.argv or '--disable' in sys.argv:
	userChoice=['','never']
	curses=False
else:
	# import dialog to build the curses interface with
	from dialog import Dialog
	# set curses interface flag 
	curses=True
	# create the root dialog object
	root=Dialog()
	# create list of available cron choices
	choices=[]
	choices.append(('reboot','Clear on reboot',0))
	choices.append(('hourly','Clear every hour',0))
	choices.append(('daily','Clear once per day',0))
	choices.append(('weekly','Clear every week',0))
	choices.append(('monthly','Clear at end of the month',0))
	choices.append(('yearly','Clear once a year',1))
	choices.append(('never','Never clear the logs',0))
	# build the curses interface
	# returns a 2 value tuple, grab value # 1
	userChoice=root.radiolist('How often would you like system logs cleared?',20,60,15,choices)
if len(userChoice[1]) > 0:
	# build the path of this cleanup script
	path='/etc/cron.d/logCleaner'
	# build the content of the cron file
	if userChoice[1] != 'never':
		# run cleanlogs script without prompting the user
		cleanupCron = ('@'+userChoice[1]+'''    root    cleanlogs -y\n''')
	else:
		# the user picked never so make the cron file blank
		cleanupCron = ''
	# write the file to the system
	fileObject=open(path,'w')
	fileObject.write(cleanupCron)
	fileObject.close()
	# check if the curses flag is true to use curses dialog boxes
	if curses:
		# use the curses interface
		if userChoice[1] == 'never':
			root.msgbox('Logs will never be cleared.')
		else:
			root.msgbox('Logs will be cleared '+userChoice[1]+'.')
	else:
		# use the cli interface
		if userChoice[1] == 'never':
			print('Logs will never be cleared.')
		else:
			print('Logs will be cleared '+userChoice[1]+'.')
