# %%
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# %%
import pandas as pd
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt
from tqdm import tqdm
import time
import random
# %%
auth_url = "https://www.strava.com/oauth/token"
activites_url = "https://www.strava.com/api/v3/athlete/activities"

payload = {
    'client_id': "99300",
    'client_secret': '3807d10d20fc27ccaf92f90bd7f51ec4c7d077cf',
    'refresh_token': 'e089ab21dfbf2d449fd4c7b988cc5fe747402f69',
    'grant_type': "refresh_token",
    'f': 'json'
}

print("Requesting Token...\n")
res = requests.post(auth_url, data=payload, verify=False)
access_token = res.json()['access_token']
print("Access Token = {}\n".format(access_token))

print("Requesting pages (200 activities per full page)...")
activities_df = pd.DataFrame()
page = 1
page_non_empty = True
while page_non_empty:
    header = {'Authorization': 'Bearer ' + access_token}
    param = {'per_page': 200, 'page': page}
    my_activities = requests.get(activites_url, headers=header, params=param).json()
    activities_df = activities_df.append(my_activities, ignore_index=True)
    page_non_empty = bool(my_activities)
    print(page)
    page += 1

print("\n", len(activities_df), "activities downloaded")
# %%
