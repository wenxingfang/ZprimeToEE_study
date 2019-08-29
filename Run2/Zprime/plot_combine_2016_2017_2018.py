
import math
import gc
import sys
import ROOT
from array import array
from ROOT import RooFit, RooRealVar, RooGaussian, RooDataSet, RooArgList, RooTreeData, RooArgSet, RooGenericPdf, RooAbsReal
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 1;")
ROOT.TH1.AddDirectory(ROOT.kFALSE)


def comb(g1, g2, g3):
    gr_comb=g1.Clone("comb_%s"%(g1.GetName()))
    for i in range(0, g1.GetN()):
        x=g1.GetX()[i]
        y1=g1.GetY()[i]
        y2=g2.GetY()[i]
        y3=g3.GetY()[i]
        e1_L=g1.GetErrorYlow(i)
        e1_U=g1.GetErrorYhigh(i)
        e2_L=g2.GetErrorYlow(i)
        e2_U=g2.GetErrorYhigh(i)
        e3_L=g3.GetErrorYlow(i)
        e3_U=g3.GetErrorYhigh(i)
        gr_comb.SetPoint(i,x,y1+y2+y3)
        gr_comb.SetPointEYhigh(i,math.sqrt(math.pow(e1_U,2)+math.pow(e2_U,2)+math.pow(e3_U,2)))
        gr_comb.SetPointEYlow (i,math.sqrt(math.pow(e1_L,2)+math.pow(e2_L,2)+math.pow(e3_L,2)))
    return gr_comb


def remove_zero_point(graph, value):
    for i in range(graph.GetN()-1,-1,-1):
        if graph.GetY()[i]==value:graph.RemovePoint(i)


def hist_rebin(min_event, hist_in, hist_tmp, using_tmp):
    
    hist_reBin=ROOT.TH1D()
    if using_tmp == True:
        hist_reBin=ROOT.TH1D()
        hist_reBin=hist_tmp.Clone("tmp_%s"%(hist_in.GetName()))
    if using_tmp == False:
        bin_low=1
        bin_edge = array('f')
        bin_edge.append(hist_in.GetXaxis().GetBinLowEdge(1))
        for ibin in range(1, hist_in.GetNbinsX()+1):
            bin_high=ibin
            if float(hist_in.Integral(bin_low, bin_high)) >  float(min_event):
                bin_edge.append(hist_in.GetXaxis().GetBinLowEdge(bin_high)+hist_in.GetXaxis().GetBinWidth(bin_high))
                bin_low=bin_high+1
        vmax=hist_in.GetXaxis().GetBinLowEdge(hist_in.GetNbinsX())+hist_in.GetXaxis().GetBinWidth(hist_in.GetNbinsX())
        if max not in bin_edge:
            bin_edge.append(vmax)
        hist_reBin=ROOT.TH1D("tmp_%s"%(hist_in.GetName()),"",len(bin_edge)-1, bin_edge)
    hist_reBin.Sumw2()
    hist_reBin.Scale(0)
    Xaxis = hist_reBin.GetXaxis()
    for ibin in range(1, hist_in.GetNbinsX()+1):
        value=hist_in.GetXaxis().GetBinLowEdge(ibin)+0.1
        bin_value=hist_in.GetBinContent(ibin)
        bin_error=hist_in.GetBinError(ibin)
        binx = Xaxis.FindBin(value)
        hist_reBin.SetBinContent(binx, hist_reBin.GetBinContent(binx)+bin_value) 
        hist_reBin.SetBinError(binx, math.sqrt(math.pow(hist_reBin.GetBinError(binx),2)+math.pow(bin_error,2))) 
    return hist_reBin

def graph_rebin(min_event, gr_in, gr_tmp, using_tmp):

    gr_reBin= ROOT.TGraphAsymmErrors() 
    gr_x = array('f')
    gr_x_err_L = array('f')
    gr_x_err_U = array('f')
    gr_y = array('f')
    gr_y_err_L = array('f')
    gr_y_err_U = array('f')
    if using_tmp == True:
        if type(gr_tmp) == ROOT.TH1D:
            gr_reBin=ROOT.TGraphAsymmErrors(gr_tmp)
        else:
            gr_reBin=gr_tmp.Clone("tmp_%s"%(gr_in.GetName()))
    if using_tmp == False:
        gr_edge = array('f')
        gr_edge.append(gr_in.GetX()[0]-gr_in.GetErrorXlow(0))
        for ig in range(0, gr_in.GetN()):
            gr_edge.append(gr_in.GetX()[ig]+gr_in.GetErrorXhigh(ig))
        hist_in=ROOT.TH1D("h_%s"%(gr_in.GetName()),"",len(gr_edge)-1,gr_edge)
        for ig in range(0, gr_in.GetN()):
            hist_in.SetBinContent(ig+1,gr_in.GetY()[ig]) 
        bin_low=1
        bin_edge = array('f')
        bin_edge.append(hist_in.GetXaxis().GetBinLowEdge(1))
        for ibin in range(1, hist_in.GetNbinsX()+1):
            bin_high=ibin
            if float(hist_in.Integral(bin_low, bin_high)) >  float(min_event):
                bin_edge.append(hist_in.GetXaxis().GetBinLowEdge(bin_high)+hist_in.GetXaxis().GetBinWidth(bin_high))
                bin_low=bin_high+1
        vmax=hist_in.GetXaxis().GetBinLowEdge(hist_in.GetNbinsX())+hist_in.GetXaxis().GetBinWidth(hist_in.GetNbinsX())
        if vmax not in bin_edge:
            bin_edge.append(vmax)
        hist_reBin=ROOT.TH1D("tmp_%s"%(hist_in.GetName()),"",len(bin_edge)-1, bin_edge)
        hist_reBin.Scale(0)
        gr_reBin=ROOT.TGraphAsymmErrors(hist_reBin)
    for ibin in range(0, gr_in.GetN()):
        value=gr_in.GetX()[ibin]
        bin_value=gr_in.GetY()[ibin]
        bin_error_L=gr_in.GetErrorYlow(ibin)
        bin_error_U=gr_in.GetErrorYhigh(ibin)
        for re in range(0, gr_reBin.GetN()):
            if value > (gr_reBin.GetX()[re]-gr_reBin.GetErrorXlow(re)) and value < (gr_reBin.GetX()[re]+gr_reBin.GetErrorXhigh(re)):
                gr_reBin.SetPoint(re,gr_reBin.GetX()[re],gr_reBin.GetY()[re]+bin_value)
                gr_reBin.SetPointEYhigh(re,math.sqrt(math.pow(gr_reBin.GetErrorYhigh(re),2)+math.pow(bin_error_U,2)))
                gr_reBin.SetPointEYlow(re,math.sqrt(math.pow(gr_reBin.GetErrorYlow(re),2)+math.pow(bin_error_L,2)))
    return gr_reBin


def hist_event_number(m_low, m_high, hist_in):
    mass_low  = m_low
    mass_high = m_high
    event=0
    error=0
    for ibin in range(1,hist_in.GetNbinsX()+1):
        bin_mean = (hist_in.GetBinLowEdge(ibin) + hist_in.GetBinLowEdge(ibin) + hist_in.GetBinWidth(ibin))/2
        if float(bin_mean) < float(mass_high) and float(bin_mean) > float(mass_low):
            event=event+hist_in.GetBinContent(ibin)
            error=math.sqrt(math.pow(error,2)+math.pow(hist_in.GetBinError(ibin),2))

    alpha = float(1 - 0.6827)
    N=event
    L = 0
    if N==0:
        L=0
    else: 
        L= float( ROOT.Math.gamma_quantile(alpha/2,N,1.) )
    U =float( ROOT.Math.gamma_quantile_c(alpha/2,N+1,1) )
    error_low=N-L
    error_up=U-N
    if 'data' in hist_in.GetName():
        print '%s from %d to %d have event= %f, error= +%f,-%f'%(hist_in.GetName(), mass_low, mass_high, event, error_up, error_low)
        return [event,error_low,error_up]
    else:
        print '%s from %d to %d have event= %f, error= %f'%(hist_in.GetName(), mass_low, mass_high, event, error)
        return [event,error,error]
    
