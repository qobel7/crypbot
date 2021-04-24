from binance.client import Client
import talib as ta
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import sys
import math
from csv import DictWriter
from datetime import datetime

class SuperTrend:
    lastOperation='Yok'
    def generateSupertrend(self,historyMap : {} , atr_period, atr_multiplier):
        close_array = historyMap["close"]
        high_array = historyMap["high"]
        low_array = historyMap["low"]
        try:
            atr = ta.ATR(high_array, low_array, close_array, atr_period)
        except:
            print('exception in atr:', sys.exc_info()[0], 'pair', pair, flush=True)
            print('filename', filename, flush=True)
            return False, False

        previous_final_upperband = 0
        previous_final_lowerband = 0
        final_upperband = 0
        final_lowerband = 0
        previous_close = 0
        previous_supertrend = 0
        supertrend = []
        supertrendc = 0

        for i in range(0, len(close_array)):
            if np.isnan(close_array[i]):
                pass
            else:
                highc = high_array[i]
                lowc = low_array[i]
                atrc = atr[i]
                closec = close_array[i]

                if math.isnan(atrc):
                    atrc = 0

                basic_upperband = (highc + lowc) / 2 + atr_multiplier * atrc
                basic_lowerband = (highc + lowc) / 2 - atr_multiplier * atrc

                if basic_upperband < previous_final_upperband or previous_close > previous_final_upperband:
                    final_upperband = basic_upperband
                else:
                    final_upperband = previous_final_upperband

                if basic_lowerband > previous_final_lowerband or previous_close < previous_final_lowerband:
                    final_lowerband = basic_lowerband
                else:
                    final_lowerband = previous_final_lowerband

                if previous_supertrend == previous_final_upperband and closec <= final_upperband:
                    supertrendc = final_upperband
                else:
                    if previous_supertrend == previous_final_upperband and closec >= final_upperband:
                        supertrendc = final_lowerband
                    else:
                        if previous_supertrend == previous_final_lowerband and closec >= final_lowerband:
                            supertrendc = final_lowerband
                        elif previous_supertrend == previous_final_lowerband and closec <= final_lowerband:
                            supertrendc = final_upperband

                supertrend.append(supertrendc)

                previous_close = closec

                previous_final_upperband = final_upperband

                previous_final_lowerband = final_lowerband

                previous_supertrend = supertrendc
     
        return {"supertrend":supertrend,"close_array":close_array}
    def getSignal(self,historyMap,conf,coinPrice,marketName=""):
        map = self.generateSupertrend(historyMap,conf["supertrend-opt"]["atr-period"], conf["supertrend-opt"]["atr-multiplier"])
        close_array = map["supertrend"]
        supertrend = map["close_array"]
        # new_time = [datetime.fromtimestamp(time / 1000) for time in historyMap["open_time"]]

        # new_time_x = [date.strftime("%y-%m-%d") for date in new_time]
        # plt.figure(figsize=(11, 6))
        # plt.plot(new_time_x[400:], close_array[400:], label='Price')
        # plt.plot(new_time_x[400:], supertrend[400:], label='Supertrend')
        # plt.xticks(rotation=90, fontsize=5)
        # plt.title("Supertrend Plot for DOGE/USDT")
        # plt.xlabel("Open Time")
        # plt.ylabel("Value")
        # plt.legend()
        # plt.show()
        now = datetime.now()
        date = now.strftime("%m/%d/%Y, %H:%M:%S")
        status = "yok";
       
        last_close = close_array[-1]
        before_close = close_array[-2]
        last_supertrend_value = supertrend[-1]
        before_supertrend_value = supertrend[-2]
        
        with open('output/'+marketName+'_'+conf["conf-name"]+'_sellbuycalculationSuperTrend_'+str(conf["history-opt"]["interval"])+'.csv', 'a+', newline='') as file:
            fieldnames = ['coinName','type', 'price','date']
            writer = DictWriter(file, fieldnames=fieldnames)

            # coinPrice = client.get_avg_price(symbol=conf['coin-name'])["price"]
            if last_close > last_supertrend_value and before_close < before_supertrend_value and self.lastOperation!='BUY':
                status = 'BUY'
                self.lastOperation=status
                writer.writerow({'coinName':conf['coin-name'],'type': status, 'price': str(coinPrice),'date':date})


            if last_close < last_supertrend_value and before_close > before_supertrend_value and self.lastOperation!='SELL':
                status = 'SELL'
                self.lastOperation=status
                writer.writerow({'coinName':conf['coin-name'],'type': status, 'price': str(coinPrice),'date':date})
        print(marketName + " ## SUPERTREND ### " +conf['coin-name'] + "-" +status+" "+" = "+str(coinPrice) + "  ----- " +date + "  || " + str(last_close) + " || "+ str(last_supertrend_value))
        return status