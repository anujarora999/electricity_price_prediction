import numpy as np
import pandas as pd


class Weightcalculation:
    def __init__(self,data):
        self.data = data
        
    
    def getdayaverages(self,data,sheet_name):
        df = pd.read_excel(self.data,sheet_name=sheet_name)
        df['Lt~'] = df['Lt']/13
        df['Lt-Lt~'] = df['Lt'] - df['Lt~']
        df['Ltp~'] = df['Ltp']/13
        df['Ltp-Ltp~'] = df['Ltp'] - df['Ltp~']
        df['Lt-1~'] = df['Lt-1']/13
        df['Lt-1 - Lt-1~'] = df['Lt-1'] - df['Lt-1~']
        df['Lt-1p~'] = df['Lt-1p']/13
        df['Lt-1p - Lt-1p~'] = df['Lt-1p'] - df['Lt-1p~']
        df['Pt~'] = df['Pt']/13
        df['Pt-Pt~'] = df['Pt'] - df['Pt~']

        df['Ptp~'] = df['Ptp']/13
        df['Ptp-Ptp~'] = df['Ptp'] - df['Ptp~']
        df['Pt-1~'] = df['Pt-1']/13
        df['Pt-1 - Pt-1~'] = df['Pt-1'] - df['Pt-1~']
        df['Pt-1p~'] = df['Pt-1p']/13
        df['Pt-1p - Pt-1p~'] = df['Pt-1p'] - df['Pt-1p~']
        columns = ['14:15 - 14:30','Lt','Lt~','Lt-Lt~','Ltp','Ltp~','Ltp-Ltp~','Lt-1','Lt-1~','Lt-1 - Lt-1~','Lt-1p','Lt-1p~',
                       'Lt-1p - Lt-1p~','Pt','Pt~','Pt-Pt~','Ptp','Ptp~', 'Ptp-Ptp~','Pt-1','Pt-1~', 'Pt-1 - Pt-1~','Pt-1p',
                       'Pt-1p~', 'Pt-1p - Pt-1p~']

        df = df[columns]
        L1 = df['Lt-Lt~']
        L2 = df['Ltp-Ltp~']
        L3 = df['Lt-1 - Lt-1~']
        L4 = df['Lt-1p - Lt-1p~']
        P1 = df['Pt-Pt~']
        P2 = df['Ptp-Ptp~']
        P3 = df['Pt-1 - Pt-1~']
        P4 = df['Pt-1p - Pt-1p~']

        df['Numerator_without_weights'] = L1*L2 + L3*L4 + P1*P2 + P3*P4
        df['Denominator_without_weights'] = np.sqrt((L1*L1)+(L3*L3)+(P1*P1)+(P3*P3)) * np.sqrt((L2*L2)+(L4*L4)+(P2*P2)+(P4*P4))
        df['Correlation_coeff_without_weights'] = df['Numerator_without_weights']/df['Denominator_without_weights']
        similardays_without_wts = df.nlargest(3,'Correlation_coeff_without_weights')
        similardays_without_wts = similardays_without_wts[['Ltp','Lt-1p','Ptp','Pt-1p']]
        similardays_without_wts = similardays_without_wts.rename(columns={'Ltp':'x1','Lt-1p':'x2','Ptp':'x3','Pt-1p':'x4'})
        average = similardays_without_wts.mean(axis=0)
        average = pd.DataFrame(average).T
        return average

    def getdataforinverse(self): # HARDCODED 
        day1 = self.getdayaverages(self.data,"24th")
        day2 = self.getdayaverages(self.data,"25th")
        day3 = self.getdayaverages(self.data,"26th")
        day4 = self.getdayaverages(self.data,"27th")
        day5 = self.getdayaverages(self.data,"28th")
        day6 = self.getdayaverages(self.data,"29th")
        day7 = self.getdayaverages(self.data,"30th")

        finaldf = pd.concat([day1,day2,day3,day4,day5,day6,day7])
        finaldf['y'] = [2441.04,2199.5,2503.08,2562.93,2889.51,2673.16,2744.24] # ADDED MANUALLY !

        finaldf['x1^2'] = finaldf['x1']*finaldf['x1']
        finaldf['x2^2'] = finaldf['x2']*finaldf['x2']
        finaldf['x3^2'] = finaldf['x3']*finaldf['x3']
        finaldf['x4^2'] = finaldf['x4']*finaldf['x4']

        finaldf['x1*x2'] = finaldf['x1']*finaldf['x2']
        finaldf['x1*x3'] = finaldf['x1']*finaldf['x3']
        finaldf['x1*x4'] = finaldf['x1']*finaldf['x4']

        finaldf['x2*x3'] = finaldf['x2']*finaldf['x3']
        finaldf['x2*x4'] = finaldf['x2']*finaldf['x4']

        finaldf['x3*x4'] = finaldf['x3']*finaldf['x4']

        finaldf['x1*y'] = finaldf['x1']*finaldf['y']
        finaldf['x2*y'] = finaldf['x2']*finaldf['y']
        finaldf['x3*y'] = finaldf['x3']*finaldf['y']
        finaldf['x4*y'] = finaldf['x4']*finaldf['y']
        
        summation = pd.DataFrame(finaldf.sum(axis=0)).T

        return summation
    
    
    def findweights(self):
        summation = self.getdataforinverse()
        n = 7
        matrix =  [[n,summation['x1'].values[0],summation['x2'].values[0],summation['x3'].values[0],summation['x4'].values[0]],
                  [summation['x1'].values[0],summation['x1^2'].values[0],summation['x1*x2'].values[0], summation['x1*x3'].values[0],summation['x1*x4'].values[0]],
                  [summation['x2'].values[0],summation['x1*x2'].values[0],summation['x2^2'].values[0],summation['x2*x3'].values[0],summation['x2*x4'].values[0]],
                  [summation['x3'].values[0],summation['x1*x3'].values[0], summation['x2*x3'].values[0], summation['x3^2'].values[0],summation['x3*x4'].values[0]],
                    [summation['x4'].values[0],summation['x1*x4'].values[0],summation['x2*x4'].values[0],summation['x3*x4'].values[0],summation['x4^2'].values[0]]]

        cols = ['x0','x1','x2','x3','x4']
        matrix = pd.DataFrame(matrix)
        matrix.columns = cols

        INVERSE = pd.DataFrame(np.linalg.inv(matrix))
        INVERSE.columns = ["x0","x1","x2","x3","x4"]

        yvals = [summation['y'].values[0],summation['x1*y'].values[0],summation['x2*y'].values[0],summation['x3*y'].values[0],summation['x4*y'].values[0]]
        INVERSE['y'] = yvals

        Inverse = np.array(INVERSE.iloc[:,:5])
        y = np.array(INVERSE['y'])

        weights = np.matmul(y,Inverse).tolist()
        INVERSE['weights'] = weights
        return weights
    
    
    def forecastprice(self,forecastdata):
        x0,x1,x2,x3,x4 = self.findweights()
        df = pd.read_excel(forecastdata,sheet_name="Sheet1")
        df['Lt~'] = df['Lt']/13
        df['Lt-Lt~'] = df['Lt'] - df['Lt~']
        df['Ltp~'] = df['Ltp']/13
        df['Ltp-Ltp~'] = df['Ltp'] - df['Ltp~']
        df['Lt-1~'] = df['Lt-1']/13
        df['Lt-1 - Lt-1~'] = df['Lt-1'] - df['Lt-1~']
        df['Lt-1p~'] = df['Lt-1p']/13
        df['Lt-1p - Lt-1p~'] = df['Lt-1p'] - df['Lt-1p~']
        df['Pt~'] = df['Pt']/13
        df['Pt-Pt~'] = df['Pt'] - df['Pt~']

        df['Ptp~'] = df['Ptp']/13
        df['Ptp-Ptp~'] = df['Ptp'] - df['Ptp~']
        df['Pt-1~'] = df['Pt-1']/13
        df['Pt-1 - Pt-1~'] = df['Pt-1'] - df['Pt-1~']
        df['Pt-1p~'] = df['Pt-1p']/13
        df['Pt-1p - Pt-1p~'] = df['Pt-1p'] - df['Pt-1p~']
        columns = ['14:15 - 14:30','Lt','Lt~','Lt-Lt~','Ltp','Ltp~','Ltp-Ltp~','Lt-1','Lt-1~','Lt-1 - Lt-1~','Lt-1p','Lt-1p~',
                       'Lt-1p - Lt-1p~','Pt','Pt~','Pt-Pt~','Ptp','Ptp~', 'Ptp-Ptp~','Pt-1','Pt-1~', 'Pt-1 - Pt-1~','Pt-1p',
                       'Pt-1p~', 'Pt-1p - Pt-1p~']

        df = df[columns]
        L1wt = df['Lt-Lt~']*x1
        L2wt = df['Ltp-Ltp~']*x2
        L3wt = df['Lt-1 - Lt-1~']*x3
        L4wt = df['Lt-1p - Lt-1p~']*x4
        P1wt = df['Pt-Pt~']*x1
        P2wt = df['Ptp-Ptp~']*x2
        P3wt = df['Pt-1 - Pt-1~']*x3
        P4wt = df['Pt-1p - Pt-1p~']*x4
        df['Numerator_with_weights'] = L1wt*L2wt + L3wt*L4wt + P1wt*P2wt + P3wt*P4wt
        df['Denominator_with_weights'] = np.sqrt((L1wt*L1wt)+(L3wt*L3wt)+(P1wt*P1wt)+(P3wt*P3wt)) * np.sqrt((L2wt*L2wt)+(L4wt*L4wt)+(P2wt*P2wt)+(P4wt*P4wt))
        df['Correlation_coeff_with_weights'] = abs(df['Numerator_with_weights']/df['Denominator_with_weights'])
        
        similardays_with_wts = df.nlargest(3,'Correlation_coeff_with_weights')
        similardays_with_wts = similardays_with_wts[['Ltp','Lt-1p','Ptp','Pt-1p']]
        forecastprice = x0 + np.mean(similardays_with_wts['Ltp']*x1) + np.mean(similardays_with_wts['Lt-1p']*x2) + np.mean(similardays_with_wts['Ptp']*x3) + np.mean(similardays_with_wts['Pt-1p']*x4)
        return forecastprice

if __name__ == "__main__":

    data = "pythondata.xlsx"
    forecastdata = "2novforecast.xlsx"

    wt = Weightcalculation(data)

    print(f"Weights => {wt.findweights()}")
    print("\n")
    print(f'Forecasted Price => {wt.forecastprice(forecastdata)}')