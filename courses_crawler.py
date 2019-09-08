import json
import time
import threading
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from course import Course

def get_courses(browser, selections, thread_name):
    # defualt content -> mainFrame(outer)
    courses = []
    browser.switch_to.frame(browser.find_element_by_name('mainFrame'))
    browser.implicitly_wait(30)
    for i, selection in enumerate(selections):
        # select and print current faculty
        select = Select(browser.find_element_by_id('Q_FACULTY_CODE'))
        select.select_by_value(selection)
        faculty_name = select.first_selected_option.text
        # click button and wait for render
        browser.find_element_by_id('QUERY_BTN1').click()
        time.sleep(2)
        # check total row amount
        total_rows = int(browser.find_element_by_id('PC_TotalRow').text)
        print('{}: {} / {}, {}, {} rows'.format(thread_name, i + 1, len(selections), faculty_name, total_rows))
        if total_rows != 0:
            # set display rows to 1000
            if int(browser.find_element_by_id('PC_PageSize').get_attribute('value')) != 1000:
                browser.execute_script('$("#PC_PageSize").attr("value", 1000)')
                browser.find_element_by_id('PC_ShowRows').send_keys(Keys.ENTER)
                time.sleep(1)
            # get course information
            for row in range(2, 2 + total_rows):
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

def parrallel(courses, selections):
    thread_name = threading.current_thread().getName()
    print('=============== {} Start ==============='.format(thread_name))
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    with webdriver.Chrome(options = options) as browser:
        browser.get('https://ais.ntou.edu.tw/outside.aspx?mainPage=LwBBAHAAcABsAGkAYwBhAHQAaQBvAG4ALwBUAEsARQAvAFQASwBFADIAMgAvAFQASwBFADIAMgAxADEAXwAuAGEAcwBwAHgAPwBwAHIAbwBnAGMAZAA9AFQASwBFADIAMgAxADEA')
        courses.extend(get_courses(browser, selections, thread_name))
    print('=============== {} Done ==============='.format(thread_name))

def get_selections(browser_amount):
    selections = []
    # set chrome options
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # get selections
    with webdriver.Chrome(options = options) as browser:
        browser.get('https://ais.ntou.edu.tw/outside.aspx?mainPage=LwBBAHAAcABsAGkAYwBhAHQAaQBvAG4ALwBUAEsARQAvAFQASwBFADIAMgAvAFQASwBFADIAMgAxADEAXwAuAGEAcwBwAHgAPwBwAHIAbwBnAGMAZAA9AFQASwBFADIAMgAxADEA')
        print('=============== get selections ===============')
        browser.switch_to.frame(browser.find_element_by_name('mainFrame'))
        browser.implicitly_wait(30)
        all_selections = list(map(lambda x: x.get_attribute('value'), Select(browser.find_element_by_id('Q_FACULTY_CODE')).options))
    # split list to browser_amount part
    average = len(all_selections) / browser_amount
    index = 0.0
    while index < len(all_selections):
        selections.append(all_selections[int(index): int(index + average)])
        index += average
    # print selections
    for selection in selections:
        print(selection)
    return selections

if __name__ == '__main__':
    # initialize variables
    courses = []
    threads = []
    browser_amount = int(input('Amount of Browsers: '))
    selections = get_selections(browser_amount)
    # get courses
    print('=============== get courses ===============')
    for i in range(browser_amount):
        threads.append(threading.Thread(target = parrallel, args = (courses, selections[i]), name = 'Thread {}'.format(i + 1)))
        threads[i].start()
    # wait all browsers and close them
    for i in range(browser_amount):
        threads[i].join()
    # dump to courses.json
    with open('courses.json', 'w') as file:
        json.dump(courses, file, ensure_ascii = False, indent = 4, default = lambda x: x.__dict__)