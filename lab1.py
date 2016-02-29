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

data_path = pjoin(PATH, 'data')
os.mkdir(data_path)

logging.basicConfig(level=logging.INFO)

def create_frame(path):
    list = glob(pjoin(path, '*.csv'))
    list.sort()
    for filename in list:
        data = read_csv(filename, index_col=False, header=1)
        print data.rename(columns = {
            'year':'Year',
            'week':'Week',
            'VCI':'VegetationConditionIndex',
            'TCI':'ThermalConditionIndex',
            'VHI':'VegetationHealthIndex',
            '%Area_VHI_LESS_15':'AreaLess15',
            '%Area_VHI_LESS_35':'AreaLess35'
        })

for index in xrange(1, 3):
    url = URL%index
    if index in [12, 20]:
        continue
    logging.info('Downloading: %s'%url)
    vhi_url = urlopen(url)
    filename = 'vhi_id_%02d_%s.csv'%(index, datetime.now().strftime("%d.%m.%Y_%I:%M"))
    with open(pjoin(data_path, filename), 'ws') as out:
        out.write(vhi_url.read())
    logging.info('File %s was created'%filename)

create_frame(data_path)

print '==='
logging.info('All regions are downloaded')
