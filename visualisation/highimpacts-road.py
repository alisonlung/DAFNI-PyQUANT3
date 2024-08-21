"""
highimpacts_road.py
Choropleth and flow maps of road mode.
"""

import os
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import plotly.express as px
import contextily as cx
import cartopy.crs as ccrs
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

################################################################################

"""
Choropleth Maps
calculated by the mean score of statistics where the particular zone number was used as origin/ destination
"""
#Choropleth maps - Quantiles
def plot_CkDiffRoad_quantiles(impacts_df, neti):
    df_mean = []

    #for each unqiue zone number, calculate mean score by zone that appeared in i/ j
    for i in neti:
        mean_score = impacts_df.loc[(impacts_df[' net_i'] == i) | (impacts_df[' net_j'] == i), 'CkDiffRoad'].mean()
        subset_df = pd.DataFrame({' net_i': [i], 'CkDiffRoad': [mean_score]})
        df_mean.append(subset_df)

    df_mean = pd.concat(df_mean, ignore_index=True)

    #merge to retrive geometry 
    df_mean = df_mean.merge(ews_i[[' net_i', 'zonei_geom']], on = ' net_i', how = 'left')
    df_mean = df_mean.set_geometry('zonei_geom')

    #plot with quantiles scheme 
    ax = df_mean.plot(column='CkDiffRoad', scheme='Quantiles', k=8, cmap='inferno', legend=True, figsize=(9.0, 15.5), legend_kwds={'title': 'CkDiffRoad', "fmt": "{:.0f}"})
    cx.add_basemap(ax, crs=df_mean.crs, source=cx.providers.CartoDB.PositronNoLabels)

    #export
    plt.savefig("outputs/road/CkDiffRoad_quantile.png", transparent=True)

def plot_SavedSecsRoad_quantiles(impacts_df, neti):
    df_mean = []

    #for each unqiue zone number, calculate mean score by zone that appeared in i/ j
    for i in neti:
        mean_score = impacts_df.loc[(impacts_df[' net_i'] == i) | (impacts_df[' net_j'] == i), 'SavedSecsRoad'].mean()
        subset_df = pd.DataFrame({' net_i': [i], 'SavedSecsRoad': [mean_score]})
        df_mean.append(subset_df)
    
    df_mean = pd.concat(df_mean, ignore_index=True)

    #merge to retrive geometry 
    df_mean = df_mean.merge(ews_i[[' net_i', 'zonei_geom']], on = ' net_i', how = 'left')
    df_mean = df_mean.set_geometry('zonei_geom')

    #plot with quantiles scheme
    ax = df_mean.plot(column='SavedSecsRoad', scheme='Quantiles', k=8, cmap='inferno', legend=True, figsize=(9.0, 15.5), legend_kwds={'title': 'savedSecsRoad', "fmt": "{:.0f}"})
    cx.add_basemap(ax, crs=df_mean.crs, source=cx.providers.CartoDB.PositronNoLabels)

    #export
    plt.savefig("outputs/road/savedSecsRoad_quantile.png", transparent=True)    

#Choropleth maps - FisherJenks
def plot_CkDiffRoad_fisherjenks(impacts_df, neti):
    df_mean = []

    #for each unqiue zone number, calculate mean score by zone that appeared in i/ j
    for i in neti:
        mean_score = impacts_df.loc[(impacts_df[' net_i'] == i) | (impacts_df[' net_j'] == i), 'CkDiffRoad'].mean()
        subset_df = pd.DataFrame({' net_i': [i], 'CkDiffRoad': [mean_score]})
        df_mean.append(subset_df)

    df_mean = pd.concat(df_mean, ignore_index=True)

    #merge to retrive geometry 
    df_mean = df_mean.merge(ews_i[[' net_i', 'zonei_geom']], on = ' net_i', how = 'left')
    df_mean = df_mean.set_geometry('zonei_geom')

    #plot with quantiles scheme 
    ax = df_mean.plot(column='CkDiffRoad', scheme='FisherJenks', k=8, cmap='inferno', legend=True, figsize=(9.0, 15.5), legend_kwds={'title': 'CkDiffRoad', "fmt": "{:.0f}"})
    cx.add_basemap(ax, crs=df_mean.crs, source=cx.providers.CartoDB.PositronNoLabels)

    #export
    plt.savefig("outputs/road/CkDiffRoad_fisherjenks.png", transparent=True)

