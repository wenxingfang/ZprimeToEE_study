import math
import gc
import sys
import ROOT
from array import array
from ROOT import RooFit, RooRealVar, RooGaussian, RooDataSet, RooArgList, RooTreeData, RooArgSet, RooGenericPdf, RooAbsReal
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 1;")
ROOT.TH1.AddDirectory(ROOT.kFALSE)

def remove_zero_point(graph, value):
    for i in range(graph.GetN()-1,-1,-1):
        if graph.GetY()[i]==value:graph.RemovePoint(i)



def fit_bgk(h_bgk, out_name, out_dir):
    x=ROOT.RooRealVar("x","x",120,4000)
    a=ROOT.RooRealVar("a","a",30,0,100)
    b=ROOT.RooRealVar("b","b",-1E-3,-1,1)
    c=ROOT.RooRealVar("c","c",1E-7,-1,1)
    d=ROOT.RooRealVar("d","d",1E-11,-1,1)
    e=ROOT.RooRealVar("e","e",1,-10,10)
#    fplo4=ROOT.RooAbsReal()
#        f_fit = ROOT.TF1('fit_%s'%(out_name), '[0]*exp([1]*x+[2]*x*x+[3]*x*x*x)*pow(x,[4])')
    fplo4=ROOT.RooGenericPdf("fplo4","","a*exp(b*x+c*x*x+d*x*x*x)*pow(x,e)",RooArgSet(x,a,b,c,d,e))
    dh=ROOT.RooDataHist("dh","dh",RooArgList(x), h_bgk)
    frame = x.frame(RooFit.Name(""),RooFit.Title(" "))
    frame.SetMaximum(1.5*h_bgk.GetMaximum())
    frame.SetMinimum(1E-4)
    dh.plotOn(frame) 
    fplo4.fitTo(dh)
    fplo4.plotOn(frame,RooFit.LineStyle(1),RooFit.LineColor(ROOT.kBlue))
    res=fplo4.fitTo(dh,RooFit.Save())
    p_a      =res.floatParsFinal().find("a").getVal()
    p_a_error=res.floatParsFinal().find("a").getError()
    p_b      =res.floatParsFinal().find("b").getVal()
    p_b_error=res.floatParsFinal().find("b").getError()
    p_c      =res.floatParsFinal().find("c").getVal()
    p_c_error=res.floatParsFinal().find("c").getError()
    p_d      =res.floatParsFinal().find("d").getVal()
    p_d_error=res.floatParsFinal().find("d").getError()
    p_e      =res.floatParsFinal().find("e").getVal()
    p_e_error=res.floatParsFinal().find("e").getError()
    can = ROOT.TCanvas("fit","fit",800,800) #X length, Y length
    can.cd()
    psize = 0.25
    pad1 = ROOT.TPad('ppad1', '', 0.0, psize, 1.0, 1.0, 0)
    pad2 = ROOT.TPad('ppad2', '', 0.0, 0.0, 1.0, psize, 0)
    pad1.Draw()
    pad2.Draw() 
    pad2.SetGridy()
    pad1.SetBottomMargin(0.07)
    pad2.SetTopMargin(0)
    pad2.SetBottomMargin(0.35)
    pad1.SetRightMargin(0.07)
    pad1.SetLeftMargin(0.13)
    pad2.SetRightMargin(0.07)
    pad2.SetLeftMargin(0.13)
    pad1.cd()
    pad1.SetLogy()
    frame.SetYTitle("Events / %.0f GeV"%(h_bgk.GetBinWidth(1))) # change y title
    frame.SetTitleOffset(1.5,"Y")#
    frame.SetLabelSize(0.025,"Y")#
    #frame.SetLabelOffset(0.03,"Y")#
    #frame.SetLabelOffset(0.03,"X")#
#    frame.SetXTitle("(E_{TMVA} - E_{reco})/ E_{reco}") # change x title
    frame.SetTitleOffset(1.2,"X")#
    frame.Draw() 
    pad2.cd()
    can.SaveAs(str(out_dir+'/'+data+'/'+out_name+'_bgkFit.png'))
    del can

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
    final_other_hist_title={'h_pv_n':'Nvtx','h_Ptll':'P_{T}(ee) [GeV]','h_Etall':'#eta(ee)','h_Phill':'#phi(ee)','h_led_Et':'E_{T}^{Leading} [GeV]','h_led_eta':'#eta^{Leading}','h_led_phi':'#phi^{Leading}',"h_led_Et_AM":'E_{T}^{Leading} [GeV]',"h_led_eta_AM":'#eta^{Leading}',"h_led_phi_AM":'#phi^{Leading}',"h_sub_Et_AM":'E_{T}^{Sub-leading} [GeV]',"h_sub_eta_AM":'#eta^{Sub-leading}',"h_sub_phi_AM":'#phi^{Sub-leading}','h_sub_Et':'E_{T}^{Sub-leading} [GeV]','h_sub_eta':'#eta^{Sub-leading}','h_sub_phi':'#phi^{Sub-leading}','h_MET':'MET [GeV]','h_MET_phi':'#phi^{MET}','h_MET_T1Txy':'MET(T1Txy) [GeV]','h_MET_phi_T1Txy':'#phi^{MET(T1Txy)}','h_MET_SF_T1Txy':'MET Significance','h_MET_Filter':'MET Filter','h_Dphi_ll':'#Delta#phi(e,e)','h_Dphi_MET_Z':'#Delta#phi(MET,ee)','h_DR_ll':'#DeltaR(e,e)','h_N_jet':'Number of jets','h_N_bjet':'Number of b jets','h_HT_sys':'HT^{system} [GeV]','h_Pt_sys':'P_{T}^{system} [GeV]','h_mee_Zpeak':'m(ee) [GeV]','h_mee_Zpeak_BB':'m(ee) [GeV]','h_mee_Zpeak_BE':'m(ee) [GeV]','h_mee_Zpeak_EE':'m(ee) [GeV]','h_mee_cosp':'m(ee) [GeV]','h_mee_cosp_BB':'m(ee) [GeV]','h_mee_cosp_BE':'m(ee) [GeV]','h_mee_cosp_EE':'m(ee) [GeV]','h_mee_cosm':'m(ee) [GeV]','h_mee_cosm_BB':'m(ee) [GeV]','h_mee_cosm_BE':'m(ee) [GeV]','h_mee_cosm_EE':'m(ee) [GeV]','h_cos':'cos#theta*','h_cos_BB':'cos#theta*','h_cos_BE':'cos#theta*','h_cos_EE':'cos#theta*','h_cos_all_region':'cos#theta*'}
    final_heep_var_hist_title={"h_dPhiIn":"#Delta#phi_{in}","h_Sieie":"#sigma_{i#eta i#eta}","h_missingHits":"Missing Hits","h_dxyFirstPV":"|d_{xy}|","h_HOverE":"H/E","h_E1x5OverE5x5":"E_{1x5}/E_{5x5}","h_E2x5OverE5x5":"E_{2x5}/E_{5x5}","h_isolEMHadDepth1":"EM + HD1","h_IsolPtTrks":"TrackIso","h_EcalDriven":"EcalDriven","h_dEtaIn":"#Delta#eta_{in}^{seeded}"}  
    final_rho_hist_title={'h_rho':'#rho','h_rho_BB':'#rho','h_rho_BE':'#rho','h_rho_EE':'#rho'}
    final_other_hist_title.update(final_heep_var_hist_title)
    final_other_hist_title.update(final_rho_hist_title)
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
        #y_max=25E5
        y_max=2*h_data.GetBinContent(h_data.GetMaximumBin())
        #if "BB" in out_name:
        #    y_min=1E0
        #    y_max=20E5
        #elif "BE" in out_name:
        #    y_min=1E0
        #    y_max=80E4
        #elif "EE" in out_name:
        #    y_min=1E0
        #    y_max=60E4
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
    #label_lumi = ROOT.TPaveLabel(0.71, 0.88, 0.992, 0.97, "35.9 fb^{-1} (13 TeV)", "brNDC")
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
        #ratio_y_min=-0.5
        #ratio_y_max= 0.5
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
    g_mc_stat.SetFillColor(stat_color)
    g_mc_stat.SetFillStyle(stat_style)
    g_mc_stat_sys.Draw("2p")
    dummy_ratio.Draw("AXISSAME")
    remove_zero_point(g_ratio, -1)
    g_ratio.Draw("pZ0")
    canvas.Update()
    canvas.Print('%s/%s/%s.png'%(out_dir,date,out_name))    
#    canvas.SaveAs('%s/%s/%s.pdf'%(out_dir,date,out_name))    
#    canvas.SaveAs('%s/%s/%s.C'%(out_dir,date,out_name))    
#    canvas.SaveAs('%s/%s/%s.root'%(out_dir,date,out_name))    
    ################## HEP Data ####################
    #if out_name in ["h_mee_all",'h_mee_all_BB','h_mee_all_BE'] and True:
    if out_name in ["h_mee_all",'h_mee_all_BB','h_mee_all_BE','h_mee_all_EE','h_mee_all_cumlative_v1','h_mee_all_cumlative_BE_v1','h_mee_all_cumlative_BB_v1','h_mee_all_cumlative_EE_v1'] and True:
        h_ZToEE_mee=0;
        h_ttbar_other_mee=0;
        h_jets_mee=0;
        TList  =h_stack.GetHists()
        Nhists =h_stack.GetNhists() 
        print "+++++++++++++++++++++++"
        print TList
        for i in range(0, Nhists):
            Object=TList.At(i)     
            if "ZToEE" in Object.GetName():h_ZToEE_mee=Object
            elif "ttbar" in Object.GetName():h_ttbar_other_mee=Object
            elif "Jets" in Object.GetName():h_jets_mee=Object
        print h_ZToEE_mee
        print h_ttbar_other_mee
        print h_jets_mee
        ####### for combine result ###################
        f_comb= ROOT.TFile("Result_2017.root","update")
        f_comb.cd()
        h_data           .Write("Data_%s"%out_name    ,ROOT.TObject.kOverwrite)
        h_mc             .Write("MC_all_%s"%out_name  ,ROOT.TObject.kOverwrite)
        g_mc             .Write("Sys_all_%s"%out_name ,ROOT.TObject.kOverwrite)
        h_ZToEE_mee      .Write("ZToEE_%s"%out_name   ,ROOT.TObject.kOverwrite)
        h_ttbar_other_mee.Write("ttbar_%s"%out_name   ,ROOT.TObject.kOverwrite)
        h_jets_mee       .Write("jets_%s"%out_name    ,ROOT.TObject.kOverwrite)
        f_comb.Close()
        print "save results for combine"
        #############################################
        g_ZToEE      =ROOT.TGraphAsymmErrors(h_ZToEE_mee) 
        g_ttbar_other=ROOT.TGraphAsymmErrors(h_ttbar_other_mee) 
        g_jets       =ROOT.TGraphAsymmErrors(h_jets_mee) 

        f_HEPData= ROOT.TFile("HEPData_2017.root","update")
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

                g_ZToEE.SetPoint(i,g_ZToEE.GetX()[i],0)
                g_ZToEE.SetPointEYlow (i,0)
                g_ZToEE.SetPointEYhigh(i,0)
                g_ttbar_other.SetPoint(i,g_ttbar_other.GetX()[i],0)
                g_ttbar_other.SetPointEYlow (i,0)
                g_ttbar_other.SetPointEYhigh(i,0)
                g_jets.SetPoint(i,g_jets.GetX()[i],0)
                g_jets.SetPointEYlow (i,0)
                g_jets.SetPointEYhigh(i,0)


        g_data_clone.Write("data_%s"%out_name,ROOT.TObject.kOverwrite) 
        g_mc_clone  .Write("mc_%s"%out_name  ,ROOT.TObject.kOverwrite) 

        g_ZToEE      .Write("ZToEE_%s"%out_name  ,ROOT.TObject.kOverwrite) 
        g_ttbar_other.Write("ttbar_%s"%out_name  ,ROOT.TObject.kOverwrite) 
        g_jets       .Write("jets_%s"%out_name   ,ROOT.TObject.kOverwrite) 

        f_HEPData.Close()
#    ################ Fit background ####################
    #if out_name in ["h_mee_usual","h_mee_BB_usual","h_mee_BE_usual","h_mee_all","h_mee_all_BB","h_mee_all_BE","h_mee_all_EE","h_mee_cosp_BB_usual","h_mee_cosp_BE_usual","h_mee_cosm_BB_usual","h_mee_cosm_BE_usual"] and True:
    if out_name in ["h_mee_usual","h_mee_BB_usual","h_mee_BE_usual"] and True:
        f_bgk_out= ROOT.TFile("bgk_2017.root","UPDATE");
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
            h_data_rebin= hist_rebin(System_uncertainty["nominal"].rebin_min_event, h_data      , System_uncertainty["nominal"].rebin_hist[0], True)
        elif out_name in ["h_mee_all_BB_sin"]:
            h_data_rebin= hist_rebin(System_uncertainty["nominal"].rebin_min_event, h_data      , System_uncertainty["nominal"].rebin_hist[1], True)
        elif out_name in ["h_mee_all_BE_sin"]:
            h_data_rebin= hist_rebin(System_uncertainty["nominal"].rebin_min_event, h_data      , System_uncertainty["nominal"].rebin_hist[2], True)
        elif out_name in ["h_mee_all_EE_sin"]:
            h_data_rebin= hist_rebin(System_uncertainty["nominal"].rebin_min_event, h_data      , System_uncertainty["nominal"].rebin_hist[3], True)
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

def Set_and_Draw(date, out_dir, hname, System_uncertainty, total_hist, ttbar_other_hist, ZToEE_hist, Jets_hist, ASF_dict):
    stack_mc  = ROOT.THStack()
    for hist in System_uncertainty["nominal"].sample_hist["data"]:
        if hist.GetName().split("data_")[-1] != hname: continue
        h_data=hist.Clone("data_"+hname)
        h_mc=total_hist[hname].Clone("mc_"+hname)
        h_ttbar_other=ttbar_other_hist[hname].Clone("ttbar_other_"+hname)
        h_ZToEE=ZToEE_hist[hname].Clone("ZToEE_"+hname)
        h_Jets=Jets_hist[hname].Clone("Jets_"+hname)
        if "cumlative" in hname:
            h_data=cumulate(hist, "data_"+hname)
        #    h_mc  =cumulate(total_hist[hname], "mc_"+hname)
        #    h_ttbar_other=cumulate(ttbar_other_hist[hname], "ttbar_other_"+hname)
        #    h_ZToEE=cumulate(ZToEE_hist[hname], "ZToEE_"+hname)
        #for sname in System_uncertainty["nominal"].sample_hist:
        #    if sname != "Jets": continue
        #    for hi in System_uncertainty["nominal"].sample_hist[sname]:
        #        if hi.GetName().split(sname+"_")[-1] != hname: continue
        #        h_tmp=hi.Clone(sname+"_"+hname)
        #        if "cumlative" in hname:
        #            h_tmp=cumulate(hi, sname+"_"+hname)
        #        h_tmp.SetFillColor(ROOT.kYellow) ##official color
        #        h_tmp.SetLineColor(ROOT.kBlack)
        #        stack_mc.Add(h_tmp)
        h_Jets.SetFillColor(ROOT.TColor.GetColor("#ffff66")) ##official color
        h_Jets.SetLineColor(ROOT.kBlack)
        stack_mc.Add(h_Jets)
        h_ttbar_other.SetFillColor(ROOT.TColor.GetColor("#ff6666"))##official color
        h_ttbar_other.SetLineColor(ROOT.kBlack)
        h_ZToEE.SetFillColor(ROOT.TColor.GetColor("#99ccff"))##official color
        h_ZToEE.SetLineColor(ROOT.kBlack)
        stack_mc.Add(h_ttbar_other)
        stack_mc.Add(h_ZToEE)
        h_data.SetStats(0)
        h_mc.SetStats(0)
        h_mc.SetLineColor(ROOT.kBlack)
        #g_mc  =get_total_err(h_mc,total_sys_err[hname]["bkg_all"][0],total_sys_err[hname]["bkg_all"][1])
        g_mc  =get_total_err(h_mc,total_system_err[hname]["bkg_all"][0],total_system_err[hname]["bkg_all"][1])
        draw_plots(date, out_dir, stack_mc,h_mc,g_mc,h_data,hname, False)
        if hname in ["h_mee_cosp_fine","h_mee_cosp_BB_fine","h_mee_cosp_BE_fine","h_mee_cosp_EE_fine","h_mee_cosm_fine","h_mee_cosm_BB_fine","h_mee_cosm_BE_fine","h_mee_cosm_EE_fine","h_mee_cosp_all_fine","h_mee_cosm_all_fine"]:
            ASF_dict[hname]=[]
            ASF_dict[hname].append(h_data)
            ASF_dict[hname].append(g_mc)

