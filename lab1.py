# -*- coding: utf-8 -*-
from datetime import datetime, date, time
from urllib2 import urlopen
from pandas import read_csv
from os.path import join as pjoin
from glob import glob
import logging
import os

URL = 'http://www.star.nesdis.noaa.gov/smcd/emb/vci/gvix/G04/ts_L1/ByProvince/Mean/L1_Mean_UKR.R%02d.txt'
PATH = os.path.dirname(os.path.abspath(__file__))

new_data_path = pjoin(PATH, 'new_data')

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
"Kiev"              : 9,
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
    pass

def vhi_extreme(path):
    pass

def vhi_moderate(path, percent):
    regex = pjoin(new_data_path, 'vhi_id_%s*'%new_regions[regions[path-1]])
    df = create_frame(glob(regex)[0])
    df = df.loc[df['AreaLess35'] > percent]['Year']
    print df
    df = set(df)
    years = list(df)[1:]
    print 'Роки з помірними посухами, які торкнулися більше %s відсотків площі (%s область):' % (str(percent), new_regions[regions[path-1]])
    for path, year in enumerate(years):
        print '%s. %s'%(str(path+1), str(year))

def rename(index):
    return 'vhi_id_%02d_%s.csv'%(new_regions[regions[index-1]], datetime.now().strftime("%d.%m.%Y_%I:%M"))

def download_files():
    os.mkdir(new_data_path)
    for index in xrange(1, 28):
        url = URL%index
        if index in [12, 20]:
            continue
        logging.info('Downloading: %s'%url)
        vhi_url = urlopen(url)
        with open(pjoin(new_data_path, rename(index)), 'ws') as out:
            out.write(vhi_url.read())
        logging.info('File %s was created'%rename(index))


print '==='
logging.info('All regions are downloaded')