def histTograph(h_data):  
    h_data_bin_value={}
    h_data_bin_width={}
    for ibin in range(1, h_data.GetNbinsX()+1):
        h_data_bin_value[ibin]=h_data.GetBinContent(ibin)*h_data.GetBinWidth(ibin) 
        h_data_bin_width[ibin]=h_data.GetBinWidth(ibin) 
    g_data = ROOT.TGraphAsymmErrors(h_data)
    g_data.SetMarkerSize(0.5)
    g_data.SetMarkerStyle (20)
    alpha = float(1 - 0.6827)
    hist_weight=['h_mee_all','h_mee_all_BB','h_mee_all_BE','h_mee_all_EE','h_mee_cosp','h_mee_cosp_BB','h_mee_cosp_BE','h_mee_cosp_EE','h_mee_cosm','h_mee_cosm_BB','h_mee_cosm_BE','h_mee_cosm_EE']
    for i in range(0,g_data.GetN()): 
        N = g_data.GetY()[i]
        error_up=0
        error_low=0
        if h_data.GetName().split("data_")[-1] in hist_weight:
           # print "data name =%s"%(h_data.GetName())
            N = h_data_bin_value[i+1]
        L = 0
        if N==0:
            L=0
        else: 
            L= float( ROOT.Math.gamma_quantile(alpha/2,N,1.) )
        U =float( ROOT.Math.gamma_quantile_c(alpha/2,N+1,1) )
        error_low=N-L
        error_up=U-N
        if h_data.GetName().split("data_")[-1] in hist_weight:
            error_low= (N-L)/h_data_bin_width[i+1]
            error_up=(U-N)/h_data_bin_width[i+1]
        if N==0:
            error_up=0
            error_low=0
        g_data.SetPointEYlow (i, error_low)
        g_data.SetPointEYhigh(i, error_up)
    return g_data

def histToRatioGraph(h_data,sum_mc ):
    ratio_x = array('f')
    ratio_x_el = array('f')
    ratio_x_eh = array('f')
    ratio_y = array('f')
    ratio_y_el = array('f')
    ratio_y_eh = array('f')
    h_data_bin_value={}
    h_data_bin_width={}
    for ibin in range(1, h_data.GetNbinsX()+1):
        h_data_bin_value[ibin]=h_data.GetBinContent(ibin)*h_data.GetBinWidth(ibin) 
        h_data_bin_width[ibin]=h_data.GetBinWidth(ibin) 
    g_data = ROOT.TGraphAsymmErrors(h_data)
    g_data.SetMarkerSize(0.5)
    g_data.SetMarkerStyle (20)
    alpha = float(1 - 0.6827)
    hist_weight=['h_mee_all_data','h_mee_all_BB_data','h_mee_all_BE_data','h_mee_all_EE_data','h_mee_all_big_data','h_mee_all_BB_big_data','h_mee_all_BE_big_data','h_mee_all_EE_big_data']
    for i in range(0,g_data.GetN()): 
        N = g_data.GetY()[i]
        error_up=0
        error_low=0
        if h_data.GetName() in hist_weight:
            N = h_data_bin_value[i+1]
        L = 0
        if N==0:
            L=0
        else: 
            L= float( ROOT.Math.gamma_quantile(alpha/2,N,1.) )
        U =float( ROOT.Math.gamma_quantile_c(alpha/2,N+1,1) )
        error_low=N-L
        error_up=U-N
        if h_data.GetName() in hist_weight:
            error_low= (N-L)/h_data_bin_width[i+1]
            error_up=(U-N)/h_data_bin_width[i+1]
        if N==0:
            error_up=0
            error_low=0
        g_data.SetPointEYlow (i, error_low)
        g_data.SetPointEYhigh(i, error_up)
        ratio_x.append( float(g_data.GetX()[i]) )   
        ratio_x_el.append( float(g_data.GetErrorXlow(i)) )   
        ratio_x_eh.append( float(g_data.GetErrorXhigh(i)))   
        if float(sum_mc.GetBinContent(i+1)) != 0:
            ratio_y.append( float((g_data.GetY()[i]/sum_mc.GetBinContent(i+1))-1) )
        else:
            ratio_y.append(0)
        ratio_y_el_tmp =0
        ratio_y_eh_tmp =0
        if float(g_data.GetY()[i]) != 0 and float(sum_mc.GetBinContent(i+1)) != 0: 
            ratio_y_el_tmp = (g_data.GetY()[i]/sum_mc.GetBinContent(i+1))*math.sqrt( pow(error_low/g_data.GetY()[i],2) + pow(sum_mc.GetBinError(i+1)/sum_mc.GetBinContent(i+1),2)) 
            ratio_y_eh_tmp = (g_data.GetY()[i]/sum_mc.GetBinContent(i+1))*math.sqrt( pow(error_up/g_data.GetY()[i],2) +  pow(sum_mc.GetBinError(i+1)/sum_mc.GetBinContent(i+1),2)) 
        ratio_y_el.append(ratio_y_el_tmp )  
        ratio_y_eh.append(ratio_y_eh_tmp )  
          
    g_ratio=ROOT.TGraphAsymmErrors(len(ratio_x),ratio_x,ratio_y,ratio_x_el,ratio_x_eh,ratio_y_el,ratio_y_eh)
    return g_ratio

def Graph_Xerror0(graph_in):
    for i in range(0,graph_in.GetN()):
        graph_in.SetPointEXlow (i, 0)
        graph_in.SetPointEXhigh(i, 0)
    
def get_total_err(h_nominal, h_err_down, h_err_up): 
    g_nominal = ROOT.TGraphAsymmErrors(h_nominal)
    for ibin in range(0,g_nominal.GetN()):
        err_down=math.sqrt(math.pow(h_nominal.GetBinError(ibin+1),2)+math.pow(h_err_down.GetBinContent(ibin+1),2))
        err_up  =math.sqrt(math.pow(h_nominal.GetBinError(ibin+1),2)+math.pow(h_err_up.GetBinContent(ibin+1),2))
        g_nominal.SetPointEYlow(ibin,err_down)
        g_nominal.SetPointEYhigh(ibin,err_up)
    return g_nominal

def get_err_range(h_nominal,h_err_down,h_err_up, low, up):
    stat_err=0
    sys_err_L=0
    sys_err_U=0
    stat_sys_err_L=0
    stat_sys_err_U=0
    Xaxis=h_nominal.GetXaxis()
    bin_L=1
    bin_U=h_nominal.GetNbinsX()
    if low > h_nominal.GetBinLowEdge(1):bin_L=Xaxis.FindBin(low+0.01)
    if up  < (h_nominal.GetBinLowEdge(bin_U)+h_nominal.GetBinWidth(bin_U)):bin_U=Xaxis.FindBin(up-0.01)
    for ibin in range(bin_L,bin_U+1):
        stat_err =math.sqrt(math.pow(stat_err ,2)+math.pow(h_nominal.GetBinError(ibin),2))
        sys_err_L=math.sqrt(math.pow(sys_err_L,2)+math.pow(h_err_down.GetBinContent(ibin),2))
        sys_err_U=math.sqrt(math.pow(sys_err_U,2)+math.pow(h_err_up.GetBinContent(ibin),2))
    
    stat_sys_err_L=math.sqrt(math.pow(stat_err,2)+math.pow(sys_err_L,2))
    stat_sys_err_U=math.sqrt(math.pow(stat_err,2)+math.pow(sys_err_U,2))
    if stat_sys_err_L > stat_sys_err_U:
        return stat_sys_err_L
    else:
        return stat_sys_err_U
def get_graph_ratio(g1, g2):
    g_ratio=g1.Clone("g_ratio_%s_%s"%(g1.GetName(),g2.GetName()))
    for ibin in range(0, g_ratio.GetN()):
         ratio=999
         err_down=0
         err_up=0
         if float(g2.GetY()[ibin]) !=0:
             ratio=float((g1.GetY()[ibin]-g2.GetY()[ibin])/g2.GetY()[ibin])
             err_down=math.fabs(float(g1.GetErrorYlow(ibin)/g2.GetY()[ibin]))
             err_up  =math.fabs(float(g1.GetErrorYhigh(ibin)/g2.GetY()[ibin]))
         g_ratio.SetPoint(ibin,g_ratio.GetX()[ibin],ratio)
         g_ratio.SetPointEYlow(ibin,err_down)
         g_ratio.SetPointEYhigh(ibin,err_up)
    return g_ratio

