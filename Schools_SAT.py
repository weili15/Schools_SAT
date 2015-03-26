""" Read in and analyze SAT school_data for California schools over the last 10 years
Plot on a map of California to visualize
Author : Wei
Date : Mar 18 2015

Need a legend title
"""


import pylab as py
import shapefile
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib as mpl
import matplotlib.cm as cm

def draw_area(llcrnrlon, llcrnrlat, urcrnrlon, urcrnrlat):
    """
    This functions draws and returns a map defined by coordinates
    """

    fig = plt.figure(figsize=(18,14))

    #Define our map: lat_0 and lon_0 are the central longitude and latitude
    #llcrnrlon and llcrnrlat are the long. and lat. of the lower left hand corner
    #urcrnrlon and urcrnrlat are the long. and lat. of the upper right hand corner

    m = Basemap(projection='cyl', llcrnrlon=llcrnrlon, llcrnrlat=llcrnrlat, urcrnrlon=urcrnrlon, urcrnrlat=urcrnrlat, resolution='h', )
    m.readshapefile("/Users/weili/Python_Work/Schools_SAT/cb_2013_us_zcta510_500k/cb_2013_us_zcta510_500k", 'zip_points')
    m.drawcoastlines()
    m.drawmapboundary()
    m.drawcountries()
    m.drawstates()
    m.drawcounties()
    m.fillcontinents(color = '#C0C0C0')

    return m,fig

#One time code to add ", CA" to School Names and export as csv
#school_data = pd.read_excel('sat13.xls', header=3)
#school_data['School Name']=school_data['School Name']+ ', CA'
#school_data.to_csv('sat13_RevisedSchoolName.csv')

def draw_zip_income(m,fig,zip_data):
    sf = shapefile.Reader("/Users/weili/Python_Work/Schools_SAT/cb_2013_us_zcta510_500k/cb_2013_us_zcta510_500k")  # or whatever filename
    shape_recs = sf.shapeRecords()

    ax = plt.gca()
    #Make colormap, with low of 10000 and max of 200000
    norm = mpl.colors.Normalize(vmin=10000, vmax=150000)
    cmap = cm.BrBG #Different colormap than the schools' red/blue colormap
    myColorMap = cm.ScalarMappable(norm=norm, cmap=cmap)

    for rec in shape_recs:
        points = rec.shape.points
        d = rec.record  # record MetaData
        zip_code = d[0]
        if (zip_data['Zip']==str(zip_code)).any(): #If this zip code exists in zip data
            this_income=zip_data['Median Total'][zip_data['Zip']==str(zip_code)].iloc[0]

            patch = patches.Polygon(points,True,label=d[0],color=myColorMap.to_rgba(this_income))
            ax.add_patch(patch)
    #Add Colormap
    ax2 = fig.add_axes([0.04, 0.1, 0.03, 0.8])
    mpl.colorbar.ColorbarBase(ax2,cmap=cmap, norm=norm, label='Income')
    return m,fig

#Draw map of California with school/SAT data
def draw_california(school_data, zip_data):
    llcrnrlon=-126
    llcrnrlat=32.0
    urcrnrlon=-114
    urcrnrlat=42.0

    #Make colormap, with low of 1000 and max of 2400
    norm = mpl.colors.Normalize(vmin=800, vmax=2000)
    cmap = cm.bwr
    myColorMap = cm.ScalarMappable(norm=norm, cmap=cmap)

    m,fig=draw_area(llcrnrlon=llcrnrlon, llcrnrlat=llcrnrlat, urcrnrlon=urcrnrlon, urcrnrlat=urcrnrlat)

    for school in school_data['School Name'].tolist():
        this_SAT_score=school_data['Tot_Mean'][school_data['School Name']==school].iloc[0]
        this_lat=school_data['Latitude'][school_data['School Name']==school].iloc[0]
        this_long=school_data['Longitude'][school_data['School Name']==school].iloc[0]
        if ~np.isnan(this_SAT_score) & (urcrnrlat>this_lat>llcrnrlat) & (urcrnrlon>this_long>llcrnrlon):
            x,y = m(this_long, this_lat)
            m.plot(x, y, color=myColorMap.to_rgba(this_SAT_score), marker='o', markersize=5)

    plt.title('Average SAT scores for schools in California')
    draw_zip_income(m,fig,zip_data)
    ax2 = fig.add_axes([0.92, 0.1, 0.03, 0.8])
    mpl.colorbar.ColorbarBase(ax2,cmap=cmap, norm=norm, label='SAT score')
    plt.savefig('California_schools_SAT')
    print "California Map Finished"

