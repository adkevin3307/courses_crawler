import json
import time
import tqdm
import getpass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

import course_information

def login(browser, data):
    browser.get('https://ais.ntou.edu.tw/Default.aspx')
    browser.find_element_by_name('M_PORTAL_LOGIN_ACNT').send_keys(data['account'])
    browser.find_element_by_name('M_PW').send_keys(data['password'])
    browser.find_element_by_name('LGOIN_BTN').click()

def select_menu(browser):
    browser.switch_to.frame(browser.find_element_by_name('menuFrame'))
    browser.implicitly_wait(30)

    browser.find_element_by_id("Menu_TreeViewt1").click() # 教學務系統
    browser.find_element_by_id('Menu_TreeViewt25').click() # 選課系統
    browser.find_element_by_id('Menu_TreeViewt34').click() # 課程課表查詢

def get_courses(browser):
    print('========== get courses ==========')

    courses = []
    browser.switch_to.frame(browser.find_element_by_name('mainFrame'))
    browser.implicitly_wait(30)

    options = list(map(lambda x: x.get_attribute('value'), Select(browser.find_element_by_id('Q_FACULTY_CODE')).options))
    for i, option in enumerate(options):
        print(option)
        Select(browser.find_element_by_id('Q_FACULTY_CODE')).select_by_value(option)
        browser.find_element_by_id('QUERY_BTN1').click()
        time.sleep(2)
        # judge display row amount
        total_row = int(browser.find_element_by_id('PC_TotalRow').text)
        if total_row == 0:
            continue
        if i == 0:
            browser.find_element_by_id('PC_PageSize').send_keys('00')
            browser.find_element_by_id('PC_ShowRows').send_keys(Keys.ENTER)
            time.sleep(1)
        # get per course information
        for course_id in tqdm.tqdm(range(2, 2 + total_row)):
            course_id = str(course_id) if course_id >= 10 else ('0' + str(course_id))
            browser.execute_script('__doPostBack("DataGrid$ctl{}$COSID", "")'.format(course_id))
            courses.append(course_information.get_course_information(browser))
    return courses

if __name__ == '__main__':
    courses = []
    account = input('Account: ')
    password = getpass.getpass()

    with webdriver.Chrome() as browser:
        login(browser, {'account': account, 'password': password})

        browser.get("https://ais.ntou.edu.tw/MainFrame.aspx")

        select_menu(browser)
        browser.switch_to.default_content()
        courses = get_courses(browser)

    with open('courses.json', 'w') as file:
        json.dump(courses, file)