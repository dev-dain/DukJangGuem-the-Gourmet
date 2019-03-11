# 다음주 식단을 미리 크롤링함
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep
import os

options = Options()
options.headless = True

driver = webdriver.Firefox(options=options)
driver.implicitly_wait(5)
driver.get('http://www.duksung.ac.kr/diet/schedule.do?menuId=1151')
driver.implicitly_wait(5)

driver.execute_script('nextWeekday(1)')
sleep(3)

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
contents_div = soup.find(id='schedule-table')

info_str = contents_div.find_all("th")
temp_str = contents_div.find_all("td")

for i in range(len(temp_str)):
    temp_str[i] = temp_str[i].get_text('\n')+'\r\r'
    # get_text('\n')이 <br /> 코드를 '\n'으로 바꿔줌

for j in range(len(info_str)):
    info_str[j] = info_str[j].get_text('\n')+'\r\r'

if os.path.exists('week_meal.txt'):
    os.remove('week_meal.txt')

meal_fp = open('week_meal.txt', 'w', encoding='utf-8')
meal_fp.writelines(temp_str)
meal_fp.close()

if os.path.exists('week_info.txt'):
    os.remove('week_info.txt')

info_fp = open('week_info.txt', 'w', encoding='utf-8')
info_fp.writelines(info_str)
info_fp.close()

driver.close()