def Draw_ASF(Dict):
    for hname in  ["h_mee_cosp_fine","h_mee_cosp_BB_fine","h_mee_cosp_BE_fine","h_mee_cosp_EE_fine","h_mee_cosp_all_fine"]:
        if Dict[hname]:
            h_cosp_data=Dict[hname][0]
            g_cosp_data=histTograph(h_cosp_data)
            g_cosp_mc  =Dict[hname][1]
            h_cosm_data=Dict[hname.replace("cosp","cosm")][0]
            g_cosm_data=histTograph(h_cosm_data)
            g_cosm_mc  =Dict[hname.replace("cosp","cosm")][1]
            g_ASF_mc  =g_cosp_mc.Clone(hname+"_mc_asf")
            g_ASF_data=g_cosp_data.Clone(hname+"_data_asf")
            if g_ASF_mc.GetN() != g_ASF_data.GetN():print "wrong bin :mc %d, data %d"%(g_ASF_mc.GetN(),g_ASF_data.GetN())
            for iN in range(0,g_ASF_mc.GetN()):
                value_data =float(g_cosp_data.GetY()[iN]-g_cosm_data.GetY()[iN])/(g_cosp_data.GetY()[iN]+g_cosm_data.GetY()[iN]) if (g_cosp_data.GetY()[iN]+g_cosm_data.GetY()[iN])!=0 else 0 ##p-m/(p+m)
                err_data_up  =2*math.sqrt(math.pow(g_cosp_data.GetY()[iN]*g_cosm_data.GetEYhigh()[iN],2)+math.pow(g_cosm_data.GetY()[iN]*g_cosp_data.GetEYhigh()[iN],2))/math.pow(g_cosp_data.GetY()[iN]+g_cosm_data.GetY()[iN],2) if (g_cosp_data.GetY()[iN]+g_cosm_data.GetY()[iN])!=0 else 0
                err_data_down=2*math.sqrt(math.pow(g_cosp_data.GetY()[iN]*g_cosm_data.GetEYlow()[iN],2) +math.pow(g_cosm_data.GetY()[iN]*g_cosp_data.GetEYlow()[iN],2)) /math.pow(g_cosp_data.GetY()[iN]+g_cosm_data.GetY()[iN],2) if (g_cosp_data.GetY()[iN]+g_cosm_data.GetY()[iN])!=0 else 0
                value_mc   =float(g_cosp_mc.GetY()[iN]-g_cosm_mc.GetY()[iN])/(g_cosp_mc.GetY()[iN]+g_cosm_mc.GetY()[iN]) if (g_cosp_mc.GetY()[iN]+g_cosm_mc.GetY()[iN])!=0 else 0 ##p-m/(p+m) 
                err_mc_up    =2*math.sqrt(math.pow(g_cosp_mc.GetY()[iN]*g_cosm_mc.GetEYhigh()[iN],2)+math.pow(g_cosm_mc.GetY()[iN]*g_cosp_mc.GetEYhigh()[iN],2))/math.pow(g_cosp_mc.GetY()[iN]+g_cosm_mc.GetY()[iN],2) if (g_cosp_mc.GetY()[iN]+g_cosm_mc.GetY()[iN])!=0 else 0
                err_mc_down  =2*math.sqrt(math.pow(g_cosp_mc.GetY()[iN]*g_cosm_mc.GetEYlow()[iN],2) +math.pow(g_cosm_mc.GetY()[iN]*g_cosp_mc.GetEYlow()[iN],2)) /math.pow(g_cosp_mc.GetY()[iN]+g_cosm_mc.GetY()[iN],2) if (g_cosp_mc.GetY()[iN]+g_cosm_mc.GetY()[iN])!=0 else 0
                g_ASF_data.SetPoint(iN,g_ASF_data.GetX()[iN],value_data) 
                g_ASF_data.SetPointEYhigh(iN,err_data_up  )
                g_ASF_data.SetPointEYlow (iN,err_data_down)
                g_ASF_mc.SetPoint(iN,g_ASF_mc.GetX()[iN],value_mc) 
                g_ASF_mc.SetPointEYhigh(iN,err_mc_up  )
                g_ASF_mc.SetPointEYlow (iN,err_mc_down)
            draw_gr_ratio(g_ASF_data,g_ASF_mc)     

def draw_gr_ratio(g_data,g_mc):
    canvas = ROOT.TCanvas('canvas','',100,100,1000,1000)
    canvas.cd()
    size = 0.25
    pad1 = ROOT.TPad('pad1', '', 0.0, size, 1.0, 1.0, 0)
    pad2 = ROOT.TPad('pad2', '', 0.0, 0.0, 1.0, size, 0)
    pad1.Draw()
    pad2.Draw() 
    pad1.SetGridy()
    pad2.SetGridy()
    pad1.SetBottomMargin(0.07)
    pad2.SetTopMargin(0)
    pad2.SetBottomMargin(0.35)
    pad1.SetRightMargin(0.07)
    pad1.SetLeftMargin(0.13)
    pad2.SetRightMargin(0.07)
    pad2.SetLeftMargin(0.13)
    pad1.cd()
    pad1.SetLogx()
    pad2.SetLogx()
    nbin=1
    x_min=60
    x_max=3000
    y_min=-0.5
    y_max=0.5
    dummy = ROOT.TH2D("dummy","",nbin,x_min,x_max,1,y_min,y_max)
    dummy.SetStats(ROOT.kFALSE)
    dummy_X_title='m(ee) [GeV]'
    dummy_Y_title='A_{FB}'
    dummy.GetYaxis().SetTitle(dummy_Y_title)
    dummy.GetYaxis().SetTitleSize(0.05)
    dummy.GetYaxis().SetLabelSize(0.045)
    dummy.GetYaxis().SetTitleOffset(1.3)
    dummy.GetXaxis().SetTitle("")
    dummy.GetXaxis().SetLabelSize(0.045)
    dummy.GetXaxis().SetMoreLogLabels()
    dummy.GetXaxis().SetNoExponent()  
    dummy.Draw()
    g_data.SetMarkerColor(ROOT.kBlack)
    g_data.SetMarkerStyle(20)
    g_data.SetMarkerSize(0.8)
    g_mc.SetLineColor(ROOT.kRed)
    g_mc.SetMarkerColor(ROOT.kRed)
    g_mc.SetMarkerStyle(4)
    g_mc.SetMarkerSize(0.8)
    g_mc.SetFillColor(ROOT.kRed-10)
    g_mc.SetFillStyle(1001)
    g_mc.Draw("2p")
    g_mc.Draw("pZ0")
    dummy.Draw("AXISSAME")
#    Graph_Xerror0(g_data) 
    g_data.Draw("pZ0")
    legend = ROOT.TLegend(0.2, 0.1, 0.50, 0.2, "", "brNDC")
    legend.AddEntry(g_data,'Data','ep')
    legend.AddEntry(g_mc  ,'bgk' ,'fepl' )
    legend.SetBorderSize(0)
    legend.SetLineColor(1)
    legend.SetLineStyle(1)
    legend.SetLineWidth(1)
    legend.SetFillColor(19)
    legend.SetFillStyle(0)
    font = 42
    legend.SetTextFont(font)
    legend.Draw()
    label_cms = ROOT.TPaveLabel(0.112, 0.811, 0.369, 0.907, "CMS", "brNDC")
    label_cms.SetBorderSize(0)
    label_cms.SetFillColor(0)
    label_cms.SetFillStyle(0)
    label_cms.SetTextFont(61)
    label_cms.SetTextSize(0.44/0.75)
    label_cms.Draw()
    label_prelim = ROOT.TPaveLabel(0.112, 0.745, 0.369, 0.841, "Preliminary", "brNDC")
    label_prelim.SetBorderSize(0)
    label_prelim.SetFillColor(0)
    label_prelim.SetFillStyle(0)
    label_prelim.SetTextFont(51)
    label_prelim.SetTextSize(0.44/0.75 * 0.8)
    label_prelim.Draw()
    label_lumi = ROOT.TPaveLabel(0.69, 0.902, 0.994, 0.997, "35.9 fb^{-1} (13 TeV)", "brNDC")
    label_lumi.SetBorderSize(0)
    label_lumi.SetFillColor(0)
    label_lumi.SetFillStyle(0)
    label_lumi.SetTextFont(font)
    label_lumi.SetTextSize(0.44)
    label_lumi.Draw()
    labels_region = ROOT.TPaveLabel(0.285268, 0.812937, 0.627902, 0.907343, "", "brNDC")
    labels_region.SetBorderSize(0)
    labels_region.SetFillColor(0)
    labels_region.SetFillStyle(0)
    labels_region.SetTextFont(font)
    labels_region.SetTextSize(0.425926 )  
    if "BB" in g_data.GetName():
        labels_region.SetLabel("Barrel-Barrel")
        labels_region.Draw()
    elif "BE" in g_data.GetName():
        labels_region.SetLabel("Barrel-Endcap")
        labels_region.Draw()
    elif "EE" in g_data.GetName():
        labels_region.SetLabel("Endcap-Endcap")
        labels_region.Draw()
    pad2.cd()
    ratio_y_min=-5
    ratio_y_max=5
    dummy_ratio = ROOT.TH2D("dummy_ratio","",nbin,x_min,x_max,1,ratio_y_min,ratio_y_max)
    dummy_ratio.SetStats(ROOT.kFALSE)
    dummy_ratio.GetYaxis().SetTitle('(data-bgk)/bgk')
    dummy_ratio.GetXaxis().SetTitle(dummy_X_title)
    dummy_ratio.SetMarkerSize(0.7)
    dummy_ratio.GetXaxis().SetTitleSize(0.14)
    dummy_ratio.GetXaxis().SetTitleOffset(1.1)
    dummy_ratio.GetXaxis().SetLabelSize(0.13)
    dummy_ratio.GetXaxis().SetMoreLogLabels()
    dummy_ratio.GetXaxis().SetNoExponent()  
    dummy_ratio.GetYaxis().SetNdivisions(405)
    dummy_ratio.GetYaxis().SetTitleSize(0.14)
    dummy_ratio.GetYaxis().SetLabelSize(0.13)
    dummy_ratio.GetYaxis().SetTitleOffset(0.38)
    dummy_ratio.Draw()
    g_ratio = get_graph_ratio(g_data, g_mc)
    g_mc_stat_sys=get_self_err(g_mc)
    g_mc_stat_sys.SetFillColor(ROOT.kRed-10)
    g_mc_stat_sys.SetFillStyle(1001)
    g_mc_stat_sys.Draw("2")
    dummy_ratio.Draw("AXISSAME")
#    Graph_Xerror0(g_ratio) 
    g_ratio.Draw("pZ0")
    
    canvas.Print('./ASF_plot/%s.png'%(g_data.GetName()))    
    del canvas
    gc.collect()
    


def hist_add(h1,h2):
    if h1.GetNbinsX() != h2.GetNbinsX():
        print "error, different bin"
        return
    for ibin in range(1,h1.GetNbinsX()+1):
        value=h1.GetBinContent(ibin)+h2.GetBinContent(ibin)
        error=math.sqrt(math.pow(h1.GetBinError(ibin),2)+math.pow(h2.GetBinError(ibin),2))
        h1.SetBinContent(ibin,value)
        h1.SetBinError(ibin,error)


def table_hist(hname, nsys, System_uncertainty): 
     
    for hist in System_uncertainty[nsys].sample_hist["data"]:
        if hist.GetName().split("data_")[-1] != hname: continue
       # list_x=[]
       # list_x.append(hist.GetBinLowEdge(1))
       # for ibin in range(1,hist.GetNbinsX()+1):
       #     list_x.append(hist.GetBinLowEdge(ibin)+hist.GetBinWidth(ibin))
       # 
       # edge_X = array(list_x,dtype=float64)
        edge_X = array('d')
        edge_i = ROOT.Double(hist.GetBinLowEdge(1))
        edge_X.append(edge_i)
       # edge_X = array('f')
       # edge_X.append(float(hist.GetBinLowEdge(1)))
        for ibin in range(1,hist.GetNbinsX()+1):
            edge_i = ROOT.Double(hist.GetBinLowEdge(ibin)+hist.GetBinWidth(ibin))
            edge_X.append(edge_i)
           # edge_X.append(float(hist.GetBinLowEdge(ibin)+hist.GetBinWidth(ibin)))
        bgk_all        =ROOT.TH1D(hname+nsys+"all"        ,"",len(edge_X)-1,edge_X)
        bgk_ZToEE      =ROOT.TH1D(hname+nsys+"ZtoEE"      ,"",len(edge_X)-1,edge_X)
        bgk_ttbar_other=ROOT.TH1D(hname+nsys+"ttbar_other","",len(edge_X)-1,edge_X)
        bgk_Jets       =ROOT.TH1D(hname+nsys+"Jets"       ,"",len(edge_X)-1,edge_X)
        #Xaxis=hist.GetXaxis()
        #Bins=Xaxis.GetXbins()
        #bgk_all        =ROOT.TH1D(hname+nsys+"all"        ,"",hist.GetNbinsX(),Bins.GetArray())
        #bgk_ZToEE      =ROOT.TH1D(hname+nsys+"ZtoEE"      ,"",hist.GetNbinsX(),Bins.GetArray())
        #bgk_ttbar_other=ROOT.TH1D(hname+nsys+"ttbar_other","",hist.GetNbinsX(),Bins.GetArray())
        #bgk_Jets       =ROOT.TH1D(hname+nsys+"Jets"       ,"",hist.GetNbinsX(),Bins.GetArray())
        #bgk_all        =hist.Clone(hname+nsys+"all")
        #bgk_ZToEE      =hist.Clone(hname+nsys+"ZtoEE")
        #bgk_ttbar_other=hist.Clone(hname+nsys+"ttbar_other")
        #bgk_Jets       =hist.Clone(hname+nsys+"Jets")
        #bgk_all        .Scale(0)
        #bgk_ZToEE      .Scale(0)
        #bgk_ttbar_other.Scale(0)
        #bgk_Jets       .Scale(0)
       
        for sname in System_uncertainty[nsys].sample_hist:
            if sname == "data":continue
            for hs in System_uncertainty[nsys].sample_hist[sname]:
                if hs.GetName().split(sname+"_")[-1] != hname: continue
               # print "for %s, %s,  %s "%(nsys, sname,hs.GetName())
                hist_add(bgk_all,hs)
               # bgk_all.Add(hs,1)
                if "Jets" not in sname and "ZToEE" not in sname:
                   # bgk_ttbar_other.Add(hs,1)
                    hist_add(bgk_ttbar_other,hs)
                if "ZToEE" in sname:
                   # bgk_ZToEE.Add(hs,1)
                    hist_add(bgk_ZToEE,hs)
                if "Jets" in sname:
                   # bgk_Jets.Add(hs,1)
                    hist_add(bgk_Jets,hs)
        return [bgk_all,bgk_ZToEE,bgk_ttbar_other,bgk_Jets]

def DY_pdf(low,up):
   pdf_uncert=ROOT.TF1("","[0]+[1]*x+[2]*x*x+[3]*x*x*x+[4]*x*x*x*x") 
   pdf_uncert.SetParameters(0.766834,0.00143718,1.77466e-07,-1.9951e-10,3.69842e-14)
   value_low=pdf_uncert.Eval(low)
   value_up =pdf_uncert.Eval(up)
#   print "%d-%d:%f"%(low,up,float(value_low+value_up)/200)
   return float(value_low+value_up)/200
def DY_pdf_new(low,up):
   pdf_uncert=ROOT.TF1("","[0]+[1]*x+[2]*x*x+[3]*x*x*x+[4]*x*x*x*x") 
   pdf_uncert.SetParameters(1.25509,-0.000131645,1.28426e-06,-5.32126e-10,7.62146e-14)
   value_low=pdf_uncert.Eval(low)
   value_up =pdf_uncert.Eval(up)
#   print "%d-%d:%f"%(low,up,float(value_low+value_up)/200)
   return float(value_low+value_up)/200

def smooth_hist(hist,low,up, value):
    Xaxis=hist.GetXaxis() 
    bin_low= Xaxis.FindBin(low)
    bin_up = Xaxis.FindBin(up )
    for ibin in range(bin_low,bin_up+1):
        hist.SetBinContent(ibin,value)

