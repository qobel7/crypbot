import FTXClient 

class FTXOperation:

    def __init__(self):
        print('start')

    def sell(self,ftx: FTXClient.FtxClient,coinName: str,coinIndex: str):
        market = ftx.list_markets()
        mm = ftx.get_balances()
        coin_index = [ x['coin'] for x in mm ].index(coinIndex)
        coin_balance  = mm[coin_index]['total']
        tt=ftx.place_order('TRX/USDT','sell',None,coin_balance,'market')

    def buy(self,ftx: FTXClient.FtxClient,coinName: str):
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
