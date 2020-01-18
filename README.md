# Stock_calculation
模拟基金净值的方式，计算A股、港股、美股全市场的个人实仓组合净值变化。

环境：Python 3.6
安装： tushare

    pip install tushare

每次新增资金时，在“份额资金投入记录.xlsx”中，记录对应的日期、入金，并根据前一日净值计算对应份额：
    
    新增份额 = 新增资金/最新基金净值

然后更新“Fund_shares.xlsx”，将文件中份额数增加至最新份额数。
当日交易完成后，更新“Read_combination_info.xlsx”，和“分账户现金.xlsx”，更新最新组合成分和账上现金状况。


每日更新净值：

    python update_simplified_combination.py (-chk 0.89 -cus 7.01)

对应汇率记录表格"Currency.xlsx"