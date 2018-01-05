#%%
import pandas as pd
import scraper as sc

#%% getting artist urls
CLE_URL = "http://www.villainarts.com/tattoo-conventions-villain-arts/\
cleveland-tattoo-arts-convention/artists-vendors-attending/"

artist_urls = sc.get_artists_urls(CLE_URL)

#%% getting names and instagram
artist_data = []

ctr = len(artist_urls)
print("{} total artists to scrape. \n".format(ctr))
for url in artist_urls:
    info = sc.get_artist_info(url)
    artist_data.append(info)
    ctr -= 1
    print("{} artists left. \n".format(ctr))

print()

#%% writing out artist info output

artist_df = pd.DataFrame(artist_data, columns=['Name', 'Instagram'])
output_address = '/output/name_insta_data.txt'

artist_df.to_csv('.' + output_address)

print("Done. Data saved to {}.".format(output_address))
