# when exporting the artist info to csv the lists of instagram accounts
# were converted to strings. to avoid that mistake again do a .to_pickle()
# in this script I use literal_eval from 'ast' to convert the strings back to list

#%%
from ast import literal_eval
import pandas as pd
import scraper as sc

#%% read data
col_dtype = dict(Name=str,
                 Instagram=list)

artist_df = pd.read_csv('./output/name_insta_data.txt', header=0,
                        index_col=0, dtype=col_dtype)

#%% get all instagram accounts

insta_list = []
for cell in artist_df.loc[:, "Instagram"]:
    for insta in literal_eval(cell):
        insta_list.append(insta)

#%% creating dictionary with number of followers for each account
ctr = len(insta_list)
print("{} total artists to scrape. \n".format(ctr))

insta_dict = dict.fromkeys(insta_list)

for insta in insta_list:
    n_followers = sc.get_total_followers(insta)
    insta_dict[insta] = n_followers
    ctr -= 1
    print("{} instagram accounts left. \n".format(ctr))

print()
print("Done.")

#%% writing output to file

id_df = pd.DataFrame.from_dict(insta_dict, orient='index')
output_address = './output/follower_count.pkl'
id_df.to_pickle(output_address)
