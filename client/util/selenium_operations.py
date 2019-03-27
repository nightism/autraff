from selenium.webdriver.common.keys import Keys

SELECT_LINK_OPEN_IN_NEW_TAB = Keys.CONTROL + Keys.SHIFT + Keys.RETURN


def extract_page_content(driver):
    if driver is None:
        return ""

    try:
        el = driver.find_element_by_tag_name("body")
        # print(el.text)
        return el.text
    except Exception as e:
        print('[Selenium Util] ' + str(e))
        return ""
