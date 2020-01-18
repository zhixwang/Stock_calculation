# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 09:26:04 2018

@author: zxwan
"""

import pandas as pd
import numpy as np
from wzx_library.plot_2D_line import plot_2D_line as p2l

comb_file = r'Simple_Auto_combination_date_info.xlsx'
comb_data = pd.read_excel(comb_file)
ref_data_file = r'Reference_date_value.xlsx'
ref_data = pd.read_excel(ref_data_file)

ref_info_file = r'Reference_codes.xlsx'
#load target combination information
ref_info = pd.read_excel(ref_info_file,dtype = str)
n = len(ref_info['ref_labels'])

dates = np.arange(len(comb_data['Date']))
xdata = dates

fig1 = p2l(xlabel = 'Date: '+comb_data['Date'].iloc[0]+" to "+comb_data['Date'].iloc[-1])
fig1.plot_curve(xdata,comb_data['Net value'],label = u'Personal')
for i in range(n):
    fig1.plot_curve(xdata,ref_data[ref_info['ref_labels'].iloc[i]],label = ref_info['ref_english'].iloc[i])
#fig1.show_figure(10)
fig1.save_figure(u"Real_combination_performance")
print("Initial value: %.3f" % comb_data['Net value'].iloc[0])
print("Latest value:")
for i in range(n):
    print("%s: %.3f" % (ref_info['ref_labels'].iloc[i],ref_data[ref_info['ref_labels'].iloc[i]].iloc[-1]))
print("%s: %.3f" % (u'大愚若智实盘',comb_data['Net value'].iloc[-1]))

"""
fig2 = p2l()
fig2.plot_curve(dates,com_close)
fig2.show_figure(10)
"""