# -*- coding: utf-8 -*-
from datetime import datetime, date, time
from urllib2 import urlopen
from pandas import read_csv
from os.path import join as pjoin
from glob import glob
import logging
import os

DATE = datetime.now().strftime("%d.%m.%Y_%I.%M")
URL = 'http://www.star.nesdis.noaa.gov/smcd/emb/vci/gvix/G04/ts_L1/ByProvince/Mean/L1_Mean_UKR.R%02d.txt'
PATH = os.path.dirname(os.path.abspath(__file__))

data_path = pjoin(PATH, 'data')

logging.basicConfig(level=logging.INFO)

regions = [ "Cherkasy", "Chernihiv", "Chernivtsi", "Crimea", "Dnipropetrovs'k",
"Donets'k", "Ivano-Frankivs'k", "Kharkiv","Kherson", "Khmel'nyts'kyy", "Kiev",
"Kiev City", "Kirovohrad", "Luhans'k", "L'viv", "Mykolayiv", "Odessa", "Poltava",
"Rivne", "Sevastopol'", "Sumy", "Ternopil'", "Zakarpats'ka", "Vinnytsya", "Volyn",
"Zaporizhzhya", "Zhytomyr" ]

new_regions = {
"Vinnytsya"         : 1,
"Volyn"             : 2,
"Dnipropetrovs'k"   : 3,
"Donets'k"          : 4,
"Zhytomyr"          : 5,
"Zakarpats'ka"      : 6,
"Zaporizhzhya"      : 7,
"Ivano-Frankivs'k"  : 8,
"Kiev City"         : 9,
"Kirovohrad"        : 10,
"Luhans'k"          : 11,
"L'viv"             : 12,
"Mykolayiv"         : 13,
"Odessa"            : 14,
"Poltava"           : 15,
"Rivne"             : 16,
"Sumy"              : 17,
"Ternopil'"         : 18,
"Kharkiv"           : 19,
"Kherson"           : 20,
"Khmel'nyts'kyy"    : 21,
"Cherkasy"          : 22,
"Chernivtsi"        : 23,
"Chernihiv"         : 24,
"Crimea"            : 25
}

def create_frame(path):
    data = read_csv(path, index_col=False, header=1)
    data.rename(columns = {
        'year':'Year',
        'week':'Week',
        'VCI':'VegetationConditionIndex',
        'TCI':'ThermalConditionIndex',
        'VHI':'VegetationHealthIndex',
        '%Area_VHI_LESS_15':'AreaLess15',
        '%Area_VHI_LESS_35':'AreaLess35'
    }, inplace = True)
    return data

def vhi_min_max(path, year):
    filename = pjoin(data_path, 'vhi_id_%02d*'%new_regions[regions[path-1]])
    df = create_frame(glob(filename)[0])
    df = df[df['Year'] == year]['VegetationHealthIndex']
    print 'VegetationHealthIndex за %s рік'%year,
    print '(%s область):'%new_regions[regions[path-1]]
    for number, week in enumerate(df):
        print '%s. %s'%(number + 1, week)
    print 'Max VegetationHealthIndex = %s'%df.max()
    print 'Min VegetationHealthIndex = %s'%df.min()

def vhi_extreme_moderate(path, percent, rate):
    filename = pjoin(data_path, 'vhi_id_%02d*'%new_regions[regions[path-1]])
    df = create_frame(glob(filename)[0])
    years = list(set(df[df['AreaLess%s'%rate] > percent]['Year']))
    if rate == 15:
        print 'Роки з екстримальними посухами, які торкнулися більше %s'%percent,
    elif rate == 35:
        print 'Роки з помірними посухами, які торкнулися більше %s'%percent,
    print 'відсотків площі (%s область):'%new_regions[regions[path-1]]
    for index, year in enumerate(years):
        print '%s. %s'%(index + 1, year)

def rename(index):
    return 'vhi_id_%02d_%s.csv'%(new_regions[regions[index-1]], DATE)

def download_files():
    os.mkdir(data_path)
    for index in xrange(1, 28):
        url = URL%index
        if index in [11, 20]:
            continue
        logging.info('Downloading: %s'%url)
        vhi_url = urlopen(url)
        with open(pjoin(data_path, rename(index)), 'ws') as out:
            out.write(vhi_url.read())
        logging.info('File %s was created'%rename(index))
    print '==='
    logging.info('All regions are downloaded')

download_files()
vhi_min_max(1, 2000)
vhi_extreme_moderate(1, 10, 35)
