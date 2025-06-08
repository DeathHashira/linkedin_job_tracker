from ui.ui import *

app = QApplication(sys.argv)
MyMainWindow = MyWindow()

MyMainWindow.show()
sys.exit(app.exec())




































# driver = Driver()
# mydriver = driver.init_driver()
# mywait = driver.init_wait(mydriver)

# myscope = {
#     'title':[],
#     'skill':[],
#     'company':[]
# }

# new_search = Search(scope=myscope, driver=mydriver, wait=mywait)

# search_queries = new_search.search_combinations()
# new_search.search(search_queries, True)

# extractor = Extractor(driver=mydriver, wait=mywait)
# my_jobs = extractor.extract_jobs()
# extractor.export_jobs(my_jobs)
