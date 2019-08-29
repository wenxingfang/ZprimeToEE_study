import ROOT
import sys
import gc
ROOT.TH1.AddDirectory(ROOT.kFALSE)
ROOT.gROOT.SetBatch(ROOT.kTRUE)

def draw_plots(date, out_dir,h_mc,h_data,out_name):
    stat_style=1001
    stat_color=ROOT.kRed-10
    stat_sys_style=1001
    stat_sys_color=ROOT.TColor.GetColor("#b4ccdb")
    canvas = ROOT.TCanvas('canvas_%s'%(out_name),'',100,100,1000,1000)
    canvas.SetLeftMargin(0.13)
    canvas.SetBottomMargin(0.13)
    canvas.cd()
    h_mc.Scale(h_data.GetSumOfWeights()/h_mc.GetSumOfWeights())##### normalized
    ########### For XY Range #############
    nbin=1
    x_min=h_mc.GetXaxis().GetXmin()
    x_max=h_mc.GetXaxis().GetXmax()
    y_min=0
    y_max=1.5*h_mc.GetMaximum() if h_mc.GetMaximum() > h_data.GetMaximum() else 1.5*h_data.GetMaximum()
    dummy = ROOT.TH2D("dummy","",1,x_min,x_max,1,y_min,y_max)
    dummy.SetStats(ROOT.kFALSE)
    Y_title='Eevent / %.1f'%(h_mc.GetXaxis().GetBinWidth(1))
    dummy.GetYaxis().SetTitle(Y_title)
    dummy.GetYaxis().SetTitleSize(0.05)
    dummy.GetYaxis().SetLabelSize(0.045)
    dummy.GetYaxis().SetTitleOffset(1.3)
    dummy.GetXaxis().SetTitleOffset(1.5)
    dummy.GetXaxis().SetTitle(h_mc.GetTitle())
    dummy.GetXaxis().SetLabelSize(0.045)
    dummy.GetXaxis().SetMoreLogLabels()
    dummy.GetXaxis().SetNoExponent()  
    dummy.GetXaxis().SetNdivisions(405)
    dummy.Draw()
    h_mc.SetMarkerColor(ROOT.kBlack)
    h_mc.SetMarkerStyle(8)
    h_mc.SetLineColor(ROOT.kBlack)
    h_data.SetMarkerColor(ROOT.kRed)
    h_data.SetLineColor(ROOT.kRed)
    h_data.SetFillColor(ROOT.TColor.GetColor("#99ccff"))
    h_data.SetMarkerStyle(4)
    #h_mc.Draw("hist:same")
    #h_mc.Draw("same:e2")
    h_mc.Draw("pe:same")
    h_data.Draw("pe:same")
    dummy.Draw("AXISSAME")
    legend = ROOT.TLegend(0.15, 0.75, 0.5, 0.9, "", "brNDC")
    legend.AddEntry(h_data,"M > %d GeV"%(Threshold),'epl')
    legend.AddEntry(h_mc  ,"1 TeV < M < %d GeV (Normalized)"%(Threshold),'epl')
    legend.SetBorderSize(0)
    legend.SetLineColor(1)
    legend.SetLineStyle(1)
    legend.SetLineWidth(1)
    legend.SetFillColor(19)
    legend.SetFillStyle(0)
    legend.SetTextSize(0.03)  
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
    label_prelim = ROOT.TPaveLabel(0.69, 0.745, 0.96, 0.841, "Internal", "brNDC")
    label_prelim.SetBorderSize(0)
    label_prelim.SetFillColor(0)
    label_prelim.SetFillStyle(0)
    label_prelim.SetTextFont(51)
    label_prelim.SetTextSize(0.44/0.75 * 0.8)
    label_prelim.Draw()
    labels_region = ROOT.TPaveLabel(0.5, 0.812937, 0.7, 0.907343, "", "brNDC")
    labels_region.SetBorderSize(0)
    labels_region.SetFillColor(0)
    labels_region.SetFillStyle(0)
    labels_region.SetTextFont(font)
    labels_region.SetTextSize(0.4)  
    if "BB" in out_name:
        labels_region.SetLabel("Barrel-Barrel")
        labels_region.Draw()
    elif "BE" in out_name:
        labels_region.SetLabel("Barrel-Endcap")
        labels_region.Draw()
    elif "EE" in out_name:
        labels_region.SetLabel("Endcap-Endcap")
        labels_region.Draw()
    canvas.Print('%s/%s/%s.png'%(out_dir,date,out_name))    
    del canvas
    gc.collect()