###### (self err - self)/self##########
def get_self_err(hist):
    if type(hist) == ROOT.TH1D:
        gr=ROOT.TGraphAsymmErrors(hist)
        gr.SetName("self_err_%s"%(gr.GetName()))
        for ibin in range(0,gr.GetN()):
            if gr.GetY()[ibin] !=0:
#                if "cum" in hist.GetName():print "low err %f, high err %f"%(gr.GetErrorYlow(ibin),gr.GetErrorYhigh(ibin))
                gr.SetPointEYlow(ibin ,math.fabs(gr.GetErrorYlow(ibin)/gr.GetY()[ibin]))
                gr.SetPointEYhigh(ibin,math.fabs(gr.GetErrorYhigh(ibin)/gr.GetY()[ibin]))
            else:
                gr.SetPointEYlow(ibin ,0)
                gr.SetPointEYhigh(ibin,0)
            gr.SetPoint(ibin,gr.GetX()[ibin],0)
        return gr
    elif type(hist) == ROOT.TGraphAsymmErrors:
        gr=hist.Clone("self_err_%s"%(hist.GetName()))
        for ibin in range(0,gr.GetN()):
            if gr.GetY()[ibin] !=0:
                gr.SetPointEYlow(ibin ,math.fabs(gr.GetErrorYlow(ibin)/gr.GetY()[ibin] ))
                gr.SetPointEYhigh(ibin,math.fabs(gr.GetErrorYhigh(ibin)/gr.GetY()[ibin]))
            else:
                gr.SetPointEYlow(ibin ,0)
                gr.SetPointEYhigh(ibin,0)
            gr.SetPoint(ibin,gr.GetX()[ibin],0)
        return gr
    else:
        print "don't match"
####################################

def cumulate(hist, cum_name):
    h_cum=hist.Clone(cum_name)
    h_cum.Scale(0)
    for ibin in range(1,h_cum.GetNbinsX()+1):
        value=0
        error=0
        for jbin in range(ibin,h_cum.GetNbinsX()+1):
            value=value+hist.GetBinContent(jbin)
            error=math.sqrt(math.pow(error,2)+math.pow(hist.GetBinError(jbin),2))
        h_cum.SetBinContent(ibin,value)
        h_cum.SetBinError(ibin,error)
    return h_cum


def draw_plots(date, out_dir, h_stack,h_mc,g_mc,h_data,out_name, blind):
    if blind:
        for ibin in range(1,h_data.GetNbinsX()+1):
            if float(h_data.GetBinLowEdge(ibin) + h_data.GetBinWidth(ibin)) > 600:
                h_data.SetBinContent(ibin,0)
                h_data.SetBinError(ibin,0)
    stat_style=1001
    stat_color=ROOT.kRed-10
    stat_sys_style=1001
    #stat_sys_color=ROOT.kGray
    stat_sys_color=ROOT.TColor.GetColor("#b4ccdb")
    canvas = ROOT.TCanvas('canvas_%s'%(out_name),'',1000,1000)

    canvas.Range(1.592761, -5.173913, 3.533814, 6.006211)
    canvas.SetFillColor(0)
    canvas.SetBorderMode(0)
    canvas.SetBorderSize(2)
    canvas.SetLeftMargin(0.13)
    canvas.SetRightMargin(0.07)
    canvas.SetFrameBorderMode(0)
    canvas.SetFrameBorderMode(0)
    canvas.SetTopMargin(0.085)
    canvas.SetBottomMargin(0.11)
    canvas.cd()
    size = 0.312
    pad1 = ROOT.TPad('pad1', '', 0.0, size, 1.0, 1.0, 0)
    pad2 = ROOT.TPad('pad2', '', 0.0, 0.0, 1.0, size, 0)
    pad1.Draw()
    pad2.Draw() 
    pad1.SetTickx(1)
    pad1.SetTicky(1)
    pad2.SetTickx(1)
    pad2.SetTicky(1)
    pad2.SetGridy()
    pad1.SetBottomMargin(0.05)
    pad1.SetRightMargin(0.05)
    pad1.SetLeftMargin(0.13)
    pad2.SetTopMargin(0.05)
    pad2.SetBottomMargin(0.5)
    pad2.SetRightMargin(0.05)
    pad2.SetLeftMargin(0.13)
    pad1.cd()
    pad1.SetLogx()
    pad2.SetLogx()
    if "cumlative" in out_name and "v1" not in out_name:
        pad1.SetLogx(ROOT.kFALSE)
        pad2.SetLogx(ROOT.kFALSE)

    pad1.SetLogy()
    final_other_hist_title={'h_pv_n':'Nvtx','h_Ptll':'P_{T}(ee) [GeV]','h_Etall':'#eta(ee)','h_Phill':'#phi(ee)','h_led_Et':'E_{T}^{Leading} [GeV]','h_led_eta':'#eta^{Leading}','h_led_phi':'#phi^{Leading}','h_sub_Et':'E_{T}^{Sub-leading} [GeV]','h_sub_eta':'#eta^{Sub-leading}','h_sub_phi':'#phi^{Sub-leading}','h_MET':'MET [GeV]','h_MET_phi':'#phi^{MET}','h_MET_T1Txy':'MET(T1Txy) [GeV]','h_MET_phi_T1Txy':'#phi^{MET(T1Txy)}','h_MET_SF_T1Txy':'MET Significance','h_MET_Filter':'MET Filter','h_Dphi_ll':'#Delta#phi(e,e)','h_Dphi_MET_Z':'#Delta#phi(MET,ee)','h_DR_ll':'#DeltaR(e,e)','h_N_jet':'Number of jets','h_N_bjet':'Number of b jets','h_HT_sys':'HT^{system} [GeV]','h_Pt_sys':'P_{T}^{system} [GeV]','h_mee_Zpeak':'m(ee) [GeV]','h_mee_Zpeak_BB':'m(ee) [GeV]','h_mee_Zpeak_BE':'m(ee) [GeV]','h_mee_Zpeak_EE':'m(ee) [GeV]','h_mee_cosp':'m(ee) [GeV]','h_mee_cosp_BB':'m(ee) [GeV]','h_mee_cosp_BE':'m(ee) [GeV]','h_mee_cosp_EE':'m(ee) [GeV]','h_mee_cosm':'m(ee) [GeV]','h_mee_cosm_BB':'m(ee) [GeV]','h_mee_cosm_BE':'m(ee) [GeV]','h_mee_cosm_EE':'m(ee) [GeV]','h_cos':'cos#theta*','h_cos_BB':'cos#theta*','h_cos_BE':'cos#theta*','h_cos_EE':'cos#theta*','h_cos_all_region':'cos#theta*'}
    final_heep_var_hist_title={"h_dPhiIn":"#Delta#phi_{in}","h_Sieie":"#sigma_{i#eta i#eta}","h_missingHits":"Missing Hits","h_dxyFirstPV":"|d_{xy}|","h_HOverE":"H/E","h_E1x5OverE5x5":"E_{1x5}/E_{5x5}","h_E2x5OverE5x5":"E_{2x5}/E_{5x5}","h_isolEMHadDepth1":"EM + HD1","h_IsolPtTrks":"TrackIso","h_EcalDriven":"EcalDriven","h_dEtaIn":"#Delta#eta_{in}^{seeded}"}  
    final_other_hist_title.update(final_heep_var_hist_title)
    ########### For XY Range #############
    nbin=1
