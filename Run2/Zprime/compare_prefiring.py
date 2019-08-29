import ROOT
import math
import gc
ROOT.TH1.AddDirectory(ROOT.kFALSE)
ROOT.gROOT.SetBatch(ROOT.kTRUE)

def get_graph_ratio(g1, g2):
    g_ratio=g1.Clone("g_ratio_%s_%s"%(g1.GetName(),g2.GetName()))
    for ibin in range(0, g_ratio.GetN()):
         ratio=999
         err_down=0
         err_up=0
         if float(g2.GetY()[ibin]) !=0:
             #ratio=float((g1.GetY()[ibin]-g2.GetY()[ibin])/g2.GetY()[ibin])
             #err_down=math.fabs(float(g1.GetErrorYlow(ibin)/g2.GetY()[ibin]))
             #err_up  =math.fabs(float(g1.GetErrorYhigh(ibin)/g2.GetY()[ibin]))
             ratio=float(g1.GetY()[ibin]/g2.GetY()[ibin])
             err_down=math.sqrt(math.pow(g2.GetY()[ibin]*g1.GetErrorYlow(ibin),2) +math.pow(g1.GetY()[ibin]*g2.GetErrorYlow(ibin),2))/math.pow(g2.GetY()[ibin],2)
             err_up  =math.sqrt(math.pow(g2.GetY()[ibin]*g1.GetErrorYhigh(ibin),2)+math.pow(g1.GetY()[ibin]*g2.GetErrorYhigh(ibin),2))/math.pow(g2.GetY()[ibin],2)
         g_ratio.SetPoint(ibin,g_ratio.GetX()[ibin],ratio)
         g_ratio.SetPointEYlow(ibin,err_down)
         g_ratio.SetPointEYhigh(ibin,err_up)
    return g_ratio

def get_graph_ratio_v1(g1, g2):
    g_ratio=g1.Clone("g_ratio_%s_%s"%(g1.GetName(),g2.GetName()))
    for ibin in range(0, g_ratio.GetN()):
         ratio=999
         err_down=0
         err_up=0
         if float(g2.GetY()[ibin]) !=0:
             ratio=float(g1.GetY()[ibin]/g2.GetY()[ibin])
             err_down=math.fabs(float(g1.GetErrorYlow(ibin)/g2.GetY()[ibin]))
             err_up  =math.fabs(float(g1.GetErrorYhigh(ibin)/g2.GetY()[ibin]))
         g_ratio.SetPoint(ibin,g_ratio.GetX()[ibin],ratio)
         g_ratio.SetPointEYlow(ibin,err_down)
         g_ratio.SetPointEYhigh(ibin,err_up)
    return g_ratio

def draw_plots(date, out_dir,h_mc,h_data,out_name):
    stat_style=1001
    stat_color=ROOT.kRed-10
    stat_sys_style=1001
    stat_sys_color=ROOT.TColor.GetColor("#b4ccdb")
    canvas = ROOT.TCanvas('canvas_%s'%(out_name),'',100,100,1000,1000)
    canvas.cd()
    size = 0.25
    pad1 = ROOT.TPad('pad1', '', 0.0, size, 1.0, 1.0, 0)
    pad2 = ROOT.TPad('pad2', '', 0.0, 0.0, 1.0, size, 0)
    pad1.Draw()
    pad2.Draw() 
    pad2.SetGridy()
    pad1.SetLogy()
    pad1.SetLogx(ROOT.kTRUE)
    pad2.SetLogx()
    pad1.SetBottomMargin(0.07)
    pad2.SetTopMargin(0)
    pad2.SetBottomMargin(0.35)
    pad1.SetRightMargin(0.07)
    pad1.SetLeftMargin(0.13)
    pad2.SetRightMargin(0.07)
    pad2.SetLeftMargin(0.13)
    pad1.cd()
    ########### For XY Range #############
    nbin=1
    #x_min=80
    #x_max=100
    x_min=50
    x_max=4000
    y_min=1E-3
    y_max=3E5
    dummy = ROOT.TH2D("dummy","",1,x_min,x_max,1,y_min,y_max)
    dummy.SetStats(ROOT.kFALSE)
    X_title='m(ee) [GeV]'
#    Y_title='Events / %.1f GeV'%h_data.GetBinWidth(1)
    Y_title='Events / GeV'
    dummy.GetYaxis().SetTitle(Y_title)
    dummy.GetYaxis().SetTitleSize(0.05)
    dummy.GetYaxis().SetLabelSize(0.045)
    dummy.GetYaxis().SetTitleOffset(1.3)
    dummy.GetXaxis().SetTitle("")
    dummy.GetXaxis().SetLabelSize(0.045)
    dummy.GetXaxis().SetMoreLogLabels()
    dummy.GetXaxis().SetNoExponent()  
    dummy.Draw()
