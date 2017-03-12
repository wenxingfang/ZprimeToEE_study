//#include "reskim.h"
//#include "reskim.C"

void reskim_all(){

  bool do_data = false ;
  bool do_MC   = true ;
  
  if(do_data){
/*
    TChain *ch_data_1 =new TChain("IIHEAnalysis");
    ifstream fin_1("/user/wenxing/run_data/CMSSW_8_0_7_patch1/src/UserCode/IIHETree/test/split_file/file_v2.txt");  
    string s_1;  
    while( getline(fin_1,s_1) )
    {   
        ch_data_1->Add(TString(s_1));
    }
    cout << "Add file finish: " << endl; 
    reskim reskim_data_1(ch_data_1, true, false, false, false, 2, 273158, 273730) ;
    reskim_data_1.Loop("ntuples/reskim/data_12p39fb_v2.root") ;

    TChain *ch_data_2 =new TChain("IIHEAnalysis");
    ifstream fin_2("/user/wenxing/run_data/CMSSW_8_0_7_patch1/src/UserCode/IIHETree/test/split_file/file_v3_1.txt");  
    string s_2;  
    while( getline(fin_2,s_2) )
    {   
        ch_data_2->Add(TString(s_2));
    }
    cout << "Add file finish: " << endl; 
    reskim reskim_data_2(ch_data_2, true, false, false, false, 3, 274094, 275066) ;
    reskim_data_2.Loop("ntuples/reskim/data_12p39fb_v3_1.root") ;

    TChain *ch_data_4 =new TChain("IIHEAnalysis");
    ifstream fin_4("/user/wenxing/run_data/CMSSW_8_0_7_patch1/src/UserCode/IIHETree/test/split_file/file_v3_2.txt");  
    string s_4;  
    while( getline(fin_4,s_4) )
    {   
        ch_data_4->Add(TString(s_4));
    }
    cout << "Add file finish: " << endl; 
    reskim reskim_data_4(ch_data_4, true, false, false, false, 3, 274094, 275066) ;
    reskim_data_4.Loop("ntuples/reskim/data_12p39fb_v3_2.root") ;


    TChain *ch_data_3 =new TChain("IIHEAnalysis");
    ifstream fin_3("/user/wenxing/run_data/CMSSW_8_0_7_patch1/src/UserCode/IIHETree/test/split_file/file_v4.txt");  
    string s_3;  
    while( getline(fin_3,s_3) )
    {   
        ch_data_3->Add(TString(s_3));
    }
    cout << "Add file finish: " << endl; 
    reskim reskim_data_3(ch_data_3, true, false, false, false, 4, 275067, 275311) ;
    reskim_data_3.Loop("ntuples/reskim/data_12p39fb_v4.root") ;

    TChain *ch_data_5 =new TChain("IIHEAnalysis");
    ifstream fin_5("/user/wenxing/run_data/CMSSW_8_0_7_patch1/src/UserCode/IIHETree/test/split_file/file_v5_1.txt");  
    string s_5;  
    while( getline(fin_5,s_5) )
    {   
        ch_data_5->Add(TString(s_5));
    }
    cout << "Add file finish: " << endl; 
    reskim reskim_data_5(ch_data_5, true, false, false, false, 5, 275319, 276811) ;
    reskim_data_5.Loop("ntuples/reskim/data_12p39fb_v5_1.root") ;

    TChain *ch_data_6 =new TChain("IIHEAnalysis");
    ifstream fin_6("/user/wenxing/run_data/CMSSW_8_0_7_patch1/src/UserCode/IIHETree/test/split_file/file_v5_2.txt");  
    string s_6;  
    while( getline(fin_6,s_6) )
    {   
        ch_data_6->Add(TString(s_6));
    }
    cout << "Add file finish: " << endl; 
    reskim reskim_data_6(ch_data_6, true, false, false, false, 5, 275319, 276811) ;
    reskim_data_6.Loop("ntuples/reskim/data_12p39fb_v5_2.root") ;

    TChain *ch_data_7 =new TChain("IIHEAnalysis");
    ifstream fin_7("/user/wenxing/run_data/CMSSW_8_0_7_patch1/src/UserCode/IIHETree/test/split_file/file_v5_3.txt");  
    string s_7;  
    while( getline(fin_7,s_7) )
    {   
        ch_data_7->Add(TString(s_7));
    }
    cout << "Add file finish: " << endl; 
    reskim reskim_data_7(ch_data_7, true, false, false, false, 5, 275319, 276811) ;
    reskim_data_7.Loop("ntuples/reskim/data_12p39fb_v5_3.root") ;
*/
/*
//------------------------------ RunE ------------------------------------
    TChain *ch_data_8 =new TChain("IIHEAnalysis");
    ifstream fin_8("/user/wenxing/run_data/CMSSW_8_0_7_patch1/src/UserCode/IIHETree/test/split_file/file_v5_RunE.txt");  
    string s_8;  
    while( getline(fin_8,s_8) )
    {   
        ch_data_8->Add(TString(s_8));
    }
    cout << "Add file finish: " << endl; 
    reskim reskim_data_8(ch_data_8, true, false, false, false, 5, 276830, 276834) ;
    reskim_data_8.Loop("ntuples/reskim/RunE/data_RunE_v5.root") ;

    TChain *ch_data_9 =new TChain("IIHEAnalysis");
    ifstream fin_9("/user/wenxing/run_data/CMSSW_8_0_7_patch1/src/UserCode/IIHETree/test/split_file/file_v6_RunE.txt");  
    string s_9;  
    while( getline(fin_9,s_9) )
    {   
        ch_data_9->Add(TString(s_9));
    }
    cout << "Add file finish: " << endl; 
    reskim reskim_data_9(ch_data_9, true, false, false, false, 6, 276870, 277420) ;
    reskim_data_9.Loop("ntuples/reskim/RunE/data_RunE_v6.root") ;
*/
//------------------------------ RunF ------------------------------------
//
//    TChain *ch_data_F_1 =new TChain("IIHEAnalysis");
//    ifstream fin_F_1("/user/wenxing/run_data/CMSSW_8_0_7_patch1/src/UserCode/IIHETree/test/split_file/file_v6_RunF.txt");  
//    string s_F_1;  
//    while( getline(fin_F_1,s_F_1) )
//    {   
//        ch_data_F_1->Add(TString(s_F_1));
//    }
//    cout << "Add file finish: " << endl; 
//    reskim reskim_data_F_1(ch_data_F_1, true, false, false, false, 6, 277820, 278240) ;
//    reskim_data_F_1.Loop("ntuples/reskim/RunF/data_RunF_v6_use.root") ;
//
//    TChain *ch_data_F_2 =new TChain("IIHEAnalysis");
//    ifstream fin_F_2("/user/wenxing/run_data/CMSSW_8_0_7_patch1/src/UserCode/IIHETree/test/split_file/file_v7_RunF.txt");  
//    string s_F_2;  
//    while( getline(fin_F_2,s_F_2) )
//    {   
//        ch_data_F_2->Add(TString(s_F_2));
//    }
//    cout << "Add file finish: " << endl; 
//    reskim reskim_data_F_2(ch_data_F_2, true, false, false, false, 7, 278273, 278808) ;
//    reskim_data_F_2.Loop("ntuples/reskim/RunF/data_RunF_v7_use.root") ;
//

//------------------------------ RunG ------------------------------------
//    TChain *ch_data_G =new TChain("IIHEAnalysis");
//    ch_data_G->Add("/pnfs/iihe/cms/store/user/rgoldouz/SkimmedData/Golden_2016_postICHEP/SingleElectron_Run2016G_PromptReco_v1_AOD/*.root");
//    cout << "Add file finish: " << endl; 
//    reskim reskim_data_G(ch_data_G, true, false, false, false, 7, 1, 1000000) ;
//    reskim_data_G.Loop("ntuples/reskim/RunG/data_RunG.root") ;

////////////////////////// Fake //////////////////////////////////////
/*
    TChain *ch_data_1 =new TChain("IIHEAnalysis");
    ifstream fin_1("/user/wenxing/run_data/CMSSW_8_0_7_patch1/src/UserCode/IIHETree/test/split_file/file_Ele33_v3_1.txt");  
    string s_1;  
    while( getline(fin_1,s_1) )
    {   
        ch_data_1->Add(TString(s_1));
    }
    cout << "Add file finish: " << endl; 
    reskim reskim_data_1(ch_data_1, true, false, false, false, 0, 273158, 273730) ;
    reskim_data_1.Loop("ntuples/reskim/data_12p39fb_FR_1.root") ;
    
    TChain *ch_data_2 =new TChain("IIHEAnalysis");
    ifstream fin_2("/user/wenxing/run_data/CMSSW_8_0_7_patch1/src/UserCode/IIHETree/test/split_file/file_Ele33_v3_2.txt");  
    string s_2;  
    while( getline(fin_2,s_2) )
    {   
        ch_data_2->Add(TString(s_2));
    }
    cout << "Add file finish: " << endl; 
    reskim reskim_data_2(ch_data_2, true, false, false, false, 0, 273158, 273730) ;
    reskim_data_2.Loop("ntuples/reskim/data_12p39fb_FR_2.root") ;
    
    TChain *ch_data_3 =new TChain("IIHEAnalysis");
    ifstream fin_3("/user/wenxing/run_data/CMSSW_8_0_7_patch1/src/UserCode/IIHETree/test/split_file/file_Ele33_v4.txt");  
    string s_3;  
    while( getline(fin_3,s_3) )
    {   
        ch_data_3->Add(TString(s_3));
    }
    cout << "Add file finish: " << endl; 
    reskim reskim_data_3(ch_data_3, true, false, false, false, 0, 273158, 273730) ;
    reskim_data_3.Loop("ntuples/reskim/data_12p39fb_FR_3.root") ;

    TChain *ch_data_4 =new TChain("IIHEAnalysis");
    ifstream fin_4("/user/wenxing/run_data/CMSSW_8_0_7_patch1/src/UserCode/IIHETree/test/split_file/file_Ele33_v5.txt");  
    string s_4;  
    while( getline(fin_4,s_4) )
    {   
        ch_data_4->Add(TString(s_4));
    }
    cout << "Add file finish: " << endl; 
    reskim reskim_data_4(ch_data_4, true, false, false, false, 0, 273158, 273730) ;
    reskim_data_4.Loop("ntuples/reskim/data_12p39fb_FR_4.root") ;

    TChain *ch_data_5 =new TChain("IIHEAnalysis");
    ifstream fin_5("/user/wenxing/run_data/CMSSW_8_0_7_patch1/src/UserCode/IIHETree/test/split_file/file_Ele33_v6_1.txt");  
    string s_5;  
    while( getline(fin_5,s_5) )
    {   
        ch_data_5->Add(TString(s_5));
    }
    cout << "Add file finish: " << endl; 
    reskim reskim_data_5(ch_data_5, true, false, false, false, 0, 273158, 273730) ;
    reskim_data_5.Loop("ntuples/reskim/data_12p39fb_FR_5.root") ;

    TChain *ch_data_6 =new TChain("IIHEAnalysis");
    ifstream fin_6("/user/wenxing/run_data/CMSSW_8_0_7_patch1/src/UserCode/IIHETree/test/split_file/file_Ele33_v6_2.txt");  
    string s_6;  
    while( getline(fin_6,s_6) )
    {   
        ch_data_6->Add(TString(s_6));
    }
    cout << "Add file finish: " << endl; 
    reskim reskim_data_6(ch_data_6, true, false, false, false, 0, 273158, 273730) ;
    reskim_data_6.Loop("ntuples/reskim/data_12p39fb_FR_6.root") ;

    TChain *ch_data_7 =new TChain("IIHEAnalysis");
    ifstream fin_7("/user/wenxing/run_data/CMSSW_8_0_7_patch1/src/UserCode/IIHETree/test/split_file/file_Ele33_v6_3.txt");  
    string s_7;  
    while( getline(fin_7,s_7) )
    {   
        ch_data_7->Add(TString(s_7));
    }
    cout << "Add file finish: " << endl; 
    reskim reskim_data_7(ch_data_7, true, false, false, false, 0, 273158, 273730) ;
    reskim_data_7.Loop("ntuples/reskim/data_12p39fb_FR_7.root") ;
*/


//------------------------------ RunE ------------------------------------
//    TChain *ch_data_E =new TChain("IIHEAnalysis");
//    ch_data_E->Add("/pnfs/iihe/cms/store/user/rgoldouz/SkimmedData/Golden_2016_postICHEP/DoubleEG_Run2016E_PromptReco_v2_AOD/*.root");
//    cout << "Add file finish: " << endl; 
//    reskim reskim_data_E(ch_data_E, true, false, false, false, 0, 1, 1000000) ;
//    reskim_data_E.Loop("ntuples/reskim/RunE/data_RunE_FR.root") ;

////--------------------------RunF--------------

//    TChain *ch_data_F =new TChain("IIHEAnalysis");
//    ch_data_F->Add("/pnfs/iihe/cms/store/user/rgoldouz/SkimmedData/Golden_2016_postICHEP/DoubleEG_Run2016F_PromptReco_v1_AOD/*.root");
//    cout << "Add file finish: " << endl; 
//    reskim reskim_data_F(ch_data_F, true, false, false, false, 0, 1, 1000000) ;
//    reskim_data_F.Loop("ntuples/reskim/RunF/data_RunF_FR.root") ;


////------------------------- RunG------------
//    TChain *ch_data_G =new TChain("IIHEAnalysis");
//    ch_data_G->Add("/pnfs/iihe/cms/store/user/rgoldouz/SkimmedData/Golden_2016_postICHEP/DoubleEG_Run2016G_PromptReco_v1_AOD/*.root");
//    cout << "Add file finish: " << endl; 
//    reskim reskim_data_G(ch_data_G, true, false, false, false, 0, 1, 1000000) ;
//    reskim_data_G.Loop("ntuples/reskim/RunG/data_RunG_FR.root") ;

  }
  
  if(do_MC){

    TChain* ch_DYToEE_1 = new TChain("IIHEAnalysis") ;
    TChain* ch_DYToEE_2 = new TChain("IIHEAnalysis") ;
    TChain* ch_DYToEE_3 = new TChain("IIHEAnalysis") ;
    TChain* ch_DY_1 = new TChain("IIHEAnalysis") ;
    TChain* ch_DY_2 = new TChain("IIHEAnalysis") ;
    TChain* ch_DY_3 = new TChain("IIHEAnalysis") ;
    TChain* ch_DY_4 = new TChain("IIHEAnalysis") ;
    TChain* ch_DY_5 = new TChain("IIHEAnalysis") ;
    TChain* ch_DY_6 = new TChain("IIHEAnalysis") ;
    TChain* ch_WJet_mad_1 = new TChain("IIHEAnalysis") ;
    TChain* ch_WJet_mad_2 = new TChain("IIHEAnalysis") ;
    TChain* ch_WJet_mad_3 = new TChain("IIHEAnalysis") ;
    TChain* ch_WJet_mad_4 = new TChain("IIHEAnalysis") ;
    TChain* ch_WJet_mad_5 = new TChain("IIHEAnalysis") ;
    TChain* ch_WJet_mad_6 = new TChain("IIHEAnalysis") ;
    TChain* ch_WJet_mad_7 = new TChain("IIHEAnalysis") ;
    TChain* ch_WJet_amc_1 = new TChain("IIHEAnalysis") ;
    TChain* ch_WW = new TChain("IIHEAnalysis") ;
    TChain* ch_WZ = new TChain("IIHEAnalysis") ;
    TChain* ch_ZZ = new TChain("IIHEAnalysis") ;
    TChain* ch_TT_1 = new TChain("IIHEAnalysis") ;
    TChain* ch_TT_2 = new TChain("IIHEAnalysis") ;
    TChain* ch_TT_3 = new TChain("IIHEAnalysis") ;
    TChain* ch_TT_4 = new TChain("IIHEAnalysis") ;
    TChain* ch_TT_5 = new TChain("IIHEAnalysis") ;
    TChain* ch_TT_6 = new TChain("IIHEAnalysis") ;
    TChain* ch_TT_7 = new TChain("IIHEAnalysis") ;
    TChain* ch_ST = new TChain("IIHEAnalysis") ;
    TChain* ch_ST_anti = new TChain("IIHEAnalysis") ;
    TChain* ch_GJ_1 = new TChain("IIHEAnalysis") ;
    TChain* ch_GJ_2 = new TChain("IIHEAnalysis") ;
    TChain* ch_GJ_3 = new TChain("IIHEAnalysis") ;
    TChain* ch_GJ_4 = new TChain("IIHEAnalysis") ;
    TChain* ch_GJ_5 = new TChain("IIHEAnalysis") ;
    
    
//    ch_DYToEE_1->Add("/pnfs/iihe/cms/store/user/wenxing/MC_PUMoriond17/MiniAOD/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-MiniAOD/170221_122606/0000/outfile_1.root") ;
//    ch_DYToEE_1->Add("/pnfs/iihe/cms/store/user/wenxing/MC_PUMoriond17/MiniAOD/DYJetsToLL_Pt-50To100_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_Pt-50To100_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8-MiniAOD/170221_114013/0000/outfile_1.root") ;
    ch_DYToEE_1->Add("/pnfs/iihe/cms/store/user/wenxing/MC_PUMoriond17/MiniAOD/DYJetsToLL_Zpt-100to200_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_DYJetsToLL_Zpt-100to200_M-50_TuneCUETP8M1_13TeV-madgraphMLM-MiniAOD/170202_110216/0000/outfile_1.root") ;
//    ch_WJet_amc_1->Add("/pnfs/iihe/cms/store/user/wenxing/MC_PUMoriond17/MiniAOD/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_WJetsToLNu_TuneCUETP8M1_13TeV-amcatnlo-MiniAOD/170220_201901/0000/outfile_1.root") ;
//    ch_WW->Add("/pnfs/iihe/cms/store/user/xgao/2016MCrereco/crab_WW/161121_151603/0000/*.root") ;
//    ch_WZ->Add("/pnfs/iihe/cms/store/user/xgao/2016MCrereco/crab_WZ/161121_151741/0000/*.root") ;
//    ch_ZZ->Add("/pnfs/iihe/cms/store/user/xgao/2016MCrereco/crab_ZZ/161120_172246/0000/*.root") ;
//    ch_ST->Add("/pnfs/iihe/cms/store/user/xgao/2016MCrereco/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/crab_ST_top/161120_172319/0000/*.root") ;
//    ch_ST_anti->Add("/pnfs/iihe/cms/store/user/xgao/2016MCrereco/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/crab_ST_antitop/161120_172209/0000/*.root") ;
//    ch_GJ_1->Add("/pnfs/iihe/cms/store/user/xgao/2016MCrereco/GJets_HT-40To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_GJets_HT_40To100/161120_173222/0000/*.root") ;
//    ch_GJ_2->Add("/pnfs/iihe/cms/store/user/xgao/2016MCrereco/GJets_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_GJets_HT_100To200/161120_173024/0000/*.root") ;
//    ch_GJ_3->Add("/pnfs/iihe/cms/store/user/xgao/2016MCrereco/GJets_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_GJets_HT_200To400/161120_172905/0000/*.root") ;
//    ch_GJ_4->Add("/pnfs/iihe/cms/store/user/xgao/2016MCrereco/GJets_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_GJets_HT_400To600/161120_172943/0000/*.root") ;
//    ch_GJ_5->Add("/pnfs/iihe/cms/store/user/xgao/2016MCrereco/GJets_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_GJets_HT_600ToInf/161120_173149/0000/*.root") ;
//    ch_TT_1->Add("/pnfs/iihe/cms/store/user/xgao/2016MCrereco/TT_TuneCUETP8M1_13TeV-powheg-pythia8/crab_TT/161120_173422/0000/*.root") ;
//    ch_TT_2->Add("/pnfs/iihe/cms/store/user/xgao/2016MCrereco/TT_TuneCUETP8M1_13TeV-powheg-pythia8/crab_TT/161120_173422/0001/*.root") ;
//    ch_TT_3->Add("/pnfs/iihe/cms/store/user/xgao/2016MCrereco/TT_TuneCUETP8M1_13TeV-powheg-pythia8/crab_TT/161120_173422/0002/*.root") ;
//    ch_TT_4->Add("/pnfs/iihe/cms/store/user/xgao/2016MCrereco/TT_TuneCUETP8M1_13TeV-powheg-pythia8/crab_TT/161120_173422/0003/*.root") ;
//    ch_TT_5->Add("/pnfs/iihe/cms/store/user/xgao/2016MCrereco/TT_TuneCUETP8M1_13TeV-powheg-pythia8/crab_TT/161120_173422/0004/*.root") ;
//    ch_TT_6->Add("/pnfs/iihe/cms/store/user/xgao/2016MCrereco/TT_TuneCUETP8M1_13TeV-powheg-pythia8/crab_TT/161120_173422/0005/*.root") ;
//    ch_TT_7->Add("/pnfs/iihe/cms/store/user/xgao/2016MCrereco/TT_TuneCUETP8M1_13TeV-powheg-pythia8/crab_TT/161120_173422/0006/*.root") ;
//

//    reskim reskim_DY_1(ch_DY_1, false, false, true, false) ;
//    reskim_DY_1.Loop("ntuples/reskim/MC_newTrkIso/ZToTT_mad_1.root") ;
//    reskim reskim_DY_2(ch_DY_2, false, false, true, false) ;
//    reskim_DY_2.Loop("ntuples/reskim/MC_newTrkIso/ZToTT_mad_2.root") ;
//    reskim reskim_DY_3(ch_DY_3, false, false, true, false) ;
//    reskim_DY_3.Loop("ntuples/reskim/MC_newTrkIso/ZToTT_mad_3.root") ;
//    reskim reskim_DY_4(ch_DY_4, false, false, true, false) ;
//    reskim_DY_4.Loop("ntuples/reskim/MC_newTrkIso/ZToTT_mad_4.root") ;
//    reskim reskim_DY_5(ch_DY_5, false, false, true, false) ;
//    reskim_DY_5.Loop("ntuples/reskim/MC_newTrkIso/ZToTT_mad_5.root") ;
//    reskim reskim_DY_6(ch_DY_6, false, false, true, false) ;
//    reskim_DY_6.Loop("ntuples/reskim/MC_newTrkIso/ZToTT_mad_6.root") ;
//    reskim reskim_WJet_mad_1(ch_WJet_mad_1, false, false, false, false) ;
//    reskim_WJet_mad_1.Loop("ntuples/reskim/MC_newTrkIso/WJet_mad_1.root") ;
//    reskim reskim_WJet_mad_2(ch_WJet_mad_2, false, false, false, false) ;
//    reskim_WJet_mad_2.Loop("ntuples/reskim/MC_newTrkIso/WJet_mad_2.root") ;
//    reskim reskim_WJet_mad_3(ch_WJet_mad_3, false, false, false, false) ;
//    reskim_WJet_mad_3.Loop("ntuples/reskim/MC_newTrkIso/WJet_mad_3.root") ;
//    reskim reskim_WJet_mad_4(ch_WJet_mad_4, false, false, false, false) ;
//    reskim_WJet_mad_4.Loop("ntuples/reskim/MC_newTrkIso/WJet_mad_4.root") ;
//    reskim reskim_WJet_mad_5(ch_WJet_mad_5, false, false, false, false) ;
//    reskim_WJet_mad_5.Loop("ntuples/reskim/MC_newTrkIso/WJet_mad_5.root") ;
//    reskim reskim_WJet_mad_6(ch_WJet_mad_6, false, false, false, false) ;
//    reskim_WJet_mad_6.Loop("ntuples/reskim/MC_newTrkIso/WJet_mad_6.root") ;
//    reskim reskim_WJet_mad_7(ch_WJet_mad_7, false, false, false, false) ;
//    reskim_WJet_mad_7.Loop("ntuples/reskim/MC_newTrkIso/WJet_mad_7.root") ;
//    reskim reskim_WW(ch_WW, false, false, false, false) ;
//    reskim_WW.Loop("ntuples/reskim/MC_newTrkIso/WW_test.root") ;
//    reskim reskim_WZ(ch_WZ, false, false, false, false) ;
//    reskim_WZ.Loop("ntuples/reskim/MC_newTrkIso/WZ.root") ;
//    reskim reskim_ZZ(ch_ZZ, false, false, false, false) ;
//    reskim_ZZ.Loop("ntuples/reskim/MC_newTrkIso/ZZ.root") ;
//    reskim reskim_ST(ch_ST, false, false, false, false) ;
//    reskim_ST.Loop("ntuples/reskim/MC_newTrkIso/ST.root") ;
//    reskim reskim_ST_anti(ch_ST_anti, false, false, false, false) ;
//    reskim_ST_anti.Loop("ntuples/reskim/MC_newTrkIso/ST_anti.root") ;
//    reskim reskim_GJ_1(ch_GJ_1, false, false, false, false) ;
//    reskim_GJ_1.Loop("ntuples/reskim/MC_newTrkIso/GJ_40_100.root") ;
//    reskim reskim_GJ_2(ch_GJ_2, false, false, false, false) ;
//    reskim_GJ_2.Loop("ntuples/reskim/MC_newTrkIso/GJ_100_200.root") ;
//    reskim reskim_GJ_3(ch_GJ_3, false, false, false, false) ;
//    reskim_GJ_3.Loop("ntuples/reskim/MC_newTrkIso/GJ_200_400.root") ;
//    reskim reskim_GJ_4(ch_GJ_4, false, false, false, false) ;
//    reskim_GJ_4.Loop("ntuples/reskim/MC_newTrkIso/GJ_400_600.root") ;
//    reskim reskim_GJ_5(ch_GJ_5, false, false, false, false) ;
//    reskim_GJ_5.Loop("ntuples/reskim/MC_newTrkIso/GJ_600_Inf.root") ;
//    reskim reskim_TT_1(ch_TT_1, false, false, false, false) ;
//    reskim_TT_1.Loop("ntuples/reskim/MC_newTrkIso/TTbar_1.root") ;
//    reskim reskim_TT_2(ch_TT_2, false, false, false, false) ;
//    reskim_TT_2.Loop("ntuples/reskim/MC_newTrkIso/TTbar_2.root") ;
//    reskim reskim_TT_3(ch_TT_3, false, false, false, false) ;
//    reskim_TT_3.Loop("ntuples/reskim/MC_newTrkIso/TTbar_3.root") ;
//    reskim reskim_TT_4(ch_TT_4, false, false, false, false) ;
//    reskim_TT_4.Loop("ntuples/reskim/MC_newTrkIso/TTbar_4.root") ;
//    reskim reskim_TT_5(ch_TT_5, false, false, false, false) ;
//    reskim_TT_5.Loop("ntuples/reskim/MC_newTrkIso/TTbar_5.root") ;
//    reskim reskim_TT_6(ch_TT_6, false, false, false, false) ;
//    reskim_TT_6.Loop("ntuples/reskim/MC_newTrkIso/TTbar_6.root") ;
//    reskim reskim_TT_7(ch_TT_7, false, false, false, false) ;
//    reskim_TT_7.Loop("ntuples/reskim/MC_newTrkIso/TTbar_7.root") ;
//
    reskim reskim_DYToEE_1(ch_DYToEE_1, false, true, false, false) ;
    reskim_DYToEE_1.Loop("ntuples/reskim/MC_newTrkIso/test.root") ;

//    reskim reskim_WJet_1(ch_WJet_amc_1, false, false, false, true) ;
//    reskim_WJet_1.Loop("ntuples/reskim/MC_newTrkIso/test.root") ;
  }
  
}

