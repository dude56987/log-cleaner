#! /usr/bin/python3
########################################################################
# Clear all logs on a Linux system immediately
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
from os import system
from sys import argv
########################################################################
def runCmd(command):
	'''
	Print and run a command.
	'''
	print(command)
	system(command)
########################################################################
goAhead=False
verbose=False
# check for the help flag
if '--help' in argv or '-h' in argv:
	print('HELP')
	print('--help or -h')
	print('    Display this help menu.')
	print('-y or --yes')
	print('    Skip confirmation and clear all logs without asking.')
	print('-v or --verbose')
	print('    Display what is happening to each file individually.')
	exit()
elif '-y' in argv or '--yes' in argv:
	# skip asking the user and just clear the logs
	goAhead=True
if '--verbose' in argv or '-v' in argv:
	verbose=True
# if no confirmation was given by the user ask with curses GUI
if goAhead == False:
	# import dialog to build the curses interface with
	from dialog import Dialog
	# set curses interface flag 
	curses=True
	# create the root dialog object
	root=Dialog()
	# display a yes/no dialog box
	output = root.yesno('Would you like to delete all system logs?')
	# output will be 'cancel' or 'ok'
	if output == 'ok':
		goAhead=True
# check if the system logs have the go ahead to be deleted
if goAhead == True:
	# check for verbose output
	if verbose:
		printFileName = ' -print '
		printShredProgress = 'v'
	else:
		printFileName = ''
		printShredProgress = ''
	# remove all compressed rotated logs
	print('#'*80)
	print('Removing rotated logs...')
	# - Delete compressed rotated logs since they are inactive and will not cause any
	#   problems when missing AFAIK
	# - Compressed files are deleted first to make less files for the next command to work
	#   with
	runCmd("find /var/log/ -name '*.gz' "+printFileName+" -type f -exec shred -uz"+printShredProgress+" {} \;")
	# overwrite all existing log files with blank files
	print('#'*80)
	print('Clearing out logs...')
	# shred the files before zeroing them out
	runCmd("find /var/log/ -type f "+printFileName+" -exec shred -z"+printShredProgress+" {} \;")
	# - zero out all files, leaving the file paths intact but removing data makes
	#   programs break less since some software can not handle logs files being
	#   removed completely
	# - leave directories intact in order to pervent breaking everything 
	runCmd('''find /var/log/ -type f -exec bash -c 'echo "" > {} ' \;''')
	print('#'*80)
	print('Log cleanup complete!')
else:
	print('#'*80)
	print('System logs were not cleared.')
