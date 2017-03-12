import math

from mod_settings import *
from mod_fit      import fit_object

##########################################################################################
#                                 Binnings for histograms                                #
##########################################################################################
pi = 3.15
nBins_phi_fit_B = 20
nBins_phi_fit_T =  4
nBins_phi_fit_E = 10
lower_phi_fit = -pi
upper_phi_fit =  pi

nBins_phi_cut_B = 30
nBins_phi_cut_T =  4
nBins_phi_cut_E = 10
lower_phi_cut = -pi
upper_phi_cut =  pi

nBins_phi_fine = 300
lower_phi_fine = -pi
upper_phi_fine =  pi

phi_boundaries_fit_B = []
phi_boundaries_fit_T = []
phi_boundaries_fit_E = []
phi_boundaries_cut_B = []
phi_boundaries_cut_T = []
phi_boundaries_cut_E = []
phi_boundaries_fine  = []

for i in range(0,nBins_phi_fit_B+1):
    phi_boundaries_fit_B.append(lower_phi_fit+(upper_phi_fit-lower_phi_fit)*i/nBins_phi_fit_B)
for i in range(0,nBins_phi_fit_T+1):
    phi_boundaries_fit_T.append(lower_phi_fit+(upper_phi_fit-lower_phi_fit)*i/nBins_phi_fit_T)
for i in range(0,nBins_phi_fit_E+1):
    phi_boundaries_fit_E.append(lower_phi_fit+(upper_phi_fit-lower_phi_fit)*i/nBins_phi_fit_E)
for i in range(0,nBins_phi_cut_B+1):
    phi_boundaries_cut_B.append(lower_phi_cut+(upper_phi_cut-lower_phi_cut)*i/nBins_phi_cut_B)
for i in range(0,nBins_phi_cut_T+1):
    phi_boundaries_cut_T.append(lower_phi_cut+(upper_phi_cut-lower_phi_cut)*i/nBins_phi_cut_T)
for i in range(0,nBins_phi_cut_E+1):
    phi_boundaries_cut_E.append(lower_phi_cut+(upper_phi_cut-lower_phi_cut)*i/nBins_phi_cut_E)
for i in range(0,nBins_phi_fine+1):
    phi_boundaries_fine.append(lower_phi_fine+(upper_phi_fine-lower_phi_fine)*i/nBins_phi_fine)

phi_boundaries_fit = {}
phi_boundaries_cut = {}
phi_boundaries_fit['Barrel'    ] = phi_boundaries_fit_B
phi_boundaries_fit['Transition'] = phi_boundaries_fit_T
phi_boundaries_fit['Endcap'    ] = phi_boundaries_fit_E
phi_boundaries_cut['Barrel'    ] = phi_boundaries_cut_B
phi_boundaries_cut['Transition'] = phi_boundaries_cut_T
phi_boundaries_cut['Endcap'    ] = phi_boundaries_cut_E

Et_boundaries_fit = {}
Et_boundaries_cut = {}
Et_boundaries_fine = []
nBins_Et_fine = 250
for i in range(0,nBins_Et_fine):
    Et_boundaries_fine.append(0+250.0*i/nBins_Et_fine)
Et_boundaries_fine.append(5000)
Et_boundaries_fit['Barrel'    ] = [20,25,30,35,40,45,60,100,250]
Et_boundaries_fit['Endcap'    ] = [20,35,60,100,250]
Et_boundaries_fit['Transition'] = [35,60,100,250]
Et_boundaries_cut['Barrel'    ] = [35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,65,70,75,100,250]
#Et_boundaries_cut['Barrel'    ] = [20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,65,70,75,100,250]
Et_boundaries_cut['Transition'] = [35,41,50,250]
#Et_boundaries_cut['Transition'] = [20,25,30,35,41,50,250]
#Et_boundaries_cut['Endcap'    ] = [35,36,37,38,39,40,41,42.5,44,46,50,70,250]
Et_boundaries_cut['Endcap'    ] = [35,36,37,38,39,40,41,42,43,45,50,70,250]
#Et_boundaries_cut['Endcap'    ] = [20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42.5,44,46,50,70,250]

