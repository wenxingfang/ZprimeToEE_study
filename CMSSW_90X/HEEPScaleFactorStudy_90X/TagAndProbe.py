#import array, 
import math

from mod_settings import *
from mod_variable import variables
from mod_fit      import fit_object
from mod_sample   import samples, sample_object
from mod_plot     import kinematic_plots, compare_plot , gr_compare_plot, compare_plot_xmas

##########################################################################################
#                             Import ROOT and apply settings                             #
##########################################################################################
import ROOT
ROOT.gROOT.SetBatch(ROOT.kTRUE)

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetFrameBorderMode(ROOT.kWhite)
#ROOT.gStyle.SetFrameFillColor(ROOT.kWhite)
ROOT.gStyle.SetCanvasBorderMode(ROOT.kWhite)
#ROOT.gStyle.SetCanvasColor(ROOT.kWhite)
ROOT.gStyle.SetPadBorderMode(ROOT.kWhite)
#ROOT.gStyle.SetPadColor(ROOT.kWhite)
ROOT.gStyle.SetStatColor(ROOT.kWhite)

##########################################################################################
#                                 Tools for making plots                                 #
##########################################################################################
class histogram_wrapper:
    def __init__(self, histogram, legend_entry, style):
        self.h = histogram
        self.legend = legend_entry
        self.style = style
        self.style.style_histogram(self.h)

class SF_object:
    def __init__(self, name, title, hw_numer, hw_denom, strategy):
        self.hw_numer = hw_numer
        self.hw_denom = hw_denom
        self.name  = name
        self.title = title
        
        self.min =  1e6
        self.max = -1e6
        
        for h in [self.hw_numer.h,self.hw_denom.h]:
            for bin in range(1, h.GetNbinsX()+1):
                value = h.GetBinContent(bin)
                error = h.GetBinError  (bin)
                if value < 1e-3:
                    continue
                if value - error < self.min:
                    self.min = value - error
                if value + error > self.max:
                    self.max = value + error
        hName_ratio = '%s_%s_ratio'%(self.hw_numer.h.GetName(), self.name)
        h_ratio = self.hw_numer.h.Clone(hName_ratio)
        h_ratio.Sumw2()
        for bin in range(1,h_ratio.GetNbinsX()+1):
             if h_ratio.GetBinContent(bin) <0.01:
                 h_ratio.SetBinContent(bin,0)
                 h_ratio.SetBinError(bin,0)
        h_denom_tmp = self.hw_denom.h.Clone('%s_%s_tmp'%(self.hw_denom.h.GetName(), self.name))
        for bin in range(1,h_denom_tmp.GetNbinsX()+1):
            h_denom_tmp.SetBinError(bin,0)     
    
        if SF_consider_MC_eff_error is True:
            h_ratio.Divide(self.hw_denom.h)
        else: 
            h_ratio.Divide(h_denom_tmp)
        self.hw_numer.h.GetYaxis().SetTitle('Efficiency')
        self.hw_denom.h.GetYaxis().SetTitle('Efficiency')
#        h_ratio.GetYaxis().SetTitle('Scale factor')
        h_ratio.GetYaxis().SetTitle('')
        
        h_ratio.GetYaxis().SetTitleSize(0.18)
        if Increase_SF_ratio is True:
            self.hw_numer.h.GetYaxis().SetLabelSize(0.05)
            self.hw_denom.h.GetYaxis().SetLabelSize(0.05)
        h_ratio.GetYaxis().SetTitleOffset(0.3)
        
        h_ratio.GetYaxis().SetLabelSize(0.15)
        h_ratio.GetXaxis().SetLabelSize(0.15)
        h_ratio.GetXaxis().SetTitleSize(0.15)
        h_ratio.GetXaxis().SetTitleOffset(1.0)
        h_ratio.GetXaxis().SetTickLength(0.1)
        h_ratio.GetXaxis().SetMoreLogLabels()
        h_ratio.GetXaxis().SetNoExponent()
        self.hw_ratio = histogram_wrapper(h_ratio, 'ratio', self.hw_numer.style)
        
        # Fit a flat line.
        self.fConstant = ROOT.TF1('fConstant_%s'%self.hw_ratio.h.GetName(), '[0]')
#        self.fConstant.SetParameters(1.0,0.0)
        self.fConstant.SetParameters(0,1.0)
        self.fConstant.SetLineColor(self.hw_ratio.h.GetLineColor())
        self.fConstant.SetLineStyle(ROOT.kDashed)
        self.fConstant.SetLineWidth(2)
        self.hw_ratio.h.Fit(self.fConstant)
        self.chi2 = self.fConstant.GetChisquare()
        self.ndof = self.hw_ratio.h.GetNbinsX()-1

        self.a_value = self.fConstant.GetParameter(0)
        self.a_error = self.fConstant.GetParError (0)

        if self.ndof < 0:
            self.ndof = 0
        self.chi2_label   = ROOT.TLatex(0.15, 0.85, '#chi^{2}/ndof = %.2f/%d'%(self.chi2,self.ndof))
        self.params_label = ROOT.TLatex(0.85, 0.85, 'SF = %.3f (#pm %.3f)'%(self.a_value, self.a_error))
        self.chi2_label  .SetNDC()
        self.params_label.SetNDC()
        self.chi2_label  .SetTextAlign(12)
        self.params_label.SetTextAlign(32)
        self.chi2_label  .SetTextSize(0.12)
        self.params_label.SetTextSize(0.12)
        if Increase_SF_ratio is True:
            self.params_label.SetTextSize(0.06)

