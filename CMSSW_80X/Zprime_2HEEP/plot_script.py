
def draw_plots(date, out_dir, h_stack,h_mc,g_mc,h_data,out_name, blind):
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
    pad1.SetTickx(1)
    pad1.SetTicky(1)
    pad2.SetTickx(1)
    pad2.SetTicky(1)
    pad2.SetGridy()
    pad1.SetBottomMargin(0.05)
    pad2.SetTopMargin(0.0375)
    pad2.SetBottomMargin(0.35)
    pad1.SetRightMargin(0.05)
    pad1.SetLeftMargin(0.13)
    pad2.SetRightMargin(0.05)
    pad2.SetLeftMargin(0.13)
    pad1.cd()
    pad1.SetLogx()
    pad2.SetLogx()
    pad1.SetLogy()
    ########### For XY Range #############
    nbin=1
    x_min=70
    x_max=4000
    y_min=1E-5
    y_max=5E6
    if "cumlative" in out_name:
        y_max=1E8
        y_min=1E-4
    dummy = ROOT.TH2D("dummy","",nbin,x_min,x_max,1,y_min,y_max)
    dummy.SetStats(ROOT.kFALSE)
    X_title='m(ee) [GeV]'
    dummy_Y_title='Events / GeV'
    if "cumlative" in out_name :
        dummy_Y_title='Events #geq m(ee)'

    dummy.GetYaxis().SetTitle(dummy_Y_title)
    dummy.GetYaxis().SetTitleSize(0.05)
    dummy.GetYaxis().SetLabelSize(0.045)
    dummy.GetYaxis().SetTitleOffset(1.3)
    dummy.GetXaxis().SetLabelSize(0.045)
    dummy.GetXaxis().SetMoreLogLabels()
    dummy.GetXaxis().SetNoExponent()  
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
            if h_Zprime.GetBinLowEdge(iZ)<2400 or h_Zprime.GetBinLowEdge(iZ)>3500:h_Zprime_bgk.SetBinContent(iZ,0)
        h_Zprime_bgk.SetLineColor(ROOT.TColor.GetColor("#008000"))
        h_Zprime_bgk.SetLineWidth(2)
        h_Zprime_bgk.Draw("sames:hist")
    ########### For bgk and data #############
    h_stack.Draw('sames:hist')
    dummy.Draw("AXISSAME")
    g_data=histTograph(h_data)
    g_data.SetLineColor(ROOT.kBlack)
    g_data.SetMarkerStyle(20)
    g_data.SetMarkerSize(0.8)
    Graph_Xerror0(g_data)
    g_mc.SetFillColor(ROOT.kRed-6)
    g_mc.SetFillStyle(3244)
    g_data.Draw("pZ0")
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
    h_tmp_Jets .SetFillColor(ROOT.kYellow) 
    legend = ROOT.TLegend(0.48, 0.61, 0.85, 0.88, "", "brNDC")
    legend.AddEntry(g_data,'Data','ep')
    legend.AddEntry(h_tmp_ZToEE,"#gamma*/Z #rightarrow e^{+} e^{-}",'f')
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
    label_lumi = ROOT.TPaveLabel(0.67, 0.902, 0.992, 0.997, "35.9 fb^{-1} (13 TeV)", "brNDC")
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
    ratio_y_min=-1
    ratio_y_max=1
    dummy_ratio = ROOT.TH2D("dummy_ratio","",nbin,x_min,x_max,1,ratio_y_min,ratio_y_max)
    dummy_ratio.SetStats(ROOT.kFALSE)
    dummy_ratio.GetYaxis().SetTitle('(Data #minus Bgk) / Bgk')
    dummy_ratio.GetXaxis().SetTitle(X_title)
    dummy_ratio.SetMarkerSize(0.7)
    dummy_ratio.GetXaxis().SetTitleSize(0.14)
    dummy_ratio.GetXaxis().SetTitleOffset(1.1)
    dummy_ratio.GetXaxis().SetLabelSize(0.14)
    dummy_ratio.GetXaxis().SetMoreLogLabels()
    dummy_ratio.GetXaxis().SetNoExponent()  
    dummy_ratio.GetYaxis().SetNdivisions(405)
    dummy_ratio.GetYaxis().SetTitleSize(0.11)
    dummy_ratio.GetYaxis().SetLabelSize(0.14)
    dummy_ratio.GetYaxis().SetTitleOffset(0.55)
    dummy_ratio.Draw()
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
    g_ratio.Draw("pZ0")
    canvas.Update()
    canvas.Print('%s/%s/%s.png'%(out_dir,date,out_name))    
    canvas.SaveAs('%s/%s/%s.pdf'%(out_dir,date,out_name))    
