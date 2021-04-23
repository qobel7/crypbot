import GmailApi
from FTXClient import FtxClient
import json
import re
from FTXOperation import FTXOperation
from GmailApi import GmailApi
from time import sleep
class Main:
    confList=[]
    ftx=None
    fTXOperation=None
    def start(self):
        self.readConfFile()   
        for conf in self.confList:
            if(conf["isAktif"]):
                while True:    
                    orderType=self.readGmail(conf)
                    self.tradeOperation(orderType,conf)
                sleep(5)
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

    def readConfFile(self):
        count = 0 ;
        with open('conf.json') as json_file:
            data = json.load(json_file)
            for i in data:
                count+=1
                self.confList.append(i)
        print(f'find conf count = {count}');
        for i in self.confList:
            print(i["gmail"]["user-name"])

