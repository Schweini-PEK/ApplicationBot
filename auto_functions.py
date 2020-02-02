# ===================================================================

# Useful functions for auto-completion of apps

# ===================================================================

import time, datetime
import re
import string

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

# ===================================================================
# Example Inputs and Useful Objects
# ===================================================================

details_example = {'id': 1330,
                   'user_id': 45,
                   'job_id': 221,
                   'role_id': 221,
                   'firstname': 'Brad',
                   'lastname': 'Yoder',
                   'gender': 'Male',
                   'race': 'White',
                   'dob': '2/23/1973',
                   'phone': 4063845577,
                   'email': 'asdf@mt2015.com',
                   'addy': "194 HENRY'S BBQ ST",
                   'addy_city': 'SHREVEPORT',
                   'addy_state': 'LA',
                   'addy_zip': 71115,
                   'start_date': '2019-11-05',
                   'schl_name': 'HELEN COX HIGH SCHOOL',
                   'schl_addy': '2200 LAPALCO BLVD HARVEY',
                   'schl_state': 'LA',
                   'schl_city': 'SHREVEPORT',
                   'schl_zip': 70058,
                   'grad_year': 1991,
                   'col_name': 'Central Louisiana Technical Community College',
                   'col_addy': '4311 South MacArthur Drive',
                   'col_state': 'LA',
                   'col_zip': 71302,
                   'bachelors': 0,
                   'major': 'Legal Office Support',
                   'social': 526078545,
                   'whywork': 'I want to use and improve my skills. ',
                   'firm': 'TESTING',
                   'city': 'Bossier City',
                   'state': 'LA',
                   'street': '3836 Industrial Circle  ',
                   'zipcode': 71112,
                   'jobtitle': 'Test',
                   'link': '',
                   'raw_name': 'TESTING',
                   'hist': [{'id': 17410,
                             'name': 'Sf Spice',
                             'position': 'Cook',
                             'addy': '1640 Tide Ct',
                             'city': 'WOODLAND',
                             'state': 'CA',
                             'zip': 95776,
                             'supervisor': 'Nico Richards',
                             'start': '7/2018',
                             'end': 'Present',
                             'whyleave': '',
                             'phone': '(530) 736-7909',
                             'type': 'Spices',
                             'sic': 54,
                             'duties': ['Operate dish washer per approved guidelines.',
                                        'Performed basic cleaning tasks as needed or directed by supervisor',
                                        'Stocked cooler with food needed for that day']},
                            {'id': 17411,
                             'name': 'Las Islitas Ostioneria',
                             'position': 'Dishwasher',
                             'addy': '737 East St',
                             'city': 'WOODLAND',
                             'state': 'CA',
                             'zip': 95776,
                             'supervisor': 'Cullen George',
                             'start': '8/2017',
                             'end': '7/2018',
                             'whyleave': 'Ready to try new things.',
                             'phone': '(530) 005-7951',
                             'type': 'Restaurants',
                             'sic': 58,
                             'duties': ['Cleaned and set up chef case with prepared foods.',
                                        'Maintain all cleaning/washing equipment at proper temperature and in proper']},
                            {'id': 17412,
                             'name': 'Famous Footwear',
                             'position': 'Customer Service Associate',
                             'addy': '2145 Bronze Star Dr # 400',
                             'city': 'WOODLAND',
                             'state': 'CA',
                             'zip': 95776,
                             'supervisor': 'Kole Warren',
                             'start': '11/2016',
                             'end': '8/2017',
                             'whyleave': 'Looking for promotion opportunities.',
                             'phone': '(530) 330-4620',
                             'type': 'Shoes-retail',
                             'sic': 56,
                             'duties': ['Answer questions regarding the store and its merchandise.',
                                        'Performed countdown of money at shift beginning and end']}]}