def plot_SavedSecsRoad_fisherjenks(impacts_df, neti):
    df_mean = []

    #for each unqiue zone number, calculate mean score by zone that appeared in i/ j
    for i in neti:
        mean_score = impacts_df.loc[(impacts_df[' net_i'] == i) | (impacts_df[' net_j'] == i), 'SavedSecsRoad'].mean()
        subset_df = pd.DataFrame({' net_i': [i], 'SavedSecsRoad': [mean_score]})
        df_mean.append(subset_df)
    
    df_mean = pd.concat(df_mean, ignore_index=True)

    #merge to retrive geometry 
    df_mean = df_mean.merge(ews_i[[' net_i', 'zonei_geom']], on = ' net_i', how = 'left')
    df_mean = df_mean.set_geometry('zonei_geom')

    #plot with quantiles scheme
    ax = df_mean.plot(column='SavedSecsRoad', scheme='FisherJenks', k=8, cmap='inferno', legend=True, figsize=(9.0, 15.5), legend_kwds={'title': 'savedSecsRoad', "fmt": "{:.0f}"})
    cx.add_basemap(ax, crs=df_mean.crs, source=cx.providers.CartoDB.PositronNoLabels)

    #export
    plt.savefig("outputs/road/savedSecsRoad_fisherjenks.png", transparent=True)    

################################################################################

"""
Flow Maps
arrows that show the top destination for each origin
"""
#Flow maps
def plot_CkDiffRoad_flowmap(merged_df):
    #group by net_i and retrieve top destination
    neti_groups = merged_df.groupby(' net_i')
    top_1_list = []
    for neti, group_data in neti_groups:
        top_1 = group_data.nlargest(1, 'CkDiffRoad') 
        top_1_list.append(top_1)
    top_1_df = pd.concat(top_1_list)
    top_1_df = top_1_df.sort_values('CkDiffRoad')

    #calculate centroids
    top_1_df['centroid_i'] = top_1_df['zonei_geom'].apply(lambda geom: geom.centroid)
    top_1_df['centroid_j'] = top_1_df['zonej_geom'].apply(lambda geom: geom.centroid)

    #set up colourmap
    cmap = plt.get_cmap("Spectral").reversed() 
    tmax = top_1_df['CkDiffRoad'].max()
    tmin = top_1_df['CkDiffRoad'].min()
    norm = Normalize(tmin, tmax)

    #plot arrows
    fig, ax = plt.subplots(figsize=(9.0, 15.5))

    for index, row in top_1_df.iterrows():
        #calculate arrow properties
        arrow_color = cmap(norm(row['CkDiffRoad']))
        arrow_start = (row['centroid_i'].x, row['centroid_i'].y)
        arrow_end = (row['centroid_j'].x, row['centroid_j'].y)
        arrow_dx = arrow_end[0] - arrow_start[0]
        arrow_dy = arrow_end[1] - arrow_start[1]
        #plot arrow
        ax.annotate("", xy=arrow_end, xytext=arrow_start, arrowprops=dict(arrowstyle="->", color=arrow_color, lw=0.25))
    
    #set up plot 
    #bounding box of the geometry column
    merged_df = merged_df.set_geometry('zonei_geom')
    bounds = merged_df.geometry.total_bounds  
    #set plot limits
    ax.set_xlim(bounds[0] - 20000, bounds[2] + 20000)
    ax.set_ylim(bounds[1] - 15000, bounds[3] + 23840)
    #basemap
    cx.add_basemap(ax, crs=ccrs.epsg(27700), source=cx.providers.CartoDB.Positron)
    #colourbar
    sm = ScalarMappable(norm=norm, cmap=cmap)
    cbar = plt.colorbar(sm, ax=ax, shrink = 0.9)
    cbar.set_label('CkDiffRoad')

    #export
    plt.savefig("outputs/road/CkDiffRoad_flowmap.png", transparent=True)  

