#Import Dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
import time

def init_browser():
    #Executable path to driver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()

    #Scraping for News and Articles
    #Setting URL
    url = "https://mars.nasa.gov/news/"

    #visit url with splinter
    browser.visit(url)
    #waiting for the page to load fully
    time.sleep(1)
    
    #HTML Object
    html = browser.html

    #Parse HTML with Beautiful Soup
    soup = bs(html, "html.parser")

    #Retrieve Elements for Latest News
    data = soup.find("div", class_='list_text')

    #Extracting Latest News and Paragraph Text

    news_title = data.find('div', class_='content_title').text.strip()
    news_p = data.find('div', class_='article_teaser_body').text.strip()

    #Scraping for images
    #Setting URL for Mars Space Images
    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    base_url = "https://www.jpl.nasa.gov/"

    #visit url with splinter
    browser.visit(url2)
    #
    time.sleep(1)
    #HTML Object
    images = browser.html

    #Parse HTML with Beautifuls Soup
    images_bs = bs(images, "html.parser")

    #Getting the featured image
    featured_image = images_bs.find('div', class_='carousel_items')('article')[0]['style'].replace("background-image: url('",'')\
                .replace(');','')[1:-1]

    #Creating featured image URL
    featured_image_url = base_url + featured_image
    featured_image_url  

    #Using pandas to extract the tables in the html
    url3 = "https://space-facts.com/mars/"
    tables = pd.read_html(url3)
    tables 

    #Creating a dataframe with the tables
    mars_facts_df = tables[0]
    mars_facts_df.columns=["Fact Description", "Values"]
    mars_facts_df.head()    

    #Converting to HTML table string
    html_table_string = mars_facts_df.to_html()
    html_table_string.replace('\n', '') 

    #Setting up URL and bs
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    hemisphere_base_url = "https://astrogeology.usgs.gov/"

    #visit with splinter
    browser.visit(hemisphere_url)
    time.sleep(1)

    #html object
    hemisphere_html = browser.html
    #beautiful soup
    hemisphere_soup = bs(hemisphere_html, "html.parser")  

    #Retrieving elements for hemisphere images
    hemisphere_data = browser.find_by_css("a.product-item h3")

    #Creating a list of dictionaries for the title and the image Url.
    hemisphere_image_urls = []

    for i in range(len(hemisphere_data)):
        browser.find_by_css("a.product-item h3")[i].click()
        hemisphere_images = browser.find_link_by_text("Sample").first 
    
        image_title = browser.find_by_css("h2.title").text
        title_image_hemisphere = {}
    
        title_image_hemisphere["title"]=image_title
        title_image_hemisphere["image_url"]=hemisphere_images["href"]
    
        hemisphere_image_urls.append(title_image_hemisphere)
       
        browser.back()
    
    print("hemisphere_image_url:", hemisphere_image_urls)

    marspage = {
        "Mars_News_Title": news_title,
        "Mars_News_Paragraph": news_p,
        "Mars_Featured_Image": featured_image_url,
        #"Mars_Facts": mars_facts_df.to_dict(orient='records'),
        "Mars_Facts": html_table_string,
        "Mars_Hemisphere_Images": hemisphere_image_urls
    } 
    
    browser.quit()

    return marspage


      