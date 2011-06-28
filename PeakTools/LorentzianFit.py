#!/usr/bin/python3
'''
  Peak fitting functions (based on ROOT) will functions within this module.
'''
import ROOT

def LorentzianFit(hist, low, high, bininput = False, minarea = 0., maxarea = 1E6, starea = False, minfwhm = 0., maxfwhm = 1E6, stfwhm = False):
    '''
      Fit a single Lorentzian function to an interval

      Inputs:
        hist: histogram containing the data to fit, must inherit from ROOT.TH1
        low: the lower limit of the fit interval
        high: the upper limit of the fit interval
        givebin: unless givebin evaluates as True, limits given are assumed to be in x-axis coordinates, not bin number (unless the are the same).
        minarea: min value set for the area parameter
        maxarea: max value set for the area parameter
        starea:  starting guess for the area parameter (if False, use mid point of min and max)
        minfwhm: min value set for the FWHM parameter
        maxfwhm: max value set for the FWHM parameter
        stfwhm:  starting guess for the fwhm parameter (if False, use mid point of min and max)

      Return:
        Returns a dictionary of fit parameters and their uncertainties.

      Wishlist:
        Add fit quality to returns?
    '''
    # Setup the fit function
    fitfun = ROOT.TF1('fitfun', '(([0] / [3]) * ((0.5 * [1]) / ((x-[2])**2 + (0.5 * [1])**2)))',low,high)
    # [0] is the area under the fit
    # [1] is the FWHM of the peak
    # [2] is the x position of the center
    # [3] is pi = 3.14........
    fitfun.SetParNames('area','fwhm','center','pi')
    fitfun.FixParameter(3, ROOT.TMath.Pi())
    if not starea:
        starea = (minarea + maxarea) / 2.0
    fitfun.SetParameter(0, starea)
    fitfun.SetParLimits(0, minarea, maxarea)
    if not stfwhm:
        stfwhm = (minfwhm + maxfwhm) / 2.0
    fitfun.SetParameter(1, stfwhm)
    fitfun.SetParLimits(1, minfwhm, maxfwhm)
    fitfun.SetParameter(2, (high + low) / 2.)
    fitfun.SetParLimits(2, low, high)
   
    # Do the fit, grab the resulting parameter values and return.
    hist.Fit('fitfun','RBMQ')
    # R uses the range set in fitfun
    # B uses the parameter bounds set for fitfun
    # M tries to do a better fit
    # Q suppresses output
    answer = {}
    for parami,param in enumerate(['area','fwhm','center']):
        answer[param] = fitfun.GetParameter(param)
        answer[param + '_error'] = fitfun.GetParError(parami)
    answer['ChiSquare']=fitfun.GetChisquare()
    answer['NDegreesFreedom']=fitfun.GetNDF()
    return answer