#Run:324202,LS:24,Event:20605594,M:1940.16,e1_Et:997.303,e1_eta:-0.266343,e1_phi:-1.15491,e1_c:1,e2_Et:961.156,e2_eta:-0.444202,e2_phi:1.66154,e2_c:-1,e1_dPhi:0.000869393,e1_Sieie:0.00872854,e1_missHit:0,e1_dxy:0.00181819,e1_HoE:0.010766,e1_E1X5:0.498449,e1_E2X5:0.960616,e1_EMHD1:10.2466,e1_trkiso:0,e1_ECAL:1,e1_dEta:0.000846663,e2_dPhi,:0.00347102,e2_Sieie:0.00879558,e2_missHit:0,e2_dxy:0.00456125,e2_HoE:0.0145708,e2_E1X5:0.876984,e2_E2X5:0.951725,e2_EMHD1:12.0164,e2_trkiso:0,e2_ECAL:1,e2_dEta:0.00108933

f=open('TeV_2018_data.txt','r')
lines=f.readlines()
dicti={}
N=0
for line in lines:
    N=N+1
    dicti[str(N)]={}
    for item in line.split(','):
        dicti[str(N)][item.split(':')[0]]=float(item.split(':')[-1])
    region=""
    if abs(dicti[str(N)]['e1_sc_eta'])<1.4442 and abs(dicti[str(N)]['e2_sc_eta'])<1.4442:region="BB"
    elif (abs(dicti[str(N)]['e1_sc_eta'])<1.4442 and abs(dicti[str(N)]['e2_sc_eta'])>1.566) or (abs(dicti[str(N)]['e1_sc_eta'])>1.566 and abs(dicti[str(N)]['e2_sc_eta'])<1.4442):region="BE"
    else:region='EE'
    dicti[str(N)]['region']=region
#print dicti
s_dict=sorted(dicti.items(), key=lambda x:x[1]['M'], reverse=True)
#print s_dict
print "No. & Mass (GeV) & Run:LS:Event & Category & $E_{T}$ & $\eta$ & $\phi$ & dEta & dPhi & dxy & MissHit & H/E & EM+HD1 & trkiso & E1X5/E5/5 & E2X5/E5X5 & sigmaieie"
No=0
for i in s_dict:
    tmp_dict=i[1]
    if tmp_dict['region']=='EE':continue
    No=No+1
    print "%-3d & %-5.1f & %-6d:%-4d:%-15d & %-2s & %-5.1f,%-5.1f & %-4.3f,%-4.3f & %-4.3f,%-4.3f & %.2e,%.2e & %.2e,%.2e & %.2e,%.2e & %-1d,%-1d & %.2e,%.2e & %.2e,%.2e & %.1f,%.1f & %.2e,%.2e & %.2e,%.2e & %.2e,%.2e"%(No,tmp_dict['M'],tmp_dict['Run'],tmp_dict['LS'],tmp_dict['Event'],tmp_dict['region'],tmp_dict['e1_Et'],tmp_dict['e2_Et'],tmp_dict['e1_eta'],tmp_dict['e2_eta'],tmp_dict['e1_phi'],tmp_dict['e2_phi'],tmp_dict['e1_dEta'],tmp_dict['e2_dEta'],tmp_dict['e1_dPhi'],tmp_dict['e2_dPhi'],tmp_dict['e1_dxy'],tmp_dict['e2_dxy'],tmp_dict['e1_missHit'],tmp_dict['e2_missHit'],tmp_dict['e1_HoE'],tmp_dict['e2_HoE'],tmp_dict['e1_EMHD1'],tmp_dict['e2_EMHD1'],tmp_dict['e1_trkiso'],tmp_dict['e2_trkiso'],tmp_dict['e1_E1X5'],tmp_dict['e2_E1X5'],tmp_dict['e1_E2X5'],tmp_dict['e2_E2X5'],tmp_dict['e1_Sieie'],tmp_dict['e2_Sieie'])

sys.exit()

H_Low={}
H_High={}

