from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium. common. exceptions import NoSuchElementException,TimeoutException,StaleElementReferenceException,ElementClickInterceptedException
import time

def scraper(keyword):

    chromedriver = "/home/abhishek/chromedriver_83"
    driver = webdriver.Chrome(chromedriver)
    driver.maximize_window()
    # wait = WebDriverWait(driver, 30)


    driver.get(f"https://www.magicbricks.com/property-for-sale/residential-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&cityName={keyword}")

    # try:
    x = driver.find_element_by_css_selector('.save-your-search')
    # print(x.text)
    # print(len(x.text))

    if not len(x.text):
        print("Invalid keyword")
        driver.close()
        exit()

        # x = driver.find_element_by_xpath('//*[@id="reqCity"]').text
        # print(x)
    # except NoSuchElementException:
    #     print("Invalid keyword")
    #     driver.close()  
    #     exit()

    # keyword_elem = driver.find_element_by_xpath("//*[@id='keyword']")
    # keyword_elem.send_keys(keyword)

    city_name = driver.find_element_by_xpath('//*[@id="reqCity"]').text
    print(city_name)

    # time.sleep(10)
    urls = driver.find_elements_by_css_selector(".domcache.js-domcache-srpgtm")
    
    url_list = [url.get_attribute("data-detailurl") for url in urls]

    # print(url_list)
    # print(len(url_list))

    for url in url_list:
        driver.get(url)

        price = driver.find_element_by_css_selector("#priceSv").text
        print(f"Price: {price}")

        name = driver.find_element_by_css_selector(".p_bhk").text
        print(f"property name: {name}")

        bedroom = driver.find_element_by_css_selector(".seeBedRoomDimen").text.split(' ')[0]
        print(f"Bedrooms: {bedroom}")

        bathroom = driver.find_element_by_css_selector("#firstFoldDisplay .p_infoColumn:nth-child(2) .p_value").text
        print(f"Bathrooms: {bathroom}")

        try:
            area = driver.find_element_by_css_selector("#secondFoldDisplay span").text
        except NoSuchElementException:
            area = None
        
        print(f"Area: {area} sqft")

        # parking = driver.find_element_by_css_selector(".p_infoColumn:nth-child(4) .p_value").text
        try:
            parking = driver.find_element_by_xpath('//div[@class="p_title" and text()="Car parking"]').find_element_by_xpath("./following-sibling::div").text
        except NoSuchElementException:
            parking = None

        print(f"Parking: {parking}")

        # description = driver.find_element_by_css_selector("#prop-detail-desc").text
        description = driver.find_element_by_xpath('//*[@id="propDetailDescriptionId"]/div[2]/div/div[1]').text.rstrip('more')
        print(f"Description: {description}")

        # address = driver.find_element_by_xpath('//*[@id="propDetailDescriptionId"]/div[2]/div/div[4]/div[2]').text.split("What's")[0]

        address = driver.find_element_by_xpath('//div[@class="p_title" and text()="Address"]')
        
        add = address.find_element_by_xpath("./following-sibling::div").text.split("What's")[0]
        
        print(f"Address: {add}")

        state = add.rsplit(", ",1)[1]
        print(f"City: {city_name}")
        print(f"State: {state}")

        # try:
        #     realtor = driver.find_element_by_css_selector(".CA_agent_name").text
        # except NoSuchElementException:
        #     realtor = driver.find_element_by_css_selector(".commercialName").text
        
        try:
            realtor = driver.find_element_by_css_selector(".ph_viewPh .nameValue").text
        except NoSuchElementException:
            realtor = driver.find_element_by_css_selector(".CAName").text

        print(f"Realtor: {realtor}")

        print("\n-------------------------------------------------------\n")

    exit()
    property_links = driver.find_elements_by_class_name('m-srp-card__title')


    for single_property in property_links:
        try:
            single_property.click()

            
            # driver.find_element_by_xpath('//span[@node-type="data-detailurl"]')
        
        
        except ElementClickInterceptedException:
            continue
        # driver.find_element(By.CSS_SELECTOR("body")).sendKeys(Keys.CONTROL + "w")
        # driver.close()

    driver.close()

    # time.sleep(1)
    # x = driver.find_element_by_xpath('//*[@id="keyword_suggest"]/div[2]').text
    # print(x)

    # # driver.find_element_by_id('keyword_suggest')

    # # driver.find_element_by_xpath('//*[@id="keyword"]').click()
    # # time.sleep(1)
    
    # time.sleep(1)
    # driver.find_element_by_xpath('//*[@id="keyword_suggest"]/div[2]').click()

    # time.sleep(2)
    # driver.find_element_by_xpath('//*[@id="btnPropertySearch"]').click()


    # # try:
    # #     wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, 'post-tag'),tag))
    # # except TimeoutException:

    # #     print("timeout !!")
    # #     driver.close()
    # #     exit()

    # time.sleep(50)  

    # driver.close()

if __name__=='__main__':
    keyword = input("enter city name: ").strip()
    scraper(keyword)