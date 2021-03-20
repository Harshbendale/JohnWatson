"""
Project Voice Assistant
Name: John Watson
@author: Harshal Bendale
"""

### Imports:
# general imports:
import datetime
import wikipedia
import requests
import numpy as np
import subprocess
from youtube_search import YoutubeSearch
from pynput.keyboard import Key,Controller
keyboard = Controller()
import time
import os
# imports for audio processing:
import pyttsx3
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from playsound import playsound
# google's speechrecognition library:
import speech_recognition as sr
# imports for browser automation (selenium):
from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
# imports for camera:
import cv2

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

# initializing output voice:
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')

for i in range(len(voices)):
    if i == 0:
	    engine.setProperty('voice', voices[i].id)

### Function declarations:
# to check if the process/application is open in the RAM:
def process_exists(process_name):
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    # use buildin check_output right away
    output = subprocess.check_output(call).decode()
    # check in last line for process name
    last_line = output.strip().split('\r\n')[-1]
    # because Fail message could be translated
    return last_line.lower().startswith(process_name.lower())

# to make John speak:
def speak(audio):
	back_to_volume = 0
	sessions = AudioUtilities.GetAllSessions()
	for session in sessions:
		volume = session._ctl.QueryInterface(ISimpleAudioVolume)
		if session.Process and session.Process.name() == "chrome.exe":
			back_to_volume = volume.GetMasterVolume()
			volume.SetMasterVolume(0.2, None)
	engine.say(audio)
	engine.runAndWait()
	for session in sessions:
		volume = session._ctl.QueryInterface(ISimpleAudioVolume)
		if session.Process and session.Process.name() == "chrome.exe":
			volume.SetMasterVolume(back_to_volume, None)

# to wish me according to the time (Good morning/evening):
def wishMe():
	hour = int(datetime.datetime.now().hour)
	if hour>= 0 and hour<12:
		speak('Good Morning!')
	elif hour>=12 and hour<18:
		speak('Good Afternoon!')
	else:
		speak('Good Evening!')
	speak(np.random.choice(["and welcome back Sir!","I am up and fully functional. How can I help sir?","I am John Watson. What can I do for you sir?","and Hello Sir, John Watson here","John Watson at your service sir"]))

# to adjust mic according to background noise:
def adjustmic():
	r = sr.Recognizer()
	with sr.Microphone() as source:
		print('Adjusting mic...')
		r.adjust_for_ambient_noise(source, duration = 0.5)

# to give command to John:
def takeCommand():
	r = sr.Recognizer()
	with sr.Microphone() as source:
		print('Listening...')
		r.pause_threshold = 1
		r.energy_threshold = 4000
		#r.adjust_for_ambient_noise(source, duration = 0.5)
		try:
			audio = r.listen(source, timeout = 2)
		except:
			time.sleep(1)
			return 'None'
	try:
		print('Recognizing...')
		query = r.recognize_google(audio, language='en-in')
		if "Amy" in query:
			query = query.replace("Amy","Emi")
		print('query:',query)
	except sr.UnknownValueError:
		print('try again')
		return 'None'
	return query

### Features of JW:
# to note down something in Notepad:
def note(text):
	date = datetime.datetime.now()
	file_name = str(date).replace(":","-") + "_note.txt"
	with open(file_name,'w') as f:
		f.write(text)
	subprocess.Popen(["notepad.exe",file_name])

# to start browser instance:
def start_browser(new_link):
	driver = webdriver.Chrome(executable_path=r"F:\\Interesting things\\Zyra\\chromedriver.exe")
	driver.get(new_link)
	all_windows = driver.window_handles
	windows_names_dict = {}
	if driver.title == 'weather outside - Google-Suche':
		windows_names_dict['weather'] = driver.current_window_handle
	else:
		windows_names_dict['youtube'] = driver.current_window_handle
	print(list(windows_names_dict.values()))
	print(list(windows_names_dict.keys()))
	print(all_windows)
	print('returning from function start_browser')
	return driver,all_windows,windows_names_dict

# update the list of tabs that are open in googel chrome:
def update_windows_list(new_tab_name,windows_names_dict):
	all_windows = driver.window_handles
	print(list(windows_names_dict.values()))
	print(list(windows_names_dict.keys()))
	print(all_windows)
	new_handle = [x for x in all_windows if x not in list(windows_names_dict.values())][0]
	windows_names_dict[new_tab_name] = new_handle
	driver.switch_to_window(new_handle)