class file_object:
    def __init__(self, file_name, name, event, crosssection, color):
        self.name = name
        self.file_name = file_name
        self.event = event
        self.crosssection = crosssection
        self.lumi = self.event/self.crosssection
        self.color = color
        #self.tfilename = 'ntuples/sys_saved_hist/20190530_NewID/all/%s.root'%(self.file_name)
        #self.tfilename = 'ntuples/sys_saved_hist/20190603_Et/all/%s.root'%(self.file_name)
        #self.tfilename = 'ntuples/sys_saved_hist/2016/20190605/all/%s.root'%(self.file_name)
        #self.tfilename = 'ntuples/sys_saved_hist/2016/20190605_pf_up/all/%s.root'%(self.file_name)
        #self.tfilename = 'ntuples/sys_saved_hist/2016/20190605_pf_down/all/%s.root'%(self.file_name)
        #self.tfilename = 'ntuples/sys_saved_hist/2016/20190614/all/%s.root'%(self.file_name)
        #self.tfilename = 'ntuples/sys_saved_hist/2016/20190614_NoPW/all/%s.root'%(self.file_name)
        #self.tfilename = 'ntuples/sys_saved_hist/2016/20190615_trigTurnOn/all/%s.root'%(self.file_name)
        #self.tfilename = 'ntuples/sys_saved_hist/2016/20190615_trigTurnOn_NoPUW/all/%s.root'%(self.file_name)
        #self.tfilename = 'ntuples/sys_saved_hist/2017/20190615/all/%s.root'%(self.file_name)
        #self.tfilename = 'ntuples/sys_saved_hist/2017/20190615_noPUW/all/%s.root'%(self.file_name)
        #self.tfilename = 'ntuples/sys_saved_hist/2017/20190623_GenM/all/%s.root'%(self.file_name)
        #self.tfilename = 'ntuples/sys_saved_hist/2017/20190628_EENoTTW/all/%s.root'%(self.file_name)
        #self.tfilename = 'ntuples/sys_saved_hist/2017/20190703_fr_MasScale/all/%s.root'%(self.file_name)
        self.tfilename = 'ntuples/sys_saved_hist/2017/20190704_newBin/all/%s.root'%(self.file_name)
        self.tfile = ROOT.TFile(self.tfilename,'READ')


class collcet_hist:
    def __init__(self, name, fewz_correct, TTbar_MLL, WW_MLL, sys_uncert):
        self.name=name
        self.use_fewz_correct=fewz_correct
        self.use_TTbar_MLL=TTbar_MLL
        self.use_WW_MLL   =WW_MLL
        self.sys_uncert=sys_uncert
        self.str_uncert=""
        self.str_uncert_Z=""
        self.rebin_min_event=10
        self.rebin_hist=[]
        if self.sys_uncert=="PU_scale_up"                 : self.str_uncert="PU_scale_up_"
        elif self.sys_uncert=="PU_scale_down"             : self.str_uncert="PU_scale_down_"
        elif self.sys_uncert=="Barrel_energy_scale_up"    : self.str_uncert="Barrel_energy_scale_up_"
        elif self.sys_uncert=="Barrel_energy_scale_down"  : self.str_uncert="Barrel_energy_scale_down_"
        elif self.sys_uncert=="Endcap_energy_scale_up"    : self.str_uncert="Endcap_energy_scale_up_"
        elif self.sys_uncert=="Endcap_energy_scale_down"  : self.str_uncert="Endcap_energy_scale_down_"
        elif self.sys_uncert=="BB_mass_scale_up"          : self.str_uncert="BB_mass_scale_up_"
        elif self.sys_uncert=="BB_mass_scale_down"        : self.str_uncert="BB_mass_scale_down_"
        elif self.sys_uncert=="BE_mass_scale_up"          : self.str_uncert="BE_mass_scale_up_"
        elif self.sys_uncert=="BE_mass_scale_down"        : self.str_uncert="BE_mass_scale_down_"
        elif self.sys_uncert=="Barrel_SF_scale_up"        : self.str_uncert="Barrel_SF_scale_up_"
        elif self.sys_uncert=="Barrel_SF_scale_down"      : self.str_uncert="Barrel_SF_scale_down_"
        elif self.sys_uncert=="Endcap_SF_scale_up"        : self.str_uncert="Endcap_SF_scale_up_"
        elif self.sys_uncert=="Endcap_SF_scale_down"      : self.str_uncert="Endcap_SF_scale_down_"
        elif self.sys_uncert=="pf_scale_up"               : self.str_uncert="pf_scale_up_"
        elif self.sys_uncert=="pf_scale_down"             : self.str_uncert="pf_scale_down_"
        self.str_uncert_Z=self.str_uncert
        if self.sys_uncert=="pdf_scale_up"                : self.str_uncert_Z="pdf_scale_up_"
        elif self.sys_uncert=="pdf_scale_down"            : self.str_uncert_Z="pdf_scale_down_"
