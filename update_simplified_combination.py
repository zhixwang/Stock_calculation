# -*- coding: utf-8 -*-
"""
Created on Sat Sep 15 14:14:18 2018

@author: zxwan
"""

from invest_combination_simplified import auto_combination as acb
import argparse
import pandas as pd

ap = argparse.ArgumentParser(description='Update values')
ap.add_argument("-chk", "--currency_hk", required=False,type = float,
	help="Currency")
ap.add_argument("-cus", "--currency_us", required=False,type = float,
	help="Currency")
args = vars(ap.parse_args())

curr_file = u"Currency.xlsx"
currency_pd = pd.read_excel(curr_file,dtype = str)
curr_hk = currency_pd['price'][0]
curr_us = currency_pd['price'][1]

if args['currency_hk'] or args['currency_us'] :
    if args['currency_hk']:
        curr_hk = args['currency_hk']
    if args['currency_us'] :
        curr_us = args['currency_us']
	#Update currency ratio
    curr_file = u"Currency.xlsx"
    #dic_curr = {'type':'out', 'price':curr_hk}
    #df_curr = pd.DataFrame(dic_curr,index = [0])
    
    currency_pd['price'][0] = curr_hk
    currency_pd['price'][1] = curr_us

    currency_pd.to_excel(curr_file)
    print(u'Currency updated')

    
curr = (float(curr_hk), float(curr_us))
cb2 = acb(curr)
cb2.save()
"""
#cb1.show()
cb1.save()

cb2 = cb('test')
cb2.read('2018Q2.csv')
cb2.show()
"""