#    h_mc.SetFillColor(ROOT.TColor.GetColor("#99ccff"))
#    h_mc.SetMarkerColor(ROOT.TColor.GetColor("#99ccff"))
#    h_mc.SetLineColor(ROOT.kBlack)
    h_mc.SetMarkerColor(ROOT.kRed)
    h_mc.SetLineColor(ROOT.kRed)
    h_mc.SetMarkerStyle(8)
    h_data.SetMarkerColor(ROOT.kBlack)
    h_data.SetLineColor(ROOT.kBlack)
    h_data.SetMarkerStyle(8)
#    h_mc.Draw("hist:same")
#    h_mc.Draw("same:e2")
    h_mc.Draw("samepe")
    h_data.Draw("samepe")
    dummy.Draw("AXISSAME")
    legend = ROOT.TLegend(0.5, 0.75, 0.75, 0.88, "", "brNDC")
    legend.AddEntry(h_data,'data 2017','epl')
    legend.AddEntry(h_mc  ,"data 2018",'epl')
    legend.SetBorderSize(0)
    legend.SetLineColor(1)
    legend.SetLineStyle(1)
    legend.SetLineWidth(1)
    legend.SetFillColor(19)
    legend.SetFillStyle(0)
    font = 42
    legend.SetTextFont(font)
    legend.Draw()
    label_cms = ROOT.TPaveLabel(0.712, 0.811, 0.969, 0.907, "CMS", "brNDC")
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
    label_lumi = ROOT.TPaveLabel(0.69, 0.902, 0.994, 0.997, "%.1f fb^{-1} (13 TeV)"%(float(Luminosity/1000)), "brNDC")
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
        labels_region.Draw()
    elif "BE" in out_name:
        labels_region.SetLabel("Barrel-Endcap")
        labels_region.Draw()
    elif "EE" in out_name:
        labels_region.SetLabel("Endcap-Endcap")
        labels_region.Draw()
    pad2.cd()
    ######################################
    #ratio_y_min=0
    #ratio_y_max=1.99
    ratio_y_min=0.5
    ratio_y_max=1.49
    dummy_ratio = ROOT.TH2D("dummy_ratio","",1,x_min,x_max,1,ratio_y_min,ratio_y_max)
    dummy_ratio.SetStats(ROOT.kFALSE)
    dummy_ratio.GetYaxis().SetTitle('2017/2018')
    dummy_ratio.GetYaxis().CenterTitle()
    dummy_ratio.GetXaxis().SetTitle(X_title)
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
    h_ratio=h_data.Clone("h_ratio_%s"%out_name)
    h_ratio.Divide(h_mc)
    h_ratio.Draw("same:pe")
#    dummy_ratio.Draw("AXISSAME")
    canvas.Print('%s/%s/%s.png'%(out_dir,date,out_name))    
    del canvas
    gc.collect()