#    x_min=75
    x_min=70
    x_max=4000
    y_min=1E-5
    y_max=3E6
    if "cumlative" in out_name:
        y_max=1E8
        y_min=1E-2
    #if "mee" not in out_name or "Zpeak" in out_name: 
    if "Zpeak" in out_name: 
        nbin =h_data.GetNbinsX()
        x_min=h_data.GetBinLowEdge(1)
        x_max=h_data.GetBinLowEdge(nbin)+h_data.GetBinWidth(nbin)
        y_min=1E0
        y_max=40E5
        if "BB" in out_name:
            y_min=1E0
            y_max=32E5
        elif "BE" in out_name:
            y_min=1E0
            y_max=100E4
        elif "EE" in out_name:
            y_min=1E0
            y_max=64E4
        pad1.SetLogx(ROOT.kFALSE)
        pad2.SetLogx(ROOT.kFALSE)
        if do_Z_XS_measure==False:
            pad1.SetLogy(ROOT.kFALSE)
    if "mee" not in out_name : 
        nbin =h_data.GetNbinsX()
        x_min=h_data.GetBinLowEdge(1)
        x_max=h_data.GetBinLowEdge(nbin)+h_data.GetBinWidth(nbin)
        y_min=0
        y_max=2*h_data.GetBinContent(h_data.GetMaximumBin())
        pad1.SetLogx(ROOT.kFALSE)
        pad1.SetLogy(ROOT.kFALSE)
        pad2.SetLogx(ROOT.kFALSE)
        if 'Et' in out_name and "Eta" not in out_name:
            y_min=1E-1
            pad1.SetLogy(ROOT.kTRUE)
    if out_name in ['h_mee_fine','h_mee_BB_fine','h_mee_BE_fine','h_mee_EE_fine']:
        x_min=100
        x_max=1000
        nbin =1
        if "BB" in out_name:
            y_min=2E0
            y_max=4E4
        elif "BE" in out_name:
            y_min=1E0
            y_max=2E4
        elif "EE" in out_name:
            y_min=0
            y_max=1E4
        else :
            y_min=1E0
            y_max=4E4
        pad1.SetLogx(ROOT.kFALSE)
        pad1.SetLogy(ROOT.kFALSE)
        pad2.SetLogx(ROOT.kFALSE)
    font = 42
    dummy = ROOT.TH2D("dummy","",nbin,x_min,x_max,1,y_min,y_max)
    dummy.SetStats(ROOT.kFALSE)
    X_title='m(ee) [GeV]'
    dummy_Y_title='Events / GeV'
    if "cumlative" in out_name :
        dummy_Y_title='Events #geq m(ee)'
    if out_name in final_other_hist_title:
        dummy_Y_title= 'Events / %.1f'%(h_data.GetBinWidth(1)) if (h_data.GetBinWidth(1)%1 !=0) else 'Events / %.0f'%(h_data.GetBinWidth(1))
        if 'GeV' in final_other_hist_title[out_name]: dummy_Y_title=dummy_Y_title+" GeV" 
        X_title=final_other_hist_title[out_name]

    dummy.GetYaxis().SetTitle(dummy_Y_title)
    dummy.GetYaxis().SetTitleSize(0.05)
    dummy.GetYaxis().SetLabelSize(0.05)
    dummy.GetXaxis().SetLabelSize(0.05)
    dummy.GetYaxis().SetTitleOffset(1.25)
    dummy.GetXaxis().SetTitleOffset(1.0)
    dummy.GetXaxis().SetMoreLogLabels()
    dummy.GetXaxis().SetNoExponent()  
    dummy.GetXaxis().SetTitleFont(font)
    dummy.GetXaxis().SetLabelFont(font)
    dummy.GetYaxis().SetTitleFont(font)
    dummy.GetYaxis().SetLabelFont(font)
    dummy.Draw()
    ########### For Zprime Shape #############
    h_Zprime=ROOT.TH1D()
    h_Zprime_bgk=ROOT.TH1D()
    if Add_Zprime and out_name in ['h_mee_all','h_mee_all_BB','h_mee_all_BE']:
        h_Zprime=F_Zprime.Get(out_name)
        Z_2000_Acc_eff_all= 0.576056
        Z_2000_Acc_eff_BB = 0.455010
        Z_2000_Acc_eff_BE = 0.121045
        G_2000_Acc_eff_all= 0.589558
        G_2000_Acc_eff_BB = 0.521078
        G_2000_Acc_eff_BE = 0.068476
        ratio_Acc_eff= 1
        if "all" in out_name:
            ratio_Acc_eff=Z_2000_Acc_eff_all/G_2000_Acc_eff_all
        elif "BB" in out_name:
            ratio_Acc_eff=Z_2000_Acc_eff_BB/G_2000_Acc_eff_BB
        elif "BE" in out_name:
            ratio_Acc_eff=Z_2000_Acc_eff_BE/G_2000_Acc_eff_BE
        Sample_Lumi=49641/float(3.816e-04*2)
        Data_lumi=float(35867.06)
        tmp_scale=ratio_Acc_eff*Data_lumi/Sample_Lumi
        h_Zprime.Scale(tmp_scale)
        h_Zprime_bgk=h_mc.Clone("Zprime_bgk")
        h_Zprime_bgk.Add(h_Zprime)
        for iZ in range(1,h_Zprime.GetNbinsX()+1):
            #if h_Zprime.GetBinContent(iZ)==0:h_Zprime_bgk.SetBinContent(iZ,0)
            if h_Zprime.GetBinLowEdge(iZ)<2400 or h_Zprime.GetBinLowEdge(iZ)>3200:h_Zprime_bgk.SetBinContent(iZ,1.1e-5)##remove other region
        h_Zprime_bgk.SetLineColor(ROOT.TColor.GetColor("#008000"))
        h_Zprime_bgk.SetLineWidth(2)
        h_Zprime_bgk.Draw("sames:hist")
    ########### For bgk and data #############
    h_stack.Draw('sames:hist')
    dummy.Draw("AXISSAME")
    g_data=histTograph(h_data)
    g_data.SetLineColor(ROOT.kBlack)
    g_data.SetMarkerStyle(20)
    g_data.SetMarkerSize(0.9)
    g_data_HEP=g_data.Clone("data_HEP")
    Graph_Xerror0(g_data)
    g_mc.SetFillColor(ROOT.kRed-6)
    g_mc.SetFillStyle(3244)
#    g_data.Draw("pZ0")
    g_data_clone=g_data.Clone("%s_clone"%g_data.GetName())
    remove_zero_point(g_data_clone,0)
    g_data_clone.Draw("pZ0")
    g_tmp_data=g_data.Clone("tmp_data")
    g_tmp_data.SetMarkerSize(1.1)
    h_tmp_ZToEE=h_mc.Clone("ZToEE") 
    h_tmp_ttbar=h_mc.Clone("ttbar") 
    h_tmp_Jets =h_mc.Clone("Jets") 
    g_tmp_uncertainty =g_mc.Clone("g_tmp_uncertainty") 
    g_tmp_uncertainty.SetLineColor(ROOT.kBlack) 
    h_tmp_ZToEE.SetLineColor(ROOT.kBlack) 
    h_tmp_ttbar.SetLineColor(ROOT.kBlack) 
    h_tmp_Jets .SetLineColor(ROOT.kBlack) 
    h_tmp_ZToEE.SetFillColor(ROOT.TColor.GetColor("#99ccff")) 
    h_tmp_ttbar.SetFillColor(ROOT.TColor.GetColor("#ff6666")) 
    h_tmp_Jets .SetFillColor(ROOT.TColor.GetColor("#ffff66")) 
    legend = ROOT.TLegend(0.516741-0.03, 0.61, 0.870536-0.03, 0.88, "", "brNDC")