#        self.DY_pdf_50_120   =DY_pdf_new(50,120)
#        self.DY_pdf_120_200  =DY_pdf_new(120,200)
#        self.DY_pdf_200_400  =DY_pdf_new(200,400)
#        self.DY_pdf_400_800  =DY_pdf_new(400,800)
#        self.DY_pdf_800_1400 =DY_pdf_new(800,1400)
#        self.DY_pdf_1400_2300=DY_pdf_new(1400,2300)
#        self.DY_pdf_2300_3500=DY_pdf_new(2300,3500)
#        self.DY_pdf_3500_4500=DY_pdf_new(3500,4500)
#        self.DY_pdf_4500_6000=DY_pdf_new(4500,6000)
#        self.DY_pdf_6000_Inf =DY_pdf_new(6000,7500)
        self.files={}
        self.files_1F={}
        self.files_2F={}
        self.hist_name=[]
        self.data_lumi=Luminosity
        self.normalized_lumi   =self.data_lumi
        self.normalized_lumi_BB=self.data_lumi
        self.normalized_lumi_BE=self.data_lumi
        self.normalized_lumi_EE=self.data_lumi
        self.Xsection={}
        self.Xsection['ZToEE_50_120']   =  1975.0  
        self.Xsection['ZToEE_120_200']  =  19.32    
        self.Xsection['ZToEE_200_400']  =  2.73     
        self.Xsection['ZToEE_400_800']  =  0.241    
        self.Xsection['ZToEE_800_1400'] =  1.68E-2   
        self.Xsection['ZToEE_1400_2300']=  1.39E-3    
        self.Xsection['ZToEE_2300_3500']=  8.948E-5     
        self.Xsection['ZToEE_3500_4500']=  4.135E-6  
        self.Xsection['ZToEE_4500_6000']=  4.56E-7   
        self.Xsection['ZToEE_6000_Inf'] =  2.06E-8   

        self.Xsection['NNPDF31_ZToEE_50_120']   = 2112.90 
        self.Xsection['NNPDF31_ZToEE_120_200']  = 20.56   
        self.Xsection['NNPDF31_ZToEE_200_400']  = 2.89    
        self.Xsection['NNPDF31_ZToEE_400_800']  = 0.252   
        self.Xsection['NNPDF31_ZToEE_800_1400'] = 1.71E-2 
        self.Xsection['NNPDF31_ZToEE_1400_2300']= 1.37E-3 
        self.Xsection['NNPDF31_ZToEE_2300_3500']= 8.178E-5
        self.Xsection['NNPDF31_ZToEE_3500_4500']= 3.191E-6
        self.Xsection['NNPDF31_ZToEE_4500_6000']= 2.787E-7
        self.Xsection['NNPDF31_ZToEE_6000_Inf'] = 9.56E-9 

        self.Xsection['ZToTT_amc']      =  5765.4   
        self.Xsection['TTbar']          =  87.31       
        self.Xsection['TTbar_500_800']  =  0.326    
        self.Xsection['TTbar_800_1200'] =  0.0326   
        self.Xsection['TTbar_1200_1800']=  3.05E-3     
        self.Xsection['TTbar_1800_Inf'] =  1.74E-4    
        self.Xsection['WW_inc']         =  118.7   
        self.Xsection['WW']             =  12.178   
        self.Xsection['WW_200_600']     =  1.386    
        self.Xsection['WW_600_1200']    =  0.05665 
        self.Xsection['WW_1200_2500']   =  0.003557
        self.Xsection['WW_2500_Inf']    =  0.00005395
        self.Xsection['WZ_inc']         =  47.13   
        self.Xsection['WZ_3LNu']        =  4.42965   
        self.Xsection['WZ_2L2Q']        =  6.331#5.595   
        self.Xsection['ZZ_inc']         =  16.523   
        self.Xsection['ZZ_2L2Q']        =  1.999   
        self.Xsection['ZZ_2L2Nu']       =  0.564   
        self.Xsection['ZZ_4L']          =  1.212   
        self.Xsection['ST']             =  19.47    
        self.Xsection['ST_anti']        =  19.47   
        self.uncer_Xsection   =0.07 
        self.Xsection_uncer             = {}
        #self.Xsection_uncer["DY"]       = 0.02
        #self.Xsection_uncer["ttbar"]    = 0.05
        #self.Xsection_uncer["WW"]       = 0.03
        #self.Xsection_uncer["WZ"]       = 0.04
        #self.Xsection_uncer["ZZ"]       = 0.04
        #self.Xsection_uncer["ST"]       = 0.05
        self.Xsection_uncer["DY"]       = 0.07
        self.Xsection_uncer["ttbar"]    = 0.07
        self.Xsection_uncer["WW"]       = 0.07
        self.Xsection_uncer["WZ"]       = 0.07
        self.Xsection_uncer["ZZ"]       = 0.07
        self.Xsection_uncer["ST"]       = 0.07
        if self.sys_uncert == "bgk_ZToTT_scale_up":
            self.Xsection['ZToTT_amc']      =  (1+self.Xsection_uncer["DY"])*self.Xsection['ZToTT_amc']      
        elif self.sys_uncert == "bgk_ZToTT_scale_down":
            self.Xsection['ZToTT_amc']      =  (1-self.Xsection_uncer["DY"])*self.Xsection['ZToTT_amc']      
        elif self.sys_uncert == "bgk_ttbar_scale_up":
            self.Xsection['TTbar']          =  (1+self.Xsection_uncer["ttbar"])*self.Xsection['TTbar']
            self.Xsection['TTbar_500_800']  =  (1+self.Xsection_uncer["ttbar"])*self.Xsection['TTbar_500_800']  
            self.Xsection['TTbar_800_1200'] =  (1+self.Xsection_uncer["ttbar"])*self.Xsection['TTbar_800_1200'] 
            self.Xsection['TTbar_1200_1800']=  (1+self.Xsection_uncer["ttbar"])*self.Xsection['TTbar_1200_1800']   
            self.Xsection['TTbar_1800_Inf'] =  (1+self.Xsection_uncer["ttbar"])*self.Xsection['TTbar_1800_Inf']   
        elif self.sys_uncert == "bgk_ttbar_scale_down":
            self.Xsection['TTbar']          =  (1-self.Xsection_uncer["ttbar"])*self.Xsection['TTbar']
            self.Xsection['TTbar_500_800']  =  (1-self.Xsection_uncer["ttbar"])*self.Xsection['TTbar_500_800']  
            self.Xsection['TTbar_800_1200'] =  (1-self.Xsection_uncer["ttbar"])*self.Xsection['TTbar_800_1200'] 
            self.Xsection['TTbar_1200_1800']=  (1-self.Xsection_uncer["ttbar"])*self.Xsection['TTbar_1200_1800']   
            self.Xsection['TTbar_1800_Inf'] =  (1-self.Xsection_uncer["ttbar"])*self.Xsection['TTbar_1800_Inf']   
        elif self.sys_uncert == "bgk_ww_scale_up":
            self.Xsection['WW_inc']         =  (1+self.Xsection_uncer["WW"])*self.Xsection['WW_inc']          
            self.Xsection['WW']             =  (1+self.Xsection_uncer["WW"])*self.Xsection['WW']          
            self.Xsection['WW_200_600']     =  (1+self.Xsection_uncer["WW"])*self.Xsection['WW_200_600']   
            self.Xsection['WW_600_1200']    =  (1+self.Xsection_uncer["WW"])*self.Xsection['WW_600_1200'] 
            self.Xsection['WW_1200_2500']   =  (1+self.Xsection_uncer["WW"])*self.Xsection['WW_1200_2500']
            self.Xsection['WW_2500_Inf']    =  (1+self.Xsection_uncer["WW"])*self.Xsection['WW_2500_Inf'] 
        elif self.sys_uncert == "bgk_ww_scale_down":
            self.Xsection['WW_inc']         =  (1-self.Xsection_uncer["WW"])*self.Xsection['WW_inc']          
            self.Xsection['WW']             =  (1-self.Xsection_uncer["WW"])*self.Xsection['WW']          
            self.Xsection['WW_200_600']     =  (1-self.Xsection_uncer["WW"])*self.Xsection['WW_200_600']   
            self.Xsection['WW_600_1200']    =  (1-self.Xsection_uncer["WW"])*self.Xsection['WW_600_1200'] 
            self.Xsection['WW_1200_2500']   =  (1-self.Xsection_uncer["WW"])*self.Xsection['WW_1200_2500']
            self.Xsection['WW_2500_Inf']    =  (1-self.Xsection_uncer["WW"])*self.Xsection['WW_2500_Inf'] 
        elif self.sys_uncert == "bgk_wz_scale_up":
            self.Xsection['WZ_inc']         =  (1+self.Xsection_uncer["WZ"])*self.Xsection['WZ_inc']          
            self.Xsection['WZ_3LNu']        =  (1+self.Xsection_uncer["WZ"])*self.Xsection['WZ_3LNu']          
            self.Xsection['WZ_2L2Q']        =  (1+self.Xsection_uncer["WZ"])*self.Xsection['WZ_2L2Q']          
        elif self.sys_uncert == "bgk_wz_scale_down":
            self.Xsection['WZ_inc']         =  (1-self.Xsection_uncer["WZ"])*self.Xsection['WZ_inc']          
            self.Xsection['WZ_3LNu']        =  (1-self.Xsection_uncer["WZ"])*self.Xsection['WZ_3LNu']          
            self.Xsection['WZ_2L2Q']        =  (1-self.Xsection_uncer["WZ"])*self.Xsection['WZ_2L2Q']          
        elif self.sys_uncert == "bgk_zz_scale_up":
            self.Xsection['ZZ_inc']         =  (1+self.Xsection_uncer["ZZ"])*self.Xsection['ZZ_inc']          
            self.Xsection['ZZ_2L2Q']        =  (1+self.Xsection_uncer["ZZ"])*self.Xsection['ZZ_2L2Q']          
            self.Xsection['ZZ_2L2Nu']       =  (1+self.Xsection_uncer["ZZ"])*self.Xsection['ZZ_2L2Nu']          
            self.Xsection['ZZ_4L']          =  (1+self.Xsection_uncer["ZZ"])*self.Xsection['ZZ_4L']          
        elif self.sys_uncert == "bgk_zz_scale_down":
            self.Xsection['ZZ_inc']         =  (1-self.Xsection_uncer["ZZ"])*self.Xsection['ZZ_inc']          
            self.Xsection['ZZ_2L2Q']        =  (1-self.Xsection_uncer["ZZ"])*self.Xsection['ZZ_2L2Q']          
            self.Xsection['ZZ_2L2Nu']       =  (1-self.Xsection_uncer["ZZ"])*self.Xsection['ZZ_2L2Nu']          
            self.Xsection['ZZ_4L']          =  (1-self.Xsection_uncer["ZZ"])*self.Xsection['ZZ_4L']          
        elif self.sys_uncert == "bgk_st_scale_up":
            self.Xsection['ST']             =  (1+self.Xsection_uncer["ST"])*self.Xsection['ST']          
            self.Xsection['ST_anti']        =  (1+self.Xsection_uncer["ST"])*self.Xsection['ST_anti']          
        elif self.sys_uncert == "bgk_st_scale_down":
            self.Xsection['ST']             =  (1-self.Xsection_uncer["ST"])*self.Xsection['ST']          
            self.Xsection['ST_anti']        =  (1-self.Xsection_uncer["ST"])*self.Xsection['ST_anti']          
    def get_input_file(self):
        self.files['data']               =file_object('hist_data_MiniAOD','data'       ,self.data_lumi      ,1     ,  ROOT.kBlack)
        if self.use_fewz_correct==False:
            self.files['ZToEE_50_120']   =file_object(self.str_uncert_Z+'hist_ZToEE_50_120','Z#rightarrowee'          , 2888223.0,  self.Xsection['NNPDF31_ZToEE_50_120']    ,    ROOT.kGreen)
            self.files['ZToEE_120_200']  =file_object(self.str_uncert_Z+'hist_ZToEE_120_200','ZToEE_120_200'          , 98968.0,    self.Xsection['NNPDF31_ZToEE_120_200']   ,    ROOT.kGreen)
            self.files['ZToEE_200_400']  =file_object(self.str_uncert_Z+'hist_ZToEE_200_400','ZToEE_200_400'          , 99572.0,    self.Xsection['NNPDF31_ZToEE_200_400']   ,    ROOT.kGreen)
            self.files['ZToEE_400_800']  =file_object(self.str_uncert_Z+'hist_ZToEE_400_800','ZToEE_400_800'          , 99888.0,    self.Xsection['NNPDF31_ZToEE_400_800']   ,    ROOT.kGreen)
            self.files['ZToEE_800_1400'] =file_object(self.str_uncert_Z+'hist_ZToEE_800_1400','ZToEE_800_1400'        , 99974.0,    self.Xsection['NNPDF31_ZToEE_800_1400']  ,    ROOT.kGreen)
            self.files['ZToEE_1400_2300']=file_object(self.str_uncert_Z+'hist_ZToEE_1400_2300','ZToEE_1400_2300'      , 99986.0,    self.Xsection['NNPDF31_ZToEE_1400_2300'] ,    ROOT.kGreen)
            self.files['ZToEE_2300_3500']=file_object(self.str_uncert_Z+'hist_ZToEE_2300_3500','ZToEE_2300_3500'      , 81440.0,    self.Xsection['NNPDF31_ZToEE_2300_3500'] ,    ROOT.kGreen)
            self.files['ZToEE_3500_4500']=file_object(self.str_uncert_Z+'hist_ZToEE_3500_4500','ZToEE_3500_4500'      , 99820.0,    self.Xsection['NNPDF31_ZToEE_3500_4500'] ,    ROOT.kGreen)
            self.files['ZToEE_4500_6000']=file_object(self.str_uncert_Z+'hist_ZToEE_4500_6000','ZToEE_4500_6000'      , 99326.0,    self.Xsection['NNPDF31_ZToEE_4500_6000'] ,    ROOT.kGreen)
            self.files['ZToEE_6000_Inf'] =file_object(self.str_uncert_Z+'hist_ZToEE_6000_Inf','ZToEE_6000_Inf'        , 97935.0,    self.Xsection['NNPDF31_ZToEE_6000_Inf']  ,    ROOT.kGreen)
        else:
            self.files['ZToEE_50_120']   =file_object(self.str_uncert_Z+'hist_ZToEE_50_120_fewz','Z#rightarrowee'     , 2888223.0,  self.Xsection['NNPDF31_ZToEE_50_120']   ,    ROOT.kGreen)
            self.files['ZToEE_120_200']  =file_object(self.str_uncert_Z+'hist_ZToEE_120_200_fewz','ZToEE_120_200'     , 98968.0,    self.Xsection['NNPDF31_ZToEE_120_200']  ,    ROOT.kGreen)
            self.files['ZToEE_200_400']  =file_object(self.str_uncert_Z+'hist_ZToEE_200_400_fewz','ZToEE_200_400'     , 99572.0,    self.Xsection['NNPDF31_ZToEE_200_400']  ,    ROOT.kGreen)
            self.files['ZToEE_400_800']  =file_object(self.str_uncert_Z+'hist_ZToEE_400_800_fewz','ZToEE_400_800'     , 99888.0,    self.Xsection['NNPDF31_ZToEE_400_800']  ,    ROOT.kGreen)
            self.files['ZToEE_800_1400'] =file_object(self.str_uncert_Z+'hist_ZToEE_800_1400_fewz','ZToEE_800_1400'   , 99974.0,    self.Xsection['NNPDF31_ZToEE_800_1400'] ,    ROOT.kGreen)
            self.files['ZToEE_1400_2300']=file_object(self.str_uncert_Z+'hist_ZToEE_1400_2300_fewz','ZToEE_1400_2300' , 99986.0,    self.Xsection['NNPDF31_ZToEE_1400_2300'],    ROOT.kGreen)
            self.files['ZToEE_2300_3500']=file_object(self.str_uncert_Z+'hist_ZToEE_2300_3500_fewz','ZToEE_2300_3500' , 81440.0,    self.Xsection['NNPDF31_ZToEE_2300_3500'],    ROOT.kGreen)
            self.files['ZToEE_3500_4500']=file_object(self.str_uncert_Z+'hist_ZToEE_3500_4500_fewz','ZToEE_3500_4500' , 99820.0,    self.Xsection['NNPDF31_ZToEE_3500_4500'],    ROOT.kGreen)
            self.files['ZToEE_4500_6000']=file_object(self.str_uncert_Z+'hist_ZToEE_4500_6000_fewz','ZToEE_4500_6000' , 99326.0,    self.Xsection['NNPDF31_ZToEE_4500_6000'],    ROOT.kGreen)
            self.files['ZToEE_6000_Inf'] =file_object(self.str_uncert_Z+'hist_ZToEE_6000_Inf_fewz','ZToEE_6000_Inf'   , 97935.0,    self.Xsection['NNPDF31_ZToEE_6000_Inf'] ,    ROOT.kGreen)
        self.files['ZToTT_amc']          =file_object(self.str_uncert+'hist_ZToTT','Z#rightarrow#tau#tau'             , 123015566.0,self.Xsection['ZToTT_amc']      ,    ROOT.kCyan)
        if self.use_TTbar_MLL == False: 
            self.files['TTbar']          =file_object(self.str_uncert+'hist_TTbar2L_all','TTbar'                      , 9511116.0,  self.Xsection['TTbar']          ,    ROOT.kYellow)
        else:
            self.files['TTbar']          =file_object(self.str_uncert+'hist_TTbar2L_500','TTbar'                      , 9511116,    self.Xsection['TTbar']          ,    ROOT.kYellow)
            self.files['TTbar_500_800']  =file_object(self.str_uncert+'hist_TTbar2L_500_800','TTbar_500_800'          , 755907,     self.Xsection['TTbar_500_800']  ,    ROOT.kYellow)
            self.files['TTbar_800_1200'] =file_object(self.str_uncert+'hist_TTbar2L_800_1200','TTbar_800_1200'        , 199636,     self.Xsection['TTbar_800_1200'] ,    ROOT.kYellow)
            self.files['TTbar_1200_1800']=file_object(self.str_uncert+'hist_TTbar2L_1200_1800','TTbar_1200_1800'      , 17507,      self.Xsection['TTbar_1200_1800'],    ROOT.kYellow)
            self.files['TTbar_1800_Inf'] =file_object(self.str_uncert+'hist_TTbar2L_1800_Inf','TTbar_1800_Inf'        , 953 ,       self.Xsection['TTbar_1800_Inf'] ,    ROOT.kYellow)
        self.files['ST']                 =file_object(self.str_uncert+'hist_ST','Single Top'                          , 4936387.0,  self.Xsection['ST']             ,    ROOT.kRed)
        self.files['ST_anti']            =file_object(self.str_uncert+'hist_ST_anti','ST_anti'                        , 5592819.0,  self.Xsection['ST_anti']        ,    ROOT.kRed)
        if self.use_WW_MLL == False: 
            self.files['WW']                 =file_object(self.str_uncert+'hist_WW','Di-Boson'                        , 1973294.0,  self.Xsection['WW_inc']         ,    ROOT.kMagenta)
        else:
            self.files['WW']                 =file_object(self.str_uncert+'hist_WW2L_200','Di-Boson'                  , 1973294.0,  self.Xsection['WW']             ,    ROOT.kMagenta)
            self.files['WW_200_600']         =file_object(self.str_uncert+'hist_WW2L_200_600','WW2L_200_600'          , 7922808.0,  self.Xsection['WW_200_600']     ,    ROOT.kMagenta)
            self.files['WW_600_1200']        =file_object(self.str_uncert+'hist_WW2L_600_1200','WW2L_600_1200'        , 2623154.0,  self.Xsection['WW_600_1200']    ,    ROOT.kMagenta)
            self.files['WW_1200_2500']       =file_object(self.str_uncert+'hist_WW2L_1200_2500','WW2L_1200_2500'      , 161573.0,   self.Xsection['WW_1200_2500']   ,    ROOT.kMagenta)
            self.files['WW_2500_Inf']        =file_object(self.str_uncert+'hist_WW2L_2500_Inf','WW2L_2500_Inf'        , 2349.0,     self.Xsection['WW_2500_Inf']    ,    ROOT.kMagenta)
        self.files['WZ_2L2Q']            =file_object(self.str_uncert+'hist_WZ_2L2Q','WZ_2L2Q'                        , 16534558.0, self.Xsection['WZ_2L2Q']        ,    ROOT.kMagenta)
        self.files['WZ_3LNu']            =file_object(self.str_uncert+'hist_WZ_3LNu','WZ_3LNu'                        , 965938.0,   self.Xsection['WZ_3LNu']        ,    ROOT.kMagenta)
        self.files['ZZ_2L2Nu']           =file_object(self.str_uncert+'hist_ZZ_2L2Nu','ZZ_2L2Nu'                      , 8733658.0,  self.Xsection['ZZ_2L2Nu']       ,    ROOT.kMagenta)
        self.files['ZZ_2L2Q']            =file_object(self.str_uncert+'hist_ZZ_2L2Q' ,'ZZ_2L2Q'                       , 17667929.0, self.Xsection['ZZ_2L2Q']        ,    ROOT.kMagenta)
        self.files['ZZ_4L']              =file_object(self.str_uncert+'hist_ZZ_4L'   ,'ZZ_4L'                         , 15912322.0, self.Xsection['ZZ_4L']          ,    ROOT.kMagenta)
        #self.files['WZ']                 =file_object(self.str_uncert+'hist_WZ','WZ'                                  , 3885000.0,  self.Xsection['WZ_inc']         ,    ROOT.kMagenta)
        #self.files['ZZ']                 =file_object(self.str_uncert+'hist_ZZ','ZZ'                                  , 1972000.0,  self.Xsection['ZZ_inc']         ,    ROOT.kMagenta)
        ############### tmp

        self.files_1F['data']               =file_object('hist_data_FR1F_MiniAOD','data'     ,self.data_lumi      ,1     ,  ROOT.kBlack)
        if self.use_fewz_correct == False:
            self.files_1F['ZToEE_50_120']   =file_object(self.str_uncert_Z+'hist_ZToEE_50_120_1F','Z#rightarrowee'          , 2888223.0,   self.Xsection['NNPDF31_ZToEE_50_120']    ,     ROOT.kGreen)
            self.files_1F['ZToEE_120_200']  =file_object(self.str_uncert_Z+'hist_ZToEE_120_200_1F','ZToEE_120_200'          , 98968.0,     self.Xsection['NNPDF31_ZToEE_120_200']   ,     ROOT.kGreen)
            self.files_1F['ZToEE_200_400']  =file_object(self.str_uncert_Z+'hist_ZToEE_200_400_1F','ZToEE_200_400'          , 99572.0,     self.Xsection['NNPDF31_ZToEE_200_400']   ,     ROOT.kGreen)
            self.files_1F['ZToEE_400_800']  =file_object(self.str_uncert_Z+'hist_ZToEE_400_800_1F','ZToEE_400_800'          , 99888.0,     self.Xsection['NNPDF31_ZToEE_400_800']   ,     ROOT.kGreen)
            self.files_1F['ZToEE_800_1400'] =file_object(self.str_uncert_Z+'hist_ZToEE_800_1400_1F','ZToEE_800_1400'        , 99974.0,     self.Xsection['NNPDF31_ZToEE_800_1400']  ,     ROOT.kGreen)
            self.files_1F['ZToEE_1400_2300']=file_object(self.str_uncert_Z+'hist_ZToEE_1400_2300_1F','ZToEE_1400_2300'      , 99986.0,     self.Xsection['NNPDF31_ZToEE_1400_2300'] ,     ROOT.kGreen)
            self.files_1F['ZToEE_2300_3500']=file_object(self.str_uncert_Z+'hist_ZToEE_2300_3500_1F','ZToEE_2300_3500'      , 81440.0,     self.Xsection['NNPDF31_ZToEE_2300_3500'] ,     ROOT.kGreen)
            self.files_1F['ZToEE_3500_4500']=file_object(self.str_uncert_Z+'hist_ZToEE_3500_4500_1F','ZToEE_3500_4500'      , 99820.0,     self.Xsection['NNPDF31_ZToEE_3500_4500'] ,     ROOT.kGreen)
            self.files_1F['ZToEE_4500_6000']=file_object(self.str_uncert_Z+'hist_ZToEE_4500_6000_1F','ZToEE_4500_6000'      , 99326.0,     self.Xsection['NNPDF31_ZToEE_4500_6000'] ,     ROOT.kGreen)
            self.files_1F['ZToEE_6000_Inf'] =file_object(self.str_uncert_Z+'hist_ZToEE_6000_Inf_1F' ,'ZToEE_6000_Inf'       , 97935.0,     self.Xsection['NNPDF31_ZToEE_6000_Inf']  ,     ROOT.kGreen)
        else:                                                                                                                                               
            self.files_1F['ZToEE_50_120']   =file_object(self.str_uncert_Z+'hist_ZToEE_50_120_fewz_1F','Z#rightarrowee'     , 2888223.0,   self.Xsection['NNPDF31_ZToEE_50_120']   ,     ROOT.kGreen)
            self.files_1F['ZToEE_120_200']  =file_object(self.str_uncert_Z+'hist_ZToEE_120_200_fewz_1F','ZToEE_120_200'     , 98968.0,     self.Xsection['NNPDF31_ZToEE_120_200']  ,     ROOT.kGreen)
            self.files_1F['ZToEE_200_400']  =file_object(self.str_uncert_Z+'hist_ZToEE_200_400_fewz_1F','ZToEE_200_400'     , 99572.0,     self.Xsection['NNPDF31_ZToEE_200_400']  ,     ROOT.kGreen)
            self.files_1F['ZToEE_400_800']  =file_object(self.str_uncert_Z+'hist_ZToEE_400_800_fewz_1F','ZToEE_400_800'     , 99888.0,     self.Xsection['NNPDF31_ZToEE_400_800']  ,     ROOT.kGreen)
            self.files_1F['ZToEE_800_1400'] =file_object(self.str_uncert_Z+'hist_ZToEE_800_1400_fewz_1F','ZToEE_800_1400'   , 99974.0,     self.Xsection['NNPDF31_ZToEE_800_1400'] ,     ROOT.kGreen)
            self.files_1F['ZToEE_1400_2300']=file_object(self.str_uncert_Z+'hist_ZToEE_1400_2300_fewz_1F','ZToEE_1400_2300' , 99986.0,     self.Xsection['NNPDF31_ZToEE_1400_2300'],     ROOT.kGreen)
            self.files_1F['ZToEE_2300_3500']=file_object(self.str_uncert_Z+'hist_ZToEE_2300_3500_fewz_1F','ZToEE_2300_3500' , 81440.0,     self.Xsection['NNPDF31_ZToEE_2300_3500'],     ROOT.kGreen)
            self.files_1F['ZToEE_3500_4500']=file_object(self.str_uncert_Z+'hist_ZToEE_3500_4500_fewz_1F','ZToEE_3500_4500' , 99820.0,     self.Xsection['NNPDF31_ZToEE_3500_4500'],     ROOT.kGreen)
            self.files_1F['ZToEE_4500_6000']=file_object(self.str_uncert_Z+'hist_ZToEE_4500_6000_fewz_1F','ZToEE_4500_6000' , 99326.0,     self.Xsection['NNPDF31_ZToEE_4500_6000'],     ROOT.kGreen)
            self.files_1F['ZToEE_6000_Inf'] =file_object(self.str_uncert_Z+'hist_ZToEE_6000_Inf_fewz_1F','ZToEE_6000_Inf'   , 97935.0,     self.Xsection['NNPDF31_ZToEE_6000_Inf'] ,     ROOT.kGreen)
        self.files_1F['ZToTT_amc']          =file_object(self.str_uncert+'hist_ZToTT_1F','Z#rightarrow#tau#tau'             , 123015566.0, self.Xsection['ZToTT_amc']      ,     ROOT.kCyan)
        if self.use_TTbar_MLL == False:                                                                                                                            
            self.files_1F['TTbar']          =file_object(self.str_uncert+'hist_TTbar2L_all_1F','TTbar'                      , 9511116.0,   self.Xsection['TTbar']          ,     ROOT.kYellow)
        else:                                                                                                                                                
            self.files_1F['TTbar']          =file_object(self.str_uncert+'hist_TTbar2L_500_1F','TTbar'                      , 9511116,     self.Xsection['TTbar']          ,     ROOT.kYellow)
            self.files_1F['TTbar_500_800']  =file_object(self.str_uncert+'hist_TTbar2L_500_800_1F','TTbar_500_800'          , 755907,      self.Xsection['TTbar_500_800']  ,     ROOT.kYellow)
            self.files_1F['TTbar_800_1200'] =file_object(self.str_uncert+'hist_TTbar2L_800_1200_1F','TTbar_800_1200'        , 199636,      self.Xsection['TTbar_800_1200'] ,     ROOT.kYellow)
            self.files_1F['TTbar_1200_1800']=file_object(self.str_uncert+'hist_TTbar2L_1200_1800_1F','TTbar_1200_1800'      , 17507,       self.Xsection['TTbar_1200_1800'],     ROOT.kYellow)
            self.files_1F['TTbar_1800_Inf'] =file_object(self.str_uncert+'hist_TTbar2L_1800_Inf_1F','TTbar_1800_Inf'        , 953 ,        self.Xsection['TTbar_1800_Inf'] ,     ROOT.kYellow)
        self.files_1F['ST']                 =file_object(self.str_uncert+'hist_ST_1F','Single Top'                          , 4936387.0,   self.Xsection['ST']             ,     ROOT.kRed)
        self.files_1F['ST_anti']            =file_object(self.str_uncert+'hist_ST_anti_1F','ST_anti'                        , 5592819.0,   self.Xsection['ST_anti']        ,     ROOT.kRed)
        if self.use_WW_MLL == False:                                                                                                                           
            self.files_1F['WW']                 =file_object(self.str_uncert+'hist_WW_1F','Di-Boson'                        , 1973294.0,   self.Xsection['WW_inc']         ,     ROOT.kOrange)
        else:                                                                                                                              
            self.files_1F['WW']                 =file_object(self.str_uncert+'hist_WW2L_200_1F','Di-Boson'                  , 1973294.0,   self.Xsection['WW']             ,     ROOT.kOrange+2)
            self.files_1F['WW_200_600']         =file_object(self.str_uncert+'hist_WW2L_200_600_1F','WW2L_200_600'          , 7922808.0,   self.Xsection['WW_200_600']     ,     ROOT.kOrange+2)
            self.files_1F['WW_600_1200']        =file_object(self.str_uncert+'hist_WW2L_600_1200_1F','WW2L_600_1200'        , 2623154.0,   self.Xsection['WW_600_1200']    ,     ROOT.kOrange+2)
            self.files_1F['WW_1200_2500']       =file_object(self.str_uncert+'hist_WW2L_1200_2500_1F','WW2L_1200_2500'      , 161573.0,    self.Xsection['WW_1200_2500']   ,     ROOT.kOrange+2)
            self.files_1F['WW_2500_Inf']        =file_object(self.str_uncert+'hist_WW2L_2500_Inf_1F','WW2L_2500_Inf'        , 2349.0,      self.Xsection['WW_2500_Inf']    ,     ROOT.kOrange+2)
        self.files_1F['WZ_2L2Q']            =file_object(self.str_uncert+'hist_WZ_2L2Q_1F','WZ_2L2Q'                        , 16534558.0,  self.Xsection['WZ_2L2Q']        ,     ROOT.kMagenta)
        self.files_1F['WZ_3LNu']            =file_object(self.str_uncert+'hist_WZ_3LNu_1F','WZ_3LNu'                        , 965938.0,    self.Xsection['WZ_3LNu']        ,     ROOT.kMagenta)
        self.files_1F['ZZ_2L2Nu']           =file_object(self.str_uncert+'hist_ZZ_2L2Nu_1F','ZZ_2L2Nu'                      , 8733658.0,   self.Xsection['ZZ_2L2Nu']       ,     ROOT.kMagenta)
        self.files_1F['ZZ_2L2Q']            =file_object(self.str_uncert+'hist_ZZ_2L2Q_1F' ,'ZZ_2L2Q'                       , 17667929.0,  self.Xsection['ZZ_2L2Q']        ,     ROOT.kMagenta)
        self.files_1F['ZZ_4L']              =file_object(self.str_uncert+'hist_ZZ_4L_1F'   ,'ZZ_4L'                         , 15912322.0,  self.Xsection['ZZ_4L']          ,     ROOT.kMagenta)
        #self.files_1F['WZ']                 =file_object(self.str_uncert+'hist_WZ_1F','Di-Boson'                            , 3885000.0,  self.Xsection['WZ_inc']         ,     ROOT.kOrange)
        #self.files_1F['ZZ']                 =file_object(self.str_uncert+'hist_ZZ_1F','Di-Boson'                            , 1972000.0,  self.Xsection['ZZ_inc']         ,     ROOT.kOrange)

        self.files_1F['QCD']                =file_object('hist_data_FR2F_MiniAOD', 'QCD(data)'   ,self.data_lumi , 1                            ,     ROOT.kYellow-10)
    def get_lumi_normalized(self):
        self.hist_name=["h_mee_usual","h_mee_BB_usual","h_mee_BE_usual","h_mee_EE_usual","h_mee_all","h_mee_all_BB","h_mee_all_BE","h_mee_all_EE","h_mee_all_cumlative","h_mee_all_cumlative_BB","h_mee_all_cumlative_BE","h_mee_all_cumlative_EE","h_mee_all_sin","h_mee_all_BB_sin","h_mee_all_BE_sin","h_mee_all_EE_sin"]
        cum_log_hist=["h_mee_all_cumlative_v1","h_mee_all_cumlative_BB_v1","h_mee_all_cumlative_BE_v1","h_mee_all_cumlative_EE_v1"]
        #other_hist=["h_Ptll","h_Etall","h_Phill","h_led_Et","h_led_eta","h_led_phi","h_sub_Et","h_sub_eta","h_sub_phi","h_MET","h_MET_phi","h_MET_T1Txy","h_MET_phi_T1Txy","h_MET_SF_T1Txy","h_MET_Filter","h_Dphi_ll","h_Dphi_MET_Z","h_DR_ll","h_N_jet","h_N_bjet","h_HT_sys","h_Pt_sys","h_mee_Zpeak","h_mee_Zpeak_BB","h_mee_Zpeak_BE","h_mee_Zpeak_EE"]
        #other_hist=["h_pv_n","h_Ptll","h_Etall","h_Phill","h_led_Et","h_led_eta","h_led_phi","h_sub_Et","h_sub_eta","h_sub_phi","h_led_Et_AM","h_led_eta_AM","h_led_phi_AM","h_sub_Et_AM","h_sub_eta_AM","h_sub_phi_AM","h_MET","h_MET_phi","h_MET_T1Txy","h_MET_phi_T1Txy","h_MET_SF_T1Txy","h_MET_Filter","h_Dphi_ll","h_Dphi_MET_Z","h_DR_ll","h_N_jet","h_N_bjet","h_HT_sys","h_Pt_sys","h_mee_Zpeak","h_mee_Zpeak_BB","h_mee_Zpeak_BE","h_mee_Zpeak_EE"]
        other_hist=["h_pv_n","h_Ptll","h_Etall","h_Phill","h_led_Et","h_led_eta","h_led_phi","h_sub_Et","h_sub_eta","h_sub_phi","h_led_Et_AM","h_led_eta_AM","h_led_phi_AM","h_sub_Et_AM","h_sub_eta_AM","h_sub_phi_AM","h_Dphi_ll","h_DR_ll","h_mee_Zpeak","h_mee_Zpeak_BB","h_mee_Zpeak_BE","h_mee_Zpeak_EE"]
        rho_hist=['h_rho','h_rho_BB','h_rho_BE','h_rho_EE']
        other_cos_hist=["h_mee_cosp","h_mee_cosp_BB","h_mee_cosp_BE","h_mee_cosp_EE","h_mee_cosm","h_mee_cosm_BB","h_mee_cosm_BE","h_mee_cosm_EE","h_cos","h_cos_BB","h_cos_BE","h_cos_EE","h_cos_all_region"]
        #other_mee_hist=["h_mee_fine","h_mee_BB_fine","h_mee_BE_fine","h_mee_EE_fine","h_mee_cosp_fine","h_mee_cosp_BB_fine","h_mee_cosp_BE_fine","h_mee_cosp_EE_fine","h_mee_cosm_fine","h_mee_cosm_BB_fine","h_mee_cosm_BE_fine","h_mee_cosm_EE_fine","h_mee_cosp_all_fine","h_mee_cosm_all_fine"]
        other_mee_hist=["h_mee_fine","h_mee_BB_fine","h_mee_BE_fine","h_mee_EE_fine"]
        other_mee_hist_v1=["h_mee_cosp_usual","h_mee_cosp_BB_usual","h_mee_cosp_BE_usual","h_mee_cosp_EE_usual","h_mee_cosm_usual","h_mee_cosm_BB_usual","h_mee_cosm_BE_usual","h_mee_cosm_EE_usual"]
        heep_var_hist=["h_dPhiIn","h_Sieie","h_missingHits","h_dxyFirstPV","h_HOverE","h_E1x5OverE5x5","h_E2x5OverE5x5","h_isolEMHadDepth1","h_IsolPtTrks","h_EcalDriven","h_dEtaIn"]  
        self.hist_name.extend(cum_log_hist)   
        self.hist_name.extend(other_hist)   
        self.hist_name.extend(other_mee_hist)   
        #self.hist_name.extend(rho_hist)   
        #self.hist_name.extend(other_cos_hist)   
        #self.hist_name.extend(other_mee_hist_v1)   
        #self.hist_name.extend(heep_var_hist)   
        self.normalize_hist_name=['h_mee_Zpeak','h_mee_Zpeak_BB','h_mee_Zpeak_BE','h_mee_Zpeak_EE']
        for hname in self.normalize_hist_name:
            N_data=0
            N_mc  =0
            for ifile in self.files:
                if ifile=="data":
                    N_data=self.files[ifile].tfile.Get(hname).GetSumOfWeights()
                else:
                    scale=float(self.data_lumi/self.files[ifile].lumi)
                    #print "%s_%s"%(hname,ifile)
                    N_mc=N_mc + self.files[ifile].tfile.Get(hname).GetSumOfWeights()*scale
                    #print "done"
            print "%s, %s scale %f"%(self.sys_uncert, hname, float(N_data/N_mc))
            if self.sys_uncert == "normalization_scale_up":
                if "BB" in hname:
                    N_data=1.02*N_data
                elif ("BE" in hname) or ("EE" in hname):
                    N_data=1.04*N_data
                else:
                    N_data=1.02*N_data
            elif self.sys_uncert == "normalization_scale_down":
                if "BB" in hname:
                    N_data=0.98*N_data
                elif ("BE" in hname) or ("EE" in hname):
                    N_data=0.96*N_data
                else:
                    N_data=0.98*N_data
            elif self.sys_uncert == "lumi_scale_up":
                N_data=1.025*N_data
            elif self.sys_uncert == "lumi_scale_down":
                N_data=0.975*N_data
            ################
            #if True and ("energy_scale" in self.sys_uncert or "mass_scale" in self.sys_uncert or "pdf_scale" in self.sys_uncert):
            #if True and ("energy_scale" in self.sys_uncert or "mass_scale" in self.sys_uncert or "pdf_scale" in self.sys_uncert or "SF" in self.sys_uncert):
            if True and ("normalization" not in self.sys_uncert and "lumi" not in self.sys_uncert):


                ###############  2017 result, prefiring, NNPDF weight ################
                RunAll_scale   =0.894072
                RunAll_BB_scale=0.895773
                RunAll_BE_scale=0.889078
                RunAll_EE_scale=0.890076

                ###############  2017 result, prefiring, NNPDF weight for <120 and > 120 ################
                RunAll_scale   =0.895176
                RunAll_BB_scale=0.902379
                RunAll_BE_scale=0.874554
                RunAll_EE_scale=0.880073

                ###############  2017 result, prefiring, NNPDF weight for <120 and > 120, new FR ################
                RunAll_scale   =0.895176
                RunAll_BB_scale=0.902374
                RunAll_BE_scale=0.874569
                RunAll_EE_scale=0.880076



                ###############  2017 result, prefiring, NNPDF weight, NO PUW ################

                #RunAll_scale   =0.903620
                #RunAll_BB_scale=0.904552
                #RunAll_BE_scale=0.900873
                #RunAll_EE_scale=0.904673


                if "BB" in hname:
                    N_data=RunAll_BB_scale
                    N_mc  =1
                elif "BE" in hname:
                    N_data=RunAll_BE_scale
                    N_mc  =1
                elif "EE" in hname:
                    N_data=RunAll_EE_scale
                    N_mc  =1
                else:
                    N_data=RunAll_scale
                    N_mc  =1

            ################
            if "BB" in hname:
                self.normalized_lumi_BB =self.normalized_lumi_BB*float(N_data/N_mc) 
            elif "BE" in hname:
                self.normalized_lumi_BE =self.normalized_lumi_BE*float(N_data/N_mc) 
            elif "EE" in hname:
                self.normalized_lumi_EE =self.normalized_lumi_EE*float(N_data/N_mc) 
            else:
                self.normalized_lumi =self.normalized_lumi*float(N_data/N_mc)
    def get_jets_hist(self):
        #f_jets=ROOT.TFile("ntuples/sys_saved_hist/20190530_NewID/all/"+self.str_uncert+"hist_jets.root","RECREATE")
        #f_jets=ROOT.TFile("ntuples/sys_saved_hist/20190603_Et/all/"+self.str_uncert+"hist_jets.root","RECREATE")
        #f_jets=ROOT.TFile("ntuples/sys_saved_hist/2016/20190605/all/"+self.str_uncert+"hist_jets.root","RECREATE")
        #f_jets=ROOT.TFile("ntuples/sys_saved_hist/2016/20190605_pf/all/"+self.str_uncert+"hist_jets.root","RECREATE")
        #f_jets=ROOT.TFile("ntuples/sys_saved_hist/2016/20190605_pf_up/all/"+self.str_uncert+"hist_jets.root","RECREATE")
        #f_jets=ROOT.TFile("ntuples/sys_saved_hist/2016/20190605_pf_down/all/"+self.str_uncert+"hist_jets.root","RECREATE")
        #f_jets=ROOT.TFile("ntuples/sys_saved_hist/2016/20190614/all/"+self.str_uncert+"hist_jets.root","RECREATE")
        #f_jets=ROOT.TFile("ntuples/sys_saved_hist/2016/20190614_NoPW/all/"+self.str_uncert+"hist_jets.root","RECREATE")
        #f_jets=ROOT.TFile("ntuples/sys_saved_hist/2016/20190615_trigTurnOn/all/"+self.str_uncert+"hist_jets.root","RECREATE")
        #f_jets=ROOT.TFile("ntuples/sys_saved_hist/2016/20190615_trigTurnOn_NoPUW/all/"+self.str_uncert+"hist_jets.root","RECREATE")
        #f_jets=ROOT.TFile("ntuples/sys_saved_hist/2017/20190615/all/"+self.str_uncert+"hist_jets.root","RECREATE")
        #f_jets=ROOT.TFile("ntuples/sys_saved_hist/2017/20190615_noPUW/all/"+self.str_uncert+"hist_jets.root","RECREATE")
        #f_jets=ROOT.TFile("ntuples/sys_saved_hist/2017/20190623_GenM/all/"+self.str_uncert+"hist_jets.root","RECREATE")
        #f_jets=ROOT.TFile("ntuples/sys_saved_hist/2017/20190628_EENoTTW/all/"+self.str_uncert+"hist_jets.root","RECREATE")
        #f_jets=ROOT.TFile("ntuples/sys_saved_hist/2017/20190703_fr_MasScale/all/"+self.str_uncert+"hist_jets.root","RECREATE")
        f_jets=ROOT.TFile("ntuples/sys_saved_hist/2017/20190704_newBin/all/"+self.str_uncert+"hist_jets.root","RECREATE")
        for h_name in self.hist_name:
            if 'BB' in h_name:
                Lumi=self.normalized_lumi_BB
            elif 'BE' in h_name:
                Lumi=self.normalized_lumi_BE
            elif 'EE' in h_name:
                Lumi=self.normalized_lumi_EE
            else:
                Lumi=self.normalized_lumi
            if self.files_1F["data"].tfile.Get(h_name):
                h_data=self.files_1F["data"].tfile.Get(h_name).Clone('data_%s'%(h_name))
                h_jets=h_data.Clone(h_name)
                h_jets.Scale(0)
