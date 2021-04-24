from binance.client import Client
import json
import numpy as np
from  util.SuperTrend import SuperTrend
from datetime import datetime
from  util.TillsonT3 import TillsonT3

from time import sleep
class BinanceOperation:
    client=None
    klines=[]
    confList=[]
    superTrend=None
    def __init__(self):
        self.superTrend = SuperTrend()
        self.tillsonT3 = TillsonT3()
        self.readConfFile()
        conf = self.confList[0];
        self.client = Client(conf["api-key"], conf["api-secret"])
    def start(self):
        conf = self.confList[0];
        while True:
            coinPrice = self.   client.get_avg_price(symbol=conf['coin-name'])["price"]
            history = self.getCoinHistory(conf["coin-name"], conf["history-opt"]["interval"], conf["history-opt"]["limit"])
            signal = self.superTrend.getSignal(history, conf,coinPrice,"Binance")
            self.tillsonT3.getSignal(history, conf, coinPrice, "Binance")

            sleep(5)

    def getCoinHistory(self,coinName,interval,limit):
        klines = self.client.get_klines(symbol=coinName, interval=interval, limit=limit)
        open_time = [int(entry[0]) for entry in klines]

        open = [float(entry[1]) for entry in klines]
        high = [float(entry[2]) for entry in klines]
        low = [float(entry[3]) for entry in klines]
        close = [float(entry[4]) for entry in klines]
        close_array = np.asarray(close)
        high_array = np.asarray(high)
        low_array = np.asarray(low)
        klinesMap = {
            "close":close_array,
            "high":high_array,
            "low":low_array
        }
        return klinesMap

    def readConfFile(self):
        count = 0 ;
        with open('binanceOpt/BinanceConf.json') as json_file:
            data = json.load(json_file)
            for i in data:
                count+=1
                self.confList.append(i)
        print(f'find conf count = {count}');

