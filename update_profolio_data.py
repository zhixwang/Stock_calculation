# -*- coding: utf-8 -*-
"""
Created on Sat Sep 15 14:14:18 2018

@author: zxwan
"""

from investing_profilio import auto_update_profolio as acb
import argparse
import pandas as pd
import re
import json
import urllib.request

ap = argparse.ArgumentParser(description='Update values')
ap.add_argument("-chk", "--currency_hk", required=False,type = float,
	help="Currency")
ap.add_argument("-cus", "--currency_us", required=False,type = float,
	help="Currency")
ap.add_argument("-w", "--write",required = False, type = str, help = "Write to file")
args = vars(ap.parse_args())

curr_file = u"Currency.xlsx"
currency_pd = pd.read_excel(curr_file,dtype = str)
curr_hk = currency_pd['price'][0]
curr_us = currency_pd['price'][1]

write_file = True
if args['write']:
    try:
        bool_write = json.loads(args['write'].lower())    
    except:
        pass
    else:
        if bool_write == False:
            write_file = False
            # print("Output to files cancelled!")
    
if args['currency_hk'] or args['currency_us'] :
    #Update currency ratio manually
    if args['currency_hk']:
        curr_hk = args['currency_hk']
    if args['currency_us'] :
        curr_us = args['currency_us']	
    HKDCNY = float(curr_hk)
    USDCNY = float(curr_us)    
    
else:
    # No manual input, by default get currency from Hexun
    usdurl = "http://webforex.hermes.hexun.com/forex/quotelist?code=FOREXUSDCNY&column=Code,Price"
    hkdurl = "http://webforex.hermes.hexun.com/forex/quotelist?code=FOREXHKDCNY&column=Code,Price"
    urdreq = urllib.request.Request(usdurl)
    hkdreq = urllib.request.Request(hkdurl)
    f = urllib.request.urlopen(urdreq)
    html = f.read().decode("utf-8")
    s = re.findall("{.*}",str(html))[0]
    sjson = json.loads(s)    
    USDCNY = sjson["Data"][0][0][1]/10000
    print("USD to CNY: %.4f " % USDCNY)
    
    f = urllib.request.urlopen(hkdreq)
    html = f.read().decode("utf-8")
    s = re.findall("{.*}",str(html))[0]
    sjson = json.loads(s)    
    HKDCNY = sjson["Data"][0][0][1]/10000
    print("HKD to CNY: %.4f " % HKDCNY)
    curr_hk = str(HKDCNY)
    curr_us = str(USDCNY)
    
currency_pd['price'][0] = curr_hk
currency_pd['price'][1] = curr_us    
curr_file = u"Currency.xlsx"

currency_pd.to_excel(curr_file, index=False)
print(u'Currency updated')
    
curr = (HKDCNY, USDCNY)
cb2 = acb(curr,write_file)
cb2.save()
"""
#cb1.show()
cb1.save()

cb2 = cb('test')
cb2.read('2018Q2.csv')
cb2.show()
"""


