Log-Cleaner
==============
Curses interface for setting a cron job to delete system logs.

* Remove logs at set intervals
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
* Remove all logs with a command.
* Prevent software compatibility issues with clearing logs using rm -r /var/log/*

###Usage

Type the below into a terminal in order to run the cron setup wizard.

	log-cleaner

To immediately clean the logs run the below command.

	cleanlogs

###How it works

For reference the commands ran by the cron job are below. The first command will remove all compressed rotated logs. The second will blank the contents of all existing logs by overwriting them with a blank file. If you run both of the below commands it would have the same effect as running "cleanlogs -y" or the cron job running.

	find /var/log/ -name '*.gz' -type f -delete

	find /var/log/ -type f -exec bash -c 'echo "" > {} ' \;