details_example_2 = {'id': 1330,
                     'user_id': 45,
                     'job_id': 221,
                     'role_id': 221,
                     'firstname': 'Maya',
                     'lastname': 'Yodern',
                     'gender': 'Male',
                     'race': 'White',
                     'dob': '2/23/1989',
                     'phone': 4064745477,
                     'email': 'asdf2@mt2015.com',
                     'addy': "2020 Oxford st",
                     'addy_city': 'Berkeley',
                     'addy_state': 'CA',
                     'addy_zip': 94709,
                     'start_date': '2019-11-05',
                     'schl_name': 'HELEN COX HIGH SCHOOL',
                     'schl_addy': '2200 LAPALCO BLVD HARVEY',
                     'schl_state': 'LA',
                     'schl_city': 'SHREVEPORT',
                     'schl_zip': 70058,
                     'grad_year': 1991,
                     'col_name': 'Central Louisiana Technical Community College',
                     'col_addy': '4311 South MacArthur Drive',
                     'col_state': 'LA',
                     'col_zip': 71302,
                     'bachelors': 0,
                     'major': 'Legal Office Support',
                     'social': 526078545,
                     'whywork': 'I want to use and improve my skills. ',
                     'firm': 'TESTING',
                     'city': 'Bossier City',
                     'state': 'LA',
                     'street': '3836 Industrial Circle  ',
                     'zipcode': 71112,
                     'jobtitle': 'Test',
                     'link': '',
                     'raw_name': 'TESTING',
                     'hist': [{'id': 3299,
                               'name': 'Witts Powder Coating',
                               'position': 'Handler',
                               'addy': '1328 Driftwood Dr',
                               'city': 'BOSSIER CITY',
                               'state': 'LA',
                               'zip': 71111,
                               'supervisor': 'Armani Russell',
                               'start': '12/2017',
                               'end': 'Present',
                               'whyleave': '',
                               'phone': '(318) 134-7492',
                               'type': 'Powder Coatings (mfrs)',
                               'duties': ['Responsible for physically loading and unloading packages',
                                          'Transported material by use of forklifts, pallet jacks and hand trucks.',
                                          'Lift, carry, push and pull packages as required']},
                              {'id': 3300,
                               'name': 'Martins Alternators & Starters',
                               'position': 'Delivery Driver / Courier',
                               'addy': '2214 Barksdale Blvd',
                               'city': 'BOSSIER CITY',
                               'state': 'LA',
                               'zip': 71112,
                               'supervisor': 'Jamarcus Powell',
                               'start': '5/2016',
                               'end': '12/2017',
                               'whyleave': 'I was exploring new lines of work.',
                               'phone': '(318) 570-9737',
                               'type': 'Alternators & Starters-marine (mfrs)',
                               'duties': ['Place orders for biweekly or weekly deliveries',
                                          'Perform vehicle safety checks before departure.',
                                          'Check with dispatcher after completed deliveries, in order to confirm deliveries and collections and to receive instructions for other deliveries.']},
                              {'id': 3301,
                               'name': 'Neff Rental',
                               'position': 'Handler',
                               'addy': '3836 Industrial Cir',
                               'city': 'BOSSIER CITY',
                               'state': 'LA',
                               'zip': 71112,
                               'supervisor': 'Darian Payne',
                               'start': '6/2014',
                               'end': '5/2016',
                               'whyleave': 'Looking for promotion opportunities.',
                               'phone': '(318) 226-6551',
                               'type': 'Construction-building Contractors',
                               'duties': ['Sorted packages by hands in an efficient manner.',
                                          'Stack materials in accordance to instructions']}]}

states = {
    'AK': 'Alaska',
    'AL': 'Alabama',
    'AR': 'Arkansas',
    'AS': 'American Samoa',
    'AZ': 'Arizona',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DC': 'District of Columbia',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'GU': 'Guam',
    'HI': 'Hawaii',
    'IA': 'Iowa',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'MA': 'Massachusetts',
    'MD': 'Maryland',
    'ME': 'Maine',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MO': 'Missouri',
    'MP': 'Northern Mariana Islands',
    'MS': 'Mississippi',
    'MT': 'Montana',
    'NA': 'National',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'NE': 'Nebraska',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NV': 'Nevada',
    'NY': 'New York',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'PR': 'Puerto Rico',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VA': 'Virginia',
    'VI': 'Virgin Islands',
    'VT': 'Vermont',
    'WA': 'Washington',
    'WI': 'Wisconsin',
    'WV': 'West Virginia',
    'WY': 'Wyoming'
}

# Possible SIC does and positions used for jobs in each.
# SIC Code Reference: https://mckimmoncenter.ncsu.edu/2digitsiccodes/
fast_food_positions = ['Crew Member', 'Cashier', 'Food prep / service', 'Cook']
food_positions = ['Server', 'Dishwasher', 'Cashier', 'Host', 'Cook']
office_positions = ['Office manager', 'Receptionist', 'Assistant']
hospitality_positions = ['Housekeeper', 'Receptionist']
delivery_positions = ['Package Handler', 'Handler', 'Laborer',
                      'Delivery Driver / Courier', 'Dockworker', 'Warehouse Associate']
