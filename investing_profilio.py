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
# import urllib
import profolio_IO_files as pfiles

class auto_update_profolio:
    nums = np.array([])                 #number of each stock that you holds
    codes = []
    names = []
    prices = np.array([])
    values = np.array([])
    currency_hk = 0.89
    currency_us = 7.0176
    date = ""
    combn_data = None # Profolio information
    value = 0.0
    ratios = np.array([])
    net_v = 1.0
    init = 100000.0
    ref_data = None
    ref_data_file = pfiles.Profolio_reference_data
    daily_file = pfiles.Profolio_net_value
    write_to_file = True
    #ts_token = r''
    #tspro = None    # For Tushare API


    def __init__(self,curr_input,write_file):
        self.write_to_file = write_file
        print("Write to files: %r " % self.write_to_file)
        # print(self.write_to_file)
        self.get_date()
        self.init = self.read_initial()
            
        (self.currency_hk, self.currency_us) = curr_input
        self.combn_data = self.read_comb_info()
        self.codes = self.combn_data['code'].tolist()
        self.nums = np.float_(self.combn_data['num'].tolist())
        self.names = self.combn_data['name'].tolist()
        #token_file = open(pfiles.Ts_token)
        #self.ts_token = token_file.read()
        #self.tspro = ts.pro_api(token = self.ts_token)
        
        i = 0
        for s_code in self.codes:
            price = self.get_price(s_code)
            print(self.names[i])
            print(price)
            self.prices = np.append(self.prices, price)
            value = price*self.nums[i]
            self.values = np.append(self.values,value)
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
        self.update_profolio_data()
        self.update_reference()
        
    def update_reference(self):
        ref_info_file = pfiles.Reference_codes
        #load target profolio information
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
        
    def is_A_stock(self, s_code):
        # Check if a stock code means a stock in Chinese A market or not
        if len(s_code) != 6:
            # Check length first
            return False
        last_c =  s_code[-1]
        # Check also the last digit
        if last_c >= '0' and last_c <= '9':
            return True
        return False
                    

    def update_profolio_data(self):
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
            file = pfiles.Profolio_component_info
        else:
            file = filename
        comb_info = pd.read_excel(file,dtype = str)
        return comb_info
    
    def read_initial(self,*filename):
        if len(filename) == 0:
            file = pfiles.Profolio_share_number
        else:
            file = filename
        init = pd.read_excel(file,dtype = str)
        return float(init['price'].iat[0])

    def get_price(self,s_code):
        try:
            tmp = int(s_code)
        except:
            pass
        else:
            if tmp == 0:
                # this is the item of Cash
                return 1.0
        
        if not self.is_A_stock(s_code):
            try:
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
            except:
                # Stock code not founded in Yahoo, such as HK Options
                # Manually input the price in "Stock_price_manual_input.xlsx" ==> not optimal!
                manual_df = pd.read_excel(pfiles.Manual_input_price)
                # Correct the format of the table
                for i in range(len(manual_df)):
                    try:
                        # Correct code name for US stocks
                        manual_df.loc[i,'code'] = manual_df['code'].iloc[i].lower()
                    except:
                        pass
                try:
                    s_code = s_code.lower()
                except:
                    pass
                selected_stock = manual_df.loc[manual_df['code'] == s_code]
                price_value = selected_stock['price'].iloc[0]
                if s_code[-2:].lower() == r"hk":
                    currency = self.currency_hk
                else:
                    currency = self.currency_us
                price = price_value*currency
                
        else:
            try:
                # A股
                df = ts.get_k_data(s_code)
                price = df.iloc[-1]['close']    # price of the latest closing trading day, numpy.float
                """
                # For the new Tushare API-pro, which doesn't work for the convertible bonds
                end_date = self.date.replace('-','')    # set end date for query
                start_date = date.today() - timedelta(days=10)    # set start date for query
                start_date = str(start_date).replace('-','')    # change start date to text 
                # Re-format the stock code for new Tushare API
                if s_code[0] == '6':
                    # Shanghai Market
                    s_code = s_code + r".SH"
                elif s_code[0] == '0':
                    # Shenzhen Market
                    s_code = s_code + r".SZ"
                else:
                    print("Unknown market for A stock: " + s_code)
                    return 0.0
                df = self.tspro.daily(ts_code=s_code, start_date = start_date, end_date=end_date)
                #df = ts.get_k_data(s_code)
                price = df.iloc[-1]['close']    # price of the latest closing trading day, numpy.float
                """
            except:
                # Manually input the price in "Stock_price_manual_input.xlsx" ==> not optimal!
                manual_df = pd.read_excel(pfiles.Manual_input_price)
                # Correct the format of the table
                for i in range(len(manual_df)):
                    manual_df.loc[i,'code'] = str(manual_df.loc[i,'code'])
                # for i in range(len(manual_df)):
                #     if isinstance(manual_df.loc[i,'code'], int):
                #         # For A-share stock: int to string
                #         manual_df.loc[i,'code'] = str(manual_df.loc[i,'code'])
                #     try:
                #         # Correct code name for US stocks
                #         manual_df.loc[i,'code'] = manual_df['code'].iloc[i].lower()
                #     except:
                #         pass
                try:
                    s_code = s_code.lower()
                except:
                    pass
                selected_stock = manual_df.loc[manual_df['code'] == s_code]
                price_value = selected_stock['price'].iloc[0]
                price = price_value
        return price
    
    def save(self, **kwargs):
        # print(self.write_to_file)
        default = {'daily_file': pfiles.Profolio_net_value,\
                   'date_file': pfiles.Profolio_component_ratio}
        for item in default:
            if item in kwargs:
                default[item] = kwargs[item]

        dic_day = {'Total_value':self.value, \
                   'Date':self.date, \
                   "Net value":self.net_v}
        df_day = pd.DataFrame(dic_day,index = [0])
        try:
            day_in = pd.read_excel(default['daily_file'])
        except: # file not exist
            day_all = df_day
        else:
            day_all = day_in.append(df_day, ignore_index=True)#,sort=False)
        if self.write_to_file == True:
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
        if self.write_to_file == True:
            df.to_excel(default['date_file'], index=False)
            self.ref_data.to_excel(self.ref_data_file, index=False)

