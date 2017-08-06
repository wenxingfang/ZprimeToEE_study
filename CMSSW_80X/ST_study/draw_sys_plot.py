import math
import gc
import sys
import ROOT
from array import array
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 1;")
ROOT.TH1.AddDirectory(ROOT.kFALSE)

def remove_zero_point(graph):
    for i in range(graph.GetN()-1,-1,-1):
        if graph.GetY()[i]==0:graph.RemovePoint(i)
   
def get_total_err(h_nominal, h_err_down, h_err_up):
    g_nominal = ROOT.TGraphAsymmErrors(h_nominal)
    for ibin in range(0,g_nominal.GetN()):
        err_down=math.sqrt(math.pow(h_nominal.GetBinError(ibin+1),2)+math.pow(h_err_down.GetBinContent(ibin+1),2))
        err_up  =math.sqrt(math.pow(h_nominal.GetBinError(ibin+1),2)+math.pow(h_err_up.GetBinContent(ibin+1),2))
        g_nominal.SetPointEYlow(ibin,err_down)
        g_nominal.SetPointEYhigh(ibin,err_up)
    return g_nominal




def Graph_Xerror0(graph_in):
    for i in range(0,graph_in.GetN()):
        graph_in.SetPointEXlow (i, 0)
        graph_in.SetPointEXhigh(i, 0)

def get_self_err(hist, style):
    if type(hist) == ROOT.TH1D:
        gr=ROOT.TGraphAsymmErrors(hist)
        for ibin in range(0,gr.GetN()):
            if gr.GetY()[ibin] !=0:
                gr.SetPointEYlow(ibin,gr.GetErrorYlow(ibin)/gr.GetY()[ibin])
                gr.SetPointEYhigh(ibin,gr.GetErrorYhigh(ibin)/gr.GetY()[ibin])
            else:
                gr.SetPointEYlow(ibin ,0)
                gr.SetPointEYhigh(ibin,0)
            if style ==1:
                gr.SetPoint(ibin,gr.GetX()[ibin],0)
            else:
                gr.SetPoint(ibin,gr.GetX()[ibin],1)
        return gr
    elif type(hist) == ROOT.TGraphAsymmErrors:
        gr=hist.Clone(hist.GetName()+"_ratio")
        for ibin in range(0,gr.GetN()):
            if gr.GetY()[ibin] !=0:
                gr.SetPointEYlow(ibin,gr.GetErrorYlow(ibin)/gr.GetY()[ibin])
                gr.SetPointEYhigh(ibin,gr.GetErrorYhigh(ibin)/gr.GetY()[ibin])
            else:
                gr.SetPointEYlow(ibin ,0)
                gr.SetPointEYhigh(ibin,0)
            if style ==1:
                gr.SetPoint(ibin,gr.GetX()[ibin],0)
            else:
                gr.SetPoint(ibin,gr.GetX()[ibin],1)
        return gr
    else:
        print "don't match"
def get_graph_ratio(g1, g2, style):
    g_ratio=g1.Clone("g_ratio")
    for ibin in range(0, g_ratio.GetN()):
         ratio=999
         err_down=0
         err_up=0
         if float(g2.GetY()[ibin]) !=0:
             if style==1:
                 ratio=float((g1.GetY()[ibin]-g2.GetY()[ibin])/g2.GetY()[ibin])
             else:
                 ratio=float(g1.GetY()[ibin]/g2.GetY()[ibin])
             err_down=float(g1.GetErrorYlow(ibin)/g2.GetY()[ibin])
             err_up  =float(g1.GetErrorYhigh(ibin)/g2.GetY()[ibin])
         g_ratio.SetPoint(ibin,g_ratio.GetX()[ibin],ratio)
         g_ratio.SetPointEYlow(ibin,err_down)
         g_ratio.SetPointEYhigh(ibin,err_up)
    return g_ratio

def histTograph(h_data):  
    h_data_bin_value={}
    h_data_bin_width={}
    for bin in range(1, h_data.GetNbinsX()+1):
        h_data_bin_value[bin]=h_data.GetBinContent(bin)*h_data.GetBinWidth(bin) 
        h_data_bin_width[bin]=h_data.GetBinWidth(bin) 
    g_data = ROOT.TGraphAsymmErrors(h_data)
    g_data.SetMarkerSize(0.5)
    g_data.SetMarkerStyle (20)
    alpha = float(1 - 0.6827)
    hist_weight=['h_mee_all','h_mee_all_BB','h_mee_all_BE','h_mee_all_EE']
    for i in range(0,g_data.GetN()): 
        N = g_data.GetY()[i]
        error_up=0
        error_low=0
        if h_data.GetName().split("data_")[-1] in hist_weight:
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

def draw_plots(chan, date, dir, stack,h_mc,h_data, g_stat_sys ,out_name, xaxis_name, ratio_Style, log_hist, h_FCNC_tug, h_FCNC_tcg):
    stat_style=3015
    stat_color=ROOT.kOrange-3
    stat_sys_style=1001
    stat_sys_color=ROOT.kGray
    can_x_min=50
    can_x_max=865
    can_y_min=50
    can_y_max=780
    if out_name == "H_njet_bjet":
        can_x_min=0
        can_x_max=800
        can_y_min=0
        can_y_max=500
    canvas = ROOT.TCanvas('canvas','',can_x_min,can_y_min,can_x_max,can_y_max)
    canvas.SetLeftMargin(0.5)
    canvas.cd()
#    size = 0.25
#    pad1 = ROOT.TPad('pad1', '', 0.0, size, 1.0, 1.0, 0)
#    pad2 = ROOT.TPad('pad2', '', 0.0, 0.0, 1.0, size, 0)
    pad1=ROOT.TPad("pad1", "pad1", 0, 0.315, 1, 0.99 , 0)#used for the hist plot
    pad2=ROOT.TPad("pad2", "pad2", 0, 0.0, 1, 0.3 , 0)#used for the ratio plot
    pad1.Draw()
    pad2.Draw() 
    pad2.SetGridy()
    pad2.SetTickx()
    pad1.SetBottomMargin(0.02)
    pad1.SetLeftMargin(0.14)
    pad1.SetRightMargin(0.05)
    pad2.SetTopMargin(0.0)
    pad2.SetBottomMargin(0.4)
    pad2.SetLeftMargin(0.14)
    pad2.SetRightMargin(0.05)
    pad1.cd()
    pad1.SetLogx(ROOT.kFALSE)
    pad2.SetLogx(ROOT.kFALSE)
    pad1.SetLogy(ROOT.kFALSE)
    ########### For XY Range #############
    nbin_x=h_data.GetNbinsX()
    x_min=h_data.GetBinLowEdge(1)
    x_max=h_data.GetBinLowEdge(h_data.GetNbinsX())+h_data.GetBinWidth(h_data.GetNbinsX())
    y_min=0
    y_max=2*h_data.GetBinContent(h_data.GetMaximumBin())
    if out_name == "H_jet_low_led_CSV" or out_name=="H_jet_Bmissed_CSV": 
        x_min=0 
        y_max=4E3
    if out_name in log_hist:
        pad1.SetLogy(ROOT.kTRUE)
        y_min=1E-1
        y_max=1E3*(round(y_max/10)*10)
    if Channel != "emu" and out_name == 'H_Limit_N_jet_bjet':
       x_min=2
       nbin_x=3
       y_max=0.6*y_max
    if Channel == "emu" and out_name == 'H_Limit_N_jet_bjet':
       x_min=1
       nbin_x=4
       y_max=0.6*y_max
    if out_name == "H_njet_bjet":
       y_max=0.8*y_max
    dummy = ROOT.TH2F("dummy","",nbin_x,x_min,x_max,1,y_min,y_max)
    dummy.SetStats(ROOT.kFALSE)
    if h_data.GetBinWidth(1)%1 != 0:  
        dummy.GetYaxis().SetTitle('Event / %.1f'%(h_data.GetBinWidth(1)))
        if "GeV" in xaxis_name:dummy.GetYaxis().SetTitle('Event / %.1f GeV'%(h_data.GetBinWidth(1)))
    else:
        dummy.GetYaxis().SetTitle('Event / %.0f'%(h_data.GetBinWidth(1)))
        if "GeV" in xaxis_name:dummy.GetYaxis().SetTitle('Event / %.0f GeV'%(h_data.GetBinWidth(1)))
    dummy.GetXaxis().SetLabelSize(0)
    dummy.GetXaxis().SetMoreLogLabels()
    dummy.GetXaxis().SetNoExponent() 
    dummy.GetYaxis().SetTitleOffset(0.88)
    dummy.GetYaxis().SetTitleSize(0.08)
    dummy.GetYaxis().SetLabelSize(0.04/0.7)
    if out_name == "H_njet_bjet":
        dummy.GetYaxis().SetTitleOffset(0.82)
    steps    =["Dilepton","Z veto","MET",">=2 jets",">=1 b jet"] 
    str_njet =["(0,0)","(1,0)","(1,1)","(2,0)","(2,1)","(2,2)","(3,0)","(3,1)","(3,2)","(3,3)","(4,0)","(4,1)","(4,2)","(4,3)","(4,4)"]
    str_njet_limit_emu=["(1,0)","(1,1)","(2,1)","(#geq2,2)"]
    str_njet_limit_ee_mumu=["(1,1)","(2,1)","(#geq2,2)"]
    if out_name == "H_steps":
        for stp in steps:
            dummy.GetXaxis().SetBinLabel(steps.index(stp)+1,stp)
    elif out_name == "H_njet_bjet": 
        for str_j in str_njet:
            dummy.GetXaxis().SetBinLabel(str_njet.index(str_j)+1,str_j)
    elif out_name == "H_Limit_N_jet_bjet": 
        if Channel == "emu":
            for str_j in str_njet_limit_emu:
                dummy.GetXaxis().SetBinLabel(str_njet_limit_emu.index(str_j)+1,str_j)
        elif Channel == "ee" or Channel=="mumu":
            for str_j in str_njet_limit_ee_mumu:
                dummy.GetXaxis().SetBinLabel(str_njet_limit_ee_mumu.index(str_j)+1,str_j)
    dummy.Draw()
    stack.Draw('sames:hist')
    dummy.Draw("AXISSAME")
    ########### For XY Range #############
    g_data=histTograph(h_data)
    g_data.SetLineColor(ROOT.kBlack)
    g_data.SetMarkerStyle(20)
    g_data.SetMarkerSize(0.9)
    Graph_Xerror0(g_data)
    g_data_clone=g_data.Clone(g_data.GetName()+"_clone")
    remove_zero_point(g_data_clone)
    h_mc.SetFillStyle(3015)
    h_mc.SetFillColorAlpha(ROOT.kOrange-3,1.0)
    g_stat_sys.SetFillStyle(3015)
    g_stat_sys.SetFillColorAlpha(ROOT.kBlue-3,1.0)
    g_stat_sys.Draw("2p")
    h_mc.Draw("sames:e2")
    if remove_data==False:
        g_data_clone.Draw("pZ0")
    if Do_FCNC_Study:
        #if "tug" in out_name:
        #    h_FCNC_tug.SetLineWidth(2)
        #    h_FCNC_tug.SetLineColor(MC_Sample["FCNC_ST_tug"].color) 
        #    h_FCNC_tug.Draw("same:hist")
        #elif "tcg" in out_name:
        #    h_FCNC_tcg.SetLineWidth(2)
        #    h_FCNC_tcg.SetLineColor(MC_Sample["FCNC_ST_tcg"].color) 
        #    h_FCNC_tcg.Draw("same:hist")
        #else:
        h_FCNC_tug.SetLineWidth(2)
        h_FCNC_tug.SetLineColor(MC_Sample["FCNC_ST_tug"].color) 
        h_FCNC_tug.Draw("same:hist")
        h_FCNC_tcg.SetLineWidth(2)
        h_FCNC_tcg.SetLineColor(MC_Sample["FCNC_ST_tcg"].color) 
        h_FCNC_tcg.Draw("same:hist")
    h_tmp_FCNC_tug =h_data.Clone("FCNC_tug") 
    h_tmp_FCNC_tug.SetLineWidth(2)
    h_tmp_FCNC_tug.SetLineColor(ROOT.TColor.GetColor("#800000")) 
    h_tmp_FCNC_tcg =h_data.Clone("FCNC_tcg") 
    h_tmp_FCNC_tcg.SetLineWidth(2)
    h_tmp_FCNC_tcg.SetLineColor(ROOT.TColor.GetColor("#ffa500")) 
    h_tmp_ST   =h_data.Clone("ST") 
    h_tmp_ttbar=h_data.Clone("ttbar") 
    h_tmp_DY   =h_data.Clone("DY") 
    h_tmp_other=h_data.Clone("other") 
    h_tmp_ss   =h_data.Clone("same-sign") 
    h_tmp_uncertainty     =h_mc.Clone("stat_Uncert") 
    h_tmp_all_uncertainty =g_stat_sys.Clone("sys_Uncert") 
    h_tmp_ST    .SetLineColor(ROOT.kBlack) 
    h_tmp_ttbar .SetLineColor(ROOT.kBlack) 
    h_tmp_DY    .SetLineColor(ROOT.kBlack) 
    h_tmp_other .SetLineColor(ROOT.kBlack) 
    h_tmp_ss    .SetLineColor(ROOT.kBlack) 
    h_tmp_ST    .SetFillColor(MC_Sample["TW_top"].color) 
    h_tmp_ttbar .SetFillColor(MC_Sample["TTTo2L2Nu"].color) 
#    h_tmp_ttbar .SetFillColor(MC_Sample["TT_TuneEE5C"].color) 
    h_tmp_DY    .SetFillColor(MC_Sample["DYJetsToLL_M50_amc"].color) 
    h_tmp_other .SetFillColor(MC_Sample["WWTo2L2Nu"].color) 
    h_tmp_ss    .SetFillColor(MC_Sample["WJet_mad"].color) 
    legend_x_min=0.73
    legend_x_max=0.93
    legend_y_min=0.6
    legend_y_max=0.88
    if out_name == "H_njet_bjet":
        legend_x_min=0.73
        legend_x_max=0.93
        legend_y_min=0.4
        legend_y_max=0.88
    legend = ROOT.TLegend(legend_x_min,legend_y_min,legend_x_max,legend_y_max)
    if remove_data==False:
        legend.AddEntry(g_data,'Data (2016)','ep')
    if Do_FCNC_Study:
        legend.AddEntry(h_tmp_FCNC_tug,'tug(%d pb)'%(FCNC_XS),'l')
        legend.AddEntry(h_tmp_FCNC_tcg,'tcg(%d pb)'%(FCNC_XS),'l')
    legend.AddEntry(h_tmp_ST,"tW",'f')
    legend.AddEntry(h_tmp_ttbar,'t#bar{t}','f')
    legend.AddEntry(h_tmp_DY,'Z+jets','f')
    legend.AddEntry(h_tmp_other,'Others','f')
    if do_same_sign==True:
        legend.AddEntry(h_tmp_ss,'Jets','f')
    legend.AddEntry(h_tmp_uncertainty,'Stat. uncertainty','f')
    if len(system_list) !=1:
        legend.AddEntry(h_tmp_all_uncertainty,'Syst. uncertainty','f')

    legend.SetBorderSize(0)
    font = 42
    legend.SetTextFont(font)
    legend.Draw()
########################################
    Label_cms_prelim = ROOT.TPaveText(0.15,0.83,0.4,0.83,"NDC")
    Label_cms_prelim.SetLineColor(10)
    Label_cms_prelim.SetFillColor(10)
    Label_cms_prelim.SetTextSize(0.052/0.7)
    Label_cms_prelim.SetTextAlign(12)
    Label_cms_prelim.AddText("CMS Preliminary")
    Label_cms_prelim.SetShadowColor(10)
    Label_cms_prelim.Draw()
    Label_lumi_x_min=0.57
    Label_lumi_x_max=0.92
    Label_lumi_y_min=0.93
    Label_lumi_y_max=0.975
    if out_name == "H_njet_bjet":
        Label_lumi_x_min=0.70
        Label_lumi_x_max=0.95
        Label_lumi_y_min=0.9
        Label_lumi_y_max=0.95
    Label_lumi = ROOT.TPaveText(Label_lumi_x_min,Label_lumi_x_max,Label_lumi_y_min,Label_lumi_y_max,"NDC")
    Label_lumi.SetLineColor(10)
    Label_lumi.SetFillColor(10)
    Label_lumi.SetTextSize(0.06/0.7)
    Label_lumi.SetTextAlign(12)
    Label_lumi.SetTextFont(42)
    Label_lumi.AddText("%.1f fb^{-1} (13 TeV)"%(float(Lumi)/1000))
    Label_lumi.SetShadowColor(10)
    Label_lumi.Draw()
    Label_chan=ROOT.TPaveText(0.18,0.72, 0.35,0.7,"blNDC")
    Label_chan.SetBorderSize(0)
    Label_chan.SetFillStyle(0)
    Label_chan.SetTextAlign(10)
    Label_chan.SetTextColor(1)
#    Label_chan.SetTextFont(32)##just like text
    Label_chan.SetTextSize(0.12)
    if "ee" in chan:
        Label_chan.AddText ('ee')
    elif "emu" in chan:
        Label_chan.AddText ('e#mu')
    elif "mumu" in chan:
        Label_chan.AddText ('#mu#mu')
    Label_chan.Draw()
    Label_region=ROOT.TPaveText(0.18,0.62, 0.35,0.6,"blNDC")
    Label_region.SetBorderSize(0)
    Label_region.SetFillStyle(0)
    Label_region.SetTextAlign(10)
    Label_region.SetTextColor(1)
    Label_region.SetTextFont(32)
    Label_region.SetTextSize(0.08)
    if "0j0b" in out_name or "0jet_0bjet" in out_name: 
        Label_region.AddText('(0jet,0bjet)')
    elif "1j0b" in out_name or "1jet_0bjet" in out_name: 
        Label_region.AddText('(1jet,0bjet)')
    elif "1j1b" in out_name or "1jet_1bjet" in out_name: 
        Label_region.AddText('(1jet,1bjet)')
    elif "2j1b" in out_name or "2jet_1bjet" in out_name: 
        Label_region.AddText('(2jet,1bjet)')
    elif "2j2b" in out_name or "2jet_2bjet" in out_name: 
        Label_region.AddText('(2jet,2bjet)')
    Label_region.Draw()
    Label_pvn=ROOT.TPaveText(0.18,0.62, 0.35,0.6,"blNDC")
    Label_pvn.SetBorderSize(0)
    Label_pvn.SetFillStyle(0)
    Label_pvn.SetTextAlign(10)
    Label_pvn.SetTextColor(1)
    Label_pvn.SetTextFont(32)
    Label_pvn.SetTextSize(0.08)
    Label_pvn.AddText('Nvtx(25-30)')
#    Label_pvn.Draw()
##### for ratio label #######################
    err_data=ROOT.Double(0)
    err_mc  =ROOT.Double(0)
    N_data= h_data.IntegralAndError(h_data.GetXaxis().FindBin(x_min+1E-4),h_data.GetXaxis().FindBin(x_max-1E-4),err_data)
    N_mc  = h_mc  .IntegralAndError(h_mc.GetXaxis().FindBin(x_min+1E-4),h_mc.GetXaxis().FindBin(x_max-1E-4),err_mc)
    ratio = N_data/N_mc if N_mc!=0 else 0
    error_ratio=ratio*math.sqrt(math.pow(err_data/N_data,2)+math.pow(err_mc/N_mc,2)) if N_data!=0 and N_mc!=0 else 0
    label_ratio_x_min=0.7
    label_ratio_x_max=0.95
    label_ratio_y_min=0.5
    label_ratio_y_max=0.6
    if out_name == "H_njet_bjet":
        label_ratio_x_min=0.7
        label_ratio_x_max=0.95
        label_ratio_y_min=0.3
        label_ratio_y_max=0.4
    label_ratio = ROOT.TPaveLabel(label_ratio_x_min, label_ratio_y_min, label_ratio_x_max, label_ratio_y_max, "data/mc=%.2f #pm %.2f"%(ratio,error_ratio), "brNDC")
    label_ratio.SetBorderSize(0)
    label_ratio.SetFillColor(0)
    label_ratio.SetFillStyle(0)
    label_ratio.SetTextFont(font)
    label_ratio.SetTextSize(0.44)
    if remove_data==False and out_name not in ["H_njet_bjet","H_Limit_N_jet_bjet"]:
        label_ratio.Draw()
    ######################################
    pad2.cd()
    ratio_y_min=-0.5
    ratio_y_max=0.5
    if ratio_Style!=1:
        ratio_y_min=0.8
        ratio_y_max=1.2
    #    ratio_y_min=0.5
    #    ratio_y_max=1.5
    dummy_ratio = ROOT.TH2F("dummy_ratio","",nbin_x,x_min,x_max,1,ratio_y_min,ratio_y_max)
    dummy_ratio.SetStats(ROOT.kFALSE)
    dummy_ratio.GetYaxis().SetTitle('Data/Pred.')
    if ratio_Style==1:
        dummy_ratio.GetYaxis().SetTitle('(data-mc)/mc')
    dummy_ratio.GetXaxis().SetTitle(xaxis_name)
    dummy_ratio.GetXaxis().SetMoreLogLabels()
    dummy_ratio.GetXaxis().SetNoExponent()  
    dummy_ratio.GetXaxis().SetTitleSize(0.058/0.3)
    dummy_ratio.GetYaxis().SetTitleSize(0.045/0.3)
    dummy_ratio.GetXaxis().SetTitleFont(42)
    dummy_ratio.GetYaxis().SetTitleFont(42)
    dummy_ratio.GetXaxis().SetTickLength(0.05)
    dummy_ratio.GetYaxis().SetTickLength(0.05)
    dummy_ratio.GetXaxis().SetLabelSize(0.045/0.3)
    dummy_ratio.GetYaxis().SetLabelSize(0.04/0.3)
    if out_name in ["H_njet_bjet","H_Limit_N_jet_bjet"]:
        dummy_ratio.GetXaxis().SetLabelSize(0.2)
    dummy_ratio.GetXaxis().SetLabelOffset(0.02)
    dummy_ratio.GetYaxis().SetLabelOffset(0.01)
    dummy_ratio.GetYaxis().SetTitleOffset(0.41)
    dummy_ratio.GetXaxis().SetTitleOffset(0.23/0.25)
    dummy_ratio.GetYaxis().SetNdivisions(504)
    if "sum" in xaxis_name:
        dummy_ratio.GetXaxis().SetTitleSize(0.6*0.058/0.3)
        dummy_ratio.GetXaxis().SetTitleOffset(1.7)
    if out_name == "H_steps":
        for stp in steps:
            dummy_ratio.GetXaxis().SetBinLabel(steps.index(stp)+1,stp)
    elif out_name == "H_njet_bjet": 
        for str_j in str_njet:
            dummy_ratio.GetXaxis().SetBinLabel(str_njet.index(str_j)+1,str_j)
    elif out_name == "H_Limit_N_jet_bjet": 
        if Channel == "emu":
            for str_j in str_njet_limit_emu:
                dummy_ratio.GetXaxis().SetBinLabel(str_njet_limit_emu.index(str_j)+1,str_j)
        elif Channel == "ee" or Channel=="mumu":
            for str_j in str_njet_limit_ee_mumu:
                dummy_ratio.GetXaxis().SetBinLabel(str_njet_limit_ee_mumu.index(str_j)+1,str_j)
    dummy_ratio.Draw()
    g_mc    = ROOT.TGraphAsymmErrors(h_mc)
    g_ratio = get_graph_ratio(g_data, g_mc, ratio_Style)
    Graph_Xerror0(g_ratio) 
    g_mc_stat    =get_self_err(h_mc      , ratio_Style)
    g_mc_stat_sys=get_self_err(g_stat_sys, ratio_Style)
    g_mc_stat.SetFillStyle(stat_style)
    g_mc_stat.SetFillColorAlpha(ROOT.kOrange-3,1.0)
    g_mc_stat_sys.SetFillStyle(stat_style)
    g_mc_stat_sys.SetFillColorAlpha(ROOT.kBlue-3,1.0)
    g_mc_stat_sys.Draw("2p")
    g_mc_stat.Draw("2p")
    dummy_ratio.Draw("AXISSAME")
    if remove_data==False:
        g_ratio.Draw("pZ0")
    #####################################
    canvas.Print('%s/%s/%s.png'%(dir,date,out_name))    
    del canvas
    gc.collect()
     
def draw_combine_MVA(chan, date, dir, MVA_hist):
    stat_style=3015
    stat_color=ROOT.kOrange-3
    stat_sys_style=1001
    stat_sys_color=ROOT.kGray
    up_high=0.62
    down_high=0.38
    if Channel=="emu":
        canvas = ROOT.TCanvas('canvas','',0,0,1500,500)
        canvas.cd()
        pad_width=0.3
        pad11=ROOT.TPad("pad11", "pad11", 0, down_high, pad_width, 1 , 0)#used for the hist plot
        pad12=ROOT.TPad("pad12", "pad12", 0, 0, pad_width, down_high , 0)#used for the ratio plot
        pad21=ROOT.TPad("pad21", "pad21", pad_width, down_high, 2*pad_width, 1 , 0)#used for the hist plot
        pad22=ROOT.TPad("pad22", "pad22", pad_width, 0, 2*pad_width, down_high , 0)#used for the ratio plot
        pad31=ROOT.TPad("pad31", "pad31", 2*pad_width, down_high, 3*pad_width, 1 , 0)#used for the hist plot
        pad32=ROOT.TPad("pad32", "pad32", 2*pad_width, 0, 3*pad_width, down_high , 0)#used for the ratio plot
        pad41=ROOT.TPad("pad41", "pad41", 3*pad_width, down_high, 1, 1 , 0)#used for the hist plot
        pad42=ROOT.TPad("pad42", "pad42", 3*pad_width, 0, 1, down_high , 0)#used for the ratio plot
        up_list  =[pad11,pad21,pad31,pad41]
        down_list=[pad12,pad22,pad32,pad42]
        pad11.SetLeftMargin(0.2)
        pad21.SetLeftMargin(0.01)
        pad31.SetLeftMargin(0.01)
        pad41.SetLeftMargin(0.01)
        pad12.SetLeftMargin(0.2)
        pad22.SetLeftMargin(0.01)
        pad32.SetLeftMargin(0.01)
        pad42.SetLeftMargin(0.01)
        pad11.SetBottomMargin(0.05)
        pad21.SetBottomMargin(0.05)
        pad31.SetBottomMargin(0.05)
        pad41.SetBottomMargin(0.05)
#        pad11.SetRightMargin(0.01)
        pad21.SetRightMargin(0.15)
        pad22.SetRightMargin(0.15)
        pad31.SetRightMargin(0.15)
        pad32.SetRightMargin(0.15)
#        pad41.SetRightMargin(0.01)
        pad12.SetBottomMargin(0.4)
        pad22.SetBottomMargin(0.4)
        pad32.SetBottomMargin(0.4)
        pad42.SetBottomMargin(0.4)
        pad12.SetTopMargin(0.01)
        pad22.SetTopMargin(0.01)
        pad32.SetTopMargin(0.01)
        pad42.SetTopMargin(0.01)
        for ip in up_list:
            ip.Draw()
        for ip in down_list:
            ip.Draw()
        hist_list=["H_MLP_1jet_0bjet","H_MLP_1jet_1bjet","H_MLP_2jet_1bjet","H_MLP_2jet_2bjet"]
        dummy_list=[]
        for hname in hist_list:
            if hname not in MVA_hist: 
                print "warning: wrong input hist name"
                break;
            up_list[hist_list.index(hname)].cd()
            nbin_x=MVA_hist[hname][1].GetNbinsX()
            x_min =MVA_hist[hname][1].GetXaxis().GetXmin()
            x_max =MVA_hist[hname][1].GetXaxis().GetXmax()
            y_min=0
            y_max=1.5*MVA_hist[hname][1].GetBinContent(MVA_hist[hname][1].GetMaximumBin())
            if hist_list.index(hname)==3:
                y_max=2.5*MVA_hist[hname][1].GetBinContent(MVA_hist[hname][1].GetMaximumBin())
            dummy = ROOT.TH2F("dummy_%s"%(hname),"",nbin_x,x_min,x_max,1,y_min,y_max)
            dummy_list.append(dummy)
            dummy.SetStats(ROOT.kFALSE)
            dummy.GetYaxis().SetTitle('Events')
            dummy.GetXaxis().SetLabelSize(0)
            dummy.GetYaxis().SetTitleOffset(1.2)
            dummy.GetYaxis().SetTitleSize(0.08)
            dummy.GetYaxis().SetLabelSize(0.08)
            if hist_list.index(hname)!=0:
                dummy.GetYaxis().SetTitle('')
            if hist_list.index(hname)!=3:
                dummy.GetXaxis().SetNdivisions(205)
                dummy.GetXaxis().SetMoreLogLabels()
                dummy.GetXaxis().SetNoExponent() 
            if hist_list.index(hname)==3:
                dummy.GetYaxis().SetLabelSize(0.15)
                dummy.GetXaxis().SetNdivisions(102)
            dummy.Draw()
            MVA_hist[hname][0].Draw('sames:hist')
            dummy.Draw("AXISSAME")
            ########### For XY Range #############
            g_data=histTograph(MVA_hist[hname][2])
            dummy_list.append(g_data)
            g_data.SetLineColor(ROOT.kBlack)
            g_data.SetMarkerStyle(20)
            g_data.SetMarkerSize(0.8)
            Graph_Xerror0(g_data)
            g_data_clone=g_data.Clone(g_data.GetName()+"_clone")
            dummy_list.append(g_data_clone)
            remove_zero_point(g_data_clone)
            MVA_hist[hname][1].SetFillStyle(3015)
            MVA_hist[hname][1].SetFillColorAlpha(ROOT.kOrange-3,1.0)
            MVA_hist[hname][3].SetFillStyle(3015)
            MVA_hist[hname][3].SetFillColorAlpha(ROOT.kBlue-3,1.0)
            MVA_hist[hname][3].Draw("2p")
            MVA_hist[hname][1].Draw("sames:e2")
            g_data_clone.Draw("pZ0")
            h_tmp_ST   =MVA_hist[hname][2].Clone("ST") 
            h_tmp_ttbar=MVA_hist[hname][2].Clone("ttbar") 
            h_tmp_DY   =MVA_hist[hname][2].Clone("DY") 
            h_tmp_other=MVA_hist[hname][2].Clone("other") 
            h_tmp_ss   =MVA_hist[hname][2].Clone("other") 
            h_tmp_uncertainty     =MVA_hist[hname][1].Clone("stat_Uncert") 
            h_tmp_all_uncertainty =MVA_hist[hname][3].Clone("sys_Uncert") 
            h_tmp_ST    .SetLineColor(ROOT.kBlack) 
            h_tmp_ttbar .SetLineColor(ROOT.kBlack) 
            h_tmp_DY    .SetLineColor(ROOT.kBlack) 
            h_tmp_other .SetLineColor(ROOT.kBlack) 
            h_tmp_ss    .SetLineColor(ROOT.kBlack) 
            h_tmp_ST    .SetFillColor(MC_Sample["TW_top"].color) 
            h_tmp_ttbar .SetFillColor(MC_Sample["TTTo2L2Nu"].color) 
            h_tmp_DY    .SetFillColor(MC_Sample["DYJetsToLL_M50_amc"].color) 
            h_tmp_other .SetFillColor(MC_Sample["WWTo2L2Nu"].color) 
            h_tmp_ss    .SetFillColor(MC_Sample["WJet_mad"].color) 
            legend = ROOT.TLegend(0.02,0.5,0.78,0.85)
            legend.AddEntry(g_data,'Data (2016)','ep')
            legend.AddEntry(h_tmp_ST,"ST_tw",'f')
            legend.AddEntry(h_tmp_ttbar,'t#bar{t}','f')
            legend.AddEntry(h_tmp_DY,'Z+jets','f')
            legend.AddEntry(h_tmp_other,'Others','f')
            legend.AddEntry(h_tmp_uncertainty,'Stat. uncertainty','f')
            legend.AddEntry(h_tmp_all_uncertainty,'Syst. uncertainty','f')
            legend.SetBorderSize(0)
            font = 42
            legend.SetTextFont(font)
            legend.SetTextSize(0.1)
            legend.Draw()
####        ####################################
            Label_cms_prelim = ROOT.TPaveText(0.25,0.83,0.4,0.83,"NDC")
            Label_cms_prelim.SetLineColor(10)
            Label_cms_prelim.SetFillColor(10)
            Label_cms_prelim.SetTextSize(0.052/0.7)
            Label_cms_prelim.SetTextAlign(12)
            Label_cms_prelim.AddText("CMS Preliminary")
            Label_cms_prelim.SetShadowColor(10)
            Label_lumi = ROOT.TPaveText(0.5,0.93,0.9,0.98,"NDC")
            Label_lumi.SetLineColor(10)
            Label_lumi.SetFillColor(10)
            Label_lumi.SetTextSize(0.06/0.7)
            Label_lumi.SetTextAlign(12)
            Label_lumi.SetTextFont(42)
            Label_lumi.AddText("%.1f fb^{-1} (13 TeV)"%(float(Lumi)/1000))
            Label_lumi.SetShadowColor(10)
            Label_chan=ROOT.TPaveText(0.25,0.72, 0.45,0.7,"blNDC")
            Label_chan.SetBorderSize(0)
            Label_chan.SetFillStyle(0)
            Label_chan.SetTextAlign(10)
            Label_chan.SetTextColor(1)
            Label_chan.SetTextFont(32)
            Label_chan.SetTextSize(0.12)
            if "ee" in chan:
                Label_chan.AddText ('ee')
            elif "emu" in chan:
                Label_chan.AddText ('e#mu')
            elif "mumu" in chan:
                Label_chan.AddText ('#mu#mu')
            if hist_list.index(hname)==0:
                Label_cms_prelim.Draw()
                Label_lumi.Draw()
                Label_chan.Draw()
                dummy_list.append(Label_cms_prelim)
                dummy_list.append(Label_lumi)
                dummy_list.append(Label_chan)
