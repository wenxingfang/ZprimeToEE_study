#define reskim_FR_1F_cxx
#include "reskim_FR_1F.h"
#include <TH2.h>
#include <TAxis.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TRandom3.h>
#include <TLorentzVector.h>

#include <time.h>
#include <iostream>

#include "turnonEle33.C"
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
  float gsf_eta;
  float gsf_phi;
  int   Et35   ;
  int   Et20   ;
  int   charge ;
  int   region ;
  
  int truthmatched  ;
  int pass_trigger  ;
  
  int accept_core_ID        ;
  int accept_core_ID_tight        ;
  int accept_isolation      ;
  int accept_isolation_tight      ;
  int accept_tag_ID         ;
  int accept_tag_ID_tight         ;
  int accept_noDEtaIn_ID    ;
  int accept_EcalDriven_ID  ;
  int accept_noIsolation_ID ;
  int accept_nominal_ID     ;
  int isTag                 ;
  int isTag_tight                 ;
  int accept_PreSelection;
  int accept_HEEP_ID    ; 
 
  TLorentzVector p4 ;
  TLorentzVector gsf_p4 ;
 
  float ele_dPhiIn         ; 
  float ele_Sieie          ;
  float ele_missingHits    ;
  float ele_dxyFirstPV     ;
  float ele_HOverE         ;
  float ele_E1x5OverE5x5   ;
  float ele_E2x5OverE5x5   ;
  float ele_isolEMHadDepth1;
  float ele_IsolPtTrks     ;
  float ele_EcalDriven     ;
  float ele_dEtaIn         ;
 
  electron_candidate(float Et_in, float eta_in, float phi_in, float gsf_eta_in, float gsf_phi_in, int charge_in){
    Et     = Et_in     ;
    eta    = eta_in    ;
    phi    = phi_in    ;
    gsf_eta= gsf_eta_in    ;
    gsf_phi= gsf_phi_in    ;
    charge = charge_in ;
    p4.SetPtEtaPhiM(Et, eta, phi, m_el) ;
    gsf_p4.SetPtEtaPhiM(Et, gsf_eta, gsf_phi, m_el) ;
    
    region = 0 ;
    if     (fabs(eta)<1.4442){ region = 1 ; }
    else if(fabs(eta)<1.566 ){ region = 2 ; }
    else if(fabs(eta)<2.5   ){ region = 3 ; }
    else{ region = 4 ; }
    
    Et20 = (Et >= 20.0) ;
    Et35 = (Et >= 35.0) ;
    
    truthmatched = 0 ;
    pass_trigger = 0 ;
    
    accept_core_ID        = 0 ;
    accept_core_ID_tight  = 0 ;
    accept_isolation      = 0 ;
    accept_isolation_tight= 0 ;
    accept_tag_ID         = 0 ;
    accept_tag_ID_tight   = 0 ;
    accept_noDEtaIn_ID    = 0 ;
    accept_EcalDriven_ID  = 0 ;
    accept_noIsolation_ID = 0 ;
    accept_nominal_ID     = 0 ;
    isTag                 = 0 ;
    isTag_tight           = 0 ;
    accept_PreSelection   = 0 ;
    accept_HEEP_ID        = 0 ;

    ele_dPhiIn          = 0;
    ele_Sieie           = 0;
    ele_missingHits     = 0;
    ele_dxyFirstPV      = 0;
    ele_HOverE          = 0;
    ele_E1x5OverE5x5    = 0;
    ele_E2x5OverE5x5    = 0;
    ele_isolEMHadDepth1 = 0;
    ele_IsolPtTrks      = 0;
    ele_EcalDriven      = 0;
    ele_dEtaIn          = 0;

  }
  
  


  void apply_ID_value(float value_dPhiIn, float value_Sieie, float value_missingHits, float value_dxyFirstPV, float value_HOverE, float value_scEnergy, float value_E1x5OverE5x5, float value_E2x5OverE5x5, float value_isolEMHadDepth1, float value_IsolPtTrks, float value_EcalDriven, float value_dEtaIn, float rho){

    ele_dPhiIn          = fabs(value_dPhiIn);
    ele_Sieie           = value_Sieie;
    ele_missingHits     = value_missingHits;
    ele_dxyFirstPV      = fabs(value_dxyFirstPV); 
    ele_HOverE          = value_HOverE;
    ele_E1x5OverE5x5    = value_E1x5OverE5x5;
    ele_E2x5OverE5x5    = value_E2x5OverE5x5; 
    ele_isolEMHadDepth1 = value_isolEMHadDepth1;
    ele_IsolPtTrks      = value_IsolPtTrks;
    ele_EcalDriven      = value_EcalDriven;
    ele_dEtaIn          = fabs(value_dEtaIn);
    
    bool accept_HOverE = true ;
    if     (region==1){ accept_HOverE = value_HOverE < 0.05 + 1.0/value_scEnergy ; } 
    else if(region==3){ accept_HOverE = value_HOverE < 0.05 + 5.0/value_scEnergy ; }
    bool accept_E1x5OverE5x5  = value_E1x5OverE5x5 > 0.83 ;
    bool accept_E2x5OverE5x5  = value_E2x5OverE5x5 > 0.94 ;
    bool accept_showershape   = (accept_E1x5OverE5x5 || accept_E2x5OverE5x5) ;
    if(region!=1) accept_showershape = true ;
    bool accept_Sieie = value_Sieie < 0.03;
    if(region!=3) accept_Sieie = true;
    bool accept_EcalDriven = value_EcalDriven == 1.0 ? 1 : 0 ;
    bool accept_dEtaIn = (fabs(value_dEtaIn) < 0.004 && region==1) || (fabs(value_dEtaIn) < 0.006 && region==3) ? 1 : 0 ;
//    bool accept_dEtaIn = (fabs(value_dEtaIn) < 0.004 && region==1) || (region==3) ? 1 : 0 ;
    bool accept_dPhiIn = (fabs(value_dPhiIn) < 0.06 &&  region==1) || (fabs(value_dPhiIn) < 0.06  && region==3) ? 1 : 0 ;
    bool accept_isolEMHadDepth1 = true;
    if     (region==1) accept_isolEMHadDepth1 = ( value_isolEMHadDepth1 < 2+ 0.03*Et + 0.28*rho ) ? 1 : 0 ;
    else if(region==3) accept_isolEMHadDepth1 = (((value_isolEMHadDepth1 < 2.5 + 0.28*rho) && Et<50) || ((value_isolEMHadDepth1 < 2.5 + 0.03*(Et-50) + 0.28*rho) && Et>50) ) ? 1 : 0 ;
    bool accept_IsolPtTrks = value_IsolPtTrks < 5 ;
    bool accept_missingHits = value_missingHits < 2 ;
    bool accept_dxyFirstPV = true;
    if     (region==1) accept_dxyFirstPV = fabs(value_dxyFirstPV) < 0.02 ? 1 : 0 ;
    else if(region==3) accept_dxyFirstPV = fabs(value_dxyFirstPV) < 0.05 ? 1 : 0 ;
  
    accept_core_ID = (accept_dPhiIn && accept_Sieie && accept_missingHits && accept_dxyFirstPV && accept_HOverE && accept_showershape) ? 1 : 0 ;
    accept_isolation = (accept_isolEMHadDepth1 && accept_IsolPtTrks) ? 1 : 0 ;
    accept_tag_ID          = (accept_core_ID && accept_isolation && accept_EcalDriven && accept_dEtaIn) ? 1 : 0 ;
    accept_noDEtaIn_ID     = (accept_core_ID && accept_isolation && accept_EcalDriven                 ) ? 1 : 0 ;
    accept_noIsolation_ID  = (accept_core_ID &&                     accept_EcalDriven && accept_dEtaIn) ? 1 : 0 ;
    accept_nominal_ID      = (accept_tag_ID                                                           ) ? 1 : 0 ;
    if(region!=3) accept_noDEtaIn_ID = accept_nominal_ID ;
    accept_EcalDriven_ID = accept_EcalDriven ;
    accept_HEEP_ID = (Et>35 && accept_tag_ID && (region==1 || region==3)) ? 1 : 0 ;
    isTag = (Et>35 && region==1 && accept_tag_ID && pass_trigger) ? 1 : 0 ;

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



void reskim_FR_1F::Loop(TString fname){
   if (fChain == 0) return;
   std::cout << fname << std::endl ;
   
   time_t time_start = time(0) ;
   char* time_start_text = ctime(&time_start) ;
   std::cout << time_start_text << std::endl ;

   Long64_t nentries = fChain->GetEntries();
   std::cout << "In:  " << nentries << std::endl ;

   fChain->SetBranchStatus("*",0) ;
   if(isData){
     fChain->SetBranchStatus("trig_HLT_*",1) ;
   }
   else{
     fChain->SetBranchStatus("mc_*",1) ;
   }
   fChain->SetBranchStatus("ev_*"           ,1) ;
   fChain->SetBranchStatus("Zee_*"          ,1) ;
   fChain->SetBranchStatus("pv_n"           ,1) ;
   fChain->SetBranchStatus("gsf*"           ,1) ;
   
   TFile file_out(fname,"RECREATE") ;
   TTree tree_out("Ele","HEEP ele") ;
   
   
   int   pv_n_out     = 0 ;
   int   PU_true_out  = 0 ;
   int   event_sign   = 0 ;
   
   float rho_out        = 0 ;

   float OS_out         = 0 ;
   float mee_out        = 0 ;
   float Pt_out         = 0 ;
   float HEEP1_Et_out   = 0 ;
   float HEEP1_eta_out  = 0 ;
   float HEEP1_phi_out  = 0 ;
   float HEEP2_Et_out   = 0 ;
   float HEEP2_eta_out  = 0 ;
   float HEEP2_phi_out  = 0 ;
   float mee_out_gsf    = 0 ;
   float HEEP1_eta_out_gsf  = 0 ;
   float HEEP1_phi_out_gsf  = 0 ;
   float HEEP2_eta_out_gsf  = 0 ;
   float HEEP2_phi_out_gsf  = 0 ;
  
   float w_PU_combined_out    = 0 ;
   float w_PU_golden_out      = 0 ; 
   float w_PU_silver_out      = 0 ;
   float w_PU_silver_down_out = 0 ; 
   float w_PU_silver_up_out   = 0 ;
 
   float e1_dPhiIn           = 0 ;
   float e1_Sieie            = 0 ;
   float e1_missingHits      = 0 ;
   float e1_dxyFirstPV       = 0 ;
   float e1_HOverE           = 0 ;
   float e1_E1x5OverE5x5     = 0 ;
   float e1_E2x5OverE5x5     = 0 ;
   float e1_isolEMHadDepth1  = 0 ;
   float e1_IsolPtTrks       = 0 ;
   float e1_EcalDriven       = 0 ;
   float e1_dEtaIn           = 0 ;
   float e2_dPhiIn           = 0 ;
   float e2_Sieie            = 0 ;
   float e2_missingHits      = 0 ;
   float e2_dxyFirstPV       = 0 ;
   float e2_HOverE           = 0 ;
   float e2_E1x5OverE5x5     = 0 ;
   float e2_E2x5OverE5x5     = 0 ;
   float e2_isolEMHadDepth1  = 0 ;
   float e2_IsolPtTrks       = 0 ;
   float e2_EcalDriven       = 0 ;
   float e2_dEtaIn           = 0 ;
 
   tree_out.Branch("pv_n"      , &pv_n_out          , "pv_n/I"        ) ;
   tree_out.Branch("PU_true"   , &PU_true_out       , "PU_true/I"     ) ;
   tree_out.Branch("event_sign", &event_sign        , "event_sign/I"  ) ;
 
   tree_out.Branch("rho"       , &rho_out           , "rho/F"      ) ;

   tree_out.Branch("OS"        , &OS_out            , "OS/F"       ) ;
   tree_out.Branch("mee"       , &mee_out           , "mee/F"      ) ;
   tree_out.Branch("Pt"        , &Pt_out            , "Pt/F"       ) ;
   tree_out.Branch("e1_Et"     , &HEEP1_Et_out      , "e1_Et/F"    ) ;
   tree_out.Branch("e1_eta"    , &HEEP1_eta_out     , "e1_eta/F"   ) ;
   tree_out.Branch("e1_phi"    , &HEEP1_phi_out     , "e1_phi/F"   ) ;
   tree_out.Branch("e2_Et"     , &HEEP2_Et_out      , "e2_Et/F"    ) ;
   tree_out.Branch("e2_eta"    , &HEEP2_eta_out     , "e2_eta/F"   ) ;
   tree_out.Branch("e2_phi"    , &HEEP2_phi_out     , "e2_phi/F"   ) ;
   tree_out.Branch("mee_gsf"   , &mee_out_gsf       , "mee_gsf/F"      ) ;
   tree_out.Branch("e1_eta_gsf", &HEEP1_eta_out_gsf , "e1_eta_gsf/F") ;
   tree_out.Branch("e1_phi_gsf", &HEEP1_phi_out_gsf , "e1_phi_gsf/F") ;
   tree_out.Branch("e2_eta_gsf", &HEEP2_eta_out_gsf , "e2_eta_gsf/F") ;
   tree_out.Branch("e2_phi_gsf", &HEEP2_phi_out_gsf , "e2_phi_gsf/F") ;

   tree_out.Branch("e1_dPhiIn"          , &e1_dPhiIn          , "e1_dPhiIn/F"              ) ;
   tree_out.Branch("e1_Sieie"           , &e1_Sieie           , "e1_Sieie/F"               ) ;
   tree_out.Branch("e1_missingHits"     , &e1_missingHits     , "e1_missingHits/F"         ) ;
   tree_out.Branch("e1_dxyFirstPV"      , &e1_dxyFirstPV      , "e1_dxyFirstPV/F"          ) ;
   tree_out.Branch("e1_HOverE"          , &e1_HOverE          , "e1_HOverE/F"              ) ;
   tree_out.Branch("e1_E1x5OverE5x5"    , &e1_E1x5OverE5x5    , "e1_E1x5OverE5x5/F"        ) ;
   tree_out.Branch("e1_E2x5OverE5x5"    , &e1_E2x5OverE5x5    , "e1_E2x5OverE5x5/F"        ) ;
   tree_out.Branch("e1_isolEMHadDepth1" , &e1_isolEMHadDepth1 , "e1_isolEMHadDepth1/F"     ) ;
   tree_out.Branch("e1_IsolPtTrks"      , &e1_IsolPtTrks      , "e1_IsolPtTrks/F"          ) ;
   tree_out.Branch("e1_EcalDriven"      , &e1_EcalDriven      , "e1_EcalDriven/F"          ) ;
   tree_out.Branch("e1_dEtaIn"          , &e1_dEtaIn          , "e1_dEtaIn/F"              ) ;
   tree_out.Branch("e2_dPhiIn"          , &e2_dPhiIn          , "e2_dPhiIn/F"              ) ;
   tree_out.Branch("e2_Sieie"           , &e2_Sieie           , "e2_Sieie/F"               ) ;
   tree_out.Branch("e2_missingHits"     , &e2_missingHits     , "e2_missingHits/F"         ) ;
   tree_out.Branch("e2_dxyFirstPV"      , &e2_dxyFirstPV      , "e2_dxyFirstPV/F"          ) ;
   tree_out.Branch("e2_HOverE"          , &e2_HOverE          , "e2_HOverE/F"              ) ;
   tree_out.Branch("e2_E1x5OverE5x5"    , &e2_E1x5OverE5x5    , "e2_E1x5OverE5x5/F"        ) ;
   tree_out.Branch("e2_E2x5OverE5x5"    , &e2_E2x5OverE5x5    , "e2_E2x5OverE5x5/F"        ) ;
   tree_out.Branch("e2_isolEMHadDepth1" , &e2_isolEMHadDepth1 , "e2_isolEMHadDepth1/F"     ) ;
   tree_out.Branch("e2_IsolPtTrks"      , &e2_IsolPtTrks      , "e2_IsolPtTrks/F"          ) ;
   tree_out.Branch("e2_EcalDriven"      , &e2_EcalDriven      , "e2_EcalDriven/F"          ) ;
   tree_out.Branch("e2_dEtaIn"          , &e2_dEtaIn          , "e2_dEtaIn/F"              ) ;

   tree_out.Branch("w_PU_combined"   , &w_PU_combined_out , "w_PU_combined/F"         ) ;
   tree_out.Branch("w_PU_golden"     , &w_PU_golden_out   , "w_PU_golden/F"           ) ;
   tree_out.Branch("w_PU_silver"     , &w_PU_silver_out   , "w_PU_silver/F"           ) ;
   tree_out.Branch("w_PU_silver_down", &w_PU_silver_down_out , "w_PU_silver_down/F"   ) ;
   tree_out.Branch("w_PU_silver_up"  , &w_PU_silver_up_out , "w_PU_silver_down/F"     ) ;
   
   TTree tree_Barrel_scale_up("Ele_Barrel_scale_up","HEEP ele") ;
   tree_Barrel_scale_up.Branch("PU_true"   , &PU_true_out       , "PU_true/I"     ) ;
   tree_Barrel_scale_up.Branch("event_sign", &event_sign        , "event_sign/I"  ) ;
   tree_Barrel_scale_up.Branch("mee"       , &mee_out           , "mee/F"      ) ;
   tree_Barrel_scale_up.Branch("e1_Et"     , &HEEP1_Et_out      , "e1_Et/F"    ) ;
   tree_Barrel_scale_up.Branch("e1_eta"    , &HEEP1_eta_out     , "e1_eta/F"   ) ;
   tree_Barrel_scale_up.Branch("e1_phi"    , &HEEP1_phi_out     , "e1_phi/F"   ) ;
   tree_Barrel_scale_up.Branch("e2_Et"     , &HEEP2_Et_out      , "e2_Et/F"    ) ;
   tree_Barrel_scale_up.Branch("e2_eta"    , &HEEP2_eta_out     , "e2_eta/F"   ) ;
   tree_Barrel_scale_up.Branch("e2_phi"    , &HEEP2_phi_out     , "e2_phi/F"   ) ;
   tree_Barrel_scale_up.Branch("w_PU_combined"   , &w_PU_combined_out , "w_PU_combined/F"         ) ;
   tree_Barrel_scale_up.Branch("mee_gsf"   , &mee_out_gsf       , "mee_gsf/F"      ) ;
   tree_Barrel_scale_up.Branch("e1_eta_gsf", &HEEP1_eta_out_gsf , "e1_eta_gsf/F") ;
   tree_Barrel_scale_up.Branch("e1_phi_gsf", &HEEP1_phi_out_gsf , "e1_phi_gsf/F") ;
   tree_Barrel_scale_up.Branch("e2_eta_gsf", &HEEP2_eta_out_gsf , "e2_eta_gsf/F") ;
   tree_Barrel_scale_up.Branch("e2_phi_gsf", &HEEP2_phi_out_gsf , "e2_phi_gsf/F") ;

   TTree tree_Barrel_scale_down("Ele_Barrel_scale_down","HEEP ele") ;
   tree_Barrel_scale_down.Branch("PU_true"   , &PU_true_out       , "PU_true/I"     ) ;
   tree_Barrel_scale_down.Branch("event_sign", &event_sign        , "event_sign/I"  ) ;
   tree_Barrel_scale_down.Branch("mee"       , &mee_out           , "mee/F"      ) ;
   tree_Barrel_scale_down.Branch("e1_Et"     , &HEEP1_Et_out      , "e1_Et/F"    ) ;
   tree_Barrel_scale_down.Branch("e1_eta"    , &HEEP1_eta_out     , "e1_eta/F"   ) ;
   tree_Barrel_scale_down.Branch("e1_phi"    , &HEEP1_phi_out     , "e1_phi/F"   ) ;
   tree_Barrel_scale_down.Branch("e2_Et"     , &HEEP2_Et_out      , "e2_Et/F"    ) ;
   tree_Barrel_scale_down.Branch("e2_eta"    , &HEEP2_eta_out     , "e2_eta/F"   ) ;
   tree_Barrel_scale_down.Branch("e2_phi"    , &HEEP2_phi_out     , "e2_phi/F"   ) ;
   tree_Barrel_scale_down.Branch("w_PU_combined"   , &w_PU_combined_out , "w_PU_combined/F"         ) ;
   tree_Barrel_scale_down.Branch("mee_gsf"   , &mee_out_gsf       , "mee_gsf/F"      ) ;
   tree_Barrel_scale_down.Branch("e1_eta_gsf", &HEEP1_eta_out_gsf , "e1_eta_gsf/F") ;
   tree_Barrel_scale_down.Branch("e1_phi_gsf", &HEEP1_phi_out_gsf , "e1_phi_gsf/F") ;
   tree_Barrel_scale_down.Branch("e2_eta_gsf", &HEEP2_eta_out_gsf , "e2_eta_gsf/F") ;
   tree_Barrel_scale_down.Branch("e2_phi_gsf", &HEEP2_phi_out_gsf , "e2_phi_gsf/F") ;

   TTree tree_Endcap_scale_up("Ele_Endcap_scale_up","HEEP ele") ;
   tree_Endcap_scale_up.Branch("PU_true"   , &PU_true_out       , "PU_true/I"     ) ;
   tree_Endcap_scale_up.Branch("event_sign", &event_sign        , "event_sign/I"  ) ;
   tree_Endcap_scale_up.Branch("mee"       , &mee_out           , "mee/F"      ) ;
   tree_Endcap_scale_up.Branch("e1_Et"     , &HEEP1_Et_out      , "e1_Et/F"    ) ;
   tree_Endcap_scale_up.Branch("e1_eta"    , &HEEP1_eta_out     , "e1_eta/F"   ) ;
   tree_Endcap_scale_up.Branch("e1_phi"    , &HEEP1_phi_out     , "e1_phi/F"   ) ;
   tree_Endcap_scale_up.Branch("e2_Et"     , &HEEP2_Et_out      , "e2_Et/F"    ) ;
   tree_Endcap_scale_up.Branch("e2_eta"    , &HEEP2_eta_out     , "e2_eta/F"   ) ;
   tree_Endcap_scale_up.Branch("e2_phi"    , &HEEP2_phi_out     , "e2_phi/F"   ) ;
   tree_Endcap_scale_up.Branch("w_PU_combined"   , &w_PU_combined_out , "w_PU_combined/F"         ) ;
   tree_Endcap_scale_up.Branch("mee_gsf"   , &mee_out_gsf       , "mee_gsf/F"      ) ;
   tree_Endcap_scale_up.Branch("e1_eta_gsf", &HEEP1_eta_out_gsf , "e1_eta_gsf/F") ;
   tree_Endcap_scale_up.Branch("e1_phi_gsf", &HEEP1_phi_out_gsf , "e1_phi_gsf/F") ;
   tree_Endcap_scale_up.Branch("e2_eta_gsf", &HEEP2_eta_out_gsf , "e2_eta_gsf/F") ;
   tree_Endcap_scale_up.Branch("e2_phi_gsf", &HEEP2_phi_out_gsf , "e2_phi_gsf/F") ;

   TTree tree_Endcap_scale_down("Ele_Endcap_scale_down","HEEP ele") ;
   tree_Endcap_scale_down.Branch("PU_true"   , &PU_true_out       , "PU_true/I"     ) ;
   tree_Endcap_scale_down.Branch("event_sign", &event_sign        , "event_sign/I"  ) ;
   tree_Endcap_scale_down.Branch("mee"       , &mee_out           , "mee/F"      ) ;
   tree_Endcap_scale_down.Branch("e1_Et"     , &HEEP1_Et_out      , "e1_Et/F"    ) ;
   tree_Endcap_scale_down.Branch("e1_eta"    , &HEEP1_eta_out     , "e1_eta/F"   ) ;
   tree_Endcap_scale_down.Branch("e1_phi"    , &HEEP1_phi_out     , "e1_phi/F"   ) ;
   tree_Endcap_scale_down.Branch("e2_Et"     , &HEEP2_Et_out      , "e2_Et/F"    ) ;
   tree_Endcap_scale_down.Branch("e2_eta"    , &HEEP2_eta_out     , "e2_eta/F"   ) ;
   tree_Endcap_scale_down.Branch("e2_phi"    , &HEEP2_phi_out     , "e2_phi/F"   ) ;
   tree_Endcap_scale_down.Branch("w_PU_combined"   , &w_PU_combined_out , "w_PU_combined/F"         ) ;
   tree_Endcap_scale_down.Branch("mee_gsf"   , &mee_out_gsf       , "mee_gsf/F"      ) ;
   tree_Endcap_scale_down.Branch("e1_eta_gsf", &HEEP1_eta_out_gsf , "e1_eta_gsf/F") ;
   tree_Endcap_scale_down.Branch("e1_phi_gsf", &HEEP1_phi_out_gsf , "e1_phi_gsf/F") ;
   tree_Endcap_scale_down.Branch("e2_eta_gsf", &HEEP2_eta_out_gsf , "e2_eta_gsf/F") ;
   tree_Endcap_scale_down.Branch("e2_phi_gsf", &HEEP2_phi_out_gsf , "e2_phi_gsf/F") ;

   std::vector<runCounter> runs ;
   
   TRandom3 rand ;
   Long64_t nbytes = 0, nb = 0;

   bool do_fakeRate_pass_fail=true;
   bool do_EnergyCorrect=true;
   bool do_EnergySmear=false;
   bool do_EnergyCorrect_UnCert=true;
   if(isData==false) do_EnergyCorrect=false;
   else{do_EnergySmear=false;
        do_EnergyCorrect_UnCert=false;}
   for (Long64_t jentry=0; jentry<nentries;jentry++){
//   displayProgress(jentry, nentries) ;
      
   Long64_t ientry = LoadTree(jentry);
   if (ientry < 0) break;
   nb = fChain->GetEntry(jentry);   
   nbytes += nb;

   if(isData==true){ if( ev_run<Run_low || ev_run>Run_high) continue;}
   if(ev_fixedGridRhoFastjetAll==-999) continue;

   rho_out = ev_fixedGridRhoFastjetAll;

      int w_sign = 1 ;
      w_sign = mc_w_sign < 0 ? -1 : 1 ;
      
      if(true==isWW || true==isTTbar){
      TLorentzVector MC_p4_1(1,0,0,0);
      TLorentzVector MC_p4_2(1,0,0,0);
      float Mass_treshold=0;
      bool accept=true;
      if(true==isWW) Mass_treshold=200;
      if(true==isTTbar) Mass_treshold=500;
      
      for(unsigned iMC=0 ; iMC<mc_n ; ++iMC){
      //if( (abs(mc_pdgId->at(iMC)) != 11 && abs(mc_pdgId->at(iMC)) != 13 && abs(mc_pdgId->at(iMC)) != 15) || mc_status->at(iMC) != 23) continue;
      if( (abs(mc_pdgId->at(iMC)) != 11 && abs(mc_pdgId->at(iMC)) != 13 && abs(mc_pdgId->at(iMC)) != 15) ) continue;
      MC_p4_1.SetPtEtaPhiM(mc_pt->at(iMC),mc_eta->at(iMC),mc_phi->at(iMC),mc_mass->at(iMC)) ;
      for(unsigned jMC=iMC+1 ; jMC<mc_n ; ++jMC){
      if( (abs(mc_pdgId->at(jMC)) != 11 && abs(mc_pdgId->at(jMC)) != 13 && abs(mc_pdgId->at(jMC)) != 15) ) continue;
      MC_p4_2.SetPtEtaPhiM(mc_pt->at(jMC),mc_eta->at(jMC),mc_phi->at(jMC),mc_mass->at(jMC)) ;
      if(MC_p4_1.DeltaR(MC_p4_2)<0.001) continue;
      if((MC_p4_1+MC_p4_2).M()>Mass_treshold){accept=false; break;}
      }
      if(accept==false) break;
      }      
      //std::cout<<"accept="<<accept<<std::endl;
      if(accept==false) continue;
      }
       
      if(true==isZToTT){
      bool accept_event = false ;
      bool has_taup = false ;
      bool has_taum = false ;
      for(unsigned iMC=0 ; iMC<mc_n ; ++iMC){
      if(mc_pdgId->at(iMC)== 15) has_taum = true ;
      if(mc_pdgId->at(iMC)==-15) has_taup = true ;
      if(has_taup && has_taum){
         accept_event = true ;
            break ;
                              }
                                           }
      if(accept_event==false) continue ;
       }


      event_sign=w_sign;      
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
        w_PU_golden_out        = w_sign*PU_reReco_Morind17::MC_pileup_weight(PU,0,"all");
        w_PU_silver_out        = w_sign*PU_reReco_Morind17::MC_pileup_weight(PU,0,"all");
        w_PU_silver_up_out     = w_sign*PU_reReco_Morind17::MC_pileup_weight(PU,1,"all");
        w_PU_silver_down_out   = w_sign*PU_reReco_Morind17::MC_pileup_weight(PU,2,"all");
      }
      
      std::vector<electron_candidate*> electrons ;
      std::vector<electron_candidate*> electrons_Barrel_scale_up ;
      std::vector<electron_candidate*> electrons_Barrel_scale_down ;
      std::vector<electron_candidate*> electrons_Endcap_scale_up ;
      std::vector<electron_candidate*> electrons_Endcap_scale_down ;
      for(unsigned int iEl=0 ; iEl<gsf_n ; ++iEl){
        float Et     = gsf_caloEnergy->at(iEl)*sin( gsf_theta->at(iEl) ) ; 
        float sc_eta    = gsf_sc_eta->at(iEl); 
        float g_eta     = gsf_eta->at(iEl); 
        if(do_EnergyCorrect==true){
        if(fabs(sc_eta)<1.4442)Et = Et*1.0012 ;
        else if(fabs(sc_eta)>1.566 && fabs(sc_eta)<2.5) Et = Et*1.0089 ;
        }
        if(do_EnergySmear==true){
        if(fabs(sc_eta)<1.4442)Et = Et*rand.Gaus(1,0.0123) ;
        else if(fabs(sc_eta)>1.566 && fabs(sc_eta)<2.5) Et = Et*rand.Gaus(1,0.0229) ;
        }
        float g_phi  = gsf_phi->at(iEl) ;
        float sc_phi = gsf_sc_phi->at(iEl) ;
        int   charge = gsf_charge->at(iEl) ;
        electron_candidate* el = new electron_candidate(Et, sc_eta, sc_phi, g_eta, g_phi, charge) ;
        
        if(isData){
//################ Pass Ele33 ########################          
          int passTrigger=0;
          int trigger_fire = trig_DE_fire ;
          vector<float>* trig_unseed_eta=0;
          vector<float>* trig_unseed_phi=0;
          int pass_unseed=0;
          trig_unseed_eta = trig_DE_unseed_eta;
          trig_unseed_phi = trig_DE_unseed_phi;

          TLorentzVector trigp4 ;
          for(unsigned int itrig=0 ; itrig<trig_unseed_eta->size() ; ++itrig){
            trigp4.SetPtEtaPhiM(100,trig_unseed_eta->at(itrig),trig_unseed_phi->at(itrig),10) ;
            if(trigp4.DeltaR(el->p4) < 0.1){
              pass_unseed=1 ;
              break ;
            }
          }           
          passTrigger = (pass_unseed && trigger_fire)? 1 : 0 ;
//####################################################          
         el->pass_trigger = passTrigger ;
        }//isData
        else{
          el->pass_trigger = trigEle33::passTrig(Et, sc_eta) ;
        }
        
        el->apply_ID_value(gsf_deltaPhiSuperClusterTrackAtVtx->at(iEl),
                           gsf_full5x5_sigmaIetaIeta->at(iEl),
                     float(gsf_nLostInnerHits->at(iEl) ),
                      fabs(gsf_dxy_firstPVtx->at(iEl)),
                           gsf_hadronicOverEm->at(iEl),
                           gsf_superClusterEnergy->at(iEl),
                          (gsf_full5x5_e1x5->at(iEl)/gsf_full5x5_e5x5->at(iEl) ),
                          (gsf_full5x5_e2x5Max->at(iEl)/gsf_full5x5_e5x5->at(iEl) ),
                          (gsf_dr03EcalRecHitSumEt->at(iEl) + gsf_dr03HcalDepth1TowerSumEt->at(iEl) ),
                           gsf_dr03TkSumPtHEEP7->at(iEl),
                     float(gsf_ecaldrivenSeed->at(iEl) ),
                           gsf_deltaEtaSeedClusterTrackAtVtx->at(iEl),
                           ev_fixedGridRhoFastjetAll) ;

        el->Pass_PreSelection(gsf_full5x5_sigmaIetaIeta->at(iEl), gsf_hadronicOverEm->at(iEl), float(gsf_nLostInnerHits->at(iEl)) , fabs(gsf_dxy_firstPVtx->at(iEl)) ); 
        electrons.push_back(el) ;
//########################### For MC energy scale #############
        if(do_EnergyCorrect_UnCert==true){
        electron_candidate* el_Barrel_scale_up   = (fabs(sc_eta)<1.4442) ? new electron_candidate(Et*1.02, sc_eta, sc_phi, g_eta, g_phi, charge) : new electron_candidate(Et, sc_eta, sc_phi, g_eta, g_phi,charge) ;
        electron_candidate* el_Barrel_scale_down = (fabs(sc_eta)<1.4442) ? new electron_candidate(Et*0.98, sc_eta, sc_phi, g_eta, g_phi, charge) : new electron_candidate(Et, sc_eta, sc_phi, g_eta, g_phi,charge) ;
        electron_candidate* el_Endcap_scale_up   = (fabs(sc_eta)>1.566 && fabs(sc_eta)<2.5) ? new electron_candidate(Et*1.01, sc_eta, sc_phi,g_eta, g_phi, charge) : new electron_candidate(Et, sc_eta, sc_phi, g_eta, g_phi,charge) ;
        electron_candidate* el_Endcap_scale_down = (fabs(sc_eta)>1.566 && fabs(sc_eta)<2.5) ? new electron_candidate(Et*0.99, sc_eta, sc_phi,g_eta, g_phi, charge) : new electron_candidate(Et, sc_eta, sc_phi, g_eta, g_phi,charge) ;
        el_Barrel_scale_up->pass_trigger  =el->pass_trigger; 
        el_Barrel_scale_down->pass_trigger=el->pass_trigger; 
        el_Endcap_scale_up->pass_trigger  =el->pass_trigger; 
        el_Endcap_scale_down->pass_trigger=el->pass_trigger;
 
        el_Barrel_scale_up->apply_ID_value(gsf_deltaPhiSuperClusterTrackAtVtx->at(iEl),
                           gsf_full5x5_sigmaIetaIeta->at(iEl),
                     float(gsf_nLostInnerHits->at(iEl) ),
                      fabs(gsf_dxy_firstPVtx->at(iEl)),
                           gsf_hadronicOverEm->at(iEl),
                           gsf_superClusterEnergy->at(iEl),
                          (gsf_full5x5_e1x5->at(iEl)/gsf_full5x5_e5x5->at(iEl) ),
                          (gsf_full5x5_e2x5Max->at(iEl)/gsf_full5x5_e5x5->at(iEl) ),
                          (gsf_dr03EcalRecHitSumEt->at(iEl) + gsf_dr03HcalDepth1TowerSumEt->at(iEl) ),
                           gsf_dr03TkSumPtHEEP7->at(iEl),
                     float(gsf_ecaldrivenSeed->at(iEl) ),
                           gsf_deltaEtaSeedClusterTrackAtVtx->at(iEl),
                           ev_fixedGridRhoFastjetAll) ;
        el_Barrel_scale_up->Pass_PreSelection(gsf_full5x5_sigmaIetaIeta->at(iEl), gsf_hadronicOverEm->at(iEl), float(gsf_nLostInnerHits->at(iEl)) , fabs(gsf_dxy_firstPVtx->at(iEl)) ); 
        electrons_Barrel_scale_up.push_back(el_Barrel_scale_up) ;

        el_Barrel_scale_down->apply_ID_value(gsf_deltaPhiSuperClusterTrackAtVtx->at(iEl),
                           gsf_full5x5_sigmaIetaIeta->at(iEl),
                     float(gsf_nLostInnerHits->at(iEl) ),
                      fabs(gsf_dxy_firstPVtx->at(iEl)),
                           gsf_hadronicOverEm->at(iEl),
                           gsf_superClusterEnergy->at(iEl),
                          (gsf_full5x5_e1x5->at(iEl)/gsf_full5x5_e5x5->at(iEl) ),
                          (gsf_full5x5_e2x5Max->at(iEl)/gsf_full5x5_e5x5->at(iEl) ),
                          (gsf_dr03EcalRecHitSumEt->at(iEl) + gsf_dr03HcalDepth1TowerSumEt->at(iEl) ),
                           gsf_dr03TkSumPtHEEP7->at(iEl),
                     float(gsf_ecaldrivenSeed->at(iEl) ),
                           gsf_deltaEtaSeedClusterTrackAtVtx->at(iEl),
                           ev_fixedGridRhoFastjetAll) ;
        el_Barrel_scale_down->Pass_PreSelection(gsf_full5x5_sigmaIetaIeta->at(iEl), gsf_hadronicOverEm->at(iEl), float(gsf_nLostInnerHits->at(iEl)) , fabs(gsf_dxy_firstPVtx->at(iEl)) ); 
        electrons_Barrel_scale_down.push_back(el_Barrel_scale_down) ;

        el_Endcap_scale_up->apply_ID_value(gsf_deltaPhiSuperClusterTrackAtVtx->at(iEl),
                           gsf_full5x5_sigmaIetaIeta->at(iEl),
                     float(gsf_nLostInnerHits->at(iEl) ),
                      fabs(gsf_dxy_firstPVtx->at(iEl)),
                           gsf_hadronicOverEm->at(iEl),
                           gsf_superClusterEnergy->at(iEl),
                          (gsf_full5x5_e1x5->at(iEl)/gsf_full5x5_e5x5->at(iEl) ),
                          (gsf_full5x5_e2x5Max->at(iEl)/gsf_full5x5_e5x5->at(iEl) ),
                          (gsf_dr03EcalRecHitSumEt->at(iEl) + gsf_dr03HcalDepth1TowerSumEt->at(iEl) ),
                           gsf_dr03TkSumPtHEEP7->at(iEl),
                     float(gsf_ecaldrivenSeed->at(iEl) ),
                           gsf_deltaEtaSeedClusterTrackAtVtx->at(iEl),
                           ev_fixedGridRhoFastjetAll) ;
        el_Endcap_scale_up->Pass_PreSelection(gsf_full5x5_sigmaIetaIeta->at(iEl), gsf_hadronicOverEm->at(iEl), float(gsf_nLostInnerHits->at(iEl)) , fabs(gsf_dxy_firstPVtx->at(iEl)) ); 
        electrons_Endcap_scale_up.push_back(el_Endcap_scale_up) ;

        el_Endcap_scale_down->apply_ID_value(gsf_deltaPhiSuperClusterTrackAtVtx->at(iEl),
                           gsf_full5x5_sigmaIetaIeta->at(iEl),
                     float(gsf_nLostInnerHits->at(iEl) ),
                      fabs(gsf_dxy_firstPVtx->at(iEl)),
                           gsf_hadronicOverEm->at(iEl),
                           gsf_superClusterEnergy->at(iEl),
                          (gsf_full5x5_e1x5->at(iEl)/gsf_full5x5_e5x5->at(iEl) ),
                          (gsf_full5x5_e2x5Max->at(iEl)/gsf_full5x5_e5x5->at(iEl) ),
                          (gsf_dr03EcalRecHitSumEt->at(iEl) + gsf_dr03HcalDepth1TowerSumEt->at(iEl) ),
                           gsf_dr03TkSumPtHEEP7->at(iEl),
                     float(gsf_ecaldrivenSeed->at(iEl) ),
                           gsf_deltaEtaSeedClusterTrackAtVtx->at(iEl),
                           ev_fixedGridRhoFastjetAll) ;
        el_Endcap_scale_down->Pass_PreSelection(gsf_full5x5_sigmaIetaIeta->at(iEl), gsf_hadronicOverEm->at(iEl), float(gsf_nLostInnerHits->at(iEl)) , fabs(gsf_dxy_firstPVtx->at(iEl)) ); 
        electrons_Endcap_scale_down.push_back(el_Endcap_scale_down) ;
}
//#######################################
      }

      for(unsigned int i_1=0 ; i_1<electrons.size() ; ++i_1){
      electron_candidate* e1 = electrons.at(i_1) ;
     if(do_fakeRate_pass_fail==true){ if(false==e1->accept_HEEP_ID || false==e1->pass_trigger) continue ;}
        
      for(unsigned int i_2=0 ; i_2<electrons.size() ; ++i_2){
      if(i_2==i_1) continue;
      electron_candidate* e2 = electrons.at(i_2) ;
      if(do_fakeRate_pass_fail==true){if(e2->Et<35 || true==e2->accept_HEEP_ID || false==e2->pass_trigger || e2->accept_PreSelection==false) continue ;}

      TLorentzVector Zp4 = e1->p4 + e2->p4 ;
      mee_out                = Zp4.M() ;
      Pt_out                 = sqrt( Zp4.Px()*Zp4.Px() + Zp4.Py()*Zp4.Py());
      OS_out                 = (e1->charge * e2->charge) > 0 ? 0 : 1 ;
      HEEP1_Et_out           = e1->Et  ;
      HEEP1_eta_out          = e1->eta ;
      HEEP1_phi_out          = e1->phi ;
      HEEP2_Et_out           = e2->Et  ;
      HEEP2_eta_out          = e2->eta ;
      HEEP2_phi_out          = e2->phi ;
      TLorentzVector gsf_Zp4 = e1->gsf_p4 + e2->gsf_p4 ;
      mee_out_gsf            = gsf_Zp4.M() ;
      HEEP1_eta_out_gsf      = e1->gsf_eta ;
      HEEP1_phi_out_gsf      = e1->gsf_phi ;
      HEEP2_eta_out_gsf      = e2->gsf_eta ;
      HEEP2_phi_out_gsf      = e2->gsf_phi ;

      e1_dPhiIn             = e1->ele_dPhiIn         ; 
      e1_Sieie              = e1->ele_Sieie          ;
      e1_missingHits        = e1->ele_missingHits    ;
      e1_dxyFirstPV         = e1->ele_dxyFirstPV     ;
      e1_HOverE             = e1->ele_HOverE         ;
      e1_E1x5OverE5x5       = e1->ele_E1x5OverE5x5   ;
      e1_E2x5OverE5x5       = e1->ele_E2x5OverE5x5   ;
      e1_isolEMHadDepth1    = e1->ele_isolEMHadDepth1;
      e1_IsolPtTrks         = e1->ele_IsolPtTrks     ;
      e1_EcalDriven         = e1->ele_EcalDriven     ;
      e1_dEtaIn             = e1->ele_dEtaIn         ;
      e2_dPhiIn             = e2->ele_dPhiIn         ; 
      e2_Sieie              = e2->ele_Sieie          ;
      e2_missingHits        = e2->ele_missingHits    ;
      e2_dxyFirstPV         = e2->ele_dxyFirstPV     ;
      e2_HOverE             = e2->ele_HOverE         ;
      e2_E1x5OverE5x5       = e2->ele_E1x5OverE5x5   ;
      e2_E2x5OverE5x5       = e2->ele_E2x5OverE5x5   ;
      e2_isolEMHadDepth1    = e2->ele_isolEMHadDepth1;
      e2_IsolPtTrks         = e2->ele_IsolPtTrks     ;
      e2_EcalDriven         = e2->ele_EcalDriven     ;
      e2_dEtaIn             = e2->ele_dEtaIn         ;
      tree_out.Fill() ;
        }
      }

///////////////// For energy scale uncert. ////////////////

      for(unsigned int i_1=0 ; i_1<electrons_Barrel_scale_up.size() ; ++i_1){
      electron_candidate* e1 = electrons_Barrel_scale_up.at(i_1) ;
      if(do_fakeRate_pass_fail==true){ if(false==e1->accept_HEEP_ID || false==e1->pass_trigger) continue ;}
      for(unsigned int i_2=0 ; i_2<electrons_Barrel_scale_up.size() ; ++i_2){
      if(i_2==i_1) continue;
      electron_candidate* e2 = electrons_Barrel_scale_up.at(i_2) ;
      if(do_fakeRate_pass_fail==true){if(e2->Et<35 || true==e2->accept_HEEP_ID || false==e2->pass_trigger || e2->accept_PreSelection==false) continue ;}
      TLorentzVector Zp4 = e1->p4 + e2->p4 ;
      mee_out                = Zp4.M() ;
      HEEP1_Et_out           = e1->Et  ;
      HEEP1_eta_out          = e1->eta ;
      HEEP1_phi_out          = e1->phi ;
      HEEP2_Et_out           = e2->Et  ;
      HEEP2_eta_out          = e2->eta ;
      HEEP2_phi_out          = e2->phi ;
      TLorentzVector gsf_Zp4 = e1->gsf_p4 + e2->gsf_p4 ;
      mee_out_gsf            = gsf_Zp4.M() ;
      HEEP1_eta_out_gsf      = e1->gsf_eta ;
      HEEP1_phi_out_gsf      = e1->gsf_phi ;
      HEEP2_eta_out_gsf      = e2->gsf_eta ;
      HEEP2_phi_out_gsf      = e2->gsf_phi ;
      tree_Barrel_scale_up.Fill() ;
        }
      }

      for(unsigned int i_1=0 ; i_1<electrons_Barrel_scale_down.size() ; ++i_1){
      electron_candidate* e1 = electrons_Barrel_scale_down.at(i_1) ;
      if(do_fakeRate_pass_fail==true){ if(false==e1->accept_HEEP_ID || false==e1->pass_trigger) continue ;}
      for(unsigned int i_2=0 ; i_2<electrons_Barrel_scale_down.size() ; ++i_2){
      if(i_2==i_1) continue;
      electron_candidate* e2 = electrons_Barrel_scale_down.at(i_2) ;
      if(do_fakeRate_pass_fail==true){if(e2->Et<35 || true==e2->accept_HEEP_ID || false==e2->pass_trigger || e2->accept_PreSelection==false) continue ;}
      TLorentzVector Zp4 = e1->p4 + e2->p4 ;
      mee_out                = Zp4.M() ;
      HEEP1_Et_out           = e1->Et  ;
      HEEP1_eta_out          = e1->eta ;
      HEEP1_phi_out          = e1->phi ;
      HEEP2_Et_out           = e2->Et  ;
      HEEP2_eta_out          = e2->eta ;
      HEEP2_phi_out          = e2->phi ;
      TLorentzVector gsf_Zp4 = e1->gsf_p4 + e2->gsf_p4 ;
      mee_out_gsf            = gsf_Zp4.M() ;
      HEEP1_eta_out_gsf      = e1->gsf_eta ;
      HEEP1_phi_out_gsf      = e1->gsf_phi ;
      HEEP2_eta_out_gsf      = e2->gsf_eta ;
      HEEP2_phi_out_gsf      = e2->gsf_phi ;
      tree_Barrel_scale_down.Fill() ;
        }
      }

      for(unsigned int i_1=0 ; i_1<electrons_Endcap_scale_up.size() ; ++i_1){
      electron_candidate* e1 = electrons_Endcap_scale_up.at(i_1) ;
      if(do_fakeRate_pass_fail==true){ if(false==e1->accept_HEEP_ID || false==e1->pass_trigger) continue ;}
      for(unsigned int i_2=0 ; i_2<electrons_Endcap_scale_up.size() ; ++i_2){
      if(i_2==i_1) continue;
      electron_candidate* e2 = electrons_Endcap_scale_up.at(i_2) ;
      if(do_fakeRate_pass_fail==true){if(e2->Et<35 || true==e2->accept_HEEP_ID || false==e2->pass_trigger || e2->accept_PreSelection==false) continue ;}
      TLorentzVector Zp4 = e1->p4 + e2->p4 ;
      mee_out                = Zp4.M() ;
      HEEP1_Et_out           = e1->Et  ;
      HEEP1_eta_out          = e1->eta ;
      HEEP1_phi_out          = e1->phi ;
      HEEP2_Et_out           = e2->Et  ;
      HEEP2_eta_out          = e2->eta ;
      HEEP2_phi_out          = e2->phi ;
      TLorentzVector gsf_Zp4 = e1->gsf_p4 + e2->gsf_p4 ;
      mee_out_gsf            = gsf_Zp4.M() ;
      HEEP1_eta_out_gsf      = e1->gsf_eta ;
      HEEP1_phi_out_gsf      = e1->gsf_phi ;
      HEEP2_eta_out_gsf      = e2->gsf_eta ;
      HEEP2_phi_out_gsf      = e2->gsf_phi ;
      tree_Endcap_scale_up.Fill() ;
        }
      }

      for(unsigned int i_1=0 ; i_1<electrons_Endcap_scale_down.size() ; ++i_1){
      electron_candidate* e1 = electrons_Endcap_scale_down.at(i_1) ;
      if(do_fakeRate_pass_fail==true){ if(false==e1->accept_HEEP_ID || false==e1->pass_trigger) continue ;}
      for(unsigned int i_2=0 ; i_2<electrons_Endcap_scale_down.size() ; ++i_2){
      if(i_2==i_1) continue;
      electron_candidate* e2 = electrons_Endcap_scale_down.at(i_2) ;
      if(do_fakeRate_pass_fail==true){if(e2->Et<35 || true==e2->accept_HEEP_ID || false==e2->pass_trigger || e2->accept_PreSelection==false) continue ;}
      TLorentzVector Zp4 = e1->p4 + e2->p4 ;
      mee_out                = Zp4.M() ;
      HEEP1_Et_out           = e1->Et  ;
      HEEP1_eta_out          = e1->eta ;
      HEEP1_phi_out          = e1->phi ;
      HEEP2_Et_out           = e2->Et  ;
      HEEP2_eta_out          = e2->eta ;
      HEEP2_phi_out          = e2->phi ;
      TLorentzVector gsf_Zp4 = e1->gsf_p4 + e2->gsf_p4 ;
      mee_out_gsf            = gsf_Zp4.M() ;
      HEEP1_eta_out_gsf      = e1->gsf_eta ;
      HEEP1_phi_out_gsf      = e1->gsf_phi ;
      HEEP2_eta_out_gsf      = e2->gsf_eta ;
      HEEP2_phi_out_gsf      = e2->gsf_phi ;
      tree_Endcap_scale_down.Fill() ;
        }
      }
//////////////////////////////////////////////////////////

      for (std::vector<electron_candidate*>::iterator it = electrons.begin(); it != electrons.end(); it ++){
      if (NULL != *it){
        delete *it; 
        *it = NULL;
                      }
      }
      electrons.clear() ;
      electrons.swap(electrons);
      
//////////////// For energy scale uncert. /////////////

      for (std::vector<electron_candidate*>::iterator it = electrons_Barrel_scale_up.begin(); it != electrons_Barrel_scale_up.end(); it ++){
      if (NULL != *it){
        delete *it; 
        *it = NULL;
                      }
      }
      electrons_Barrel_scale_up.clear() ;
      electrons_Barrel_scale_up.swap(electrons_Barrel_scale_up);
      for (std::vector<electron_candidate*>::iterator it = electrons_Barrel_scale_down.begin(); it != electrons_Barrel_scale_down.end(); it ++){
      if (NULL != *it){
        delete *it; 
        *it = NULL;
                      }
      }
      electrons_Barrel_scale_down.clear() ;
      electrons_Barrel_scale_down.swap(electrons_Barrel_scale_down);

      for (std::vector<electron_candidate*>::iterator it = electrons_Endcap_scale_up.begin(); it != electrons_Endcap_scale_up.end(); it ++){
      if (NULL != *it){
        delete *it; 
        *it = NULL;
                      }
      }
      electrons_Endcap_scale_up.clear() ;
      electrons_Endcap_scale_up.swap(electrons_Endcap_scale_up);
      for (std::vector<electron_candidate*>::iterator it = electrons_Endcap_scale_down.begin(); it != electrons_Endcap_scale_down.end(); it ++){
      if (NULL != *it){
        delete *it; 
        *it = NULL;
                      }
      }
      electrons_Endcap_scale_down.clear() ;
      electrons_Endcap_scale_down.swap(electrons_Endcap_scale_down);

////////////////////////////////////////////////////////

      
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
   tree_out.Write() ;
   tree_Barrel_scale_up.Write();
   tree_Barrel_scale_down.Write();
   tree_Endcap_scale_up.Write();
   tree_Endcap_scale_down.Write();
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
