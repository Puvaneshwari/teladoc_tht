# teladoc_tht
This is a project created for automation testing of web page https://www.way2automation.com/angularjs-protractor/webtables/.
This project intends to test 2 workflows.
1. Create User
2. Delete User

**Setup**

This is a python project which uses selenium and pytest to power the test suite. This project also uses chrome webdriver.
1. Install python 3.10
2. Install pip 21.1.2 
3. Install chrome web driver: https://chromedriver.chromium.org/downloads
4. Clone project to local: git clone https://github.com/Puvaneshwari/teladoc_tht.git
5. cd to the project folder
6. Install pytest: pip install -U pytest
7. Install selenium: pip install -U selenium
8. Install webdriver_manager: pip install webdriver_manager
9. Run tests: 
   1. cd <project folder>/src/com/teladoc
   2. py.test test_user.py
