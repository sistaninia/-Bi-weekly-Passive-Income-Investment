# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 20:29:42 2020

@author: sista https://handsoffinvesting.com/a-simple-program-to-get-thousands-of-stocks-data/
"""
import sys
if len(sys.argv)>1:sys.path.insert(0,sys.argv[1])
import pandas as pd, shutil, os
from get_all_tickers import get_tickers as gt
from get_all_tickers.get_tickers import Region
import time
import matplotlib.pyplot as plt
#from array import array
import numpy as np
#import math
#from yahoofinancials import YahooFinancials as YFin
from shutil import copyfile
#from sklearn.linear_model import LinearRegression
#from math import log10,log
from Gui import * 
from CallCode import buildyf,sort,marketPredict
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning) 
#---------------------------------------------------Stre------------------------ 
MS=MyStock()
Mincap,flagDel,MRegion,country,tickersfile,mkb_no,maxcap,LP,MP,SP,LPno,MPno,SPno=MS.mincap,MS.dele,MS.Reg,MS.Count,MS.filename,MS.mkb_no,MS.maxcap,MS.LP,MS.MP,MS.SP,int(MS.LPno),int(MS.MPno),int(MS.SPno)
Duration=30 #days
ttest=float(MS.Backd)
tbuy = time.time()
tbuy=tbuy+ttest*24*3600
tsel=tbuy+Duration*24*3600
Start_time = ([int(time.localtime(tbuy)[0]),int(time.localtime(tbuy)[1]),int(time.localtime(tbuy)[2])])#([2020, 12, 16])
End_time =  ([int(time.localtime(tsel)[0]),int(time.localtime(tsel)[1]),int(time.localtime(tsel)[2])])
# MRegion=input("Which region(None =all)?" or None )#Region.EUROPE 
#df = pd.read_csv('Alltickers50cap.csv')df
#tickers=df['tickers']
dfticker=[]
Logfile='Run'+time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
Inter={24:'1wk',14:'1wk',11:'5d',3:'1d',6:'1d',2:'1d',1:'1d',0.7:'1d',0.5:'1d',0.4:'1d'}

def Ana3y(tickers,reg,TickersMKB):
    Periodyears=float(MS.YP)
    if not '^GSPC' in tickers:
        try:
            tickers.insert(0,'^GSPC')
            tickers.insert(0,'CHF=X')
        except:
            tickers=tickers.insert(0,'^GSPC')
            tickers=tickers.insert(0,'CHF=X')
    # preselection based on the last 3-4 years at this time of yearb
    tbuyYp=tbuy
    Endtime= ([int(time.localtime(tbuyYp)[0]),int(time.localtime(tbuyYp)[1]),int(time.localtime(tbuyYp)[2])])
    tsta=tbuy-Periodyears*30*24*3600*12
    Starttime = ([int(time.localtime(tsta)[0]),int(time.localtime(tsta)[1]),int(time.localtime(tsta)[2])])#([2020, 12, 16])
    startt=str(Starttime[0])+"-"+str(Starttime[1])+"-"+str(Starttime[2])
    endt=str(Endtime[0])+"-"+str(Endtime[1])+"-"+str(Endtime[2])
    yfy=buildyf(startt,endt,"1wk")
    yfy.callyf(tickers,'read',Incr=1) 
    dfYP = pd.DataFrame(data=tickers,columns=['tickers']) 
    dfYP["first"+startt]=yfy.first
    dfYP["maximum"]=yfy.maximum
    dfYP["minimum"]=yfy.minimum
    dfYP["last"]=yfy.last
    dfYP["Maxdrop"]=yfy.Maxdrop
    dfYP["AveGrowth(per month)"]=yfy.aver
    dfYP["Sort"]=[TickersMKB[tickers[i]] for i in range(len(yfy.aver))]
    dfYP=dfYP.set_index('tickers')
    dfYP=dfYP.dropna()
    dfYP.sort_values(by=["Sort"], inplace=True, ascending=False)
    tickers3y=dfYP.index[0:int(reg)].tolist()
    writer = pd.ExcelWriter(excel_dir, engine='xlsxwriter')
    dfYP.to_excel(writer,sheet_name="R%dy_%sto%s" %(Periodyears,startt,endt))
    writer.close()
    return tickers3y,dfYP

def AnaLP(tickers3y,TickersMKB=None):
    #preselection second layer thelast 10-11 monthes
    MPeriod=LP
    if not 'CHF=X' in tickers3y:tickers3y.insert(0,'CHF=X')
    if not '^GSPC' in tickers3y:tickers3y.insert(0,'^GSPC')

            # tickers3y=tickers3y.insert(len(tickers3y),'^IXIC')
    Endtime= ([int(time.localtime(tbuy)[0]),int(time.localtime(tbuy)[1]),int(time.localtime(tbuy)[2])])
    tsta=tbuy-MPeriod*30*24*3600
    Starttime = ([int(time.localtime(tsta)[0]),int(time.localtime(tsta)[1]),int(time.localtime(tsta)[2])])#([2020, 12, 16])
    tickersLP=tickers3y
    startt=str(Starttime[0])+"-"+str(Starttime[1])+"-"+str(Starttime[2])
    endt=str(Endtime[0])+"-"+str(Endtime[1])+"-"+str(Endtime[2])
    yfLP=buildyf(startt,endt,Inter[LP])
    # if float(MS.Backint)*float(MS.Backdu)*ttest>=0:yfLP.callyf(tickersLP,'download')
    # else:yfLP.callyf(tickersLP,'read')
    yfLP.callyf(tickersLP,MS.LPD)#,Lastsale=TickersMKB['Last Sale']
    dfLP = pd.DataFrame(data=tickersLP,columns=['tickers']) 
    dfLP["first"+startt]=yfLP.first
    dfLP=dfLP.set_index('tickers')
    dfLP["Last Ave"]=yfLP.lastav
    dfLP["last"]=yfLP.last
    dfLP["maximum"]=yfLP.maximum
    dfLP["minimum"]=yfLP.minimum
    dfLP["Volume"]=yfLP.volume#[yfLP.volume[i]/TickersMKB.loc[tickersLP[i],'NoShares'] for i in range(len(yfLP.aver))]
    dfLP["Mkp"]= [yfLP.volume[i]*sum(yfLP.p[tickersLP[i]][90:180])/(len(yfLP.p[tickersLP[i]][90:180])+1) for i in range(len(yfLP.aver))]
    dfLP["MximumDrop"]=yfLP.Maxdrop
    dfLP["1-Stochastic14d"]=[yfLP.last[i]/yfLP.minimum[i] for i in range(len(yfLP.aver))]
    dfLP["AveGrowth(per month)"]=yfLP.aver
    dfLP['Max expected in 1m']=[yfLP.lastav[i]*(1+yfLP.aver[i]*(1 if yfLP.aver[i] > 0 else 0)+yfLP.maximum[i]) for i in range(len(yfLP.aver))]
    dfLP['Min expected in 1m']=[yfLP.lastav[i]*(1+yfLP.aver[i]*(0 if yfLP.aver[i] > 0 else 1)+yfLP.minimum[i]) for i in range(len(yfLP.aver))]
    dfLP.loc['CHF=X','Max expected in 1m']=100
    # dfLP.sort_values(by=["Max expected in 1m"], inplace=True, ascending=False)

    # reg=int(len(tickersLP)*0.9)
    # dfLP=dfLP[0:reg]
    dfLP.sort_values(by=["Mkp"], inplace=True, ascending=False)
    dfLP["Mkp"] = dfLP["Mkp"].fillna(0)
    reg=min(int(MS.YPno),int(len(tickersLP)-1))
    MRKmin=dfLP.iloc[reg]["Mkp"]
    tt=[dfLP["AveGrowth(per month)"][i]*LP/2+dfLP["minimum"][i] for i in range(len(dfLP["AveGrowth(per month)"]))]
    newlist = [x for x,y in zip(dfLP["Volume"],dfLP["Mkp"]) if (np.isnan(x)  == False and x!=0 and y>MRKmin)]
    sort(newlist,newlist.copy())
    Vollim=min(int(620),int(len(newlist)*0.80))
    if MS.MB=='vs' or MS.MB=='s':VoluMin=newlist[Vollim]
    else:VoluMin=newlist[0]
    dfLP["AveGrowth-drop"]=[tt[i] if dfLP["Volume"][i]>VoluMin and dfLP["Mkp"][i]>MRKmin else -1000+tt[i] for i in range(len(dfLP["Volume"]))]   

    dfLP.sort_values(by=["AveGrowth-drop"], inplace=True, ascending=False)
    if MS.YP=='0':writer = pd.ExcelWriter(excel_dir, engine='xlsxwriter')
    else:writer = pd.ExcelWriter(excel_dir, engine='openpyxl', mode='a')
    dfLP.to_excel(writer,"RLP_%sto%s" %(startt,endt))
    writer.close()
    return tickersLP,dfLP,yfLP
def AnaMP(tickersLP,yfLP,dfLP,MP,reg,tbuy):
    #preselection second layer the last 2 monthes
    MPeriod=MP
    Endtime= ([int(time.localtime(tbuy)[0]),int(time.localtime(tbuy)[1]),int(time.localtime(tbuy)[2])])
    tsta=tbuy-MPeriod*28*24*3600
    Starttime = ([int(time.localtime(tsta)[0]),int(time.localtime(tsta)[1]),int(time.localtime(tsta)[2])])#([2020, 12, 16]) 
    startt=str(Starttime[0])+"-"+str(Starttime[1])+"-"+str(Starttime[2])
    endt=str(Endtime[0])+"-"+str(Endtime[1])+"-"+str(Endtime[2])
    if MP==0:
        tickersMP=tickersLP.copy()
        yfMP=yfLP
        MPeriod=LP
    else:
        tickersMP=dfLP.index[0:int(reg)].tolist()
        if not 'CHF=X' in tickersMP: tickersMP.insert(0,'CHF=X')
        if not '^GSPC' in tickersMP: tickersMP.insert(0,'^GSPC')
        # if not '^IXIC' in tickersMP: tickersMP=tickersMP.insert(len(tickersMP),'^IXIC')
        tickersMP=list(set(tickersMP))
        yfMP=buildyf(startt,endt,Inter[MP])
        yfMP.callyf(tickersMP,MS.MPD)
#    tickersMP=dfLP.index[0:int(reg)]
    dfMP = pd.DataFrame(data=tickersMP,columns=['tickers'])    
    dfMP["first"+startt]=yfMP.first
    dfMP["Last Ave"]=yfMP.lastav
    dfMP["last"]=[(yfMP.last[i]+1)*yfMP.lastav[i] for i in range(len(yfMP.lastav))]
    dfMP["maximum"]=yfMP.maximum
    dfMP["minimum"]=yfMP.minimum
    dfMP["MximumDrop"]=yfMP.Maxdrop
    dfMP["AveGrowth(per month)"]=yfMP.aver
    dfMP["ADX"]=yfMP.ADX
    dfMP["DADX"]=yfMP.DADX
    dfMP["MAV"]=yfMP.MAV
    dfMP["Risk"]=yfMP.Riskflag
    dfMP["Mom"]=yfMP.ROC
    dfMP["maxlast"]=[yfMP.last[i]/yfMP.maximum[i] for i in range(len(yfMP.aver))]
    dfMP["Bolinger"]=yfMP.Stoch
    if MS.MB=='vs' or MS.MB=='s':dfMP["1-Stochastic14d"]=[yfMP.last[i]/(yfMP.minimum[i]+0.0001) for i in range(len(yfMP.aver))]
    else:dfMP["1-Stochastic14d"]=[1-yfMP.Stoch[i] for i in range(len(yfMP.aver))]
    tt=[yfMP.minimum[i] if yfMP.Riskflag[i]=='Low' else -10+yfMP.minimum[i] for i in range(len(yfMP.aver))]
    dfMP["Min Benefit-last"]=yfMP.minimum
    dfMP['Max expected in 1m']=[(1+yfMP.aver[i]*(1 if yfMP.aver[i] > 0 else 0)+yfMP.maximum[i]-(yfMP.last[i]+1))/(yfMP.last[i]+1) for i in range(len(yfMP.aver))]
    dfMP['Min expected in 1m']=[(1+yfMP.aver[i]*(0 if yfMP.aver[i] > 0 else 0.5)+yfMP.minimum[i]-(yfMP.last[i]+1))/(yfMP.last[i]+1) for i in range(len(yfMP.aver))]
    dfMP=dfMP.set_index('tickers')
    dfMP.sort_values(by=["Min Benefit-last"], inplace=True, ascending=False)
    if LP:writer = pd.ExcelWriter(excel_dir, engine='openpyxl', mode='a',if_sheet_exists='overlay')
    else: writer = pd.ExcelWriter(excel_dir, engine='xlsxwriter') 
    dfMP.to_excel(writer,"RMP_%sto%s" %(startt,endt))
    writer.close()
    return tickersMP,dfMP,yfMP
def AnaSP(dfMP,yfMP,SP,reg,tbuy):
    #third layer based on the last month
    
    MPeriod=SP
    Endtime= ([int(time.localtime(tbuy)[0]),int(time.localtime(tbuy)[1]),int(time.localtime(tbuy)[2])])
    tsta=tbuy-MPeriod*28*24*3600
    Starttime = ([int(time.localtime(tsta)[0]),int(time.localtime(tsta)[1]),int(time.localtime(tsta)[2])])#([2020, 12, 16])  
    startt=str(Starttime[0])+"-"+str(Starttime[1])+"-"+str(Starttime[2])
    endt=str(Endtime[0])+"-"+str(Endtime[1])+"-"+str(Endtime[2])
    if SP==0:
        yfSP=yfMP
        tickersSP=yfMP.tickers
    else:
        tickersSP=dfMP.index[0:int(reg)].tolist()
        if not 'CHF=X' in tickersSP:tickersSP.insert(0,'CHF=X')
        if not '^GSPC' in tickersSP:tickersSP.insert(0,'^GSPC')
        # if not '^IXIC' in tickersSP:tickersSP=tickersSP.insert(len(tickersSP),'^IXIC')                                                                                      
        tickersSP=list(set(tickersSP))
        yfSP=buildyf(startt,endt,Inter[SP])
        yfSP.callyf(tickersSP,MS.SPD)
    dfSP = pd.DataFrame(data=tickersSP,columns=['tickers']) 
    dfSP=dfSP.set_index('tickers')
    dfSP["first"+startt]=yfSP.first
    dfSP["Last Ave"]=yfSP.lastav
    dfSP["last"]=[(yfSP.last[i]+1)*yfSP.lastav[i] for i in range(len(yfSP.lastav))]
    dfSP["maximum"]=yfSP.maximum
    dfSP["minimum"]=yfSP.minimum
    dfSP["MAV"]=yfSP.MAV
    dfSP["MximumDrop"]=yfSP.Maxdrop
    dfSP["PPO"]=yfSP.PPO
    dfSP["PPOsum"]=yfSP.PPOSum
    dfSP["AveGrowth(per month)"]=yfSP.aver
    dfSP["1-Stochastic14d"]=[1-dfMP.loc[tickersSP[i],"Bolinger"] for i in range(len(yfSP.aver))]
    dfSP["ADXd"]=[yfSP.ADX[i] if yfSP.ADX[i]  else dfMP.loc[tickersSP[i],"ADX"]  for i in range(len(yfSP.aver))]
    dfSP["LastMin"]=[yfSP.last[i]/yfSP.minimum[i] for i in range(len(yfSP.aver))]
    tt=[(yfSP.aver[i]-dfMP.loc[tickersSP[i],"AveGrowth(per month)"])*dfMP.loc[tickersSP[i],"ADX"] for i in range(len(yfSP.aver))]
    # tt=[yfSP.aver[i]*(SP+1)-dfMP.loc[tickersSP[i],"AveGrowth(per month)"]+yfSP.minimum[i] for i in range(len(yfSP.aver))]
    dfSP["sizor"]=[(yfSP.p[tickersSP[i]][-1]-yfSP.p[tickersSP[i]][0])*(yfSP.p[tickersSP[i]][0]-min(yfSP.p[tickersSP[i]]))/min(yfSP.p[tickersSP[i]])**2
        if yfSP.p[tickersSP[i]][0]*yfSP.p[tickersSP[i]][-1] else -100 for i in range(len(yfSP.aver))]
    if MS.MB=='vs' or MS.MB=='s':
        Splim=0.40-0.2*(dfMP.loc['^GSPC',"Bolinger"])
        #Splim=0.3-dfSP.loc['^GSPC',"AveGrowth(per month)"]*3
        Splim=max(Splim,0.2)
        Splim=min(Splim,0.4)
    else:Splim=0.8
    #dfSP["Min Benefit-last"]=[tt[i] if (yfSP.aver[i]<Splim and yfSP.aver[i]>-0.01 and dfLP.loc[tickersSP[i],"1-Stochastic14d"]>0.02 and yfSP.Maxdrop[i]>-0.12) and (dfMP.loc[tickersSP[i],"AveGrowth(per month)"]<Splim*0.5) else -100+tt[i] for i in range(len(yfSP.aver))]
    #Spmin=min(dfSP.loc['^IXIC',"AveGrowth(per month)"],dfSP.loc['^GSPC',"AveGrowth(per month)"],-0.01)
    dfSP["Min Benefit-last"]=[tt[i] if (yfSP.aver[i]<Splim and yfSP.Maxdrop[i]>-0.12) and (dfMP.loc[tickersSP[i],"AveGrowth(per month)"]<Splim*0.5) else -100+tt[i] for i in range(len(yfSP.aver))]
    dfSP['Max expected in 1m']=[yfSP.lastav[i]*(1+yfSP.aver[i]*(1 if yfSP.aver[i] > 0 else 0)+yfSP.maximum[i]) for i in range(len(yfSP.aver))]
    dfSP['Min expected in 1m']=[yfSP.lastav[i]*(1+yfSP.aver[i]*(0 if yfSP.aver[i] > 0 else 1)+yfSP.minimum[i]) for i in range(len(yfSP.aver))]
    if SP:dfSP.sort_values(by=["Min Benefit-last"], inplace=True, ascending=False)
    writer = pd.ExcelWriter(excel_dir, engine='openpyxl', mode='a',if_sheet_exists='overlay')
    dfSP.to_excel(writer,sheet_name="RSP%sto%s" %(startt,endt))
    writer.close()
    return tickersSP,dfSP,yfSP
def Ana1wk(tickers,dfMP,dfSP,dfLP,reg,tend,readflag,day):
    tst=tend-day*24*3600
    Endtime= ([int(time.localtime(tend)[0]),int(time.localtime(tend)[1]),int(time.localtime(tend)[2])])
    Starttime= ([int(time.localtime(tst)[0]),int(time.localtime(tst)[1]),int(time.localtime(tst)[2])])#([2020, 12, 16])
    #sort(tt,tickers3,Maxdrop)
    df1wk = pd.DataFrame(data=tickers,columns=['tickers']) 
    startt=str(Starttime[0])+"-"+str(Starttime[1])+"-"+str(Starttime[2])
    endt=str(Endtime[0])+"-"+str(Endtime[1])+"-"+str(Endtime[2])
    yf1wk=buildyf(startt,endt,"1d")
    yf1wk.callyf(tickers,readflag,Overwrite=False)
    df1wk["first"+startt]=yf1wk.first
    df1wk["Last Ave"]=yf1wk.lastav
    df1wk["last"]=[(yf1wk.last[i]+1)*yf1wk.lastav[i] for i in range(len(yf1wk.first))]
    #df1wk["maximum"]=yf1wk2.maximum
    #df1wk["minimum"]=yf1wk2.minimum
    #df1wk["MximumDrop"]=yf1wk2.Maxdropi share
    df1wk=df1wk.set_index('tickers')
    df1wk["AveGrowth(per month)"]=yf1wk.aver
    #df1wk["Min Benefit-last"]=[(dfSP.loc[SS,'last']-min(dfMP.loc[SS,'Min expected in 1m'],dfSP.loc[SS,'Min expected in 1m']))/(min(dfMP.loc[SS,'Max expected in 1m'],dfSP.loc[SS,'Max expected in 1m'])-min(dfMP.loc[SS,'Min expected in 1m'],dfSP.loc[SS,'Min expected in 1m'])) for SS in df1wk.head(reg).index.values]
    #df1wk["Min Benefit-last"]=[min(dfMP.loc[SS,'AveGrowth(per month)'],dfSP.loc[SS,'AveGrowth(per month)'])/2+(min(dfMP.loc[SS,'Min expected in 1m'],dfSP.loc[SS,'Min expected in 1m'])-dfSP.loc[SS,'last'])/dfSP.loc[SS,'last'] for SS in df1wk.head(reg).index.values]
    #df1wk["Min Benefit-last"]=[(min(dfMP.loc[SS,'Last Ave'],dfSP.loc[SS,'Last Ave'])-dfSP.loc[SS,'last'])/dfSP.loc[SS,'last'] for SS in df1wk.head(reg).index.values]
#    df1wk["Min Benefit-last"]=[dfMP.loc[SS,"1-Stochastic14d"]*dfMP.loc[SS,"ADX"] if  dfSP.loc[SS,'AveGrowth(per month)']>-0.01
#                                          and yfSP.p[SS][0]-min(yfSP.p[SS][2],yfSP.p[SS][1])>0.05*abs(yfSP.p[SS][2]-yfSP.p[SS][1]) else -100+dfMP.loc[SS,"1-Stochastic14d"]*dfMP.loc[SS,"ADX"] for SS in df1wk.head(reg).index.values]
    df1wk["PPO"]=[dfSP.loc[SS,'PPO']for SS in df1wk.head(reg).index.values]
    df1wk["PPOSum"]=[dfSP.loc[SS,'PPOsum']for SS in df1wk.head(reg).index.values]
    df1wk["LPStoch"]=[dfLP.loc[SS,"1-Stochastic14d"] for SS in df1wk.head(reg).index.values]
    df1wk["SPAver"]=[dfSP.loc[SS,'AveGrowth(per month)'] for SS in df1wk.head(reg).index.values]
    df1wk["MPStoch"]=[dfMP.loc[SS,"1-Stochastic14d"] for SS in df1wk.head(reg).index.values]
    df1wk["LastMin"]=[dfSP.loc[SS,"1-Stochastic14d"] for SS in df1wk.head(reg).index.values]
    #milPs=df1wk.sort_values(by=["LPStoch"]).iloc[45]["LPStoch"]

    df1wk["Min Benefit-last"]=[dfMP.loc[SS,"1-Stochastic14d"]*dfMP.loc[SS,"ADX"] if dfSP.loc[SS,'AveGrowth(per month)']>min(-0.01,df1wk["SPAver"].mean())
            and dfSP.loc[SS,'AveGrowth(per month)']<0.22 
            and 1.5*dfSP.loc[SS,"PPO"]>dfSP.loc[SS,"PPOsum"]
            and dfMP.loc[SS,"1-Stochastic14d"]*dfMP.loc[SS,"ADX"]<max(8,dfMP.loc['^GSPC',"1-Stochastic14d"]*dfMP.loc['^GSPC',"ADX"])
            and dfSP.loc[SS,"1-Stochastic14d"]>0.1 #and dfMP.loc[SS,"1-Stochastic14d"]*dfMP.loc[SS,"ADX"]<8#and dfMP.loc[SS,"ADX"]*dfSP.loc[SS,'AveGrowth(per month)']*100>20
            and dfSP.loc[SS,"1-Stochastic14d"]<0.9
            and dfLP.loc[SS,"1-Stochastic14d"]>=-0.01 # and df1wk.loc[SS,"AveGrowth(per month)"]>=0.0#and (dfLP.loc['^GSPC',"1-Stochastic14d"]>-0.5 or dfMP.loc['^GSPC',"AveGrowth(per month)"]>0) 
            else -1000+dfMP.loc[SS,"1-Stochastic14d"]*dfMP.loc[SS,"ADX"]  for SS in df1wk.head(reg).index.values]
# or dfMP.loc[SS,"maxlast"]>1 and dfMP.loc[SS,"'AveGrowth(per month"]<0
#    df1wk["Min Benefit-last"]=[dfMP.loc[SS,"1-Stochastic14d"]/(dfSP.loc[SS,"maximum"]-dfSP.loc[SfrfrfS,"minimum"]) if  dfSP.loc[SS,'AveGrowth(per month)']>-0.01
#                                          and dfMP.loc[SS,"1-Stochastic14d"]>0.02 else -100+dfMP.loc[SS,"1-Stochastic14d"]/(dfSP.loc[SS,"maximum"]-dfSP.loc[SS,"minimum"]) for SS in df1wk.head(reg).index.values]


    df1wk.loc['^GSPC',"Min Benefit-last"]=-2000
    df1wk.loc['CHF=X',"Min Benefit-last"]=-2001
    #else:df1wk['Min Benefit-last']=[dfSP.loc[SS,'AveGrowth(per month)']+(dfSP.loc[SS,'Last Ave']-dfSP.loc[SS,'last'])/dfSP.loc[SS,'last'] for SS in df1wk.head(reg).index.values]
    df1wk['Buying Price']=[min(yf1wk.p[tickers[i]]) for i in range(len(yf1wk.aver))]
    df1wk['target prise']=[max(yf1wk.p[tickers[i]]) for i in range(len(yf1wk.aver))]
    df1wk['Min SP based']=[dfSP.loc[SS,'Min expected in 1m'] for SS in df1wk.head(reg).index.values]
    df1wk['Min MP based']=[dfMP.loc[SS,'Min expected in 1m'] for SS in df1wk.head(reg).index.values]
    df1wk['Max Of all']=[max(dfMP.loc[SS,'Min expected in 1m'],dfSP.loc[SS,'Min expected in 1m'],min(0.88*dfMP.loc[SS,'Last Ave'],0.88*dfSP.loc[SS,'Last Ave'],0.95*dfSP.loc[SS,'last'])) for SS in df1wk.head(reg).index.values]
    df1wk['Max based on SP']=[dfSP.loc[SS,'Max expected in 1m'] for SS in df1wk.head(reg).index.values]
    df1wk['Max based on MP']=[dfMP.loc[SS,'Max expected in 1m'] for SS in df1wk.head(reg).index.values]
    #df1wk['Rel Min 1wk']=[df1wk.loc[SS,'Buying Price']/df1wk.loc[SS,'last'] for SS in df1wk.head(reg).index.values]
    df1wk['Rel Min 1m']=[dfSP.loc[SS,'Min expected in 1m']/dfSP.loc[SS,'last'] for SS in df1wk.head(reg).index.values]
    df1wk['Rel Min MP']=[dfMP.loc[SS,'Min expected in 1m']/dfMP.loc[SS,'last'] for SS in df1wk.head(reg).index.values]
    df1wk['Rel Min Max']=[df1wk.loc[SS,'Max Of all']/dfMP.loc[SS,'last'] for SS in df1wk.head(reg).index.values]
    df1wk.sort_values(by=["Min Benefit-last"], inplace=True, ascending=False)
    writer = pd.ExcelWriter(excel_dir, engine='openpyxl', mode='a',if_sheet_exists='new')
    df1wk.to_excel(writer,sheet_name="R1w%sto%s" %(startt,endt))
    writer.close()
    return df1wk,yf1wk,startt,endt
def shift_to_bottom(df,index_shift):
    idx=df.index.tolist()
    idx.pop(index_shift)
    df=df.reindex(idx+[index_shift])
    return df
def Post(Nomtick,dfSP,dfMP,dfLP,df1wk,yfSP,yfMP,Logfile,tbuy,next5):
    Colum=3
    if Nomtick<4:
        Colum=2
    fig, ax = plt.subplots(Colum, int((Nomtick+2)/Colum), constrained_layout=True,figsize=(19,9.5),clear=True)
    plt.ion()
    Priseflage='Relative'
    tickers4=df1wk.index[0:Nomtick]
    # tickers4=df1wk.index[0:Nomtick*2]
    # for SS in tickers4:
    #     if next5[SS][-1]<0 :
    #         tickers4=tickers4.drop(SS)
    # tickers4=tickers4[0:4]
    if len(tickers4)==0:tickers4=tickers4=df1wk.index[0:Nomtick]
    Nomtick=len(tickers4)
    Dpdtfram= pd.DataFrame(data=tickers4,columns=['tickers'])
    Dpdtfram['ADX']=[dfMP.loc[SS,'ADX'] for SS in tickers4]
    Dpdtfram['AVSP']=[dfSP.loc[SS,'AveGrowth(per month)'] for SS in tickers4]
    Dpdtfram['AVMP']=[dfMP.loc[SS,'AveGrowth(per month)'] for SS in tickers4]
    Dpdtfram['AVLP']=[dfLP.loc[SS,'AveGrowth(per month)'] for SS in tickers4]
    Dpdtfram['Stoch']=[dfMP.loc[SS,'1-Stochastic14d'] for SS in tickers4]
    Dpdtfram['Mom']=[dfMP.loc[SS,'Mom'] for SS in tickers4]
    Dpdtfram['AVSP*ADX']=Dpdtfram['ADX']*Dpdtfram['AVSP']
    Dpdtfram['Stoch*ADX']=Dpdtfram['ADX']*Dpdtfram['Stoch']
    Dpdtfram=Dpdtfram.set_index('tickers')
    
    Bday=[i for i in range(0,int(MS.Backdu)+7,int(MS.Backint))]
    Bdate=[str(time.localtime(tbuy+i*3600*24)[0])+'-'+str(time.localtime(tbuy+i*3600*24)[1])+'-'+str(time.localtime(tbuy+i*3600*24)[2]) for i in Bday]
    Bdata={'days':Bday, 'day':Bdate}
    SummaryResults= pd.DataFrame(Bdata)
    if MP!=0:
        period=MP*30
    else:
        period=LP*30
    dd=0
    benefit=0
    DOW=0
    Pureb=0
    comm=''
    benefits=[]
    benefits_stp=[]
    benefitsDows=[]
    CHF=[]
    benefitsCHF=[]
    tbuy_tem=tbuy
    
    list_toadd={}
    RemainSt=Nomtick
    Dtotal_Sum=0
    Dp={}

    for SS in tickers4:Dp[SS]=0
    byprise={}
    tickers5=tickers4.copy()
    if not '^GSPC' in tickers5:tickers5=tickers5.insert(len(tickers5),'^GSPC')
    if not 'CHF=X' in tickers5:tickers5=tickers5.insert(len(tickers5),'CHF=X')
    df1wk2,yf1wk2,startt,endt=Ana1wk(tickers5,dfMP,dfSP,dfLP,reg,tbuy,'download',10)
    for SS in tickers4:
        byprise[SS]=yf1wk2.p[SS][0]
        if byprise[SS]==0:byprise[SS]=yfSP.p[SS][0]
    Dpdtfram['BuyP']=[byprise[SS] for SS in tickers4]    
    SS='CHF=X'
    chfini=yf1wk2.p[SS][0]
    yaxis='NonUniform'
    while comm=='':
        Dtotal=0
        RemainSt=0
        j=0
        i=-1
        Dp_old=Dp.copy()
        Dpdtfram['Drop']=[(-byprise[SS]+df1wk2.loc[SS,'Buying Price'])/byprise[SS] for SS in tickers4]
        Dpdtfram['Max']=[(-byprise[SS]+df1wk2.loc[SS,'target prise'])/byprise[SS] for SS in tickers4]
        Dpdtfram['tMax-tmin']=[yf1wk2.p[SS].index(df1wk2.loc[SS,'target prise'])-yf1wk2.p[SS].index(df1wk2.loc[SS,'Buying Price']) for SS in tickers4]
        #if dd==10:Dpdtfram['firstlost']=[(yf1wk2.p[SS][0]yfSP.p[SS][0])/yfSP.p[SS][0] for SS in df1wk.head(Nomtick).index.values]
        for SS in tickers4:
            i+=1
            if i==Colum:
                j+=1
                i=0
            sd=lambda d : (d-tbuy_tem)/3600/24+period
            if LP:
                t=np.array(yfLP.t[SS])
                p=np.array(yfLP.p[SS])
            else:
                t=np.array(yfMP.t[SS])
                p=np.array(yfMP.p[SS])
            twkmin=min(yf1wk2.t[SS])
            p=p[t<twkmin]
            t=t[t<twkmin]
            p=np.append(p,yf1wk2.p[SS])
            t=np.append(t,yf1wk2.t[SS])
            Dp[SS]=((yf1wk2.p[SS][0]-byprise[SS])/(byprise[SS]))
            Logfile+=SS+":"+str(Dp[SS])+"\n"
            check=(yf1wk2.p[SS][0]-byprise[SS])/(min(byprise[SS],yf1wk2.p[SS][0]))
            if yf1wk2.p[SS][0]==0 or check>0.4 or check<-0.4:
                for jj in range(5):
                    print('*********Warning Yahoo Finance data for '+ SS+' *'+str(check)+' **********************************************') 
                    Logfile+='*********Warning Yahoo Finance data for '+ SS+' *'+str(check)+' **********************************************'+'\n'
            if yf1wk2.p[SS][0]==0:Dp[SS]=0
            StopL=-0.12
            StopP= (yfSP.p[SS][0]-StopL)*2+yfSP.p[SS][0]
            Pricebuy=max(dfSP.loc[SS,'Last Ave'],yfSP.p[SS][0] )
            Dpsp=(-Pricebuy+yf1wk2.p[SS][0])/Pricebuy
            # if dfSP.loc[SS,'Last Ave']<max(yf1wk2.p[SS]) and dd:
            #     if not SS in list_toadd:
            #         list_toadd.append(SS)
            #         RemainSt-=1
            # if min(yf1wk2.p[SS])<StopL and dd:
            #     Dtotal=Dtotal+(((StopL-yfSP.p[SS][0])/yfSP.p[SS][0]))
            #     list_toadd[SS]=(((StopL-yfSP.p[SS][0])/yfSP.p[SS][0]))
            # elif max(yf1wk2.p[SS])>StopP and dd:
            #     Dtotal=Dtotal+(((StopP-yfSP.p[SS][0])/yfSP.p[SS][0]))
            #     list_toadd[SS]=(((StopP-yfSP.p[SS][0])/yfSP.p[SS][0]))
            if Dpdtfram['Drop'][SS]<StopL:Dtotal=Dtotal+StopL
            # elif Dpdtfram['Max'][SS]>StopP and Dpdtfram['Drop'][SS]>StopL:Dtotal=Dtotal+StopP
            # elif Dpdtfram['tMax-tmin'][SS]<0 and Dpdtfram['Max'][SS]>StopP:Dtotal=Dtotal+StopP
            # elif Dpdtfram['tMax-tmin'][SS]>0 and Dpdtfram['Drop'][SS]<StopL:Dtotal=Dtotal+StopL
            #elif Dpdtfram['Max'][SS]>0.05:Dtotal=Dtotal+max(0.04,Dp[-1])
            else: Dtotal=Dtotal+Dp[SS]
            # if SS in list_toadd:
            #     Dtotal=Dtotal+Dp[SS]
            #     RemainSt+=1
            ax[i][j].clear()
            p=p[t>tbuy_tem-period*24*3600]
            t=t[t>tbuy_tem-period*24*3600]
            sort(t,p)
            try:
                p0=min(p) 
            except:
                continue
            if Priseflage=='Relative':rp=lambda p : (p-p0)/p0
            else:rp=lambda p : p
            ax[i][j].plot(list(map(sd,t)), list(map(rp,p)),'r')
            Per=int(min(SP*30,period))
            if SP==0:Per=period
            t=np.array(range(int(tbuy_tem)-Per*24*3600,int(tbuy_tem+8*3600),int(Per/24*3600*24)))
            td=list(map(sd,t))
            t=t.reshape((-1, 1))
            pSP=10**yfSP.model[SS].predict(t)
            pSPmin=10**yfSP.model[SS].predict(t)*(1+dfSP.loc[SS,'minimum'])
            pSPmax=10**yfSP.model[SS].predict(t)*(1+dfSP.loc[SS,'maximum'])
            ax[i][j].plot(td,list(map(rp,pSPmin)),'k',linestyle='dashed')
            ax[i][j].plot(td,list(map(rp,pSPmax)),'k',linestyle='dashed')
            ax[i][j].plot(td,list(map(rp,pSP)),color ='k', label='SP')
            Per=int(min(60,period))
            t=np.array(range(int(tbuy_tem)-Per*24*3600,int(tbuy_tem+8*3600),int(Per/24*3600*24)))
            td=list(map(sd,t))
            t=t.reshape((-1, 1))
            pMP=10**yfMP.model[SS].predict(t)
            pMPmin=10**yfMP.model[SS].predict(t)*(1+dfMP.loc[SS,'minimum'])
            pMPmax=10**yfMP.model[SS].predict(t)*(1+dfMP.loc[SS,'maximum'])
            #p7d=10**yf1wk2.model[SS].predict(t)
            ax[i][j].plot(td,list(map(rp,pMP)),color ='g', label='MP')
            ax[i][j].plot(td,list(map(rp,pMPmin)),'g',linestyle='dashed')
            ax[i][j].plot(td,list(map(rp,pMPmax)),'g',linestyle='dashed')
            Per=int(min(LP*30,period))
            t=np.array(range(int(tbuy_tem)-Per*24*3600,int(tbuy_tem+8*3600),int(Per/24*3600*24)))
            td=list(map(sd,t))
            t=t.reshape((-1, 1))
            pLP=10**yfLP.model[SS].predict(t)
            pLPmin=10**yfLP.model[SS].predict(t)*(1+dfLP.loc[SS,'minimum'])
            ax[i][j].plot(td,list(map(rp,pLP)),color ='b', label='LP')
            #ax[i][j].plot(td,pLPmin,color ='b',linestyle='dashed')
            P0=min(p0,min(pLP))
            ymax=rp(max(p))*1.1
            ymin=rp(P0)        
            ax[i][j].set_xlim([0, period])
            if yaxis=='NonUniform':ax[i][j].set_ylim([ymin, ymax])
            else:ax[i][j].set_ylim([0.0, 0.2])
            ax[i][j].set_title(SS)
            if df1wk.loc[SS,"Min Benefit-last"]<-800 and dd==0: ax[i][j].set_facecolor("yellow")
            ax[i][j].legend()
            ax[i][j].grid()
        plt.pause(0.1)
        plt.savefig(pathd+'\\Fig'+str(dd)+'.png')
        
        Dpdtfram['DP']=Dp.values()
        if float(MS.Backint)*float(MS.Backdu)*ttest>=0:
            DS=Display()
            comm,Priseflage,period,yaxis=DS.Update,DS.Prise,int(DS.Period),DS.yaxis
        else:
            if dd==100:
                DS=Display()
                comm,Priseflage,period,yaxis=DS.Update,DS.Prise,int(DS.Period),DS.yaxis
            SS='^GSPC'
            DDOW=(yf1wk2.p[SS][0]-yfSP.p[SS][0])/yfSP.p[SS][0]-DOW
            DOW=(yf1wk2.p[SS][0]-yfSP.p[SS][0])/yfSP.p[SS][0]
            SS='CHF=X'
            CHFD=(yf1wk2.p[SS][0]-chfini)/chfini
            benefit=Dpdtfram['DP'].sum()/Nomtick-Pureb
            Pureb=Dpdtfram['DP'].sum()/Nomtick
            Dtotal_Sum=Dtotal/Nomtick
            benefits.append(Pureb)
            benefits_stp.append(Dtotal_Sum)
            benefitsDows.append(DOW)
            CHF.append(CHFD)
            benefitsCHF.append(CHFD+Pureb)
    #        print('Dptotal={a} pure={b} DowSt={c} Nas={d}'.format(a=Dtotal/Nomtick,b=Pureb,c=next5['^GSPC'][0],d=next5['^IXIC'][0]))
            print(str(time.localtime(tbuy)[0])+'-'+str(time.localtime(tbuy)[1])+'-'+str(time.localtime(tbuy)[2]))        
            print('DpStopLost={a} Pure={b} CHF={c}'.format(a=Dtotal_Sum,b=Pureb,c=CHFD))
            print('DOW={a}, WeekB={b}, Delta={c}\n\n'.format(a=str(DDOW),b=str(benefit),c=str(Pureb-DOW)))
            Logfile+=(str(time.localtime(tbuy)[0])+'-'+str(time.localtime(tbuy)[1])+'-'+str(time.localtime(tbuy)[2])+'\n'+
                'DpStopLost={a} Pure={b} CHF={c}'.format(a=Dtotal_Sum,b=Pureb,c=CHFD)+'\n'+
                'DOW={a}, WeekB={b}, Delta={c}\n\n'.format(a=str(DDOW),b=str(benefit),c=str(Pureb-DOW))+'\n')
            
            tbuy_tem=tbuy+(float(MS.Backint)+dd)*24*3600
            if float(MS.Backint)+dd>float(MS.Backdu):comm='f'
            dd=dd+(float(MS.Backint))  
        if comm!='':
            #Dpdtfram.sort_values(by=['firstlost'], inplace=True, ascending=False)
            #print('Dptotal2={a}'.format(a=(Dpdtfram['DP'][0:10].sum()*2-Dpdtfram['firstlost'][0:10].sum()+Dpdtfram['firstlost'][10:].sum())/Nomtick))
            print('duration:{a} and days:{b} option:{c}'.format(a=dd-float(MS.Backint), b=ttest,c=str(Mincap)+MS.MB))
            Logfile+=('duration:{a} and days:{b} option:{c}'.format(a=dd-float(MS.Backint), b=ttest,c=str(Mincap)+MS.MB)+'\n')
            break    
        #tbuy=time.time()+(ttest+float(MS.Backdu))*24*3600
        writer = pd.ExcelWriter(excel_dir, engine='openpyxl', mode='a',if_sheet_exists='overlay')
        Dpdtfram.to_excel(writer,sheet_name="Dpdtfram_%s" %(endt))
        writer.close()
        df1wk2,yf1wk2,startt,endt=Ana1wk(tickers5,dfMP,dfSP,dfLP,reg,tbuy_tem,'download',(tbuy_tem-tbuy)/3600/24)
    if ttest:
        SummaryResults['gain']=benefits
        SummaryResults['gain2']=benefits_stp
        SummaryResults.to_csv('summary.csv', mode='a')
    writer = pd.ExcelWriter(excel_dir, engine='openpyxl', mode='a',if_sheet_exists='overlay')
    Dpdtfram.to_excel(writer,sheet_name="Dpdtfram_%s_%i" %(endt,Nomtick))
    writer.close()
    Logfile+="\nReturn Dollor\n"
    print("Return")
    for bb in benefits: 
        Logfile+=str(bb)+'\n'
        print(bb)
    Logfile+="\nReturn CHF\n"
    print("Return CHF")
    for bb in benefitsCHF:
        Logfile+=str(bb)+'\n'   
        print(bb)
    Logfile+="\nS&P 500\n"
    print("Return S&P")
    for bb in benefitsDows:
        Logfile+=str(bb)+'\n'
        print(bb)
    return Logfile,benefits,Dpdtfram,benefitsCHF
     

if MS.MAN=='Yes':
    tickerss=['^GSPC','^DJI','^IXIC','BTC-USD']
    #tickerss=['AAPL','MSFT','META','TSLA','BABA',"AMZN","GOOG"]
    next5=marketPredict(tbuy,tickerss,30,5)
# if MS.MAN=='Yes' or ttest!=0:
#     next5=marketPredict(tbuy)
#     if next5['^IXIC'][0]<-0.2 and next5['^IXIC'][0]>-0.7:
#         ttest+=5
#         tbuy=tbuy+ttest*24*3600

if ttest!=0:
    print (str(ttest)+' '+MS.MB)
    Logfile+=str(ttest)+' '+MS.MB+'\n'
Logfile+=str(LPno)+' '+str(MPno)+' '+str(SPno)+'\n'
Logfile+=str(LP)+' '+str(MP)+' '+str(SP)+'\n'  
if tickersfile=='Cancle':
    sys.exit()
if tickersfile!=None:
    dfticker = pd.read_csv(tickersfile)
    tickersfile
    pathd=".\\Results\\result"+str(Start_time[0])+'_'+str(Start_time[1])+'_'+str(Start_time[2])+'_'+tickersfile[-12:-4]
    dfticker=dfticker.set_index('tickers')
    tickers=dfticker.index
    tickers.sort_values()
    tickers=tickers.tolist() 
elif mkb_no!='Inf': 
    pathd=".\\Results\\result"+str(Start_time[0])+'_'+str(Start_time[1])+'_'+str(Start_time[2])+"Mcap"+str(Mincap)
    TickersMKB = gt.get_biggest_n_tickers(int(mkb_no),minPrice=15,Tilist=MS.TickL  ) 
    tickers=TickersMKB.index.tolist()
    tickers.sort()  
    TickersMKB.loc['^GSPC']=[37e6,3895]
    TickersMKB.loc['CHF=X']=[37e6,1.0]
elif MRegion==None or MRegion=='' or MRegion=='All':
    pathd=".\\Results\\result"+str(Start_time[0])+'_'+str(Start_time[1])+'_'+str(Start_time[2])+"Mcap"+str(Mincap)
    tickers = gt.get_tickers_filtered(mktcap_min=Mincap,mktcap_max=maxcap, country=country)
else:
    pathd=".\\Results\\result"+str(Start_time[0])+'_'+str(Start_time[1])+'_'+str(Start_time[2])+"Mcap"+str(Mincap)
    pathd=pathd+Region.EUROPE.name
    tickers = gt.get_tickers_by_region(Region.EUROPE,mktcap_min=Mincap,mktcap_max=maxcap,country=country)
excel_dir=pathd+"\\St%sResults%s.xlsx"%(MS.NoStock,str(Start_time[0])+str(Start_time[1])+str(Start_time[2]))

#print(tickers[:5])
# if Mincap==0:
#     tickers = ['RUN','ENPH','BILI','ZS','CRSP','BE', 'DQ','TSLA','FCEL' ]
#tickers = gt.get_tickers_by_region(Region.EUROPE,mktcap_min=Mincap,mktcap_max=maxcap,country='Switzerland')
if flagDel!='No'and os.path.exists(pathd):
    shutil.rmtree(pathd)
os.mkdir(pathd)
copyfile(".\\myfund.py",pathd+"\\myfund.py")
copyfile(".\\CallCode.py",pathd+"\\CallCode.py")
copyfile(".\\Gui.py",pathd+"\\Gui.py")



Stocks_Not_Imported=0
print("The amount of stocks chosen to observe: " + str(len(tickers)))
Logfile+="The amount of stocks chosen to observe: " + str(len(tickers))+'\n'
Logfile+=MS.TickL+'\n'
print(MS.TickL+'\n')
#shutil.rmtree(pathd)

reg=min(int(MS.YPno),int(len(tickers)))
if MS.YP=='0':
    tickers3y=tickers
else:
    tickers3y,dfy=Ana3y(tickers,reg)#,TickersMKB

if LP:tickersLP,dfLP,yfLP=AnaLP(tickers3y)#,TickersMKB
else:tickersLP=tickers
reg=min(LPno,int(len(tickers3y)))
tickersMP,dfMP,yfMP=AnaMP(tickersLP,yfLP,dfLP,MP,reg,tbuy)
reg=min(MPno,int(len(tickersMP)),yfMP.Stocks_Imported)
tickersSP,dfSP,yfSP=AnaSP(dfMP,yfMP,SP,reg,tbuy)
#SPno0=SPno+int(dfLP.loc['^GSPC',"1-Stochastic14d"]*(30))
reg=min(SPno,int(len(tickersSP)),yfSP.Stocks_Imported)
#last layer based on the last 7das
tickers4=dfSP.index[0:reg]

#tickers4=tickers4.drop('WLTW')
if not '^GSPC' in tickers4:
    tickers4=tickers4.insert(len(tickers4),'^GSPC')
    reg+=1
if not 'CHF=X' in tickers4:
    tickers4=tickers4.insert(len(tickers4),'CHF=X')
    reg+=1
df1wk,yf1wk,startt,endt=Ana1wk(tickers4,dfMP,dfSP,dfLP,reg,tbuy,'read',7)
#if ttest==0:Nomtick+=1

Nomtick=min(int(MS.NoStock),reg)

tickerss=df1wk.index[0:Nomtick]
next5=marketPredict(tbuy,tickerss,30,5)



Logfile+="Number of Stocks:"+str(Nomtick)+'\n'
Logfile,benefits,AnalysSt,benefitsCHF=Post(Nomtick,dfSP,dfMP,dfLP,df1wk,yfSP,yfMP,Logfile,tbuy,next5)



# Nomtick=min(int(3),reg)
# Logfile+="Number of Stocks:"+str(Nomtick)+'\n'
# Logfile,benefits,AnalysSt,benefitsCHF=Post(Nomtick,dfSP,dfMP,dfLP,df1wk,yfSP,yfMP,Logfile,tbuy)


with open(pathd+"\\Logfile.dat", 'w') as f:
    f.write(Logfile)
#sm,Stocht,Stochp, StochtS,StochpS =inde('^IXIC',48)
#=============================================================================
# class Maxben:
#     def __init__(self,reg2,capital):
#         self.minl=-1e9
#         self.MinlostTemp=np.zeros(reg2)
#         self.Minlost=np.zeros(reg2)
#         self.capital=capital
#         self.lost=0
#         self.MaxBen(1.0,reg2-1,0,0)
    
#     def MaxBen(self,coeff, j,minlt0, lost0):
#         minall=min(df1wk.loc[df1wk.head(reg).index.values[j],'Min SP based'],df1wk.loc[df1wk.head(reg).index.values[j],'Min MP based'])
#         #maxir=min(df1wk.loc[df1wk.head(reg).index.values[j],'Max based on 1month'],df1wk.loc[df1wk.head(reg).index.values[j],'Max based on MPonth'])
#         #minall=df1wk.loc[df1wk.head(reg).index.values[j],'Min MP based']
#         maxir=0
#         Lastre=df1wk.loc[df1wk.head(reg).index.values[j],"last"] 
#         if j==0 or coeff<0.1:
#             self.MinlostTemp[0:j]=np.zeros(j)
#             self.MinlostTemp[j]=coeff
#             lost=(minall-Lastre)/Lastre*coeff*self.capital
#             Benefit=(maxir-Lastre)/Lastre*coeff*self.capital 
#             maxcoef=max(self.MinlostTemp)
#             minlt=minlt0+Benefit+lost-maxcoef*self.capital
#             if minlt>self.minl:
#                 self.lost=lost+lost0
#                 self.minl=minlt
#                 self.Minlost=self.MinlostTemp.copy() 
#         else: 
#             d=int(coeff/0.1)
#             for i in range(d+1):
#                 coeff2=coeff*(d-i)/d
#                 lost=(minall-Lastre)/Lastre*(coeff-coeff2)*self.capital
#                 Benefit=(maxir-Lastre)/Lastre*(coeff-coeff2)*self.capital
#                 minlt=minlt0+Benefit+lost
#                 self.MinlostTemp[j]=(coeff-coeff2)
#                 self.MaxBen(coeff2, j-1,minlt,lost+lost0)
  
# capital=40000
# Nomtick=min(10,reg)
# MB=Maxben(Nomtick,capital) 
# Minlost=MB.Minlost
# minl=MB.minl 
# worslost=MB.lost  
# #=============================================================================


# print('min Lost for '+str(capital)+'Chf capital: '+str(minl)+' and worst lot'+str(worslost))
# buyrecom=[]
# for j in range(Nomtick):
#     print(df1wk.head(reg).index.values[j],int(Minlost[j]*capital/100)*100)
#     buyrecom.append(int(Minlost[j]*capital/100)*100)
# for j in range(reg-Nomtick):
#     buyrecom.append(float('NaN'))
# df1wk['Buy Capi='+str(capital)+' Minlost'+str(minl)+' and worst lot'+str(worslost)]=buyrecom
#================================================================================
# if 'value' in dfticker:
#     myLost=[]
#     myLostAct=[]
#     tota=0
#     totaAct=0
#     for SS in df1wk.head(reg).index.values:
#         minall=df1wk.loc[SS,'Max Of all']
#         Lastre=df1wk.loc[SS,"last"] 
#         los=((minall-Lastre)/Lastre)*dfticker.loc[SS,'value']
#         losActual=((dfticker.loc[SS,'SS']-Lastre)/Lastre)*dfticker.loc[SS,'value']
#         tota=tota+los
#         totaAct=totaAct+losActual
#         myLost.append(los)
#         myLostAct.append(losActual)
#     df1wk['My Current Capi='+str(dfticker['value'].sum())+' Minlost'+str(tota)]=myLost 
#     df1wk['My Current Capi='+str(dfticker['value'].sum())+' Actual lost'+str(tota)]=myLostAct 
#     print('My Capi='+str(dfticker['value'].sum())+' Minlost '+str(tota))  
#     print('My Capi='+str(dfticker['value'].sum())+' Minlost '+str(totaAct)) 