H_Low['H_Led_Et']=ROOT.TH1D("H_Led_Et"     ,"E^{Leading}_{T} (GeV)"              ,20,0,2000)
H_Low['H_Led_Eta']=ROOT.TH1D("H_Led_Eta"    ,"#eta^{Leading}"                     ,12,-3,3)
H_Low['H_Led_Phi']=ROOT.TH1D("H_Led_Phi"    ,"#phi^{Leading}"                     ,10,-4,4)
H_Low['H_Led_Ch']=ROOT.TH1D("H_Led_Ch"     ,"Charge^{Leading}"                   ,20,-2,2)
H_Low['H_Led_Dphi']=ROOT.TH1D("H_Led_Dphi"   ,"#Delta#phi^{Leading}"               ,10,0,0.06)
H_Low['H_Led_Sieie']=ROOT.TH1D("H_Led_Sieie"  ,"#sigma_{i#eta i#eta}^{Leading}"     ,10,0,0.03)
H_Low['H_Led_MissHit']=ROOT.TH1D("H_Led_MissHit","MissingHit^{Leading}"               ,10,0,2)
H_Low['H_Led_Dxy']=ROOT.TH1D("H_Led_Dxy"    ,"d_{xy}^{Leading}"                   ,10,0,0.05)
H_Low['H_Led_HoE']=ROOT.TH1D("H_Led_HoE"    ,"(#frac{H}{E})^{Leading}"            ,10,0,0.2)
H_Low['H_Led_E15']=ROOT.TH1D("H_Led_E15"    ,"(#frac{E_{1X5}}{E_{5X5}})^{Leading}",10,0,1)
H_Low['H_Led_E25']=ROOT.TH1D("H_Led_E25"    ,"(#frac{E_{2X5}}{E_{5X5}})^{Leading}",20,0,1)
H_Low['H_Led_EMHD1']=ROOT.TH1D("H_Led_EMHD1"  ,"(EM+HD1)^{Leading}"                 ,10,0,10)
H_Low['H_Led_Trkiso']=ROOT.TH1D("H_Led_Trkiso" ,"TrackIso^{Leading}"                 ,10,0,5)
H_Low['H_Led_Deta']=ROOT.TH1D("H_Led_Deta"   ,"#Delta#eta^{Leading}"               ,10,0,0.006)
H_Low['H_Sub_Et']=ROOT.TH1D("H_Sub_Et"     ,"E^{Sub-leading}_{T} (GeV)"              ,20,0,2000)
H_Low['H_Sub_Eta']=ROOT.TH1D("H_Sub_Eta"    ,"#eta^{Sub-leading}"                     ,12,-3,3)
H_Low['H_Sub_Phi']=ROOT.TH1D("H_Sub_Phi"    ,"#phi^{Sub-leading}"                     ,10,-4,4)
H_Low['H_Sub_Ch']=ROOT.TH1D("H_Sub_Ch"     ,"Charge^{Sub-leading}"                   ,20,-2,2)
H_Low['H_Sub_Dphi']=ROOT.TH1D("H_Sub_Dphi"   ,"#Delta#phi^{Sub-leading}"               ,10,0,0.06)
H_Low['H_Sub_Sieie']=ROOT.TH1D("H_Sub_Sieie"  ,"#sigma_{i#eta i#eta}^{Sub-leading}"     ,10,0,0.03)
H_Low['H_Sub_MissHit']=ROOT.TH1D("H_Sub_MissHit","MissingHit^{Sub-leading}"               ,10,0,2)
H_Low['H_Sub_Dxy']=ROOT.TH1D("H_Sub_Dxy"    ,"d_{xy}^{Sub-leading}"                   ,10,0,0.05)
H_Low['H_Sub_HoE']=ROOT.TH1D("H_Sub_HoE"    ,"(#frac{H}{E})^{Sub-leading}"            ,10,0,0.2)
H_Low['H_Sub_E15']=ROOT.TH1D("H_Sub_E15"    ,"(#frac{E_{1X5}}{E_{5X5}})^{Sub-leading}",10,0,1)
H_Low['H_Sub_E25']=ROOT.TH1D("H_Sub_E25"    ,"(#frac{E_{2X5}}{E_{5X5}})^{Sub-leading}",20,0,1)
H_Low['H_Sub_EMHD1']=ROOT.TH1D("H_Sub_EMHD1"  ,"(EM+HD1)^{Sub-leading}"                 ,10,0,10)
H_Low['H_Sub_Trkiso']=ROOT.TH1D("H_Sub_Trkiso" ,"TrackIso^{Sub-leading}"                 ,10,0,5)
H_Low['H_Sub_Deta']=ROOT.TH1D("H_Sub_Deta"   ,"#Delta#eta^{Sub-leading}"               ,10,0,0.006)


