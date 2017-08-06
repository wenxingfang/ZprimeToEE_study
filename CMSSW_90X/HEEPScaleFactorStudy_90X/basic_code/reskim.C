#define reskim_cxx
#include "reskim.h"
#include <TH2.h>
#include <TAxis.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TRandom3.h>
#include <TLorentzVector.h>
#include <time.h>
#include <iostream>

#include "turnon.C"
#include "MC_pileup_weight.C"
const float m_el = 0.000511 ;

struct runCounter{
  unsigned int runNumber ;
  int nRaw ;
  int nTriggerMatch ;
  int nHasTAndP ;
  runCounter(int number){
    runNumber = number ;
    nRaw = 0 ;
    nTriggerMatch = 0 ;
    nHasTAndP = 0 ;
  }
  void increment(bool triggerMatch, bool hasTAndP){
    nRaw++ ;
    if(triggerMatch) nTriggerMatch++ ;
    if(hasTAndP    ) nHasTAndP++     ;
  }
  void print(){
    std::cout << Form("%6d   %6d  %6d  %6d  %5.2f%%", runNumber, nRaw, nTriggerMatch, nHasTAndP, 100.0*nHasTAndP/nRaw) << std::endl ;
  }
};

struct electron_candidate{
  float Et     ;
  float eta    ;
  float phi    ;
  int   Et35   ;
  int   Et20   ;
  int   charge ;
  int   region ;
  
  int pass_HLT_Ele32_Filter  ;
  int pass_HLT_Ele32_L1_Filter  ;
  int pass_HLT_Ele32_L1_Filter_v1  ;
  int pass_HLT_Ele32_L1_Filter_v2  ;
  int pass_HLT_Ele35_Filter  ;
  
  int accept_core_ID        ;
  int accept_core_ID_tight        ;
  int accept_isolation      ;
  int accept_isolation_tight      ;
  int accept_tag_ID         ;
  int accept_tag_ID_tight         ;
  int accept_noEcalDriven_ID    ;
  int accept_noDPhiIn_ID   ;
  int accept_noShower_ID   ;
  int accept_noTrkIso_ID   ;
  int accept_noEMHD1Iso_ID ;
  int accept_noMissHit_ID  ;
  int accept_noDxy_ID      ;
  int accept_noHoE_ID      ;
  int accept_noDEtaIn_ID    ;
  int accept_noDEtaIn_ID_barrel    ;
  int accept_noDEtaIn_ID_endcap    ;
  int accept_EcalDriven_ID  ;
  int accept_noIsolation_ID ;
  int accept_noTrk_ID      ;
  int accept_nominal_ID     ;
  int isTag                 ;
  int isTag_tight                 ;
  int accept_PreSelection;
  int accept_HEEP_ID    ; 

  int accept_HOverE          ;
  int accept_E1x5OverE5x5    ;
  int accept_E2x5OverE5x5    ;
  int accept_showershape     ;
  int accept_Sieie           ;
  int accept_EcalDriven      ;
  int accept_dEtaIn          ;
  int accept_dPhiIn          ;
  int accept_isolEMHadDepth1 ;
  int accept_IsolPtTrks      ;
  int accept_missingHits     ;
  int accept_dxyFirstPV      ;

  float value_out_HOverE          ;
  float value_out_E1x5OverE5x5    ;
  float value_out_E2x5OverE5x5    ;
  float value_out_Sieie           ;
  float value_out_EcalDriven      ;
  float value_out_dEtaIn          ;
  float value_out_dPhiIn          ;
  float value_out_isolEMHadDepth1 ;
  float value_out_IsolPtTrks      ;
  float value_out_missingHits     ;
  float value_out_dxyFirstPV      ;
  float value_out_EM      ;
  float value_out_HD1      ;

 
  TLorentzVector p4 ;
  
  electron_candidate(float Et_in, float eta_in, float phi_in, int charge_in){
    Et     = Et_in     ;
    eta    = eta_in    ;
    phi    = phi_in    ;
    charge = charge_in ;
    p4.SetPtEtaPhiM(Et, eta, phi, m_el) ;
    
    region = 0 ;
    if     (fabs(eta)<1.4442){ region = 1 ; }
    else if(fabs(eta)<1.566 ){ region = 2 ; }
    else if(fabs(eta)<2.5   ){ region = 3 ; }
    else{ region = 4 ; }
    
    Et20 = (Et >= 20.0) ;
    Et35 = (Et >= 35.0) ;
    
    pass_HLT_Ele32_Filter    = 0 ;
    pass_HLT_Ele32_L1_Filter =0  ;
    pass_HLT_Ele32_L1_Filter_v1 =0  ;
    pass_HLT_Ele32_L1_Filter_v2 =0  ;
    pass_HLT_Ele35_Filter    =0  ;
    
    accept_core_ID        = 0 ;
    accept_core_ID_tight        = 0 ;
    accept_isolation      = 0 ;
    accept_isolation_tight      = 0 ;
    accept_tag_ID         = 0 ;
    accept_tag_ID_tight         = 0 ;
    accept_noEcalDriven_ID    = 0 ;
    accept_noDPhiIn_ID   =0;
    accept_noShower_ID   =0;
    accept_noTrkIso_ID   =0;
    accept_noEMHD1Iso_ID =0;
    accept_noMissHit_ID  =0;
    accept_noDxy_ID      =0;
    accept_noHoE_ID      =0;
    accept_noDEtaIn_ID    = 0 ;
    accept_noDEtaIn_ID_barrel    = 0 ;
    accept_noDEtaIn_ID_endcap    = 0 ;
    accept_EcalDriven_ID  = 0 ;
    accept_noIsolation_ID = 0 ;
    accept_noTrk_ID      = 0 ;
    accept_nominal_ID     = 0 ;
    isTag                 = 0 ;
    isTag_tight                 = 0 ;
    accept_PreSelection   =0;
    accept_HEEP_ID        =0;

    accept_HOverE          = 0 ;
    accept_E1x5OverE5x5    = 0 ;
    accept_E2x5OverE5x5    = 0 ;
    accept_showershape     = 0 ;
    accept_Sieie           = 0 ;
    accept_EcalDriven      = 0 ;
    accept_dEtaIn          = 0 ;
    accept_dPhiIn          = 0 ;
    accept_isolEMHadDepth1 = 0 ;
    accept_IsolPtTrks      = 0 ;
    accept_missingHits     = 0 ;
    accept_dxyFirstPV      = 0 ;

    value_out_HOverE          = 0 ;
    value_out_E1x5OverE5x5    = 0 ;
    value_out_E2x5OverE5x5    = 0 ;
    value_out_Sieie           = 0 ;
    value_out_EcalDriven      = 0 ;
    value_out_dEtaIn          = 0 ;
    value_out_dPhiIn          = 0 ;
    value_out_isolEMHadDepth1 = 0 ;
    value_out_IsolPtTrks      = 0 ;
    value_out_missingHits     = 0 ;
    value_out_dxyFirstPV      = 0 ;
    value_out_EM       = 0 ;
    value_out_HD1      = 0 ;

  }
  

