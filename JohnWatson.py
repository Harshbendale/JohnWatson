import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import requests
import numpy as np
import subprocess
from youtube_search import YoutubeSearch
from pynput.mouse import Button, Controller
import keyboard
import time
import os
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume

from selenium import webdriver
from selenium.webdriver.chrome import service

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

global driver

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')

for i in range(len(voices)):
    if i == 0:
	    engine.setProperty('voice', voices[i].id)


def process_exists(process_name):
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    # use buildin check_output right away
    output = subprocess.check_output(call).decode()
    # check in last line for process name
    last_line = output.strip().split('\r\n')[-1]
    # because Fail message could be translated
    return last_line.lower().startswith(process_name.lower())

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

def wishMe():
	hour = int(datetime.datetime.now().hour)
	if hour>= 0 and hour<12:
		speak('Good Morning!')
	elif hour>=12 and hour<18:
		speak('Good Afternoon!')
	else:
		speak('Good Evening!')
	speak(np.random.choice(["I am John Watson. What can I do for you sir?",'John Watson at your service sir!','and Hello Sir, John Watson here']))

def adjustmic():
	r = sr.Recognizer()
	with sr.Microphone() as source:
		print('Adjusting mic...')
		r.adjust_for_ambient_noise(source)

def takeCommand():

	r = sr.Recognizer()
	with sr.Microphone() as source:
		print('Listening...')
		r.pause_threshold = 1
		r.energy_threshold = 5000
		#r.adjust_for_ambient_noise(source, duration = 0.5)
		try:
			audio = r.listen(source, timeout = 3)
		except:
			time.sleep(1)
			return 'None'

	try:
		print('Recognizing...')
		query = r.recognize_google(audio, language='en-in')
		print('query:',query)
	except sr.UnknownValueError:
		print('try again')
		return 'None'
	except Exception as e:
		print('Say that again please!')
		return 'None'
	return query

def note(text):
	date = datetime.datetime.now()
	file_name = str(date).replace(":","-") + "_note.txt"
	with open(file_name,'w') as f:
		f.write(text)
	subprocess.Popen(["notepad.exe",file_name])

