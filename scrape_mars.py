from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pandas as pd

def br_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = br_browser()
    mars_list = {}

    #mars news scrape
    browser.visit('https://mars.nasa.gov/news/')
    html = browser.html
    news_soup = bs(html, 'html.parser')
    news_title = browser.find_by_css('div.content_title a')[0].text
    news_p = news_soup.find_all('div', class_='article_teaser_body')[0].text

    browser.visit('https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html')
    browser.links.find_by_partial_text('FULL IMAGE').click()
    image = browser.find_by_css('img.fancybox-image')['src']
    image_url = image

    br_facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(br_facts_url)
    big_red_df = tables[2]
    big_red_df.columns = ['Description','Mars']
    big_red_df.set_index('Description', inplace=True)
    html_tbl = big_red_df.to_html()
    html_tbl.replace('\n','')

    #Mars Hemisphere name and image scrape
    main_url = 'https://astrogeology.usgs.gov'
    hemispheres = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres)
    hemispheres_html = browser.html
    h_soup = bs(hemispheres_html, 'html.parser')
    all_hemp= h_soup.find('div',class_ = 'collapsible results')
    big_red_hemp = all_hemp.find_all('div',class_='item')
    hemi_images = []

#for loop for hemi data
for d in big_red_hemp:
    #title
    hemisphere = d.find('div', class_ ="description")
    title = hemisphere.h3.text
    
    #Image link
    hemp_url = hemisphere.a["href"]
    browser.visit(main_url + hemisphere_url)
    
    i_html = browser.html
    i_soup = bs(i_html, 'html.parser')
    
    link = i_soup.find('div', class_ ='downloads')
    image_url = link.find('li').a['href']
    
    