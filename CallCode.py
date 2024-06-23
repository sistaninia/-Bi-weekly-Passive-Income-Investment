# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 09:17:50 2021

@author: meisam
from pandas_datareader import data as pdr
data = pdr.get_data_yahoo("SPY", start="2021-09-01", end="2021-09-25")

"""
import yfinance as yf, pandas as pd, os#, shutil #C:\ProgramData\Anaconda3\envs\spyder-env\lib\site-packages\yfinance\base.py
import time
#import sys
import matplotlib.pyplot as plt
#from array import array
import numpy as np
#import math
#from yahoofinancials import YahooFinancials as YFin
#from shutil import copyfile
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from math import log10#,log
from smt.surrogate_models import IDW
from ta.trend import ADXIndicator, SMAIndicator
#from ta.momentum import StochasticOscillator as StocO
from ta.momentum import ROCIndicator as ROC
from ta.volatility import BollingerBands
from ta.momentum import ppo,ppo_signal
#from progressbar import ProgressBar
#from pandas_datareader import data as pdr
pd.options.mode.chained_assignment = None 
 #s
def sort(x,y,z=None):
    for i in range(len(x)):
        swap = i + np.argmax(x[i:])
        (x[i], x[swap]) = (x[swap], x[i])
        (y[i], y[swap]) = (y[swap], y[i])
        if z!=None:
            (z[i], z[swap]) = (z[swap], z[i])
    return x,y
class buildyf:
    def __init__(self,startt,endt,Interval1):
        self.ValuInc=[]
        self.tickInc=[]
        self.maximum=[]
        self.minimum=[]
        self.first=[]
        self.last=[]
        self.aver=[]
        self.lastav=[]
        self.Maxdrop=[]
        self.model={}
        self.t={}
        self.p={}
        self.Stoch=[]
        self.Riskflag=[]
        self.ADX=[]
        self.MAV=[]
        self.sizor=[]
        self.ROC=[]
        self.dailymove=[]
        self.DADX=[]
        self.volume=[]
        self.Dvolume=[]
        self.PPOSum=[]
        self.PPO=[]
        self.startt,self.endt,self.Interval1=startt,endt,Interval1
    def callyf (self,tickers,flagDel,Incr=5,Overwrite=True,Lastsale=[]):
        self.tickers=tickers
        Stock_Failure = 0
        Stocks_Not_Imported = 0
        Amount_of_API_Calls=0
        i=0
        t0=int(time.mktime(time.strptime(str(self.startt), '%Y-%m-%d')))
        t1=int(time.mktime(time.strptime(str(self.endt), '%Y-%m-%d')))
        Dt=t1-t0
        self.period=int(Dt/3600/24*Incr/7)
        tst=t0-Dt
        ten=t1+24*3600
        Starttime=([int(time.localtime(tst)[0]),int(time.localtime(tst)[1]),int(time.localtime(tst)[2])])#([2020, 12, 16])
        startt=str(Starttime[0])+"-"+str(Starttime[1])+"-"+str(Starttime[2])
        endttime=([int(time.localtime(ten)[0]),int(time.localtime(ten)[1]),int(time.localtime(ten)[2])])#([2020, 12, 16])
        endt=str(endttime[0])+"-"+str(endttime[1])+"-"+str(endttime[2])
        print('Start time:'+startt)
        print('End time:'+endt)
        st1=time.time()
        try:
            pathd="C:\\TEMP\\READ"+str(endttime[0])+'_'+str(endttime[1])+'_'+str(endttime[2])
            if not os.path.exists(pathd): os.mkdir(pathd)
        except:
            pathd="D:\\TEMP\\READ"+str(endttime[0])+'_'+str(endttime[1])+'_'+str(endttime[2])
            if not os.path.exists(pathd): os.mkdir(pathd)

        treadmax=0
        #bar = ProgressBar(max_value=100)
        di=1
        rev=1
        while (i < len(tickers)):
            
            progress=int(i/len(tickers)*40)
            rev+=di
            if rev>=40 or rev<=progress:
                di*=-1
                rev+=di
            try:
                stock = tickers[i]  # Gets the current stock ticker        
                self.t[stock]=[]
                self.p[stock]=[]
                excel_dirxlsx=pathd+"\\"+stock+".xlsx"
                excel_dir=pathd+"\\"+stock+".csv"
                flag='download'
                if (os.path.exists(excel_dir) or os.path.exists(excel_dirxlsx)) and flagDel=='read':
                    try:
                        Hist_data_min=pd.read_csv(excel_dir)                     
                        Hist_data_min=Hist_data_min.set_index('Date')
                        if Hist_data_min['time'].min()<tst+3*24*3600 and Hist_data_min['time'].max()>treadmax and Hist_data_min['time'].min() and Hist_data_min[Hist_data_min['time']>=t0].shape[0]>self.period*0.6:flag='read'  #and Hist_data_min.shpe[0]>self.period

                    except:
                        try:
                            Hist_data_min=pd.read_excel(excel_dirxlsx)   
                            Hist_data_min=Hist_data_min.set_index('Date')
                            if Hist_data_min['time'].min()<tst+3*24*3600 and Hist_data_min['time'].max()>treadmax and Hist_data_min['time'].min() and Hist_data_min[Hist_data_min['time']>=t0].shape[0]>self.period*0.6:flag='read'  #and Hist_data_min.shape[0]>self.period                        
                        except:
                            flag='download'                            
                        #Hist_data_min=readexcel[ (readexcel['time']>=tst) ] #& (readexcel['time']<=ten)
                if len(Lastsale) and flag=='read':
                    if Lastsale[stock]<0.5*Hist_data_min['Low'].min():flag='download'
                if flag=='download': 
                    sleeptime=max(1.2-(time.time()-st1),0)                  # Pauses the loop for two seconds so we don't cause issues with Yahoo Finance's backend operations
                    time.sleep(sleeptime)                  
                    st1=time.time()
                    temp = yf.Ticker(str(stock))  # Instantiate the ticker as a stock with Yahoo Finance
                    Hist_data_min = temp.history(start=startt, end=endt,interval=self.Interval1,timeout=5)  # Tells yfinance what kind of data we want about this stock (In this example, all of the historical data)
                    #Hist_data_min = pdr.get_data_yahoo(str(stock),start=startt, end=endt)
                    st1=time.time()
                    # tstartt=time.mktime(time.strptime(startt, '%Y-%m-%d'))
                    # tendt=time.mktime(time.strptime(endt, '%Y-%m-%d'))
                    Hist_data_min= Hist_data_min[Hist_data_min['Close'].notna()]
                    Hist_data_min= Hist_data_min[Hist_data_min['Volume'].notna()]
                    Hist_data_min= Hist_data_min[Hist_data_min['Low']>Hist_data_min['High']*0.2]
                    Hist_data_min['time']=[int(time.mktime(time.strptime(str(index)[0:19], '%Y-%m-%d %H:%M:%S'))) for index, row in Hist_data_min.iterrows()]
                    if Hist_data_min.shape[0]<self.period and Stock_Failure==0:raise ValueError
                    if Overwrite:Hist_data_min.to_csv(excel_dir,date_format='%Y-%m-%d %H:%M:%S')
                    # with pd.ExcelWriter(excel_dir,if_sheet_exists="replace",mode="w",) as writer:
                    #     Hist_data_min.to_excel(writer,sheet_name="RMP_%sto%s.csv" %(startt,endt))
                    #     writer.save()
                if i==0:treadmax=Hist_data_min['time'].max()-3600
                Hist_data_min=Hist_data_min[~Hist_data_min.index.duplicated(keep='last')]
                tend=int(time.mktime(time.strptime(str(Hist_data_min.last_valid_index())[0:19], '%Y-%m-%d %H:%M:%S')))
                tfir=int(time.mktime(time.strptime(str(Hist_data_min.first_valid_index())[0:19], '%Y-%m-%d %H:%M:%S')))
                if (tend-t0<1*24*3600) and i==0:
                    #Dt=Dt+24*3600
                    t0=t0-24*3600
                    tst=t0-Dt
                    Starttime=([int(time.localtime(tst)[0]),int(time.localtime(tst)[1]),int(time.localtime(tst)[2])])#([2020, 12, 16])
                    startt=str(Starttime[0])+"-"+str(Starttime[1])+"-"+str(Starttime[2])
                    continue
                Hist_data = Hist_data_min[ Hist_data_min['time']>=t0]
                Hist_data_full=Hist_data_min
                #Hist_data.dropna()
                n1=Hist_data.first_valid_index()
                n2=Hist_data.last_valid_index()
                if n1 and n2:
                    fi=Hist_data.at[n1,'Open']
                    la=Hist_data.at[n2,'Close']
                else:
                    int("error")
                rmax=0
                rmin=1e9
                MiniValue=1e9
                tclose=[]
                pclose=[]
                maxval=0

                self.t[stock]=Hist_data["time"].values.tolist()
                self.p[stock]=Hist_data["Close"].values.tolist()
                Hist_data["timeL"]=Hist_data["time"]-4*3600
                self.t[stock].extend(Hist_data["timeL"].values.tolist())
                self.p[stock].extend(Hist_data["Low"].values.tolist())
                Hist_data["timeH"]=Hist_data["time"]-2*3600
                self.t[stock].extend(Hist_data["timeH"].values.tolist())
                self.p[stock].extend(Hist_data["High"].values.tolist())
                rmax=Hist_data[Hist_data["time"]>t1-20*3600*24]['High'].max()
                rmin=Hist_data[Hist_data["time"]>t1-20*3600*4]['Low'].min()
                tclose=Hist_data["time"].values.tolist()
                pclose=Hist_data["Close"].values.tolist()
                idindex=Hist_data['Close'].idxmax()
                meanval=(Hist_data.loc[idindex,'Low']+Hist_data.loc[idindex,'Close'])/2
                imax=Hist_data.index.get_loc(idindex)
                pclose[imax]=meanval

                sort(self.t[stock],self.p[stock])
                row=Hist_data.tail(1)
                sizor=1-(abs(row['Close']-row['Open'])+(row['High']-row['Close']))/(row['High']-row['Low'])/2
                #print(stock+'_'+str(rmin)+' '+str(la)+'_'+str(rmax))
                x=np.array(tclose)
                x=x.reshape((-1, 1))
                y=[log10(pclose[ii]) for ii in range(len(pclose))]
                self.model[stock]=LinearRegression()
                self.model[stock].fit(x, y)
                average=10**self.model[stock].predict([[tend+30*24*3600]])[0]
                fic=10**self.model[stock].predict([[tend]])[0]
                maxh=fi
                minh=fi
                maxDiv=0
                inc=(average-fic)/fic+maxDiv
                tt=1/inc
                maxDivt=np.array([0.0,0.0,0.0])
                minDivt=np.array([0.0,0.0,0.0])
                minDiv=0
                drop=0
                tmini=0
                dailymovmax=0
                for index, row in Hist_data.iterrows():
                    tc=row['time']
                    tmax=tc
                    tmin=tmax-Dt
                    Hist_data_min=Hist_data_min[Hist_data_min['time']>tmin]
                    x=Hist_data_min[Hist_data_min['time']<=tmax]['time'].values
                    if len(x)==0:
                        Dt=Dt+24*3600
                        tst=t0-Dt
                        Starttime=([int(time.localtime(tst)[0]),int(time.localtime(tst)[1]),int(time.localtime(tst)[2])])#([2020, 12, 16])
                        startt=str(Starttime[0])+"-"+str(Starttime[1])+"-"+str(Starttime[2])
                        int("error")
                    dailymov=row['High']-row['Low']
                    if dailymov>dailymovmax:dailymovmax=dailymov
                    y=Hist_data_min[Hist_data_min['time']<=tmax]['Open'].values
                    x=np.append(x,Hist_data_min[Hist_data_min['time']<=tmax]['time'].values)
                    y=np.append(y,Hist_data_min[Hist_data_min['time']<=tmax]['Close'].values)
                    x=x.reshape((-1, 1))
                    y=[log10(y[ii]) for ii in range(len(y))]
                    model=LinearRegression().fit(x,y)
                    Div=(row['Close']-10**model.predict([[tc]])[0])/10**model.predict([[tc]])[0]
                    for jj in range(3):
                        if Div>maxDivt[jj]:
                            if jj!=2:maxDivt[jj+1]=maxDivt[jj]
                            maxDivt[jj]=Div
                            break
                    Div=(row['Low']-10**model.predict([[tc]])[0])/10**model.predict([[tc]])[0]
                    for jj in range(3):
                        if Div<minDivt[jj]:
                            if jj!=2:minDivt[jj+1]=minDivt[jj]
                            minDivt[jj]=Div       
                            if jj==0:tmini=tc
                            break
                    if row['High']>=maxh:
                        maxh=row['High']
                    else:
                        minh=row['Close']
                        if drop<(maxh-minh)/10**model.predict([[tc]])[0]:
                            drop=(maxh-minh)/10**model.predict([[tc]])[0]
                minDiv=sum(minDivt[1:])/2
                maxDiv=maxDivt[1]
                
                PPolin=ppo(Hist_data_full['Close'])
                Dppo=PPolin-ppo_signal(Hist_data_full['Close'])
                
                MA=SMAIndicator(Hist_data_full['Close'],10).sma_indicator()-SMAIndicator(Hist_data_full['Close'],20).sma_indicator()
                risk='Low'
                if (la-fic)/fic-minDivt[0]<=0.02:
                    risk='High'
                if  t1-tmini<3*24*3600:
                    risk='High'
                try:
                    ROC1=ROC(Hist_data_full['Close'])
                    self.ROC.append(ROC1.roc()[-1])
                except:
                    self.ROC.append(0)
                try:
                    indicator_bb = BollingerBands(close=Hist_data_full["Close"], window=20, window_dev=2)
                    h=indicator_bb.bollinger_hband()[-1]
                    l=indicator_bb.bollinger_lband()[-1]
                    self.Stoch.append((la-l)/(h-l+0.00001))
                except:
                    self.Stoch.append((la-rmin)/(rmax-rmin+0.00001)) 
                try:
                    adxI = ADXIndicator(Hist_data_full['High'],Hist_data_full['Low'],Hist_data_full['Close'],20)
                    self.ADX.append(adxI.adx()[-1])
                except:
                    self.ADX.append(1)
                try:
                    adxI = ADXIndicator(Hist_data_full['High'],Hist_data_full['Low'],Hist_data_full['Close'],20)
                    self.DADX.append(adxI.adx_pos()[-1]-adxI.adx_neg()[-1])
                except:
                    self.DADX.append(-1)
                # try:
                #     RSIvalu = StocO(Hist_data_full['High'],Hist_data_full['Low'],Hist_data_full['Close'])
                #     self.Stoch.append(RSIvalu.stoch()[-1]/100)
                # except:
                #     self.Stoch.append((la-rmin)/(rmax-rmin+0.00001)) 
                self.Riskflag.append(risk)
                Progbar=stock+' '+flag+'   '+str(int((average-fic)/fic*1000)/1000)
                for j in range(len(Progbar),30):Progbar+=' '
                Progbar+='<'
                
                for j in range(40):
                    if j<progress or j==rev: Progbar+='#'
                    else:Progbar+=' '
                Progbar+='>'
                print(Progbar) 
                self.PPO.append(Dppo[-1])
                self.PPOSum.append(Dppo[-10:].mean())
                self.ValuInc.append(inc)
                self.tickInc.append(i-1)
                self.sizor.append(sizor)
                self.MAV.append(MA[-1])
                self.dailymove.append(dailymovmax/fic)
                self.aver.append((average-fic)/fic)
                self.first.append(fi)
                self.volume.append(Hist_data[Hist_data['time']>t1-3600*24*14]['Volume'].mean())
                self.Dvolume.append(Hist_data[Hist_data['time']>t1-3600*24*14]['Volume'].mean()-Hist_data[Hist_data['time']>t1-3600*24*50]['Volume'].mean())
                self.lastav.append(fic)
                self.last.append((la-fic)/fic)
                self.Maxdrop.append(-1*drop) 
                self.maximum.append(maxDiv) #Maximum with respect to avergae trend line
                self.minimum.append(minDiv) #Min with respect to avergae trend line
                #Hist_data.to_csv("C:\\Users\\sista\\Desktop\\fund\\results\\results.csv")  # Saves the historical data in csv format for further processing later
                Amount_of_API_Calls += 1 
                Stock_Failure = 0
                i += 1  # Iteration to the next ticker
            except:# ValueError or RuntimeError or HTTPError:
                print("Yahoo Finance Back-end Error for %s, Attempting to Fix" % stock)  # An error occurred on Yahoo Finance's back-end. We will attempt to retreive the data again
                #time.sleep(2)
                if Stock_Failure > 1:  # Move on to the next ticker if the current ticker fails more than 5 times
                    Stocks_Not_Imported += 1               
                    self.first.append(float("NaN"))
                    self.lastav.append(float("NaN"))
                    self.last.append(float("NaN"))
                    self.Maxdrop.append(float("NaN")) 
                    self.aver.append(float("NaN"))
                    self.maximum.append(float("NaN"))
                    self.minimum.append(float("NaN"))
                    self.Riskflag.append('High')
                    self.ValuInc.append(-1)
                    self.Stoch.append(float("NaN"))
                    self.tickInc.append(i-1)
                    self.ADX.append(0)
                    self.ROC.append(0)
                    self.p[stock].append(0)
                    self.t[stock].append(0)
                    self.MAV.append(0)
                    self.dailymove.append(0)
                    self.DADX.append(-1)
                    self.volume.append(0)
                    self.Dvolume.append(0)
                    self.sizor.append(1)
                    self.PPO.append(0)
                    self.PPOSum.append(0)
                    i+=1
                Amount_of_API_Calls += 1
                Stock_Failure += 1
        self.Stocks_Imported =i - Stocks_Not_Imported
        print("The amount of stocks we successfully imported: " + str(i - Stocks_Not_Imported))
        if len(self.ADX)!=len(self.first):int('ERR')
    # return ValuInc,tickInc,maximum,minimum,first,last,aver,Maxdrop,lastav
def marketPredict(tbuy,tickerss,Pe,Days):
    #tickersIn='^DJI'
    #preselection second layer thelast 10-11 monthes
    testdomai=0
    MPeriod=Pe
    IndexNames={'BTC-USD':"Bitcoin",'^GSPC':"S&P 500",'^DJI':"Dow Jones",'^IXIC':"NASDAQ Composite"}
    #tickerss=['Futu','BILI','ABNB','EXPI',]
    Endtime=([int(time.localtime(tbuy)[0]),int(time.localtime(tbuy)[1]),int(time.localtime(tbuy)[2])])
    tsta=tbuy-MPeriod*30*24*3600
    Starttime = ([int(time.localtime(tsta)[0]),int(time.localtime(tsta)[1]),int(time.localtime(tsta)[2])])#([2020, 12, 16])
    startt=str(Starttime[0])+"-"+str(Starttime[1])+"-"+str(Starttime[2])
    endt=str(Endtime[0])+"-"+str(Endtime[1])+"-"+str(Endtime[2])
    yfIn=buildyf(startt,endt,'1d')
    yfIn.callyf(tickerss,'download')
    ii=0
    jj=0
    le=int((len(tickerss))**0.5)
    fig, ax = plt.subplots(le, int(len(tickerss)/le-0.001)+1, constrained_layout=True,figsize=(19,9.5),clear=True)
    fig2, ax2 = plt.subplots(le, int(len(tickerss)/le-0.001)+1,  constrained_layout=True,figsize=(19,9.5),clear=True)
    plt.ion()
    next5={}
    for tickersIn in tickerss:
        tim=yfIn.t[tickersIn][testdomai*3:]
        pri=yfIn.p[tickersIn][testdomai*3:]
        tim.reverse()
        pri.reverse()
        Stocht=[]
        Stochp=[]
        Stochp2=[]
        StochpS=[]
        StochtS=[]
        Stochpy=[]
        Stochpy2=[]
        Stochp_Ger=[]
        Stocha=0
        Stochtf=[]
        StochRP=[]
        Stochpf=[]
        Stochpf2=[]
        Stochpf_Ger=[]
        Stochpfy=[]
        Wind=20
        yday=1
        smooth=3
        from ta.momentum import StochasticOscillator as StocO
        
        for i in range(Wind*3,len(tim)+1,3):
            maxval=max(pri[i-Wind*3:i])
            minval=min(pri[i-Wind*3:i])
            last=pri[i-1]
            Stochtf.append(tim[i-1])
            stocha_Pre=Stocha
            Stocha=(last-minval)/(maxval-minval)
            Stochpf.append(Stocha)
            Stochpf_Ger.append(Stocha-stocha_Pre)
        SlowV=sum(Stochpf[0:3])/3
        for i in range(3,len(Stochpf)):
            SlowV_Pre=SlowV
            SlowV=sum(Stochpf[i-2:i+1])/3
            Stocht.append(Stochtf[i])
            Stochp.append(SlowV)
            Stochp_Ger.append(SlowV-SlowV_Pre)
        SlowV=sum(Stochp[0:3])/3
        
        for i in range(3,len(Stochp)-yday):
            SlowV_Pre=SlowV   
            SlowV=sum(Stochp[i-2:i+1])/3
            if Stochp_Ger[i]>=0:Stochp2.append(Stochp[i])
            else:Stochp2.append(Stochp[i]*-1)
            Stochpy.append(Stochp[i+yday])
            Stochpy2.append(sum(Stochp[i-2+yday:i+1+yday])/3)
            StochtS.append(Stocht[i])
            if Stochpf_Ger[i+3]>=0:Stochpf2.append(Stochpf[i+3])
            else:Stochpf2.append(Stochpf[i+3]*-1)
            Stochpfy.append(Stochpf[i+3+yday])
        #    Stochp_Ger2.append(int(Stochp_Ger[lastn]*10)*10)
            if(SlowV-SlowV_Pre)>=0:StochpS.append(SlowV)
            else:StochpS.append(SlowV*-1)
            StochRP.append(pri[(i+Wind+3)*3-1]/last)
        #    StochpS.append(int(SlowV*10)*10) 
        #    StochpS_Ger.append(int((SlowV-SlowV_Pre)*10)*10)
        
        close=pd.DataFrame([])
        close["t"]=yfIn.t[tickersIn][testdomai*3::3]
        close["p"]=yfIn.p[tickersIn][testdomai*3::3]
        close["pl"]=yfIn.p[tickersIn][testdomai*3+2::3]
        close["ph"]=yfIn.p[tickersIn][testdomai*3+1::3]
        close.sort_values(by= "t" ,inplace=True)
        close=close.set_index("t" )
        indicator_bb = BollingerBands(close=close["p"], window=20, window_dev=2)
        close["h"]=indicator_bb.bollinger_hband()
        close["l"]=indicator_bb.bollinger_lband()
        close["stoB"]=(close["p"]-close["l"])/(close["h"]-close["l"])
        close["m"]=indicator_bb.bollinger_mavg()
        close["m"]=(close["m"]-close.shift(periods=1)["m"])/(close["m"]-close.shift(periods=20)["m"])
        SMAIndicator(close["p"],10).sma_indicator()
        close["PPO"]=ppo(close["p"])
        close["Stochf"]=StocO(high=close["ph"],low=close["pl"], close=close["p"],  window=Wind,fillna=True).stoch()/100
        close["Stochm"]=close["Stochf"].rolling(smooth).mean()
        close["Stochs"]=close["Stochm"].rolling(smooth).mean()
        # close["max"]=close["p"].rolling(Wind).max()
        # close["min"]=close["p"].rolling(Wind).min()
        #close["Stochs"]=StocO(high=close["ph"],low=close["pl"], close=close["p"],  window=Wind-4,fillna=True).stoch()/100
        
        close["Stochf"]=close["Stochf"].diff()/abs(close["Stochf"].diff())*close["Stochf"] 
        close["Stochm"]=close["Stochm"].diff()/abs(close["Stochm"].diff())*close["Stochm"]        
        close["Stochs"]=close["Stochs"].diff()/abs(close["Stochs"].diff())*close["Stochs"]
        
        sizedf=close.shape[0]-(len(Stochp)-3)
        

        #close=close.drop(close.index[0:sizedf]).fillna(0) #.round(2)
        close=close.dropna()
        
        last=close["p"].iloc[-1]
        
        x3=close["stoB"].tolist()[:-yday]
        x4=close["m"].tolist()[:-yday]
        
        x0=close["Stochf"].tolist()[:-yday]
        x1=close["Stochm"].tolist()[:-yday]
        x2=close["Stochs"].tolist()[:-yday]
        
        pl=close["p"].tolist()[:-yday]
        # pmax=close["max"].tolist()[:-yday]
        # pmin=close["min"].tolist()[:-yday]
		
        
        # xt01 = np.float64(np.column_stack((Stochpf2,Stochp2)))#Stochpf2,Stochp2
        # xt12 = np.float64(np.column_stack((Stochp2,StochpS)))
        # xt012 = np.float64(np.column_stack((Stochpf2,Stochp2,StochpS)))
        xt01 = np.round(np.float64(np.column_stack((x0,x2))), decimals=2)#Stochpf2,Stochp2
        xt12 = np.round(np.float64(np.column_stack((x1,x2))), decimals=2)
        xt012 = np.round(np.float64(np.column_stack((x0,x1,x2))), decimals=2)
        # xt = np.round(np.float64(np.column_stack((pl,pmax,pmin))), decimals=2)        
        
        
        # xt01=np.round(xt01, 3)
        # xt12=np.round(xt12, 3)
        # xt012=np.round(xt012, 3)
        
        yt0=np.array(abs(close["Stochf"]).tolist()[1:], dtype=float)
        yt1=np.array(abs(close["Stochm"]).tolist()[1:], dtype=float)
        yt2=np.array(abs(close["Stochs"]).tolist()[1:], dtype=float)

        
        # yt0=np.array(Stochpfy, dtype=float)
        # yt1=np.array(Stochpy, dtype=float)
        # yt2=np.array(Stochpy2, dtype=float)
        # yt0=np.round(yt0, 3)
        # yt1=np.round(yt1, 3)
        # yt2=np.round(yt2, 3)        
        
        xlimits = np.array([[-1.0, 1.0],[-1.0, 1.0]])
        

        #sm0 = RBF(d0=4)
        #sm01 = RBF(d0=4)
        # sm12 = RBF(d0=4)
        # sm2 = RBF(d0=4)  
        sm0 = IDW(p=3.5,print_global=False)
        sm01 = IDW(p=3.5,print_global=False)
        sm12 = IDW(p=3.5,print_global=False)
        sm2 = IDW(p=3.5,print_global=False)  
        #sm0 = RMTB(xlimits=xlimits, order=3,  regularization_weight=1e-10,)
        # sm01 = RMTB(xlimits=xlimits, order=3,   regularization_weight=1e-10,)
        # sm12 = RMTB(xlimits=xlimits, order=3,   regularization_weight=1e-10,)
        # sm2 = RMTB(xlimits=xlimits, order=3,   regularization_weight=1e-10,)
        
        X_train, X_test, y_train, y_test = train_test_split(xt01,yt0, test_size=0.20, random_state=101)
        sm0.set_training_values(X_train, y_train) 
        sm0.train()
        predictions = sm0.predict_values(X_test)
        predictions =[row for row in predictions.T][0]

        y_test2=[yte-abs(xte[0]) for yte,xte in zip(y_test,X_test)]
        predictions2=[yte-abs(xte[0]) for yte,xte in zip(predictions,X_test)]
        #from sklearn.metrics import r2_score
        R2=[1 if (yte-abs(xte[0]))/(ytr-abs(xte[0]))>0 else 0 for yte,ytr,xte in zip(y_test,predictions,X_test)]
        R2=sum(R2)/len(R2)
        next5[tickersIn]=[R2]   
        
        sm0.set_training_values(xt01,yt0)
        sm01.set_training_values(xt01, yt1) 
        sm12.set_training_values(xt12, yt1)
        sm2.set_training_values(xt12, yt2)
        if len(xt01)==0:
            np.zerro
            next5[tickersIn]=[-1 for i in range(Days)] 
            continue
        sm0.train()
        sm01.train()
        sm12.train()
        sm2.train()
        i+=yday
        StochRP.append(pri[(i+Wind+3)*3-1]/last)
        if Stochpf_Ger[i+3]>=0:x0=Stochpf[i+3]
        else:x0=Stochpf[i+3]*-1
        if Stochp_Ger[i]>=0:x1=Stochp[i]
        else:x1=Stochp[i]*-1
        SlowV_Pre=SlowV   
        SlowV=sum(Stochp[i-2:i+1])/3
        if(SlowV-SlowV_Pre)>=0:x2=SlowV
        else:x2=SlowV*-1
        


        x0=close["Stochf"].tolist()[-yday]
        x1=close["Stochm"].tolist()[-yday]
        x2=close["Stochs"].tolist()[-yday]
        
        x4=close["m"].tolist()[-yday]

        x01=np.array([[x0,x2]])                
        x012=np.array([[x0,x1,x2]])
        x12=np.array([[x1,x2]])
        
        # x01=np.round(x01, 3)
        # x012=np.round(x012, 3)
        # x12=np.round(x12, 3)
        
        
        StochtS.append(Stocht[i])
        StochpS.append(x2)
        Stoch_predif=[abs(x1)]
        Stoch_predis=[abs(x2)]
        Stoch_predisff=[abs(x0)]
        Stoch_predit=[Stocht[i]]
        Prise_predit=[1]
        Stochp2.append(x1)
        Stochpf2.append(x0)
        #next5[tickersIn].append(x0)
        next5[tickersIn].append(0)
        Rph=close["ph"].iloc[-1]/close["p"].iloc[-1]
        Rpl=close["pl"].iloc[-1]/close["p"].iloc[-1]
        for i in range(Days):
            # xold12=x12
            # xold01=x01
            
            x1=(sm12.predict_values(x12)[0][0]+sm01.predict_values(x01)[0][0])/2
            x2=sm2.predict_values(x12)[0][0]
            x0=sm0.predict_values(x01)[0][0]
            
            #x0=3*(x1-abs(xold01[0][1]))+Stochpf[-3]
            p0=x0*(maxval-minval)+minval
            for j in range(3):pri.append(p0)
            Prise_predit.append(p0/last)
            tt=Stocht[-1]+24*3600*(i+1)
            
            #x0=sm0.predict_values(x01)[0][0]
            maxval=max(pri[-Wind*3:-1])
            minval=min(pri[-Wind*3:-1])   
            # if x0-abs(xold01[0][0])<0:x0=x0*-1
            # if x1-abs(xold12[0][0])<0:x1=x1*-1
            # if x2-abs(xold12[0][1])<0:x2=x2*-1
            
            close.loc[tt]=[p0,p0*Rpl,p0*Rph,0,0,0,0,0,x0,x1,x2]
            close["PPO"]=ppo(close["p"])
            indicator_bb = BollingerBands(close=close["p"], window=20, window_dev=2)
            close["h"]=indicator_bb.bollinger_hband()
            close["l"]=indicator_bb.bollinger_lband()
            close["stoB"]=(close["p"]-close["l"])/(close["h"]-close["l"])
            close["m"]=indicator_bb.bollinger_mavg()
            close["m"]=(close["m"]-close.shift(periods=2)["m"])*100/close["m"]
            
            close["Stochf"]=StocO(high=close["ph"],low=close["pl"], close=close["p"],  window=Wind,fillna=True).stoch()/100
            close["Stochm"]=close["Stochf"].rolling(smooth).mean()
            close["Stochs"]=close["Stochm"].rolling(smooth).mean()
            
            close["Stochf"]=close["Stochf"].diff()/abs(close["Stochf"].diff())*close["Stochf"] 
            close["Stochm"]=close["Stochm"].diff()/abs(close["Stochm"].diff())*close["Stochm"]        
            close["Stochs"]=close["Stochs"].diff()/abs(close["Stochs"].diff())*close["Stochs"]

            x0=close["Stochf"].tolist()[-yday]
            x1=close["Stochm"].tolist()[-yday]
            x2=close["Stochs"].tolist()[-yday]

            
            x3= close["stoB"].tolist()[-yday]
            x4= close["m"].tolist()[-yday]
            
            x01=np.array([[x0,x2]])
            x12=np.array([[x1,x2]])
            x012=np.array([[x0,x1,x2]])
            
            # x01=np.round(x01, 2)
            # x012=np.round(x012, 2)
            # x12=np.round(x12, 2)
            
            next5[tickersIn].append((p0-last)/last)
            Stoch_predif.append(abs(x1))
            Stoch_predisff.append(abs(x0))
            Stochpf.append(x0)
            Stoch_predis.append(abs(x2))
            Stoch_predit.append(Stocht[-1]+24*3600*(i+1))
            #print(str(x1)+' '+str(x2))
        sd=lambda d : (d-Stocht[-1])/3600/24
        td=list(map(sd,Stocht))
        ax[ii][jj].plot(td,abs(np.array(Stochp)))
        td=list(map(sd,StochtS))
        ax[ii][jj].plot(td,abs(np.array(StochpS)))
        ax2[ii][jj].plot(td,abs(np.array(StochRP))) 
        ax[ii][jj].plot(td,abs(np.array(Stochpf2))) 
        td=list(map(sd,Stoch_predit))
        ax[ii][jj].plot(td,Stoch_predif,'r' )
        ax[ii][jj].plot(td,Stoch_predis)
        ax[ii][jj].plot(td,Stoch_predisff) 
        ax2[ii][jj].plot(td,Prise_predit) 
        ax[ii][jj].set_xlim([-50, 10])
        ax[ii][jj].set_ylim([0.0, 1.1])
        try:
            ax[ii][jj].set_title(IndexNames[tickersIn]+': Price '+str(round(last))+'$ R2='+str(R2))
            ax2[ii][jj].set_title(IndexNames[tickersIn]+': Price '+str(round(last))+'$ R2='+str(R2))
        except:
            ax[ii][jj].set_title(tickersIn+': Price '+str(round(last))+'$ R2='+str(R2))
            ax2[ii][jj].set_title(tickersIn+': Price '+str(round(last))+'$ R2='+str(R2))
 
        ax[ii][jj].grid()
        ax2[ii][jj].grid()
        ii+=1
        if ii==le:
            jj+=1
            ii=0
    # # =============================================================================
    #---------------------------------------------
#     tim=yfIn.t[tickersIn]
#     pri=yfIn.p[tickersIn]
#     tim.reverse()
#     pri.reverse()
#     Stocht=[]
#     Stochp=[]
#     Stochp2=[]
#     StochpS=[]
#     StochtS=[]
#     Stochpy=[]
#     Stochpy2=[]
#     Stochp_Ger=[]
#     Stocha=0
#     Stochtf=[]
#     StochRP=[]
#     Stochpf=[]
#     Stochpf2=[]
#     Stochpf_Ger=[]
#     Stochpfy=[]
#     for i in range(14*3,len(tim)+1,3):
#         maxval=max(pri[i-14*3:i])
#         minval=min(pri[i-14*3:i])
#         last=pri[i-1]
#         Stochtf.append(tim[i-1])
#         stocha_Pre=Stocha
#         Stocha=(last-minval)/(maxval-minval)
#         Stochpf.append(Stocha)
#         Stochpf_Ger.append(Stocha-stocha_Pre)
#     SlowV=sum(Stochpf[0:3])/3
#     for i in range(3,len(Stochpf)):
#         SlowV_Pre=SlowV
#         SlowV=sum(Stochpf[i-2:i+1])/3
#         Stocht.append(Stochtf[i])
#         Stochp.append(SlowV)
#         Stochp_Ger.append(SlowV-SlowV_Pre)
#     SlowV=sum(Stochp[0:3])/3
#     for i in range(3,len(Stochp)):
#         SlowV_Pre=SlowV   
#         SlowV=sum(Stochp[i-2:i+1])/3
#         if Stochp_Ger[i]>=0:Stochp2.append(Stochp[i])
#         else:Stochp2.append(Stochp[i]*-1)
#         StochtS.append(Stocht[i])
#         if Stochpf_Ger[i]>=0:Stochpf2.append(Stochpf[i+3])
#         else:Stochpf2.append(Stochpf[i+3]*-1)
#     #    Stochp_Ger2.append(int(Stochp_Ger[lastn]*10)*10)
#         if(SlowV-SlowV_Pre)>=0:StochpS.append(SlowV)
#         else:StochpS.append(SlowV*-1)
#         StochRP.append(pri[(i+14+3)*3-1]/last)
#     #    StochpS.append(int(SlowV*10)*10) 
#     #    StochpS_Ger.append(int((SlowV-SlowV_Pre)*10)*10)
#     Stoch_predif=[]
#     Stoch_predis=[]
#     Stoch_predisff=[]
#     Stoch_predit=[]
#     Prise_predit=[]
#     Prise_real=[]
#     rsquerd=[]
#     Prise_real2=[]
#     pda=2
#     for i in range(len(Stochp2)-testdomai,len(Stochp2)-pda):
#         x0=Stochpf2[i]
#         x1=Stochp2[i]
#         x2=StochpS[i]
#         for hh in range(pda):
#             x012=np.array([[x0,x1,x2]])
#             x01=np.array([[x0,x1]])
#             x12=np.array([[x1,x2]])
#             xold12=x12
#             xold01=x01
#             x0=sm0.predict_values(x01)[0][0]
#             x1=(sm12.predict_values(x12)[0][0]+sm01.predict_values(x01)[0][0])/2
#             x2=sm2.predict_values(x12)[0][0]
#             if x0<abs(xold01[0][0]):x0=x0*-1
#             if x1<abs(xold01[0][1]):x1=x1*-1
#             if x2<abs(xold12[0][1]):x2=x2*-1
#         hh+=1
#         maxval=max(pri[(i+3+3+hh)*3-1:(i+14+3+3+hh)*3])
#         minval=min(pri[(i+3+3+hh)*3-1:(i+14+3+3+hh)*3])
#         #x0=3*(x1-abs(xold01[0][1]))+abs(Stochpf2[i-3])
#         #x00=3*(x1-abs(xold01[0][1]))+abs(Stochpf2[i-3])
#         p0=abs(x0)*(maxval-minval)+minval
#         Prise_predit.append(p0/last)
#         if (p0-StochRP[i]*last)*(StochRP[i+hh]-StochRP[i])>0:ff=1
#         else:ff=0
#         rsquerd.append(ff)
#         #rsquerd.append(((abs(x0)-abs(Stochpf2[i+hh]))**2+(abs(x1)-abs(Stochp2[i+hh]))**2)**0.5)
#         Stoch_predif.append(abs(x1))
#         Stoch_predisff.append(abs(x0))
#         Stoch_predis.append(abs(x2))
#         Stoch_predit.append(StochtS[i+hh])
#         Prise_real.append(abs(Stochp2[i+hh]))
#         Prise_real2.append(abs(StochRP[i+hh]))
#         print(str(x1)+' '+str(x2))
#     sd=lambda d : (d-Stoch_predit[0])/3600/24
#     td=list(map(sd,Stoch_predit))
#     fig, ax = plt.subplots(2, 1, constrained_layout=True,figsize=(19,9.5),clear=True)
#     ax[0].plot(td,abs(np.array(rsquerd)))
#     ax[0].plot(td,abs(np.array(Stoch_predif)), 'o')
#     ax[0].plot(td,abs(np.array(Prise_real)))
#     ax[0].set_xlim([0.0, 60.0])
#     ax[0].set_ylim([0, 1])
#     ax[0].set_title(sum(rsquerd)/len(rsquerd))
#     ax[0].grid()
#     minor_ticks = np.arange(0, 90, 2)
#     ax[0].set_xticks(minor_ticks, minor=True)
#     ax[1].plot(td,abs(np.array(Prise_predit)), 'o',label='Forcast')
#     ax[1].plot(td,abs(np.array(Prise_real2)),label='Market Price')
#     ax[1].set_xlim([0.0, 90.0])
#     ax[1].legend()
#     ax[1].set_xticks(minor_ticks, minor=True)
#     ax[1].set_xlabel('time (day)', fontsize=14)
#     ax[1].tick_params(axis='y', labelsize=14)
#     ax[1].set_ylabel('Normalized Price (-)', fontsize=14)
#     ax[1].tick_params(axis='x', labelsize=14)
# #    ax[1].set_ylim([0, 1])
#     ax[1].set_title('2 Days forcast for '+tickersIn, fontsize=14)
#     ax[1].grid(which='minor', alpha=0.2)
#     ax[1].grid(which='major', alpha=0.5)
#    =============================================================================
    return next5#Stochpf2

    
# capital=20000
# import random
# minl=-1e9
# Minlost=[]
# for i in range(100000):
#     coeff=[]
#     lost=Benefit=0
#     benefit=0
#     Residu=1
#     for j in range(reg):
#         ran=int(random.random()*10)/10
#         tt=(ran*Residu if j<(reg-1) else Residu)
#         coeff.append(tt)        
#         Residu=Residu-tt
#         minall=df1wk.loc[df1wk.head(reg).index.values[j],'Min Of all']
#         maxir=min(df1wk.loc[df1wk.head(reg).index.values[j],'Max based on 1month'],df1wk.loc[df1wk.head(reg).index.values[j],'Max based on MPonth'])
#         Lastre=df1wk.loc[df1wk.head(reg).index.values[j],"last"]
#         #lost=lost+df1m.loc[df1wk.head(reg).index.values[j],"minimum"]*tt*tt*capital+tt*0.002
#         lost=lost+(minall-Lastre)/Lastre*tt*capital
#         Benefit=Benefit+(maxir-Lastre)/Lastre*tt*capital
#     maxcoef=max(coeff)
#     lost=lost-maxcoef*capital
#     if Benefit+lost>minl:
#         minl=Benefit+lost
#         Minlost=coeff.copy()
# minl=-1e9
# Minlost=[]
# for i in range(10000):
#     coeff=[]
#     lost=0
#     benefit=0
#     Residu=1
#     for j in range(reg-1):
#         tt=random.random()*Residu
#         coeff.append(tt)
#         Residu=Residu-tt
#         #lost=lost+df1m.loc[df1wk.head(reg).index.values[j],"minimum"]*tt*tt*capital+tt*0.002
#         lost=lost+(+df1m.loc[df1wk.head(reg).index.values[j],"Min expected in 1m"]-df1m.loc[df1wk.head(reg).index.values[j],"last"])/df1m.loc[df1wk.head(reg).index.values[j],"last"]*tt*capital
#     tt=Residu
#     j+=1
#     coeff.append(tt)
#     #lost=lost+df1m.loc[df1wk.head(reg).index.values[j],"minimum"]*tt*tt*capital+tt*0.002
#     lost=lost+(df1m.loc[df1wk.head(reg).index.values[j],"Min expected in 1m"]-df1m.loc[df1wk.head(reg).index.values[j],"last"])/df1m.loc[df1wk.head(reg).index.values[j],"last"]*tt*capital
#     if minl<lost:
#         minl=lost
#         Minlost=coeff.copy()
# print('min Lost for '+str(capital)+'Chf capital: '+str(minl))
# buyrecom=[]
# for j in range(reg):
#     print(df1wk.head(reg).index.values[j],int(Minlost[j]*capital/100)*100)
#     buyrecom.append(int(Minlost[j]*capital/100)*100)
# df1wk['Buy recommend based on 1m']=buyrecom
# df1wk.to_csv(pathd+"\\R1w%sto%s.csv" %(startt,endt))

# minl=-1e9
# Minlost=[]
# for i in range(10000):
#     coeff=[]
#     lost=0
#     benefit=0
#     Residu=1
#     for j in range(reg-1):
#         tt=random.random()*Residu
#         coeff.append(tt)
#         Residu=Residu-tt
#         #lost=lost+df2m.loc[df1wk.head(reg).index.values[j],"minimum"]*tt*tt*capital+tt*0.002
#         lost=lost+(+df2m.loc[df1wk.head(reg).index.values[j],"Min expected in 1m"]-df2m.loc[df1wk.head(reg).index.values[j],"last"])/df2m.loc[df1wk.head(reg).index.values[j],"last"]*tt*capital
#     tt=Residu
#     j+=1
#     coeff.append(tt)
#     #lost=lost+df2m.loc[df1wk.head(reg).index.values[j],"minimum"]*tt*tt*capital+tt*0.002
#     lost=lost+(df2m.loc[df1wk.head(reg).index.values[j],"Min expected in 1m"]-df2m.loc[df1wk.head(reg).index.values[j],"last"])/df2m.loc[df1wk.head(reg).index.values[j],"last"]*tt*capital
#     if minl<lost:
#         minl=lost
#         Minlost=coeff.copy()
# print('min Lost for '+str(capital)+'Chf capital: '+str(minl))
# buyrecom=[]
# for j in range(reg):
#     print(df1wk.head(reg).index.values[j],int(Minlost[j]*capital/100)*100)
#     buyrecom.append(int(Minlost[j]*capital/100)*100)
# df1wk['Buy recommend based on 2m']=buyrecom
# df1wk.to_csv(pathd+"\\R1w%sto%s.csv" %(startt,endt))

#tick = YFin(tickers)
#print(tickers[:5])
#tickers = ['BILI',"ccep","NIO","NVS"]
#tickers = gt.get_tickers_by_region(Region.EUROPE,mktcap_min=Mincap,mktcap_max=maxcap,country='Switzerland')
#tick = YFin(tickers)
#yy=tick.get_market_cap()
#---------------------------------------------------------------------------
# tickerstem=tickers.copy()
# tick = YFin(tickers)
# CapM=tick.get_market_cap()
# for stock in tickerstem:    
#     if tick.get_market_cap():
#         if CapM[stock]<Mincap*1e6:
#             tickers.remove(stock)
#         elif maxcap!=None and CapM[stock]>maxcap*1e6:
#             tickers.remove(stock)
#     else:
#         tickers.remove(stock)
#------------------------------------------------------------------------
# from symfit import parameters, variables, sin, cos, Fit
# import numpy as np
# import matplotlib.pyplot as plt

# def fourier_series(x, f, n=0):
#     """
#     Returns a symbolic fourier series of order `n`.

