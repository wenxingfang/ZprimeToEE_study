void reskim_all_FR_1F(){
  
  bool do_data = true ;
  bool do_MC   = false;
  
  if(do_data){
/*
    TChain *ch_data_1 =new TChain("IIHEAnalysis");
    ifstream fin_1("/user/wenxing/run_data/CMSSW_8_0_7_patch1/src/UserCode/IIHETree/test/split_file/file_Ele33_v3_1.txt");  
    string s_1;  
    while( getline(fin_1,s_1) )
    {   
        ch_data_1->Add(TString(s_1));
    }
    cout << "Add file finish: " << endl; 
    reskim_FR_1F reskim_data_1(ch_data_1, true, false, false, false, 3, 273158, 274442) ;
    reskim_data_1.Loop("ntuples/reskim/data_12p39fb_v3_1_1F.root") ;

    TChain *ch_data_2 =new TChain("IIHEAnalysis");
    ifstream fin_2("/user/wenxing/run_data/CMSSW_8_0_7_patch1/src/UserCode/IIHETree/test/split_file/file_Ele33_v3_2.txt");  
    string s_2;  
    while( getline(fin_2,s_2) )
    {   
        ch_data_2->Add(TString(s_2));
    }
    cout << "Add file finish: " << endl; 
    reskim_FR_1F reskim_data_2(ch_data_2, true, false, false, false, 3, 273158, 274442) ;
    reskim_data_2.Loop("ntuples/reskim/data_12p39fb_v3_2_1F.root") ;

    TChain *ch_data_3 =new TChain("IIHEAnalysis");
    ifstream fin_3("/user/wenxing/run_data/CMSSW_8_0_7_patch1/src/UserCode/IIHETree/test/split_file/file_Ele33_v4.txt");  
    string s_3;  
    while( getline(fin_3,s_3) )
    {   
        ch_data_3->Add(TString(s_3));
    }
    cout << "Add file finish: " << endl; 
    reskim_FR_1F reskim_data_3(ch_data_3, true, false, false, false, 4, 274954, 275066) ;
    reskim_data_3.Loop("ntuples/reskim/data_12p39fb_v4_1F.root") ;

    TChain *ch_data_4 =new TChain("IIHEAnalysis");
    ifstream fin_4("/user/wenxing/run_data/CMSSW_8_0_7_patch1/src/UserCode/IIHETree/test/split_file/file_Ele33_v5.txt");  
    string s_4;  
    while( getline(fin_4,s_4) )
    {   
        ch_data_4->Add(TString(s_4));
    }
    cout << "Add file finish: " << endl; 
    reskim_FR_1F reskim_data_4(ch_data_4, true, false, false, false, 5, 275067, 275311) ;
    reskim_data_4.Loop("ntuples/reskim/data_12p39fb_v5_1F.root") ;

    TChain *ch_data_5 =new TChain("IIHEAnalysis");
    ifstream fin_5("/user/wenxing/run_data/CMSSW_8_0_7_patch1/src/UserCode/IIHETree/test/split_file/file_Ele33_v6_1.txt");  
    string s_5;  
    while( getline(fin_5,s_5) )
    {   
        ch_data_5->Add(TString(s_5));
    }
    cout << "Add file finish: " << endl; 
    reskim_FR_1F reskim_data_5(ch_data_5, true, false, false, false, 6, 275319, 276811) ;
    reskim_data_5.Loop("ntuples/reskim/data_12p39fb_v6_1_1F.root") ;

    TChain *ch_data_6 =new TChain("IIHEAnalysis");
    ifstream fin_6("/user/wenxing/run_data/CMSSW_8_0_7_patch1/src/UserCode/IIHETree/test/split_file/file_Ele33_v6_2.txt");  
    string s_6;  
    while( getline(fin_6,s_6) )
    {   
        ch_data_6->Add(TString(s_6));
    }
    cout << "Add file finish: " << endl; 
    reskim_FR_1F reskim_data_6(ch_data_6, true, false, false, false, 6, 275319, 276811) ;
    reskim_data_6.Loop("ntuples/reskim/data_12p39fb_v6_2_1F.root") ;

    TChain *ch_data_7 =new TChain("IIHEAnalysis");
    ifstream fin_7("/user/wenxing/run_data/CMSSW_8_0_7_patch1/src/UserCode/IIHETree/test/split_file/file_Ele33_v6_3.txt");  
    string s_7;  
    while( getline(fin_7,s_7) )
    {   
        ch_data_7->Add(TString(s_7));
    }
    cout << "Add file finish: " << endl; 
    reskim_FR_1F reskim_data_7(ch_data_7, true, false, false, false, 6, 275319, 276811) ;
    reskim_data_7.Loop("ntuples/reskim/data_12p39fb_v6_3_1F.root") ;
*/

//--------------------------- RunE ------------------------------------
    TChain *ch_data_8 =new TChain("IIHEAnalysis");
    ifstream fin_8("/user/wenxing/run_data/CMSSW_8_0_7_patch1/src/UserCode/IIHETree/test/split_file/file_Ele33_v6_RunE.txt");  
    string s_8;  
    while( getline(fin_8,s_8) )
    {   
        ch_data_8->Add(TString(s_8));
    }
    cout << "Add file finish: " << endl; 
    reskim_FR_1F reskim_data_8(ch_data_8, true, false, false, false, 6, 276830, 276834) ;
    reskim_data_8.Loop("ntuples/reskim/RunE/data_RunE_v6_1F.root") ;

    TChain *ch_data_9 =new TChain("IIHEAnalysis");
    ifstream fin_9("/user/wenxing/run_data/CMSSW_8_0_7_patch1/src/UserCode/IIHETree/test/split_file/file_Ele33_v7_RunE.txt");  
    string s_9;  
    while( getline(fin_9,s_9) )
    {   
        ch_data_9->Add(TString(s_9));
    }
    cout << "Add file finish: " << endl; 
    reskim_FR_1F reskim_data_9(ch_data_9, true, false, false, false, 7, 276870, 277420) ;
    reskim_data_9.Loop("ntuples/reskim/RunE/data_RunE_v7_1F.root") ;

//--------------------------- RunF ------------------------------------
/*
    TChain *ch_data_F_1 =new TChain("IIHEAnalysis");
    ifstream fin_F_1("/user/wenxing/run_data/CMSSW_8_0_7_patch1/src/UserCode/IIHETree/test/split_file/file_Ele33_v7_RunF.txt");  
    string s_F_1;  
    while( getline(fin_F_1,s_F_1) )
    {   
        ch_data_F_1->Add(TString(s_F_1));
    }
    cout << "Add file finish: " << endl; 
    reskim_FR_1F reskim_data_F_1(ch_data_F_1, true, false, false, false, 7, 277820, 278240) ;
    reskim_data_F_1.Loop("ntuples/reskim/RunF/data_RunF_v7_1F.root") ;

    TChain *ch_data_F_2 =new TChain("IIHEAnalysis");
    ifstream fin_F_2("/user/wenxing/run_data/CMSSW_8_0_7_patch1/src/UserCode/IIHETree/test/split_file/file_Ele33_v8_RunF.txt");  
    string s_F_2;  
    while( getline(fin_F_2,s_F_2) )
    {   
        ch_data_F_2->Add(TString(s_F_2));
    }
    cout << "Add file finish: " << endl; 
    reskim_FR_1F reskim_data_F_2(ch_data_F_2, true, false, false, false, 8, 278273, 278808) ;
    reskim_data_F_2.Loop("ntuples/reskim/RunF/data_RunF_v8_1F.root") ;
*/
//---------------------------- RunG ---------------------------------------

//    TChain *ch_data_G =new TChain("IIHEAnalysis");
//    ch_data_G->Add("/pnfs/iihe/cms/store/user/rgoldouz/SkimmedData/Golden_2016_postICHEP/DoubleEG_Run2016G_PromptReco_v1_AOD/*.root");
//    cout << "Add file finish: " << endl; 
//    reskim_FR_1F reskim_data_G(ch_data_G, true, false, false, false, 9, 1, 1000000) ;
//    reskim_data_G.Loop("ntuples/reskim/RunG/data_RunG_Ele33MW_1F.root") ;

}
  
  
  if(do_MC){
    TChain* ch_ZToEE_1 = new TChain("IIHEAnalysis") ;
    TChain* ch_ZToEE_2 = new TChain("IIHEAnalysis") ;
    TChain* ch_ZToEE_3 = new TChain("IIHEAnalysis") ;
    TChain* ch_ZToEE_4 = new TChain("IIHEAnalysis") ;
    TChain* ch_ZToEE_5 = new TChain("IIHEAnalysis") ;
    TChain* ch_ZToEE_6 = new TChain("IIHEAnalysis") ;
    TChain* ch_ZToEE_7 = new TChain("IIHEAnalysis") ;
    TChain* ch_ZToEE_8 = new TChain("IIHEAnalysis") ;
    TChain* ch_ZToEE_9 = new TChain("IIHEAnalysis") ;
    TChain* ch_ZToEE_10 = new TChain("IIHEAnalysis") ;
    TChain* ch_DY_1 = new TChain("IIHEAnalysis") ;
    TChain* ch_DY_2 = new TChain("IIHEAnalysis") ;
    TChain* ch_DY_3 = new TChain("IIHEAnalysis") ;
    TChain* ch_DY_amc_1 = new TChain("IIHEAnalysis") ;
    TChain* ch_DY_amc_2 = new TChain("IIHEAnalysis") ;
    TChain* ch_DYToEE_1 = new TChain("IIHEAnalysis") ;
    TChain* ch_DYToEE_2 = new TChain("IIHEAnalysis") ;
    TChain* ch_DYToEE_3 = new TChain("IIHEAnalysis") ;
    TChain* ch_WJet_mad_1 = new TChain("IIHEAnalysis") ;
    TChain* ch_WJet_mad_2 = new TChain("IIHEAnalysis") ;
    TChain* ch_WZ = new TChain("IIHEAnalysis") ;
    TChain* ch_ZZ = new TChain("IIHEAnalysis") ;
    TChain* ch_ST = new TChain("IIHEAnalysis") ;
    TChain* ch_ST_anti = new TChain("IIHEAnalysis") ;
    TChain* ch_GJ_1 = new TChain("IIHEAnalysis") ;
    TChain* ch_GJ_2 = new TChain("IIHEAnalysis") ;
    TChain* ch_GJ_3 = new TChain("IIHEAnalysis") ;
    TChain* ch_GJ_4 = new TChain("IIHEAnalysis") ;
    TChain* ch_GJ_5 = new TChain("IIHEAnalysis") ;
    TChain* ch_TT2L_1 = new TChain("IIHEAnalysis") ;
    TChain* ch_TT2L_2 = new TChain("IIHEAnalysis") ;
    TChain* ch_TT2L_3 = new TChain("IIHEAnalysis") ;
    TChain* ch_TT2L_4 = new TChain("IIHEAnalysis") ;
    TChain* ch_TT2L_5 = new TChain("IIHEAnalysis") ;
    TChain* ch_TT2L_6 = new TChain("IIHEAnalysis") ;
    TChain* ch_TT2L_7 = new TChain("IIHEAnalysis") ;
    TChain* ch_TT2L_8 = new TChain("IIHEAnalysis") ;
    TChain* ch_WW2L_1 = new TChain("IIHEAnalysis") ;
    TChain* ch_WW2L_2 = new TChain("IIHEAnalysis") ;
    TChain* ch_WW2L_3 = new TChain("IIHEAnalysis") ;
    TChain* ch_WW2L_4 = new TChain("IIHEAnalysis") ;
    TChain* ch_WW2L_5 = new TChain("IIHEAnalysis") ;
    
    ch_ZToEE_1->Add( "/pnfs/iihe/cms/store/user/rgoldouz/RunIISpring16DR80/ZToEE_NNPDF30_13TeV-powheg_M_50_120/crab_ZToEE_NNPDF30_13TeV-powheg_M_50_120/160731_213921/0000/*.root") ;
    ch_ZToEE_2->Add( "/pnfs/iihe/cms/store/user/rgoldouz/RunIISpring16DR80/ZToEE_NNPDF30_13TeV-powheg_M_120_200/crab_ZToEE_NNPDF30_13TeV-powheg_M_120_200/160731_213950/0000/*.root") ;
    ch_ZToEE_3->Add( "/pnfs/iihe/cms/store/user/rgoldouz/RunIISpring16DR80/ZToEE_NNPDF30_13TeV-powheg_M_200_400/crab_ZToEE_NNPDF30_13TeV-powheg_M_200_400/160731_214014/0000/*.root") ;
    ch_ZToEE_4->Add( "/pnfs/iihe/cms/store/user/rgoldouz/RunIISpring16DR80/ZToEE_NNPDF30_13TeV-powheg_M_400_800/crab_ZToEE_NNPDF30_13TeV-powheg_M_400_800/160731_214041/0000/*.root") ;
    ch_ZToEE_5->Add( "/pnfs/iihe/cms/store/user/rgoldouz/RunIISpring16DR80/ZToEE_NNPDF30_13TeV-powheg_M_800_1400/crab_ZToEE_NNPDF30_13TeV-powheg_M_800_1400/160731_214118/0000/*.root") ;
    ch_ZToEE_6->Add( "/pnfs/iihe/cms/store/user/rgoldouz/RunIISpring16DR80/ZToEE_NNPDF30_13TeV-powheg_M_1400_2300/crab_ZToEE_NNPDF30_13TeV-powheg_M_1400_2300/160731_214156/0000/*.root") ;
    ch_ZToEE_7->Add( "/pnfs/iihe/cms/store/user/rgoldouz/RunIISpring16DR80/ZToEE_NNPDF30_13TeV-powheg_M_2300_3500/crab_ZToEE_NNPDF30_13TeV-powheg_M_2300_3500/160731_214342/0000/*.root") ;
    ch_ZToEE_8->Add( "/pnfs/iihe/cms/store/user/rgoldouz/RunIISpring16DR80/ZToEE_NNPDF30_13TeV-powheg_M_3500_4500/crab_ZToEE_NNPDF30_13TeV-powheg_M_3500_4500/160731_214413/0000/*.root") ;
    ch_ZToEE_9->Add( "/pnfs/iihe/cms/store/user/rgoldouz/RunIISpring16DR80/ZToEE_NNPDF30_13TeV-powheg_M_4500_6000/crab_ZToEE_NNPDF30_13TeV-powheg_M_4500_6000/160731_214504/0000/*.root") ;
    ch_ZToEE_10->Add("/pnfs/iihe/cms/store/user/rgoldouz/RunIISpring16DR80/ZToEE_NNPDF30_13TeV-powheg_M_6000_Inf/crab_ZToEE_NNPDF30_13TeV-powheg_M_6000_Inf/160731_214530/0000/*.root") ;
    
    ch_DY_1->Add("/pnfs/iihe/cms/store/user/rgoldouz/RunIISpring16DR80/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1/160712_190218/0000/*.root") ;
    ch_DY_2->Add("/pnfs/iihe/cms/store/user/rgoldouz/RunIISpring16DR80/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1/160712_190218/0001/*.root") ;
    ch_DY_3->Add("/pnfs/iihe/cms/store/user/rgoldouz/RunIISpring16DR80/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext1/160712_190218/0002/*.root") ;

    ch_DY_amc_1->Add("/pnfs/iihe/cms/store/user/rgoldouz/RunIISpring16DR80/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/160712_190253/0000/*.root") ;
    ch_DY_amc_2->Add("/pnfs/iihe/cms/store/user/rgoldouz/RunIISpring16DR80/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/160712_190253/0001/*.root") ;
   
    ch_DYToEE_1->Add("/pnfs/iihe/cms/store/user/rgoldouz/RunIISpring16DR80/DYToEE_NNPDF30_13TeV-powheg-pythia8/crab_DYToEE_NNPDF30_13TeV-powheg-pythia8/160712_190134/0000/*.root") ;
    ch_DYToEE_2->Add("/pnfs/iihe/cms/store/user/rgoldouz/RunIISpring16DR80/DYToEE_NNPDF30_13TeV-powheg-pythia8/crab_DYToEE_NNPDF30_13TeV-powheg-pythia8/160712_190134/0001/*.root") ;
    ch_DYToEE_3->Add("/pnfs/iihe/cms/store/user/rgoldouz/RunIISpring16DR80/DYToEE_NNPDF30_13TeV-powheg-pythia8/crab_DYToEE_NNPDF30_13TeV-powheg-pythia8/160712_190134/0002/*.root") ;
    
    ch_WJet_mad_1->Add("/pnfs/iihe/cms/store/user/wenxing/RunIISpring16DR80/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM/160712_203514/0000/*.root") ;
    ch_WJet_mad_2->Add("/pnfs/iihe/cms/store/user/wenxing/RunIISpring16DR80/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM/160712_203514/0001/*.root") ;

    ch_WZ->Add("/pnfs/iihe/cms/store/user/xgao/RunIISpring16DR80/WZ_TuneCUETP8M1_13TeV-pythia8/*.root") ;
    ch_ZZ->Add("/pnfs/iihe/cms/store/user/xgao/RunIISpring16DR80/ZZ_TuneCUETP8M1_13TeV-pythia8/*.root") ;

    ch_ST->Add("/pnfs/iihe/cms/store/user/wenxing/RunIISpring16DR80/ST_tW_top_5f_inclusiveDecays-powheg/160712_203406/0000/*.root") ;
    ch_ST_anti->Add("/pnfs/iihe/cms/store/user/wenxing/RunIISpring16DR80/ST_tW_antitop_5f_inclusiveDecays-powheg/160712_185604/0000/*.root") ;
    ch_GJ_1->Add("/pnfs/iihe/cms/store/user/wenxing/RunIISpring16DR80/GJets_HT-40To100_TuneCUETP8M1-madgraphMLM/160712_203547/0000/*.root") ;
    ch_GJ_2->Add("/pnfs/iihe/cms/store/user/wenxing/RunIISpring16DR80/GJets_HT-100To200_TuneCUETP8M1-madgraphMLM/160712_203617/0000/*.root") ;
    ch_GJ_3->Add("/pnfs/iihe/cms/store/user/wenxing/RunIISpring16DR80/GJets_HT-200To400_TuneCUETP8M1-madgraphMLM/160712_203649/0000/*.root") ;
    ch_GJ_4->Add("/pnfs/iihe/cms/store/user/wenxing/RunIISpring16DR80/GJets_HT-400To600_TuneCUETP8M1-madgraphMLM/160712_203717/0000/*.root") ;
    ch_GJ_5->Add("/pnfs/iihe/cms/store/user/wenxing/RunIISpring16DR80/GJets_HT-600ToInf_TuneCUETP8M1-madgraphMLM/160712_203802/0000/*.root") ;
//

    ch_TT2L_1->Add("/pnfs/iihe/cms/store/user/wenxing/RunIISpring16DR80/TTTo2L2Nu_13TeV-powheg/160712_203936/0000/*.root") ;
    ch_TT2L_2->Add("/pnfs/iihe/cms/store/user/wenxing/RunIISpring16DR80/TTTo2L2Nu_13TeV-powheg/160712_203936/0001/*.root") ;
    ch_TT2L_3->Add("/pnfs/iihe/cms/store/user/wenxing/RunIISpring16DR80/TTTo2L2Nu_13TeV-powheg/160712_203936/0002/*.root") ;
    ch_TT2L_4->Add("/pnfs/iihe/cms/store/user/wenxing/RunIISpring16DR80/TTTo2L2Nu_13TeV-powheg/160712_203936/0003/*.root") ;
    ch_TT2L_5->Add("/pnfs/iihe/cms/store/user/wenxing/RunIISpring16DR80/TTTo2L2Nu_13TeV-powheg/160712_203936/0004/*.root") ;
    ch_TT2L_6->Add("/pnfs/iihe/cms/store/user/wenxing/RunIISpring16DR80/TTTo2L2Nu_13TeV-powheg/160712_203936/0005/*.root") ;
    ch_TT2L_7->Add("/pnfs/iihe/cms/store/user/wenxing/RunIISpring16DR80/TTTo2L2Nu_13TeV-powheg/160712_203936/0006/*.root") ;
    ch_TT2L_8->Add("/pnfs/iihe/cms/store/user/wenxing/RunIISpring16DR80/TTTo2L2Nu_13TeV-powheg/160712_203936/0007/*.root") ;


    ch_WW2L_1->Add("/pnfs/iihe/cms/store/user/xgao/RunIISpring16DR80/WWTo2L2Nu_13TeV-powheg/*.root") ;
    ch_WW2L_2->Add("/pnfs/iihe/cms/store/user/xgao/RunIISpring16DR80/WWTo2L2Nu_Mll_200To600_13TeV-powheg/*.root") ;
    ch_WW2L_3->Add("/pnfs/iihe/cms/store/user/xgao/RunIISpring16DR80/WWTo2L2Nu_Mll_600To1200_13TeV-powheg/*.root") ;
    ch_WW2L_4->Add("/pnfs/iihe/cms/store/user/xgao/RunIISpring16DR80/WWTo2L2Nu_Mll_1200To2500_13TeV-powheg/*.root") ;
    ch_WW2L_5->Add("/pnfs/iihe/cms/store/user/xgao/RunIISpring16DR80/WWTo2L2Nu_Mll_2500ToInf_13TeV-powheg/*.root") ;

    reskim_FR_1F reskim_ZToEE_1(ch_ZToEE_1, false, false, false, false) ;
    reskim_ZToEE_1.Loop("ntuples/reskim/RunE/ZToEE_powheg_M_50_120_1F.root") ;
    reskim_FR_1F reskim_ZToEE_2(ch_ZToEE_2, false, false, false, false) ;
    reskim_ZToEE_2.Loop("ntuples/reskim/RunE/ZToEE_powheg_M_120_200_1F.root") ;
    reskim_FR_1F reskim_ZToEE_3(ch_ZToEE_3, false, false, false, false) ;
    reskim_ZToEE_3.Loop("ntuples/reskim/RunE/ZToEE_powheg_M_200_400_1F.root") ;
    reskim_FR_1F reskim_ZToEE_4(ch_ZToEE_4, false, false, false, false) ;
    reskim_ZToEE_4.Loop("ntuples/reskim/RunE/ZToEE_powheg_M_400_800_1F.root") ;
    reskim_FR_1F reskim_ZToEE_5(ch_ZToEE_5, false, false, false, false) ;
    reskim_ZToEE_5.Loop("ntuples/reskim/RunE/ZToEE_powheg_M_800_1400_1F.root") ;
    reskim_FR_1F reskim_ZToEE_6(ch_ZToEE_6, false, false, false, false) ;
    reskim_ZToEE_6.Loop("ntuples/reskim/RunE/ZToEE_powheg_M_1400_2300_1F.root") ;
    reskim_FR_1F reskim_ZToEE_7(ch_ZToEE_7, false, false, false, false) ;
    reskim_ZToEE_7.Loop("ntuples/reskim/RunE/ZToEE_powheg_M_2300_3500_1F.root") ;
    reskim_FR_1F reskim_ZToEE_8(ch_ZToEE_8, false, false, false, false) ;
    reskim_ZToEE_8.Loop("ntuples/reskim/RunE/ZToEE_powheg_M_3500_4500_1F.root") ;
    reskim_FR_1F reskim_ZToEE_9(ch_ZToEE_9, false, false, false, false) ;
    reskim_ZToEE_9.Loop("ntuples/reskim/RunE/ZToEE_powheg_M_4500_6000_1F.root") ;
    reskim_FR_1F reskim_ZToEE_10(ch_ZToEE_10, false, false, false, false) ;
    reskim_ZToEE_10.Loop("ntuples/reskim/RunE/ZToEE_powheg_M_6000_Inf_1F.root") ;

    reskim_FR_1F reskim_DY_1(ch_DY_1, false, false, true, false) ;
    reskim_DY_1.Loop("ntuples/reskim/RunE/ZToTT_mad_1_1F.root") ;
    reskim_FR_1F reskim_DY_2(ch_DY_2, false, false, true, false) ;
    reskim_DY_2.Loop("ntuples/reskim/RunE/ZToTT_mad_2_1F.root") ;
    reskim_FR_1F reskim_DY_3(ch_DY_3, false, false, true, false) ;
    reskim_DY_3.Loop("ntuples/reskim/RunE/ZToTT_mad_3_1F.root") ;
    
    reskim_FR_1F reskim_WJet_mad_1(ch_WJet_mad_1, false, false, false, false) ;
    reskim_WJet_mad_1.Loop("ntuples/reskim/RunE/WJet_mad_1_1F.root") ;
    reskim_FR_1F reskim_WJet_mad_2(ch_WJet_mad_2, false, false, false, false) ;
    reskim_WJet_mad_2.Loop("ntuples/reskim/RunE/WJet_mad_2_1F.root") ;

    reskim_FR_1F reskim_WZ(ch_WZ, false, false, false, false) ;
    reskim_WZ.Loop("ntuples/reskim/RunE/WZ_1F.root") ;
    reskim_FR_1F reskim_ZZ(ch_ZZ, false, false, false, false) ;
    reskim_ZZ.Loop("ntuples/reskim/RunE/ZZ_1F.root") ;
    reskim_FR_1F reskim_ST(ch_ST, false, false, false, false) ;
    reskim_ST.Loop("ntuples/reskim/RunE/ST_1F.root") ;
    reskim_FR_1F reskim_ST_anti(ch_ST_anti, false, false, false, false) ;
    reskim_ST_anti.Loop("ntuples/reskim/RunE/ST_anti_1F.root") ;
    reskim_FR_1F reskim_GJ_1(ch_GJ_1, false, false, false, false) ;
    reskim_GJ_1.Loop("ntuples/reskim/RunE/GJ_40_100_1F.root") ;
    reskim_FR_1F reskim_GJ_2(ch_GJ_2, false, false, false, false) ;
    reskim_GJ_2.Loop("ntuples/reskim/RunE/GJ_100_200_1F.root") ;
    reskim_FR_1F reskim_GJ_3(ch_GJ_3, false, false, false, false) ;
    reskim_GJ_3.Loop("ntuples/reskim/RunE/GJ_200_400_1F.root") ;
    reskim_FR_1F reskim_GJ_4(ch_GJ_4, false, false, false, false) ;
    reskim_GJ_4.Loop("ntuples/reskim/RunE/GJ_400_600_1F.root") ;
    reskim_FR_1F reskim_GJ_5(ch_GJ_5, false, false, false, false) ;
    reskim_GJ_5.Loop("ntuples/reskim/RunE/GJ_600_Inf_1F.root") ;


    reskim_FR_1F reskim_TT2L_1(ch_TT2L_1, false, false, false, false) ;
    reskim_TT2L_1.Loop("ntuples/reskim/RunE/ttbar2L_1_1F.root") ;
    reskim_FR_1F reskim_TT2L_2(ch_TT2L_2, false, false, false, false) ;
    reskim_TT2L_2.Loop("ntuples/reskim/RunE/ttbar2L_2_1F.root") ;
    reskim_FR_1F reskim_TT2L_3(ch_TT2L_3, false, false, false, false) ;
    reskim_TT2L_3.Loop("ntuples/reskim/RunE/ttbar2L_3_1F.root") ;
    reskim_FR_1F reskim_TT2L_4(ch_TT2L_4, false, false, false, false) ;
    reskim_TT2L_4.Loop("ntuples/reskim/RunE/ttbar2L_4_1F.root") ;
    reskim_FR_1F reskim_TT2L_5(ch_TT2L_5, false, false, false, false) ;
    reskim_TT2L_5.Loop("ntuples/reskim/RunE/ttbar2L_5_1F.root") ;
    reskim_FR_1F reskim_TT2L_6(ch_TT2L_6, false, false, false, false) ;
    reskim_TT2L_6.Loop("ntuples/reskim/RunE/ttbar2L_6_1F.root") ;
    reskim_FR_1F reskim_TT2L_7(ch_TT2L_7, false, false, false, false) ;
    reskim_TT2L_7.Loop("ntuples/reskim/RunE/ttbar2L_7_1F.root") ;
    reskim_FR_1F reskim_TT2L_8(ch_TT2L_8, false, false, false, false) ;
    reskim_TT2L_8.Loop("ntuples/reskim/RunE/ttbar2L_8_1F.root") ;

    reskim_FR_1F reskim_WW2L_1(ch_WW2L_1, false, false, false, true) ;
    reskim_WW2L_1.Loop("ntuples/reskim/RunE/WW2L_200_1F.root") ;
    reskim_FR_1F reskim_WW2L_2(ch_WW2L_2, false, false, false, false) ;
    reskim_WW2L_2.Loop("ntuples/reskim/RunE/WW2L_200_600_1F.root") ;
    reskim_FR_1F reskim_WW2L_3(ch_WW2L_3, false, false, false, false) ;
    reskim_WW2L_3.Loop("ntuples/reskim/RunE/WW2L_600_1200_1F.root") ;
    reskim_FR_1F reskim_WW2L_4(ch_WW2L_4, false, false, false, false) ;
    reskim_WW2L_4.Loop("ntuples/reskim/RunE/WW2L_1200_2500_1F.root") ;
    reskim_FR_1F reskim_WW2L_5(ch_WW2L_5, false, false, false, false) ;
    reskim_WW2L_5.Loop("ntuples/reskim/RunE/WW2L_2500_Inf_1F.root") ;

/*
    reskim_FR_1F reskim_DY_1(ch_DY_1, false, true, false, false) ;
    reskim_DY_1.Loop("ntuples/reskim/DYToEE_mad_1_1F.root") ;
    reskim_FR_1F reskim_DY_2(ch_DY_2, false, true, false, false) ;
    reskim_DY_2.Loop("ntuples/reskim/DYToEE_mad_2_1F.root") ;
    reskim_FR_1F reskim_DY_3(ch_DY_3, false, true, false, false) ;
    reskim_DY_3.Loop("ntuples/reskim/DYToEE_mad_3_1F.root") ;

    reskim_FR_1F reskim_DYToEE_1(ch_DYToEE_1, false, false, false, false) ;
    reskim_DYToEE_1.Loop("ntuples/reskim/DYToEE_pow_1_1F.root") ;
    reskim_FR_1F reskim_DYToEE_2(ch_DYToEE_2, false, false, false, false) ;
    reskim_DYToEE_2.Loop("ntuples/reskim/DYToEE_pow_2_1F.root") ;
    reskim_FR_1F reskim_DYToEE_3(ch_DYToEE_3, false, false, false, false) ;
    reskim_DYToEE_3.Loop("ntuples/reskim/DYToEE_pow_3_1F.root") ;

    reskim_FR_1F reskim_DY_amc_1(ch_DY_amc_1, false, true, false, false) ;
    reskim_DY_amc_1.Loop("ntuples/reskim/DYToEE_amc_1_1F.root") ;
    reskim_FR_1F reskim_DY_amc_2(ch_DY_amc_2, false, true, false, false) ;
    reskim_DY_amc_2.Loop("ntuples/reskim/DYToEE_amc_2_1F.root") ;
*/
  }
}

