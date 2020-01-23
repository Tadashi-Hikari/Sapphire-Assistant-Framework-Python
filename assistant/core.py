* Functions
** post_office()
*** This is the central routing function for core.py. It reads the message from or to, and determines the next place to send the payload. It also logs the prior from/payload in the message chain
** load_config
*** Loads the configuration file
** log()
*** Logs data in it's appropriate location
**** Needs to be more flexible than it currently is
** edit_utterances()
*** This plugs into a spreadsheet program (or anything that can read csv files, for editing the data
* Config File
** Style
*** Ini
** Options
*** Default
**** Components to run on startup
**** Internal variables? <- component locations
**** cascade files
**** Server port = 9999
**** Command = how to run a command from the command line
**** Parser = which parser to use
**** Sphinx = Which STT to use (change to STT, not Sphinx)
**** Database = Which database to use
**** Home = Users home directory (check env-var first)
**** Links to other conf/rc files
*** post-office
**** This category defines the redirects, and custom message data
** Comments
*** Uses # for comments