H_High['H_Led_Et']=ROOT.TH1D("H_Led_Et"     ,"E^{Leading}_{T} (GeV)"              ,20,0,2000)
H_High['H_Led_Eta']=ROOT.TH1D("H_Led_Eta"    ,"#eta^{Leading}"                     ,12,-3,3)
H_High['H_Led_Phi']=ROOT.TH1D("H_Led_Phi"    ,"#phi^{Leading}"                     ,10,-4,4)
H_High['H_Led_Ch']=ROOT.TH1D("H_Led_Ch"     ,"Charge^{Leading}"                   ,20,-2,2)
H_High['H_Led_Dphi']=ROOT.TH1D("H_Led_Dphi"   ,"#Delta#phi^{Leading}"               ,10,0,0.06)
H_High['H_Led_Sieie']=ROOT.TH1D("H_Led_Sieie"  ,"#sigma_{i#eta i#eta}^{Leading}"     ,10,0,0.03)
H_High['H_Led_MissHit']=ROOT.TH1D("H_Led_MissHit","MissingHit^{Leading}"               ,10,0,2)
H_High['H_Led_Dxy']=ROOT.TH1D("H_Led_Dxy"    ,"d_{xy}^{Leading}"                   ,10,0,0.05)
H_High['H_Led_HoE']=ROOT.TH1D("H_Led_HoE"    ,"(#frac{H}{E})^{Leading}"            ,10,0,0.2)
H_High['H_Led_E15']=ROOT.TH1D("H_Led_E15"    ,"(#frac{E_{1X5}}{E_{5X5}})^{Leading}",10,0,1)
H_High['H_Led_E25']=ROOT.TH1D("H_Led_E25"    ,"(#frac{E_{2X5}}{E_{5X5}})^{Leading}",20,0,1)
H_High['H_Led_EMHD1']=ROOT.TH1D("H_Led_EMHD1"  ,"(EM+HD1)^{Leading}"                 ,10,0,10)
H_High['H_Led_Trkiso']=ROOT.TH1D("H_Led_Trkiso" ,"TrackIso^{Leading}"                 ,10,0,5)
H_High['H_Led_Deta']=ROOT.TH1D("H_Led_Deta"   ,"#Delta#eta^{Leading}"               ,10,0,0.006)
H_High['H_Sub_Et']=ROOT.TH1D("H_Sub_Et"     ,"E^{Sub-leading}_{T} (GeV)"              ,20,0,2000)
H_High['H_Sub_Eta']=ROOT.TH1D("H_Sub_Eta"    ,"#eta^{Sub-leading}"                     ,12,-3,3)
H_High['H_Sub_Phi']=ROOT.TH1D("H_Sub_Phi"    ,"#phi^{Sub-leading}"                     ,10,-4,4)
H_High['H_Sub_Ch']=ROOT.TH1D("H_Sub_Ch"     ,"Charge^{Sub-leading}"                   ,20,-2,2)
H_High['H_Sub_Dphi']=ROOT.TH1D("H_Sub_Dphi"   ,"#Delta#phi^{Sub-leading}"               ,10,0,0.06)
H_High['H_Sub_Sieie']=ROOT.TH1D("H_Sub_Sieie"  ,"#sigma_{i#eta i#eta}^{Sub-leading}"     ,10,0,0.03)
H_High['H_Sub_MissHit']=ROOT.TH1D("H_Sub_MissHit","MissingHit^{Sub-leading}"               ,10,0,2)
H_High['H_Sub_Dxy']=ROOT.TH1D("H_Sub_Dxy"    ,"d_{xy}^{Sub-leading}"                   ,10,0,0.05)
H_High['H_Sub_HoE']=ROOT.TH1D("H_Sub_HoE"    ,"(#frac{H}{E})^{Sub-leading}"            ,10,0,0.2)
H_High['H_Sub_E15']=ROOT.TH1D("H_Sub_E15"    ,"(#frac{E_{1X5}}{E_{5X5}})^{Sub-leading}",10,0,1)
H_High['H_Sub_E25']=ROOT.TH1D("H_Sub_E25"    ,"(#frac{E_{2X5}}{E_{5X5}})^{Sub-leading}",20,0,1)
H_High['H_Sub_EMHD1']=ROOT.TH1D("H_Sub_EMHD1"  ,"(EM+HD1)^{Sub-leading}"                 ,10,0,10)
H_High['H_Sub_Trkiso']=ROOT.TH1D("H_Sub_Trkiso" ,"TrackIso^{Sub-leading}"                 ,10,0,5)
H_High['H_Sub_Deta']=ROOT.TH1D("H_Sub_Deta"   ,"#Delta#eta^{Sub-leading}"               ,10,0,0.006)

