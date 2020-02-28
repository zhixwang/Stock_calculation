# Stock_calculation
模拟基金净值的方式，计算A股、港股、美股全市场的个人实仓组合净值变化。

环境：Python 3.6；

需要安装 tushare 和 pandas-datareader

    pip install tushare
    pip install pandas-datareader

## 使用方法

- 手动在 "Real_combination_info.xlsx" 记录持仓信息，并且在每次调仓时更新。每天运行Python程序时，会自动从这个文件里读取数据，计算净值。
- 每日更新净值：

    python update_simplified_combination.py (-chk 0.89 -cus 7.01)

说明： -chk 人民币港币汇率； -cus 人民币美元汇率；若不输入任何参数，则会自动从和讯网查询实时美元和港币汇率并参与计算。基础货币为人民币。

相应汇率会自动更新到表格"Currency.xlsx"里。

- 每次新增资金时，手动在“份额资金投入记录.xlsx”中，记录对应的日期、入金记录，并根据前一日净值计算对应份额：
    
    新增份额 = 新增资金/最新基金净值

然后更新“Fund_shares.xlsx”，将文件中份额数更新为最新份额数。运行Python程序时，会自动读取该文件里的份额数据，计算模拟的基金净值：

    净值 = 总市值(来自"Real_combination_info.xlsx")/总份额("Fund_shares.xlsx")

- 每次运行完Python程序，会自动把最新净值和市值记录在"Simple_Auto_combination_date_info.xlsx"里，作为对比，每日的中证500、沪深300和创业板指会记录在"Reference_date_value.xlsx"里。想考察自己的组合净值变化曲线时，可以运行

> compare_history_performance.py

，会自动生成跟以上三个指数对比的组合净值曲线图。

- 持仓和个股仓位占比，会自动记录到"Latest_combination_ratio.xlsx"文件中。

- "Reference_codes.xlsx" 存放作为对比的指数代码

- 文件总结：英文名的xlsx文件会被程序自动写入或读取；中文名的xlsx文件仅用于手动辅助记录。
