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
import os
from dialog import Dialog
########################################################################
# create the root dialog object
root=Dialog()
########################################################################
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
	# the content of the log cleanup script
	if userChoice[1] != 'never':
		# build the content of the cron file, remove all files but leave directories
		# intact in order to pervent breaking everything 
		cleanupCron = ('@'+userChoice[1]+'    root    find /var/log/ -type f -delete')
	else:
		# the user picked never so make the cron file blank
		cleanupCron = ''
	# write the file to the system
	fileObject=open(path,'w')
	fileObject.write(cleanupCron)
	fileObject.close()
	if userChoice[1] == 'never':
		root.msgbox('Logs will never be cleared.')
	else:
		root.msgbox('Logs will be cleared '+userChoice[1]+'.')