####        # for ratio label #######################
            err_data=ROOT.Double(0)
            err_mc  =ROOT.Double(0)
            N_data= MVA_hist[hname][2].IntegralAndError(MVA_hist[hname][2].GetXaxis().FindBin(x_min+1E-4),MVA_hist[hname][2].GetXaxis().FindBin(x_max-1E-4),err_data)
            N_mc  = MVA_hist[hname][1].IntegralAndError(MVA_hist[hname][1].GetXaxis().FindBin(x_min+1E-4),MVA_hist[hname][1].GetXaxis().FindBin(x_max-1E-4),err_mc)
            ratio = N_data/N_mc if N_mc!=0 else 0
            error_ratio=ratio*math.sqrt(math.pow(err_data/N_data,2)+math.pow(err_mc/N_mc,2)) if N_data!=0 and N_mc!=0 else 0
            label_ratio = ROOT.TPaveLabel(0.6, 0.5, 0.9, 0.6, "data/mc=%.2f #pm %.2f"%(ratio,error_ratio), "brNDC")
            label_ratio.SetBorderSize(0)
            label_ratio.SetFillColor(0)
            label_ratio.SetFillStyle(0)
            label_ratio.SetTextFont(font)
            label_ratio.SetTextSize(0.44)
#            label_ratio.Draw()
            ######################################
            down_list[hist_list.index(hname)].cd()
            ratio_y_min=0.8
            ratio_y_max=1.2
            dummy_ratio = ROOT.TH2F("dummy_ratio_%s"%(hname),"",nbin_x,x_min,x_max,1,ratio_y_min,ratio_y_max)
            dummy_list.append(dummy_ratio)
            dummy_ratio.SetStats(ROOT.kFALSE)
            dummy_ratio.GetYaxis().SetTitle('Data/Pred.')
            if hist_list.index(hname)!=0:
                dummy_ratio.GetYaxis().SetTitle('')
            dummy_ratio.GetXaxis().SetTitle(dir_MVA[hname])
            dummy_ratio.GetXaxis().CenterTitle()
            dummy_ratio.GetYaxis().CenterTitle()
            dummy_ratio.GetXaxis().SetMoreLogLabels()
            dummy_ratio.GetXaxis().SetNoExponent()  
            dummy_ratio.GetXaxis().SetTitleSize(0.04/0.3)
            dummy_ratio.GetYaxis().SetTitleSize(0.04/0.3)
            dummy_ratio.GetXaxis().SetTitleFont(42)
            dummy_ratio.GetYaxis().SetTitleFont(42)
            dummy_ratio.GetXaxis().SetTickLength(0.05)
            dummy_ratio.GetYaxis().SetTickLength(0.05)
            dummy_ratio.GetXaxis().SetLabelSize(0.045/0.3)
            dummy_ratio.GetYaxis().SetLabelSize(0.04/0.3)
            dummy_ratio.GetXaxis().SetLabelOffset(0.02)
            dummy_ratio.GetYaxis().SetLabelOffset(0.01)
            dummy_ratio.GetYaxis().SetTitleOffset(0.7)
            dummy_ratio.GetXaxis().SetTitleOffset(1.3)
            dummy_ratio.GetYaxis().SetNdivisions(504)
            if hist_list.index(hname)==3:
                dummy_ratio.GetXaxis().SetNdivisions(102)
                dummy_ratio.GetXaxis().SetLabelSize(0)
                dummy_ratio.GetYaxis().SetLabelSize(1.1*0.04/0.3)
            if hist_list.index(hname)!=3:
                dummy_ratio.GetXaxis().SetNdivisions(205)
            
            dummy_ratio.Draw()
            g_mc    = ROOT.TGraphAsymmErrors(MVA_hist[hname][1])
            dummy_list.append(g_mc)
            g_ratio = get_graph_ratio(g_data, g_mc, 0)
            dummy_list.append(g_ratio)
            Graph_Xerror0(g_ratio) 
            g_mc_stat    =get_self_err(MVA_hist[hname][1] , 0)
            dummy_list.append(g_mc_stat)
            g_mc_stat_sys=get_self_err(MVA_hist[hname][3] , 0)
            dummy_list.append(g_mc_stat_sys)
            g_mc_stat.SetFillStyle(stat_style)
            g_mc_stat.SetFillColorAlpha(ROOT.kOrange-3,1.0)
            g_mc_stat_sys.SetFillStyle(stat_style)
            g_mc_stat_sys.SetFillColorAlpha(ROOT.kBlue-3,1.0)
            g_mc_stat_sys.Draw("2p")
            g_mc_stat.Draw("2p")
            dummy_ratio.Draw("AXISSAME")
            g_ratio.Draw("pZ0")
            #####################################
        canvas.Print('%s/%s/%s_mva_combine.png'%(dir,date,chan))    
        del canvas
        gc.collect()
             
#    else:
#        pad_width=0.4
#        pad11=ROOT.TPad("pad11", "pad11", 0, down_high, pad_width, 1 , 0)#used for the hist plot
#        pad12=ROOT.TPad("pad12", "pad12", 0, 0, pad_width, down_high , 0)#used for the ratio plot
#        pad21=ROOT.TPad("pad21", "pad21", pad_width, down_high, 2*pad_width, 1 , 0)#used for the hist plot
#        pad22=ROOT.TPad("pad22", "pad22", pad_width, 0, 2*pad_width, down_high , 0)#used for the ratio plot
#        pad31=ROOT.TPad("pad31", "pad31", 2*pad_width, down_high, 1, 1 , 0)#used for the hist plot
#        pad32=ROOT.TPad("pad32", "pad32", 2*pad_width, 0, 1, down_high , 0)#used for the ratio plot
#        pad_list=[pad11,pad12,pad21,pad22,pad31,pad32]
#        for ip in pad_list:
#            pad_list[ip].Draw()
#        ["H_MLP_1jet_0bjet","H_MLP_1jet_1bjet","H_MLP_2jet_1bjet","H_MLP_2jet_2bjet"]
    
def H2D_2H1D(h2):
    h_x=h2.ProjectionX("h_x")
    h_y=h2.ProjectionY("h_y")
    for ix in range(1, h2.GetXaxis().GetNbins()+1):
        x_value=0
        x_err  =0
        for iy in range(1, h2.GetYaxis().GetNbins()+1):
            x_value=x_value+h2.GetBinContent(ix,iy)
            x_err  =math.sqrt(math.pow(x_err,2)+math.pow(h2.GetBinError(ix,iy),2))
        h_x.SetBinContent(ix,x_value)
        h_x.SetBinError  (ix,x_err  )
    for iy in range(1, h2.GetYaxis().GetNbins()+1):
        y_value=0
        y_err  =0
        for ix in range(1, h2.GetXaxis().GetNbins()+1):
            y_value=y_value+h2.GetBinContent(ix,iy)
            y_err  =math.sqrt(math.pow(y_err,2)+math.pow(h2.GetBinError(ix,iy),2))
        h_y.SetBinContent(iy,y_value)
        h_y.SetBinError  (iy,y_err  )
    return [h_x,h_y]

def draw_graph_compare(g1,g2,out_name,chan):
    canvas = ROOT.TCanvas('canvas','',50,50,865,780)
    canvas.SetLeftMargin(0.5)
    canvas.cd()
    pad1=ROOT.TPad("pad1", "pad1", 0, 0.315, 1, 0.99 , 0)#used for the hist plot
    pad2=ROOT.TPad("pad2", "pad2", 0, 0.0, 1, 0.3 , 0)#used for the ratio plot
    pad1.Draw()
    pad2.Draw() 
    pad2.SetGridy()
    pad2.SetTickx()
    pad1.SetBottomMargin(0.02)
    pad1.SetLeftMargin(0.14)
    pad1.SetRightMargin(0.05)
    pad2.SetTopMargin(0.0)
    pad2.SetBottomMargin(0.42)
    pad2.SetLeftMargin(0.14)
    pad2.SetRightMargin(0.05)
    pad1.cd()
    x_min=g1.GetX()[0]-g1.GetErrorXlow(0)
    x_max=g1.GetX()[g1.GetN()-1]+g1.GetErrorXhigh(g1.GetN()-1)
    y_min=0.96
    y_max=1.01
    if "eta" in out_name:
        y_min=0.92
        y_max=1.02
        #y_min=0.97
        #y_max=1.005
    if "pt" in out_name:
        y_min=0.92
        y_max=1.02
    dummy = ROOT.TH2D("dummy","",1,x_min,x_max,1,y_min,y_max)
    dummy.SetStats(ROOT.kFALSE)
    dummy.GetYaxis().SetTitle('Efficiency')
    dummy.GetXaxis().SetLabelSize(0)
    dummy.GetXaxis().SetMoreLogLabels()
    dummy.GetXaxis().SetNoExponent() 
    dummy.GetYaxis().SetTitleOffset(0.88)
    dummy.GetYaxis().SetTitleSize(0.08)
    dummy.GetYaxis().SetLabelSize(0.04/0.7)
    dummy.Draw()
    g1.SetMarkerColor(ROOT.kBlue)
    g1.SetMarkerStyle(8)
    g1.SetLineColor(ROOT.kBlue)
    g2.SetFillColor(ROOT.kRed-10)
    g2.SetMarkerStyle(8)
    g2.SetMarkerColor(ROOT.kRed)
    g2.SetLineColor(ROOT.kRed)
    g2.Draw("e20")
    g2.Draw("pe0")
    g1.Draw("pe0")
    dummy.Draw("AXISSAME")

    legend = ROOT.TLegend(0.2,0.73,0.5,0.88)
    #legend.AddEntry(g1,'Data (2016)','lep')
    legend.AddEntry(g1,'Data (2016 B-E)','lep')
    legend.AddEntry(g2,"MC",'flpe')
    legend.SetBorderSize(0)
    font = 42
    legend.SetTextFont(font)
    legend.Draw()

################## ratio ########################
    pad2.cd()
    ratio_y_min=0.95
    ratio_y_max=1.05
    dummy_ratio = ROOT.TH2F("dummy_ratio","",1,x_min,x_max,1,ratio_y_min,ratio_y_max)
    dummy_ratio.SetStats(ROOT.kFALSE)
    dummy_ratio.GetYaxis().SetTitle('Scale factor')
    dummy_ratio.GetXaxis().SetMoreLogLabels()
    dummy_ratio.GetXaxis().SetNoExponent()  
    dummy_ratio.GetXaxis().SetTitleSize(0.058/0.3)
    dummy_ratio.GetYaxis().SetTitleSize(0.045/0.3)
    dummy_ratio.GetXaxis().SetTitleFont(42)
    dummy_ratio.GetYaxis().SetTitleFont(42)
    dummy_ratio.GetXaxis().SetTickLength(0.05)
    dummy_ratio.GetYaxis().SetTickLength(0.05)
    dummy_ratio.GetXaxis().SetLabelSize(0.045/0.3)
    dummy_ratio.GetYaxis().SetLabelSize(0.04/0.3)
    dummy_ratio.GetXaxis().SetLabelOffset(0.02)
    dummy_ratio.GetYaxis().SetLabelOffset(0.01)
    dummy_ratio.GetYaxis().SetTitleOffset(0.41)
    dummy_ratio.GetXaxis().SetTitleOffset(0.23/0.25)
    dummy_ratio.GetYaxis().SetNdivisions(405)
    dummy_ratio.GetXaxis().SetTitle("")
    if "pt" in out_name:
        dummy_ratio.GetXaxis().SetTitle("P_{T}^{Leading lepton} (GeV)")
        if "sub" in out_name:
            dummy_ratio.GetXaxis().SetTitle("P_{T}^{Sub-leading lepton} (GeV)")
    elif "eta" in out_name:
        str_eta=" "
        if chan=="ee":str_eta="sc" 
        print "channel:%s,%s"%(chan,str_eta)
        dummy_ratio.GetXaxis().SetTitle("#eta_{"+str_eta+"}^{Leading lepton}")
        if "sub" in out_name:
            dummy_ratio.GetXaxis().SetTitle("#eta_{"+str_eta+"}^{Sub-leading lepton}")
    elif "MET" in out_name:
        dummy_ratio.GetXaxis().SetTitle("MET(T1Txy)(GeV)")
    elif "Nvtx" in out_name:
        dummy_ratio.GetXaxis().SetTitle("Nvtx")
    elif "Njet" in out_name:
        dummy_ratio.GetXaxis().SetTitle("Number of jet")
    elif "Nbjet" in out_name:
        dummy_ratio.GetXaxis().SetTitle("Number of b jet")
    dummy_ratio.Draw()
    g_ratio=g1.Clone("ratio")
    g_ratio.SetLineColor(ROOT.kBlack)
    g_ratio.SetMarkerColor(ROOT.kBlack)
    g_ratio.SetMarkerStyle(8)
    for ir in range(0,g1.GetN()):
        ratio_value=g1.GetY()[ir]/g2.GetY()[ir] if g2.GetY()[ir] !=0 else 0
        g1_err_up  =g1.GetEYhigh()[ir]
        g1_err_down=g1.GetEYlow()[ir]
        g2_err_up  =g2.GetEYhigh()[ir]
        g2_err_down=g2.GetEYlow()[ir]
        ratio_err_up  =ratio_value*math.sqrt(math.pow(g1_err_up  /g1.GetY()[ir],2)+math.pow(g2_err_up  /g2.GetY()[ir],2)) if g1.GetY()[ir]!=0 and g2.GetY()[ir] !=0 else 0
        ratio_err_down=ratio_value*math.sqrt(math.pow(g1_err_down/g1.GetY()[ir],2)+math.pow(g2_err_down/g2.GetY()[ir],2)) if g1.GetY()[ir]!=0 and g2.GetY()[ir] !=0 else 0
        g_ratio.SetPoint(ir,g_ratio.GetX()[ir],ratio_value)
        g_ratio.SetPointEYhigh(ir,ratio_err_up  )
        g_ratio.SetPointEYlow (ir,ratio_err_down)
    g_ratio.Draw("pe0")
    fline = ROOT.TF1('fline', '[0]')
    fline.SetParameters(0,1)
    fline.SetLineColor(ROOT.kBlue)
    fline.SetLineWidth(2)
    g_ratio.Fit(fline,"","",x_min,x_max)
    fit_ratio_label = ROOT.TLatex()
    fit_ratio_label.SetTextAlign(12)
    fit_ratio_label.SetTextSize(0.09)
    fit_ratio_label.SetNDC(ROOT.kTRUE)
    fit_ratio_label.DrawLatex(0.65,0.95, '#chi^{2}/ndof    %.2f / %d'%(fline.GetChisquare(),fline.GetNDF()))
#    fit_ratio_label.DrawLatex(0.15,0.5 ,'Prob            %.3f '%(fline.GetProb()))
    fit_ratio_label.DrawLatex(0.65,0.85 ,'p0              %.3f #pm %.3f'%(fline.GetParameter(0),fline.GetParError(0)))
    canvas.Print('%s/%s/%s.png'%(dir,date,out_name))    
    del canvas
    gc.collect()


def Draw_all_system_plots(dir, date, Dicit, color, dir_hist, dir_system_name):
    for hname in Dicit:
        canvas = ROOT.TCanvas('canvas_%s'%(hname),'',50,50,865,780)
        canvas.SetLeftMargin(0.5)
        canvas.cd()
        pad1=ROOT.TPad("pad1", "pad1", 0, 0.6, 1, 0.99 , 0)#used for the hist plot
        pad2=ROOT.TPad("pad2", "pad2", 0, 0.0, 1, 0.6 , 0)#used for the ratio plot
        pad1.Draw()
        pad2.Draw() 
        pad2.SetGridy()
        pad2.SetTickx()
        pad1.SetBottomMargin(0.02)
        pad1.SetLeftMargin(0.14)
        pad1.SetRightMargin(0.05)
        pad2.SetTopMargin(0.0)
        pad2.SetBottomMargin(0.2)
        pad2.SetLeftMargin(0.14)
        pad2.SetRightMargin(0.05)
        pad1.cd()
        h_mc_nominal=Dicit[hname]["nominal"].Clone("%s_nominal"%(hname))
        x_min=h_mc_nominal.GetXaxis().GetXmin()
        x_max=h_mc_nominal.GetXaxis().GetXmax()
        y_min=0
        y_max=2*h_mc_nominal.GetBinContent(h_mc_nominal.GetMaximumBin())
        dummy = ROOT.TH2D("dummy","",1,x_min,x_max,1,y_min,y_max)
        dummy.SetStats(ROOT.kFALSE)
        dummy.GetYaxis().SetTitle('Events / %.1f'%(h_mc_nominal.GetBinWidth(1)))
        dummy.GetXaxis().SetLabelSize(0)
        dummy.GetXaxis().SetMoreLogLabels()
        dummy.GetXaxis().SetNoExponent() 
        dummy.GetYaxis().SetTitleOffset(0.88)
        dummy.GetYaxis().SetTitleSize(0.08)
        dummy.GetYaxis().SetLabelSize(0.04/0.7)
        dummy.Draw()
        line_width=2
        h_mc_nominal.SetLineWidth(line_width)
        h_mc_nominal.SetLineColor(color["nominal"])
        h_mc_nominal.Draw("same:hist")
        legend = ROOT.TLegend(0.16,0.55,0.93,0.88)
        legend.SetBorderSize(0)
        legend.SetNColumns(5)
        legend.AddEntry(h_mc_nominal,'nominal','l')
        dicit_dummy=[]
        for nsys in Dicit[hname] :
            if nsys is "nominal":continue
            #if "lumi" in nsys or "bgk" in nsys or "trig" in nsys or "SF" in nsys:continue
            if "Sample" not in nsys:continue
            pad1.cd()
            h_mc=Dicit[hname][nsys].Clone("%s_%s"%(hname,nsys))
            h_mc.SetLineWidth(line_width)
            h_mc.SetLineColor(color[nsys])
            h_mc.Draw("same:hist")
            legend.AddEntry(h_mc,dir_system_name[nsys],'l')
            dicit_dummy.append(h_mc)
        pad1.cd()
        dummy.Draw("AXISSAME")
        legend.Draw()
        pad2.cd()
        ratio_y_min=0.5
        ratio_y_max=1.5
        dummy_ratio = ROOT.TH2F("dummy_ratio_%s"%(hname),"",1,x_min,x_max,1,ratio_y_min,ratio_y_max)
        dummy_ratio.SetStats(ROOT.kFALSE)
        dummy_ratio.GetYaxis().SetTitle('Relative uncertainty')
        dummy_ratio.GetYaxis().CenterTitle()
        dummy_ratio.GetXaxis().SetTitle("")
        if dir_hist[hname]:
            dummy_ratio.GetXaxis().SetTitle(dir_hist[hname])
        dummy_ratio.GetXaxis().SetMoreLogLabels()
        dummy_ratio.GetXaxis().SetNoExponent()  
        dummy_ratio.GetXaxis().SetTitleSize(0.025/0.3)
        dummy_ratio.GetYaxis().SetTitleSize(0.025/0.3)
        dummy_ratio.GetXaxis().SetTitleFont(42)
        dummy_ratio.GetYaxis().SetTitleFont(42)
        dummy_ratio.GetXaxis().SetTickLength(0.05)
        dummy_ratio.GetYaxis().SetTickLength(0.05)
        dummy_ratio.GetXaxis().SetLabelSize(0.02/0.3)
        dummy_ratio.GetYaxis().SetLabelSize(0.02/0.3)
        dummy_ratio.GetXaxis().SetLabelOffset(0.02)
        dummy_ratio.GetYaxis().SetLabelOffset(0.01)
        dummy_ratio.GetYaxis().SetTitleOffset(0.7)
        dummy_ratio.GetXaxis().SetTitleOffset(0.25/0.25)
        dummy_ratio.GetYaxis().SetNdivisions(504)
        dummy_ratio.Draw()
        for nsys in Dicit[hname]:
            #if "lumi" in nsys or "bgk" in nsys or "trig" in nsys or "SF" in nsys:continue
            if "Sample" not in nsys:continue
            pad2.cd()
            h_mc=Dicit[hname][nsys].Clone("ratio_%s_%s"%(hname,nsys))
            h_mc.Divide(h_mc_nominal)
            h_mc.SetLineWidth(line_width)
            h_mc.SetLineColor(color[nsys])
            h_mc.Draw("same:hist")
            dicit_dummy.append(h_mc)
        dummy_ratio.Draw("AXISSAME")
        canvas.Print('%s/%s/sys_%s.png'%(dir,date,hname))    
        del canvas
        gc.collect()
        
def Draw_all_system_ratio(dir, date, Dicit, color, dir_hist, dir_system_name, sys_name):
    for hname in Dicit:
        canvas = ROOT.TCanvas('canvas_%s'%(hname),'',50,50,865,780)
        canvas.SetLeftMargin(0.1)
        canvas.SetBottomMargin(0.1)
        canvas.cd()
        canvas.SetGridy()
        canvas.SetTickx()
        canvas.cd()
        h_mc_nominal=Dicit[hname]["nominal"].Clone("%s_nominal"%(hname))
        x_min=h_mc_nominal.GetXaxis().GetXmin()
        x_max=h_mc_nominal.GetXaxis().GetXmax()
        line_width=2
        dicit_dummy=[]
        ratio_y_min=0.5
        ratio_y_max=2.0
        nbin=h_mc_nominal.GetNbinsX()
        if hname == "H_Limit_N_jet_bjet":
            if Channel == "ee" or Channel=="mumu":
                x_min=2
                nbin=3
            elif Channel == "emu":
                x_min=1
                nbin=4
        dummy_ratio = ROOT.TH2F("dummy_ratio_%s"%(hname),"",nbin,x_min,x_max,1,ratio_y_min,ratio_y_max)
        dummy_ratio.SetStats(ROOT.kFALSE)
        dummy_ratio.GetYaxis().SetTitle('Relative uncertainty')
        dummy_ratio.GetYaxis().CenterTitle()
        dummy_ratio.GetXaxis().SetTitle("")
        if dir_hist[hname]:
            dummy_ratio.GetXaxis().SetTitle(dir_hist[hname])
        str_njet =["(0,0)","(1,0)","(1,1)","(2,0)","(2,1)","(2,2)","(3,0)","(3,1)","(3,2)","(3,3)","(4,0)","(4,1)","(4,2)","(4,3)","(4,4)"]
        str_njet_limit_emu=["(1,0)","(1,1)","(2,1)","(#geq2,2)"]
        str_njet_limit_ee_mumu=["(1,1)","(2,1)","(#geq2,2)"]
        if hname == "H_njet_bjet": 
            for str_j in str_njet:
                dummy_ratio.GetXaxis().SetBinLabel(str_njet.index(str_j)+1,str_j)
        elif hname == "H_Limit_N_jet_bjet": 
            if Channel == "emu":
                for str_j in str_njet_limit_emu:
                    dummy_ratio.GetXaxis().SetBinLabel(str_njet_limit_emu.index(str_j)+1,str_j)
            elif Channel == "ee" or Channel=="mumu":
                for str_j in str_njet_limit_ee_mumu:
                    dummy_ratio.GetXaxis().SetBinLabel(str_njet_limit_ee_mumu.index(str_j)+1,str_j)
        dummy_ratio.GetXaxis().SetMoreLogLabels()
        dummy_ratio.GetXaxis().SetNoExponent()  
        dummy_ratio.GetXaxis().SetTitleSize(0.03)
        dummy_ratio.GetYaxis().SetTitleSize(0.03)
        dummy_ratio.GetXaxis().SetTitleFont(42)
        dummy_ratio.GetYaxis().SetTitleFont(42)
        dummy_ratio.GetXaxis().SetTickLength(0.05)
        dummy_ratio.GetYaxis().SetTickLength(0.05)
        dummy_ratio.GetXaxis().SetLabelSize(0.01/0.3)
        dummy_ratio.GetYaxis().SetLabelSize(0.01/0.3)
        dummy_ratio.GetXaxis().SetLabelOffset(0.01)
        dummy_ratio.GetYaxis().SetLabelOffset(0.01)
        dummy_ratio.GetYaxis().SetTitleOffset(1.5)
        dummy_ratio.GetXaxis().SetTitleOffset(1.5)
        dummy_ratio.GetYaxis().SetNdivisions(504)
        dummy_ratio.Draw()
        legend = ROOT.TLegend(0.15,0.65,0.85,0.88)
        legend.SetBorderSize(0)
        legend.SetNColumns(5)
#        print "%s_%s:%f"%(hname,"nominal",h_mc_nominal.GetSumOfWeights())
        for nsys in Dicit[hname]:
            if sys_name not in nsys:continue
            h_mc=Dicit[hname][nsys].Clone("ratio_%s_%s"%(hname,nsys))
#            print "%s_%s:%f"%(hname,nsys,h_mc.GetSumOfWeights())
            h_mc.Divide(h_mc_nominal)
            h_mc.SetLineWidth(line_width)
            h_mc.SetLineColor(color[nsys])
            h_mc.Draw("same:hist")
            legend.AddEntry(h_mc,dir_system_name[nsys],'l')
            dicit_dummy.append(h_mc)
        dummy_ratio.Draw("AXISSAME")
        legend.Draw()
        canvas.Print('%s/%s/%s_%s.png'%(dir,date,sys_name,hname))    
        del canvas
        gc.collect()
            
def Draw_all_system_ratio_v1(dir, date, Dicit, color, dir_hist, dir_system_name, sys_list, sys_name, shape_name):
    
    for hname in Dicit:
        canvas = ROOT.TCanvas('canvas_%s'%(hname),'',50,50,865,780)
        canvas.cd()
        canvas.cd()
        pad1=ROOT.TPad("pad1", "pad1", 0, 0, 0.8, 1  , 0)#used for the hist plot
        pad2=ROOT.TPad("pad2", "pad2", 0.8, 0, 1, 1  , 0)#used for the ratio plot
        pad1.Draw()
        pad2.Draw() 
        pad1.SetGridy()
        pad1.SetTickx()
        pad1.SetTicky()
        pad1.SetBottomMargin(0.1)
        pad1.SetTopMargin(0.08)
        pad1.SetLeftMargin(0.14)
        pad1.SetRightMargin(0.024)
        pad2.SetTopMargin(0.08)
        pad2.SetBottomMargin(0.04)
        pad2.SetRightMargin(0.15)
        pad1.cd()
        h_mc_nominal=Dicit[hname]["nominal"].Clone("%s_nominal"%(hname))
        x_min=h_mc_nominal.GetXaxis().GetXmin()
        x_max=h_mc_nominal.GetXaxis().GetXmax()
        line_width=2
        dicit_dummy=[]
        ratio_y_min=0.5
        ratio_y_max=1.5
        if "Sample_TT" not in sys_name and "Sample_ST_tW" not in sys_name:
            if "lepton" in hname:
                ratio_y_min=0.9
                ratio_y_max=1.1
            elif hname in ["H_N_loose_jets","H_N_b_jets","H_njet_bjet"]:
                ratio_y_min=0.8
                ratio_y_max=1.2
        nbin=h_mc_nominal.GetNbinsX()
        if hname == "H_Limit_N_jet_bjet":
            if Channel == "ee" or Channel=="mumu":
                x_min=2
                nbin=3
            elif Channel == "emu":
                x_min=1
                nbin=4
        dummy_ratio = ROOT.TH2F("dummy_ratio_%s"%(hname),"",nbin,x_min,x_max,1,ratio_y_min,ratio_y_max)
        dummy_ratio.SetStats(ROOT.kFALSE)
        dummy_ratio.GetYaxis().SetTitle('Relative uncertainty')
        dummy_ratio.GetYaxis().CenterTitle()
        dummy_ratio.GetXaxis().SetTitle("")
        if dir_hist[hname]:
            dummy_ratio.GetXaxis().SetTitle(dir_hist[hname])
        str_njet =["(0,0)","(1,0)","(1,1)","(2,0)","(2,1)","(2,2)","(3,0)","(3,1)","(3,2)","(3,3)","(4,0)","(4,1)","(4,2)","(4,3)","(4,4)"]
        str_njet_limit_emu=["(1,0)","(1,1)","(2,1)","(#geq2,2)"]
        str_njet_limit_ee_mumu=["(1,1)","(2,1)","(#geq2,2)"]
        if hname == "H_njet_bjet": 
            for str_j in str_njet:
                dummy_ratio.GetXaxis().SetBinLabel(str_njet.index(str_j)+1,str_j)
        elif hname == "H_Limit_N_jet_bjet": 
            if Channel == "emu":
                for str_j in str_njet_limit_emu:
                    dummy_ratio.GetXaxis().SetBinLabel(str_njet_limit_emu.index(str_j)+1,str_j)
            elif Channel == "ee" or Channel=="mumu":
                for str_j in str_njet_limit_ee_mumu:
                    dummy_ratio.GetXaxis().SetBinLabel(str_njet_limit_ee_mumu.index(str_j)+1,str_j)
        dummy_ratio.GetXaxis().SetMoreLogLabels()
        dummy_ratio.GetXaxis().SetNoExponent()  
        dummy_ratio.GetYaxis().SetMoreLogLabels()
        dummy_ratio.GetYaxis().SetNoExponent()  
        dummy_ratio.GetXaxis().SetTitleSize(0.04)
        dummy_ratio.GetYaxis().SetTitleSize(0.05)
        dummy_ratio.GetXaxis().SetTitleFont(42)
        dummy_ratio.GetYaxis().SetTitleFont(42)
        dummy_ratio.GetXaxis().SetTickLength(0.05)
        dummy_ratio.GetYaxis().SetTickLength(0.05)
        dummy_ratio.GetXaxis().SetLabelSize(0.012/0.3)
        dummy_ratio.GetYaxis().SetLabelSize(0.012/0.3)
        dummy_ratio.GetXaxis().SetLabelOffset(0.01)
        dummy_ratio.GetYaxis().SetLabelOffset(0.01)
        dummy_ratio.GetYaxis().SetTitleOffset(1.3)
        dummy_ratio.GetXaxis().SetTitleOffset(1.2)
        dummy_ratio.GetYaxis().SetNdivisions(510)
        dummy_ratio.Draw()
        legend = ROOT.TLegend(0.01,0.02,0.95,0.92)
        legend.SetBorderSize(1)
#        legend.SetNColumns(2)
        legend.SetLineColor(1)
        legend.SetLineStyle(1)
        legend.SetLineWidth(2)
        legend.SetFillColor(19)
        legend.SetFillStyle(0)
        legend.SetTextSize(0.1)
        font = 62#42
        legend.SetTextFont(font)
#        for nsys in Dicit[hname]:
        for nsys in sys_list:
            if Channel=="emu"     and "UnclusteredEn" in nsys:continue
            elif Channel=="ee"    and "Muon" in nsys:continue
            elif Channel=="mumu"  and "Ele" in nsys:continue
            use=False
            for isys in sys_name:
                if isys in nsys:
                    use=True
                    break 
            if use==False:continue
            #if sys_name not in nsys and "nominal" not in nsys:continue
            h_mc=Dicit[hname][nsys].Clone("ratio_%s_%s"%(hname,nsys))
            h_mc.Divide(h_mc_nominal)
            h_mc.SetLineWidth(line_width)
            if "Sample_" in nsys and "CR" not in nsys:
                cname=nsys.split("Sample_")[-1]
                h_mc.SetLineColor(color[cname].color)
            elif "CR" in nsys:
                h_mc.SetLineColor(color["TT_QCDbasedCRTune_erdON"].color)
            elif "isr" in nsys:
                h_mc.SetLineColor(color["TT_isrdown"].color)
            elif "fsr" in nsys:
                h_mc.SetLineColor(color["TT_fsrdown"].color)
            else:
                h_mc.SetLineColor(color[nsys].color)
            if "down" in nsys or "Down" in nsys or "DOWN" in nsys:
                h_mc.SetLineStyle(2)
                cname=nsys
                cname.replace("down","up")
                cname.replace("Down","Up")
                cname.replace("DOWN","UP")
            
            h_mc.Draw("same:hist")
            nlegend=dir_system_name[nsys]
            if "TT_" in nlegend:
                nlegend=nlegend.split("TT_")[-1]
            if "tw_" in nlegend:
                nlegend=nlegend.split("tw_")[-1]
            nlegend=nlegend.replace("JetEnergyResolution","JER") 
            nlegend=nlegend.replace("JetEnergyScale"     ,"JES") 
            nlegend=nlegend.replace("BtagScaleFactor"    ,"BSF") 
            nlegend=nlegend.replace("UnclusteredEn"      ,"UCEn") 
            legend.AddEntry(h_mc,nlegend,'l')
            dicit_dummy.append(h_mc)
        dummy_ratio.Draw("AXISSAME")
        Label_cms_prelim = ROOT.TPaveText(0.15,0.83,0.4,0.83,"NDC")
        Label_cms_prelim.SetLineColor(10)
        Label_cms_prelim.SetFillColor(10)
        Label_cms_prelim.SetTextSize(0.06)
        Label_cms_prelim.SetTextAlign(12)
        Label_cms_prelim.AddText("CMS Preliminary")
        Label_cms_prelim.SetShadowColor(10)
        Label_cms_prelim.Draw()
        Label_lumi = ROOT.TPaveText(0.6,0.93,0.85,0.98,"NDC")
        Label_lumi.SetLineColor(10)
        Label_lumi.SetFillColor(10)
        Label_lumi.SetTextSize(0.05)
        Label_lumi.SetTextAlign(12)
        Label_lumi.SetTextFont(42)
        Label_lumi.AddText("%.1f fb^{-1} (13 TeV)"%(float(Lumi)/1000))
        Label_lumi.SetShadowColor(10)
        Label_lumi.Draw()
        Label_chan=ROOT.TPaveText(0.18,0.72, 0.35,0.7,"blNDC")
        Label_chan.SetBorderSize(0)
        Label_chan.SetFillStyle(0)
        Label_chan.SetTextAlign(10)
        Label_chan.SetTextColor(1)
        Label_chan.SetTextFont(32)
        Label_chan.SetTextSize(0.1)
        if "ee" in Channel:
            if "Sample_TT" in sys_name:
                Label_chan.AddText ('t#bar{t}(ee)')
            elif "Sample_ST_tW" in sys_name:
                Label_chan.AddText ('tW(ee)')
            else:
                Label_chan.AddText ('ee')
        elif "emu" in Channel:
            if "Sample_TT" in sys_name:
                Label_chan.AddText ('t#bar{t}(e#mu)')
            elif "Sample_ST_tW" in sys_name:
                Label_chan.AddText ('tW(e#mu)')
            else:
                Label_chan.AddText ('e#mu')
        elif "mumu" in Channel:
            if "Sample_TT" in sys_name:
                Label_chan.AddText ('t#bar{t}(#mu#mu)')
            elif "Sample_ST_tW" in sys_name:
                Label_chan.AddText ('tW(#mu#mu)')
            else:
                Label_chan.AddText ('#mu#mu')
        Label_chan.Draw()
        pad2.cd()
        legend.Draw()
        canvas.Print('%s/%s/%s_%s.png'%(dir,date,shape_name,hname))    
        del canvas
        gc.collect()

