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
            'max_students': 0,
            'min_students': 0,
            'category': '',
            'duration': '',
            'internship': '',
            'class_schedule': [],
            'classroom': [],
            'main_field': '',
            'sub_field': '',
            'students': 0,
            'description': '',
            'co_professors': []
        },
        'core_ability': '',
        'curriculum_guidelines': {
            'objective': {
                'chinese': '',
                'english': ''
            },
            'pre_course': {
                'chinese': '',
                'english': ''
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

def processing_course_information(course):
    # remove ' ' in co-professors list
    while ' ' in course['basic_information']['co_professors']:
        course['basic_information']['co_professors'].remove(' ')

def get_course_information(browser, course_id):
    browser.execute_script('__doPostBack("DataGrid$ctl{}$COSID", "")'.format(course_id)) # open fancybox

    browser.switch_to.frame(browser.find_element_by_tag_name('iframe'))
    browser.switch_to.frame(browser.find_element_by_name('mainFrame'))

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
    course['basic_information']['max_students'] = int(browser.find_element_by_id('M_MAX_ST').text)
    course['basic_information']['min_students'] = int(browser.find_element_by_id('M_MIN_ST').text)
    course['basic_information']['category'] = browser.find_element_by_id('M_MUST').text
    course['basic_information']['duration'] = browser.find_element_by_id('M_COSTERM').text
    course['basic_information']['internship'] = browser.find_element_by_id('M_CLASS_LAB').text
    course['basic_information']['class_schedule'] = browser.find_element_by_id('M_SEG').text.split(',')
    course['basic_information']['classroom'] = browser.find_element_by_id('M_CLSSRM_ID').text.split(',')
    course['basic_information']['main_field'] = browser.find_element_by_id('M_MAIN_NAME').text
    course['basic_information']['sub_field'] = browser.find_element_by_id('M_CHILD_NAME').text
    course['basic_information']['students'] = int(browser.find_element_by_id('M_CHOICE_QTY').text)
    course['basic_information']['description'] = browser.find_element_by_id('M_DESCRIPTION').text
    course['basic_information']['co_professors'] = browser.find_element_by_id('TCH_NAME_LIST').text.split(',')
    # core ability
    course['core_ability'] = browser.find_element_by_id('L_CORE_ABILITY').text
    # curriculum_guidelines
    course['curriculum_guidelines']['objective']['chinese'] = browser.find_element_by_id('M_CH_TARGET').text
    course['curriculum_guidelines']['objective']['english'] = browser.find_element_by_id('M_ENG_TARGET').text
    course['curriculum_guidelines']['pre_course']['chinese'] = browser.find_element_by_id('M_CH_PREOBJ').text
    course['curriculum_guidelines']['pre_course']['english'] = browser.find_element_by_id('M_ENG_PREOBJ').text
    course['curriculum_guidelines']['outline']['chinese'] = browser.find_element_by_id('M_CH_OBJECT').text
    course['curriculum_guidelines']['outline']['english'] = browser.find_element_by_id('M_ENG_OBJECT').text
    course['curriculum_guidelines']['teaching_method']['chinese'] = browser.find_element_by_id('M_CH_TEACH').text
    course['curriculum_guidelines']['teaching_method']['english'] = browser.find_element_by_id('M_ENG_TEACH').text
    course['curriculum_guidelines']['reference']['chinese'] = browser.find_element_by_id('M_CH_REF').text
    course['curriculum_guidelines']['reference']['english'] = browser.find_element_by_id('M_ENG_REF').text
    course['curriculum_guidelines']['syllabus']['chinese'] = browser.find_element_by_id('M_CH_TEACHSCH').text
    course['curriculum_guidelines']['syllabus']['english'] = browser.find_element_by_id('M_ENG_TEACHSCH').text
    course['curriculum_guidelines']['evaluation']['chinese'] = browser.find_element_by_id('M_CH_TYPE').text
    course['curriculum_guidelines']['evaluation']['english'] = browser.find_element_by_id('M_ENG_TYPE').text
    course['curriculum_guidelines']['reference_link'] = browser.find_element_by_id('M_DOWNLOAD_ADDR').text

    browser.switch_to.parent_frame()
    browser.switch_to.parent_frame()

    browser.execute_script('top.mainFrame.$.fancybox.close()') # close fancybox

    processing_course_information(course)

    return course