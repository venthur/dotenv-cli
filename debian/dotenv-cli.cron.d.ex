#
# Regular cron jobs for the dotenv-cli package
#
0 4	* * *	root	[ -x /usr/bin/dotenv-cli_maintenance ] && /usr/bin/dotenv-cli_maintenance