def plot_SavedSecsRoad_flowmap(merged_df):
    #group by net_i and retrieve top destination
    neti_groups = merged_df.groupby(' net_i')
    top_1_list = []
    for neti, group_data in neti_groups:
        top_1 = group_data.nlargest(1, 'SavedSecsRoad') 
        top_1_list.append(top_1)
    top_1_df = pd.concat(top_1_list)
    top_1_df = top_1_df.sort_values('SavedSecsRoad')

    #calculate centroids
    top_1_df['centroid_i'] = top_1_df['zonei_geom'].apply(lambda geom: geom.centroid)
    top_1_df['centroid_j'] = top_1_df['zonej_geom'].apply(lambda geom: geom.centroid)

    #set up colourmap
    cmap = plt.get_cmap("Spectral").reversed() 
    tmax = top_1_df['SavedSecsRoad'].max()
    tmin = top_1_df['SavedSecsRoad'].min()
    norm = Normalize(tmin, tmax)

    #plot arrows
    fig, ax = plt.subplots(figsize=(9.0, 15.5))

    for index, row in top_1_df.iterrows():
        #calculate arrow properties
        arrow_color = cmap(norm(row['SavedSecsRoad']))
        arrow_start = (row['centroid_i'].x, row['centroid_i'].y)
        arrow_end = (row['centroid_j'].x, row['centroid_j'].y)
        arrow_dx = arrow_end[0] - arrow_start[0]
        arrow_dy = arrow_end[1] - arrow_start[1]
        #plot arrow
        ax.annotate("", xy=arrow_end, xytext=arrow_start, arrowprops=dict(arrowstyle="->", color=arrow_color, lw=0.25))
    
    #set up plot 
    #bounding box of the geometry column 
    merged_df = merged_df.set_geometry('zonei_geom')
    bounds = merged_df.geometry.total_bounds  
    #set plot limits
    ax.set_xlim(bounds[0] - 20000, bounds[2] + 20000)
    ax.set_ylim(bounds[1] - 15000, bounds[3] + 23840)
    #basemap
    cx.add_basemap(ax, crs=ccrs.epsg(27700), source=cx.providers.CartoDB.Positron)
    #colourbar
    sm = ScalarMappable(norm=norm, cmap=cmap)
    cbar = plt.colorbar(sm, ax=ax, shrink = 0.9)
    cbar.set_label('savedSecsRoad')

    #export
    plt.savefig("outputs/road/savedSecsRoad_flowmap.png", transparent=True)  

