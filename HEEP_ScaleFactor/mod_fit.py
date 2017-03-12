import ROOT
ROOT.gROOT.SetBatch(ROOT.kTRUE)

from mod_settings import *

##########################################################################################
#                                      Create fit                                        #
##########################################################################################
class fit_object:
    def __init__(self):
        self.rrv_mee = ROOT.RooRealVar('m','m(ee) [GeV]', lower_mee, upper_mee)
        
        self.gauss_mean  = ROOT.RooRealVar('non-DY #mu'   , 'Gaussian #mu', 130,  0, 200)
        self.gauss_sigma = ROOT.RooRealVar('non-DY #sigma', 'Gaussian #sigma',  50, 20, 500)
        self.gauss       = ROOT.RooGaussian('Gauss', 'Gaussian', self.rrv_mee, self.gauss_mean, self.gauss_sigma)
        
        self.CB1_mean  = ROOT.RooRealVar('CB1 #mu'    , '',    0)
        self.CB1_sigma = ROOT.RooRealVar('CB1 #sigma' , '',  0.5)
        self.CB1_alpha = ROOT.RooRealVar('CB1 #alpha' , '', 80.0)
        self.CB1_n     = ROOT.RooRealVar('CB1 n'      , '',  0.5)
        self.CB1       = ROOT.RooCBShape('CB1', 'Cystal Ball Function', self.rrv_mee, self.CB1_mean, self.CB1_sigma, self.CB1_alpha, self.CB1_n)
        
        self.CB2_mean  = ROOT.RooRealVar('CB2 #mu'    , '',  0.1)
        self.CB2_sigma = ROOT.RooRealVar('CB2 #sigma' , '',  0.5)
        self.CB2_alpha = ROOT.RooRealVar('CB2 #alpha' , '', 80.0)
        self.CB2_n     = ROOT.RooRealVar('CB2 n'      , '',  0.5)
        self.CB2       = ROOT.RooCBShape('CB2', 'Cystal Ball Function', self.rrv_mee, self.CB2_mean, self.CB2_sigma, self.CB2_alpha, self.CB2_n)
        
        self.Voigt_mean  = ROOT.RooRealVar('Voigt #mu'   , 'Voigt #mu'   , 91.8, 50, 120)
        self.Voigt_width = ROOT.RooRealVar('Voigt width' , 'Voigt width' , 2.0,  0,  50)
        self.Voigt_sigma = ROOT.RooRealVar('Voigt #sigma', 'Voigt #sigma', 2.0,  0,  50)
        self.Voigt = ROOT.RooVoigtian('Voigtian', 'Voigtian', self.rrv_mee, self.Voigt_mean, self.Voigt_width, self.Voigt_sigma)
        
        self.fCB1   = ROOT.RooRealVar('f(CB1)'   , 'Fraction of CB1 events' , 1e3, 0, 1e9)
        self.fCB2   = ROOT.RooRealVar('f(CB2)'   , 'Fraction of CB2 events' , 1e3, 0, 1e9)
        self.nDY    = ROOT.RooRealVar('n(DY)'    , 'Number of DY events'    , 1e3, 0, 1e9)
        self.nNonDY = ROOT.RooRealVar('n(non-DY)', 'Number of non DY events', 1e3, 0, 1e9)
        
        self.dCB     = ROOT.RooAddPdf('dCB', '', ROOT.RooArgList(self.CB1, self.CB2), ROOT.RooArgList(self.fCB1,self.fCB2))
        self.VoigtdCB = ROOT.RooFFTConvPdf('VoigtxCB', '', self.rrv_mee, self.Voigt, self.dCB)
#        self.model = ROOT.RooAddPdf('model', 'DY+nonDY', ROOT.RooArgList(self.VoigtdCB, self.gauss), ROOT.RooArgList(self.nDY,self.nNonDY))
        
        # RooBreitWigner
        self.bw_mean = ROOT.RooRealVar('bw_mean'    , 'BreitWigner mean'                 , 91.2, 88.2, 94.2)
        self.bw_width= ROOT.RooRealVar('bw_width'  , 'BreitWigner width'                ,    1,    0,   50)
        self.bw      = ROOT.RooBreitWigner('BreitWigner', 'BreitWigner', self.rrv_mee, self.bw_mean, self.bw_width)
        # Signal model- a bifurcated Gaussian.
        self.biGauss_mean   = ROOT.RooRealVar('mean'  , 'Bifurcated Gaussian #mu'     , 91.2, 88.2, 94.2)
        self.biGauss_sigmaL = ROOT.RooRealVar('sigmaL', 'Bifurcated Gaussian #sigma L',  2.5,  0.0, 50.0)
        self.biGauss_sigmaR = ROOT.RooRealVar('sigmaR', 'Bifurcated Gaussian #sigma R',  2.5,  0.0, 50.0)
        self.biGauss        = ROOT.RooBifurGauss('biGauss', 'Gaussian', self.rrv_mee, self.biGauss_mean, self.biGauss_sigmaL, self.biGauss_sigmaR)
        
        self.bwCovbiGauss   = ROOT.RooFFTConvPdf("bwCovbiGauss","bwCovbiGauss",self.rrv_mee ,bw,biGauss) 
        # Background model taken from AN-09-111.
        # Values taken from https://github.com/kalanand/UserCode/blob/master/TagAndProbe-2-2-8/test/Muon_TagProbeEDMAnalysis_example_cfg.py
        self.bkg_alpha = ROOT.RooRealVar('alpha', '#alpha', 124.0   ,  0.0, 150.0)
        self.bkg_beta  = ROOT.RooRealVar('beta' , '#beta' ,  -0.028 , -1.0,   1.0)
        self.bkg_gamma = ROOT.RooRealVar('gamma', '#gamma',   0.0379, -1.0,   0.5)
        self.bkg_zPole = ROOT.RooRealVar('zPole', 'z_Pole', 91.1876)
        self.bkg = ROOT.RooGenericPdf('bkg', 'bkg', 'exp(-gamma*(m-zPole))*erfc(beta*(alpha-m))', ROOT.RooArgList(self.rrv_mee, self.bkg_zPole, self.bkg_gamma, self.bkg_beta, self.bkg_alpha) )
        
        self.fDY = ROOT.RooRealVar('f(DY)', 'fraction of DY events', 0.9, 0.0, 1.0)
