# -*- coding: utf-8 -*-
import numpy as np
import netCDF4 as nc
import scipy.ndimage as img
import matplotlib.patches as pa
import scipy.interpolate as si
import pylab as plt
import copy
import scipy as sc

from utils import getAlt, centroid, centroidmax, centroidmin

PLOT=not False

# параметры расчета
PATH = r'../ecmwf-getmeteo/ex2008.nc'
LON0 = 131.9
LAT0 = 43.1
eps=0.75/2
threshold = 50
itime = 10



# Читаем базу данных
F = nc.Dataset(PATH)

varTime = F.variables['time']
N = len(varTime)

Time = nc.num2date(varTime, varTime.units)

lat = F.variables['latitude'][::-1]
lon = F.variables['longitude'][...]
level = F.variables['level'][...]

# Ищем индексы координат Владивостока
ilon, = np.where(np.abs(lon-LON0)<eps)[0]
ilat, = np.where(np.abs(lat-LAT0)<eps)[0]


# Разрез скорости ветра
uwnd = F.variables['u'][...]
centers = []

for itime in range(N):


    # вдоль долготы ilon
    uwnd0=uwnd[itime,:,:,ilon]

    alt0 = getAlt(level, 1013.25)


    fuwnd = si.interp2d(lat, alt0, uwnd0, kind='linear', bounds_error=False, fill_value=0)


    # Новая сетка высот
    nAlt = np.linspace(0,25000,200)
    nlat = np.linspace(30,60,60)

    # Интерполяция данных скорости ветра на новую сетку
    uwnd0 = fuwnd(nlat, nAlt)

    threshold = uwnd0.max()*0.90

    # применяем пороговый фильтр
    uwnd0_thres = copy.deepcopy(uwnd0)
    uwnd0_thres = uwnd0_thres - threshold
    uwnd0_thres[uwnd0_thres<0] = 0

    # выделяем найденные области
    labeled_image, number_of_objects = img.label(uwnd0_thres)
    peak_slices = img.find_objects(labeled_image)




    centeroids=[]
    # поиск центров масс
    for peak_slice in peak_slices:
        dy,dx  = peak_slice

        alat = nlat[dx]
        alev = nAlt[dy]


        cx,cy = centroid(alat, alev, uwnd0[peak_slice])
        centeroids.append((Time[itime], cx, cy))
    centers=centers+list(centeroids)
#    print centroids


    if PLOT:
        # Рисуем графики
        plt.figure()
        ax1 = plt.subplot(221)
        ax2 = plt.subplot(222)
        ax4 = plt.subplot2grid([2,2],(1,0),colspan=2)
        #ax4 = plt.subplot(223, colspan=2)

        ax1.imshow(uwnd0, extent=(nlat.min(),nlat.max(), nAlt.min(),nAlt.max()), aspect='auto',
                   origin='lower')

        ax2.imshow(uwnd0_thres, extent=(nlat.min(),nlat.max(), nAlt.min(),nAlt.max()), aspect='auto',
                   origin='lower')

        #ax3.hist(uwnd0.flat, bins=15, normed=True, cumulative=True, histtype='step')
        #ax3.hist(uwnd0_thres.flat, bins=15, normed=True, cumulative=True, histtype='step')


        ax4.imshow(uwnd0_thres, extent=(nlat.min(),nlat.max(), nAlt.min(),nAlt.max()), aspect='auto',
                   origin='lower')
        ax4.grid(which='both', c='w',ls='-.', lw=1)

        for centr in centeroids:
            ax4.plot(centr[1],centr[2],'kx', mew=7)

        figname = "figure%03d.pdf"%(itime)
        plt.savefig(figname)
        for ax in (ax1,ax2, ax4):
            ax.clear()
        plt.close()
# Закрываем базу данных
F.close()

for item in centers:
    print item[0].strftime('%Y-%m-%d'), item[1], item[2]