#    legend.AddEntry(g_tmp_data,'Data','ep')
    legend.AddEntry(g_data,'Data','ep')
    legend.AddEntry(h_tmp_ZToEE,"#gamma*/Z #rightarrow e^{#plus}e#lower[-0.4]{^{#minus}}",'f')
    legend.AddEntry(h_tmp_ttbar,'t#bar{t}, tW, WW, WZ, ZZ, #tau#tau','f')
    legend.AddEntry(h_tmp_Jets,'Jets','f')
    if Add_Zprime and out_name in ['h_mee_all','h_mee_all_BB','h_mee_all_BE']:
        legend.AddEntry(h_Zprime_bgk,"Z'_{#psi} (M = 3 TeV)",'l')
    legend.SetBorderSize(0)
    legend.SetLineColor(1)
    legend.SetLineStyle(1)
    legend.SetLineWidth(1)
    legend.SetFillColor(19)
    legend.SetFillStyle(0)
    legend.SetTextFont(font)
    legend.Draw()
    cms_x_low=0.712
    cms_x_up =0.969
    cms_y_low=0.811-0.02
    cms_y_up =0.907-0.02
    if isSupplementStyle:
        cms_x_low=0.12
        cms_x_up =0.22
        cms_y_low=0.88
        cms_y_up =0.97
    label_cms = ROOT.TPaveLabel(cms_x_low, cms_y_low, cms_x_up, cms_y_up, "CMS", "brNDC")
    label_cms.SetBorderSize(0)
    label_cms.SetFillColor(0)
    label_cms.SetFillStyle(0)
    label_cms.SetTextFont(61)
    label_cms.SetTextSize(0.44/0.75)
    label_cms.Draw()
    label_prelim = ROOT.TPaveLabel(0.69, 0.745, 0.96, 0.841, "Preliminary", "brNDC")
    label_prelim.SetBorderSize(0)
    label_prelim.SetFillColor(0)
    label_prelim.SetFillStyle(0)
    label_prelim.SetTextFont(51)
    label_prelim.SetTextSize(0.44/0.75 * 0.8)
    label_prelim.Draw()
    label_supply = ROOT.TPaveLabel(0.25, cms_y_low, 0.4, cms_y_up, "Supplementary", "brNDC")
    label_supply.SetBorderSize(0)
    label_supply.SetFillColor(0)
    label_supply.SetFillStyle(0)
    label_supply.SetTextFont(51)
    label_supply.SetTextSize(0.44/0.75 * 0.8)
    if isSupplementStyle:
        label_supply.Draw()
    label_lumi = ROOT.TPaveLabel(0.74, 0.88, 0.99, 0.96, "%.1f fb^{-1} (13 TeV)"%float(Luminosity/1000), "brNDC")
    label_lumi.SetBorderSize(0)
    label_lumi.SetFillColor(0)
    label_lumi.SetFillStyle(0)
    label_lumi.SetTextFont(font)
    label_lumi.SetTextSize(0.44)
    label_lumi.Draw()
    labels_region = ROOT.TPaveLabel(0.185268, 0.812937, 0.527902, 0.907343, "", "brNDC")
    labels_region.SetBorderSize(0)
    labels_region.SetFillColor(0)
    labels_region.SetFillStyle(0)
    labels_region.SetTextFont(font)
    labels_region.SetTextSize(0.425926 )  
    if "BB" in out_name:
        labels_region.SetLabel("Barrel-Barrel")
        if "cosm"   in out_name:labels_region.SetLabel("Barrel-Barrel (cos#theta*<0)")
        elif "cosp" in out_name:labels_region.SetLabel("Barrel-Barrel (cos#theta*>0)")
        labels_region.Draw()
    elif "BE" in out_name:
        labels_region.SetLabel("Barrel-Endcap")
        if "cosm"   in out_name:labels_region.SetLabel("Barrel-Endcap (cos#theta*<0)")
        elif "cosp" in out_name:labels_region.SetLabel("Barrel-Endcap (cos#theta*>0)")
        labels_region.Draw()
    elif "EE" in out_name:
        labels_region.SetLabel("Endcap-Endcap")
        if "cosm"   in out_name:labels_region.SetLabel("Endcap-Endcap (cos#theta*<0)")
        elif "cosp" in out_name:labels_region.SetLabel("Endcap-Endcap (cos#theta*>0)")
        labels_region.Draw()
    elif "cosm" in out_name:
        labels_region.SetLabel("cos#theta*<0")
        labels_region.Draw()
    elif "cosp" in out_name:
        labels_region.SetLabel("cos#theta*>0")
        labels_region.Draw()
    pad2.cd()
    ######################################
    fontScale = pad1.GetHNDC()/pad2.GetHNDC()
    ratio_y_min=-1
    ratio_y_max=1
    if out_name in final_other_hist_title:
        ratio_y_min=-1
        ratio_y_max= 1
    dummy_ratio = ROOT.TH2D("dummy_ratio","",nbin,x_min,x_max,1,ratio_y_min,ratio_y_max)
    dummy_ratio.SetStats(ROOT.kFALSE)
    dummy_ratio.GetYaxis().SetTitle('(Data #minus Bkg) / Bkg')
    dummy_ratio.GetXaxis().SetTitle(X_title)
    dummy_ratio.GetXaxis().SetTitleSize(0.05*fontScale)
    dummy_ratio.GetXaxis().SetLabelSize(0.05*fontScale)
#    dummy_ratio.GetXaxis().SetTitleOffset(1.1)
    dummy_ratio.GetXaxis().SetMoreLogLabels()
    dummy_ratio.GetXaxis().SetNoExponent()  
    dummy_ratio.GetYaxis().SetNdivisions(305)
    dummy_ratio.GetYaxis().SetTitleSize(0.037*fontScale)
    dummy_ratio.GetYaxis().SetLabelSize(0.05 * fontScale * 0.96)
    dummy_ratio.GetYaxis().SetTitleOffset(0.7)
    dummy_ratio.GetXaxis().SetTitleFont(font)
    dummy_ratio.GetYaxis().SetTitleFont(font)
    dummy_ratio.GetXaxis().SetLabelFont(font)
    dummy_ratio.GetYaxis().SetLabelFont(font)
    dummy_ratio.Draw()
    g_ratio=ROOT.TGraph()
    if g_data.GetN()==g_mc.GetN():
        g_ratio = get_graph_ratio(g_data, g_mc)
    Graph_Xerror0(g_ratio) 
    g_mc_stat    =get_self_err(h_mc)
    g_mc_stat_sys=get_self_err(g_mc)
    g_mc_stat_sys.SetFillColor(stat_sys_color)
    g_mc_stat_sys.SetFillStyle(stat_sys_style)
    #g_mc_stat.SetFillColor(stat_sys_color)
    #g_mc_stat.SetFillStyle(stat_sys_style)
    g_mc_stat_sys.Draw("2p")
    #g_mc_stat.Draw("2p")
    dummy_ratio.Draw("AXISSAME")
    remove_zero_point(g_ratio, -1)
    g_ratio.Draw("pZ0")
    canvas.Update()
    canvas.Print('%s/%s/%s.png'%(out_dir,date,out_name))    
#    canvas.SaveAs('%s/%s/%s.pdf'%(out_dir,date,out_name))    
#    canvas.SaveAs('%s/%s/%s.C'%(out_dir,date,out_name))    
#    canvas.SaveAs('%s/%s/%s.root'%(out_dir,date,out_name))    
    ################## HEP Data ####################
    if out_name in ["h_mee_all",'h_mee_all_BB','h_mee_all_BE'] and False:
        f_HEPData= ROOT.TFile("HEPData_Run2.root","update")
        f_HEPData.cd()
        g_data_clone=g_data_HEP.Clone("data_clone_%s"%out_name)
        g_mc_clone  =g_mc  .Clone("mc_clone_%s"%out_name)
        for i in range(0,g_data_clone.GetN()):
            if (g_data_clone.GetX()[i]<70) or (g_data_clone.GetX()[i]>4000):
                g_data_clone.SetPoint(i,g_data_clone.GetX()[i],0)
                g_data_clone.SetPointEYlow (i,0)
                g_data_clone.SetPointEYhigh(i,0)
                g_mc_clone.SetPoint(i,g_mc_clone.GetX()[i],0)
                g_mc_clone.SetPointEYlow (i,0)
                g_mc_clone.SetPointEYhigh(i,0)
        g_data_clone.Write("data_%s"%out_name,ROOT.TObject.kOverwrite) 
        g_mc_clone  .Write("mc_%s"%out_name  ,ROOT.TObject.kOverwrite) 
        f_HEPData.Close()
#    ################ Fit background ####################
    if out_name in ["h_mee_usual","h_mee_BB_usual","h_mee_BE_usual","h_mee_all","h_mee_all_BB","h_mee_all_BE","h_mee_all_EE","h_mee_cosp_BB_usual","h_mee_cosp_BE_usual","h_mee_cosm_BB_usual","h_mee_cosm_BE_usual"] and False:
        f_bgk_out= ROOT.TFile("bgk_20180306_TT_WW_check.root","UPDATE");
        f_bgk_out.cd()
        h_bgk=h_mc.Rebin(2,"bgk_%s"%(out_name))
        h_bgk.Write("",ROOT.TObject.kOverwrite) 
        f_bgk_out.Close() 
