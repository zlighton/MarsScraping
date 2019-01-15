#import dependencies 
import pandas as pd 
from bs4 import BeautifulSoup as bs 
from splinter import Browser

def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    marsScrape = {}

    #Nasa Mars News
    #define and go to URL
    NASAUrl = "https://mars.nasa.gov/news/"
    browser.visit(NASAUrl)
    #BeautifulSoup connection
    html = browser.html
    NASASoup = bs(html, 'html.parser')
    #Headline of most recent article
    marsScrape['articleTitle'] = NASAsoup.find('div', class_='content_title').text
    marsScrape['articleSubtitle'] = NASAsoup.find('div', class_='rollover_description_inner').text
    
    #Mars Images from JPL
    #define and go to URL
    JPLUrl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(JPLUrl)
    #BeautifulSoup connection
    JPLHtml = browser.html
    JPLSoup = bs(JPLHtml, 'html.parser')
    #featured image scrape
    JPLFeatImg = JPLSoup.find('a', class_='button fancybox')['data-fancybox-href']
    #featured image url scrape
    marsScrape['JPLFeatImgUrl'] = f'https://www.jpl.nasa.gov{feat_img}'
    
    #Mars Weather from Twitter
    #define and go to URL
    twitterUrl = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitterUrl)
    #BeautifulSoup connection
    twitterHtml = browser.html
    twitterSoup = bs(twitterHtml, 'html.parser')
    #weather tweet scrape
    marsScrape['weatherTweet'] = twitterSoup.find('div', class_='js-tweet-text-container').get_text()

    #Mars Space Facts
    #define URL
    SpaceFactsUrl = 'https://space-facts.com/mars/'
    #use Pandas to read HTML directly into dataframe
    table = pd.read_html(SpaceFactsUrl)
    indexedDF = table[0]
    indexedDF.columns = ['Description', 'Value']
    #remove index
    DF = indexedDF.set_index('Description')
    #convert dataframe table to HTML for output
    marsScrape['htmlTable'] = DF.to_html()

    #Mars Hemispheres (website unavailable)


    return marsScrape