#Draw map of LOS ANGELES with school/SAT data
def draw_LA(school_data, zip_data):
    llcrnrlon=-118.81
    llcrnrlat=33.229
    urcrnrlon=-116.977
    urcrnrlat=34.232

    #Make colormap, with low of 1000 and max of 2400
    norm = mpl.colors.Normalize(vmin=800, vmax=2000)
    cmap = cm.bwr
    myColorMap = cm.ScalarMappable(norm=norm, cmap=cmap)
    m,fig=draw_area(llcrnrlon=llcrnrlon, llcrnrlat=llcrnrlat, urcrnrlon=urcrnrlon, urcrnrlat=urcrnrlat)
    for school in school_data['School Name'].tolist():
        this_SAT_score=school_data['Tot_Mean'][school_data['School Name']==school].iloc[0]
        this_lat=school_data['Latitude'][school_data['School Name']==school].iloc[0]
        this_long=school_data['Longitude'][school_data['School Name']==school].iloc[0]
        if ~np.isnan(this_SAT_score) & (urcrnrlat>this_lat>llcrnrlat) & (urcrnrlon>this_long>llcrnrlon):
            x,y = m(this_long, this_lat)
            m.plot(x, y, color=myColorMap.to_rgba(this_SAT_score), marker='o', markersize=5)

    plt.title('Average SAT scores for schools in Los Angeles')

    #Add in some LA Landmarks
    lons = [-118.48829, -118.402463, -118.34074, -117.809747, -118.354944, -118.129724, -117.923862]
    lats = [34.017511, 34.073268, 33.836488, 33.682204, 33.960013, 34.147748, 33.868876]
    x,y=m(lons,lats)

    labels = ['Santa Monica', 'Beverly Hills', 'Torrance', 'Irvine', 'Inglewood', 'Pasadena','Fullerton']
    for label, xpt, ypt in zip(labels, x, y):
        plt.text(xpt, ypt, label, color='white')

    draw_zip_income(m,fig,zip_data)
    #COLORBAR
    ax2 = fig.add_axes([0.92, 0.1, 0.03, 0.8])
    mpl.colorbar.ColorbarBase(ax2,cmap=cmap, norm=norm, label='SAT score')

    plt.savefig('LA_schools_SAT')
    print "LA Map Finished"


#Draw map of SAN FRANCISCO with school/SAT data
def draw_SF(school_data, zip_data):
    llcrnrlon=-122.744151
    llcrnrlat=37.263361
    urcrnrlon=-121.722422
    urcrnrlat=38.021284

    #Make colormap, with low of 1000 and max of 2400
    norm = mpl.colors.Normalize(vmin=800, vmax=2000)
    cmap = cm.bwr
    myColorMap = cm.ScalarMappable(norm=norm, cmap=cmap)
    m,fig=draw_area(llcrnrlon=llcrnrlon, llcrnrlat=llcrnrlat, urcrnrlon=urcrnrlon, urcrnrlat=urcrnrlat)
    for school in school_data['School Name'].tolist():
        this_SAT_score=school_data['Tot_Mean'][school_data['School Name']==school].iloc[0]
        this_lat=school_data['Latitude'][school_data['School Name']==school].iloc[0]
        this_long=school_data['Longitude'][school_data['School Name']==school].iloc[0]
        if ~np.isnan(this_SAT_score) & (urcrnrlat>this_lat>llcrnrlat) & (urcrnrlon>this_long>llcrnrlon):
            x,y = m(this_long, this_lat)
            m.plot(x, y, color=myColorMap.to_rgba(this_SAT_score), marker='o', markersize=5)

    plt.title('Average SAT scores for schools in San Francisco')

    #Add in some LA Landmarks
    lons = [-122.264872, -122.413531, -122.146082, -121.896143, -122.034804, -122.069476]
    lats = [37.805679, 37.760637, 37.444027, 37.340375, 37.323312, 37.908546]
    x,y=m(lons,lats)

    labels = ['Oakland', 'Mission District', 'Palo Alto', 'San Jose','Cupertino', 'Walnut Creek']
    for label, xpt, ypt in zip(labels, x, y):
        plt.text(xpt, ypt, label, color='blue')

    draw_zip_income(m,fig,zip_data)
    #COLORBAR
    ax2 = fig.add_axes([0.92, 0.1, 0.03, 0.8])
    mpl.colorbar.ColorbarBase(ax2,cmap=cmap, norm=norm, label='SAT score')

    plt.savefig('SF_schools_SAT')
    print "SF Map Finished"


#Plot test scores onto map, with RED as higher scores and BLUE as lower scores
school_data = pd.read_csv('sat13_RevisedSchoolName.csv') #Get school/SAT data
zip_data = pd.read_csv('income_zip_code.csv')
zip_data[zip_data=='2,500-']=2500
zip_data[zip_data=='200,000']=200000
draw_california(school_data,zip_data)
draw_LA(school_data,zip_data)
draw_SF(school_data,zip_data)
plt.show()