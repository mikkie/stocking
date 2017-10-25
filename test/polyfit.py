import numpy as np
import pandas as pd

def trendline(data, order=1):
    coeffs = np.polyfit(data.index.values, list(data), order)
    slope = coeffs[-2]
    return float(slope)

#Sample Dataframe
revenue = [10, 9,8, 7, 6, 5, 4, 3]
year = [1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000]
df = pd.DataFrame({'year': year, 'revenue': revenue})


slope = trendline(df['revenue'])
print(slope)