def draw_plots_gr(date, out_dir,gr1,gr2,cat,out_name):
    stat_style=1001
    stat_color=ROOT.kRed-10
    stat_sys_style=1001
    stat_sys_color=ROOT.TColor.GetColor("#b4ccdb")
    canvas = ROOT.TCanvas('canvas_%s'%(out_name),'',100,100,1000,1000)
    canvas.cd()
    size = 0.25
    pad1 = ROOT.TPad('pad1', '', 0.0, size, 1.0, 1.0, 0)
    pad2 = ROOT.TPad('pad2', '', 0.0, 0.0, 1.0, size, 0)
    pad1.Draw()
    pad2.Draw() 
    pad2.SetGridy()
    pad1.SetLogy()
    pad1.SetLogx(ROOT.kTRUE)
    pad2.SetLogx()
    pad1.SetBottomMargin(0.07)
    pad2.SetTopMargin(0)
    pad2.SetBottomMargin(0.35)
    pad1.SetRightMargin(0.07)
    pad1.SetLeftMargin(0.13)
    pad2.SetRightMargin(0.07)
    pad2.SetLeftMargin(0.13)
    pad1.cd()
    ########### For XY Range #############
    nbin=1
    x_min=70
    x_max=4000
    y_min=1E-3
    y_max=1E7
    dummy = ROOT.TH2D("dummy","",1,x_min,x_max,1,y_min,y_max)
    dummy.SetStats(ROOT.kFALSE)
    X_title='m(ee) [GeV]'
    Y_title='Events / GeV'
    dummy.GetYaxis().SetTitle(Y_title)
    dummy.GetYaxis().SetTitleSize(0.05)
    dummy.GetYaxis().SetLabelSize(0.045)
    dummy.GetYaxis().SetTitleOffset(1.3)
    dummy.GetXaxis().SetTitle("")
    dummy.GetXaxis().SetLabelSize(0.045)
    dummy.GetXaxis().SetMoreLogLabels()
    dummy.GetXaxis().SetNoExponent()  
    dummy.Draw()
    gr1.SetMarkerColor(ROOT.kRed)
    gr1.SetLineColor(ROOT.kRed)
    gr1.SetMarkerStyle(8)
    gr1.SetMarkerSize(1)
    gr2.SetMarkerColor(ROOT.kBlack)
    gr2.SetLineColor(ROOT.kBlack)
    gr2.SetMarkerStyle(8)
    gr2.SetMarkerSize(1)
    gr1.Draw("pe")
    gr2.Draw("pe")
    dummy.Draw("AXISSAME")
    legend = ROOT.TLegend(0.4, 0.77, 0.65, 0.9, "", "brNDC")
    str_add=""
    if cat=="mc":
        str_add="94X"
    #legend.AddEntry(gr1,'%s %s 2017'%(cat,str_add),'epl')
    legend.AddEntry(gr1,'%s 102X_Autumn18 2018'%(cat),'epl')
    legend.AddEntry(gr2,"%s %s 2018"%(cat,str_add),'epl')
    legend.SetBorderSize(0)
    legend.SetLineColor(1)
    legend.SetLineStyle(1)
    legend.SetLineWidth(1)
    legend.SetFillColor(19)
    legend.SetFillStyle(0)
    legend.SetTextSize(0.04)
    font = 42
    legend.SetTextFont(font)
    legend.Draw()
    label_cms = ROOT.TPaveLabel(0.712, 0.811, 0.969, 0.907, "CMS", "brNDC")
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
    label_lumi = ROOT.TPaveLabel(0.69, 0.902, 0.994, 0.997, "%.1f fb^{-1} (13 TeV)"%(float(Luminosity/1000)), "brNDC")
    label_lumi.SetBorderSize(0)
    label_lumi.SetFillColor(0)
    label_lumi.SetFillStyle(0)
    label_lumi.SetTextFont(font)
    label_lumi.SetTextSize(0.44)
    label_lumi.Draw()
    labels_region = ROOT.TPaveLabel(0.12, 0.812937, 0.5, 0.907343, "", "brNDC")
    labels_region.SetBorderSize(0)
    labels_region.SetFillColor(0)
    labels_region.SetFillStyle(0)
    labels_region.SetTextFont(font)
    labels_region.SetTextSize(0.425926 )  
    if "BB" in out_name:
        labels_region.SetLabel("Barrel-Barrel")
        labels_region.Draw()
    elif "BE" in out_name:
        labels_region.SetLabel("Barrel-Endcap")
        labels_region.Draw()
    elif "EE" in out_name:
        labels_region.SetLabel("Endcap-Endcap")
        labels_region.Draw()
    pad2.cd()
    ######################################
    #ratio_y_min=0
    #ratio_y_max=1.99
    ratio_y_min=0.7
    ratio_y_max=1.29
    dummy_ratio = ROOT.TH2D("dummy_ratio","",1,x_min,x_max,1,ratio_y_min,ratio_y_max)
    dummy_ratio.SetStats(ROOT.kFALSE)
    #dummy_ratio.GetYaxis().SetTitle('2017/2018')
    dummy_ratio.GetYaxis().SetTitle('102X/94X')
    dummy_ratio.GetYaxis().CenterTitle()
    dummy_ratio.GetXaxis().SetTitle(X_title)
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
    g_ratio=ROOT.TGraph()
    if gr1.GetN()==gr2.GetN():
        g_ratio = get_graph_ratio(gr1, gr2)
#    Graph_Xerror0(g_ratio) 
#    remove_zero_point(g_ratio, -1)
    g_ratio.Draw("pZ0")
    dummy_ratio.Draw("AXISSAME")
    canvas.Update()
    canvas.Print('%s/%s/%s_%s.png'%(out_dir,date,cat,out_name))    
    del canvas
    gc.collect()



