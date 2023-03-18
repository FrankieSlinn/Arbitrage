#"totalGain", totalGain, "Curr", BstReports[i][-1], "Ask", BstReports[i][8], "Bid", CBReports[i][7]#explore limit order possibility / amts
#fees - Trading, Withdrawal
#xrp removed from CB, not tradable
#Volume Bst: amt of asset that was traded

#Capture gap between spreads, add fees, currency conversions,
#import forex_python
import requests
import datetime
import json, hmac, hashlib, time, base64
import cbpro

from forex_python.converter import CurrencyRates

#for mode choose "r" for report or "c" for calculation. To view report access CryptoData File.
mode = "c"

cr = CurrencyRates()

currencies = ["BTC", "ETH", "XRP", "LTC", "PAX", "XLM", "LINK", "OMG", "AAVE", "BAT", "UMA", "DAI", "KNC", "MKR", "ZRX","ALGO", "AUDIO", "CRV", "SNX", "UNI"]

#to get numeric values from string
nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]


#Bitfinex

#Fees
#Fees listed are max fees
#Fiat BF withdrawal / deposit fees in %
#Exmo trading fees 0.093% max // crypto deposit 0 // crypto withdrawal certain amount of cryptocurrency //SEPA 0 deposit and withdrawal fee //Not taking on new resident UK people.
#LocalBitcoins - has lower prices but need reputation to buy. 0.0002526 BTC is wallet transfer fee. // no buying or selling transaction fee(1st month)? 1% fee?.
url = "https://api-pub.bitfinex.com/v2/tickers?symbols"

headers = {"accept": "application/json"}

bfresponse = requests.get(url, headers=headers)

#APIs for Exchanges

#CoinBase

responseCB = requests.get("https://api.coinbase.com/v2/exchange-rates?currency=USD")
responseCBGBP = requests.get("https://api.coinbase.com/v2/exchange-rates?currency=GBP")
#print("responseCB", responseCB)
dataUSD = responseCB.json()
dataCBGBP = responseCBGBP.json()


#Bitstamp

response = requests.get("https://www.bitstamp.net/api/v2/ticker/")
ResponseSplit = ""

for i in response:
    strResponse = i.decode()
    ResponseSplit += strResponse
    strResponse = ""
#print("i", i)


parsedBst = json.loads(ResponseSplit)
for i in parsedBst:
    del i['open']
    del i['high']
    del i['low']
    del i['vwap']
    del i['open_24']
    if i["percent_change_24"] == None:
        i["percent_change_24"] = 0


timeStamp = datetime.datetime.fromtimestamp(int(parsedBst[0]["timestamp"])).isoformat()



HeadingData = ("{:<10} {:<30} {:<10} {:<13} {:<15} {:<13} {:<13} {:<10} {:<10} {:<10} {:<10} {:<15} {:<10}".format("Exchange ","TimeStamp ", "Max Fee %", "Deposit Fee", "Wthdraw Fee GBP", "Xfer Fee", "Xfer to Fee",  "USD Bid ", "USD Ask ", "GBP Bid ", "GBP Ask ", "% Change 24H ", "Volume"))
#print(HeadingData)
reportform = ""
#to display report
if mode =="r":
    reportform = "{:<10} {:<30} {:<10} {:<13} {:<15} {:<13} {:<13} {:<10} {:<10} {:<10} {:<10} {:<15} {:<10}"
#to obtain arbitrage opportunities
else:
    reportform = "{:<10}, {:<30}, {:<10}, {:<13}, {:<15}, {:<13}, {:<13}, {:<10}, {:<10}, {:<10}, {:<10}, {:<15}, {:<10}"


#BTC
sign = "BTC"

#Bitfinex
urlUSD = "https://api-pub.bitfinex.com/v2/tickers?symbols=t"+sign+"USD"

bfresponse = requests.get(urlUSD, headers=headers)
bfUSdata = bfresponse.json()[0]
#print("bid", bfUSdata[1])
#print("ask", bfUSdata[3])

urlGBP = "https://api-pub.bitfinex.com/v2/tickers?symbols=t"+sign+"GBP"

bfresponse = requests.get(urlGBP, headers=headers)
bfGBPdata = bfresponse.json()[0]

#cb

CBUSDBTC = 1//float(dataUSD["data"]["rates"]["BTC"])
CBGBPBTC = 1//float(dataCBGBP["data"]["rates"]["BTC"])


