from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from functools import reduce
import selenium.common.exceptions as err


delay = 10
driver = webdriver.Chrome()
driver.set_window_size(678, 700)
driver.get('https://techstepacademy.com/trial-of-the-stones')


def quit_driver(seconds=3):

    sleep(seconds)
    driver.quit()


def wait_until(_condition):
    WebDriverWait(driver, delay).until(_condition)


def activate_driver():
    try:
        driver.find_element_by_css_selector(
            'input[name="r1Input"]').send_keys('rock')

        driver.find_element_by_name('r1Btn').click()

        wait_until(EC.visibility_of_element_located((By.ID, 'passwordBanner')))

        pwd = driver.find_element_by_xpath(
            '//div[@id="passwordBanner"]/h4').text

        driver.find_element_by_name('r2Input').send_keys(pwd)

        driver.find_element_by_name('r2Butn').click()

        wait_until(EC.visibility_of_element_located((By.ID, 'successBanner1')))

        msg = driver.find_element_by_xpath('//div[@id="successBanner1"]/h4')

        assert msg.text == 'Success!'
        
        names = [
            s.text for s in driver.find_elements_by_xpath('//div/span')]
        wealth = [int(n.text)
                    for n in driver.find_elements_by_xpath('//div/span/../p')]
        max_amt = reduce(lambda a, b: a if a > b else b, wealth)

        for n, w in zip(names, wealth):
            if w == max_amt:
                driver.find_element_by_id('r3Input').send_keys(n)
                driver.find_element_by_id('r3Butn').click()
                break

        wait_until(EC.visibility_of_element_located(
            (By.ID, 'successBanner2')))

        msg2 = driver.find_element_by_id('successBanner2')

        assert msg2.text == 'Success!'

        driver.find_element_by_id('checkButn').click()
        wait_until(EC.visibility_of_element_located(
            (By.ID, 'trialCompleteBanner')))
        msg3 = driver.find_element_by_xpath(
            '//div[@id="trialCompleteBanner"]/h4')

        assert msg3.text == 'Trial Complete'
        
        print("Mission accomplished soulja")
        quit_driver(5)
        

    except err.NoSuchElementException:
        print('Did not find element you were looking for.')
        quit_driver()
    except err.TimeoutException:
        print('Loading took too much time')
        quit_driver()


activate_driver()
