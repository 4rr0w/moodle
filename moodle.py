from selenium import webdriver
from selenium.webdriver.support.ui import Select
from huepy import *
import re



def login(user,key):
	browser = webdriver.Firefox()
	browser.get('https://moodle.iitd.ac.in/login/index.php')
	browser.accept_untrusted_certs = True
	browser.find_element_by_id('username').send_keys(user)
	browser.find_element_by_id('password').send_keys(key)

	html_source = browser.find_element_by_id('login').text
	search = re.search('(Please) (\D*) (\d*) ([+ , -]) (\d+)',html_source)

	if search.group(4) == '+':
		capcha = int(search.group(3)) + int(search.group(5))
	elif search.group(4) == '-':
		capcha = int(search.group(3)) - int(search.group(5))
	elif len(search.group(2)) == 22:
		capcha = int(search.group(5))
	else:
		capcha = int(search.group(3))
	browser.find_element_by_id('valuepkg3').clear()
	browser.find_element_by_id('valuepkg3').send_keys(capcha)
	browser.find_element_by_id('valuepkg3').submit()

	


username = raw_input('enter your kebros username:')
password = raw_input('enter your kebros password:')

try:
	login(username,password)
except Exception as exp:
	print "\n" + bad(str(exp))
	

	

