# -*- coding: utf-8 -*-
from datetime import datetime, date, time
from urllib2 import urlopen
from pandas import read_csv
from pandas import DataFrame
import logging
import os

url = 'http://www.star.nesdis.noaa.gov/smcd/emb/vci/gvix/G04/ts_L1/ByProvince/Mean/L1_Mean_UKR.R%02d.txt'%i

logging.basicConfig(level=logging.INFO)

def createFolder(path):
    os.chdir(path)
    folder = 'data'
    os.mkdir(folder)
    return '%s%s'%(path, folder)

path = './'
folder = createFolder(path) + '/'
print folder

def createFrame():
    data = read_csv(filename, index_col=False, header=1)
    c = data.rename(columns = {
        'year':'Рік',
        'week':'Тиждень'
    })
    print c[:1]

for i in xrange(1, 3):
    if i in [12, 20]:
        continue
    logging.info('Downloading: %s'%url)
    vhi_url = urlopen(url)
    filename = 'vhi_id_%02d_%s.csv'%(i, datetime.now().strftime("%d.%m.%Y_%I:%M"))
    out = open(folder+filename, 'ws')
    out.write(vhi_url.read())
    out.close()
    logging.info('File %s was created'%filename)

print '==='
logging.info('All regions are downloaded')
