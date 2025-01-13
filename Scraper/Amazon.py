from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from selenium_stealth import stealth
from selenium.common.exceptions import TimeoutException
from seleniumbase import Driver
from fake_useragent import UserAgent
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver import ChromeOptions
from Scraper.pushData import sync_to_woocommerce
from .Db import insertData
import random
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class AmazonScraper:
    def __init__(self, headless=False):
        ua = UserAgent()

        # Create Chrome options
        self.options = ChromeOptions()

        # Set up the proxy (SOCKS5)
        # self.options.add_argument(f'--proxy-server={socks_proxy}')

        # Set headless mode if required
        if headless:
            self.options.add_argument('--headless')

        # Other Chrome options to bypass bot detection
        self.options.add_argument('--start-maximized')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument(f"user-agent={ua.random}")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument("--disable-blink-features")

        # Initialize the driver using undetected_chromedriver
        # self.driver = uc.Chrome(options=self.options)
        self.driver = Driver(uc=True,headless2=True,headed=True,proxy="odyuipwr-rotate:o3aagt6vgwds@p.webshare.io:80")
        


        # Apply stealth to avoid detection
        stealth(self.driver, languages=["en-US", "en"],
                     vendor="Google Inc.",
                     platform="Win32",
                     webgl_vendor="Intel Inc.",
                     renderer="Intel Iris OpenGL Engine",
                     fix_hairline=True)

    def Keyword(self):
        try:
            return ['Laptop', 'Iphone16']
        except Exception as e:
            print('Error keywords-------', e)

    def getmainpage(self, url, keyword):
        try:
            self.driver.get(url)
            time.sleep(random.uniform(1, 5))
            searchbox = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#twotabsearchtextbox')))
            searchbox.send_keys(keyword)
            time.sleep(random.uniform(1, 5))
            submit_btn = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#nav-search-submit-button')))
            time.sleep(random.uniform(1, 5))
            submit_btn.click()
            time.sleep(random.uniform(1, 5))
        except Exception as e:
            print('Error In Getting Main Page', e)

    def getCards(self,api_sec,api_key,apiurl):
        try:
            hrefs = []
            while True:
                print("Starting to scrape product links...")
                time.sleep(random.uniform(1, 5))

                # Wait for the product links to appear
                get_a = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.a-link-normal.s-no-outline'))
                )

                for a in get_a:
                    try:
                        time.sleep(random.uniform(1, 3))
                        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", a)
                        time.sleep(random.uniform(1, 3))
                        url = a.get_attribute('href')
                        if url:
                            hrefs.append(url)
                        else:
                            print("URL is None or empty.")
                    except Exception as element_error:
                        print(f"Error processing element: {element_error}")
                
                backurl=self.driver.current_url
                for li in hrefs:
                    self.get_details(li,api_sec,api_key,apiurl)

                try:
                    hrefs.clear()
                    print('--')
                    self.driver.get(backurl)
                    
                    time.sleep(5)
                    NEXT_PAGE = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.s-pagination-item.s-pagination-next')))
                    self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", NEXT_PAGE)
                    time.sleep(random.uniform(1, 3))
                    NEXT_PAGE.click()
                    time.sleep(random.uniform(1, 3))
                except TimeoutError as e:
                    print('Element Donot Clickable', e)
                    break
                except Exception as e:
                    print('Error Msg For Exception', e)
                    break


        except Exception as e:
            print(f"Error in getCards(): {e}")
            return []

    def get_details(self, url,api_sec,api_key,apiurl):
        try:
            pass    
            self.driver.get(url)
            time.sleep(random.uniform(10, 15))
            self.driver.get(url)
            time.sleep(random.uniform(1, 2))
            Title = self.driver.title
            Description = None
            prices = None
            stock_status = None
            product_url = url,
            images = []
            sizes = []
            color_var = []
            try:
                print(Title)
                time.sleep(random.uniform(1, 2))
                ul_list = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div#altImages')))

                try:
                    all_img = ul_list.find_elements(By.TAG_NAME,'img')
                    for img in all_img:
                        src = img.get_attribute('src')
                        print(src)
                        images.append({'src':src})
                except Exception as e:
                    print('Error In Image Src')

            except Exception as e:
                print('Error While Scrapping Images.....')

            try:
                get_dec=WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'div#featurebullets_feature_div.celwidget')))
                Description=get_dec.text
                print(Description)
            except Exception as e:
                print('Some Error Found While Scraping Description')    
            
            try:
                get_price=WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'span.a-price-whole')))
                prices=get_price.text
                stock_status='In Stock'
                print(prices,stock_status)
            except Exception as e:
                print('error While Scraping prices')    

            try:
                try:
                    get_sizes=WebDriverWait(self.driver,10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,'p.a-text-left.a-size-base')))
                    for size in get_sizes:
                        sizes.append(size.text)
                    print(sizes)    
                except Exception as e:
                    print('Error While Scraping Sizes...')    
                try:
                    # List of common colors
                    common_colors = [
                        'black', 'pink', 'red', 'blue', 'green', 'yellow', 'white', 
                        'orange', 'purple', 'brown', 'gray', 'silver', 'gold', 'beige'
                    ]
                    get_color_ul=WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'ul.a-unordered-list.a-nostyle.a-button-list.a-declarative.a-button-toggle-group.a-horizontal.a-spacing-top-micro.swatches.swatchesSquare.imageSwatches')))
                    get_all_li=get_color_ul.find_elements(By.TAG_NAME,'li')
                    for li in get_all_li:
                        colortext=li.get_attribute('title')
                        for color in common_colors:
                            if color in colortext.lower():   
                                color_var.append(color)
                    print(color_var)            
                        
                except Exception as e:
                    print('Error While Scraping colors...')     

            except Exception as e:
                print('error in scrapping variations')        

            if prices:
                # Create a JSON object
                product_data = {
                    "name": Title,
                    "Description": Description,
                    "Prices": prices,
                    "StockStatus": stock_status,
                    "images": images,
                    "Sizes": sizes,
                    'product_url':url,
                    "ColorVariations": color_var
                }
                sync_to_woocommerce(product_data,apiurl,api_key,api_sec,False)    
                insertData('amazon',product_data)

        except TimeoutException as e:
            self.get_details(url)        

        except Exception as e:
                print('Error in getting details')
                


    def Quit_Browser(self):
        try:
            self.driver.quit()
        except Exception as e:
            print('Error', e)


def amaz_scraper(keys,api_sec,api_key,apiurl):
    amamzon = AmazonScraper()

    for key in keys:
        amamzon.getmainpage('https://www.amazon.com/gp/browse.html?node=21217037011&ref_=nav_em_sh_plugs-outlets_0_2_7_7', key)
        amamzon.getCards(api_sec,api_key,apiurl)
