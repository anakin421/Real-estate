from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium. common. exceptions import NoSuchElementException,TimeoutException,StaleElementReferenceException,ElementClickInterceptedException
import time
import urllib.request
import os
from db_add_data import add_data
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def scraper(keyword):

    chromedriver = "/home/abhishek/chromedriver_83"
    driver = webdriver.Chrome(chromedriver)
    driver.maximize_window()
    wait = WebDriverWait(driver, 30)


    driver.get(f"https://www.magicbricks.com/property-for-sale/residential-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&cityName={keyword}")

    x = driver.find_element_by_css_selector('.save-your-search')

    if not len(x.text):
        print("Invalid keyword")
        driver.close()
        exit()


    city_name = driver.find_element_by_xpath('//*[@id="reqCity"]').text

    urls = driver.find_elements_by_css_selector(".domcache.js-domcache-srpgtm")
    
    url_list = [url.get_attribute("data-detailurl") for url in urls]


    for url in url_list:
        driver.get(url)

        data = dict()

        property_id = driver.find_element_by_css_selector(".propertyId").text.rsplit(" ",1)[1]
        print(f"Property Id: {property_id}")
        data["property_id"] = property_id

        check = add_data(data)
        if not check.check_duplication():
            continue

        price = driver.find_element_by_css_selector("#priceSv").text
        print(f"Price: {price}")
        data["price"] = price

        title = driver.find_element_by_css_selector(".p_bhk").text
        print(f"property name: {title}")
        data["title"] = title

        bedrooms = driver.find_element_by_css_selector(".seeBedRoomDimen").text.split(' ')[0]
        print(f"Bedrooms: {bedrooms}")
        data["bedrooms"] = bedrooms

        bathrooms = driver.find_element_by_css_selector("#firstFoldDisplay .p_infoColumn:nth-child(2) .p_value").text
        print(f"Bathrooms: {bathrooms}")
        data["bathrooms"] = bathrooms

        try:
            sqft = driver.find_element_by_css_selector("#secondFoldDisplay span").text
        except NoSuchElementException:
            sqft = None
        
        print(f"Area: {sqft} sqft")
        data["sqft"] = sqft

        # parking = driver.find_element_by_css_selector(".p_infoColumn:nth-child(4) .p_value").text
        try:
            parking = driver.find_element_by_xpath('//div[@class="p_title" and text()="Car parking"]').find_element_by_xpath("./following-sibling::div").text
        except NoSuchElementException:
            parking = None

        # parking = None if not len(parking) else parking
        # try:
        #     parking = 0 if not len(parking) else parking
        # except TypeError:
        #     parking = 0

        print(f"Parking: {parking}")
        data["parking"] = parking

        # description = driver.find_element_by_css_selector("#prop-detail-desc").text
        description = driver.find_element_by_xpath('//*[@id="propDetailDescriptionId"]/div[2]/div/div[1]').text.rstrip('more')
        print(f"Description: {description}")
        data["description"] = description

        # address = driver.find_element_by_xpath('//*[@id="propDetailDescriptionId"]/div[2]/div/div[4]/div[2]').text.split("What's")[0]

        address = driver.find_element_by_xpath('//div[@class="p_title" and text()="Address"]')
        
        add = address.find_element_by_xpath("./following-sibling::div").text.split("What's")[0]
        
        print(f"Address: {add}")
        data["address"] = add

        state = add.rsplit(", ",1)[1]
        print(f"City: {city_name}")
        print(f"State: {state}")

        data["city"] = city_name
        data["state"] = state

        list_date = driver.find_element_by_css_selector(".postedOn").text.split(": ")[1]
        data["list_date"] = list_date
        data["is_published"] = True

        try:
            realtor = driver.find_element_by_css_selector(".ph_viewPh .nameValue").text
        except NoSuchElementException:
            realtor = driver.find_element_by_css_selector(".CAName").text

        print(f"Realtor: {realtor}")
        data["realtor"] = realtor 

        driver.find_element_by_css_selector(".bigImage").click()


        try:
            iframe = driver.find_element_by_css_selector("#photoMapFrame")
            driver.switch_to.frame(iframe)
        except (NoSuchElementException,StaleElementReferenceException):
            image_list = []


        try:
            images = driver.find_elements_by_css_selector(".mbPhoto.projectComPhoto .imageZoomScrollBound img")
            image_list = [single_image.get_attribute("data-src") for single_image in images]
        except NoSuchElementException:
            image_list = []

        total_image = len(image_list)
        print(total_image)

        if not total_image:
            print("No images")
            continue

        path = os.path.join(BASE_DIR, f"real-estate/media/property_images/{property_id}")
        mode = 0o777
        
        os.makedirs(path, mode)


        # path = os.makedirs(f'{BASE_DIR}/images/{property_id}')
        # img_path = os.path.join(BASE_DIR, f'/images/{property_id}')

        # for img_url in image_list:
        #     urllib.request.urlretrieve(img_url, f"{path}/"+f"{img_url.rsplit('/')[-1]}")

        max_image = 7
        data_img_list = ['property_images/default.jpg'] * max_image

        req_image = max_image if total_image > 7 else total_image
        
        for i in range(req_image):
            img_path = f"{path}/"+f"{image_list[i].rsplit('/')[-1]}"

            try:
                urllib.request.urlretrieve(image_list[i], img_path)
            except urllib.error.HTTPError:
                media_img_path = 'media/property_images/default.jpg'
            
            media_img_path = img_path.split("media/")[1]
            data_img_list[i] = media_img_path

        data["photo_main"] = data_img_list[0]
        data["photo_1"] = data_img_list[1]
        data["photo_2"] = data_img_list[2]
        data["photo_3"] = data_img_list[3]
        data["photo_4"] = data_img_list[4]
        data["photo_5"] = data_img_list[5]
        data["photo_6"] = data_img_list[6]

        driver.switch_to.default_content()

        add = add_data(data)
        if add.check_duplication():
            add.insert_data()

        print("\n-------------------------------------------------------\n")


    driver.close()

if __name__=='__main__':
    keyword = input("enter city name: ").strip()
    scraper(keyword)