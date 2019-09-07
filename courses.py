import json
import time
import tqdm
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

import course_information

def get_courses(browser):
    print('========== get courses ==========')

    courses = []
    browser.switch_to.frame(browser.find_element_by_name('mainFrame'))
    browser.implicitly_wait(30)

    options = list(map(lambda x: x.get_attribute('value'), Select(browser.find_element_by_id('Q_FACULTY_CODE')).options))
    for i, option in enumerate(options):
        # select and print current faculty
        select = Select(browser.find_element_by_id('Q_FACULTY_CODE'))
        select.select_by_value(option)
        print('{} / {}: {}'.format(i + 1, len(options), select.first_selected_option.text))
        # click button and wait for render
        browser.find_element_by_id('QUERY_BTN1').click()
        time.sleep(2)
        # check total row amount
        total_row = int(browser.find_element_by_id('PC_TotalRow').text)
        if total_row != 0:
            # adjust display row
            if i == 0:
                browser.execute_script('$("#PC_PageSize").attr("value", 1000)')
                browser.find_element_by_id('PC_ShowRows').send_keys(Keys.ENTER)
                time.sleep(1)
            # get per course information
            for course_id in tqdm.tqdm(range(2, 2 + total_row)):
                course_id = str(course_id) if course_id >= 10 else ('0' + str(course_id))
                courses.append(course_information.get_course_information(browser, course_id))
                time.sleep(1)
    return courses

if __name__ == '__main__':
    with webdriver.Chrome() as browser:
        browser.get('https://ais.ntou.edu.tw/outside.aspx?mainPage=LwBBAHAAcABsAGkAYwBhAHQAaQBvAG4ALwBUAEsARQAvAFQASwBFADIAMgAvAFQASwBFADIAMgAxADEAXwAuAGEAcwBwAHgAPwBwAHIAbwBnAGMAZAA9AFQASwBFADIAMgAxADEA')
        courses = get_courses(browser)

    with open('courses.json', 'w') as file:
        json.dump(courses, file, ensure_ascii = False, indent = 4)