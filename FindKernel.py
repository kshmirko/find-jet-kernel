# -*- coding: utf-8 -*-
import numpy as np
import netCDF4 as nc
import scipy.ndimage as img
import matplotlib.patches as pa
import scipy.interpolate as si
import pylab as plt
import copy

from utils import getAlt, centroid

# параметры расчета
PATH = r'../ecmwf-getmeteo/ex2008.nc'
LON0 = 131.9
LAT0 = 43.1
eps=0.75/2
threshold = 15
itime = 10



# Читаем базу данных
F = nc.Dataset(PATH)

varTime = F.variables['time']
Time = nc.num2date(varTime, varTime.units)

lat = F.variables['latitude'][::-1]
lon = F.variables['longitude'][...]
level = F.variables['level'][...]

# Ищем индексы координат Владивостока
ilon, = np.where(np.abs(lon-LON0)<eps)[0]
ilat, = np.where(np.abs(lat-LAT0)<eps)[0]


# Разрез скорости ветра
uwnd = F.variables['u'][...]

# вдоль долготы ilon
uwnd0=uwnd[itime,:,:,ilon]

print level, level[-1]


alt0 = getAlt(level, 1013.25)


fuwnd = si.interp2d(lat, alt0, uwnd0, kind='linear', bounds_error=False, fill_value=0)


# Новая сетка высот
Alt = np.linspace(0,25000,200)
lat = np.linspace(30,60,60)

# Интерполяция данных скорости ветра на новую сетку
uwnd0 = fuwnd(lat, Alt)


# применяем пороговый фильтр
uwnd0_thres = copy.deepcopy(uwnd0)
uwnd0_thres[uwnd0_thres<threshold] = 0

# выделяем найденные области
labeled_image, number_of_objects = img.label(uwnd0_thres)
peak_slices = img.find_objects(labeled_image)


# поиск центров масс
centroids = []

for peak_slice in peak_slices:
    dy,dx  = peak_slice

    alat = lat[dx]
    alev = Alt[dy]


    cx,cy = centroid(alat, alev, uwnd0[peak_slice])
    centroids.append((cx, cy))

print centroids

plt.figure()
ax1 = plt.subplot(221)
ax2 = plt.subplot(222)
ax3 = plt.subplot(223)
ax4 = plt.subplot(224)

ax1.imshow(uwnd0, extent=(lat.min(),lat.max(), Alt.min(),Alt.max()), aspect='auto',
           origin='lower')

ax2.imshow(uwnd0_thres, extent=(lat.min(),lat.max(), Alt.min(),Alt.max()), aspect='auto',
           origin='lower')

ax3.hist(uwnd0.flat)


#for peak_slice in peak_slices:  #Draw some rectangles around the objects
#    dy,dx  = peak_slice
#    alat = lat[dx]
#    alev = Alt[dy]
#    xy     = (lat[dx.start], Alt[dy.start])
#    width  = (lat[dx.stop] - lat[dx.start])
#    height = (Alt[dy.stop] - Alt[dy.start])
#    rect = pa.Rectangle(xy,width,height,fc='none',ec='red')
#    ax3.add_patch(rect,)

ax4.imshow(uwnd0_thres, extent=(lat.min(),lat.max(), Alt.min(),Alt.max()), aspect='auto',
           origin='lower')

for centr in centroids:
    ax4.plot(centr[0],centr[1],'kx')

#ax4.imshow(uwnd0_thres, extent=(lat.min(),lat.max(), Alt.min(),Alt.max()), aspect='auto',
#           origin='lower')

plt.show()
# Закрываем базу данных
F.close()






#
#uwnd[uwnd<threshold]=0
#uwnd0=uwnd[0,:,:,ilon]

#def centroid(alat, alev, data):
#    h,w = np.shape(data)
#    x = alat
#    y = alev
#
#    X,Y = np.meshgrid(x-x[0],y-y[0])
#
#    cx = np.sum(X*data)/np.sum(data)
#    cy = np.sum(Y*data)/np.sum(data)
#
#    return cx+x[0],cy+y[0]

#def centroid(data):
#    h,w = np.shape(data)
#    x = np.arange(0,w)
#    y = np.arange(0,h)
#
#    X,Y = np.meshgrid(x,y)
#
#    cx = np.sum(X*data)/np.sum(data)
#    cy = np.sum(Y*data)/np.sum(data)
#
#    return cx,cy
#
#def getAlt(P,P0):
#    return 1/7988.28*np.log(P0/P)



#
#
#print F.variables['pv'].shape
#
#
#
#
#
#
#
#
#
#
#
#labeled_image, number_of_objects = img.label(uwnd0)
#peak_slices = img.find_objects(labeled_image)
#
#
#
#centroids = []
#import pylab as plt
#for peak_slice in peak_slices:
#    dy,dx  = peak_slice
#
#    x,y = dx.start, dy.start
#
#    cx,cy = centroid(uwnd0[peak_slice])
#    centroids.append((cx+x,cy+y))
#
#
#print centroids
#
#
#
#print labeled_image, number_of_objects
#
#plt.figure()
#plt.imshow(labeled_image)
#for c in centroids:
#    plt.plot(c[0],c[1],'kx')
#
#
#
#plt.figure(dpi=100)
#plt.imshow(uwnd[0,:,:,ilon], vmin=0, vmax=50,
#           extent=(lat.min(),lat.max(), level.max(), level.min()),
#           interpolation='bilinear',
#           norm=None,
#           aspect='auto')
#
#plt.colorbar()
#plt.contour(uwnd[0,:,:,ilon],10, vmin=0, vmax=50,
#           extent=(lat.min(),lat.max(), level.min(),level.max()),
#           interpolation='gaussian',
#           norm=None,
#           aspect='auto',
#           colors='k')
#
#
#
#plt.figure()
#plt.hist(uwnd[0,:,:,ilon].flat)
#
#plt.show()
#F.close()
