import time
import os
import numpy as np 
import pandas as pd 
import tushare as ts 
import datetime 
import stock_dict
import math
from pandas import Series, DataFrame
from  sunxb_lazhu import computeM

stockSelectFile = 'D:/sunxb_finance/sunxb_策略/'
stockPoolPath = 'D:/sunxb_finance/股票池/'
stockInfoPath = 'D:/sunxb_finance/stock_info/'
def searchStockPool(File):
    stockLsit=[]
    stockLsit1=[]
    
    stockPoolFile = stockPoolPath + File +'.xlsx'
    
    
    stockPool = pd.read_excel(stockPoolFile)
    
    lenth = len(stockPool)
    
    for i in range(lenth):
        if i <0:
            continue
        codeid = stock_dict.stockDict[stockPool['name'][i]]
        #stockInfo = ts.get_hist_data(codeid,start='2018-01-01')

        stockInfo = ts.get_k_data(codeid,start='2017-11-01')
        stockInfo.index = list(range(len(stockInfo)))
        xx = computeM(stockInfo,5)
        yy = computeM(stockInfo,10)
        zz = computeM(stockInfo,20)
        stockInfo['ma5']= Series(xx)
        stockInfo['ma10']= Series(yy)
        stockInfo['ma20']= Series(zz)
        
        info = len(stockInfo)
        if info <50:
            continue
        #print(stockPool['name'][i])
        #print(stockInfo.head(1))

        m10 = stockInfo['ma10'][0] - stockInfo['ma10'][5]
        m20 = stockInfo['ma20'][0] - stockInfo['ma20'][5]
        
        
        delta_m20_10= stockInfo['ma20'][0]-stockInfo['ma10'][0]

        
        #delta_m20_10 = xx/stockInfo['ma20'][0] *100

        delta_m20_10_20= stockInfo['ma20'][20]-stockInfo['ma10'][20]
        

        zz = stockInfo['close'][0] - stockInfo['ma20'][0]
        kk = zz/stockInfo['close'][0] *100

        

        qq = stockInfo['ma20'][0] - stockInfo['ma20'][5]
        tt = stockInfo['ma20'][0] - stockInfo['ma20'][1]
        
        if  abs(kk)<2 and delta_m20_10 <0 and delta_m20_10_20 > 0 and m10 >0 and m20 >0:  # and kk <1 
            stockLsit.append(stockPool['name'][i])
            print(stockInfo.tail(1))
            #break
            
        #if abs(kk) < 0.5 :  # and kk <1 
            #stockLsit1.append(stockPool['name'][i])

        if abs(kk) < 2 and qq < 0  and tt >0:  # and kk <1 
            stockLsit1.append(stockPool['name'][i])
            #print(stockInfo.head(10))
            
    xx = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    SelectFile1 = stockSelectFile + File + xx  +'.xlsx'
    SelectFile2 = stockSelectFile + File + xx +'_1' +'.xlsx'
    data= {'name':stockLsit}
    df = pd.DataFrame(data)
    df.to_excel(SelectFile1)
    data= {'name':stockLsit1}
    df = pd.DataFrame(data)
    df.to_excel(SelectFile2)
    print(stockLsit)
    print(stockLsit1)
    

    
def searchStrategy_wjh(File):

    stockLsit=[]
    stockLsit1=[]
    
    stockPoolFile = stockPoolPath + File +'.xlsx'
    
    
    stockPool = pd.read_excel(stockPoolFile)
    
    lenth = len(stockPool)
    for i in range(lenth):
        if i <0:
            continue
        codeid = stock_dict.stockDict[stockPool['name'][i]]
        outstanding = stockPool['outstanding'][i]*10000
        stockInfo = ts.get_k_data(codeid,start='2018-01-01')
        
        info = len(stockInfo)
        if info <20:
            continue
        stockInfo['turnover']=stockInfo['volume']/outstanding
        stockInfo1 = stockInfo[stockInfo.turnover > 2]
        stockInfo2 = stockInfo1[stockInfo1.turnover <5]

        
        info1 = len(stockInfo2)
        xx = float(info1)/float(info)
        if xx < 0.7:     #需要满足80%以上换手率在2%到5%之间
            continue
        print('CodeId:%s\n' %(codeid))
        k=0
        for j in range(10):  #10日内有换手率超过10%情况
            if stockInfo.turnover[info - 1 - j] > 10:
                break
        if  j == 9:
            continue

        print('10日内换手率有超过百分之10的CodeId:%s\n' %(codeid))
        for j in range(5):  #5日内换手率都超过8%
            if stockInfo.turnover[info -1-j] < 8:
                break
        if j < 4:
            continue
            
        xx = ((stockInfo.close[info-1-20] - stockInfo.close[info-1])/stockInfo.close[info-1])*100
        print(xx)
        
        #估价远离20日均线，或者在20日均线附近
        if xx < 20 and xx  >2:   
            continue
        if xx < -2 :
            continue
        
        stockLsit.append(stockPool['name'][i])
        stockInfo.to_excel(codeid + '.xlsx' )

    xx = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    SelectFile1 = stockSelectFile + File + xx  +'.xlsx'
    
    data= {'name':stockLsit}
    df = pd.DataFrame(data)
    df.to_excel(SelectFile1)
    
    print(stockLsit)


