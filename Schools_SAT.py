""" Read in and analyze SAT data for California schools over the last 10 years
Plot on a map of California to visualize
Author : Wei
Date : Mar 18 2015

Need a legend title
"""


import pylab as py
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib as mpl
import matplotlib.cm as cm



def draw_area(llcrnrlon, llcrnrlat, urcrnrlon, urcrnrlat):
    """
    This functions draws and returns a map of California
    """

    fig = plt.figure(figsize=(18,14))

    #Define our map: lat_0 and lon_0 are the central longitude and latitude
    #llcrnrlon and llcrnrlat are the long. and lat. of the lower left hand corner
    #urcrnrlon and urcrnrlat are the long. and lat. of the upper right hand corner

    m = Basemap(projection='cyl', llcrnrlon=llcrnrlon, llcrnrlat=llcrnrlat, urcrnrlon=urcrnrlon, urcrnrlat=urcrnrlat, resolution='h', )
    m.readshapefile("/Users/weili/Python_Work/Schools_SAT/USA_adm/USA_adm0", 'USA_adm')
    m.drawcoastlines()
    m.drawmapboundary()
    m.drawcountries()
    m.drawstates()
    m.drawcounties()
    m.fillcontinents(color = '#C0C0C0')

    return m,fig

#One time code to add ", CA" to School Names and export as csv
#data = pd.read_excel('sat13.xls', header=3)
#data['School Name']=data['School Name']+ ', CA'
#data.to_csv('sat13_RevisedSchoolName.csv')

#Plot test scores onto map, with RED as higher scores and BLUE as lower scores
data = pd.read_csv('sat13_RevisedSchoolName.csv')

#Test maps starting here
#Make colormap, with low of 1000 and max of 2400
norm = mpl.colors.Normalize(vmin=800, vmax=2000)
cmap = cm.bwr

myColorMap = cm.ScalarMappable(norm=norm, cmap=cmap)

# #Draw map of California
# llcrnrlon=-126
# llcrnrlat=32.0
# urcrnrlon=-114
# urcrnrlat=42.0
# m,fig=draw_area(llcrnrlon=llcrnrlon, llcrnrlat=llcrnrlat, urcrnrlon=urcrnrlon, urcrnrlat=urcrnrlat)
# for school in data['School Name'].tolist():
#     this_SAT_score=data['Tot_Mean'][data['School Name']==school].iloc[0]
#     this_lat=data['Latitude'][data['School Name']==school].iloc[0]
#     this_long=data['Longitude'][data['School Name']==school].iloc[0]
#     if ~np.isnan(this_SAT_score) & (urcrnrlat>this_lat>llcrnrlat) & (urcrnrlon>this_long>llcrnrlon):
#         x,y = m(this_long, this_lat)
#         m.plot(x, y, color=myColorMap.to_rgba(this_SAT_score), marker='o', markersize=5)
#
# plt.title('Average SAT scores for schools in California')
# ax2 = fig.add_axes([0.92, 0.1, 0.03, 0.8])
# mpl.colorbar.ColorbarBase(ax2,cmap=cmap, norm=norm, label='SAT score')
# plt.savefig('California_schools_SAT')
# plt.show()

#Draw map of LOS ANGELES
# llcrnrlon=-118.81
# llcrnrlat=33.229
# urcrnrlon=-116.977
# urcrnrlat=34.232
# m,fig=draw_area(llcrnrlon=llcrnrlon, llcrnrlat=llcrnrlat, urcrnrlon=urcrnrlon, urcrnrlat=urcrnrlat)
# for school in data['School Name'].tolist():
#     this_SAT_score=data['Tot_Mean'][data['School Name']==school].iloc[0]
#     this_lat=data['Latitude'][data['School Name']==school].iloc[0]
#     this_long=data['Longitude'][data['School Name']==school].iloc[0]
#     if ~np.isnan(this_SAT_score) & (urcrnrlat>this_lat>llcrnrlat) & (urcrnrlon>this_long>llcrnrlon):
#         x,y = m(this_long, this_lat)
#         m.plot(x, y, color=myColorMap.to_rgba(this_SAT_score), marker='o', markersize=5)
#
# plt.title('Average SAT scores for schools in Los Angeles')
#
# #Add in some LA Landmarks
# lons = [-118.48829, -118.402463, -118.34074, -117.809747, -118.354944, -118.129724, -117.923862]
# lats = [34.017511, 34.073268, 33.836488, 33.682204, 33.960013, 34.147748, 33.868876]
# x,y=m(lons,lats)
#
# labels = ['Santa Monica', 'Beverly Hills', 'Torrance', 'Irvine', 'Inglewood', 'Pasadena','Fullerton']
# for label, xpt, ypt in zip(labels, x, y):
#     plt.text(xpt, ypt, label)
#
# #COLORBAR
# ax2 = fig.add_axes([0.92, 0.1, 0.03, 0.8])
# mpl.colorbar.ColorbarBase(ax2,cmap=cmap, norm=norm, label='SAT score')
#
#
#
# plt.savefig('LA_schools_SAT')
# plt.show()


#Draw map of SAN FRANCISCO
llcrnrlon=-122.744151
llcrnrlat=37.263361
urcrnrlon=-121.722422
urcrnrlat=38.021284
m,fig=draw_area(llcrnrlon=llcrnrlon, llcrnrlat=llcrnrlat, urcrnrlon=urcrnrlon, urcrnrlat=urcrnrlat)
for school in data['School Name'].tolist():
    this_SAT_score=data['Tot_Mean'][data['School Name']==school].iloc[0]
    this_lat=data['Latitude'][data['School Name']==school].iloc[0]
    this_long=data['Longitude'][data['School Name']==school].iloc[0]
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
    plt.text(xpt, ypt, label)

#COLORBAR
ax2 = fig.add_axes([0.92, 0.1, 0.03, 0.8])
mpl.colorbar.ColorbarBase(ax2,cmap=cmap, norm=norm, label='SAT score')



plt.savefig('SF_schools_SAT')
plt.show()