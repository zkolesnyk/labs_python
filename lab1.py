# -*- coding: utf-8 -*-
from datetime import datetime, date, time
from urllib2 import urlopen
from pandas import read_csv
from pandas import DataFrame
from os.path import join as pjoin
from glob import glob
import logging
import os

URL = 'http://www.star.nesdis.noaa.gov/smcd/emb/vci/gvix/G04/ts_L1/ByProvince/Mean/L1_Mean_UKR.R%02d.txt'
PATH = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(level=logging.INFO)

def createFrame():
    list = glob('*.csv')
    list.sort()
    for filename in list:
        data = read_csv(filename, index_col=False, header=1)
        print filename
    # c = data.rename(columns = {
    #     'year':'Рік',
    #     'week':'Тиждень'
    # })

for i in xrange(1, 3):
    url = URL%i
    if i in [12, 20]:
        continue
    logging.info('Downloading: %s'%url)
    vhi_url = urlopen(url)
    filename = 'vhi_id_%02d_%s.csv'%(i, datetime.now().strftime("%d.%m.%Y_%I:%M"))
    with open(pjoin(PATH, filename), 'ws') as out:
        out.write(vhi_url.read())
    logging.info('File %s was created'%filename)

createFrame()

print '==='
logging.info('All regions are downloaded')