BFBTCReport = (reportform.format("Bitfinex", "" , 0.2, 0.1, 0.1, "0.0004 BTC" , 0, bfUSdata[1] , bfUSdata[3], bfGBPdata[1], bfGBPdata[3] ,"" , ""))
CBBTCReport = (reportform.format("CoinBase", "" , 0.6, 0, 0, 0 , 0, CBUSDBTC , CBUSDBTC, CBGBPBTC, CBGBPBTC ,"" , ""))
reportBTC = (reportform.format("Bitstamp", timeStamp , 0.4, 0, 2, "0.0005BTC" , 0, parsedBst[0]["bid"] , parsedBst[0]["ask"] , parsedBst[2]["bid"], parsedBst[2]["ask"] ,parsedBst[0]["percent_change_24"] , parsedBst[0]["volume"]))


#ETH
sign = "ETH"
#cb
responseCB = requests.get("https://api.coinbase.com/v2/prices/ETH-USD/spot")

data = responseCB.json()
#print("data", data)
CBETHUSD = float(data["data"]["amount"])

responseCB = requests.get("https://api.coinbase.com/v2/prices/ETH-GBP/spot")

data = responseCB.json()
#print("data", data)
CBETHGBP = float(data["data"]["amount"])

#bst

#Bitfinex
urlUSD = "https://api-pub.bitfinex.com/v2/tickers?symbols=t"+sign+"USD"

bfresponse = requests.get(urlUSD, headers=headers)
bfUSdata = bfresponse.json()[0]


urlGBP = "https://api-pub.bitfinex.com/v2/tickers?symbols=t"+sign+"GBP"

bfresponse = requests.get(urlGBP, headers=headers)
bfGBPdata = bfresponse.json()[0]


BFETHReport = (reportform.format("Bitfinex", "" , 0.2, 0.1, 0.1, "0.0016695 ETH" , 0, bfUSdata[1] , bfUSdata[3], bfGBPdata[1], bfGBPdata[3] ,"" , ""))
reportETH = (reportform.format("Bitstamp", timeStamp , 0.4, 0, 2, "0.006 ETH", 0, parsedBst[16]["bid"] , parsedBst[16]["ask"] , parsedBst[18]["bid"], parsedBst[18]["ask"] , parsedBst[16]["percent_change_24"] , parsedBst[16]["volume"]))

CBETHReport = (reportform.format("Coinbase", timeStamp , 0.6, 0, 0, 0, 0, CBETHUSD , CBETHUSD, CBETHGBP , CBETHGBP,"", ""))
#print("CBReportEth", CBReportEth)
#print(parsedBst[16])

#XRP
sign = "XRP"

#cb
CBUSDXRP = round(1/float(dataUSD["data"]["rates"]["XRP"]), 5)
CBGBPXRP = round(1/float(dataCBGBP["data"]["rates"]["XRP"]), 5)

#Bitfinex

urlUSD = "https://api-pub.bitfinex.com/v2/tickers?symbols=t"+sign+"USD"

bfresponse = requests.get(urlUSD, headers=headers)
bfUSdata = bfresponse.json()[0]

urlGBP = "https://api-pub.bitfinex.com/v2/tickers?symbols=t"+sign+"GBP"

bfresponse = requests.get(urlGBP, headers=headers)

if len(bfresponse.json()) >= 1:
    bfGBPdata = bfresponse.json()[0]
else:
    bfGBPdata = ""

BFXRPReport = (reportform.format("Bitfinex", "" , 0.2, 0.1, 0.1, "0.1 XRP" , 0, bfUSdata[1] , bfUSdata[3], "", "" ,"" , ""))

CBXRPReport = (reportform.format("CoinBase", "" , 0.6, 0, 0, 0 , 0, CBUSDXRP , CBUSDXRP, CBGBPXRP, CBGBPXRP ,"" , ""))

reportXRP = (reportform.format("Bitstamp", timeStamp , 0.4, 0, 2, "0.02 XRP", 0,parsedBst[7]["bid"] , parsedBst[7]["ask"] , parsedBst[10]["bid"], parsedBst[10]["ask"] ,parsedBst[7]["percent_change_24"] , parsedBst[7]["volume"]))
#print(reportXRP)
#print(CBXRPReport)
#print("XRPGBP", dataCBGBP["data"]["rates"]["XRP"])
#print("XRPGBP", '{:.4f}'.format(1/float(dataCBGBP["data"]["rates"]["XRP"])))

#LTC
sign = "LTC"

#cb
CBUSDLTC = round(1/float(dataUSD["data"]["rates"]["LTC"]), 5)
CBGBPLTC = round(1/float(dataCBGBP["data"]["rates"]["LTC"]), 5)

#bf
#Bitfinex

urlUSD = "https://api-pub.bitfinex.com/v2/tickers?symbols=t"+sign+"USD"

bfresponse = requests.get(urlUSD, headers=headers)
bfUSdata = bfresponse.json()[0]

urlGBP = "https://api-pub.bitfinex.com/v2/tickers?symbols=t"+sign+"GBP"

