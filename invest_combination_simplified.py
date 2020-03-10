# -*- coding: utf-8 -*-
"""
Created on Sat Sep 15 13:29:00 2018

@author: zxwan
"""
import numpy as np
#import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from datetime import date
from datetime import timedelta
from pytz import timezone 
import tushare as ts 
import pandas_datareader.data as web  

class auto_combination:
    nums = np.array([])                 #number of each stock that you holds
    codes = []
    names = []
    prices = np.array([])
    values = np.array([])
    #pes = np.array([])
    #pbs = np.array([])
    #profits = np.array([])
    currency_hk = 0.89
    currency_us = 7.0176
    #profitable_values = np.array([])
    #epses = np.array([])
    #is_stock = []   # if is a stock or not
    date = ""
    combn_data = None #combination information
    #info_all = None
    #nassets = np.array([])
    #asset = 0.0
    #pe = 0.0
    #pb = 0.0
    #roe = 0.0
    #total_profit = 0.0
    value = 0.0
    ratios = np.array([])
    net_v = 1.0
    init = 100000.0
    ref_data = None
    ref_data_file = r'Reference_date_value.xlsx'
    daily_file = r'Simple_Auto_combination_date_info.xlsx'


    def __init__(self,curr_input):
        self.get_date()
        self.init = self.read_initial()
        # curr_input = (curr_hk, curr_us)

        #if curr_input == 0:
        #    self.currency = self.read_currency()    # HK vs rmb
        #else:
        #    self.currency = curr_input
            
        (self.currency_hk, self.currency_us) = curr_input
        self.combn_data = self.read_comb_info()
        self.codes = self.combn_data['code'].tolist()
        self.nums = np.float_(self.combn_data['num'].tolist())
        self.names = self.combn_data['name'].tolist()
        
        #self.get_stock_basic_all()
        #print('Stock profits downloaded!')
        
        i = 0
        for s_code in self.codes:
            price = self.get_price(s_code)
            print(self.names[i])
            print(price)
            self.prices = np.append(self.prices, price)
                #self.pes = np.append(self.pes, np.Infinity)   # numpy.float64
                #self.pbs = np.append(self.pbs, np.Infinity)   # numpy.float64
                #self.epses = np.append(self.epses, 0)
                #self.is_stock.append(False)
            value = price*self.nums[i]
            self.values = np.append(self.values,value)
                #self.profits = np.append(self.profits,0)
                #self.nassets = np.append(self.nassets,0)
                #self.profitable_values = np.append(self.profitable_values,0.0)
            """
            else:
                # This is not an ETF, but a stock
                price = self.get_price(s_code)
                print(self.names[i])
                print(price)
                self.prices = np.append(self.prices, price)         
                pe = self.info_all.loc[s_code]['pe']
                self.pes = np.append(self.pes, pe)   # numpy.float64
                pb = self.info_all.loc[s_code]['pb']
                self.pbs = np.append(self.pbs, self.info_all.loc[s_code]['pb'])
                eps = self.info_all.loc[s_code]['esp']# numpy.float64
                self.epses = np.append(self.epses, eps)
                self.is_stock.append(True)
                value = price*self.nums[i]
                self.values = np.append(self.values,value)
                seasons = round(price/pe/eps)
                profit = eps/seasons*4*self.nums[i]   # latest profit per year (effectively)
                self.profits = np.append(self.profits,profit)  
                asset = price/pb*self.nums[i]
                self.nassets = np.append(self.nassets, asset)
                self.profitable_values = np.append(self.profitable_values,value)
            """
            i = i+1
        self.update_combi_data()
        self.update_reference()
        
    def update_reference(self):
        ref_info_file = r'Reference_codes.xlsx'
        #load target combination information
        ref_info = pd.read_excel(ref_info_file,dtype = str)
        comb_data = pd.read_excel(self.daily_file)
        comb_value_0 = comb_data['Net value'].iloc[0]
        ref_data = pd.read_excel(self.ref_data_file)
        ini_date = ref_data['Date'].iloc[0]
        n = len(ref_info['ref_labels'])
        tmp_df = pd.DataFrame({"Date":[self.date]})
        for i in range(n):
            s_code = ref_info['ref_code'].iloc[i]
            tmp_data = ts.get_k_data(s_code)
            tmp_close = tmp_data.iloc[-1]['close']
            tmp_0 = tmp_data.loc[tmp_data['date']==ini_date]['close'].tolist()[0]
            tmp_df[ref_info['ref_labels'].iloc[i]] = tmp_close/tmp_0*comb_value_0
        self.ref_data = pd.concat([ref_data,tmp_df])


                    

    def update_combi_data(self):
        #self.asset = self.nassets.sum()
        #self.total_profit = self.profits.sum()
        #total_profit_value = self.profitable_values.sum()
        #self.pe = total_profit_value/self.total_profit
        #self.pb = total_profit_value/self.asset
        #self.roe = self.total_profit/self.asset
        self.value = self.values.sum()
        self.ratios = self.values/self.value
        self.net_v = self.value/self.init
               
    def get_date(self):
        # date of beijing
        bj = timezone('Asia/Hong_Kong')
        bj_time = datetime.now(bj)
        bj_date = bj_time.strftime('%Y-%m-%d')
        self.date = bj_date
        
    def read_comb_info(self,*filename):
        if len(filename) == 0:
            file = u"Real_combination_info.xlsx"
        else:
            file = filename
        comb_info = pd.read_excel(file,dtype = str)
        return comb_info
    
    """
    def read_currency(self,*filename):
        if len(filename) == 0:
            file = u"Currency.xlsx"
        else:
            file = filename
        currency = pd.read_excel(file,dtype = str)
        return float(currency['price'].iat[0])
    """  
    def read_initial(self,*filename):
        if len(filename) == 0:
            file = u"Fund_shares.xlsx"
        else:
            file = filename
        init = pd.read_excel(file,dtype = str)
        return float(init['price'].iat[0])
    
    """
    def get_stock_basic_all(self):
        df_all = ts.get_stock_basics()
        self.info_all = df_all
    """  
    def get_price(self,s_code):
        try:
            tmp = int(s_code)
        except:
            pass
        else:
            if tmp == 0:
                # this is the item of Cash
                return 1.0
        if len(s_code) != 6:
            # HK or US stocks
            pdate = date.today() - timedelta(10)
            pdatet = pdate.strftime('%Y-%m-%d')
            data_Df=web.get_data_yahoo(s_code,pdatet,self.date)
            if s_code[-3:] == ".hk":
                # HK Stock
                currency = self.currency_hk
            else:
                # US Stock
                currency = self.currency_us
            price = data_Df['Close'].iloc[-1]*currency
        else:
            # A股
            df = ts.get_k_data(s_code)
            price = df.iloc[-1]['close']    # price of the latest closing trading day, numpy.float
        return price
    
    def save(self, **kwargs):
        default = {'daily_file': 'Simple_Auto_combination_date_info',\
                   'date_file': 'Latest_combination_ratio'}
        for item in default:
            if item in kwargs:
                default[item] = kwargs[item]

        dic_day = {'Total_value':self.value, \
                   'Date':self.date, \
                   "Net value":self.net_v}
        df_day = pd.DataFrame(dic_day,index = [0])
        try:
            day_in = pd.read_excel(default['daily_file']+ '.xlsx')
        except: # file not exist
            day_all = df_day
        else:
            day_all = day_in.append(df_day, ignore_index=True)#,sort=False)
        day_all.to_excel(self.daily_file, index=False)
        print(u'总市值:')
        print(self.value)
        print(u"净值:")
        print(self.net_v)
      
        
        dic = {'code':self.codes, 'name': self.names, 'num': self.nums,\
               'value':self.values,'ratio':self.ratios}
        df = pd.DataFrame.from_dict(dic)
        df = df.sort_values('ratio',ascending = False)
        print(df)
        df.to_excel(default['date_file'] + '.xlsx', index=False)
        self.ref_data.to_excel(self.ref_data_file, index=False)