date='20190629'
out_dir='plot_High_Mass_Check'
#Region="All"
Region="BE"

#Threshold=1500
Threshold=1800

for i in dicti:
    region=-1
    if abs(dicti[i]['e1_sc_eta'])<1.4442 and abs(dicti[i]['e2_sc_eta'])<1.4442:region=0
    elif (abs(dicti[i]['e1_sc_eta'])<1.4442 and abs(dicti[i]['e2_sc_eta'])>1.566) or (abs(dicti[i]['e1_sc_eta'])>1.566 and abs(dicti[i]['e2_sc_eta'])<1.4442):region=1
    else: region=2
    if Region=="BB"   and region!=0:continue##for BB
    elif Region=="BE" and region!=1:continue##for BE
    elif Region=="EE" and region!=2:continue##for EE

    if dicti[i]['M'] < Threshold:
        if dicti[i]['e1_Et'] > dicti[i]['e2_Et']:
            H_Low['H_Led_Et'].Fill(dicti[i]['e1_Et'])
            H_Low['H_Led_Eta'].Fill(dicti[i]['e1_eta'])
            H_Low['H_Led_Phi'].Fill(dicti[i]['e1_phi'])
            H_Low['H_Led_Ch'].Fill(dicti[i]['e1_c'])
            H_Low['H_Led_Dphi'].Fill(dicti[i]['e1_dPhi'])
            if abs(dicti[i]['e1_sc_eta'])>1.566: 
                H_Low['H_Led_Sieie'].Fill(dicti[i]['e1_Sieie'])
            H_Low['H_Led_MissHit'].Fill(dicti[i]['e1_missHit'])
            H_Low['H_Led_Dxy'].Fill(dicti[i]['e1_dxy'])
            H_Low['H_Led_HoE'].Fill(dicti[i]['e1_HoE'])
            if abs(dicti[i]['e1_sc_eta'])<1.4442:
                H_Low['H_Led_E15'].Fill(dicti[i]['e1_E1X5'])
                H_Low['H_Led_E25'].Fill(dicti[i]['e1_E2X5'])
            H_Low['H_Led_EMHD1'].Fill(dicti[i]['e1_EMHD1'])
            H_Low['H_Led_Trkiso'].Fill(dicti[i]['e1_trkiso'])
            H_Low['H_Led_Deta'].Fill(dicti[i]['e1_dEta'])
            H_Low['H_Sub_Et'].Fill(dicti[i]['e2_Et'])
            H_Low['H_Sub_Eta'].Fill(dicti[i]['e2_eta'])
            H_Low['H_Sub_Phi'].Fill(dicti[i]['e2_phi'])
            H_Low['H_Sub_Ch'].Fill(dicti[i]['e2_c'])
            H_Low['H_Sub_Dphi'].Fill(dicti[i]['e2_dPhi'])
            if abs(dicti[i]['e2_sc_eta'])>1.566: 
                H_Low['H_Sub_Sieie'].Fill(dicti[i]['e2_Sieie'])
            H_Low['H_Sub_MissHit'].Fill(dicti[i]['e2_missHit'])
            H_Low['H_Sub_Dxy'].Fill(dicti[i]['e2_dxy'])
            H_Low['H_Sub_HoE'].Fill(dicti[i]['e2_HoE'])
            if abs(dicti[i]['e2_sc_eta'])<1.4442:
                H_Low['H_Sub_E15'].Fill(dicti[i]['e2_E1X5'])
                H_Low['H_Sub_E25'].Fill(dicti[i]['e2_E2X5'])
            H_Low['H_Sub_EMHD1'].Fill(dicti[i]['e2_EMHD1'])
            H_Low['H_Sub_Trkiso'].Fill(dicti[i]['e2_trkiso'])
            H_Low['H_Sub_Deta'].Fill(dicti[i]['e2_dEta'])
        else:
            H_Low['H_Led_Et'].Fill(dicti[i]['e2_Et'])
            H_Low['H_Led_Eta'].Fill(dicti[i]['e2_eta'])
            H_Low['H_Led_Phi'].Fill(dicti[i]['e2_phi'])
            H_Low['H_Led_Ch'].Fill(dicti[i]['e2_c'])
            H_Low['H_Led_Dphi'].Fill(dicti[i]['e2_dPhi'])
            if abs(dicti[i]['e2_sc_eta'])>1.566: 
                H_Low['H_Led_Sieie'].Fill(dicti[i]['e2_Sieie'])
            H_Low['H_Led_MissHit'].Fill(dicti[i]['e2_missHit'])
            H_Low['H_Led_Dxy'].Fill(dicti[i]['e2_dxy'])
            H_Low['H_Led_HoE'].Fill(dicti[i]['e2_HoE'])
            if abs(dicti[i]['e2_sc_eta'])<1.4442:
                H_Low['H_Led_E15'].Fill(dicti[i]['e2_E1X5'])
                H_Low['H_Led_E25'].Fill(dicti[i]['e2_E2X5'])
            H_Low['H_Led_EMHD1'].Fill(dicti[i]['e2_EMHD1'])
            H_Low['H_Led_Trkiso'].Fill(dicti[i]['e2_trkiso'])
            H_Low['H_Led_Deta'].Fill(dicti[i]['e2_dEta'])
            H_Low['H_Sub_Et'].Fill(dicti[i]['e1_Et'])
            H_Low['H_Sub_Eta'].Fill(dicti[i]['e1_eta'])
            H_Low['H_Sub_Phi'].Fill(dicti[i]['e1_phi'])
            H_Low['H_Sub_Ch'].Fill(dicti[i]['e1_c'])
            H_Low['H_Sub_Dphi'].Fill(dicti[i]['e1_dPhi'])
            if abs(dicti[i]['e1_sc_eta'])>1.566: 
                H_Low['H_Sub_Sieie'].Fill(dicti[i]['e1_Sieie'])
            H_Low['H_Sub_MissHit'].Fill(dicti[i]['e1_missHit'])
            H_Low['H_Sub_Dxy'].Fill(dicti[i]['e1_dxy'])
            H_Low['H_Sub_HoE'].Fill(dicti[i]['e1_HoE'])
            if abs(dicti[i]['e1_sc_eta'])<1.4442: 
                H_Low['H_Sub_E15'].Fill(dicti[i]['e1_E1X5'])
                H_Low['H_Sub_E25'].Fill(dicti[i]['e1_E2X5'])
            H_Low['H_Sub_EMHD1'].Fill(dicti[i]['e1_EMHD1'])
            H_Low['H_Sub_Trkiso'].Fill(dicti[i]['e1_trkiso'])
            H_Low['H_Sub_Deta'].Fill(dicti[i]['e1_dEta'])

    else:
        print "M:%f,e1_eta:%f,e2_eta:%f"%(dicti[i]['M'],dicti[i]['e1_eta'],dicti[i]['e2_eta'])
        if dicti[i]['e1_Et'] > dicti[i]['e2_Et']:
            H_High['H_Led_Et'].Fill(dicti[i]['e1_Et'])
            H_High['H_Led_Eta'].Fill(dicti[i]['e1_eta'])
            H_High['H_Led_Phi'].Fill(dicti[i]['e1_phi'])
            H_High['H_Led_Ch'].Fill(dicti[i]['e1_c'])
            H_High['H_Led_Dphi'].Fill(dicti[i]['e1_dPhi'])
            if abs(dicti[i]['e1_sc_eta'])>1.566: 
                H_High['H_Led_Sieie'].Fill(dicti[i]['e1_Sieie'])
            H_High['H_Led_MissHit'].Fill(dicti[i]['e1_missHit'])
            H_High['H_Led_Dxy'].Fill(dicti[i]['e1_dxy'])
            H_High['H_Led_HoE'].Fill(dicti[i]['e1_HoE'])
            if abs(dicti[i]['e1_sc_eta'])<1.4442:
                H_High['H_Led_E15'].Fill(dicti[i]['e1_E1X5'])
                H_High['H_Led_E25'].Fill(dicti[i]['e1_E2X5'])
            H_High['H_Led_EMHD1'].Fill(dicti[i]['e1_EMHD1'])
            H_High['H_Led_Trkiso'].Fill(dicti[i]['e1_trkiso'])
            H_High['H_Led_Deta'].Fill(dicti[i]['e1_dEta'])
            H_High['H_Sub_Et'].Fill(dicti[i]['e2_Et'])
            H_High['H_Sub_Eta'].Fill(dicti[i]['e2_eta'])
            H_High['H_Sub_Phi'].Fill(dicti[i]['e2_phi'])
            H_High['H_Sub_Ch'].Fill(dicti[i]['e2_c'])
            H_High['H_Sub_Dphi'].Fill(dicti[i]['e2_dPhi'])
            if abs(dicti[i]['e2_sc_eta'])>1.566: 
                H_High['H_Sub_Sieie'].Fill(dicti[i]['e2_Sieie'])
            H_High['H_Sub_MissHit'].Fill(dicti[i]['e2_missHit'])
            H_High['H_Sub_Dxy'].Fill(dicti[i]['e2_dxy'])
            H_High['H_Sub_HoE'].Fill(dicti[i]['e2_HoE'])
            if abs(dicti[i]['e2_sc_eta'])<1.4442:
                H_High['H_Sub_E15'].Fill(dicti[i]['e2_E1X5'])
                H_High['H_Sub_E25'].Fill(dicti[i]['e2_E2X5'])
            H_High['H_Sub_EMHD1'].Fill(dicti[i]['e2_EMHD1'])
            H_High['H_Sub_Trkiso'].Fill(dicti[i]['e2_trkiso'])
            H_High['H_Sub_Deta'].Fill(dicti[i]['e2_dEta'])
        else:
            H_High['H_Led_Et'].Fill(dicti[i]['e2_Et'])
            H_High['H_Led_Eta'].Fill(dicti[i]['e2_eta'])
            H_High['H_Led_Phi'].Fill(dicti[i]['e2_phi'])
            H_High['H_Led_Ch'].Fill(dicti[i]['e2_c'])
            H_High['H_Led_Dphi'].Fill(dicti[i]['e2_dPhi'])
            if abs(dicti[i]['e2_sc_eta'])>1.566: 
                H_High['H_Led_Sieie'].Fill(dicti[i]['e2_Sieie'])
            H_High['H_Led_MissHit'].Fill(dicti[i]['e2_missHit'])
            H_High['H_Led_Dxy'].Fill(dicti[i]['e2_dxy'])
            H_High['H_Led_HoE'].Fill(dicti[i]['e2_HoE'])
            if abs(dicti[i]['e2_sc_eta'])<1.4442:
                H_High['H_Led_E15'].Fill(dicti[i]['e2_E1X5'])
                H_High['H_Led_E25'].Fill(dicti[i]['e2_E2X5'])
            H_High['H_Led_EMHD1'].Fill(dicti[i]['e2_EMHD1'])
            H_High['H_Led_Trkiso'].Fill(dicti[i]['e2_trkiso'])
            H_High['H_Led_Deta'].Fill(dicti[i]['e2_dEta'])
            H_High['H_Sub_Et'].Fill(dicti[i]['e1_Et'])
            H_High['H_Sub_Eta'].Fill(dicti[i]['e1_eta'])
            H_High['H_Sub_Phi'].Fill(dicti[i]['e1_phi'])
            H_High['H_Sub_Ch'].Fill(dicti[i]['e1_c'])
            H_High['H_Sub_Dphi'].Fill(dicti[i]['e1_dPhi'])
            if abs(dicti[i]['e1_sc_eta'])>1.566: 
                H_High['H_Sub_Sieie'].Fill(dicti[i]['e1_Sieie'])
            H_High['H_Sub_MissHit'].Fill(dicti[i]['e1_missHit'])
            H_High['H_Sub_Dxy'].Fill(dicti[i]['e1_dxy'])
            H_High['H_Sub_HoE'].Fill(dicti[i]['e1_HoE'])
            if abs(dicti[i]['e1_sc_eta'])<1.4442: 
                H_High['H_Sub_E15'].Fill(dicti[i]['e1_E1X5'])
                H_High['H_Sub_E25'].Fill(dicti[i]['e1_E2X5'])
            H_High['H_Sub_EMHD1'].Fill(dicti[i]['e1_EMHD1'])
            H_High['H_Sub_Trkiso'].Fill(dicti[i]['e1_trkiso'])
            H_High['H_Sub_Deta'].Fill(dicti[i]['e1_dEta'])

for hist in H_Low:
    draw_plots(date, out_dir,H_Low[hist],H_High[hist],hist+"_"+Region)