#        self.model = ROOT.RooAddPdf('model', 'DY+nonDY', ROOT.RooArgList(self.biGauss, self.bkg), ROOT.RooArgList(self.fDY))
        self.model = ROOT.RooAddPdf('model', 'DY+nonDY', ROOT.RooArgList(self.bwCovbiGauss, self.bkg), ROOT.RooArgList(self.fDY))
    def plot(self, RDH, canvas, printName, HEEPname, var_text, strname, cname, rname, OSSSname, aname, card):
        mee_frame = self.rrv_mee.frame()
        
        canvas.SetRightMargin(0.4)
        canvas.SetGridx(False)
        canvas.SetGridy(False)
        
        normalisation = ROOT.RooFit.Normalization(1.0,ROOT.RooAbsReal.RelativeExpected)
        RDH.plotOn(mee_frame, ROOT.RooFit.DataError(ROOT.RooAbsData.Auto))
        
        self.model.plotOn(mee_frame,normalisation)
        self.model.plotOn(mee_frame)
        self.model.plotOn(mee_frame, ROOT.RooFit.Components('bkg'), normalisation, ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineColor(ROOT.kRed))
#        self.model.plotOn(mee_frame, ROOT.RooFit.Components('Gauss'), normalisation, ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineColor(ROOT.kRed))
        self.model.paramOn(mee_frame, ROOT.RooFit.Layout(0.62,0.98,0.9))
        
        NParams = 7
        self.chi2 = mee_frame.chiSquare()
        self.NDof = mee_frame.GetNbinsX()
        self.NDof -= NParams
        self.chi2OverNDof = 0 if self.NDof==0 else self.chi2/self.NDof
        
        mee_frame.SetTitle('')
        
        mee_frame.GetXaxis().SetTitle('m(ee) [GeV]')
        mee_frame.GetXaxis().SetTitleSize(0.05)
        mee_frame.GetXaxis().SetLabelSize(0.04)
        mee_frame.GetXaxis().SetTitleOffset(0.8)
        
        mee_frame.GetYaxis().SetTitle('entries')
        mee_frame.GetYaxis().SetTitleSize(0.06)
        mee_frame.GetYaxis().SetLabelSize(0.04)
        mee_frame.GetYaxis().SetTitleOffset(0.7)
        
        labels = make_labels([HEEPname, strname, cname, rname, OSSSname, aname], chi2=self.chi2, NDof=self.NDof, chi2OverNDof=self.chi2OverNDof, vartext=var_text, lumi=card.lumi)
        
        labels['lumibeam'].SetY(0.38)
        labels['OSSS'    ].SetY(0.14)
        labels['region'  ].SetY(0.20)
        
        for lname in labels:
            labels[lname].SetX(0.62)
            labels[lname].SetTextAlign(12)
        
        labels['OSSS'    ].SetX(0.85)
        labels['region'  ].SetX(0.85)
        for lname in labels:
            mee_frame.addObject(labels[lname])
        
        mee_frame.Draw()
        
        canvas.Print(printName)

    def fill_parameter_histogram(self,histograms, param_name, param, vBin):
        histograms['%s_value'%param_name].SetBinContent(vBin, param.  getVal())
        histograms['%s_value'%param_name].SetBinError  (vBin, param.getError())
        histograms['%s_range'%param_name].SetBinContent(vBin, 0.5*(param.getMin()+param.getMax()))
        histograms['%s_range'%param_name].SetBinError  (vBin, 0.5*(param.getMin()-param.getMax()))
        
    def fill_all_parameter_histograms(self,fh,vBin):
        self.fill_parameter_histogram(fh, 'GaussMu'   , self.gauss_mean , vBin)
        self.fill_parameter_histogram(fh, 'GaussSigma', self.gauss_sigma, vBin)
        self.fill_parameter_histogram(fh, 'CBMu'      , self.CB1_mean   , vBin)
        self.fill_parameter_histogram(fh, 'CBSigma'   , self.CB1_sigma  , vBin)
        self.fill_parameter_histogram(fh, 'CBAlpha'   , self.CB1_alpha  , vBin)
        self.fill_parameter_histogram(fh, 'CBN'       , self.CB1_n      , vBin)
        self.fill_parameter_histogram(fh, 'VoigtMu'   , self.Voigt_mean , vBin)
        self.fill_parameter_histogram(fh, 'VoigtWidth', self.Voigt_sigma, vBin)
        self.fill_parameter_histogram(fh, 'VoigtSigma', self.Voigt_mean , vBin)
    
    
    
