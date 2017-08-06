import ROOT

#Dir="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/ntuples/saved_hist/Step1_0725_PDF_uncluster/"
#Dir="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/ntuples/saved_hist/Step1_0725_PDF_uncluster_NoNvtex/"
#Dir="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/ntuples/saved_hist/Step1_0726_PDF_uncluster_Nvtex/"
#Dir="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/ntuples/saved_hist/Step2_0726_PDF_uncluster/"
#Dir="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/ntuples/saved_hist/Step2_SameSign_0726_PDF_uncluster/"
#Dir="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/ntuples/saved_hist/Step1_0729_Nvtx_25_30/"
#Dir="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/ntuples/saved_hist/Step1_0729_noPU/"
#Dir="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/ntuples/saved_hist/Step1_0731_noPU_reNvtx/"
#Dir="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/ntuples/saved_hist/Step2_0801/"
#Dir="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/ntuples/saved_hist/Step2_SameSign_0801/"
#Dir="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/ntuples/saved_hist/Step2_0803/"
#Dir="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/ntuples/saved_hist/Step2_SameSign_0803/"
#Dir="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/ntuples/saved_hist/Step2_0805/"
Dir="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/ntuples/saved_hist/Step2_SameSign_0805/"
#channel="ee"
#channel="emu"
channel="mumu"
if channel == "ee":
    F_1=ROOT.TFile(Dir+"ee_nominal_.root","UPDATE")
    F_2=ROOT.TFile(Dir+"ee_nominal_singleEle.root","READ")
    for ih in range(0,F_2.GetListOfKeys().GetSize()):
        hname=F_2.GetListOfKeys()[ih].GetName()
        print hname
        hist_1=F_1.Get(hname)
        print hist_1.GetSumOfWeights()
        hist_2=F_2.Get(hname)
        hist_1.Add(hist_2,1)
        print hist_1.GetSumOfWeights()
        F_1.cd()
        hist_1.Write("",ROOT.TObject.kOverwrite)
    print "done"

elif channel == "mumu":
    F_1=ROOT.TFile(Dir+"mumu_nominal_.root","UPDATE")
    F_2=ROOT.TFile(Dir+"mumu_nominal_singleMuon.root","READ")
    for ih in range(0,F_2.GetListOfKeys().GetSize()):
        hname=F_2.GetListOfKeys()[ih].GetName()
        print hname
        hist_1=F_1.Get(hname)
        print hist_1.GetSumOfWeights()
        hist_2=F_2.Get(hname)
        hist_1.Add(hist_2,1)
        print hist_1.GetSumOfWeights()
        F_1.cd()
        hist_1.Write("",ROOT.TObject.kOverwrite)
    print "done"

elif channel == "emu":
    F_1=ROOT.TFile(Dir+"emu_nominal_.root","UPDATE")
    F_2=ROOT.TFile(Dir+"emu_nominal_singleMuon.root","READ")
    F_3=ROOT.TFile(Dir+"emu_nominal_singleEle.root","READ")
    for ih in range(0,F_2.GetListOfKeys().GetSize()):
        hname=F_2.GetListOfKeys()[ih].GetName()
        print hname
        hist_1=F_1.Get(hname)
        print hist_1.GetSumOfWeights()
        hist_2=F_2.Get(hname)
        hist_3=F_3.Get(hname)
        hist_1.Add(hist_2,1)
        hist_1.Add(hist_3,1)
        print hist_1.GetSumOfWeights()
        F_1.cd()
        hist_1.Write("",ROOT.TObject.kOverwrite)
    print "done"
