from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import setting as S
import traceback
import time


contest_title = S.Contest_Title

display_browser = False


chrome_service = service.Service(executable_path = S.chromedriver_path)
chrome_options = Options()
if not display_browser:
	chrome_options.add_argument('--headless')
driver = webdriver.Chrome(service = chrome_service, options = chrome_options)
wait = WebDriverWait(driver = driver, timeout = 60)

def display_All():
	dropdown = driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[6]/div/div/div[1]/div/div[1]/span')
	dropdown.find_element(by = By.TAG_NAME, value = 'button').click()
	time.sleep(0.3)
	ul = dropdown.find_element(by = By.TAG_NAME, value = 'ul')
	li = ul.find_elements(by = By.TAG_NAME, value = 'li')
	li[4].find_element(by = By.TAG_NAME, value = 'a').click()
	wait.until(EC.presence_of_all_elements_located)
	time.sleep(0.3)

def collect_past_log():
	driver.get('https://kenkoooo.com/atcoder/#/contest/recent')
	wait.until(EC.presence_of_all_elements_located)
	time.sleep(1)
	display_All()
	table =  driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[6]/div/div/div[2]/div[2]/table/tbody')
	tr = table.find_elements(by = By.TAG_NAME, value = 'tr')
	time.sleep(0.3)
	n = len(tr)
	for i in range(n):
		table =  driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[6]/div/div/div[2]/div[2]/table/tbody')
		tr = table.find_elements(by = By.TAG_NAME, value = 'tr')
		tds = tr[i].find_elements(by = By.TAG_NAME, value = 'td')
		title = tds[0].find_element(by = By.TAG_NAME, value = 'a').get_attribute("textContent")
		title = title[7:]
		print(title)
		date = tds[3].find_element(by = By.TAG_NAME, value = 'div').get_attribute("textContent")
		date = date.split(' ')[0]
		print(date)
		if title == contest_title:
			tds[0].find_element(by = By.TAG_NAME, value = 'a').click()
			wait.until(EC.presence_of_all_elements_located)
			time.sleep(1)
			file = open(S.Dir_path + '/past_log/' + date, 'w')
			table_2 = driver.find_element(by = By.XPATH, value = '//*[@id="root"]/div/div[2]/div[6]/div[2]/div/table/tbody')
			tr_2 = table_2.find_elements(by = By.TAG_NAME, value = 'tr')
			for problem in tr_2:
				tds_2 = problem.find_elements(by = By.TAG_NAME, value = 'td')
				problem_url = tds_2[0].find_element(by = By.TAG_NAME, value = 'a').get_attribute('href')
				problem_name = problem_url.split('/')[-1]
				file.write(problem_name + '\n')
			file.close()
			driver.back()
			wait.until(EC.presence_of_all_elements_located)
			time.sleep(1)
			display_All()


if __name__ == '__main__':
	try:
		collect_past_log()
	except Exception:
		print(traceback.format_exc())
	finally:
		driver.close()