def searchStrategy(File):

    stockLsit=[]
    stockLsit1=[]
    
    stockPoolFile = stockPoolPath + File +'.xlsx'
    stockBasicFile = stockInfoPath + '基本数据.xlsx'
    
    stockPool = pd.read_excel(stockPoolFile)
    stockBasicInfo = pd.read_excel(stockBasicFile,converters={'code':str})
    stockIndexList = list(stockBasicInfo['code'])
    
    lenth = len(stockPool)
    z= 0
    for i in range(lenth):
        if i <0:
            continue
        codeid = stock_dict.stockDict[stockPool['name'][i]]
        index = stockIndexList.index(codeid)
        outstanding = stockBasicInfo['outstanding'][index]*10000
        if outstanding > 5000:  #小盘股选股
        	continue
        stockInfo = ts.get_k_data(codeid,start='2017-11-01')
        stockInfo.index = list(range(len(stockInfo)))
        info = len(stockInfo)
        if info <20:
            continue
        stockInfo['turnover']=stockInfo['volume']/outstanding
        stockInfo1 = stockInfo[stockInfo.turnover > 1]
        stockInfo2 = stockInfo1[stockInfo1.turnover < 3]
        #stockInfo2 = stockInfo[stockInfo.turnover < 3]
        
        info1 = len(stockInfo2)
        xx = float(info1)/float(info)
        if xx < 0.8:     #需要满足80%以上换手率在2%到5%之间
            continue
        print('100日内换手率2~5的CodeId:%s\n' %(codeid))
        
        k=0
        for j in range(10):  #10日内有换手率超过10%情况
            if stockInfo.turnover[info - 1 - j] > 10:
                break
        if  j == 9:
            continue
            
        print('10日内换手率有超过百分之10的CodeId:%s\n' %(codeid))  
        k=0 
        for j in range(5):  #5日内换手率都超过8%
            if stockInfo.turnover[info -1-j] > 8:
            	  k=k+1
                
        if k < 3:
            continue

        print('连续内换手率有超过百分之8的CodeId:%s\n' %(codeid)) 
        
            
        xx = ((stockInfo.close[info-1-20] - stockInfo.close[info-1])/stockInfo.close[info-1])*100
        print(xx)
        
        #估价远离20日均线，或者在20日均线附近
        if xx < 20 and xx  >2:   
            continue
        if xx < -2 :
            continue

        
        z= z+1
        print('所有条件都满足的股票总数%d只:%s\n' %(z,codeid))
        
        stockLsit.append(stockPool['name'][i])
        #stockInfo.to_excel(codeid + '.xlsx' )

    xx = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    SelectFile1 = stockSelectFile + File +'small'+ xx  +'.xlsx'
    
    data= {'name':stockLsit}
    df = pd.DataFrame(data)
    df.to_excel(SelectFile1)
    
    print(stockLsit)
    
    
    
def Sunxb_Computor_EMA(closeP):
    info = len(closeP)
    if info <50:
        return(False)
    EMA12 = list()
    EMA26 = list()
    EMA12.append(closeP[0])
    EMA26.append(closeP[0])
    for i in range(info-1):
        value12 = (2/13)*(closeP[i+1]-EMA12[i]) + EMA12[i]
        value26 = (2/27)*(closeP[i+1]-EMA26[i]) + EMA26[i]
        #diff = value12 - value26
        EMA12.append(value12)
        EMA26.append(value26)
    return(EMA12,EMA26)