#                h_jets.Sumw2()
                for ifile in self.files_1F:
                    if "data" not in ifile:
                        if ifile == 'QCD':
                            h_jets.Add(self.files_1F[ifile].tfile.Get(h_name),-1) 
                        else:
                            h_jets.Add(self.files_1F[ifile].tfile.Get(h_name),-1*Lumi/self.files_1F[ifile].lumi) 
                for bin in range(1,h_jets.GetNbinsX()+1):
                    bin_value=h_data.GetBinContent(bin)+h_jets.GetBinContent(bin)
                    bin_error=math.sqrt(math.pow(h_data.GetBinError(bin),2) + math.pow(h_jets.GetBinError(bin),2))
                    if float(bin_value) < 0:#this means 1F<2F, so 1F all come from QCD, and 50% of 1F is QCD
                        #bin_value=0
                        #bin_error=0
                        bin_value=h_data.GetBinContent(bin)/2
                        bin_error=h_data.GetBinError(bin)/2
                    h_jets.SetBinContent(bin,float(bin_value))
                    h_jets.SetBinError(bin,float(bin_error))
                smooth_range_low=75
                smooth_range_up=105
                if do_Z_XS_measure and True:
                    smooth_range_low=80
                    smooth_range_up =118.9
                smooth_QCD=False
                if "mee"in h_name and "sin" not in h_name: smooth_QCD=True
                if smooth_QCD is True:
                    Xaxis = h_jets.GetXaxis()
                    bin_low = Xaxis.FindBin(smooth_range_low-1)
                    bin_up = Xaxis.FindBin(smooth_range_up+1)
                    bin_low_value=h_jets.GetBinContent(bin_low)
                    bin_up_value=h_jets.GetBinContent(bin_up)
                    region_events=(smooth_range_up-smooth_range_low)*(bin_low_value+bin_up_value)/2
                    h_QCD=self.files_1F['QCD'].tfile.Get(h_name).Clone('QCD_%s'%(h_name))        
