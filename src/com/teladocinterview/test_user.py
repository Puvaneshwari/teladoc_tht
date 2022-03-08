import pytest
import logging

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from libraries import userlb as val_user
from data import test_data as data


@pytest.fixture(scope="function")
def driver():
    """
    This method will be called in the module scope to load the web page using selenium chrome driver
    and close the driver once the function run is done.
    """
    selenium_driver = webdriver.Chrome(service=Service(ChromeDriverManager(version="98.0.4758.102").install()))
    selenium_driver.get("https://www.way2automation.com/angularjs-protractor/webtables/")
    selenium_driver.maximize_window()
    selenium_driver.implicitly_wait(10)
    yield selenium_driver
    selenium_driver.close()
    return selenium_driver

@pytest.fixture(scope="function")
def user_records_added():
    """
    This method will delete the test data once the test run is over in the module scope.
    """
    user_data_records = []
    yield
    if not user_data_records:
       # call the method to delete the user test data
       val_user.delete_user_test_data(driver, user_data_records)
    return user_data_records


def test_add_user_and_verify(driver,user_records_added):
    """
    Test: Test able to add a user and verify whether the user is added to the table.
    Steps: Click and add user link then add the new user details
           Click Save
           Verify whether the user is added to the table with right details.
    """
    val_user.click_element_by_css(driver, css_elem=data.add_user_css)
    expected_values = []
    for user in data.valid_user_data_obj:
        expected_values.append("") if user.get("field") == "pwd" else expected_values.append(user.get("value"))
        print(user.get("field"))
        val_user.click_elem(driver, locator=user.get("locator"), elem_type=user.get("type"), text=user.get("value"))
    val_user.click_element_by_css(driver, css_elem=data.save_css)
    user_data = val_user.fetch_table_data(driver)
    user_records_added = expected_values[2]
    assert expected_values in user_data, "Expected user details are not present in user details"


def test_delete_user_and_verify(driver):
    """
      Test : Test able to delete the specified user
      Steps: Delete the User using delete icon and verify whether the user is deleted from the table.
    """
    user_name = "novak"
    row_number = val_user.find_row_num_by_user_name(driver, user_name)
    if row_number != -1:
        val_user.click_delete_by_user_name(driver, row_number)
    else:
        logging.error("Specified user not found in the user table")
    user_detail = val_user.fetch_table_data(driver)
    assert user_name not in user_detail, "Error: User name %s still present in the table" + user_name


def test_invalid_data(driver):
    """
    Test  : Test able to add a user with invalid data
    Steps : Try to add a user with invalid data and check whether we are not able to add the user
            with invalid data.
            If we are able to add invalid user throw assertion error
    """
    val_user.click_element_by_css(driver, css_elem=data.add_user_css)
    invalid_exp_values = []
    for user in data.invalid_user_data_obj:
        invalid_exp_values.append("") if user.get("field") == "pwd" else invalid_exp_values.append(user.get("value"))
        val_user.click_elem(driver, locator=user.get("locator"), elem_type=user.get("type"), text=user.get("value"))
    val_user.click_element_by_css(driver, css_elem=data.save_css)
    logging.info("Clicked the Save button")
    user_data = val_user.fetch_table_data(driver)
    assert invalid_exp_values not in user_data, "Error: Able to add an invalid user"


def test_invalid_email_id(driver):
    """
    Test  : Test able to add a user with invalid email id
    Steps : Try to add a user with invalid email id and check whether we are not able to add the user
            with invalid email id
            If we are able to add invalid user throw assertion error
    """
    val_user.click_element_by_css(driver, css_elem=data.add_user_css)
    for user in data.invalid_user_email_obj:
        val_user.click_elem(driver, locator=user.get("locator"), elem_type=user.get("type"), text=user.get("value"))
    email_error_msg = driver.find_element(By.XPATH, "//span[contains( text( ), 'Not valid email!')]")
    save_btn_enabled = val_user.click_element_by_css(driver, css_elem=data.save_css)
    assert (not save_btn_enabled and email_error_msg.is_displayed()), \
        "Able to add an invalid user with invalid email which is not expected"