def Sunxb_Computor_DIFF(closeP):
    info = len(closeP)
    if info <50:
        return(False)
    xx =0
    yy = 0
    for i in range(12):
    	xx = closeP[i]+ xx
    xx = xx/12
    for i in range(26):
    	yy = closeP[i]+ yy
    yy = yy/26
    EMA12 = list()
    EMA26 = list()
    DIFF = list()
    DIFF.append(0)
    #EMA12.append(closeP[0])
    #EMA26.append(closeP[0])
    EMA12.append(xx)
    EMA26.append(yy)
    for i in range(info-1):
        value12 = (2/13)*(closeP[i+1]-EMA12[i]) + EMA12[i]
        value26 = (2/27)*(closeP[i+1]-EMA26[i]) + EMA26[i]
        diff = value12 - value26
        EMA12.append(value12)
        EMA26.append(value26)
        DIFF.append(diff)
    return(DIFF)	
    
def Sunxb_Computor_DEA(DIFF):
    info = len(DIFF)
    if info <50:
        return(False)
    DEA = list()
    DEA.append(DIFF[0])
    for i in range(info-1):
        value9 = (2/13)*(DIFF[i+1]-DEA[i]) + DEA[i]
        DEA.append(value9)
    return(DEA)

def SunxbsearchStrategy(File):

    stockLsit=[]
    stockLsit1=[]
    
    stockPoolFile = stockPoolPath + File +'.xlsx'
    stockBasicFile = stockInfoPath + '基本数据.xlsx'
    
    stockPool = pd.read_excel(stockPoolFile)
    stockBasicInfo = pd.read_excel(stockBasicFile,converters={'code':str})
    stockIndexList = list(stockBasicInfo['code'])
    
    lenth = len(stockPool)
    z= 0
    for i in range(lenth):
        if i <0:
            continue
        codeid = stock_dict.stockDict[stockPool['name'][i]]
        index = stockIndexList.index(codeid)
        outstanding = stockBasicInfo['outstanding'][index]*10000
        if outstanding < 10000:  #大盘股选股
        	continue
        stockInfo = ts.get_k_data(codeid,start='2017-11-01')
        if len(stockInfo) < 50:
        	continue
        stockInfo.index = list(range(len(stockInfo)))
        DIFF = Sunxb_Computor_DIFF(list(stockInfo.close)) 
        if DIFF == False:
        	continue
        DEA = Sunxb_Computor_DEA(DIFF)
        if DEA == False:
        	continue
        stockInfo['DIFF']= DIFF
        stockInfo['DEA'] = DEA
        stockInfo['MACD'] = 2*(stockInfo['DIFF'] - stockInfo['DEA'])
        info = len(stockInfo)
        if stockInfo.DIFF[info - 1]  < 0:
            continue
        #print('DIFF大于0的CodeId:%s\n' %(codeid))
        if stockInfo.DEA[info - 1]  < 0:
            continue
        #print('DEA/DIFF大于0的CodeId:%s\n' %(codeid))

        if stockInfo.MACD[info - 1]  < 0:
            continue
        
        if stockInfo.MACD[info - 2]  > 0:
            continue
        print('MACD大于0的CodeId:%s\n' %(codeid))
        if info <20:
            continue   
        stockInfo['turnover']=stockInfo['volume']/outstanding
        stockInfo1 = stockInfo[stockInfo.turnover > 0]
        stockInfo2 = stockInfo1[stockInfo1.turnover < 1.5]
        #stockInfo2 = stockInfo[stockInfo.turnover < 3]
        
        info1 = len(stockInfo2)
        xx = float(info1)/float(info)
        if xx < 0.9:     #需要满足80%以上换手率在2%到5%之间
            continue
        print('100日内换手率0~1.5的CodeId:%s\n' %(codeid))
        
        k=0
        for j in range(10):  #10日内有换手率超过10%情况
            if stockInfo.turnover[info - 1 - j] > 4:
                break
        if  j == 9:
            continue
            
        print('10日内换手率有超过百分之4的CodeId:%s\n' %(codeid))  
        k=0 
        for j in range(5):  #5日内换手率都超过8%
            if stockInfo.turnover[info -1-j] > 2:
            	  k=k+1
                
        if k < 3:
            continue

        print('连续内换手率有超过百分之2的CodeId:%s\n' %(codeid))  
        
        if stockInfo.DIFF[info - 1]  < 0:
            continue
        print('DIFF大于0的CodeId:%s\n' %(codeid))
        if stockInfo.DEA[info - 1]  < 0:
            continue
        print('DEA大于0的CodeId:%s\n' %(codeid))
        stockLsit.append(stockPool['name'][i])
        #stockInfo.to_excel(codeid + '.xlsx' )

    xx = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    SelectFile1 = stockSelectFile + File +'big'+ xx  +'.xlsx'
    
    data= {'name':stockLsit}
    df = pd.DataFrame(data)
    df.to_excel(SelectFile1)
    
    print(stockLsit)        
        
        