#                    h_QCD.Sumw2()
                    QCD_bin_low_value=h_QCD.GetBinContent(bin_low)
                    QCD_bin_up_value=h_QCD.GetBinContent(bin_up)
                    QCD_region_events=0
                    for bin in range(1,h_QCD.GetNbinsX()+1):
                        mean_value= (h_QCD.GetXaxis().GetBinUpEdge(bin)+h_QCD.GetXaxis().GetBinLowEdge(bin))/2
                        if float(mean_value)>float(smooth_range_low) and float(mean_value)<float(smooth_range_up):
                            QCD_region_events=QCD_region_events+h_QCD.GetBinContent(bin)*h_QCD.GetBinWidth(bin)
                             
                    Scale = float(region_events/QCD_region_events)
                    h_QCD.Scale(Scale)
                    for bin in range(1,h_jets.GetNbinsX()+1):
                        mean_value= (h_jets.GetXaxis().GetBinUpEdge(bin)+h_jets.GetXaxis().GetBinLowEdge(bin))/2    
                        if float(mean_value)>float(smooth_range_low) and float(mean_value)<float(smooth_range_up):
                            h_jets.SetBinContent(bin,h_QCD.GetBinContent(bin))
                            h_jets.SetBinError(bin,h_QCD.GetBinError(bin))
                if self.sys_uncert == "bgk_Jets_scale_up"    : h_jets.Scale(1.5)
                elif self.sys_uncert == "bgk_Jets_scale_down": h_jets.Scale(0.5)        
                #Remove_error=True  ###### remove jet statistic uncertainty in mass plot 
                Remove_error=False  ##for bgk fit 
                if Remove_error:
                    for ibin in range(1,h_jets.GetNbinsX()+1):
                        h_jets.SetBinError(ibin,0)    
                f_jets.cd()
                h_jets.Write()
        f_jets.Close()
        self.files['Jets']     =file_object(self.str_uncert+'hist_jets' ,'Jets'            ,self.data_lumi,      1,           ROOT.kYellow+3)


    def get_all_hist(self):
        self.sample_hist={}
        for sname in self.files:     
            self.sample_hist[sname]=[] 
            for hname in self.hist_name:
               # print "get %s"%hname
                h_tmp=self.files[sname].tfile.Get(hname).Clone(sname+"_"+hname)
#                h_tmp.Sumw2()
                scale=1
                if "data" not in sname and "Jets" not in sname:
                    if 'BB' in hname:
                        Lumi=self.normalized_lumi_BB
                    elif 'BE' in hname:
                        Lumi=self.normalized_lumi_BE
                    elif 'EE' in hname:
                        Lumi=self.normalized_lumi_EE
                    else:
                        Lumi=self.normalized_lumi
                    scale=float(Lumi/self.files[sname].lumi)
                h_tmp.Scale(scale)
                #if sname == "Jets":print "%s, SUM %f"%(hname,self.files[sname].tfile.Get(hname).GetSumOfWeights())
                self.sample_hist[sname].append(h_tmp)
    def get_rebin_hist(self):
        if self.sys_uncert == "nominal":
            for hname in ["h_mee_all_sin","h_mee_all_BB_sin","h_mee_all_BE_sin","h_mee_all_EE_sin"]:
                h_tmp=ROOT.TH1D()
                first=True
                for sname in self.files:
                    if sname is "data":continue
                    for hist in self.sample_hist[sname]:
                        if hist.GetName().split(sname+"_")[-1] != hname: continue
                        if first:
                            h_tmp=hist.Clone("rebin_"+hname)
                            first=False
                        else:
                            h_tmp.Add(hist,1)
                self.rebin_hist.append(hist_rebin(self.rebin_min_event , h_tmp, h_tmp, False))
    def close_files(self):
    #    pass
        for sname in self.files:
            self.files[sname].tfile.Close()     
        for sname in self.files_1F:
            self.files_1F[sname].tfile.Close()     
############## BEGIN ############################
Draw_plots =True
Print_table=True
isSupplementStyle=False
F_Zprime=ROOT.TFile()
Add_Zprime=False
do_Z_XS_measure=False
if Add_Zprime:
    F_Zprime=ROOT.TFile("ntuples/sys_saved_hist/1013_Extend/hist_RSG_3000.root","read")

Luminosity=float(41500)
System_list=["nominal"]
#System_list.append("normalization_scale_up")
#System_list.append("normalization_scale_down")
#System_list.append("bgk_ttbar_scale_up")
#System_list.append("bgk_ttbar_scale_down")
#System_list.append("bgk_ZToTT_scale_up")
#System_list.append("bgk_ZToTT_scale_down")
#System_list.append("bgk_ww_scale_up")
#System_list.append("bgk_ww_scale_down")
#System_list.append("bgk_wz_scale_up")
#System_list.append("bgk_wz_scale_down")
#System_list.append("bgk_zz_scale_up")
#System_list.append("bgk_zz_scale_down")
#System_list.append("bgk_st_scale_up")
#System_list.append("bgk_st_scale_down")
#System_list.append("bgk_Jets_scale_up")
#System_list.append("bgk_Jets_scale_down")
########### Shape dependent#########################
#System_list.append("PU_scale_up"             )
#System_list.append("PU_scale_down"           )
#System_list.append("BB_mass_scale_up"  )
#System_list.append("BB_mass_scale_down")
#System_list.append("BE_mass_scale_up"  )
#System_list.append("BE_mass_scale_down")
#System_list.append("Barrel_SF_scale_up"  )
#System_list.append("Barrel_SF_scale_down")
#System_list.append("Endcap_SF_scale_up"  )
#System_list.append("Endcap_SF_scale_down")
#System_list.append("pf_scale_up"  )
#System_list.append("pf_scale_down")
#System_list.append("pdf_scale_up"  )
#System_list.append("pdf_scale_down")
###System_list.append("lumi_scale_up")   ##not used
###System_list.append("lumi_scale_down") ##not used


##################### not used ##################
#System_list.append("Barrel_energy_scale_up"  )
#System_list.append("Barrel_energy_scale_down")
#System_list.append("Endcap_energy_scale_up"  )
#System_list.append("Endcap_energy_scale_down")
#System_list.append("pdf_50_120_scale_up"      )
#System_list.append("pdf_50_120_scale_down"    )
#System_list.append("pdf_120_200_scale_up"     )
#System_list.append("pdf_120_200_scale_down"   )
#System_list.append("pdf_200_400_scale_up"     )
#System_list.append("pdf_200_400_scale_down"   )
#System_list.append("pdf_400_800_scale_up"     )
#System_list.append("pdf_400_800_scale_down"   )
#System_list.append("pdf_800_1400_scale_up"    )
#System_list.append("pdf_800_1400_scale_down"  )
#System_list.append("pdf_1400_2300_scale_up"   )
#System_list.append("pdf_1400_2300_scale_down" )
#System_list.append("pdf_2300_3500_scale_up"   )
#System_list.append("pdf_2300_3500_scale_down" )
#System_list.append("pdf_3500_4500_scale_up"   )
#System_list.append("pdf_3500_4500_scale_down" )
#System_list.append("pdf_4500_6000_scale_up"   )
#System_list.append("pdf_4500_6000_scale_down" )
#System_list.append("pdf_6000_Inf_scale_up"    )
#System_list.append("pdf_6000_Inf_scale_down"  )
########################################

remove_Energy_scale_60_120=True

System_uncertainty={}
for nsys in System_list:
    System_uncertainty[nsys]=collcet_hist(nsys, True, True, True, nsys)
    #System_uncertainty[nsys]=collcet_hist(nsys, True, False, False, nsys)

all_hist={}

for nsys in System_uncertainty:
    System_uncertainty[nsys].get_input_file()
    System_uncertainty[nsys].get_lumi_normalized()
    System_uncertainty[nsys].get_jets_hist()
    System_uncertainty[nsys].get_all_hist()
    System_uncertainty[nsys].get_rebin_hist()
    all_hist[nsys]=System_uncertainty[nsys].sample_hist
    System_uncertainty[nsys].close_files()
#print all_hist

final_hist_name=['h_mee_usual','h_mee_BB_usual','h_mee_BE_usual','h_mee_EE_usual','h_mee_all','h_mee_all_BB','h_mee_all_BE','h_mee_all_EE','h_mee_all_cumlative','h_mee_all_cumlative_BB','h_mee_all_cumlative_BE','h_mee_all_cumlative_EE','h_mee_all_sin','h_mee_all_BB_sin','h_mee_all_BE_sin','h_mee_all_EE_sin'] 
final_cum_log_hist=["h_mee_all_cumlative_v1","h_mee_all_cumlative_BB_v1","h_mee_all_cumlative_BE_v1","h_mee_all_cumlative_EE_v1"]
final_other_hist=["h_pv_n","h_Ptll","h_Etall","h_Phill","h_led_Et","h_led_eta","h_led_phi","h_sub_Et","h_sub_eta","h_sub_phi","h_led_Et_AM","h_led_eta_AM","h_led_phi_AM","h_sub_Et_AM","h_sub_eta_AM","h_sub_phi_AM","h_Dphi_ll","h_DR_ll","h_mee_Zpeak","h_mee_Zpeak_BB","h_mee_Zpeak_BE","h_mee_Zpeak_EE"]
#final_other_hist=["h_pv_n","h_Ptll","h_Etall","h_Phill","h_led_Et","h_led_eta","h_led_phi","h_sub_Et","h_sub_eta","h_sub_phi","h_led_Et_AM","h_led_eta_AM","h_led_phi_AM","h_sub_Et_AM","h_sub_eta_AM","h_sub_phi_AM","h_MET","h_MET_phi","h_MET_T1Txy","h_MET_phi_T1Txy","h_MET_SF_T1Txy","h_MET_Filter","h_Dphi_ll","h_Dphi_MET_Z","h_DR_ll","h_N_jet","h_N_bjet","h_HT_sys","h_Pt_sys","h_mee_Zpeak","h_mee_Zpeak_BB","h_mee_Zpeak_BE","h_mee_Zpeak_EE"]
final_rho_hist=['h_rho','h_rho_BB','h_rho_BE','h_rho_EE']
#final_other_hist=["h_Ptll","h_Etall","h_Phill","h_led_Et","h_led_eta","h_led_phi","h_sub_Et","h_sub_eta","h_sub_phi","h_MET","h_MET_phi","h_MET_T1Txy","h_MET_phi_T1Txy","h_MET_SF_T1Txy","h_MET_Filter","h_Dphi_ll","h_Dphi_MET_Z","h_DR_ll","h_N_jet","h_N_bjet","h_HT_sys","h_Pt_sys","h_mee_Zpeak","h_mee_Zpeak_BB","h_mee_Zpeak_BE","h_mee_Zpeak_EE"]
final_other_cos_hist=["h_mee_cosp","h_mee_cosp_BB","h_mee_cosp_BE","h_mee_cosp_EE","h_mee_cosm","h_mee_cosm_BB","h_mee_cosm_BE","h_mee_cosm_EE","h_cos","h_cos_BB","h_cos_BE","h_cos_EE","h_cos_all_region"]
#final_other_mee_hist=["h_mee_fine","h_mee_BB_fine","h_mee_BE_fine","h_mee_EE_fine","h_mee_cosp_fine","h_mee_cosp_BB_fine","h_mee_cosp_BE_fine","h_mee_cosp_EE_fine","h_mee_cosm_fine","h_mee_cosm_BB_fine","h_mee_cosm_BE_fine","h_mee_cosm_EE_fine","h_mee_cosp_all_fine","h_mee_cosm_all_fine"]
#final_other_mee_hist_v1=["h_mee_cosp_usual","h_mee_cosp_BB_usual","h_mee_cosp_BE_usual","h_mee_cosp_EE_usual","h_mee_cosm_usual","h_mee_cosm_BB_usual","h_mee_cosm_BE_usual","h_mee_cosm_EE_usual"]
final_other_mee_hist=["h_mee_fine","h_mee_BB_fine","h_mee_BE_fine","h_mee_EE_fine"]
final_heep_var_hist=["h_dPhiIn","h_Sieie","h_missingHits","h_dxyFirstPV","h_HOverE","h_E1x5OverE5x5","h_E2x5OverE5x5","h_isolEMHadDepth1","h_IsolPtTrks","h_EcalDriven","h_dEtaIn"]  
final_hist_name.extend(final_cum_log_hist)
final_hist_name.extend(final_other_hist)
#final_hist_name.extend(final_other_cos_hist)
final_hist_name.extend(final_other_mee_hist)
#final_hist_name.extend(final_other_mee_hist_v1)
#final_hist_name.extend(final_heep_var_hist)
#final_hist_name.extend(final_rho_hist)
#

hist_system={}
for hname in final_hist_name:
    hist_system[hname]={}
    for nsys in System_uncertainty:
        for hist in System_uncertainty["nominal"].sample_hist["ZToEE_50_120"]:
            if hist.GetName().split("ZToEE_50_120_")[-1] != hname: continue
            hist_system[hname][nsys]=[]
            total_hist=hist.Clone(hname+"_total")
            ZToEE_hist=hist.Clone(hname+"_ZToEE")
            ttbar_other_hist=hist.Clone(hname+"_ttbar_other")
            Jets_hist=hist.Clone(hname+"_Jets")
            if "cumlative" in hname:
                hist_cum=cumulate(hist, nsys+"_"+hist.GetName())
                total_hist      =hist_cum.Clone(hname+"_total")
                ZToEE_hist      =hist_cum.Clone(hname+"_ZToEE")
                ttbar_other_hist=hist_cum.Clone(hname+"_ttbar_other")
                Jets_hist       =hist_cum.Clone(hname+"_Jets")
            total_hist.Scale(0)
            ZToEE_hist.Scale(0)
            ttbar_other_hist.Scale(0)
            Jets_hist.Scale(0)
            for sname in System_uncertainty[nsys].sample_hist:
                if sname == "data":continue
                for hs in System_uncertainty[nsys].sample_hist[sname]:
                    if hs.GetName().split(sname+"_")[-1] != hname: continue
                    h_tmp=hs.Clone("%s_%s_tmp"%(hname,nsys))
                    if "cumlative" in hname:
                        h_tmp=cumulate(hs, nsys+"_"+hist.GetName()+"_tmp")
                    total_hist.Add(h_tmp,1)
                    if "Jets" not in sname and "ZToEE" not in sname:
                        ttbar_other_hist.Add(h_tmp,1)
                    if "ZToEE" in sname:
                        ZToEE_hist.Add(h_tmp,1)
                    if "Jets" in sname:
                        Jets_hist.Add(h_tmp,1)
           ################### Rebin ####################
            if hname in ["h_mee_all_sin"]:
                hist_system[hname][nsys].append(hist_rebin(System_uncertainty["nominal"].rebin_min_event, total_hist      , System_uncertainty["nominal"].rebin_hist[0], True))
                hist_system[hname][nsys].append(hist_rebin(System_uncertainty["nominal"].rebin_min_event, ZToEE_hist      , System_uncertainty["nominal"].rebin_hist[0], True))
                hist_system[hname][nsys].append(hist_rebin(System_uncertainty["nominal"].rebin_min_event, ttbar_other_hist, System_uncertainty["nominal"].rebin_hist[0], True))
                hist_system[hname][nsys].append(hist_rebin(System_uncertainty["nominal"].rebin_min_event, Jets_hist       , System_uncertainty["nominal"].rebin_hist[0], True))
            elif hname in ["h_mee_all_BB_sin"]:
                hist_system[hname][nsys].append(hist_rebin(System_uncertainty["nominal"].rebin_min_event, total_hist      , System_uncertainty["nominal"].rebin_hist[1], True))
                hist_system[hname][nsys].append(hist_rebin(System_uncertainty["nominal"].rebin_min_event, ZToEE_hist      , System_uncertainty["nominal"].rebin_hist[1], True))
                hist_system[hname][nsys].append(hist_rebin(System_uncertainty["nominal"].rebin_min_event, ttbar_other_hist, System_uncertainty["nominal"].rebin_hist[1], True))
                hist_system[hname][nsys].append(hist_rebin(System_uncertainty["nominal"].rebin_min_event, Jets_hist       , System_uncertainty["nominal"].rebin_hist[1], True))
            elif hname in ["h_mee_all_BE_sin"]:
                hist_system[hname][nsys].append(hist_rebin(System_uncertainty["nominal"].rebin_min_event, total_hist      , System_uncertainty["nominal"].rebin_hist[2], True))
                hist_system[hname][nsys].append(hist_rebin(System_uncertainty["nominal"].rebin_min_event, ZToEE_hist      , System_uncertainty["nominal"].rebin_hist[2], True))
                hist_system[hname][nsys].append(hist_rebin(System_uncertainty["nominal"].rebin_min_event, ttbar_other_hist, System_uncertainty["nominal"].rebin_hist[2], True))
                hist_system[hname][nsys].append(hist_rebin(System_uncertainty["nominal"].rebin_min_event, Jets_hist       , System_uncertainty["nominal"].rebin_hist[2], True))
            elif hname in ["h_mee_all_EE_sin"]:
                hist_system[hname][nsys].append(hist_rebin(System_uncertainty["nominal"].rebin_min_event, total_hist      , System_uncertainty["nominal"].rebin_hist[3], True))
                hist_system[hname][nsys].append(hist_rebin(System_uncertainty["nominal"].rebin_min_event, ZToEE_hist      , System_uncertainty["nominal"].rebin_hist[3], True))
                hist_system[hname][nsys].append(hist_rebin(System_uncertainty["nominal"].rebin_min_event, ttbar_other_hist, System_uncertainty["nominal"].rebin_hist[3], True))
                hist_system[hname][nsys].append(hist_rebin(System_uncertainty["nominal"].rebin_min_event, Jets_hist       , System_uncertainty["nominal"].rebin_hist[3], True))
            ##################
            else:
                hist_system[hname][nsys].append(total_hist)             
                hist_system[hname][nsys].append(ZToEE_hist)             
                hist_system[hname][nsys].append(ttbar_other_hist)             
                hist_system[hname][nsys].append(Jets_hist)             
            
