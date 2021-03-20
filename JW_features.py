### imports
import datetime
import subprocess
# selenium imports:
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pynput.keyboard import Key

### Features of JW:
# to note down something in Notepad:
def note(text):
	date = datetime.datetime.now()
	file_name = str(date).replace(":","-") + "_note.txt"
	with open("Quick_notes//" + file_name,'w') as f:
		f.write(text)
	subprocess.Popen(["notepad.exe","Quick_notes//" + file_name])

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

# update the list of tabs that are open in google chrome:
def update_windows_list(new_tab_name,windows_names_dict,driver):
	all_windows = driver.window_handles
	print(list(windows_names_dict.values()))
	print(list(windows_names_dict.keys()))
	print(all_windows)
	new_handle = [x for x in all_windows if x not in list(windows_names_dict.values())][0]
	windows_names_dict[new_tab_name] = new_handle
	driver.switch_to_window(new_handle)

# to switch from one tab to another in google chrome:
def switch_tab_driver(new_tab_name,windows_names_dict,driver):
	driver.switch_to_window(windows_names_dict[new_tab_name])
	pass

# to adjust PC volume:
def adjust_pc_volume(vol,pc_volume,keyboard):
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

# clear "I Agree" pop-up from google:
def click_i_agree(i_agree,driver):
	retry_counter = 0
	while i_agree == False:
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
	return i_agree

# clicking "No Thanks" google pop-up in google chrome:
def click_no_thanks(no_thanks,driver):
	retry_counter = 0
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
	return no_thanks