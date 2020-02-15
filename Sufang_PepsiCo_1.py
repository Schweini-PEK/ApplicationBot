#!/usr/bin/env python
# coding: utf-8

# In[54]:


from selenium.webdriver.chrome.options import Options as chropopt
from pyvirtualdisplay import Display
from auto_functions import *


# In[55]:


"""UNCOMMENT HERE"""    

# display = Display(visible=0, size=(1200, 900))
# display.start()

chrome_options = chropopt()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=1200x900")
chrome_options.add_argument("--no-sanbdox")

"""UPDATE PATHS HERE"""

browserpath = '/Users/kendy/Desktop/For fun/Bot/chromedriver'
chrome_options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
browser = webdriver.Chrome(browserpath, options=chrome_options)


# In[74]:


"""
UNCOMMENT HERE
The links of the jobs are in the 'details', uncommented
"""

details = {'id': 1330,
                   'user_id': 45,
                   'job_id': 221,
                   'role_id': 221,
                   'firstName': 'Brad',
                   'lastName': 'Yoder',
                   'gender': 'Male',
                   'race': 'White',
                   'dob': '2/23/1973',
                   'phone': 4063845577,
                   'email': 'schweinikendy@gmail.com',
                   'password': 'tsf19980730',
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
                   'race': 'African American',
                   'jobtitle': 'Test',
                   'customer service experience': 'No Experience',
                   'truck operating experience': 'No Experience',
                   'under limited supervision working experience': 'No',
                   'grocery working experience': 'No Experience',
                   'product displaying experience': 'No Experience',
                   'different locations experience': 'No Experience',
                   'documenting DOT experience': 'No',
                   'documentation experience': 'No Experience',
                   'operating equipment experience': 'No Experience',
                   'merchandising products experience': 'No Experience',
                   'hands on activity experience': 'No Experience',
                   'feet working experience': 'No Experience',
                   'independent working experience': 'No Experience',
                   # 'link': 'https://www.pepsicojobs.com/unitedstates/jobs/5000578525506?lang=en-us&previousLocale=en-US',
                   'link': 'https://www.pepsicojobs.com/main/jobs/5000580989506?lang=en-us&previousLocale=en-US',
                   # 'link': 'https://www.pepsicojobs.com/main/jobs/5000582348306?lang=en-us&previousLocale=en-US',
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


# In[57]:


# Big picture opxtions
firm = details['raw_name']
app_id = details['id']

# 0) Go to URL

browser.get(details['link'])
wait_visible((By.XPATH, "//a[text()='Apply']"), browser)
scroll_shim(browser.find_element_by_xpath("//a[text()='Apply']"), browser)
browser.find_element_by_xpath("//a[text()='Apply']").click()


# In[58]:


fill_in_xpath("//input[@name='email']", details['email'], browser)
fill_in_xpath("//input[@name='password']", details['password'], browser)
fill_in_xpath("//input[@name='passwordConfirm']", details['password'], browser)
ActionChains(browser).send_keys(Keys.ENTER).perform()


# In[59]:


try:
    wait_visible((By.XPATH, "//span[contains(text(), 'Email in use already')]"), browser)
    click_link_by_text("Sign in with existing account", browser)
    fill_in_xpath("//input[@name='password']", details['password'], browser)
    click_at(browser.find_element_by_xpath("//button[contains(text(), 'SIGN IN')]"), browser)
    time.sleep(5)

    wait_visible((By.XPATH, "//div[contains(text(), 'Your application is not yet complete')]"), browser)
    click_at(browser.find_element_by_xpath("//div[contains(text(), 'Your application is not yet complete')]"),
             browser)
    time.sleep(5)
except:
    print("No need to log in ")


# In[7]:


# Enter information
wait_visible((By.XPATH, "//input[@name='firstName']"), browser)
scroll(browser.find_element_by_xpath("//input[@name='firstName']"), browser)
fill_simple_validate(browser.find_element_by_xpath("//input[@name='firstName']"), details['firstName'],
                     browser)
scroll(browser.find_element_by_xpath("//input[@name='lastName']"), browser)
fill_simple_validate(browser.find_element_by_xpath("//input[@name='lastName']"), details['lastName'],
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


# In[9]:


# state
el = browser.find_element_by_xpath('//label[text()="State"]/parent::div/table')
opt = ''
while not (opt == states[details['state']]):
    el.click()
    down_enter(1, browser)
    WebDriverWait(browser, 20).until(lambda browser:
                                     opt is not el.find_element_by_xpath(
                                         '//label[text()="State"]/parent::div/table//span').text.strip())
    opt = el.find_element_by_xpath('//label[text()="State"]/parent::div/table//span').text.strip()

# Click next
click_at(browser.find_elements_by_xpath("//div[@aria-label='Continue']")[-1], browser)


# In[48]:


# 1) Agree to data protection
try:
    browser.find_element_by_xpath(
        "//span[contains(@class, 'required')]/preceding-sibling::div/input").click()
    time.sleep(1)

    # Click next
    [k for k in browser.find_elements_by_xpath("//div[@aria-label='Continue']")
    if k.is_displayed()][0].click()
except:
    print("No data protection")


# In[8]:


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
    


# In[9]:


# 3) How did you hear about us
try:
    wait_visible((By.XPATH, '//label[text()="Main Source"]'), browser)
    el = browser.find_element_by_xpath('//label[text()="Main Source"]/parent::div/table')
    opt = ''
    iters = 0
    while not (opt == 'PepsiCo Website'):
        el.click()
        down_enter(1, browser)
        WebDriverWait(browser, 20).until(lambda browser:
                                         opt is not el.find_element_by_xpath(
                                             '//label[text()="Main Source"]/parent::div/table//span').text.strip())
        opt = el.find_element_by_xpath(
            '//label[text()="Main Source"]/parent::div/table//span').text.strip()
        iters += 1
        if iters >= 55:
            raise ValueError("Couldn't select source")

    # Click next
    [k for k in browser.find_elements_by_xpath("//div[@aria-label='Continue']")
     if k.is_displayed()][0].click()
    time.sleep(5)
except:
    print("No candidate source")


# In[10]:


# For Relief Route Sales Driver: https://www.pepsicojobs.com/main/jobs/5000582348306?lang=en-us&previousLocale=en-US

try:
    qs_list = [('A person of Cuban,',           'No'),
           ('one of the following categories',       details['race']),
           ('Voluntary Self-Identification', details['gender']),
           ('VETERAN', 'I CHOOSE NOT TO SELF IDENTIFY'),
           ('years of age or older?',   'Yes')
            ]

    for qs in qs_list:
        try:
            xp_question = "//span[contains(text(),'{}')]/following-sibling::label/child::span".format(qs[0])
            xp_answer = "[contains(text(), '{}')]".format(qs[1])
            browser.find_element_by_xpath(xp_question + xp_answer).click()
            print("Q complete ::: ", qs[0])
        except:
            try:
                xp_question = "//span[contains(text(),'{}')]/parent::div/following-sibling::label/child::span".format(qs[0])
                xp_answer = "[contains(text(), '{}')]".format(qs[1])
                browser.find_element_by_xpath(xp_question + xp_answer).click()
                print("Q complete ::: ", qs[0])
            except:
                try:
                    xp_question = "//h3[contains(text(),'{}')]/following-sibling::fieldset/child::label/child::span".format(qs[0])
                    xp_answer = "[contains(text(), '{}')]".format(qs[1])
                    browser.find_element_by_xpath(xp_question + xp_answer).click()
                    print("Q complete ::: ", qs[0])
                except :
                    try:
                        xp_answer = "//span[contains(text(), '{}')]".format(qs[1])
                        browser.find_element_by_xpath(xp_answer).click()
                        print("Q complete ::: ", qs[0])
                    except:
                        pass
except:
    pass


# In[49]:


# Confirm Personal Information

[k for k in browser.find_elements_by_xpath("//div[@aria-label='Continue']")
if k.is_displayed()][0].click()


# In[50]:


# Electronic Signature
scroll(browser.find_element_by_xpath("//input[@name='esigABSignature_RTiAssignment']"), browser)
signature = details['firstName'] + ' ' + details['lastName']
fill_simple_validate(browser.find_element_by_xpath("//input[@name='esigABSignature_RTiAssignment']"),
                         str_format(signature), browser)
browser.find_element_by_xpath(
        "//input[@name='esigABStatus_RTiAssignment']").click()

[k for k in browser.find_elements_by_xpath("//div[@aria-label='Continue']")
if k.is_displayed()][0].click()


# In[51]:


# Confirm after E-Signature

[k for k in browser.find_elements_by_xpath("//div[@aria-label='Continue']")
if k.is_displayed()][0].click()


# In[52]:


# In some jobs, there might need one more step to confirm
# AKA, Application Form Confirmation

try:
    [k for k in browser.find_elements_by_xpath("//div[@aria-label='Continue']")
    if k.is_displayed()][0].click()
except:
    print("No need for another 'Continue'")


# In[76]:


qs_list = [('Have you previously been employed by PBC or any division ',           'No'),
           ('This position will require PBC to verify every',       'Yes'),
           ('Please confirm the language you are completing this application in so we can optimize your candidate experience.',         'English/Inglés'),
           ('What is your highest level of completed education?',                      'High School Diploma or GED'),
           ('years of age or older?',   'Yes'),
           ('If I receive a bona fide contingent offer', 'Yes'),
           ('The target pay rate for this', 'Yes'),
           ('This position is for Day', 'Yes'),
           ('This position requires the following driver', 'Yes'),
           ('Are you comfortable with the responsibilities', 'Yes'),
           ('transportation to access', 'Yes'),
           ('Can you provide proof of insurance', 'Yes'),
           ('Are you available and willing', 'Yes'),
           ('Are you able and willing to perform', 'Yes'),
           ('Are you able and willing to cover', 'Yes'),
           ('Are you able and willing to start', 'Yes'),
           ('Are you able and willing to work', 'Yes'),
           ('For positions requiring a', 'Yes'),
           ('Experience with customer service', details['customer service experience']),
           ('Experience serving customers', details['customer service experience']),
           ('Experience operating trucks', details['truck operating experience']),
           ('Do you have experience working under limited supervision', details['under limited supervision working experience']),
           ('Experience getting to different locations', details['different locations experience']),
           ('Experience documenting DOT', details['documenting DOT experience']),
           ('Experience producing', details['documentation experience']),
           ('Experience operating equipment', details['operating equipment experience']),
           ('Experience merchandising', details['merchandising products experience']),
           ('How much experience do you have working in a retail,', details['grocery working experience']),
           ('How much experience do you have setting up product displays', details['product displaying experience']),
           ('How much experience do you have doing hands-on', details['hands on activity experience']),
           ('How much experience do you have working on your feet', details['feet working experience']),
           ('How much experience do you have working independently', details['independent working experience']),
           ('Do you have experience working holidays?', 'No'),
           ('Do you have experience working early shifts?', 'No'),
           ('Do you have experience working weekends?', 'No'),
           ('INCLUDING BUT NOT LIMITED TO', "I Agree")
            ]

for qs in qs_list:
    try:
        xp_question = "//div[contains(text(),'{}')]/parent::label/following-sibling::label/child::span".format(qs[0])
        xp_answer = "[text()='{}']".format(qs[1])
        browser.find_element_by_xpath(xp_question + xp_answer).click()
        print("Q complete ::: ", qs[0])
        
    except:
        try:
            xp_question = "//label[contains(text(),'{}')]/following-sibling::label/child::span".format(qs[0])
            browser.find_element_by_xpath(xp_question + xp_answer).click()
            print("Q complete ::: ", qs[0])
        except:
            pass


# In[10]:


"""UNCOMMENT HERE"""

# [k for k in browser.find_elements_by_xpath("//div[@aria-label='Continue']")
# if k.is_displayed()][0].click()
# 
# browser.quit()

