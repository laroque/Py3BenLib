#!/usr/bin/python3
'''
  Find the literal FWHM of a TH1 derived object.
'''
import ROOT,numpy

def LiteralFWHM(hist, low, high, givebin):
    '''
      Find the literal FWHM of a peak in an interval. This is done by finding the global max of the interval. From the max moving out, the first bin is found with a value < 1/2 Max. Assuming local linearity and that the bin content is the actual value at the bin center, the location of the half max is estimated. The x-axis distance between these location of these nearest half maxes is taken as the FWHM.

      Inputs:
        hist: histogram containing the data, must inherit from ROOT.TH1
        low: the lower limit of the search interval
        high: the upper limit of the fit interval
        givebin: unless givebin evaluates as True, <low> and <high> are assumed to by x-axis coordinate values, and the bin containing each is taken as the bin limits. If True, then <low> and <high> are interpreted as the bin numbers.

      Return:
        Returns the FWHM in x-axis units.

      WARNING:
        It is left to the user to decide if the peak is "clean" enough for this method. That is, if bin contents are not large compared to the noise, this algorithm does not let it "average out" in the same way that a fit would.
    '''
    # Need bounds in bin number
    if not givebin:
        low = hist.GetXaxis().FindBin(low)
        high = hist.GetXaxis().FindBin(high)

    # Need to get values for the interval into an array:
    values = numpy.array([])
    for binN in range(low, high+1):
        values = numpy.append(values,hist.GetBinContent(binN))

    # Find each half max position
    halfmax = max(values) / 2.
    under = numpy.where(values < halfmax)[0]
    highunderindex = numpy.where(under > numpy.where(values == max(values))[0][0])[0][0]
    lowunderbin = int(low + under[highunderindex - 1])
    highunderbin = int(low + under[highunderindex])
    xlower1 = hist.GetBinCenter(lowunderbin)
    ylower1 = hist.GetBinContent(lowunderbin)
    xlower2 = hist.GetBinCenter(lowunderbin+1)
    ylower2 = hist.GetBinContent(lowunderbin+1)
    xupper1 = hist.GetBinCenter(highunderbin)
    yupper1 = hist.GetBinContent(highunderbin)
    xupper2 = hist.GetBinCenter(highunderbin-1)
    yupper2 = hist.GetBinContent(highunderbin-1)
    xlower = ((halfmax - ylower1) * (xlower2 - xlower1))/(ylower2 - ylower1) + xlower1
    xupper = ((halfmax - yupper1) * (xupper2 - xupper1))/(yupper2 - yupper1) + xupper1

    fwhm = xupper - xlower
    return fwhm
