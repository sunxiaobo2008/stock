from tkinter import *
from functools import partial
from tkinter.scrolledtext import *
import time
import os
from socket import create_connection
from configparser import ConfigParser
import tkinter as tk
from tkinter import tix
from tkinter import ttk
import tkinter.messagebox as tMsg
import queue
import tkinter.font
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import tushare as ts 
from datetime import datetime 
import matplotlib.dates as mdates 
from matplotlib.dates import AutoDateLocator 
from matplotlib.font_manager import FontProperties
import matplotlib as mpl
import matplotlib
import socket
import select
import threading
import queue 
from socket import *
import itchat
import read_selfStock
from copy import deepcopy
import stock_dict
from  sunxb_lazhu import Sunxb_candlestick_ohlc,computeM,SunxbPlotCandle
from pandas import Series, DataFrame
from read_selfStock import add_dict
from Stock_Strategy import searchStockPool,searchStrategy,SunxbsearchStrategy

stockPoolFile1 = 'D:/sunxb_finance/股票池/bvps0212.xlsx'
stockPoolFile2 = 'D:/sunxb_finance/股票池/good.xlsx'
stockPoolFile3 = 'D:/sunxb_finance/股票池/cz.xlsx'
stockPoolFile4 = 'D:/sunxb_finance/股票池/xjl.xlsx'

stockSelectFile = 'D:/sunxb_finance/sunxb_策略/'
stockPoolPath = 'D:/sunxb_finance/股票池/'       
stockInfoPath = 'D:/sunxb_finance/stock_info/'

#HOST = '192.168.1.60'  
pathRoute='D:/sunxb_finance/stock_info/'

pathRouteXX='D:/sunxb_finance/'
#pathRoute='D:/Users/sunxiaobo/finance_python/stock_info/'
pathxx='D:/sunxb_finance/stocks/2018-01-31/' 
StockDate={}
StockDate['卖盘']={}
StockDate['买盘']={}

SelfStockNum = 0

def printList(event):  
    print(GUI.Listbox1.get(self.Listbox1.curselection())) 

