#%%
import time
import re
import requests
from bs4 import BeautifulSoup as bs


#%% get artists urls


def get_artists_urls(url):
    '''get artists url list from convention url
    - pars -
    url: string; address to page with list of artists for a specific convention
    - returns -
    artists_urls: list of strings; links to each artist page in villainarts website
    '''
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
    '''get artists name and instagram from artist url
    - pars -
    url: string, address to page artist page on villainarts domain
    - returns -
    name, insta: str, list of str; artist name and list of artist instagram page
    (usually personal page and studio page)
    '''
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
            # splitting by '/'
            link_url_list = link_url.split('/')
            # removing empty elements
            link_url_list = [i for i in link_url_list if i is not '']
            # gettig last element (insta_name and appending to insta list)
            insta.append(link_url_list[-1])
    return name, insta


#%% get number of instagram followers from instagram name

def get_total_followers(insta_name):
    '''get number of followers (float) from instagram username from profile webpage
    - pars -
    insta_name: str; instagram username
    - returns -
    n_followers: float; number of instagram followers'''
    url = "https://www.instagram.com/" + insta_name
    time.sleep(1)
    response = requests.get(url)
    html = response.text
    # parsing html
    soup = bs(html, 'html.parser')
    # getting n_followers
    # relevant piece of text
    insta_text = str(soup.find_all('script', type="text/javascript"))
    # regex to find follower count piece
    pattern = r"\"followed_by\": {\"count\":\s\d+"
    try:
        insta_text_refined = re.search(pattern, insta_text).group()
    except:
        return None
    # getting the numbers out of the text
    pattern = r"\d+"
    n_followers = re.search(pattern, insta_text_refined).group()
    # ensuring they're floats and return
    return float(n_followers)
