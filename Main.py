from ftxOpt.FTXOperation import  FTXOperation
from binanceOpt.BinanceOperation import BinanceOperation

class Main:
  
    def start(self,marketName,confName):
        if(marketName == 'FTX'):
            self.ftxLocalIndicator(confName)
        if(marketName == 'Binance'):
            self.binanceLocalIndicator(confName)
    def binanceLocalIndicator(self,confName):
        BinanceOperation(confName).start()
    def ftxLocalIndicator(self,confName):
        FTXOperation(confName).start()