# to switch from one tab to another in google chrome:
def switch_tab_driver(new_tab_name,windows_names_dict):
	driver.switch_to_window(windows_names_dict[new_tab_name])
	pass

# to adjust PC volume:
def adjust_pc_volume(vol,pc_volume):
	vol_diff = abs(vol-pc_volume)
	vol_tens = (vol_diff//10)*5
	vol_units = vol_diff%10//2
	if vol > pc_volume:
		for i in range(vol_tens):
			keyboard.press(Key.media_volume_up)
			keyboard.release(Key.media_volume_up)
		for i in range(vol_units):
			keyboard.press(Key.media_volume_up)
			keyboard.release(Key.media_volume_up)
		pc_volume = pc_volume + ((vol_tens*2)+(vol_units*2))
	elif vol < pc_volume:
		for i in range(vol_tens):
			keyboard.press(Key.media_volume_down)
			keyboard.release(Key.media_volume_down)
		for i in range(vol_units):
			keyboard.press(Key.media_volume_down)
			keyboard.release(Key.media_volume_down)
		pc_volume = pc_volume - ((vol_tens*2)+(vol_units*2))
	return pc_volume

### Main function:
if __name__ == '__main__':
	for i in range(50):
		keyboard.press(Key.media_volume_down)
		keyboard.release(Key.media_volume_down)
	for i in range(25):
		keyboard.press(Key.media_volume_up)
		keyboard.release(Key.media_volume_up)
	playsound("Audio//Boot_soundclip.mp3")
	# speak('Hello')
	wishMe()
	while True:
		### Loop routines before taking command:
		# to adjust mic:
		if process_exists('chrome.exe') == True:
			if 'youtube' in list(windows_names_dict.keys()):
				pass
				adjustmic()
		
		# to give command to John:
		query = takeCommand().lower()

		### General conversation querries:
		# general_conversation1 (How are you?):
		if 'how are you johnny' in query or 'how are you' in query:
			how_am_i = np.random.choice(['I am doing great. I learn a lot from you sir! How are you sir?','I am nicely hold in this cute little laptop. How are you sir?','I must say I am doing very good these days. How about you sir?'])
			speak(how_am_i)
			query2 = takeCommand()
			if 'not' in query2 or 'just fine' in query2:
				speak('o oh!')
				#delay
				pause = 0
				for i in range(300):
						pause += 1
				pause = 0
				speak(np.random.choice(['dont worry sir, every thing will be okay','dont worry sir, you are stronger than this']))
				speak('I am sure something good will happen soon')
				speak('how can I pour colors and be more helpful in your difficult times, sir?')
			elif 'good' in query2 or 'great' in query2 or 'well' in query2:
				speak(np.random.choice(['cool','awesome','great']))
				speak(np.random.choice(['Its always glad to hear you speak, Sir!','Nice, nice, its always glad to hear from you, Sir!']))
				speak(np.random.choice(['Tell me how I can be useful, Sir?','So! What can I do for you today sir?']))
		
		# general_conversation2 (What are you doing?):
		elif 'what are you doing' in query:
			speak('just doing my thing. Being with you, accompanying you, annnnd helping you in between, sir?')

		# general_conversation3 (Hello):
		elif query == 'hello' or query=='hi john' or query=='hey' or query == 'hi' or query == 'hi johnny' or query == 'hello john' or query == 'hey john'  or query == 'hey johnny':
			speak(np.random.choice(['hi sir','hello sir']))

		# general_conversation4 (Ask if John is still listening):
		elif query == 'john' or 'are you listening' in query or 'can you hear me' in query:
			query_yes_sir = np.random.choice(['yes sir?','ah ha, I am listening','Right here sir!'])
			speak(query_yes_sir)

		# general_conversation5 (Asking his name):
		elif query == 'what is your name' or query=="what's your name":
			name_text = np.random.choice(['you can call me John or Johnny','its John Watson,Sir','You might have missed it in the begining, its John Watson, sir!'])
			speak(name_text)
		
		# general_conversation6 (introduce him to someone):
		elif 'this is my' in query:
			split_query = query.split()
			speak('hello {} I am John Watson. Nice to meet you.'.format(split_query[-1]))
			
		# general_conversation7 (ask him to roll a die):
		elif 'roll a die' in query  or 'rohan or die' in query or 'roll or die' in query:
			speak('rolling a die')
			speak(np.random.choice(['and, and, and','annnd','ah ha','okaay','hmmmmm']))
			speak('It is a {}'.format(np.random.randint(1,7)))

		# general_conversation8 (ask him to roll 2 dice):
		elif 'roll the dice' in query:
			speak('rolling dice now')
			speak(np.random.choice(['annnd','ah ha','hmmmmm']))
			speak('It is a {} and a {}'.format(np.random.randint(1,7),np.random.randint(1,7)))

		# general_conversation9 (ask him to toss a coin):
		elif 'toss a coin' in query:
			speak('tossing a coin now')
			speak(np.random.choice(['and, and, and','ah ha','okaay,','hmmmmm']))
			speak('it is {}'.format(np.random.choice(['heads','tails'])))

		# general_conversation10 (compliment John):
		elif query == 'awesome' or query == 'great' or query == 'good' or query == 'nice' or query == 'cool':
			awesome_temp = ['yeaaa sir','awesome','all good','cool','great!']
			speak(np.random.choice(awesome_temp))

		# general_conversation11 (thank John):
		elif 'thank' in query:
			speak(np.random.choice(['happy to help sir','you are welcome sir']))

		# general_conversation12 (ask John for a favour):
		elif 'do me a favour' in query:
			speak(np.random.choice(['any time sir, just tell me what you would want me to do','definitely sir, tell me how I can help','sure sir, what is it?']))

		### Task querries:
		# Ask for time:
		elif 'the time' in query:
			strTime = datetime.datetime.now().strftime("%I:%M %p")
			speak("Sir, the time is {}".format(strTime))

		# Ask him to take note:
		elif 'take note' in query or 'write down' in query:
			speak('sure, what would you like me to write down?')
			note_text = takeCommand()
			note(note_text)
			speak('I have a made a note of that')
		
		# Ask for current weather report:
		elif 'weather outside' in query or 'temperature outside' in query:
			weather_link = 'https://google.com/search?q=weather outside'
			if process_exists('chrome.exe') == True:
				driver.execute_script("window.open('https://google.com/search?q=weather outside')")
				#now switch tabs
				update_windows_list('weather',windows_names_dict)
			else:
				driver,all_windows,windows_names_dict = start_browser(weather_link)
			temperature_span = driver.find_elements_by_xpath('//*[@id="wob_tm"]')
			sky = driver.find_elements_by_xpath('//*[@id="wob_dc"]')
			sky_now = {'Schneeschauer':'Snow showers','Regen':'rainy','Überwiegend bewölkt':'Mostly cloudy','Nebel':'its foggy','Stark bewölkt':'the sky is densly cloudy','Klar und vereinzelt Wolken':'we have clear sky with isolated clouds','Wolkenlos':'we have a clear sky','Überwiegend sonnig':'Mostly Sunny','Teils bewölkt':'it is partly cloudy','Sonnig':'it is sunny','Leichte Regenschauer':'there can be Light rain showers'}
			wind = driver.find_elements_by_xpath('//*[@id="wob_ws"]')
			print(sky,type(sky))
			speak('sir, the temperature right now is {} degree celcius'.format(temperature_span[0].get_attribute('innerHTML')))
			speak('and {} today'.format(sky_now[sky[0].get_attribute('innerHTML')]))
			speak('with a wind speed of {}'.format(wind[0].get_attribute('innerHTML')))
			driver.maximize_window()
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
			if process_exists('chrome.exe') == True:
				if 'youtube.com' in driver.current_url:
					speak('sure sir, playing it in same tab now')
					driver.get('https://youtube.com/search?q={}'.format(query))
				else:
					speak('sure sir, opening youtube in new tab now')
					driver.execute_script("window.open('https://youtube.com')")
					update_windows_list('youtube',windows_names_dict)
					driver.get(youtube_link)
			else:
				speak('sure sir, opening youtube now')
				i_agree = False
				no_thanks = False
				pop_ups_clean = False
				driver,all_windows,windows_names_dict = start_browser(youtube_link)
			# clear "I Agree" pop-up from google:
			while i_agree == False:
				retry_counter = 0
				# clicking "I Agree" button:
				try:
					try:
						print('searching I Agree btn in german format')
						WebDriverWait(driver, 1).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"/html/body/div[7]/div[2]/div[6]/div/div[2]/span/div/div/iframe")))
						print('switching to iframe')
						WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div#introAgreeButton"))).click()
						i_agree = True
						driver.switch_to.default_content()
					except:
						print('not found')
						retry_counter += 1
						if retry_counter == 10:
							break
					print('searching I Agree btn in regular format now')
					WebDriverWait(driver, 1).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe#iframe")))
					print('switching to iframe')
					WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div#introAgreeButton"))).click()
					i_agree = True
					driver.switch_to.default_content()
				except:
					print('no IAgree found')
					retry_counter += 1
					if retry_counter == 10:
						driver.switch_to.default_content()
						break
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
			# Skipping ads and bypassing Youtube sign-in pop-up in google chrome:
			while no_thanks == False:
				# clicking "No Thanks" button:
				try:
					print('finding NOTHANKS')
					WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/ytd-app/ytd-popup-container/tp-yt-paper-dialog/yt-upsell-dialog-renderer/div/div[3]/div[1]/yt-button-renderer/a/paper-button"))).click()
					driver.switch_to.default_content()
					driver.find_element_by_tag_name('body').send_keys('k')
					print("SWITCHED TO BODY")
					no_thanks = True
				except:
					print('no NoThanks found')
					retry_counter += 1
					if retry_counter == 10:
						break
				print("retry_counter: ",retry_counter)
				print("i_agree: ",i_agree)
				print("no_thanks: ",no_thanks)
				pop_ups_clean = i_agree and no_thanks
				print("pop_ups_clean :", pop_ups_clean)			

		# Ask him to play/pause the YouTube video in google chrome:
		elif 'play video' in query or 'play my video' in query or 'play the song' in query or 'continue playing' in query or 'pause' in query or query == 'stop':
			if process_exists('chrome.exe') == True:
				if 'youtube.com' in driver.current_url:
					driver.find_element_by_tag_name('body').send_keys('k')
				elif 'youtube.com' in windows_names_dict.keys:
					switch_tab_driver('youtube',windows_names_dict)
					play_button = driver.find_elements_by_xpath('//*[@id="movie_player"]/div[27]/div[2]/div[1]/button/svg')
					play_button.click()
				speak(np.random.choice(['sure sir','yes sir','ok sir']))
			else:
				speak('Sorry Sir, youtube is not opened in any tab')

		# Ask to play next song/video on YouTube in google chrome:
		elif 'next' in query or 'change song' in query:
			driver.find_element_by_tag_name('body').send_keys(Keys.SHIFT + 'n')
			next_text = np.random.choice(['next one coming up right away sir!',"here's the next one",'going next sir','aye aye sir, here is the next one'])
			speak(next_text)

		# Ask to play previous song/video on YouTube in google chrome:
		elif 'previous' in query or 'back' in query:
			if process_exists('chrome.exe') == True:
				try:
					driver.back()
					speak('going back sir')
				except:
					speak("sir, this browser was not opened by me, so I have no access to it")
					speak("Please ask me to close this browser and start a new session")

		# Ask him to close the current tab in google chrome
		elif 'close tab' in query or 'close the tab' in query:
			with keyboard.pressed(Key.ctrl):
				keyboard.press('w')
				keyboard.release('w')
			speak('tab closed')

		# Ask him to close the current window of application:
		elif 'close window' in query or 'close the window' in query:
			with keyboard.pressed(Key.alt):
				keyboard.press(Key.f4)
				keyboard.release(Key.f4)
			speak('window closed')

		# Ask him to open sublime text editor:
		elif 'open sublime' in query:
			subprocess.call("F:\\Downloads\\Setups\\Sublime Text Build 3207 x64\\sublime_text.exe")
			speak('coming up on window, your favourite toy, sir. Enjoy')

		# Ask him to press "Alt+Tab" once:
		elif 'switch window' in query:
			with keyboard.pressed(Key.alt):
				keyboard.press(Key.tab)
				keyboard.release(Key.tab)
			speak(np.random.choice(['ok sir','yes sir','sure sir']))
			speak('window switched')

		# Ask him to adjust volume of google chrome browser:
		elif 'volume' in query:
			temp_vol_query = query.split()
			if len(temp_vol_query)>1:
				vol_str = temp_vol_query[-1]
				if vol_str.isnumeric():
					pc_volume = adjust_pc_volume(int(vol_str)%100,pc_volume)
				else:
					if "mute" in vol_str:
						keyboard.press(Key.media_volume_mute)
						keyboard.release(Key.media_volume_mute)
					elif vol_str == "half":
						pc_volume = adjust_pc_volume(50,pc_volume)
					elif vol_str == "full" or vol_str == "max":
						pc_volume = adjust_pc_volume(100,pc_volume)
					elif "%" in vol_str:
						pc_volume = adjust_pc_volume(int(vol_str[:-1])%100,pc_volume)
					elif vol_str == "volume":
						if "max" in temp_vol_query[-2]:
							pc_volume = adjust_pc_volume(100,pc_volume)
						elif "mute" in temp_vol_query[-2]:
							keyboard.press(Key.media_volume_mute)
							keyboard.release(Key.media_volume_mute)
				print("new pc_volume:",pc_volume)
				speak("Volume set on {}".format(pc_volume))

		# Ask John to open camera:
		elif 'camera' in query:
			cam = cv2.VideoCapture(1)
			cv2.namedWindow("Harshi's Cam")
			speak(np.random.choice(["Sure sir, ready when you are!","Welcome to Harshi's Cam, sir"]))
			while True:
				date = datetime.datetime.now()
				ret, frame = cam.read()
				if not ret:
					print("failed to grab frame")
					break
				cv2.imshow("Harshi's Cam", frame)
				k = cv2.waitKey(1)
				if k%256 == 27:#'close camera' in pic_query:
					speak("Camera closed")
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
			speak("Sure sir, which playlist?")
			accept_count = 0
			youtube_link = ''
			while True:
				mysong_query = takeCommand()
				print(mysong_query)
				if 'Hindi' in mysong_query:
					youtube_link = 'https://www.youtube.com/watch?v=YR12Z8f1Dh8&list=PLziXWRw7-BE3oN7WpHG_G88QIT3dkj8QK&index=2&t=0s'
					break
				elif 'English' in mysong_query or 'english' in mysong_query:
					youtube_link = 'https://www.youtube.com/watch?v=ZY_2E8lVvFU&list=PLziXWRw7-BE1N1aKpGB66uCVwngR3Jl5i'
					break
				else:
					accept_count += 1
					if accept_count == 3:
						speak("sorry sir, still could not get you. Try saying play my songs again")
						break
					speak("sorry sir, could you please repeat?")

			if youtube_link != '':
				if process_exists('chrome.exe') == True:
					if 'youtube.com' in driver.current_url:
						speak('sure sir, playing it in same tab now')
						driver.get(youtube_link)
					else:
						speak('sure sir, opening youtube in new tab now')
						driver.execute_script("window.open('https://youtube.com')")
						update_windows_list('youtube',windows_names_dict)
						driver.get(youtube_link)
				else:
					speak('sure sir, opening youtube now')
					driver,all_windows,windows_names_dict = start_browser(youtube_link)
				try:
					yt_red_button = driver.find_elements_by_xpath('//*[@id="movie_player"]/div[5]/button')[0]
					yt_red_button.click()
				except:
					print("no red play button found")
					pass
				driver.maximize_window()

		# Ask to shuffle playlist
		elif 'shuffle playlist' in query:
			if process_exists('chrome.exe') == True:
				if 'youtube.com' in driver.current_url:
					try:
						shuffle_button3 = driver.find_elements_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div[2]/div/ytd-playlist-panel-renderer/div/div[1]/div/div[2]/div[1]/div[1]/ytd-menu-renderer/div/ytd-toggle-button-renderer[2]/a/yt-icon-button/button')
						shuffle_button3[0].click()
						speak("shuffling toggled")
						print("shuffling toggled")
					except:
						speak("sorry sir, this is not a playlist that can be shuffled")

		# Switch off John Wattson:
		elif ('get some rest' in query) or ('get some sleep' in query) or 'rest' in query or 'stop listening' in query:
			speak(np.random.choice(["Ok sir, I will be here if you need anything","Ok sir, bye bye, and have a nice day","Sure sir, if you need anything, you know where to find me"]))
			time.sleep(0.1)
			playsound("Audio//Shutdown_soundclip.mp3")
			break

		### Loop routines after taking command:
		# to skip YouTube ads if any:
		if process_exists('chrome.exe') == True:
			try:
				driver.switch_to.default_content()
				skip = driver.find_element_by_class_name('ytp-ad-skip-button-container')
				speak(np.random.choice(['let me skip the ad sir','just a moment! sir']))
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

