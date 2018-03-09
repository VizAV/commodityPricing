import pandas as pd
from dataClass import cAPMC,removeOutlier,interpolateData,cMSP,extrapolateData
from statsmodels.tsa import seasonal

def main():

    APMCdata,MSPdata=readInput()
    APMCdata.groupData()
    MSPdata.groupData()
    flucData = getFluctuation(APMCdata.groupList,MSPdata.groupList)
    flucData=flucData.reset_index()
    flucData.to_csv('./data/flucData.csv',index=False)
def readInput():
    APMCdata = cAPMC(pd.read_csv('./data/Monthly_data_cmo.csv'))
    MSPdata = cMSP(pd.read_csv('./data/CMO_MSP_Mandi.csv'))
    return APMCdata,MSPdata
def getFluctuation(APMCgroupList,MSPgroupList):
    #Calculating the fluctuation for each APMC and Commodity
    print("Calculating the fluctuation for each APMC and Commodity")
    flucData = pd.DataFrame()
    for APMCdata in APMCgroupList:
        for commodityData in APMCdata['commodityList']:
            mspData = [data for data in MSPgroupList if data['Name'] == commodityData['Name']]
            if len(mspData)>0:
                data = stationarity(commodityData['salesList'],mspData[0]['salesList'])
            else:
                data = stationarity(commodityData['salesList'])
            try:
                # data['fluc']=data['deSeasonalized'].diff()
                data['Commodity']=commodityData['Name']
                data['APMC']=APMCdata['Name']
                flucData = pd.concat([flucData, data[['date']+['fluc'] + ['APMC'] + ['Commodity']+['diff']]], axis=0)
            except:
                continue
    return flucData


def stationarity(data,mspdata=None):
    data=pd.DataFrame(data)

    data.set_index('date',inplace=True)
    data = removeOutlier(data)
    data= interpolateData(data)
    if mspdata:
        mspdata = pd.DataFrame(mspdata)
        mspdata.set_index('date', inplace=True)
        mspdata=extrapolateData(mspdata,data.index)

    try:
        decompData = seasonal.seasonal_decompose(data['modal_price'], model='multiplicative', freq=4)
        # Multiply the trend and residue to get the de-seasonalized value
        data['deSeasonalized'] = decompData.resid * decompData.trend
        data['fluc'] = data['deSeasonalized'].diff()
        if mspdata.shape[0]:
            data['diff']=data['deSeasonalized']-mspdata['price']
        data.reset_index(inplace=True)
        return data
    except:
        pass

def analysis():
    inpFile = pd.read_csv('./data/flucData.csv')
    # inpFile['date'] = pd.to_datetime(inpFile['date'], format='%Y-%m-%d')
    flucDiffList=[]
    # diffList=[]
    seasonList=[]
    for APMC in list(inpFile['APMC'].unique()):
        # print(APMC)
        APMCData=inpFile[(inpFile['APMC']==APMC)]
        # print(APMCData.shape)
        for commodity in list(APMCData['Commodity'].unique()):
            # print(commodity)
            commodityData = APMCData[APMCData['Commodity']==commodity]
            # print (commodityData['fluc'].max(),commodityData['fluc'].argmax())
            try:
                flucDiffList.append(pd.Series([APMC,commodity,commodityData['fluc'].max(),commodityData.loc[commodityData['fluc'].idxmax(),'date'],commodityData['diff'].max(),commodityData.loc[commodityData['diff'].idxmax(),'date']],index=['APMC','commodity','max_fluc','date_max_fluc','max_diff','date_max_diff']))
            except:
                continue


    for date in list(inpFile['date'].unique()):
        dateData=inpFile[inpFile['date']==date]
        # dateData=dateData[(dateData['fluc'].notnull()) &(dateData['diff'].notnull())]
        try:
             seasonList.append(pd.Series([date,dateData['fluc'].max(),dateData.loc[dateData['fluc'].argmax(),'APMC'],
                                         dateData.loc[dateData['fluc'].argmax(),'Commodity'],
                                        dateData['diff'].max(), dateData.loc[dateData['diff'].argmax(), 'APMC'],dateData.loc[dateData['diff'].argmax(), 'Commodity']
            ],index=['date','max_fluc','max_fluc_APMC','max_fluc_commodity','max_diff','max_diff_APMC','max_diff_commodity']))
        except:
            continue


    flucDiffData=pd.DataFrame(flucDiffList)
    flucDiffData.to_csv('./data/flucDiffMaxAPMCCOmmodity.csv')

    seasonData=pd.DataFrame(seasonList)
    seasonData.to_csv('./data/flucDiffMaxDate.csv')

if __name__=='__main__':
    # main()
    analysis()