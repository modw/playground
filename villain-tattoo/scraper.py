#%%
import time
import requests
import re
from bs4 import BeautifulSoup as bs


#%% get artists urls


def get_artists_urls(url):
    '''get artists url list from convention url'''
    time.sleep(1)
    response = requests.get(url)
    html = response.text
    # parsing html
    soup = bs(html, 'html.parser')
    links = soup.find_all("a", href=True)
    link_pre = "http://www.villainarts.com/artists/"
    artists_urls = []
    for link in links:
        link_url = link['href']
        if link_url.startswith(link_pre):
            artists_urls.append(link_url)

    # excluding duplicates
    artists_urls = list(set(artists_urls))
    return sorted(artists_urls)


#%% get artists name and instagram links from artist page


def get_artist_info(url):
    '''get artists name and instagram from artist url'''
    time.sleep(1)
    response = requests.get(url)
    html = response.text
    # parsing html
    soup = bs(html, 'html.parser')

    # name
    name = soup.h1.text

    # instagram
    insta = []
    info_links = soup.find("div", class_="span3").find_all("a")
    for link in info_links:
        link_url = link['href']
        if re.search('instagram', link_url):
            print(link_url)
            # splitting by '/'
            link_url_list = link_url.split('/')
            # removing empty elements
            link_url_list = [i for i in link_url_list if i is not '']
            # gettig last element (insta_name and appending to insta list)
            insta.append(link_url_list[-1])
    return name, insta


#%% get number of instagram followers from instagram name

def get_total_followers(insta_name):
    '''get number of followers (float) from instagram username from profile webpage'''
    url = "https://www.instagram.com/" + insta_name
    time.sleep(1)
    response = requests.get(url)
    html = response.text
    # parsing html
    soup = bs(html, 'html.parser')
    # getting n_followers
    descr = soup.find('html').find(
        'meta', property="og:description")['content']
    n_followers = descr.split()[0]
    n_followers = float(''.join(n_followers.split(",")))
    return n_followers

#%% looping over every artist of convention and getting instagram


CONV_CLE_URL = "http://www.villainarts.com/tattoo-conventions-villain-arts/\
cleveland-tattoo-arts-convention/artists-vendors-attending/"

artists_links = get_artists_urls(CONV_CLE_URL)
artists_info = []

counter = 0  # to test
for link in artists_links:
    info = get_artist_info(link)
    artists_info.append(info)
    print(info)

    counter += 1
    if counter == 8:
        print('')
        print('-----------------')
        print('')
        break