standard_positions = ['Team Member', 'Retail Associate', 'Cashier',
                      'Stocker', 'Customer Service Associate']  # Works for all but food

pos_map = {15: office_positions,
           24: office_positions,
           25: office_positions,
           34: office_positions,
           36: office_positions,
           42: office_positions,
           53: standard_positions,
           54: fast_food_positions,
           56: standard_positions,
           58: food_positions,
           64: office_positions,
           65: office_positions,
           70: hospitality_positions + food_positions,
           73: office_positions,
           80: office_positions, }


# ===================================================================
# Useful Functions for Robots
# ===================================================================

def str_format(x):
    try:
        words = re.findall("[\w']+", x)
        return " ".join([w.capitalize() for w in words])
    except:
        return string.capwords(x)


def scroll_shim(element, browser):
    x = element.location['x']
    y = element.location['y']
    scroll_by_coord = 'window.scrollTo(%s,%s);' % (
        x,
        y
    )
    scroll_nav_out_of_way = 'window.scrollBy(0, -120);'
    browser.execute_script(scroll_by_coord)
    browser.execute_script(scroll_nav_out_of_way)
    time.sleep(1)
    return "Scrolled!"


def scroll(element, browser):
    x = element.location['x']
    y = element.location['y']
    scroll_by_coord = 'window.scrollTo(%s,%s);' % (
        x,
        y
    )
    browser.execute_script(scroll_by_coord)
    time.sleep(1)
    return "Scrolled!"


def scroll_xpath(xpath, browser, num=0, delay=30):
    WebDriverWait(browser, delay).until(
        EC.visibility_of_element_located((By.XPATH, xpath)))
    el = browser.find_elements_by_xpath(xpath)[num]
    scroll_shim(el, browser)
    return "Waited & Scrolled!"


def click_link_by_text(link_text, browser):
    WebDriverWait(browser, 20).until(
        EC.element_to_be_clickable(
            (By.PARTIAL_LINK_TEXT, link_text)))
    WebDriverWait(browser, 20).until(
        EC.visibility_of_element_located(
            (By.PARTIAL_LINK_TEXT, link_text)))
    browser.find_element_by_partial_link_text(link_text).click()
    return "Clicked!"


def scroll_click_xp(xpath, browser, num=0, delay=30):
    WebDriverWait(browser, delay).until(
        EC.visibility_of_element_located((By.XPATH, xpath)))
    time.sleep(0.5)
    scroll_xpath(xpath, browser, num=num, delay=delay)
    browser.find_elements_by_xpath(xpath)[num].click()
    return "Waited, Scrolled, & Clicked!"


def wait_click_xp(xpath, browser, num=0, delay=30):
    WebDriverWait(browser, delay).until(
        EC.visibility_of_element_located(
            (By.XPATH, xpath)))
    time.sleep(1)
    browser.find_elements_by_xpath(xpath)[num].click()
    return "Waited & Clicked"


def click_xpath(xpath, browser):
    WebDriverWait(browser, 20).until(
        EC.visibility_of_element_located(
            (By.XPATH, xpath)))
    action = ActionChains(browser)
    action.move_to_element_with_offset(
        browser.find_element_by_xpath(xpath), 0, 0)
    action.click()
    action.perform()
    return "Clicked!"


def click_text(text, browser):
    WebDriverWait(browser, 20).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[contains(text(), '{}')]".format(text))))
    action = ActionChains(browser)
    action.move_to_element_with_offset(
        browser.find_element_by_xpath("//*[contains(text(), '{}')]".format(text)), 5, 5)
    action.click()
    action.perform()
    return "Clicked"


def add_key_to_field(key, element):
    current_text = element.get_attribute("value")
    new_text = current_text + key
    loop = 0
    while element.get_attribute("value") != new_text:
        element.send_keys(key)
        time.sleep(.1)
        loop += 1
        if loop >= 100:
            raise ValueError("Unable to add new key to field {}".format(element))
            break
    return None


def fill_in_xpath(xpath, text, browser, k=0):
    WebDriverWait(browser, 20).until(
        EC.visibility_of_element_located((By.XPATH, xpath)))
    field = browser.find_elements_by_xpath(xpath)[k]
    field.clear()
    for t in text:
        add_key_to_field(t, field)
    WebDriverWait(browser, 5).until(lambda browser:
                                    field.get_attribute('value') == text)
    return "Waited & Filled!"


