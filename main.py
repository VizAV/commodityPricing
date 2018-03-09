# Author: VIshwanath AV
# Description: Reads the APMC data and the MSP data from a data file, groups them and pushes them into the DB

from dataClass import cAPMC, cMSP
from database import dataBase
import pandas as pd

def main():
    #read and treat input
    APMCdata = cAPMC(pd.read_csv('./data/Monthly_data_cmo.csv'))
    MSPdata = cMSP(pd.read_csv('./data/CMO_MSP_Mandi.csv'))

    # Assign DB name
    dB = dataBase('socialCops')

    #GRoup Data
    APMCdata.groupData()

    #update Data
    dB.updateDB("APMC",APMCdata.groupList)

    # GRoup Data
    MSPdata.groupData()

    # update Data
    dB.updateDB("MSP",MSPdata.groupList)



if __name__=="__main__":
    main()