  void apply_ID_value(float value_dPhiIn, float value_Sieie, float value_missingHits, float value_dxyFirstPV, float value_HOverE, float value_scEnergy, float value_E1x5OverE5x5, float value_E2x5OverE5x5, float value_isolEMHadDepth1, float value_IsolPtTrks, float value_EcalDriven, float value_dEtaIn, float rho, float value_EM, float value_HD1){

    value_out_HOverE          = value_HOverE ;
    value_out_E1x5OverE5x5    = value_E1x5OverE5x5 ;
    value_out_E2x5OverE5x5    = value_E2x5OverE5x5 ;
    value_out_Sieie           = value_Sieie ;
    value_out_EcalDriven      = value_EcalDriven ;
    value_out_dEtaIn          = value_dEtaIn ;
    value_out_dPhiIn          = value_dPhiIn ;
    value_out_isolEMHadDepth1 = value_isolEMHadDepth1 ;
    value_out_IsolPtTrks      = value_IsolPtTrks ;
    value_out_missingHits     = value_missingHits ;
    value_out_dxyFirstPV      = value_dxyFirstPV ;
    value_out_EM              = value_EM ;
    value_out_HD1             = value_HD1 ;


    if     (region==1){ accept_HOverE = (value_HOverE < 0.05 + 1.0/value_scEnergy) ? 1 : 0 ; } 
    else if(region==3){ accept_HOverE = (value_HOverE < 0.05 + 5.0/value_scEnergy) ? 1 : 0 ; }
    accept_E1x5OverE5x5  = value_E1x5OverE5x5 > 0.83 ? 1 : 0 ;
    accept_E2x5OverE5x5  = value_E2x5OverE5x5 > 0.94 ? 1 : 0 ;
    accept_showershape   = (accept_E1x5OverE5x5 || accept_E2x5OverE5x5) ? 1 : 0 ;
    if(region!=1) accept_showershape = 1 ;
    accept_Sieie = value_Sieie < 0.03 ? 1 : 0;
    if(region!=3) accept_Sieie = 1;
    accept_EcalDriven = value_EcalDriven == 1.0 ? 1 : 0 ;
    accept_dEtaIn = (fabs(value_dEtaIn) < 0.004 && region==1) || ( fabs(value_dEtaIn) < 0.006 && region==3) ? 1 : 0 ;
    accept_dPhiIn = (fabs(value_dPhiIn) < 0.06  && region==1) || ( fabs(value_dPhiIn) < 0.06  && region==3) ? 1 : 0 ;
    if     (region==1) accept_isolEMHadDepth1 = ( value_isolEMHadDepth1 < 2+ 0.03*Et + 0.28*rho ) ? 1 : 0 ;
    else if(region==3) accept_isolEMHadDepth1 = (((value_isolEMHadDepth1 < 2.5 + 0.28*rho) && Et<50) || ((value_isolEMHadDepth1 < 2.5 + 0.03*(Et-50) + 0.28*rho) && Et>50) ) ? 1 : 0 ;
    accept_IsolPtTrks = value_IsolPtTrks < 5 ? 1 : 0 ;
    accept_missingHits = value_missingHits < 2 ? 1 : 0 ;
    if     (region==1) accept_dxyFirstPV = fabs(value_dxyFirstPV) < 0.02 ? 1 : 0 ;
    else if(region==3) accept_dxyFirstPV = fabs(value_dxyFirstPV) < 0.05 ? 1 : 0 ;
  
    accept_core_ID         = (accept_dPhiIn && accept_Sieie && accept_missingHits && accept_dxyFirstPV && accept_HOverE && accept_showershape) ? 1 : 0 ;
    accept_isolation       = (accept_isolEMHadDepth1 && accept_IsolPtTrks) ? 1 : 0 ;
    accept_tag_ID          = (accept_core_ID && accept_isolation && accept_EcalDriven && accept_dEtaIn) ? 1 : 0 ;
    accept_noEcalDriven_ID = (accept_core_ID && accept_isolation &&                      accept_dEtaIn) ? 1 : 0 ;
    accept_noDPhiIn_ID     = (accept_Sieie && accept_missingHits && accept_dxyFirstPV && accept_HOverE && accept_showershape && accept_isolation && accept_EcalDriven && accept_dEtaIn) ? 1 : 0 ;
    accept_noShower_ID     = (accept_dPhiIn && accept_missingHits && accept_dxyFirstPV && accept_HOverE && accept_isolation && accept_EcalDriven && accept_dEtaIn) ? 1 : 0 ;
    accept_noTrkIso_ID     = (accept_core_ID && accept_isolEMHadDepth1 && accept_EcalDriven && accept_dEtaIn) ? 1 : 0 ;
    accept_noEMHD1Iso_ID   = (accept_core_ID && accept_IsolPtTrks && accept_EcalDriven && accept_dEtaIn) ? 1 : 0 ;
    accept_noMissHit_ID    = (accept_dPhiIn && accept_Sieie && accept_dxyFirstPV && accept_HOverE && accept_showershape && accept_isolation && accept_EcalDriven && accept_dEtaIn) ? 1 : 0 ;
    accept_noDxy_ID        = (accept_dPhiIn && accept_Sieie && accept_missingHits && accept_HOverE && accept_showershape && accept_isolation && accept_EcalDriven && accept_dEtaIn) ? 1 : 0 ;
    accept_noHoE_ID        = (accept_dPhiIn && accept_Sieie && accept_missingHits && accept_dxyFirstPV && accept_showershape && accept_isolation && accept_EcalDriven && accept_dEtaIn) ? 1 : 0 ;
    accept_noDEtaIn_ID     = (accept_core_ID && accept_isolation && accept_EcalDriven                 ) ? 1 : 0 ;
    accept_noIsolation_ID  = (accept_core_ID &&                     accept_EcalDriven && accept_dEtaIn) ? 1 : 0 ;
    accept_noTrk_ID        = (accept_Sieie && accept_missingHits && accept_HOverE && accept_showershape && accept_isolation && accept_EcalDriven) ? 1 : 0;                                                           accept_nominal_ID      = (accept_tag_ID                                                           ) ? 1 : 0 ;
    
    if(region==1) accept_noDEtaIn_ID_barrel = accept_noDEtaIn_ID ;
    else accept_noDEtaIn_ID_barrel= accept_nominal_ID;

    if(region==3) accept_noDEtaIn_ID_endcap = accept_noDEtaIn_ID ;
    else accept_noDEtaIn_ID_endcap= accept_nominal_ID;

    accept_EcalDriven_ID   = accept_EcalDriven ;
//    accept_HEEP_ID = (Et>35 && accept_tag_ID ) ? 1 : 0 ;
//    isTag = (Et>35 && region==1 && accept_tag_ID && pass_HLT_Ele32_Filter) ? 1 : 0 ;
    isTag = (Et>35 && region==1 && accept_tag_ID ) ? 1 : 0 ;

}

void Pass_PreSelection(float value_Sieie, float value_HOverE, float value_missingHits, float value_dxyFirstPV){
bool accept_sieie = false;
if(region==1) accept_sieie = value_Sieie < 0.013 ? 1 : 0 ;
else if(region==3) accept_sieie = value_Sieie < 0.034 ? 1 : 0 ;
bool accept_HoverE = false;
if(region==1) accept_HoverE = value_HOverE < 0.15 ? 1 : 0 ;
else if(region==3) accept_HoverE = value_HOverE < 0.1 ? 1 : 0 ;
bool accept_missHit = false;
if(region==1 || region==3) accept_missHit = value_missingHits < 2 ? 1 : 0 ;
bool accept_dxy = false;
if(region==1) accept_dxy = fabs(value_dxyFirstPV) < 0.02 ? 1 : 0 ;
else if(region==3) accept_dxy = fabs(value_dxyFirstPV) < 0.05 ? 1 : 0 ;
accept_PreSelection = (accept_sieie && accept_HoverE && accept_missHit && accept_dxy) ? 1 : 0 ;
}

};

