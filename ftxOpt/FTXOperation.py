from binance.client import Client
import json
import numpy as np
from  util.SuperTrend import SuperTrend
from ftxOpt.FTXClient import FtxClient
from time import sleep
import datetime
class FTXOperation:
    superTrend =None
    ftx=None
    confList=[]
    confMailList=[]
    isMailAktif=False
    def __init__(self):
        print('start')
        self.confList = self.readConfFile("FTXConfLocal")
        self.confMailList = self.readConfFile("FTXConfMail")
        self.isMailAktif = self.readConfFile("FTXConfAktif")["isMailAktif"]
        conf = self.confList[0];
        self.superTrend = SuperTrend()
        self.ftx =FtxClient(conf["api-key"], conf["api-secret"])

    def start(self):
        if(self.isMailAktif==False):
            # pythondan supertrend okuyan kısım
            while True:
                conf = self.confList[0]
                self.getSignal(conf)
                sleep(5)

        if(self.isMailAktif==False):
            #gmail üzerinden trading viewden gelen mail ile al sat yapan kısım
            for conf in self.confList:
                if(conf["isAktif"]):
                    while True:    
                        orderType=self.readGmail(conf)
                        self.tradeOperation(orderType,conf)
                    sleep(5)

    def sell(self,ftx,coinName: str,coinIndex: str):
        market = ftx.list_markets()
        mm = ftx.get_balances()
        coin_index = [ x['coin'] for x in mm ].index(coinIndex)
        coin_balance  = mm[coin_index]['total']
        tt=ftx.place_order('TRX/USDT','sell',None,coin_balance,'market')

    def buy(self,ftx,coinName: str):
        print('test')
        #ftx.place_order('TRX/USDT','buy',None,coin_balance,'market')

    def getCoinBalances(self,ftx,coinName: str):
        market = ftx.list_markets()
        mm = ftx.get_balances()
        coin_index = [ x['coin'] for x in mm ].index(coinName)
        coin_balance  = mm[coin_index]['total']
        if coinName != 'USD':
            coinPrice = market[[ x['name'] for x in market ].index(coinName+"/USDT")]["price"]
            print(f'coinName {coinName} ,  coinPrice {coinPrice}')
        return coin_balance

    def convert(self,ftx,fromcoinName,toCoinName):
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
        klines = self.ftx.get_market_history('TRX/USD',300,500,then, now)
        high = [float(entry["high"]) for entry in klines]
        low = [float(entry["low"]) for entry in klines]
        close = [float(entry["close"]) for entry in klines]
        close_array = np.asarray(close)
        high_array = np.asarray(high)
        low_array = np.asarray(low)
        klinesMap = {
            "close":close_array,
            "high":high_array,
            "low":low_array
        }
        return klinesMap;
    def getSignal(self,conf):
        coinHistoryMap = self.getMarketHistory(conf)
        coinPrice = self.ftx.get_market_price(conf["coin-name"])["price"];
        signal = self.superTrend.getSignal(coinHistoryMap, conf,coinPrice,"FTX")


        
    def tradeOperation(self,orderType,conf):
        ftxOperation = FTXOperation();  
        self.ftx =FtxClient(conf["ftx"]["private-key"],conf["ftx"]["public-key"])
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