class gr_SF_object:
    def __init__(self, name, title, gw_numer, gw_denom, strategy):
        self.gw_numer = gw_numer
        self.gw_denom = gw_denom
        self.name  = name
        self.title = title
        
        self.min =  1e6
        self.max = -1e6
        
        for h in [self.gw_numer.h,self.gw_denom.h]:
            for bin in range(0, h.GetN()):
                value = h.GetY()[bin]
                error = h.GetErrorYhigh(bin)
                if value < 1e-3:
                    continue
                if value - error < self.min:
                    self.min = value - error
                if value + error > self.max:
                    self.max = value + error
        gName_ratio = '%s_%s_ratio'%(self.gw_numer.h.GetName(), self.name)
       # g_ratio=ROOT.TGraphAsymmErrors()
        g_ratio= self.gw_numer.h.Clone(gName_ratio)
        for bin in range(0, g_ratio.GetN()):
            numer      =self.gw_numer.h.GetY()[bin] 
            numer_err_L=self.gw_numer.h.GetErrorYlow(bin) 
            numer_err_U=self.gw_numer.h.GetErrorYhigh(bin) 
            denom      =self.gw_denom.h.GetY()[bin] 
            denom_err_L=self.gw_denom.h.GetErrorYlow(bin) 
            denom_err_U=self.gw_denom.h.GetErrorYhigh(bin) 
            ratio=float(numer/denom) if denom!=0 else 0
            ratio_err_L=ratio*math.sqrt(math.pow(numer_err_L/numer,2)+math.pow(denom_err_L/denom,2)) if numer!=0 and denom!=0 else 0
            ratio_err_U=ratio*math.sqrt(math.pow(numer_err_U/numer,2)+math.pow(denom_err_U/denom,2)) if numer!=0 and denom!=0 else 0
            g_ratio.SetPoint(bin,g_ratio.GetX()[bin],ratio)
            g_ratio.SetPointEYlow(bin,ratio_err_L)
            g_ratio.SetPointEYhigh(bin,ratio_err_U)
 
        self.gw_numer.h.GetYaxis().SetTitle('Efficiency')
        self.gw_denom.h.GetYaxis().SetTitle('Efficiency')
#        h_ratio.GetYaxis().SetTitle('Scale factor')
        g_ratio.GetYaxis().SetTitle('')
        
        g_ratio.GetYaxis().SetTitleSize(0.18)
        if Increase_SF_ratio is True:
            self.gw_numer.h.GetYaxis().SetLabelSize(0.05)
            self.gw_denom.h.GetYaxis().SetLabelSize(0.05)
        g_ratio.GetYaxis().SetTitleOffset(0.3)
        g_ratio.GetYaxis().SetLabelSize(0.15)
        g_ratio.GetXaxis().SetLabelSize(0.15)
        g_ratio.GetXaxis().SetTitleSize(0.15)
        g_ratio.GetXaxis().SetTitleOffset(1.0)
        g_ratio.GetXaxis().SetTickLength(0.1)
        g_ratio.GetXaxis().SetMoreLogLabels()
        g_ratio.GetXaxis().SetNoExponent()
        self.gw_ratio = histogram_wrapper(g_ratio, 'ratio', self.gw_numer.style)
        
        # Fit a flat line.
        self.fConstant = ROOT.TF1('fConstant_%s'%self.gw_ratio.h.GetName(), '[0]')
#        self.fConstant.SetParameters(1.0,0.0)
        self.fConstant.SetParameters(0,1.0)
        self.fConstant.SetLineColor(self.gw_ratio.h.GetLineColor())
        self.fConstant.SetLineStyle(ROOT.kDashed)
        self.fConstant.SetLineWidth(2)
        self.gw_ratio.h.Fit(self.fConstant)
        self.chi2 = self.fConstant.GetChisquare()
        self.ndof = self.gw_ratio.h.GetN()-1

        self.a_value = self.fConstant.GetParameter(0)
        self.a_error = self.fConstant.GetParError (0)

        if self.ndof < 0:
            self.ndof = 0
        self.chi2_label   = ROOT.TLatex(0.15, 0.85, '#chi^{2}/ndof = %.2f/%d'%(self.chi2,self.ndof))
        self.params_label = ROOT.TLatex(0.85, 0.85, 'SF = %.3f (#pm %.3f)'%(self.a_value, self.a_error))
        self.chi2_label  .SetNDC()
        self.params_label.SetNDC()
        self.chi2_label  .SetTextAlign(12)
        self.params_label.SetTextAlign(32)
        self.chi2_label  .SetTextSize(0.12)
        self.params_label.SetTextSize(0.12)
        if Increase_SF_ratio is True:
            self.params_label.SetTextSize(0.06)

def graph_add(g1,g2):
    x=array.array('f')
    x_low=array.array('f')
    x_high=array.array('f')
    y=array.array('f')
    y_low=array.array('f')
    y_high=array.array('f')
    for i in range(0,g1.GetN()):
        x.append(g1.GetX()[i])
        x_low.append(g1.GetErrorXlow(i))
        x_high.append(g1.GetErrorXhigh(i))
        y.append(g1.GetY()[i])
        y_low.append(g1.GetErrorYlow(i))
        y_high.append(g1.GetErrorYhigh(i))
    for i in range(0,g2.GetN()):
        x.append(g2.GetX()[i])
        x_low.append(g2.GetErrorXlow(i))
        x_high.append(g2.GetErrorXhigh(i))
        y.append(g2.GetY()[i])
        y_low.append(g2.GetErrorYlow(i))
        y_high.append(g2.GetErrorYhigh(i))
    g12=ROOT.TGraphAsymmErrors(len(x),x,y,x_low,x_high,y_low,y_high)
    return g12
        
##########################################################################################
#                                    Now do the study                                    #
##########################################################################################

ScaleFactors = {}

for card in deck_of_cards:
    print card.name , card.options
    
    for sname in samples:
        samples[sname].set_card(card)
    for vname in card.variable_names:
        variables[vname].set_card(card)

    if card.options['base_histograms']:
        fBase = ROOT.TFile('hBase.root','RECREATE')
        for vname in card.variable_names:
            v = variables[vname]
            v.hBase_1D_fine.Write()
            v.hBase_2D_fine.Write()
            for rname in card.region_names:
                v.hBase_1D_fit[rname].Write()
                v.hBase_2D_fit[rname].Write()
                v.hBase_1D_cut[rname].Write()
                v.hBase_2D_cut[rname].Write()
        fBase.Close()
    
    for sname in samples:
        samples[sname].load_histograms_from_file()

    if card.options['do_analysis'] and (card.options['do_fits'] or card.options['do_cuts']):