'''	
xx =ts.get_k_data('600291',start='2017-11-01')

#EMA12,EMA26 = Sunxb_Computor_EMA(list(xx.close))
#print(EMA12)
#print(EMA26)

DIFF = Sunxb_Computor_DIFF(list(xx.close)) 

DEA = Sunxb_Computor_DEA(DIFF)


xx['DIFF']= DIFF
xx['DEA'] = DEA
xx['MACD'] = 2*(xx['DIFF'] - xx['DEA'])
print(xx)
'''     
'''
def searchCondition1(stockInfo,lenth,V_H,V_L,value):
	
	info = len(stockInfo)
    if info <20:
        return(False)

	
    stockInfo1 = stockInfo[stockInfo.turnover > V_L]
    stockInfo2 = stockInfo1[stockInfo1.turnover < V_H]
    info1 = len(stockInfo2)
    xx = float(info1)/float(lenth)
    if xx < value:     #需要满足80%以上换手率在2%到5%之间
        return(False)
    return(True)
    
def searchCondition2(stockInfo,T_H,V_M):
	
	info = len(stockInfo)
    if info <20:
        return(False)
	
	for j in range(10):  #10日内有换手率超过10%情况
        if stockInfo.turnover[info - 1 - j] > T_H:
                break
    if  j == 9:
        return(False)
             
    k=0 
    for j in range(5):  #5日内换手率都超过8%
        if stockInfo.turnover[info -1-j] > V_M:
            k=k+1
                
    if k < 3:
        return(False)
    return(True)
            
def searchCondition3(stockInfo,Condition):
	return(True)	


def Sunxb_searchStrategy(stock_searchFile,stock_storeFile,stock_condition1,stock_condition2,stock_condition3,stock_turnoverH,stock_turnoverL,stock_TT_H,stock_TT_M):
	stockLsit=[]
    #stockLsit1=[]
    
    stockPoolFile = stockPoolPath + stock_searchFile +'.xlsx'
    stockBasicFile = stockInfoPath + '基本数据.xlsx'
    
    stockPool = pd.read_excel(stockPoolFile)
    stockBasicInfo = pd.read_excel(stockBasicFile,converters={'code':str})
    stockIndexList = list(stockBasicInfo['code'])
    
    lenth = len(stockPool)
    z= 0
    for i in range(lenth):
        if i <0:
            continue
        codeid = stock_dict.stockDict[stockPool['name'][i]]
        index = stockIndexList.index(codeid)
        outstanding = stockBasicInfo['outstanding'][index]*10000
        stockInfo = ts.get_k_data(codeid,start='2018-01-01')
        info = len(stockInfo)
        if info <20:
            continue
        condition = True
        stockInfo['turnover']=stockInfo['volume']/outstanding
        if stock_condition1==1:
        	
        	
            stockInfo1 = stockInfo[stockInfo.turnover > float(stock_turnoverH)]
            stockInfo2 = stockInfo1[stockInfo1.turnover <float(stock_turnoverL)]
      
        
            info1 = len(stockInfo2)
            xx = float(info1)/float(info)
            if xx < 0.9:     #需要满足80%以上换手率在2%到5%之间
                continue
        	
        	
       
        z= z+1
        print('满足条件1的股票总数%d只:%s\n' %(z,codeid))
       
        if stock_condition1 == 1:
        	
        
            k=0
            for j in range(10):  #10日内有换手率超过10%情况
                if stockInfo.turnover[info - 1 - j] > float(stock_TT_H):
                    break
            if  j == 9:
                continue
                
            print('10日内换手率有超过百分之8的CodeId:%s\n' %(codeid))  
            k=0 
            for j in range(5):  #5日内换手率都超过8%
                if stockInfo.turnover[info -1-j] > float(stock_TT_M):
                	  k=k+1
                    
            if k < 3:
                continue 
        

            
        xx = ((stockInfo.close[info-1-20] - stockInfo.close[info-1])/stockInfo.close[info-1])*100
        print(xx)
        
        #估价远离20日均线，或者在20日均线附近
        if xx < 20 and xx  >2:   
            continue
        if xx < -2 :
            continue
        
        stockLsit.append(stockPool['name'][i])
        stockInfo.to_excel(codeid + '.xlsx' )

    xx = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    SelectFile1 = stockSelectFile + stock_storeFile + xx  +'.xlsx'
    
    data= {'name':stockLsit}
    df = pd.DataFrame(data)
    df.to_excel(SelectFile1)
    
    print(stockLsit)
 '''
#SunxbsearchStrategy('good')
#searchStockPool('good')	
