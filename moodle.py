from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from huepy import * #refer to this https://github.com/s0md3v/huepy
import re
import argparse
import os
import time
import getpass


parser = argparse.ArgumentParser()
parser.add_argument('-u', help = "Kebros Username", dest = 'username', default ='-1')
parser.add_argument('-p', help = "Kebros Password" , dest = 'password', default = '-1')
parser.add_argument('-c', help = "Course code" , dest = 'course' , default = '-1')
parser.add_argument('-r', help = "Remove any saved username", dest = 'do_truncate', action = 'store_true')

args = parser.parse_args() 
username = args.username
password = args.password
course = args.course
do_truncate = args.do_truncate

course_dict = {'NEN100' : '8501', 'NIN100' : '8489', 'NLN100' : '8319' , 'MTL101' : '8291', 'MCP101' : '8209',
				'MCP100' : '8208', 'CMP100' : '7800', 'CML100' : '7778', 'PYP100' : '9281', 'PYL100' : '9238',
				'NLN101' : '9218', 'NEN101' : '9217', 'MTL100' : '9188', 'ELL100' : '8890', 'COL100' : '8693'

}

def open_courses():
	print(good('opening ' + course ))
	if course.upper() in course_dict:
		browser.get('https://moodle.iitd.ac.in/course/view.php?id='+course_dict[course.upper()])
	else:
		print('Course link could not be found')
	exit()

def loggedin(): #When you are logged in 
	delay = 10 # seconds
	try:
	    myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'page-my-index')))
	    os.system('clear')
	    print(good(green('Successfully logged in as ' + username)))
	    if course != '-1':
	    	open_courses()

	except TimeoutException:
		print(bad(red('Check your Internet conection, Loading took too much time!')))
		exit()


def login(user,key):#automated login 
	
	browser.find_element_by_id('username').send_keys(user)
	browser.find_element_by_id('password').send_keys(key)

	html_source = browser.find_element_by_id('login').text
	search = re.search('(Please) (\D*) (\d*) ([+ , -]) (\d+)',html_source)
	
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

def store(username):#stores the username to a txt file named credentials.txt also checks validity of username before storing it.
	valid_user = re.search('(\w\w\d{7})',username)
	if valid_user == None:
		print(bad("Invalid username"))
		exit()

	file = open('credentials.txt','w')
	file.truncate()
	file.write(username)
	file.close()

def readfile():#reads the credentials.txt file
	file = open('credentials.txt','r')
	username = file.read().rstrip()
	file.close()
	return username

def delete():# delets any saved username from credentials.txt
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
		username = input('enter your kebros username: ')
		store(username)
else:
	store(username)


if password == '-1':
	password = getpass.getpass(prompt = 'enter your kebros password for ' + username + ' : ')


if course == '-1':
	course = input('Enter Course code like \'NLN100\' (empty to skip) : ')
	if course == '':
		course = '-1'


try:
	browser = webdriver.Firefox()
	browser.get('https://moodle.iitd.ac.in/login/index.php')
	browser.accept_untrusted_certs = True
	login(username,password)
except Exception as exp:
	print("\n" + bad(str(exp)))
