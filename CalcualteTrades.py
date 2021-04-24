from csv import DictWriter
class CalcualteTrades:
    def __init__(self,fileName):
        print("start")
        self.readFromFile(fileName)
    def readFromFile(self,fileName):
        count = 0 ;
        confList=[]
        buyList=[]
        sellList=[]
        result = 0
        with open(fileName+'.csv') as f:
            for i, line in enumerate(f):             
                list = line.split(",")
                if list[1]=='BUY':
                    buyList.append(list[2])
                if list[1]=='SELL':
                    sellList.append(list[2])
        for i in range(0,len(sellList)):
            result += -(float(buyList[i])-float(sellList[i]))
        print(result)

CalcualteTrades("output/FTX_SELLBUY_sellbuycalculationSuperTrend_300")