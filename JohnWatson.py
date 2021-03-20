"""
Project Voice Assistant
Name: John Watson
@author: Harshal Bendale
"""

### Imports:
# general imports:
import wikipedia
import requests
import numpy as np
from youtube_search import YoutubeSearch
from pynput.keyboard import Key,Controller
import time
import os
# imports for audio processing:
from playsound import playsound
# google's speechrecognition library:
import speech_recognition as sr
# imports for browser automation (selenium):
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
# imports for camera:
import cv2
# local file imports:
import JW_functions as jw_fn
import JW_features as jw_ft

### Declaring global variables: 
# to access the same chrome web driver:
global driver
# for handling of tabs in chrome:
global all_windows
all_windows = []
global windows_names_dict
windows_names_dict = {}
# to handle google pop-ups:
global pop_ups_clean
pop_ups_clean = False
global i_agree
i_agree = False
global no_thanks
no_thanks = False
# PC Volume
global pc_volume
pc_volume = 50

keyboard = Controller()

### Main function:
if __name__ == '__main__':
	for i in range(50):
		keyboard.press(Key.media_volume_down)
		keyboard.release(Key.media_volume_down)
	for i in range(25):
		keyboard.press(Key.media_volume_up)
		keyboard.release(Key.media_volume_up)
	playsound("Audio//Boot_soundclip.mp3")
	jw_fn.wishMe()
	while True:
		### Loop routines before taking command:
		# to adjust mic:
		if jw_fn.process_exists('chrome.exe') == True:
			if 'youtube' in list(windows_names_dict.keys()):
				pass
				jw_fn.adjustmic()
		
		# to give command to John:
		query = jw_fn.takeCommand().lower()

		### General conversation querries:
		# general_conversation1 (How are you?):
		if 'how are you johnny' in query or 'how are you' in query:
			how_am_i = np.random.choice(['I am doing great. I learn a lot from you sir! How are you sir?','I am nicely hold in this cute little laptop. How are you sir?','I must say I am doing very good these days. How about you sir?'])
			jw_fn.speak(how_am_i)
			query2 = jw_fn.takeCommand()
			if 'not' in query2 or 'just fine' in query2:
				jw_fn.speak('o oh!')
				#delay
				pause = 0
				for i in range(300):
						pause += 1
				pause = 0
				jw_fn.speak(np.random.choice(['dont worry sir, every thing will be okay','dont worry sir, you are stronger than this']))
				jw_fn.speak('I am sure something good will happen soon')
				jw_fn.speak('how can I pour colors and be more helpful in your difficult times, sir?')
			elif 'good' in query2 or 'great' in query2 or 'well' in query2:
				jw_fn.speak(np.random.choice(['cool','awesome','great']))
				jw_fn.speak(np.random.choice(['Its always glad to hear you speak, Sir!','Nice, nice, its always glad to hear from you, Sir!']))
				jw_fn.speak(np.random.choice(['Tell me how I can be useful, Sir?','So! What can I do for you today sir?']))
		
		# general_conversation2 (What are you doing?):
		elif 'what are you doing' in query:
			jw_fn.speak('just doing my thing. Being with you, accompanying you, annnnd helping you in between, sir?')

		# general_conversation3 (Hello):
		elif query == 'hello' or query=='hi john' or query=='hey' or query == 'hi' or query == 'hi johnny' or query == 'hello john' or query == 'hey john'  or query == 'hey johnny':
			jw_fn.speak(np.random.choice(['hi sir','hello sir']))

		# general_conversation4 (Ask if John is still listening):
		elif query == 'john' or 'are you listening' in query or 'can you hear me' in query:
			query_yes_sir = np.random.choice(['yes sir?','ah ha, I am listening','Right here sir!'])
			jw_fn.speak(query_yes_sir)

		# general_conversation5 (Asking his name):
		elif query == 'what is your name' or query=="what's your name":
			name_text = np.random.choice(['you can call me John or Johnny','its John Watson,Sir','You might have missed it in the begining, its John Watson, sir!'])
			jw_fn.speak(name_text)
		
		# general_conversation6 (introduce him to someone):
		elif 'this is my' in query:
			split_query = query.split()
			jw_fn.speak('hello {} I am John Watson. Nice to meet you.'.format(split_query[-1]))
			
		# general_conversation7 (ask him to roll a die):
		elif 'roll a die' in query  or 'rohan or die' in query or 'roll or die' in query:
			jw_fn.speak('rolling a die')
			jw_fn.speak(np.random.choice(['and, and, and','annnd','ah ha','okaay','hmmmmm']))
			jw_fn.speak('It is a {}'.format(np.random.randint(1,7)))

		# general_conversation8 (ask him to roll 2 dice):
		elif 'roll the dice' in query:
			jw_fn.speak('rolling dice now')
			jw_fn.speak(np.random.choice(['annnd','ah ha','hmmmmm']))
			jw_fn.speak('It is a {} and a {}'.format(np.random.randint(1,7),np.random.randint(1,7)))

		# general_conversation9 (ask him to toss a coin):
		elif 'toss a coin' in query:
			jw_fn.speak('tossing a coin now')
			jw_fn.speak(np.random.choice(['and, and, and','ah ha','okaay,','hmmmmm']))
			jw_fn.speak('it is {}'.format(np.random.choice(['heads','tails'])))

		# general_conversation10 (compliment John):
		elif query == 'awesome' or query == 'great' or query == 'good' or query == 'nice' or query == 'cool':
			awesome_temp = ['yeaaa sir','awesome','all good','cool','great!']
			jw_fn.speak(np.random.choice(awesome_temp))

		# general_conversation11 (thank John):
		elif 'thank' in query:
			jw_fn.speak(np.random.choice(['happy to help sir','you are welcome sir']))

		# general_conversation12 (ask John for a favour):
		elif 'do me a favour' in query:
			jw_fn.speak(np.random.choice(['any time sir, just tell me what you would want me to do','definitely sir, tell me how I can help','sure sir, what is it?']))

		### Task querries:
		# Ask for time:
		elif 'the time' in query:
			strTime = jw_fn.datetime.datetime.now().strftime("%I:%M %p")
			jw_fn.speak("Sir, the time is {}".format(strTime))

		# Ask him to take note:
		elif 'quick note' in query or 'write down quickly' in query:
			jw_fn.speak('sure, what would you like me to write down?')
			note_text = jw_fn.takeCommand()
			jw_ft.note(note_text)
			jw_fn.speak('I have a made a note of that')
		
		# Ask for current weather report:
		elif 'weather outside' in query or 'temperature outside' in query:
			weather_link = 'https://google.com/search?q=weather outside'
			if jw_fn.process_exists('chrome.exe') == True:
				driver.execute_script("window.open('https://google.com/search?q=weather outside')")
				#now switch tabs
				jw_ft.update_windows_list('weather',windows_names_dict,driver)
			else:
				driver,all_windows,windows_names_dict = jw_ft.start_browser(weather_link)
			temperature_span = driver.find_elements_by_xpath('//*[@id="wob_tm"]')
			sky = driver.find_elements_by_xpath('//*[@id="wob_dc"]')
			sky_now = {'Schneeschauer':'Snow showers','Regen':'rainy','Überwiegend bewölkt':'Mostly cloudy','Nebel':'its foggy','Stark bewölkt':'the sky is densly cloudy','Klar und vereinzelt Wolken':'we have clear sky with isolated clouds','Wolkenlos':'we have a clear sky','Überwiegend sonnig':'Mostly Sunny','Teils bewölkt':'it is partly cloudy','Sonnig':'it is sunny','Leichte Regenschauer':'there can be Light rain showers'}
			wind = driver.find_elements_by_xpath('//*[@id="wob_ws"]')
			print(sky,type(sky))
			jw_fn.speak('sir, the temperature right now is {} degree celcius'.format(temperature_span[0].get_attribute('innerHTML')))
			jw_fn.speak('and {} today'.format(sky_now[sky[0].get_attribute('innerHTML')]))
			jw_fn.speak('with a wind speed of {}'.format(wind[0].get_attribute('innerHTML')))
			driver.maximize_window()
			if i_agree == False:
				i_agree = jw_ft.click_i_agree(i_agree,driver)
			if 'youtube' in list(windows_names_dict.keys()):
				driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
				driver.switch_to_window(windows_names_dict['youtube'])
				print('title:',driver.title)

		# Ask him to play something on YouTube in google chrome:
		elif 'youtube' in query:
			if 'on youtube' in query:
				query = query.replace('on youtube',"")
			else:
				query = query.replace('youtube',"")
			youtube_link = 'https://youtube.com/search?q={}'.format(query)
			# check if google chrome is already open, else start from scratch:
			if jw_fn.process_exists('chrome.exe') == True:
				if 'youtube.com' in driver.current_url:
					jw_fn.speak('sure sir, playing it in same tab now')
					driver.get('https://youtube.com/search?q={}'.format(query))
				else:
					jw_fn.speak('sure sir, opening youtube in new tab now')
					driver.execute_script("window.open('https://youtube.com')")
					jw_ft.update_windows_list('youtube',windows_names_dict,driver)
					if no_thanks == False:
						no_thanks = jw_ft.click_no_thanks(no_thanks,driver)
					driver.get(youtube_link)
			else:
				jw_fn.speak('sure sir, opening youtube now')
				i_agree = False
				no_thanks = False
				pop_ups_clean = False
				driver,all_windows,windows_names_dict = jw_ft.start_browser(youtube_link)
			# clear "I Agree" pop-up from google:
			if i_agree == False:
				i_agree = jw_ft.click_i_agree(i_agree,driver)
			# click the first video in the list of querry hits:
			if driver.find_elements_by_xpath('//*[@id="ad-badge-container"]/ytd-badge-supported-renderer/div/span'):
				print('ad found,\n now clicking second video')
				second_video = driver.find_elements_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/ytd-thumbnail/a/yt-img-shadow')
				second_video[0].click()
			else:
				first_video = driver.find_elements_by_xpath('//*[@id="thumbnail"]')
				driver.switch_to.default_content()
				first_video[0].click()
				print('first video clicked!')
			driver.maximize_window()
			time.sleep(1)
			# Bypassing Youtube sign-in pop-up in google chrome:
			if no_thanks == False:
				no_thanks = jw_ft.click_no_thanks(no_thanks,driver)			

		# Ask him to play/pause the YouTube video in google chrome:
		elif 'play video' in query or 'play my video' in query or 'play the song' in query or 'continue playing' in query or 'pause' in query or query == 'stop':
			if jw_fn.process_exists('chrome.exe') == True:
				if 'youtube.com' in driver.current_url:
					driver.find_element_by_tag_name('body').send_keys('k')
				elif 'youtube.com' in windows_names_dict.keys():
					jw_ft.switch_tab_driver('youtube',windows_names_dict,driver)
					play_button = driver.find_elements_by_xpath('//*[@id="movie_player"]/div[27]/div[2]/div[1]/button/svg')
					play_button.click()
				jw_fn.speak(np.random.choice(['sure sir','yes sir','ok sir']))
			else:
				jw_fn.speak('Sorry Sir, youtube is not opened in any tab')

		# Ask to play next song/video on YouTube in google chrome:
		elif 'next' in query or 'change song' in query:
			driver.find_element_by_tag_name('body').send_keys(Keys.SHIFT + 'n')
			next_text = np.random.choice(['next one coming up right away sir!',"here's the next one",'going next sir','aye aye sir, here is the next one'])
			jw_fn.speak(next_text)

		# Ask to play previous song/video on YouTube in google chrome:
		elif 'previous' in query or 'back' in query:
			if jw_fn.process_exists('chrome.exe') == True:
				try:
					driver.back()
					jw_fn.speak('going back sir')
				except:
					jw_fn.speak("sir, this browser was not opened by me, so I have no access to it")
					jw_fn.speak("Please ask me to close this browser and start a new session")

		# Ask him to close the current tab in google chrome
		elif 'close tab' in query or 'close the tab' in query:
			with keyboard.pressed(Key.ctrl):
				keyboard.press('w')
				keyboard.release('w')
			jw_fn.speak('tab closed')

		# Ask him to close the current window of application:
		elif 'close window' in query or 'close the window' in query:
			with keyboard.pressed(Key.alt):
				keyboard.press(Key.f4)
				keyboard.release(Key.f4)
			jw_fn.speak('window closed')

		# Ask him to press "Alt+Tab" once:
		elif 'switch window' in query:
			with keyboard.pressed(Key.alt):
				keyboard.press(Key.tab)
				keyboard.release(Key.tab)
			jw_fn.speak(np.random.choice(['ok sir','yes sir','sure sir']))
			jw_fn.speak('window switched')

		# Ask him to adjust volume of PC:
		elif 'volume' in query:
			temp_vol_query = query.split()
			if len(temp_vol_query)>1:
				vol_str = temp_vol_query[-1]
				if vol_str.isnumeric():
					pc_volume = jw_ft.adjust_pc_volume(int(vol_str)%100,pc_volume,keyboard)
				else:
					if "mute" in vol_str:
						keyboard.press(Key.media_volume_mute)
						keyboard.release(Key.media_volume_mute)
					elif vol_str == "half":
						pc_volume = jw_ft.adjust_pc_volume(50,pc_volume,keyboard)
					elif vol_str == "full" or vol_str == "max":
						pc_volume = jw_ft.adjust_pc_volume(100,pc_volume,keyboard)
					elif "%" in vol_str:
						pc_volume = jw_ft.adjust_pc_volume(int(vol_str[:-1])%100,pc_volume,keyboard)
					elif vol_str == "volume":
						if "max" in temp_vol_query[-2]:
							pc_volume = jw_ft.adjust_pc_volume(100,pc_volume,keyboard)
						elif "mute" in temp_vol_query[-2]:
							keyboard.press(Key.media_volume_mute)
							keyboard.release(Key.media_volume_mute)
				print("new pc_volume:",pc_volume)
				jw_fn.speak("Volume set on {}".format(pc_volume))

		# Ask John to open camera:
		elif 'camera' in query:
			cam = cv2.VideoCapture(1)
			cv2.namedWindow("Harshi's Cam")
			jw_fn.speak(np.random.choice(["Sure sir, ready when you are!","Welcome to Harshi's Cam, sir"]))
			while True:
				date = datetime.datetime.now()
				ret, frame = cam.read()
				if not ret:
					print("failed to grab frame")
					break
				cv2.imshow("Harshi's Cam", frame)
				k = cv2.waitKey(1)
				if k%256 == 27:#'close camera' in pic_query:
					jw_fn.speak("Camera closed")
					break
				elif k%256 == 32:
					playsound("Audio//Camera_shutter.mp3")
					img_name = "Harshiz_Cam\\Harshi's Cam_"+ str(date).replace(":","-") + ".png"
					cv2.imwrite(img_name, frame)
					print("{} Image saved!".format(img_name))
			cam.release()
			cv2.destroyAllWindows()

		# Ask to play my songs playlist on YouTube:
		elif 'my songs' in query:
			jw_fn.speak("Sure sir, which playlist?")
			accept_count = 0
			youtube_link = ''
			while True:
				mysong_query = jw_fn.takeCommand().lower
				print(mysong_query)
				if 'hindi' in mysong_query:
					youtube_link = 'https://www.youtube.com/watch?v=YR12Z8f1Dh8&list=PLziXWRw7-BE3oN7WpHG_G88QIT3dkj8QK&index=2&t=0s'
					break
				elif 'english' in mysong_query:
					youtube_link = 'https://www.youtube.com/watch?v=AEVaK0e1kTE&list=PLziXWRw7-BE1N1aKpGB66uCVwngR3Jl5i&index=1'
					break
				elif 'mix 1' in mysong_query or '1' in mysong_query or 'one' in mysong_query:
					youtube_link = 'https://www.youtube.com/watch?v=pXRviuL6vMY&list=RDpXRviuL6vMY'
				elif 'mix 2' in mysong_query or '2' in mysong_query or 'two' in mysong_query:
					youtube_link = 'https://www.youtube.com/watch?v=fKopy74weus&list=RDfKopy74weus'
				elif 'mix 3' in mysong_query or '3' in mysong_query or 'three' in mysong_query or '3d' in mysong_query:
					youtube_link = 'https://www.youtube.com/watch?v=S7LCkEJcEag&list=RDS7LCkEJcEag'
				else:
					accept_count += 1
					if accept_count == 3:
						jw_fn.speak("sorry sir, still could not get you. Try saying play my songs again")
						break
					jw_fn.speak("sorry sir, could you please repeat?")

			if youtube_link != '':
				if jw_fn.process_exists('chrome.exe') == True:
					if 'youtube.com' in driver.current_url:
						jw_fn.speak('sure sir, playing it in same tab now')
						driver.get(youtube_link)
					else:
						jw_fn.speak('sure sir, opening youtube in new tab now')
						driver.execute_script("window.open('https://youtube.com')")
						jw_ft.update_windows_list('youtube',windows_names_dict,driver)
						driver.get(youtube_link)
				else:
					jw_fn.speak('sure sir, opening youtube now')
					driver,all_windows,windows_names_dict = jw_ft.start_browser(youtube_link)
				try:
					yt_red_button = driver.find_elements_by_xpath('//*[@id="movie_player"]/div[5]/button')[0]
					yt_red_button.click()
				except:
					print("no red play button found")
					pass
				driver.maximize_window()

		# Ask to shuffle playlist
		elif 'shuffle playlist' in query:
			if jw_fn.process_exists('chrome.exe') == True:
				if 'youtube.com' in driver.current_url:
					try:
						shuffle_button3 = driver.find_elements_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div[2]/div/ytd-playlist-panel-renderer/div/div[1]/div/div[2]/div[1]/div[1]/ytd-menu-renderer/div/ytd-toggle-button-renderer[2]/a/yt-icon-button/button')
						shuffle_button3[0].click()
						jw_fn.speak("shuffling toggled")
						print("shuffling toggled")
					except:
						jw_fn.speak("sorry sir, this is not a playlist that can be shuffled")

		# Switch off John Wattson:
		elif ('get some rest' in query) or ('get some sleep' in query) or 'rest' in query or 'stop listening' in query:
			jw_fn.speak(np.random.choice(["Ok sir, I will be here if you need anything","Ok sir, bye bye, and have a nice day","Sure sir, if you need anything, you know where to find me"]))
			time.sleep(0.1)
			playsound("Audio//Shutdown_soundclip.mp3")
			break

		### Loop routines after taking command:
		# to skip YouTube ads if any:
		if jw_fn.process_exists('chrome.exe') == True:
			try:
				driver.switch_to.default_content()
				skip = driver.find_element_by_class_name('ytp-ad-skip-button-container')
				jw_fn.speak(np.random.choice(['let me skip the ad sir','just a moment! sir']))
				while True:
					try:
						skip = driver.find_element_by_class_name('ytp-ad-skip-button-container')
						pause = 0
						for i in range(300):
								pause += 1
						pause = 0
						skip.click()
						break
					except:
						continue
			except:
				print("no ad skips found")

