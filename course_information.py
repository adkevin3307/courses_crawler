import time

def initialize():
    course = {
        'basic_information': {
            'year_semester': '',
            'course_id': '',
            'faculty_name': '',
            'professor': '',
            'course_name': {
                'chinese': '',
                'english': ''
            },
            'grade': '',
            'credit': 0,
            'hour': 0,
            'max_student': 0,
            'min_student': 0,
            '選課類別': '',
            '開課期限': '',
            '是否實習': '',
            'class_schedule': [],
            'classroom': [],
            'main_field': '',
            'sub_field': '',
            '選課人數': 0,
            'description': '',
            'co_professors': []
        },
        'core_ability': '',
        '課程綱要': {
            'objective': {
                'chinese': '',
                'english': ''
            },
            'pre_course': {
                'chinese': '',
                'englist': ''
            },
            'outline': {
                'chinese': '',
                'english': ''
            },
            'teaching_method': {
                'chinese': '',
                'english': ''
            },
            'reference': {
                'chinese': '',
                'english': ''
            },
            'syllabus': {
                'chinese': '',
                'english': ''
            },
            'evaluation': {
                'chinese': '',
                'english': ''
            },
            'reference_link': ''
        }
    }
    return course

def get_course_information(browser):
    print('========== get course information ==========')

    browser.switch_to.frame(browser.find_element_by_tag_name('iframe'))
    browser.switch_to.frame(browser.find_element_by_name('mainFrame'))
    browser.implicitly_wait(30)

    print(browser.find_element_by_id('M_COSID').text)

    course = initialize()
    # basic information
    course['basic_information']['year_semester'] = browser.find_element_by_id('M_AYEARSMS').text
    course['basic_information']['course_id'] = browser.find_element_by_id('M_COSID').text
    course['basic_information']['faculty_name'] = browser.find_element_by_id('M_FACULTY_NAME').text
    course['basic_information']['professor'] = browser.find_element_by_id('M_LECTR_TCH_CH').text
    course['basic_information']['course_name']['chinese'] = browser.find_element_by_id('CH_LESSON').text
    course['basic_information']['course_name']['english'] = browser.find_element_by_id('M_ENG_LESSON').text
    course['basic_information']['grade'] = browser.find_element_by_id('M_GRADE').text
    course['basic_information']['credit'] = int(browser.find_element_by_id('M_CRD').text)
    course['basic_information']['hour'] = int(browser.find_element_by_id('M_LECTR_HOUR').text)
    course['basic_information']['max_student'] = int(browser.find_element_by_id('M_MAX_ST').text)
    course['basic_information']['min_student'] = int(browser.find_element_by_id('M_MIN_ST').text)
    course['basic_information']['選課類別'] = browser.find_element_by_id('M_MUST').text
    course['basic_information']['開課期限'] = browser.find_element_by_id('M_COSTERM').text
    course['basic_information']['是否實習'] = browser.find_element_by_id('M_CLASS_LAB').text
    course['basic_information']['class_schedule'] = browser.find_element_by_id('M_SEG').text.split(',')
    course['basic_information']['classroom'] = browser.find_element_by_id('M_CLSSRM_ID').text.split(',')
    course['basic_information']['main_field'] = browser.find_element_by_id('M_MAIN_NAME').text
    course['basic_information']['sub_field'] = browser.find_element_by_id('M_CHILD_NAME').text
    course['basic_information']['選課人數'] = int(browser.find_element_by_id('M_CHOICE_QTY').text)
    course['basic_information']['description'] = browser.find_element_by_id('M_DESCRIPTION').text
    course['basic_information']['co_professors'] = browser.find_element_by_id('TCH_NAME_LIST').text.split(',')
    # core ability
    course['core_ability'] = browser.find_element_by_id('L_CORE_ABILITY').text
    # 課程綱要
    course['課程綱要']['objective']['chinese'] = browser.find_element_by_id('M_CH_TARGET').text
    course['課程綱要']['objective']['english'] = browser.find_element_by_id('M_ENG_TARGET').text
    course['課程綱要']['pre_course']['chinese'] = browser.find_element_by_id('M_CH_PREOBJ').text
    course['課程綱要']['pre_course']['english'] = browser.find_element_by_id('M_ENG_PREOBJ').text
    course['課程綱要']['outline']['chinese'] = browser.find_element_by_id('M_CH_OBJECT').text
    course['課程綱要']['outline']['english'] = browser.find_element_by_id('M_ENG_OBJECT').text
    course['課程綱要']['teaching_method']['chinese'] = browser.find_element_by_id('M_CH_TEACH').text
    course['課程綱要']['teaching_method']['english'] = browser.find_element_by_id('M_ENG_TEACH').text
    course['課程綱要']['reference']['chinese'] = browser.find_element_by_id('M_CH_REF').text
    course['課程綱要']['reference']['english'] = browser.find_element_by_id('M_ENG_REF').text
    course['課程綱要']['syllabus']['chinese'] = browser.find_element_by_id('M_CH_TEACHSCH').text
    course['課程綱要']['syllabus']['english'] = browser.find_element_by_id('M_ENG_TEACHSCH').text
    course['課程綱要']['evaluation']['chinese'] = browser.find_element_by_id('M_CH_TYPE').text
    course['課程綱要']['evaluation']['english'] = browser.find_element_by_id('M_ENG_TYPE').text
    course['課程綱要']['reference_link'] = browser.find_element_by_id('M_DOWNLOAD_ADDR').text

    browser.find_element_by_id('Button1').click()

    browser.switch_to.parent_frame()
    browser.switch_to.parent_frame()

    return course