#     :param n: Order of the fourier series.
#     :param x: Independent variable
#     :param f: Frequency of the fourier series
#     """
#     # Make the parameter objects for all the terms
#     a0, *cos_a = parameters(','.join(['a{}'.format(i) for i in range(0, n + 1)]))
#     sin_b = parameters(','.join(['b{}'.format(i) for i in range(1, n + 1)]))
#     # Construct the series
#     series = a0 + sum(ai * cos(i * f * x) + bi * sin(i * f * x)
#                      for i, (ai, bi) in enumerate(zip(cos_a, sin_b), start=1))
#     return series

# x, y = variables('x, y')
# w, = parameters('w')
# model_dict = {y: fourier_series(x, f=w, n=30)}
# fit = Fit(model_dict, x=yf2m.t[SS], y=yf2m.p[SS])    
# fit_result = fit.execute()
# print(fit_result)
# plt.plot(yf2m.t[SS], yf2m.p[SS])
# plt.plot(yf2m.t[SS], fit.model(x=np.array(yf2m.t[SS]), **fit_result.params).y, color='green', ls=':')
 # Mincap = int(input("Minimum Market cap to be considered?") or 5000)
# flag3y = input("Run 3y Analysis filter?(Yes/No)" or 'Yes')
# flagDel = input("Delet previous folder(Yes/No)?" or 'Yes' )   