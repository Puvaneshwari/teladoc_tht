import time
import pytest
import logging

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from libraries import userlb as val_user
from data import test_data as data


@pytest.fixture(scope="module")
def driver():
    selenium_driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    selenium_driver.get("https://www.way2automation.com/angularjs-protractor/webtables/")
    selenium_driver.maximize_window()
    selenium_driver.implicitly_wait(10)
    yield selenium_driver
    selenium_driver.close()
    return selenium_driver


def test_add_user_and_verify(driver):
    """
    Test: Test able to add a user and verify whether the user is added to the table.
    Steps: Click and add user link then add the new user details
           Click Save
           Verify whether the user is added to the table with right details.
    """
    val_user.click_element_by_css(driver, css_elem="button.btn.btn-link.pull-right")
    time.sleep(10)
    expected_values = []
    for user in data.valid_user_data_obj:
        expected_values.append("") if user.get("field") == "pwd" else expected_values.append(user.get("value"))
        val_user.click_elem(driver, locator=user.get("locator"), elem_type=user.get("type"), text=user.get("value"))
    time.sleep(5)
    val_user.click_element_by_css(driver, css_elem="button.btn.btn-success")
    time.sleep(10)
    user_data = val_user.fetch_table_data(driver)
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
    val_user.click_element_by_css(driver, css_elem="button.btn.btn-link.pull-right")
    time.sleep(10)
    invalid_exp_values = []
    for user in data.invalid_user_data_obj:
        invalid_exp_values.append("") if user.get("field") == "pwd" else invalid_exp_values.append(user.get("value"))
        val_user.click_elem(driver, locator=user.get("locator"), elem_type=user.get("type"), text=user.get("value"))

    time.sleep(5)
    val_user.click_element_by_css(driver, css_elem="button.btn.btn-success")
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
    val_user.click_element_by_css(driver, css_elem="button.btn.btn-link.pull-right")
    time.sleep(10)
    for user in data.invalid_user_email_obj:
        val_user.click_elem(driver, locator=user.get("locator"), elem_type=user.get("type"), text=user.get("value"))
    time.sleep(5)
    email_error_msg = driver.find_element(By.XPATH, "//span[contains( text( ), 'Not valid email!')]")
    save_btn_enabled = val_user.click_element_by_css(driver, css_elem="button.btn.btn-success")
    if not save_btn_enabled and email_error_msg.is_displayed():
        logging.info("Not able to add the user with invalid email as expected")
    else:
        raise Exception("Able to add an invalid user with invalid email which is not expected")