def quadratic_sum(*args):
    N=len(args)
#    print "get %d inout"%(N)
    if N==0:
        print" Error no input"
        return
    h_out=args[0].Clone("%s_quad_sum"%(args[0].GetName()))
    for ibin in range(1,h_out.GetNbinsX()+1):
        value=0
        error=0
        for ih in range(0,N):
            error=math.sqrt((math.pow(value*error,2)+math.pow(args[ih].GetBinContent(ibin)*args[ih].GetBinError(ibin),2))/(math.pow(value,2)+math.pow(args[ih].GetBinContent(ibin),2))) if (math.pow(value,2)+math.pow(args[ih].GetBinContent(ibin),2))!=0 else 0
            value=math.sqrt(math.pow(value,2)+math.pow(args[ih].GetBinContent(ibin),2))
        value=float(value)/math.sqrt(N)
        error=float(error)/math.sqrt(N)
        h_out.SetBinContent(ibin,value)
        h_out.SetBinError  (ibin,error)
    return h_out


def stat_up_down(hist,is_Up):
    if is_Up:
        for ibin in range(1,hist.GetNbinsX()+1):
            value=hist.GetBinContent(ibin)+hist.GetBinError(ibin) if hist.GetBinContent(ibin)+hist.GetBinError(ibin) >0 else 0
            hist.SetBinContent(ibin,value)
    else:
        for ibin in range(1,hist.GetNbinsX()+1):
            value=hist.GetBinContent(ibin)-hist.GetBinError(ibin) if hist.GetBinContent(ibin)-hist.GetBinError(ibin) >0 else 0
            hist.SetBinContent(ibin,value)

def change_zero_bin(hist):
    for ibin in range(1,hist.GetNbinsX()+1):   
         if hist.GetBinContent(ibin)<=0:
             hist.SetBinContent(ibin,1E-6)
             hist.SetBinError  (ibin,1E-6)

def stat_uncertainty(hist, chan_region_name):
    tmp_hist_list=[]
    for ibin in range(1,hist.GetNbinsX()+1):
        bin_up  =hist.GetBinContent(ibin)+hist.GetBinError(ibin)
        bin_down=hist.GetBinContent(ibin)-hist.GetBinError(ibin) if hist.GetBinContent(ibin)-hist.GetBinError(ibin) >=0 else 0
        tmp_hist_up  =hist.Clone(hist.GetName()+"_"+chan_region_name+hist.GetName()+"_stat_bin%s_Up"%(str(ibin)))
        tmp_hist_up  .SetBinContent(ibin,bin_up)
        tmp_hist_down=hist.Clone(hist.GetName()+"_"+chan_region_name+hist.GetName()+"_stat_bin%s_Down"%(str(ibin)))
        tmp_hist_down.SetBinContent(ibin,bin_down)
        tmp_hist_list.append(tmp_hist_up)
        tmp_hist_list.append(tmp_hist_down)
    return tmp_hist_list


def save_uncertainty_table(out_name, dicti,chan):
    template_emu='''
\\begin{table}[]
\centering
\caption{%(process)s systematic uncertainty effect for %(chan)s channel}
\label{tab:%(chan)s_%(process)s}
\scalebox{0.8}{
\\begin{tabular}{|l|c|c|c|c|c|}
\hline
%(process)s                                 & all                                              & 1jet, 0bjet                                       & 1jet, 1bjet                                       & 2jet, 1bjet                                      & $>=2$jet, 2bjet     \\\\ \hline
%(nominal)s                                 & %(nominal_all)s                                  & %(nominal_1j0t)s                                  & %(nominal_1j1t)s                                  & %(nominal_2j1t)s                                 & %(nominal_2j2t)s             \\\\ \hline \hline
%(luminosity_up)s                           & %(luminosity_up_all)s                            & %(luminosity_up_1j0t)s                            & %(luminosity_up_1j1t)s                            & %(luminosity_up_2j1t)s                           & %(luminosity_up_2j2t)s                            \\\\ \hline 
%(luminosity_down)s                         & %(luminosity_down_all)s                          & %(luminosity_down_1j0t)s                          & %(luminosity_down_1j1t)s                          & %(luminosity_down_2j1t)s                         & %(luminosity_down_2j2t)s                          \\\\ \hline 
%(bgk_DYJetsToLL_M10to50_amc_DYJetsToLL_M50_amc_scale_up)s  & %(bgk_DYJetsToLL_M10to50_amc_DYJetsToLL_M50_amc_scale_up_all)s   & %(bgk_DYJetsToLL_M10to50_amc_DYJetsToLL_M50_amc_scale_up_1j0t)s   & %(bgk_DYJetsToLL_M10to50_amc_DYJetsToLL_M50_amc_scale_up_1j1t)s   & %(bgk_DYJetsToLL_M10to50_amc_DYJetsToLL_M50_amc_scale_up_2j1t)s  & %(bgk_DYJetsToLL_M10to50_amc_DYJetsToLL_M50_amc_scale_up_2j2t)s   \\\\ \hline 
%(bgk_DYJetsToLL_M10to50_amc_DYJetsToLL_M50_amc_scale_down)s& %(bgk_DYJetsToLL_M10to50_amc_DYJetsToLL_M50_amc_scale_down_all)s & %(bgk_DYJetsToLL_M10to50_amc_DYJetsToLL_M50_amc_scale_down_1j0t)s & %(bgk_DYJetsToLL_M10to50_amc_DYJetsToLL_M50_amc_scale_down_1j1t)s & %(bgk_DYJetsToLL_M10to50_amc_DYJetsToLL_M50_amc_scale_down_2j1t)s& %(bgk_DYJetsToLL_M10to50_amc_DYJetsToLL_M50_amc_scale_down_2j2t)s \\\\ \hline 
%(bgk_WJet_scale_up)s                       & %(bgk_WJet_scale_up_all)s                        & %(bgk_WJet_scale_up_1j0t)s                        & %(bgk_WJet_scale_up_1j1t)s                        & %(bgk_WJet_scale_up_2j1t)s                       & %(bgk_WJet_scale_up_2j2t)s                        \\\\ \hline 
%(bgk_WJet_scale_down)s                     & %(bgk_WJet_scale_down_all)s                      & %(bgk_WJet_scale_down_1j0t)s                      & %(bgk_WJet_scale_down_1j1t)s                      & %(bgk_WJet_scale_down_2j1t)s                     & %(bgk_WJet_scale_down_2j2t)s                      \\\\ \hline 
%(other_scale_up)s                          & %(other_scale_up_all)s                           & %(other_scale_up_1j0t)s                           & %(other_scale_up_1j1t)s                           & %(other_scale_up_2j1t)s                          & %(other_scale_up_2j2t)s                           \\\\ \hline 
%(other_scale_down)s                        & %(other_scale_down_all)s                         & %(other_scale_down_1j0t)s                         & %(other_scale_down_1j1t)s                         & %(other_scale_down_2j1t)s                        & %(other_scale_down_2j2t)s                         \\\\ \hline \hline 
%(TrigSF_up)s                               & %(TrigSF_up_all)s                                & %(TrigSF_up_1j0t)s                                & %(TrigSF_up_1j1t)s                                & %(TrigSF_up_2j1t)s                               & %(TrigSF_up_2j2t)s                                \\\\ \hline 
%(TrigSF_down)s                             & %(TrigSF_down_all)s                              & %(TrigSF_down_1j0t)s                              & %(TrigSF_down_1j1t)s                              & %(TrigSF_down_2j1t)s                             & %(TrigSF_down_2j2t)s                              \\\\ \hline 
%(PU_scale_up)s                             & %(PU_scale_up_all)s                              & %(PU_scale_up_1j0t)s                              & %(PU_scale_up_1j1t)s                              & %(PU_scale_up_2j1t)s                             & %(PU_scale_up_2j2t)s                              \\\\ \hline 
%(PU_scale_down)s                           & %(PU_scale_down_all)s                            & %(PU_scale_down_1j0t)s                            & %(PU_scale_down_1j1t)s                            & %(PU_scale_down_2j1t)s                           & %(PU_scale_down_2j2t)s                            \\\\ \hline 
%(SmearedJetResUp)s                         & %(SmearedJetResUp_all)s                          & %(SmearedJetResUp_1j0t)s                          & %(SmearedJetResUp_1j1t)s                          & %(SmearedJetResUp_2j1t)s                         & %(SmearedJetResUp_2j2t)s                          \\\\ \hline     
%(SmearedJetResDown)s                       & %(SmearedJetResDown_all)s                        & %(SmearedJetResDown_1j0t)s                        & %(SmearedJetResDown_1j1t)s                        & %(SmearedJetResDown_2j1t)s                       & %(SmearedJetResDown_2j2t)s                        \\\\ \hline    
%(JetEnUp)s                                 & %(JetEnUp_all)s                                  & %(JetEnUp_1j0t)s                                  & %(JetEnUp_1j1t)s                                  & %(JetEnUp_2j1t)s                                 & %(JetEnUp_2j2t)s                                  \\\\ \hline    
%(JetEnDown)s                               & %(JetEnDown_all)s                                & %(JetEnDown_1j0t)s                                & %(JetEnDown_1j1t)s                                & %(JetEnDown_2j1t)s                               & %(JetEnDown_2j2t)s                                \\\\ \hline    
%(BtagSFbcUp)s                              & %(BtagSFbcUp_all)s                               & %(BtagSFbcUp_1j0t)s                               & %(BtagSFbcUp_1j1t)s                               & %(BtagSFbcUp_2j1t)s                              & %(BtagSFbcUp_2j2t)s                               \\\\ \hline    
%(BtagSFbcDown)s                            & %(BtagSFbcDown_all)s                             & %(BtagSFbcDown_1j0t)s                             & %(BtagSFbcDown_1j1t)s                             & %(BtagSFbcDown_2j1t)s                            & %(BtagSFbcDown_2j2t)s                             \\\\ \hline    
%(BtagSFudsgUp)s                            & %(BtagSFudsgUp_all)s                             & %(BtagSFudsgUp_1j0t)s                             & %(BtagSFudsgUp_1j1t)s                             & %(BtagSFudsgUp_2j1t)s                            & %(BtagSFudsgUp_2j2t)s                             \\\\ \hline     
%(BtagSFudsgDown)s                          & %(BtagSFudsgDown_all)s                           & %(BtagSFudsgDown_1j0t)s                           & %(BtagSFudsgDown_1j1t)s                           & %(BtagSFudsgDown_2j1t)s                          & %(BtagSFudsgDown_2j2t)s                           \\\\ \hline     
%(EleSFReco_up)s                            & %(EleSFReco_up_all)s                             & %(EleSFReco_up_1j0t)s                             & %(EleSFReco_up_1j1t)s                             & %(EleSFReco_up_2j1t)s                            & %(EleSFReco_up_2j2t)s                             \\\\ \hline    
%(EleSFReco_down)s                          & %(EleSFReco_down_all)s                           & %(EleSFReco_down_1j0t)s                           & %(EleSFReco_down_1j1t)s                           & %(EleSFReco_down_2j1t)s                          & %(EleSFReco_down_2j2t)s                           \\\\ \hline    
%(EleSFID_up)s                              & %(EleSFID_up_all)s                               & %(EleSFID_up_1j0t)s                               & %(EleSFID_up_1j1t)s                               & %(EleSFID_up_2j1t)s                              & %(EleSFID_up_2j2t)s                               \\\\ \hline    
%(EleSFID_down)s                            & %(EleSFID_down_all)s                             & %(EleSFID_down_1j0t)s                             & %(EleSFID_down_1j1t)s                             & %(EleSFID_down_2j1t)s                            & %(EleSFID_down_2j2t)s                             \\\\ \hline        
%(MuonSFID_up)s                             & %(MuonSFID_up_all)s                              & %(MuonSFID_up_1j0t)s                              & %(MuonSFID_up_1j1t)s                              & %(MuonSFID_up_2j1t)s                             & %(MuonSFID_up_2j2t)s                              \\\\ \hline    
%(MuonSFID_down)s                           & %(MuonSFID_down_all)s                            & %(MuonSFID_down_1j0t)s                            & %(MuonSFID_down_1j1t)s                            & %(MuonSFID_down_2j1t)s                           & %(MuonSFID_down_2j2t)s                            \\\\ \hline    
%(MuonSFIso_up)s                            & %(MuonSFIso_up_all)s                             & %(MuonSFIso_up_1j0t)s                             & %(MuonSFIso_up_1j1t)s                             & %(MuonSFIso_up_2j1t)s                            & %(MuonSFIso_up_2j2t)s                             \\\\ \hline           
%(MuonSFIso_down)s                          & %(MuonSFIso_down_all)s                           & %(MuonSFIso_down_1j0t)s                           & %(MuonSFIso_down_1j1t)s                           & %(MuonSFIso_down_2j1t)s                          & %(MuonSFIso_down_2j2t)s                           \\\\ \hline    
%(MuonSFtrack_up)s                          & %(MuonSFtrack_up_all)s                           & %(MuonSFtrack_up_1j0t)s                           & %(MuonSFtrack_up_1j1t)s                           & %(MuonSFtrack_up_2j1t)s                          & %(MuonSFtrack_up_2j2t)s                           \\\\ \hline    
%(MuonSFtrack_down)s                        & %(MuonSFtrack_down_all)s                         & %(MuonSFtrack_down_1j0t)s                         & %(MuonSFtrack_down_1j1t)s                         & %(MuonSFtrack_down_2j1t)s                        & %(MuonSFtrack_down_2j2t)s                         \\\\ \hline \hline 
%(isrdown)s                              & %(isrdown_all)s                                     & %(isrdown_1j0t)s                                  & %(isrdown_1j1t)s                                  & %(isrdown_2j1t)s                                    & %(isrdown_2j2t)s                               \\\\ \hline
%(isrup)s                                & %(isrup_all)s                                       & %(isrup_1j0t)s                                    & %(isrup_1j1t)s                                    & %(isrup_2j1t)s                                      & %(isrup_2j2t)s                                 \\\\ \hline
%(fsrdown)s                              & %(fsrdown_all)s                                     & %(fsrdown_1j0t)s                                  & %(fsrdown_1j1t)s                                  & %(fsrdown_2j1t)s                                    & %(fsrdown_2j2t)s                               \\\\ \hline
%(fsrup)s                                & %(fsrup_all)s                                       & %(fsrup_1j0t)s                                    & %(fsrup_1j1t)s                                    & %(fsrup_2j1t)s                                      & %(fsrup_2j2t)s                                 \\\\ \hline 
%(Sample_TT_TuneEE5C)s                      & %(Sample_TT_TuneEE5C_all)s                       & %(Sample_TT_TuneEE5C_1j0t)s                       & %(Sample_TT_TuneEE5C_1j1t)s                       & %(Sample_TT_TuneEE5C_2j1t)s                      & %(Sample_TT_TuneEE5C_2j2t)s                       \\\\ \hline         
%(Sample_TT_CR)s                            & %(Sample_TT_CR_all)s                             & %(Sample_TT_CR_1j0t)s                             & %(Sample_TT_CR_1j1t)s                             & %(Sample_TT_CR_2j1t)s                            & %(Sample_TT_CR_2j2t)s                             \\\\ \hline        
%(Sample_TT_PDF_Up)s                        & %(Sample_TT_PDF_Up_all)s                         & %(Sample_TT_PDF_Up_1j0t)s                         & %(Sample_TT_PDF_Up_1j1t)s                         & %(Sample_TT_PDF_Up_2j1t)s                        & %(Sample_TT_PDF_Up_2j2t)s                         \\\\ \hline    
%(Sample_TT_PDF_Down)s                      & %(Sample_TT_PDF_Down_all)s                       & %(Sample_TT_PDF_Down_1j0t)s                       & %(Sample_TT_PDF_Down_1j1t)s                       & %(Sample_TT_PDF_Down_2j1t)s                      & %(Sample_TT_PDF_Down_2j2t)s                       \\\\ \hline    
%(Sample_TT_mtop1695)s                      & %(Sample_TT_mtop1695_all)s                       & %(Sample_TT_mtop1695_1j0t)s                       & %(Sample_TT_mtop1695_1j1t)s                       & %(Sample_TT_mtop1695_2j1t)s                      & %(Sample_TT_mtop1695_2j2t)s                       \\\\ \hline    
%(Sample_TT_mtop1755)s                      & %(Sample_TT_mtop1755_all)s                       & %(Sample_TT_mtop1755_1j0t)s                       & %(Sample_TT_mtop1755_1j1t)s                       & %(Sample_TT_mtop1755_2j1t)s                      & %(Sample_TT_mtop1755_2j2t)s                       \\\\ \hline        
%(Sample_TT_TuneCUETP8M2T4down)s            & %(Sample_TT_TuneCUETP8M2T4down_all)s             & %(Sample_TT_TuneCUETP8M2T4down_1j0t)s             & %(Sample_TT_TuneCUETP8M2T4down_1j1t)s             & %(Sample_TT_TuneCUETP8M2T4down_2j1t)s            & %(Sample_TT_TuneCUETP8M2T4down_2j2t)s             \\\\ \hline      
%(Sample_TT_TuneCUETP8M2T4up)s              & %(Sample_TT_TuneCUETP8M2T4up_all)s               & %(Sample_TT_TuneCUETP8M2T4up_1j0t)s               & %(Sample_TT_TuneCUETP8M2T4up_1j1t)s               & %(Sample_TT_TuneCUETP8M2T4up_2j1t)s              & %(Sample_TT_TuneCUETP8M2T4up_2j2t)s               \\\\ \hline    
%(Sample_TT_hdampDOWN)s                  & %(Sample_TT_hdampDOWN_all)s                         & %(Sample_TT_hdampDOWN_1j0t)s                      & %(Sample_TT_hdampDOWN_1j1t)s                      & %(Sample_TT_hdampDOWN_2j1t)s                        & %(Sample_TT_hdampDOWN_2j2t)s                   \\\\ \hline
%(Sample_TT_hdampUP)s                    & %(Sample_TT_hdampUP_all)s                           & %(Sample_TT_hdampUP_1j0t)s                        & %(Sample_TT_hdampUP_1j1t)s                        & %(Sample_TT_hdampUP_2j1t)s                          & %(Sample_TT_hdampUP_2j2t)s                     \\\\ \hline
%(Sample_ST_tW_herwigpp)s                & %(Sample_ST_tW_herwigpp_all)s                       & %(Sample_ST_tW_herwigpp_1j0t)s                    & %(Sample_ST_tW_herwigpp_1j1t)s                    & %(Sample_ST_tW_herwigpp_2j1t)s                      & %(Sample_ST_tW_herwigpp_2j2t)s                 \\\\ \hline
%(Sample_ST_tW_DS)s                      & %(Sample_ST_tW_DS_all)s                             & %(Sample_ST_tW_DS_1j0t)s                          & %(Sample_ST_tW_DS_1j1t)s                          & %(Sample_ST_tW_DS_2j1t)s                            & %(Sample_ST_tW_DS_2j2t)s                       \\\\ \hline
%(Sample_ST_tW_mtop1695)s                & %(Sample_ST_tW_mtop1695_all)s                       & %(Sample_ST_tW_mtop1695_1j0t)s                    & %(Sample_ST_tW_mtop1695_1j1t)s                    & %(Sample_ST_tW_mtop1695_2j1t)s                      & %(Sample_ST_tW_mtop1695_2j2t)s                 \\\\ \hline
%(Sample_ST_tW_mtop1755)s                & %(Sample_ST_tW_mtop1755_all)s                       & %(Sample_ST_tW_mtop1755_1j0t)s                    & %(Sample_ST_tW_mtop1755_1j1t)s                    & %(Sample_ST_tW_mtop1755_2j1t)s                      & %(Sample_ST_tW_mtop1755_2j2t)s                 \\\\ \hline
%(Sample_ST_tW_MEscaledown)s             & %(Sample_ST_tW_MEscaledown_all)s                    & %(Sample_ST_tW_MEscaledown_1j0t)s                 & %(Sample_ST_tW_MEscaledown_1j1t)s                 & %(Sample_ST_tW_MEscaledown_2j1t)s                   & %(Sample_ST_tW_MEscaledown_2j2t)s              \\\\ \hline
%(Sample_ST_tW_MEscaleup)s               & %(Sample_ST_tW_MEscaleup_all)s                      & %(Sample_ST_tW_MEscaleup_1j0t)s                   & %(Sample_ST_tW_MEscaleup_1j1t)s                   & %(Sample_ST_tW_MEscaleup_2j1t)s                     & %(Sample_ST_tW_MEscaleup_2j2t)s                \\\\ \hline
%(total_scale_up)s                          & %(total_scale_up_all)s                           & %(total_scale_up_1j0t)s                           & %(total_scale_up_1j1t)s                           & %(total_scale_up_2j1t)s                          & %(total_scale_up_2j2t)s                           \\\\ \hline 
%(total_scale_down)s                        & %(total_scale_down_all)s                         & %(total_scale_down_1j0t)s                         & %(total_scale_down_1j1t)s                         & %(total_scale_down_2j1t)s                        & %(total_scale_down_2j2t)s                         \\\\ \hline \hline 
\end{tabular}}
\end{table}
'''
    template_ee='''
\\begin{table}[]
\centering
\caption{%(process)s systematic uncertainty effect for %(chan)s channel}
\label{tab:%(chan)s_%(process)s}
\scalebox{0.8}{
\\begin{tabular}{|l|c|c|c|c|}
\hline
%(process)s                                 & all                                              & 1jet, 1bjet                                       & 2jet, 1bjet                                      & $>=2$jet, 2bjet     \\\\ \hline
%(nominal)s                                 & %(nominal_all)s                                  & %(nominal_1j1t)s                                  & %(nominal_2j1t)s                                 & %(nominal_2j2t)s             \\\\ \hline \hline
%(luminosity_up)s                           & %(luminosity_up_all)s                            & %(luminosity_up_1j1t)s                            & %(luminosity_up_2j1t)s                           & %(luminosity_up_2j2t)s                            \\\\ \hline 
%(luminosity_down)s                         & %(luminosity_down_all)s                          & %(luminosity_down_1j1t)s                          & %(luminosity_down_2j1t)s                         & %(luminosity_down_2j2t)s                          \\\\ \hline 
%(bgk_DYJetsToLL_M10to50_amc_DYJetsToLL_M50_amc_scale_up)s  & %(bgk_DYJetsToLL_M10to50_amc_DYJetsToLL_M50_amc_scale_up_all)s   & %(bgk_DYJetsToLL_M10to50_amc_DYJetsToLL_M50_amc_scale_up_1j1t)s   & %(bgk_DYJetsToLL_M10to50_amc_DYJetsToLL_M50_amc_scale_up_2j1t)s  & %(bgk_DYJetsToLL_M10to50_amc_DYJetsToLL_M50_amc_scale_up_2j2t)s   \\\\ \hline 
%(bgk_DYJetsToLL_M10to50_amc_DYJetsToLL_M50_amc_scale_down)s& %(bgk_DYJetsToLL_M10to50_amc_DYJetsToLL_M50_amc_scale_down_all)s & %(bgk_DYJetsToLL_M10to50_amc_DYJetsToLL_M50_amc_scale_down_1j1t)s & %(bgk_DYJetsToLL_M10to50_amc_DYJetsToLL_M50_amc_scale_down_2j1t)s& %(bgk_DYJetsToLL_M10to50_amc_DYJetsToLL_M50_amc_scale_down_2j2t)s \\\\ \hline 
%(bgk_WJet_scale_up)s                       & %(bgk_WJet_scale_up_all)s                        & %(bgk_WJet_scale_up_1j1t)s                        & %(bgk_WJet_scale_up_2j1t)s                       & %(bgk_WJet_scale_up_2j2t)s                        \\\\ \hline 
%(bgk_WJet_scale_down)s                     & %(bgk_WJet_scale_down_all)s                      & %(bgk_WJet_scale_down_1j1t)s                      & %(bgk_WJet_scale_down_2j1t)s                     & %(bgk_WJet_scale_down_2j2t)s                      \\\\ \hline 
%(other_scale_up)s                          & %(other_scale_up_all)s                           & %(other_scale_up_1j1t)s                           & %(other_scale_up_2j1t)s                          & %(other_scale_up_2j2t)s                           \\\\ \hline 
%(other_scale_down)s                        & %(other_scale_down_all)s                         & %(other_scale_down_1j1t)s                         & %(other_scale_down_2j1t)s                        & %(other_scale_down_2j2t)s                         \\\\ \hline \hline 
%(TrigSF_up)s                               & %(TrigSF_up_all)s                                & %(TrigSF_up_1j1t)s                                & %(TrigSF_up_2j1t)s                               & %(TrigSF_up_2j2t)s                                \\\\ \hline 
%(TrigSF_down)s                             & %(TrigSF_down_all)s                              & %(TrigSF_down_1j1t)s                              & %(TrigSF_down_2j1t)s                             & %(TrigSF_down_2j2t)s                              \\\\ \hline 
%(PU_scale_up)s                             & %(PU_scale_up_all)s                              & %(PU_scale_up_1j1t)s                              & %(PU_scale_up_2j1t)s                             & %(PU_scale_up_2j2t)s                              \\\\ \hline 
%(PU_scale_down)s                           & %(PU_scale_down_all)s                            & %(PU_scale_down_1j1t)s                            & %(PU_scale_down_2j1t)s                           & %(PU_scale_down_2j2t)s                            \\\\ \hline 
%(SmearedJetResUp)s                         & %(SmearedJetResUp_all)s                          & %(SmearedJetResUp_1j1t)s                          & %(SmearedJetResUp_2j1t)s                         & %(SmearedJetResUp_2j2t)s                          \\\\ \hline     
%(SmearedJetResDown)s                       & %(SmearedJetResDown_all)s                        & %(SmearedJetResDown_1j1t)s                        & %(SmearedJetResDown_2j1t)s                       & %(SmearedJetResDown_2j2t)s                        \\\\ \hline    
%(JetEnUp)s                                 & %(JetEnUp_all)s                                  & %(JetEnUp_1j1t)s                                  & %(JetEnUp_2j1t)s                                 & %(JetEnUp_2j2t)s                                  \\\\ \hline    
%(JetEnDown)s                               & %(JetEnDown_all)s                                & %(JetEnDown_1j1t)s                                & %(JetEnDown_2j1t)s                               & %(JetEnDown_2j2t)s                                \\\\ \hline    
%(BtagSFbcUp)s                              & %(BtagSFbcUp_all)s                               & %(BtagSFbcUp_1j1t)s                               & %(BtagSFbcUp_2j1t)s                              & %(BtagSFbcUp_2j2t)s                               \\\\ \hline    
%(BtagSFbcDown)s                            & %(BtagSFbcDown_all)s                             & %(BtagSFbcDown_1j1t)s                             & %(BtagSFbcDown_2j1t)s                            & %(BtagSFbcDown_2j2t)s                             \\\\ \hline    
%(BtagSFudsgUp)s                            & %(BtagSFudsgUp_all)s                             & %(BtagSFudsgUp_1j1t)s                             & %(BtagSFudsgUp_2j1t)s                            & %(BtagSFudsgUp_2j2t)s                             \\\\ \hline     
%(BtagSFudsgDown)s                          & %(BtagSFudsgDown_all)s                           & %(BtagSFudsgDown_1j1t)s                           & %(BtagSFudsgDown_2j1t)s                          & %(BtagSFudsgDown_2j2t)s                           \\\\ \hline     
%(EleSFReco_up)s                            & %(EleSFReco_up_all)s                             & %(EleSFReco_up_1j1t)s                             & %(EleSFReco_up_2j1t)s                            & %(EleSFReco_up_2j2t)s                             \\\\ \hline    
%(EleSFReco_down)s                          & %(EleSFReco_down_all)s                           & %(EleSFReco_down_1j1t)s                           & %(EleSFReco_down_2j1t)s                          & %(EleSFReco_down_2j2t)s                           \\\\ \hline    
%(EleSFID_up)s                              & %(EleSFID_up_all)s                               & %(EleSFID_up_1j1t)s                               & %(EleSFID_up_2j1t)s                              & %(EleSFID_up_2j2t)s                               \\\\ \hline    
%(EleSFID_down)s                            & %(EleSFID_down_all)s                             & %(EleSFID_down_1j1t)s                             & %(EleSFID_down_2j1t)s                            & %(EleSFID_down_2j2t)s                             \\\\ \hline        
%(UnclusteredEnUp)s                         & %(UnclusteredEnUp_all)s                          & %(UnclusteredEnUp_1j1t)s                          & %(UnclusteredEnUp_2j1t)s                         & %(UnclusteredEnUp_2j2t)s                          \\\\ \hline    
%(UnclusteredEnDown)s                      & %(UnclusteredEnDown_all)s                         & %(UnclusteredEnDown_1j1t)s                        & %(UnclusteredEnDown_2j1t)s                       & %(UnclusteredEnDown_2j2t)s                        \\\\ \hline   \hline 
%(isrdown)s                                & %(isrdown_all)s                                   & %(isrdown_1j1t)s                                  & %(isrdown_2j1t)s                                 & %(isrdown_2j2t)s                                  \\\\ \hline
%(isrup)s                                  & %(isrup_all)s                                     & %(isrup_1j1t)s                                    & %(isrup_2j1t)s                                   & %(isrup_2j2t)s                                    \\\\ \hline
%(fsrdown)s                                & %(fsrdown_all)s                                   & %(fsrdown_1j1t)s                                  & %(fsrdown_2j1t)s                                 & %(fsrdown_2j2t)s                                  \\\\ \hline
%(fsrup)s                                  & %(fsrup_all)s                                     & %(fsrup_1j1t)s                                    & %(fsrup_2j1t)s                                   & %(fsrup_2j2t)s                                    \\\\ \hline 
%(Sample_TT_TuneEE5C)s                      & %(Sample_TT_TuneEE5C_all)s                       & %(Sample_TT_TuneEE5C_1j1t)s                       & %(Sample_TT_TuneEE5C_2j1t)s                      & %(Sample_TT_TuneEE5C_2j2t)s                       \\\\ \hline         
%(Sample_TT_CR)s                            & %(Sample_TT_CR_all)s                             & %(Sample_TT_CR_1j1t)s                             & %(Sample_TT_CR_2j1t)s                            & %(Sample_TT_CR_2j2t)s                             \\\\ \hline        
%(Sample_TT_PDF_Up)s                        & %(Sample_TT_PDF_Up_all)s                         & %(Sample_TT_PDF_Up_1j1t)s                         & %(Sample_TT_PDF_Up_2j1t)s                        & %(Sample_TT_PDF_Up_2j2t)s                       \\\\ \hline    
%(Sample_TT_PDF_Down)s                      & %(Sample_TT_PDF_Down_all)s                       & %(Sample_TT_PDF_Down_1j1t)s                       & %(Sample_TT_PDF_Down_2j1t)s                      & %(Sample_TT_PDF_Down_2j2t)s                       \\\\ \hline    
%(Sample_TT_mtop1695)s                      & %(Sample_TT_mtop1695_all)s                       & %(Sample_TT_mtop1695_1j1t)s                       & %(Sample_TT_mtop1695_2j1t)s                      & %(Sample_TT_mtop1695_2j2t)s                       \\\\ \hline    
%(Sample_TT_mtop1755)s                      & %(Sample_TT_mtop1755_all)s                       & %(Sample_TT_mtop1755_1j1t)s                       & %(Sample_TT_mtop1755_2j1t)s                      & %(Sample_TT_mtop1755_2j2t)s                       \\\\ \hline        
%(Sample_TT_TuneCUETP8M2T4down)s            & %(Sample_TT_TuneCUETP8M2T4down_all)s             & %(Sample_TT_TuneCUETP8M2T4down_1j1t)s             & %(Sample_TT_TuneCUETP8M2T4down_2j1t)s            & %(Sample_TT_TuneCUETP8M2T4down_2j2t)s             \\\\ \hline      
%(Sample_TT_TuneCUETP8M2T4up)s              & %(Sample_TT_TuneCUETP8M2T4up_all)s               & %(Sample_TT_TuneCUETP8M2T4up_1j1t)s               & %(Sample_TT_TuneCUETP8M2T4up_2j1t)s              & %(Sample_TT_TuneCUETP8M2T4up_2j2t)s               \\\\ \hline    
%(Sample_TT_hdampDOWN)s                  & %(Sample_TT_hdampDOWN_all)s                         & %(Sample_TT_hdampDOWN_1j1t)s                      & %(Sample_TT_hdampDOWN_2j1t)s                        & %(Sample_TT_hdampDOWN_2j2t)s                   \\\\ \hline
%(Sample_TT_hdampUP)s                    & %(Sample_TT_hdampUP_all)s                           & %(Sample_TT_hdampUP_1j1t)s                        & %(Sample_TT_hdampUP_2j1t)s                          & %(Sample_TT_hdampUP_2j2t)s                     \\\\ \hline
%(Sample_ST_tW_herwigpp)s                & %(Sample_ST_tW_herwigpp_all)s                       & %(Sample_ST_tW_herwigpp_1j1t)s                    & %(Sample_ST_tW_herwigpp_2j1t)s                      & %(Sample_ST_tW_herwigpp_2j2t)s                 \\\\ \hline
%(Sample_ST_tW_DS)s                      & %(Sample_ST_tW_DS_all)s                             & %(Sample_ST_tW_DS_1j1t)s                          & %(Sample_ST_tW_DS_2j1t)s                            & %(Sample_ST_tW_DS_2j2t)s                       \\\\ \hline
%(Sample_ST_tW_mtop1695)s                & %(Sample_ST_tW_mtop1695_all)s                       & %(Sample_ST_tW_mtop1695_1j1t)s                    & %(Sample_ST_tW_mtop1695_2j1t)s                      & %(Sample_ST_tW_mtop1695_2j2t)s                 \\\\ \hline
%(Sample_ST_tW_mtop1755)s                & %(Sample_ST_tW_mtop1755_all)s                       & %(Sample_ST_tW_mtop1755_1j1t)s                    & %(Sample_ST_tW_mtop1755_2j1t)s                      & %(Sample_ST_tW_mtop1755_2j2t)s                 \\\\ \hline
%(Sample_ST_tW_MEscaledown)s             & %(Sample_ST_tW_MEscaledown_all)s                    & %(Sample_ST_tW_MEscaledown_1j1t)s                 & %(Sample_ST_tW_MEscaledown_2j1t)s                   & %(Sample_ST_tW_MEscaledown_2j2t)s              \\\\ \hline
%(Sample_ST_tW_MEscaleup)s               & %(Sample_ST_tW_MEscaleup_all)s                      & %(Sample_ST_tW_MEscaleup_1j1t)s                   & %(Sample_ST_tW_MEscaleup_2j1t)s                     & %(Sample_ST_tW_MEscaleup_2j2t)s                \\\\ \hline
%(total_scale_up)s                          & %(total_scale_up_all)s                           & %(total_scale_up_1j1t)s                           & %(total_scale_up_2j1t)s                          & %(total_scale_up_2j2t)s                           \\\\ \hline 
%(total_scale_down)s                        & %(total_scale_down_all)s                         & %(total_scale_down_1j1t)s                         & %(total_scale_down_2j1t)s                        & %(total_scale_down_2j2t)s                         \\\\ \hline \hline 
\end{tabular}}
\end{table}
'''
    template_mumu='''
\\begin{table}[]
\centering
\caption{%(process)s systematic uncertainty effect for %(chan)s channel}
\label{tab:%(chan)s_%(process)s}
\scalebox{0.8}{
\\begin{tabular}{|l|c|c|c|c|}
\hline
%(process)s                                 & all                                              & 1jet, 1bjet                                       & 2jet, 1bjet                                      & $>=2$jet, 2bjet     \\\\ \hline
%(nominal)s                                 & %(nominal_all)s                                  & %(nominal_1j1t)s                                  & %(nominal_2j1t)s                                 & %(nominal_2j2t)s             \\\\ \hline \hline
%(luminosity_up)s                           & %(luminosity_up_all)s                            & %(luminosity_up_1j1t)s                            & %(luminosity_up_2j1t)s                           & %(luminosity_up_2j2t)s                            \\\\ \hline 
%(luminosity_down)s                         & %(luminosity_down_all)s                          & %(luminosity_down_1j1t)s                          & %(luminosity_down_2j1t)s                         & %(luminosity_down_2j2t)s                          \\\\ \hline 
%(bgk_DYJetsToLL_M10to50_amc_DYJetsToLL_M50_amc_scale_up)s  & %(bgk_DYJetsToLL_M10to50_amc_DYJetsToLL_M50_amc_scale_up_all)s   & %(bgk_DYJetsToLL_M10to50_amc_DYJetsToLL_M50_amc_scale_up_1j1t)s   & %(bgk_DYJetsToLL_M10to50_amc_DYJetsToLL_M50_amc_scale_up_2j1t)s  & %(bgk_DYJetsToLL_M10to50_amc_DYJetsToLL_M50_amc_scale_up_2j2t)s   \\\\ \hline 
%(bgk_DYJetsToLL_M10to50_amc_DYJetsToLL_M50_amc_scale_down)s& %(bgk_DYJetsToLL_M10to50_amc_DYJetsToLL_M50_amc_scale_down_all)s & %(bgk_DYJetsToLL_M10to50_amc_DYJetsToLL_M50_amc_scale_down_1j1t)s & %(bgk_DYJetsToLL_M10to50_amc_DYJetsToLL_M50_amc_scale_down_2j1t)s& %(bgk_DYJetsToLL_M10to50_amc_DYJetsToLL_M50_amc_scale_down_2j2t)s \\\\ \hline 
%(bgk_WJet_scale_up)s                       & %(bgk_WJet_scale_up_all)s                        & %(bgk_WJet_scale_up_1j1t)s                        & %(bgk_WJet_scale_up_2j1t)s                       & %(bgk_WJet_scale_up_2j2t)s                        \\\\ \hline 
%(bgk_WJet_scale_down)s                     & %(bgk_WJet_scale_down_all)s                      & %(bgk_WJet_scale_down_1j1t)s                      & %(bgk_WJet_scale_down_2j1t)s                     & %(bgk_WJet_scale_down_2j2t)s                      \\\\ \hline 
%(other_scale_up)s                          & %(other_scale_up_all)s                           & %(other_scale_up_1j1t)s                           & %(other_scale_up_2j1t)s                          & %(other_scale_up_2j2t)s                           \\\\ \hline 
%(other_scale_down)s                        & %(other_scale_down_all)s                         & %(other_scale_down_1j1t)s                         & %(other_scale_down_2j1t)s                        & %(other_scale_down_2j2t)s                         \\\\ \hline \hline 
%(TrigSF_up)s                               & %(TrigSF_up_all)s                                & %(TrigSF_up_1j1t)s                                & %(TrigSF_up_2j1t)s                               & %(TrigSF_up_2j2t)s                                \\\\ \hline 
%(TrigSF_down)s                             & %(TrigSF_down_all)s                              & %(TrigSF_down_1j1t)s                              & %(TrigSF_down_2j1t)s                             & %(TrigSF_down_2j2t)s                              \\\\ \hline 
%(PU_scale_up)s                             & %(PU_scale_up_all)s                              & %(PU_scale_up_1j1t)s                              & %(PU_scale_up_2j1t)s                             & %(PU_scale_up_2j2t)s                              \\\\ \hline 
%(PU_scale_down)s                           & %(PU_scale_down_all)s                            & %(PU_scale_down_1j1t)s                            & %(PU_scale_down_2j1t)s                           & %(PU_scale_down_2j2t)s                            \\\\ \hline 
%(SmearedJetResUp)s                         & %(SmearedJetResUp_all)s                          & %(SmearedJetResUp_1j1t)s                          & %(SmearedJetResUp_2j1t)s                         & %(SmearedJetResUp_2j2t)s                          \\\\ \hline     
%(SmearedJetResDown)s                       & %(SmearedJetResDown_all)s                        & %(SmearedJetResDown_1j1t)s                        & %(SmearedJetResDown_2j1t)s                       & %(SmearedJetResDown_2j2t)s                        \\\\ \hline    
%(JetEnUp)s                                 & %(JetEnUp_all)s                                  & %(JetEnUp_1j1t)s                                  & %(JetEnUp_2j1t)s                                 & %(JetEnUp_2j2t)s                                  \\\\ \hline    
%(JetEnDown)s                               & %(JetEnDown_all)s                                & %(JetEnDown_1j1t)s                                & %(JetEnDown_2j1t)s                               & %(JetEnDown_2j2t)s                                \\\\ \hline    
%(BtagSFbcUp)s                              & %(BtagSFbcUp_all)s                               & %(BtagSFbcUp_1j1t)s                               & %(BtagSFbcUp_2j1t)s                              & %(BtagSFbcUp_2j2t)s                               \\\\ \hline    
%(BtagSFbcDown)s                            & %(BtagSFbcDown_all)s                             & %(BtagSFbcDown_1j1t)s                             & %(BtagSFbcDown_2j1t)s                            & %(BtagSFbcDown_2j2t)s                             \\\\ \hline    
%(BtagSFudsgUp)s                            & %(BtagSFudsgUp_all)s                             & %(BtagSFudsgUp_1j1t)s                             & %(BtagSFudsgUp_2j1t)s                            & %(BtagSFudsgUp_2j2t)s                             \\\\ \hline     
%(BtagSFudsgDown)s                          & %(BtagSFudsgDown_all)s                           & %(BtagSFudsgDown_1j1t)s                           & %(BtagSFudsgDown_2j1t)s                          & %(BtagSFudsgDown_2j2t)s                           \\\\ \hline     
%(MuonSFID_up)s                             & %(MuonSFID_up_all)s                              & %(MuonSFID_up_1j1t)s                              & %(MuonSFID_up_2j1t)s                             & %(MuonSFID_up_2j2t)s                              \\\\ \hline    
%(MuonSFID_down)s                           & %(MuonSFID_down_all)s                            & %(MuonSFID_down_1j1t)s                            & %(MuonSFID_down_2j1t)s                           & %(MuonSFID_down_2j2t)s                            \\\\ \hline    
%(MuonSFIso_up)s                            & %(MuonSFIso_up_all)s                             & %(MuonSFIso_up_1j1t)s                             & %(MuonSFIso_up_2j1t)s                            & %(MuonSFIso_up_2j2t)s                             \\\\ \hline           
%(MuonSFIso_down)s                          & %(MuonSFIso_down_all)s                           & %(MuonSFIso_down_1j1t)s                           & %(MuonSFIso_down_2j1t)s                          & %(MuonSFIso_down_2j2t)s                           \\\\ \hline    
%(MuonSFtrack_up)s                          & %(MuonSFtrack_up_all)s                           & %(MuonSFtrack_up_1j1t)s                           & %(MuonSFtrack_up_2j1t)s                          & %(MuonSFtrack_up_2j2t)s                           \\\\ \hline    
%(MuonSFtrack_down)s                        & %(MuonSFtrack_down_all)s                         & %(MuonSFtrack_down_1j1t)s                         & %(MuonSFtrack_down_2j1t)s                        & %(MuonSFtrack_down_2j2t)s                         \\\\ \hline  
%(UnclusteredEnUp)s                         & %(UnclusteredEnUp_all)s                          & %(UnclusteredEnUp_1j1t)s                          & %(UnclusteredEnUp_2j1t)s                         & %(UnclusteredEnUp_2j2t)s                          \\\\ \hline    
%(UnclusteredEnDown)s                      & %(UnclusteredEnDown_all)s                         & %(UnclusteredEnDown_1j1t)s                        & %(UnclusteredEnDown_2j1t)s                       & %(UnclusteredEnDown_2j2t)s                        \\\\ \hline   \hline 
%(isrdown)s                                & %(isrdown_all)s                                   & %(isrdown_1j1t)s                                  & %(isrdown_2j1t)s                                 & %(isrdown_2j2t)s                                  \\\\ \hline
%(isrup)s                                  & %(isrup_all)s                                     & %(isrup_1j1t)s                                    & %(isrup_2j1t)s                                   & %(isrup_2j2t)s                                    \\\\ \hline
%(fsrdown)s                                & %(fsrdown_all)s                                   & %(fsrdown_1j1t)s                                  & %(fsrdown_2j1t)s                                 & %(fsrdown_2j2t)s                                  \\\\ \hline
%(fsrup)s                                  & %(fsrup_all)s                                     & %(fsrup_1j1t)s                                    & %(fsrup_2j1t)s                                   & %(fsrup_2j2t)s                                    \\\\ \hline 
%(Sample_TT_TuneEE5C)s                      & %(Sample_TT_TuneEE5C_all)s                       & %(Sample_TT_TuneEE5C_1j1t)s                       & %(Sample_TT_TuneEE5C_2j1t)s                      & %(Sample_TT_TuneEE5C_2j2t)s                       \\\\ \hline         
%(Sample_TT_CR)s                            & %(Sample_TT_CR_all)s                             & %(Sample_TT_CR_1j1t)s                             & %(Sample_TT_CR_2j1t)s                            & %(Sample_TT_CR_2j2t)s                             \\\\ \hline        
%(Sample_TT_PDF_Up)s                        & %(Sample_TT_PDF_Up_all)s                         & %(Sample_TT_PDF_Up_1j1t)s                         & %(Sample_TT_PDF_Up_2j1t)s                        & %(Sample_TT_PDF_Up_2j2t)s                       \\\\ \hline    
%(Sample_TT_PDF_Down)s                      & %(Sample_TT_PDF_Down_all)s                       & %(Sample_TT_PDF_Down_1j1t)s                       & %(Sample_TT_PDF_Down_2j1t)s                      & %(Sample_TT_PDF_Down_2j2t)s                       \\\\ \hline    
%(Sample_TT_mtop1695)s                      & %(Sample_TT_mtop1695_all)s                       & %(Sample_TT_mtop1695_1j1t)s                       & %(Sample_TT_mtop1695_2j1t)s                      & %(Sample_TT_mtop1695_2j2t)s                       \\\\ \hline    
%(Sample_TT_mtop1755)s                      & %(Sample_TT_mtop1755_all)s                       & %(Sample_TT_mtop1755_1j1t)s                       & %(Sample_TT_mtop1755_2j1t)s                      & %(Sample_TT_mtop1755_2j2t)s                       \\\\ \hline        
%(Sample_TT_TuneCUETP8M2T4down)s            & %(Sample_TT_TuneCUETP8M2T4down_all)s             & %(Sample_TT_TuneCUETP8M2T4down_1j1t)s             & %(Sample_TT_TuneCUETP8M2T4down_2j1t)s            & %(Sample_TT_TuneCUETP8M2T4down_2j2t)s             \\\\ \hline      
%(Sample_TT_TuneCUETP8M2T4up)s              & %(Sample_TT_TuneCUETP8M2T4up_all)s               & %(Sample_TT_TuneCUETP8M2T4up_1j1t)s               & %(Sample_TT_TuneCUETP8M2T4up_2j1t)s              & %(Sample_TT_TuneCUETP8M2T4up_2j2t)s               \\\\ \hline    
%(Sample_TT_hdampDOWN)s                  & %(Sample_TT_hdampDOWN_all)s                         & %(Sample_TT_hdampDOWN_1j1t)s                      & %(Sample_TT_hdampDOWN_2j1t)s                        & %(Sample_TT_hdampDOWN_2j2t)s                   \\\\ \hline
%(Sample_TT_hdampUP)s                    & %(Sample_TT_hdampUP_all)s                           & %(Sample_TT_hdampUP_1j1t)s                        & %(Sample_TT_hdampUP_2j1t)s                          & %(Sample_TT_hdampUP_2j2t)s                     \\\\ \hline
%(Sample_ST_tW_herwigpp)s                & %(Sample_ST_tW_herwigpp_all)s                       & %(Sample_ST_tW_herwigpp_1j1t)s                    & %(Sample_ST_tW_herwigpp_2j1t)s                      & %(Sample_ST_tW_herwigpp_2j2t)s                 \\\\ \hline
%(Sample_ST_tW_DS)s                      & %(Sample_ST_tW_DS_all)s                             & %(Sample_ST_tW_DS_1j1t)s                          & %(Sample_ST_tW_DS_2j1t)s                            & %(Sample_ST_tW_DS_2j2t)s                       \\\\ \hline
%(Sample_ST_tW_mtop1695)s                & %(Sample_ST_tW_mtop1695_all)s                       & %(Sample_ST_tW_mtop1695_1j1t)s                    & %(Sample_ST_tW_mtop1695_2j1t)s                      & %(Sample_ST_tW_mtop1695_2j2t)s                 \\\\ \hline
%(Sample_ST_tW_mtop1755)s                & %(Sample_ST_tW_mtop1755_all)s                       & %(Sample_ST_tW_mtop1755_1j1t)s                    & %(Sample_ST_tW_mtop1755_2j1t)s                      & %(Sample_ST_tW_mtop1755_2j2t)s                 \\\\ \hline
%(Sample_ST_tW_MEscaledown)s             & %(Sample_ST_tW_MEscaledown_all)s                    & %(Sample_ST_tW_MEscaledown_1j1t)s                 & %(Sample_ST_tW_MEscaledown_2j1t)s                   & %(Sample_ST_tW_MEscaledown_2j2t)s              \\\\ \hline
%(Sample_ST_tW_MEscaleup)s               & %(Sample_ST_tW_MEscaleup_all)s                      & %(Sample_ST_tW_MEscaleup_1j1t)s                   & %(Sample_ST_tW_MEscaleup_2j1t)s                     & %(Sample_ST_tW_MEscaleup_2j2t)s                \\\\ \hline
%(total_scale_up)s                          & %(total_scale_up_all)s                           & %(total_scale_up_1j1t)s                           & %(total_scale_up_2j1t)s                          & %(total_scale_up_2j2t)s                           \\\\ \hline 
%(total_scale_down)s                        & %(total_scale_down_all)s                         & %(total_scale_down_1j1t)s                         & %(total_scale_down_2j1t)s                        & %(total_scale_down_2j2t)s                         \\\\ \hline \hline 
\end{tabular}}
\end{table}
'''
    text_file = open("%s.tex" % (out_name), "w")
    if chan =="emu":
        text_file.write(template_emu % (dicti))
    elif chan =="ee":
        text_file.write(template_ee % (dicti))
    elif chan =="mumu":
        text_file.write(template_mumu % (dicti))
    text_file.close()
    print "%s.tex is saved"%(out_name)