#        can_bgk = ROOT.TCanvas('can_bgk_%s'%(out_name),'',100,100,1000,1000)
#        can_bgk.cd()
#        pad_bgk1 = ROOT.TPad('pad_bgk1', '', 0.0, size, 1.0, 1.0, 0)
#        pad_bgk2 = ROOT.TPad('pad_bgk2', '', 0.0, 0.0, 1.0, size, 0)
#        pad_bgk1.Draw()
#        pad_bgk2.Draw() 
#        pad_bgk2.SetGridy()
#        pad_bgk1.SetBottomMargin(0.07)
#        pad_bgk2.SetTopMargin(0)
#        pad_bgk2.SetBottomMargin(0.35)
#        pad_bgk1.SetRightMargin(0.07)
#        pad_bgk1.SetLeftMargin(0.13)
#        pad_bgk2.SetRightMargin(0.07)
#        pad_bgk2.SetLeftMargin(0.13)
#        pad_bgk1.cd()
#        pad_bgk1.SetLogy()
#        fit_low=200
#        fit_up=4000
#        h_bgk=h_mc.Rebin(2,"h_bgk_%s"%(out_name))
#        dum_bgk = ROOT.TH2D("dummy_bgk","",1,fit_low,fit_up,1,1E-4,5E4)
#        dum_bgk.SetStats(ROOT.kFALSE)
#        dum_bgk.GetYaxis().SetTitle("Events / %.0f GeV"%(h_bgk.GetBinWidth(1)))
#        dum_bgk.GetYaxis().SetTitleSize(0.05)
#        dum_bgk.GetYaxis().SetLabelSize(0.045)
#        dum_bgk.GetYaxis().SetTitleOffset(1.3)
#        dum_bgk.GetXaxis().SetLabelSize(0.045)
#        dum_bgk.GetXaxis().SetMoreLogLabels()
#        dum_bgk.GetXaxis().SetNoExponent()  
#        dum_bgk.Draw()
#        h_bgk.Draw('sames:pe')
#        dum_bgk.Draw("AXISSAME")
##        ROOT.gStyle.SetOptFit(111)
#        f_fit = ROOT.TF1('fit_%s'%(out_name), '[0]*exp([1]*x+[2]*x*x+[3]*x*x*x)*pow(x,[4])')
#        f_fit.SetParameters(35,-2E-3,3E-7,-3E-11,-5);
#        h_bgk.Fit(f_fit,"","",fit_low,fit_up)
#        ROOT.gStyle.SetOptFit(ROOT.kFALSE)
#        fit_bkg_label = ROOT.TLatex()
#        fit_bkg_label.SetTextAlign(12)
#        fit_bkg_label.SetTextSize(0.04)
#        fit_bkg_label.SetNDC(ROOT.kTRUE)
#        y_space=0.05
#        fit_bkg_label.DrawLatex(0.5,0.88, '#chi^{2}/ndof      %.2f / %d'%(f_fit.GetChisquare(),f_fit.GetNDF()))
#        fit_bkg_label.DrawLatex(0.5,0.88-y_space,'Prob        %f '%(f_fit.GetProb()))
#        fit_bkg_label.DrawLatex(0.5,0.88-2*y_space,'p0        %f #pm %f'%(f_fit.GetParameter(0),f_fit.GetParError(0)))
#        fit_bkg_label.DrawLatex(0.5,0.88-3*y_space,'p1        %f #pm %f'%(f_fit.GetParameter(1),f_fit.GetParError(1)))
#        fit_bkg_label.DrawLatex(0.5,0.88-4*y_space,'p2        %e #pm %e'%(f_fit.GetParameter(2),f_fit.GetParError(2)))
#        fit_bkg_label.DrawLatex(0.5,0.88-5*y_space,'p3        %e #pm %e'%(f_fit.GetParameter(3),f_fit.GetParError(3)))
#        fit_bkg_label.DrawLatex(0.5,0.88-6*y_space,'p4        %f #pm %f'%(f_fit.GetParameter(4),f_fit.GetParError(4)))
################## Ratio ##########################
#        pad_bgk2.cd()
#        dum_bgk_ratio = ROOT.TH2D("dummy_bgk_ratio","",1,fit_low,fit_up,1,0.5,1.5)
#        dum_bgk_ratio.SetStats(ROOT.kFALSE)
#        dum_bgk_ratio.GetYaxis().SetTitle("bgk / fit")
#        dum_bgk_ratio.GetXaxis().SetTitle("m(ee) [GeV]")
#        dum_bgk_ratio.GetXaxis().SetTitleSize(0.14)
#        dum_bgk_ratio.GetXaxis().SetTitleOffset(1.1)
#        dum_bgk_ratio.GetXaxis().SetLabelSize(0.13)
#        dum_bgk_ratio.GetXaxis().SetMoreLogLabels()
#        dum_bgk_ratio.GetXaxis().SetNoExponent()  
#        dum_bgk_ratio.GetYaxis().SetNdivisions(405)
#        dum_bgk_ratio.GetYaxis().SetTitleSize(0.14)
#        dum_bgk_ratio.GetYaxis().SetLabelSize(0.13)
#        dum_bgk_ratio.GetYaxis().SetTitleOffset(0.38)
#        dum_bgk_ratio.Draw()
#        fit_ratio=h_bgk.Clone("ratio_%s"%(h_bgk.GetName()))
#        for ibin in range(1,fit_ratio.GetNbinsX()+1):
#            x_mean=fit_ratio.GetBinLowEdge(ibin)+(fit_ratio.GetBinWidth(ibin)/2)
#            fit_ratio.SetBinContent(ibin,h_bgk.GetBinContent(ibin)/f_fit.Eval(x_mean))
#            fit_ratio.SetBinError(ibin,h_bgk.GetBinError(ibin)/f_fit.Eval(x_mean))
#        fit_ratio.Draw("sames:pe")
#        dum_bgk.Draw("AXISSAME")
#        fline = ROOT.TF1('fline_%s'%(out_name), '[0]')
#        fline.SetParameters(0,1)
#        fline.SetLineColor(ROOT.kBlue)
#        fline.SetLineWidth(2)
#        fit_ratio.Fit(fline,"","",fit_low,fit_up)
#        fit_ratio_label = ROOT.TLatex()
#        fit_ratio_label.SetTextAlign(12)
#        fit_ratio_label.SetTextSize(0.07)
#        fit_ratio_label.SetNDC(ROOT.kTRUE)
#        fit_ratio_label.DrawLatex(0.15,0.6, '#chi^{2}/ndof                %.2f / %d'%(fline.GetChisquare(),fline.GetNDF()))
#        fit_ratio_label.DrawLatex(0.15,0.5 ,'Prob                        %.3f '%(fline.GetProb()))
#        fit_ratio_label.DrawLatex(0.15,0.4 ,'p0                          %.3f #pm %.3f'%(fline.GetParameter(0),fline.GetParError(0)))
#        can_bgk.Print('%s/%s/%s_bgk.png'%(out_dir,date,out_name))    
#        del can_bgk
#        fit_bgk(h_mc, out_name, out_dir)
######################## From final style mass plot ####################################
    final_out_name={'h_mee_all':'massHist','h_mee_all_BB':'massHistEBEB','h_mee_all_BE':'massHistEBEE','h_mee_all_EE':'massHistEEEE','h_mee_all_cumlative':'cMassHist','h_mee_all_cumlative_BB':'cMassHistEBEB','h_mee_all_cumlative_BE':'cMassHistEBEE','h_mee_all_cumlative_EE':'cMassHistEEEE','h_mee_all_sin':'SignalRegionHist','h_mee_all_BB_sin':'SignalRegionHistEBEB','h_mee_all_BE_sin':'SignalRegionHistEBEE','h_mee_all_EE_sin':'SignalRegionHistEEEE'}
    if out_name in final_out_name and "sin" not in out_name and False:
        canvas_mass = ROOT.TCanvas('canvas_mass_%s'%(out_name),'',900, 600)
        canvas_mass.cd()
        ROOT.gStyle.SetOptFit(1111)
        ROOT.gStyle.SetOptStat(0)
        ROOT.gStyle.SetStatX(0.457589)
        ROOT.gStyle.SetStatY(0.312937)
        ROOT.gStyle.SetStatW(0.29241/2+0.0185)
        ROOT.gStyle.SetStatH(0.169580+0.05)
        ROOT.gStyle.SetStatFontSize(0.0402098)
        ROOT.gStyle.SetStatFont(font)
        ROOT.gStyle.SetFitFormat("5.2g")
        ROOT.gStyle.SetStatBorderSize(0)
        ROOT.gStyle.SetStatFontSize(0.040209)
        ROOT.gStyle.SetStatFontSize(0.035209)
        canvas_mass.Range(1.592761, -5.173913, 3.533814, 6.006211)
        canvas_mass.SetFillColor(0)
        canvas_mass.SetBorderMode(0)
        canvas_mass.SetBorderSize(2)
        canvas_mass.SetTickx(1)
        canvas_mass.SetTicky(1)
        canvas_mass.SetLeftMargin(0.13)
        canvas_mass.SetRightMargin(0.07)
        canvas_mass.SetFrameBorderMode(0)
        canvas_mass.SetFrameBorderMode(0)
        canvas_mass.SetTopMargin(0.085)
        canvas_mass.SetBottomMargin(0.11)
        canvas_mass.SetLogy()
        canvas_mass.SetLogx()
        if "cum" in out_name:canvas_mass.SetLogx(ROOT.kFALSE)
        dum = ROOT.TH2D("dum","",1,x_min,x_max,1,y_min,y_max)
        dum.SetStats(ROOT.kFALSE)
        dum.GetXaxis().SetMoreLogLabels()
        dum.GetXaxis().SetNoExponent()  
        dum.GetXaxis().SetLabelSize(0.05) 
        dum.GetYaxis().SetLabelSize(0.05)
        dum.GetXaxis().SetTitleSize(0.05)
        dum.GetXaxis().SetTitleOffset(1.0)
        dum.GetXaxis().SetTitle('m(ee) [GeV]')
        dum.GetYaxis().SetTitle('Events / GeV')
        dum.GetYaxis().SetTitleSize(0.05)
        dum.GetYaxis().SetTitleOffset(1)
        dum.GetYaxis().SetTitleFont(font)
        dum.GetYaxis().SetLabelFont(font)
        dum.GetXaxis().SetTitleFont(font)
        dum.GetXaxis().SetLabelFont(font)
        dum.Draw()
        h_stack.Draw('sames:hist')
        dum.Draw("AXISSAME")
        #h_mc.Draw('sames:hist')
        g_data.Draw("PZ0") 
        leg_mass = ROOT.TLegend(0.516741, 0.61, 0.870536, 0.88, "", "brNDC")
        leg_mass.AddEntry(g_data,'Data','ep')
        leg_mass.AddEntry(h_tmp_ZToEE,"#gamma*/Z #rightarrow e^{+} e^{-}",'f')
        leg_mass.AddEntry(h_tmp_ttbar,'t#bar{t}, tW, WW, WZ, ZZ, #tau#tau','f')
        leg_mass.AddEntry(h_tmp_Jets,'Jets','f')
        leg_mass.SetBorderSize(0)
        leg_mass.SetLineColor(1)
        leg_mass.SetLineStyle(1)
        leg_mass.SetLineWidth(1)
        leg_mass.SetFillColor(19)
        leg_mass.SetFillStyle(0)
        leg_mass.SetTextFont(font)
        leg_mass.Draw()
        label_cms.Draw()
        if isSupplementStyle:
            label_supply.Draw()
        else:
            label_prelim.Draw()
        label_lumi.Draw()
        labels_region.Draw()
        saved_name=final_out_name[out_name]
        canvas_mass.Print('%s/%s/%s.png'%(out_dir,date,saved_name)) 
        canvas_mass.Print('%s/%s/%s.pdf'%(out_dir,date,saved_name)) 
        del canvas_mass 
