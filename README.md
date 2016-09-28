Log-Cleaner
==============
[Curses](https://en.wikipedia.org/wiki/Ncurses) and Command line utility to manage cleanup of system logs.

###Features

* Curses wizard to setup removal of logs on a schedule using  [cron](https://en.wikipedia.org/wiki/Cron).
  * Reboot
    * Remove logs on every system reboot.
  * Hourly
    * Remove logs every hour the system is running.
  * Daily
    * Remove logs once per day.
  * Weekly
    * Remove logs every week.
  * Monthly
    * Remove logs once per month.
  * Yearly
    * Remove all logs once per year.
* Remove all logs with a single command. 
* Prevent software compatibility issues with clearing logs using rm -r /var/log/*
* Uses shred to securely remove logs.

###Usage

Type the below into a terminal in order to run the cron setup wizard.

	logcleanersetup

To immediately clean the logs run the below command.

	cleanlogs

###How it works

For reference the commands ran during log cleanup are shown below. All logs will be shredded by overwriting them a few times with random data. The first command will shred and remove all compressed rotated logs. The second will shred the the contents of the still existing logs. The third command will blank the contents of all existing logs by overwriting them with a blank file. If you run all of the below commands it would have the same effect as running "cleanlogs -y -v". The cronjob would also have the same effect but does not include verbose output.

	find /var/log/ -name '*.gz' -print -type f -exec shred -uzv {} \;
	
	find /var/log/ -type f -print -exec shred -zv {} \;

	find /var/log/ -type f -exec bash -c 'echo "" > {} ' \;

To run cleanup without using shred you would use the below commands.

	find /var/log/ -name -print '*.gz' -type f -delete

	find /var/log/ -type f -print -exec bash -c 'echo "" > {} ' \;
