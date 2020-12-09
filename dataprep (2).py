import os
import pandas as pd
from datetime import datetime, timedelta

def openpricefiles():
    cwd = os.path.abspath('') 
    files = os.listdir(cwd) 
    df = pd.DataFrame()
    for file in files:
        if file.endswith('.xlsx') and "p" in file:
            df = df.append(pd.read_excel(file), ignore_index=True) 
    return df 

def openloadfiles():
    cwd = os.path.abspath('') 
    files = os.listdir(cwd) 
    df = pd.DataFrame()
    for file in files:
        if file.endswith('.xlsx') and "L" in file:
            df = df.append(pd.read_excel(file), ignore_index=True) 
    return df

# this willbe used once we have data for last 45 days in the dataframe 
def getNdates(): # last 45 days 
    N_DAYS_AGO = 7
    today = pd.to_datetime("2020-10-27")
    firstday = today - timedelta(days=N_DAYS_AGO)
    secondday = firstday - timedelta(days=N_DAYS_AGO)
    thirdday = secondday - timedelta(days=N_DAYS_AGO)
    fourday = thirdday - timedelta(days=N_DAYS_AGO)
    fifthday = fourday - timedelta(days=N_DAYS_AGO)
    reqdates = [today,firstday,secondday,thirdday,fourday,fifthday]
    reqdates = [x.strftime('%Y-%m-%d') for x in reqdates]
    reqdates.sort(key=lambda date: datetime.strptime(date, "%Y-%m-%d"))
    return reqdates

datelist = getNdates()
pricedf = openpricefiles()
loaddf = openloadfiles()

def getfinaldf():
    nextslot = "0:45 - 1:00"
    prevslot = "0:15 - 0:30"
    currslot = "0:30 - 0:45"

    # PRICEVALS 
    torepeat = len(pricedf['Date'].unique())
    pt = pricedf.loc[(pricedf['Date']==datelist[-1]) & (pricedf['Time Slots']==currslot)]['MCP'].reset_index(drop=True)[0]
    pt_ = [pt]*(torepeat-1)
    ptprev = pricedf.loc[(pricedf['Date']==datelist[-1]) & (pricedf['Time Slots']==prevslot)]['MCP'].reset_index(drop=True)[0]
    ptprev_ = [ptprev]*(torepeat-1)

    ptpvals = []
    ptpprevvals = []
    for i in range(-2,-7,-1):
        ptp = pricedf.loc[(pricedf['Date']==datelist[i]) & (pricedf['Time Slots']==currslot)]['MCP'].reset_index(drop=True)[0]
        ptp_prev = pricedf.loc[(pricedf['Date']==datelist[i]) & (pricedf['Time Slots']==prevslot)]['MCP'].reset_index(drop=True)[0]
        ptpvals.append(ptp)
        ptpprevvals.append(ptp_prev)
        
    # LOAD VALS 

    lt = loaddf.loc[(loaddf['Date']==datelist[-1]) & (loaddf['Time Slots']==currslot)]['MCV'].reset_index(drop=True)[0]
    lt_ = [lt]*(torepeat-1)
    ltprev = loaddf.loc[(loaddf['Date']==datelist[-1]) & (loaddf['Time Slots']==prevslot)]['MCV'].reset_index(drop=True)[0]
    ltprev_ = [ltprev]*(torepeat-1)

    ltpvals = []
    ltpprevvals = []
    for i in range(-2,-7,-1):
        ltp = loaddf.loc[(loaddf['Date']==datelist[i]) & (loaddf['Time Slots']==currslot)]['MCV'].reset_index(drop=True)[0]
        ltp_prev = loaddf.loc[(loaddf['Date']==datelist[i]) & (loaddf['Time Slots']==prevslot)]['MCV'].reset_index(drop=True)[0]
        ltpvals.append(ltp)
        ltpprevvals.append(ltp_prev)

    result = pd.DataFrame({f"{currslot}":datelist[::-1][:5],"Pt":pt_,"Pt-1":ptprev_,"Ptp":ptpvals,"Ptp-1":ptpprevvals,
                        "Lt":lt_,"Lt-1":ltprev_,"Ltp":ltpvals,"Ltp-1":ltpprevvals})
    return result 

if __name__ == "__main__":
    result = getfinaldf()
    print(result)