#                canvas = ROOT.TCanvas('canvas','',100,100,1000,1000)
#                canvas.cd()
#                canvas.SetLogy()
#                canvas.SetLogx()
#                tmp_total_hist=hist_rebin(10, total_hist      , System_uncertainty["nominal"].rebin_hist[3], True)
#                hist_system[hname][nsys][0].Draw()
#                canvas.Print('./test.png')    
#                del canvas
#                gc.collect()

total_system_err={}
for hname in final_hist_name:
    total_system_err[hname]={}
    total_system_err[hname]["bkg_all"]=[]
    total_system_err[hname]["bkg_ZToEE"]=[]
    total_system_err[hname]["bkg_ttbar_other"]=[]
    total_system_err[hname]["bkg_Jets"]=[]
    h_tot_down        =hist_system[hname]["nominal"][0].Clone(hname+"_system_tot_down")
    h_tot_up          =hist_system[hname]["nominal"][0].Clone(hname+"_system_tot_up")
    h_ZToEE_down      =hist_system[hname]["nominal"][0].Clone(hname+"_system_ZToEE_down")
    h_ZToEE_up        =hist_system[hname]["nominal"][0].Clone(hname+"_system_ZToEE_up")
    h_ttbar_other_down=hist_system[hname]["nominal"][0].Clone(hname+"_system_ttbar_other_down")
    h_ttbar_other_up  =hist_system[hname]["nominal"][0].Clone(hname+"_system_ttbar_other_up")
    h_Jets_down       =hist_system[hname]["nominal"][0].Clone(hname+"_system_Jets_down")
    h_Jets_up         =hist_system[hname]["nominal"][0].Clone(hname+"_system_Jets_up")
    h_tot_down        .Scale(0)
    h_tot_up          .Scale(0)
    h_ZToEE_down      .Scale(0)
    h_ZToEE_up        .Scale(0)
    h_ttbar_other_down.Scale(0)
    h_ttbar_other_up  .Scale(0)
    h_Jets_down       .Scale(0)
    h_Jets_up         .Scale(0)
    h_tot_nominal        =hist_system[hname]["nominal"][0].Clone(hname+"_nominal_tot")
    h_ZToEE_nominal      =hist_system[hname]["nominal"][1].Clone(hname+"_nominal_ZToEE")
    h_ttbar_other_nominal=hist_system[hname]["nominal"][2].Clone(hname+"_nominal_ttbar_other")
    h_Jets_nominal       =hist_system[hname]["nominal"][3].Clone(hname+"_nominal_Jets")
    for nsys in hist_system[hname]:
        if nsys == "nominal":continue
        for ibin in range(1,h_tot_nominal.GetNbinsX()+1):
            if remove_Energy_scale_60_120 and "mee" in hname and ("energy_scale" in nsys or "mass_scale" in nsys):
                if 60 < float(h_tot_nominal.GetBinLowEdge(ibin)) and float(h_tot_nominal.GetBinLowEdge(ibin)) < 120:continue
                if 60 < float(h_tot_nominal.GetBinLowEdge(ibin)+h_tot_nominal.GetBinWidth(ibin)) and float(h_tot_nominal.GetBinLowEdge(ibin)+h_tot_nominal.GetBinWidth(ibin)) < 120:continue
            total_tmp      =hist_system[hname][nsys][0].GetBinContent(ibin)-h_tot_nominal.GetBinContent(ibin)
            ZToEE_tmp      =hist_system[hname][nsys][1].GetBinContent(ibin)-h_ZToEE_nominal.GetBinContent(ibin)
            ttbar_other_tmp=hist_system[hname][nsys][2].GetBinContent(ibin)-h_ttbar_other_nominal.GetBinContent(ibin)
            Jets_tmp       =hist_system[hname][nsys][3].GetBinContent(ibin)-h_Jets_nominal.GetBinContent(ibin)
            if( total_tmp>0):
                value_tmp=math.sqrt(math.pow(h_tot_up.GetBinContent(ibin),2)+math.pow(total_tmp,2))
                h_tot_up.SetBinContent(ibin,value_tmp)
            else:
                value_tmp=math.sqrt(math.pow(h_tot_down.GetBinContent(ibin),2)+math.pow(total_tmp,2))
                h_tot_down.SetBinContent(ibin,value_tmp)
            if( ZToEE_tmp>0):
                value_tmp=math.sqrt(math.pow(h_ZToEE_up.GetBinContent(ibin),2)+math.pow(ZToEE_tmp,2))
                h_ZToEE_up.SetBinContent(ibin,value_tmp)
            else:
                value_tmp=math.sqrt(math.pow(h_ZToEE_down.GetBinContent(ibin),2)+math.pow(ZToEE_tmp,2))
                h_ZToEE_down.SetBinContent(ibin,value_tmp)
            if( ttbar_other_tmp>0):
                value_tmp=math.sqrt(math.pow(h_ttbar_other_up.GetBinContent(ibin),2)+math.pow(ttbar_other_tmp,2))
                h_ttbar_other_up.SetBinContent(ibin,value_tmp)
            else:
                value_tmp=math.sqrt(math.pow(h_ttbar_other_down.GetBinContent(ibin),2)+math.pow(ttbar_other_tmp,2))
                h_ttbar_other_down.SetBinContent(ibin,value_tmp)
            if( Jets_tmp>0):
                value_tmp=math.sqrt(math.pow(h_Jets_up.GetBinContent(ibin),2)+math.pow(Jets_tmp,2))
                h_Jets_up.SetBinContent(ibin,value_tmp)
            else:
                value_tmp=math.sqrt(math.pow(h_Jets_down.GetBinContent(ibin),2)+math.pow(Jets_tmp,2))
                h_Jets_down.SetBinContent(ibin,value_tmp)
    total_system_err[hname]["bkg_all"].append(h_tot_down) 
    total_system_err[hname]["bkg_all"].append(h_tot_up) 
    total_system_err[hname]["bkg_ZToEE"].append(h_ZToEE_down) 
    total_system_err[hname]["bkg_ZToEE"].append(h_ZToEE_up) 
    total_system_err[hname]["bkg_ttbar_other"].append(h_ttbar_other_down) 
    total_system_err[hname]["bkg_ttbar_other"].append(h_ttbar_other_up) 
    total_system_err[hname]["bkg_Jets"].append(h_Jets_down) 
    total_system_err[hname]["bkg_Jets"].append(h_Jets_up) 
    ############## make the system uncertainty smooth for m<120###################
    #if hname in ['h_mee_all','h_mee_all_BB','h_mee_all_BE','h_mee_all_cumlative','h_mee_all_cumlative_BB','h_mee_all_cumlative_BE',"h_mee_cosp","h_mee_cosp_BB","h_mee_cosp_BE","h_mee_cosm","h_mee_cosm_BB","h_mee_cosm_BE"]:
    if hname in ['h_mee_all','h_mee_all_BB','h_mee_all_BE','h_mee_all_cumlative','h_mee_all_cumlative_BB','h_mee_all_cumlative_BE']:
        for ibin in range(1,total_system_err[hname]["bkg_all"][0].GetNbinsX()+1):
            tmp_mean=total_system_err[hname]["bkg_all"][0].GetBinLowEdge(ibin)+0.5*total_system_err[hname]["bkg_all"][0].GetBinWidth(ibin)
            if tmp_mean<120:
                tmp_scale=1
                if "BB" in hname:tmp_scale=1.5
                elif "BE" in hname:tmp_scale=1.2
                else:tmp_scale=1.3
                if hname =='h_mee_all_cumlative_BB':tmp_scale=2.5
                total_system_err[hname]["bkg_all"][0].SetBinContent(ibin,tmp_scale*total_system_err[hname]["bkg_all"][0].GetBinContent(ibin))
                total_system_err[hname]["bkg_all"][1].SetBinContent(ibin,tmp_scale*total_system_err[hname]["bkg_all"][1].GetBinContent(ibin))
            else:## remove spike
                if hist_system[hname]["nominal"][0].GetBinContent(ibin) == 0: continue
                if "BB" in hname:
                    if math.fabs(total_system_err[hname]["bkg_all"][0].GetBinContent(ibin)/hist_system[hname]["nominal"][0].GetBinContent(ibin))>0.1:
                        total_system_err[hname]["bkg_all"][0].SetBinContent(ibin,(6.65e-2+3.45e-5*tmp_mean)*hist_system[hname]["nominal"][0].GetBinContent(ibin))
                    if math.fabs(total_system_err[hname]["bkg_all"][1].GetBinContent(ibin)/hist_system[hname]["nominal"][0].GetBinContent(ibin))>0.1:
                        total_system_err[hname]["bkg_all"][1].SetBinContent(ibin,(6.65e-2+3.45e-5*tmp_mean)*hist_system[hname]["nominal"][0].GetBinContent(ibin))
                elif "BE" in hname:
                    if math.fabs(total_system_err[hname]["bkg_all"][0].GetBinContent(ibin)/hist_system[hname]["nominal"][0].GetBinContent(ibin))>0.1:
                        total_system_err[hname]["bkg_all"][0].SetBinContent(ibin,(4.7e-2+3e-5*tmp_mean)*hist_system[hname]["nominal"][0].GetBinContent(ibin))
                    if math.fabs(total_system_err[hname]["bkg_all"][1].GetBinContent(ibin)/hist_system[hname]["nominal"][0].GetBinContent(ibin))>0.1:
                        total_system_err[hname]["bkg_all"][1].SetBinContent(ibin,(4.7e-2+3e-5*tmp_mean)*hist_system[hname]["nominal"][0].GetBinContent(ibin))
                else:
                    if math.fabs(total_system_err[hname]["bkg_all"][0].GetBinContent(ibin)/hist_system[hname]["nominal"][0].GetBinContent(ibin))>0.1:
                        total_system_err[hname]["bkg_all"][0].SetBinContent(ibin,(4.7e-2+3e-5*tmp_mean)*hist_system[hname]["nominal"][0].GetBinContent(ibin))
                    if math.fabs(total_system_err[hname]["bkg_all"][1].GetBinContent(ibin)/hist_system[hname]["nominal"][0].GetBinContent(ibin))>0.1:
                        total_system_err[hname]["bkg_all"][1].SetBinContent(ibin,(4.7e-2+3e-5*tmp_mean)*hist_system[hname]["nominal"][0].GetBinContent(ibin))
        if "cumlative" not in hname:
            Xaxis_tmp=total_system_err[hname]["bkg_all"][0].GetXaxis()
            bin_tmp=Xaxis_tmp.FindBin(119)
            value_down=total_system_err[hname]["bkg_all"][0].GetBinContent(bin_tmp)
            value_up  =total_system_err[hname]["bkg_all"][1].GetBinContent(bin_tmp)
            smooth_hist(total_system_err[hname]["bkg_all"][0],119,131, value_down)
            smooth_hist(total_system_err[hname]["bkg_all"][1],119,131, value_up  )


total_hist={}
ttbar_other_hist={}
ZToEE_hist={}
Jets_hist={}
for hname in final_hist_name:
    for hist in System_uncertainty["nominal"].sample_hist["ZToEE_50_120"]:
        if hist.GetName().split("ZToEE_50_120_")[-1] != hname: continue
        total_hist[hname]      =hist_system[hname]["nominal"][0].Clone(hname)
        ZToEE_hist[hname]      =hist_system[hname]["nominal"][1].Clone(hname)
        #ZToEE_hist[hname]      =hist_system[hname]["BB_mass_scale_down"][1].Clone(hname)
        ttbar_other_hist[hname]=hist_system[hname]["nominal"][2].Clone(hname)
        Jets_hist[hname]       =hist_system[hname]["nominal"][3].Clone(hname)

f_out=ROOT.TFile("./hist_out.root","UPDATE")
for hname in final_hist_name:
    for hist in System_uncertainty["nominal"].sample_hist["ZToEE_50_120"]:
        if hist.GetName().split("ZToEE_50_120_")[-1] != hname: continue
        #h_mc_out=hist.Clone("ZToEE_50_120_"+hname)
        #h_mc_out=ZToEE_hist[hname].Clone("nominal_"+hname)
        h_mc_out=ZToEE_hist[hname].Clone("BB_mass_scale_down_"+hname)
        #h_mc_out=ZToEE_hist[hname].Clone("Zmatch_mc_"+hname)
        #h_mc_out=Jets_hist[hname].Clone("Jets_"+hname)
    #h_mc_out=ZToEE_hist[hname].Clone("Endcap_energy_scale_down_mc_"+hname)
    #h_mc_out=ZToEE_hist[hname].Clone("Endcap_energy_scale_up_mc_"+hname)
    #h_mc_out=ZToEE_hist[hname].Clone("Barrel_energy_scale_up_mc_"+hname)
    #h_mc_out=ZToEE_hist[hname].Clone("Barrel_energy_scale_down_mc_"+hname)
    #h_mc_out=total_hist[hname].Clone("nominal_mc_"+hname)
    #h_mc_out=total_hist[hname].Clone("Barrel_energy_scale_up_mc_"+hname)
    #h_mc_out=total_hist[hname].Clone("Barrel_energy_scale_down_mc_"+hname)
    #h_mc_out=total_hist[hname].Clone("Endcap_energy_scale_up_mc_"+hname)
    #h_mc_out=total_hist[hname].Clone("Endcap_energy_scale_down_mc_"+hname)
    #h_mc_out=total_hist[hname].Clone("BB_mass_scale_up_mc_"+hname)
    
        f_out.cd()
        h_mc_out.Write("",ROOT.TObject.kOverwrite)
f_out.Close()
 
#
#### For ploting #########
    
if Draw_plots:
    print "begin draw plots"               
    date='20190605'
    dir_out = './sys_plots'
    ASF_dict={}
    for hname in final_hist_name:
        Set_and_Draw(date, dir_out, hname, System_uncertainty, total_hist, ttbar_other_hist, ZToEE_hist, Jets_hist, ASF_dict)
    print ASF_dict
#    Draw_ASF(ASF_dict)
    print "end draw plots"               

########## For print event table ###################
if Print_table:
    print "begin event table"               
    #table_hist_name=['h_mee_usual','h_mee_BB_usual','h_mee_BE_usual','h_mee_EE_usual']
    #table_hist_name=['h_mee_usual']
    #table_hist_name=['h_mee_BB_usual']
    #table_hist_name=['h_mee_BE_usual']
    for tmp_table_hist_name in ['h_mee_usual','h_mee_BB_usual','h_mee_BE_usual']:
        print "########## %s ##############"%(tmp_table_hist_name)
        table_hist_name=[] 
        table_hist_name.append(tmp_table_hist_name)
        table={}
        for hname in table_hist_name:
            table[hname]={}
            for nsys in System_uncertainty:
                table[hname][nsys]=[]
                print "FOR %s , %s "%(hname,nsys)               
                hist_list=table_hist(hname, nsys, System_uncertainty) 
                table[hname][nsys].append(hist_list[0])        
                table[hname][nsys].append(hist_list[1])        
                table[hname][nsys].append(hist_list[2])        
                table[hname][nsys].append(hist_list[3])    
        print "end event table"               
               # for hist in System_uncertainty[nsys].sample_hist["data"]:
               #     if hist.GetName().split("data_")[-1] != hname: continue
               #     bgk_all        =hist.Clone(hname+nsys+"all")
               #     bgk_ZToEE      =hist.Clone(hname+nsys+"ZtoEE")
               #     bgk_ttbar_other=hist.Clone(hname+nsys+"ttbar_other")
               #     bgk_Jets       =hist.Clone(hname+nsys+"Jets")
               #     bgk_all        .Scale(0)
               #     bgk_ZToEE      .Scale(0)
               #     bgk_ttbar_other.Scale(0)
               #     bgk_Jets       .Scale(0)
               #     for sname in System_uncertainty[nsys].sample_hist:
               #         if sname == "data":continue
               #         for hs in System_uncertainty[nsys].sample_hist[sname]:
               #             if hs.GetName().split(sname+"_")[-1] != hname: continue
               #             print "for %s,  %s "%(sname,hs.GetName())               
               #             bgk_all.Add(hs,1)
               #             if "Jets" not in sname and "ZToEE" not in sname:
               #                 bgk_ttbar_other.Add(hs,1)
               #             if "ZToEE" in sname:
               #                 bgk_ZToEE.Add(hs,1)
               #             if "Jets" in sname:
               #                 bgk_Jets.Add(hs,1)
               #     table[hname][nsys].append(bgk_all)        
               #     table[hname][nsys].append(bgk_ZToEE)        
               #     table[hname][nsys].append(bgk_ttbar_other)        
               #     table[hname][nsys].append(bgk_Jets)    
               #     print "append %s,  %s "%(hname,nsys)               
