import unittest
import csv
import json
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
import pickle
import random
import datetime
import sqlite3
from random import gauss
from time import sleep as original_sleep
import logging


# initialize and setup logging system



# create a new Chrome session
browser = webdriver.Chrome()
browser.implicitly_wait(30)
browser.maximize_window()
username='parasvc18'
password= 'vandanach12'

STDEV = 0.5
sleep_percentage = 1







def scroll_bottom(browser, element, range_int):
	# put a limit to the scrolling
	if range_int > 50:
		range_int = 50

	for i in range(int(range_int / 2)):
		browser.execute_script(
			"arguments[0].scrollTop = arguments[0].scrollHeight", element)
		# update server calls

	return


def formatNumber(number):
	formattedNum = number.replace(',', '').replace('.', '')
	formattedNum = int(formattedNum.replace('k', '00').replace('m', '00000'))
	return formattedNum

def randomize_time(mean):
	allowed_range = mean * STDEV
	stdev = allowed_range / 3  # 99.73% chance to be in the allowed range

	t = 0
	while abs(mean - t) > allowed_range:
		t = gauss(mean, stdev)

	return t

def set_sleep_percentage(percentage):
	global sleep_percentage
	sleep_percentage = percentage/100

def sleep(t, custom_percentage=None):
	if custom_percentage is None:
	   custom_percentage = sleep_percentage
	time = randomize_time(t)*custom_percentage
	original_sleep(time)

def follow_user_followers(    
							  usernames,
							  amount=10,
							  randomize=False,
							  interact=False,
							  sleep_delay=600):

		userFollowed = []
		if not isinstance(usernames, list):
			usernames = [usernames]
		for user in usernames:

			
			userFollowed += follow_given_user_followers(browser,
														user,
														amount,
														'',
														username,
														'',
														randomize,
														sleep_delay,
														'',
														'',
														'')

			
		
		if interact:
			userFollowed = random.sample(userFollowed, int(ceil(
				user_interact_percentage * len(userFollowed) / 100)))
			like_by_users(userFollowed,
							   user_interact_amount,
							   user_interact_random,
							   user_interact_media)

		return

def follow_given_user_followers(browser,
								user_name,
								amount,
								dont_include,
								login,
								follow_restrict,
								random,
								delay,
								blacklist,
								logger,
								follow_times):

	browser.get('https://www.instagram.com/' + user_name)
	# update server calls
	 
	#  check how many poeple are following this user.
	#  throw RuntimeWarning if we are 0 people following this user
	
	allfollowing = formatNumber(
		browser.find_element_by_xpath("//li[2]/a/span").text)
	
	
	following_link = browser.find_elements_by_xpath(
		"//a[starts-with(@href,'/p/Bd')]")
	following_link[1].send_keys("\n")
	
	sleep(5)

	likes_link = browser.find_elements_by_xpath(
		"//a[@class='_nzn1h _gu6vm']")
	likes_link[0].send_keys("\n")

	personFollowed = follow_through_dialog(browser,
										   user_name,
										   amount,
										   dont_include,
										   login,
										   follow_restrict,
										   allfollowing,
										   random,
										   delay,
										   blacklist,
										   logger,
										   follow_times,
										   callbacks=[])

	return personFollowed

def follow_through_dialog(browser,
						  user_name,
						  amount,
						  dont_include,
						  login,
						  follow_restrict,
						  allfollowing,
						  randomize,
						  delay,
						  blacklist,
						  logger,
						  follow_times,
						  callbacks=[]):
	sleep(2)
	person_followed = []
	real_amount = amount
	if randomize and amount >= 3:
		# expanding the popultaion for better sampling distribution
		amount = amount * 3

	# find dialog box
	dialog = browser.find_element_by_xpath(
	  "//div[@class='_p4iax']")

	# scroll down the page
	scroll_bottom(browser, dialog, allfollowing)

	# get follow buttons. This approch will find the follow buttons and
	# ignore the Unfollow/Requested buttons.
	follow_buttons = dialog.find_elements_by_xpath(
		"//div/div/span/button[text()='Follow']")

	person_list = []
	abort = False
	total_list = len(follow_buttons)

	# scroll down if the generated list of user to follow is not enough to
	# follow amount set
	while (total_list < amount) and not abort:
		amount_left = amount - total_list
		before_scroll = total_list
		scroll_bottom(browser, dialog, amount_left)
		sleep(1)
		follow_buttons = dialog.find_elements_by_xpath(
			"//div/div/span/button[text()='Follow']")
		total_list = len(follow_buttons)
		abort = (before_scroll == total_list)

	for person in follow_buttons:

		if person and hasattr(person, 'text') and person.text:
			person_list.append(person.find_element_by_xpath("../../../*")
							   .find_elements_by_tag_name("a")[1].text)
			

	if amount >= total_list:
		amount = total_list
		

	# follow loop
	hasSlept = False
	btnPerson = list(zip(follow_buttons, person_list))
	if randomize:
		sample = random.sample(range(0, len(follow_buttons)), real_amount)
		finalBtnPerson = []
		for num in sample:
			finalBtnPerson.append(btnPerson[num])
	else:
		finalBtnPerson = btnPerson

	followNum = 0

	for button, person in finalBtnPerson:
		if followNum >= real_amount:
			
			break

		if followNum != 0 and hasSlept is False and followNum % 10 == 0:	
			sleep(delay)
			hasSlept = True
			continue

		followNum += 1
		# Register this session's followed user for further interaction
		person_followed.append(person)

		button.send_keys("\n")
		
		for callback in callbacks:
			callback(person.encode('utf-8'))
		sleep(15)

		# To only sleep once until there is the next follow
		if hasSlept:
			hasSlept = False

		continue

		if randomize:
			repickedNum = -1
			while repickedNum not in sample and repickedNum != -1:
				repickedNum = random.randint(0, len(btnPerson))
			sample.append(repickedNum)
			finalBtnPerson.append(btnPerson[repickedNum])
		continue

	return person_followed

browser.get('https://www.instagram.com')

# try to load cookie from username
try:
	browser.get('https://www.google.com')
	for cookie in pickle.load(open('./logs/{}_cookie.pkl'
								   .format(username), 'rb')):
		browser.add_cookie(cookie)
	# logged in!
except (WebDriverException, OSError, IOError):
	print("Cookie file not found, creating cookie...")
	browser.get('https://www.instagram.com')

login_elem = browser.find_element_by_xpath(
	"//article/div/div/p/a[text()='Log in']")
if login_elem is not None:
	ActionChains(browser).move_to_element(login_elem).click().perform()

# Enter username and password and logs the user in
# Sometimes the element name isn't 'Username' and 'Password'
# (valid for placeholder too)
input_username = browser.find_elements_by_xpath(
	"//input[@name='username']")

ActionChains(browser).move_to_element(input_username[0]). \
	click().send_keys(username).perform()
sleep(1)
input_password = browser.find_elements_by_xpath(
	"//input[@name='password']")
ActionChains(browser).move_to_element(input_password[0]). \
	click().send_keys(password).perform()

login_button = browser.find_element_by_xpath(
	"//form/span/button[text()='Log in']")
ActionChains(browser).move_to_element(login_button).click().perform()

sleep(5)

follow_user_followers(['pranavkalraa', 'abhimanyudhall', 'pranavkhanna_1997'], amount=500, randomize=False)

# close the browser window
browser.quit()

