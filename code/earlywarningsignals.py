#!/bin/python3

import scipy.stats
import numpy as np

## Description of the collection of functions

def check_time_series(input):
    ## Dummy function.
    return 'Hello world!'

def logtransform(ts):
    
    """Compute the logtransform of the original timeseries
    
    :param ts: original timeseries with variables in rows
    :return: logtransform of ts 

    
    Created by Ingrid van de Leemput
    """
    ts_log = np.log(ts+1)
    return ts_log

def EWS(timeseries,autocorrelation=False,variance=False,skewness=False):
    
    """Function that calculates early warning signals
    
    :param timeseries: Original timeseries (first column time indixes, other 
    columns time series for different variables)
    :param autocorrelation: Set to True if autocorrelation is required in output
    :param variance: Set to True if variance is required in output
    :param skewness: Set to True if skewness is required in output
    :return: dict with the chosen output and for every output an array with the   
    values for each variable (every column).
    
    """
    
    nr_vars=len(timeseries[0,:])-1
    result={}
    
    if autocorrelation == True:
        AC=[0]*nr_vars
        for i in range(nr_vars):
            AC[i]=np.corrcoef(timeseries[1:,i+1],timeseries[:-1,i+1])[1,0]
            result.update({'autocorrelation' : AC})
            
    if variance == True:
        Var=[0]*nr_vars
        for i in range(nr_vars):
            Var[i]=np.var(timeseries[:,i+1])
            result.update({'variance' : Var})
            
    if skewness == True:
        Skews=[0]*nr_vars
        for i in range(nr_vars):
            Skews[i]=scipy.stats.skew(timeseries[:,i+1])
            result.update({'skewness' : Skews})
            
        
        
    return result

def apply_rolling_window(ts,winsize=50):
    
    """Re-arrange time series for rolling window
    
    :param ts: original timeseries (one-dimensional!!)
    :param winsize:  the size of the rolling window expressed as percentage of the timeseries length (must be numeric between 0 and 100). Default is 50\%.
    :return: matrix of different windows

    !! This function can only handle one-dimensional timeseries, and we don't check for that (yet)
    Created by Ingrid van de Leemput
    """
    
    # WE SHOULD CHECK HERE THAT ts is one-dimensional.. 
    
    mw=round(ts.size * winsize/100) # length moving window
    omw=ts.size-mw+1 # number of moving windows
    nMR = np.empty(shape=(omw,mw))
    nMR[:] = np.nan
    
    #not needed in this function: 
    low=2 
    high=mw 
    x = range(1,mw) 
    
    for i in range(0,omw):
        nMR[i,:]=ts[i:i+mw]  
    return nMR

def kendalltau(indicatorvec):
    ## Kendall trend statistic
    timevec = range(len(indicatorvec))
    tau, p_value = scipy.stats.kendalltau(timevec,indicatorvec)
    return [tau, p_value]

# temporary input for Kendall trend statistic (remove when other functions are ready)
nARR = [2,3,4,6,7,8,5,9,10,20]
nACF = [2,3,4,6,7,8,5,9,10,20]
nSD = [2,3,4,6,7,8,5,9,10,20]
nSK = [2,3,4,6,7,8,5,9,10,20]
nKURT = [2,3,4,6,7,8,5,9,10,20]
nDENSITYRATIO = [2,3,4,6,7,8,5,9,10,20]
nRETURNRATE = [2,3,4,6,7,8,5,9,10,20]
nCV = [2,3,4,6,7,8,5,9,10,20]

# Estimate Kendall trend statistic for indicators (ouput: [Tau,p_value])
KtAR=kendalltau(nARR)
KtACF=kendalltau(nACF)
KtSD=kendalltau(nSD)
KtSK=kendalltau(nSK)
KtKU=kendalltau(nKURT)
KtDENSITYRATIO=kendalltau(nDENSITYRATIO)
KtRETURNRATE=kendalltau(nRETURNRATE)
KtCV=kendalltau(nCV)

#print Kendall output (to be removed later?)
print('\nKtAR (Tau,p_value): %.4f, %.4f' % (KtAR[0],KtAR[1]))
print('\nKtACF (Tau,p_value): %.4f, %.4f' % (KtACF[0],KtACF[1]))
print('\nKtSD (Tau,p_value): %.4f, %.4f' % (KtSD[0],KtSD[1]))
print('\nKtSK (Tau,p_value): %.4f, %.4f' % (KtSK[0],KtSK[1]))
print('\nKtKU (Tau,p_value): %.4f, %.4f' % (KtKU[0],KtKU[1]))
print('\nKtDENSITYRATIO (Tau,p_value): %.4f, %.4f' % (KtDENSITYRATIO[0],KtDENSITYRATIO[1]))
print('\nKtRETURNRATE (Tau,p_value): %.4f, %.4f' % (KtRETURNRATE[0],KtRETURNRATE[1]))
print('\nKtCV (Tau,p_value): %.4f, %.4f' % (KtCV[0],KtCV[1]))

#Interpolation function
def interpolate(x, y, new_x = None, dim = 1, method = 'linear', spline = False, k = 3, s = 0, der = 0):
    """
    Function interpolates data with in one or two dimension. Returns interpolated data.
    x: Original data point coordinates or time in case of time series. If dim = 2 then it should be a 2-dim array/float/tuple. Required value.
    y: Original data values. Must be the same dimension as x. If dim = 2 then it should a 2-dim array/float/tuple. Required value.
    new_x: Points at which to interpolate data. For 2-dim it should a grid. Required value.
    dim: Specifies dimension of data. Currently only for 1 or 2 dimensions. Default is 1
    method: Specifies interpolation method used. One of
    	‘nearest’: return the value at the data point closest to the point of interpolation.
        'linear’: interpolates linearly between data points on new data points
        'cubic’: Interpolated values determined from a cubic spline
        Default is ‘linear’
    spline: Spline interpolation. Can be True or False. If True then the function ignores the method call. Default is False. 
    k: Degree of the smoothing spline. Must be <= 5. Default is k=3, a cubic spline. 
    der: The order of derivative of the spline to compute (must be less than or equal to k)
    Created by M Usman Mirza
    """
    if dim == 1 & spline == False:
        f = interp1d(x = x, y = y, kind = method)
        i = f(new_x)
        return i
    elif dim == 2 & spline == False:
        i = griddata(points = x, values = y, xi = new_x, method = method)
        return i
    elif dim == 1 & spline == True:
        f = splrep(x = x, y = y, k = k, s = s)
        i = splev(x = new_x, tck = f, der = der)
        return i
    elif dim == 2 & spline == True:
        f = bisplrep(x = x[:,0], y = x[:,1], z = y, k = k, s = s)
        i = bisplev(x = new_x[:,0], y = new_x[0,:], tck = f)
        return i
    else:
        print('Dimension > 2 not supported')