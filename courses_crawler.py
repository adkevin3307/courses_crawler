import json
import time
import tqdm
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from course import Course

def get_courses(browser):
    print('========== get courses ==========')
    # defualt content -> mainFrame(outer)
    courses = []
    browser.switch_to.frame(browser.find_element_by_name('mainFrame'))
    browser.implicitly_wait(30)
    # select fauclty and get all courses
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
        total_rows = int(browser.find_element_by_id('PC_TotalRow').text)
        if total_rows != 0:
            # set display rows to 1000
            if i == 0:
                browser.execute_script('$("#PC_PageSize").attr("value", 1000)')
                browser.find_element_by_id('PC_ShowRows').send_keys(Keys.ENTER)
                time.sleep(1)
            # get course information
            for row in tqdm.tqdm(range(2, 2 + total_rows)):
                # open fancybox
                browser.execute_script('__doPostBack("DataGrid$ctl{:02d}$COSID", "")'.format(row))
                time.sleep(0.5)
                # mainFrame(outer) -> iframe -> mainFrame(inner)
                browser.switch_to.frame(browser.find_element_by_tag_name('iframe'))
                browser.switch_to.frame(browser.find_element_by_name('mainFrame'))
                # initialize Course and get information
                courses.append(Course().get_information(browser))
                # mainFrame(inner) -> iframe -> mainFrame(outer)
                browser.switch_to.parent_frame()
                browser.switch_to.parent_frame()
                # close fancybox
                browser.execute_script('top.mainFrame.$.fancybox.close()')
                time.sleep(0.5)
    return courses

if __name__ == '__main__':
    with webdriver.Chrome() as browser:
        browser.get('https://ais.ntou.edu.tw/outside.aspx?mainPage=LwBBAHAAcABsAGkAYwBhAHQAaQBvAG4ALwBUAEsARQAvAFQASwBFADIAMgAvAFQASwBFADIAMgAxADEAXwAuAGEAcwBwAHgAPwBwAHIAbwBnAGMAZAA9AFQASwBFADIAMgAxADEA')
        courses = get_courses(browser)

    with open('courses.json', 'w') as file:
        json.dump(courses, file, ensure_ascii = False, indent = 4, default = lambda x: x.__dict__)