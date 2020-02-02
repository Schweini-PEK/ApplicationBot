"""
Auto-completion of Labcorp applications
"""
import pandas as pd
import numpy as np
import time
import datetime
import os, re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as chropopt
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
import string
from auto_functions import *

from uszipcode import SearchEngine


# details = details_example
# details['email'] = 'asdf@mt2015.com'
# details['link'] = 'https://jobs.labcorp.com/job/lakewood/courier-driver-lakewood-co/668/15141452'

def submit_labcorp(details):
    try:
        display = Display(visible=0, size=(1200, 900))
        display.start()

        # browserpath = '/Users/evanrose/Dropbox/GSI-GSR-Reader/Chris/automation/auto/bin/chromedriver'
        chrome_options = chropopt()
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--window-size=1200x900")
        chrome_options.add_argument("--no-sanbdox")
        browserpath = '/accounts/projects/pkline/randres/randres/scraping/chromedriver_new'
        chrome_options.binary_location = '/accounts/projects/pkline/randres/chrome/opt/google/chrome/chrome'
        browser = webdriver.Chrome(browserpath, options=chrome_options)

        # Big picture opxtions
        firm = details['raw_name']
        app_id = details['id']

        # 0) Go to URL
        browser.get(details['link'])
        wait_visible((By.XPATH, "//a[text()='Apply Now']"), browser)
        scroll_shim(browser.find_element_by_xpath("//a[text()='Apply Now']"), browser)
        browser.find_element_by_xpath("//a[text()='Apply Now']").click()

        # 0) Login / create account
        # Enter information
        fill_in_xpath("//input[@name='email']", details['email'], browser)
        fill_in_xpath("//input[@name='password']", 'Spaghettimonster!1', browser)
        fill_in_xpath("//input[@name='passwordConfirm']", 'Spaghettimonster!1', browser)
        ActionChains(browser).send_keys(Keys.ENTER).perform()

        try:
            wait_visible((By.XPATH, "//span[contains(text(), 'Email in use already')]"), browser)
            click_link_by_text("Sign in with existing account", browser)
            fill_in_xpath("//input[@name='password']", 'Spaghettimonster!1', browser)
            click_at(browser.find_element_by_xpath("//button[contains(text(), 'SIGN IN')]"), browser)
            time.sleep(5)

            wait_visible((By.XPATH, "//div[contains(text(), 'Your application is not yet complete')]"), browser)
            click_at(browser.find_element_by_xpath("//div[contains(text(), 'Your application is not yet complete')]"),
                     browser)
            time.sleep(5)
        except:
            print("No need to log in ")

        # Enter information
        try:
            wait_visible((By.XPATH, "//input[@name='firstName']"), browser)
            scroll(browser.find_element_by_xpath("//input[@name='firstName']"), browser)
            fill_simple_validate(browser.find_element_by_xpath("//input[@name='firstName']"), details['firstname'],
                                 browser)
            scroll(browser.find_element_by_xpath("//input[@name='lastName']"), browser)
            fill_simple_validate(browser.find_element_by_xpath("//input[@name='lastName']"), details['lastname'],
                                 browser)
            scroll(browser.find_element_by_xpath("//input[@name='phone']"), browser)
            fill_simple_validate(browser.find_element_by_xpath("//input[@name='phone']"), str(details['phone']),
                                 browser)
            scroll(browser.find_element_by_xpath("//input[@name='address1']"), browser)
            fill_simple_validate(browser.find_element_by_xpath("//input[@name='address1']"),
                                 str_format(details['addy']), browser)
            scroll(browser.find_element_by_xpath("//input[@name='city']"), browser)
            fill_simple_validate(browser.find_element_by_xpath("//input[@name='city']"),
                                 str_format(details['addy_city']), browser)
            scroll(browser.find_element_by_xpath("//input[@name='zip']"), browser)
            fill_simple_validate(browser.find_element_by_xpath("//input[@name='zip']"),
                                 "{:05d}".format(details['addy_zip']), browser)

            # state
            el = browser.find_element_by_xpath('//label[text()="State"]/parent::div/table')
            opt = ''
            iters = 0
            while not (opt == states[details['state']]):
                el.click()
                down_enter(1, browser)
                WebDriverWait(browser, 20).until(lambda browser:
                                                 opt is not el.find_element_by_xpath(
                                                     '//label[text()="State"]/parent::div/table//span').text.strip())
                opt = el.find_element_by_xpath('//label[text()="State"]/parent::div/table//span').text.strip()
                iters += 1
                if iters >= 55:
                    raise ValueError("Couldn't select state")

            # Click next
            click_at(browser.find_elements_by_xpath("//div[@aria-label='Continue']")[-1], browser)
            time.sleep(5)
        except:
            print("no initial info")

        # 1) Agree to data protection
        try:
            wait_visible((By.XPATH, "//span[contains(text(), 'I agree to the above')]"), browser)
            browser.find_element_by_xpath(
                "//span[contains(text(), 'I agree to the above')]/preceding-sibling::div/input").click()
            time.sleep(1)

            # Click next
            click_at(browser.find_elements_by_xpath("//div[@aria-label='Continue']")[0], browser)
            time.sleep(5)
        except:
            print("No data protection")

        # 2) Rehire check
        try:
            wait_visible((By.XPATH, '//label[contains(text(), "Last 4 digits")]'), browser)
            time.sleep(2)
            browser.find_element_by_xpath('//label[contains(text(), "Last 4 digits")]/parent::div/div').click()
            ActionChains(browser).send_keys(str(details['social'])[-4:]).perform()

            el = browser.find_elements_by_xpath(
                '//label[contains(text(), "Birthday")]/parent::div/parent::div/div//table')
            el[0].click()
            down_enter(int(details['dob'].split('/')[1]), browser)
            el[1].click()
            down_enter(int(details['dob'].split('/')[0]), browser)

            # Click next
            [k for k in browser.find_elements_by_xpath("//div[@aria-label='Continue']")
             if k.is_displayed()][0].click()
            time.sleep(5)
        except:
            print("No rehire check")

        # 3) How did you hear about us
        try:
            wait_visible((By.XPATH, '//label[text()="Candidate Source"]'), browser)
            el = browser.find_element_by_xpath('//label[text()="Candidate Source"]/parent::div/table')
            opt = ''
            iters = 0
            while not (opt == 'LabCorp Career Site'):
                el.click()
                down_enter(1, browser)
                WebDriverWait(browser, 20).until(lambda browser:
                                                 opt is not el.find_element_by_xpath(
                                                     '//label[text()="Candidate Source"]/parent::div/table//span').text.strip())
                opt = el.find_element_by_xpath(
                    '//label[text()="Candidate Source"]/parent::div/table//span').text.strip()
                iters += 1
                if iters >= 55:
                    raise ValueError("Couldn't select source")

            # Click next
            [k for k in browser.find_elements_by_xpath("//div[@aria-label='Continue']")
             if k.is_displayed()][0].click()
            time.sleep(5)
        except:
            print("No candidate source")

        ### 4) Upload resume
        try:
            wait_visible((By.XPATH, "//span[contains(text(), 'Resume')]"), browser)
            el = browser.find_element_by_xpath(
                "//span[contains(text(), 'Resume')]/parent::div/parent::div/parent::div//span[contains(text(), 'Select')]")
            el.click()
            WebDriverWait(browser, 60).until(lambda browser:
                                             len(browser.find_elements_by_xpath("//input[@type='file']")) > 0)
            el = browser.find_element_by_xpath("//input[@type='file']")
            pdf_name = "{}_{}_{}.pdf".format(details['firm'], details['firstname'], details['lastname'])
            el.send_keys('/accounts/projects/pkline/randres/randres/resumes/' + pdf_name)
            time.sleep(5)

            # Click next
            [k for k in browser.find_elements_by_xpath("//div[@aria-label='Continue']")
             if k.is_displayed()][0].click()
        except:
            print("No resume upload")

        ### 5) Decline to identify EEOC
        try:
            wait_visible((By.XPATH, "//span[contains(text(), 'Decline to identify')]"), browser)
            declines = browser.find_elements_by_xpath(
                "//span[contains(text(), 'Decline to identify')]/preceding-sibling::div/input" +
                " | //span[contains(text(), 'CHOOSE NOT TO')]/preceding-sibling::div/input")
            for el in declines:
                el.click()
                time.sleep(1)

            # Decline hispanic
            browser.find_element_by_xpath("//span[text()='No']").click()
            time.sleep(1)

            # Click next
            [k for k in browser.find_elements_by_xpath("//div[@aria-label='Continue']")
             if k.is_displayed()][0].click()
        except:
            print("No EEOC")

        #### 6) Preliminary questions
        try:
            wait_visible((By.XPATH, "//p[contains(text(), 'we are driven by your success')]"), browser)
            for qs in [('Are you at least', 0),
                       ('What is your highest level of completed', 1 + 3 * (details['col_name'] is not None)),
                       ('Are you authorized to work', 0),
                       ('The hiring process could consist', 0),
                       ('Have you previously executed a non-compete', -1),
                       ('Office of the Inspector General', -1),
                       ('state laboratory licensing program', -1),
                       ('Foreign Assets Control', -1),
                       ('Federal healthcare program', -1),
                       ('by the U.S. Food and Drug Administration (FDA)', -1),
                       ('Federal government agency and/or', -1),
                       ('not otherwise referenced in questions', -1),
                       ('I certify that all information I have provided', 0)
                       ]:
                wait_visible((By.XPATH, "//*[contains(text(), '{}')]".format(qs[0])), browser)
                time.sleep(1)
                el = browser.find_elements_by_xpath(
                    "//span[contains(text(), '{}')]/parent::a/parent::div/".format(qs[0])
                    + "parent::label/parent::div//input | " +
                    "//*[contains(text(), '{}')]/parent::label/parent::div//input".format(qs[0])
                    + " | //span[contains(text(), '{}')]/parent::div/parent::label/parent::div//input".format(qs[0]))
                el[qs[1]].click()

            # Click next
            [k for k in browser.find_elements_by_xpath("//div[@aria-label='Continue']")
             if k.is_displayed()][0].click()
        except:
            print("No preliminary qs")

        #### 7) Assessment
        try:
            wait_visible((By.XPATH, "//div[contains(text(), 'Click the button below to start the assessment.')]"),
                         browser)
            browser.find_element_by_xpath("//b[text()='Start Assessment']").click()
            WebDriverWait(browser, 30).until(lambda browser:
                                             len(browser.window_handles) > 0)
            browser.switch_to.window(browser.window_handles[-1])

            try:
                wait_visible((By.XPATH, "//input[@type='checkbox']"), browser)
                if not browser.find_element_by_xpath("//input[@type='checkbox']").is_selected():
                    browser.find_element_by_xpath("//input[@type='checkbox']").click()
                browser.find_element_by_xpath("//input[@type='submit']").click()
            except:
                pass

            wait_displayed("//b[text()='Prefer not to answer']", browser)
            for el in browser.find_elements_by_xpath("//b[text()='Prefer not to answer']"):
                el.click()
                time.sleep(1)
            browser.find_element_by_xpath("//input[@name='navfinish']").click()

            wait_displayed("//a[text()='Take Assessment']", browser)
            browser.find_element_by_xpath("//a[text()='Take Assessment']").click()

            # Assessment itself
            unfinished = True
            while unfinished:
                try:
                    obj = browser.switch_to.alert
                    obj.accept()
                    answers = browser.find_elements_by_xpath("//input[@class='deadInput']")
                    inputs = browser.find_elements_by_xpath("//input[@onpaste='event.returnValue=false;']")
                    for i, el in enumerate(answers):
                        ans = el.get_attribute('value')
                        fill_simple_validate(inputs[i], ans, browser)
                        time.sleep(np.random.randint(1, 2))
                    [k for k in browser.find_elements_by_xpath("//span[text()='Next']")
                     if k.is_displayed()][0].click()
                except:
                    unfinished = False

            # Finish up
            browser.switch_to.window(browser.window_handles[0])

            # Click next
            [k for k in browser.find_elements_by_xpath("//div[@aria-label='Continue']")
             if k.is_displayed()][0].click()
        except:
            print("No assessment")

        ### 7) Electronic data protection
        try:
            wait_visible((By.XPATH, "//span[contains(text(), 'I agree to the above')]"), browser)
            browser.find_element_by_xpath(
                "//span[contains(text(), 'I agree to the above')]/preceding-sibling::div/input").click()
            time.sleep(1)

            # Click next
            [k for k in browser.find_elements_by_xpath("//div[@aria-label='Continue']")
             if k.is_displayed()][0].click()
        except:
            print("No electronic data")

        ### 8) Rest of profile
        # Middle name
        el = browser.find_element_by_xpath(
            '//div[text()="Do you have a legal middle name?"]/parent::label/parent::div//table')
        iters = 0
        while not ("No" in el.text):
            el.click()
            down_enter(1, browser)
            iters += 1
            if iters >= 10:
                raise ValueError("Couldn't select middle name")

        # Select authorized to work in the US
        for el in browser.find_elements_by_xpath("//span[contains(text(),  'US')]"):
            if not el.find_element_by_xpath("parent::label/parent::div/input").is_selected():
                el.click()
            time.sleep(2)

        # When available
        scroll_fill_visible("//input[contains(@name, 'WhenAvailableToStart')]", details['start_date'], browser)

        # Other questions
        for qs, ans in [('require sponsorship', 'No'), ('Have you ever been employed', 'No'),
                        ('records under another name', 'No'), ('Are you related to any LabCorp', 'No'),
                        ('Years of Experience related', '1 - 3')]:
            el = browser.find_element_by_xpath('//div[contains(text(), "{}")]'.format(qs)
                                               + '/parent::label/parent::div//table')
            iters = 0
            while not (ans in el.text):
                el.click()
                down_enter(1, browser)
                iters += 1
                if iters >= 10:
                    raise ValueError("Couldn't select option for: {}".format(qs))

        # Select english as first language
        el = [k for k in browser.find_elements_by_xpath("//span[contains(text(),  'English')]")
              if k.is_displayed()][0]
        if not el.find_element_by_xpath("parent::label/parent::div/input").is_selected():
            el.click()
        time.sleep(2)

        # Click next
        [k for k in browser.find_elements_by_xpath("//div[@aria-label='Continue']")
         if k.is_displayed()][0].click()

        ### 9) Rest of employment history
        wait_visible((By.XPATH, '//h3[text()="Employment History"]'), browser)

        # Remove any employers
        while browser.find_element_by_xpath("//span[text()='Remove Last Employer']").is_displayed():
            time.sleep(1)
            click_at(browser.find_element_by_xpath("//span[text()='Remove Last Employer']"), browser)
            time.sleep(1)

        # Add these jobs
        for idx, h in enumerate(details['hist']):
            if idx > 0:
                click_at(browser.find_element_by_xpath("//span[text()='Add Employer']"), browser)
                time.sleep(5)

            # Employment type
            el = [k for k in browser.find_elements_by_xpath('//label[contains(text(), "Employment Type")]')
                  if k.is_displayed()]
            el = el[0].find_element_by_xpath('parent::div//table')
            iters = 0
            ans = 'Current'
            if idx > 0:
                ans = 'Previous'
            while not (ans in el.text):
                el.click()
                down_enter(1, browser)
                iters += 1
                if iters >= 10:
                    raise ValueError("Couldn't select employer type")

            # Employer details
            fill_simple_validate(
                browser.find_element_by_xpath("//input[contains(@name, 'employerName_{}')]".format(idx + 1)),
                str_format(h['name']), browser)
            fill_simple_validate(
                browser.find_element_by_xpath("//input[contains(@name, 'employerCity_{}')]".format(idx + 1)),
                str_format(h['city']), browser)
            fill_simple_validate(
                browser.find_element_by_xpath("//input[contains(@name, 'employerZip_{}')]".format(idx + 1)),
                "{:05d}".format(h['zip']), browser)

            # Country
            el = \
            [k for k in browser.find_elements_by_xpath('//label[contains(text(), "Country")]') if k.is_displayed()][0]
            el = el.find_element_by_xpath('parent::div//tbody')
            iters = 0
            while 'United States' not in el.text:
                el.click()
                down_enter(1, browser)
                time.sleep(2)
                iters += 1
                if iters >= 10:
                    raise ValueError("Couldn't find Country")

            # State
            el = [k for k in browser.find_elements_by_xpath('//label[contains(text(), "State")]') if k.is_displayed()][
                0]
            el = el.find_element_by_xpath('parent::div//tbody')
            iters = 0
            while states[h['state']] not in el.text:
                el.click()
                down_enter(1, browser)
                time.sleep(2)
                iters += 1
                if iters >= 60:
                    raise ValueError("Couldn't find State")

            # Other details
            phone = re.sub("[\s()-]", "", h['phone'])
            fill_simple_validate(
                browser.find_element_by_xpath("//input[contains(@name, 'employerSupvPhone_{}')]".format(idx + 1)),
                phone[:3] + '-' + phone[3:6] + '-' + phone[6:], browser)

            stm, sty = h['start'].split("/")
            goal = "{:02d}/01/{}".format(int(stm), sty)
            scroll_fill_visible("//label[contains(text(), 'Start Date')]/parent::div//input", goal, browser)
            if idx > 0:
                stm, sty = h['end'].split("/")
                goal = "{:02d}/01/{}".format(int(stm), sty)
                scroll_fill_visible("//label[contains(text(), 'End Date')]/parent::div//input", goal, browser)

            fill_simple_validate(
                browser.find_element_by_xpath("//input[contains(@name, 'StartTitle_{}')]".format(idx + 1)),
                str_format(h['position']), browser)
            fill_simple_validate(
                browser.find_element_by_xpath("//textarea[contains(@name, 'JobDuties_{}')]".format(idx + 1)),
                '. '.join([re.sub('\.$', '', d) for d in h['duties']]) + '.', browser)

            # May we contact
            el = [k for k in browser.find_elements_by_xpath('//span[contains(text(), "May we contact")]') if
                  k.is_displayed()][0]
            el = el.find_element_by_xpath('parent::div/parent::label/parent::div//tbody')
            iters = 0
            while "Yes" not in el.text:
                el.click()
                down_enter(1, browser)
                iters += 1
                if iters >= 10:
                    raise ValueError("Couldn't select contact permission")

            scroll_fill_visible("//input[contains(@name, 'RecordonDifferentName')]", 'n/a', browser)

        # Click next
        [k for k in browser.find_elements_by_xpath("//div[@aria-label='Continue']")
         if k.is_displayed()][0].click()

        ### 10) Skip licenses
        wait_displayed("//*[text()='Professional License and Certifications']", browser)

        # Click next
        [k for k in browser.find_elements_by_xpath("//div[@aria-label='Continue']")
         if k.is_displayed()][0].click()

        ### 11) Rest of education
        wait_visible((By.XPATH, '//h3[contains(text(), "Education History")]'), browser)

        # Only do section if incomplete
        complete = browser.find_elements_by_xpath("//b[text()='Education History']/parent::div//div")[-1].text
        if complete != "Complete":

            # Remove any education
            while browser.find_element_by_xpath("//span[text()='Remove Last Education']").is_displayed():
                time.sleep(1)
                click_at(browser.find_element_by_xpath("//span[text()='Remove Last Education']"), browser)
                time.sleep(1)

            # Degree
            el = [k for k in browser.find_elements_by_xpath('//span[contains(text(), "Diploma or Degree Obtained")]') if
                  k.is_displayed()][0]
            el = el.find_element_by_xpath('parent::div/parent::label/parent::div//tbody')
            iters = 0
            ans = 'HS Graduate'
            if details['col_name'] is not None:
                ans = '2 - Year College Degree'
            while ans not in el.text:
                el.click()
                down_enter(1, browser)
                iters += 1
                if iters >= 25:
                    raise ValueError("Couldn't select Degree type")

            # Major
            if details['col_name'] is not None:
                pos_majors = [k.get_attribute('innerText').strip('\xa0') for k in browser.find_elements_by_xpath(
                    "//span[contains(text(), 'Aviation')]/parent::td/parent::tr/parent::tbody//span[@class='label']")]
                if details['major'] not in pos_majors:
                    details['major'] = 'Other'

                el = [k for k in browser.find_elements_by_xpath('//label[contains(text(), "Major/Concentration")]') if
                      k.is_displayed()][0]
                el = el.find_element_by_xpath('parent::div//tbody')
                iters = 0
                while details['major'] not in el.text:
                    el.click()
                    down_enter(1, browser)
                    iters += 1
                    if iters >= 150:
                        raise ValueError("Couldn't select Major")

            # School name
            pos_schools = [k.get_attribute('innerText').strip('\xa0') for k in browser.find_elements_by_xpath(
                "//span[contains(text(), 'Other Educational Institution')]/parent::td/parent::tr/parent::tbody//span[@class='label']")]
            myschol = str_format(details['schl_name'])
            if details['col_name'] is not None:
                myschol = str_format(details['col_name']).replace('Community College', "").replace("University",
                                                                                                   "").replace(
                    "College", "")
            if myschol not in pos_schools:
                myschol = 'Other Educational Institution'

            el = [k for k in browser.find_elements_by_xpath('//label[contains(text(), "Major/Concentration")]') if
                  k.is_displayed()][0]
            el = el.find_element_by_xpath('parent::div//tbody')
            iters = 0
            while details['major'] not in el.text:
                el.click()
                down_enter(1, browser)
                iters += 1
                if iters >= 1000:
                    raise ValueError("Couldn't select School name")

            # Specific Degree
            el = \
            [k for k in browser.find_elements_by_xpath('//label[contains(text(), "Specific Diploma or Degree")]') if
             k.is_displayed()][0]
            el = el.find_element_by_xpath('parent::div//tbody')
            iters = 0
            ans = 'High School Graduate'
            if details['col_name'] is not None:
                ans = 'Associate of Arts'
            while ans not in el.text:
                el.click()
                down_enter(1, browser)
                iters += 1
                if iters >= 25:
                    raise ValueError("Couldn't select Degree type")

            # Country
            el = \
            [k for k in browser.find_elements_by_xpath('//label[contains(text(), "Country")]') if k.is_displayed()][0]
            el = el.find_element_by_xpath('parent::div//tbody')
            iters = 0
            while 'United States' not in el.text:
                el.click()
                down_enter(1, browser)
                time.sleep(2)
                iters += 1
                if iters >= 10:
                    raise ValueError("Couldn't find Country")

            # State
            el = [k for k in browser.find_elements_by_xpath('//label[contains(text(), "State")]') if k.is_displayed()][
                0]
            el = el.find_element_by_xpath('parent::div//tbody')
            iters = 0
            while states[h['state']] not in el.text:
                el.click()
                down_enter(1, browser)
                time.sleep(2)
                iters += 1
                if iters >= 60:
                    raise ValueError("Couldn't find State")

            # City
            search = SearchEngine(simple_zipcode=True)
            zipcode = search.by_zipcode(str(details['col_zip']))
            zip_dict = zipcode.to_dict()
            scroll_fill_visible("//input[contains(@name, 'educationCity')]", str_format(str(zip_dict['major_city'])),
                                browser)

            # Graduated?
            el = \
            [k for k in browser.find_elements_by_xpath('//label[contains(text(), "Graduated?")]') if k.is_displayed()][
                0]
            el = el.find_element_by_xpath('parent::div//tbody')
            iters = 0
            while "Yes" not in el.text:
                el.click()
                down_enter(1, browser)
                time.sleep(2)
                iters += 1
                if iters >= 60:
                    raise ValueError("Couldn't indicate graduation")

            # Different name?
            el = \
            [k for k in browser.find_elements_by_xpath('//div[contains(text(), "Is this educational record under")]') if
             k.is_displayed()][0]
            el = el.find_element_by_xpath('parent::label/parent::div//tbody')
            iters = 0
            while "No" not in el.text:
                el.click()
                down_enter(1, browser)
                time.sleep(2)
                iters += 1
                if iters >= 60:
                    raise ValueError("Couldn't indicate not different name")

        # Click next
        [k for k in browser.find_elements_by_xpath("//div[@aria-label='Continue']")
         if k.is_displayed()][0].click()

        ### 11) Profesional references
        try:
            wait_visible((By.XPATH, "//input[contains(@name, 'referenceName_1')]"), browser)
            fill_simple_validate(browser.find_element_by_xpath("//input[contains(@name, 'referenceName_1')]"),
                                 details['hist'][0]['supervisor'], browser)
            fill_simple_validate(browser.find_element_by_xpath("//input[contains(@name, 'referenceHomePhone_1')]"),
                                 details['hist'][0]['phone'], browser)
            fill_simple_validate(browser.find_element_by_xpath("//input[contains(@name, 'referenceCompany_1')]"),
                                 str_format(details['hist'][0]['name']), browser)
            fill_simple_validate(browser.find_element_by_xpath("//input[contains(@name, 'referenceEmail_1')]"),
                                 "na", browser)
            fill_simple_validate(browser.find_element_by_xpath("//input[contains(@name, 'referenceCity')]"),
                                 str_format(details['hist'][0]['city']), browser)

            # State
            el = [k for k in browser.find_elements_by_xpath('//label[contains(text(), "State")]') if k.is_displayed()][
                0]
            el = el.find_element_by_xpath('parent::div//tbody')
            iters = 0
            while states[details['hist'][0]['state']] not in el.text:
                el.click()
                down_enter(1, browser)
                time.sleep(2)
                iters += 1
                if iters >= 60:
                    raise ValueError("Couldn't find State")

            # Click next
            [k for k in browser.find_elements_by_xpath("//div[@aria-label='Continue']")
             if k.is_displayed()][0].click()

        except Exception as e:
            print("No references: {}".format(e))

        # ### 13) Requires wet signature!
        # try:
        #     wait_visible((By.XPATH, '//span[contains(text(), "Create a signature image to be used in conjunction")]'), browser)

        #     canvas = browser.find_element_by_tag_name("canvas")
        #     drawing = ActionChains(browser)
        #     drawing = drawing.click_and_hold(canvas)
        #     for k in range(10):
        #         drawing = drawing.move_by_offset(np.random.randint(10,20), np.random.randint(-20,20))
        #     for k in range(10):
        #         drawing = drawing.move_by_offset(np.random.randint(-25,15), np.random.randint(-20,20))

        #     drawing.release().perform()

        # except Exception as e:
        #     print("No wet signature: {}".format(e))

        # ### 14) E siganture
        # wait_visible((By.XPATH, "//input[contains(@name, 'esigABSignature_RTiAssignment')]"), browser)
        # fill_simple_validate(browser.find_element_by_xpath("//input[contains(@name, 'esigABSignature_RTiAssignment')]"),
        #         details['firstname'] + ' ' + details['lastname'], browser)
        # browser.find_elements_by_xpath("//input[@type='radio']")[0].click()
        # time.sleep(1)

        # browser.find_element_by_xpath('//b[contains(text(), "Please let us know if you received assistanc")]/parent::div/parent::label/parent::div/div/div/table').click()
        # down_enter(1, browser)

        # # Click next
        # time.sleep(5)
        # el = [k for k in browser.find_elements_by_xpath("//div[@aria-label='Continue']") if k.is_displayed()]
        # click_at(el[0], browser)
        # time.sleep(5)

        # ### 14) Review and submit
        # wait_visible((By.XPATH, "//*[contains(text(), 'Personal Information')]"), browser)

        # element = browser.find_element_by_tag_name('body')
        # element.screenshot("/accounts/projects/pkline/randres/randres/automation/screenshots/{}_app{}_page_final.png".format(firm,app_id))

        # # Click next
        # wait_visible((By.XPATH, "//div[@aria-label='Continue']"), browser)
        # el = [k for k in browser.find_elements_by_xpath("//div[@aria-label='Continue']") if k.is_displayed()]
        # click_at(el[0], browser)
        # time.sleep(5)

        # # Final confirmation
        # wait_visible((By.XPATH, "//div[contains(text(), 'Thank you for completing the application')]"), browser)

        # # Click next
        # time.sleep(10)
        # tryagain = True
        # iters = 0
        # while tryagain:
        #     try:
        #         el = [k for k in browser.find_elements_by_xpath("//div[@aria-label='Continue']") if k.is_displayed()]
        #         click_at(el[0], browser)
        #         tryagain = False
        #     except:
        #         iters += 1
        #         if iters >= 100:
        #             raise ValueError("Couldn't click continue")
        # time.sleep(5)

        # # Click next
        # el = [k for k in browser.find_elements_by_xpath("//div[@aria-label='Continue']") if k.is_displayed()]
        # click_at(el[0], browser)
        # time.sleep(5)

        # wait_visible((By.XPATH, "//*[contains(text(), 'Thank you for your interest in opportunities with the')]"), browser)

        # element = browser.find_element_by_tag_name('body')
        # element.screenshot("/accounts/projects/pkline/randres/randres/automation/screenshots/{}_app{}_page_submit.png".format(firm,app_id))

        # Close window
        browser.quit()
        display.sendstop()
        return None
    except Exception as e:
        print("Automation error for {} {} job {} {} {}: {}".format(details['firstname'], details['lastname'],
                                                                   details['firm'], details['city'], details['state'],
                                                                   e))
        try:
            element = browser.find_element_by_tag_name('body')
            element.screenshot(
                "/accounts/projects/pkline/randres/randres/automation/screenshots/{}_app{}_error.png".format(firm,
                                                                                                             app_id))
            browser.quit()
            display.sendstop()
        except:
            print("Couldn't print error screen")
        print('\a\a\a\a\a\a\a\a\a\a\a\a\a\a\a\a')