def draw_plots_gr_v1(date, out_dir,gr1,gr2,gr3,gr4,cat,out_name):
    stat_style=1001
    stat_color=ROOT.kRed-10
    stat_sys_style=1001
    stat_sys_color=ROOT.TColor.GetColor("#b4ccdb")
    canvas = ROOT.TCanvas('canvas_%s'%(out_name),'',100,100,1000,1000)
    canvas.cd()
    size = 0.25
    pad1 = ROOT.TPad('pad1', '', 0.0, size, 1.0, 1.0, 0)
    pad2 = ROOT.TPad('pad2', '', 0.0, 0.0, 1.0, size, 0)
    pad1.Draw()
    pad2.Draw() 
    pad2.SetGridy()
    pad1.SetLogy()
    pad1.SetLogx(ROOT.kTRUE)
    pad2.SetLogx()
    pad1.SetBottomMargin(0.07)
    pad2.SetTopMargin(0)
    pad2.SetBottomMargin(0.35)
    pad1.SetRightMargin(0.07)
    pad1.SetLeftMargin(0.13)
    pad2.SetRightMargin(0.07)
    pad2.SetLeftMargin(0.13)
    pad1.cd()
    ########### For XY Range #############
    nbin=1
    x_min=70
    x_max=4000
    y_min=1E-3
    y_max=1E7
    dummy = ROOT.TH2D("dummy","",1,x_min,x_max,1,y_min,y_max)
    dummy.SetStats(ROOT.kFALSE)
    X_title='m(ee) [GeV]'
    Y_title='Events / GeV'
    dummy.GetYaxis().SetTitle(Y_title)
    dummy.GetYaxis().SetTitleSize(0.05)
    dummy.GetYaxis().SetLabelSize(0.045)
    dummy.GetYaxis().SetTitleOffset(1.3)
    dummy.GetXaxis().SetTitle("")
    dummy.GetXaxis().SetLabelSize(0.045)
    dummy.GetXaxis().SetMoreLogLabels()
    dummy.GetXaxis().SetNoExponent()  
    dummy.Draw()
    gr1.SetMarkerColor(ROOT.kBlack)
    gr1.SetLineColor(ROOT.kBlack)
    gr1.SetMarkerStyle(8)
    gr1.SetMarkerSize(1)
    gr2.SetMarkerColor(ROOT.kGreen)
    gr2.SetLineColor(ROOT.kGreen)
    gr2.SetMarkerStyle(8)
    gr2.SetMarkerSize(1)
    gr3.SetMarkerColor(ROOT.kBlue)
    gr3.SetLineColor(ROOT.kBlue)
    gr3.SetMarkerStyle(8)
    gr3.SetMarkerSize(1)
    gr4.SetMarkerColor(ROOT.kRed)
    gr4.SetLineColor(ROOT.kRed)
    gr4.SetMarkerStyle(8)
    gr4.SetMarkerSize(1)
    gr1.Draw("pe")
    gr2.Draw("pe")
    gr3.Draw("pe")
    gr4.Draw("pe")
    dummy.Draw("AXISSAME")
    legend = ROOT.TLegend(0.45, 0.7, 0.7, 0.88, "", "brNDC")
    str_add=""
    legend.AddEntry(gr1,'Nominal'       ,'epl')
    legend.AddEntry(gr2,"Prefiring"     ,'epl')
    legend.AddEntry(gr3,"Prefiring up"  ,'epl')
    legend.AddEntry(gr4,"Prefiring down",'epl')
    legend.SetBorderSize(0)
    legend.SetLineColor(1)
    legend.SetLineStyle(1)
    legend.SetLineWidth(1)
    legend.SetFillColor(19)
    legend.SetFillStyle(0)
    legend.SetTextSize(0.04)
    font = 42
    legend.SetTextFont(font)
    legend.Draw()
    label_cms = ROOT.TPaveLabel(0.712, 0.811, 0.969, 0.907, "CMS", "brNDC")
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
    label_lumi = ROOT.TPaveLabel(0.7, 0.89, 0.99, 0.96, "%.1f fb^{-1} (13 TeV)"%(float(Luminosity/1000)), "brNDC")
    label_lumi.SetBorderSize(0)
    label_lumi.SetFillColor(0)
    label_lumi.SetFillStyle(0)
    label_lumi.SetTextFont(font)
    label_lumi.SetTextSize(0.44)
    label_lumi.Draw()
    labels_region = ROOT.TPaveLabel(0.12, 0.812937, 0.5, 0.907343, "", "brNDC")
    labels_region.SetBorderSize(0)
    labels_region.SetFillColor(0)
    labels_region.SetFillStyle(0)
    labels_region.SetTextFont(font)
    labels_region.SetTextSize(0.425926 )  
    if "BB" in out_name:
        labels_region.SetLabel("Barrel-Barrel")
        labels_region.Draw()
    elif "BE" in out_name:
        labels_region.SetLabel("Barrel-Endcap")
        labels_region.Draw()
    elif "EE" in out_name:
        labels_region.SetLabel("Endcap-Endcap")
        labels_region.Draw()
    pad2.cd()
    ######################################
    #ratio_y_min=0
    #ratio_y_max=1.99
    ratio_y_min=0.7
    ratio_y_max=1.29
    dummy_ratio = ROOT.TH2D("dummy_ratio","",1,x_min,x_max,1,ratio_y_min,ratio_y_max)
    dummy_ratio.SetStats(ROOT.kFALSE)
    dummy_ratio.GetYaxis().SetTitle('X/Prefiring')
    dummy_ratio.GetYaxis().CenterTitle()
    dummy_ratio.GetXaxis().SetTitle(X_title)
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
    g_ratio_N=ROOT.TGraph()
    g_ratio_U=ROOT.TGraph()
    g_ratio_D=ROOT.TGraph()
    g_ratio_N = get_graph_ratio_v1(gr1, gr2)
    g_ratio_U = get_graph_ratio_v1(gr3, gr2)
    g_ratio_D = get_graph_ratio_v1(gr4, gr2)
