from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QHBoxLayout, QWidget, QPushButton, QStackedLayout, QFormLayout, QLabel, QRadioButton, 
    QButtonGroup, QCheckBox, QLineEdit
    )
from pyqt6_multiselect_combobox import MultiSelectComboBox
from PyQt6.QtCore import Qt, QTimer, QObject, pyqtSignal, QRunnable, pyqtSlot, QThreadPool
from ui.data import *
from services.linkdin_scraper import *

class WorkerSignals(QObject):
    finished = pyqtSignal()

class Worker(QRunnable):
    def __init__(self, function, *args, **kwargs):
        super().__init__()
        self.args = args
        self.kwargs = kwargs
        self.function = function
        self.signals = WorkerSignals()
    
    @pyqtSlot()
    def run(self):
        self.function(*self.args, **self.kwargs)

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.threadpool = QThreadPool()

        self.setWindowTitle('Job Tracker')
        self.stacked_layout = QStackedLayout()

        self.page1 = QWidget()
        self.page2 = QWidget()
        self.page3 = QWidget()

        self.page1_layout = QFormLayout()
        self.page2_layout = QFormLayout()
        self.page3_layout = QFormLayout()

        self.page1.setLayout(self.page1_layout)
        self.page2.setLayout(self.page2_layout)
        self.page3.setLayout(self.page3_layout)

        self.timer = QTimer(self)

        # page 1 setup
            # row one
        self.label1 = QLabel('Please enter your job titles and skills')
        self.label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.page1_layout.addRow(self.label1)

            # row two
        self.skills = MultiSelectComboBox()
        self.skills.addItems(linkedin_skills)
        self.titles = MultiSelectComboBox()
        self.titles.addItems(linkedin_job_titles)
        self.row12 = QHBoxLayout()
        self.row12.addWidget(QLabel('Titles: '))
        self.row12.addWidget(self.titles)
        self.row12.addWidget(QLabel('Skills: '))
        self.row12.addWidget(self.skills)
        self.page1_layout.addRow(self.row12)

            # row three
        self.country = QLineEdit()
        self.country.setPlaceholderText('Default: Iran')
        self.page1_layout.addRow(QLabel('Country: '), self.country)

            # row four
        self.filter = QPushButton('Filter Jobs')
        self.filter.clicked.connect(self.__filter_check)
        self.search = QPushButton('Search')
        self.search.clicked.connect(self.__check_scope)
        self.row13 = QHBoxLayout()
        self.row13.addWidget(self.search)
        self.row13.addWidget(self.filter)
        self.page1_layout.addRow(self.row13)

            # row five
        self.check = QLabel()
        self.check.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.page1_layout.addRow(self.check)

            # row six
        self.quit = QPushButton('Quit')
        self.quit.clicked.connect(self.__quit)
        self.page1_layout.addRow(self.quit)

            # row seven
        self.login = QPushButton('Log out from account')
        self.login.clicked.connect(self.__delete_log)
        self.page1_layout.addRow(self.login)

        # page 2 setup
            # row one
        self.row21 = QHBoxLayout()
        self.button21 = QButtonGroup()
        self.rece = QRadioButton('Most recent')
        self.relev = QRadioButton('Most relevant')
        self.button21.addButton(self.rece)
        self.button21.addButton(self.relev)
        self.row21.addWidget(QLabel('Sort by: '))
        self.row21.addWidget(self.rece)
        self.row21.addWidget(self.relev)
        self.clear_button = QPushButton('Unselect')
        self.clear_button.clicked.connect(self.__uncheck_radio_button)
        self.row21.addWidget(self.clear_button)
        self.page2_layout.addRow(self.row21)

            # row two
        self.button22 = QButtonGroup()
        self.anyt = QRadioButton('Any time')
        self.pasm = QRadioButton('Past month')
        self.pasw = QRadioButton('Past week')
        self.pash = QRadioButton('Past 24 hours')
        self.button22.addButton(self.anyt)
        self.button22.addButton(self.pasm)
        self.button22.addButton(self.pasw)
        self.button22.addButton(self.pash)
        self.row22 = QHBoxLayout()
        self.row22.addWidget(QLabel('Date pasted: '))
        self.row22.addWidget(self.anyt)
        self.row22.addWidget(self.pasm)
        self.row22.addWidget(self.pasw)
        self.row22.addWidget(self.pash)
        self.page2_layout.addRow(self.row22)

            # row three
        self.exprience = MultiSelectComboBox()
        self.exprience.setPlaceholderText('Exprience level')
        self.exprience.addItems(exprience_level)
        self.jobtype = MultiSelectComboBox()
        self.jobtype.setPlaceholderText('Job type')
        self.jobtype.addItems(job_type)
        self.remo = MultiSelectComboBox()
        self.remo.setPlaceholderText('Remote')
        self.remo.addItems(remote)
        self.row23 = QHBoxLayout()
        self.row23.addWidget(self.exprience)
        self.row23.addWidget(self.jobtype)
        self.row23.addWidget(self.remo)
        self.page2_layout.addRow(self.row23)

            # row four
        self.row24 = QHBoxLayout()
        self.easyapply = QCheckBox('Easy apply')
        self.hasverification = QCheckBox('Has verification')
        self.under = QCheckBox('Under 10 applicants')
        self.row24.addWidget(self.easyapply)
        self.row24.addWidget(self.hasverification)
        self.row24.addWidget(self.under)
        self.page2_layout.addRow(self.row24)

            # row five
        self.newsearch = QPushButton('Search')
        self.newsearch.clicked.connect(self.__execute_filter)
        self.page2_layout.addRow(self.newsearch)

            # row six
        self.quit = QPushButton('Quit')
        self.quit.clicked.connect(self.__quit)
        self.page2_layout.addRow(self.quit)

            # row seven
        self.back = QPushButton('Back to search page')
        self.back.clicked.connect(self.__back)
        self.page2_layout.addRow(self.back)


        # page 3 setup
            # row one
        self.start = QLabel('The process has been started')
        self.start.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.page3_layout.addRow(self.start)

            # row two
        self.showjob = QLabel()
        self.showjob.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.page3_layout.addRow(self.showjob)

            # row three
        self.showpage = QLabel()
        self.showpage.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.page3_layout.addRow(self.showpage)

            # row four
        self.workdon = QLabel()
        self.workdon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.page3_layout.addRow(self.workdon)

        self.stacked_layout.addWidget(self.page1)
        self.stacked_layout.addWidget(self.page2)
        self.stacked_layout.addWidget(self.page3)
        self.stacked_layout.setCurrentIndex(0)

        central_widget = QWidget()
        central_widget.setLayout(self.stacked_layout)
        self.setCentralWidget(central_widget)

            # row five
        self.quit = QPushButton('Quit')
        self.quit.clicked.connect(self.__quit)
        self.page3_layout.addRow(self.quit)

    def __check_scope(self):
        if len(self.skills.currentData()) == 0 and len(self.titles.currentData()) == 0:
            self.check.setText('Please choose at least one skill or title')
        else:
            self.__go_to_search()
            self.__execute_no_filter()

    def __filter_check(self):
        if len(self.skills.currentData()) == 0 and len(self.titles.currentData()) == 0:
            self.check.setText('Please choose at least one skill or title')
        elif self.country.text() == '':
            self.check.setText('For filter, you have to choose another country')
        else:
            self.__go_to_filter()

    def __search_without_filter(self):
        self.__go_to_search()

        driver = Driver()
        my_driver = driver.init_driver()
        my_wait = driver.init_wait(my_driver)

        scope = {
            'title':self.skills.currentData(),
            'skill':self.titles.currentData()
        }

        new_search = Search(scope=scope, driver=my_driver, wait=my_wait)
        search_queries = new_search.search_combinations()

        new_search.search(search_queries, False, country=self.country.text())

        extractor = Extractor(driver=my_driver, wait=my_wait)
        my_jobs = extractor.extract_jobs()
        extractor.export_jobs(my_jobs)
        self.__quit()

    def __search_with_filter(self):
        self.__go_to_search()

        driver = Driver()
        my_driver = driver.init_driver()
        my_wait = driver.init_wait(my_driver)

        scope = {
            'title':self.skills.currentData(),
            'skill':self.titles.currentData()
        }

        scope2 = {
            'Exprience level':self.exprience.currentData(),
            'Job type':self.jobtype.currentData(),
            'Remote':self.remo.currentData()
        }

        new_search = Search(scope=scope, driver=my_driver, wait=my_wait)
        search_queries = new_search.search_combinations()

        try:
            date = self.button22.checkedButton().text()
        except:
            date = None

        try:
            sort = self.button21.checkedButton().text()
        except:
            sort = None

        new_search.search(
            search_queries, 
            True, 
            sort, 
            date,
            self.hasverification.isChecked(),
            self.easyapply.isChecked(),
            self.under.isChecked(),
            scope2,
            self.country.text()
        )

        extractor = Extractor(driver=my_driver, wait=my_wait)
        self.timer.timeout.connect(self.__updated_value(extractor.global_num, extractor.global_page_num, extractor.current_page_num))
        self.timer.start(1000)
        my_jobs = extractor.extract_jobs()
        extractor.export_jobs(my_jobs)
        self.__quit()

    def __go_to_filter(self):
        self.stacked_layout.setCurrentIndex(1)

    def __go_to_search(self):
        self.stacked_layout.setCurrentIndex(2)

    def __quit(self):
        QApplication.quit()

    def __delete_log(self):
        with open("linkedin_cookies.json", "w") as file:
            file.write("")
        
        self.login.setText('Logged out')

    def __back(self):
        self.stacked_layout.setCurrentIndex(0)

    def __updated_value(self, total_job, total_page, current_page):
        self.showjob.setText(f'The total number of jobs that has been found for you is {total_job}')
        self.showpage.setText(f'Collecting jobs in page {current_page} from {total_page}')

    def __uncheck_radio_button(self):
        self.button22.setExclusive(False)
        for btn in self.button22.buttons():
            btn.setAutoExclusive(False)
            btn.setChecked(False)
            btn.setAutoExclusive(True)

        self.button22.setExclusive(True)

        self.button21.setExclusive(False)
        for btn in self.button21.buttons():
            btn.setAutoExclusive(False)
            btn.setChecked(False)
            btn.setAutoExclusive(True)

        self.button21.setExclusive(True)

    def __execute_no_filter(self):
        worker = Worker(
            self.__search_without_filter
        )
        self.threadpool.start(worker)

    def __execute_filter(self):
        worker = Worker(
            self.__search_with_filter
        )
        self.threadpool.start(worker)