def test_first_name_blank(driver):
    """
    Test  : Test not able to add a user without full name
    Steps : Try to add a user without full name and check whether we are not able to add the user
            without full name
    """
    val_user.click_element_by_css(driver, css_elem=data.add_user_css)
    for user in data.invalid_user_blank_fn:
        val_user.click_elem(driver, locator=user.get("locator"), elem_type=user.get("type"), text=user.get("value"))
    fn_error_msg = driver.find_element(By.XPATH, "//span[contains( text( ), 'Required!')]")
    save_btn_enabled = val_user.click_element_by_css(driver, css_elem=data.save_css)
    if not save_btn_enabled and fn_error_msg.is_displayed():
        logging.info("Not able to add the user without full name as expected")
    else:
        raise Exception("Able to add an invalid user without full name which is not expected")


def test_user_name_blank(driver):
    """
    Test  : Test not able to add a user without username
    Steps : Try to add a user without username and check whether we are not able to add the user
            without username
    """
    val_user.click_element_by_css(driver, css_elem=data.add_user_css)
    for user in data.invalid_user_blank_user_name:
        val_user.click_elem(driver, locator=user.get("locator"), elem_type=user.get("type"), text=user.get("value"))
    save_btn_enabled = val_user.click_element_by_css(driver, css_elem=data.save_css)
    if not save_btn_enabled:
        logging.info("Not able to add the user without user name as expected")
    else:
        raise Exception("Able to add an invalid user without user name which is not expected")


def test_mobile_number_blank(driver):
    """
    Test  : Test not able to add a user without mobile number
    Steps : Try to add a user without mobile number and check whether we are not able to add the user
    """
    val_user.click_element_by_css(driver, css_elem=data.add_user_css)
    for user in data.invalid_user_blank_mobile_num:
        val_user.click_elem(driver, locator=user.get("locator"), elem_type=user.get("type"), text=user.get("value"))
    save_btn_enabled = val_user.click_element_by_css(driver, css_elem=data.save_css)
    if not save_btn_enabled:
        logging.info("Not able to add the user without mobile number as expected")
    else:
        raise Exception("Able to add an invalid user without mobile number which is not expected")


def test_blank_role(driver):
    """
    Test  : Test not able to add a user without sales team
    Steps : Try to add a user without role and check whether we are not able to add the user without role
    """
    val_user.click_element_by_css(driver, css_elem=data.add_user_css)
    for user in data.invalid_user_blank_role_id:
        if not user.get("field") == "role":
            val_user.click_elem(driver, locator=user.get("locator"), elem_type=user.get("type"), text=user.get("value"))
    role_error_msg = driver.find_element(By.XPATH, "//tr[6]//span[contains( text( ), 'Required!')]")
    save_btn_enabled = val_user.click_element_by_css(driver, css_elem=data.save_css)
    if not save_btn_enabled and role_error_msg.is_displayed():
        logging.info("Not able to add the user without role as expected")
    else:
        raise Exception("Able to add an invalid user without role which is not expected")


def test_with_valid_company(driver):
    """
    Test  : Test able to add a user with company details
    Steps : Try to add a user with company details and verify whether those details are saved.
    """
    val_user.click_element_by_css(driver, css_elem=data.add_user_css)
    expected_values = []
    for user in data.valid_user_with_company:
        expected_values.append("") if user.get("field") == "pwd" else expected_values.append(user.get("value"))
        val_user.click_elem(driver, locator=user.get("locator"), elem_type=user.get("type"), text=user.get("value"))
    val_user.click_element_by_css(driver, css_elem=data.save_css)
    user_data = val_user.fetch_table_data(driver)
    assert expected_values in user_data, "Expected user details are not matching with user details"
