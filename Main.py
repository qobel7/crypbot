from ftxOpt.FTXOperation import  FTXOperation
from binanceOpt.BinanceOperation import BinanceOperation

class Main:
  
    def start(self,marketName):
        if(marketName == 'FTX'):
            self.ftxLocalIndicator()
        if(marketName == 'Binance'):
            self.binanceLocalIndicator()
    def binanceLocalIndicator(self):
        BinanceOperation().start()
    def ftxLocalIndicator(self):
        FTXOperation().start()





