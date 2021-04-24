from binance.client import Client
import json
import numpy as np
from  util.SuperTrend import SuperTrend
from  util.TillsonT3 import TillsonT3
from ftxOpt.FTXClient import FtxClient
from time import sleep
import datetime
class FTXOperation:
    superTrend =None
    tillsonT3=None
    ftx=None
    confList={}
    isMailAktif=False
    def __init__(self):
        print('start')
        self.confList = self.readConfFile("FTXConf")
        self.superTrend = SuperTrend()
        self.tillsonT3 = TillsonT3()
        self.ftx =FtxClient(self.confList["api-key"], self.confList["api-secret"])

    def start(self):
        if(self.isMailAktif==False):
            # pythondan supertrend okuyan kısım
            while True:
                
                signal = self.getSignalSuperTrend(self.confList["local-opt"])
                self.getSignalTillsonT3(self.confList["local-opt"])
                self.tradeOperationLocal(self.confList["local-opt"],signal)
                sleep(5)

        if(self.isMailAktif==False):
            #gmail üzerinden trading viewden gelen mail ile al sat yapan kısım
            for conf in self.confList:
                if(conf["isAktif"]):
                    while True:    
                        orderType=self.readGmail(conf)
                        self.tradeOperation(orderType,conf)
                    sleep(10)

    def sell(self,coinName,coinIndex):
        market = self.ftx.list_markets()
        mm = self.ftx.get_balances()
        coin_index = [ x['coin'] for x in mm ].index(coinIndex)
        coin_balance  = mm[coin_index]['total']
        try:
            tt=self.ftx.place_order(coinName,'sell',None,coin_balance,'market')
            print("sell response:"+str(tt))
        except:
            print("sell balance too small: "+coin_balance)
        

    def buy(self,coinName,coinIndex):
        balance = self.getCoinBalances("USDT")
        if(balance>0.01):
            tt = self.ftx.place_order(coinName,'buy',None,balance*100,'market')
            print("buy response:"+str(tt))
        else:
            print("not enough balance:"+str(balance))
    def getCoinBalances(self,coinName: str):
        market = self.ftx.list_markets()
        mm = self.ftx.get_balances()
        coin_balance=0
        try:
            coin_index = [ x['coin'] for x in mm ].index(coinName)
            coin_balance  = mm[coin_index]['total']
            if coinName != 'USDT':
                coinPrice = market[[ x['name'] for x in market ].index(coinName+"/USDT")]["price"]
                print(f'coinName {coinName} ,  coinPrice {coinPrice}')
        except ValueError:
            print(coinName+' can''t found ')
        return coin_balance

    def convert(self,fromcoinName,toCoinName):
         balance = self.getCoinBalances(ftx,fromcoinName)
         if balance == 0 :
             print('miktar yok')
             return
         
         convertResponse = ftx.convert(fromcoinName,toCoinName,balance)
         print(ftx.convert_status(convertResponse['quoteId']))
         ftx.convert_accept(convertResponse['quoteId'])
         print(ftx.convert_status(convertResponse['quoteId']))

    def readConfFile(self,fileName):
        count = 0 ;
        confList=[]
        with open("ftxOpt/"+fileName+'.json') as json_file:
            data = json.load(json_file)

        return data;
    def readConfMailFile(self):
            count = 0 ;
            confList=[]
            with open('FTXconf.json') as json_file:
                data = json.load(json_file)
                for i in data:
                    count+=1
                    confList.append(i)
            print(f'find conf count = {count}');

            return confList;

    def getMarketHistory(self,conf):
        now =  datetime.datetime.now().timestamp();
        then =  (datetime.datetime.now() - datetime.timedelta(days=30)).timestamp()
        klines = self.ftx.get_market_history(conf['coin-name'],300,5000,then, now)
        
        open_time = [float(entry["time"]) for entry in klines]
        high = [float(entry["high"]) for entry in klines]
        low = [float(entry["low"]) for entry in klines]
        close = [float(entry["close"]) for entry in klines]
        close_array = np.asarray(close)
        high_array = np.asarray(high)
        low_array = np.asarray(low)
        klinesMap = {
            "close":close_array,
            "high":high_array,
            "low":low_array,
            "open_time":open_time
        }
        return klinesMap;
    def getSignalSuperTrend(self,conf):
        coinHistoryMap = self.getMarketHistory(conf)
        coinPrice = self.ftx.get_market_price(conf["coin-name"])["price"];
        signal = self.superTrend.getSignal(coinHistoryMap, conf,coinPrice,"FTX")
        return signal

    def getSignalTillsonT3(self,conf):
            coinHistoryMap = self.getMarketHistory(conf)
            coinPrice = self.ftx.get_market_price(conf["coin-name"])["price"];
            signal = self.tillsonT3.getSignal(coinHistoryMap, conf,coinPrice,"FTX")
            return signal


    def tradeOperationLocal(self,conf,optType):
        if(optType=='BUY'):
            self.buy(conf["coin-name"], conf["coin-transfer-name"])
            #self.convert(self.ftx,'USD',conf["coin-transfer-name"])
        if(optType=='SELL'):
            self.sell(conf["coin-name"], conf["coin-transfer-name"])
            #self.convert(self.ftx,conf["coin-transfer-name"],'USD')



    def tradeOperationMail(self,orderType,conf):
        if(orderType != None):
            if(orderType['subject'].find(conf['mailSubject']) != -1):
                if orderType._payload.find(conf['mailBuyPattern']) != -1:
                    ftxOperation.convert(self.ftx,'USD',conf["coinName"])
                    print('ALERT BUY')
                if orderType._payload.find(conf['mailSellPattern']) != -1 :
                    ftxOperation.convert(self.ftx,conf["coinName"],'USD')
                    print('ALERT SELL')

    def readGmail(self,conf):
        gmailtest = GmailApi(conf["gmail"]["user-name"],conf["gmail"]["user-password"])
        return gmailtest.read_email_from_gmail()