####    #############    print table 
        #System_error={"nominal":{"60-120":[1,2,3,4]}}
        System_error={}
        #Mass_range_list=[[60,120],[120,400],[400,600],[600,900],[900,1300],[1300,1800],[1800,2800],[2800,6000],[60,6000]]#for event list in different mass range.
        #Mass_range_list=[[60,120],[120,400],[400,600],[600,900],[900,1300],[1300,1800],[1800,2800],[2800,6000],[60,6000],[150,6000],[200,6000]]#for event list in different mass range.
        Mass_range_list=[[60,120],[120,400],[400,600],[600,900],[900,1300],[1300,1800],[1800,6000]]#for paper.
        Sys_list=System_list
        for hname in table:
            print "%-25s:"%(hname),
            for im in Mass_range_list:
                print "| %d-%d %-5s"%(im[0],im[1]," "),
            print "\n"
            for hist in System_uncertainty["nominal"].sample_hist["data"]:
                if hist.GetName().split("data_")[-1] != hname : continue
                hist_data=hist.Clone("data_"+hname)#for data
                Xaxis=hist_data.GetXaxis()
                err =ROOT.Double(0)
                print "data:",
                for im in Mass_range_list:
                    print "| %.3f +- %.3f "%(hist_data.IntegralAndError(Xaxis.FindBin(im[0]+0.01),Xaxis.FindBin(im[1]-0.01),err),err),       
                print "\n"
 
                for nsys in Sys_list:
                    if nsys in table[hname]:
                        System_error[nsys]={}
                        hist_all=table[hname][nsys][0]#bkg_all
                        hist_ZToEE=table[hname][nsys][1]#bgk_ZToEE
                        hist_ttbar=table[hname][nsys][2]#bgk_ttbar
                        hist_jet  =table[hname][nsys][3]#bgk_jet
                        nominal_hist_all=table[hname]["nominal"][0]#bkg_all
                        nominal_hist_ZToEE=table[hname]["nominal"][1]#bkg_ZToEE
                        nominal_hist_ttbar=table[hname]["nominal"][2]#bkg_ttbar
                        nominal_hist_jet  =table[hname]["nominal"][3]#bkg_jet
                        print "%-25s:"%(nsys),
                        for im in Mass_range_list:
                            diff_all  =hist_all.IntegralAndError(Xaxis.FindBin(im[0]+0.01),Xaxis.FindBin(im[1]-0.01),err)-nominal_hist_all.IntegralAndError(Xaxis.FindBin(im[0]+0.01),Xaxis.FindBin(im[1]-0.01),err)
                            diff_ZToEE=hist_ZToEE.IntegralAndError(Xaxis.FindBin(im[0]+0.01),Xaxis.FindBin(im[1]-0.01),err)-nominal_hist_ZToEE.IntegralAndError(Xaxis.FindBin(im[0]+0.01),Xaxis.FindBin(im[1]-0.01),err)
                            diff_ttabr=hist_ttbar.IntegralAndError(Xaxis.FindBin(im[0]+0.01),Xaxis.FindBin(im[1]-0.01),err)-nominal_hist_ttbar.IntegralAndError(Xaxis.FindBin(im[0]+0.01),Xaxis.FindBin(im[1]-0.01),err)
                            diff_jet  =hist_jet.IntegralAndError(Xaxis.FindBin(im[0]+0.01),Xaxis.FindBin(im[1]-0.01),err)-nominal_hist_jet.IntegralAndError(Xaxis.FindBin(im[0]+0.01),Xaxis.FindBin(im[1]-0.01),err)
                            if(nsys=="nominal"):print "| %.3f +- %.3f "%(hist_all.IntegralAndError(Xaxis.FindBin(im[0]+0.01),Xaxis.FindBin(im[1]-0.01),err),err),       
                            else :
                                print "| %-+15.3f"%(diff_all),       
                            str_mass=str(im[0])+"_"+str(im[1])
                            System_error[nsys][str_mass]=[diff_all,diff_ZToEE,diff_ttabr,diff_jet]
                        print "\n"
#        print System_error
####    ### For combine some uncertainty###########
        combine_list=["normalization","lumi","pdf","mass","PU","bgk","SF","pf","total"]
        combine_err_scale_up  ={}
        combine_err_scale_down={}
        for ic in combine_list:
            combine_err_scale_up  [ic]={}
            combine_err_scale_down[ic]={}
            first=True
            for nsys in System_error:
                if ic in nsys or "total" in ic:
                    for rmass in Mass_range_list:
                        str_mass=str(rmass[0])+"_"+str(rmass[1])
                        if first:
                            combine_err_scale_up  [ic][str_mass]=0
                            combine_err_scale_down[ic][str_mass]=0
                        if System_error[nsys][str_mass][0] > 0 : combine_err_scale_up  [ic][str_mass]=math.sqrt(math.pow(combine_err_scale_up  [ic][str_mass],2)+math.pow(System_error[nsys][str_mass][0],2)) 
                        else                                   : combine_err_scale_down[ic][str_mass]=math.sqrt(math.pow(combine_err_scale_down[ic][str_mass],2)+math.pow(System_error[nsys][str_mass][0],2)) 
                    first=False
        print "combine some uncertainty:"
        for hname in table:
            for hist in System_uncertainty["nominal"].sample_hist["data"]:
                if hist.GetName().split("data_")[-1] != hname : continue
                hist_tmp=hist.Clone("tmp_data_"+hname)
                Xaxis=hist_tmp.GetXaxis()
                err =ROOT.Double(0)
                nominal_hist_all=table[hname]["nominal"][0]#bkg_all
                print "%-25s:"%(hname),
                for im in Mass_range_list:
                    print "| %d-%d %-5s"%(im[0],im[1]," "),
                for ic in combine_list:
                    do_print=False
                    for nsys in System_list:
                        if ic in nsys or "total" in ic:
                            do_print=True
                            break
                    if do_print==False: continue 
                    print "\n"
                    print "%-25s:"%(ic+"_scale_up"),
                    for im in Mass_range_list:
                        nominal_value  =nominal_hist_all.IntegralAndError(Xaxis.FindBin(im[0]+0.01),Xaxis.FindBin(im[1]-0.01),err)
                        str_mass=str(im[0])+"_"+str(im[1])
                        #print "| %.2f  %-5s"%(combine_err_scale_up  [ic][str_mass]," "),
                        print "| %.3f%%  %-5s"%(100*combine_err_scale_up  [ic][str_mass]/nominal_value," "),
                    print "\n"
                    print "%-25s:"%(ic+"_scale_down"),
                    for im in Mass_range_list:
                        nominal_value  =nominal_hist_all.IntegralAndError(Xaxis.FindBin(im[0]+0.01),Xaxis.FindBin(im[1]-0.01),err)
                        str_mass=str(im[0])+"_"+str(im[1])
                        #print "| %.2f  %-5s"%(combine_err_scale_down  [ic][str_mass]," "),
                        print "| %.3f%%  %-5s"%(100*combine_err_scale_down  [ic][str_mass]/nominal_value," "),
        print "\n"
        print "------------------------"
####    ####For final system uncertainty###########    
        final_sys={}
        for rmass in Mass_range_list:
            str_mass=str(rmass[0])+"_"+str(rmass[1])
            final_sys[str_mass]=[]
            sys_all_U=0
            sys_all_L=0
            sys_ZToEE_U=0
            sys_ZToEE_L=0
            sys_ttbar_U=0
            sys_ttbar_L=0
            sys_jet_U=0
            sys_jet_L=0
            for nsys in System_error:
                if System_error[nsys][str_mass][0]>0:sys_all_U  =math.sqrt(math.pow(sys_all_U  ,2)+math.pow(System_error[nsys][str_mass][0],2))
                else                                :sys_all_L  =math.sqrt(math.pow(sys_all_L  ,2)+math.pow(System_error[nsys][str_mass][0],2))
                if System_error[nsys][str_mass][1]>0:sys_ZToEE_U=math.sqrt(math.pow(sys_ZToEE_U,2)+math.pow(System_error[nsys][str_mass][1],2))
                else                                :sys_ZToEE_L=math.sqrt(math.pow(sys_ZToEE_L,2)+math.pow(System_error[nsys][str_mass][1],2))
                if System_error[nsys][str_mass][2]>0:sys_ttbar_U=math.sqrt(math.pow(sys_ttbar_U,2)+math.pow(System_error[nsys][str_mass][2],2))
                else                                :sys_ttbar_L=math.sqrt(math.pow(sys_ttbar_L,2)+math.pow(System_error[nsys][str_mass][2],2))
                if System_error[nsys][str_mass][3]>0:sys_jet_U  =math.sqrt(math.pow(sys_jet_U  ,2)+math.pow(System_error[nsys][str_mass][3],2))
                else                                :sys_jet_L  =math.sqrt(math.pow(sys_jet_L  ,2)+math.pow(System_error[nsys][str_mass][3],2))
            if sys_all_U > sys_all_L    :final_sys[str_mass].append(sys_all_U)
            else                        :final_sys[str_mass].append(sys_all_L)                   
            if sys_ZToEE_U > sys_ZToEE_L:final_sys[str_mass].append(sys_ZToEE_U)
            else                        :final_sys[str_mass].append(sys_ZToEE_L)                   
            if sys_ttbar_U > sys_ttbar_L:final_sys[str_mass].append(sys_ttbar_U)
            else                        :final_sys[str_mass].append(sys_ttbar_L)                   
            if sys_jet_U > sys_jet_L    :final_sys[str_mass].append(sys_jet_U)
            else                        :final_sys[str_mass].append(sys_jet_L)                   
#        print final_sys
####    ############# Print final event table ##################
        for hname in table:
            print "%s"%(hname)
            print " mass range      | data                      | total bkg                    | ZToEE                     | ttbar+ other prompt  | Jets"
            for rmass in Mass_range_list:
                for hist in System_uncertainty["nominal"].sample_hist["data"]:
                    if hist.GetName().split("data_")[-1] != hname : continue
                    hist_data=hist.Clone("data_"+hname)#for data
                    Xaxis=hist_data.GetXaxis()
                    bin_L=1
                    bin_U=hist_data.GetNbinsX()
                    if rmass[0] >  hist_data.GetBinLowEdge(1):bin_L=Xaxis.FindBin(rmass[0]+0.01)
                    if rmass[1] < (hist_data.GetBinLowEdge(bin_U)+hist_data.GetBinWidth(bin_U)):bin_U=Xaxis.FindBin(rmass[1]-0.01)
                    bkg_all_err        =ROOT.Double(0) 
                    bkg_ZToEE_err      =ROOT.Double(0) 
                    bkg_ttbar_other_err=ROOT.Double(0) 
                    bkg_Jets_err       =ROOT.Double(0) 
                    data_stat_err           =ROOT.Double(0) 
                    bkg_all_stat_err        =ROOT.Double(0) 
                    bkg_ZToEE_stat_err      =ROOT.Double(0) 
                    bkg_ttbar_other_stat_err=ROOT.Double(0) 
                    bkg_Jets_stat_err       =ROOT.Double(0) 
                    N_bkg_all          =table[hname]["nominal"][0].IntegralAndError(bin_L,bin_U,bkg_all_stat_err        )
                    N_bkg_ZToEE        =table[hname]["nominal"][1].IntegralAndError(bin_L,bin_U,bkg_ZToEE_stat_err      )
                    N_bkg_ttbar_other  =table[hname]["nominal"][2].IntegralAndError(bin_L,bin_U,bkg_ttbar_other_stat_err)
                    N_bkg_Jets         =table[hname]["nominal"][3].IntegralAndError(bin_L,bin_U,bkg_Jets_stat_err       )
                    str_mass=str(rmass[0])+"_"+str(rmass[1])
                    bkg_all_err        =math.sqrt(math.pow(bkg_all_stat_err        ,2)+math.pow(final_sys[str_mass][0],2))
                    bkg_ZToEE_err      =math.sqrt(math.pow(bkg_ZToEE_stat_err      ,2)+math.pow(final_sys[str_mass][1],2))
                    bkg_ttbar_other_err=math.sqrt(math.pow(bkg_ttbar_other_stat_err,2)+math.pow(final_sys[str_mass][2],2))
                    bkg_Jets_err       =math.sqrt(math.pow(bkg_Jets_stat_err       ,2)+math.pow(final_sys[str_mass][3],2))
                    N_data             =hist_data.IntegralAndError(bin_L,bin_U,data_stat_err) 
                   # N_data             =hist_data.Integral(bin_L,bin_U) 
                   # N_bkg_all        =table[hname]["nominal"][0].Integral(bin_L,bin_U)
                   # N_bkg_ZToEE      =table[hname]["nominal"][1].Integral(bin_L,bin_U)
                   # N_bkg_ttbar_other=table[hname]["nominal"][2].Integral(bin_L,bin_U)
                   # N_bkg_Jets       =table[hname]["nominal"][3].Integral(bin_L,bin_U)
                   # bkg_all_err         =get_err_range(table[hname]["nominal"][0],total_sys_err[hname]["bkg_all"][0],total_sys_err[hname]["bkg_all"][1],rmass[0],rmass[1])
                   # bkg_ZToEE_err       =get_err_range(table[hname]["nominal"][1],total_sys_err[hname]["bkg_ZToEE"][0],total_sys_err[hname]["bkg_ZToEE"][1],rmass[0],rmass[1])
                   # bkg_ttbar_other_err =get_err_range(table[hname]["nominal"][2],total_sys_err[hname]["bkg_ttbar_other"][0],total_sys_err[hname]["bkg_ttbar_other"][1],rmass[0],rmass[1])
                   # bkg_Jets_err        =get_err_range(table[hname]["nominal"][3],total_sys_err[hname]["bkg_Jets"][0],total_sys_err[hname]["bkg_Jets"][1],rmass[0],rmass[1])
                   # print " %-5d to %-5d | %-10d +- %-10.2f(stat.) | %-10.2f +- %-10.2f(stat.+syst.) | %-10.2f +- %-10.2f(stat.+syst.) | %-10.2f +- %-10.2f(stat.+syst.) | %-10.2f +- %-10.2f(stat.+syst.)"%(rmass[0],rmass[1],N_data,data_stat_err,N_bkg_all,bkg_all_err,N_bkg_ZToEE,bkg_ZToEE_err,N_bkg_ttbar_other,bkg_ttbar_other_err,N_bkg_Jets,bkg_Jets_err)
                   # print " %-5d to %-5d | %-10d +- %-10.2f(stat.) | %-10.2f +- %-10.2f(stat.)       | %-10.2f +- %-10.2f(stat.)       | %-10.2f +- %-10.2f(stat.)       | %-10.2f +- %-10.2f(stat.)"%(rmass[0],rmass[1],N_data,data_stat_err,N_bkg_all,bkg_all_stat_err,N_bkg_ZToEE,bkg_ZToEE_stat_err,N_bkg_ttbar_other,bkg_ttbar_other_stat_err,N_bkg_Jets,bkg_Jets_stat_err)
                  #  print " %-5d to %-5d | %-10d +- %-10.2f(stat.) | %-10.2f +- %-10.2f(stat.+syst.) | %-10.2f +- %-10.2f(stat.)       | %-10.2f +- %-10.2f(stat.)       | %-10.2f +- %-10.2f(stat.)"%(rmass[0],rmass[1],N_data,data_stat_err,N_bkg_all,bkg_all_err,N_bkg_ZToEE,bkg_ZToEE_stat_err,N_bkg_ttbar_other,bkg_ttbar_other_stat_err,N_bkg_Jets,bkg_Jets_stat_err)
                    #print " %-5d to %-5d | %-10d +- %-10.1f(stat.) | %-10.1f +- %-10.1f(st.+sy.) | %-10.1f +- %-10.1f(st.+sy.)       | %-10.1f +- %-10.1f(st.+sy.)       | %-10.1f +- %-10.1f(st.+sy.)"%(rmass[0],rmass[1],N_data,data_stat_err,N_bkg_all,bkg_all_err,N_bkg_ZToEE,bkg_ZToEE_err,N_bkg_ttbar_other,bkg_ttbar_other_err,N_bkg_Jets,0.5*N_bkg_Jets)
                    print " %-5d to %-5d | %-10d +- %-10.1f(stat.) | %-10.2f +- %-10.2f(st.+sy.) | %-10.2f +- %-10.2f(st.+sy.)       | %-10.2f +- %-10.2f(st.+sy.)       | %-10.2f +- %-10.2f(st.+sy.)"%(rmass[0],rmass[1],N_data,data_stat_err,N_bkg_all,bkg_all_err,N_bkg_ZToEE,bkg_ZToEE_err,N_bkg_ttbar_other,bkg_ttbar_other_err,N_bkg_Jets,0.5*N_bkg_Jets)
        print "end event table"        
        del table 
print "end job"         

sys.exit()

      
