### imports
import subprocess
# imports for audio processing:
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import pyttsx3
import datetime
import numpy as np
import speech_recognition as sr
import time

### Function declarations:
# initializing output voice:
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
for i in range(len(voices)):
	if i == 0:
		engine.setProperty('voice', voices[i].id)

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
	sessions = AudioUtilities.GetAllSessions()
	for session in sessions:
		volume = session._ctl.QueryInterface(ISimpleAudioVolume)
		if session.Process and (session.Process.name() == "chrome.exe" or session.Process.name() == "vlc.exe"):
			volume.SetMasterVolume(0.2, None)
	engine.say(audio)
	engine.runAndWait()
	for session in sessions:
		volume = session._ctl.QueryInterface(ISimpleAudioVolume)
		if session.Process and (session.Process.name() == "chrome.exe" or session.Process.name() == "vlc.exe"):
			volume.SetMasterVolume(0.9, None)

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