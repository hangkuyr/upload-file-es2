import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller
from pyvirtualdisplay import Display

    

def test_first_case_selenium():

	display = Display(visible=0, size=(800, 800))  
	display.start()

	chromedriver_autoinstaller.install()

	chrome_options = webdriver.ChromeOptions()    
	# Add your options as needed    
	options = [
	  # Define window size here
	   "--window-size=1200,1200",
	    "--ignore-certificate-errors"
	 
	    "--headless",
	    #"--disable-gpu",
	    #"--window-size=1920,1200",
	    #"--ignore-certificate-errors",
	    #"--disable-extensions",
	    "--no-sandbox",
	    "--disable-dev-shm-usage",
	    #'--remote-debugging-port=9222'
	]

	for option in options:
	    chrome_options.add_argument(option)

    
	driver = webdriver.Chrome(options = chrome_options)
	
	driver.get("localhost:80")
	assert " Upload File" == driver.title