"""
Local Flow Maps
zoomed in flow maps generated by setting up a bounding box for a specific city/ town 
*examples below: London, Birmingham, Manchester, Glasgow, Liverpool and Newcastle
*produce maps that have colourbar normalised to the data in the filtered area
"""
#Local flow maps
def plot_CkDiffRoad_localflowmap(merged_df, regions):
    #group by net_i and retrieve top destination
    neti_groups = merged_df.groupby(' net_i')
    top_1_list = []
    for neti, group_data in neti_groups:
        top_1 = group_data.nlargest(1, 'CkDiffRoad') 
        top_1_list.append(top_1)
    top_1_df = gpd.GeoDataFrame(pd.concat(top_1_list), geometry='zonei_geom')

    #calculate centroids
    top_1_df['centroid_i'] = top_1_df['zonei_geom'].apply(lambda geom: geom.centroid)
    top_1_df['centroid_j'] = top_1_df['zonej_geom'].apply(lambda geom: geom.centroid)

    #iterate over each bounding box region
    for bbox, region_name in regions:
        #filter dataframe for the current bounding box region
        region_df = top_1_df.cx[bbox[0]:bbox[2], bbox[1]:bbox[3]]

        #set up colourmap
        cmap = plt.get_cmap("Spectral").reversed() 
        tmax = region_df['CkDiffRoad'].max()
        tmin = region_df['CkDiffRoad'].min()
        norm = Normalize(tmin, tmax)
    
        #plot arrows
        fig, ax = plt.subplots(figsize=(7.5, 5))

        for index, row in region_df.iterrows():
            #calculate arrow properties
            arrow_color = cmap(norm(row['CkDiffRoad']))
            arrow_start = (row['centroid_i'].x, row['centroid_i'].y)
            arrow_end = (row['centroid_j'].x, row['centroid_j'].y)
            arrow_dx = arrow_end[0] - arrow_start[0]
            arrow_dy = arrow_end[1] - arrow_start[1]
            #plot arrow
            ax.annotate("", xy=arrow_end, xytext=arrow_start, arrowprops=dict(arrowstyle="->", color=arrow_color, lw=0.5))
    
        #set up plot  
        #set plot limits
        ax.set_xlim(bbox[0] - 10000, bbox[2] + 10000)  
        ax.set_ylim(bbox[1] - 10000, bbox[3] + 10000) 
        #basemap
        cx.add_basemap(ax, crs=ccrs.epsg(27700), source=cx.providers.CartoDB.Positron)
        #colourbar
        sm = ScalarMappable(norm=norm, cmap=cmap)
        cbar = plt.colorbar(sm, ax=ax)
        cbar.set_label('CkDiffRoad')
        ax.set_title(f'{region_name}')

        #export
        plt.savefig(f"outputs/road/CkDiffRoad_flowmap_{region_name}.png", transparent=True)  

def plot_SavedSecsRoad_localflowmap(merged_df, regions):
    #group by net_i and retrieve top destination
    neti_groups = merged_df.groupby(' net_i')
    top_1_list = []
    for neti, group_data in neti_groups:
        top_1 = group_data.nlargest(1, 'SavedSecsRoad') 
        top_1_list.append(top_1)
    top_1_df = gpd.GeoDataFrame(pd.concat(top_1_list), geometry='zonei_geom')

    #calculate centroids
    top_1_df['centroid_i'] = top_1_df['zonei_geom'].apply(lambda geom: geom.centroid)
    top_1_df['centroid_j'] = top_1_df['zonej_geom'].apply(lambda geom: geom.centroid)

    #iterate over each bounding box region
    for bbox, region_name in regions:
        #filter dataframe for the current bounding box region
        region_df = top_1_df.cx[bbox[0]:bbox[2], bbox[1]:bbox[3]]

        #set up colourmap
        cmap = plt.get_cmap("Spectral").reversed() 
        tmax = region_df['SavedSecsRoad'].max()
        tmin = region_df['SavedSecsRoad'].min()
        norm = Normalize(tmin, tmax)
    
        #plot arrows
        fig, ax = plt.subplots(figsize=(7.5, 5))

        for index, row in region_df.iterrows():
            #calculate arrow properties
            arrow_color = cmap(norm(row['SavedSecsRoad']))
            arrow_start = (row['centroid_i'].x, row['centroid_i'].y)
            arrow_end = (row['centroid_j'].x, row['centroid_j'].y)
            arrow_dx = arrow_end[0] - arrow_start[0]
            arrow_dy = arrow_end[1] - arrow_start[1]
            #plot arrow
            ax.annotate("", xy=arrow_end, xytext=arrow_start, arrowprops=dict(arrowstyle="->", color=arrow_color, lw=0.5))
    
        #set up plot 
        #set plot limits
        ax.set_xlim(bbox[0] - 10000, bbox[2] + 10000)  
        ax.set_ylim(bbox[1] - 10000, bbox[3] + 10000) 
        #basemap
        cx.add_basemap(ax, crs=ccrs.epsg(27700), source=cx.providers.CartoDB.Positron)
        #colourbar
        sm = ScalarMappable(norm=norm, cmap=cmap)
        cbar = plt.colorbar(sm, ax=ax)
        cbar.set_label('savedSecsRoad')
        ax.set_title(f'{region_name}')

        #export
        plt.savefig(f"outputs/road/savedSecsRoad_flowmap_{region_name}.png", transparent=True)  

