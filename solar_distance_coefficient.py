# -*- coding: utf-8 -*-
"""
@author: Manchun LEI

Calculate the solar-earth distance coefficient R
from date or from day-of-year (doy)

F0 of a specifical date/doy = F0_sc * R

R0_sc is the extraterrestrial solar irradiance at R=1

Usually month=4,day=4 (doy=94) is the closest date/doy for R=1

"""
import numpy as np
import datetime

def julian_day(year,month,day):
    if month <= 2:
        year -= 1
        month += 12
    A = np.floor(year / 100)
    B = 2 - A + np.floor(A / 4)
    JD = np.floor(365.25 * (year + 4716)) + np.floor(30.6001 * (month + 1)) + day + B - 1524.5
    return JD

def solar_distance_coefficient_date(year,month,day):
    JD = julian_day(year, month, day)
    g = 357.529 + 0.98560028 * (JD - 2451545)
    g = np.deg2rad(g)  
    d = 1.00014 - 0.01671 * np.cos(g) - 0.00014 * np.cos(2 * g)
    R = 1 / (d ** 2)
    return R

def solar_distance_coefficient_doy(doy):
    g = 357.529 + 0.98560028 * (doy - 1)
    g = np.deg2rad(g)  
    d = 1.00014 - 0.01671 * np.cos(g) - 0.00014 * np.cos(2 * g)
    R = 1 / (d ** 2)
    return R

def date_to_doy(year,month,day):
    return datetime.datetime(year,month,day).timetuple().tm_yday

def doy_to_date(year,doy):
    start_date = datetime.datetime(year,1,1)
    doy = int(doy)
    date = start_date + datetime.timedelta(days=doy - 1)
    return date