########### For sin ratio plots ################################
    if out_name in final_out_name and 'sin' in out_name and True : 
        canvas_ratio = ROOT.TCanvas('canvas_ratio_%s'%(out_name),'',900,600)
        canvas_ratio.cd()
        canvas_ratio.SetLeftMargin(0.13)
        canvas_ratio.SetRightMargin(0.06)
        canvas_ratio.SetFrameBorderMode(0)
        canvas_ratio.SetFrameBorderMode(0)
        canvas_ratio.SetTopMargin(0.1)
        canvas_ratio.SetBottomMargin(0.11)
   #     hist_event_number(500, 800, sum_mc_clone)
   #     hist_event_number(500, 800, h_data)
   #     h_mc_out_stat      = hist_rebin(10 , h_mc  , h_mc          , False)
   #     g_mc_out_stat_sys  = graph_rebin(10, g_mc  , h_mc_out_stat , True)
   #     h_data_out         = hist_rebin(10, h_data , h_mc_out_stat , True)
        h_mc_out_stat     = h_mc.Clone("h_mc_"+out_name)
        g_mc_out_stat_sys = g_mc.Clone("g_mc_"+out_name)
   #     g_data_out        = g_data.Clone("g_data_"+out_name)
        h_data_rebin=ROOT.TH1D()
        if out_name in ["h_mee_all_sin"]:
            h_data_rebin= hist_rebin(10, h_data      , h_mc, True)
        elif out_name in ["h_mee_all_BB_sin"]:
            h_data_rebin= hist_rebin(10, h_data      , h_mc, True)
        elif out_name in ["h_mee_all_BE_sin"]:
            h_data_rebin= hist_rebin(10, h_data      , h_mc, True)
        elif out_name in ["h_mee_all_EE_sin"]:
            h_data_rebin= hist_rebin(10, h_data      , h_mc, True)
        else: print "wrong name?"
        g_data_out         =histTograph(h_data_rebin)
   #     Graph_Xerror0(g_data_out)
        g_mc_out_stat= ROOT.TGraphAsymmErrors(h_mc_out_stat)
        sin_ratio = get_graph_ratio(g_data_out, g_mc_out_stat)
        sin_ratio.SetMarkerStyle(8)
        sin_ratio.SetMarkerSize(0.7)
   #     Graph_Xerror0(sin_ratio) 
        sin_mc_stat    =get_self_err(h_mc_out_stat)
        sin_mc_stat_sys=get_self_err(g_mc_out_stat_sys)
        sin_mc_stat_sys.SetFillColor(stat_sys_color)
        sin_mc_stat_sys.SetFillStyle(stat_sys_style)
        sin_mc_stat.SetFillColor(stat_color)
        sin_mc_stat.SetFillStyle(stat_style)
        x_low=h_mc_out_stat.GetBinLowEdge(1)
        last_bin_low=h_mc_out_stat.GetBinLowEdge(h_mc_out_stat.GetNbinsX())
        last_bin_high=last_bin_low + h_mc_out_stat.GetBinWidth(h_mc_out_stat.GetNbinsX())
        last_bin_value=sin_ratio.GetY()[sin_ratio.GetN()-1]
        last_bin_error_high=sin_ratio.GetErrorYhigh(sin_ratio.GetN()-1)
        last_bin_error_low=sin_ratio.GetErrorYlow(sin_ratio.GetN()-1)
        x_high=last_bin_low
        print "x_high=%f"%(x_high)
        sin_dummy=ROOT.TH2D("dum","",1,x_low,x_high,1,-1,1) 
        sin_dummy.SetStats(ROOT.kFALSE)
        sin_dummy.GetYaxis().SetTitle('(data-bkg)/bkg')
        sin_dummy.GetXaxis().SetTitle("m(ee) [GeV]")
        sin_dummy.SetMarkerStyle(8)
        sin_dummy.SetMarkerSize(0.7)
        sin_dummy.GetXaxis().SetTitleSize(0.05)
        sin_dummy.GetXaxis().SetTitleOffset(1)
        sin_dummy.GetXaxis().SetLabelSize(0.045)
        sin_dummy.GetXaxis().SetMoreLogLabels()
        sin_dummy.GetYaxis().SetNdivisions(10,4,0,ROOT.kFALSE)
        sin_dummy.GetYaxis().SetTitleSize(0.05)
        sin_dummy.GetYaxis().SetLabelSize(0.045)
        sin_dummy.GetYaxis().SetTitleOffset(0.95)
        sin_dummy.Draw()
        sin_mc_stat_sys.Draw("2p")