bfresponse = requests.get(urlGBP, headers=headers)

if len(bfresponse.json()) >= 1:
    bfGBPdata = bfresponse.json()[0]
else:
    bfGBPdata = ""

BFLTCReport = (reportform.format("Bitfinex", "" , 0.2, 0.1, 0.1, "0.001 LTC" , 0, bfUSdata[1] , bfUSdata[3], "", "" ,"" , ""))

CBLTCReport = (reportform.format("CoinBase", "" , 0.6, 0, 0, 0 , 0, CBUSDLTC , CBUSDLTC, CBGBPLTC, CBGBPLTC ,"" , ""))

reportLTC = (reportform.format("Bitstamp", timeStamp , 0.4, 0, 2, "0.001 LTC", 0, parsedBst[12]["bid"] , parsedBst[12]["ask"] , parsedBst[14]["bid"], parsedBst[14]["ask"], parsedBst[12]["percent_change_24"] , parsedBst[12]["volume"]))
#print("reportLTC", reportLTC)
#Paxos
sign =  "PAX"

#cb
CBUSDPAX = round(1/float(dataUSD["data"]["rates"]["PAX"]), 5)
CBGBPPAX = round(1/float(dataCBGBP["data"]["rates"]["PAX"]), 5)

#Bitfinex

urlUSD = "https://api-pub.bitfinex.com/v2/tickers?symbols=t"+sign+"USD"

bfresponse = requests.get(urlUSD, headers=headers)
bfUSdata = bfresponse.json()[0]

urlGBP = "https://api-pub.bitfinex.com/v2/tickers?symbols=t"+sign+"GBP"

bfresponse = requests.get(urlGBP, headers=headers)

def bflen():
    if len(bfresponse.json()) >= 1:
        bfGBPdata = bfresponse.json()[0]
    else:
        bfGBPdata = ""
bflen()

BFPAXReport = (reportform.format("Bitfinex", "" , 0.2, 0.1, 0.1, "2.0065 PAX" , 0, bfUSdata[1] , bfUSdata[3], "", "" ,"" , ""))

CBPAXReport = (reportform.format("CoinBase", "" , 0.6, 0, 0, 0 , 0, CBUSDPAX , CBUSDPAX, CBGBPPAX, CBGBPPAX ,"" , ""))

reportPAX = (reportform.format("Bitstamp", timeStamp , 0.4, 0, 2, "20 PAX", 0, parsedBst[23]["bid"] , parsedBst[23]["ask"] , " ", " " , parsedBst[23]["percent_change_24"] , parsedBst[23]["volume"]))

#Stellar - XLM
sign = "XLM"

#cb
CBUSDXLM = round(1/float(dataUSD["data"]["rates"]["XLM"]), 5)
CBGBPXLM = round(1/float(dataCBGBP["data"]["rates"]["XLM"]), 5)

#Bitfinex

urlUSD = "https://api-pub.bitfinex.com/v2/tickers?symbols=t"+sign+"USD"

bfresponse = requests.get(urlUSD, headers=headers)
bfUSdata = bfresponse.json()[0]

urlGBP = "https://api-pub.bitfinex.com/v2/tickers?symbols=t"+sign+"GBP"

bfresponse = requests.get(urlGBP, headers=headers)

bflen()

BFXLMReport = (reportform.format("Bitfinex", "" , 0.2, 0.1, 0.1, 0 , 0, bfUSdata[1] , bfUSdata[3], "", "" ,"" , ""))

CBXLMReport = (reportform.format("CoinBase", "" , 0.6, 0, 0, 0 , 0, CBUSDXLM , CBUSDXLM, CBGBPXLM, CBGBPXLM ,"" , ""))

reportXLM = (reportform.format("Bitstamp", timeStamp , 0.4, 0, 2, "0.005 XLM", 0, parsedBst[25]["bid"] , parsedBst[25]["ask"] , parsedBst[27]["bid"], parsedBst[27]["ask"], parsedBst[25]["percent_change_24"] , parsedBst[25]["volume"]))

#LINK = ChainLink
sign = "LINK"

#cb
CBUSDLINK = round(1/float(dataUSD["data"]["rates"]["LINK"]), 5)
CBGBPLINK = round(1/float(dataCBGBP["data"]["rates"]["LINK"]), 5)

# Bitfinex

urlUSD = "https://api-pub.bitfinex.com/v2/tickers?symbols=t" + sign + "USD"
bfresponse = requests.get(urlUSD, headers=headers)
#print("linkrequest", requests.get(urlUSD, headers=headers).json())

