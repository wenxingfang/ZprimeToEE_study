void reskim_all_mc(){
  
  bool do_MC   = true ;
  
  
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
    TChain* ch_DY_amc_1 = new TChain("IIHEAnalysis") ;
    TChain* ch_DY_amc_2 = new TChain("IIHEAnalysis") ;
    TChain* ch_DY_amc_3 = new TChain("IIHEAnalysis") ;
    TChain* ch_DY_amc_4 = new TChain("IIHEAnalysis") ;
    TChain* ch_DY_amc_5 = new TChain("IIHEAnalysis") ;
    TChain* ch_DY_amc_6 = new TChain("IIHEAnalysis") ;
    TChain* ch_DY_amc_7 = new TChain("IIHEAnalysis") ;
    TChain* ch_DY_amc_8 = new TChain("IIHEAnalysis") ;
    TChain* ch_DY_amc_9 = new TChain("IIHEAnalysis") ;
    
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
    

    ch_DY_amc_1->Add("/pnfs/iihe/cms/store/user/rgoldouz/DYJetsToLL_M-100to200_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_M-100to200_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/160731_213306/0000/*.root") ;
    ch_DY_amc_2->Add("/pnfs/iihe/cms/store/user/rgoldouz/DYJetsToLL_M-200to400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_M-200to400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/160731_213329/0000/*.root") ;
    ch_DY_amc_3->Add("/pnfs/iihe/cms/store/user/rgoldouz/DYJetsToLL_M-400to500_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_M-400to500_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/160731_213424/0000/*.root") ;
    ch_DY_amc_4->Add("/pnfs/iihe/cms/store/user/rgoldouz/DYJetsToLL_M-500to700_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_M-500to700_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/160731_213444/0000/*.root") ;
    ch_DY_amc_5->Add("/pnfs/iihe/cms/store/user/rgoldouz/DYJetsToLL_M-700to800_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_M-700to800_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/160731_213507/0000/*.root") ;
    ch_DY_amc_6->Add("/pnfs/iihe/cms/store/user/rgoldouz/DYJetsToLL_M-800to1000_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_M-800to1000_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/160731_213534/0000/*.root") ;
    ch_DY_amc_7->Add("/pnfs/iihe/cms/store/user/rgoldouz/DYJetsToLL_M-1000to1500_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_M-1000to1500_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/160731_213600/0000/*.root") ;
    ch_DY_amc_8->Add("/pnfs/iihe/cms/store/user/rgoldouz/DYJetsToLL_M-1500to2000_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_M-1500to2000_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/160731_213704/0000/*.root") ;
    ch_DY_amc_9->Add("/pnfs/iihe/cms/store/user/rgoldouz/DYJetsToLL_M-2000to3000_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_DYJetsToLL_M-2000to3000_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/160731_213729/0000/*.root") ;
   


    reskim_mc reskim_ZToEE_1(ch_ZToEE_1, false, true, false, false) ;
    reskim_ZToEE_1.Loop("ntuples/reskim/ZToEE_powheg_M_50_120_mc.root") ;
    reskim_mc reskim_ZToEE_2(ch_ZToEE_2, false, true, false, false) ;
    reskim_ZToEE_2.Loop("ntuples/reskim/ZToEE_powheg_M_120_200_mc.root") ;
    reskim_mc reskim_ZToEE_3(ch_ZToEE_3, false, true, false, false) ;
    reskim_ZToEE_3.Loop("ntuples/reskim/ZToEE_powheg_M_200_400_mc.root") ;
    reskim_mc reskim_ZToEE_4(ch_ZToEE_4, false, true, false, false) ;
    reskim_ZToEE_4.Loop("ntuples/reskim/ZToEE_powheg_M_400_800_mc.root") ;
    reskim_mc reskim_ZToEE_5(ch_ZToEE_5, false, true, false, false) ;
    reskim_ZToEE_5.Loop("ntuples/reskim/ZToEE_powheg_M_800_1400_mc.root") ;
    reskim_mc reskim_ZToEE_6(ch_ZToEE_6, false, true, false, false) ;
    reskim_ZToEE_6.Loop("ntuples/reskim/ZToEE_powheg_M_1400_2300_mc.root") ;
    reskim_mc reskim_ZToEE_7(ch_ZToEE_7, false, true, false, false) ;
    reskim_ZToEE_7.Loop("ntuples/reskim/ZToEE_powheg_M_2300_3500_mc.root") ;
    reskim_mc reskim_ZToEE_8(ch_ZToEE_8, false, true, false, false) ;
    reskim_ZToEE_8.Loop("ntuples/reskim/ZToEE_powheg_M_3500_4500_mc.root") ;
    reskim_mc reskim_ZToEE_9(ch_ZToEE_9, false, true, false, false) ;
    reskim_ZToEE_9.Loop("ntuples/reskim/ZToEE_powheg_M_4500_6000_mc.root") ;
    reskim_mc reskim_ZToEE_10(ch_ZToEE_10, false, true, false, false) ;
    reskim_ZToEE_10.Loop("ntuples/reskim/ZToEE_powheg_M_6000_Inf_mc.root") ;


    reskim_mc reskim_DY_amc_1(ch_DY_amc_1, false, true, false, false) ;
    reskim_DY_amc_1.Loop("ntuples/reskim/DYToEE_amc_100_200_mc.root") ;
    reskim_mc reskim_DY_amc_2(ch_DY_amc_2, false, true, false, false) ;
    reskim_DY_amc_2.Loop("ntuples/reskim/DYToEE_amc_200_400_mc.root") ;
    reskim_mc reskim_DY_amc_3(ch_DY_amc_3, false, true, false, false) ;
    reskim_DY_amc_3.Loop("ntuples/reskim/DYToEE_amc_400_500_mc.root") ;
    reskim_mc reskim_DY_amc_4(ch_DY_amc_4, false, true, false, false) ;
    reskim_DY_amc_4.Loop("ntuples/reskim/DYToEE_amc_500_700_mc.root") ;
    reskim_mc reskim_DY_amc_5(ch_DY_amc_5, false, true, false, false) ;
    reskim_DY_amc_5.Loop("ntuples/reskim/DYToEE_amc_700_800_mc.root") ;
    reskim_mc reskim_DY_amc_6(ch_DY_amc_6, false, true, false, false) ;
    reskim_DY_amc_6.Loop("ntuples/reskim/DYToEE_amc_800_1000_mc.root") ;
    reskim_mc reskim_DY_amc_7(ch_DY_amc_7, false, true, false, false) ;
    reskim_DY_amc_7.Loop("ntuples/reskim/DYToEE_amc_1000_1500_mc.root") ;
    reskim_mc reskim_DY_amc_8(ch_DY_amc_8, false, true, false, false) ;
    reskim_DY_amc_8.Loop("ntuples/reskim/DYToEE_amc_1500_2000_mc.root") ;
    reskim_mc reskim_DY_amc_9(ch_DY_amc_9, false, true, false, false) ;
    reskim_DY_amc_9.Loop("ntuples/reskim/DYToEE_amc_2000_3000_mc.root") ;

  }
  
}

