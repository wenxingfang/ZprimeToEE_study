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
    size = 0.23
    pad1 = ROOT.TPad('pad1', '', 0.0, size, 1.0, 1.0)
    pad2 = ROOT.TPad('pad2', '', 0.0, 0.0 , 1.0, 1.14*size)
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
    pad2.SetBottomMargin(0.36)
    pad2.SetRightMargin(0.05)
    pad2.SetLeftMargin(0.13)
    pad1.SetLogx()
    pad2.SetLogx()
    if "cumlative" in out_name and "v1" not in out_name:
        pad1.SetLogx(ROOT.kFALSE)
        pad2.SetLogx(ROOT.kFALSE)

    pad1.SetLogy()
    pad1.cd()
    final_other_hist_title={'h_pv_n':'Nvtx','h_Ptll':'P_{T}(ee) [GeV]','h_Etall':'#eta(ee)','h_Phill':'#phi(ee)','h_led_Et':'E_{T}^{Leading} [GeV]','h_led_eta':'#eta^{Leading}','h_led_phi':'#phi^{Leading}','h_sub_Et':'E_{T}^{Sub-leading} [GeV]','h_sub_eta':'#eta^{Sub-leading}','h_sub_phi':'#phi^{Sub-leading}','h_MET':'MET [GeV]','h_MET_phi':'#phi^{MET}','h_MET_T1Txy':'MET(T1Txy) [GeV]','h_MET_phi_T1Txy':'#phi^{MET(T1Txy)}','h_MET_SF_T1Txy':'MET Significance','h_MET_Filter':'MET Filter','h_Dphi_ll':'#Delta#phi(e,e)','h_Dphi_MET_Z':'#Delta#phi(MET,ee)','h_DR_ll':'#DeltaR(e,e)','h_N_jet':'Number of jets','h_N_bjet':'Number of b jets','h_HT_sys':'HT^{system} [GeV]','h_Pt_sys':'P_{T}^{system} [GeV]','h_mee_Zpeak':'m(ee) [GeV]','h_mee_Zpeak_BB':'m(ee) [GeV]','h_mee_Zpeak_BE':'m(ee) [GeV]','h_mee_Zpeak_EE':'m(ee) [GeV]','h_mee_cosp':'m(ee) [GeV]','h_mee_cosp_BB':'m(ee) [GeV]','h_mee_cosp_BE':'m(ee) [GeV]','h_mee_cosp_EE':'m(ee) [GeV]','h_mee_cosm':'m(ee) [GeV]','h_mee_cosm_BB':'m(ee) [GeV]','h_mee_cosm_BE':'m(ee) [GeV]','h_mee_cosm_EE':'m(ee) [GeV]','h_cos':'cos#theta*','h_cos_BB':'cos#theta*','h_cos_BE':'cos#theta*','h_cos_EE':'cos#theta*','h_cos_all_region':'cos#theta*'}
    ########### For XY Range #############
    nbin=1
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
        y_max=1E10
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
    dummy.GetYaxis().SetTitleSize(0.063)
    dummy.GetYaxis().SetLabelSize(0.06)
    dummy.GetXaxis().SetLabelSize(0.06)
    dummy.GetYaxis().SetTitleOffset(1.06)
    dummy.GetXaxis().SetTitleOffset(1.0)
    dummy.GetXaxis().SetMoreLogLabels()
    dummy.GetXaxis().SetNoExponent()  
    dummy.GetXaxis().SetTitleFont(font)
    dummy.GetXaxis().SetLabelFont(font)
    dummy.GetYaxis().SetTitleFont(font)
    dummy.GetYaxis().SetLabelFont(font)
    dummy.GetXaxis().SetLabelSize(0)###remove top label
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
    Graph_Xerror0(g_data)
    g_mc.SetFillColor(ROOT.kRed-6)
    g_mc.SetFillStyle(3244)
    g_data.Draw("pZ0")
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
    legend = ROOT.TLegend(0.516741-0.065, 0.57, 0.870536-0.055, 0.88, "", "brNDC")
    legend.AddEntry(g_tmp_data,'Data','ep')
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
    legend.SetTextSize(0.055)
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
    label_cms.SetTextSize(0.53/0.75)
    label_cms.Draw()
    label_prelim = ROOT.TPaveLabel(0.69, 0.745, 0.96, 0.841, "Preliminary", "brNDC")
    label_prelim.SetBorderSize(0)
    label_prelim.SetFillColor(0)
    label_prelim.SetFillStyle(0)
    label_prelim.SetTextFont(51)
    label_prelim.SetTextSize(0.44/0.75 * 0.8)
    ##label_prelim.Draw()
    label_supply = ROOT.TPaveLabel(0.25, cms_y_low, 0.4, cms_y_up, "Supplementary", "brNDC")
    label_supply.SetBorderSize(0)
    label_supply.SetFillColor(0)
    label_supply.SetFillStyle(0)
    label_supply.SetTextFont(51)
    label_supply.SetTextSize(0.44/0.75 * 0.8)
    if isSupplementStyle:
        label_supply.Draw()
    label_lumi = ROOT.TPaveLabel(0.65, 0.888, 0.95, 0.988, "35.9 fb^{-1} (13 TeV)", "brNDC")
    label_lumi.SetBorderSize(0)
    label_lumi.SetFillColor(0)
    label_lumi.SetFillStyle(0)
    label_lumi.SetTextFont(font)
    label_lumi.SetTextSize(0.55)
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
    elif "BE" in out_name:
        labels_region.SetLabel("Barrel-Endcap")
        if "cosm"   in out_name:labels_region.SetLabel("Barrel-Endcap (cos#theta*<0)")
        elif "cosp" in out_name:labels_region.SetLabel("Barrel-Endcap (cos#theta*>0)")
    elif "EE" in out_name:
        labels_region.SetLabel("Endcap-Endcap")
        if "cosm"   in out_name:labels_region.SetLabel("Endcap-Endcap (cos#theta*<0)")
        elif "cosp" in out_name:labels_region.SetLabel("Endcap-Endcap (cos#theta*>0)")
    elif "cosm" in out_name:
        labels_region.SetLabel("cos#theta*<0")
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
    dummy_ratio.GetXaxis().SetTitleSize(0.06*fontScale)
    dummy_ratio.GetXaxis().SetTitleOffset(0.9)
    dummy_ratio.GetXaxis().SetLabelSize(0.044*fontScale)
    dummy_ratio.GetXaxis().SetTickLength(0.07)
    dummy_ratio.GetXaxis().SetMoreLogLabels()
    dummy_ratio.GetXaxis().SetNoExponent()  
    dummy_ratio.GetYaxis().SetNdivisions(305)
    dummy_ratio.GetYaxis().SetTitleSize(0.041*fontScale)
    dummy_ratio.GetYaxis().SetLabelSize(0.05 * fontScale * 0.96*1.1)
    dummy_ratio.GetYaxis().SetTitleOffset(0.54)
    dummy_ratio.GetYaxis().SetLabelOffset(0.012)
    dummy_ratio.GetXaxis().SetTitleFont(font)
    dummy_ratio.GetYaxis().SetTitleFont(font)
    dummy_ratio.GetXaxis().SetLabelFont(font)
    dummy_ratio.GetYaxis().SetLabelFont(font)
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
    remove_zero_point(g_ratio)
    g_ratio.Draw("pZ0")
    ######################################
#    pad2.RedrawAxis()
#    pad1.cd()
#    pad1.RedrawAxis()
#    pad1.Draw()
    ######################################
#    canvas.Update()
#    canvas.RedrawAxis()
    canvas.Print('%s/%s/%s.png'%(out_dir,date,out_name))    
    canvas.SaveAs('%s/%s/%s.pdf'%(out_dir,date,out_name))    
    canvas.SaveAs('%s/%s/%s.C'%(out_dir,date,out_name))    
    canvas.SaveAs('%s/%s/%s.root'%(out_dir,date,out_name))    