urlGBP = "https://api-pub.bitfinex.com/v2/tickers?symbols=t" + sign + "GBP"
bfresponse = requests.get(urlGBP, headers=headers)
if len(bfresponse.json()) >= 1:
    bfGBPdata = bfresponse.json()[0]
    bfUSdata = bfresponse.json()[0]
else:
    bfGBPdata = ""
    bfUSDdata = ""

BFLINKReport = ("")

CBLINKReport = (reportform.format("CoinBase", "" , 0.6, 0, 0, 0 , 0, CBUSDLINK , CBUSDLINK, CBGBPLINK, CBGBPLINK,"" , ""))

reportLINK = (reportform.format("Bitstamp", timeStamp , 0.4, 0, 2, "1.5 LINK", 0, parsedBst[28]["bid"] , parsedBst[28]["ask"] , parsedBst[30]["bid"], parsedBst[30]["ask"], "", "", parsedBst[28]["percent_change_24"] , parsedBst[28]["volume"]))

#OMG
sign = "OMG"

#cb
CBUSDOMG = round(1/float(dataUSD["data"]["rates"]["OMG"]), 5)
CBGBPOMG = round(1/float(dataCBGBP["data"]["rates"]["OMG"]), 5)

#Bitfinex

urlUSD = "https://api-pub.bitfinex.com/v2/tickers?symbols=t"+sign+"USD"
bfresponse = requests.get(urlUSD, headers=headers)
bfUSdata = bfresponse.json()[0]

urlGBP = "https://api-pub.bitfinex.com/v2/tickers?symbols=t"+sign+"GBP"
bfresponse = requests.get(urlGBP, headers=headers)
bflen()

BFOMGReport = (reportform.format("Bitfinex", "" , 0.2, 0.1, 0.1, "1.9252 OMG", 0, bfUSdata[1] , bfUSdata[3], "", "" ,"" , ""))

CBOMGReport = (reportform.format("CoinBase", "" , 0.6, 0, 0, 0 , 0, CBUSDOMG , CBUSDOMG, CBGBPOMG, CBGBPOMG,"" , ""))

reportOMG = (reportform.format("Bitstamp", timeStamp , 0.4, 0, 2, "3 OMG", 0, parsedBst[32]["bid"] , parsedBst[32]["ask"] , parsedBst[34]["bid"], parsedBst[34]["ask"], parsedBst[32]["percent_change_24"] , parsedBst[32]["volume"]))

#Aave
sign = "AAVE"

#Bitfinex

urlUSD = "https://api-pub.bitfinex.com/v2/tickers?symbols=t"+sign+"USD"
bfresponse = requests.get(urlUSD, headers=headers)
if len(bfresponse.json()) !=0:
    bfUSdata = bfresponse.json()[0]

urlGBP = "https://api-pub.bitfinex.com/v2/tickers?symbols=t"+sign+"GBP"
bfresponse = requests.get(urlGBP, headers=headers)
bflen()

BFAAVEReport = (reportform.format("Bitfinex", "" , 0.2, 0.1, 0.1, "0.034718 AAVE", 0, bfUSdata[1] , bfUSdata[3], "", "" ,"" , ""))

#cb
CBUSAAVE = round(1/float(dataUSD["data"]["rates"]["AAVE"]), 5)
CBGBPAAVE = round(1/float(dataCBGBP["data"]["rates"]["AAVE"]), 5)

CBAAVEReport = (reportform.format("CoinBase", "" , 0.6, 0, 0, 0 , 0, CBUSAAVE , CBUSAAVE, CBGBPAAVE, CBGBPAAVE,"" , "","" , ""))

reportAAVE= (reportform.format("Bitstamp", timeStamp , 0.4, 0, 2, "0.2 AAVE", 0, parsedBst[41]["bid"] , parsedBst[41]["ask"] , "", "", parsedBst[41]["percent_change_24"] , parsedBst[41]["volume"]))

#BAT
sign = "BAT"

#cb
CBUSBAT = round(1/float(dataUSD["data"]["rates"]["BAT"]), 5)
CBGBPBAT = round(1/float(dataCBGBP["data"]["rates"]["BAT"]), 5)

#Bitfinex

urlUSD = "https://api-pub.bitfinex.com/v2/tickers?symbols=t"+sign+"USD"
bfresponse = requests.get(urlUSD, headers=headers)
if len(bfresponse.json()) !=0:
    bfUSdata = bfresponse.json()[0]

urlGBP = "https://api-pub.bitfinex.com/v2/tickers?symbols=t"+sign+"GBP"
bfresponse = requests.get(urlGBP, headers=headers)
bflen()

BFBATReport = (reportform.format("Bitfinex", "" , 0.2, 0.1, 0.1, "10.342 BAT", 0, bfUSdata[1] , bfUSdata[3], "", "" ,"" , ""))