#    Graph_Xerror0(g_ratio) 
#    remove_zero_point(g_ratio, -1)
    g_ratio_N.Draw("pZ0")
    g_ratio_U.Draw("pZ0")
    g_ratio_D.Draw("pZ0")
    dummy_ratio.Draw("AXISSAME")
    canvas.Update()
    canvas.Print('%s/%s/%s_%s.png'%(out_dir,date,cat,out_name))    
    del canvas
    gc.collect()


Luminosity=41500.0

if False:
    out_dir="./compare_plot"
    date="20180616"
    F_2018 =ROOT.TFile("/user/wenxing/ST_TW_channel/CMSSW_10_1_4/src/Zprime/ntuples/sys_saved_hist/20180616/all/hist_data_MiniAOD.root","read")
    F_2017 =ROOT.TFile("/user/wenxing/ST_TW_channel/CMSSW_9_4_0/src/Zprime/ntuples/sys_saved_hist/20180302_newTurnOn/all/hist_data_MiniAOD.root","read")
    L_2018=9535.0
    L_2017=41368.0
    
    for hist in ["h_mee_all","h_mee_all_BB","h_mee_all_BE","h_mee_all_EE"]:
        h_2018=F_2018.Get(hist)
        h_2017=F_2017.Get(hist)
        h_2018.Scale(Luminosity/L_2018)
        h_2017.Scale(Luminosity/L_2017)
        draw_plots(date, out_dir,h_2018,h_2017,hist)
    print "plot done!!"


if True:
    out_dir="./compare_plot"
    date="20190606"
    F_nominal =ROOT.TFile("/user/wenxing/ST_TW_channel/CMSSW_10_2_13/src/Zprime/HEPData_2016_nominal.root" ,"read")
    F_pf      =ROOT.TFile("/user/wenxing/ST_TW_channel/CMSSW_10_2_13/src/Zprime/HEPData_2016_pf.root"      ,"read")
    F_pf_up   =ROOT.TFile("/user/wenxing/ST_TW_channel/CMSSW_10_2_13/src/Zprime/HEPData_2016_pf_up.root"   ,"read")
    F_pf_down =ROOT.TFile("/user/wenxing/ST_TW_channel/CMSSW_10_2_13/src/Zprime/HEPData_2016_pf_down.root" ,"read")
    
#    cat="mc"
#    cat="ZToEE"
    for cat in ['mc','ZToEE','ttbar','jets']:
        for hist in ["h_mee_all","h_mee_all_BB","h_mee_all_BE","h_mee_all_EE"]:
            gr_nominal=F_nominal.Get(str(cat+"_"+hist))
            gr_pf     =F_pf     .Get(str(cat+"_"+hist))
            gr_pf_up  =F_pf_up  .Get(str(cat+"_"+hist))
            gr_pf_down=F_pf_down.Get(str(cat+"_"+hist))
            if gr_nominal.GetN() != gr_pf.GetN():
                print "wrong bin"
                continue
            draw_plots_gr_v1(date, out_dir,gr_nominal, gr_pf, gr_pf_up, gr_pf_down, cat, hist)
    print "plot done!!"