class file_object:
    def __init__(self, path, file_name, name, event, crosssection, color):
        self.name = name
        self.path = path
        self.file_name = file_name
        self.event = event
        self.crosssection = crosssection
        self.lumi = float(self.event)/float(self.crosssection)
        self.color = color
        self.tfilename = self.path+"%s.root"%(self.file_name)
        self.tfile = ROOT.TFile(self.tfilename,'READ')

class mc_object:
    def __init__(self, name, event, crosssection, color):
        self.name = name
        self.event= event
        self.crosssection = crosssection
        self.lumi = float(self.event)/float(self.crosssection)
        self.color = color
class sys_uncert_object:
    def __init__(self, name, sys_list, file_in, mc_sample, sys_sample, hist_dir):
        self.name = name
        self.sys_list = sys_list
        self.file_in= file_in
        self.lumi = file_in["nominal"].lumi
        self.mc_sample= mc_sample
        self.sys_sample= sys_sample
        self.hist_dir = hist_dir
        self.all_hist={}
        self.xsection_uncer={}
        self.xsection_uncer["ST"]            =0.05      
        self.xsection_uncer["ST_anti"]       =0.05
        self.xsection_uncer["TTTo2L2Nu"]     =0.05
        self.xsection_uncer["DYJetsToLL_M10to50_amc"]=0.5
        self.xsection_uncer["DYJetsToLL_M50_amc"]    =0.5
        if Apply_Rin_out_ratio:
            self.xsection_uncer["DYJetsToLL_M10to50_amc"]=0.3
            self.xsection_uncer["DYJetsToLL_M50_amc"]    =0.3
        self.xsection_uncer["TTWJetsToQQ"]   =0.5
        self.xsection_uncer["TTWJetsToLNu"]  =0.5
        self.xsection_uncer["TTZToLLNuNu"]   =0.5
        self.xsection_uncer["TTZToQQ"]       =0.5
        self.xsection_uncer["TTGJets"]       =0.5
        self.xsection_uncer["WJet"]          =0.5
        self.xsection_uncer["WWTo2L2Nu"]     =0.5
        self.xsection_uncer["WZ_3LNu"]       =0.5
        self.xsection_uncer["WZ_2L2Q"]       =0.5
        self.xsection_uncer["ZZ_2L2Nu"]      =0.5
        self.xsection_uncer["ZZ_4L"]         =0.5
        self.xsection_uncer["WG_LNuG"]       =0.5
        self.xsection_uncer["GGHWWTo2L2Nu"]  =0.5
        self.xsection_uncer["VBFHWWTo2L2Nu"] =0.5

    def Xsection_uncert(self, uncert, sname):
        if sname in uncert:
            if "up" in uncert:return (1+self.xsection_uncer[sname])
            elif "down" in uncert:return (1-self.xsection_uncer[sname])
            else: print "wrong uncertainty name %s"%(uncert)
        else: return 1    
    def save_hist(self):
        for hname in self.hist_dir:
            self.all_hist[hname]={}
            print "%s"%(hname)
            for nsys in self.sys_list:
                self.all_hist[hname][nsys]={}
                self.all_hist[hname][nsys]["data"]=self.file_in["nominal"].tfile.Get("nominal__data__"+hname).Clone("%s__data__%s"%(nsys,hname))
                for sname in self.mc_sample:
                    self.all_hist[hname][nsys][sname]=ROOT.TH1D()            
                    if "lumi" in nsys or "bgk" in nsys :
                        self.all_hist[hname][nsys][sname]=self.file_in["nominal"].tfile.Get("nominal__"+sname+"__"+hname).Clone("%s__%s__%s"%(nsys,sname,hname))
                        tmp_scale=float(self.lumi)/float(self.mc_sample[sname].lumi)
                        if "luminosity_up" in nsys:tmp_scale=(1+0.025)*tmp_scale
                        elif "luminosity_down" in nsys:tmp_scale=(1-0.025)*tmp_scale
                        elif "bgk" in nsys:tmp_scale=tmp_scale*self.Xsection_uncert(nsys,sname)
                        else              : print "something wrong ?"   
                     #   self.all_hist[hname][nsys][sname].Sumw2(ROOT.kTRUE)   
                        self.all_hist[hname][nsys][sname].Scale(tmp_scale)         
                     ############### CR envelope ##################
                    elif nsys == "Sample_TT_CR": ##for CR envelope
                        if "TTTo2L2Nu" in sname:
                            h_tmp1=self.file_in["TT_QCDbasedCRTune_erdON"].tfile.Get("TT_QCDbasedCRTune_erdON"+"__"+sname+"__"+hname) 
                            h_tmp2=self.file_in["TT_GluonMoveCRTune"     ].tfile.Get("TT_GluonMoveCRTune"     +"__"+sname+"__"+hname) 
                            h_tmp3=self.file_in["TT_erdON"               ].tfile.Get("TT_erdON"               +"__"+sname+"__"+hname) 
                            h_tmp1.Scale(float(self.lumi)/float(self.sys_sample["TT_QCDbasedCRTune_erdON"].lumi))
                            h_tmp2.Scale(float(self.lumi)/float(self.sys_sample["TT_GluonMoveCRTune"     ].lumi))
                            h_tmp3.Scale(float(self.lumi)/float(self.sys_sample["TT_erdON"               ].lumi))
                            self.all_hist[hname][nsys][sname]=quadratic_sum(h_tmp1,h_tmp2,h_tmp3)
                        else:
                            self.all_hist[hname][nsys][sname]=self.file_in["nominal"].tfile.Get("nominal"+"__"+sname+"__"+hname)
                            tmp_scale=float(self.lumi)/float(self.mc_sample[sname].lumi)
                            self.all_hist[hname][nsys][sname].Scale(tmp_scale)         
                     ############# TT, TW ISR, FSR ################################
                    elif nsys in ["isrup","isrdown","fsrup","fsrdown"]:
                        if "TTTo2L2Nu" in sname:
                            h_tmp=self.file_in["TT_"+str(nsys)].tfile.Get("TT_"+str(nsys)+"__"+sname+"__"+hname) 
                            h_tmp.Scale(float(self.lumi)/float(self.sys_sample["TT_"+str(nsys)].lumi))
                            self.all_hist[hname][nsys][sname]=h_tmp
                        elif "TW_top" in sname:
                            h_tmp=self.file_in["ST_tW_"+str(nsys)].tfile.Get("ST_tW_"+str(nsys)+"__"+sname+"__"+hname) 
                            h_tmp.Scale(float(self.lumi)/float(self.sys_sample["ST_tW_"+str(nsys)+"_top"].lumi))
                            self.all_hist[hname][nsys][sname]=h_tmp
                        elif "TW_antitop" in sname:
                            h_tmp=self.file_in["ST_tW_"+str(nsys)].tfile.Get("ST_tW_"+str(nsys)+"__"+sname+"__"+hname) 
                            h_tmp.Scale(float(self.lumi)/float(self.sys_sample["ST_tW_"+str(nsys)+"_antitop"].lumi))
                            self.all_hist[hname][nsys][sname]=h_tmp
                        else:
                            self.all_hist[hname][nsys][sname]=self.file_in["nominal"].tfile.Get("nominal"+"__"+sname+"__"+hname)
                            tmp_scale=float(self.lumi)/float(self.mc_sample[sname].lumi)
                            self.all_hist[hname][nsys][sname].Scale(tmp_scale)         
                     ############# TT, TW modeling ################################
                    elif "Sample" in nsys and "TT" in nsys:
                        self.all_hist[hname][nsys][sname]=self.file_in[nsys.split("Sample_")[-1]].tfile.Get(nsys.split("Sample_")[-1]+"__"+sname+"__"+hname)
                        tmp_scale=float(self.lumi)/float(self.mc_sample[sname].lumi)
                        if "TTTo2L2Nu" in sname:
                            tmp_scale=float(self.lumi)/float(self.sys_sample[nsys.split("Sample_")[-1]].lumi)
                        self.all_hist[hname][nsys][sname].Scale(tmp_scale)         
                    elif "Sample" in nsys and "ST_tW" in nsys:
                        self.all_hist[hname][nsys][sname]=self.file_in[nsys.split("Sample_")[-1]].tfile.Get(nsys.split("Sample_")[-1]+"__"+sname+"__"+hname)
                        tmp_scale=float(self.lumi)/float(self.mc_sample[sname].lumi)
                        if "TW_top" in sname:
                            tmp_scale=float(self.lumi)/float(self.sys_sample[nsys.split("Sample_")[-1]+"_top"].lumi)
                        #    print "nsys %s:, hname %s, scale %f"%(nsys,hname,tmp_scale)
                        elif "TW_antitop" in sname:
                            tmp_scale=float(self.lumi)/float(self.sys_sample[nsys.split("Sample_")[-1]+"_antitop"].lumi)
                        self.all_hist[hname][nsys][sname].Scale(tmp_scale)         
                    else:             
                        self.all_hist[hname][nsys][sname]=self.file_in[nsys].tfile.Get(nsys+"__"+sname+"__"+hname)
                        #print "%s__%s__%s"%(nsys,sname,hname)
                        tmp_scale=float(self.lumi)/float(self.mc_sample[sname].lumi)
                        #print "%s, %s, %s, scale=%f"%(hname,nsys,sname,tmp_scale)
                        self.all_hist[hname][nsys][sname].Scale(tmp_scale)         
                     ########### set negative bin to zero ###########################
                    for ibin in range(1,self.all_hist[hname][nsys][sname].GetNbinsX()+1):
                        if self.all_hist[hname][nsys][sname].GetBinContent(ibin)<0:
                            self.all_hist[hname][nsys][sname].SetBinContent(ibin,0)
                            self.all_hist[hname][nsys][sname].SetBinError  (ibin,0)
                         
        if Apply_Rin_out_ratio:
            for hname in self.all_hist:
                if "Rinout" in hname:continue
                for nsys in self.all_hist[hname]:
                    for sname in self.all_hist[hname][nsys]: 
                        if "DYJets" in sname:
                            Ratio=1                                              
                            if "0j0b" in hname or "0jet_0bjet" in hname  :Ratio=Ratio_DY_0j0b
                            elif "1j0b" in hname or "1jet_0bjet" in hname:Ratio=Ratio_DY_1j0b
                            elif "1j1b" in hname or "1jet_1bjet" in hname:Ratio=Ratio_DY_1j1b
                            elif "2j1b" in hname or "2jet_1bjet" in hname:Ratio=Ratio_DY_2j1b
                            elif "2j2b" in hname or "2jet_2bjet" in hname:Ratio=Ratio_DY_2j2b
                            else                                         :Ratio=Ratio_DY_all 
                            self.all_hist[hname][nsys][sname].Scale(Ratio)
                        
    def close_file(self):
        for ifile in self.file_in:
            self.file_in[ifile].tfile.Close()                     
############## BEGIN ########################
#Channel="ee"
Channel="emu"
#Channel="mumu"
Do_FCNC_Study       =True# False is for EFT study
remove_data         =False
do_same_sign        =True
remove_herwig       =True
do_system           =True
add_sys_uncertainty =True
draw_all_system_plot=False
Save_uncert_table   =False
do_plot_main        =False
do_print_sys_region =False
do_draw_combine_MVA =False
do_save_sys_hist    =True
do_print_table      =False
do_trigger_study    =False
Apply_Rin_out_ratio =True
if Channel=="emu":
    Apply_Rin_out_ratio =False
date="20170427"
dir="./plots"
Lumi_RunB=float(5788.348)
Lumi_RunC=float(2573.399)
Lumi_RunD=float(4248.384)
Lumi_RunE=float(4009.132)
Lumi_RunF=float(3101.618)
Lumi_RunG=float(7540.488)
Lumi_RunH=float(8390.540+215.149)
#Lumi=Lumi_RunB+Lumi_RunC+Lumi_RunD
#Lumi=Lumi_RunE+Lumi_RunF
#Lumi=Lumi_RunG+Lumi_RunH
Lumi=35867
FCNC_XS=10
######For ee and mumu Ratio in/out################
Ratio_DY_all =1
Ratio_DY_0j0b=1
Ratio_DY_1j0b=1
Ratio_DY_1j1b=1
Ratio_DY_2j1b=1
Ratio_DY_2j2b=1
if Channel=="ee":
    Ratio_DY_all =0.855
    Ratio_DY_0j0b=0.835
    Ratio_DY_1j0b=0.886
    Ratio_DY_1j1b=0.828
    Ratio_DY_2j1b=1.002
    Ratio_DY_2j2b=0.985
elif Channel=="mumu":
    Ratio_DY_all =0.848
    Ratio_DY_0j0b=0.833
    Ratio_DY_1j0b=0.872
    Ratio_DY_1j1b=0.783
    Ratio_DY_2j1b=0.821
    Ratio_DY_2j2b=0.945