nBins_eta_fit = 8
lower_eta_fit = -3.0
upper_eta_fit =  3.0

nBins_eta_fine = 240
lower_eta_fine = -3.0
upper_eta_fine =  3.0

eta_boundaries_fit_tmp = []
eta_boundaries_fine = []
for i in range(0,nBins_eta_fit+1):
    eta_boundaries_fit_tmp.append(lower_eta_fit+(upper_eta_fit-lower_eta_fit)*i/nBins_eta_fit)
for i in range(0,nBins_eta_fine+1):
    eta_boundaries_fine.append(lower_eta_fit+(upper_eta_fine-lower_eta_fine)*i/nBins_eta_fine)

eta_boundaries_cut_tmp = []
eta_boundaries_cut_tmp.append( 1.4442)
eta_boundaries_cut_tmp.append( 1.566 )

eta_boundaries_cut_tmp.append(0.1)
eta_boundaries_cut_tmp.append(0.2)
eta_boundaries_cut_tmp.append(0.3)
eta_boundaries_cut_tmp.append(0.4)
eta_boundaries_cut_tmp.append(0.5)
eta_boundaries_cut_tmp.append(0.6)
eta_boundaries_cut_tmp.append(0.8)
eta_boundaries_cut_tmp.append(1.0)
eta_boundaries_cut_tmp.append(1.2)

eta_boundaries_cut_tmp.append(1.8)
eta_boundaries_cut_tmp.append(2.0)
eta_boundaries_cut_tmp.append(2.2)
#eta_boundaries_cut_tmp.append(2.4)
eta_boundaries_cut_tmp.append(2.5)
bins_tmp = []
for ebct in eta_boundaries_cut_tmp:
    bins_tmp.append( ebct)
    bins_tmp.append(-ebct)
eta_boundaries_cut_tmp = bins_tmp
eta_boundaries_cut_tmp.append(0.0)

eta_boundaries_fit_tmp.append(-1.566 )
eta_boundaries_fit_tmp.append(-1.4442)
eta_boundaries_fit_tmp.append( 1.4442)
eta_boundaries_fit_tmp.append( 1.566 )
eta_boundaries_fine.append(-1.566 )
eta_boundaries_fine.append(-1.4442)
eta_boundaries_fine.append( 1.4442)
eta_boundaries_fine.append( 1.566 )

eta_boundaries_fit_tmp  = sorted(eta_boundaries_fit_tmp)
eta_boundaries_fine = sorted(eta_boundaries_fine)

eta_boundaries_fit = {}
eta_boundaries_cut = {}
eta_boundaries_fit['Barrel'    ] = eta_boundaries_fit_tmp
eta_boundaries_fit['Transition'] = eta_boundaries_fit_tmp
eta_boundaries_fit['Endcap'    ] = eta_boundaries_fit_tmp
eta_boundaries_cut['Barrel'    ] = eta_boundaries_cut_tmp
eta_boundaries_cut['Transition'] = eta_boundaries_cut_tmp
eta_boundaries_cut['Endcap'    ] = eta_boundaries_cut_tmp

nBins_nVtx = 16
nVtx_boundaries_tmp = [-0.5]
for i in range(5,nBins_nVtx+1):
    nVtx_boundaries_tmp.append(-0.5+i)
nVtx_boundaries_tmp.append(20)
#nVtx_boundaries_tmp.append(30)
nVtx_boundaries_tmp.append(40)
nVtx_boundaries_fine = nVtx_boundaries_tmp
nVtx_boundaries_fit = {}
nVtx_boundaries_cut = {}
nVtx_boundaries_fit['Barrel'    ] = nVtx_boundaries_tmp
nVtx_boundaries_fit['Transition'] = nVtx_boundaries_tmp
nVtx_boundaries_fit['Endcap'    ] = nVtx_boundaries_tmp
nVtx_boundaries_cut['Barrel'    ] = nVtx_boundaries_tmp
nVtx_boundaries_cut['Transition'] = nVtx_boundaries_tmp
nVtx_boundaries_cut['Endcap'    ] = nVtx_boundaries_tmp

