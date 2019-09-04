import json
import time
import getpass
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

import course_information

def login(browser, data):
    print('========== login ==========')

    browser.get('https://ais.ntou.edu.tw/Default.aspx')
    browser.find_element_by_name('M_PORTAL_LOGIN_ACNT').send_keys(data['account'])
    browser.find_element_by_name('M_PW').send_keys(data['password'])
    browser.find_element_by_name('LGOIN_BTN').click()

def select_menu(browser):
    print('========== select menu ==========')

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

    select = Select(browser.find_element_by_id('Q_FACULTY_CODE'))
    for option in select.options:
        print(option.get_attribute('value'))

        select.select_by_value(option.get_attribute('value'))
        browser.find_element_by_id('QUERY_BTN1').click()
        time.sleep(0.5)
        # judge display row amount
        total_row = int(browser.find_element_by_id('PC_TotalRow').text)
        browser.find_element_by_id('PC_PageSize').send_keys('00')
        browser.find_element_by_id('PC_ShowRows').send_keys(Keys.ENTER)

        # get per course information
        for course_id in range(2, 2 + total_row):
            course_id = str(course_id) if course_id >= 10 else ('0' + str(course_id))
            script = '__doPostBack("DataGrid$ctl{}$COSID", "")'.format(course_id)
            print(script)
            browser.execute_script(script)
            courses.append(course_information.get_course_information(browser))
    return courses

if __name__ == '__main__':
    account = input('Account: ')
    password = getpass.getpass()

    courses = []

    with webdriver.Chrome() as browser:
        login(browser, {'account': account, 'password': password})

        browser.get("https://ais.ntou.edu.tw/MainFrame.aspx")

        select_menu(browser)
        browser.switch_to.default_content()
        courses = get_courses(browser)

    print('========== courses ==========')
    
    print(len(courses))
    with open('courses.json', 'w') as file:
        json.dump(courses, file)