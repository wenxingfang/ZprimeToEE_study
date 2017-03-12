void fill_all_histograms_simple(){
  fill_histograms_simple fh ;
  
  bool do_data = false;
  bool do_MC   = true;
  
  if(do_data){

    
    TChain* ch_json = new TChain("tap") ;
    ch_json->Add("/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/Data_out_perone/RunB.root") ;
    ch_json->Add("/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/Data_out_perone/RunC.root") ;
    ch_json->Add("/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/Data_out_perone/RunD.root") ;
    ch_json->Add("/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/Data_out_perone/RunE.root") ;
    ch_json->Add("/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/Data_out_perone/RunF.root") ;
    fh.Init(ch_json) ;
    fh.Loop("data_RunBCDEF") ;


  }
  
  if(do_MC){

//    TFile f_DYToEE  ("ntuples/reskim/RunE/DYToEE_powheg_M_50_RunE.root") ;
//    TFile f_ZToTT  ("ntuples/reskim/RunE/ZToTT_mad_RunE.root") ;
//    TFile f_WJets_mad("ntuples/reskim/RunE/WJet_mad_RunE.root") ;
//    TFile f_WZ     ("ntuples/reskim/RunE/WZ_RunE.root") ;
//    TFile f_WW     ("ntuples/reskim/RunE/WW_RunE.root") ;
//    TFile f_ZZ     ("ntuples/reskim/RunE/ZZ_RunE.root") ;
//    TFile f_TT     ("ntuples/reskim/RunE/TTbar_RunE.root") ;
//    TFile f_ST     ("ntuples/reskim/RunE/ST_RunE.root") ;
//    TFile f_ST_anti("ntuples/reskim/RunE/ST_anti_RunE.root") ;
//    TFile f_GamJet_1("ntuples/reskim/RunE/GJ_40_100_RunE.root") ;
//    TFile f_GamJet_2("ntuples/reskim/RunE/GJ_100_200_RunE.root") ;
//    TFile f_GamJet_3("ntuples/reskim/RunE/GJ_200_400_RunE.root") ;
//    TFile f_GamJet_4("ntuples/reskim/RunE/GJ_400_600_RunE.root") ;
//    TFile f_GamJet_5("ntuples/reskim/RunE/GJ_600_Inf_RunE.root") ;
    
//    TTree* t_DYToEE     = (TTree*) f_DYToEE.Get("tap") ;
//    TTree* t_ZToTT     = (TTree*) f_ZToTT.Get("tap") ;
//    TTree* t_WJets_mad = (TTree*) f_WJets_mad.Get("tap") ;
//    TTree* t_WW        = (TTree*) f_WW   .Get("tap") ;
//    TTree* t_WZ        = (TTree*) f_WZ   .Get("tap") ;
//    TTree* t_ZZ        = (TTree*) f_ZZ   .Get("tap") ;
//    TTree* t_TT        = (TTree*) f_TT   .Get("tap") ;
//    TTree* t_ST        = (TTree*) f_ST   .Get("tap") ;
//    TTree* t_ST_anti   = (TTree*) f_ST_anti.Get("tap") ;
//    TTree* t_GamJet_1  = (TTree*) f_GamJet_1.Get("tap") ;
//    TTree* t_GamJet_2  = (TTree*) f_GamJet_2.Get("tap") ;
//    TTree* t_GamJet_3  = (TTree*) f_GamJet_3.Get("tap") ;
//    TTree* t_GamJet_4  = (TTree*) f_GamJet_4.Get("tap") ;
//    TTree* t_GamJet_5  = (TTree*) f_GamJet_5.Get("tap") ;
//
//    fh.Init(t_DYToEE) ; fh.Loop("DYToEE_powheg_50_RunE") ;
//    fh.Init(t_ZToTT) ; fh.Loop("ZToTT_mad_RunE") ;
//    fh.Init(t_WJets_mad) ; fh.Loop("WJets_mad_RunE") ;
//    fh.Init(t_WW   ) ; fh.Loop("WW_RunE") ;
//    fh.Init(t_WZ   ) ; fh.Loop("WZ_RunE") ;
//    fh.Init(t_ZZ   ) ; fh.Loop("ZZ_RunE") ;
//    fh.Init(t_TT   ) ; fh.Loop("ttbar_RunE") ;
//    fh.Init(t_ST)    ; fh.Loop("ST_RunE") ;
//    fh.Init(t_ST_anti) ; fh.Loop("ST_anti_RunE") ;
//    fh.Init(t_GamJet_1 ) ; fh.Loop("GamJet_40_100_RunE") ;
//    fh.Init(t_GamJet_2 ) ; fh.Loop("GamJet_100_200_RunE") ;
//    fh.Init(t_GamJet_3 ) ; fh.Loop("GamJet_200_400_RunE") ;
//    fh.Init(t_GamJet_4 ) ; fh.Loop("GamJet_400_600_RunE") ;
//    fh.Init(t_GamJet_5 ) ; fh.Loop("GamJet_600_Inf_RunE") ;

    TChain* test = new TChain("tap") ;
    test->Add("/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/reskim_script/reskim_out/MC_out/MiniAOD/GJ_600ToInf*.root") ;
    fh.Init(test) ;
    fh.Loop("GJ_test") ;
  }
}