if __name__ == '__main__':
	#adjustmic()
	speak('Hello')
	wishMe()
	while True:
		query = takeCommand().lower()

		if 'the time' in query:
			strTime = datetime.datetime.now().strftime("%I:%M %p")
			speak("Sir, the time is {}".format(strTime))

		elif 'how are you johnny' in query or 'how are you' in query:
			how_am_i = np.random.choice(['I am doing great. I learn a lot from you sir! How are you sir?','I am nicely hold in this cute little laptop. How are you sir?','I must say I am doing very good these days. How about you sir?'])
			speak(how_am_i)
			query2 = takeCommand()
			if 'not' in query2 or 'just fine' in query2:
				speak('o oh!')
				pause = 0
				for i in range(300):
						pause += 1
				pause = 0
				speak(np.random.choice(['dont worry sir, every thing will be okay','dont worry sir, you are stronger than this']))
				speak('I am sure something good will happen soon')
				speak('how can I pour colors and be more helpful in your difficult times, sir?')
			elif 'good' in query2 or 'great' in query2:
				speak(np.random.choice(['cool','awesome','great']))
				speak(np.random.choice(['Its always glad to hear you speak, Sir!','Nice, nice, its always glad to hear from you, Sir!']))
				speak(np.random.choice(['Tell me how I can be useful, Sir?','So! What can I do for you today sir?']))

		elif query == 'john' or query=='johnny' or 'can you hear me' in query or query == 'hey john'  or query == 'hey johnny':
			query_yes_sir = np.random.choice(['yes sir?','ah ha, I am listening'])
			speak(query_yes_sir)

		elif 'are you there' in query:
			speak('Right here sir!')

		elif query == 'what is your name' or query=="what's your name":
			name_text = np.random.choice(['you can call me John or Johnny','its John Watson,Sir','You might have missed it in the begining, its John Watson, sir!'])
			speak(name_text)

		elif 'what are you doing' in query:
			speak('just doing my thing. Being with you, accompanying you, annnnd helping you in between, sir?')

		elif query == 'hello' or query=='hi john' or query=='hey' or query == 'hi' or query == 'hi johnny' or query == 'hello john':
			speak(np.random.choice(['hi sir','hello sir']))

		elif 'weather outside' in query:
			res = requests.get('https://google.com/search?q='+''.join('weather outside'))
			print(res,type(res))

		elif 'take note' in query or 'write down' in query:
			speak('sure, what would you like me to write down?')
			note_text = takeCommand()
			note(note_text)
			speak('I have a made a note of that')

		elif 'youtube' in query:
			speak('sure sir, opening youtube now')
			if 'on youtube' in query:
				query = query.replace('on youtube',"")
			else:
				query = query.replace('youtube',"")
			results = YoutubeSearch(query, max_results=1).to_dict()

			driver = webdriver.Chrome(executable_path=r"F:\\Downloads\\Setups\\chrome_driver\\chromedriver.exe")
			driver.get('https://youtube.com'+results[0]['link'])
			driver.maximize_window()
			#player_status = driver.execute_script("return document.getElementById('movie_player').getPlayerState()")
			time.sleep(1)
			yt_red_button = driver.find_elements_by_xpath('//*[@id="movie_player"]/div[5]/button')[0]
			yt_red_button.click()
			'''
			ad_skipped=False
			if process_exists('chrome.exe') == True:
				while ad_skipped==False:
					try:
						skip = driver.find_element_by_class_name('ytp-ad-skip-button-container')
						skip.click()
						ad_skipped=True
					except:
						ad_skipped=False
						speak(np.random.choice(['let me skip the ad sir','just a moment! sir','uh oh, please wait']))
						continue

			#webbrowser.open('https://youtube.com'+results[0]['link'])
			#adjustmic()
			'''
		elif 'skip' in query:
			mouse = Controller()
			mouse.position=(830,500)
			mouse.click(Button.left,1)
			speak(np.random.choice(['sure sir','skipping now sir']))
			

		elif 'play video' in query or 'play my video' in query or 'play the song' in query or 'continue playing' in query or 'pause' in query or query == 'stop':
			mouse = Controller()
			mouse.position=(500,400)
			mouse.click(Button.left,1)
			speak(np.random.choice(['sure sir','yes sir','ok sir']))
			if 'play' in query:
				adjustmic()

		elif 'next' in query or 'change song' in query:
			keyboard.press_and_release('shift+n')
			next_text = np.random.choice(['next one coming up right away sir!',"here's the next one",'going next sir','aye aye sir, here is the next one'])
			speak(next_text)
			ad_skipped=False
			if process_exists('chrome.exe') == True:
				while ad_skipped==False:
					try:
						ad_exists = False
						skip = driver.find_element_by_class_name('ytp-ad-skip-button-container')
						ad_exists = True
						skip.click()
						ad_skipped=True
					except:
						ad_skipped=False
						if ad_exists==True:
							speak(np.random.choice(['let me skip the ad sir','just a moment! sir']))
							time.sleep(3)
						continue

		elif 'previous' in query or 'back' in query:
			mouse = Controller()
			mouse.position=(60,50)
			mouse.click(Button.left,1)
			speak('going back sir')

		elif 'close tab' in query or 'close the tab' in query:
			keyboard.press_and_release('ctrl+w')
			speak('tab closed')

		elif 'open opera' in query or 'opera' in query:
			os.startfile('C:\\Users\\Harshal\\AppData\\Local\\Programs\\Opera\\launcher.exe')
			speak('opened up opera browser')

		elif 'close window' in query or 'close the window' in query:
			keyboard.press_and_release('alt+f4')
			speak('window closed')

		elif 'this is my' in query:
			split_query = query.split()
			speak('hello {} I am John Watson. Nice to meet you.'.format(split_query[-1]))

		elif 'open sublime' in query:
			keyboard.press_and_release('cmd+d')
			mouse = Controller()
			mouse.position=(860,140)
			pause = 0
			for i in range(300):
					pause += 1
			pause = 0
			mouse.click(Button.left,2)
			speak('coming up on window, your favourite toy, sir. Enjoy')

		elif 'switch window' in query:
			keyboard.press_and_release('alt+tab')
			speak(np.random.choice(['ok sir','yes sir','sure sir']))
			speak('window switched')

		elif 'roll a die' in query  or 'rohan or die' in query or 'roll or die' in query:
			speak('rolling a die')
			speak(np.random.choice(['and, and, and','annnd','ah ha','okaay','hmmmmm']))
			speak('It is a {}'.format(np.random.randint(1,7)))

		elif 'roll a dice' in query:
			speak('rolling dice now')
			speak(np.random.choice(['annnd','ah ha','hmmmmm']))
			speak('It is a {} and a {}'.format(np.random.randint(1,7),np.random.randint(1,7)))

		elif 'toss a coin' in query:
			speak('tossing a coin now')
			speak(np.random.choice(['and, and, and','ah ha','okaay,','hmmmmm']))
			speak('it is {}'.format(np.random.choice(['heads','tails'])))

		elif query == 'awesome' or query == 'great' or query == 'good' or query == 'nice' or query == 'cool':
			awesome_temp = ['yeaaa sir','awesome','all good','cool','great!']
			speak(np.random.choice(awesome_temp))

		elif 'thank' in query:
			speak(np.random.choice(['happy to help sir','you are welcome sir','welcome!']))

		elif 'volume' in query:
			temp_vol_query = query.split()
			vol = temp_vol_query[-1]
			max_vol = temp_vol_query[-2]
			print(vol)
			temp_vol = 0
			if vol == 'one' or vol == '1' or vol == 'ten' or vol=='10':
				temp_vol = 0.1
			elif vol == 'two' or vol == '2' or vol == 'to' or vol=='twelve' or vol=='12':
				temp_vol = 0.2
			elif vol == 'three' or vol == '3' or vol=='thirteen' or vol=='13':
				temp_vol = 0.3
			elif vol == 'four' or vol == '4' or vol == 'for' or vol == 'fourteen' or vol=='14':
				temp_vol = 0.4
			elif vol == 'five' or vol == '5' or vol == 'fifteen' or vol == '15' or vol == 'half':
				temp_vol = 0.5
			elif vol == 'six' or vol == '6' or vol == 'sixteen' or vol == '16':
				temp_vol = 0.6
			elif vol == 'seven' or vol == '7' or vol == 'seventeen' or vol == '17':
				temp_vol = 0.7
			elif vol == 'eight' or vol == '8' or vol == 'eighteen' or vol == '18':
				temp_vol = 0.8
			elif vol == 'nine' or vol == '9' or vol == 'nineteen' or vol == '9':
				temp_vol = 0.9
			elif vol == 'mute' or vol == '0' or vol == 'zero' or max_vol=='mute':
				temp_vol = 0.0
				vol = 'mute'
			elif vol == 'max' or vol == 'maximum' or vol == 'full' or max_vol == 'maximum' or max_vol=='full' or max_vol=='max':
				temp_vol = 1.0
				vol = 'maximum'
			else:
				sessions = AudioUtilities.GetAllSessions()
				for session in sessions:
					volume = session._ctl.QueryInterface(ISimpleAudioVolume)
					if session.Process and session.Process.name() == "chrome.exe":
						print('not changing and keeping it on:',volume.GetMasterVolume())
						temp_vol = volume.GetMasterVolume()
			sessions = AudioUtilities.GetAllSessions()
			for session in sessions:
				volume = session._ctl.QueryInterface(ISimpleAudioVolume)
				if session.Process and session.Process.name() == "chrome.exe":
					print(volume.GetMasterVolume())
					volume.SetMasterVolume(temp_vol, None)
			print('volume set on {}'.format(vol))
			speak('volume set on {}'.format(vol))


		elif ('get some rest' in query) or ('get some sleep' in query) or 'rest' in query or 'stop listening' in query:
			speak("Ok sir, I will be here if you need anything")
			break


		if process_exists('chrome.exe') == True:
			try:
				skip = driver.find_element_by_class_name('ytp-ad-skip-button-container')
				speak(np.random.choice(['let me skip the ad sir','just a moment! sir']))
				skip.click()
			except:
				continue