CBBATReport = (reportform.format("CoinBase", "" , 0.6, 0, 0, 0 , 0, CBUSBAT , CBUSBAT, CBGBPBAT, CBGBPBAT,"" , "","" , ""))

reportBAT = (reportform.format("Bitstamp", timeStamp , 0.4, 0, 2, "25 BAT", 0, parsedBst[44]["bid"] , parsedBst[44]["ask"] , "", "", parsedBst[44]["percent_change_24"] , parsedBst[44]["volume"]))

#UMA
sign = "UMA"

#cb
CBUSUMA = round(1/float(dataUSD["data"]["rates"]["UMA"]), 5)
CBGBPUMA = round(1/float(dataCBGBP["data"]["rates"]["UMA"]), 5)

CBUMAReport = (reportform.format("CoinBase", "" , 0.6, 0, 0, 0 , 0, CBUSUMA , CBUSUMA, CBGBPUMA, CBGBPUMA, "" , ""))
BFUMAReport = ""
reportUMA = (reportform.format("Bitstamp", timeStamp , 0.4, 0, 2, "2 UMA", 0, parsedBst[46]["bid"] , parsedBst[46]["ask"] , "", "", parsedBst[46]["percent_change_24"] , parsedBst[46]["volume"]))

#DAI
sign = "DAI"
#cb
CBUSDAI = round(1/float(dataUSD["data"]["rates"]["DAI"]), 5)
CBGBPDAI = round(1/float(dataCBGBP["data"]["rates"]["DAI"]), 5)

#Bitfinex

urlUSD = "https://api-pub.bitfinex.com/v2/tickers?symbols=t"+sign+"USD"
bfresponse = requests.get(urlUSD, headers=headers)

if len(bfresponse.json()) !=0:

    bfUSdata = bfresponse.json()[0]


urlGBP = "https://api-pub.bitfinex.com/v2/tickers?symbols=t"+sign+"GBP"
bfresponse = requests.get(urlGBP, headers=headers)
bflen()

BFDAIReport = (reportform.format("Bitfinex", "" , 0.2, 0.1, 0.1, "2.0118 DAI", 0, bfUSdata[1] , bfUSdata[3], "", "" ,"" , ""))

CBDAIReport = (reportform.format("CoinBase", "" , 0.6, 0, 0, 0 , 0, CBUSDAI , CBUSDAI, CBGBPDAI, CBGBPDAI,"" , "","" , ""))

reportDAI = (reportform.format("Bitstamp", timeStamp , 0.4, 0, 2, "15 DAI", 0, parsedBst[48]["bid"] , parsedBst[48]["ask"] , "", "", parsedBst[48]["percent_change_24"] , parsedBst[48]["volume"]))

#Kyber Network
sign = "KNC"
#cb
CBUSKNC = round(1/float(dataUSD["data"]["rates"]["KNC"]), 5)
CBGBPKNC = round(1/float(dataCBGBP["data"]["rates"]["KNC"]), 5)

#Bitfinex

urlUSD = "https://api-pub.bitfinex.com/v2/tickers?symbols=t"+sign+"USD"
bfresponse = requests.get(urlUSD, headers=headers)

if len(bfresponse.json()) !=0:

    bfUSdata = bfresponse.json()[0]


urlGBP = "https://api-pub.bitfinex.com/v2/tickers?symbols=t"+sign+"GBP"
bfresponse = requests.get(urlGBP, headers=headers)
bflen()

BFKNCReport = (reportform.format("Bitfinex", "" , 0.2, 0.1, 0.1, "3.883 KNC", 0, bfUSdata[1] , bfUSdata[3], "", "" ,"" , ""))

CBKNCReport = (reportform.format("CoinBase", "" , 0.6, 0, 0, 0 , 0, CBUSKNC , CBUSKNC,CBGBPKNC, CBGBPKNC,"" , "","" , ""))

reportKNC = (reportform.format("Bitstamp", timeStamp , 0.4, 0, 2, "15 KNC", 0, parsedBst[49]["bid"] , parsedBst[49]["ask"] , "", "", "", "", parsedBst[49]["percent_change_24"] , parsedBst[49]["volume"]))

#Maker
sign = "MKR"
#cb
CBUSMKR = round(1/float(dataUSD["data"]["rates"]["MKR"]), 5)
CBGBPMKR = round(1/float(dataCBGBP["data"]["rates"]["MKR"]), 5)

#Bitfinex

urlUSD = "https://api-pub.bitfinex.com/v2/tickers?symbols=t"+sign+"USD"
bfresponse = requests.get(urlUSD, headers=headers)

if len(bfresponse.json()) !=0:

    bfUSdata = bfresponse.json()[0]