def scroll_fill(xpath, text, browser, k=0):
    scroll_shim(browser.find_elements_by_xpath(xpath)[k], browser)
    return fill_in_xpath(xpath, text, browser, k)


def scroll_fill_visible(xpath, text, browser, k=0):
    vis = [el for el in browser.find_elements_by_xpath(xpath) if el.is_displayed()]
    scroll_shim(vis[k], browser)
    field = vis[k]
    field.clear()
    for t in text:
        add_key_to_field(t, field)
    WebDriverWait(browser, 5).until(lambda browser:
                                    field.get_attribute('value') == text)
    return "Filled!"


def has_value(xpath, text, browser):
    try:
        element = browser.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    print(element.get_attribute("value"), text)
    return element.get_attribute("value") == text


def fill_in_id(id, text, browser):
    WebDriverWait(browser, 20).until(
        EC.visibility_of_element_located((By.ID, id)))
    field = browser.find_element_by_id(id)
    field.clear()
    field.send_keys(text)
    WebDriverWait(browser, 5).until(
        EC.text_to_be_present_in_element_value((By.ID, id), text))
    return "filled"


def pick_option_id(id, browser):
    field = browser.find_element_by_id(id)
    field.click()
    return "selected"


def scroll_fill_element(element, text, browser, clearfield=True):
    scroll_shim(element, browser)
    WebDriverWait(browser, 20).until(
        EC.visibility_of(element))
    element.click()
    if clearfield:
        element.clear()
    for t in text:
        add_key_to_field(t, element)
    return "Filled!"


def fill_simple(el, text, browser):
    el.send_keys(text)
    WebDriverWait(browser, 5).until(
        EC.text_to_be_present_in_element_value((By.ID, el.get_attribute('id')),
                                               text))
    return "Filled!"


def fill_simple_validate(el, text, browser):
    el.clear()
    for t in text:
        add_key_to_field(t, el)
    WebDriverWait(browser, 5).until(
        EC.text_to_be_present_in_element_value((By.ID, el.get_attribute('id')),
                                               text))
    return "Filled!"


def click_options(option_text, browser, n=0):
    WebDriverWait(browser, 20).until(
        lambda browser: browser.find_elements_by_xpath(
            "//div[contains(text(), '{}')]".format(option_text))
    )
    st = browser.find_elements_by_xpath("//div[contains(text(), '{}')]".format(option_text))
    scroll_shim(st[n], browser)
    st[n].click()
    return "Clicked!"


def click_at(el, browser):
    action = ActionChains(browser)
    action.move_to_element(el)
    action.click()
    action.click()
    action.perform()
    return "Clicked!"


def find_displayed(xpath, browser):
    return [k for k in browser.find_elements_by_xpath(xpath) if k.is_displayed()]


def wait_displayed(xpath, browser, quant=1, delay=30):
    WebDriverWait(browser, delay).until(
        lambda browser: len([k for k in browser.find_elements_by_xpath(xpath)
                             if k.is_displayed()]) >= quant
    )
    return "Waited"


def click_displayed(xpath, browser, quant=0, delay=30):
    wait_displayed(xpath, browser, quant + 1, delay=delay)
    [k for k in browser.find_elements_by_xpath(xpath)
     if k.is_displayed()][quant].click()
    return "Waited & Clicked!"


def wait_visible(selector_tuple, browser, delay=30):
    WebDriverWait(browser, delay).until(
        EC.visibility_of_element_located(selector_tuple)
    )
    return "Waited"


def wait_clickable(selector_tuple, browser, delay=20):
    WebDriverWait(browser, delay).until(
        EC.element_to_be_clickable(selector_tuple)
    )
    return "Waited"


def wait_invisible(selector_tuple, browser, delay=20):
    WebDriverWait(browser, delay).until(
        EC.invisibility_of_element_located(selector_tuple)
    )
    return "Waited"


def down_enter(times, browser):
    for k in range(times):
        ActionChains(browser).send_keys(Keys.DOWN).perform()
        time.sleep(1)
    ActionChains(browser).send_keys(Keys.ENTER).perform()
    time.sleep(1)
    return "Pressed down {} times".format(times)


def up_enter(times, browser):
    for k in range(times):
        ActionChains(browser).send_keys(Keys.UP).perform()
        time.sleep(1)
    ActionChains(browser).send_keys(Keys.ENTER).perform()
    time.sleep(1)
    return "Pressed down {} times".format(times)
