# moodle

Automated login to moodle using Selenium


Preffered OS:

	LINUX


pre-requesties:

      Firefox web browser
      then run the following commands in your terminal(only in case if gico driver is not found in path):
      	- wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz
  	- mkdir geckodriver
  	- tar -xzf geckodriver-v0.24.0-linux64.tar.gz -C geckodriver
  	- export PATH=$PATH:$PWD/geckodriver
	
Usage:

      pull this git repo and run : 
      _> pip install -r requirements.txt //only for first usage
      _> python moodle.py
      to remove saved user name from credentials file just run  _> python moodle.py -r
      