urlGBP = "https://api-pub.bitfinex.com/v2/tickers?symbols=t"+sign+"GBP"
bfresponse = requests.get(urlGBP, headers=headers)
bflen()

BFMKRReport = (reportform.format("Bitfinex", "" , 0.2, 0.1, 0.1, "0.0035055 MKR", 0, bfUSdata[1] , bfUSdata[3], "", "" ,"" , ""))

CBMKRReport = (reportform.format("CoinBase", "" , 0.6, 0, 0, 0 , 0, CBUSMKR , CBUSMKR, CBGBPMKR, CBGBPMKR,"" , ""))

reportMKR = (reportform.format("Bitstamp", timeStamp , 0.4, 0, 2, "0.005 MKR", 0, parsedBst[51]["bid"] , parsedBst[51]["ask"], "", "", parsedBst[51]["percent_change_24"] , parsedBst[51]["volume"]))

#Ox
sign = "ZRX"
#cb
CBUSZRX = round(1/float(dataUSD["data"]["rates"]["ZRX"]), 5)
CBGBPZRX = round(1/float(dataCBGBP["data"]["rates"]["ZRX"]), 5)

#Bitfinex

urlUSD = "https://api-pub.bitfinex.com/v2/tickers?symbols=t"+sign+"USD"
bfresponse = requests.get(urlUSD, headers=headers)

if len(bfresponse.json()) !=0:
    bfUSdata = bfresponse.json()[0]

urlGBP = "https://api-pub.bitfinex.com/v2/tickers?symbols=t"+sign+"GBP"
bfresponse = requests.get(urlGBP, headers=headers)
bflen()

BFZRXReport = (reportform.format("Bitfinex", "" , 0.2, 0.1, 0.1, "11.347 ZRX", 0, bfUSdata[1] , bfUSdata[3], "", "" ,"" , ""))

CBZRXReport = (reportform.format("CoinBase", "" , 0.6, 0, 0, 0 , 0, CBUSZRX , CBUSZRX, CBGBPZRX, CBGBPZRX,"" , "","" , ""))

reportZRX = (reportform.format("Bitstamp", timeStamp , 0.4, 0, 2, "12 ZRX", 0, parsedBst[53]["bid"] , parsedBst[53]["ask"] , "", "", parsedBst[53]["percent_change_24"] , parsedBst[53]["volume"]))


#Algorand
sign: "ALGO"
#cb
CBUSALGO = round(1/float(dataUSD["data"]["rates"]["ALGO"]), 5)
CBGBPALGO = round(1/float(dataCBGBP["data"]["rates"]["ALGO"]), 5)

#Bitfinex

urlUSD = "https://api-pub.bitfinex.com/v2/tickers?symbols=t"+sign+"USD"
bfresponse = requests.get(urlUSD, headers=headers)

if len(bfresponse.json()) !=0:
    bfUSdata = bfresponse.json()[0]

urlGBP = "https://api-pub.bitfinex.com/v2/tickers?symbols=t"+sign+"GBP"
bfresponse = requests.get(urlGBP, headers=headers)
bflen()

BFALGOReport = (reportform.format("Bitfinex", "" , 0.2, 0.1, 0.1, 0, 0, bfUSdata[1] , bfUSdata[3], "", "" ,"" , ""))

CBALGOReport = (reportform.format("CoinBase", "" , 0.6, 0, 0, 0 , 0, CBUSALGO , CBUSALGO, CBGBPALGO, CBGBPALGO,"" , "","" , ""))

reportALGO = (reportform.format("Bitstamp", timeStamp , 0.4, 0, 2, "0.1 ALGO", 0, parsedBst[56]["bid"] , parsedBst[56]["ask"] , "", "", parsedBst[56]["percent_change_24"] , parsedBst[56]["volume"]))

#Audius

#cb
#not supported
#Bitfinex not supported
#Bitfinex

reportAUDIO = (reportform.format("Bitstamp", timeStamp , 0.4, 0, 2, "10 AUDIO", 0, parsedBst[59]["bid"] , parsedBst[59]["ask"] , "", "", parsedBst[59]["percent_change_24"] , parsedBst[59]["volume"]))
BFAUDIOReport = ""
CBAUDIOReport = ("")
#Curve
sign = "CRV"
#cb
CBUSCRV = round(1/float(dataUSD["data"]["rates"]["CRV"]), 5)
CBGBPCRV = round(1/float(dataCBGBP["data"]["rates"]["CRV"]), 5)

#Bitfinex
urlUSD = "https://api-pub.bitfinex.com/v2/tickers?symbols=t"+sign+"USD"
bfresponse = requests.get(urlUSD, headers=headers)

if len(bfresponse.json()) !=0:
    bfUSdata = bfresponse.json()[0]

