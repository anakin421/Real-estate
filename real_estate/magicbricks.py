from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time

def scraper(keyword):

    chromedriver = "/home/abhishek/chromedriver_83"
    driver = webdriver.Chrome(chromedriver)
    driver.maximize_window()
    wait = WebDriverWait(driver, 30)

    driver.implicitly_wait(1000)

    driver.get("https://www.magicbricks.com/")

    keyword_elem = driver.find_element_by_xpath("//*[@id='keyword']")
    keyword_elem.send_keys(keyword)

    # time.sleep(3)

    # driver.find_element_by_xpath('//*[@id="keyword_suggest"]/div[2]').click()

    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="btnPropertySearch"]').click()


    # try:
    #     wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, 'post-tag'),tag))
    # except TimeoutException:

    #     print("timeout !!")
    #     driver.close()
    #     exit()

    time.sleep(50)  

    driver.close()

if __name__=='__main__':
    keyword = input("enter city name: ").strip()
    scraper(keyword)