################################################################################

"""
main
"""
#read impact statistics
dfs = []
for root, dirs, files in os.walk('inputs/model-runs/dafni_impacts_road'):
    for file in files:
        #check if it is csv file and append to the list 
        if file.endswith('.csv'):
            df = pd.read_csv(os.path.join(root, file))
            dfs.append(df)
impacts_df = pd.concat(dfs, ignore_index=True)

#read zone codes and msoa shapefile 
ews_zones = pd.read_csv('inputs/model-runs/EWS_ZoneCodes.csv')
msoa = gpd.read_file('inputs/model-runs/EnglandWalesScotland_IZ_MSOA_2011.shp')
boundary = gpd.read_file('inputs/model-runs/TCITY_2015_EW_BGG_V2.shp')
boundary_scot = gpd.read_file('inputs/model-runs/Localities2020_MHW.shp')

#join tables
# - merge ews code and msoa shapefile - 
merged_ews = ews_zones.merge(msoa, left_on='areakey', right_on='msoa_iz')
# - for destination j - 
ews_j = merged_ews.rename(columns={"zonei": " net_j", "geometry": "zonej_geom"})
merged_df = impacts_df.merge(ews_j[[' net_j', 'zonej_geom']], on = ' net_j', how = 'left')
# - for orign i - 
ews_i = merged_ews.rename(columns={"zonei": " net_i", "geometry": "zonei_geom"})
merged_df = merged_df.merge(ews_i[[' net_i', 'zonei_geom']], on = ' net_i', how = 'left')
# - retrieve unique zone numbers -
neti = impacts_df[' net_i'].unique()

#bounding box for cities/ towns (local flow maps)
London_bbox = boundary[boundary['TCITY15NM'] == 'London'].total_bounds
Birmingham_bbox = boundary[boundary['TCITY15NM'] == 'Birmingham'].total_bounds
Glasgow_bbox = boundary_scot[boundary_scot['name'] == 'Glasgow'].total_bounds
Manchester_bbox = boundary[boundary['TCITY15NM'] == 'Manchester'].total_bounds
Liverpool_bbox = boundary[boundary['TCITY15NM'] == 'Liverpool'].total_bounds
Newcastle_bbox = boundary[boundary['TCITY15NM'] == 'Newcastle upon Tyne'].total_bounds
regions = [
        (London_bbox, 'London'),
        (Birmingham_bbox, 'Birmingham'),
        (Glasgow_bbox, 'Glasgow'),
        (Manchester_bbox, 'Manchester'),
        (Liverpool_bbox, 'Liverpool'),
        (Newcastle_bbox, 'Newcastle upon Tyne')
    ] 

#plot
#choropleth maps
plot_CkDiffRoad_quantiles(impacts_df, neti)
plot_SavedSecsRoad_quantiles(impacts_df, neti)
plot_CkDiffRoad_fisherjenks(impacts_df, neti)
plot_SavedSecsRoad_fisherjenks(impacts_df, neti)
#flow maps
plot_CkDiffRoad_flowmap(merged_df)
plot_SavedSecsRoad_flowmap(merged_df)
#local flow maps
plot_CkDiffRoad_localflowmap(merged_df, regions)
plot_SavedSecsRoad_localflowmap(merged_df, regions)


################################################################################