urlGBP = "https://api-pub.bitfinex.com/v2/tickers?symbols=t"+sign+"GBP"
bfresponse = requests.get(urlGBP, headers=headers)
bflen()

BFCRVReport = (reportform.format("Bitfinex", "" , 0.2, 0.1, 0.1,"3.7029 CRV", 0, bfUSdata[1] , bfUSdata[3], "", "" ,"" , ""))

CBCRVReport = (reportform.format("CoinBase", "" , 0.6, 0, 0, 0 , 0, CBUSCRV , CBUSCRV, CBGBPCRV, CBGBPCRV,"" , ""))

reportCRV = (reportform.format("Bitstamp", timeStamp , 0.4, 0, 2, "7 CRV", 0, parsedBst[62]["bid"] , parsedBst[62]["ask"] , "", "", parsedBst[62]["percent_change_24"] , parsedBst[62]["volume"]))

#Synthetix
sign = "SNX"

#cb
CBUSSNX = round(1/float(dataUSD["data"]["rates"]["SNX"]), 5)
CBGBPSNX = round(1/float(dataCBGBP["data"]["rates"]["SNX"]), 5)

#Bitfinex
urlUSD = "https://api-pub.bitfinex.com/v2/tickers?symbols=t"+sign+"USD"
bfresponse = requests.get(urlUSD, headers=headers)

if len(bfresponse.json()) !=0:
    bfUSdata = bfresponse.json()[0]

urlGBP = "https://api-pub.bitfinex.com/v2/tickers?symbols=t"+sign+"GBP"
bfresponse = requests.get(urlGBP, headers=headers)
bflen()

BFSNXReport = (reportform.format("Bitfinex", "" , 0.2, 0.1, 0.1,"1.2711 SNX", 0, bfUSdata[1] , bfUSdata[3], "", "" ,"" , ""))


CBSNXReport = (reportform.format("CoinBase", "" , 0.6, 0, 0, 0 , 0, CBUSSNX , CBUSSNX, CBGBPSNX, CBGBPSNX,"" , ""))

reportSNX = (reportform.format("Bitstamp", timeStamp , 0.4, 0, 2, "4 SNX", 0, parsedBst[64]["bid"] , parsedBst[64]["ask"] , "", "", parsedBst[64]["percent_change_24"] , parsedBst[64]["volume"]))

#Uniswap
sign = "UNI"

#cb
CBUSUNI = round(1/float(dataUSD["data"]["rates"]["UNI"]), 5)
CBGBPUNI = round(1/float(dataCBGBP["data"]["rates"]["UNI"]), 5)

#Bitfinex
urlUSD = "https://api-pub.bitfinex.com/v2/tickers?symbols=t"+sign+"USD"
bfresponse = requests.get(urlUSD, headers=headers)

if len(bfresponse.json()) !=0:
    bfUSdata = bfresponse.json()[0]

urlGBP = "https://api-pub.bitfinex.com/v2/tickers?symbols=t"+sign+"GBP"
bfresponse = requests.get(urlGBP, headers=headers)
bflen()

BFUNIReport = (reportform.format("Bitfinex", "" , 0.2, 0.1, 0.1,"0.35809 UNI", 0, bfUSdata[1] , bfUSdata[3], "", "" ,"" , ""))

CBUNIReport = (reportform.format("CoinBase", "" , 0.6, 0, 0, 0 , 0, CBUSUNI , CBUSUNI, CBGBPUNI, CBGBPUNI,"" , ""))

reportUNI = (reportform.format("Bitstamp", timeStamp , 0.4, 0, 2, "2 UNI", 0, parsedBst[66]["bid"] , parsedBst[66]["ask"] , "", "", parsedBst[66]["percent_change_24"] , parsedBst[66]["volume"]))



file1 = open('CryptoData.txt', 'w')

n = file1.writelines("\n")

for i in currencies:
    file1.writelines(i)
    file1.writelines("\n \n")
    file1.writelines(HeadingData)
    file1.writelines("\n")
    file1.writelines(globals()["report" + i])
    file1.writelines("\n")
    file1.writelines(globals()["CB"+i+"Report"])
    file1.writelines("\n")
    file1.writelines(globals()["BF" + i + "Report"])
    file1.writelines("\n")
    file1.writelines("\n")

file1.close()

#Calculation

BstReports = []
CBReports = []
BFReports = []

BstXferFeeStr = ""
BstXferFee = 0


currencyRpt = []

#Put all currency reports for an exchange into one