void displayProgress(long current, long max){
  using std::cerr;

  if (current % (max / 1000) != 0) return;

  int width = 40; // Hope the terminal is at least that wide.

  int barWidth = width - 2;
  cerr << "\x1B[2K"; // Clear line
  cerr << "\x1B[2000D"; // Cursor left
  cerr << '[';
  for(int i=0 ; i<barWidth ; ++i){ if(i<barWidth*current/max){ cerr << '=' ; }else{ cerr << ' ' ; } }
  cerr << ']';
  cerr << " " << Form("%8d/%8d (%5.2f%%)", (int)current, (int)max, 100.8*current/max) ;
  cerr.flush();
}



void reskim::Loop(TString fname){
   if (fChain == 0) return;
   std::cout << fname << std::endl ;
   
   time_t time_start = time(0) ;
   char* time_start_text = ctime(&time_start) ;
   std::cout << time_start_text << std::endl ;

   Long64_t nentries = fChain->GetEntries();
   std::cout << "In:  " << nentries << std::endl ;
   
   TFile file_out(fname,"RECREATE") ;
   TTree tree_out("tap","Streamlined tag and probe") ;
  
   int   ev_run_out; 
   int   ev_sign_out; 
   int   pass_HLT_Ele32_require_out ;
   int   pass_HLT_Ele32_require_v1_out ;
   int   pass_HLT_Ele32_require_v2_out ;
   int   pass_HLT_Ele35_require_out ;



   float mee_out ;
   float Pt_out ;
   int   OS_out ;
   
   int   pv_n_out ;
   int   PU_true_out ;
   float w_PU_golden_out ;
   float w_PU_silver_out ;
   float w_PU_silver_up_out ;
   float w_PU_silver_down_out ;
   float w_PU_combined_out ;
   
   float tag_Et_out ;
   float tag_eta_out ;
   float tag_phi_out ;
   int   tag_Et35_out ;
   int   tag_Et20_out ;
   int   tag_charge_out ;
   int   tag_region_out ;
   int   tag_ID_tag_out ;
   int   tag_ID_noDEtaIn_out ;
   int   tag_ID_EcalDriven_out ;
   int   tag_ID_noIsolation_out ;
   int   tag_ID_nominal_out ;
   int   tag_isTag_out ;
   int   tag_truthmatched_out ;
   int   tag_PreSelection_out ; 
   int   tag_passtrigger_out; 
   float tag_DeltaR;

   float probe_Et_out ;
   float probe_eta_out ;
   float probe_phi_out ;
   int   probe_Et35_out ;
   int   probe_Et20_out ;
   int   probe_charge_out ;
   int   probe_region_out ;
   int   probe_ID_tag_out ;
   int   probe_ID_noEcalDriven_out ;
   int   probe_ID_noDPhiIn_out   ;
   int   probe_ID_noShower_out   ;
   int   probe_ID_noTrkIso_out   ;
   int   probe_ID_noEMHD1Iso_out ;
   int   probe_ID_noMissHit_out  ;
   int   probe_ID_noDxy_out      ;
   int   probe_ID_noHoE_out      ;
   int   probe_ID_noDEtaIn_out ;
   int   probe_ID_noDEtaIn_barrel_out ;
   int   probe_ID_noDEtaIn_endcap_out ;
   int   probe_ID_EcalDriven_out ;
   int   probe_ID_noIsolation_out ;
   int   probe_ID_noTrk_out ;
   int   probe_ID_nominal_out ;
   int   probe_isTag_out ;
   int   probe_truthmatched_out ;
   int   probe_PreSelection_out;
   int   probe_passtrigger_out; 
   float probe_DeltaR;

   int probe_HOverE         ;
   int probe_E1x5OverE5x5   ;
   int probe_E2x5OverE5x5   ;
   int probe_showershape    ;
   int probe_Sieie          ;
   int probe_EcalDriven     ;
   int probe_dEtaIn         ;
   int probe_dPhiIn         ;
   int probe_isolEMHadDepth1;
   int probe_IsolPtTrks     ;
   int probe_missingHits    ;
   int probe_dxyFirstPV     ;

   float probe_value_HOverE         ;
   float probe_value_E1x5OverE5x5   ;
   float probe_value_E2x5OverE5x5   ;
   float probe_value_Sieie          ;
   float probe_value_EcalDriven     ;
   float probe_value_dEtaIn         ;
   float probe_value_dPhiIn         ;
   float probe_value_isolEMHadDepth1;
   float probe_value_IsolPtTrks     ;
   float probe_value_oldIsolPtTrks  ;
   float probe_value_missingHits    ;
   float probe_value_dxyFirstPV     ;
   float probe_value_EM             ;
   float probe_value_HD1            ;


   // These variables keep track of how many Z->ee candidates we have in the event.
   int Zee_index_out ;
   int tag_index_out ;
   int probe_index_out ;
   
   tree_out.Branch("Z_index", &Zee_index_out  , "Z_index/I") ;
   tree_out.Branch("t_index", &tag_index_out  , "t_index/I") ;
   tree_out.Branch("p_index", &probe_index_out, "p_index/I") ;
   
   tree_out.Branch("ev_run"   , &ev_run_out   , "ev_run/I"  ) ;
   tree_out.Branch("ev_sign"   , &ev_sign_out   , "ev_sign/I"  ) ;
   tree_out.Branch("pass_HLT_Ele32_require"   , &pass_HLT_Ele32_require_out   , "pass_HLT_Ele32_require/I"  ) ;
   tree_out.Branch("pass_HLT_Ele32_require_v1"   , &pass_HLT_Ele32_require_v1_out   , "pass_HLT_Ele32_require_v1/I"  ) ;
   tree_out.Branch("pass_HLT_Ele32_require_v2"   , &pass_HLT_Ele32_require_v2_out   , "pass_HLT_Ele32_require_v2/I"  ) ;
   tree_out.Branch("pass_HLT_Ele35_require"   , &pass_HLT_Ele35_require_out   , "pass_HLT_Ele35_require/I"  ) ;
   tree_out.Branch("mee"      , &mee_out      , "mee/F"     ) ;
   tree_out.Branch("Pt"      , &Pt_out        , "Pt/F"      ) ;
   tree_out.Branch("OS"       , &OS_out       , "OS/I"       ) ;
   
   tree_out.Branch("pv_n"   , &pv_n_out, "pv_n/I") ;
   tree_out.Branch("PU_true", &PU_true_out , "PU_true/I"  ) ;
   
   tree_out.Branch("w_PU_golden"         , &w_PU_golden_out          , "w_PU_golden/F"          ) ;
   tree_out.Branch("w_PU_silver"         , &w_PU_silver_out          , "w_PU_silver/F"          ) ;
   tree_out.Branch("w_PU_silver_down"    , &w_PU_silver_down_out     , "w_PU_silver_down/F"     ) ;
   tree_out.Branch("w_PU_silver_up"      , &w_PU_silver_up_out       , "w_PU_silver_up/F"       ) ;
   tree_out.Branch("w_PU_combined"       , &w_PU_combined_out        , "w_PU_combined/F"        ) ;
   
   tree_out.Branch("t_Et"    , &tag_Et_out    , "t_Et/F"    ) ;
   tree_out.Branch("t_eta"   , &tag_eta_out   , "t_eta/F"   ) ;
   tree_out.Branch("t_phi"   , &tag_phi_out   , "t_phi/F"   ) ;
   tree_out.Branch("t_Et35"  , &tag_Et35_out  , "t_Et35/I"  ) ;
   tree_out.Branch("t_Et20"  , &tag_Et20_out  , "t_Et20/I"  ) ;
   tree_out.Branch("t_charge", &tag_charge_out, "t_charge/I") ;
   tree_out.Branch("t_region", &tag_region_out, "t_region/I") ;
   
   tree_out.Branch("t_ID_tag"        , &tag_ID_tag_out        , "t_ID_tag/I"        ) ;
   tree_out.Branch("t_ID_nominal"    , &tag_ID_nominal_out    , "t_ID_nominal/I"    ) ;
   tree_out.Branch("t_PreSelection"  , &tag_PreSelection_out  , "t_PreSelection/I"    ) ;
   tree_out.Branch("t_passtrigger"   , &tag_passtrigger_out   , "t_passtrigger/I"  ) ;
   tree_out.Branch("t_DeltaR"   , &tag_DeltaR   , "t_DeltaR/F"  ) ;
   
   tree_out.Branch("p_Et"    , &probe_Et_out    , "p_Et/F"    ) ;
   tree_out.Branch("p_eta"   , &probe_eta_out   , "p_eta/F"   ) ;
   tree_out.Branch("p_phi"   , &probe_phi_out   , "p_phi/F"   ) ;
   tree_out.Branch("p_Et35"  , &probe_Et35_out  , "p_Et35/I"  ) ;
   tree_out.Branch("p_Et20"  , &probe_Et20_out  , "p_Et20/I"  ) ;
   tree_out.Branch("p_charge", &probe_charge_out, "p_charge/I") ;
   tree_out.Branch("p_region", &probe_region_out, "p_region/I") ;
   tree_out.Branch("p_DeltaR", &probe_DeltaR    , "p_DeltaR/F"  ) ;
   
   tree_out.Branch("p_ID_tag"        , &probe_ID_tag_out        , "p_ID_tag/I"        ) ;
   tree_out.Branch("p_ID_noEcalDriven", &probe_ID_noEcalDriven_out   , "p_ID_noEcalDriven/I"   ) ;
   tree_out.Branch("p_ID_noDPhiIn"   , &probe_ID_noDPhiIn_out   , "p_ID_noDPhiIn/I"   ) ;
   tree_out.Branch("p_ID_noShower"   , &probe_ID_noShower_out   , "p_ID_noShower/I"   ) ;
   tree_out.Branch("p_ID_noTrkIso"   , &probe_ID_noTrkIso_out   , "p_ID_noTrkIso/I"   ) ;
   tree_out.Branch("p_ID_noEMHD1Iso" , &probe_ID_noEMHD1Iso_out , "p_ID_noEMHD1Iso/I"   ) ;
   tree_out.Branch("p_ID_noMissHit"  , &probe_ID_noMissHit_out  , "p_ID_noMissHit/I"   ) ;
   tree_out.Branch("p_ID_noDxy"      , &probe_ID_noDxy_out      , "p_ID_noDxy/I"   ) ;
   tree_out.Branch("p_ID_noHoE"      , &probe_ID_noHoE_out      , "p_ID_noHoE/I"   ) ;
   tree_out.Branch("p_ID_noDEtaIn"   , &probe_ID_noDEtaIn_out   , "p_ID_noDEtaIn/I"   ) ;
   tree_out.Branch("p_ID_noDEtaIn_barrel", &probe_ID_noDEtaIn_barrel_out   , "p_ID_noDEtaIn_barrel/I"   ) ;
   tree_out.Branch("p_ID_noDEtaIn_endcap", &probe_ID_noDEtaIn_endcap_out   , "p_ID_noDEtaIn_endcap/I"   ) ;
   tree_out.Branch("p_ID_EcalDriven" , &probe_ID_EcalDriven_out , "p_ID_EcalDriven/I" ) ;
   tree_out.Branch("p_ID_noIsolation", &probe_ID_noIsolation_out, "p_ID_noIsolation/I") ;
   tree_out.Branch("p_ID_noTrk"      , &probe_ID_noTrk_out      , "p_ID_noTrk/I") ;
   tree_out.Branch("p_ID_nominal"    , &probe_ID_nominal_out    , "p_ID_nominal/I"    ) ;
   tree_out.Branch("p_PreSelection"  , &probe_PreSelection_out    , "p_PreSelection/I"    ) ;
   tree_out.Branch("p_passtrigger"   , &probe_passtrigger_out  , "p_passtrigger/I"  ) ;
  

   tree_out.Branch("p_E1x5OverE5x5"   , & probe_E1x5OverE5x5   , "p_E1x5OverE5x5/I"    );
   tree_out.Branch("p_E2x5OverE5x5"   , & probe_E2x5OverE5x5   , "p_E2x5OverE5x5/I"    );
   tree_out.Branch("p_HOverE"         , & probe_HOverE         , "p_HOverE/I"          );
   tree_out.Branch("p_showershape"    , & probe_showershape    , "p_showershape/I"     );
   tree_out.Branch("p_Sieie"          , & probe_Sieie          , "p_Sieie/I"           );
   tree_out.Branch("p_EcalDriven"     , & probe_EcalDriven     , "p_EcalDriven/I"      );
   tree_out.Branch("p_dEtaIn"         , & probe_dEtaIn         , "p_dEtaIn/I"          );
   tree_out.Branch("p_dPhiIn"         , & probe_dPhiIn         , "p_dPhiIn/I"          );
   tree_out.Branch("p_isolEMHadDepth1", & probe_isolEMHadDepth1, "p_isolEMHadDepth1/I" );
   tree_out.Branch("p_IsolPtTrks"     , & probe_IsolPtTrks     , "p_IsolPtTrks/I"      );
   tree_out.Branch("p_missingHits"    , & probe_missingHits    , "p_missingHits/I"     );
   tree_out.Branch("p_dxyFirstPV"     , & probe_dxyFirstPV     , "p_dxyFirstPV/I"      );

   tree_out.Branch("p_value_HOverE"         , & probe_value_HOverE         , "p_value_HOverE/F"          );
   tree_out.Branch("p_value_E1x5OverE5x5"   , & probe_value_E1x5OverE5x5   , "p_value_E1x5OverE5x5/F"    );
   tree_out.Branch("p_value_E2x5OverE5x5"   , & probe_value_E2x5OverE5x5   , "p_value_E2x5OverE5x5/F"    );
   tree_out.Branch("p_value_Sieie"          , & probe_value_Sieie          , "p_value_Sieie/F"           );
   tree_out.Branch("p_value_EcalDriven"     , & probe_value_EcalDriven     , "p_value_EcalDriven/F"      );
   tree_out.Branch("p_value_dEtaIn"         , & probe_value_dEtaIn         , "p_value_dEtaIn/F"          );
   tree_out.Branch("p_value_dPhiIn"         , & probe_value_dPhiIn         , "p_value_dPhiIn/F"          );
   tree_out.Branch("p_value_isolEMHadDepth1", & probe_value_isolEMHadDepth1, "p_value_isolEMHadDepth1/F" );
   tree_out.Branch("p_value_IsolPtTrks"     , & probe_value_IsolPtTrks     , "p_value_IsolPtTrks/F"      );
   tree_out.Branch("p_value_missingHits"    , & probe_value_missingHits    , "p_value_missingHits/F"     );
   tree_out.Branch("p_value_dxyFirstPV"     , & probe_value_dxyFirstPV     , "p_value_dxyFirstPV/F"      );
   tree_out.Branch("p_value_EM"             , & probe_value_EM             , "p_value_EM/F"              );
   tree_out.Branch("p_value_HD1"            , & probe_value_HD1            , "p_value_HD1/F"             );


   TH1F *h_pv_n=new TH1F("pv_n_Allprobe","",50,0,50); 
   TH1F *h_pv_n_B=new TH1F("pv_n_Allprobe_barrel","",50,0,50); 
   TH1F *h_pv_n_E=new TH1F("pv_n_Allprobe_endcap","",50,0,50); 

   std::vector<runCounter> runs ;
   
   TRandom3 rand ;
   Long64_t nbytes = 0, nb = 0;
//nentries=200;
   bool do_fakeRate=false;
   bool do_EnergyCorrect=false;
   if(isData==false) do_EnergyCorrect=false;
   for (Long64_t jentry=0; jentry<nentries;jentry++){
//   displayProgress(jentry, nentries) ;
//   std::cout<<"event="<<jentry<<std::endl;     
   //######## init trigger #######
   trig_Ele32_accept=-1;
   trig_Ele35_accept=-1;
   //#############################
   Long64_t ientry = LoadTree(jentry);
   if (ientry < 0) break;
   nb = fChain->GetEntry(jentry);   
   nbytes += nb;
   if(ev_fixedGridRhoFastjetAll==-999) continue;
//   if(isData==true){ {if (ev_run<=0 || ev_run<Run_low || ev_run>Run_high) continue;}
//                   }
      float w_sign = mc_w_sign < 0 ? -1 : 1 ;

      if(true==isZToTT){
      bool accept_event = true ;
      bool has_taup = false ;
      bool has_taum = false ;
      bool has_mup = false ;
      bool has_mum = false ;
      for(unsigned iMC=0 ; iMC<mc_n ; ++iMC){
      if(mc_pdgId->at(iMC)== 15) has_taum = true ;
      if(mc_pdgId->at(iMC)==-15) has_taup = true ;
      if(mc_pdgId->at(iMC)== 13) has_mum = true ;
      if(mc_pdgId->at(iMC)==-13) has_mup = true ;
/*
      if(has_taup && has_taum){
         accept_event = true ;
            break ;
                              }
*/

      if( (has_taup && has_taum) || (has_mum && has_mup)){
         accept_event = false ;
            break ;
                              }

                                           }
      if(accept_event==false) continue ;
       }

      if(true==isZToEE || true==isWJets){
      TLorentzVector MC_p4_1(1,0,0,0);
      TLorentzVector MC_p4_2(1,0,0,0);
      float Pt_treshold=0;
      bool accept=true;
      if(true==isZToEE) Pt_treshold=50;
      if(true==isWJets) Pt_treshold=100;
      
      for(unsigned iMC=0 ; iMC<mc_n ; ++iMC){
      if( (abs(mc_pdgId->at(iMC)) <11 || abs(mc_pdgId->at(iMC)) >16) ) continue;
      MC_p4_1.SetPtEtaPhiM(mc_pt->at(iMC),mc_eta->at(iMC),mc_phi->at(iMC),mc_mass->at(iMC)) ;
      for(unsigned jMC=iMC+1 ; jMC<mc_n ; ++jMC){
      if( (abs(mc_pdgId->at(jMC)) <11 || abs(mc_pdgId->at(jMC)) >16) ) continue;
      MC_p4_2.SetPtEtaPhiM(mc_pt->at(jMC),mc_eta->at(jMC),mc_phi->at(jMC),mc_mass->at(jMC)) ;
      if(MC_p4_1.DeltaR(MC_p4_2)<0.001) continue;
      if((MC_p4_1+MC_p4_2).Pt()>Pt_treshold){accept=false; break;}
      }
      if(accept==false) break;
      }      
      if(accept==false) continue;
      }
/*
      if(true==isZToEE || isWJets==true){
      bool accept_event = true ;
      float Pt_threshold=0;
      if(isWJets==true){
      Pt_threshold=100;
      TLorentzVector p4_lepton ;
      TLorentzVector p4_neutrion ;
      bool has_lepton_form_W=false;
      bool has_neutrion_form_W=false;
      bool has_direct_W=false;
      for(unsigned iMC=0 ; iMC<mc_n ; ++iMC){
      if(abs(mc_pdgId->at(iMC))== 24 && (mc_pt->at(iMC)>Pt_threshold) ) {accept_event=false;
                                                                         has_direct_W=true;
                                                                         break;}
      if(has_direct_W==false && (abs(mc_pdgId->at(iMC))==11 || abs(mc_pdgId->at(iMC))==13 || abs(mc_pdgId->at(iMC))==15) && mc_status->at(iMC)==23 ){
                                                                                                                         has_lepton_form_W=true;
                                                                                                                         p4_lepton.SetPtEtaPhiM(mc_pt->at(iMC),mc_eta->at(iMC),mc_phi->at(iMC),mc_mass->at(iMC));
                                                                                                                        }
      if(has_direct_W==false && (abs(mc_pdgId->at(iMC))==12 || abs(mc_pdgId->at(iMC))==14 || abs(mc_pdgId->at(iMC))==16) && mc_status->at(iMC)==23 ){
                                                                                                                       has_neutrion_form_W=true;
                                                                                                                       p4_neutrion.SetPtEtaPhiM(mc_pt->at(iMC),mc_eta->at(iMC),mc_phi->at(iMC),mc_mass->at(iMC));
                                                                                                                       }
                                           }
      if(has_direct_W==false && has_lepton_form_W && has_neutrion_form_W){
                                                                        if((p4_lepton+p4_neutrion).Pt()>Pt_threshold) accept_event=false;
                                                                       }
                      }
      if(isZToEE==true){
      Pt_threshold=100;
      TLorentzVector p4_lepton1 ;
      TLorentzVector p4_lepton2 ;
      bool has_lepton1_form_Z=false;
      bool has_lepton2_form_Z=false;
      bool has_direct_Z=false;
      for(unsigned iMC=0 ; iMC<mc_n ; ++iMC){
      if(abs(mc_pdgId->at(iMC))== 23) std::cout<<"has Z,status="<<mc_pdgId->at(iMC)<<",pt="<<mc_pt->at(iMC)<<std::endl;
      if(abs(mc_pdgId->at(iMC))== 23 && (mc_pt->at(iMC)>Pt_threshold) ) {accept_event=false;
                                                                         has_direct_Z=true;
                                                                         break;}
      if(has_direct_Z==false && (mc_pdgId->at(iMC)==11 || mc_pdgId->at(iMC)==13 || mc_pdgId->at(iMC)==15) && mc_status->at(iMC)==23){
                                                                                                           has_lepton1_form_Z=true;
                                                                                                           p4_lepton1.SetPtEtaPhiM(mc_pt->at(iMC),mc_eta->at(iMC),mc_phi->at(iMC),mc_mass->at(iMC));
                                                                                                          }
      if(has_direct_Z==false && (mc_pdgId->at(iMC)==-11 || mc_pdgId->at(iMC)==-13 || mc_pdgId->at(iMC)==-15) && mc_status->at(iMC)==23){
                                                                                                              has_lepton2_form_Z=true;
                                                                                                              p4_lepton2.SetPtEtaPhiM(mc_pt->at(iMC),mc_eta->at(iMC),mc_phi->at(iMC),mc_mass->at(iMC));
                                                                                                             }
                                           }
      if(has_direct_Z==false && has_lepton1_form_Z && has_lepton2_form_Z){
                                                                        if((p4_lepton1+p4_lepton2).Pt()>Pt_threshold) accept_event=false;
                                                                         }
                      }
      if(accept_event==false) continue ;
       }
*/
      Zee_index_out = 0 ;
      tag_index_out = 0 ;
      pv_n=-1;//no pv_n saved now 
      pv_n_out = pv_n ;
      bool triggerMatch = false ;
      bool hasTAndP     = false ;
      if(true==isData){
        PU_true_out = -1 ;
        // Set weights to 1
        w_PU_golden_out         = 1 ;
        w_PU_silver_out         = 1 ;
        w_PU_silver_down_out    = 1 ;
        w_PU_silver_up_out      = 1 ;
        w_PU_combined_out = 1.0 ;
      }
      else{
        // Set PU weights
        int PU = mc_trueNumInteractions ;
        PU_true_out = PU ;
        w_PU_combined_out      = w_sign*PU_reReco_Morind17::MC_pileup_weight(PU,0,"all");
        w_PU_golden_out        = w_sign*PU_reReco_Morind17::MC_pileup_weight(PU,0,"B2F");
        w_PU_silver_out        = w_sign*PU_reReco_Morind17::MC_pileup_weight(PU,0,"GH" );
        w_PU_silver_down_out   = w_sign*PU_reReco_Morind17::MC_pileup_weight(PU,1,"all");
        w_PU_silver_up_out     = w_sign*PU_reReco_Morind17::MC_pileup_weight(PU,2,"all");
      }
      
      std::vector<electron_candidate*> electrons ;
      for(unsigned int iEl=0 ; iEl<gsf_n ; ++iEl){
        float Et     = gsf_caloEnergy->at(iEl)*sin( gsf_theta->at(iEl) ) ;
        float eta    = gsf_sc_eta->at(iEl);
        if(do_EnergyCorrect==true){
        if(fabs(eta)<1.4441)Et = Et*1.0012 ;
        else if(fabs(eta)>1.566 && fabs(eta)<2.5) Et = Et*1.0089 ;
        }
        float phi    = gsf_phi->at(iEl) ;
        int   charge = gsf_charge->at(iEl) ;
        electron_candidate* el = new electron_candidate(Et, eta, phi, charge) ;
       
 
        if(isData){
          // Match to the trigger.
          if(do_fakeRate==false){
          TLorentzVector trigp4 ;
          if(trig_Ele32_accept!=-1){
          for(unsigned int itrig=0 ; itrig<trig_Ele32_eta->size() ; ++itrig){
            trigp4.SetPtEtaPhiM(100,trig_Ele32_eta->at(itrig),trig_Ele32_phi->at(itrig),10) ;
            if(trigp4.DeltaR(el->p4) < 0.1){
              el->pass_HLT_Ele32_Filter = 1  ;
              break ;
            }
          }//match to HLT last filter
          for(unsigned int itrig=0 ; itrig<trig_Ele32_L1_eta->size() ; ++itrig){
            trigp4.SetPtEtaPhiM(100,trig_Ele32_L1_eta->at(itrig),trig_Ele32_L1_phi->at(itrig),10) ;
            if(trigp4.DeltaR(el->p4) < 0.1){
              el->pass_HLT_Ele32_L1_Filter = 1  ;
              break ;
            }
          }//match to L1 filter
          for(unsigned int itrig=0 ; itrig<trig_Ele32_L1_eta_v1->size() ; ++itrig){
            trigp4.SetPtEtaPhiM(100,trig_Ele32_L1_eta_v1->at(itrig),trig_Ele32_L1_phi_v1->at(itrig),10) ;
            if(trigp4.DeltaR(el->p4) < 0.1){
              el->pass_HLT_Ele32_L1_Filter_v1 = 1  ;
              break ;
            }
          }//match to L1 filter
          for(unsigned int itrig=0 ; itrig<trig_Ele32_L1_eta_v2->size() ; ++itrig){
            trigp4.SetPtEtaPhiM(100,trig_Ele32_L1_eta_v2->at(itrig),trig_Ele32_L1_phi_v2->at(itrig),10) ;
            if(trigp4.DeltaR(el->p4) < 0.1){
              el->pass_HLT_Ele32_L1_Filter_v2 = 1  ;
              break ;
            }
          }//match to L1 filter
          }//HLT_Ele32
          if(trig_Ele35_accept!=-1){
          for(unsigned int itrig=0 ; itrig<trig_Ele35_eta->size() ; ++itrig){
            trigp4.SetPtEtaPhiM(100,trig_Ele35_eta->at(itrig),trig_Ele35_phi->at(itrig),10) ;
            if(trigp4.DeltaR(el->p4) < 0.1){
              el->pass_HLT_Ele35_Filter = 1  ;
              break ;
            }
          }//match to HLT last filter
          }//HLT_Ele35
          }
          else{
            el->pass_HLT_Ele32_Filter   =1;
            el->pass_HLT_Ele32_L1_Filter=1;
            el->pass_HLT_Ele32_L1_Filter_v1=1;
            el->pass_HLT_Ele32_L1_Filter_v2=1;
            el->pass_HLT_Ele35_Filter   =1;
          }
        }//isData
        else{
          el->pass_HLT_Ele32_Filter = trigEle27::passTrig(Et, eta) ;
        }


        float gsf_trkiso=0;
        float gsf_EM=0;
        float gsf_HD1=0;
        gsf_trkiso     = gsf_dr03TkSumPtHEEP7->at(iEl);
        gsf_EM = gsf_dr03EcalRecHitSumEt->at(iEl);
        gsf_HD1 = gsf_dr03HcalDepth1TowerSumEt->at(iEl);

        el->apply_ID_value(fabs(gsf_deltaPhiSuperClusterTrackAtVtx->at(iEl)),
                           gsf_full5x5_sigmaIetaIeta->at(iEl),
                     float(gsf_nLostInnerHits->at(iEl) ),
                      fabs(gsf_dxy_firstPVtx->at(iEl)),
                           gsf_hadronicOverEm->at(iEl),
                           gsf_sc_energy->at(iEl),
                          (gsf_full5x5_e1x5->at(iEl)/gsf_full5x5_e5x5->at(iEl) ),
                          (gsf_full5x5_e2x5Max->at(iEl)/gsf_full5x5_e5x5->at(iEl) ),
                          (gsf_dr03EcalRecHitSumEt->at(iEl) + gsf_dr03HcalDepth1TowerSumEt->at(iEl) ),
                           gsf_trkiso,
                     float(gsf_ecaldrivenSeed->at(iEl) ),
                           fabs(gsf_deltaEtaSeedClusterTrackAtVtx->at(iEl)),
                           ev_fixedGridRhoFastjetAll,
                           gsf_EM,
                           gsf_HD1) ;

        el->Pass_PreSelection(gsf_full5x5_sigmaIetaIeta->at(iEl), gsf_hadronicOverEm->at(iEl), float(gsf_nLostInnerHits->at(iEl) ), fabs(gsf_dxy_firstPVtx->at(iEl))); 
        electrons.push_back(el) ;
      }
       
      for(unsigned int iTag=0 ; iTag<electrons.size() ; ++iTag){
        electron_candidate* tag = electrons.at(iTag) ;
        if(do_fakeRate==false){
        if(false==tag->isTag) continue ;}
        else{
        if(tag->Et <35 || tag->accept_PreSelection==false || tag->accept_tag_ID == true || tag->region != 1 || tag->pass_HLT_Ele32_Filter==0) continue ;
        }
        tag_index_out = iTag ;
        
        tag_Et_out             = tag->Et ;
        tag_eta_out            = tag->eta ;
        tag_phi_out            = tag->phi ;
        tag_Et35_out           = tag->Et35 ;
        tag_Et20_out           = tag->Et20 ;
        tag_charge_out         = tag->charge ;
        tag_region_out         = tag->region ;
        tag_ID_tag_out         = tag->accept_tag_ID ;
        tag_ID_nominal_out     = tag->accept_nominal_ID ;
        tag_PreSelection_out   = tag->accept_PreSelection ;
        tag_isTag_out          = tag->isTag ;
        tag_passtrigger_out    = tag->pass_HLT_Ele32_Filter ;
        triggerMatch = true ;
        
        for(unsigned int iProbe=0 ; iProbe<electrons.size() ; ++iProbe){
          if(iTag==iProbe) continue ;
          electron_candidate* probe = electrons.at(iProbe) ;

          if(do_fakeRate==true){if(probe->accept_tag_ID == true) continue;}
          TLorentzVector Zp4 = tag->p4 + probe->p4 ;
          mee_out = Zp4.M() ;
          Pt_out = sqrt( Zp4.Px()*Zp4.Px() + Zp4.Py()*Zp4.Py());
           
          OS_out = (tag->charge*probe->charge<0) ;
          Zee_index_out++ ;
          probe_index_out = iProbe ;
   
          probe_Et_out             = probe->Et ;
          probe_eta_out            = probe->eta ;
          probe_phi_out            = probe->phi ;
          probe_Et35_out           = probe->Et35 ;
          probe_Et20_out           = probe->Et20 ;
          probe_charge_out         = probe->charge ;
          probe_region_out         = probe->region ;
          probe_ID_tag_out         = probe->accept_tag_ID ;
          probe_ID_noEcalDriven_out= probe->accept_noEcalDriven_ID ;
          probe_ID_noDPhiIn_out    = probe->accept_noDPhiIn_ID     ;
          probe_ID_noShower_out    = probe->accept_noShower_ID     ;
          probe_ID_noTrkIso_out    = probe->accept_noTrkIso_ID     ;
          probe_ID_noEMHD1Iso_out  = probe->accept_noEMHD1Iso_ID   ;
          probe_ID_noMissHit_out   = probe->accept_noMissHit_ID    ;
          probe_ID_noDxy_out       = probe->accept_noDxy_ID        ;
          probe_ID_noHoE_out       = probe->accept_noHoE_ID        ;
          probe_ID_noDEtaIn_out    = probe->accept_noDEtaIn_ID ;
          probe_ID_noDEtaIn_barrel_out = probe->accept_noDEtaIn_ID_barrel ;
          probe_ID_noDEtaIn_endcap_out = probe->accept_noDEtaIn_ID_endcap ;
          probe_ID_EcalDriven_out  = probe->accept_EcalDriven_ID ;
          probe_ID_noIsolation_out = probe->accept_noIsolation_ID ;
          probe_ID_noTrk_out       = probe->accept_noTrk_ID ;
          probe_ID_nominal_out     = probe->accept_nominal_ID ;
          probe_PreSelection_out   = probe->accept_PreSelection ;
          probe_isTag_out          = probe->isTag ;
          probe_passtrigger_out    = probe->pass_HLT_Ele32_Filter ;
          
          probe_HOverE             = probe->accept_HOverE         ;       
          probe_E1x5OverE5x5       = probe->accept_E1x5OverE5x5   ;   
          probe_E2x5OverE5x5       = probe->accept_E2x5OverE5x5   ;
          probe_showershape        = probe->accept_showershape    ;
          probe_Sieie              = probe->accept_Sieie          ;
          probe_EcalDriven         = probe->accept_EcalDriven     ;
          probe_dEtaIn             = probe->accept_dEtaIn         ;
          probe_dPhiIn             = probe->accept_dPhiIn         ;
          probe_isolEMHadDepth1    = probe->accept_isolEMHadDepth1;
          probe_IsolPtTrks         = probe->accept_IsolPtTrks     ;
          probe_missingHits        = probe->accept_missingHits    ;
          probe_dxyFirstPV         = probe->accept_dxyFirstPV     ;

          probe_value_HOverE          = probe->value_out_HOverE        ; 
          probe_value_E1x5OverE5x5    = probe->value_out_E1x5OverE5x5  ; 
          probe_value_E2x5OverE5x5    = probe->value_out_E2x5OverE5x5  ; 
          probe_value_Sieie           = probe->value_out_Sieie         ; 
          probe_value_EcalDriven      = probe->value_out_EcalDriven    ; 
          probe_value_dEtaIn          = probe->value_out_dEtaIn        ; 
          probe_value_dPhiIn          = probe->value_out_dPhiIn        ; 
          probe_value_isolEMHadDepth1 = probe->value_out_isolEMHadDepth1;
          probe_value_IsolPtTrks      = probe->value_out_IsolPtTrks    ; 
          probe_value_missingHits     = probe->value_out_missingHits   ; 
          probe_value_dxyFirstPV      = probe->value_out_dxyFirstPV    ; 
          probe_value_EM              = probe->value_out_EM            ; 
          probe_value_HD1             = probe->value_out_HD1           ; 

 
          hasTAndP = true ;
          ev_run_out               = ev_run;    
          ev_sign_out              = w_sign;    
          int pass_HLT_Ele32_require=(trig_Ele32_accept && tag->pass_HLT_Ele32_Filter && probe->pass_HLT_Ele32_L1_Filter) ? 1 : 0 ;
          int pass_HLT_Ele32_require_v1=(trig_Ele32_accept && tag->pass_HLT_Ele32_Filter && probe->pass_HLT_Ele32_L1_Filter_v1) ? 1 : 0 ;
          int pass_HLT_Ele32_require_v2=(trig_Ele32_accept && tag->pass_HLT_Ele32_Filter && probe->pass_HLT_Ele32_L1_Filter_v2) ? 1 : 0 ;
          int pass_HLT_Ele35_require=(trig_Ele35_accept && tag->pass_HLT_Ele35_Filter ) ? 1 : 0 ;
          pass_HLT_Ele32_require_out=pass_HLT_Ele32_require;
          pass_HLT_Ele32_require_v1_out=pass_HLT_Ele32_require_v1;
          pass_HLT_Ele32_require_v2_out=pass_HLT_Ele32_require_v2;
          pass_HLT_Ele35_require_out=pass_HLT_Ele35_require;
          tree_out.Fill() ;
          if(70<mee_out && mee_out<110 && probe_Et_out>35 ){
                                                            h_pv_n->Fill(pv_n,w_sign);
                                                            if(fabs(probe_eta_out)<1.4442)h_pv_n_B->Fill(pv_n,w_sign); 
                                                            else if(fabs(probe_eta_out)>1.566 && fabs(probe_eta_out)<2.5) h_pv_n_E->Fill(pv_n,w_sign);
                                                           }
        }
      }

      for (std::vector<electron_candidate*>::iterator it = electrons.begin(); it != electrons.end(); it ++){
      if (NULL != *it){
        delete *it; 
        *it = NULL;
                      }
      }
      electrons.clear() ;
      electrons.swap(electrons);
            
      bool foundRun = false ;
      for(unsigned iRun=0 ; iRun<runs.size() ; ++iRun){
        if(runs.at(iRun).runNumber==ev_run){
          foundRun = true ;
          runs.at(iRun).increment(triggerMatch,hasTAndP) ;
          break ;
        }
      }
      if(false==foundRun){
        runCounter rc(ev_run) ;
        rc.increment(triggerMatch,hasTAndP) ;
        runs.push_back(rc) ;
      }
      
   }
   std::cout << std::endl ;
   std::cout << "Out: " << tree_out.GetEntries() << std::endl ;
   file_out.cd();
   h_pv_n->Write();
   h_pv_n_B->Write();
   h_pv_n_E->Write();
   tree_out.Write() ;
   file_out.Close() ;
   
   int nRaw = 0 ;
   int nHasTAndP = 0 ;
   for(unsigned iRun=0 ; iRun<runs.size() ; ++iRun){
      runs.at(iRun).print() ;
      nRaw      += runs.at(iRun).nRaw      ;
      nHasTAndP += runs.at(iRun).nHasTAndP ;
   }
   std::cout << endl ;
   std::cout << Form("%6d  %6d  %5.2f", nRaw, nHasTAndP, 100.0*nHasTAndP/nRaw) << std::cout << endl ;
   std::cout << endl ;
   
   time_t time_end = time(0) ;
   char* time_end_text = ctime(&time_end) ;
   std::cout << time_end_text << std::endl ;
}
