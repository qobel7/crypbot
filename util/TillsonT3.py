from binance.client import Client
import talib as ta
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import sys
import math
from csv import DictWriter
from datetime import datetime
class TillsonT3:
    lastOperation='Yok'
    def generateTillsonT3(self,historyMap, volume_factor, t3Length):
        
        close_array = historyMap["close"]
        high_array = historyMap["high"]
        low_array = historyMap["low"]

        ema_first_input = (high_array + low_array + 2 * close_array) / 4

        e1 = ta.EMA(ema_first_input, t3Length)

        e2 = ta.EMA(e1, t3Length)

        e3 = ta.EMA(e2, t3Length)

        e4 = ta.EMA(e3, t3Length)

        e5 = ta.EMA(e4, t3Length)

        e6 = ta.EMA(e5, t3Length)

        c1 = -1 * volume_factor * volume_factor * volume_factor

        c2 = 3 * volume_factor * volume_factor + 3 * volume_factor * volume_factor * volume_factor

        c3 = -6 * volume_factor * volume_factor - 3 * volume_factor - 3 * volume_factor * volume_factor * volume_factor

        c4 = 1 + 3 * volume_factor + volume_factor * volume_factor * volume_factor + 3 * volume_factor * volume_factor

        T3 = c1 * e6 + c2 * e5 + c3 * e4 + c4 * e3

        return T3
    def getSignal(self,historyMap,conf,coinPrice,marketName):
        tillsont3 = self.generateTillsonT3(historyMap,conf["tillson-tr-opt"]["value-factor"],conf["tillson-tr-opt"]["t3length"])
        t3_last = tillsont3[-1]
        t3_previous = tillsont3[-2]
        t3_prev_previous = tillsont3[-3]
        now = datetime.now()
        date = now.strftime("%m/%d/%Y, %H:%M:%S")
        status = "yok";
        with open(marketName+'_'+conf["conf-name"]+'_sellbuycalculationT3_'+str(conf["history-opt"]["interval"])+'.csv', 'a+', newline='') as file:
            fieldnames = ['coinName','type', 'price','date']
            writer = DictWriter(file, fieldnames=fieldnames)
            if t3_last > t3_previous and t3_previous < t3_prev_previous and self.lastOperation!='BUY':
                status="BUY"
                self.lastOperation=status
                writer.writerow({'coinName':conf['coin-name'],'type': status, 'price': str(coinPrice),'date':date})

            elif t3_last < t3_previous and t3_previous > t3_prev_previous and self.lastOperation!='SELL':
                status="SELL"
                self.lastOperation=status
                writer.writerow({'coinName':conf['coin-name'],'type': status, 'price': str(coinPrice),'date':date})
        print(marketName + " ## TILLSON T3 ### " +conf['coin-name'] + "-" +status+" "+" = "+str(coinPrice) + "  ----- " +date + "  || " )

        return status;
