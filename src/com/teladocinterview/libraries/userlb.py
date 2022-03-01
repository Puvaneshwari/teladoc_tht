import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as exp_cond


def fetch_table_data(driver):
    """
    Used to return the user table data by looping the rows and columns
    user_detail_data(List): Returns user table data
    """
    total_rows = len(driver.find_elements(By.XPATH, "//tbody/tr"))
    logging.info("Total number of rows %d", total_rows)
    # get the number of columns
    total_columns = len(driver.find_elements(By.XPATH, "//tbody/tr[2]/td")) - 2
    logging.info("Total number of rows %d", total_columns)
    user_detail_data = []
    # iterate the rows
    for i in range(1, total_rows):
        # reset the row data each time
        row_data = []
        # iterate the columns for each row
        for j in range(1, total_columns):
            # fetch the cell value for the specified row and column
            row_data.append(driver.find_element(By.XPATH, "//tbody/tr[" + str(i) + "]/td[" + str(j) + "]").text)

            logging.debug("row data is list{}".format(row_data))
        # add the row data to append in user_detail_data
        user_detail_data.append(row_data)
        logging.debug("user data is list{}".format(user_detail_data))
    return user_detail_data


def find_row_num_by_user_name(driver, user_name):
    """
    Used to return the row number based on passed username
    driver(Object)    : selenium driver object
    user_name(String) : Username to find the row number
    :return row_num(Integer)
    """
    total_rows = len(driver.find_elements(By.XPATH, "//tbody/tr"))
    logging.info("Total number of rows %d", total_rows)
    un_col_num = "3"
    for row_num in range(1, total_rows):
        actual_user_name = (driver.find_element
                            (By.XPATH, "//tbody/tr[" + str(row_num) + "]/td[" + str(un_col_num) + "]").text)
        if actual_user_name == user_name:
            logging.info("Searched user name found on the row number is %d", row_num)
            return row_num
    return -1


def click_delete_by_user_name(driver, row_number):
    """
    Used to delete the row based on the row number passed
    driver(Object)   : selenium driver object
    row_num(integer) : row number to delete the user.
    """
    click_element_by_xpath(driver, xpath_elem="//tbody/tr[" + str(row_number) + "]/td[11]/button")
    logging.info("Clicked the delete element")
    click_element_by_css(driver, css_elem="button.btn.ng-scope.ng-binding.btn-primary")
    logging.info("Deleted the specified row")


def enter_input_text_by_name(driver, elem_name, inp_txt):
    """
    driver(Object)   : selenium driver object
    elem_name(String): Locator element name
    inp_txt(String)  : input text to enter in the text box
    """
    txt_firstname = driver.find_element(By.NAME, elem_name)
    txt_firstname.clear()
    txt_firstname.send_keys(inp_txt)
    txt_firstname.send_keys(Keys.ENTER)
    logging.info("Input text is %s", inp_txt)


def click_element_by_css(driver, css_elem):
    """
    driver(Object)   : selenium driver object
    css_elem(String) : Locator element css to click
    """
    btn = WebDriverWait(driver, 10).until(exp_cond.visibility_of_element_located((By.CSS_SELECTOR, css_elem)))
    if btn.is_enabled():
        btn.click()
        logging.info("Clicked the button")
        return True
    return False


def select_dropdown_value_by_name(driver, drpdown_elem_name, txt):
    """
    driver(Object)   : selenium driver object
    elem_name(String): Locator element name
    txt(String)      : Text to select in the dropdown
    """
    select_txt = Select(driver.find_element(By.NAME, drpdown_elem_name))
    select_txt.select_by_visible_text(txt)
    logging.info("Selected the dropdown value: %s", txt)


def click_element_by_xpath(driver, xpath_elem):
    """
    driver(Object)   : selenium driver objectt
    xpath_elem(String): Locator element xpath to click
    """
    btn = WebDriverWait(driver, 10).until(exp_cond.visibility_of_element_located((By.XPATH, xpath_elem)))
    if btn.is_enabled():
        btn.click()
        logging.info("Clicked the button")
        return True
    return False


def click_elem(driver, locator, elem_type, text):
    if elem_type == "input":
        enter_input_text_by_name(driver, elem_name=locator, inp_txt=text)
        logging.info("Element type is input")
    elif elem_type == "dropdown":
        logging.info("Element type is dropdown")
        select_dropdown_value_by_name(driver, drpdown_elem_name=locator, txt=text)
    elif elem_type == "radio":
        logging.info("Element type is radio")
        click_element_by_xpath(driver, xpath_elem=locator)
