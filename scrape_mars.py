#Import Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time


def init_browser():
    executable_path = {"executable_path": "C:/Program Files/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    
    # Create a dictionary to store all Mars data
    mars_dictionary = {}
    
    #----------------------------------------------------------------------------------------------------------------------------
    
    # Scrape Nasa News for latest News
    url = 'https://mars.nasa.gov/news'
    response = requests.get(url)
    soup = bs(response.text, 'lxml')

    results = soup.find('div', class_='features')
    news_title = results.find('div', class_='content_title').text
    newsp = results.find('div', class_='rollover_description').text
    
    # Store scraped data in dictionary
    mars_dictionary['title'] = title
    mars_dictionary['text'] = text
    
    #----------------------------------------------------------------------------------------------------------------------------
    
    # Scrape Nasa for Featured Image
    nasa_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(nasa_url)

    nasa_html = browser.html
    nasa_soup = bs(nasa_html, "lxml")

    image = nasa_soup.find('div', class_='default floating_text_area ms-layer').find('footer')
    image_url = 'https://www.jpl.nasa.gov'+ image.find('a')['data-fancybox-href']
    
    # Store scraped image url to dictionary
    mars_dictionary['image_url'] = image_url
    
    #----------------------------------------------------------------------------------------------------------------------------
    
    # Scrape Mars Weather from Twitter
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    twitter_response = requests.get(twitter_url)
    twitter_soup = bs(twitter_response.text, 'lxml')
    
    twitter_result = twitter_soup.find('div', class_='js-tweet-text-container')
    weather = twitter_result.find('p', class_='js-tweet-text').text
    
    # Store scraped data in dictionary
    mars_dictionary['weather'] = weather
    
    #----------------------------------------------------------------------------------------------------------------------------

    # Scrape Mars facts
    facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(facts_url)
    df = tables[0]
    df.columns = ['Description', 'Value']
    df.set_index('Description', inplace=True)

    # Export scraped data table to html    
    facts = df.to_html()
    facts.replace("\n","")
    df.to_html('facts.html')

    # Store scraped data in dictionary
    mars_dictionary['facts'] = facts
    
    
    #----------------------------------------------------------------------------------------------------------------------------

    # Scrape hemisphere images of Mars
    h_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(h_url)

    h_html = browser.html
    he_soup = bs(h_html, 'lxml')
    base_url ="https://astrogeology.usgs.gov"

    h_list = h_soup.find_all('div', class_='item')

    # Create a list to store urls and image titles
    h_image_urls = []

    # Loop through list to find images
    for image in h_list:

        # Create a dicitonary to store urls and titles
        h_dictionary = {}
        
        # Find link to large image
        href = image.find('a', class_='itemLink product-item')
        link = base_url + href['href']

        # Visit the link
        browser.visit(link)

        # Parse the html of the new page
        h_html2 = browser.html
        h_soup2 = bs(h_html2, 'lxml')

        # Find image title
        img_title = h_soup2.find('div', class_='content').find('h2', class_='title').text
        
        # Append to dictionary
        h_dictionary['title'] = img_title
        
        # Find image url
        img_url = h_soup2.find('div', class_='downloads').find('a')['href']
        
        # Append to dictionary
        h_dictionary['url_img'] = img_url
        
        # Append dictionary to list
        h_image_urls.append(h_dictionary)
        
    # Store hemisphere image urls in dictionary
    mars_dictionary['h_image_urls'] = h_image_urls
    
    return mars_dictionary