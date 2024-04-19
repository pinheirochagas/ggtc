
#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mpl_scatter_density
from astropy.visualization import LogStretch
from astropy.visualization.mpl_normalize import ImageNormalize

# add directory to path 
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath('/Users/pinheirochagas/Pedro/Stanford/code/fit2gpx/src'))))
from fit2gpx import Converter


# %%
# import csv as df
df = pd.read_csv('/Users/pinheirochagas/Downloads/strava_export/activities.csv')
# filter activities done in 2022
df = df[df['Activity Date'].str.contains('2022')]
# get unique values of activity type
df['Activity Type'].unique()
# set virtual ride and ride as the same activity type
df['Activity Type'] = df['Activity Type'].replace(['Virtual Ride', 'Ride'], 'Ride')
# filter for only rides
#df = df[df['Activity Type'] == 'Run']


# %%    
# concatenate all activities in one dataframe based on activity ID
df_concat = pd.DataFrame()
for activity_id in df['Filename']:
    file = '/Users/pinheirochagas/Downloads/strava_export/' + str(activity_id)[:-3] # dirty drop of gz
    # if file does not exist, skip
    if  os.path.exists(file) and os.path.isfile(file):
        conv = Converter()
        df_lap, df_point = conv.fit_to_dataframes(fname=file)
        df_concat = pd.concat([df_concat, df_point])
        continue

# %%
df_concat_filter = df_concat


# filter activities on the bay area

df_concat_filter = df_concat_filter[df_concat_filter['longitude'] > -122.7]
df_concat_filter = df_concat_filter[df_concat_filter['longitude'] < -122.3]
df_concat_filter = df_concat_filter[df_concat_filter['latitude'] > 37.7]
df_concat_filter = df_concat_filter[df_concat_filter['latitude'] < 38]


# %%
# filter activities done in december 2022























# %%
# make a density scatter plot

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(1, 1, 1, projection='scatter_density')
norm = ImageNormalize(vmin=0., vmax=100, stretch=LogStretch())
ax.scatter_density(df_concat_filter['longitude'], df_concat_filter['latitude'], dpi=100, norm=norm, cmap='viridis')
# set y lim
ax.set_ylim(37.7, 38)
# set x lim
ax.set_xlim(-122.7, -122.3)
# save image to pdf
plt.savefig('density_scatter.pdf', dpi=600, bbox_inches='tight')




# %%
file = '/Users/pinheirochagas/Downloads/dip_tam.fit'
conv = Converter()
df_lap, df_point = conv.fit_to_dataframes(fname=file)


# %%


# %%
# plot enhanced altitude
plt.plot(df_point['enhanced_altitude'])
# %%
# plot longitude, latitude and enhanced altitude in 3d dynamic
fig = plt.figure(figsize=(20,10))
ax = fig.add_subplot(111, projection='3d')
ax.plot(df_point['longitude'], df_point['latitude'], df_point['enhanced_altitude'])

#%% plot longitude, latitude and enhanced altitude in 3d dynamic plot





# %%
# plot longitude, latitude and enhanced altitude in 3d interactive plotly
import plotly.graph_objects as go


# %%
from fit2gpx import StravaConverter

DIR_STRAVA = '/Users/pinheirochagas/Downloads/strava_export/'

# Step 1: Create StravaConverter object 
# - Note: the dir_in must be the path to the central unzipped Strava bulk export folder 
# - Note: You can specify the dir_out if you wish. By default it is set to 'activities_gpx', which will be created in main Strava folder specified.

strava_conv = StravaConverter(
    dir_in=DIR_STRAVA
)

# Step 2: Unzip the zipped files
strava_conv.unzip_activities()

# Step 3: Add metadata to existing GPX files
strava_conv.add_metadata_to_gpx()

# Step 4: Convert FIT to GPX
strava_conv.strava_fit_to_gpx()

# %%
