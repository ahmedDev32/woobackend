from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import undetected_chromedriver as uc
from selenium_stealth import stealth
from fake_useragent import UserAgent
from selenium.webdriver import ChromeOptions
from .pushData import sync_to_woocommerce
from selenium.webdriver.common.action_chains import ActionChains
from .Db import insertData
import random
import time

class WalmartScrapper:
    def __init__(self,headless=False):
        self.ua=UserAgent()
        chromeoptions=self.chromeoptions(headless)
        self.driver=uc.Chrome(options=chromeoptions)
        self.apply_sealth()

    def chromeoptions(self,headless):
        '''
        setup options for chrome driver
        '''    
        options=ChromeOptions()
        if headless:
            options.add_argument('--headless=new')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-gpu')
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(f"user-agent={self.ua.random}")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-blink-features")
        return options

    def apply_sealth(self): 
        '''
        Applying sealth to remains undective
        '''   
        stealth(self.driver,languages=["en-US", "en"],
                vendor="Google Inc.", platform="Win32",
                webgl_vendor="Intel Inc.", renderer="Intel Iris OpenGL Engine",
                fix_hairline=True)

    def get_key_words(self):
        try:
            return ['Iphone16','Laptop']
        except Exception as e:
            print('Error in getting keyword',e)                

    def call_long_press(self,element):
        try:
           click_me=WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,element)))
           initial_title=self.driver.title
           action=ActionChains(click_me)
           action.click_and_hold().perform()
           print('pressing elements.....')
           while True:
               current=self.driver.title
               if initial_title != current:
                   break
           action.release().perform()     
           return True
        except Exception as e:
            print('element invalid',e)            
            return False
    
    def handle_boot_detaction(self):
        try:
               print('we are facing boot detection.............') 
               get_all_p=WebDriverWait(self.driver,10).until(EC.visibility_of_all_elements_located((By.TAG_NAME,'p')))
               for p in get_all_p:
                   if p.text=='Press & Hold':
                       self.call_long_press(self.driver,p)
               

        except Exception as e:
            print('Error While PreventDetaction',e)    
            self.QuitBrowser()

    def scrape_main_page(self,url,searchkey):
        '''
        Move Driver To Main Page
        '''
        try:
            self.driver.get(url)
            time.sleep(random.uniform(1,2))
            try:
                input_tag=WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'input.flex-auto.lh-solid.sans-serif.search-bar.br-pill.f5.search-input-field-v2.b--none.search-bar-redesigned-v2')))
                time.sleep(random.uniform(1,5))
                input_tag.send_keys(searchkey)
                try:
                    time.sleep(random.uniform(1,2))
                    serch_icon=WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'button.absolute.bn.br-100.hover-bg-navy.search-icon-redesigned-v2')))
                    serch_icon.click()
                    time.sleep(random.uniform(1,2))
                except TimeoutError as e:
                    print('Time Out Element search icon not found')    

            except TimeoutError as e:
                print('failed To Fatch input_tag')    

        except Exception as e:
            print('Error Due To--->',e)    
            self.handle_boot_detaction()

    def scrape_cards_links(self,api_sec,apikey,api_url):
        try:
                hrefs=[]
                while True:
                 try:
                    time.sleep(5)
                    get_all_a=WebDriverWait(self.driver,10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,'a.w-100.h-100.z-1.hide-sibling-opacity.absolute')))
                    for a in get_all_a:
                        try:
                            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", a)
                            time.sleep(random.uniform(1,2))
                            link=a.get_attribute('href')
                            print(link)
                            hrefs.append(link)
                        except TimeoutException as e:
                            print('error while getting href-->',e)    

                    prev_url=self.driver.current_url        
                    for i in hrefs:
                        self.get_details(i,api_sec,apikey,api_url)        


                    try:
                        self.driver.get(prev_url)
                         
                        hrefs.clear()
                        time.sleep(5)
                        NEXT_PAGE=WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'a[aria-label="Next Page"]')))        
                        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",NEXT_PAGE)
                        time.sleep(random.uniform(1,5))
                        NEXT_PAGE.click()
                    except TimeoutException as e:
                        print('NEXT PAGE ENDED')    
                        break
                
                 except TimeoutException as e:
                    print('error get_all_a not found',e)

        except Exception as e:
            print('Error due to-->',e)        
            self.handle_boot_detaction()

    def get_details(self, url,api_sec,apikey,api_url):
     try:
        self.driver.get(url)
        time.sleep(random.uniform(1, 5))
        Title = self.driver.title
        Description = None
        prices = None
        stock_status = 'outofstock'
        product_url = url
        images = []
        sizes = []
        color_var = []

        try:
            get_image_div = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div[data-seo-id="hero-carousel-image"]'))
            )
            for div in get_image_div:
                try:
                    img = div.find_element(By.TAG_NAME, 'img')
                    src = img.get_attribute('src')
                    print(src)
                    images.append({'src':src})
                except TimeoutException as e:
                    print('Error while scraping img tag')

        except TimeoutException as e:
            print('Error While Scraping Images.....')

        try:
            get_price_span = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'span[data-seo-id="hero-price"]'))
            )
            if 'Now' in get_price_span.text:
             prices = get_price_span.text.replace('Now','')
            else:
             prices = get_price_span.text

            stock_status = 'instock'

        except Exception as e:
            print('Error while scraping price')

        try:
            desc = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.expand-collapse-content.dangerous-html.w_ckL_'))
            )
            Description = desc.text
        except TimeoutException as e:
            print('Error While Scraping Description')

        try:
            get_colors = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div.relative.z-1.br-100.h4.w4.self-center'))
            )
            for image in get_colors:
                try:
                    color = image.get_attribute('aria-label')
                    color_var.append(color)
                except Exception as e:
                    print('This Color Skipped...')
        except TimeoutException as e:
            print('Color Extraction Failed')

        try:
            # Extracting Sizes
            get_sizes_div = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, './/*[@id="item-page-variant-group-bg-div"]/div[3]/div[2]'))
            )
            get_all_span = WebDriverWait(get_sizes_div, 10).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'button[data-testid="variant-tile-chip"]'))
            )
            for span in get_all_span:
                try:
                    get_size = WebDriverWait(span, 10).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, 'span[aria-hidden="true"]'))
                    )
                    text = get_size.text.strip()
                    sizes.append(text)
                except Exception as e:
                    print('Failed To Get Attribute, skipping...')

        except Exception as e:
            print('Error While Scraping The Sizes')

        if prices:
            images.pop(0)
            # Prepare the product data for WooCommerce format
            product_data = {
                "name": Title,  # Product title
                "description": Description,  # Product description
                "regular_price": prices,  # Product price
                "stock_status": stock_status,  # Stock status ('instock' or 'outofstock')
                "product_url": product_url,  # Product URL
                "images": images,  # Image URLs
                "attributes": [
                    {"name": "Size", "options": sizes},  # Size options
                    {"name": "Color", "options": color_var}  # Color variations
                ]
            }
            print(product_data['images'])
            sync_to_woocommerce(product_data,api_url,apikey,api_sec)
            insertData('warlmart',product_data)

     except Exception as e:
        print('Facing Boot Detection')
        self.handle_boot_detection()
        self.__init__()



    def QuitBrowser(self):
        self.driver.quit()    


def main(keys,api_sec,apikey,api_url):
    Scraper=WalmartScrapper(True)
    for key in keys:
     Scraper.scrape_main_page('https://www.walmart.com/search?q=""',key)
     Scraper.scrape_cards_links(api_sec,apikey,api_url) 
    Scraper.QuitBrowser()
