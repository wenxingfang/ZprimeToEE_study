import ROOT
import gc
ROOT.TH1.AddDirectory(ROOT.kFALSE)
ROOT.gROOT.SetBatch(ROOT.kTRUE)

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
    x_min=60
    x_max=120
    y_min=0
    y_max=2*h_data.GetMaximum()
    dummy = ROOT.TH2D("dummy","",1,x_min,x_max,1,y_min,y_max)
    dummy.SetStats(ROOT.kFALSE)
    X_title='m(ee) [GeV]'
    Y_title='Events / %.1f GeV'%h_data.GetBinWidth(1)
    dummy.GetYaxis().SetTitle(Y_title)
    dummy.GetYaxis().SetTitleSize(0.05)
    dummy.GetYaxis().SetLabelSize(0.045)
    dummy.GetYaxis().SetTitleOffset(1.3)
    dummy.GetXaxis().SetTitle("")
    dummy.GetXaxis().SetLabelSize(0.045)
    dummy.GetXaxis().SetMoreLogLabels()
    dummy.GetXaxis().SetNoExponent()  
    dummy.Draw()
    h_mc.SetFillColor(ROOT.TColor.GetColor("#99ccff"))
    h_mc.SetMarkerColor(ROOT.TColor.GetColor("#99ccff"))
#    h_mc.SetLineColor(ROOT.TColor.GetColor("#99ccff"))
    h_mc.SetLineColor(ROOT.kBlack)
    h_data.SetMarkerColor(ROOT.kBlack)
    h_data.SetMarkerStyle(8)
    h_mc.Draw("hist:same")
    h_mc.Draw("same:e2")
    h_data.Draw("pe:same")
    dummy.Draw("AXISSAME")
    legend = ROOT.TLegend(0.5, 0.68, 0.84, 0.88, "", "brNDC")
    legend.AddEntry(h_data,'Data','epl')
    legend.AddEntry(h_mc  ,"#gamma*/Z #rightarrow e^{+} e^{-}",'f')
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
    #ratio_y_max=2
    ratio_y_min=0.7
    ratio_y_max=1.3
    dummy_ratio = ROOT.TH2D("dummy_ratio","",1,x_min,x_max,1,ratio_y_min,ratio_y_max)
    dummy_ratio.SetStats(ROOT.kFALSE)
    dummy_ratio.GetYaxis().SetTitle('Data/mc')
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

#F_out=ROOT.TFile("./mee_Zpeak_2016.root","RECREATE")
#F_out=ROOT.TFile("./mee_Zpeak_2017.root","RECREATE")
F_out=ROOT.TFile("./mee_Zpeak_2018.root","RECREATE")
#F_mc_in  =ROOT.TFile("/user/wenxing/ST_TW_channel/CMSSW_10_2_13/src/Zprime/ntuples/sys_saved_hist/2016/20190621_GenM/all/hist_ZToEE_50_120_fewz.root","read")
#F_mc_in  =ROOT.TFile("/user/wenxing/ST_TW_channel/CMSSW_10_2_13/src/Zprime/ntuples/sys_saved_hist/2017/20190623_GenM/all/hist_ZToEE_50_120_fewz.root","read")
F_mc_in  =ROOT.TFile("/user/wenxing/ST_TW_channel/CMSSW_10_2_13/src/Zprime/ntuples/sys_saved_hist/2018/20190623_GenM/all/hist_ZToEE_50_120_fewz.root","read")
hist_mc_BB  =F_mc_in.Get("h_mee_Zpeak_BB_v1")
hist_mc_BE  =F_mc_in.Get("h_mee_Zpeak_BE_v1")
F_out.cd()
hist_mc_BB  .Write("mc_BB")
hist_mc_BE  .Write("mc_BE")
#for run in ["RunB","RunC","RunD","RunE","RunF","RunBCDEF"]:
for run in ["RunAll"]:
    #F_data_in=ROOT.TFile("/user/wenxing/ST_TW_channel/CMSSW_10_2_13/src/Zprime/ntuples/sys_saved_hist/2016/20190621_GenM/all/hist_data_MiniAOD.root","read")
    #F_data_in=ROOT.TFile("/user/wenxing/ST_TW_channel/CMSSW_10_2_13/src/Zprime/ntuples/sys_saved_hist/2017/20190623_GenM/all/hist_data_MiniAOD.root","read")
    F_data_in=ROOT.TFile("/user/wenxing/ST_TW_channel/CMSSW_10_2_13/src/Zprime/ntuples/sys_saved_hist/2018/20190623_GenM/all/hist_data_MiniAOD.root","read")
    for hist in ["h_mee_Zpeak_BB_v1","h_mee_Zpeak_BE_v1"]:
        hist_data=F_data_in.Get(hist)
        F_out.cd()
        str_out="data"
        if "BB" in hist:
            str_out=str_out+"_BB"
        elif "BE" in hist:
            str_out=str_out+"_BE"
        str_out=str_out+"_"+run
        hist_data.Write(str_out)
    F_data_in.Close()
F_out.Close()

print "save done!!"
if False:
    out_dir="./Zpeak_plot"
    date="20180227"
    #Luminosity=float(41368)
    Luminosity=float(13433)
    #mc_lumi=float(117344021.0)/(5765.4)
    mc_lumi=float(130621333.0)/(5765.4)
    F_data_in=ROOT.TFile("/user/wenxing/ST_TW_channel/CMSSW_9_4_0/src/Zprime/ntuples/sys_saved_hist/20180301_L1DR0p5/runF/hist_data_MiniAOD.root","read")
    F_mc_in  =ROOT.TFile("/user/wenxing/ST_TW_channel/CMSSW_9_4_0/src/Zprime/ntuples/sys_saved_hist/20180228_L1SingleEG/runF/hist_DYToLL_amc.root","read")
    RunF_HEEP_SF_BB=0.941*0.941
    RunF_HEEP_SF_BE=0.941*0.957
    RunF_HEEP_SF_EE=0.957*0.957
    #RunF_HEEP_SF_BB=1
    #RunF_HEEP_SF_BE=1
    for hist in ["h_mee_Zpeak_BB_v1","h_mee_Zpeak_BE_v1","h_mee_Zpeak_EE_v1"]:
    #for hist in ["h_mee_Zpeak_BB","h_mee_Zpeak_BE"]:
        h_data=F_data_in.Get(hist)
        print "%s N data=%f"%(str(hist),h_data.GetSumOfWeights())
        h_mc  =F_mc_in.Get(hist)
    #    h_mc.Sumw2()
        if "BB" in hist:
            h_mc.Scale(RunF_HEEP_SF_BB*Luminosity/mc_lumi)
        elif "BE" in hist:
            h_mc.Scale(RunF_HEEP_SF_BE*Luminosity/mc_lumi)
        elif "EE" in hist:
            h_mc.Scale(RunF_HEEP_SF_EE*Luminosity/mc_lumi)
        draw_plots(date, out_dir,h_mc,h_data,hist)
    print "plot done!!"