#####################
#File_path="./ntuples/saved_hist/Step2_sys_MVA_0620/"#TOPEFT
#File_path_same_sign="./ntuples/saved_hist/Step2_sys_MVA_SameSign_0620/"
##File_path="./ntuples/saved_hist/Step2_MVA_0702/"                    #MVA for SM and BSM split
##File_path_same_sign="./ntuples/saved_hist/Step2_MVA_SameSign_0702/" #
##File_path="./ntuples/saved_hist/Step2_MVA_BSM_0702/"
##File_path_same_sign="./ntuples/saved_hist/Step2_MVA_BSM_SameSign_0702/"
################### For FCNC ######################
#File_path="./ntuples/saved_hist/Step2_MVA_FCNC_0712/"  ####fast sim sample
#File_path_same_sign="./ntuples/saved_hist/Step2_MVA_FCNC_SameSign_0712/"
################### For tW measure, TOPEFT and FCNC(full sim and fast sim include, tug,tcg using tug MLP) ######################
#File_path="./ntuples/saved_hist/Step2_0719/"
#File_path_same_sign="./ntuples/saved_hist/Step2_SameSign_0719/"
#################### Step 1, ele eta, trigger changed ####################
#File_path="./ntuples/saved_hist/Step1_0725_PDF_uncluster_NoNvtex/"
#File_path="./ntuples/saved_hist/Step1_0726_PDF_uncluster_Nvtex/"
#File_path="./ntuples/saved_hist/Step1_0729_Nvtx_25_30/"
#File_path="./ntuples/saved_hist/Step1_0729_noPU/"
#File_path="./ntuples/saved_hist/Step1_0731_noPU_reNvtx/"
#################### Step 2, ele eta, trigger changed ####################
#File_path="./ntuples/saved_hist/Step2_0726_PDF_uncluster/"
#File_path_same_sign="./ntuples/saved_hist/Step2_SameSign_0726_PDF_uncluster/"
#################### Step 2, ele eta, trigger changed, new MVA####################
#File_path="./ntuples/saved_hist/Step2_0801/"
#File_path_same_sign="./ntuples/saved_hist/Step2_SameSign_0801/"
#################### Step 2, 2j2b variables add, Rin/out####################
#File_path="./ntuples/saved_hist/Step2_0803/"
#File_path_same_sign="./ntuples/saved_hist/Step2_SameSign_0803/"
#################### new MLP from Reza for emu####################
File_path="./ntuples/saved_hist/Step2_0805/"
File_path_same_sign="./ntuples/saved_hist/Step2_SameSign_0805/"
if do_system:
    Files={}
    Files_same_sign={}
    Files["nominal"                    ]=file_object(File_path, Channel+"_nominal_"            ,"data_mc",Lumi,1,ROOT.kBlack)             
    if do_same_sign:
        Files_same_sign["nominal"                ]=file_object(File_path_same_sign, Channel+"_nominal_"            ,"data_mc",Lumi,1,ROOT.kBlack)             
    if add_sys_uncertainty: 
        Files["PU_scale_up"            ]=file_object(File_path, Channel+"_PU_scale_up_"        ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#ff0000"))         
        Files["PU_scale_down"          ]=file_object(File_path, Channel+"_PU_scale_down_"      ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#ff0000"))       
        Files["SmearedJetResUp"        ]=file_object(File_path, Channel+"_SmearedJetResUp_"    ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#ffd700"))     
        Files["SmearedJetResDown"      ]=file_object(File_path, Channel+"_SmearedJetResDown_"  ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#ffd700"))   
        Files["JetEnUp"                ]=file_object(File_path, Channel+"_JetEnUp_"            ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#0000ff"))             
        Files["JetEnDown"              ]=file_object(File_path, Channel+"_JetEnDown_"          ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#0000ff"))           
        Files["BtagSFbcUp"             ]=file_object(File_path, Channel+"_BtagSFbcUp_"         ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#800080"))          
        Files["BtagSFbcDown"           ]=file_object(File_path, Channel+"_BtagSFbcDown_"       ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#800080"))        
        Files["BtagSFudsgUp"           ]=file_object(File_path, Channel+"_BtagSFudsgUp_"       ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#008080"))        
        Files["BtagSFudsgDown"         ]=file_object(File_path, Channel+"_BtagSFudsgDown_"     ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#008080"))      
        Files["T1JetEnUp"              ]=file_object(File_path, Channel+"_T1JetEnUp_"          ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#00ffff"))           
        Files["T1JetEnDown"            ]=file_object(File_path, Channel+"_T1JetEnDown_"        ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#00ffff"))         
        Files["EleSFReco_up"           ]=file_object(File_path, Channel+"_EleSFReco_up_"       ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#00ff00"))        
        Files["EleSFReco_down"         ]=file_object(File_path, Channel+"_EleSFReco_down_"     ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#00ff00"))      
        Files["EleSFID_up"             ]=file_object(File_path, Channel+"_EleSFID_up_"         ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#00ff00"))          
        Files["EleSFID_down"           ]=file_object(File_path, Channel+"_EleSFID_down_"       ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#00ff00"))        
        Files["MuonSFID_up"            ]=file_object(File_path, Channel+"_MuonSFID_up_"        ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#00ff00"))         
        Files["MuonSFID_down"          ]=file_object(File_path, Channel+"_MuonSFID_down_"      ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#00ff00"))       
        Files["MuonSFIso_up"           ]=file_object(File_path, Channel+"_MuonSFIso_up_"       ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#00ff00"))        
        Files["MuonSFIso_down"         ]=file_object(File_path, Channel+"_MuonSFIso_down_"     ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#00ff00"))      
        Files["MuonSFtrack_up"         ]=file_object(File_path, Channel+"_MuonSFtrack_up_"     ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#00ff00"))      
        Files["MuonSFtrack_down"       ]=file_object(File_path, Channel+"_MuonSFtrack_down_"   ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#00ff00"))    
        Files["UnclusteredEnUp"        ]=file_object(File_path, Channel+"_UnclusteredEnUp_"    ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#00ff00"))      
        Files["UnclusteredEnDown"      ]=file_object(File_path, Channel+"_UnclusteredEnDown_"  ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#00ff00"))      
        Files["TrigSF_up"              ]=file_object(File_path, Channel+"_TrigSF_up_"          ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#00ff00"))      
        Files["TrigSF_down"            ]=file_object(File_path, Channel+"_TrigSF_down_"        ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#00ff00"))      

        Files["TT_TuneCUETP8M2T4down"  ]=file_object(File_path, Channel+"_TT_TuneCUETP8M2T4down_"   ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#ff0000"))
        Files["TT_TuneCUETP8M2T4up"    ]=file_object(File_path, Channel+"_TT_TuneCUETP8M2T4up_"     ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#ff0000"))
############### for color reconnection : envelope 
        Files["TT_QCDbasedCRTune_erdON"]=file_object(File_path, Channel+"_TT_QCDbasedCRTune_erdON_" ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#008080"))
        Files["TT_GluonMoveCRTune"     ]=file_object(File_path, Channel+"_TT_GluonMoveCRTune_"      ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#008080"))
        Files["TT_erdON"               ]=file_object(File_path, Channel+"_TT_erdON_"                ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#008080"))
############### for TT PDF uncertainty ########## 
        Files["TT_PDF_Up"              ]=file_object(File_path, Channel+"_TT_PDF_Up_"               ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#ccff00"))
        Files["TT_PDF_Down"            ]=file_object(File_path, Channel+"_TT_PDF_Down_"             ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#ccff00"))
#################################################
        Files["TT_fsrdown"             ]=file_object(File_path, Channel+"_TT_fsrdown_"              ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#ffd700"))
        Files["TT_fsrup"               ]=file_object(File_path, Channel+"_TT_fsrup_"                ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#ffd700"))
        Files["TT_hdampDOWN"           ]=file_object(File_path, Channel+"_TT_hdampDOWN_"            ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#0000ff"))
        Files["TT_hdampUP"             ]=file_object(File_path, Channel+"_TT_hdampUP_"              ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#0000ff"))
        Files["TT_isrdown"             ]=file_object(File_path, Channel+"_TT_isrdown_"              ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#800080"))
        Files["TT_isrup"               ]=file_object(File_path, Channel+"_TT_isrup_"                ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#800080"))
        Files["TT_mtop1695"            ]=file_object(File_path, Channel+"_TT_mtop1695_"             ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#00ffff"))
        Files["TT_mtop1755"            ]=file_object(File_path, Channel+"_TT_mtop1755_"             ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#00ff00"))
        Files["TT_TuneEE5C"            ]=file_object(File_path, Channel+"_TT_TuneEE5C_"             ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#ff00ff"))
        Files["ST_tW_herwigpp"         ]=file_object(File_path, Channel+"_ST_tW_herwigpp_"          ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#ff00ff"))
        Files["ST_tW_DS"               ]=file_object(File_path, Channel+"_ST_tW_DS_"                ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#008080"))
        Files["ST_tW_MEscaledown"      ]=file_object(File_path, Channel+"_ST_tW_MEscaledown_"       ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#ff0000"))
        Files["ST_tW_MEscaleup"        ]=file_object(File_path, Channel+"_ST_tW_MEscaleup_"         ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#ff0000"))
        Files["ST_tW_PSscaledown"      ]=file_object(File_path, Channel+"_ST_tW_PSscaledown_"       ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#0000ff"))
        Files["ST_tW_PSscaleup"        ]=file_object(File_path, Channel+"_ST_tW_PSscaleup_"         ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#0000ff"))
        Files["ST_tW_fsrdown"          ]=file_object(File_path, Channel+"_ST_tW_fsrdown_"           ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#ffd700"))
        Files["ST_tW_fsrup"            ]=file_object(File_path, Channel+"_ST_tW_fsrup_"             ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#ffd700"))
        Files["ST_tW_isrdown"          ]=file_object(File_path, Channel+"_ST_tW_isrdown_"           ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#800080"))
        Files["ST_tW_isrup"            ]=file_object(File_path, Channel+"_ST_tW_isrup_"             ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#800080"))
        Files["ST_tW_mtop1695"         ]=file_object(File_path, Channel+"_ST_tW_mtop1695_"          ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#00ffff"))
        Files["ST_tW_mtop1755"         ]=file_object(File_path, Channel+"_ST_tW_mtop1755_"          ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#00ff00"))
        if do_same_sign:
            Files_same_sign["PU_scale_up"            ]=file_object(File_path_same_sign, Channel+"_PU_scale_up_"        ,"data_mc",Lumi,1,ROOT.kBlack)         
            Files_same_sign["PU_scale_down"          ]=file_object(File_path_same_sign, Channel+"_PU_scale_down_"      ,"data_mc",Lumi,1,ROOT.kBlack)       
            Files_same_sign["SmearedJetResUp"        ]=file_object(File_path_same_sign, Channel+"_SmearedJetResUp_"    ,"data_mc",Lumi,1,ROOT.kBlack)     
            Files_same_sign["SmearedJetResDown"      ]=file_object(File_path_same_sign, Channel+"_SmearedJetResDown_"  ,"data_mc",Lumi,1,ROOT.kBlack)   
            Files_same_sign["JetEnUp"                ]=file_object(File_path_same_sign, Channel+"_JetEnUp_"            ,"data_mc",Lumi,1,ROOT.kBlack)             
            Files_same_sign["JetEnDown"              ]=file_object(File_path_same_sign, Channel+"_JetEnDown_"          ,"data_mc",Lumi,1,ROOT.kBlack)           
            Files_same_sign["BtagSFbcUp"             ]=file_object(File_path_same_sign, Channel+"_BtagSFbcUp_"         ,"data_mc",Lumi,1,ROOT.kBlack)          
            Files_same_sign["BtagSFbcDown"           ]=file_object(File_path_same_sign, Channel+"_BtagSFbcDown_"       ,"data_mc",Lumi,1,ROOT.kBlack)        
            Files_same_sign["BtagSFudsgUp"           ]=file_object(File_path_same_sign, Channel+"_BtagSFudsgUp_"       ,"data_mc",Lumi,1,ROOT.kBlack)        
            Files_same_sign["BtagSFudsgDown"         ]=file_object(File_path_same_sign, Channel+"_BtagSFudsgDown_"     ,"data_mc",Lumi,1,ROOT.kBlack)      
            Files_same_sign["T1JetEnUp"              ]=file_object(File_path_same_sign, Channel+"_T1JetEnUp_"          ,"data_mc",Lumi,1,ROOT.kBlack)           
            Files_same_sign["T1JetEnDown"            ]=file_object(File_path_same_sign, Channel+"_T1JetEnDown_"        ,"data_mc",Lumi,1,ROOT.kBlack)         
            Files_same_sign["EleSFReco_up"           ]=file_object(File_path_same_sign, Channel+"_EleSFReco_up_"       ,"data_mc",Lumi,1,ROOT.kBlack)        
            Files_same_sign["EleSFReco_down"         ]=file_object(File_path_same_sign, Channel+"_EleSFReco_down_"     ,"data_mc",Lumi,1,ROOT.kBlack)      
            Files_same_sign["EleSFID_up"             ]=file_object(File_path_same_sign, Channel+"_EleSFID_up_"         ,"data_mc",Lumi,1,ROOT.kBlack)          
            Files_same_sign["EleSFID_down"           ]=file_object(File_path_same_sign, Channel+"_EleSFID_down_"       ,"data_mc",Lumi,1,ROOT.kBlack)        
            Files_same_sign["MuonSFID_up"            ]=file_object(File_path_same_sign, Channel+"_MuonSFID_up_"        ,"data_mc",Lumi,1,ROOT.kBlack)         
            Files_same_sign["MuonSFID_down"          ]=file_object(File_path_same_sign, Channel+"_MuonSFID_down_"      ,"data_mc",Lumi,1,ROOT.kBlack)       
            Files_same_sign["MuonSFIso_up"           ]=file_object(File_path_same_sign, Channel+"_MuonSFIso_up_"       ,"data_mc",Lumi,1,ROOT.kBlack)        
            Files_same_sign["MuonSFIso_down"         ]=file_object(File_path_same_sign, Channel+"_MuonSFIso_down_"     ,"data_mc",Lumi,1,ROOT.kBlack)      
            Files_same_sign["MuonSFtrack_up"         ]=file_object(File_path_same_sign, Channel+"_MuonSFtrack_up_"     ,"data_mc",Lumi,1,ROOT.kBlack)      
            Files_same_sign["MuonSFtrack_down"       ]=file_object(File_path_same_sign, Channel+"_MuonSFtrack_down_"   ,"data_mc",Lumi,1,ROOT.kBlack)    
            Files_same_sign["UnclusteredEnUp"        ]=file_object(File_path_same_sign, Channel+"_UnclusteredEnUp_"    ,"data_mc",Lumi,1,ROOT.kBlack)      
            Files_same_sign["UnclusteredEnDown"      ]=file_object(File_path_same_sign, Channel+"_UnclusteredEnDown_"  ,"data_mc",Lumi,1,ROOT.kBlack)      
            Files_same_sign["TrigSF_up"              ]=file_object(File_path_same_sign, Channel+"_TrigSF_up_"          ,"data_mc",Lumi,1,ROOT.kBlack)      
            Files_same_sign["TrigSF_down"            ]=file_object(File_path_same_sign, Channel+"_TrigSF_down_"        ,"data_mc",Lumi,1,ROOT.kBlack)      

            Files_same_sign["TT_TuneCUETP8M2T4down"  ]=file_object(File_path_same_sign, Channel+"_TT_TuneCUETP8M2T4down_"   ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#ff0000"))
            Files_same_sign["TT_TuneCUETP8M2T4up"    ]=file_object(File_path_same_sign, Channel+"_TT_TuneCUETP8M2T4up_"     ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#ff0000"))
########    #####_same_sign## for color reconnection : envelope 
            Files_same_sign["TT_QCDbasedCRTune_erdON"]=file_object(File_path_same_sign, Channel+"_TT_QCDbasedCRTune_erdON_" ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#008080"))
            Files_same_sign["TT_GluonMoveCRTune"     ]=file_object(File_path_same_sign, Channel+"_TT_GluonMoveCRTune_"      ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#008080"))
            Files_same_sign["TT_erdON"               ]=file_object(File_path_same_sign, Channel+"_TT_erdON_"                ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#008080"))
############### for same-sign TT PDF uncertainty ########## 
            Files_same_sign["TT_PDF_Up"              ]=file_object(File_path_same_sign, Channel+"_TT_PDF_Up_"               ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#ccff00"))
            Files_same_sign["TT_PDF_Down"            ]=file_object(File_path_same_sign, Channel+"_TT_PDF_Down_"             ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#ccff00"))
########    #####_same_sign####################################
            Files_same_sign["TT_fsrdown"             ]=file_object(File_path_same_sign, Channel+"_TT_fsrdown_"              ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#ffd700"))
            Files_same_sign["TT_fsrup"               ]=file_object(File_path_same_sign, Channel+"_TT_fsrup_"                ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#ffd700"))
            Files_same_sign["TT_hdampDOWN"           ]=file_object(File_path_same_sign, Channel+"_TT_hdampDOWN_"            ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#0000ff"))
            Files_same_sign["TT_hdampUP"             ]=file_object(File_path_same_sign, Channel+"_TT_hdampUP_"              ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#0000ff"))
            Files_same_sign["TT_isrdown"             ]=file_object(File_path_same_sign, Channel+"_TT_isrdown_"              ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#800080"))
            Files_same_sign["TT_isrup"               ]=file_object(File_path_same_sign, Channel+"_TT_isrup_"                ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#800080"))
            Files_same_sign["TT_mtop1695"            ]=file_object(File_path_same_sign, Channel+"_TT_mtop1695_"             ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#00ffff"))
            Files_same_sign["TT_mtop1755"            ]=file_object(File_path_same_sign, Channel+"_TT_mtop1755_"             ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#00ff00"))
            Files_same_sign["TT_TuneEE5C"            ]=file_object(File_path_same_sign, Channel+"_TT_TuneEE5C_"             ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#ff00ff"))
            Files_same_sign["ST_tW_herwigpp"         ]=file_object(File_path_same_sign, Channel+"_ST_tW_herwigpp_"          ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#ff00ff"))
            Files_same_sign["ST_tW_DS"               ]=file_object(File_path_same_sign, Channel+"_ST_tW_DS_"                ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#008080"))
            Files_same_sign["ST_tW_MEscaledown"      ]=file_object(File_path_same_sign, Channel+"_ST_tW_MEscaledown_"       ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#ff0000"))
            Files_same_sign["ST_tW_MEscaleup"        ]=file_object(File_path_same_sign, Channel+"_ST_tW_MEscaleup_"         ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#ff0000"))
            Files_same_sign["ST_tW_PSscaledown"      ]=file_object(File_path_same_sign, Channel+"_ST_tW_PSscaledown_"       ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#0000ff"))
            Files_same_sign["ST_tW_PSscaleup"        ]=file_object(File_path_same_sign, Channel+"_ST_tW_PSscaleup_"         ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#0000ff"))
            Files_same_sign["ST_tW_fsrdown"          ]=file_object(File_path_same_sign, Channel+"_ST_tW_fsrdown_"           ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#ffd700"))
            Files_same_sign["ST_tW_fsrup"            ]=file_object(File_path_same_sign, Channel+"_ST_tW_fsrup_"             ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#ffd700"))
            Files_same_sign["ST_tW_isrdown"          ]=file_object(File_path_same_sign, Channel+"_ST_tW_isrdown_"           ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#800080"))
            Files_same_sign["ST_tW_isrup"            ]=file_object(File_path_same_sign, Channel+"_ST_tW_isrup_"             ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#800080"))
            Files_same_sign["ST_tW_mtop1695"         ]=file_object(File_path_same_sign, Channel+"_ST_tW_mtop1695_"          ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#00ffff"))
            Files_same_sign["ST_tW_mtop1755"         ]=file_object(File_path_same_sign, Channel+"_ST_tW_mtop1755_"          ,"data_mc",Lumi,1,ROOT.TColor.GetColor("#00ff00"))

    MC_Sample={}
    MC_Sample["TW_top"                ]=mc_object("TW_top"                ,8609398  ,19.47  ,ROOT.kOrange-3)
    MC_Sample["TW_antitop"            ]=mc_object("TW_antitop"            ,8681265  ,19.47  ,ROOT.kOrange-3)
    MC_Sample["TTTo2L2Nu"             ]=mc_object("TTTo2L2Nu"             ,64910035 ,87.31  ,ROOT.kRed-4)
################# For FCNC ########################
    if Do_FCNC_Study:
        #MC_Sample["FCNC_ST_tug"           ]=mc_object("FCNC_ST_tug"       ,100000  ,FCNC_XS  ,ROOT.TColor.GetColor("#800000"))
        #MC_Sample["FCNC_ST_tcg"           ]=mc_object("FCNC_ST_tcg"       ,100000  ,FCNC_XS  ,ROOT.TColor.GetColor("#ffa500"))
        MC_Sample["FCNC_ST_tug"           ]=mc_object("FCNC_ST_tug"       ,1952506  ,FCNC_XS  ,ROOT.TColor.GetColor("#800000"))
        MC_Sample["FCNC_ST_tcg"           ]=mc_object("FCNC_ST_tcg"       ,1807365  ,FCNC_XS  ,ROOT.TColor.GetColor("#ffa500"))
################# For BSM ########################
#    MC_Sample["TW_top"                ]=mc_object("TW_top"                ,100000 ,7.52778*0.9962,ROOT.kOrange-3)
#    MC_Sample["TTTo2L2Nu"             ]=mc_object("TTTo2L2Nu"             ,200000 ,87.31  *1.0004,ROOT.kRed-4)
##################################################

#    MC_Sample["TT_hdampUP"             ]=mc_object("TT_hdampUP"            ,26535098 ,831.76 ,ROOT.kRed-4)
#    MC_Sample["TTJets_Dilept"        ]=mc_object("TTJets_Dilept"         ,25008083 ,87.31  ,ROOT.kRed-4)
#    MC_Sample["TTJets_madgraph"      ]=mc_object("TTJets_madgraph"         ,10040835 ,831.76  ,ROOT.kRed-4)
#    MC_Sample["TT_TuneEE5C"          ]=mc_object("TT_TuneEE5C"            ,59052949 ,831.76 ,ROOT.kRed-4)
#    MC_Sample["DYJetsToLL_M10to50_amc_wx"]=mc_object("DYJetsToLL_M10to50_amc_wx",98685522 ,18610  ,ROOT.kBlue-3)
    MC_Sample["DYJetsToLL_M10to50_amc"]=mc_object("DYJetsToLL_M10to50_amc",29332494 ,18610  ,ROOT.kBlue-3)
    MC_Sample["DYJetsToLL_M50_amc"    ]=mc_object("DYJetsToLL_M50_amc"    ,68009629 ,5765.4 ,ROOT.kBlue-3)
    MC_Sample["TTWJetsToQQ"           ]=mc_object("TTWJetsToQQ"           ,72339    ,0.4062 ,ROOT.kGreen)
    MC_Sample["TTWJetsToLNu"          ]=mc_object("TTWJetsToLNu"          ,1552336  ,0.2043 ,ROOT.kGreen)
    MC_Sample["TTZToLLNuNu"           ]=mc_object("TTZToLLNuNu"           ,678038   ,0.2529 ,ROOT.kGreen)
    MC_Sample["TTZToQQ"               ]=mc_object("TTZToQQ"               ,90425    ,0.5297 ,ROOT.kGreen)
    MC_Sample["TTGJets"               ]=mc_object("TTGJets"               ,1771676  ,3.697  ,ROOT.kGreen)
    MC_Sample["WJet_mad"              ]=mc_object("WJet_mad"              ,51285955 ,61526.7,ROOT.kGreen)
    if do_same_sign:
        MC_Sample["WJet_mad"          ]=mc_object("WJet_mad"              ,51285955 ,61526.7,ROOT.kYellow)
    MC_Sample["WWTo2L2Nu"             ]=mc_object("WWTo2L2Nu"             ,1671947  ,12.178 ,ROOT.kGreen)
    MC_Sample["WZ_3LNu"               ]=mc_object("WZ_3LNu"               ,1993154  ,4.42965,ROOT.kGreen)
    MC_Sample["WZ_2L2Q"               ]=mc_object("WZ_2L2Q"               ,10254393 ,5.595  ,ROOT.kGreen)
    MC_Sample["ZZ_2L2Nu"              ]=mc_object("ZZ_2L2Nu"              ,7819554  ,0.564  ,ROOT.kGreen)
    MC_Sample["ZZ_4L"                 ]=mc_object("ZZ_4L"                 ,6544107  ,1.212  ,ROOT.kGreen)
    MC_Sample["WG_LNuG"               ]=mc_object("WG_LNuG"               ,6304489  ,489    ,ROOT.kGreen)
    MC_Sample["GGHWWTo2L2Nu"          ]=mc_object("GGHWWTo2L2Nu"          ,499466  ,2.5     ,ROOT.kGreen)
    MC_Sample["VBFHWWTo2L2Nu"         ]=mc_object("VBFHWWTo2L2Nu"         ,485693  ,0.175   ,ROOT.kGreen)
    
    Sys_MC_Sample={}
    Sys_MC_Sample["TT_TuneCUETP8M2T4down"    ]=mc_object("TT_TuneCUETP8M2T4down"           ,27877257 ,831.76 ,ROOT.kRed-4)
    Sys_MC_Sample["TT_TuneCUETP8M2T4up"      ]=mc_object("TT_TuneCUETP8M2T4up"             ,28701616 ,831.76 ,ROOT.kRed-4)
############### for color reconnection : envelope 
    Sys_MC_Sample["TT_QCDbasedCRTune_erdON"  ]=mc_object("TT_QCDbasedCRTune_erdON"         ,28789634 ,831.76 ,ROOT.kRed-4)
    Sys_MC_Sample["TT_GluonMoveCRTune"       ]=mc_object("TT_GluonMoveCRTune"              ,56456001 ,831.76 ,ROOT.kRed-4)
    Sys_MC_Sample["TT_erdON"                 ]=mc_object("TT_erdON"                        ,28550174 ,831.76 ,ROOT.kRed-4)
################# For PDF uncertainty sample ####
    Sys_MC_Sample["TT_PDF_Up"                ]=mc_object("TT_PDF_Up"                       ,78055599 ,87.31 ,ROOT.kRed-4)
    Sys_MC_Sample["TT_PDF_Down"              ]=mc_object("TT_PDF_Down"                     ,78055599 ,87.31 ,ROOT.kRed-4)
#################################################
    Sys_MC_Sample["TT_fsrdown"               ]=mc_object("TT_fsrdown"                      ,29156223 ,831.76 ,ROOT.kRed-4)
    Sys_MC_Sample["TT_fsrup"                 ]=mc_object("TT_fsrup"                        ,29022611 ,831.76 ,ROOT.kRed-4)
    Sys_MC_Sample["TT_hdampDOWN"             ]=mc_object("TT_hdampDOWN"                    ,28003470 ,831.76 ,ROOT.kRed-4)
    Sys_MC_Sample["TT_hdampUP"               ]=mc_object("TT_hdampUP"                      ,29151802 ,831.76 ,ROOT.kRed-4)
    Sys_MC_Sample["TT_isrdown"               ]=mc_object("TT_isrdown"                      ,28744718 ,831.76 ,ROOT.kRed-4)
    Sys_MC_Sample["TT_isrup"                 ]=mc_object("TT_isrup"                        ,57577179 ,831.76 ,ROOT.kRed-4)
    Sys_MC_Sample["TT_mtop1695"              ]=mc_object("TT_mtop1695"                     ,19295090 ,831.76 ,ROOT.kRed-4)
    Sys_MC_Sample["TT_mtop1755"              ]=mc_object("TT_mtop1755"                     ,28979681 ,831.76 ,ROOT.kRed-4)
    Sys_MC_Sample["TT_TuneEE5C"              ]=mc_object("TT_TuneEE5C"                     ,27034509 ,831.76 ,ROOT.kRed-4)
    Sys_MC_Sample["ST_tW_herwigpp_top"       ]=mc_object("ST_tW_herwigpp_top"              ,3200997 ,19.47   ,ROOT.kRed-4)
    Sys_MC_Sample["ST_tW_DS_top"             ]=mc_object("ST_tW_DS_top"                    ,3192538 ,19.47   ,ROOT.kRed-4)
    Sys_MC_Sample["ST_tW_MEscaledown_top"    ]=mc_object("ST_tW_MEscaledown_top"           ,3051991 ,19.47   ,ROOT.kRed-4)
    Sys_MC_Sample["ST_tW_MEscaleup_top"      ]=mc_object("ST_tW_MEscaleup_top"             ,3188665 ,19.47   ,ROOT.kRed-4)
    Sys_MC_Sample["ST_tW_PSscaledown_top"    ]=mc_object("ST_tW_PSscaledown_top"           ,3181559 ,19.47   ,ROOT.kRed-4)
    Sys_MC_Sample["ST_tW_PSscaleup_top"      ]=mc_object("ST_tW_PSscaleup_top"             ,3124846 ,19.47   ,ROOT.kRed-4)
    Sys_MC_Sample["ST_tW_fsrdown_top"        ]=mc_object("ST_tW_fsrdown_top"               ,2935595 ,19.47   ,ROOT.kRed-4)
    Sys_MC_Sample["ST_tW_fsrup_top"          ]=mc_object("ST_tW_fsrup_top"                 ,3192325 ,19.47   ,ROOT.kRed-4)
    Sys_MC_Sample["ST_tW_herwigpp_top"       ]=mc_object("ST_tW_herwigpp_top"              ,3200997 ,19.47   ,ROOT.kRed-4)
    Sys_MC_Sample["ST_tW_isrdown_top"        ]=mc_object("ST_tW_isrdown_top"               ,3181500 ,19.47   ,ROOT.kRed-4)
    Sys_MC_Sample["ST_tW_isrup_top"          ]=mc_object("ST_tW_isrup_top"                 ,3110339 ,19.47   ,ROOT.kRed-4)
    Sys_MC_Sample["ST_tW_mtop1695_top"       ]=mc_object("ST_tW_mtop1695_top"              ,3178900 ,19.47   ,ROOT.kRed-4)
    Sys_MC_Sample["ST_tW_mtop1755_top"       ]=mc_object("ST_tW_mtop1755_top"              ,2938402 ,19.47   ,ROOT.kRed-4)
    Sys_MC_Sample["ST_tW_herwigpp_antitop"   ]=mc_object("ST_tW_herwigpp_antitop"          ,3096291 ,19.47   ,ROOT.kRed-4)
    Sys_MC_Sample["ST_tW_DS_antitop"         ]=mc_object("ST_tW_DS_antitop"                ,3098002 ,19.47   ,ROOT.kRed-4)
    Sys_MC_Sample["ST_tW_MEscaledown_antitop"]=mc_object("ST_tW_MEscaledown_antitop"       ,1575142 ,19.47   ,ROOT.kRed-4)
    Sys_MC_Sample["ST_tW_MEscaleup_antitop"  ]=mc_object("ST_tW_MEscaleup_antitop"         ,1606961 ,19.47   ,ROOT.kRed-4)
    Sys_MC_Sample["ST_tW_PSscaledown_antitop"]=mc_object("ST_tW_PSscaledown_antitop"       ,1568912 ,19.47   ,ROOT.kRed-4)
    Sys_MC_Sample["ST_tW_PSscaleup_antitop"  ]=mc_object("ST_tW_PSscaleup_antitop"         ,1608419 ,19.47   ,ROOT.kRed-4)
    Sys_MC_Sample["ST_tW_fsrdown_antitop"    ]=mc_object("ST_tW_fsrdown_antitop"           ,3234964 ,19.47   ,ROOT.kRed-4)
    Sys_MC_Sample["ST_tW_fsrup_antitop"      ]=mc_object("ST_tW_fsrup_antitop"             ,3001527 ,19.47   ,ROOT.kRed-4)
    Sys_MC_Sample["ST_tW_isrdown_antitop"    ]=mc_object("ST_tW_isrdown_antitop"           ,3101321 ,19.47   ,ROOT.kRed-4)
    Sys_MC_Sample["ST_tW_isrup_antitop"      ]=mc_object("ST_tW_isrup_antitop"             ,3076275 ,19.47   ,ROOT.kRed-4)
    Sys_MC_Sample["ST_tW_mtop1695_antitop"   ]=mc_object("ST_tW_mtop1695_antitop"          ,2968744 ,19.47   ,ROOT.kRed-4)
    Sys_MC_Sample["ST_tW_mtop1755_antitop"   ]=mc_object("ST_tW_mtop1755_antitop"          ,3194626 ,19.47   ,ROOT.kRed-4)


    system_list=[]
    system_list.append("nominal")            
    if add_sys_uncertainty: 
        system_list.append("luminosity_up")            
        system_list.append("luminosity_down")            
#        system_list.append("bgk_ST_ST_anti_scale_up")            
#        system_list.append("bgk_ST_ST_anti_scale_down")            
#        system_list.append("bgk_TTTo2L2Nu_scale_up")     
#        system_list.append("bgk_TTTo2L2Nu_scale_down")     
        system_list.append("bgk_DYJetsToLL_M10to50_amc_DYJetsToLL_M50_amc_scale_up")    
        system_list.append("bgk_DYJetsToLL_M10to50_amc_DYJetsToLL_M50_amc_scale_down")    
        system_list.append("bgk_TTWJetsToLNu_TTWJetsToQQ_scale_up")   
        system_list.append("bgk_TTWJetsToLNu_TTWJetsToQQ_scale_down")   
        system_list.append("bgk_TTZToQQ_TTZToLLNuNu_scale_up")   
        system_list.append("bgk_TTZToQQ_TTZToLLNuNu_scale_down")   
        system_list.append("bgk_TTGJets_scale_up")       
        system_list.append("bgk_TTGJets_scale_down")       
        system_list.append("bgk_WJet_scale_up")          
        system_list.append("bgk_WJet_scale_down")          
        system_list.append("bgk_WWTo2L2Nu_scale_up")     
        system_list.append("bgk_WWTo2L2Nu_scale_down")     
        system_list.append("bgk_WZ_2L2Q_WZ_3LNu_scale_up")       
        system_list.append("bgk_WZ_2L2Q_WZ_3LNu_scale_down")       
        system_list.append("bgk_ZZ_4L_ZZ_2L2Nu_scale_up")      
        system_list.append("bgk_ZZ_4L_ZZ_2L2Nu_scale_down")      
        system_list.append("bgk_WG_LNuG_scale_up")       
        system_list.append("bgk_WG_LNuG_scale_down")       
        system_list.append("bgk_GGHWWTo2L2Nu_scale_up")       
        system_list.append("bgk_GGHWWTo2L2Nu_scale_down")       
        system_list.append("bgk_VBFHWWTo2L2Nu_scale_up")       
        system_list.append("bgk_VBFHWWTo2L2Nu_scale_down")       

        system_list.append("PU_scale_up"       )         
        system_list.append("PU_scale_down"     )       
        system_list.append("SmearedJetResUp"   )     
        system_list.append("SmearedJetResDown" )   
        system_list.append("JetEnUp"           )             
        system_list.append("JetEnDown"         )           
        system_list.append("BtagSFbcUp"        )          
        system_list.append("BtagSFbcDown"      )        
        system_list.append("BtagSFudsgUp"      )        
        system_list.append("BtagSFudsgDown"    )      
        system_list.append("EleSFReco_up"      )   
        system_list.append("EleSFReco_down"    )
        system_list.append("EleSFID_up"        )
        system_list.append("EleSFID_down"      )
        system_list.append("MuonSFID_up"       )
        system_list.append("MuonSFID_down"     )
        system_list.append("MuonSFIso_up"      )
        system_list.append("MuonSFIso_down"    )
        system_list.append("MuonSFtrack_up"    )
        system_list.append("MuonSFtrack_down"  )
        system_list.append("UnclusteredEnUp"   )       
        system_list.append("UnclusteredEnDown" )       
        system_list.append("TrigSF_up"         )       
        system_list.append("TrigSF_down"       )               

        ########## Systematic sample ##############
#        system_list.append("Sample_TT_QCDbasedCRTune_erdON"                )
#        system_list.append("Sample_TT_GluonMoveCRTune"                )
#        system_list.append("Sample_TT_erdON"                )
        system_list.append("isrup"                       )
        system_list.append("isrdown"                     )
        system_list.append("fsrup"                       )
        system_list.append("fsrdown"                     )
        system_list.append("Sample_TT_TuneEE5C"          )
        system_list.append("Sample_TT_CR"                )
        system_list.append("Sample_TT_PDF_Up"            )
        system_list.append("Sample_TT_PDF_Down"          )
        system_list.append("Sample_TT_mtop1695"          )
        system_list.append("Sample_TT_mtop1755"          )
        system_list.append("Sample_TT_TuneCUETP8M2T4down")
        system_list.append("Sample_TT_TuneCUETP8M2T4up"  )
        system_list.append("Sample_TT_hdampDOWN"         )
        system_list.append("Sample_TT_hdampUP"           )
#        system_list.append("Sample_TT_isrdown"           )
#        system_list.append("Sample_TT_isrup"             )
#        system_list.append("Sample_TT_fsrdown"           )
#        system_list.append("Sample_TT_fsrup"             )
        system_list.append("Sample_ST_tW_herwigpp"       )
        system_list.append("Sample_ST_tW_DS"             )
        system_list.append("Sample_ST_tW_mtop1695"       )
        system_list.append("Sample_ST_tW_mtop1755"       )
        system_list.append("Sample_ST_tW_MEscaledown"    )
        system_list.append("Sample_ST_tW_MEscaleup"      )
##        system_list.append("Sample_ST_tW_PSscaledown"    )
##        system_list.append("Sample_ST_tW_PSscaleup"      )
#        system_list.append("Sample_ST_tW_isrdown"        )
#        system_list.append("Sample_ST_tW_isrup"          )
#        system_list.append("Sample_ST_tW_fsrdown"        )
#        system_list.append("Sample_ST_tW_fsrup"          )
        if remove_herwig:
            system_list.remove("Sample_TT_TuneEE5C") 
            system_list.remove("Sample_ST_tW_herwigpp") 
    dict_system_table_name={ 
 "nominal"                                : "nominal",
"luminosity_up"                           :"luminosity\_up", 
"luminosity_down"                         :"luminosity\_down",
"bgk_DYJetsToLL_M10to50_amc_DYJetsToLL_M50_amc_scale_up"  :  "DY\_up",    
"bgk_DYJetsToLL_M10to50_amc_DYJetsToLL_M50_amc_scale_down":  "DY\_down",      
"bgk_TTWJetsToLNu_TTWJetsToQQ_scale_up"   :  "TTW\_up",   
"bgk_TTWJetsToLNu_TTWJetsToQQ_scale_down" :  "TTW\_down",   
"bgk_TTZToQQ_TTZToLLNuNu_scale_up"        :  "TTZ\_up",   
"bgk_TTZToQQ_TTZToLLNuNu_scale_down"      :  "TTZ\_down",   
"bgk_TTGJets_scale_up"                    :  "TTGJets\_up",       
"bgk_TTGJets_scale_down"                  :  "TTGJets\_down",       
"bgk_WJet_scale_up"                       :  "Jets\_up",          
"bgk_WJet_scale_down"                     :  "Jets\_down",          
"bgk_WWTo2L2Nu_scale_up"                  :  "WW\_up",     
"bgk_WWTo2L2Nu_scale_down"                :  "WW\_down",     
"bgk_WZ_2L2Q_WZ_3LNu_scale_up"            :  "WZ\_up",       
"bgk_WZ_2L2Q_WZ_3LNu_scale_down"          :  "WZ\_down",       
"bgk_ZZ_4L_ZZ_2L2Nu_scale_up"             :  "ZZ\_up",      
"bgk_ZZ_4L_ZZ_2L2Nu_scale_down"           :  "ZZ\_down",      
"bgk_WG_LNuG_scale_up"                    :  "WG\_up",       
"bgk_WG_LNuG_scale_down"                  :  "WG\_down",       
"TrigSF_up"                               :  "TriggerSF\_up",       
"TrigSF_down"                             :  "TriggerSF\_down",       
"UnclusteredEnUp"                         :  "UnclusteredEn\_up", 
"UnclusteredEnDown"                       :  "UnclusteredEn\_down", 
"PU_scale_up"                             : "PileUp\_up",
"PU_scale_down"                           : "PileUp\_down",
"SmearedJetResUp"                         : "JER\_up",
"SmearedJetResDown"                       : "JER\_down",
"JetEnUp"                                 : "JES\_up",
"JetEnDown"                               : "JES\_down",
"BtagSFbcUp"                              : "BTagSF\_bc\_up",
"BtagSFbcDown"                            : "BTagSF\_bc\_down",
"BtagSFudsgUp"                            : "BTagSF\_udsg\_up",
"BtagSFudsgDown"                          : "BTagSF\_udsg\_down",
"EleSFReco_up"                            : "EleRecoSF\_up",
"EleSFReco_down"                          : "EleRecoSF\_down",
"EleSFID_up"                              : "EleIDIsoSF\_up",
"EleSFID_down"                            : "EleIDIsoSF\_down",
"MuonSFID_up"                             : "MuIDSF\_up",
"MuonSFID_down"                           : "MuIDSF\_down",
"MuonSFIso_up"                            : "MuIsoSF\_up",
"MuonSFIso_down"                          : "MuIsoSF\_down",
"MuonSFtrack_up"                          : "MuTrackSF\_up",
"MuonSFtrack_down"                        : "MuTrackSF\_down",
"isrup"                                   :"ISR\_up"                ,
"isrdown"                                 :"ISR\_down"              ,
"fsrup"                                   :"FSR\_up"                ,
"fsrdown"                                 :"FSR\_down"              ,
"Sample_TT_TuneCUETP8M2T4down"            :"TT\_Tune\_down",
"Sample_TT_TuneCUETP8M2T4up"              :"TT\_Tune\_up",
"Sample_TT_CR"                            :"TT\_CR",
"Sample_TT_PDF_Up"                        :"TT\_PDF\_Up",
"Sample_TT_PDF_Down"                      :"TT\_PDF\_Down",
"Sample_TT_fsrdown"                       :"TT\_fsr\_down",
"Sample_TT_fsrup"                         :"TT\_fsr\_up",
"Sample_TT_hdampDOWN"                     :"TT\_hdamp\_down",
"Sample_TT_hdampUP"                       :"TT\_hdamp\_up",
"Sample_TT_isrdown"                       :"TT\_isr\_down",
"Sample_TT_isrup"                         :"TT\_isr\_up",
"Sample_TT_mtop1695"                      :"TT\_TopMass\_down",
"Sample_TT_mtop1755"                      :"TT\_TopMass\_up",
"Sample_TT_TuneEE5C"                      :"TT\_herwig++",
"Sample_ST_tW_herwigpp"                   :"TW\_herwig++",
"Sample_ST_tW_DS"                         :"TW\_DS",
"Sample_ST_tW_MEscaledown"                :"TW\_MEscale\_down",
"Sample_ST_tW_MEscaleup"                  :"TW\_MEscale\_up",
"Sample_ST_tW_PSscaledown"                :"TW\_PSscale\_down",
"Sample_ST_tW_PSscaleup"                  :"TW\_PSscale\_up",
"Sample_ST_tW_fsrdown"                    :"TW\_fsr\_down",
"Sample_ST_tW_fsrup"                      :"TW\_fsr\_up",
"Sample_ST_tW_isrdown"                    :"TW\_isr\_down",
"Sample_ST_tW_isrup"                      :"TW\_isr\_up",
"Sample_ST_tW_mtop1695"                   :"TW\_TopMass\_down",
"Sample_ST_tW_mtop1755"                   :"TW\_TopMass\_up"  
}
    dict_system_name1={
 "nominal"          : "nominal",
 "PU_scale_up"      : "PileUp_Up",
 "PU_scale_down"    : "PileUp_Down",
 "SmearedJetResUp"  : "JetEnergyResolution_Up",
 "SmearedJetResDown": "JetEnergyResolution_Down",
 "JetEnUp"          : "JetEnergyScale_Up",
 "JetEnDown"        : "JetEnergyScale_Down",
 "BtagSFbcUp"       : "BtagScaleFactor_bc_Up",
 "BtagSFbcDown"     : "BtagScaleFactor_bc_Down",
 "BtagSFudsgUp"     : "BtagScaleFactor_udsg_Up",
 "BtagSFudsgDown"   : "BtagScaleFactor_udsg_Down",
 "EleSFReco_up"     : "ElectronReconstructionScaleFactor_Up",
 "EleSFReco_down"   : "ElectronReconstructionScaleFactor_Down",
 "EleSFID_up"       : "ElectronIDIsoScaleFactor_Up",
 "EleSFID_down"     : "ElectronIDIsoScaleFactor_Down",
 "MuonSFID_up"      : "MuonIDScaleFactor_Up",
 "MuonSFID_down"    : "MuonIDScaleFactor_Down",
 "MuonSFIso_up"     : "MuonIsoScaleFactor_Up",
 "MuonSFIso_down"   : "MuonIsoScaleFactor_Down",
 "MuonSFtrack_up"   : "MuonTrackEfficiencyScaleFactor_Up",
 "MuonSFtrack_down" : "MuonTrackEfficiencyScaleFactor_Down",
 "TrigSF_up"        : "TriggerSF_Up",       
 "TrigSF_down"      : "TriggerSF_Down",       
 "UnclusteredEnUp"  : "UnclusteredEn_Up", 
 "UnclusteredEnDown": "UnclusteredEn_Down"} 
    dict_system_name2={
"isrup"                       :"ISR_Up"                ,
"isrdown"                     :"ISR_Down"              ,
"fsrup"                       :"FSR_Up"                ,
"fsrdown"                     :"FSR_Down"              ,
"Sample_TT_TuneCUETP8M2T4down":"TT_Tune_Down"          ,
"Sample_TT_TuneCUETP8M2T4up"  :"TT_Tune_Up"            ,
"Sample_TT_CR"                :"TT_CR"                 ,
"Sample_TT_PDF_Up"            :"TT_PDF_Up"             ,
"Sample_TT_PDF_Down"          :"TT_PDF_Down"           ,
"Sample_TT_fsrdown"           :"TT_fsr_Down"           ,
"Sample_TT_fsrup"             :"TT_fsr_Up"             ,
"Sample_TT_hdampDOWN"         :"TT_hdamp_Down"         ,
"Sample_TT_hdampUP"           :"TT_hdamp_Up"           ,
"Sample_TT_isrdown"           :"TT_isr_Down"           ,
"Sample_TT_isrup"             :"TT_isr_Up"             ,
"Sample_TT_mtop1695"          :"TT_mtop169.5"          ,
"Sample_TT_mtop1755"          :"TT_mtop175.5"          ,
"Sample_TT_TuneEE5C"          :"TT_herwig++"           ,
"Sample_ST_tW_herwigpp"       :"tw_herwig++"           ,
"Sample_ST_tW_DS"             :"tw_DS"                 ,
"Sample_ST_tW_MEscaledown"    :"tw_MEscale_Down"       ,
"Sample_ST_tW_MEscaleup"      :"tw_MEscale_Up"         ,
"Sample_ST_tW_PSscaledown"    :"tw_PSscale_Down"       ,
"Sample_ST_tW_PSscaleup"      :"tw_PSscale_Up"         ,
"Sample_ST_tW_fsrdown"        :"tw_fsr_Down"           ,
"Sample_ST_tW_fsrup"          :"tw_fsr_Up"             ,
"Sample_ST_tW_isrdown"        :"tw_isr_Down"           ,
"Sample_ST_tW_isrup"          :"tw_isr_Up"             ,
"Sample_ST_tW_mtop1695"       :"tw_mtop169.5"          ,
"Sample_ST_tW_mtop1755"       :"tw_mtop175.5"         }
    dict_system_name_limit={
"isrup"                       :"ISR_Up"                ,
"isrdown"                     :"ISR_Down"              ,
"fsrup"                       :"FSR_Up"                ,
"fsrdown"                     :"FSR_Down"              ,
"Sample_TT_TuneCUETP8M2T4down":"TT_Tune_Down"          ,
"Sample_TT_TuneCUETP8M2T4up"  :"TT_Tune_Up"            ,
"Sample_TT_CR"                :"TT_CR"                 ,
"Sample_TT_PDF_Up"            :"TT_PDF_Up"             ,
"Sample_TT_PDF_Down"          :"TT_PDF_Down"           ,
"Sample_TT_fsrdown"           :"TT_fsr_Down"           ,
"Sample_TT_fsrup"             :"TT_fsr_Up"             ,
"Sample_TT_hdampDOWN"         :"TT_hdamp_Down"         ,
"Sample_TT_hdampUP"           :"TT_hdamp_Up"           ,
"Sample_TT_isrdown"           :"TT_isr_Down"           ,
"Sample_TT_isrup"             :"TT_isr_Up"             ,
"Sample_TT_mtop1695"          :"TT_TopMass_Down"       ,
"Sample_TT_mtop1755"          :"TT_TopMass_Up"         ,
"Sample_TT_TuneEE5C"          :"TT_herwig++"           ,
"Sample_ST_tW_herwigpp"       :"tw_herwig++"           ,
"Sample_ST_tW_DS"             :"tw_DS"                 ,
"Sample_ST_tW_MEscaledown"    :"tw_MEscale_Down"       ,
"Sample_ST_tW_MEscaleup"      :"tw_MEscale_Up"         ,
"Sample_ST_tW_PSscaledown"    :"tw_PSscale_Down"       ,
"Sample_ST_tW_PSscaleup"      :"tw_PSscale_Up"         ,
"Sample_ST_tW_fsrdown"        :"tw_fsr_Down"           ,
"Sample_ST_tW_fsrup"          :"tw_fsr_Up"             ,
"Sample_ST_tW_isrdown"        :"tw_isr_Down"           ,
"Sample_ST_tW_isrup"          :"tw_isr_Up"             ,
"Sample_ST_tW_mtop1695"       :"tw_TopMass_Down"       ,
"Sample_ST_tW_mtop1755"       :"tw_TopMass_Up"         }
    dir_system_name={}
    dir_system_name.update(dict_system_name1)
    dir_system_name.update(dict_system_name2)
    dict_sys_limit_name={} 
    dict_sys_limit_name.update(dict_system_name1) 
    dict_sys_limit_name.update(dict_system_name_limit) 

    dir_hist={"H_Mll":"M_{ll} (GeV/c^{2})","H_Mll_Zpeak":"M_{ll} (GeV/c^{2})","H_Ptll":"P_{T}^{ll} (GeV/c)","H_lepton_led_pt":"P_{T}^{leading lepton} (GeV/c)","H_lepton_led_eta":"#eta^{leading lepton}","H_lepton_led_phi":"#phi^{leading lepton}","H_lepton_sub_pt":"P_{T}^{Sub-leading lepton} (GeV/c)","H_lepton_sub_eta":"#eta^{Sub-leading lepton}","H_lepton_sub_phi":"#phi^{Sub-leading lepton}","H_jet_led_pt":"P_{T}^{leading jet} (GeV/c)","H_jet_led_eta":"#eta^{leading jet}","H_jet_led_phi":"#phi^{leading jet}","H_jet_sub_pt":"P_{T}^{Sub-leading jet} (GeV/c)","H_jet_sub_eta":"#eta^{Sub-leading jet}","H_jet_sub_phi":"#phi^{Sub-leading jet}","H_jet_forward_led_pt":"P_{T}^{leading jet}(2.4<|#eta|<5.2) (GeV/c)","H_N_loose_jets":"Number of jet","H_N_loose_jets_low":"Number of jet(20<Pt<30)","H_N_b_jets":"Number of bjet","H_N_b_jets_low":"Number of bjet(20<Pt<30)","H_N_eta2p4_30_jets":"N jets(2.4<|#eta|<5.2,Pt>30)","H_N_eta2p4_40_jets":"N jets(2.4<|#eta|<5.2,Pt>40)","H_MET_Et":"MET","H_MET_phi":"MET_{#phi}","H_MET_Z_phi":"#Delta#phi(MET,ll)","H_MET_T1Txy_et":"MET(T1Txy)","H_MET_T1Txy_phi":"MET(T1Txy)_{#phi}","H_MET_Z_T1Txy_phi":"#Delta#phi(MET(T1Txy),ll)","H_MET_T1Txy_sf":"MET(T1Txy)_{significance}","H_HT_sys":"HT^{sys}","H_Pt_sys":"Pt^{sys}","H_MT_sys":"MT^{sys}","H_pv_n":"Nvtx","H_rho":"#rho","H_njet_bjet":"(jet,bjet) multiplicity","H_Ptll_phi":"#phi_{ll}","H_ll_Dphi":"#Delta#phi(ll)","H_ll_DR":"#DeltaR(ll)","H_Rll":"Rapidity(ll)","H_N_b_jets_low":"Number of bjet(20-30 GeV)","H_jet_low_led_CSV":"CSV^{Leading jet} (20<Pt<30)","H_jet_Bmissed_CSV":"CSV(jet in 2j1t)","H_HT":"HT","H_Limit_N_jet_bjet":"(jet,bjet) multiplicity","H_N_loose_jets_pt20":"Number of jet(P_{T}>20)"}
    ###### hist name saved for limit #########
    #dir_MVA={"H_MLP_0jet_0bjet":"MLP(0jet,0bjet)","H_MLP_1jet_0bjet":"MLP(1jet,0bjet)","H_MLP_1jet_1bjet":"MLP(1jet,1bjet)","H_MLP_2jet_1bjet":"MLP(2jet,1bjet)","H_MLP_2jet_2bjet":"MLP(2jet,2bjet)"}
    #dir_MVA={"H_MLP_0jet_0bjet":"MLP(0jet,0bjet)","H_MLP_1jet_0bjet":"MLP(1jet,0bjet)","H_MLP_1jet_1bjet":"MLP(1jet,1bjet)","H_MLP_2jet_1bjet":"MLP(2jet,1bjet)","H_2j2b_j1_pt":""}
    #dir_MVA={"H_MLP_0jet_0bjet":"MLP(0jet,0bjet)","H_MLP_1jet_0bjet_comb":"MLP(1jet,0bjet)","H_MLP_1jet_1bjet_comb":"MLP(1jet,1bjet)","H_MLP_2jet_1bjet_comb":"MLP(2jet,1bjet)","H_MLP_2jet_2bjet":""}
    #dir_MVA={"H_MLP_tug_0jet_0bjet":"MLP(0jet,0bjet)","H_MLP_tug_1jet_0bjet":"MLP(1jet,0bjet)","H_MLP_tug_1jet_1bjet":"MLP(1jet,1bjet)","H_MLP_tug_2jet_1bjet":"MLP(2jet,1bjet)","H_MLP_tug_2jet_2bjet":"MLP(2jet,2bjet)"}
    dir_MVA={"H_MLP_tcg_0jet_0bjet":"MLP(0jet,0bjet)","H_MLP_tcg_1jet_0bjet":"MLP(1jet,0bjet)","H_MLP_tcg_1jet_1bjet":"MLP(1jet,1bjet)","H_MLP_tcg_2jet_1bjet":"MLP(2jet,1bjet)","H_MLP_tcg_2jet_2bjet":"MLP(2jet,2bjet)"}
#    dir_MVA={"H_BDT_0jet_0bjet":"BDT(0jet,0bjet)","H_BDT_1jet_0bjet":"BDT(1jet,0bjet)","H_BDT_1jet_1bjet":"BDT(1jet,1bjet)","H_BDT_2jet_1bjet":"BDT(2jet,1bjet)","H_BDT_2jet_2bjet":"BDT(2jet,2bjet)"}
#    dir_MVA={"H_0jet_0bjet":"(0jet,0bjet)","H_1jet_0bjet":"(1jet,0bjet)","H_1jet_1bjet":"(1jet,1bjet)","H_2jet_1bjet":"(2jet,1bjet)","H_2jet_2bjet":"(2jet,2bjet)"}
    ########################################
    dir_MVA_all={"H_MLP_all":"MLP","H_BDT_all":"BDT","H_MLP_all_v1":"MLP","H_BDT_all_v1":"BDT"}
    dir_MVA_MLP={"H_MLP_0jet_0bjet":"NN output","H_MLP_1jet_0bjet":"NN output","H_MLP_1jet_1bjet":"NN output","H_MLP_2jet_1bjet":"NN output","H_MLP_2jet_2bjet":"NN output"}
    dir_MVA_BDT={"H_BDT_0jet_0bjet":"BDT output","H_BDT_1jet_0bjet":"BDT output","H_BDT_1jet_1bjet":"BDT output","H_BDT_2jet_1bjet":"BDT output","H_BDT_2jet_2bjet":"BDT output"}
    dir_MVA_1bin={"H_0jet_0bjet":"(0jet,0bjet)","H_1jet_0bjet":"(1jet,0bjet)","H_1jet_1bjet":"(1jet,1bjet)","H_2jet_1bjet":"(2jet,1bjet)","H_2jet_2bjet":"(2jet,2bjet)"}
    dir_MVA_comb={"H_MLP_0jet_0bjet_comb":"NN output","H_MLP_1jet_0bjet_comb":"NN output","H_MLP_1jet_1bjet_comb":"NN output","H_MLP_2jet_1bjet_comb":"NN output","H_MLP_2jet_2bjet_comb":"NN output"}
    dir_MVA_FCNC_tug={"H_MLP_tug_all":"NN output","H_BDT_tug_all":"BDT","H_MLP_tug_all_v1":"NN output","H_BDT_tug_all_v1":"BDT","H_MLP_tug_0jet_0bjet":"NN output","H_MLP_tug_1jet_0bjet":"NN output","H_MLP_tug_1jet_1bjet":"NN output","H_MLP_tug_2jet_1bjet":"NN output","H_MLP_tug_2jet_2bjet":"NN output","H_BDT_tug_0jet_0bjet":"BDT","H_BDT_tug_1jet_0bjet":"BDT","H_BDT_tug_1jet_1bjet":"BDT","H_BDT_tug_2jet_1bjet":"BDT","H_BDT_tug_2jet_2bjet":"BDT"}
    dir_MVA_FCNC_tcg={"H_MLP_tcg_all":"NN output","H_BDT_tcg_all":"BDT","H_MLP_tcg_all_v1":"NN output","H_BDT_tcg_all_v1":"BDT","H_MLP_tcg_0jet_0bjet":"NN output","H_MLP_tcg_1jet_0bjet":"NN output","H_MLP_tcg_1jet_1bjet":"NN output","H_MLP_tcg_2jet_1bjet":"NN output","H_MLP_tcg_2jet_2bjet":"NN output","H_BDT_tcg_0jet_0bjet":"BDT","H_BDT_tcg_1jet_0bjet":"BDT","H_BDT_tcg_1jet_1bjet":"BDT","H_BDT_tcg_2jet_1bjet":"BDT","H_BDT_tcg_2jet_2bjet":"BDT"}
    dir_MVA_variables={
"H_0j0b_l1_pt"             : "P_{T}^{leading lepton} (GeV/c)",
"H_0j0b_N_loose_jets_low"  : "Number of jet(20<Pt<30)",
"H_0j0b_Ptll"              : "P_{T}^{ll} (GeV/c)",
"H_0j0b_dPt_l1_l2"         : "#DeltaP_{T}(l,l)",
"H_0j0b_Mll"               : "M_{ll} (GeV/c^{2})",
"H_0j0b_Cll"               : "Centrality(ll)",
"H_1j0b_l1_pt"             : "P_{T}^{leading lepton} (GeV/c)",
"H_1j0b_N_loose_jets_low"  : "Number of jet(20<Pt<30)",
"H_1j0b_Ptll"              : "P_{T}^{ll} (GeV/c)",
"H_1j0b_dPt_l1_l2"         : "#DeltaP_{T}(l,l)",
"H_1j0b_Mll"               : "M_{ll} (GeV/c^{2})",
"H_1j0b_Cll"               : "Centrality(ll)",
"H_1j0b_Cl1_j1"            : "Centrality(l^{leading}jet^{leading})",
"H_1j0b_dPhi_ll_j1"        : "#Delta#phi(ll,jet^{leading})",
"H_1j1b_led_Fjet_pt"       : "P_{T}^{leading jet}(2.4<|#eta|<5.2) (GeV/c)",
"H_1j1b_N_Fjet"            : "N jets(2.4<|#eta|<5.2,Pt>30)",
"H_1j1b_led_Lowjet"        : "P_{T}^{leading jet}(20<Pt<30) (GeV/c)",
"H_1j1b_N_Lowjet"          : "Number of jet(20<Pt<30)",
"H_1j1b_N_Lowbjet"         : "Number of bjet(20<Pt<30)",
"H_1j1b_ll_j1_pt"          : "P_{T}^{ll,jet^{leading}} (GeV/c)",
"H_1j1b_dR_l1_j1"          : "#DeltaR(lepton^{leading},jet^{leading})",
"H_1j1b_dR_l1_l2"          : "#DeltaR(l,l)",
"H_1j1b_dPhi_ll_j1"        : "#Delta#phi(ll,jet^{leading})",
"H_1j1b_Cll"               : "Centrality(ll)",
"H_1j1b_Cll_j1"            : "Centrality(lljet^{leading})",
"H_1j1b_l1_j1_pt"          : "P_{T}^{leading lepton,leading jet} (GeV/c)",
"H_2j1b_N_jet_low_low"     : "Number of jet(20<Pt<30)",
"H_2j1b_l1_pt"             : "P_{T}^{leading lepton} (GeV/c)",
"H_2j1b_Ptll"              : "P_{T}^{ll} (GeV/c)",
"H_2j1b_j2_pt"             : "P_{T}^{sub-leading jet} (GeV/c)",
"H_2j1b_dPt_l2_j2"         : "#DeltaP_{T}(l^{sub},jet^{sub}) (GeV/c)",
"H_2j1b_dR_l1_j2"          : "#DeltaR(lepton^{leading},jet^{sub})",
"H_2j1b_dR_ll_j1"          : "#DeltaR(ll,jet^{leading})",
"H_2j1b_dPhi_ll_j1"        : "#Delta#phi(ll,jet^{leading})",
"H_2j1b_M_l1_j2"           : "M(lepton^{leading},jet^{sub-leading}) (GeV/c^{2})",
"H_2j1b_M_j1_j2"           : "M(jet^{leading},jet^{sub-leading}) (GeV/c^{2})",
    }
    dir_2j2b_variables={
"H_2j2b_l1_pt"             :"P_{T}^{leading lepton} (GeV/c)", 
"H_2j2b_l2_pt"             :"P_{T}^{sub-leading lepton} (GeV/c)", 
"H_2j2b_j1_pt"             :"P_{T}^{leading jet} (GeV/c)", 
"H_2j2b_j2_pt"             :"P_{T}^{sub-leading jet} (GeV/c)", 
"H_2j2b_dphi_ll"           :"#Delta#phi(l,l)", 
"H_2j2b_dphi_ll_j1"        :"#Delta#phi(ll,jet^{leading})" 
    }
    dir_BSM_MVA_variables={
"H_BSM_l1_pt"              : "P_{T}^{leading lepton} (GeV/c)",
"H_BSM_Ptll"               : "P_{T}^{ll} (GeV/c)",
"H_BSM_dPt_l1_l2"          : "#DeltaP_{T}(l,l)",
"H_BSM_Mll"                : "M_{ll} (GeV/c^{2})",
"H_BSM_Cll"                : "Centrality(ll)",
"H_BSM_ll_j1_pt"           : "P_{T}^{ll,jet^{leading}} (GeV/c)",
"H_BSM_dR_ll_j1"           : "#DeltaR(ll,jet^{leading})",
"H_BSM_M_l2_j1"            : "M(lepton^{sub-leading},jet^{leading}) (GeV/c^{2})",
"H_BSM_Cl1_j1"             : "Centrality(lljet^{leading})",
"H_BSM_0j0b_l1_pt"         : "P_{T}^{leading lepton} (GeV/c)",
"H_BSM_0j0b_Ptll"          : "P_{T}^{ll} (GeV/c)",
"H_BSM_0j0b_dPt_l1_l2"     : "#DeltaP_{T}(l,l)",
"H_BSM_0j0b_Mll"           : "M_{ll} (GeV/c^{2})",
"H_BSM_0j0b_Cll"           : "Centrality(ll)",
"H_BSM_0j0b_ll_j1_pt"      : "P_{T}^{ll,jet^{leading}} (GeV/c)",
"H_BSM_0j0b_dR_ll_j1"      : "#DeltaR(ll,jet^{leading})",
"H_BSM_0j0b_M_l2_j1"       : "M(lepton^{sub-leading},jet^{leading}) (GeV/c^{2})",
"H_BSM_0j0b_Cl1_j1"        : "Centrality(lljet^{leading})",
"H_BSM_1j0b_l1_pt"         : "P_{T}^{leading lepton} (GeV/c)",
"H_BSM_1j0b_Ptll"          : "P_{T}^{ll} (GeV/c)",
"H_BSM_1j0b_dPt_l1_l2"     : "#DeltaP_{T}(l,l)",
"H_BSM_1j0b_Mll"           : "M_{ll} (GeV/c^{2})",
"H_BSM_1j0b_Cll"           : "Centrality(ll)",
"H_BSM_1j0b_ll_j1_pt"      : "P_{T}^{ll,jet^{leading}} (GeV/c)",
"H_BSM_1j0b_dR_ll_j1"      : "#DeltaR(ll,jet^{leading})",
"H_BSM_1j0b_M_l2_j1"       : "M(lepton^{sub-leading},jet^{leading}) (GeV/c^{2})",
"H_BSM_1j0b_Cl1_j1"        : "Centrality(lljet^{leading})",
"H_BSM_1j1b_l1_pt"         : "P_{T}^{leading lepton} (GeV/c)",
"H_BSM_1j1b_Ptll"          : "P_{T}^{ll} (GeV/c)",
"H_BSM_1j1b_dPt_l1_l2"     : "#DeltaP_{T}(l,l)",
"H_BSM_1j1b_Mll"           : "M_{ll} (GeV/c^{2})",
"H_BSM_1j1b_Cll"           : "Centrality(ll)",
"H_BSM_1j1b_ll_j1_pt"      : "P_{T}^{ll,jet^{leading}} (GeV/c)",
"H_BSM_1j1b_dR_ll_j1"      : "#DeltaR(ll,jet^{leading})",
"H_BSM_1j1b_M_l2_j1"       : "M(lepton^{sub-leading},jet^{leading}) (GeV/c^{2})",
"H_BSM_1j1b_Cl1_j1"        : "Centrality(lljet^{leading})",
"H_BSM_2j1b_l1_pt"         : "P_{T}^{leading lepton} (GeV/c)",
"H_BSM_2j1b_Ptll"          : "P_{T}^{ll} (GeV/c)",
"H_BSM_2j1b_dPt_l1_l2"     : "#DeltaP_{T}(l,l)",
"H_BSM_2j1b_Mll"           : "M_{ll} (GeV/c^{2})",
"H_BSM_2j1b_Cll"           : "Centrality(ll)",
"H_BSM_2j1b_ll_j1_pt"      : "P_{T}^{ll,jet^{leading}} (GeV/c)",
"H_BSM_2j1b_dR_ll_j1"      : "#DeltaR(ll,jet^{leading})",
"H_BSM_2j1b_M_l2_j1"       : "M(lepton^{sub-leading},jet^{leading}) (GeV/c^{2})",
"H_BSM_2j1b_Cl1_j1"        : "Centrality(lljet^{leading})"
    }
    dir_Rinout_variables={
"H_Rinout_Mll_all"  : "M_{ll} (GeV/c^{2})", 
"H_Rinout_Mll_0j0b" : "M_{ll} (GeV/c^{2})", 
"H_Rinout_Mll_1j0b" : "M_{ll} (GeV/c^{2})", 
"H_Rinout_Mll_1j1b" : "M_{ll} (GeV/c^{2})", 
"H_Rinout_Mll_2j1b" : "M_{ll} (GeV/c^{2})", 
"H_Rinout_Mll_2j2b" : "M_{ll} (GeV/c^{2})", 
    }


    dir_hist.update(dir_MVA_MLP)
    dir_hist.update(dir_MVA_BDT)
    dir_hist.update(dir_MVA_1bin)
    dir_hist.update(dir_MVA_comb)
    dir_hist.update(dir_MVA_variables)
    dir_hist.update(dir_2j2b_variables)##for 2j2b variable
    dir_hist.update(dir_Rinout_variables)##for Rin/out mll variable
#    dir_hist.update(dir_MVA_all)
#    dir_hist.update(dir_BSM_MVA_variables)
    if Do_FCNC_Study:
        dir_hist.update(dir_MVA_FCNC_tug)
        dir_hist.update(dir_MVA_FCNC_tcg)

    print "begin save hist"
    all_sys_uncert=sys_uncert_object("all_system_uncert", system_list, Files, MC_Sample, Sys_MC_Sample, dir_hist)
    all_sys_uncert.save_hist()
    all_system_hist=all_sys_uncert.all_hist
    all_sys_uncert.close_file()
    print "saved hist:nsys:ssample!"
    if do_same_sign:
        print "begin save hist for same-sign"
        all_sys_uncert_ss=sys_uncert_object("all_system_uncert_same_sign", system_list, Files_same_sign, MC_Sample, Sys_MC_Sample, dir_hist)
        all_sys_uncert_ss.save_hist()
        all_system_hist_ss=all_sys_uncert_ss.all_hist
        all_sys_uncert_ss.close_file()
        print "saved hist:nsys:ssample for same-sign!"
        for hname in all_system_hist_ss:
            for nsys in all_system_hist_ss[hname]:
                h_ss=all_system_hist_ss[hname][nsys]["data"].Clone("%s__WJet_mad_ss__%s"%(nsys,hname))
                for sname in all_system_hist_ss[hname][nsys]:
                    if sname == "WJet_mad" or sname == "data" or "FCNC" in sname:continue
                    h_ss.Add(all_system_hist_ss[hname][nsys][sname],-1)
                for ibin in range(1,h_ss.GetNbinsX()+1):
                    h_ss.SetBinError(ibin,0)
                    if h_ss.GetBinContent(ibin)<0:h_ss.SetBinContent(ibin,0)
                all_system_hist[hname][nsys]["WJet_mad"]=h_ss
                if nsys=="bgk_WJet_scale_up":
                    all_system_hist[hname][nsys]["WJet_mad"].Scale(1.5)#50% uncertainty
                elif nsys=="bgk_WJet_scale_down":
                    all_system_hist[hname][nsys]["WJet_mad"].Scale(0.5)

        print "replaced Wjet with same-sign!"
    print "begin add systematic all,TT,TW hist"
    hist_sys_mc_all={}
    hist_sys_mc_TT={}
    hist_sys_mc_TW={}
    for hname in all_system_hist:
        hist_sys_mc_all[hname]={}
        hist_sys_mc_TT[hname]={}
        hist_sys_mc_TW[hname]={}
        for nsys in all_system_hist[hname]:
            hist_sys_mc_all[hname][nsys]=all_system_hist[hname][nsys]["data"].Clone("%s__%s__mc_all"%(hname,nsys))
            hist_sys_mc_all[hname][nsys].Scale(0)
            hist_sys_mc_TT[hname][nsys]=all_system_hist[hname][nsys]["data"].Clone("%s__%s__mc_TT"%(hname,nsys))
            hist_sys_mc_TT[hname][nsys].Scale(0)
            hist_sys_mc_TW[hname][nsys]=all_system_hist[hname][nsys]["data"].Clone("%s__%s__mc_TW"%(hname,nsys))
            hist_sys_mc_TW[hname][nsys].Scale(0)
            for sname in all_system_hist[hname][nsys]:
                if "data" in sname or "FCNC" in sname:continue
                hist_sys_mc_all[hname][nsys].Add(all_system_hist[hname][nsys][sname]) 
                if "TTTo2L2Nu" in sname:
                    hist_sys_mc_TT[hname][nsys].Add(all_system_hist[hname][nsys][sname]) 
                elif "TW_" in sname:
                    hist_sys_mc_TW[hname][nsys].Add(all_system_hist[hname][nsys][sname]) 
    print "added systematic all,TT,TW hist"
    hist_sys={}    
    hist_sys_all_region={}    
    hist_sys_other={}    
    hist_sys_other_all_region={}    
    for hname in hist_sys_mc_all:
        hist_nominal  =hist_sys_mc_all[hname]["nominal"].Clone("%s__nominal"%(hname))
        hist_sys[hname]=[]
        hist_sys_all_region[hname]=[]
        sys_up  =hist_sys_mc_all[hname]["nominal"].Clone("%s__sys_up"%(hname))
        sys_down=hist_sys_mc_all[hname]["nominal"].Clone("%s__sys_down"%(hname))
        sys_up.Scale(0)
        sys_down.Scale(0)
        hist_sys_other[hname]=[]
        hist_sys_other_all_region[hname]=[]
        sys_other_up  =hist_sys_mc_all[hname]["nominal"].Clone("%s__sys_other_up"%(hname))
        sys_other_down=hist_sys_mc_all[hname]["nominal"].Clone("%s__sys_other_down"%(hname))
        sys_other_up.Scale(0)
        sys_other_down.Scale(0)
        N_sys_up=0
        N_sys_down=0
        N_sys_other_up=0
        N_sys_other_down=0
        for nsys in hist_sys_mc_all[hname]:
            if "nominal" in nsys:continue
            N_sys     =hist_sys_mc_all[hname][nsys].GetSumOfWeights()-hist_sys_mc_all[hname]["nominal"].GetSumOfWeights()
            if N_sys>0:
                N_sys_up=math.sqrt(math.pow(N_sys_up,2)+math.pow(N_sys,2))
                if "bgk" in nsys and "bgk_DYJets" not in nsys and "bgk_WJet" not in nsys:
                    N_sys_other_up=math.sqrt(math.pow(N_sys_other_up,2)+math.pow(N_sys,2))
            else:
                N_sys_down=math.sqrt(math.pow(N_sys_down,2)+math.pow(N_sys,2))
                if "bgk" in nsys and "bgk_DYJets" not in nsys and "bgk_WJet" not in nsys:
                    N_sys_other_down=math.sqrt(math.pow(N_sys_other_down,2)+math.pow(N_sys,2))
                
            for ibin in range(1, hist_nominal.GetNbinsX()+1):
                tmp_value=float(hist_sys_mc_all[hname][nsys].GetBinContent(ibin)-hist_nominal.GetBinContent(ibin))
                if tmp_value>0:sys_up  .SetBinContent(ibin,math.sqrt(math.pow(sys_up  .GetBinContent(ibin),2)+math.pow(tmp_value,2)))
                else          :sys_down.SetBinContent(ibin,math.sqrt(math.pow(sys_down.GetBinContent(ibin),2)+math.pow(tmp_value,2)))
                if "bgk" in nsys and "bgk_DYJets" not in nsys and "bgk_WJet" not in nsys:
                    if tmp_value>0:sys_other_up  .SetBinContent(ibin,math.sqrt(math.pow(sys_other_up  .GetBinContent(ibin),2)+math.pow(tmp_value,2)))
                    else          :sys_other_down.SetBinContent(ibin,math.sqrt(math.pow(sys_other_down.GetBinContent(ibin),2)+math.pow(tmp_value,2)))
        hist_sys[hname].append(sys_up)    
        hist_sys[hname].append(sys_down)
        hist_sys_other[hname].append(sys_other_up)    
        hist_sys_other[hname].append(sys_other_down)
        hist_sys_all_region[hname].append(N_sys_up)    
        hist_sys_all_region[hname].append(N_sys_down)
        hist_sys_other_all_region[hname].append(N_sys_other_up)    
        hist_sys_other_all_region[hname].append(N_sys_other_down)
    print "saved total systematic for all and other !"
    if draw_all_system_plot:
        print "draw all systematic sample hist !"
        Draw_all_system_ratio_v1(dir, date, hist_sys_mc_TT , Files, dir_hist, dir_system_name, system_list, ["Sample_TT","isr","fsr"],"TT_Samples")
        Draw_all_system_ratio_v1(dir, date, hist_sys_mc_TW , Files, dir_hist, dir_system_name, system_list, ["Sample_ST_tW","isr","fsr"],"TW_Samples")
        Draw_all_system_ratio_v1(dir, date, hist_sys_mc_all, Files, dir_hist, dir_system_name, system_list, ["PU","JetEn","SmearedJetRes","BtagSF","UnclusteredEn"],"Shape_uncert")
        print "draw all systematic sample hist done !"
    if Save_uncert_table:
        print "making uncert table.."
        for hists in [hist_sys_mc_TT,hist_sys_mc_TW,hist_sys_mc_all]:
            dict_table={}
            hist_sys_mc=hists
            dict_table["chan"]=Channel
            dict_table["process"]="all"
            if hists==hist_sys_mc_TT:dict_table["process"]="TT\_Modeling"
            elif hists==hist_sys_mc_TW:dict_table["process"]="TW\_Modeling"
            for nsys in system_list:
                if nsys in dict_system_table_name:dict_table[nsys]=dict_system_table_name[nsys]
                else                             :dict_table[nsys]=nsys
                if nsys=="nominal":
                    dict_table[nsys+"_all" ]=("%.3f")%(hist_sys_mc["H_lepton_led_phi"  ][nsys].GetSumOfWeights())#bin 1 is 0j0b
                    dict_table[nsys+"_1j0t"]=("%.3f")%(hist_sys_mc["H_Limit_N_jet_bjet"][nsys].GetBinContent(2) )#bin 1 is 0j0b
                    dict_table[nsys+"_1j1t"]=("%.3f")%(hist_sys_mc["H_Limit_N_jet_bjet"][nsys].GetBinContent(3) )#bin 1 is 0j0b
                    dict_table[nsys+"_2j1t"]=("%.3f")%(hist_sys_mc["H_Limit_N_jet_bjet"][nsys].GetBinContent(4) )#bin 1 is 0j0b
                    dict_table[nsys+"_2j2t"]=("%.3f")%(hist_sys_mc["H_Limit_N_jet_bjet"][nsys].GetBinContent(5) )#bin 1 is 0j0b
                else:
                    
                    dict_table[nsys+"_all" ]=("%.3f")%(100*(hist_sys_mc["H_lepton_led_phi"  ][nsys].GetSumOfWeights()-hist_sys_mc["H_lepton_led_phi"  ]["nominal"].GetSumOfWeights())/hist_sys_mc["H_lepton_led_phi"  ]["nominal"].GetSumOfWeights())+str("\%") 
                    dict_table[nsys+"_1j0t"]=("%.3f")%(100*(hist_sys_mc["H_Limit_N_jet_bjet"][nsys].GetBinContent(2) -hist_sys_mc["H_Limit_N_jet_bjet"]["nominal"].GetBinContent(2) )/hist_sys_mc["H_Limit_N_jet_bjet"]["nominal"].GetBinContent(2) )+str("\%") 
                    dict_table[nsys+"_1j1t"]=("%.3f")%(100*(hist_sys_mc["H_Limit_N_jet_bjet"][nsys].GetBinContent(3) -hist_sys_mc["H_Limit_N_jet_bjet"]["nominal"].GetBinContent(3) )/hist_sys_mc["H_Limit_N_jet_bjet"]["nominal"].GetBinContent(3) )+str("\%") 
                    dict_table[nsys+"_2j1t"]=("%.3f")%(100*(hist_sys_mc["H_Limit_N_jet_bjet"][nsys].GetBinContent(4) -hist_sys_mc["H_Limit_N_jet_bjet"]["nominal"].GetBinContent(4) )/hist_sys_mc["H_Limit_N_jet_bjet"]["nominal"].GetBinContent(4) )+str("\%") 
                    dict_table[nsys+"_2j2t"]=("%.3f")%(100*(hist_sys_mc["H_Limit_N_jet_bjet"][nsys].GetBinContent(5) -hist_sys_mc["H_Limit_N_jet_bjet"]["nominal"].GetBinContent(5) )/hist_sys_mc["H_Limit_N_jet_bjet"]["nominal"].GetBinContent(5) )+str("\%") 
            dict_table["other_scale_up" ]="other\_up"
            dict_table["other_scale_up_all" ]=("%.3f")%(100*(hist_sys_other_all_region["H_lepton_led_phi"][0])/hist_sys_mc["H_lepton_led_phi"  ]["nominal"].GetSumOfWeights())+str("\%")
            dict_table["other_scale_up_1j0t"]=("%.3f")%(100*(hist_sys_other["H_Limit_N_jet_bjet"][0].GetBinContent(2))/hist_sys_mc["H_Limit_N_jet_bjet"]["nominal"].GetBinContent(2) )+str("\%")
            dict_table["other_scale_up_1j1t"]=("%.3f")%(100*(hist_sys_other["H_Limit_N_jet_bjet"][0].GetBinContent(3))/hist_sys_mc["H_Limit_N_jet_bjet"]["nominal"].GetBinContent(3) )+str("\%")
            dict_table["other_scale_up_2j1t"]=("%.3f")%(100*(hist_sys_other["H_Limit_N_jet_bjet"][0].GetBinContent(4))/hist_sys_mc["H_Limit_N_jet_bjet"]["nominal"].GetBinContent(4) )+str("\%")
            dict_table["other_scale_up_2j2t"]=("%.3f")%(100*(hist_sys_other["H_Limit_N_jet_bjet"][0].GetBinContent(5))/hist_sys_mc["H_Limit_N_jet_bjet"]["nominal"].GetBinContent(5) )+str("\%")
            dict_table["other_scale_down" ]="other\_down"
            dict_table["other_scale_down_all" ]=("-%.3f")%(100*(hist_sys_other_all_region["H_lepton_led_phi"][1])/hist_sys_mc["H_lepton_led_phi"  ]["nominal"].GetSumOfWeights())+str("\%")
            dict_table["other_scale_down_1j0t"]=("-%.3f")%(100*(hist_sys_other["H_Limit_N_jet_bjet"][1].GetBinContent(2))/hist_sys_mc["H_Limit_N_jet_bjet"]["nominal"].GetBinContent(2) )+str("\%")
            dict_table["other_scale_down_1j1t"]=("-%.3f")%(100*(hist_sys_other["H_Limit_N_jet_bjet"][1].GetBinContent(3))/hist_sys_mc["H_Limit_N_jet_bjet"]["nominal"].GetBinContent(3) )+str("\%")
            dict_table["other_scale_down_2j1t"]=("-%.3f")%(100*(hist_sys_other["H_Limit_N_jet_bjet"][1].GetBinContent(4))/hist_sys_mc["H_Limit_N_jet_bjet"]["nominal"].GetBinContent(4) )+str("\%")
            dict_table["other_scale_down_2j2t"]=("-%.3f")%(100*(hist_sys_other["H_Limit_N_jet_bjet"][1].GetBinContent(5))/hist_sys_mc["H_Limit_N_jet_bjet"]["nominal"].GetBinContent(5) )+str("\%")
            dict_table["total_scale_up" ]="total\_up"
            dict_table["total_scale_up_all" ]=("%.3f")%(100*(hist_sys_all_region["H_lepton_led_phi"][0])/hist_sys_mc["H_lepton_led_phi"  ]["nominal"].GetSumOfWeights())+str("\%")
            dict_table["total_scale_up_1j0t"]=("%.3f")%(100*(hist_sys["H_Limit_N_jet_bjet"][0].GetBinContent(2))/hist_sys_mc["H_Limit_N_jet_bjet"]["nominal"].GetBinContent(2) )+str("\%")
            dict_table["total_scale_up_1j1t"]=("%.3f")%(100*(hist_sys["H_Limit_N_jet_bjet"][0].GetBinContent(3))/hist_sys_mc["H_Limit_N_jet_bjet"]["nominal"].GetBinContent(3) )+str("\%")
            dict_table["total_scale_up_2j1t"]=("%.3f")%(100*(hist_sys["H_Limit_N_jet_bjet"][0].GetBinContent(4))/hist_sys_mc["H_Limit_N_jet_bjet"]["nominal"].GetBinContent(4) )+str("\%")
            dict_table["total_scale_up_2j2t"]=("%.3f")%(100*(hist_sys["H_Limit_N_jet_bjet"][0].GetBinContent(5))/hist_sys_mc["H_Limit_N_jet_bjet"]["nominal"].GetBinContent(5) )+str("\%")
            dict_table["total_scale_down" ]="total\_down"
            dict_table["total_scale_down_all" ]=("-%.3f")%(100*(hist_sys_all_region["H_lepton_led_phi"][1])/hist_sys_mc["H_lepton_led_phi"  ]["nominal"].GetSumOfWeights())+str("\%")
            dict_table["total_scale_down_1j0t"]=("-%.3f")%(100*(hist_sys["H_Limit_N_jet_bjet"][1].GetBinContent(2))/hist_sys_mc["H_Limit_N_jet_bjet"]["nominal"].GetBinContent(2) )+str("\%")
            dict_table["total_scale_down_1j1t"]=("-%.3f")%(100*(hist_sys["H_Limit_N_jet_bjet"][1].GetBinContent(3))/hist_sys_mc["H_Limit_N_jet_bjet"]["nominal"].GetBinContent(3) )+str("\%")
            dict_table["total_scale_down_2j1t"]=("-%.3f")%(100*(hist_sys["H_Limit_N_jet_bjet"][1].GetBinContent(4))/hist_sys_mc["H_Limit_N_jet_bjet"]["nominal"].GetBinContent(4) )+str("\%")
            dict_table["total_scale_down_2j2t"]=("-%.3f")%(100*(hist_sys["H_Limit_N_jet_bjet"][1].GetBinContent(5))/hist_sys_mc["H_Limit_N_jet_bjet"]["nominal"].GetBinContent(5) )+str("\%")

            if remove_herwig:
                dict_table["Sample_TT_TuneEE5C" ]="TT\_herwigpp"
                dict_table["Sample_TT_TuneEE5C_all" ]=0
                dict_table["Sample_TT_TuneEE5C_1j0t"]=0
                dict_table["Sample_TT_TuneEE5C_1j1t"]=0
                dict_table["Sample_TT_TuneEE5C_2j1t"]=0
                dict_table["Sample_TT_TuneEE5C_2j2t"]=0
                dict_table["Sample_ST_tW_herwigpp" ] ="TW\_herwigpp"
                dict_table["Sample_ST_tW_herwigpp_all" ]=0
                dict_table["Sample_ST_tW_herwigpp_1j0t"]=0
                dict_table["Sample_ST_tW_herwigpp_1j1t"]=0
                dict_table["Sample_ST_tW_herwigpp_2j1t"]=0
                dict_table["Sample_ST_tW_herwigpp_2j2t"]=0
            save_uncertainty_table("%s_%s_uncert_table"%(Channel,dict_table["process"].split("\\")[0]), dict_table, Channel)

    ratio_style=2# 1:(data-mc)/mc,other data/mc
    #log_hist_name=["H_jet_forward_led_pt","H_Mll","H_Mll_Zpeak"]
    log_hist_name=["H_jet_forward_led_pt"]
    print_hist_name=["H_njet_bjet"]
    
    Save_hist=["H_pv_n"]
    
#    sample_list=["WJet_mad","WG_LNuG","ZZ_4L","ZZ_2L2Nu","WZ_2L2Q","WZ_3LNu","WWTo2L2Nu","TTGJets","TTZToQQ","TTZToLLNuNu","TTWJetsToLNu","TTWJetsToQQ","DYJetsToLL_M50_amc","DYJetsToLL_M10to50_amc_wx","TTTo2L2Nu","TW_antitop","TW_top"]
    sample_list=["WJet_mad","GGHWWTo2L2Nu","VBFHWWTo2L2Nu","WG_LNuG","ZZ_4L","ZZ_2L2Nu","WZ_2L2Q","WZ_3LNu","WWTo2L2Nu","TTGJets","TTZToQQ","TTZToLLNuNu","TTWJetsToLNu","TTWJetsToQQ","DYJetsToLL_M50_amc","DYJetsToLL_M10to50_amc","TTTo2L2Nu","TW_antitop","TW_top"]
    if Do_FCNC_Study:
        sample_list=["WJet_mad","GGHWWTo2L2Nu","VBFHWWTo2L2Nu","WG_LNuG","ZZ_4L","ZZ_2L2Nu","WZ_2L2Q","WZ_3LNu","WWTo2L2Nu","TTGJets","TTZToQQ","TTZToLLNuNu","TTWJetsToLNu","TTWJetsToQQ","DYJetsToLL_M50_amc","DYJetsToLL_M10to50_amc","TTTo2L2Nu","TW_antitop","TW_top","FCNC_ST_tug","FCNC_ST_tcg"]
    ############ MAIN ploting ######################
    if do_plot_main:
        print "begin plot"
        f_out=ROOT.TFile("Saved.root","RECREATE")
        F_out=ROOT.TFile("%s_Limit_plot.root"%(Channel),"RECREATE")
        MVA_hist={}
        for hist in dir_hist:
            if all_system_hist[hist]["nominal"]["data"]:
                hist_out_list={}
                h_data=all_system_hist[hist]["nominal"]["data"].Clone("nominal_data_%s"%(hist))
                h_data.SetStats(0)
                h_mc =h_data.Clone("h_sum_mc_%s"%(hist))
                h_mc.Scale(0)
                h_ttbar =h_data.Clone("h_ttbar_%s"%(hist))
                h_ttbar.Scale(0)
                h_tW    =h_data.Clone("h_tW_%s"%(hist))
                h_tW.Scale(0)
                h_FCNC_tug =h_data.Clone("h_FCNC_tug_%s"%(hist))
                h_FCNC_tug.Scale(0)
                h_FCNC_tcg =h_data.Clone("h_FCNC_tcg_%s"%(hist))
                h_FCNC_tcg.Scale(0)
                if Do_FCNC_Study:
                    h_FCNC_tug =all_system_hist[hist]["nominal"]["FCNC_ST_tug"].Clone("h_FCNC_tug_%s"%(hist))
                    h_FCNC_tcg =all_system_hist[hist]["nominal"]["FCNC_ST_tcg"].Clone("h_FCNC_tcg_%s"%(hist))
                stack=ROOT.THStack()
                if hist == "H_MET_T1Txy_phi":
                    print "%s data events=%f:"%(hist,h_data.GetSumOfWeights())
                for sname in sample_list:
                    if sname not in all_system_hist[hist]["nominal"]: continue
                    if "FCNC" in sname: continue
                    h_tmp=all_system_hist[hist]["nominal"][sname]
                    if hist == "H_MET_T1Txy_phi":
                        err_tmp=ROOT.Double(0)
                        N_MC   =h_tmp.IntegralAndError(1,h_tmp.GetNbinsX(),err_tmp)
                        #print "%s %s events=%f+-%f"%(hist,sname,h_tmp.GetSumOfWeights(),)
                        print "%s %s events=%f+-%f"%(hist,sname,N_MC,err_tmp)
                    if hist == "H_Limit_N_jet_bjet" and sname =="WJet_mad":
                        print "WJet|",
                        for ibin in range(1,h_tmp.GetNbinsX()+1):
                            print "bin %s:%f +- %f|"%(str(ibin),h_tmp.GetBinContent(ibin),h_tmp.GetBinError(ibin)),
                    h_tmp.SetStats(0)
                    h_tmp.SetLineColor(MC_Sample[sname].color)
                    h_tmp.SetFillColor(MC_Sample[sname].color)
                    h_mc.Add(h_tmp)
                    stack.Add(h_tmp)
                    hist_out_list[sname]=h_tmp
                    if sname == "TTTo2L2Nu":
                        h_ttbar.Add(h_tmp)
                    elif sname in ["TW_antitop","TW_top"]:
                        h_tW.Add(h_tmp)
                gr_stat_sys = get_total_err(h_mc, hist_sys[hist][1], hist_sys[hist][0])
                draw_plots(Channel, date, dir, stack, h_mc, h_data, gr_stat_sys, hist, dir_hist[hist], ratio_style,log_hist_name, h_FCNC_tug, h_FCNC_tcg)
                hist_out_list["sys_stat_err"]=gr_stat_sys
                hist_out_list["data"]        =h_data
                if hist in dir_MVA:
                    MVA_hist[hist]=[stack,h_mc,h_data,gr_stat_sys]

                if do_print_sys_region:
                    if hist == "H_Limit_N_jet_bjet":
                        print "channel %s :"%(Channel)
                        for ibin in range(1,h_data.GetNbinsX()+1):
                            N_data  =h_data.GetBinContent(ibin)
                            err_data=h_data.GetBinError(ibin)
                            N_mc    =h_mc  .GetBinContent(ibin)
                            err_mc_stat_sys= float(gr_stat_sys.GetErrorYhigh(ibin-1)) if (float(gr_stat_sys.GetErrorYhigh(ibin-1))>float(gr_stat_sys.GetErrorYlow(ibin-1))) else float(gr_stat_sys.GetErrorYlow(ibin-1))                        
                            ratio=float(N_data)/float(N_mc) if N_mc!=0 else 0
                            err_ratio=float(ratio*math.sqrt(math.pow(err_data/N_data,2)+math.pow(err_mc_stat_sys/N_mc,2)))
                            N_ttbar  =h_ttbar.GetBinContent(ibin)
                            err_ttbar=h_ttbar.GetBinError(ibin)
                            N_tW     =h_tW.GetBinContent(ibin)
                            err_tW   =h_tW.GetBinError(ibin)
                            print "%d bin & %s:%d$\pm$%d(stat.) & %s:%.1f$\pm$%.1f(stat.) & %s:%.1f$\pm$%.1f(stat.) & %s:%.1f$\pm$%.1f(stat.+syst.) & %s:%.3f$\pm$%.3f(stat.+syst.) "%(ibin,"data",N_data,err_data,"tW",N_tW,err_tW,"ttbar",N_ttbar,err_ttbar,"mc",N_mc,err_mc_stat_sys,"data/mc",ratio,err_ratio)
                    ##### save limit plot with system uncertainty####
                        F_out.cd()
                        for iout in hist_out_list:
                            hist_out_list[iout].Write(iout)
                        F_out.Close()
                        print "%s is saved"%(F_out.GetName())
                    ##########################################
                if hist in Save_hist:
                    f_out.cd()
                    h_data.Scale(1/h_data.GetSumOfWeights())
                    h_mc  .Scale(1/h_mc  .GetSumOfWeights())
                    h_data.Divide(h_mc)
                    h_data.SetName(hist)
                    h_data.Write()
#        print MVA_hist
        if do_draw_combine_MVA:
            print "begin draw combine MVA.."
            draw_combine_MVA(Channel, date, dir, MVA_hist)
            print "draw combine MVA done!"
        f_out.Close()   
        print "Plotting Done!!"
    ######### save hist of limit ##############
    if do_save_sys_hist:
        no_signal=False
        Ctg_LO=False
        system_uncert_list=system_list
        ############# remove incorret stat error######
        #stat_list=["TW_stat_Up","TW_stat_Down","TT_stat_Up","TT_stat_Down"]
        #other_stat_list=["DY_stat_Up","DY_stat_Down","other_stat_Up","other_stat_Down"]
        #stat_system_hist={}
        #system_uncert_list.extend(stat_list)
        #system_uncert_list.extend(other_stat_list)
        #    
        #for region in dir_MVA:
        #   stat_system_hist[region]={}
        #   tmp_tt         =all_system_hist[region]["nominal"]["TTTo2L2Nu"].Clone("%s_ttbar"%(str(region)))
        #   tmp_tw_top     =all_system_hist[region]["nominal"]["TW_top"].Clone("%s_tw_top"%(str(region)))
        #   tmp_tw_antitop =all_system_hist[region]["nominal"]["TW_antitop"].Clone("%s_tw_antitop"%(str(region)))
        #   tmp_tt_stat_up           =tmp_tt.Clone(tmp_tt.GetName()+"_Up")
        #   tmp_tt_stat_down         =tmp_tt.Clone(tmp_tt.GetName()+"_Down")
        #   tmp_tw_top_stat_up       =tmp_tw_top.Clone(tmp_tw_top.GetName()+"_Up")
        #   tmp_tw_top_stat_down     =tmp_tw_top.Clone(tmp_tw_top.GetName()+"_Down")
        #   tmp_tw_antitop_stat_up   =tmp_tw_antitop.Clone(tmp_tw_antitop.GetName()+"_Up")
        #   tmp_tw_antitop_stat_down =tmp_tw_antitop.Clone(tmp_tw_antitop.GetName()+"_Down")
        #   stat_up_down(tmp_tt_stat_up, True)
        #   stat_up_down(tmp_tt_stat_down, False)
        #   stat_up_down(tmp_tw_top_stat_up, True)
        #   stat_up_down(tmp_tw_top_stat_down, False)
        #   stat_up_down(tmp_tw_antitop_stat_up, True)
        #   stat_up_down(tmp_tw_antitop_stat_down, False)
        #   stat_system_hist[region]["TT_stat_Up"]  ={} 
        #   stat_system_hist[region]["TT_stat_Down"]={} 
        #   stat_system_hist[region]["TW_stat_Up"]  ={} 
        #   stat_system_hist[region]["TW_stat_Up"]  ={} 
        #   stat_system_hist[region]["TW_stat_Down"]={} 
        #   stat_system_hist[region]["TW_stat_Down"]={} 
        #   stat_system_hist[region]["TT_stat_Up"]  ["TTTo2L2Nu"]  =tmp_tt_stat_up
        #   stat_system_hist[region]["TT_stat_Up"]  ["TW_top"]     =tmp_tw_top
        #   stat_system_hist[region]["TT_stat_Up"]  ["TW_antitop"] =tmp_tw_antitop
        #   stat_system_hist[region]["TT_stat_Down"]["TTTo2L2Nu"]  =tmp_tt_stat_down
        #   stat_system_hist[region]["TT_stat_Down"]["TW_top"]     =tmp_tw_top
        #   stat_system_hist[region]["TT_stat_Down"]["TW_antitop"] =tmp_tw_antitop
        #   stat_system_hist[region]["TW_stat_Up"]  ["TTTo2L2Nu"]  =tmp_tt
        #   stat_system_hist[region]["TW_stat_Up"]  ["TW_top"]     =tmp_tw_top_stat_up
        #   stat_system_hist[region]["TW_stat_Up"]  ["TW_antitop"] =tmp_tw_antitop_stat_up
        #   stat_system_hist[region]["TW_stat_Down"]["TTTo2L2Nu"]  =tmp_tt
        #   stat_system_hist[region]["TW_stat_Down"]["TW_top"]     =tmp_tw_top_stat_down
        #   stat_system_hist[region]["TW_stat_Down"]["TW_antitop"] =tmp_tw_antitop_stat_down
        #for sf in [1.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.02, 0.5, 1.5, 2, 2.5, 3, 4, 5]:
        for sf in [1.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.02, 0.5]:
            Frist=True 
            for do_opposite in [True,False]:
                for choose_C in ["Ctg","Ctw","Cphiq"]:
                    if Frist==False and Do_FCNC_Study:continue
                    Frist=False 
                    dir_sf={str(1.00):"1.00", str(0.05):"0.05", str(0.10):"0.10", str(0.15):"0.15", str(0.20):"0.20", str(0.25):"0.25", str(0.30):"0.30", str(0.02):"0.02",str(0.5):"0.50", str(1.5):"1.50", str(2):"2.00", str(2.5):"2.50", str(3):"3.00", str(4):"4.00", str(5):"5.00"}
                    str_sf=dir_sf[str(sf)]
                    for_Ctg  =False
                    for_Cphiq=False
                    for_Ctw  =False
                    if choose_C == "Ctg":for_Ctg=True
                    elif choose_C == "Ctw":for_Ctw=True
                    elif choose_C == "Cphiq":for_Cphiq=True
                    else: print "wrong"
                    if no_signal:
                        for_Ctg  =False
                        for_Cphiq=False
                        for_Ctw  =False
                    tw_NLO_xs          =float((71.7-55.24)*(1-0.676*0.676)/2)#  NLO - LO
                    ttbar_NLO_xs       =float(730.7*0.324*0.324)#NLO
                    signal_tw_Cphiq_xs =float((55.24+6.7*sf+0.21*sf*sf)*(1-0.676*0.676)/2)
                    signal_tw_Ctw_xs   =float((55.24-4.45*sf+1*sf*sf)*(1-0.676*0.676)/2)
                    signal_tw_Ctg_xs   =float((55.24+6.55*sf+4.99*sf*sf)*(1-0.676*0.676)/2)
                    signal_ttbar_Ctg_xs=float(76.63+405.66*0.324*0.324*sf + 94.176*0.324*0.324*sf*sf )
                    if Ctg_LO:
                        signal_ttbar_Ctg_xs=float(76.63+274.1*0.324*0.324*sf + 65.4*0.324*0.324*sf*sf )
                    if do_opposite:
                        signal_tw_Cphiq_xs =float((55.24-6.7*sf+0.21*sf*sf)  *(1-0.676*0.676)/2)
                        signal_tw_Ctw_xs   =float((55.24+4.45*sf+1*sf*sf)    *(1-0.676*0.676)/2)
                        signal_tw_Ctg_xs   =float((55.24-6.55*sf+4.99*sf*sf) *(1-0.676*0.676)/2)
                        signal_ttbar_Ctg_xs=float(76.63-405.66*0.324*0.324*sf + 94.176*0.324*0.324*sf*sf )
                        if Ctg_LO:
                            signal_ttbar_Ctg_xs=float(76.63-274.1*0.324*0.324*sf + 65.4*0.324*0.324*sf*sf )
                    signalonly_tw_Cphiq_xs  =float((0.21*sf*sf)*(1-0.676*0.676)/2)
                    signalonly_tw_Ctw_xs   =float((1*sf*sf)*(1-0.676*0.676)/2)
                    signalonly_tw_Ctg_xs   =float(4.99*sf*sf*(1-0.676*0.676)/2)
                    signalonly_ttbar_Ctg_xs=float(94.176*0.324*0.324*sf*sf )
                    if Ctg_LO:
                        signalonly_ttbar_Ctg_xs=float(65.4*0.324*0.324*sf*sf )
                    for region in dir_MVA:
                        str_extra=""
                        #if "H_1jet_1bjet" in dir_MVA:
                        #    str_extra="_"+region.split("H_")[-1] 
                        #elif "H_MLP_1jet_1bjet" in dir_MVA: 
                        #    str_extra="_"+region.split("H_MLP_")[-1] 
                        #elif "H_BDT_1jet_1bjet" in dir_MVA:
                        #    str_extra="_"+region.split("H_BDT_")[-1] 
                        #elif "H_MLP_tug_1jet_1bjet" in dir_MVA:
                        #    str_extra="_"+region.split("H_MLP_tug_")[-1] 
                        #elif "H_BDT_tug_1jet_1bjet" in dir_MVA:
                        #    str_extra="_"+region.split("H_BDT_tug_")[-1] 
                        #elif "H_MLP_tcg_1jet_1bjet" in dir_MVA:
                        #    str_extra="_"+region.split("H_MLP_tcg_")[-1] 
                        #elif "H_BDT_tcg_1jet_1bjet" in dir_MVA:
                        #    str_extra="_"+region.split("H_BDT_tcg_")[-1] 
                        if   "0jet_0bjet" in region or "0j0b" in region :str_extra="_0jet_0bjet"
                        elif "1jet_0bjet" in region or "1j0b" in region :str_extra="_1jet_0bjet"
                        elif "1jet_1bjet" in region or "1j1b" in region :str_extra="_1jet_1bjet"
                        elif "2jet_1bjet" in region or "2j1b" in region :str_extra="_2jet_1bjet"
                        elif "2jet_2bjet" in region or "2j2b" in region :str_extra="_2jet_2bjet"
                        str_chan_region=Channel+str_extra+"_"##for stat bin by bin name
                        if Do_FCNC_Study:
                            str_extra=str_extra+"_FCNC"+"_"+str_sf
                            for_Ctg  =False
                            for_Cphiq=False
                            for_Ctw  =False
                        else:
                            str_extra=str_extra+"_"+choose_C
                            str_extra=str_extra+"_"+str_sf
                            if no_signal:str_extra=str_extra+"_noSignal"
                            if do_opposite:str_extra=str_extra+"_opposite"
                        dir_out="./Limit_out/"
                        f_out=ROOT.TFile(dir_out+Channel+str_extra+".root","RECREATE")
                      #  for nsys in all_system_hist[region]:
                        for nsys in system_uncert_list:
                            if "bgk" in nsys or "lumi" in nsys :continue
                            h_data_out            =ROOT.TH1D()
                            h_tw_out              =ROOT.TH1D()
                            h_tw_NLO_out          =ROOT.TH1D()
                            h_ttbar_out           =ROOT.TH1D()
                            h_ttbar_NNLO_out      =ROOT.TH1D()
                            h_DY_out              =ROOT.TH1D()
                            h_other_out           =ROOT.TH1D()
                            h_jets_out            =ROOT.TH1D()
                            h_tw_signal_out       =ROOT.TH1D()
                            h_tw_signalonly_out   =ROOT.TH1D()
                            h_ttbar_signal_out    =ROOT.TH1D()
                            h_ttbar_signalonly_out=ROOT.TH1D()
                            #all_system_hist[region][nsys]["data"].Sumw2(ROOT.kTRUE)
                            h_data             =all_system_hist[region]["nominal"]["data"].Clone("Data_"+nsys)
                            h_tw               =all_system_hist[region]["nominal"]["data"].Clone("TW_"+nsys)
                            h_tw_NLO           =all_system_hist[region]["nominal"]["data"].Clone("TWNLO_"+nsys)
                            h_ttbar            =all_system_hist[region]["nominal"]["data"].Clone("TT_"+nsys)
                            h_ttbar_NNLO       =all_system_hist[region]["nominal"]["data"].Clone("TT_NNLO"+nsys)
                            h_DY               =all_system_hist[region]["nominal"]["data"].Clone("DY_"+nsys)
                            h_other            =all_system_hist[region]["nominal"]["data"].Clone("other_"+nsys)
                            h_jets             =all_system_hist[region]["nominal"]["data"].Clone("jets_"+nsys)
                            h_tw_signal        =all_system_hist[region]["nominal"]["data"].Clone("tw_signal_"+nsys)
                            h_tw_signalonly    =all_system_hist[region]["nominal"]["data"].Clone("tw_signalonly_"+nsys)
                            h_ttbar_signal     =all_system_hist[region]["nominal"]["data"].Clone("ttbar_signal_"+nsys)
                            h_ttbar_signalonly =all_system_hist[region]["nominal"]["data"].Clone("ttbar_signalonly_"+nsys)
                            h_data            .Scale(0)
                            h_tw              .Scale(0)
                            h_tw_NLO          .Scale(0)
                            h_ttbar           .Scale(0)
                            h_ttbar_NNLO      .Scale(0)
                            h_DY              .Scale(0)
                            h_other           .Scale(0)
                            h_jets            .Scale(0)
                            h_tw_signal       .Scale(0)
                            h_tw_signalonly   .Scale(0)
                            h_ttbar_signal    .Scale(0)
                            h_ttbar_signalonly.Scale(0)
                            #if nsys not in stat_list and nsys not in other_stat_list:
                            for sname in all_system_hist[region][nsys]:
                                if "data" in sname:h_data.Add(all_system_hist[region][nsys][sname],1)
                                elif "TW_" in sname :
                                    if for_Cphiq or for_Ctw or for_Ctg:
                                        h_tw.Add(all_system_hist[region][nsys][sname],float(55.24/71.74))
                                        h_tw_NLO.Add(all_system_hist[region][nsys][sname],float(tw_NLO_xs/MC_Sample["TW_top"].crosssection))
                                    else:
                                        h_tw.Add(all_system_hist[region][nsys][sname],1)
                                    if for_Cphiq:
                                        h_tw_signal.Add(all_system_hist[region][nsys][sname],float(signal_tw_Cphiq_xs/MC_Sample["TW_top"].crosssection))
                                        h_tw_signalonly.Add(all_system_hist[region][nsys][sname],float(signalonly_tw_Cphiq_xs/MC_Sample["TW_top"].crosssection))
                                    elif for_Ctw:
                                        h_tw_signal.Add(all_system_hist[region][nsys][sname],float(signal_tw_Ctw_xs/MC_Sample["TW_top"].crosssection))
                                        h_tw_signalonly.Add(all_system_hist[region][nsys][sname],float(signalonly_tw_Ctw_xs/MC_Sample["TW_top"].crosssection))
                                    elif for_Ctg:
                                        h_tw_signal.Add(all_system_hist[region][nsys][sname],float(signal_tw_Ctg_xs/MC_Sample["TW_top"].crosssection))
                                        h_tw_signalonly.Add(all_system_hist[region][nsys][sname],float(signalonly_tw_Ctg_xs/MC_Sample["TW_top"].crosssection))
                                elif "TTTo2L2Nu" in sname:
                                    if for_Ctg==False:h_ttbar.Add(all_system_hist[region][nsys][sname],1)
                                    if for_Cphiq:pass
                                    elif for_Ctw:pass
                                    elif for_Ctg:
                                        h_ttbar_NNLO.Add(all_system_hist[region][nsys][sname],float((MC_Sample["TTTo2L2Nu"].crosssection-ttbar_NLO_xs)/MC_Sample["TTTo2L2Nu"].crosssection))##for ttbar nnlo only
                                        h_ttbar     .Add(all_system_hist[region][nsys][sname],float(ttbar_NLO_xs/MC_Sample["TTTo2L2Nu"].crosssection))##for ttbar NLO
                                        h_ttbar_signal    .Add(all_system_hist[region][nsys][sname],float(signal_ttbar_Ctg_xs/MC_Sample["TTTo2L2Nu"].crosssection))
                                        h_ttbar_signalonly.Add(all_system_hist[region][nsys][sname],float(signalonly_ttbar_Ctg_xs/MC_Sample["TTTo2L2Nu"].crosssection))
                                elif "DY" in sname:h_DY.Add(all_system_hist[region][nsys][sname],1) 
                                elif "WJet_mad" in sname:h_jets .Add(all_system_hist[region][nsys][sname],1) 
                                elif "FCNC" not in sname:h_other.Add(all_system_hist[region][nsys][sname],1)
                            ########################### For TT,TW stat scale Up/Down ##############################
                            #elif nsys in stat_list:
                            #    for sname in all_system_hist[region]["nominal"]:
                            #        if "data" in sname:h_data.Add(all_system_hist[region]["nominal"][sname],1)
                            #        elif "TW_" in sname :
                            #            if for_Cphiq or for_Ctw or for_Ctg:
                            #                h_tw.Add(stat_system_hist[region][nsys][sname],float(55.24/71.74))
                            #                h_tw_NLO.Add(stat_system_hist[region][nsys][sname],float(tw_NLO_xs/MC_Sample["TW_top"].crosssection))
                            #            else:
                            #                h_tw.Add(stat_system_hist[region][nsys][sname],1)
                            #            if for_Cphiq:
                            #                h_tw_signal.Add(stat_system_hist[region][nsys][sname],float(signal_tw_Cphiq_xs/MC_Sample["TW_top"].crosssection))
                            #                h_tw_signalonly.Add(stat_system_hist[region][nsys][sname],float(signalonly_tw_Cphiq_xs/MC_Sample["TW_top"].crosssection))
                            #            elif for_Ctw:
                            #                h_tw_signal.Add(stat_system_hist[region][nsys][sname],float(signal_tw_Ctw_xs/MC_Sample["TW_top"].crosssection))
                            #                h_tw_signalonly.Add(stat_system_hist[region][nsys][sname],float(signalonly_tw_Ctw_xs/MC_Sample["TW_top"].crosssection))
                            #            elif for_Ctg:
                            #                h_tw_signal.Add(stat_system_hist[region][nsys][sname],float(signal_tw_Ctg_xs/MC_Sample["TW_top"].crosssection))
                            #                h_tw_signalonly.Add(stat_system_hist[region][nsys][sname],float(signalonly_tw_Ctg_xs/MC_Sample["TW_top"].crosssection))
                            #        elif "TTTo2L2Nu" in sname:
                            #         #   print stat_system_hist[region][nsys]
                            #            if for_Ctg==False:h_ttbar.Add(stat_system_hist[region][nsys][sname],1)
                            #            if for_Cphiq:pass
                            #            elif for_Ctw:pass
                            #            elif for_Ctg:
                            #                h_ttbar_NNLO.Add(stat_system_hist[region][nsys][sname],float((MC_Sample["TTTo2L2Nu"].crosssection-ttbar_NLO_xs)/MC_Sample["TTTo2L2Nu"].crosssection))##for ttbar nnlo only
                            #                h_ttbar     .Add(stat_system_hist[region][nsys][sname],float(ttbar_NLO_xs/MC_Sample["TTTo2L2Nu"].crosssection))##for ttbar NLO
                            #                h_ttbar_signal    .Add(stat_system_hist[region][nsys][sname],float(signal_ttbar_Ctg_xs/MC_Sample["TTTo2L2Nu"].crosssection))
                            #                h_ttbar_signalonly.Add(stat_system_hist[region][nsys][sname],float(signalonly_ttbar_Ctg_xs/MC_Sample["TTTo2L2Nu"].crosssection))
                            #        elif "DY" in sname:h_DY.Add(all_system_hist[region]["nominal"][sname],1) 
                            #        elif "WJet_mad" in sname:h_jets.Add(all_system_hist[region]["nominal"][sname],1) 
                            #        else:h_other.Add(all_system_hist[region]["nominal"][sname],1)
                            ########################### For DY,other stat scale Up/Down ##############################
                            #elif nsys in other_stat_list:
                            #    for sname in all_system_hist[region]["nominal"]:
                            #        if "data" in sname:h_data.Add(all_system_hist[region]["nominal"][sname],1)
                            #        elif "TW_" in sname :
                            #            if for_Cphiq or for_Ctw or for_Ctg:
                            #                h_tw.Add(all_system_hist[region]["nominal"][sname],float(55.24/71.74))
                            #                h_tw_NLO.Add(all_system_hist[region]["nominal"][sname],float(tw_NLO_xs/MC_Sample["TW_top"].crosssection))
                            #            else:
                            #                h_tw.Add(all_system_hist[region]["nominal"][sname],1)
                            #            if for_Cphiq:
                            #                h_tw_signal.Add(all_system_hist[region]["nominal"][sname],float(signal_tw_Cphiq_xs/MC_Sample["TW_top"].crosssection))
                            #                h_tw_signalonly.Add(all_system_hist[region]["nominal"][sname],float(signalonly_tw_Cphiq_xs/MC_Sample["TW_top"].crosssection))
                            #            elif for_Ctw:
                            #                h_tw_signal.Add(all_system_hist[region]["nominal"][sname],float(signal_tw_Ctw_xs/MC_Sample["TW_top"].crosssection))
                            #                h_tw_signalonly.Add(all_system_hist[region]["nominal"][sname],float(signalonly_tw_Ctw_xs/MC_Sample["TW_top"].crosssection))
                            #            elif for_Ctg:
                            #                h_tw_signal.Add(all_system_hist[region]["nominal"][sname],float(signal_tw_Ctg_xs/MC_Sample["TW_top"].crosssection))
                            #                h_tw_signalonly.Add(all_system_hist[region]["nominal"][sname],float(signalonly_tw_Ctg_xs/MC_Sample["TW_top"].crosssection))
                            #        elif "TTTo2L2Nu" in sname:
                            #            if for_Ctg==False:h_ttbar.Add(all_system_hist[region]["nominal"][sname],1)
                            #            if for_Cphiq:pass
                            #            elif for_Ctw:pass
                            #            elif for_Ctg:
                            #                h_ttbar_NNLO.Add(all_system_hist[region]["nominal"][sname],float((MC_Sample["TTTo2L2Nu"].crosssection-ttbar_NLO_xs)/MC_Sample["TTTo2L2Nu"].crosssection))##for ttbar nnlo only
                            #                h_ttbar     .Add(all_system_hist[region]["nominal"][sname],float(ttbar_NLO_xs/MC_Sample["TTTo2L2Nu"].crosssection))##for ttbar NLO
                            #                h_ttbar_signal    .Add(all_system_hist[region]["nominal"][sname],float(signal_ttbar_Ctg_xs/MC_Sample["TTTo2L2Nu"].crosssection))
                            #                h_ttbar_signalonly.Add(all_system_hist[region]["nominal"][sname],float(signalonly_ttbar_Ctg_xs/MC_Sample["TTTo2L2Nu"].crosssection))
                            #        elif "DY" in sname:h_DY.Add(all_system_hist[region]["nominal"][sname],1) 
                            #        elif "WJet_mad" in sname:h_jets.Add(all_system_hist[region]["nominal"][sname],1) 
                            #        else:h_other.Add(all_system_hist[region]["nominal"][sname],1)
                            #    if nsys=="DY_stat_Up":stat_up_down(h_DY,True)   
                            #    elif nsys=="DY_stat_Down":stat_up_down(h_DY,False)   
                            #    elif nsys=="other_stat_Up":stat_up_down(h_other,True)   
                            #    elif nsys=="other_stat_Down":stat_up_down(h_other,False)   
                            #    else:print "wrong stat"
                            #else:print "wrong nsys"         
                            #
                            ########################### Save histograms ##############################
                            sys_name="" 
                            if nsys!="nominal":
                                if nsys in dict_sys_limit_name: sys_name="_"+dict_sys_limit_name[nsys]
                            h_data_out            = h_data            .Clone("data_obs"    +sys_name)          
                            h_tw_signal_out       = h_tw_signal       .Clone("TWSignal"    +sys_name)
                            h_tw_signalonly_out   = h_tw_signalonly   .Clone("TWSignalonly"+sys_name)
                            h_ttbar_signal_out    = h_ttbar_signal    .Clone("TTSignal"    +sys_name)
                            h_ttbar_signalonly_out= h_ttbar_signalonly.Clone("TTSignalonly"+sys_name)
                            h_tw_out              = h_tw              .Clone("TW"          +sys_name)
                            h_tw_NLO_out          = h_tw_NLO          .Clone("TWNLO"       +sys_name)
                            h_ttbar_out           = h_ttbar           .Clone("TT"          +sys_name)
                            h_ttbar_NNLO_out      = h_ttbar_NNLO      .Clone("TTNNLO"      +sys_name)
                            h_DY_out              = h_DY              .Clone("DY"          +sys_name)
                            h_jets_out            = h_jets            .Clone("jets"        +sys_name)
                            h_other_out           = h_other           .Clone("other"       +sys_name)
                            #########change zero bin ########
                            change_zero_bin(h_tw_signal_out)
                            change_zero_bin(h_tw_signalonly_out)
                            change_zero_bin(h_ttbar_signal_out)
                            change_zero_bin(h_ttbar_signalonly_out)
                            change_zero_bin(h_tw_out)
                            change_zero_bin(h_tw_NLO_out)
                            change_zero_bin(h_ttbar_out)
                            change_zero_bin(h_ttbar_NNLO_out)
                            change_zero_bin(h_DY_out)
                            change_zero_bin(h_jets_out)
                            change_zero_bin(h_other_out)
                            ################################
                            str_fcnc="FCNCSignal"
                            f_out.cd()
                            if nsys=="nominal":
                                h_data_out    .Write()
                                if no_signal==False and Do_FCNC_Study==False:
                                    h_tw_signal_out       .Write()
                                    h_tw_signalonly_out   .Write()
                                    h_ttbar_signal_out    .Write()
                                    h_ttbar_signalonly_out.Write()
                                    h_tw_NLO_out          .Write()
                                    h_ttbar_NNLO_out      .Write()
                                    ####################For TT_CR and tw_DS: just using nominal as Down#########
                                    h_tw_signal_out       .Write(h_tw_signal_out       .GetName()+"_TT_CR_Down")
                                    h_tw_signalonly_out   .Write(h_tw_signalonly_out   .GetName()+"_TT_CR_Down")
                                    h_ttbar_signal_out    .Write(h_ttbar_signal_out    .GetName()+"_TT_CR_Down")
                                    h_ttbar_signalonly_out.Write(h_ttbar_signalonly_out.GetName()+"_TT_CR_Down")
                                    h_tw_NLO_out          .Write(h_tw_NLO_out          .GetName()+"_TT_CR_Down")
                                    h_ttbar_NNLO_out      .Write(h_ttbar_NNLO_out      .GetName()+"_TT_CR_Down")
                                    h_tw_signal_out       .Write(h_tw_signal_out       .GetName()+"_tw_DS_Down")
                                    h_tw_signalonly_out   .Write(h_tw_signalonly_out   .GetName()+"_tw_DS_Down")
                                    h_ttbar_signal_out    .Write(h_ttbar_signal_out    .GetName()+"_tw_DS_Down")
                                    h_ttbar_signalonly_out.Write(h_ttbar_signalonly_out.GetName()+"_tw_DS_Down")
                                    h_tw_NLO_out          .Write(h_tw_NLO_out          .GetName()+"_tw_DS_Down")
                                    h_ttbar_NNLO_out      .Write(h_ttbar_NNLO_out      .GetName()+"_tw_DS_Down")
                                elif Do_FCNC_Study:
                                    if "tug" in region:
                                        tmp_hist=all_system_hist[region][nsys]["FCNC_ST_tug"].Clone(str_fcnc)
                                        tmp_hist.Scale(float(sf))
                                        tmp_hist.Write()
                                        #all_system_hist[region][nsys]["FCNC_ST_tug"].Write(str_fcnc)
                                    elif "tcg" in region:
                                        tmp_hist=all_system_hist[region][nsys]["FCNC_ST_tcg"].Clone(str_fcnc)
                                        tmp_hist.Scale(float(sf))
                                        tmp_hist.Write()
                                        #all_system_hist[region][nsys]["FCNC_ST_tcg"].Scale(float(sf))
                                        #all_system_hist[region][nsys]["FCNC_ST_tcg"].Write(str_fcnc)
                                    else: print "Error: no tug or tcg !!!"
                                h_tw_out      .Write()
                                h_ttbar_out   .Write()
                                h_DY_out      .Write()
                                h_jets_out    .Write()
                                h_other_out   .Write()
                                ####For TT_CR and tw_DS: just using nominal as Down#########
                                h_tw_out      .Write(h_tw_out      .GetName()+"_TT_CR_Down")
                                h_ttbar_out   .Write(h_ttbar_out   .GetName()+"_TT_CR_Down")
                                h_DY_out      .Write(h_DY_out      .GetName()+"_TT_CR_Down")
                                h_jets_out    .Write(h_jets_out    .GetName()+"_TT_CR_Down")
                                h_other_out   .Write(h_other_out   .GetName()+"_TT_CR_Down")
                                h_tw_out      .Write(h_tw_out      .GetName()+"_tw_DS_Down")
                                h_ttbar_out   .Write(h_ttbar_out   .GetName()+"_tw_DS_Down")
                                h_DY_out      .Write(h_DY_out      .GetName()+"_tw_DS_Down")
                                h_jets_out    .Write(h_jets_out    .GetName()+"_tw_DS_Down")
                                h_other_out   .Write(h_other_out   .GetName()+"_tw_DS_Down")
                                ############## For stat. uncertainty per bin ###########
                                stat_hist_list=[]
                                stat_hist_list.extend(stat_uncertainty(h_tw_out   ,str_chan_region))
                                stat_hist_list.extend(stat_uncertainty(h_ttbar_out,str_chan_region))
                                stat_hist_list.extend(stat_uncertainty(h_DY_out   ,str_chan_region))
                                stat_hist_list.extend(stat_uncertainty(h_other_out,str_chan_region))
                                if Do_FCNC_Study:
                                    if "tug" in region:
                                        tmp_hist=all_system_hist[region][nsys]["FCNC_ST_tug"].Clone(str_fcnc)
                                        tmp_hist.Scale(float(sf))
                                        tmp_hist.Write()
                                        stat_hist_list.extend(stat_uncertainty(tmp_hist,str_chan_region))
                                    elif "tcg" in region:
                                        tmp_hist=all_system_hist[region][nsys]["FCNC_ST_tcg"].Clone(str_fcnc)
                                        tmp_hist.Scale(float(sf))
                                        tmp_hist.Write()
                                        stat_hist_list.extend(stat_uncertainty(tmp_hist,str_chan_region))
                                    else: print "Error: no tug or tcg !!!"
                                for ihist in stat_hist_list:
                                    ihist.Write()
                                ######################################################## 
                            elif nsys=="Sample_TT_CR" or nsys=="Sample_ST_tW_DS":
                                sys_name_Up=sys_name+"_Up"
                                #sys_name_Down=sys_name+"_Down"
                                if no_signal==False and Do_FCNC_Study==False :
                                    h_tw_signal_out       .Write(h_tw_signal_out       .GetName().split(sys_name)[0]+sys_name_Up)
                                    h_tw_signalonly_out   .Write(h_tw_signalonly_out   .GetName().split(sys_name)[0]+sys_name_Up)
                                    h_ttbar_signal_out    .Write(h_ttbar_signal_out    .GetName().split(sys_name)[0]+sys_name_Up)
                                    h_ttbar_signalonly_out.Write(h_ttbar_signalonly_out.GetName().split(sys_name)[0]+sys_name_Up)
                                    h_tw_NLO_out          .Write(h_tw_NLO_out          .GetName().split(sys_name)[0]+sys_name_Up)
                                    h_ttbar_NNLO_out      .Write(h_ttbar_NNLO_out      .GetName().split(sys_name)[0]+sys_name_Up)

                                    #h_tw_signal_out       .Write(h_tw_signal_out       .GetName().split(sys_name)[0]+sys_name_Down)
                                    #h_tw_signalonly_out   .Write(h_tw_signalonly_out   .GetName().split(sys_name)[0]+sys_name_Down)
                                    #h_ttbar_signal_out    .Write(h_ttbar_signal_out    .GetName().split(sys_name)[0]+sys_name_Down)
                                    #h_ttbar_signalonly_out.Write(h_ttbar_signalonly_out.GetName().split(sys_name)[0]+sys_name_Down)
                                    #h_tw_NLO_out          .Write(h_tw_NLO_out          .GetName().split(sys_name)[0]+sys_name_Down)
                                    #h_ttbar_NNLO_out      .Write(h_ttbar_NNLO_out      .GetName().split(sys_name)[0]+sys_name_Down)
                                elif Do_FCNC_Study:
                                    if "tug" in region:
                                        pass
                                    #    tmp_hist=all_system_hist[region][nsys]["FCNC_ST_tug"].Clone(str_fcnc+sys_name_Up)
                                    #    tmp_hist.Scale(float(sf))
                                    #    tmp_hist.Write(str_fcnc+sys_name_Up)
                                    #    tmp_hist.Write(str_fcnc+sys_name_Down)
                                    elif "tcg" in region:
                                        pass
                                    #    tmp_hist=all_system_hist[region][nsys]["FCNC_ST_tcg"].Clone(str_fcnc+sys_name_Up)
                                    #    tmp_hist.Scale(float(sf))
                                    #    tmp_hist.Write(str_fcnc+sys_name_Up)
                                    #    tmp_hist.Write(str_fcnc+sys_name_Down)
                                    else: print "Error: no tug or tcg !!!"
                                h_tw_out      .Write(h_tw_out    .GetName().split(sys_name)[0]+sys_name_Up)
                                h_ttbar_out   .Write(h_ttbar_out .GetName().split(sys_name)[0]+sys_name_Up)
                                h_DY_out      .Write(h_DY_out    .GetName().split(sys_name)[0]+sys_name_Up)
                                h_jets_out    .Write(h_jets_out  .GetName().split(sys_name)[0]+sys_name_Up)
                                h_other_out   .Write(h_other_out .GetName().split(sys_name)[0]+sys_name_Up)

                                #h_tw_out      .Write(h_tw_out    .GetName().split(sys_name)[0]+sys_name_Down)
                                #h_ttbar_out   .Write(h_ttbar_out .GetName().split(sys_name)[0]+sys_name_Down)
                                #h_DY_out      .Write(h_DY_out    .GetName().split(sys_name)[0]+sys_name_Down)
                                #h_jets_out    .Write(h_jets_out  .GetName().split(sys_name)[0]+sys_name_Down)
                                #h_other_out   .Write(h_other_out .GetName().split(sys_name)[0]+sys_name_Down)
                            else:
                                if no_signal==False and Do_FCNC_Study==False:
                                    h_tw_signal_out.Write()
                                    h_tw_signalonly_out.Write()
                                    h_ttbar_signal_out.Write()
                                    h_ttbar_signalonly_out.Write()
                                    h_tw_NLO_out.Write()
                                    h_ttbar_NNLO_out.Write()
                                elif Do_FCNC_Study:
                                    if "tug" in region:
                                        tmp_hist=all_system_hist[region][nsys]["FCNC_ST_tug"].Clone(str_fcnc+sys_name)
                                        tmp_hist.Scale(float(sf))
                                        tmp_hist.Write()
                                    elif "tcg" in region:
                                        tmp_hist=all_system_hist[region][nsys]["FCNC_ST_tcg"].Clone(str_fcnc+sys_name)
                                        tmp_hist.Scale(float(sf))
                                        tmp_hist.Write()
                                    else: print "Error: no tug or tcg !!!"
                                h_tw_out      .Write()
                                h_ttbar_out   .Write()
                                h_DY_out      .Write()
                                h_jets_out    .Write()
                                h_other_out   .Write()
                        f_out.Close()   
                        print "%s is saved"%(f_out.GetName())
        print "Limit hist Done!!"
            
    ############## event table #################
    event_table={}        
    if do_print_table:
        for hname in print_hist_name:
            event_table[hname]={}
            for nsys in all_system_hist[hanme]:
                event_table[hname][nsys]={}
                event_table[hname][nsys]["data"]   =all_system_hist[hanme][nsys]["data"].Clone("%s_%s_data"  %(hname,nsys))
                event_table[hname][nsys]["MC_all"] =all_system_hist[hanme][nsys]["data"].Clone("%s_%s_MC_all"%(hname,nsys))
                event_table[hname][nsys]["TW"]     =all_system_hist[hanme][nsys]["data"].Clone("%s_%s_TW"    %(hname,nsys))
                event_table[hname][nsys]["TTbar"]  =all_system_hist[hanme][nsys]["data"].Clone("%s_%s_TTbar" %(hname,nsys))
                event_table[hname][nsys]["other"]  =all_system_hist[hanme][nsys]["data"].Clone("%s_%s_other" %(hname,nsys))
                event_table[hname][nsys]["data"]  .Scale(0) 
                event_table[hname][nsys]["MC_all"].Scale(0) 
                event_table[hname][nsys]["TW"]    .Scale(0) 
                event_table[hname][nsys]["TTbar"] .Scale(0) 
                event_table[hname][nsys]["other"] .Scale(0) 
                for sname in all_system_hist[hanme][nsys]:
                    if "data" in sname:event_table[hname][nsys]["data"].Add(all_system_hist[hanme][nsys][sname])
                    elif "TW" in sname:
                        event_table[hname][nsys]["TW"]    .Add(all_system_hist[hanme][nsys][sname])
                        event_table[hname][nsys]["MC_all"].Add(all_system_hist[hanme][nsys][sname])
                    elif "TTTo2L2Nu" in sname:
                        event_table[hname][nsys]["TTbar"] .Add(all_system_hist[hanme][nsys][sname])
                        event_table[hname][nsys]["MC_all"].Add(all_system_hist[hanme][nsys][sname])
                    else: 
                        event_table[hname][nsys]["other"] .Add(all_system_hist[hanme][nsys][sname])
                        event_table[hname][nsys]["MC_all"].Add(all_system_hist[hanme][nsys][sname])
        for hname in print_hist_name:
            print "%s| data | all mc | TW  | ttbar  | other |"%(hname)
            Nbins=event_table[hname]["nominal"]["data"].GetNbinsX()
            err_data_nominal  =ROOT.Double(0)
            err_MC_all_nominal=ROOT.Double(0)
            err_TW_nominal    =ROOT.Double(0)
            err_TTbar_nominal =ROOT.Double(0)
            err_other_nominal =ROOT.Double(0)
            N_data_nominal  = event_table[hname]["nominal"]["data"]  .IntegralAndError(1,Nbins,err_data_nominal  )
            N_MC_all_nominal= event_table[hname]["nominal"]["MC_all"].IntegralAndError(1,Nbins,err_MC_all_nominal)
            N_TW_nominal    = event_table[hname]["nominal"]["TW"]    .IntegralAndError(1,Nbins,err_TW_nominal    )
            N_TTbar_nominal = event_table[hname]["nominal"]["TTbar"] .IntegralAndError(1,Nbins,err_TTbar_nominal )
            N_other_nominal = event_table[hname]["nominal"]["other"] .IntegralAndError(1,Nbins,err_other_nominal )
            print "nominal| %f +- %f | %f +- %f | %f +- %f | %f +- %f | %f +- %f |"%(N_data_nominal,err_data_nominal,N_MC_all_nominal,err_MC_all_nominal,N_TW_nominal,err_TW_nominal,N_TTbar_nominal,err_TTbar_nominal,N_other_nominal,err_other_nominal) 
            for nsys in event_table[hname]:
                if nsys == "nominal": continue
                N_data_diff  = float(event_table[hname][nsys]["data"]  .IntegralAndError(1,Nbins,err_data_nominal  ) - N_data_nominal  ) 
                N_MC_all_diff= float(event_table[hname][nsys]["MC_all"].IntegralAndError(1,Nbins,err_MC_all_nominal) - N_MC_all_nominal)
                N_TW_diff    = float(event_table[hname][nsys]["TW"]    .IntegralAndError(1,Nbins,err_TW_nominal    ) - N_TW_nominal    )
                N_TTbar_diff = float(event_table[hname][nsys]["TTbar"] .IntegralAndError(1,Nbins,err_TTbar_nominal ) - N_TTbar_nominal )
                N_other_diff = float(event_table[hname][nsys]["other"] .IntegralAndError(1,Nbins,err_other_nominal ) - N_other_nominal )
                print "%s| %f  | %f  | %f  | %f  | %f  |"%(nsys,N_data_diff,N_MC_all_diff,N_TW_diff,N_TTbar_diff,N_other_diff) 
                        
            
            
        


if do_trigger_study:
    #Files_trig               =file_object(Channel+"_"+"trig_hist"            ,"data and mc"          , Lumi    ,1      ,ROOT.kBlack)
    Files_trig               =file_object(Channel+"_"+"trig_hist_noSkip"            ,"data and mc"          , Lumi    ,1      ,ROOT.kBlack)
    #str_data="trig__RunBCDEFGH__"
    str_data="trig__RunBCDE__"
    #str_data="trig__RunFGH__"
    str_mc  ="trig__TTTo2L2Nu__"
    hist_list=['H2_pt1_pt2','H2_MET_Nvtx','H2_Njet_Nbjet']
    if   Channel=="ee"  :
        hist_list.append('H2_ee_eta1_eta2')
        hist_list.append('H_ee_region')
    elif Channel=="emu" :
        hist_list.append('H2_emu_eta1_eta2')
        hist_list.append('H_emu_region')
    elif Channel=="mumu":
        hist_list.append('H2_mumu_eta1_eta2')
        hist_list.append('H_mumu_region')

    for hname in hist_list:
        if "region" not in hname:
            h_2D_data     =Files_trig.tfile.Get(str_data+hname)
            h_2D_data_pass=Files_trig.tfile.Get(str_data+hname+"_pass")
            h_2D_mc       =Files_trig.tfile.Get(str_mc+hname)
            h_2D_mc_pass  =Files_trig.tfile.Get(str_mc+hname+"_pass")
            h_data_x      =H2D_2H1D(h_2D_data)[0] 
            h_data_y      =H2D_2H1D(h_2D_data)[1] 
            h_mc_x        =H2D_2H1D(h_2D_mc)[0] 
            h_mc_y        =H2D_2H1D(h_2D_mc)[1] 
            h_data_pass_x =H2D_2H1D(h_2D_data_pass)[0] 
            h_data_pass_y =H2D_2H1D(h_2D_data_pass)[1] 
            h_mc_pass_x   =H2D_2H1D(h_2D_mc_pass)[0] 
            h_mc_pass_y   =H2D_2H1D(h_2D_mc_pass)[1] 
            eff_data_x = ROOT.TGraphAsymmErrors()
            eff_data_y = ROOT.TGraphAsymmErrors()
            eff_mc_x   = ROOT.TGraphAsymmErrors()
            eff_mc_y   = ROOT.TGraphAsymmErrors()
            eff_data_x.Divide(h_data_pass_x,h_data_x,"cl=0.683 b(1,1) mode")
            eff_data_y.Divide(h_data_pass_y,h_data_y,"cl=0.683 b(1,1) mode")
            eff_mc_x  .Divide(h_mc_pass_x  ,h_mc_x  ,"cl=0.683 b(1,1) mode")
            eff_mc_y  .Divide(h_mc_pass_y  ,h_mc_y  ,"cl=0.683 b(1,1) mode")
            out_name1="_unname1"
            out_name2="_unname2"
            if "eta" in hname:
                out_name1="lead_eta"
                out_name2="sub_eta"
            elif "pt" in hname:
                out_name1="lead_pt"
                out_name2="sub_pt"
            elif "MET" in hname:
                out_name1="MET"
                out_name2="Nvtx"
            elif "Njet" in hname:
                out_name1="Njet"
                out_name2="Nbjet"
            draw_graph_compare(eff_data_x,eff_mc_x,out_name1,Channel)
            draw_graph_compare(eff_data_y,eff_mc_y,out_name2,Channel)

            can = ROOT.TCanvas('can','',50,50,865,780)
            can.cd()
            h_data_x.Draw("hist")
            h_data_pass_x.Draw("same:pe")
            can.Print('%s/%s/%s.png'%(dir,date,hname+"_data_x"))    
            can.Clear()
            h_data_y.Draw("hist")
            h_data_pass_y.Draw("same:pe")
            can.Print('%s/%s/%s.png'%(dir,date,hname+"_data_y"))    
            can.Clear()
            h_mc_x.Draw("hist")
            h_mc_pass_x.Draw("same:pe")
            can.Print('%s/%s/%s.png'%(dir,date,hname+"_mc_x"))    
            can.Clear()
            h_mc_y.Draw("hist")
            h_mc_pass_y.Draw("same:pe")
            can.Print('%s/%s/%s.png'%(dir,date,hname+"_mc_y"))    
            del can
            gc.collect()
        else:
            h_data     =Files_trig.tfile.Get(str_data+hname)
            h_data_pass=Files_trig.tfile.Get(str_data+hname+"_pass")
            h_mc       =Files_trig.tfile.Get(str_mc+hname)
            h_mc_pass  =Files_trig.tfile.Get(str_mc+hname+"_pass")
            eff_data   = ROOT.TGraphAsymmErrors()
            eff_mc     = ROOT.TGraphAsymmErrors()
            eff_data  .Divide(h_data_pass,h_data  ,"cl=0.683 b(1,1) mode")
            eff_mc    .Divide(h_mc_pass  ,h_mc  ,"cl=0.683 b(1,1) mode")
            print "|%s    | BB                 | BE                 | EE                 |   BB+BE+EE   |"%(Channel)
            print "| data |",
            for ix in range(0,eff_data.GetN()):
                print " %.3f +%.3f/-%.3f |"%(eff_data.GetY()[ix],eff_data.GetErrorYhigh(ix),eff_data.GetErrorYlow(ix)),
            print "\n"
            print "| MC   |",
            for ix in range(0,eff_mc.GetN()):
                print " %.3f +%.3f/-%.3f |"%(eff_mc.GetY()[ix],eff_mc.GetErrorYhigh(ix),eff_mc.GetErrorYlow(ix)),
            print "\n"
            print "| sf   |",
            for ir in range(0,eff_mc.GetN()):
                ratio_value  =eff_data.GetY()[ir]/eff_mc.GetY()[ir] if eff_mc.GetY()[ir] !=0 else 0
                data_err_up  =eff_data.GetEYhigh()[ir]
                data_err_down=eff_data.GetEYlow()[ir]
                mc_err_up    =eff_mc.GetEYhigh()[ir]
                mc_err_down  =eff_mc.GetEYlow()[ir]
                ratio_err_up  =ratio_value*math.sqrt(math.pow(data_err_up  /eff_data.GetY()[ir],2)+math.pow(mc_err_up  /eff_mc.GetY()[ir],2)) if eff_data.GetY()[ir]!=0 and eff_mc.GetY()[ir] !=0 else 0
                ratio_err_down=ratio_value*math.sqrt(math.pow(data_err_down/eff_data.GetY()[ir],2)+math.pow(mc_err_down/eff_mc.GetY()[ir],2)) if eff_data.GetY()[ir]!=0 and eff_mc.GetY()[ir] !=0 else 0
                print " %.3f +%.3f/-%.3f |"%(ratio_value,ratio_err_up,ratio_err_down),
            print "\n"
            print "trigger sf table done!" 