def mkdir(path):
    # 引入模块
    #import os
 
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
 
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)
 
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path) 
 
        print (path+' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print (path+' 目录已存在')
        return False

    
class msgself:
    def __init__(self, initdir = None):
        self.top = tix.Tk(className='股票信息系统——孙孝波')
        self.top.geometry=('=930x700+300+100')
        self.top.maxsize(1600,1200)
        #self.top.minsize(530,450)
        
        self.top.iconbitmap(default='')

        self.stockDict = stock_dict.stockDict

        self.stock_pb_flag =IntVar()
        self.stock_pe_flag =IntVar()
        self.stock_esp_flag =IntVar()
        #self.stock_sjl =IntVar()
        #self.stock_sjl_d =IntVar()
        self.stock_sjl =StringVar()
        self.stock_sjl_d =StringVar()
        
        self.stock_sy =StringVar()
        self.stock_sy_d =StringVar()
        self.stock_syl =StringVar()
        self.stock_syl_d =StringVar()
        #self.Check_button_value.set('')
        self.frame_item = LabelFrame(self.top,relief=FLAT)
        self.frame_item.grid(column=0,row=0,sticky=N,pady=5)
        self.value=[]
        self.notebook = ttk.Notebook(self.frame_item,padding =10)
        self.notebook.grid()
        self.frameIT = Frame(self.notebook,name='hh')
        self.notebook.add(self.frameIT,text='综合数据')
        self.frameSunxb = Frame(self.notebook,name='sxb')
        self.notebook.add(self.frameSunxb,text='基本面获取')

        self.frameSunxb1 = Frame(self.notebook,name='sxb1')
        self.notebook.add(self.frameSunxb1,text='基本面选股(1)')

        self.frameSunxb2 = Frame(self.notebook,name='sxb2')
        self.notebook.add(self.frameSunxb2,text='基本面选股(2)')

        self.frameSunxb3 = Frame(self.notebook,name='sxb3')
        self.notebook.add(self.frameSunxb3,text='基本数据选股')

        self.frameSelfStock= Frame(self.notebook,name='sxb4')
        self.notebook.add(self.frameSelfStock,text='自选股')

        self.frameMonitor= Frame(self.notebook,name='sxb5')
        self.notebook.add(self.frameMonitor,text='股票监控')

        self.MonitorStockId=StringVar()
        self.MonitorPriceH=StringVar()
        self.MonitorPriceL=StringVar()
        self.MonitorPriceL.set('0')
        self.MonitorPriceH.set('100')
        self.MonitorFlag=StringVar()
        self.MonitorFlag.set('0')
        self.stockPoolFile = StringVar()

        self.LableMonitor = LabelFrame(self.frameMonitor,relief=GROOVE,borderwidth=2,text='股票监控',foreground='blue')
        self.LableMonitor.grid(sticky=W,padx=30)
        self.lable_M=tix.LabelEntry(self.LableMonitor)
        self.lable_M.subwidget_list['label']['text']='股票代码：'
        self.lable_M.subwidget_list['entry']['textvariable']=self.MonitorStockId

        self.lable_M1=tix.LabelEntry(self.LableMonitor)
        self.lable_M1.subwidget_list['label']['text']='价格高限：'
        self.lable_M1.subwidget_list['entry']['textvariable']=self.MonitorPriceH

        self.lable_M2=tix.LabelEntry(self.LableMonitor)
        self.lable_M2.subwidget_list['label']['text']='价格低限：'
        self.lable_M2.subwidget_list['entry']['textvariable']=self.MonitorPriceL

        self.lable_M.grid(column=0,row=0,padx=16,ipadx = 20)
        self.lable_M1.grid(column=1,row=0,padx=16,ipadx = 20)
        self.lable_M2.grid(column=2,row=0,padx=16,ipadx = 20)

        self.Monitorbutton=ttk.Button(self.LableMonitor,text='添加监控',width=5,command = self.button_add_Monitor)
        
        self.Monitorbutton.grid(column=0,row=1,padx=16,ipadx = 20)
        
        self.Monitorbutton=ttk.Button(self.LableMonitor,text='删除监控',width=5,command = self.button_del_Monitor)
        
        self.Monitorbutton.grid(column=1,row=1,padx=16,ipadx = 20)

        self.Monitorbutton=ttk.Button(self.LableMonitor,text='实施监控',width=5,command = self.button_do_Monitor)
        
        self.Monitorbutton.grid(column=2,row=1,padx=16,ipadx = 20)

        self.LableStrategy = LabelFrame(self.frameMonitor,relief=GROOVE,borderwidth=2,text='选股策略',foreground='blue')
        self.LableStrategy.grid(sticky=W,padx=30)

        self.lableStrategy_1=tix.LabelEntry(self.LableStrategy)
        self.lableStrategy_1.subwidget_list['label']['text']='股票池文件'
        self.lableStrategy_1.subwidget_list['entry']['textvariable']=self.stockPoolFile   #self.DateTime
        self.lableStrategy_1.grid(column=0,row=0,padx=15,pady=20,ipadx=30)

        self.Strategybutton=ttk.Button(self.LableStrategy,text='策略一',width=5,command = self.button_doStrategy)
        
        self.Strategybutton.grid(column=0,row=1,padx=16,ipadx = 20)

        self.Strategybutton=ttk.Button(self.LableStrategy,text='策略二',width=5,command = self.button_doStrategy2)
        
        self.Strategybutton.grid(column=1,row=1,padx=16,ipadx = 20)

        
        '''
        以下为根据技术面进行选股
        '''
        self.stock_condition1 = IntVar()
        self.stock_condition2 = IntVar()
        self.stock_condition3 = IntVar()
        self.stock_condition1.set(0)
        self.stock_condition2.set(0)
        self.stock_condition3.set(0)
        self.stock_turnoverH = StringVar()
        self.stock_turnoverL = StringVar()
        self.stock_TT_H = StringVar()
        self.stock_TT_M = StringVar()
        self.stock_priceH = StringVar()
        self.stock_priceL = StringVar()
        self.search_jishu_file = StringVar()
        self.store_jishu_file = StringVar()
        '''
        self.StockStrategy = LabelFrame(self.frameMonitor,relief=GROOVE,borderwidth=2,text='技术选股策略',foreground='blue')
        self.StockStrategy.grid(sticky=W,padx=30)
        
        self.lable_c7=tix.LabelEntry(self.StockStrategy)
        self.lable_c7.subwidget_list['label']['text']='搜索文件'
        self.lable_c7.subwidget_list['entry']['textvariable']=self.search_jishu_file   #self.DateTime
        self.lable_c7.grid(column=0,row=0,padx=15,pady=20,ipadx=30)

        self.lable_s7=tix.LabelEntry(self.StockStrategy)
        self.lable_s7.subwidget_list['label']['text']='存储文件'
        self.lable_s7.subwidget_list['entry']['textvariable']=self.store_jishu_file   #self.DateTime
        self.lable_s7.grid(column=1,row=0,padx=15,pady=20,ipadx=30)
        
        self.lable_2button=ttk.Button(self.StockStrategy,text='条件搜索',width=5,command = self.button_condition_search)
        
        self.lable_2button.grid(column=0,row=1,padx=16,ipadx = 20)

        self.checkbutton0=Checkbutton(self.StockStrategy, text="条件一", variable=self.stock_condition1)# ,command = check_command,onvalue ='hahah',offvalue='gggg'

        self.checkbutton0.grid(row=2,pady=8,stick=W,column=0,columnspan=4)
        self.checkbutton1=Checkbutton(self.StockStrategy, text="条件二", variable=self.stock_condition2)# ,command = check_command,onvalue ='hahah',offvalue='gggg'

        self.checkbutton1.grid(row=3,pady=8,stick=W,column=0,columnspan=4)
        
        self.checkbutton2=Checkbutton(self.StockStrategy, text="条件三", variable=self.stock_condition3)# ,command = check_command,onvalue ='hahah',offvalue='gggg'

        self.checkbutton2.grid(row=4,pady=8,stick=W,column=0,columnspan=4)

        self.lable_sjl=tix.LabelEntry(self.StockStrategy)
        self.lable_sjl.subwidget_list['label']['text']='换手率小于'
        self.lable_sjl.subwidget_list['entry']['textvariable']=self.stock_turnoverH   #self.DateTime
        self.lable_sjl.grid(column=1,row=2,padx=15,pady=20,ipadx=10)

        self.lable_sjl_d=tix.LabelEntry(self.StockStrategy)
        self.lable_sjl_d.subwidget_list['label']['text']='换手率大于：'
        self.lable_sjl_d.subwidget_list['entry']['textvariable']=self.stock_turnoverL   #self.DateTime
        self.lable_sjl_d.grid(column=2,row=2,padx=15,pady=20,ipadx=10)

        self.lable_sy=tix.LabelEntry(self.StockStrategy)
        self.lable_sy.subwidget_list['label']['text']='突破换手率'
        self.lable_sy.subwidget_list['entry']['textvariable']=self.stock_TT_H   #self.DateTime
        self.lable_sy.grid(column=1,row=3,padx=15,pady=20,ipadx=10)

        self.lable_sy_d=tix.LabelEntry(self.StockStrategy)
        self.lable_sy_d.subwidget_list['label']['text']='突破换手率均值：'
        self.lable_sy_d.subwidget_list['entry']['textvariable']=self.stock_TT_M   #self.DateTime
        self.lable_sy_d.grid(column=2,row=3,padx=15,pady=20,ipadx=10)

        self.lable_syl=tix.LabelEntry(self.StockStrategy)
        self.lable_syl.subwidget_list['label']['text']='估价小于'
        self.lable_syl.subwidget_list['entry']['textvariable']=self.stock_priceH   #self.DateTime
        self.lable_syl.grid(column=1,row=4,padx=15,pady=20,ipadx=10)

        self.lable_syl_d=tix.LabelEntry(self.StockStrategy)
        self.lable_syl_d.subwidget_list['label']['text']='估价大于：'
        self.lable_syl_d.subwidget_list['entry']['textvariable']=self.stock_priceL   #self.DateTime
        self.lable_syl_d.grid(column=2,row=4,padx=15,pady=20,ipadx=10)
        '''

        #self.ceshiCnt=IntVar()
        self.ceshiCnt=StringVar()
        self.ceshiCnt.set('000519')
        self.StockName=StringVar()
        self.StockCode=StringVar()
        #self.StockName.set('000519')
        
        self.DateTime=StringVar()
        self.DateTime.set('2018-01-05')
        self.DayCnt = StringVar()
        self.DayCnt.set(5)
        self.profit_store_file = StringVar()
        self.pay_store_file = StringVar()
        self.grow_store_file = StringVar()
        self.service_store_file = StringVar()
        self.outstanding_store_file = StringVar()
        self.cash_store_file = StringVar()
        self.baisc_store_file = StringVar()
        self.DayBegin = StringVar()
        self.DayBegin.set('2017-11-05')
        self.DayEnd = StringVar()
        xx = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        self.DayEnd.set(xx)

        self.K_P = StringVar()
        self.K_P.set('day')
        self.Year = StringVar()
        self.Year.set('2017')
        self.Jidu = StringVar()
        self.Jidu.set('1')

        self.search_file = StringVar()
        self.search_file.set('基本数据')
        
        self.search_basic_file = StringVar()
        self.search_basic_file.set('基本数据')
        

        self.search_pay_file  = StringVar()
        self.search_pay_file.set('2017_3_偿债能力')
        self.search_profit_file = StringVar()
        self.search_profit_file.set('2017_3_盈利能力')

        self.search_cash_file = StringVar()
        self.search_cash_file.set('2017_3_现金流量')
        
        self.store_file = StringVar()
        self.search_grow_file  = StringVar()
        self.search_grow_file.set('2017_3_成长能力')

        self.search_outstanding_file  = StringVar()
        self.search_outstanding_file.set('2017_3_业绩报告')
        '''
        增加基本数据选股
        '''
        self.baisc_hint_text=StringVar()
        self.baisc_hint_text.set('1、name, 2、industry, 3、area, 4、pe, 5、outstanding, 6、totals,7、totalAssets, 8、liquidAssets, 9、fixedAssets, 10、reserved,11、reservedPerShare, 12、esp, 13、bvps, 14、pb, 15、timeToMarket, 16、undp,17、perundp, 18、rev, 19、profit, 20、gpr, 21、npr, 22、holders')
        self.baisc_num  =StringVar()
        self.baisc_value_min  =StringVar()
        self.baisc_value_max  =StringVar()
        
        self.value_testResult =StringVar()
        self.value_testResult.set('bvps:每股净资  profit:利润同比(%)  npr:净利润率(%)')
        self.profit_hint_text =StringVar()
        self.profit_hint_text.set('[1]roe,净资产收益率(%)   [2]net_profit_ratio,净利率(%)\n [3]gross_profit_rate,毛利率(%)   [4]net_profits,净利润(万元)\n [5]esp,每股收益    [6]business_income,营业收入(百万元)\n [7]bips,每股主营业务收入(元)\n')
        self.profit_num  =StringVar()
        self.profit_value_min  =StringVar()
        self.profit_value_max  =StringVar()

        self.cash_hint_text =StringVar()
        self.cash_hint_text.set('[1]cf_sales,经营现金净流量对销售收入比率  [2]rateofreturn,资产的经营现金流量回报率\n [3]cf_nm,经营现金净流量与净利润的比率   [4]cf_liabilities,经营现金净流量对负债比率\n [5]cashflowratio,现金流量比率\n  ')

        self.cash_num  =StringVar()
        self.cash_value_min  =StringVar()
        self.cash_value_max  =StringVar()
        
        self.service_hint_text =StringVar()
        self.service_hint_text.set('[1]arturnover,应收账款周转率(次)  [2]arturndays,应收账款周转天数(天)\n[3]inventory_turnover,存货周转率(次)  [4]inventory_days,存货周转天数(天)\n[5]currentasset_turnover,流动资产周转率(次) [6]currentasset_days,流动资产周转天数(天) ')

        self.service_num  =StringVar()
        self.service_value_min  =StringVar()
        self.service_value_max  =StringVar()
        
        self.pay_hint_text =StringVar()
        self.pay_hint_text.set('[1]currentratio,流动比率       [2]quickratio,速动比率\n[3]cashratio,现金比率           [4]icratio,利息支付倍数\n[5]sheqratio,股东权益比率  [6]adratio,股东权益增长率 ')
        self.pay_num  =StringVar()
        self.pay_value_min  =StringVar()
        self.pay_value_max  =StringVar()
        self.grow_num  =StringVar()
        self.grow_value_min  =StringVar()
        self.grow_value_max  =StringVar()
        self.outstanding_num  =StringVar()
        self.outstanding_value_min  =StringVar()
        self.outstanding_value_max  =StringVar()

        self.grow_hint_text =StringVar()
        self.grow_hint_text.set('[1]mbrg,主营业务收入增长率(%)   [2]nprg,净利润增长率(%)\n[3]nav,净资产增长率                        [4]targ,总资产增长率\n[5]epsg,每股收益增长率                 [6]seg,股东权益增长率 ')
        self.outstanding_hint_text =StringVar()
        self.outstanding_hint_text.set('[1]eps,每股收益    [2]eps_yoy,每股收益同比(%)\n[3]bvps,每股净资产   [4]roe,净资产收益率(%)\n[5]epcf,每股现金流量(元) [6]net_profits,净利润(万元)\n[7]profits_yoy,净利润同比(%)   [8]distrib,分配方案\n[9]report_date,发布日期 ')
        
        #self.frame_control = LabelFrame(self.frame_item,relief=GROOVE,borderwidth=2,text='sunxiaobo2',foreground='blue')
        self.frame_control = LabelFrame(self.frameSunxb,relief=GROOVE,borderwidth=2,text='sunxiaobo2',foreground='blue')
        self.frame_control.grid(sticky=W,padx=30)
        self.lable_1=tix.LabelEntry(self.frame_control)
        self.lable_1.subwidget_list['label']['text']='股票代码：'
        self.lable_1.subwidget_list['entry']['textvariable']=self.StockCode

        self.lable_1.grid(column=0,row=0,padx=10,pady=10,ipadx=20)
 
        self.lable_1button=ttk.Button(self.frame_control,text='添加字典',width=5,command = self.button_add_dict)
        
        self.lable_1button.grid(column=1,row=0,padx=16,ipadx = 20)
        

        self.lable_2=tix.LabelEntry(self.frame_control)
        self.lable_2.subwidget_list['label']['text']='股票简称：'
        self.lable_2.subwidget_list['entry']['textvariable']=self.StockName

        self.lable_2.grid(column=0,row=1,padx=10,pady=10,ipadx=20)
 
        #self.lable_2button=ttk.Button(self.frame_control,text='设置',width=5,command = self.button_set)
        
        #self.lable_2button.grid(column=1,row=1,padx=8)

        self.stock_search = LabelFrame(self.frameSunxb,relief=GROOVE,borderwidth=2,text='stock_search',foreground='blue')
        self.stock_search.grid(sticky=W,padx=30)


        self.profit_search = LabelFrame(self.frameSunxb1,relief=GROOVE,borderwidth=2,text='盈利能力选股',foreground='blue')
        self.profit_search.grid(sticky=W,padx=30)

        self.profit_hint=Message(self.profit_search,width=500,textvariable=self.profit_hint_text,justify='left',foreground='blue',font=('Arial',9))
        self.profit_hint.grid(row=0,pady=5,stick=W,column=0,columnspan=4)

        self.cash_search = LabelFrame(self.frameSunxb1,relief=GROOVE,borderwidth=2,text='现金流选股',foreground='blue')
        self.cash_search.grid(sticky=W,padx=30)

        self.cash_hint=Message(self.cash_search,width=500,textvariable=self.cash_hint_text,justify='left',foreground='blue',font=('Arial',9))
        self.cash_hint.grid(row=0,pady=5,stick=W,column=0,columnspan=4)
        
        self.service_search = LabelFrame(self.frameSunxb1,relief=GROOVE,borderwidth=2,text='营运能力选股',foreground='blue')
        self.service_search.grid(sticky=W,padx=30)
        self.service_hint=Message(self.service_search,width=500,textvariable=self.service_hint_text,justify='left',foreground='blue',font=('Arial',9))
        self.service_hint.grid(row=0,pady=5,stick=W,column=0,columnspan=4)

        self.pay_search = LabelFrame(self.frameSunxb2,relief=GROOVE,borderwidth=2,text='偿债能力选股',foreground='blue')
        self.pay_search.grid(sticky=W,padx=30)

        self.pay_hint=Message(self.pay_search,width=500,textvariable=self.pay_hint_text,justify='left',foreground='blue',font=('Arial',9))
        self.pay_hint.grid(row=0,pady=5,stick=W,column=0,columnspan=4)
        
        self.grow_search = LabelFrame(self.frameSunxb2,relief=GROOVE,borderwidth=2,text='成长能力选股',foreground='blue')
        self.grow_search.grid(sticky=W,padx=30)

        self.grow_hint=Message(self.grow_search,width=500,textvariable=self.grow_hint_text,justify='left',foreground='blue',font=('Arial',9))
        self.grow_hint.grid(row=0,pady=5,stick=W,column=0,columnspan=4)

        self.outstanding_search = LabelFrame(self.frameSunxb2,relief=GROOVE,borderwidth=2,text='业绩报告选股',foreground='blue')
        self.outstanding_search.grid(sticky=W,padx=30)
        self.outstanding_hint=Message(self.outstanding_search,width=500,textvariable=self.outstanding_hint_text,justify='left',foreground='blue',font=('Arial',9))
        self.outstanding_hint.grid(row=0,pady=5,stick=W,column=0,columnspan=4)

        self.lable_c8=tix.LabelEntry(self.profit_search)
        self.lable_c8.subwidget_list['label']['text']='搜索文件'
        self.lable_c8.subwidget_list['entry']['textvariable']=self.search_profit_file   #self.DateTime
        self.lable_c8.grid(column=0,row=1,padx=15,pady=20,ipadx=30)

        self.lable_p=tix.LabelEntry(self.profit_search)
        self.lable_p.subwidget_list['label']['text']='存储文件'
        self.lable_p.subwidget_list['entry']['textvariable']=self.profit_store_file   #self.DateTime
        self.lable_p.grid(column=1,row=1,padx=40,pady=0,ipadx=20)
        
        self.lable_Pbutton=ttk.Button(self.profit_search,text='条件搜索',width=5,command = self.profit_search_stock)
     
        self.lable_Pbutton.grid(column=2,row=1,padx=40,ipadx = 20)

        self.profit_para=tix.LabelEntry(self.profit_search)
        self.profit_para.subwidget_list['label']['text']='选择参数'
        self.profit_para.subwidget_list['entry']['textvariable']=self.profit_num   #self.DateTime
        self.profit_para.grid(column=0,row=2,padx=40,pady=20,ipadx=10)

        self.profit_para2=tix.LabelEntry(self.profit_search)
        self.profit_para2.subwidget_list['label']['text']='小于参数：'
        self.profit_para2.subwidget_list['entry']['textvariable']=self.profit_value_min   #self.DateTime
        self.profit_para2.grid(column=1,row=2,padx=40,pady=20,ipadx=10)
        
        self.profit_para3=tix.LabelEntry(self.profit_search)
        self.profit_para3.subwidget_list['label']['text']='大于参数：'
        self.profit_para3.subwidget_list['entry']['textvariable']=self.profit_value_max   #self.DateTime
        self.profit_para3.grid(column=2,row=2,padx=40,pady=20,ipadx=10)
        '''
        现金流
        '''
        self.lable_cash8=tix.LabelEntry(self.cash_search)
        self.lable_cash8.subwidget_list['label']['text']='搜索文件'
        self.lable_cash8.subwidget_list['entry']['textvariable']=self.search_cash_file   #self.DateTime
        self.lable_cash8.grid(column=0,row=1,padx=15,pady=20,ipadx=30)

        self.lable_cashp=tix.LabelEntry(self.cash_search)
        self.lable_cashp.subwidget_list['label']['text']='存储文件'
        self.lable_cashp.subwidget_list['entry']['textvariable']=self.cash_store_file   #self.DateTime
        self.lable_cashp.grid(column=1,row=1,padx=40,pady=0,ipadx=20)
        
        self.lable_cashPbutton=ttk.Button(self.cash_search,text='条件搜索',width=5,command = self.cash_search_stock)
     
        self.lable_cashPbutton.grid(column=2,row=1,padx=40,ipadx = 20)

        self.cash_para=tix.LabelEntry(self.cash_search)
        self.cash_para.subwidget_list['label']['text']='选择参数'
        self.cash_para.subwidget_list['entry']['textvariable']=self.cash_num   #self.DateTime
        self.cash_para.grid(column=0,row=2,padx=40,pady=20,ipadx=10)

        self.cash_para2=tix.LabelEntry(self.cash_search)
        self.cash_para2.subwidget_list['label']['text']='小于参数：'
        self.cash_para2.subwidget_list['entry']['textvariable']=self.cash_value_min   #self.DateTime
        self.cash_para2.grid(column=1,row=2,padx=40,pady=20,ipadx=10)
        
        self.cash_para3=tix.LabelEntry(self.cash_search)
        self.cash_para3.subwidget_list['label']['text']='大于参数：'
        self.cash_para3.subwidget_list['entry']['textvariable']=self.cash_value_max   #self.DateTime
        self.cash_para3.grid(column=2,row=2,padx=40,pady=20,ipadx=10)
        

        '''
        '''
        self.lable_c9=tix.LabelEntry(self.pay_search)
        self.lable_c9.subwidget_list['label']['text']='搜索文件'
        self.lable_c9.subwidget_list['entry']['textvariable']=self.search_pay_file   #self.DateTime
        self.lable_c9.grid(column=0,row=1,padx=15,pady=20,ipadx=30)
        
        self.lable_pay=tix.LabelEntry(self.pay_search)
        self.lable_pay.subwidget_list['label']['text']='存储文件'
        self.lable_pay.subwidget_list['entry']['textvariable']=self.pay_store_file   #self.DateTime
        self.lable_pay.grid(column=1,row=1,padx=40,pady=0,ipadx=20)
        
        self.lable_Paybutton=ttk.Button(self.pay_search,text='条件搜索',width=5,command = self.pay_search_stock)
     
        self.lable_Paybutton.grid(column=2,row=1,padx=40,ipadx = 20)

        self.pay_para=tix.LabelEntry(self.pay_search)
        self.pay_para.subwidget_list['label']['text']='选择参数'
        self.pay_para.subwidget_list['entry']['textvariable']=self.pay_num   #self.DateTime
        self.pay_para.grid(column=0,row=2,padx=40,pady=10,ipadx=10)

        self.pay_para2=tix.LabelEntry(self.pay_search)
        self.pay_para2.subwidget_list['label']['text']='小于参数：'
        self.pay_para2.subwidget_list['entry']['textvariable']=self.pay_value_min   #self.DateTime
        self.pay_para2.grid(column=1,row=2,padx=40,pady=10,ipadx=10)
        
        self.pay_para3=tix.LabelEntry(self.pay_search)
        self.pay_para3.subwidget_list['label']['text']='大于参数：'
        self.pay_para3.subwidget_list['entry']['textvariable']=self.pay_value_max   #self.DateTime
        self.pay_para3.grid(column=2,row=2,padx=40,pady=10,ipadx=10)
        '''
        成长能力
        '''
        self.lable_grow9=tix.LabelEntry(self.grow_search)
        self.lable_grow9.subwidget_list['label']['text']='搜索文件'
        self.lable_grow9.subwidget_list['entry']['textvariable']=self.search_grow_file   #self.DateTime
        self.lable_grow9.grid(column=0,row=1,padx=15,pady=20,ipadx=30)
        
        self.lable_grow=tix.LabelEntry(self.grow_search)
        self.lable_grow.subwidget_list['label']['text']='存储文件'
        self.lable_grow.subwidget_list['entry']['textvariable']=self.grow_store_file   #self.DateTime
        self.lable_grow.grid(column=1,row=1,padx=40,pady=0,ipadx=20)
        
        self.lable_growbutton=ttk.Button(self.grow_search,text='条件搜索',width=5,command = self.grow_search_stock)
     
        self.lable_growbutton.grid(column=2,row=1,padx=40,ipadx = 20)

        self.grow_para=tix.LabelEntry(self.grow_search)
        self.grow_para.subwidget_list['label']['text']='选择参数'
        self.grow_para.subwidget_list['entry']['textvariable']=self.grow_num   #self.DateTime
        self.grow_para.grid(column=0,row=2,padx=40,pady=15,ipadx=10)

        self.grow_para2=tix.LabelEntry(self.grow_search)
        self.grow_para2.subwidget_list['label']['text']='小于参数：'
        self.grow_para2.subwidget_list['entry']['textvariable']=self.grow_value_min   #self.DateTime
        self.grow_para2.grid(column=1,row=2,padx=40,pady=15,ipadx=10)
        
        self.grow_para3=tix.LabelEntry(self.grow_search)
        self.grow_para3.subwidget_list['label']['text']='大于参数：'
        self.grow_para3.subwidget_list['entry']['textvariable']=self.grow_value_max   #self.DateTime
        self.grow_para3.grid(column=2,row=2,padx=40,pady=15,ipadx=10)
        
        '''
        业绩选股
        '''
        self.lable_outstanding9=tix.LabelEntry(self.outstanding_search)
        self.lable_outstanding9.subwidget_list['label']['text']='搜索文件'
        self.lable_outstanding9.subwidget_list['entry']['textvariable']=self.search_outstanding_file   #self.DateTime
        self.lable_outstanding9.grid(column=0,row=1,padx=15,pady=20,ipadx=30)
        
        self.lable_outstanding=tix.LabelEntry(self.outstanding_search)
        self.lable_outstanding.subwidget_list['label']['text']='存储文件'
        self.lable_outstanding.subwidget_list['entry']['textvariable']=self.outstanding_store_file   #self.DateTime
        self.lable_outstanding.grid(column=1,row=1,padx=40,pady=0,ipadx=20)
        
        self.lable_outstandingbutton=ttk.Button(self.outstanding_search,text='条件搜索',width=5,command = self.outstanding_search_stock)
     
        self.lable_outstandingbutton.grid(column=2,row=1,padx=40,ipadx = 20)

        self.outstanding_para=tix.LabelEntry(self.outstanding_search)
        self.outstanding_para.subwidget_list['label']['text']='选择参数'
        self.outstanding_para.subwidget_list['entry']['textvariable']=self.outstanding_num   #self.DateTime
        self.outstanding_para.grid(column=0,row=2,padx=40,pady=15,ipadx=10)

        self.outstanding_para2=tix.LabelEntry(self.outstanding_search)
        self.outstanding_para2.subwidget_list['label']['text']='小于参数：'
        self.outstanding_para2.subwidget_list['entry']['textvariable']=self.outstanding_value_min   #self.DateTime
        self.outstanding_para2.grid(column=1,row=2,padx=40,pady=15,ipadx=10)
        
        self.outstanding_para3=tix.LabelEntry(self.outstanding_search)
        self.outstanding_para3.subwidget_list['label']['text']='大于参数：'
        self.outstanding_para3.subwidget_list['entry']['textvariable']=self.outstanding_value_max   #self.DateTime
        self.outstanding_para3.grid(column=2,row=2,padx=40,pady=15,ipadx=10)
        '''
        '''
        self.baisc_search = LabelFrame(self.frameSunxb3,relief=GROOVE,borderwidth=2,text='基本数据选股',foreground='blue')
        self.baisc_search.grid(sticky=W,padx=30)

        self.baisc_hint=Message(self.baisc_search,width=500,textvariable=self.baisc_hint_text,justify='left',foreground='blue',font=('Arial',9))
        self.baisc_hint.grid(row=0,pady=5,stick=W,column=0,columnspan=4)
                                 
        self.lable_b9=tix.LabelEntry(self.baisc_search)
        self.lable_b9.subwidget_list['label']['text']='搜索文件'
        self.lable_b9.subwidget_list['entry']['textvariable']=self.search_basic_file   #self.DateTime
        self.lable_b9.grid(column=0,row=1,padx=15,pady=20,ipadx=30)
        
        self.lable_baisc=tix.LabelEntry(self.baisc_search)
        self.lable_baisc.subwidget_list['label']['text']='存储文件'
        self.lable_baisc.subwidget_list['entry']['textvariable']=self.baisc_store_file   #self.DateTime
        self.lable_baisc.grid(column=1,row=1,padx=40,pady=0,ipadx=20)
        
        self.lable_baiscbutton=ttk.Button(self.baisc_search,text='条件搜索',width=5,command = self.baisc_search_stock)
     
        self.lable_baiscbutton.grid(column=2,row=1,padx=40,ipadx = 20)


        
        self.baisc_para=tix.LabelEntry(self.baisc_search)
        self.baisc_para.subwidget_list['label']['text']='选择参数'
        self.baisc_para.subwidget_list['entry']['textvariable']=self.baisc_num   #self.DateTime
        self.baisc_para.grid(column=0,row=2,padx=40,pady=15,ipadx=10)

        self.baisc_para2=tix.LabelEntry(self.baisc_search)
        self.baisc_para2.subwidget_list['label']['text']='小于参数：'
        self.baisc_para2.subwidget_list['entry']['textvariable']=self.baisc_value_min   #self.DateTime
        self.baisc_para2.grid(column=0,row=3,padx=40,pady=15,ipadx=10)
        
        self.baisc_para3=tix.LabelEntry(self.baisc_search)
        self.baisc_para3.subwidget_list['label']['text']='大于参数：'
        self.baisc_para3.subwidget_list['entry']['textvariable']=self.baisc_value_max   #self.DateTime
        self.baisc_para3.grid(column=1,row=3,padx=40,pady=15,ipadx=10)


        
        
        print(self.ceshiCnt.get())
        

        
        
        
        self.null_ctr=Label(self.frame_control)
        self.null_ctr.grid(column=2,row=0,padx=40)

        self.button_ctl=Button(self.frame_control,text='显示',relief='groove',command = self.Print_result)

        self.button_ctl.grid(column =3,row=0,padx=5)
        self.msg_control=Message(self.frame_control,width=500,textvariable=self.value_testResult,justify='center',foreground='blue',font=('Arial',9))
        self.msg_control.grid(row=10,pady=5,stick=W,column=0,columnspan=4)

        self.stockInfo = StringVar()
        self.stockInfo.set('codeName  price\n')
        self.msg_stock=Message(self.frameMonitor,width=500,textvariable=self.stockInfo,justify='left',foreground='blue',font=('Arial',9))
        self.msg_stock.grid(row=11,pady=5,stick=W,column=0,columnspan=4)
        
        #Check_button_value=1
        
        #self.checkbutton=Checkbutton(self.frame_control, text="Enabled", variable=self.Check_button_value,command = check_command)# ,command = check_command,onvalue ='hahah',offvalue='gggg'

        #self.checkbutton.grid(row=7,pady=8,stick=W,column=0,columnspan=4)

        #
        self.frame_control_It = LabelFrame(self.frameIT,relief=GROOVE,borderwidth=2,text='sunxiaobo3',foreground='blue')
        self.frame_control_It.grid(sticky=N,padx=20)
        self.lable_2=tix.LabelEntry(self.frame_control_It)
        self.lable_2.subwidget_list['label']['text']='股票代码：'
        self.lable_2.subwidget_list['entry']['textvariable']=self.ceshiCnt
        self.lable_2.grid(column=0,row=1,padx=15,pady=20,ipadx=10)

        self.lable_3=tix.LabelEntry(self.frame_control_It)
        self.lable_3.subwidget_list['label']['text']='数据日期：'
        self.lable_3.subwidget_list['entry']['textvariable']=self.DayCnt   #self.DateTime
        self.lable_3.grid(column=0,row=0,padx=15,pady=20,ipadx=10)



        self.lable_c5=tix.LabelEntry(self.frame_control)
        self.lable_c5.subwidget_list['label']['text']='日期：(年)'
        self.lable_c5.subwidget_list['entry']['textvariable']=self.Year   #self.DateTime
        self.lable_c5.grid(column=0,row=2,padx=15,pady=20,ipadx=10)
        self.lable_c6=tix.LabelEntry(self.frame_control)
        self.lable_c6.subwidget_list['label']['text']='日期：(季度)'
        self.lable_c6.subwidget_list['entry']['textvariable']=self.Jidu  #self.DateTime
        self.lable_c6.grid(column=0,row=3,padx=15,pady=20,ipadx=10)
        
        self.lable_C2button=ttk.Button(self.frame_control,text='获取基本面',width=5,command = self.button_get_profit)
        
        self.lable_C2button.grid(column=1,row=2,padx=16,ipadx=15)

        self.lable_slfbutton=ttk.Button(self.frameSelfStock,text='自选股一',width=5,command = self.button_load_selfStock1)
        
        self.lable_slfbutton.grid(column=0,row=0,padx=16,ipadx=10)
        self.lable_slfbutton=ttk.Button(self.frameSelfStock,text='自选股二',width=5,command = self.button_load_selfStock2)
        
        self.lable_slfbutton.grid(column=1,row=0,padx=16,ipadx=10)
        self.lable_slfbutton=ttk.Button(self.frameSelfStock,text='自选股三',width=5,command = self.button_load_selfStock3)
        
        self.lable_slfbutton.grid(column=2,row=0,padx=16,ipadx=10)
        
        self.lable_slfbutton=ttk.Button(self.frameSelfStock,text='自选股四',width=5,command = self.button_load_selfStock4)
        
        self.lable_slfbutton.grid(column=3,row=0,padx=16,ipadx=10)

        self.Kbutton=ttk.Button(self.frameSelfStock,text='K线',width=5,command = self.button_K_Real)
        
        self.Kbutton.grid(column=4,row=0,padx=16,ipadx=10)
        
        self.Listbox1 = Listbox(self.frameSelfStock,relief=GROOVE,borderwidth=2,selectmode = BROWSE)
        stockId_self = read_selfStock.read_selfStock()
        #print(stockId_self)
        for item in stockId_self:  
            self.Listbox1.insert(END, item)
        #self.Listbox1.pack()
        self.Listbox1.grid(column=0,row=1,padx=40,pady=20,ipady=200)
        #self.Listbox1.bind('<Double-Button-1>',printList)
        self.Listbox1.bind('<Double-Button-1>',self.Plot_k)
        #self.Listbox1.bind('<ButtonRelease-Button-1>',Plot_k_1)

        '''
        以下为根据基本面进行选股
        '''
        
        self.lable_c7=tix.LabelEntry(self.stock_search)
        self.lable_c7.subwidget_list['label']['text']='搜索文件'
        self.lable_c7.subwidget_list['entry']['textvariable']=self.search_file   #self.DateTime
        self.lable_c7.grid(column=0,row=0,padx=15,pady=20,ipadx=30)

        self.lable_s7=tix.LabelEntry(self.stock_search)
        self.lable_s7.subwidget_list['label']['text']='存储文件'
        self.lable_s7.subwidget_list['entry']['textvariable']=self.store_file   #self.DateTime
        self.lable_s7.grid(column=1,row=0,padx=15,pady=20,ipadx=30)
        
        self.lable_2button=ttk.Button(self.stock_search,text='条件搜索',width=5,command = self.button_search_stock)
        
        self.lable_2button.grid(column=0,row=1,padx=16,ipadx = 20)

        self.checkbutton0=Checkbutton(self.stock_search, text="市净率", variable=self.stock_pb_flag)# ,command = check_command,onvalue ='hahah',offvalue='gggg'

        self.checkbutton0.grid(row=2,pady=8,stick=W,column=0,columnspan=4)
        self.checkbutton1=Checkbutton(self.stock_search, text="每股收益", variable=self.stock_esp_flag)# ,command = check_command,onvalue ='hahah',offvalue='gggg'

        self.checkbutton1.grid(row=3,pady=8,stick=W,column=0,columnspan=4)
        
        self.checkbutton2=Checkbutton(self.stock_search, text="市盈率", variable=self.stock_pe_flag)# ,command = check_command,onvalue ='hahah',offvalue='gggg'

        self.checkbutton2.grid(row=4,pady=8,stick=W,column=0,columnspan=4)

        self.lable_sjl=tix.LabelEntry(self.stock_search)
        self.lable_sjl.subwidget_list['label']['text']='市净率小于'
        self.lable_sjl.subwidget_list['entry']['textvariable']=self.stock_sjl   #self.DateTime
        self.lable_sjl.grid(column=1,row=2,padx=15,pady=20,ipadx=10)

        self.lable_sjl_d=tix.LabelEntry(self.stock_search)
        self.lable_sjl_d.subwidget_list['label']['text']='市净率大于：'
        self.lable_sjl_d.subwidget_list['entry']['textvariable']=self.stock_sjl_d   #self.DateTime
        self.lable_sjl_d.grid(column=2,row=2,padx=15,pady=20,ipadx=10)

        self.lable_sy=tix.LabelEntry(self.stock_search)
        self.lable_sy.subwidget_list['label']['text']='每股收益小于'
        self.lable_sy.subwidget_list['entry']['textvariable']=self.stock_sy   #self.DateTime
        self.lable_sy.grid(column=1,row=3,padx=15,pady=20,ipadx=10)

        self.lable_sy_d=tix.LabelEntry(self.stock_search)
        self.lable_sy_d.subwidget_list['label']['text']='每股收益大于：'
        self.lable_sy_d.subwidget_list['entry']['textvariable']=self.stock_sy_d   #self.DateTime
        self.lable_sy_d.grid(column=2,row=3,padx=15,pady=20,ipadx=10)

        self.lable_syl=tix.LabelEntry(self.stock_search)
        self.lable_syl.subwidget_list['label']['text']='市盈率小于'
        self.lable_syl.subwidget_list['entry']['textvariable']=self.stock_syl   #self.DateTime
        self.lable_syl.grid(column=1,row=4,padx=15,pady=20,ipadx=10)

        self.lable_syl_d=tix.LabelEntry(self.stock_search)
        self.lable_syl_d.subwidget_list['label']['text']='市盈率大于：'
        self.lable_syl_d.subwidget_list['entry']['textvariable']=self.stock_syl_d   #self.DateTime
        self.lable_syl_d.grid(column=2,row=4,padx=15,pady=20,ipadx=10)
        
        '''
        '''
        
        

        self.lable_5=tix.LabelEntry(self.frame_control_It)
        self.lable_5.subwidget_list['label']['text']='起始日期：'
        self.lable_5.subwidget_list['entry']['textvariable']=self.DayBegin   #self.DateTime
        self.lable_5.grid(column=0,row=2,padx=15,pady=20,ipadx=10)

        self.lable_6=tix.LabelEntry(self.frame_control_It)
        self.lable_6.subwidget_list['label']['text']='终止日期：'
        self.lable_6.subwidget_list['entry']['textvariable']=self.DayEnd   #self.DateTime
        self.lable_6.grid(column=0,row=3,padx=15,pady=20,ipadx=10)

        '''
        增加文件合并选择
        '''
        self.StoreFile1 = StringVar()
        self.SearchFile1 = StringVar()
        self.SearchFile2 = StringVar()
        self.SearchFile1.set('2016yj_roe')
        self.SearchFile2.set('2015yj_roe')
        self.lable_s6=tix.LabelEntry(self.frame_control_It)
        self.lable_s6.subwidget_list['label']['text']='合并文件1：'
        self.lable_s6.subwidget_list['entry']['textvariable']=self.SearchFile1   #self.DateTime
        self.lable_s6.grid(column=0,row=7,padx=15,pady=20,ipadx=10)

        self.lable_s7=tix.LabelEntry(self.frame_control_It)
        self.lable_s7.subwidget_list['label']['text']='合并文件2：'
        self.lable_s7.subwidget_list['entry']['textvariable']=self.SearchFile2   #self.DateTime
        self.lable_s7.grid(column=0,row=8,padx=15,pady=20,ipadx=10)

        self.lable_s7=tix.LabelEntry(self.frame_control_It)
        self.lable_s7.subwidget_list['label']['text']='存储文件：'
        self.lable_s7.subwidget_list['entry']['textvariable']=self.StoreFile1   #self.DateTime
        self.lable_s7.grid(column=1,row=8,padx=15,pady=20,ipadx=10)
        
        self.lable_2button=ttk.Button(self.frame_control_It,text='交集合并',width=5,command = self.button_intersection)
        
        self.lable_2button.grid(column=1,row=7,padx=16,ipadx=10)
        

        self.lable_7=tix.LabelEntry(self.frame_control_It)
        self.lable_7.subwidget_list['label']['text']='K线周期:(5,15,30,60,W,M)'
        self.lable_7.subwidget_list['entry']['textvariable']=self.K_P   #self.DateTime
        self.lable_7.grid(column=0,row=4,padx=15,pady=20,ipadx=10)
        
        print(self.ceshiCnt.get())
        #self.lable_2.grid(column=0,row=1,padx=10,pady=20,ipadx=20)
 
        self.lable_2button=ttk.Button(self.frame_control_It,text='设置',width=5,command = self.button_set)
        
        self.lable_2button.grid(column=1,row=0,padx=16,ipadx=10)

        self.lable_slfbutton=ttk.Button(self.frame_control_It,text='添加自选股',width=5,command = self.button_add_selfStock)
        
        self.lable_slfbutton.grid(column=1,row=1,padx=16,ipadx=10)
        
        self.lable_slfbutton=ttk.Button(self.frame_control_It,text='删除自选股',width=5,command = self.button_del_selfStock)
        
        self.lable_slfbutton.grid(column=1,row=2,padx=16,ipadx=10)

        self.lable_3button=ttk.Button(self.frame_control_It,text='绘制K线',width=5,command = self.button_K_write)
        
        self.lable_3button.grid(column=1,row=4,padx=16,ipadx=10)

        self.lable_4button=ttk.Button(self.frame_control_It,text='实时行情',width=5,command = self.button_real_quat)
        
        self.lable_4button.grid(column=1,row=5,padx=16,ipadx=10)

        
        
        self.null_ctr=Label(self.frame_control_It)
        self.null_ctr.grid(column=2,row=0,padx=40)

        self.button_ctl2=Button(self.frame_control_It,text='网爬数据',relief='groove',command = self.Print_result)

        self.button_ctl2.grid(column =3,row=0,padx=5)

        self.button_report_basic=Button(self.frame_control_It,text='业绩报告',relief='groove',command = self.button_report_basic)

        self.button_report_basic.grid(column =3,row=1,padx=5)

        self.button_report_basic1=Button(self.frame_control_It,text='机构数据',relief='groove',command = self.button_jigou)

        self.button_report_basic1.grid(column =3,row=2,padx=5)

        self.button_report_basic2=Button(self.frame_control_It,text='上证融资融券',relief='groove',command = self.button_sh_margins)

        self.button_report_basic2.grid(column =3,row=3,padx=5)

        self.button_report_basic3=Button(self.frame_control_It,text='深成融资融券明细',relief='groove',command = self.button_sc_margins)

        self.button_report_basic3.grid(column =3,row=4,padx=5) 
        self.button_report_basic4=Button(self.frame_control_It,text='深成个股融资明细',relief='groove',command = self.button_scgg_margins)

        self.button_report_basic4.grid(column =3,row=5,padx=5)
        
        self.button_report_basic5=Button(self.frame_control_It,text='深成融资融券总额',relief='groove',command = self.button_scze_margins)

        self.button_report_basic5.grid(column =2,row=5,padx=5)

        self.button_report_basic5=Button(self.frame_control_It,text='沪市融资融券总额',relief='groove',command = self.button_shze_margins)

        self.button_report_basic5.grid(column =2,row=4,padx=5)

        
        self.msg_control=Message(self.frame_control_It,width=500,textvariable=self.value_testResult,justify='center',foreground='blue',font=('Arial',9))
        self.msg_control.grid(row=10,pady=5,stick=W,column=0,columnspan=4)

        self.frame_log=LabelFrame(self.top,height = 50,relief=GROOVE,borderwidth=4,text='日志',foreground = 'blue')
        self.frame_log.grid(column=1,row=0,sticky=N,pady=15,ipady=5)
        self.LogMsg=ScrolledText(self.frame_log,width=47,height=31,font=('Arial',10))
        self.LogMsg.grid(padx=10,pady=5,sticky=W,column=0,columnspan=2)
        self.button_log_1=ttk.Button(self.frame_log,text='保存',width=5,command=self.saveLog)
        self.button_log_1.grid(column=0,row=1,sticky=E,padx=10)
        self.button_log_2=ttk.Button(self.frame_log,text='清除',width=5,command=self.clearLog)
        self.button_log_2.grid(column=1,row=1,sticky=E,padx=10)
        
        #self.msg.insert('end','sunxiaobo nihao!\n ','INT')
        #self.msg.see('end')
        #self.msg.insert('end','sunxiaobo nihao ma?\n ','INT')
        #self.msg.insert('end','sunxiaobo nihao ma?\n ','INT')
        
        self.date = StringVar()
        self.date.set('hh')
        self.dateShow()
        print('time test!')
         
        self.Log_message()
    def button_K_Real(self):
        if self.Kbutton['text']=='K线':
            self.Kbutton['text']='实时'
        elif self.Kbutton['text']=='实时':
            self.Kbutton['text']='K线'
        
    def button_add_selfStock(self):
    
        codeid = self.ceshiCnt.get()
        codeId = self.searchStockDictCode(codeid)
        code = self.searchStockDictName(codeId)
        #x=len(str(codeId))
        #codeId = (6-x)*'0'+str(codeId)
        read_selfStock.add_selfStock(code)
        stockId_self = read_selfStock.read_selfStock()  
        self.Listbox1.delete(0, END)
        for item in stockId_self:  
            self.Listbox1.insert(END, item)
        #self.Listbox1.pack()
        #self.Listbox1.grid(column=0,row=2,padx=15,pady=20,ipadx=10)
        self.Listbox1.grid(column=0,row=1,padx=40,pady=20,ipady=200)
    
    def button_del_selfStock(self):
        codeid = self.ceshiCnt.get()
        codeId = self.searchStockDictCode(codeid)
        code = self.searchStockDictName(codeId)
        read_selfStock.del_selfStock(code)
        #self_kong=[]
        #self.Listbox1=[]
        #for item in self_stock:  
        self.Listbox1.delete(0, END)
            
        self.Listbox1.grid(column=0,row=2,padx=15,pady=20,ipadx=10)
        self_stock = read_selfStock.read_selfStock()
        for item in self_stock:  
            self.Listbox1.insert(END, item)
        #self.Listbox1.grid(column=0,row=2,padx=15,pady=20,ipadx=10)
        self.Listbox1.grid(column=0,row=1,padx=40,pady=20,ipady=200)    
    '''
    def button_add_selfStock(self):
        codeid = self.ceshiCnt.get()
        codeId = self.searchStockDictCode(codeid)
        code = self.searchStockDictName(codeId)
        stockInfo = pd.read_excel(stockPoolFile1)
        selfStockList = list(stockInfo['name'])
        self.Listbox1.delete(0, END)
        for item in selfStockList:  
            self.Listbox1.insert(END, item)
        #self.Listbox1.pack()
        self.Listbox1.grid(column=0,row=2,padx=15,pady=20,ipadx=10)
    '''   
    def button_load_selfStock1(self):
        stockInfo = pd.read_excel(stockPoolFile1)
        selfStockList = list(stockInfo['name'])
        self.Listbox1.delete(0, END)
        for item in selfStockList:  
            self.Listbox1.insert(END, item)
        #self.Listbox1.pack()
        #self.Listbox1.grid(column=0,row=2,padx=15,pady=20,ipadx=10)
        self.Listbox1.grid(column=0,row=1,padx=40,pady=20,ipady=200)

    def button_load_selfStock2(self):
        stockInfo = pd.read_excel(stockPoolFile2)
        selfStockList = list(stockInfo['name'])
        self.Listbox1.delete(0, END)
        for item in selfStockList:  
            self.Listbox1.insert(END, item)
        #self.Listbox1.pack()
        #self.Listbox1.grid(column=0,row=2,padx=15,pady=20,ipadx=10)
        self.Listbox1.grid(column=1,row=1,padx=40,pady=20,ipady=200)
    def button_load_selfStock3(self):
        stockInfo = pd.read_excel(stockPoolFile3)
        selfStockList = list(stockInfo['name'])
        self.Listbox1.delete(0, END)
        for item in selfStockList:  
            self.Listbox1.insert(END, item)
        #self.Listbox1.pack()
        #self.Listbox1.grid(column=0,row=2,padx=15,pady=20,ipadx=10)
        self.Listbox1.grid(column=2,row=1,padx=40,pady=20,ipady=200)
    def button_load_selfStock4(self):
        stockInfo = pd.read_excel(stockPoolFile4)
        selfStockList = list(stockInfo['name'])
        self.Listbox1.delete(0, END)
        for item in selfStockList:  
            self.Listbox1.insert(END, item)
        #self.Listbox1.pack()
        #self.Listbox1.grid(column=0,row=2,padx=15,pady=20,ipadx=10)
        self.Listbox1.grid(column=3,row=1,padx=40,pady=20,ipady=200)
        
    def dateShow(self):
        date=time.ctime()
        #print(date)
        self.date.set(date)
        self.top.after(1000,self.dateShow)   #递归，每秒钟
        #self.top.grid()
        self.value_testResult.set(date)
        
    def saveLog(self):
        global StockDate
        content=self.LogMsg.get(1.0,'end')
        #dateT=StringVar()
        #dateT.set(StockDate['卖盘'][0])
        stockId=self.ceshiCnt.get()
        #dateT=stockId + dateT
        logName = stockId +'.log'
        log=open('%s'%logName,'a')
        log.write(content)
        #content=self.msg.get(1.0,'end')
        #logName=self.value_data.get()
        #logName=logName.replace(':','_')
        print('Log 已经保存')

    def clearLog(self):
        self.LogMsg.delete(1.0,'end')

    def button_doStrategy(self):
        print('do Strategy!')
        File = self.stockPoolFile.get()
        if File == '':
            tMsg.showinfo('提示','请输入文件名')
            return
        searchStockPool(File)
        print('do Strategy complete!')
        
    def button_doStrategy2(self):
        print('do Strategy!')
        File = self.stockPoolFile.get()
        if File == '':
            tMsg.showinfo('提示','请输入文件名')
            return
        searchStrategy(File)
        SunxbsearchStrategy(File)
        print('do Strategy complete!')


    def button_add_Monitor(self):
        print('add monitor')
        file = '监控股票.xlsx'
        df = pd.read_excel(file,converters={'CodeId':str,'PriceH':str,'PriceL':str})   #converters 可以指示某列按照固定格式读取
        codeid = self.MonitorStockId.get()
        priceH = self.MonitorPriceH.get()
        priceL = self.MonitorPriceL.get()
        lenth = len(df)
        for i in range(lenth):
            if str(codeid) == str(df['CodeId'][i]):
                df['PriceH'][i] = priceH
                df['PriceL'][i] = priceL
                df.to_excel(file)
                return
        '''    
        df['PriceH'][lenth] = priceH
        df['PriceL'][lenth] = priceL
        df['CodeId'][lenth] = codeid
        '''
        df.loc[lenth] = [codeid,priceH,priceL]
        #df['CodeId'] = str(df['CodeId'])
        #df['PriceH'] = str(df['PriceH'])
        #df['PriceL'] = str(df['PriceL'])
        
        df.to_excel(file)
        
                

    def button_del_Monitor(self):
        
        file = '监控股票.xlsx'
        df = pd.read_excel(file,converters={'CodeId':str,'PriceH':str,'PriceL':str})
        codeid = self.MonitorStockId.get()
        lenth = len(df)
        for i in range(lenth):
            if codeid == df['CodeId'][i]:
                print('del monitor%s' %codeid)
                df = df.drop(i)
                df.index=range(lenth-1)
                print(df)
                df.to_excel(file)
                return
        
    def button_do_Monitor(self):
        print('do monitor')
        file = '监控股票.xlsx'
        if self.MonitorFlag == '1':
            tMsg.showinfo('提示错误','已实施监控，重新监控请重启软件')
            return
        else:
            self.MonitorFlag.set('1')
        df = pd.read_excel(file,converters={'CodeId':str,'PriceH':str,'PriceL':str})
        #itchat.auto_login()
        thread_list = []
        thread_list.append(threading.Thread(target= Monitor_stockList, args = (df, )))
    
        for a in thread_list:
            a.start()
        
    def mainloop(self):
        while 1:
            self.dateShow()
            
    def button_shze_margins(self):
        path_sc= pathRouteXX + '沪市融资融券明细/'
        mkdir(path_sc)
        DayBegin=self.DayBegin.get()
        DayEnd =self.DayEnd.get()
        print('please wait!')
        xx=ts.sh_margins(start=DayBegin, end=DayEnd)
    
        rzrq_name = path_sc  +'沪市融资融券总额' +'.xlsx'
        
        xx.to_excel(rzrq_name)
    
        rzze_1= xx.rzye[0]-xx.rzye[1]
        rzze_5= xx.rzye[0]-xx.rzye[5]
        rzze_10= xx.rzye[0]-xx.rzye[10]
        Message_Print('%s沪市融资余额总额%d\n' % (xx.opDate[0],xx.rzye[0]))
        Message_Print('%s沪市融资流入资金总额%d\n ,5日沪市融资流入总额%d\n.10日沪市融资流入总额%d\n' % (xx.opDate[0],rzze_1,rzze_5,rzze_10))
        date_time=xx.opDate
        date_time_translation = [datetime.strptime(d, '%Y-%m-%d').date() for d in date_time]
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.plot(date_time_translation,xx.rzye)
        plt.gcf().autofmt_xdate()
    
    
        plt.xlabel('Time',size=20) 
        plt.ylabel('融资金额',size=20,fontproperties=myfont)
        CodeName = '沪市融资总额'
        plt.title(CodeName,size=20,fontproperties=myfont)
        
        plt.show()
        Message_Print('沪市融资融券总额已经获取并存储本地 ')
        
    
    def button_scze_margins(self):
        path_sc= pathRouteXX + '深成融资融券明细/'
        DayBegin=self.DayBegin.get()
        DayEnd =self.DayEnd.get()
        print('please wait!')
        xx=ts.sz_margins(start=DayBegin, end=DayEnd)
    
        rzrq_name = path_sc  +'深成融资融券总额' +'.xlsx'
    
        lenth = len(xx)
        xx.index =range(lenth-1,-1,-1)
        xx.to_excel(rzrq_name)
    
        rzze_1= xx.rzye[0]-xx.rzye[1]
        rzze_5= xx.rzye[0]-xx.rzye[5]
        rzze_10= xx.rzye[0]-xx.rzye[10]
        Message_Print('%s深市融资余额总额%d\n' % (xx.opDate[0],xx.rzye[0]))
        Message_Print('%s深市融资流入资金总额%d\n ,5日深市融资流入总额%d\n.10日深市融资流入总额%d\n' % (xx.opDate[0],rzze_1,rzze_5,rzze_10))
        date_time=xx.opDate
        date_time_translation = [datetime.strptime(d, '%Y-%m-%d').date() for d in date_time]
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.plot(date_time_translation,xx.rzye)
        plt.gcf().autofmt_xdate()
    
    
        plt.xlabel('Time',size=20) 
        plt.ylabel('融资金额',size=20,fontproperties=myfont)
        CodeName = '深市融资总额'
        plt.title(CodeName,size=20,fontproperties=myfont)
        
        plt.show()
        Message_Print('深成融资融券总额已经获取并存储本地 ')
        
    def button_scgg_margins(self):
        path_sc= pathRouteXX + '深成融资融券明细/'
        stockid=self.ceshiCnt.get()
        stockId = self.searchStockDictCode(stockid)
        
    
        stock = int(int(stockId)/100000)
        
        if stock == 6:
            Message_Print('非深成融资股票')
            return
        a = np.random.standard_normal((1, 9))
        xx = pd.DataFrame(a)
    
        xx.columns = ['stockCode', 'securityAbbr', 'rzmre', 'rzye', 'rqmcl', 'rqyl', 'rqye',
           'rzrqye', 'opDate']
    
        DayBegin=self.DayBegin.get()
        DayEnd =self.DayEnd.get()
        yy=ts.sz_margins(start=DayBegin, end=DayEnd)
        #dataa=ts.get_hist_data('000519')
    
        rzrq_name = path_sc + stockId +'深成融资融券明细' +'.xlsx'
        i = 0
        #j=0
        for index in yy.opDate:
            rzrq_sc = path_sc + index +'深成融资融券明细' +'.xlsx'
            rzrqwj= pd.read_excel(rzrq_sc)
            j=0
            for index1 in rzrqwj.stockCode:
                
                if int(index1) == int(stockId):
                    
                    xx.ix[i] = rzrqwj.ix[j]
                    i=i+1
                    #print('sunxiaobo %d' %i)
                    #print('%s' %rzrqwj.ix[j])
                j=j+1
        xx.to_excel(rzrq_name)
    
        date_time=xx.opDate
        date_time_translation = [datetime.strptime(d, '%Y-%m-%d').date() for d in date_time]
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.plot(date_time_translation,xx.rzye)
        plt.gcf().autofmt_xdate()
    
    
        plt.xlabel('Time',size=20) 
        plt.ylabel('融资金额',size=20,fontproperties=myfont)
        CodeName = str(stockId) + xx.securityAbbr[0]
        plt.title(CodeName,size=20,fontproperties=myfont)
        
        plt.show()
                    
        Message_Print('%s深成融资融券明细已经获取并存储 ' %stockId)
         
            
    def button_sc_margins(self):
        path_sc= pathRouteXX + '深成融资融券明细/'
        mkdir(path_sc)
        DayBegin=self.DayBegin.get()
        DayEnd =self.DayEnd.get()
        rzrq_sc = path_sc + DayBegin +'深成融资融券明细' +'.xlsx'
    
        #dataa=ts.get_hist_data('000519')
        xx=ts.sz_margins(start=DayBegin, end=DayEnd)
        xx.to_excel(rzrq_sc)
        i=0
        for index in xx.opDate:
            i=i+1
            
            rzrq = ts.sz_margin_details(index)
            rzrq_sc = path_sc + index +'深成融资融券明细' +'.xlsx'
            rzrq.to_excel(rzrq_sc)
            time.sleep(2)
        Message_Print('%s深成融资融券明细已经获取并存储 ' %DayBegin )
    
    
        
    def button_sh_margins(self):
        DayBegin=self.DayBegin.get()
        DayEnd =self.DayEnd.get()
        #stockId=self.ceshiCnt.get()
        codeid = self.ceshiCnt.get()
        stockId = self.searchStockDictCode(codeid)
        
        stock = int(int(stockId)/100000)
        
        if stock != 6:
            Message_Print('非上证融资股票')
            return
        else:
            rzrq=ts.sh_margin_details(start=DayBegin, end=DayEnd, symbol=stockId)
    
        for i in range(5):
            rzlre = rzrq.rzye[i] - rzrq.rzye[i+1]
            Message_Print('%s %s 融资流入%.2f\n'%(rzrq.opDate[i],rzrq.securityAbbr[i],rzlre))
            Message_Print('%s %s 融资余额%.2f\n'%(rzrq.opDate[i],rzrq.securityAbbr[i],rzrq.rzye[i]))
        date_time=rzrq.opDate
        date_time_translation = [datetime.strptime(d, '%Y-%m-%d').date() for d in date_time]
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.plot(date_time_translation,rzrq.rzye)
        plt.gcf().autofmt_xdate()
    
        plt.xlabel('Time',size=20) 
        plt.ylabel('融资金额',size=20,fontproperties=myfont)
        CodeName = str(stockId) + rzrq.securityAbbr[0]
        plt.title(CodeName,size=20,fontproperties=myfont)
        
        plt.show()
    def button_set(self):
        
        global StockDate
        StockDate['卖盘']={}
        StockDate['买盘']={}
        #stockId=self.ceshiCnt.get()
        codeid = self.ceshiCnt.get()
        stockId = self.searchStockDictCode(codeid)
        #dateT = self.DateTime.get()
        #codeId = self.ceshiCnt.get()
        #print(codeId)
        #tick的数据，并非按照时间来的
        
        dataa=ts.get_hist_data(stockId)
        DayCount = self.DayCnt.get()
    
        DayCnt=int(DayCount)
        #print('DayCntXX is %d' %DayCntXX)
        #Message_Print('请等待...\n')
        self.value_testResult.set('请等待...')
    
        CountXX=0
        CountYY= 0
        Count_M = [0]*DayCnt
        Count_MM = [0]*DayCnt
        StockInVolumn=[0]*DayCnt
        StockInVolumn1=[0]*DayCnt
        for i in range(DayCnt):
            countX = 0
            countY = 0
            
            print('i%d' %i)
            #dataT=dataa.index[i]
            #StockData = ts.get_tick_data(stockId,dataa.index[i])
            pathCode= pathRoute + stockId + '-'+dataa.index[i]+'.cvs'
            try:
                StockData = pd.read_csv(pathCode)
            except IOError as e:
                print(e)
            else:
            #StockData = pd.read_cvs('')
                for index in StockData.index:
                    #index = StockData.index.max()-indexx
                    if StockData['type'][index] == '卖盘':
                        countX = countX + StockData['amount'][index]
                        #CountXX= CountXX + StockData['amount'][index]
                        #Count_M[i] = countX
                    #StockInVolumn[i]=-countX 
                    elif StockData['type'][index] == '买盘':
                        countY = countY + StockData['amount'][index]
                        #CountYY= CountYY + StockData['amount'][index]
                        #Count_MM[i] = countY
                    #StockInVolumn[i]=countY
                Count_M[i] = countX
                Count_MM[i] = countY
            
                #StockDate['卖盘'][dataa.index[i]] = countX
                #StockDate['买盘'][dataa.index[i]] = countY
                print('日期：%s,股票代码%s'% (dataa.index[i],stockId))
                print('卖盘金额总量是：%d' %countX)
                print('买盘金额总量是：%d' %countY)
            '''    
                StockInVolumn[i]=countY-countX
                StockInVolumn1[i]=CountYY-CountXX
            '''                                               
            #StockInVolumn[i]=countY
                
                #i=i+1
        i=0
        Count_M.reverse()
        Count_MM.reverse()
        for i in range(DayCnt):
            if i==0:
                StockInVolumn[i]= Count_MM[i]-Count_M[i]
                StockInVolumn1[i]=StockInVolumn[i]
            else:
                StockInVolumn[i]= Count_MM[i]-Count_M[i]
                StockInVolumn1[i]= StockInVolumn1[i-1]+ StockInVolumn[i]
        #i=i-1
        #dataT=dataa.index[0]
        #Message_Print('日期：%s,'%dateT)
        Message_Print('共计%d天,' %(i+1))
        Message_Print('股票代码%s' %stockId)
        Message_Print('资金流入%d \n' %StockInVolumn1[i])
        '''
        if StockInVolumn1< 0:
            
            Message_Print('日期：%s,'%dateT)
            Message_Print('共计%d天,' %i)
            Message_Print('股票代码%s' %stockId)
            Message_Print('资金流出%d \n' %StockInVolumn1[i])
        else:
            #xxx=zzz-yyy
            Message_Print('日期：%s,'%dateT)
            Message_Print('共计%d天,' %i)
            Message_Print('股票代码%s' %stockId)
            Message_Print('资金流入%d \n' %StockInVolumn1[i])
        '''
        
        '''
        self.DateTime.set(dataa.index[0])
        xxx=0
        yyy=0
        zzz =0
        x=0
        stockId=self.ceshiCnt.get()
        dateT = self.DateTime.get()
        for xxx in StockDate['卖盘']:
            yyy=yyy+StockDate['卖盘'][xxx]
        
        for xxx in StockDate['买盘']:
            zzz=zzz+StockDate['买盘'][xxx]
        x=len(StockDate['卖盘'])
        if yyy> zzz:
            xxx=yyy-zzz
            Message_Print('日期：%s,'%dateT)
            Message_Print('共计%d天,' %x)
            Message_Print('股票代码%s' %stockId)
            Message_Print('资金流出%d \n' %xxx)
        else:
            xxx=zzz-yyy
            Message_Print('日期：%s,'%dateT)
            Message_Print('共计%d天,' %x)
            Message_Print('股票代码%s' %stockId)
            Message_Print('资金流入%d \n' %xxx)
        '''
        plt.plot(StockInVolumn,'red',label="买卖量")
        plt.plot(StockInVolumn1,'blue',label="买卖积累量")
        #plt.plot(dataa['close'])
        plt.xlabel('Time',size=20) 
        plt.ylabel('Volumn',size=20)
        plt.grid(True, linestyle = "-.", color = "y", linewidth = "1")
        #codeId = 'Stock:'+stockId
        #plt.title(codeId,size=20)
        plt.legend(prop = myfont)
        plt.show()
        #df = ts.get_tick_data(stockId,)
        #HOST= '192.168.1.8' 
        #PORT = 9999  
        #print(HOST)
        #s = socket(AF_INET,SOCK_DGRAM)  
        #xx=s.bind((HOST,PORT))
        #print(xx)
    
    def button_report_basic(self):
        DayBegin=self.DayBegin.get()
        DayEnd =self.DayEnd.get()
        print('button_report_basic\n')
        #profit = ts.get_profit_data(Year,Jidu)
        #stockId=int(self.ceshiCnt.get())
        stockid=self.ceshiCnt.get()
        
        stock = self.searchStockDictCode(stockid)
        stockId = int(stock)
        
        
        pathCode=pathRoute  + '2017' +'_' +'3'+'_'+'盈利能力'+'.xlsx'
        ylnl=pd.read_excel(pathCode)
        i= 0
        j=0
        #print('%d\n' %stockId)
        #jbsj=pd.read_excel(pathCode)
        a = np.random.standard_normal((1, 11))
        xx = pd.DataFrame(a)
    
        xx.columns=['code', 'name', 'roe', 'net_profit_ratio', 'gross_profit_rate',
           'net_profits', 'eps', 'business_income', 'bips','year','quarter']
        #xx['year']='NA'
        #xx['quarter']='NA'
        for index in ylnl.index:
            
            if stockId == ylnl.code[i]:
                Message_Print('%s盈利能力2017.3：\n'%stockId)
                Message_Print('%s\n' %ylnl.ix[i])
                xx.ix[j]=ylnl.ix[i]
                xx.year[j]= '2017'
                xx.quarter[j]= '3'
                j=j+1
                break
                
            i =i+1
        print('button_report_basic  2 \n')
        Message_Print('button_report_basic  3 \n')
        pathCode=pathRoute  + '2016' +'_' +'4'+'_'+'盈利能力'+'.xlsx'
        ylnl=pd.read_excel(pathCode)
        for index in ylnl.index:
            if stockId == ylnl.code[index]:
                Message_Print('盈利能力2016.4：\n')
                Message_Print('%s\n' %ylnl.ix[index])
                xx.ix[j]=ylnl.ix[index]
                xx.year[j]='2016'
                xx.quarter[j]='4'
                j=j+1
                break
        pathCode=pathRoute  + '2015' +'_' +'4'+'_'+'盈利能力'+'.xlsx'
        ylnl=pd.read_excel(pathCode)
        for index in ylnl.index:
            if stockId == ylnl.code[index]:
                Message_Print('盈利能力2015.4：\n')
                Message_Print('%s\n' %ylnl.ix[index])
                xx.ix[j]=ylnl.ix[index]
                xx.year[j]='2015'
                xx.quarter[j]='4'
                j=j+1
                break
        pathCode=pathRoute  + '2014' +'_' +'4'+'_'+'盈利能力'+'.xlsx'
        ylnl=pd.read_excel(pathCode)
        for index in ylnl.index:
            if stockId == ylnl.code[index]:
                Message_Print('盈利能力2014.4：\n')
                Message_Print('%s\n' %ylnl.ix[index])
                xx.ix[j]=ylnl.ix[index]
                xx.year[j]='2014'
                xx.quarter[j]='4'
                j=j+1
                break
        pathCode=pathRoute  + '2013' +'_' +'4'+'_'+'盈利能力'+'.xlsx'
        ylnl=pd.read_excel(pathCode)
        for index in ylnl.index:
            if stockId == ylnl.code[index]:
                Message_Print('盈利能力2013.4：\n')
                Message_Print('%s\n' %ylnl.ix[index])
                xx.ix[j]=ylnl.ix[index]
                xx.year[j]='2013'
                xx.quarter[j]='4'
                j=j+1
                break
        pathCode=pathRoute  + '2012' +'_' +'4'+'_'+'盈利能力'+'.xlsx'
        ylnl=pd.read_excel(pathCode)
        for index in ylnl.index:
            if stockId == ylnl.code[index]:
                Message_Print('盈利能力2012.4：\n')
                Message_Print('%s\n' %ylnl.ix[index])
                xx.ix[j]=ylnl.ix[index]
                xx.year[j]='2012'
                xx.quarter[j]='4'
                j=j+1
                break
        if xx.name[0][0]=='*':
            pathCode=pathRoute  +str(xx.code[0]) +'盈利能力'+'.xlsx'
        else:
            pathCode=pathRoute  +xx.name[0] +'盈利能力'+'.xlsx'
        #xx.join(pd.DataFrame(['2017_3','2016_4','2015_4','2014_4','2013_4'],index=['0','1','2','3','4'],columns=['date',]))
        #xx['date']=['2017_3','2016_4','2015_4','2014_4','2013_4','2012_4']
        xx.to_excel(pathCode)
    
    
        a = np.random.standard_normal((1, 9))
        xx = pd.DataFrame(a)
    
        xx.columns=['code', 'name', 'cf_sales', 'rateofreturn', 'cf_nm', 'cf_liabilities',
           'cashflowratio','year','quarter']
        j=0
        #xx['date']='NA'
        pathCode=pathRoute  + '2017' +'_' +'3'+'_'+'现金流量'+'.xlsx'
        ylnl=pd.read_excel(pathCode)
        for index in ylnl.index:
            if stockId == ylnl.code[index]:
                Message_Print('现金流量2017.3：\n')
                Message_Print('%s\n' %ylnl.ix[index])
                xx.ix[j]=ylnl.ix[index]
                xx.year[j]='2017'
                xx.quarter[j]='3'
                j=j+1
                break
        pathCode=pathRoute  + '2016' +'_' +'4'+'_'+'现金流量'+'.xlsx'
        ylnl=pd.read_excel(pathCode)
        for index in ylnl.index:
            if stockId == ylnl.code[index]:
                Message_Print('现金流量2016.4：\n')
                Message_Print('%s\n' %ylnl.ix[index])
                xx.ix[j]=ylnl.ix[index]
                xx.year[j]='2016'
                xx.quarter[j]='4'
                j=j+1
                break
    
        pathCode=pathRoute  + '2015' +'_' +'4'+'_'+'现金流量'+'.xlsx'
        ylnl=pd.read_excel(pathCode)
        for index in ylnl.index:
            if stockId == ylnl.code[index]:
                Message_Print('现金流量2015.4：\n')
                Message_Print('%s\n' %ylnl.ix[index])
                xx.ix[j]=ylnl.ix[index]
                xx.year[j]='2015'
                xx.quarter[j]='4'
                j=j+1
                break
        pathCode=pathRoute  + '2014' +'_' +'4'+'_'+'现金流量'+'.xlsx'
        ylnl=pd.read_excel(pathCode)
        for index in ylnl.index:
            if stockId == ylnl.code[index]:
                Message_Print('现金流量2014.4：\n')
                Message_Print('%s\n' %ylnl.ix[index])
                xx.ix[j]=ylnl.ix[index]
                xx.year[j]='2014'
                xx.quarter[j]='4'
                j=j+1
                break
        pathCode=pathRoute  + '2013' +'_' +'3'+'_'+'现金流量'+'.xlsx'
        ylnl=pd.read_excel(pathCode)
        for index in ylnl.index:
            if stockId == ylnl.code[index]:
                Message_Print('现金流量2013.4：\n')
                Message_Print('%s\n' %ylnl.ix[index])
                xx.ix[j]=ylnl.ix[index]
                xx.year[j]='2013'
                xx.quarter[j]='4'
                j=j+1
                break
        pathCode=pathRoute  + '2012' +'_' +'4'+'_'+'现金流量'+'.xlsx'
        ylnl=pd.read_excel(pathCode)
        for index in ylnl.index:
            if stockId == ylnl.code[index]:
                Message_Print('现金流量2012.4：\n')
                Message_Print('%s\n' %ylnl.ix[index])
                xx.ix[j]=ylnl.ix[index]
                xx.year[j]='2012'
                xx.quarter[j]='4'
                j=j+1
                break
        #xx['date']=['2017_3','2016_4','2015_4','2014_4','2013_4','2012_4']
        

        if xx.name[0][0]=='*':
            pathCode=pathRoute  +str(xx.code[0]) +'现金流量'+'.xlsx'
        else:
            pathCode=pathRoute  +xx.name[0] +'现金流量'+'.xlsx'
        xx.to_excel(pathCode)
    
        j=0
        
        a = np.random.standard_normal((1, 13))
        xx = pd.DataFrame(a)
        xx.columns = ['code', 'name', 'eps', 'eps_yoy', 'bvps', 'roe', 'epcf', 'net_profits',
           'profits_yoy', 'distrib', 'report_date','year','quarter']
        #xx['date']='NA'
        pathCode=pathRoute  + '2017' +'_' + '3' +'_'+'业绩报告'+'.xlsx'
        ylnl=pd.read_excel(pathCode)
        for index in ylnl.index:
            if stockId == ylnl.code[index]:
                Message_Print('业绩报告2017.3：\n')
                Message_Print('%s\n' %ylnl.ix[index])
                xx.ix[j]=ylnl.ix[index]
                xx.year[j]='2017'
                xx.quarter[j]='3'
                j=j+1
                break
        pathCode=pathRoute  + '2016' +'_' + '4' +'_'+'业绩报告'+'.xlsx'
        ylnl=pd.read_excel(pathCode)
        for index in ylnl.index:
            if stockId == ylnl.code[index]:
                Message_Print('业绩报告2016.4：\n')
                Message_Print('%s\n' %ylnl.ix[index])
                xx.ix[j]=ylnl.ix[index]
                xx.year[j]='2016'
                xx.quarter[j]='4'
                j=j+1
                break
        pathCode=pathRoute  + '2015' +'_' + '4' +'_'+'业绩报告'+'.xlsx'
        ylnl=pd.read_excel(pathCode)
        for index in ylnl.index:
            if stockId == ylnl.code[index]:
                Message_Print('业绩报告2015.4：\n')
                Message_Print('%s\n' %ylnl.ix[index])
                xx.ix[j]=ylnl.ix[index]
                xx.year[j]='2015'
                xx.quarter[j]='4'
                j=j+1
                break
        pathCode=pathRoute  + '2014' +'_' + '4' +'_'+'业绩报告'+'.xlsx'
        ylnl=pd.read_excel(pathCode)
        for index in ylnl.index:
            if stockId == ylnl.code[index]:
                Message_Print('业绩报告2014.4：\n')
                Message_Print('%s\n' %ylnl.ix[index])
                xx.ix[j]=ylnl.ix[index]
                xx.year[j]='2014'
                xx.quarter[j]='4'
                j=j+1
                break
        pathCode=pathRoute  + '2013' +'_' + '4' +'_'+'业绩报告'+'.xlsx'
        ylnl=pd.read_excel(pathCode)
        for index in ylnl.index:
            if stockId == ylnl.code[index]:
                Message_Print('业绩报告2013.4：\n')
                Message_Print('%s\n' %ylnl.ix[index])
                xx.ix[j]=ylnl.ix[index]
                xx.year[j]='2013'
                xx.quarter[j]='4'
                j=j+1
                break
        pathCode=pathRoute  + '2012' +'_' + '4' +'_'+'业绩报告'+'.xlsx'
        ylnl=pd.read_excel(pathCode)
        for index in ylnl.index:
            if stockId == ylnl.code[index]:
                Message_Print('业绩报告2012.4：\n')
                Message_Print('%s\n' %ylnl.ix[index])
                xx.ix[j]=ylnl.ix[index]
                xx.year[j]='2012'
                xx.quarter[j]='4'
                j=j+1
                break
        #xx['date']=['2017_3','2016_4','2015_4','2014_4','2013_4','2012_4']
        #pathCode=pathRoute  +xx.name[0] +'业绩报告'+'.xlsx'
        if xx.name[0][0]=='*':
            pathCode=pathRoute  +str(xx.code[0]) +'业绩报告'+'.xlsx'
        else:
            pathCode=pathRoute  +xx.name[0] +'业绩报告'+'.xlsx'
        xx.to_excel(pathCode)
        
        '''
        profit.to_excel(pathCode)
        Message_Print('盈利能力已存至%s \n,'%pathCode)
        
        yynl = ts.get_operation_data(Year,Jidu)
        pathCode=pathRoute  + self.Year.get() +'_' +self.Jidu.get() +'_'+'营运能力'+'.xlsx'
        profit.to_excel(pathCode)
        Message_Print('营运能力已存至%s \n,'%pathCode)
    
        cznl = ts.get_growth_data(Year,Jidu)
        pathCode=pathRoute  + self.Year.get() +'_' +self.Jidu.get() +'_'+'成长能力'+'.xlsx'
        yynl.to_excel(pathCode)
        Message_Print('成长能力已存至%s \n,'%pathCode)
    
        czhnl = ts.get_debtpaying_data(Year,Jidu)
        pathCode=pathRoute  + self.Year.get() +'_' +self.Jidu.get() +'_'+'偿债能力'+'.xlsx'
        czhnl.to_excel(pathCode)
        Message_Print('偿债能力已存至%s \n,'%pathCode)
        
        xjll = ts.get_cashflow_data(Year,Jidu)
        pathCode=pathRoute  + self.Year.get() +'_' +self.Jidu.get() +'_'+'现金流量'+'.xlsx'
        xjll.to_excel(pathCode)
        Message_Print('现金流量已存至%s \n,'%pathCode)
    
        yjbg = ts.get_report_data(Year,Jidu)
        pathCode=pathRoute  + self.Year.get() +'_' +self.Jidu.get() +'_'+'业绩报告'+'.xlsx'
        yjbg.to_excel(pathCode)
        Message_Print('业绩报告已存至%s \n,'%pathCode)
        '''
    def button_jigou(self):
        #机构成交明细
        pathXX = pathRouteXX + '机构数据/'
        mkdir(pathXX)
        xx=ts.inst_detail()
        date = xx.date[0]
        pathCode=pathXX + date +'机构成交明细'+'.xlsx'
        xx.to_excel(pathCode)
        
        xx = ts.inst_tops()
        
        pathCode=pathXX   + date +'机构席位追踪'+'.xlsx'
        xx.to_excel(pathCode)
    
        xx = ts.cap_tops()
        
        pathCode=pathXX   + date +'个股上榜统计'+'.xlsx'
        xx.to_excel(pathCode)
    
        xx = ts.broker_tops()
        
        pathCode=pathXX   + date +'营业部上榜统计'+'.xlsx'
        xx.to_excel(pathCode)
    
        Message_Print('%s机构相关数据已经提取存储 \n' %date)
    
        
    def button_K_write(self):
        #code=self.ceshiCnt.get()
        codeid = self.ceshiCnt.get()
        codeId = self.searchStockDictCode(codeid)
        code =(6-( len(str(codeId))))*'0' + str(codeId)
        #code = self.Listbox1.get(self.Listbox1.curselection())
        Period = self.K_P.get()
        DayBegin=self.DayBegin.get()
        DayEnd =self.DayEnd.get()
        #df = ts.get_realtime_quotes(code)
        #CodeName = 
        CodeName = code + self.searchStockDictName(code)
        
    
        if Period == '5' or Period == '15'or Period == '30'or Period == '60':
            #stock_codes = ts.get_hist_data(code,ktype=Period)
            stockInfo = ts.get_k_data(code,ktype=Period,start=DayBegin,end = DayEnd)
            stockInfo['date'] = pd.to_datetime(stockInfo['date'])
            stockInfo.set_index("date", inplace=True)
            stockInfo[['close']].plot()
            plt.grid(True)
            plt.show()
            
    
        elif Period == 'day':
            stock_codes = ts.get_k_data(code,start=DayBegin,end = DayEnd)  #get_hist_data
            '''
            xx = computeM(stock_codes,5)
            yy = computeM(stock_codes,10)
            zz = computeM(stock_codes,20)
            stock_codes['ma5']= Series(xx)
            stock_codes['ma10']= Series(yy)
            stock_codes['ma20']= Series(zz)
            '''
            stock_codes['ma5'] = stock_codes['close'].rolling(window=5,center=False).mean()
            stock_codes['ma10'] = stock_codes['close'].rolling(window=10,center=False).mean()
            stock_codes['ma20'] = stock_codes['close'].rolling(window=20,center=False).mean()
            

            stock_codes['date'] = pd.to_datetime(stock_codes['date'])

            stock_codes.set_index('date', inplace=True)

            Sunxb_candlestick_ohlc(stock_codes,CodeName,'day')

            
        elif Period == 'W':
            stock_codes = ts.get_k_data(code,start=DayBegin,end = DayEnd)  #get_hist_data
            xx = computeM(stock_codes,5)
            yy = computeM(stock_codes,10)
            zz = computeM(stock_codes,20)
            stock_codes['ma5']= Series(xx)
            stock_codes['ma10']= Series(yy)
            stock_codes['ma20']= Series(zz)


            #guojin = ts.get_k_data('002373',str(start),str(end))
            stock_codes['date'] = pd.to_datetime(stock_codes['date'])

            stock_codes.set_index('date', inplace=True)

            Sunxb_candlestick_ohlc(stock_codes,CodeName,'week')
        elif Period == 'M':
            stock_codes = ts.get_k_data(code,start=DayBegin,end = DayEnd)  #get_hist_data
            xx = computeM(stock_codes,5)
            yy = computeM(stock_codes,10)
            zz = computeM(stock_codes,20)
            stock_codes['ma5']= Series(xx)
            stock_codes['ma10']= Series(yy)
            stock_codes['ma20']= Series(zz)


            #guojin = ts.get_k_data('002373',str(start),str(end))
            stock_codes['date'] = pd.to_datetime(stock_codes['date'])

            stock_codes.set_index('date', inplace=True)

            Sunxb_candlestick_ohlc(stock_codes,CodeName,'month')
        
        
    def Plot_k_1(event):
        print('sunxb')
        
    def Plot_k(self,event):
        #code=self.ceshiCnt.get()
        codeid = self.Listbox1.get(self.Listbox1.curselection())
        #codeid = self.ceshiCnt.get()
        codeId = self.searchStockDictCode(codeid)
        codeName = self.searchStockDictName(codeId)
        x=len(str(codeId))
        code=(6-x)*'0'+str(codeId)
        self.ceshiCnt.set(codeName)
        if self.Kbutton['text']=='K线':
            Period = 'day'
        elif self.Kbutton['text']=='实时':
            Period = '实时'
        DayBegin=self.DayBegin.get()
        DayEnd =self.DayEnd.get()
        #df = ts.get_realtime_quotes(code)
        #CodeName = code + df['name'][0]
        CodeName = code + self.searchStockDictName(code)
    
        if Period == '实时':
            stock_codes = ts.get_today_ticks(code)
            len(stock_codes)
            plt.plot(stock_codes['price'])
            plt.show()

    
        elif Period == 'day':
            '''
            stock_codes = ts.get_k_data(code,start=DayBegin,end = DayEnd)  #get_hist_data
            xx = computeM(stock_codes,5)
            yy = computeM(stock_codes,10)
            zz = computeM(stock_codes,20)
            stock_codes['ma5']= Series(xx)
            stock_codes['ma10']= Series(yy)
            stock_codes['ma20']= Series(zz)

            stock_codes['date'] = pd.to_datetime(stock_codes['date'])

            stock_codes.set_index('date', inplace=True)

            Sunxb_candlestick_ohlc(stock_codes,CodeName,'day','ma20')
            '''
            SunxbPlotCandle(code,DayBegin,DayEnd)
            plt.title(code + codeName,size=20,fontproperties=myfont)
            plt.show()
            
            
        elif Period == 'W':
            stock_codes = ts.get_k_data(code,start=DayBegin,end = DayEnd)  #get_hist_data
            xx = computeM(stock_codes,5)
            yy = computeM(stock_codes,10)
            zz = computeM(stock_codes,20)
            stock_codes['ma5']= Series(xx)
            stock_codes['ma10']= Series(yy)
            stock_codes['ma20']= Series(zz)


            #guojin = ts.get_k_data('002373',str(start),str(end))
            stock_codes['date'] = pd.to_datetime(stock_codes['date'])

            stock_codes.set_index('date', inplace=True)

            Sunxb_candlestick_ohlc(stock_codes,CodeName,'week')
        elif Period == 'M':
            stock_codes = ts.get_k_data(code,start=DayBegin,end = DayEnd)  #get_hist_data
            xx = computeM(stock_codes,5)
            yy = computeM(stock_codes,10)
            zz = computeM(stock_codes,20)
            stock_codes['ma5']= Series(xx)
            stock_codes['ma10']= Series(yy)
            stock_codes['ma20']= Series(zz)


            #guojin = ts.get_k_data('002373',str(start),str(end))
            stock_codes['date'] = pd.to_datetime(stock_codes['date'])

            stock_codes.set_index('date', inplace=True)

            Sunxb_candlestick_ohlc(stock_codes,CodeName,'month')
        '''
        plt.grid(True, linestyle = "-.", color = "y", linewidth = "1")
        Time_P = 'Time' + Period 
        plt.xlabel(Time_P,size=20) 
        plt.ylabel('Price',size=20)
        #autodates = AutoDateLocator()                # 时间间隔自动选取 
    #autodates.intervald[DAILY]=[5] 
           #autodates.intervald[0] =[5] 
        #plt.gca().xaxis.set_major_locator(autodates)
        #plt.gcf().autofmt_xdate()
        plt.title(CodeName,size=20,fontproperties=myfont)
        #plt.gcf().autofmt_xdate()
    
    
        plt.show()
        '''
    def Print_result(self):
        '''
        tMsg.showinfo('提示','搜索5倍股')
        codename = ts.get_stock_basics()
        DayBegin=self.DayBegin.get()
        DayEnd =self.DayEnd.get()
        i=0
        j=0
        pathCode=pathRoute  +self.ceshiCnt.get() +'业绩报告'+'.xlsx'
    
        #date = df.ix[codeId]['timeToMarket']
        for codeId in codename.index:
            
            dateSS = codename.ix[codeId]['timeToMarket']
            Year = int(dateSS/10000)
            if Year >2016:
                continue
            Year =Year+1
            Year = str(Year)
            startDay = Year + '-02-01'
            endDay = Year + '-12-10'
            startDay1 = '2017' + '-01-01'
            endDay1 = '2018' + '-01-30'
            
            print('%s' %codeId)
            gj = ts.get_h_data(codeId,start = startDay,end=endDay)
            time.sleep(5)
            gj1 = ts.get_h_data(codeId,start = startDay1,end=endDay1)
            time.sleep(5)
            #pathCode1= pathxx  +codeId +'.xlsx'
            
                #length = len(gj.index)
            gj_new = gj1.close[0]
            gj_old = gj.close[0]
                
            if gj_new > gj_old*4:
                Message_Print('4倍股票%s\n,'%codeId)
                #j=j+1
            if gj_new > gj_old*10:
                Message_Print('10倍股票%s\n,'%codeId)
                #j=j+1
            
            i=i+1
            if i>3475:
                break
        tMsg.showinfo('提示','搜索5倍股完毕')
        
        
    
        '''
        code=self.ceshiCnt.get()
        DayBegin=self.DayBegin.get()
        DayEnd =self.DayEnd.get()
        stock_codes = ts.get_hist_data(code,start=DayBegin,end = DayEnd)#,end ='2017-07-19'
        pathCode= pathRoute + code +'.cvs'
        stock_codes.to_csv(pathCode)
        for data_time in stock_codes.index:
            print('日期%s' %data_time)
            df = ts.get_tick_data(code,data_time)
            pathCode=  pathRoute + code + '-'+data_time+'.cvs'
    
        #df = ts.get_tick_data(code,TICKS_DATA_DATE)
            df.to_csv(pathCode)
            time.sleep(3)
        self.value_testResult.set('xxxx')
        
        
    
    def check_command(self):
        #global Check_button_value
        print(self.Check_button_value.get())
    
        codeId = self.ceshiCnt.get()
        
        print(codeId)
        data = ts.get_hist_data(codeId,start='2016-06-23',end='2018-01-04')
        print(data)
    
        data_time  = data.index 
        data_time_translation = [datetime.strptime(d, '%Y-%m-%d').date() for d in data_time] 
        data_close = data['ma5'].values 
    
    # 配置时间坐标轴 
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d')) # 显示时间坐标的格式 
    
        autodates = AutoDateLocator()                # 时间间隔自动选取 
    #autodates.intervald[DAILY]=[5] 
        autodates.intervald[0] =[1] 
        plt.gca().xaxis.set_major_locator(autodates)
    
    
        #plt.plot(data_time_translation,data['low'].values,lw=1.5,label="low",color='yellow') 
        #plt.plot(data_time_translation, data['ma10'].values,lw=3,label="ma10",color='blue') 
        #plt.plot(data_time_translation, data['ma5'].values,lw=3,label="ma5",color='g') 
        #plt.plot(data_time_translation, data['ma20'].values,lw=3,label="ma20",color='red')
        plt.plot(data_time_translation, data['turnover'].values,lw=3,label="turnover",color='black')
        plt.gcf().autofmt_xdate() 
    
    # 绘图细节 
        plt.grid(True) 
        plt.axis("tight") 
        plt.xlabel('Time',size=20) 
        plt.ylabel('Price',size=20) 
        plt.title(codeId,size=20) 
    # 添加图例 
        plt.legend(loc=0) 
    
        plt.show()
    
    
    def button_get_profit(self):
        tMsg.showinfo('提示','数据下载中，请等待')
    
        Year = int(self.Year.get())
        Jidu = int(self.Jidu.get())

        yynl = ts.get_operation_data(Year,Jidu)
        pathCode=pathRoute  + self.Year.get() +'_' +self.Jidu.get() +'_'+'营运能力'+'.xlsx'
        yynl.to_excel(pathCode)
        Message_Print('营运能力已存至%s \n,'%pathCode)
        
        
        jbsj = ts.get_stock_basics()
        pathCode=pathRoute  + '基本数据'+'.xlsx'
        jbsj.to_excel(pathCode)
        Message_Print('基本数据已存至%s \n,'%pathCode)
        '''
        '''
        profit = ts.get_profit_data(Year,Jidu)
        pathCode=pathRoute  + self.Year.get() +'_' +self.Jidu.get() +'_'+'盈利能力'+'.xlsx'
        profit.to_excel(pathCode)
        Message_Print('盈利能力已存至%s \n,'%pathCode)
        
        
    
        cznl = ts.get_growth_data(Year,Jidu)
        pathCode=pathRoute  + self.Year.get() +'_' +self.Jidu.get() +'_'+'成长能力'+'.xlsx'
        cznl.to_excel(pathCode)
        Message_Print('成长能力已存至%s \n,'%pathCode)
        
    
        czhnl = ts.get_debtpaying_data(Year,Jidu)
        pathCode=pathRoute  + self.Year.get() +'_' +self.Jidu.get() +'_'+'偿债能力'+'.xlsx'
        czhnl.to_excel(pathCode)
        Message_Print('偿债能力已存至%s \n,'%pathCode)
        
        xjll = ts.get_cashflow_data(Year,Jidu)
        pathCode=pathRoute  + self.Year.get() +'_' +self.Jidu.get() +'_'+'现金流量'+'.xlsx'
        xjll.to_excel(pathCode)
        Message_Print('现金流量已存至%s \n,'%pathCode)
        
        yjbg = ts.get_report_data(Year,Jidu)
        pathCode=pathRoute  + self.Year.get() +'_' +self.Jidu.get() +'_'+'业绩报告'+'.xlsx'
        yjbg.to_excel(pathCode)
        Message_Print('业绩报告已存至%s \n,'%pathCode)
        
        
    def button_get_stock_basic(self):
        #pathCode=pathRoute  + self.Year.get() +'_' +self.Jidu.get() +'_'+'盈利能力'+'.xlsx'
        #ylnl=pd.read_excel(pathCode)
        #ylnl
    
    
        jbsj = ts.get_stock_basics()
        pathCode=pathRoute  + '基本数据'+'.xlsx'
        jbsj.to_excel(pathCode)
        Message_Print('基本数据已存至%s \n,'%pathCode)
        
    def button_search_stock(self):
        
        i=0
    
        FileName = self.search_file.get()
        pathCode=pathRoute  + FileName+'.xlsx'
        jbsj=pd.read_excel(pathCode)
        a = np.random.standard_normal((1, 23))
        xx = pd.DataFrame(a)
        yy = pd.DataFrame(a)
        zz = pd.DataFrame(a)
        xx.columns=['code', 'name', 'industry', 'area', 'pe', 'outstanding', 'totals',
           'totalAssets', 'liquidAssets', 'fixedAssets', 'reserved',
           'reservedPerShare', 'esp', 'bvps', 'pb', 'timeToMarket', 'undp',
           'perundp', 'rev', 'profit', 'gpr', 'npr', 'holders']
        yy.columns=['code', 'name', 'industry', 'area', 'pe', 'outstanding', 'totals',
           'totalAssets', 'liquidAssets', 'fixedAssets', 'reserved',
           'reservedPerShare', 'esp', 'bvps', 'pb', 'timeToMarket', 'undp',
           'perundp', 'rev', 'profit', 'gpr', 'npr', 'holders']
        zz.columns=['code', 'name', 'industry', 'area', 'pe', 'outstanding', 'totals',
           'totalAssets', 'liquidAssets', 'fixedAssets', 'reserved',
           'reservedPerShare', 'esp', 'bvps', 'pb', 'timeToMarket', 'undp',
           'perundp', 'rev', 'profit', 'gpr', 'npr', 'holders']
        
        '''
        for index in jbsj.index:
            if jbsj.esp[index] > 2:
               Message_Print('%s每股收益%f,静利润率%f\n' %(jbsj.name[index],jbsj.esp[index],jbsj.npr[index]))
               Message_Print('%s' %jbsj.ix[index])
               xx.ix[i]=jbsj.ix[index]
               i=i+1
    
        
        pathCode=pathRoute  + '选定股票基本数据'+'.xlsx'
        xx.to_excel(pathCode)
        Message_Print('共%d只股票搜索保存完毕，%s！' %(i,pathCode))
        '''
        
        
        i=0
        j=0
        k=0
        Flag_esp = self.stock_esp_flag.get()
        Flag_pb = self.stock_pb_flag.get()
        Flag_pe = self.stock_pe_flag.get()
        Store_file = pathRoute + self.store_file.get()+ '.xlsx'
    
        
        print('stock_esp_flag is %d \n' %Flag_esp)
        #for index in jbsj.index:
        if Flag_esp == 1 :
            stock_esp = float(self.stock_sy.get())
            stock_esp_max =float( self.stock_sy_d.get())
            for index in jbsj.index:
                if stock_esp_max > stock_esp:   #选取大于大值，小于小值的
                    if jbsj.esp[index] > stock_esp_max or jbsj.esp[index] < stock_esp:
                        xx.ix[i]=jbsj.ix[index]
                        i=i+1
    
                    
                else: #选取大于小值，小于大值值
                    if jbsj.esp[index] > stock_esp_max and jbsj.esp[index] < stock_esp:
                        xx.ix[i]=jbsj.ix[index]
                        i=i+1
                
            if Flag_pb == 1 :
                stock_pb = float(self.stock_sjl.get())
                stock_pb_max =float( self.stock_sjl_d.get())
                for pb_index in xx.index:
                    if stock_pb_max > stock_pb:   #选取大于大值，小于小值的
                        if xx.pb[pb_index] > stock_pb_max or xx.pb[pb_index] < stock_pb:
                            yy.ix[j]=xx.ix[pb_index]
                            j=j+1
    
                    
                    else: #选取大于小值，小于大值值
                        if xx.pb[pb_index] > stock_pb_max and xx.pb[pb_index] < stock_pb:
                            yy.ix[j]=xx.ix[pb_index]
                            j=j+1
                if Flag_pe ==1:
                    stock_pe =float( self.stock_syl.get())
                    stock_pe_max =float( self.stock_syl_d.get())
                    for pe_index in yy.index:
                        if stock_pe_max > stock_pe:   #选取大于大值，小于小值的
                            if yy.pe[pe_index] > stock_pe_max or yy.pe[pe_index] < stock_pe:
                                zz.ix[k]=yy.ix[pe_index]
                                k=k+1
    
                    
                        else: #选取大于小值，小于大值值
                            if yy.pe[pe_index] > stock_pe_max and yy.pe[pe_index] < stock_pe:
                                zz.ix[k]=yy.ix[pe_index]
                                k=k+1
                    zz.to_excel(Store_file)
                    Message_Print('共%d只股票搜索完毕！' %k)
                else:
                    yy.to_excel(Store_file)
                    Message_Print('共%d只股票搜索完毕！' %j)
                
                
            else:
                xx.to_excel(Store_file)
                Message_Print('共%d只股票搜索完毕！' %i)
                            
        else:
            if Flag_pb == 1 :
                stock_pb = float(self.stock_sjl.get())
                stock_pb_max = float(self.stock_sjl_d.get())
                for index in jbsj.index:
                    if stock_pb_max > stock_pb:   #选取大于大值，小于小值的
                        if jbsj.pb[index] > stock_pb_max or jbsj.pb[index] < stock_pb:
                            xx.ix[i]=jbsj.ix[index]
                            i=i+1
    
                    
                    else: #选取大于小值，小于大值值
                        if jbsj.pb[index] > stock_pb_max and jbsj.pb[index] < stock_pb:
                            xx.ix[i]=jbsj.ix[index]
                            i=i+1
                if Flag_pe ==1:
                    stock_pe = float(self.stock_syl.get())
                    stock_pe_max = float(self.stock_syl_d.get())
                    for pe_index in xx.index:
                        if stock_pe_max > stock_pe:   #选取大于大值，小于小值的
                            if xx.pe[pe_index] > stock_pe_max or xx.pe[pe_index] < stock_pe:
                                yy.ix[k]=xx.ix[pe_index]
                                k=k+1
    
                    
                        else: #选取大于小值，小于大值值
                            if xx.pe[pe_index] > stock_pe_max and xx.pe[pe_index] < stock_pe:
                                yy.ix[k]=xx.ix[pe_index]
                                k=k+1
                    yy.to_excel(Store_file)
                    Message_Print('共%d只股票搜索完毕！' %k)
                else:
                    xx.to_excel(Store_file)
                    Message_Print('共%d只股票搜索完毕！' %i)
            else:
                if Flag_pe ==1:
                    stock_pe =float( self.stock_syl.get())
                    stock_pe_max =float( self.stock_syl_d.get())
                    Message_Print('sunxiaobo 1 \n')
                    for pe_index in jbsj.index:
                        if stock_pe_max > stock_pe:   #选取大于大值，小于小值的
                            if jbsj.pe[pe_index] > stock_pe_max or jbsj.pe[pe_index] < stock_pe:
                                xx.ix[k]=jbsj.ix[pe_index]
                                k=k+1
    
                    
                        else: #选取大于小值，小于大值值
                            if jbsj.pe[pe_index] > stock_pe_max and jbsj.pe[pe_index] < stock_pe:
                                xx.ix[k]=jbsj.ix[pe_index]
                                k=k+1
    
                    Message_Print('sunxiaobo 2 \n')
                    xx.to_excel(Store_file)
                    Message_Print('共%d只股票搜索完毕！' %k)
                else:
                    #yy.to_excel(Store_file),meiyou
                    Message_Print('搜索完毕！没有符合股票')
                    
        '''
        for index in jbsj.index:
            if Flag_pb == 1:
                stock_pb = self.stock_sjl.get()
                stock_pb_max = self.stock_sjl_d.get()
                if stock_pb_max > stock_pb:   #选取大于大值，小于小值的
                    if jbsj.esp[index] > stock_esp_max or jbsj.esp[index] < stock_esp
                        xx.ix[i]=jbsj.ix[index]
                        i=i+1
    
                    
                else: #选取大于小值，小于大值值
                    if jbsj.esp[index] < stock_esp_max and jbsj.esp[index] < stock_esp
                        xx.ix[i]=jbsj.ix[index]
                        i=i+1
    
                        
                if xx.npr[index] > 25:
                    Message_Print('%s每股收益%f,静利润率%f \n' %(xx.name[index],xx.esp[index],xx.npr[index]))
                    i=i+1
        '''
        #Message_Print('共%d只股票搜索完毕！' %i)
        
        
    def profit_search_stock(self):
        profit_store_file = self.profit_store_file.get()
        profit_num = self.profit_num.get()
        profit_min = float(self.profit_value_min.get())
        profit_max = float(self.profit_value_max.get())
        a = np.random.standard_normal((1, 9))
        
        xx = pd.DataFrame(a)
        xx.columns=['code', 'name', 'roe', 'net_profit_ratio', 'gross_profit_rate',
           'net_profits', 'eps', 'business_income', 'bips']
    
        #search_file = pathRoute + '2017_3_'+'盈利能力'+ '.xlsx'
        #search_file = pathRoute +'roe选股'+ '.xlsx'
    
        FileName = self.search_profit_file.get()
        #pathCode=pathRoute  + FileName+'.xlsx'
        
        search_file = pathRoute +FileName+ '.xlsx'
        store_file = pathRoute + profit_store_file+ '.xlsx'
        k=0
        ylnl=pd.read_excel(search_file)
        if profit_num == '1':
            profit_para='roe'
    
            for index in ylnl.index:
                if profit_max > profit_min:  #选取大于大值，或者小于小值的
                
                    if ylnl.roe[index] > profit_max or ylnl.roe[index] < profit_min:
                        xx.ix[k]=jbsj.ix[pe_index]
                        k=k+1
    
                    
                else: #选取大于小值，小于大值值
                    if ylnl.roe[index] > profit_max and ylnl.roe[index] < profit_min:
                        xx.ix[k]=ylnl.ix[index]
                        k=k+1
            xx.to_excel(store_file)
        elif profit_num == '2':
            profit_para='net_profit_ratio'
    
            for index in ylnl.index:
                if profit_max > profit_min:  #选取大于大值，或者小于小值的
                
                    if ylnl.net_profit_ratio[index] > profit_max or ylnl.net_profit_ratio[index] < profit_min:
                        xx.ix[k]=ylnl.ix[pe_index]
                        k=k+1
    
                    
                else: #选取大于小值，小于大值值
                    if ylnl.net_profit_ratio[index] > profit_max and ylnl.net_profit_ratio[index] < profit_min:
                        xx.ix[k]=ylnl.ix[index]
                        k=k+1
            xx.to_excel(store_file)
        elif profit_num == '3':
            profit_para='gross_profit_rate'
    
            for index in ylnl.index:
                if profit_max > profit_min:  #选取大于大值，或者小于小值的
                
                    if ylnl.gross_profit_rate[index] > profit_max or ylnl.gross_profit_rate[index] < profit_min:
                        xx.ix[k]=ylnl.ix[pe_index]
                        k=k+1
    
                    
                else: #选取大于小值，小于大值值
                    if ylnl.gross_profit_rate[index] > profit_max and ylnl.gross_profit_rate[index] < profit_min:
                        xx.ix[k]=ylnl.ix[index]
                        k=k+1
            xx.to_excel(store_file)
        elif profit_num == '4':
            profit_para='net_profits'
    
            for index in ylnl.index:
                if profit_max > profit_min:  #选取大于大值，或者小于小值的
                
                    if ylnl.net_profits[index] > profit_max or ylnl.net_profits[index] < profit_min:
                        xx.ix[k]=ylnl.ix[pe_index]
                        k=k+1
    
                    
                else: #选取大于小值，小于大值值
                    if ylnl.net_profits[index] > profit_max and ylnl.net_profits[index] < profit_min:
                        xx.ix[k]=ylnl.ix[index]
                        k=k+1
            
            xx.to_excel(store_file)
        elif profit_num == '5':
            profit_para='eps'
    
            for index in ylnl.index:
                if profit_max > profit_min:  #选取大于大值，或者小于小值的
                
                    if ylnl.eps[index] > profit_max or ylnl.eps[index] < profit_min:
                        xx.ix[k]=ylnl.ix[pe_index]
                        k=k+1
    
                    
                else: #选取大于小值，小于大值值
                    if ylnl.eps[index] > profit_max and ylnl.eps[index] < profit_min:
                        xx.ix[k]=ylnl.ix[index]
                        k=k+1
            xx.to_excel(store_file)
        elif profit_num == '6':
            profit_para='business_income'
    
            for index in ylnl.index:
                if profit_max > profit_min:  #选取大于大值，或者小于小值的
                
                    if ylnl.business_income[index] > profit_max or ylnl.business_income[index] < profit_min:
                        xx.ix[k]=ylnl.ix[pe_index]
                        k=k+1
    
                    
                else: #选取大于小值，小于大值值
                    if ylnl.business_income[index] > profit_max and ylnl.business_income[index] < profit_min:
                        xx.ix[k]=ylnl.ix[index]
                        k=k+1
            xx.to_excel(store_file)
        elif profit_num == '7':
            profit_para='bips'
    
            for index in ylnl.index:
                if profit_max > profit_min:  #选取大于大值，或者小于小值的
                
                    if ylnl.bips[index] > profit_max or ylnl.bips[index] < profit_min:
                        xx.ix[k]=ylnl.ix[pe_index]
                        k=k+1
    
                    
                else: #选取大于小值，小于大值值
                    if ylnl.bips[index] > profit_max and ylnl.bips[index] < profit_min:
                        xx.ix[k]=ylnl.ix[index]
                        k=k+1
            xx.to_excel(store_file)
        else:
            tMsg.showinfo('提示','请输入正确标号')
        tMsg.showinfo('提示','选股完毕')
    def cash_search_stock(self):
        profit_store_file = self.cash_store_file.get()
        profit_num = self.cash_num.get()
        profit_min = float(self.cash_value_min.get())
        profit_max = float(self.cash_value_max.get())
        a = np.random.standard_normal((1, 9))
        
        xx = pd.DataFrame(a)
        xx.columns=['code', 'name', 'cf_sales', 'rateofreturn', 'cf_nm', 'cf_liabilities',
           'cashflowratio','year','quarter']
    
        #search_file = pathRoute + '2017_3_'+'盈利能力'+ '.xlsx'
        #search_file = pathRoute +'roe选股'+ '.xlsx'
    
        FileName = self.search_cash_file.get()
        #pathCode=pathRoute  + FileName+'.xlsx'
        
        search_file = pathRoute +FileName+ '.xlsx'
        store_file = pathRoute + profit_store_file+ '.xlsx'
        k=0
        ylnl=pd.read_excel(search_file)
        if profit_num == '1':
            profit_para='cf_sales'
    
            for index in ylnl.index:
                if profit_max > profit_min:  #选取大于大值，或者小于小值的
                
                    if ylnl.cf_sales[index] > profit_max or ylnl.cf_sales[index] < profit_min:
                        xx.ix[k]=jbsj.ix[pe_index]
                        k=k+1
    
                    
                else: #选取大于小值，小于大值值
                    if ylnl.cf_sales[index] > profit_max and ylnl.cf_sales[index] < profit_min:
                        xx.ix[k]=ylnl.ix[index]
                        k=k+1
            xx.to_excel(store_file)
        elif profit_num == '2':
            profit_para='rateofreturn'
    
            for index in ylnl.index:
                if profit_max > profit_min:  #选取大于大值，或者小于小值的
                
                    if ylnl.rateofreturn[index] > profit_max or ylnl.rateofreturn[index] < profit_min:
                        xx.ix[k]=ylnl.ix[pe_index]
                        k=k+1
    
                    
                else: #选取大于小值，小于大值值
                    if ylnl.rateofreturn[index] > profit_max and ylnl.rateofreturn[index] < profit_min:
                        xx.ix[k]=ylnl.ix[index]
                        k=k+1
            xx.to_excel(store_file)
        elif profit_num == '3':
            profit_para='cf_nm'
    
            for index in ylnl.index:
                if profit_max > profit_min:  #选取大于大值，或者小于小值的
                
                    if ylnl.cf_nm[index] > profit_max or ylnl.cf_nm[index] < profit_min:
                        xx.ix[k]=ylnl.ix[pe_index]
                        k=k+1
    
                    
                else: #选取大于小值，小于大值值
                    if ylnl.cf_nm[index] > profit_max and ylnl.cf_nm[index] < profit_min:
                        xx.ix[k]=ylnl.ix[index]
                        k=k+1
            xx.to_excel(store_file)
        elif profit_num == '4':
            profit_para='cf_liabilities'
    
            for index in ylnl.index:
                if profit_max > profit_min:  #选取大于大值，或者小于小值的
                
                    if ylnl.cf_liabilities[index] > profit_max or ylnl.cf_liabilities[index] < profit_min:
                        xx.ix[k]=ylnl.ix[pe_index]
                        k=k+1
    
                    
                else: #选取大于小值，小于大值值
                    if ylnl.cf_liabilities[index] > profit_max and ylnl.cf_liabilities[index] < profit_min:
                        xx.ix[k]=ylnl.ix[index]
                        k=k+1
            
            xx.to_excel(store_file)
        elif profit_num == '5':
            profit_para='cashflowratio'
    
            for index in ylnl.index:
                if profit_max > profit_min:  #选取大于大值，或者小于小值的
                
                    if ylnl.cashflowratio[index] > profit_max or ylnl.cashflowratio[index] < profit_min:
                        xx.ix[k]=ylnl.ix[pe_index]
                        k=k+1
    
                    
                else: #选取大于小值，小于大值值
                    if ylnl.cashflowratio[index] > profit_max and ylnl.cashflowratio[index] < profit_min:
                        xx.ix[k]=ylnl.ix[index]
                        k=k+1
            xx.to_excel(store_file)
        
        else:
            tMsg.showinfo('提示','请输入正确标号')
        tMsg.showinfo('提示','选股完毕')
    def pay_search_stock(self):
        pay_store_file = self.pay_store_file.get()
    
        #profit_store_file = self.profit_store_file.get()
        profit_num = self.pay_num.get()
        profit_min = float(self.pay_value_min.get())
        profit_max = float(self.pay_value_max.get())
        a = np.random.standard_normal((1, 8))
        
        xx = pd.DataFrame(a)
        xx.columns=['code', 'name', 'currentratio', 'quickratio', 'cashratio', 'icratio',
           'sheqratio', 'adratio']
    
        #search_file = pathRoute + '2017_3_'+'盈利能力'+ '.xlsx'
        #search_file = pathRoute +'roe选股'+ '.xlsx'
    
        FileName = self.search_pay_file.get()
        #pathCode=pathRoute  + FileName+'.xlsx'
        
        search_file = pathRoute +FileName+ '.xlsx'
        store_file = pathRoute + pay_store_file+ '.xlsx'
        k=0
        ylnl=pd.read_excel(search_file)
        if profit_num == '1':
            profit_para='currentratio'
    
            for index in ylnl.index:
                if ylnl.currentratio[index]== '--':
                    continue
                if profit_max > profit_min:  #选取大于大值，或者小于小值的
                    
                
                    if float(ylnl.currentratio[index]) > profit_max or float(ylnl.currentratio[index]) < profit_min:
                        xx.ix[k]=jbsj.ix[pe_index]
                        k=k+1
    
                    
                else: #选取大于小值，小于大值值
                    
                    if float(ylnl.currentratio[index]) > profit_max and float(ylnl.currentratio[index]) < profit_min:
                        xx.ix[k]=ylnl.ix[index]
                        k=k+1
            xx.to_excel(store_file)
        elif profit_num == '2':
            profit_para='quickratio'
    
            for index in ylnl.index:
                if ylnl.quickratio[index]== '--':
                    continue
                if profit_max > profit_min:  #选取大于大值，或者小于小值的
                    
                
                    if ylnl.quickratio[index] > profit_max or ylnl.quickratio[index] < profit_min:
                        xx.ix[k]=ylnl.ix[pe_index]
                        k=k+1
    
                    
                else: #选取大于小值，小于大值值
                    if ylnl.quickratio[index] > profit_max and ylnl.quickratio[index] < profit_min:
                        xx.ix[k]=ylnl.ix[index]
                        k=k+1
            xx.to_excel(store_file)
        elif profit_num == '3':
            profit_para='cashratio'
    
            for index in ylnl.index:
                if ylnl.cashratio[index]== '--':
                    continue
                if profit_max > profit_min:  #选取大于大值，或者小于小值的
                
                    if ylnl.cashratio[index] > profit_max or ylnl.cashratio[index] < profit_min:
                        xx.ix[k]=ylnl.ix[pe_index]
                        k=k+1
    
                    
                else: #选取大于小值，小于大值值
                    if ylnl.cashratio[index] > profit_max and ylnl.cashratio[index] < profit_min:
                        xx.ix[k]=ylnl.ix[index]
                        k=k+1
            xx.to_excel(store_file)
        elif profit_num == '4':
            profit_para='icratio'
    
            for index in ylnl.index:
                if ylnl.icratio[index]== '--':
                    continue
                if profit_max > profit_min:  #选取大于大值，或者小于小值的
                
                    if ylnl.icratio[index] > profit_max or ylnl.icratio[index] < profit_min:
                        xx.ix[k]=ylnl.ix[pe_index]
                        k=k+1
    
                    
                else: #选取大于小值，小于大值值
                    if ylnl.icratio[index] > profit_max and ylnl.icratio[index] < profit_min:
                        xx.ix[k]=ylnl.ix[index]
                        k=k+1
            
            xx.to_excel(store_file)
        elif profit_num == '5':
            profit_para='sheqratio'
    
            for index in ylnl.index:
                if ylnl.sheqratio[index]== '--':
                    continue
                if profit_max > profit_min:  #选取大于大值，或者小于小值的
                
                    if ylnl.sheqratio[index] > profit_max or ylnl.sheqratio[index] < profit_min:
                        xx.ix[k]=ylnl.ix[pe_index]
                        k=k+1
    
                    
                else: #选取大于小值，小于大值值
                    if ylnl.sheqratio[index] > profit_max and ylnl.sheqratio[index] < profit_min:
                        xx.ix[k]=ylnl.ix[index]
                        k=k+1
            xx.to_excel(store_file)
        elif profit_num == '6':
            profit_para='adratio'
    
            for index in ylnl.index:
                if ylnl.adratio[index]== '--':
                    continue
                if profit_max > profit_min:  #选取大于大值，或者小于小值的
                
                    if ylnl.adratio[index] > profit_max or ylnl.adratio[index] < profit_min:
                        xx.ix[k]=ylnl.ix[pe_index]
                        k=k+1
    
                    
                else: #选取大于小值，小于大值值
                    if ylnl.adratio[index] > profit_max and ylnl.adratio[index] < profit_min:
                        xx.ix[k]=ylnl.ix[index]
                        k=k+1
            xx.to_excel(store_file)
    
        else:
            tMsg.showinfo('提示','请输入正确标号')
        tMsg.showinfo('提示','选股完毕')
        
    def outstanding_search_stock(self):
        outstanding_store_file = self.outstanding_store_file.get()
    
        #profit_store_file = self.profit_store_file.get()
        profit_num = self.outstanding_num.get()
        profit_min = float(self.outstanding_value_min.get())
        profit_max = float(self.outstanding_value_max.get())
        a = np.random.standard_normal((1, 11))
        
        xx = pd.DataFrame(a)
        xx.columns=['code', 'name', 'eps', 'eps_yoy', 'bvps', 'roe', 'epcf', 'net_profits',
       'profits_yoy', 'distrib', 'report_date']
    
        #search_file = pathRoute + '2017_3_'+'盈利能力'+ '.xlsx'
        #search_file = pathRoute +'roe选股'+ '.xlsx'
    
        FileName = self.search_outstanding_file.get()
        #pathCode=pathRoute  + FileName+'.xlsx'
        
        search_file = pathRoute +FileName+ '.xlsx'
        store_file = pathRoute + outstanding_store_file+ '.xlsx'
        k=0
        ylnl=pd.read_excel(search_file)
        if profit_num == '1':
            profit_para='eps'
    
            for index in ylnl.index:
                if ylnl.eps[index]== '--':
                    continue
                if profit_max > profit_min:  #选取大于大值，或者小于小值的
                    
                
                    if float(ylnl.eps[index]) > profit_max or float(ylnl.eps[index]) < profit_min:
                        xx.ix[k]=jbsj.ix[pe_index]
                        k=k+1
    
                    
                else: #选取大于小值，小于大值值
                    
                    if float(ylnl.eps[index]) > profit_max and float(ylnl.eps[index]) < profit_min:
                        xx.ix[k]=ylnl.ix[index]
                        k=k+1
            xx.to_excel(store_file)
        
        elif profit_num == '7':
            profit_para='profits_yoy'
    
            for index in ylnl.index:
                if ylnl.profits_yoy[index]== '--':
                    continue
                if profit_max > profit_min:  #选取大于大值，或者小于小值的
                    
                
                    if ylnl.profits_yoy[index] > profit_max or ylnl.profits_yoy[index] < profit_min:
                        xx.ix[k]=ylnl.ix[pe_index]
                        k=k+1
    
                    
                else: #选取大于小值，小于大值值
                    if ylnl.profits_yoy[index] > profit_max and ylnl.profits_yoy[index] < profit_min:
                        xx.ix[k]=ylnl.ix[index]
                        k=k+1
            xx.to_excel(store_file)
        elif profit_num == '2':
            profit_para='eps_yoy'
    
            for index in ylnl.index:
                if ylnl.eps_yoy[index]== '--':
                    continue
                if profit_max > profit_min:  #选取大于大值，或者小于小值的
                    
                
                    if ylnl.eps_yoy[index] > profit_max or ylnl.eps_yoy[index] < profit_min:
                        xx.ix[k]=ylnl.ix[pe_index]
                        k=k+1
    
                    
                else: #选取大于小值，小于大值值
                    if ylnl.eps_yoy[index] > profit_max and ylnl.eps_yoy[index] < profit_min:
                        xx.ix[k]=ylnl.ix[index]
                        k=k+1
            xx.to_excel(store_file)
        elif profit_num == '3':
            profit_para='bvps'
    
            for index in ylnl.index:
                if ylnl.bvps[index]== '--':
                    continue
                if profit_max > profit_min:  #选取大于大值，或者小于小值的
                
                    if ylnl.bvps[index] > profit_max or ylnl.bvps[index] < profit_min:
                        xx.ix[k]=ylnl.ix[pe_index]
                        k=k+1
    
                    
                else: #选取大于小值，小于大值值
                    if ylnl.bvps[index] > profit_max and ylnl.bvps[index] < profit_min:
                        xx.ix[k]=ylnl.ix[index]
                        k=k+1
            xx.to_excel(store_file)
        elif profit_num == '4':
            profit_para='roe'
    
            for index in ylnl.index:
                if ylnl.roe[index]== '--':
                    continue
                if profit_max > profit_min:  #选取大于大值，或者小于小值的
                
                    if ylnl.roe[index] > profit_max or ylnl.roe[index] < profit_min:
                        xx.ix[k]=ylnl.ix[pe_index]
                        k=k+1
    
                    
                else: #选取大于小值，小于大值值
                    if ylnl.roe[index] > profit_max and ylnl.roe[index] < profit_min:
                        xx.ix[k]=ylnl.ix[index]
                        k=k+1
            
            xx.to_excel(store_file)
        elif profit_num == '5':
            profit_para='epcf'
    
            for index in ylnl.index:
                if ylnl.epcf[index]== '--':
                    continue
                if profit_max > profit_min:  #选取大于大值，或者小于小值的
                
                    if ylnl.epcf[index] > profit_max or ylnl.epcf[index] < profit_min:
                        xx.ix[k]=ylnl.ix[pe_index]
                        k=k+1
    
                    
                else: #选取大于小值，小于大值值
                    if ylnl.epcf[index] > profit_max and ylnl.epcf[index] < profit_min:
                        xx.ix[k]=ylnl.ix[index]
                        k=k+1
            xx.to_excel(store_file)
        elif profit_num == '6':
            profit_para='net_profits'
    
            for index in ylnl.index:
                if ylnl.net_profits[index]== '--':
                    continue
                if profit_max > profit_min:  #选取大于大值，或者小于小值的
                
                    if ylnl.net_profits[index] > profit_max or ylnl.net_profits[index] < profit_min:
                        xx.ix[k]=ylnl.ix[pe_index]
                        k=k+1
    
                    
                else: #选取大于小值，小于大值值
                    if ylnl.net_profits[index] > profit_max and ylnl.net_profits[index] < profit_min:
                        xx.ix[k]=ylnl.ix[index]
                        k=k+1
            xx.to_excel(store_file)
    
        else:
            tMsg.showinfo('提示','请输入正确标号')
        tMsg.showinfo('提示','选股完毕')

    def grow_search_stock(self):
        grow_store_file = self.grow_store_file.get()
    
        #profit_store_file = self.profit_store_file.get()
        profit_num = self.grow_num.get()
        profit_min = float(self.grow_value_min.get())
        profit_max = float(self.grow_value_max.get())
        a = np.random.standard_normal((1, 8))
        
        xx = pd.DataFrame(a)
        xx.columns=['code', 'name', 'mbrg', 'nprg', 'nav', 'targ',
           'epsg', 'seg']
    
        #search_file = pathRoute + '2017_3_'+'盈利能力'+ '.xlsx'
        #search_file = pathRoute +'roe选股'+ '.xlsx'
    
        FileName = self.search_grow_file.get()
        #pathCode=pathRoute  + FileName+'.xlsx'
        
        search_file = pathRoute +FileName+ '.xlsx'
        store_file = pathRoute + grow_store_file+ '.xlsx'
        k=0
        ylnl=pd.read_excel(search_file)
        if profit_num == '1':
            profit_para='mbrg'
    
            for index in ylnl.index:
                if ylnl.mbrg[index]== '--':
                    continue
                if profit_max > profit_min:  #选取大于大值，或者小于小值的
                    
                
                    if float(ylnl.mbrg[index]) > profit_max or float(ylnl.mbrg[index]) < profit_min:
                        xx.ix[k]=jbsj.ix[pe_index]
                        k=k+1
    
                    
                else: #选取大于小值，小于大值值
                    
                    if float(ylnl.mbrg[index]) > profit_max and float(ylnl.mbrg[index]) < profit_min:
                        xx.ix[k]=ylnl.ix[index]
                        k=k+1
            xx.to_excel(store_file)
        elif profit_num == '2':
            profit_para='nprg'
    
            for index in ylnl.index:
                if ylnl.nprg[index]== '--':
                    continue
                if profit_max > profit_min:  #选取大于大值，或者小于小值的
                    
                
                    if ylnl.nprg[index] > profit_max or ylnl.nprg[index] < profit_min:
                        xx.ix[k]=ylnl.ix[pe_index]
                        k=k+1
    
                    
                else: #选取大于小值，小于大值值
                    if ylnl.nprg[index] > profit_max and ylnl.nprg[index] < profit_min:
                        xx.ix[k]=ylnl.ix[index]
                        k=k+1
            xx.to_excel(store_file)
        elif profit_num == '3':
            profit_para='nav'
    
            for index in ylnl.index:
                if ylnl.nav[index]== '--':
                    continue
                if profit_max > profit_min:  #选取大于大值，或者小于小值的
                
                    if ylnl.nav[index] > profit_max or ylnl.nav[index] < profit_min:
                        xx.ix[k]=ylnl.ix[pe_index]
                        k=k+1
    
                    
                else: #选取大于小值，小于大值值
                    if ylnl.nav[index] > profit_max and ylnl.nav[index] < profit_min:
                        xx.ix[k]=ylnl.ix[index]
                        k=k+1
            xx.to_excel(store_file)
        elif profit_num == '4':
            profit_para='targ'
    
            for index in ylnl.index:
                if ylnl.targ[index]== '--':
                    continue
                if profit_max > profit_min:  #选取大于大值，或者小于小值的
                
                    if ylnl.targ[index] > profit_max or ylnl.targ[index] < profit_min:
                        xx.ix[k]=ylnl.ix[pe_index]
                        k=k+1
    
                    
                else: #选取大于小值，小于大值值
                    if ylnl.targ[index] > profit_max and ylnl.targ[index] < profit_min:
                        xx.ix[k]=ylnl.ix[index]
                        k=k+1
            
            xx.to_excel(store_file)
        elif profit_num == '5':
            profit_para='epsg'
    
            for index in ylnl.index:
                if ylnl.epsg[index]== '--':
                    continue
                if profit_max > profit_min:  #选取大于大值，或者小于小值的
                
                    if ylnl.epsg[index] > profit_max or ylnl.epsg[index] < profit_min:
                        xx.ix[k]=ylnl.ix[pe_index]
                        k=k+1
    
                    
                else: #选取大于小值，小于大值值
                    if ylnl.epsg[index] > profit_max and ylnl.epsg[index] < profit_min:
                        xx.ix[k]=ylnl.ix[index]
                        k=k+1
            xx.to_excel(store_file)
        elif profit_num == '6':
            profit_para='seg'
    
            for index in ylnl.index:
                if ylnl.seg[index]== '--':
                    continue
                if profit_max > profit_min:  #选取大于大值，或者小于小值的
                
                    if ylnl.seg[index] > profit_max or ylnl.seg[index] < profit_min:
                        xx.ix[k]=ylnl.ix[pe_index]
                        k=k+1
    
                    
                else: #选取大于小值，小于大值值
                    if ylnl.seg[index] > profit_max and ylnl.seg[index] < profit_min:
                        xx.ix[k]=ylnl.ix[index]
                        k=k+1
            xx.to_excel(store_file)
    
        else:
            tMsg.showinfo('提示','请输入正确标号')
        tMsg.showinfo('提示','选股完毕')
    
    def baisc_search_stock(self):
        Basic_store_file = self.baisc_store_file.get()
    
        #profit_store_file = self.profit_store_file.get()
        profit_num = self.baisc_num.get()
        profit_min = float(self.baisc_value_min.get())
        profit_max = float(self.baisc_value_max.get())
        a = np.random.standard_normal((1, 22))
        
        xx = pd.DataFrame(a)
        xx.columns=['name', 'industry', 'area', 'pe', 'outstanding', 'totals',
           'totalAssets', 'liquidAssets', 'fixedAssets', 'reserved',
           'reservedPerShare', 'esp', 'bvps', 'pb', 'timeToMarket', 'undp',
           'perundp', 'rev', 'profit', 'gpr', 'npr', 'holders']
    
        #search_file = pathRoute + '2017_3_'+'盈利能力'+ '.xlsx'
        #search_file = pathRoute +'roe选股'+ '.xlsx'
    
        FileName = self.search_basic_file.get()
        #pathCode=pathRoute  + FileName+'.xlsx'
        
        search_file = pathRoute +FileName+ '.xlsx'
        store_file = pathRoute + Basic_store_file+ '.xlsx'
        k=0
        ylnl=pd.read_excel(search_file)
        if profit_num == '11':
            profit_para='reservedPerShare'
    
            for index in ylnl.index:
                if ylnl.reservedPerShare[index]== '--':
                    continue
                if profit_max > profit_min:  #选取大于大值，或者小于小值的
                    
                
                    if float(ylnl.reservedPerShare[index]) > profit_max or float(ylnl.reservedPerShare[index]) < profit_min:
                        xx.ix[k]=jbsj.ix[pe_index]
                        k=k+1
    
                    
                else: #选取大于小值，小于大值值
                    
                    if float(ylnl.reservedPerShare[index]) > profit_max and float(ylnl.reservedPerShare[index]) < profit_min:
                        xx.ix[k]=ylnl.ix[index]
                        k=k+1
            xx.to_excel(store_file)
        elif profit_num == '12':
            profit_para='esp'
    
            for index in ylnl.index:
                if ylnl.esp[index]== '--':
                    continue
                if profit_max > profit_min:  #选取大于大值，或者小于小值的
                    
                
                    if ylnl.esp[index] > profit_max or ylnl.esp[index] < profit_min:
                        xx.ix[k]=ylnl.ix[pe_index]
                        k=k+1
    
                    
                else: #选取大于小值，小于大值值
                    if ylnl.esp[index] > profit_max and ylnl.esp[index] < profit_min:
                        xx.ix[k]=ylnl.ix[index]
                        k=k+1
            xx.to_excel(store_file)
        elif profit_num == '17':
            profit_para='perundp'
    
            for index in ylnl.index:
                if ylnl.perundp[index]== '--':
                    continue
                if profit_max > profit_min:  #选取大于大值，或者小于小值的
                
                    if ylnl.perundp[index] > profit_max or ylnl.perundp[index] < profit_min:
                        xx.ix[k]=ylnl.ix[pe_index]
                        k=k+1
    
                    
                else: #选取大于小值，小于大值值
                    if ylnl.perundp[index] > profit_max and ylnl.perundp[index] < profit_min:
                        xx.ix[k]=ylnl.ix[index]
                        k=k+1
            xx.to_excel(store_file)
        elif profit_num == '13':
            profit_para='bvps'
    
            for index in ylnl.index:
                if ylnl.bvps[index]== '--':
                    continue
                if profit_max > profit_min:  #选取大于大值，或者小于小值的
                
                    if ylnl.bvps[index] > profit_max or ylnl.bvps[index] < profit_min:
                        xx.ix[k]=ylnl.ix[pe_index]
                        k=k+1
    
                    
                else: #选取大于小值，小于大值值
                    if ylnl.bvps[index] > profit_max and ylnl.bvps[index] < profit_min:
                        xx.ix[k]=ylnl.ix[index]
                        k=k+1
            
            xx.to_excel(store_file)
        elif profit_num == '5':
            profit_para='outstanding'
    
            for index in ylnl.index:
                if ylnl.outstanding[index]== '--':
                    continue
                if profit_max > profit_min:  #选取大于大值，或者小于小值的
                
                    if ylnl.outstanding[index] > profit_max or ylnl.outstanding[index] < profit_min:
                        xx.ix[k]=ylnl.ix[pe_index]
                        k=k+1
    
                    
                else: #选取大于小值，小于大值值
                    if ylnl.outstanding[index] > profit_max and ylnl.outstanding[index] < profit_min:
                        xx.ix[k]=ylnl.ix[index]
                        k=k+1
            xx.to_excel(store_file)
        elif profit_num == '6':
            profit_para='adratio'
    
            for index in ylnl.index:
                if ylnl.adratio[index]== '--':
                    continue
                if profit_max > profit_min:  #选取大于大值，或者小于小值的
                
                    if ylnl.adratio[index] > profit_max or ylnl.adratio[index] < profit_min:
                        xx.ix[k]=ylnl.ix[pe_index]
                        k=k+1
    
                    
                else: #选取大于小值，小于大值值
                    if ylnl.adratio[index] > profit_max and ylnl.adratio[index] < profit_min:
                        xx.ix[k]=ylnl.ix[index]
                        k=k+1
            xx.to_excel(store_file)
    
        elif profit_num == '15':
            profit_para='timeToMarket'
    
            for index in ylnl.index:
                if ylnl.timeToMarket[index]== '--':
                    continue
                if profit_max > profit_min:  #选取大于大值，或者小于小值的
                
                    if ylnl.timeToMarket[index] > profit_max or ylnl.timeToMarket[index] < profit_min:
                        xx.ix[k]=ylnl.ix[pe_index]
                        k=k+1
    
                    
                else: #选取大于小值，小于大值值
                    if ylnl.timeToMarket[index] > profit_max and ylnl.timeToMarket[index] < profit_min:
                        xx.ix[k]=ylnl.ix[index]
                        k=k+1
            xx.to_excel(store_file)
        elif profit_num == '19':
            profit_para='profit'
    
            for index in ylnl.index:
                if ylnl.timeToMarket[index]== '--':
                    continue
                if profit_max > profit_min:  #选取大于大值，或者小于小值的
                
                    if ylnl.profit[index] > profit_max or ylnl.profit[index] < profit_min:
                        xx.ix[k]=ylnl.ix[pe_index]
                        k=k+1
    
                    
                else: #选取大于小值，小于大值值
                    if ylnl.profit[index] > profit_max and ylnl.profit[index] < profit_min:
                        xx.ix[k]=ylnl.ix[index]
                        k=k+1
            xx.to_excel(store_file)
        elif profit_num == '4':
            profit_para='pe'
    
            for index in ylnl.index:
                if ylnl.timeToMarket[index]== '--':
                    continue
                if profit_max > profit_min:  #选取大于大值，或者小于小值的
                
                    if ylnl.pe[index] > profit_max or ylnl.pe[index] < profit_min:
                        xx.ix[k]=ylnl.ix[pe_index]
                        k=k+1
    
                    
                else: #选取大于小值，小于大值值
                    if ylnl.pe[index] > profit_max and ylnl.pe[index] < profit_min:
                        xx.ix[k]=ylnl.ix[index]
                        k=k+1
            xx.to_excel(store_file)
    
        else:
            tMsg.showinfo('提示','请输入正确标号')
        tMsg.showinfo('提示','选股完毕')
    



    

    def Log_message(self):
        try:
            message=QueX.get(block=False)
        except queue.Empty:
            pass
        else:
            self.LogMsg.insert('end',message)
            self.LogMsg.see('end')
        self.top.after(300,self.Log_message)
    def button_real_quat(self):
        code = self.ceshiCnt.get()
        codeid = self.searchStockDictCode(code)
        codeID = (6-len(str(codeid)))*'0' + str(codeid)
        df = ts.get_today_ticks(codeID)
        #df = ts.get_tick_data(code,date='2017-01-09')
        #plt.plot(df['price'])
        codeName = codeID + self.searchStockDictName(codeID)
        date_time=df.time
        #date_time_translation = [datetime.strptime(d, '%Y-%m-%d').date() for d in date_time]
        #plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        #plt.plot(date_time,df['price'])
        #autodates = AutoDateLocator()
        #plt.gca().xaxis.set_major_locator(autodates)  
        #plt.gca().set_xticks(np.linspace(0,1,9))
        #plt.gca().set_xticklabels( ('275', '280', '285', '290', '295',  '300',  '305',  '310', '315'))
        #plt.gcf().autofmt_xdate()
    
        plt.plot(df['price'])
        plt.xlabel('tick',size=20) 
        plt.ylabel('price',size=20,fontproperties=myfont)
        #CodeName = 'co'
        plt.title(codeName,size=20,fontproperties=myfont)
        plt.show()
    def button_intersection(self):
        storeFile = pathRoute+self.StoreFile1.get()+'.xlsx'
        file1 = self.SearchFile1.get()
        file2 = self.SearchFile2.get()
        print(file1)
        print('sunxb')
        print(file2)
        filename1= pathRoute + file1 +'.xlsx'
        filename2= pathRoute + file2 +'.xlsx'
        va = stock_intersection(filename1,filename2)
        Message_Print(va)
        vb=list(va)
        b=len(vb)
        a = np.random.standard_normal((b, 1))
        xx = pd.DataFrame(a)
        xx.columns=['name']
        #b=len(vb)
        #b =self.stockDict['威孚高科']
        #print('sunxiaobo %d' %b)
        for i in range(b):
            #global dict stockDict
            xx.name[i]=vb[i] #self.searchStockDictName(vb[i])
            #xx.code[i]=stockNameToCodeId(vb[i])
            #yy= str(vb[i])
            #xx.code[i]= vb[i]
        print(b)
        print(xx.name)
        xx.to_excel(storeFile)
        #print(va)
        
        #Message_Print(vb)

    def searchStockDictCode(self,stockid):
    
        #stockid=self.ceshiCnt.get()
        if stockid in stock_dict.stockDict:#.has_key(stockid):
            stock = stock_dict.stockDict[stockid]
            #stock = (6-len(str(stockId)))*'0' + str(stockId)
        else:
            stock= stockid
        return(stock)

    def searchStockDictName(self,stockid):
    
        #stockid=self.ceshiCnt.get()
        if stockid in stock_dict.NewStockDict:#.has_key(stockid):
            stockName = stock_dict.NewStockDict[stockid]
        else:
            stockName= stockid
        return(stockName)
    def button_add_dict(self):
        CodeId = self.StockCode.get()
        CodeName = self.StockName.get()
        add_dict(CodeName,CodeId)
        #stock_dict.stockDict[CodeName] = CodeId
    def button_condition_search(self):
        stock_condition1 = self.stock_condition1.get()
        stock_condition2 = self.stock_condition2.get()
        stock_condition3 = self.stock_condition3.get()
        stock_searchFile = self.search_jishu_file.get()
        stock_storeFile = self.store_jishu_file.get()
        stock_turnoverH = self.stock_turnoverH.get()
        stock_turnoverL = self.stock_turnoverL.get()
        stock_TT_H = self.stock_TT_H.get()
        stock_TT_M = self.stock_TT_M.get()
        stock_priceH = self.stock_priceH.get()
        stock_priceL = self.stock_priceL.get()
        #Sunxb_searchStrategy(stock_searchFile,stock_storeFile,stock_condition1,stock_condition2,stock_condition3,stock_turnoverH,stock_turnoverL,stock_TT_H,stock_TT_M)
        print('条件%d,%d,%d,文件%s,%s,换手率%s,%s' %(stock_condition1,stock_condition2,stock_condition3,stock_searchFile,stock_storeFile,stock_turnoverH,stock_turnoverL))
        
        
        

def Message_Print(msgX):
        #global QueX
        QueX.put(msgX)

def Monitor_stockList_bak(MonitorList):
    users = itchat.search_friends(name='sundy2008')#name='燕子'
    account=itchat.get_friends()
    userName = users[0]['UserName']
    lenth = len(MonitorList)

    while 1:
    
      for i in range(lenth):
        CodeId = MonitorList['CodeId'][i]
        Name = stock_dict.NewStockDict[CodeId]
        price_high = float(MonitorList['PriceH'][i])
        price_low = float(MonitorList['PriceL'][i])
        StockInfo = ts.get_realtime_quotes(CodeId)
        price = StockInfo.price[0]
        price = float(price)
        xx= float(StockInfo.pre_close[0] )
        yy = (price-xx)/xx*100
        if price > price_high  or  yy > 2:
            msg = '%s价格上涨百分之%f，当前价格%f' %(Name,yy,price)
            itchat.send(msg, toUserName=  userName)  #'filehelper'

        elif price < price_low  or yy < -2:
            msg = '%s价格下跌百分之%f，当前价格%f' %(Name,yy,price)
            itchat.send(msg, toUserName=  userName)  #'filehelper'
        else:
            msg = '%s当前价格%f' %(Name,price)
            heartBeat = heartBeat+1
            if heartBeat >20:
                heartBeat = 0
                itchat.send(msg, toUserName='filehelper')
        
        time.sleep(2)
      print("Monitor Run")
      time.sleep(20)

def Monitor_stockList(MonitorList):
    
    lenth = len(MonitorList)
    heartBeat = 0
    while 1:
    #if 1:
      msg = 'CodeName  Price 涨幅\n'
      xx = list(MonitorList.CodeId)
      StockInfo = ts.get_realtime_quotes(xx)
      for i in range(len(StockInfo)):
          CodeId = StockInfo.code[i]
          Name = stock_dict.NewStockDict[str(CodeId)]
          price = float(StockInfo.price[i])
          zz= float(StockInfo.pre_close[i] )
          yy = (price-zz)/zz*100
          msg = msg + '%s  %3.2f  涨幅 %.2f%%\n' %(Name,price,yy)
      #print(xx)
      time.sleep(10)
      GUI.stockInfo.set(msg)
      '''
      for i in range(lenth):
        CodeId = MonitorList['CodeId'][i]
        Name = stock_dict.NewStockDict[str(CodeId)]
        price_high = float(MonitorList['PriceH'][i])
        price_low = float(MonitorList['PriceL'][i])
        StockInfo = ts.get_realtime_quotes(CodeId)
        price = StockInfo.price[0]
        price = float(price)
        xx= float(StockInfo.pre_close[0] )
        yy = (price-xx)/xx*100
        
        msg = msg + '%s  %3.2f  涨幅 %.2f%%\n' %(Name,price,yy)
        
        time.sleep(1)
      print("Monitor Run")
      time.sleep(1)
      GUI.stockInfo.set(msg)
      '''  
def stock_intersection(search_file1,search_file2):
    file1=pd.read_excel(search_file1)
    file2=pd.read_excel(search_file2)
    file1_name=file1.name
    file2_name=file2.name
    p=set(file1_name)
    q=set(file2_name)
    va=p.intersection(q)
    
    return(va)

def stockCode_intersection(search_file1,search_file2):
    file1=pd.read_excel(search_file1)
    file2=pd.read_excel(search_file2)
    file1_code=file1.code
    file2_code=file2.code
    p=set(file1_code)
    q=set(file1_code)
    va=p.intersection(q)

    return(va)

def stockNameToCodeId(Name):
    jbdate_file1 = pathRoute +'基本数据.xlsx'
    
    file1=pd.read_excel(jbdate_file1)
    lenth = len(file1)
    for i in range(lenth):
        if Name == file1.name[i]:
            break
        else:
            continue
    if i == lenth:
        return (0)
    codeid = file1.code[i]
    return (codeid)


def stockDict1():
    jbdate_file1 = pathRoute +'基本数据.xlsx'
    file1=pd.read_excel(jbdate_file1)
    lenth = len(file1)
    d={}
    for i in range(lenth):
        code = file1.code[i]
        codeid = (6-len(str(code)))*'0' +str(code)
        d[file1.name[i]]=codeid
    filename='字典.txt'    
    P_file=open(filename, 'w',encoding="utf-8")
    #=0
    P_file.write('%s\n' %d)
    

        #time.sleep(10)
    #return(stock)
myfont = matplotlib.font_manager.FontProperties(fname='C:/Windows/Fonts/msyh.ttf')  
mpl.rcParams['axes.unicode_minus'] = False 
QueX = queue.Queue() 
GUI=msgself()
#searchStockDictCode()
'''

#b =stockDict['千山药机']
#print('sunxiaobo %d' %b)
#p =stockNameToCodeId('威孚高科')
#print(p)

itchat.auto_login()
#Log_message()
#itchat.auto_login()
#Monitor_price('000519',7.05,7.12)
#Message_Print('sunxiaobo')
#print('hahahhah')

thread_list = []
thread_list.append(threading.Thread(target=Monitor_price, args = ('601989', 5.65,5.95,)))
thread_list.append(threading.Thread(target=Monitor_price, args = ('600729', 24.90,26.50,)))


#thread_list.append(threading.Thread(target=self.mainloop))
#thread_list.append(threading.Thread(target=Log_message))
for a in thread_list:
    a.start()
#for a in thread_list:

    #a.join() #表示等待直到线程运行完毕
'''
mainloop()


