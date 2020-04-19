from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from huepy import *
import re
import argparse
import os


parser = argparse.ArgumentParser()
parser.add_argument('-u', help = "Kebros Username", dest = 'username', default ='-1')
parser.add_argument('-p', help = "Kebros Password" , dest = 'password', default = '-1')
parser.add_argument('-c', help = "Course code" , dest = 'course' , default = '-1')
parser.add_argument('-f', help = "Name of file you wanna upload", dest = 'file' , default ='-1')
parser.add_argument('-r', help = "Remove any saved username", dest = 'do_truncate', action = 'store_true')

args = parser.parse_args() 
username = args.username
password = args.password
course = args.course
do_truncate = args.do_truncate

def loggedin():
	print 'logedin'
	print browser.find_element_by_xpath('/html').text

def login(user,key):
	
	browser.find_element_by_id('username').send_keys(user)
	browser.find_element_by_id('password').send_keys(key)

	html_source = browser.find_element_by_id('login').text
	search = re.search('(Please) (\D*) (\d*) ([+ , -]) (\d+)',html_source)
	print len(search.group(2))
	if search.group(4) == '+':
		captcha = int(search.group(3)) + int(search.group(5))
	elif search.group(4) == '-':
		captcha = int(search.group(3)) - int(search.group(5))
	elif len(search.group(2)) == 17:
		captcha = int(search.group(3))
	else:
		captcha = int(search.group(5))
	browser.find_element_by_id('valuepkg3').clear()
	browser.find_element_by_id('valuepkg3').send_keys(captcha)
	browser.find_element_by_id('valuepkg3').submit()
	loggedin()

def store(username):
	valid_user = re.search('(\w\w\d{7})',username)
	if valid_user == None:
		print bad("Invalid username")
		exit()

	file = open('credentials.txt','w')
	file.truncate()
	file.write(username)
	file.close()

def readfile():
	file = open('credentials.txt','r')
	username = file.read().rstrip()
	file.close()
	return username

def delete():
	file = open('credentials.txt','w')
	file.truncate()
	file.close()

if do_truncate:
	delete()
	exit()

if username == '-1':
	if os.path.isfile('credentials.txt') and readfile() is not '':
		username = readfile()
	else:
		username = raw_input('enter your kebros username: ')
		store(username)
else:
	store(username)

if password == '-1':
	password = raw_input('enter your kebros password for ' + username + ' : ')


try:
	browser = webdriver.Firefox()
	browser.get('https://moodle.iitd.ac.in/login/index.php')
	browser.accept_untrusted_certs = True
	login(username,password)
except Exception as exp:
	print "\n" + bad(str(exp))
	

	