for i in range(0, len(currencies)):
    currencyRpt = globals()["report" + currencies[i]].split(",")
    currencyRpt.append(currencies[i])
    currencyRptCB = globals()["CB"+currencies[i]+"Report"].split(",")
    currencyRptCB.append(currencies[i])
    currencyRptBF = globals()["BF" + currencies[i] + "Report"].split(",")
    currencyRptBF.append(currencies[i])
    #print("currencyRptBF", currencyRptBF)
    for j in range(0, len(currencyRpt)):
        currencyRpt[j] = currencyRpt[j].replace(" ", "")
    BstReports.append(currencyRpt)
    currencyRpt = []
    for j in range(0, len(currencyRptCB)):
        currencyRptCB[j] = currencyRptCB[j].replace(" ", "")
    CBReports.append(currencyRptCB)
    currencyRptCB = []
    for j in range(0, len(currencyRptBF)):
        currencyRptBF[j] = currencyRptBF[j].replace(" ", "")
    BFReports.append(currencyRptBF)
    currencyRptBF = []


totalGain = 0
BsttoCBOver0 = []
BsttoBFOver0 = []
BFtoBstOver0 = []
#print("BstReportsInit", BstReports)
#print("currencyRptCB", CBReports)
#print("currencyRptBF", BFReports)

# Buy Bst Sell CB
for i in range(0, len(BstReports)):

    if len(BstReports[i])>=8 and len(CBReports[i])>=8:
        bidBst = float(BstReports[i][8])
        #print("bstreports[i][8]", BstReports[i][8])
        #print("bidBst", float(bidBst))
        askCB = float(CBReports[i][7])
       # print("bidask", bidBst, askCB)
        if(float(BstReports[i][8])< float(CBReports[i][7])):
           # print("YES, Bst to CB", BstReports[i][-1], BstReports[i][8], CBReports[i][7])
            gain = (100/bidBst*askCB-100)
            totalGain =  gain - (0.004*bidBst) - 2
            #print("Bst to CB", BstReports[i][-1], BstReports[i][8], CBReports[i][7], "totalgain", totalGain)
            if totalGain >0:
               # print("Buy Bst Sell BF //", "Currency - ", currencies[i], totalGain)
                BsttoCB = ["totalGain", totalGain, "Curr", BstReports[i][-1], "Ask", BstReports[i][8], "Bid", CBReports[i][7]]
                BsttoCBOver0.append(BsttoCB)
                BsttoCB = []

if len(BsttoCBOver0) ==0:
    print("Buy Bst Sell CB - No Arbitrage Opportunities")
else:
    print("Buy Bst Sell GB", BsttoCBOver0)



for i in range(0, len(BstReports)):
    if len(BstReports[i]) >= 8 and len(BFReports[i]) >= 8:
        #Get Bst transfer fee
        for j in BstReports[i][5]:
            if j in nums or j == ".":
                BstXferFeeStr += j
        BstXferFee = float(BstXferFeeStr)
        BstXferFeeStr = ""
        #get bid / ask for exchanges
        bidBst = float(BstReports[i][7])
        askBF = float(BFReports[i][8])
        bidBF = float(BFReports[i][7])
        askBst = float(BstReports[i][8])

    #print("BstXferFee", BstXferFee)

        #Buy Bitstamp Sell Bitfinex

        if float(BstReports[i][8]) < float(BFReports[i][7]):
            #gain is percentage
            gain = ((100 / askBst * bidBF)-100)
            #totalGain based on hypothetical $100. Figures are approximate.
            totalGain =  gain - (0.004*askBst) - 2 - (0.001*askBst) - BstXferFee*askBst
            if totalGain >0:
                print("Buy Bst Sell BF //", "Currency - ", currencies[i], totalGain)
                BsttoBF = ["totalGain", totalGain, "Curr", BstReports[i][-1], "Ask", BstReports[i][8], "Bid", BFReports[i][7]]
                BsttoBFOver0.append(BsttoBF)
                BsttoBF = []


            #Buy Bitfinex Sell Bitstamp

        if (float(BFReports[i][8]) < float(BstReports[i][7])):
            gain = ((100 / askBF * bidBst) - 100)
            totalGain = gain - 0.2*askBF - 0.1*askBF - 2
            if totalGain >0:
                BFtoBst = ["totalGain", totalGain, "Curr", BFReports[i][-1], "Ask", BFReports[i][8], "Bid", BstReports[i][7]]
                BFtoBstOver0.append(BFtoBst)
                BFtoBst = []



if len(BsttoBFOver0) == 0:
    print("Buy Bst Sell BF - No Arbitrage Opportunities")
else:
    print("Buy Bst Sell BF", BsttoBFOver0)

if len(BFtoBstOver0) == 0:
    print("Buy BF Sell Bst - No Arbitrage Opportunities")
else:
    print("Buy BF Sell Bst", BFtoBstOver0)






