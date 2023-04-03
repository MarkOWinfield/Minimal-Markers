# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 11:13:08 2023

@author: bzmow
"""

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")


st.header("Cider Apple Locations")

dfLatLong = pd.read_csv('./data/lat_long.csv')
# dfLatLong["Number of Markers"] = dfLatLong["Number of Markers"].astype(str) #convert to string
# df["size"] = df["size"].astype(float) #convert back to numeric

 
# data = {"lat": dfLatLong['Latitude'],
#         "lon": dfLatLong['Longitude'],
#         "What 3 Words": dfLatLong['What3Words']}
 
# df = pd.DataFrame(data)
# df
# st.map(data=df)

# df = pd.read_csv('./data/wellbore_exploration_all.csv', 
#                   usecols=['wlbWellboreName', 'wlbNsDecDeg', 'wlbEwDesDeg'])

# df.columns = ['Well Name', 'latitude', 'longitude']

fig = px.scatter_mapbox(dfLatLong, lat="Latitude", lon="Longitude",
                        hover_name="Variety",
                        hover_data=["What3Words", "Pomiferous"],
                        color='Identified',
                        color_discrete_map={
                            "No": "red", 
                            "Yes": "green", 
                            "Yes (with mismatch)": "blue"},
                        category_orders={"Identified": ["No", "Yes", "Yes (with mismatch)"]},
                        size="Size", zoom=8, height=600, width=1200)
# fig = px.scatter_mapbox(dfLatLong, lat="Latitude", lon="Longitude", hover_name="Variety",
#                         color='Identified', color_discrete_sequence=["red", "green", "blue"], size="Size", zoom=8, height=600, width=1200)
# fig = px.scatter_mapbox(dfLatLong, lat="Latitude", lon="Longitude", hover_name='What3Words',  hover_data=["Variety", "Number of Markers"],
#                         color='Number of Markers', color_discrete_sequence=px.colors.qualitative.Plotly, zoom=8, height=600, width=800)
# fig = px.scatter_mapbox(dfLatLong, lat="Latitude", lon="Longitude", hover_name='What3Words',  hover_data=["Variety", "Number of Markers"],
                        # color='Number of Markers', color_continuous_scale=px.colors.cyclical.IceFire, size='Number of Markers', size_max=11,zoom=7, height=600, width=800)
# fig = px.scatter_mapbox(dfLatLong, lat="Latitude", lon="Longitude", hover_name='What3Words',  hover_data=["Variety", "Flavour"],
#                         color_discrete_sequence=["#FF0000"], zoom=7, height=600, width=800)

# color_discrete_map={
#                 "Europe": "red",
#                 "Asia": "green",
#                 "Americas": "blue",
#                 "Oceania": "goldenrod",
#                 "Africa": "magenta"},
#              category_orders={"continent": ["Oceania", "Europe", "Asia", "Africa", "Americas"]},
#              title="Explicit color mapping with explicit ordering"




fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig)

# import plotly.express as px
# px.set_mapbox_access_token(open(".mapbox_token").read())
# df = px.data.carshare()
# fig = px.scatter_mapbox(df, lat="centroid_lat", lon="centroid_lon",     color="peak_hour", size="car_hours",
#                   color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10)
# fig.show()