#        fOut = ROOT.TFile(card.filename_histos,'UPDATE')
        fOut = ROOT.TFile(card.filename_histos,'RECREATE')
    
        fOut.cd()
        cut_eff_histograms = {}
        fit_eff_histograms = {}
        if card.options['do_fits']:
            canvas.Print('%s/h_fit_eff_%s.pdf['%(card.plot_prefix,card.name))
            canvas.Print('%s/h_fit_2D_%s.pdf[' %(card.plot_prefix,card.name))
        if card.options['do_cuts']:
            canvas.Print('%s/h_cut_eff_%s.pdf['%(card.plot_prefix,card.name))
            canvas.Print('%s/h_cut_2D_%s.pdf[' %(card.plot_prefix,card.name))
        for vname in card.variable_names:
            v = variables[vname]
            for rname in card.region_names:
                for cname in card.charge_names:
                    for tname in card.tagCharge_names:
                        for aname in card.altCut_names:
                            for OSSSname in card.OSSS_names:
                                for strname in strategyNames:
                                    for PUname in card.PUW_names:
                                        v.fit_spectrum(samples, rname, cname, tname, strname, aname, OSSSname, PUname, fit_eff_histograms, cut_eff_histograms, fOut)
        if card.options['do_fits']:
            canvas.Print('%s/h_fit_eff_%s.pdf]'%(card.plot_prefix,card.name))
            canvas.Print('%s/h_fit_2D_%s.pdf]' %(card.plot_prefix,card.name))
        if card.options['do_cuts']:
            canvas.Print('%s/h_cut_eff_%s.pdf]'%(card.plot_prefix,card.name))
            canvas.Print('%s/h_cut_2D_%s.pdf]' %(card.plot_prefix,card.name))

        fOut.Close()
    
    if card.options['do_compare']:
        fCompare_out = ROOT.TFile(card.compare_histos ,'RECREATE')
        fCompare     = ROOT.TFile(card.filename_histos,'READ'    )
    
        methodNames = []
        if card.options['do_fits']:
            methodNames.append('fit')
        if card.options['do_cuts']:
            methodNames.append('cut')
    
        for mname in methodNames:
            for vname in card.variable_names:
                for rname in card.region_names:
                    for cname in card.charge_names:
                        for tname in card.tagCharge_names:
                            for aname in card.altCut_names:
                                for OSSSname in card.OSSS_names:
                                    for PUWname in card.PUW_names:
                                        for strname in ['exc','inc']:
                                            if vname == "Pt": continue
                                            # Get histograms.
                                            suffix = '%s_%s_%s_%s_pass_%s_%s_%s'%(strname, rname, cname,tname, OSSSname, aname, PUWname)##Change
                                            hName_data = 'h_%s_eff_%s_data_%s'%(mname,vname,suffix)
                                            hName_MC   = 'h_%s_eff_%s_MC_%s'  %(mname,vname,suffix)
                                            h_data = fCompare.Get(hName_data)
                                            h_MC   = fCompare.Get(hName_MC  )
                                            
                                            gName_data = 'g_%s_eff_%s_data_%s'%(mname,vname,suffix)
                                            gName_MC   = 'g_%s_eff_%s_MC_%s'  %(mname,vname,suffix)
                                            g_data = fCompare.Get(gName_data)
                                            g_MC   = fCompare.Get(gName_MC  )
                                            
                                            labels = make_labels(args=['CMS',OSSSname,aname,rname,cname,strname], lumi=card.lumi)
                                            suffix = '%s_%s_%s_%s_%s_%s_%s_%s_%s'%(mname,vname,rname,cname,tname,strname,OSSSname,aname,PUWname)
                                
                                            data_legend = 'Data' if strname=='inc' else 'Data (non DY subtracted)'
                                            MC_legend   = 'DY'   if strname=='exc' else 'DY+non-DY'
                                
                                            if not h_data or not h_MC or not g_data or not g_MC:
                                                fCompare.ls()
                                                print hName_data
                                                print hName_MC
                                                print gName_data
                                                print gName_MC
                                                print '!!'
                                
                                            hw_data = histogram_wrapper(h_data, data_legend, styles['data_%s'%strname])
                                            hw_MC   = histogram_wrapper(h_MC  ,   MC_legend, styles[  'MC_%s'%strname])
                                   
                                            gw_data = histogram_wrapper(g_data, data_legend, styles['data_%s'%strname])
                                            gw_MC   = histogram_wrapper(g_MC  ,   MC_legend, styles[  'MC_%s'%strname])
 
                                            SF = SF_object('', '', hw_data, hw_MC, strname)
                                            gr_SF = gr_SF_object('', '', gw_data, gw_MC, strname)
                                            ScaleFactors[(mname,vname,rname,cname,tname,aname,OSSSname,strname,PUWname)] = SF
                                    
                                            compare_plot([SF], labels, vname, suffix, card, fCompare_out)
                                            if do_poisson or do_asymmetric_error: gr_compare_plot([gr_SF], labels, vname, suffix, card, fCompare_out)
                                
                                        # Get histograms.
                                        suffix = '%s_%s_%s_pass_%s_%s_%s'%(rname, cname, tname, OSSSname, aname, PUWname)##Change
                                        hName_data_inc = 'h_%s_eff_%s_data_inc_%s'%(mname,vname,suffix)
                                        hName_data_exc = 'h_%s_eff_%s_data_exc_%s'%(mname,vname,suffix)
                                        hName_MC_inc   = 'h_%s_eff_%s_MC_inc_%s'  %(mname,vname,suffix)
                                        hName_MC_exc   = 'h_%s_eff_%s_MC_exc_%s'  %(mname,vname,suffix)
                            
                                        h_data_inc = fCompare.Get(hName_data_inc)
                                        h_MC_inc   = fCompare.Get(hName_MC_inc  )
                                        h_data_exc = fCompare.Get(hName_data_exc)
                                        h_MC_exc   = fCompare.Get(hName_MC_exc  )
                                        
                                          
                                        if not h_data_inc or not h_MC_inc:
                                                fCompare.ls()
                                                print hName_data_inc
                                                print hName_MC_inc
                                                print '!!!' 
                                        labels = make_labels(args=[OSSSname,aname,'CMS',rname,cname], lumi=card.lumi)
                                
                                        suffix = '%s_%s_%s_%s_%s_%s_%s_%s'%(mname,vname,rname,cname,tname,OSSSname,aname,PUWname)
                            
                                        data_legend = 'Data' if strname=='inc' else 'Data (non DY subtracted)'
                                        MC_legend   = 'DY'   if strname=='exc' else 'DY+non-DY'
                                        hw_data_inc = histogram_wrapper(h_data_inc, 'Data'                    , styles['data_inc'])
                                        hw_MC_inc   = histogram_wrapper(h_MC_inc  , 'DY+non-DY'               , styles[  'MC_inc'])
                                        hw_data_exc = histogram_wrapper(h_data_exc, 'Data (non DY subtracted)', styles['data_exc'])
                                        hw_MC_exc   = histogram_wrapper(h_MC_exc  , 'DY'                      , styles[  'MC_exc'])
                            
                                        SF_inc = SF_object('inc', 'non-DY included'  , hw_data_inc, hw_MC_inc, strname)
                                        SF_exc = SF_object('exc', 'non-DY subtracted', hw_data_exc, hw_MC_exc, strname)
                                        compare_plot([SF_inc,SF_exc], labels, vname, suffix, card, None)

                                        if vname =='eta' and rname !='Transition':
                                            print 'plot eta'
                                            suffix_eta_barrel = 'Barrel_%s_%s_pass_%s_%s_%s'%(cname, tname, OSSSname, aname, PUWname)
                                            suffix_eta_endcap = 'Endcap_%s_%s_pass_%s_%s_%s'%(cname, tname, OSSSname, aname, PUWname)
                                            hName_data_inc_eta_barrel = 'h_%s_eff_%s_data_inc_%s'%(mname,vname,suffix_eta_barrel)
                                            hName_data_inc_eta_endcap = 'h_%s_eff_%s_data_inc_%s'%(mname,vname,suffix_eta_endcap)
                                            hName_data_exc_eta_barrel = 'h_%s_eff_%s_data_exc_%s'%(mname,vname,suffix_eta_barrel)
                                            hName_data_exc_eta_endcap = 'h_%s_eff_%s_data_exc_%s'%(mname,vname,suffix_eta_endcap)
                                            hName_MC_inc_eta_barrel   = 'h_%s_eff_%s_MC_inc_%s'  %(mname,vname,suffix_eta_barrel)
                                            hName_MC_inc_eta_endcap   = 'h_%s_eff_%s_MC_inc_%s'  %(mname,vname,suffix_eta_endcap)
                                            hName_MC_exc_eta_barrel   = 'h_%s_eff_%s_MC_exc_%s'  %(mname,vname,suffix_eta_barrel)
                                            hName_MC_exc_eta_endcap   = 'h_%s_eff_%s_MC_exc_%s'  %(mname,vname,suffix_eta_endcap)
                                       
                                            gName_data_inc_eta_barrel = 'g_%s_eff_%s_data_inc_%s'%(mname,vname,suffix_eta_barrel)
                                            gName_data_inc_eta_endcap = 'g_%s_eff_%s_data_inc_%s'%(mname,vname,suffix_eta_endcap)
                                            gName_data_exc_eta_barrel = 'g_%s_eff_%s_data_exc_%s'%(mname,vname,suffix_eta_barrel)
                                            gName_data_exc_eta_endcap = 'g_%s_eff_%s_data_exc_%s'%(mname,vname,suffix_eta_endcap)
                                            gName_MC_inc_eta_barrel   = 'g_%s_eff_%s_MC_inc_%s'  %(mname,vname,suffix_eta_barrel)
                                            gName_MC_inc_eta_endcap   = 'g_%s_eff_%s_MC_inc_%s'  %(mname,vname,suffix_eta_endcap)
                                            gName_MC_exc_eta_barrel   = 'g_%s_eff_%s_MC_exc_%s'  %(mname,vname,suffix_eta_barrel)
                                            gName_MC_exc_eta_endcap   = 'g_%s_eff_%s_MC_exc_%s'  %(mname,vname,suffix_eta_endcap)

 
                                            suffix_eta = 'Barrel+Endcap_%s_%s_pass_%s_%s_%s'%(cname, tname, OSSSname, aname, PUWname)
                                            hName_data_inc_eta = 'h_%s_eff_%s_data_inc_%s'%(mname,vname,suffix_eta)
                                            hName_data_exc_eta = 'h_%s_eff_%s_data_exc_%s'%(mname,vname,suffix_eta)
                                            hName_MC_inc_eta =   'h_%s_eff_%s_MC_inc_%s'%(mname,vname,suffix_eta)
                                            hName_MC_exc_eta =   'h_%s_eff_%s_MC_exc_%s'%(mname,vname,suffix_eta)
                                            gName_data_inc_eta = 'g_%s_eff_%s_data_inc_%s'%(mname,vname,suffix_eta)
                                            gName_data_exc_eta = 'g_%s_eff_%s_data_exc_%s'%(mname,vname,suffix_eta)
                                            gName_MC_inc_eta =   'g_%s_eff_%s_MC_inc_%s'%(mname,vname,suffix_eta)
                                            gName_MC_exc_eta =   'g_%s_eff_%s_MC_exc_%s'%(mname,vname,suffix_eta)
                                                              
                                            h_data_inc_eta_barrel = fCompare.Get(hName_data_inc_eta_barrel)
                                            h_data_inc_eta_endcap = fCompare.Get(hName_data_inc_eta_endcap)
                                            h_MC_inc_eta_barrel   = fCompare.Get(hName_MC_inc_eta_barrel  )
                                            h_MC_inc_eta_endcap   = fCompare.Get(hName_MC_inc_eta_endcap  )
                                            h_data_exc_eta_barrel = fCompare.Get(hName_data_exc_eta_barrel)
                                            h_data_exc_eta_endcap = fCompare.Get(hName_data_exc_eta_endcap)
                                            h_MC_exc_eta_barrel   = fCompare.Get(hName_MC_exc_eta_barrel  )
                                            h_MC_exc_eta_endcap   = fCompare.Get(hName_MC_exc_eta_endcap  )
                                             
                                            g_data_inc_eta_barrel = fCompare.Get(gName_data_inc_eta_barrel)
                                            g_data_inc_eta_endcap = fCompare.Get(gName_data_inc_eta_endcap)
                                            g_MC_inc_eta_barrel   = fCompare.Get(gName_MC_inc_eta_barrel  )
                                            g_MC_inc_eta_endcap   = fCompare.Get(gName_MC_inc_eta_endcap  )
                                            g_data_exc_eta_barrel = fCompare.Get(gName_data_exc_eta_barrel)
                                            g_data_exc_eta_endcap = fCompare.Get(gName_data_exc_eta_endcap)
                                            g_MC_exc_eta_barrel   = fCompare.Get(gName_MC_exc_eta_barrel  )
                                            g_MC_exc_eta_endcap   = fCompare.Get(gName_MC_exc_eta_endcap  )

 
                                            if not h_data_inc_eta_barrel or not h_MC_inc_eta_barrel:
                                                    print 'some error'
                                            if not g_data_inc_eta_barrel or not g_MC_inc_eta_barrel:
                                                    print 'some error'
                                            h_data_inc_eta = h_data_inc_eta_barrel.Clone(hName_data_inc_eta)
                                            h_data_inc_eta.Sumw2()
                                            h_data_inc_eta.Add(h_data_inc_eta_barrel,h_data_inc_eta_endcap,1,1)
                                            h_data_exc_eta = h_data_exc_eta_barrel.Clone(hName_data_exc_eta)
                                            h_data_exc_eta.Sumw2()
                                            h_data_exc_eta.Add(h_data_exc_eta_barrel,h_data_exc_eta_endcap,1,1)
                                            h_MC_inc_eta = h_MC_inc_eta_barrel.Clone(hName_MC_inc_eta)
                                            h_MC_inc_eta.Sumw2()
                                            h_MC_inc_eta.Add(h_MC_inc_eta_barrel,h_MC_inc_eta_endcap,1,1)
                                            h_MC_exc_eta = h_MC_exc_eta_barrel.Clone(hName_MC_exc_eta)
                                            h_MC_exc_eta.Sumw2()
                                            h_MC_exc_eta.Add(h_MC_exc_eta_barrel,h_MC_exc_eta_endcap,1,1)
                                           
                                            g_data_inc_eta=graph_add(g_data_inc_eta_endcap,g_data_inc_eta_barrel)
                                            g_data_exc_eta=graph_add(g_data_exc_eta_endcap,g_data_exc_eta_barrel)
                                            g_MC_inc_eta    =graph_add(g_MC_inc_eta_endcap,  g_MC_inc_eta_barrel)
                                            g_MC_exc_eta    =graph_add(g_MC_exc_eta_endcap,  g_MC_exc_eta_barrel)
                                            g_data_inc_eta.SetName(gName_data_inc_eta)
                                            g_data_exc_eta.SetName(gName_data_exc_eta)
                                            g_MC_inc_eta  .SetName(gName_MC_inc_eta)                                           
                                            g_MC_exc_eta  .SetName(gName_MC_exc_eta)
 
                                            labels = make_labels(args=[OSSSname,aname,'CMS','Barrel+Endcap',cname], lumi=card.lumi)
                                
                                            suffix = '%s_%s_Barrel+Endcap_%s_%s_%s_%s_%s'%(mname,vname,cname,tname,OSSSname,aname,PUWname)
                            
                                            data_legend = 'Data' if strname=='inc' else 'Data (non DY subtracted)'
                                            MC_legend   = 'DY'   if strname=='exc' else 'DY+non-DY'
                                            hw_data_inc_eta = histogram_wrapper(h_data_inc_eta, 'Data'                    , styles['data_inc'])
                                            hw_MC_inc_eta   = histogram_wrapper(h_MC_inc_eta  , 'DY+non-DY'               , styles[  'MC_inc'])
                                            hw_data_exc_eta = histogram_wrapper(h_data_exc_eta, 'Data (non DY subtracted)', styles['data_exc'])
                                            hw_MC_exc_eta   = histogram_wrapper(h_MC_exc_eta  , 'DY'                      , styles[  'MC_exc'])
                                            gw_data_inc_eta = histogram_wrapper(g_data_inc_eta, 'Data'                    , styles['data_inc'])
                                            gw_MC_inc_eta   = histogram_wrapper(g_MC_inc_eta  , 'DY+non-DY'               , styles[  'MC_inc'])
                                            gw_data_exc_eta = histogram_wrapper(g_data_exc_eta, 'Data (non DY subtracted)', styles['data_exc'])
                                            gw_MC_exc_eta   = histogram_wrapper(g_MC_exc_eta  , 'DY'                      , styles[  'MC_exc'])
                            

                                            SF_inc_eta = SF_object('', 'non-DY included'  , hw_data_inc_eta, hw_MC_inc_eta, strname)
                                            SF_exc_eta = SF_object('', 'non-DY subtracted', hw_data_exc_eta, hw_MC_exc_eta, strname)
                                            gr_SF_inc_eta = gr_SF_object('', 'non-DY included'  , gw_data_inc_eta, gw_MC_inc_eta, strname)
                                            gr_SF_exc_eta = gr_SF_object('', 'non-DY subtracted', gw_data_exc_eta, gw_MC_exc_eta, strname)
                            
                                            compare_plot([SF_inc_eta,SF_exc_eta], labels, vname, suffix, card, None)
                                            
                                            suffix_inc = '%s_%s_Barrel+Endcap_%s_%s_inc_%s_%s_%s'%(mname,vname,cname,tname,OSSSname,aname,PUWname)
                                            suffix_exc = '%s_%s_Barrel+Endcap_%s_%s_exc_%s_%s_%s'%(mname,vname,cname,tname,OSSSname,aname,PUWname)
                                            
                                            labels_inc = make_labels(args=['CMS',OSSSname,aname,'Barrel+Endcap',cname,'inc'], lumi=card.lumi)
                                            labels_exc = make_labels(args=['CMS',OSSSname,aname,'Barrel+Endcap',cname,'exc'], lumi=card.lumi)
                                            compare_plot([SF_inc_eta], labels_inc, vname, suffix_inc, card, fCompare_out)
                                            compare_plot([SF_exc_eta], labels_exc, vname, suffix_exc, card, fCompare_out)
                                            if do_poisson or do_asymmetric_error:
                                                gr_compare_plot([gr_SF_inc_eta], labels_inc, vname, suffix_inc, card, fCompare_out)
                                                gr_compare_plot([gr_SF_exc_eta], labels_exc, vname, suffix_exc, card, fCompare_out)
                                            
    
    if card.options['print_effs']:
        #for vname in ['phi']:
        for vname in ['Et']:
            v = variables[vname]
            for rname in card.region_names:
                for cname in card.charge_names:
                    for tname in card.tagCharge_names:
                        #for aname in ['nominal']:
                        for aname in card.altCut_names:
                            for PUWname in card.PUW_names:
                                for OSSSname in card.OSSS_names:
                                #for OSSSname in ['AS']:
                                #for OSSSname in ['OS']:
                                #for OSSSname in ['SS']:
                                    nEvents  = {}
                                    variance = {}
                                    eff_value = {}
                                    eff_error = {}
                                    eff_value_new = {}
                                    eff_error_new = {}
                        
                                    print '%4s  %10s  %2s  %2s  %20s  %2s'%(vname, rname, cname, tname, aname, OSSSname)
                                    for strname in strategyNames:
                                        nEvents [strname] = {}
                                        variance[strname] = {}
                            
                                        for HEEPname in card.HEEP_names:
                                            args = (vname, rname, cname, tname, HEEPname, OSSSname, aname, PUWname)
                                            histos = get_histos_from_args(args, strname, samples, card)
                                            h_2D_cut = histos['cut']
                                
                                           # nEvents[strname][HEEPname] = h_2D_cut.GetSumOfWeights()
                                            event=0
                                            error = 0
                                            for binX in range(1, h_2D_cut.GetNbinsX()+1):
                                                #if float(h_2D_cut.GetXaxis().GetBinLowEdge(binX)+h_2D_cut.GetXaxis().GetBinUpEdge(binX))/2 < 40:continue##for Et > 40
                                                if float(h_2D_cut.GetXaxis().GetBinLowEdge(binX)+h_2D_cut.GetXaxis().GetBinUpEdge(binX))/2 < 35:continue##for Et > 35
                                                for binY in range(1, h_2D_cut.GetNbinsY()+1):
                                                    event += h_2D_cut.GetBinContent(binX,binY)
                                                    error += math.pow(h_2D_cut.GetBinError(binX,binY),2)
                                            nEvents[strname][HEEPname]  = event
                                            variance[strname][HEEPname] = error

                                    for strname in strategyNames:
                                        eff_value[strname] = 1
                                        eff_error[strname] = 0
                                        eff_value_new[strname] = 1
                                        eff_error_new[strname] = 0
                                        if nEvents[strname]['probes'] > 0 and nEvents[strname]['pass'] > 0:
                                            N1 = nEvents[strname]['probes']
                                            N2 = nEvents[strname]['pass'  ]
                                            N3 = nEvents[strname]['fail'  ]
                                            e1 = math.sqrt(variance[strname]['probes'])/N1
                                            e2 = math.sqrt(variance[strname]['pass'  ])/N2
                                            e3 = math.sqrt(variance[strname]['fail'  ])/N3 if N3 !=0 else 0
                                            eff = N2/N1
                                            eff_1 = N2/(N2+N3)
                                            #eff = eff_value[strname]
                                            err = math.sqrt(abs((1-2*eff)*e2*e2+math.pow(eff*e1,2)/(N2*N2)))
                                            err_1 = math.sqrt((N3*N3*e2*e2*N2*N2+N2*N2*e3*e3*N3*N3)/math.pow(N2+N3,4)) 
                                            eff_value[strname] = nEvents[strname]['pass']/nEvents[strname]['probes']
                                            eff_error[strname] = err
                                            eff_value_new[strname] = eff_1
                                            eff_error_new[strname] = err_1
                                             
                                    #        print '%10s  %5.2f%% +- %5.2f%%'%(strname, 100*eff_value[strname], 100*eff_error[strname])
                        
                                            print 'new%10s  %5.2f%% +- %5.2f%%'%(strname, 100*eff_1, 100*err_1)
                        
                                    SF_value = {}
                                    SF_error = {}
                                    SF_value_new = {}
                                    SF_error_new = {}
                                    for strname in ['inc','exc']:
                                        deff = eff_value['data_%s'%strname]
                                        Meff = eff_value[  'MC_%s'%strname]
                                        derr = eff_error['data_%s'%strname]
                                        Merr = eff_error[  'MC_%s'%strname]
                                        SF_value[strname] = deff/Meff
                                        SF_error[strname] = SF_value[strname]*math.sqrt(math.pow(derr/deff,2)+math.pow(Merr/Meff,2))
                                     #   print 'SF (%3s)  %5.3f  +- %5.3f'%(strname,SF_value[strname],SF_error[strname])
                                        deff_new = eff_value_new['data_%s'%strname]
                                        Meff_new = eff_value_new[  'MC_%s'%strname]
                                        derr_new = eff_error_new['data_%s'%strname]
                                        Merr_new = eff_error_new[  'MC_%s'%strname]
                                        SF_value_new[strname] = deff_new/Meff_new
                                        SF_error_new[strname] = SF_value_new[strname]*math.sqrt(math.pow(derr_new/deff_new,2)+math.pow(Merr_new/Meff_new,2))
                                        print 'new SF (%3s)  %5.3f  +- %5.3f'%(strname,SF_value_new[strname],SF_error_new[strname])
                                    print
     
    if card.options['print_effs_eta']:
        do_symmetry=True
        for vname in ['eta']:
            v = variables[vname]
            for rname in card.region_names:
                if rname !="Barrel" and rname !="Endcap" : continue
                eta_bin=[]
                if rname == "Barrel":
                    #eta_bin=[[-1.4442,-1],[-1,-0.5],[-0.5,0],[0,0.5],[0.5,1],[1,1.4442]]
                    eta_bin=[[-1.4442,-0.5],[-0.5,0],[0,0.5],[0.5,1.4442]]
                elif rname == "Endcap":
                    eta_bin=[[-2.5,-1.566],[1.566,2.5]]
                for ieta in eta_bin:
                    eta_low=float(ieta[0])
                    eta_up =float(ieta[1])
                    for cname in card.charge_names:
                        for tname in card.tagCharge_names:
                            for aname in card.altCut_names:
                                for PUWname in card.PUW_names:
                                    for OSSSname in card.OSSS_names:
                                        nEvents  = {}
                                        variance = {}
                                        eff_value_new = {}
                                        eff_error_new = {}
                                        if do_symmetry == False:
                                            print '%4s(%.2fto%.2f)  %10s  %2s  %2s  %20s  %2s'%(vname,eta_low ,eta_up, rname, cname, tname, aname, OSSSname)
                                        else:
                                            print '%4s(abs(%.2f)toabs(%.2f))  %10s  %2s  %2s  %20s  %2s'%(vname,math.fabs(eta_low) ,math.fabs(eta_up), rname, cname, tname, aname, OSSSname)
                                        for strname in strategyNames:
                                            nEvents [strname] = {}
                                            variance[strname] = {}
                                
                                            for HEEPname in card.HEEP_names:
                                                args = (vname, rname, cname, tname, HEEPname, OSSSname, aname, PUWname)
                                                histos = get_histos_from_args(args, strname, samples, card)
                                                h_2D_cut = histos['cut']
                                                Xaxis = h_2D_cut.GetXaxis()
                                                bin_low = Xaxis.FindBin(eta_low) 
                                                bin_up  = Xaxis.FindBin(eta_up)
                                                bin_low_sym=0
                                                bin_up_sym=0
                                                if do_symmetry:
                                                    bin_up_sym = Xaxis.FindBin(-1*eta_low) 
                                                    bin_low_sym  = Xaxis.FindBin(-1*eta_up)
                                                nEvents[strname][HEEPname]=0
                                                variance[strname][HEEPname]=0
                                                for iy in range(1,h_2D_cut.GetNbinsY()+1):
                                                    for ix in range(bin_low,bin_up+1):
                                                        nEvents[strname][HEEPname]+=  h_2D_cut.GetBinContent(ix,iy)
                                                        variance[strname][HEEPname]+= math.pow(h_2D_cut.GetBinError(ix,iy),2)
                                                    if do_symmetry:
                                                        for ix in range(bin_low_sym,bin_up_sym+1):
                                                            nEvents[strname][HEEPname]+=  h_2D_cut.GetBinContent(ix,iy)
                                                            variance[strname][HEEPname]+= math.pow(h_2D_cut.GetBinError(ix,iy),2)

                                        for strname in strategyNames:
                                            eff_value_new[strname] = 1
                                            eff_error_new[strname] = 0
                                            if nEvents[strname]['probes'] > 0 and nEvents[strname]['pass'] > 0:
                                                N1 = nEvents[strname]['probes']
                                                N2 = nEvents[strname]['pass'  ]
                                                N3 = nEvents[strname]['fail'  ]
                                                e1 = math.sqrt(variance[strname]['probes'])
                                                e2 = math.sqrt(variance[strname]['pass'  ])
                                                e3 = math.sqrt(variance[strname]['fail'  ])
                                                eff_1 = N2/(N2+N3)
                                                err_1 = math.sqrt((N3*N3*e2*e2+N2*N2*e3*e3)/math.pow(N2+N3,4)) 
                                                eff_value_new[strname] = eff_1
                                                eff_error_new[strname] = err_1
                                                print 'new%10s  %5.2f%% +- %5.2f%%'%(strname, 100*eff_1, 100*err_1)
                                        SF_value_new = {}
                                        SF_error_new = {}
                                        for strname in ['inc','exc']:
                                            deff_new = eff_value_new['data_%s'%strname]
                                            Meff_new = eff_value_new[  'MC_%s'%strname]
                                            derr_new = eff_error_new['data_%s'%strname]
                                            Merr_new = eff_error_new[  'MC_%s'%strname]
                                            SF_value_new[strname] = deff_new/Meff_new
                                            SF_error_new[strname] = SF_value_new[strname]*math.sqrt(math.pow(derr_new/deff_new,2)+math.pow(Merr_new/Meff_new,2))
                                            print 'new SF (%3s)  %5.3f  +- %5.3f'%(strname,SF_value_new[strname],SF_error_new[strname])

    if card.options['kinematics']:
        kinematic_plots(card)
    
    if card.options['do_PUStudy']:
        hBase_SF_variations_PUW = ROOT.TH1F('hBase_SF_variations_PUW', '', 10, 0.5, 40.5)
        hBase_SF_variations_PUW.GetXaxis().SetNdivisions(010,False)
        hBase_SF_variations_PUW.SetMinimum(0.95)
        hBase_SF_variations_PUW.SetMaximum(1.15)
        hBase_SF_variations_PUW.GetXaxis().SetTitle('PU weight')
        hBase_SF_variations_PUW.GetXaxis().SetBinLabel( 1, '(N-1)/(N-1)')
        hBase_SF_variations_PUW.GetXaxis().SetBinLabel( 2, '(N-1)/(N)'  )
        hBase_SF_variations_PUW.GetXaxis().SetBinLabel( 3, '(N-1)/(N+1)')
        hBase_SF_variations_PUW.GetXaxis().SetBinLabel( 4,   '(N)/(N-1)')
        hBase_SF_variations_PUW.GetXaxis().SetBinLabel( 5,   '(N)/(N)'  )
        hBase_SF_variations_PUW.GetXaxis().SetBinLabel( 6,   '(N)/(N+1)')
        hBase_SF_variations_PUW.GetXaxis().SetBinLabel( 7, '(N+1)/(N-1)')
        hBase_SF_variations_PUW.GetXaxis().SetBinLabel( 8, '(N+1)/(N)'  )
        hBase_SF_variations_PUW.GetXaxis().SetBinLabel( 9, '(N+1)/(N+1)')
        hBase_SF_variations_PUW.GetXaxis().SetBinLabel(10, '1.0'        )
    
        hBase_SF_variations_var = ROOT.TH1F('hBase_SF_variations_var', '', 40, 0.5, 40.5)
        hBase_SF_variations_Et   = hBase_SF_variations_var.Clone('hBase_SF_variations_Et'  )
        hBase_SF_variations_eta  = hBase_SF_variations_var.Clone('hBase_SF_variations_eta' )
        hBase_SF_variations_phi  = hBase_SF_variations_var.Clone('hBase_SF_variations_phi' )
        hBase_SF_variations_nVtx = hBase_SF_variations_var.Clone('hBase_SF_variations_nVtx')
    
        styles[  'Et'].style_histogram(hBase_SF_variations_Et  )
        styles[ 'eta'].style_histogram(hBase_SF_variations_eta )
        styles[ 'phi'].style_histogram(hBase_SF_variations_phi )
        styles['nVtx'].style_histogram(hBase_SF_variations_nVtx)
    
        legend_variation = ROOT.TLegend(0.15, 0.85, 0.85, 0.8)
        legend_variation.SetFillColor(0)
        legend_variation.SetBorderSize(0)
        legend_variation.SetShadowColor(0)
        legend_variation.SetNColumns(4)
        legend_variation.AddEntry(hBase_SF_variations_Et  , 'E_{T}'  , 'pe')
        legend_variation.AddEntry(hBase_SF_variations_eta , '#eta'   , 'pe')
        legend_variation.AddEntry(hBase_SF_variations_phi , '#phi'   , 'pe')
        legend_variation.AddEntry(hBase_SF_variations_nVtx, 'n_{Vtx}', 'pe')
    
    
        h_SF_variations_Et   = {}
        h_SF_variations_eta  = {}
        h_SF_variations_phi  = {}
        h_SF_variations_nVtx = {}
        for strname in ['inc','exc']:
            for rname in card.region_names:
                h_SF_variations_Et  [(rname,strname)] = hBase_SF_variations_Et  .Clone('h_SF_variations_Et_%s_%s'  %(rname,strname))
                h_SF_variations_eta [(rname,strname)] = hBase_SF_variations_eta .Clone('h_SF_variations_eta_%s_%s' %(rname,strname))
                h_SF_variations_phi [(rname,strname)] = hBase_SF_variations_phi .Clone('h_SF_variations_phi_%s_%s' %(rname,strname))
                h_SF_variations_nVtx[(rname,strname)] = hBase_SF_variations_nVtx.Clone('h_SF_variations_nVtx_%s_%s'%(rname,strname))
                
                PUcounter = 1
                for PUWname in card.PUW_names:
                    SF_Et   = ScaleFactors[('cut','Et'  ,rname,'ea','ta','nominal','AS',strname,PUWname)]
                    SF_eta  = ScaleFactors[('cut','eta' ,rname,'ea','ta','nominal','AS',strname,PUWname)]
                    SF_phi  = ScaleFactors[('cut','phi' ,rname,'ea','ta','nominal','AS',strname,PUWname)]
                    SF_nVtx = ScaleFactors[('cut','nVtx',rname,'ea','ta','nominal','AS',strname,PUWname)]
            
                    bin0 = 4*PUcounter-3
                    h_SF_variations_Et  [(rname,strname)].SetBinContent(bin0+0, SF_Et  .a_value)
                    h_SF_variations_Et  [(rname,strname)].SetBinError  (bin0+0, SF_Et  .a_error)
            
                    h_SF_variations_eta [(rname,strname)].SetBinContent(bin0+1, SF_eta .a_value)
                    h_SF_variations_eta [(rname,strname)].SetBinError  (bin0+1, SF_eta .a_error)
            
                    h_SF_variations_phi [(rname,strname)].SetBinContent(bin0+2, SF_phi .a_value)
                    h_SF_variations_phi [(rname,strname)].SetBinError  (bin0+2, SF_phi .a_error)
            
                    h_SF_variations_nVtx[(rname,strname)].SetBinContent(bin0+3, SF_nVtx.a_value)
                    h_SF_variations_nVtx[(rname,strname)].SetBinError  (bin0+3, SF_nVtx.a_error)
                    
                    PUcounter += 1
    
    
        canvas_variation = ROOT.TCanvas('canvas_variation', '', 100, 100, 1000, 600)
        canvas_variation.SetGridx()
        canvas_variation.SetGridy()
        for strname in ['inc','exc']:
            for rname in card.region_names:
                canvas_variation.Clear()
                hBase_SF_variations_PUW.Draw()
                h_SF_variations_Et  [(rname,strname)].Draw('sames:pe')
                h_SF_variations_eta [(rname,strname)].Draw('sames:pe')
                h_SF_variations_phi [(rname,strname)].Draw('sames:pe')
                h_SF_variations_nVtx[(rname,strname)].Draw('sames:pe')
                legend_variation.Draw()
                hBase_SF_variations_PUW.Draw('sames:axis')
                canvas_variation.Print('%s/variations_%s_%s.eps'%(card.plot_prefix,rname,strname))
                canvas_variation.Print('%s/variations_%s_%s.png'%(card.plot_prefix,rname,strname))
    
    if False:
        for sname in samples:
            s = samples[sname]
            w = card.lumi/s.effectiveLumi
            print '%20s  %8.4f pb^-1  %10f'%(s.name , s.effectiveLumi, w)

