import pytest
from selenium import webdriver

@pytest.fixture
def browser():
	driver = webdriver.Firefox()

	yield driver

	driver.quit()

def test_first_case_selenium(browser):
	
	browser.get("http://127.0.0.1:80")
	browser.maximize_window()
	assert "Upload File" == browser.title