#        sin_mc_stat.Draw("2p")
        sin_dummy.Draw("AXISSAME")
        sin_ratio.Draw("PZ0")
        fConstant = ROOT.TF1('fConstant_%s'%(out_name), '[0]')
        fConstant.SetParameters(0,0)
        fConstant.SetLineColor(ROOT.kBlue)
        fConstant.SetLineWidth(2)
        sin_ratio.Fit(fConstant,"","",x_low,x_high)
        a_value = fConstant.GetParameter(0)
        a_error = fConstant.GetParError (0)
        fit_label        = ROOT.TLatex()
        fit_label.SetTextAlign(12)
        fit_label.SetTextSize(0.04)
        fit_label.SetNDC(ROOT.kTRUE)
        ROOT.gStyle.SetOptFit(ROOT.kFALSE)
        fit_label.DrawLatex(0.18,0.3, '#chi^{2}/ndof                       %.2f / %d'%(fConstant.GetChisquare(),fConstant.GetNDF()))
        fit_label.DrawLatex(0.18,0.25,'p0                          %.3f #pm %.3f'%(a_value,a_error))
        fit_label.DrawLatex(0.18,0.2, 'last bin ( %d - %d): %.2f^{+%.2f}_{-%.2f}'%(last_bin_low, last_bin_high, last_bin_value, last_bin_error_high, last_bin_error_low))
        labels_sin = ROOT.TLatex(0.45 , 0.85, '#bf{signal region}')
        labels_sin.SetTextAlign(32)
        labels_sin.SetTextSize(0.035)
        labels_sin.SetNDC(ROOT.kTRUE)
        labels_sin.SetX(0.87)
        labels_sin.SetY(0.85)
      #  labels_sin.Draw()
        label_cms.Draw()
        label_supply_1 = ROOT.TPaveLabel(0.22, cms_y_low, 0.37, cms_y_up, "Supplementary", "brNDC")
        label_supply_1.SetBorderSize(0)
        label_supply_1.SetFillColor(0)
        label_supply_1.SetFillStyle(0)
        label_supply_1.SetTextFont(51)
        label_supply_1.SetTextSize(0.44/0.75 * 0.8)
        if isSupplementStyle:
            label_supply_1.Draw()
        else:
            label_prelim.Draw()
        label_lumi.Draw()
        labels_region.Draw()
        saved_name=final_out_name[out_name]
        canvas_ratio.Print('%s/%s/%s.png'%(out_dir,date,saved_name))    
        canvas_ratio.Print('%s/%s/%s.pdf'%(out_dir,date,saved_name))    
        sin_ratio.Delete()
        del sin_ratio
        del canvas_ratio
    del canvas
    del final_other_hist_title
    del final_out_name
    gc.collect()
############################ Main ######################

date='20190627'
dir_out = './combine_plots'
Luminosity=float(35922.0)+float(41500.0)+float(59401.0)

isSupplementStyle=False
do_Z_XS_measure=False
Add_Zprime=False
if Add_Zprime:
    F_Zprime=ROOT.TFile("ntuples/sys_saved_hist/1013_Extend/hist_RSG_3000.root","read")

Input_2016="/user/wenxing/ST_TW_channel/CMSSW_10_2_13/src/Zprime/Result_2016.root"
Input_2017="/user/wenxing/ST_TW_channel/CMSSW_10_2_13/src/Zprime/Result_2017.root"
Input_2018="/user/wenxing/ST_TW_channel/CMSSW_10_2_13/src/Zprime/Result_2018.root"
F_2016=ROOT.TFile(Input_2016,"READ")
F_2017=ROOT.TFile(Input_2017,"READ")
F_2018=ROOT.TFile(Input_2018,"READ")
H_2016_list=[]
H_2017_list=[]
H_2018_list=[]
for ih in range(0,F_2016.GetListOfKeys().GetSize()):
    hname=F_2016.GetListOfKeys()[ih].GetName()
    if "Data_" in hname:
        tmp=hname.split("Data_")[-1]
        H_2016_list.append(tmp)
for ih in range(0,F_2017.GetListOfKeys().GetSize()):
    hname=F_2017.GetListOfKeys()[ih].GetName()
    if "Data_" in hname:
        tmp=hname.split("Data_")[-1]
        H_2017_list.append(tmp)
for ih in range(0,F_2018.GetListOfKeys().GetSize()):
    hname=F_2018.GetListOfKeys()[ih].GetName()
    if "Data_" in hname:
        tmp=hname.split("Data_")[-1]
        H_2018_list.append(tmp)
print H_2016_list
for hname in H_2016_list:
    if hname not in H_2017_list or hname not in H_2018_list:continue
    h_data_2016          =F_2016.Get("Data_%s"%hname)
    h_mc_2016            =F_2016.Get("MC_all_%s"%hname)
    g_mc_2016            =F_2016.Get("Sys_all_%s"%hname)
    h_ZToEE_2016         =F_2016.Get("ZToEE_%s"%hname)
    h_ttbar_other_2016   =F_2016.Get("ttbar_%s"%hname)
    h_Jets_2016          =F_2016.Get("jets_%s"%hname)##be careful for stat error
    h_data_2017          =F_2017.Get("Data_%s"%hname)
    h_mc_2017            =F_2017.Get("MC_all_%s"%hname)
    g_mc_2017            =F_2017.Get("Sys_all_%s"%hname)
    h_ZToEE_2017         =F_2017.Get("ZToEE_%s"%hname)
    h_ttbar_other_2017   =F_2017.Get("ttbar_%s"%hname)
    h_Jets_2017          =F_2017.Get("jets_%s"%hname)##be careful for stat error
    h_data_2018          =F_2018.Get("Data_%s"%hname)
    h_mc_2018            =F_2018.Get("MC_all_%s"%hname)
    g_mc_2018            =F_2018.Get("Sys_all_%s"%hname)
    h_ZToEE_2018         =F_2018.Get("ZToEE_%s"%hname)
    h_ttbar_other_2018   =F_2018.Get("ttbar_%s"%hname)
    h_Jets_2018          =F_2018.Get("jets_%s"%hname)##be careful for stat error
    '''
    if hname in ["h_mee_all_sin","h_mee_all_BB_sin","h_mee_all_BE_sin","h_mee_all_EE_sin"]:
            h_mc_2          = hist_rebin(10, h_mc_2          , h_mc, True)
            h_ZToEE_2       = hist_rebin(10, h_ZToEE_2       , h_mc, True)
            h_ttbar_other_2 = hist_rebin(10, h_ttbar_other_2 , h_mc, True)
            h_Jets_2        = hist_rebin(10, h_Jets_2        , h_mc, True)
    '''
    h_data_2016         .Add(h_data_2017) 
    h_data_2016         .Add(h_data_2018) 
    h_mc_2016           .Add(h_mc_2017) 
    h_mc_2016           .Add(h_mc_2018) 
    h_ZToEE_2016        .Add(h_ZToEE_2017) 
    h_ZToEE_2016        .Add(h_ZToEE_2018) 
    h_ttbar_other_2016  .Add(h_ttbar_other_2017) 
    h_ttbar_other_2016  .Add(h_ttbar_other_2018) 
    h_Jets_2016         .Add(h_Jets_2017) 
    h_Jets_2016         .Add(h_Jets_2018) 
    ###########################################
    stack_mc  = ROOT.THStack()
    h_Jets_2016.SetFillColor(ROOT.TColor.GetColor("#ffff66")) ##official color
    h_Jets_2016.SetLineColor(ROOT.kBlack)
    stack_mc.Add(h_Jets_2016)
    h_ttbar_other_2016.SetFillColor(ROOT.TColor.GetColor("#ff6666"))##official color
    h_ttbar_other_2016.SetLineColor(ROOT.kBlack)
    h_ZToEE_2016.SetFillColor(ROOT.TColor.GetColor("#99ccff"))##official color
    h_ZToEE_2016.SetLineColor(ROOT.kBlack)
    stack_mc.Add(h_ttbar_other_2016)
    stack_mc.Add(h_ZToEE_2016)
    h_data_2016.SetStats(0)
    h_mc_2016.SetStats(0)
    h_mc_2016.SetLineColor(ROOT.kBlack)
    g_mc=comb(g_mc_2016, g_mc_2017, g_mc_2018) 
    draw_plots(date, dir_out, stack_mc,h_mc_2016,g_mc,h_data_2016,hname, False)##the g_mc is not correct for now
    print "%s done"%hname
print "done"