##########################################################################################
#                                   Create variables                                     #
##########################################################################################
class variable_object:
    def __init__(self, name, latex, unit, binBoundaries_fit, binBoundaries_cut, binBoundaries_fine):
        self.name  = name
        self.latex = latex
        self.unit  = unit
        self.binBoundaries_fit  = binBoundaries_fit
        self.binBoundaries_cut  = binBoundaries_cut
        self.binBoundaries_fine = sorted(binBoundaries_fine)
        self.card = nominal_card
    def set_card(self, card):
        self.card = card
    def make_hBases(self):
        self.nBins_fit     = {}
        self.lower_fit     = {}
        self.upper_fit     = {}
        self.binsArray_fit = {}
        self.hBase_1D_fit  = {}
        self.hBase_2D_fit  = {}
        
        self.nBins_cut     = {}
        self.lower_cut     = {}
        self.upper_cut     = {}
        self.binsArray_cut = {}
        self.hBase_1D_cut  = {}
        self.hBase_2D_cut  = {}
        
        self.nBins_fine = len(self.binBoundaries_fine)-1
        self.lower_fine = self.binBoundaries_fine[ 0]
        self.upper_fine = self.binBoundaries_fine[-1]
        self.binsArray_fine = array.array('d', self.binBoundaries_fine)
        
        self.hBase_1D_fine = ROOT.TH1F('hBase_%s_fine'%(self.name), '', self.nBins_fine, self.binsArray_fine)
        self.hBase_1D_fine.GetXaxis().SetTitle('%s'%self.name)
        self.hBase_1D_fine.GetYaxis().SetTitle('Efficiency')
        self.hBase_1D_fine.SetLineColor(ROOT.kBlack)
        self.hBase_1D_fine.SetMarkerColor(ROOT.kBlack)
        self.hBase_1D_fine.SetMarkerStyle(20)
        
        self.hBase_2D_fine = ROOT.TH2F('hBase_%s_fine_mee'%(self.name), '', self.nBins_fine, self.binsArray_fine, nBins_mee, lower_mee, upper_mee)
        self.hBase_2D_fine.GetXaxis().SetTitle('%s'%self.name)
        self.hBase_2D_fine.GetYaxis().SetTitle('m(ee) [GeV/c^{2}]')
        
        for rname in regionNames:
            self.binBoundaries_fit[rname] = sorted(self.binBoundaries_fit[rname])
            self.nBins_fit[rname] = len(self.binBoundaries_fit[rname])-1
            self.lower_fit[rname] = self.binBoundaries_fit[rname][ 0]
            self.upper_fit[rname] = self.binBoundaries_fit[rname][-1]
            self.binsArray_fit[rname] = array.array('d', self.binBoundaries_fit[rname])
        
            h_fit_1D = ROOT.TH1F('hBase_1D_fit_%s_%s'%(self.name,rname), '', self.nBins_fit[rname], self.binsArray_fit[rname])
            h_fit_1D.GetXaxis().SetTitle('%s'%self.name)
            h_fit_1D.GetYaxis().SetTitle('#varepsilon(HEEP)')
            h_fit_1D.SetLineColor(ROOT.kBlack)
            h_fit_1D.SetMarkerColor(ROOT.kBlack)
            h_fit_1D.SetMarkerStyle(20)
            self.hBase_1D_fit[rname] = h_fit_1D
        
            h_fit_2D = ROOT.TH2F('hBase_2D_fit_%s_%s_mee'%(self.name,rname), '', self.nBins_fit[rname], self.binsArray_fit[rname], nBins_mee, lower_mee, upper_mee)
            h_fit_2D.GetXaxis().SetTitle('%s'%self.name)
            h_fit_2D.GetYaxis().SetTitle('m(ee) [GeV/c^{2}]')
            self.hBase_2D_fit[rname] = h_fit_2D
            
            self.binBoundaries_cut[rname] = sorted(self.binBoundaries_cut[rname])
            self.nBins_cut[rname] = len(self.binBoundaries_cut[rname])-1
            self.lower_cut[rname] = self.binBoundaries_cut[rname][ 0]
            self.upper_cut[rname] = self.binBoundaries_cut[rname][-1]
            self.binsArray_cut[rname] = array.array('d', self.binBoundaries_cut[rname])
        
            h_cut_1D = ROOT.TH1F('hBase_1D_cut_%s_%s'%(self.name,rname), '', self.nBins_cut[rname], self.binsArray_cut[rname])
            h_cut_1D.GetXaxis().SetTitle('%s'%self.name)
            h_cut_1D.GetYaxis().SetTitle('#varepsilon(HEEP)')
            h_cut_1D.SetLineColor(ROOT.kBlack)
            h_cut_1D.SetMarkerColor(ROOT.kBlack)
            h_cut_1D.SetMarkerStyle(20)
            self.hBase_1D_cut[rname] = h_cut_1D
        
            h_cut_2D = ROOT.TH2F('hBase_2D_cut_%s_%s_mee'%(self.name,rname), '', self.nBins_cut[rname], self.binsArray_cut[rname], nBins_mee, lower_mee, upper_mee)
            h_cut_2D.GetXaxis().SetTitle('%s'%self.name)
            h_cut_2D.GetYaxis().SetTitle('m(ee) [GeV/c^{2}]')
            self.hBase_2D_cut[rname] = h_cut_2D
    
    def fit_spectrum(self, samples, rname, cname, tname, strname, aname, OSSSname, PUWname, fit_eff_histograms, cut_eff_histograms, fOut):
        fOut.cd()
        nDY_values_cut = {}
        nDY_errors_cut = {}
        
        suffix = '%s_%s_%s_%s_%s_%s'%(self.name, strname, rname, cname, aname, OSSSname)
        h_fit_eff = self.hBase_1D_fit[rname].Clone('h_tmp_fit_eff_%s'%suffix)
        h_cut_eff = self.hBase_1D_cut[rname].Clone('h_tmp_cut_eff_%s'%suffix)
        
        if self.card.options['do_fits'] == True:
            pname = '%s/fit_%s_%s_%s_%s_%s_%s_%s.pdf'%(self.card.plot_prefix, rname, strname, cname, tname, self.name, OSSSname, aname)
            canvas.Print('%s['%pname)
            nDY_values_fit = {}
            nDY_errors_fit = {}
            
            h_2D_fit = {}
            for HEEPname in self.card.HEEP_names:
                # Get and manipulate histograms
                args = (self.name, rname, cname, tname, HEEPname, OSSSname, aname, PUWname)
                histos = get_histos_from_args(args, strname, samples, self.card)
                h_2D_fit[HEEPname] = histos['fit']
                    
                labels = make_labels([HEEPname, strname, cname, rname, OSSSname, aname], lumi=self.card.lumi)
                
                canvas.SetRightMargin(0.45)
                h_2D_fit[HEEPname].Draw('colz')
                for lname in labels:
                    labels[lname].Draw()
                canvas.Print('%s/h_fit_2D_%s.pdf'%(self.card.plot_prefix,self.card.name))
            
            for vBin in range(1, h_2D_fit['probes'].GetNbinsX()+1):
                nDY_values_fit[vBin] = {}
                nDY_errors_fit[vBin] = {}
                
                for HEEPname in self.card.HEEP_names:
                    hName = 'h_mee_fit_%s_%d__%s_%s_%s_%s_%s_%s_%s_%s'%(self.name, vBin, strname, rname, cname, tname, OSSSname, HEEPname, aname, PUWname)
                    h_1D_fit = hBase_mee.Clone(hName)
                    for mBin in range(1, h_2D_fit[HEEPname].GetNbinsY()+1):
                        value = h_2D_fit[HEEPname].GetBinContent(vBin, mBin)
                        error = h_2D_fit[HEEPname].GetBinError  (vBin, mBin)
                        h_1D_fit.SetBinContent(mBin, value)
                        h_1D_fit.SetBinError  (mBin, error)
                    
                    if h_1D_fit.GetSumOfWeights() < minNEventsPerFit:
                        nDY_values_fit[vBin][HEEPname] = 0
                        nDY_errors_fit[vBin][HEEPname] = 0
                        continue
                    
                    # Make the fit object here so that all slices start with exactly the same
                    # starting parameters.
                    f = fit_object()
                    
                    h_1D_fit.Rebin(2)
                    for bin in range(1, h_1D_fit.GetNbinsX()+1):
                        if h_1D_fit.GetBinContent(bin)<0:
                            h_1D_fit.SetBinContent(bin,0)
                    
                    RDH = ROOT.RooDataHist('RDH', '', ROOT.RooArgList(f.rrv_mee), h_1D_fit)
                    result = f.model.fitTo(RDH, ROOT.RooFit.Minos(False), ROOT.RooFit.Range(lower_mee, upper_mee), ROOT.RooFit.Save(True), ROOT.RooFit.SumW2Error(True), ROOT.RooFit.PrintLevel(-1))
                    
                    lower =         h_2D_fit[HEEPname].GetXaxis().GetBinLowEdge(vBin)
                    upper = lower + h_2D_fit[HEEPname].GetXaxis().GetBinWidth  (vBin)
                    varText = '%.2f < %s < %.2f %s'%(lower, self.latex, upper, self.unit)
                    
                    f.plot(RDH, canvas, pname, HEEPname, varText, strname, cname, rname, OSSSname, aname, self.card)
                    
                    nDY_values_fit[vBin][HEEPname] = f.nDY.getVal()
                    nDY_errors_fit[vBin][HEEPname] = f.nDY.getError()
                    
                    h_1D_fit.Write('',ROOT.TObject.kOverwrite)
        
            canvas.Print('%s]'%pname)
        
            nCols = 101
            print '^%s^'%('='*nCols)
            print '^%25s%10s  %8s  %2s  %4s  %15s  %2s%25s^'%(' ',rname,strname,cname,self.name,aname,OSSSname,' ')
            print '^%20s|%28s|%28s|%22s^'%('   Variable range   ','       Passing probes       ','       All probes       ','      Efficiency     ')
            print '^%s^'%('-'*nCols)
        
            labels = make_labels([HEEPname, strname, cname, rname, OSSSname, aname], lumi=self.card.lumi)
            for vBin in range(1, h_fit_eff.GetNbinsX()+1):
                value_1HEEP = nDY_values_fit[vBin]['probes']
                error_1HEEP = nDY_errors_fit[vBin]['probes']
                value_2HEEP = nDY_values_fit[vBin]['pass'  ]
                error_2HEEP = nDY_errors_fit[vBin]['pass'  ]
        
                eff = 0.0 if value_1HEEP<1e-6 else value_2HEEP/value_1HEEP
                if eff>1 and value_2HEEP-value_1HEEP < 2*(error_1HEEP+error_2HEEP):
                    eff = 1.0
                err = 0.0 if value_1HEEP<1e-6 or value_2HEEP<1e-6 or eff<0 or eff>1  else math.sqrt(1.0/value_1HEEP+1.0/value_2HEEP)
            
                lower =       h_fit_eff.GetBinLowEdge(vBin)
                upper = lower+h_fit_eff.GetBinWidth  (vBin)
                print '^ %8.4f  %8.4f |  %10.3f +- %10.3f  |  %10.3f +- %10.3f  | %8.4f +- %8.4f'%(lower, upper, value_2HEEP, error_2HEEP, value_1HEEP, error_1HEEP, eff, err)
            
                h_fit_eff.SetBinContent(vBin, eff)
                h_fit_eff.SetBinError  (vBin, err)
        
            print '^%s^'%('='*nCols)
            h_fit_eff.Draw('pe')
            for lname in labels:
                labels[lname].Draw()
            canvas.Print('%s/h_fit_eff_%s.pdf'%(self.card.plot_prefix,self.card.name))
        
        
            suffix = '%s_%s_%s_%s_%s_%s_%s_%s_%s'%(self.name, strname, rname, cname, tname, HEEPname, OSSSname, aname, PUWname)
            hName_fit = 'h_fit_eff_%s'%suffix
            args = (self.name,rname,cname,aname,OSSSname,strname)
            fit_eff_histograms[args] = h_fit_eff.Clone(hName_fit)
            fit_eff_histograms[args].Write('',ROOT.TObject.kOverwrite)
    
        if self.card.options['do_cuts']==True:
            for HEEPname in self.card.HEEP_names:
                # Get and manipulate histograms
                args = (self.name, rname, cname, tname, HEEPname, OSSSname, aname, PUWname)
                histos = get_histos_from_args(args, strname, samples, self.card)
                h_2D_cut = histos['cut']
                
                labels = make_labels([HEEPname, strname, cname, rname, OSSSname, aname], lumi=self.card.lumi)
                
                canvas.SetRightMargin(0.45)
                h_2D_cut.Draw('colz')
                for lname in labels:
                    labels[lname].Draw()
                canvas.Print('%s/h_cut_2D_%s.pdf'%(self.card.plot_prefix,self.card.name))
            
                nDY_values_cut[HEEPname] = {}
                nDY_errors_cut[HEEPname] = {}
                
                for vBin in range(1, h_2D_cut.GetNbinsX()+1):
                    hName = 'h_mee_cut_%s_%d__%s_%s_%s_%s_%s_%s_%s_%s'%(self.name, vBin, strname, rname, cname, tname, OSSSname, HEEPname, aname, PUWname)
                    h_1D_cut = hBase_mee.Clone(hName)
                    value = 0
                    error = 0
                    for mBin in range(1, h_2D_cut.GetNbinsY()+1):
                        if h_2D_cut.GetYaxis().GetBinLowEdge(mBin)                                         > self.card.mee_range[1]:
                            continue
                        if h_2D_cut.GetYaxis().GetBinLowEdge(mBin) + h_2D_cut.GetYaxis().GetBinWidth(mBin) < self.card.mee_range[0]:
                            continue
                        value +=        h_2D_cut.GetBinContent(vBin, mBin)
                        error += math.pow(h_2D_cut.GetBinError(vBin, mBin),2)
                        h_1D_cut.SetBinContent(mBin, h_2D_cut.GetBinContent(vBin, mBin))
                        h_1D_cut.SetBinError  (mBin, h_2D_cut.GetBinError  (vBin, mBin))
                    h_1D_cut.Write('',ROOT.TObject.kOverwrite)
                
                    nDY_values_cut[HEEPname][vBin] = value
                    nDY_errors_cut[HEEPname][vBin] = math.sqrt(error)

            
            nCols = 101
            print '^%s^'%('='*nCols)
            print '^%25s%10s  %8s  %2s  %4s  %15s  %2s%25s^'%(' ',rname,strname,cname,self.name,aname,OSSSname,' ')
            print '^%20s|%28s|%28s|%22s^'%('   Variable range   ','       Passing probes       ','       All probes       ','      Efficiency     ')
            print '^%s^'%('-'*nCols)
        
            labels = make_labels([HEEPname, strname, cname, rname, OSSSname, aname], lumi=self.card.lumi)
            
            value_1HEEP_total=0            
            value_2HEEP_total=0            
            error_1HEEP_total=0            
            error_2HEEP_total=0            
            error_1HEEP_tmp=0            
            error_2HEEP_tmp=0            

            for vBin in range(1, h_cut_eff.GetNbinsX()+1):
                value_1HEEP = nDY_values_cut['probes'][vBin]
                error_1HEEP = nDY_errors_cut['probes'][vBin]
                value_2HEEP = nDY_values_cut['pass'  ][vBin]
                error_2HEEP = nDY_errors_cut['pass'  ][vBin]
                
                value_1HEEP_total+=value_1HEEP
                value_2HEEP_total+=value_2HEEP
                error_1HEEP_tmp+=math.pow(error_1HEEP,2)
                error_2HEEP_tmp+=math.pow(error_2HEEP,2)
           
                eff = 0.0 if value_1HEEP<1e-6 else value_2HEEP/value_1HEEP
                if eff>1 and value_2HEEP-value_1HEEP < 2*(error_1HEEP+error_2HEEP):
                    eff = 1.0
                err = 0
                if value_1HEEP>1e-6 and value_2HEEP>1e-6 and eff>=0 and eff<=1:
                    N1 = value_1HEEP
                    N2 = value_2HEEP
                    e1 = error_1HEEP/N1
                    e2 = error_2HEEP/N2
                    err = math.sqrt(abs((1-2*eff)*e2*e2+math.pow(eff*e1,2)/(N2*N2)))
                
                lower =       h_cut_eff.GetBinLowEdge(vBin)
                upper = lower+h_cut_eff.GetBinWidth  (vBin)
                print '^ %8.4f  %8.4f |  %10.3f +- %10.3f  |  %10.3f +- %10.3f  | %8.4f +- %8.4f ^'%(lower, upper, value_2HEEP, error_2HEEP, value_1HEEP, error_1HEEP, eff, err)
            
                h_cut_eff.SetBinContent(vBin, eff)
                h_cut_eff.SetBinError  (vBin, err)

            error_1HEEP_total=math.sqrt(error_1HEEP_tmp)
            error_2HEEP_total=math.sqrt(error_2HEEP_tmp)

            eff_total = 0.0 if value_1HEEP_total<1e-6 else value_2HEEP_total/value_1HEEP_total
            if eff_total>1 and value_2HEEP_total-value_1HEEP_total < 2*(error_1HEEP_total+error_2HEEP_total):
                eff_total=1
            error_total=0
            if value_1HEEP_total>1e-6 and value_2HEEP_total>1e-6 and eff_total>=0 and eff_total<=1:
                N1_total = value_1HEEP_total
                N2_total = value_2HEEP_total
                e1_total = error_1HEEP_total/N1_total
                e2_total = error_2HEEP_total/N2_total
                err_total = math.sqrt(abs((1-2*eff_total)*e2_total*e2_total+math.pow(eff_total*e1_total,2)/(N2_total*N2_total)))
            print '^ total:| %10.3f +- %10.3f  |  %10.3f +- %10.3f  | %8.4f +- %8.4f ^'%( value_2HEEP_total, error_2HEEP_total, value_1HEEP_total, error_1HEEP_total, eff_total, err_total)

            print '^%s^'%('='*nCols)
            h_cut_eff.Draw('pe')
            for lname in labels:
                labels[lname].Draw()
            canvas.Print('%s/h_cut_eff_%s.pdf'%(self.card.plot_prefix,self.card.name))
        
        
            suffix = '%s_%s_%s_%s_%s_%s_%s_%s_%s'%(self.name, strname, rname, cname, tname, HEEPname, OSSSname, aname, PUWname)
            hName_cut = 'h_cut_eff_%s'%suffix
            args = (self.name,rname,cname,aname,OSSSname,strname)
            cut_eff_histograms[args] = h_cut_eff.Clone(hName_cut)
            cut_eff_histograms[args].Write('',ROOT.TObject.kOverwrite)


variables = {}
variables['Et'   ] = variable_object('Et'  , 'E_{T}(probe)', 'GeV', Et_boundaries_fit  , Et_boundaries_cut   , Et_boundaries_fine  )
variables['eta'  ] = variable_object('eta' , '#eta(probe)' , ''   , eta_boundaries_fit , eta_boundaries_cut  , eta_boundaries_fine )
variables['phi'  ] = variable_object('phi' , '#phi(probe)' , ''   , phi_boundaries_fit , phi_boundaries_cut  , phi_boundaries_fine )
variables['nVtx' ] = variable_object('nVtx', 'n_{Vtx}'     , ''   , nVtx_boundaries_fit, nVtx_boundaries_cut , nVtx_boundaries_fine)

for vname in variables:
    variables[vname].make_hBases()
