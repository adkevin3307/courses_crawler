class Course:
    def __init__(self):
        self.basic_information = {
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
        }
        self.core_ability = ''
        self.curriculum_guidelines = {
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

    def _processing(self):
        # remove ' ' in class_schedule
        while ' ' in self.basic_information['class_schedule']:
            self.basic_information['class_schedule'].remove(' ')
        # remove ' ' in classroom
        while ' ' in self.basic_information['classroom']:
            self.basic_information['classroom'].remove(' ')
        # remove ' ' in co_professors
        while ' ' in self.basic_information['co_professors']:
            self.basic_information['co_professors'].remove(' ')

    def get_information(self, browser):
        # basic information
        self.basic_information['year_semester'] = browser.find_element_by_id('M_AYEARSMS').text
        self.basic_information['course_id'] = browser.find_element_by_id('M_COSID').text
        self.basic_information['faculty_name'] = browser.find_element_by_id('M_FACULTY_NAME').text
        self.basic_information['professor'] = browser.find_element_by_id('M_LECTR_TCH_CH').text
        self.basic_information['course_name']['chinese'] = browser.find_element_by_id('CH_LESSON').text
        self.basic_information['course_name']['english'] = browser.find_element_by_id('M_ENG_LESSON').text
        self.basic_information['grade'] = browser.find_element_by_id('M_GRADE').text
        self.basic_information['credit'] = int(browser.find_element_by_id('M_CRD').text)
        self.basic_information['hour'] = int(browser.find_element_by_id('M_LECTR_HOUR').text)
        self.basic_information['max_students'] = int(browser.find_element_by_id('M_MAX_ST').text)
        self.basic_information['min_students'] = int(browser.find_element_by_id('M_MIN_ST').text)
        self.basic_information['category'] = browser.find_element_by_id('M_MUST').text
        self.basic_information['duration'] = browser.find_element_by_id('M_COSTERM').text
        self.basic_information['internship'] = browser.find_element_by_id('M_CLASS_LAB').text
        self.basic_information['class_schedule'] = browser.find_element_by_id('M_SEG').text.split(',')
        self.basic_information['classroom'] = browser.find_element_by_id('M_CLSSRM_ID').text.split(',')
        self.basic_information['main_field'] = browser.find_element_by_id('M_MAIN_NAME').text
        self.basic_information['sub_field'] = browser.find_element_by_id('M_CHILD_NAME').text
        self.basic_information['students'] = int(browser.find_element_by_id('M_CHOICE_QTY').text)
        self.basic_information['description'] = browser.find_element_by_id('M_DESCRIPTION').text
        self.basic_information['co_professors'] = browser.find_element_by_id('TCH_NAME_LIST').text.split(',')
        # core ability
        self.core_ability = browser.find_element_by_id('L_CORE_ABILITY').text
        # curriculum_guidelines
        self.curriculum_guidelines['objective']['chinese'] = browser.find_element_by_id('M_CH_TARGET').text
        self.curriculum_guidelines['objective']['english'] = browser.find_element_by_id('M_ENG_TARGET').text
        self.curriculum_guidelines['pre_course']['chinese'] = browser.find_element_by_id('M_CH_PREOBJ').text
        self.curriculum_guidelines['pre_course']['english'] = browser.find_element_by_id('M_ENG_PREOBJ').text
        self.curriculum_guidelines['outline']['chinese'] = browser.find_element_by_id('M_CH_OBJECT').text
        self.curriculum_guidelines['outline']['english'] = browser.find_element_by_id('M_ENG_OBJECT').text
        self.curriculum_guidelines['teaching_method']['chinese'] = browser.find_element_by_id('M_CH_TEACH').text
        self.curriculum_guidelines['teaching_method']['english'] = browser.find_element_by_id('M_ENG_TEACH').text
        self.curriculum_guidelines['reference']['chinese'] = browser.find_element_by_id('M_CH_REF').text
        self.curriculum_guidelines['reference']['english'] = browser.find_element_by_id('M_ENG_REF').text
        self.curriculum_guidelines['syllabus']['chinese'] = browser.find_element_by_id('M_CH_TEACHSCH').text
        self.curriculum_guidelines['syllabus']['english'] = browser.find_element_by_id('M_ENG_TEACHSCH').text
        self.curriculum_guidelines['evaluation']['chinese'] = browser.find_element_by_id('M_CH_TYPE').text
        self.curriculum_guidelines['evaluation']['english'] = browser.find_element_by_id('M_ENG_TYPE').text
        self.curriculum_guidelines['reference_link'] = browser.find_element_by_id('M_DOWNLOAD_ADDR').text
        # processing course information
        self._processing()
        return self