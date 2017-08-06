#define reskim_cxx
#include "reskim.h"
#include <TH2.h>
#include <TAxis.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TRandom3.h>
#include <TLorentzVector.h>
#include <cstdlib>
#include <string>
#include <time.h>
#include <iostream>
#include "MC_pileup_weight.C"
#include "/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/Scale_Factor/RoccoR.cc"
const float m_el = 0.000511 ;
const float m_mu = 0.10566  ;

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
  float pt     ;
  float et     ;
  float sc_eta    ;
  float sc_phi    ;
  float eta    ;
  float phi    ;
  int   charge ;
  int   region ;
  
  int truthmatched  ;
  int pass_trigger  ;
  int pass_VIDHEEP7  ;
  int pass_HEEP7  ;
  int pass_PreSelection  ;
  int pass_VIDLoose  ;
  int pass_VIDTight  ;
  
  TLorentzVector p4 ;

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

 
  electron_candidate(float Et_in, float Pt_in, float sc_eta_in, float sc_phi_in, float gsf_eta_in, float gsf_phi_in, int charge_in){
    et     = Et_in     ;
    pt     = Pt_in     ;
    eta    = gsf_eta_in;
    phi    = gsf_phi_in;
    sc_eta = sc_eta_in ;
    sc_phi = sc_phi_in ;
    charge = charge_in ;
    p4.SetPtEtaPhiM(pt, eta, phi, m_el) ;
    truthmatched = 0 ;
    pass_trigger = 0 ;
    pass_VIDHEEP7=0;
    pass_HEEP7   =0;
    pass_PreSelection=0; 
    pass_VIDLoose=0; 
    pass_VIDTight=0; 
    if(fabs(sc_eta)<1.4442) region=1;
    else if(fabs(sc_eta)<1.566)region=2;
    else if(fabs(sc_eta)<2.5)  region=3;
    else region=4;
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
    bool accept_dPhiIn = (fabs(value_dPhiIn) < 0.06 &&  region==1) || (fabs(value_dPhiIn) < 0.06  && region==3) ? 1 : 0 ;
    bool accept_isolEMHadDepth1 = true;
    if     (region==1) accept_isolEMHadDepth1 = ( value_isolEMHadDepth1 < 2+ 0.03*et + 0.28*rho ) ? 1 : 0 ;
    else if(region==3) accept_isolEMHadDepth1 = (((value_isolEMHadDepth1 < 2.5 + 0.28*rho) && et<50) || ((value_isolEMHadDepth1 < 2.5 + 0.03*(et-50) + 0.28*rho) && et>50) ) ? 1 : 0 ;
    bool accept_IsolPtTrks = value_IsolPtTrks < 5 ;
    bool accept_missingHits = value_missingHits < 2 ;
    bool accept_dxyFirstPV = true;
    if     (region==1) accept_dxyFirstPV = fabs(value_dxyFirstPV) < 0.02 ? 1 : 0 ;
    else if(region==3) accept_dxyFirstPV = fabs(value_dxyFirstPV) < 0.05 ? 1 : 0 ;
  
    bool accept_core_ID   = (accept_dPhiIn && accept_Sieie && accept_missingHits && accept_dxyFirstPV && accept_HOverE && accept_showershape) ? 1 : 0 ;
    bool accept_isolation = (accept_isolEMHadDepth1 && accept_IsolPtTrks) ? 1 : 0 ;
    bool accept_nominal_ID= (accept_core_ID && accept_isolation && accept_EcalDriven && accept_dEtaIn) ? 1 : 0 ;
    pass_HEEP7 = (et>35 && accept_nominal_ID && (region==1 || region==3)) ? 1 : 0 ;

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
pass_PreSelection = (accept_sieie && accept_HoverE && accept_missHit && accept_dxy) ? 1 : 0 ;
}

};

struct muon_candidate{
  float Et     ;
  float pt     ;
  float eta    ;
  float phi    ;
  int   charge ;
  int   region ;
  
  int isLoose;
  int isMedium;
  int isTight;
  int passIso;

  int truthmatched  ;
  int trackerLayersWithMeasurement;
  bool muon_isBad ;
  float rochester_sf; 
  TLorentzVector p4 ;
  
  muon_candidate(float pt_in, float eta_in, float phi_in, int charge_in){
    pt     = pt_in     ;
    eta    = eta_in    ;
    phi    = phi_in    ;
    charge = charge_in ;
    p4.SetPtEtaPhiM(pt, eta, phi, m_mu) ;
    region = 0 ;
    if     (fabs(eta)<1.2){ region = 1 ; }
    else if(fabs(eta)<2.4 ){ region = 3 ; }
    else{ region = 4 ; }
  }
}; 



struct jet_candidate{
float pt    ;
float eta   ;
float phi   ;
float mass  ;
float energy;
float CSV        =0;
int pass_loose_ID=0;
int pass_tight_ID=0;

float BtagSF_medium           =0;
float BtagSFbcUp_medium       =0;
float BtagSFbcDown_medium     =0;
float BtagSFudsgUp_medium     =0;
float BtagSFudsgDown_medium   =0;
float SmearedJetResUp_pt      =0;
float SmearedJetResUp_energy  =0;
float SmearedJetResDown_pt    =0;
float SmearedJetResDown_energy=0;
float EnUp_pt                 =0;
float EnUp_energy             =0;
float EnDown_pt               =0;
float EnDown_energy           =0;

jet_candidate(float pt_in, float eta_in, float phi_in, float mass_in, float energy_in ){
pt    =pt_in    ;
eta   =eta_in   ;
phi   =phi_in   ;
mass  =mass_in  ;
energy=energy_in;
}
void Apply_ID(float NHF, float NEMF, float CHF, float MUF, float CEMF, int NumConst, int NumNeutralParticle, int CHM){
if(fabs(eta)<=2.7){
pass_loose_ID=int( (NHF<0.99 && NEMF<0.99 && NumConst>1) && ((fabs(eta)<=2.4 && CHF>0 && CHM>0 && CEMF<0.99) || fabs(eta)>2.4) && fabs(eta)<=2.7 );
pass_tight_ID=int( (NHF<0.90 && NEMF<0.90 && NumConst>1) && ((fabs(eta)<=2.4 && CHF>0 && CHM>0 && CEMF<0.99) || fabs(eta)>2.4) && fabs(eta)<=2.7 );
}
else if (fabs(eta)>2.7 && fabs(eta)<=3.0){
pass_loose_ID=int( (NHF<0.98 && NEMF>0.01 && NumNeutralParticle>2 && fabs(eta)>2.7 && fabs(eta)<=3.0 ) );
pass_tight_ID=int( (NHF<0.98 && NEMF>0.01 && NumNeutralParticle>2 && fabs(eta)>2.7 && fabs(eta)<=3.0 ) );
}
else{
pass_loose_ID=int((NEMF<0.90 && NumNeutralParticle>10 && fabs(eta)>3.0 ) ); 
pass_tight_ID=int((NEMF<0.90 && NumNeutralParticle>10 && fabs(eta)>3.0 ) ); 
}
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
   TTree tree_out("LL","ll") ;
   
   
   int   pv_n_out             = 0 ;
   vector<int>   pv_isValid_out       ;
   vector<int>   pv_ndof_out          ;
   vector<int>   pv_nTracks_out       ;
   vector<int>   pv_totTrackSize_out  ;
   vector<float> pv_normalizedChi2_out;


   int   PU_true_out     = 0 ;
   int   event_sign      = 0 ;
   float rho_out         = 0 ;

   int trig_Ele23_Ele12_out  = 0;
   int trig_DEle33_out       = 0;
   int trig_DEle33_MW_out    = 0;
   int trig_DEle33_CaloId_out= 0;
   int trig_Ele27_out        = 0;
   int trig_Mu8_Ele23_out    = 0;
   int trig_Mu23_Ele12_out   = 0;
   int trig_Mu8_Ele23_DZ_out = 0;
   int trig_Mu23_Ele12_DZ_out= 0;
   int trig_Mu30_Ele30_out   = 0;
   int trig_Mu33_Ele33_out   = 0;
   int trig_Mu17_TkMu8_out   = 0;
   int trig_Mu17_Mu8_out     = 0;
   int trig_Mu17_TkMu8_DZ_out= 0;
   int trig_Mu17_Mu8_DZ_out  = 0;
   int trig_Mu30_TkMu11_out  = 0;
   int trig_IsoMu24_out      = 0; 
   int trig_IsoTkMu24_out    = 0; 
   int trig_HLT_PFHT300_PFMET110_out         =0; 
   int trig_HLT_MET200_out                   =0; 
   int trig_HLT_PFMET300_out                 =0; 
   int trig_HLT_PFMET120_PFMHT120_IDTight_out=0; 
   int trig_HLT_PFMET170_HBHECleaned_out     =0; 
   int trig_HLT_MET75_IsoTrk50_out           =0; 

   vector<float> trig_DEle33_unseed_eta_out   ;
   vector<float> trig_DEle33_unseed_phi_out   ;
   vector<float> trig_DEle33_MW_unseed_eta_out;
   vector<float> trig_DEle33_MW_unseed_phi_out;
    

   float Met_et_out      = 0 ; 
   float Met_phi_out     = 0 ;
   float MET_T1Txy_et_out          =0; 
   float MET_T1Txy_phi_out         =0; 
   float MET_T1Txy_significance_out=0;  
   float MET_T1JetEnDown_Pt_out    =0; 
   float MET_T1JetEnDown_phi_out   =0; 
   float MET_T1JetEnUp_Pt_out      =0; 
   float MET_T1JetEnUp_phi_out     =0; 
   float MET_T1JetResDown_Pt_out   =0;
   float MET_T1JetResDown_phi_out  =0;
   float MET_T1JetResUp_Pt_out     =0;
   float MET_T1JetResUp_phi_out    =0;
   float MET_T1UnclusteredEnUp_Pt_out  =0; 
   float MET_T1UnclusteredEnUp_Px_out  =0; 
   float MET_T1UnclusteredEnUp_Py_out  =0; 
   float MET_T1UnclusteredEnDown_Pt_out=0; 
   float MET_T1UnclusteredEnDown_Px_out=0; 
   float MET_T1UnclusteredEnDown_Py_out=0; 



   vector<float> electrons_pt      ;
   vector<float> electrons_eta     ;
   vector<float> electrons_sc_eta  ;
   vector<float> electrons_phi     ;
   vector<float> electrons_sc_phi  ;
   vector<int>   electrons_charge  ;
   vector<int>   electrons_tight_ID;
   vector<float> electrons_74_pt      ;
   vector<float> electrons_74_eta     ;
   vector<float> electrons_74_sc_eta  ;
   vector<float> electrons_74_phi     ;
   vector<float> electrons_74_sc_phi  ;
   vector<int>   electrons_74_charge  ;
   vector<int>   electrons_74_tight_ID;
   vector<float> heeps_80_et                        ; 
   vector<float> heeps_80_eta                       ; 
   vector<float> heeps_80_sc_eta                    ; 
   vector<float> heeps_80_phi                       ; 
   vector<float> heeps_80_sc_phi                    ; 
   vector<int>   heeps_80_charge                    ; 
   vector<int>   heeps_80_isHEEP7                   ; 
   vector<int>   heeps_80_PreSelection              ;
   vector<float> heeps_74_et                        ; 
   vector<float> heeps_74_eta                       ; 
   vector<float> heeps_74_sc_eta                    ; 
   vector<float> heeps_74_phi                       ; 
   vector<float> heeps_74_sc_phi                    ; 
   vector<int>   heeps_74_charge                    ; 
   vector<int>   heeps_74_isHEEP7                   ; 
   vector<int>   heeps_74_PreSelection              ;
   vector<float> heeps_74_dPhiIn                    ;
   vector<float> heeps_74_Sieie                     ;
   vector<float> heeps_74_missingHits               ;
   vector<float> heeps_74_dxyFirstPV                ;
   vector<float> heeps_74_HOverE                    ;
   vector<float> heeps_74_E1x5OverE5x5              ;
   vector<float> heeps_74_E2x5OverE5x5              ;
   vector<float> heeps_74_isolEMHadDepth1           ;
   vector<float> heeps_74_IsolPtTrks                ;
   vector<float> heeps_74_EcalDriven                ;
   vector<float> heeps_74_dEtaIn                    ;
   vector<int>   heeps_74_match                     ; 
   vector<float> heeps_74_B_EnScaleUp_et            ;
   vector<float> heeps_74_B_EnScaleUp_eta           ;
   vector<float> heeps_74_B_EnScaleUp_sc_eta        ;
   vector<float> heeps_74_B_EnScaleUp_phi           ;
   vector<float> heeps_74_B_EnScaleUp_sc_phi        ;
   vector<int>   heeps_74_B_EnScaleUp_charge        ;
   vector<int>   heeps_74_B_EnScaleUp_isHEEP7       ;
   vector<int>   heeps_74_B_EnScaleUp_PreSelection  ;
   vector<float> heeps_74_B_EnScaleDown_et          ;
   vector<float> heeps_74_B_EnScaleDown_eta         ;
   vector<float> heeps_74_B_EnScaleDown_sc_eta      ;
   vector<float> heeps_74_B_EnScaleDown_phi         ;
   vector<float> heeps_74_B_EnScaleDown_sc_phi      ;
   vector<int>   heeps_74_B_EnScaleDown_charge      ;
   vector<int>   heeps_74_B_EnScaleDown_isHEEP7     ;
   vector<int>   heeps_74_B_EnScaleDown_PreSelection;
   vector<float> heeps_74_E_EnScaleUp_et            ;
   vector<float> heeps_74_E_EnScaleUp_eta           ;
   vector<float> heeps_74_E_EnScaleUp_sc_eta        ;
   vector<float> heeps_74_E_EnScaleUp_phi           ;
   vector<float> heeps_74_E_EnScaleUp_sc_phi        ;
   vector<int>   heeps_74_E_EnScaleUp_charge        ;
   vector<int>   heeps_74_E_EnScaleUp_isHEEP7       ;
   vector<int>   heeps_74_E_EnScaleUp_PreSelection  ;
   vector<float> heeps_74_E_EnScaleDown_et          ;
   vector<float> heeps_74_E_EnScaleDown_eta         ;
   vector<float> heeps_74_E_EnScaleDown_sc_eta      ;
   vector<float> heeps_74_E_EnScaleDown_phi         ;
   vector<float> heeps_74_E_EnScaleDown_sc_phi      ;
   vector<int>   heeps_74_E_EnScaleDown_charge      ;
   vector<int>   heeps_74_E_EnScaleDown_isHEEP7     ;
   vector<int>   heeps_74_E_EnScaleDown_PreSelection;



   vector<float> muons_pt          ;
   vector<float> muons_pt_rochest  ;
   vector<float> muons_eta         ;
   vector<float> muons_phi         ;
   vector<int>   muons_charge      ;
   vector<int>   muons_tight_ID    ;
   vector<int>   muons_pfIso       ;
   vector<int>   muons_match       ;
   vector<int>   muons_trackerLayer;
   vector<float> muons_rochester_sf;

   vector<float> jets_pt      ;
   vector<float> jets_eta     ;
   vector<float> jets_phi     ;
   vector<float> jets_mass    ;
   vector<float> jets_energy  ;
   vector<float> jets_CSV     ;
   vector<int>   jets_loose_ID;
   vector<float> jets_BtagSF_medium           ;
   vector<float> jets_BtagSFbcUp_medium       ;
   vector<float> jets_BtagSFbcDown_medium     ;
   vector<float> jets_BtagSFudsgUp_medium     ;
   vector<float> jets_BtagSFudsgDown_medium   ;
   vector<float> jets_SmearedJetResUp_pt      ;
   vector<float> jets_SmearedJetResUp_energy  ;
   vector<float> jets_SmearedJetResDown_pt    ;
   vector<float> jets_SmearedJetResDown_energy;
   vector<float> jets_EnUp_pt                 ;
   vector<float> jets_EnUp_energy             ;
   vector<float> jets_EnDown_pt               ;
   vector<float> jets_EnDown_energy           ;
   vector<float> LHE_sys_weight               ;
   vector<int>   LHE_sys_id                   ;


 
   float LHE_Z_mass           = 1 ;
   float Z_region             = 0 ;
   float LHE_weight           = 1 ;
   float w_PU_combined_out    = 0 ;
   float w_PU_silver_down_out = 0 ; 
   float w_PU_silver_up_out   = 0 ;
   int trig_Flag_HBHENoiseFilter_out                   =0; 
   int trig_Flag_HBHENoiseIsoFilter_out                =0; 
   int trig_Flag_CSCTightHaloFilter_out                =0; 
   int trig_Flag_CSCTightHaloTrkMuUnvetoFilter_out     =0; 
   int trig_Flag_CSCTightHalo2015Filter_out            =0; 
   int trig_Flag_globalTightHalo2016Filter_out         =0; 
   int trig_Flag_globalSuperTightHalo2016Filter_out    =0; 
   int trig_Flag_goodVertices_out                      =0; 
   int trig_Flag_HcalStripHaloFilter_out               =0; 
   int trig_Flag_hcalLaserEventFilter_out              =0; 
   int trig_Flag_EcalDeadCellTriggerPrimitiveFilter_out=0; 
   int trig_Flag_EcalDeadCellBoundaryEnergyFilter_out  =0; 
   int trig_Flag_ecalLaserCorrFilter_out               =0; 
   int trig_Flag_chargedHadronTrackResolutionFilter_out=0; 
   int trig_Flag_muonBadTrackFilter_out                =0; 
   int trig_Flag_BadPFMuonFilter_out                   =0; 
   int trig_Flag_BadChargedCandidateFilter_out         =0; 
   int trig_Flag_eeBadScFilter_out                     =0; 
   int trig_Flag_trkPOG_manystripclus53X_out           =0; 
   int trig_Flag_trkPOG_toomanystripclus53X_out        =0; 
   int trig_Flag_trkPOG_logErrorTooManyClusters_out    =0; 
   int trig_Flag_METFilters_out                        =0;

   ULong_t ev_run_out=0;
   ULong_t ev_event_out=0;
   ULong_t ev_luminosityBlock_out=0;
 
   tree_out.Branch("ev_run"                     , &ev_run_out                , "ev_run/l"                       ) ;
   tree_out.Branch("ev_event"                   , &ev_event_out              , "ev_event/l"                     ) ;
   tree_out.Branch("ev_luminosityBlock"         , &ev_luminosityBlock_out    , "ev_luminosityBlock/l"           ) ;
   tree_out.Branch("pv_n"                       , &pv_n_out                  , "pv_n/I"                         ) ;
   tree_out.Branch("pv_isValid"                 , &pv_isValid_out            ) ;
   tree_out.Branch("pv_ndof"                    , &pv_ndof_out               ) ;
   tree_out.Branch("pv_nTracks"                 , &pv_nTracks_out            ) ;
   tree_out.Branch("pv_totTrackSize"            , &pv_totTrackSize_out       ) ;
   tree_out.Branch("pv_normalizedChi2"          , &pv_normalizedChi2_out     ) ;
   tree_out.Branch("PU_true"                    , &PU_true_out               , "PU_true/I"                      ) ;
   tree_out.Branch("event_sign"                 , &event_sign                , "event_sign/I"                   ) ;
   tree_out.Branch("trig_Flag_HBHENoiseFilter_accept"                   , &trig_Flag_HBHENoiseFilter_out                     , "trig_Flag_HBHENoiseFilter_accept/I"                     ) ;
   tree_out.Branch("trig_Flag_HBHENoiseIsoFilter_accept"                , &trig_Flag_HBHENoiseIsoFilter_out                  , "trig_Flag_HBHENoiseIsoFilter_accept/I"                  ) ;
   tree_out.Branch("trig_Flag_CSCTightHaloFilter_accept"                , &trig_Flag_CSCTightHaloFilter_out                  , "trig_Flag_CSCTightHaloFilter_accept/I"                  ) ;
   tree_out.Branch("trig_Flag_CSCTightHaloTrkMuUnvetoFilter_accept"     , &trig_Flag_CSCTightHaloTrkMuUnvetoFilter_out       , "trig_Flag_CSCTightHaloTrkMuUnvetoFilter_accept/I"       ) ;
   tree_out.Branch("trig_Flag_CSCTightHalo2015Filter_accept"            , &trig_Flag_CSCTightHalo2015Filter_out              , "trig_Flag_CSCTightHalo2015Filter_accept/I"              ) ;
   tree_out.Branch("trig_Flag_globalTightHalo2016Filter_accept"         , &trig_Flag_globalTightHalo2016Filter_out           , "trig_Flag_globalTightHalo2016Filter_accept/I"           ) ;
   tree_out.Branch("trig_Flag_globalSuperTightHalo2016Filter_accept"    , &trig_Flag_globalSuperTightHalo2016Filter_out      , "trig_Flag_globalSuperTightHalo2016Filter_accept/I"      ) ;
   tree_out.Branch("trig_Flag_goodVertices_accept"                      , &trig_Flag_goodVertices_out                        , "trig_Flag_goodVertices_accept/I"                        ) ;
   tree_out.Branch("trig_Flag_HcalStripHaloFilter_accept"               , &trig_Flag_HcalStripHaloFilter_out                 , "trig_Flag_HcalStripHaloFilter_accept/I"                 ) ;
   tree_out.Branch("trig_Flag_hcalLaserEventFilter_accept"              , &trig_Flag_hcalLaserEventFilter_out                , "trig_Flag_hcalLaserEventFilter_accept/I"                ) ;
   tree_out.Branch("trig_Flag_EcalDeadCellTriggerPrimitiveFilter_accept", &trig_Flag_EcalDeadCellTriggerPrimitiveFilter_out  , "trig_Flag_EcalDeadCellTriggerPrimitiveFilter_accept/I"  ) ;
   tree_out.Branch("trig_Flag_EcalDeadCellBoundaryEnergyFilter_accept"  , &trig_Flag_EcalDeadCellBoundaryEnergyFilter_out    , "trig_Flag_EcalDeadCellBoundaryEnergyFilter_accept/I"    ) ;
   tree_out.Branch("trig_Flag_ecalLaserCorrFilter_accept"               , &trig_Flag_ecalLaserCorrFilter_out                 , "trig_Flag_ecalLaserCorrFilter_accept/I"                 ) ;
   tree_out.Branch("trig_Flag_chargedHadronTrackResolutionFilter_accept", &trig_Flag_chargedHadronTrackResolutionFilter_out  , "trig_Flag_chargedHadronTrackResolutionFilter_accept/I"  ) ;
   tree_out.Branch("trig_Flag_muonBadTrackFilter_accept"                , &trig_Flag_muonBadTrackFilter_out                  , "trig_Flag_muonBadTrackFilter_accept/I"                  ) ;
   tree_out.Branch("trig_Flag_BadPFMuonFilter_accept"                   , &trig_Flag_BadPFMuonFilter_out                     , "trig_Flag_BadPFMuonFilter_accept/I"                     ) ;
   tree_out.Branch("trig_Flag_BadChargedCandidateFilter_accept"         , &trig_Flag_BadChargedCandidateFilter_out           , "trig_Flag_BadChargedCandidateFilter_accept/I"           ) ;
   tree_out.Branch("trig_Flag_eeBadScFilter_accept"                     , &trig_Flag_eeBadScFilter_out                       , "trig_Flag_eeBadScFilter_accept/I"                       ) ;
   tree_out.Branch("trig_Flag_trkPOG_manystripclus53X_accept"           , &trig_Flag_trkPOG_manystripclus53X_out             , "trig_Flag_trkPOG_manystripclus53X_accept/I"             ) ;
   tree_out.Branch("trig_Flag_trkPOG_toomanystripclus53X_accept"        , &trig_Flag_trkPOG_toomanystripclus53X_out          , "trig_Flag_trkPOG_toomanystripclus53X_accept/I"          ) ;
   tree_out.Branch("trig_Flag_trkPOG_logErrorTooManyClusters_accept"    , &trig_Flag_trkPOG_logErrorTooManyClusters_out      , "trig_Flag_trkPOG_logErrorTooManyClusters_accept/I"      ) ;
   tree_out.Branch("trig_Flag_METFilters_accept"                        , &trig_Flag_METFilters_out                          , "trig_Flag_METFilters_accept/I"                          ) ;
   tree_out.Branch("rho"                        , &rho_out                   , "rho/F"                          ) ;

   tree_out.Branch("trig_Ele23_Ele12"      , &trig_Ele23_Ele12_out        , "trig_Ele23_Ele12/I"        ) ;
   tree_out.Branch("trig_DEle33"           , &trig_DEle33_out             , "trig_DEle33/I"             ) ;
   tree_out.Branch("trig_DEle33_MW"        , &trig_DEle33_MW_out          , "trig_DEle33_MW/I"          ) ;
   tree_out.Branch("trig_DEle33_CaloId"    , &trig_DEle33_CaloId_out      , "trig_DEle33_CaloId/I"      ) ;
   tree_out.Branch("trig_Ele27"            , &trig_Ele27_out              , "trig_Ele27/I"              ) ;
   tree_out.Branch("trig_Mu8_Ele23"        , &trig_Mu8_Ele23_out          , "trig_Mu8_Ele23/I"          ) ;
   tree_out.Branch("trig_Mu23_Ele12"       , &trig_Mu23_Ele12_out         , "trig_Mu23_Ele12/I"         ) ;
   tree_out.Branch("trig_Mu8_Ele23_DZ"     , &trig_Mu8_Ele23_DZ_out       , "trig_Mu8_Ele23_DZ/I"       ) ;
   tree_out.Branch("trig_Mu23_Ele12_DZ"    , &trig_Mu23_Ele12_DZ_out      , "trig_Mu23_Ele12_DZ/I"      ) ;
   tree_out.Branch("trig_Mu30_Ele30"       , &trig_Mu30_Ele30_out         , "trig_Mu30_Ele30/I"         ) ;
   tree_out.Branch("trig_Mu33_Ele33"       , &trig_Mu33_Ele33_out         , "trig_Mu33_Ele33/I"         ) ;
   tree_out.Branch("trig_Mu17_TkMu8"       , &trig_Mu17_TkMu8_out         , "trig_Mu17_TkMu8/I"         ) ;
   tree_out.Branch("trig_Mu17_Mu8"         , &trig_Mu17_Mu8_out           , "trig_Mu17_Mu8/I"           ) ;
   tree_out.Branch("trig_Mu17_TkMu8_DZ"    , &trig_Mu17_TkMu8_DZ_out      , "trig_Mu17_TkMu8_DZ/I"      ) ;
   tree_out.Branch("trig_Mu17_Mu8_DZ"      , &trig_Mu17_Mu8_DZ_out        , "trig_Mu17_Mu8_DZ/I"        ) ;
   tree_out.Branch("trig_Mu30_TkMu11"      , &trig_Mu30_TkMu11_out        , "trig_Mu30_TkMu11/I"        ) ;
   tree_out.Branch("trig_IsoMu24"          , &trig_IsoMu24_out            , "trig_IsoMu24/I"            ) ;
   tree_out.Branch("trig_IsoTkMu24"        , &trig_IsoTkMu24_out          , "trig_IsoTkMu24/I"          ) ;
   tree_out.Branch("trig_HLT_PFHT300_PFMET110"            , &trig_HLT_PFHT300_PFMET110_out                    , "trig_HLT_PFHT300_PFMET110/I"                    ) ;
   tree_out.Branch("trig_HLT_MET200"                      , &trig_HLT_MET200_out                              , "trig_HLT_MET200/I"                              ) ;
   tree_out.Branch("trig_HLT_PFMET300"                    , &trig_HLT_PFMET300_out                            , "trig_HLT_PFMET300/I"                            ) ;
   tree_out.Branch("trig_HLT_PFMET120_PFMHT120_IDTight"   , &trig_HLT_PFMET120_PFMHT120_IDTight_out           , "trig_HLT_PFMET120_PFMHT120_IDTight/I"           ) ;
   tree_out.Branch("trig_HLT_PFMET170_HBHECleaned"        , &trig_HLT_PFMET170_HBHECleaned_out                , "trig_HLT_PFMET170_HBHECleaned/I"                ) ;
   tree_out.Branch("trig_HLT_MET75_IsoTrk50"              , &trig_HLT_MET75_IsoTrk50_out                      , "trig_HLT_MET75_IsoTrk50/I"                      ) ;
   tree_out.Branch("trig_DEle33_unseed_eta"        , &trig_DEle33_unseed_eta_out             ) ;
   tree_out.Branch("trig_DEle33_unseed_phi"        , &trig_DEle33_unseed_phi_out             ) ;
   tree_out.Branch("trig_DEle33_MW_unseed_eta"     , &trig_DEle33_MW_unseed_eta_out          ) ;
   tree_out.Branch("trig_DEle33_MW_unseed_phi"     , &trig_DEle33_MW_unseed_phi_out          ) ;
   tree_out.Branch("Met_et"                 , &Met_et_out                  , "Met_et/F"                  ) ;
   tree_out.Branch("Met_phi"                , &Met_phi_out                 , "Met_phi/F"                 ) ;
   tree_out.Branch("MET_T1Txy_et"           , &MET_T1Txy_et_out            , "MET_T1Txy_et/F"            ) ;
   tree_out.Branch("MET_T1Txy_phi"          , &MET_T1Txy_phi_out           , "MET_T1Txy_phi/F"           ) ;
   tree_out.Branch("MET_T1Txy_significance" , &MET_T1Txy_significance_out  , "MET_T1Txy_significance/F"  ) ;
   tree_out.Branch("MET_T1JetEnDown_Pt_out" , &MET_T1JetEnDown_Pt_out      , "MET_T1JetEnDown_Pt_out/F"  ) ;
   tree_out.Branch("MET_T1JetEnDown_phi_out", &MET_T1JetEnDown_phi_out     , "MET_T1JetEnDown_phi_out/F" ) ;
   tree_out.Branch("MET_T1JetEnUp_Pt_out"   , &MET_T1JetEnUp_Pt_out        , "MET_T1JetEnUp_Pt_out/F"    ) ;
   tree_out.Branch("MET_T1JetEnUp_phi_out"  , &MET_T1JetEnUp_phi_out       , "MET_T1JetEnUp_phi_out/F"   ) ;
   tree_out.Branch("MET_T1JetResDown_Pt_out" , &MET_T1JetResDown_Pt_out      , "MET_T1JetResDown_Pt_out/F"  ) ;
   tree_out.Branch("MET_T1JetResDown_phi_out", &MET_T1JetResDown_phi_out     , "MET_T1JetResDown_phi_out/F" ) ;
   tree_out.Branch("MET_T1JetResUp_Pt_out"   , &MET_T1JetResUp_Pt_out        , "MET_T1JetResUp_Pt_out/F"    ) ;
   tree_out.Branch("MET_T1JetResUp_phi_out"  , &MET_T1JetResUp_phi_out       , "MET_T1JetResUp_phi_out/F"   ) ;
   tree_out.Branch("MET_T1UnclusteredEnUp_Pt_out"    , &MET_T1UnclusteredEnUp_Pt_out         , "MET_T1UnclusteredEnUp_Pt_out/F"     ) ;
   tree_out.Branch("MET_T1UnclusteredEnUp_Px_out"    , &MET_T1UnclusteredEnUp_Px_out         , "MET_T1UnclusteredEnUp_Px_out/F"     ) ;
   tree_out.Branch("MET_T1UnclusteredEnUp_Py_out"    , &MET_T1UnclusteredEnUp_Py_out         , "MET_T1UnclusteredEnUp_Py_out/F"     ) ;
   tree_out.Branch("MET_T1UnclusteredEnDown_Pt_out"  , &MET_T1UnclusteredEnDown_Pt_out       , "MET_T1UnclusteredEnDown_Pt_out/F"   ) ;
   tree_out.Branch("MET_T1UnclusteredEnDown_Px_out"  , &MET_T1UnclusteredEnDown_Px_out       , "MET_T1UnclusteredEnDown_Px_out/F"   ) ;
   tree_out.Branch("MET_T1UnclusteredEnDown_Py_out"  , &MET_T1UnclusteredEnDown_Py_out       , "MET_T1UnclusteredEnDown_Py_out/F"   ) ;
   tree_out.Branch("electrons_pt"         , &electrons_pt               ) ;
   tree_out.Branch("electrons_eta"        , &electrons_eta              ) ;
   tree_out.Branch("electrons_sc_eta"     , &electrons_sc_eta           ) ;
   tree_out.Branch("electrons_phi"        , &electrons_phi              ) ;
   tree_out.Branch("electrons_sc_phi"     , &electrons_sc_phi           ) ;
   tree_out.Branch("electrons_charge"     , &electrons_charge           ) ;
   tree_out.Branch("electrons_tight_ID"   , &electrons_tight_ID         ) ;
   tree_out.Branch("electrons_74_pt"      , &electrons_74_pt            ) ;
   tree_out.Branch("electrons_74_eta"     , &electrons_74_eta           ) ;
   tree_out.Branch("electrons_74_sc_eta"  , &electrons_74_sc_eta        ) ;
   tree_out.Branch("electrons_74_phi"     , &electrons_74_phi           ) ;
   tree_out.Branch("electrons_74_sc_phi"  , &electrons_74_sc_phi        ) ;
   tree_out.Branch("electrons_74_charge"  , &electrons_74_charge        ) ;
   tree_out.Branch("electrons_74_tight_ID", &electrons_74_tight_ID      ) ;
   tree_out.Branch("heeps_80_et"                        , &heeps_80_et                        );
   tree_out.Branch("heeps_80_eta"                       , &heeps_80_eta                       );
   tree_out.Branch("heeps_80_sc_eta"                    , &heeps_80_sc_eta                    );
   tree_out.Branch("heeps_80_phi"                       , &heeps_80_phi                       );
   tree_out.Branch("heeps_80_sc_phi"                    , &heeps_80_sc_phi                    );
   tree_out.Branch("heeps_80_charge"                    , &heeps_80_charge                    );
   tree_out.Branch("heeps_80_isHEEP7"                   , &heeps_80_isHEEP7                   );
   tree_out.Branch("heeps_80_PreSelection"              , &heeps_80_PreSelection              );
   tree_out.Branch("heeps_74_et"                        , &heeps_74_et                        );
   tree_out.Branch("heeps_74_eta"                       , &heeps_74_eta                       );
   tree_out.Branch("heeps_74_sc_eta"                    , &heeps_74_sc_eta                    );
   tree_out.Branch("heeps_74_phi"                       , &heeps_74_phi                       );
   tree_out.Branch("heeps_74_sc_phi"                    , &heeps_74_sc_phi                    );
   tree_out.Branch("heeps_74_charge"                    , &heeps_74_charge                    );
   tree_out.Branch("heeps_74_isHEEP7"                   , &heeps_74_isHEEP7                   );
   tree_out.Branch("heeps_74_PreSelection"              , &heeps_74_PreSelection              );
   tree_out.Branch("heeps_74_dPhiIn"                    , &heeps_74_dPhiIn                    ); 
   tree_out.Branch("heeps_74_Sieie"                     , &heeps_74_Sieie                     ); 
   tree_out.Branch("heeps_74_missingHits"               , &heeps_74_missingHits               ); 
   tree_out.Branch("heeps_74_dxyFirstPV"                , &heeps_74_dxyFirstPV                ); 
   tree_out.Branch("heeps_74_HOverE"                    , &heeps_74_HOverE                    ); 
   tree_out.Branch("heeps_74_E1x5OverE5x5"              , &heeps_74_E1x5OverE5x5              ); 
   tree_out.Branch("heeps_74_E2x5OverE5x5"              , &heeps_74_E2x5OverE5x5              ); 
   tree_out.Branch("heeps_74_isolEMHadDepth1"           , &heeps_74_isolEMHadDepth1           ); 
   tree_out.Branch("heeps_74_IsolPtTrks"                , &heeps_74_IsolPtTrks                ); 
   tree_out.Branch("heeps_74_EcalDriven"                , &heeps_74_EcalDriven                ); 
   tree_out.Branch("heeps_74_dEtaIn"                    , &heeps_74_dEtaIn                    ); 
   tree_out.Branch("heeps_74_match"                     , &heeps_74_match                     );
   tree_out.Branch("heeps_74_B_EnScaleUp_et"            , &heeps_74_B_EnScaleUp_et            );
   tree_out.Branch("heeps_74_B_EnScaleUp_eta"           , &heeps_74_B_EnScaleUp_eta           );
   tree_out.Branch("heeps_74_B_EnScaleUp_sc_eta"        , &heeps_74_B_EnScaleUp_sc_eta        );
   tree_out.Branch("heeps_74_B_EnScaleUp_phi"           , &heeps_74_B_EnScaleUp_phi           );
   tree_out.Branch("heeps_74_B_EnScaleUp_sc_phi"        , &heeps_74_B_EnScaleUp_sc_phi        );
   tree_out.Branch("heeps_74_B_EnScaleUp_charge"        , &heeps_74_B_EnScaleUp_charge        );
   tree_out.Branch("heeps_74_B_EnScaleUp_isHEEP7"       , &heeps_74_B_EnScaleUp_isHEEP7       );
   tree_out.Branch("heeps_74_B_EnScaleUp_PreSelection"  , &heeps_74_B_EnScaleUp_PreSelection  );
   tree_out.Branch("heeps_74_B_EnScaleDown_et"          , &heeps_74_B_EnScaleDown_et          );
   tree_out.Branch("heeps_74_B_EnScaleDown_eta"         , &heeps_74_B_EnScaleDown_eta         );
   tree_out.Branch("heeps_74_B_EnScaleDown_sc_eta"      , &heeps_74_B_EnScaleDown_sc_eta      );
   tree_out.Branch("heeps_74_B_EnScaleDown_phi"         , &heeps_74_B_EnScaleDown_phi         );
   tree_out.Branch("heeps_74_B_EnScaleDown_sc_phi"      , &heeps_74_B_EnScaleDown_sc_phi      );
   tree_out.Branch("heeps_74_B_EnScaleDown_charge"      , &heeps_74_B_EnScaleDown_charge      );
   tree_out.Branch("heeps_74_B_EnScaleDown_isHEEP7"     , &heeps_74_B_EnScaleDown_isHEEP7     );
   tree_out.Branch("heeps_74_B_EnScaleDown_PreSelection", &heeps_74_B_EnScaleDown_PreSelection);
   tree_out.Branch("heeps_74_E_EnScaleUp_et"            , &heeps_74_E_EnScaleUp_et            );
   tree_out.Branch("heeps_74_E_EnScaleUp_eta"           , &heeps_74_E_EnScaleUp_eta           );
   tree_out.Branch("heeps_74_E_EnScaleUp_sc_eta"        , &heeps_74_E_EnScaleUp_sc_eta        );
   tree_out.Branch("heeps_74_E_EnScaleUp_phi"           , &heeps_74_E_EnScaleUp_phi           );
   tree_out.Branch("heeps_74_E_EnScaleUp_sc_phi"        , &heeps_74_E_EnScaleUp_sc_phi        );
   tree_out.Branch("heeps_74_E_EnScaleUp_charge"        , &heeps_74_E_EnScaleUp_charge        );
   tree_out.Branch("heeps_74_E_EnScaleUp_isHEEP7"       , &heeps_74_E_EnScaleUp_isHEEP7       );
   tree_out.Branch("heeps_74_E_EnScaleUp_PreSelection"  , &heeps_74_E_EnScaleUp_PreSelection  );
   tree_out.Branch("heeps_74_E_EnScaleDown_et"          , &heeps_74_E_EnScaleDown_et          );
   tree_out.Branch("heeps_74_E_EnScaleDown_eta"         , &heeps_74_E_EnScaleDown_eta         );
   tree_out.Branch("heeps_74_E_EnScaleDown_sc_eta"      , &heeps_74_E_EnScaleDown_sc_eta      );
   tree_out.Branch("heeps_74_E_EnScaleDown_phi"         , &heeps_74_E_EnScaleDown_phi         );
   tree_out.Branch("heeps_74_E_EnScaleDown_sc_phi"      , &heeps_74_E_EnScaleDown_sc_phi      );
   tree_out.Branch("heeps_74_E_EnScaleDown_charge"      , &heeps_74_E_EnScaleDown_charge      );
   tree_out.Branch("heeps_74_E_EnScaleDown_isHEEP7"     , &heeps_74_E_EnScaleDown_isHEEP7     );
   tree_out.Branch("heeps_74_E_EnScaleDown_PreSelection", &heeps_74_E_EnScaleDown_PreSelection);
   tree_out.Branch("muons_pt"            , &muons_pt                    ) ;
   tree_out.Branch("muons_pt_rochest"    , &muons_pt_rochest            ) ;
   tree_out.Branch("muons_eta"           , &muons_eta                   ) ;
   tree_out.Branch("muons_phi"           , &muons_phi                   ) ;
   tree_out.Branch("muons_charge"        , &muons_charge                ) ;
   tree_out.Branch("muons_tight_ID"      , &muons_tight_ID              ) ;
   tree_out.Branch("muons_pfIso"         , &muons_pfIso                 ) ;
   tree_out.Branch("muons_match"         , &muons_match                 ) ;
   tree_out.Branch("muons_trackerLayer"  , &muons_trackerLayer          ) ;
   tree_out.Branch("muons_rochester_sf"  , &muons_rochester_sf          ) ;
   tree_out.Branch("jets_pt"             , &jets_pt          ) ;
   tree_out.Branch("jets_eta"            , &jets_eta         ) ;
   tree_out.Branch("jets_phi"            , &jets_phi         ) ;
   tree_out.Branch("jets_mass"           , &jets_mass        ) ;
   tree_out.Branch("jets_energy"         , &jets_energy      ) ;
   tree_out.Branch("jets_CSV"            , &jets_CSV         ) ;
   tree_out.Branch("jets_loose_ID"       , &jets_loose_ID    ) ;
   tree_out.Branch("jets_BtagSF_medium"            , &jets_BtagSF_medium               ) ;
   tree_out.Branch("jets_BtagSFbcUp_medium"        , &jets_BtagSFbcUp_medium           ) ;
   tree_out.Branch("jets_BtagSFbcDown_medium"      , &jets_BtagSFbcDown_medium         ) ;
   tree_out.Branch("jets_BtagSFudsgUp_medium"      , &jets_BtagSFudsgUp_medium         ) ;
   tree_out.Branch("jets_BtagSFudsgDown_medium"    , &jets_BtagSFudsgDown_medium       ) ;
   tree_out.Branch("jets_SmearedJetResUp_pt"       , &jets_SmearedJetResUp_pt          ) ;
   tree_out.Branch("jets_SmearedJetResUp_energy"   , &jets_SmearedJetResUp_energy      ) ;
   tree_out.Branch("jets_SmearedJetResDown_pt"     , &jets_SmearedJetResDown_pt        ) ;
   tree_out.Branch("jets_SmearedJetResDown_energy" , &jets_SmearedJetResDown_energy    ) ;
   tree_out.Branch("jets_EnUp_pt"                  , &jets_EnUp_pt                     ) ;
   tree_out.Branch("jets_EnUp_energy"              , &jets_EnUp_energy                 ) ;
   tree_out.Branch("jets_EnDown_pt"                , &jets_EnDown_pt                   ) ;
   tree_out.Branch("jets_EnDown_energy"            , &jets_EnDown_energy               ) ;
   tree_out.Branch("LHE_sys_weight"                , &LHE_sys_weight                   ) ;
   tree_out.Branch("LHE_sys_id"                    , &LHE_sys_id                       ) ;


   tree_out.Branch("LHE_Z_mass"      , &LHE_Z_mass        , "LHE_Z_mass/F"            ) ;
   tree_out.Branch("Z_region"        , &Z_region          , "Z_region/F"              ) ;
   tree_out.Branch("w_LHE"           , &LHE_weight        , "w_LHE/F"                 ) ;
   tree_out.Branch("w_PU_combined"   , &w_PU_combined_out , "w_PU_combined/F"         ) ;
   tree_out.Branch("w_PU_silver_down", &w_PU_silver_down_out , "w_PU_silver_down/F"   ) ;
   tree_out.Branch("w_PU_silver_up"  , &w_PU_silver_up_out , "w_PU_silver_down/F"     ) ;
   
   TRandom3 rand ;
   Long64_t nbytes = 0, nb = 0;
   bool tw_study=true;
   bool Zprime_study=false;
   bool do_EnergyCorrect_74=true;
   bool do_EnergySmear=false;
   if(isData==false) do_EnergyCorrect_74=false;
   else do_EnergySmear=false;
   RoccoR  rc("/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/Scale_Factor/rcdata.2016.v3"); //directory path as input for now; initialize only once, contains all variations
   for (Long64_t jentry=0; jentry<nentries;jentry++){
//   for (Long64_t jentry=0; jentry<100;jentry++){
   
//// Init trigger //////////
   trig_Ele23_Ele12_fire  =-1; 
   trig_DEle33_fire       =-1;
   trig_DEle33_MW_fire    =-1;
   trig_DEle33_CaloId_fire=-1;
   trig_Ele27_fire        =-1;
   trig_Mu8_Ele23_fire    =-1;
   trig_Mu23_Ele12_fire   =-1;
   trig_Mu8_Ele23_DZ_fire =-1;
   trig_Mu23_Ele12_DZ_fire=-1;
   trig_Mu30_Ele30_fire   =-1;
   trig_Mu33_Ele33_fire   =-1;
   trig_Mu17_TkMu8_fire   =-1;
   trig_Mu17_Mu8_fire     =-1;
   trig_Mu17_TkMu8_DZ_fire=-1;
   trig_Mu17_Mu8_DZ_fire  =-1;
   trig_Mu30_TkMu11_fire  =-1;
   trig_IsoMu24_fire      =-1; 
   trig_IsoTkMu24_fire    =-1; 
   trig_HLT_PFHT300_PFMET110_fire          =-1; 
   trig_HLT_MET200_fire                    =-1; 
   trig_HLT_PFMET300_fire                  =-1; 
   trig_HLT_PFMET120_PFMHT120_IDTight_fire =-1; 
   trig_HLT_PFMET170_HBHECleaned_fire      =-1; 
   trig_HLT_MET75_IsoTrk50_fire            =-1; 

////////Init LHE weight //////////////////////
   LHE_weight_nominal=-1;

//////////////////////////////

//   displayProgress(jentry, nentries) ;
//   std::cout<<"event:"<<jentry<<std::endl;   
   Long64_t ientry = LoadTree(jentry);
   if (ientry < 0) break;
   nb = fChain->GetEntry(jentry);   
   nbytes += nb;
//   if(isData==true){ if( ev_run<Run_low || ev_run>Run_high) continue;}
      
      if(true==isWW || true==isTTbar){
      TLorentzVector MC_p4_1(1,0,0,0);
      TLorentzVector MC_p4_2(1,0,0,0);
      float Mass_treshold=0;
      bool accept=true;
      if(true==isWW) Mass_treshold=200;
      if(true==isTTbar) Mass_treshold=500;
      for(unsigned iMC=0 ; iMC<mc_n ; ++iMC){
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
      LHE_weight=1;
      LHE_Z_mass=1;
      if(isData==false){
      float tmp_weight=1;
      for(unsigned int iL=0; iL<LHE_Pt->size();iL++){
      //if(LHE_status->at(iL)>0 && abs(LHE_pdgid->at(iL))==6) tmp_weight=tmp_weight*exp(0.0615-0.0005*LHE_Pt->at(iL));
      if( abs(LHE_pdgid->at(iL))==6) tmp_weight=tmp_weight*exp(0.0615-0.0005*LHE_Pt->at(iL));
      }
      LHE_weight=sqrt(tmp_weight); 
      if(Zprime_study){
      TLorentzVector MC_p4_Z(0,0,0,0);
      for(unsigned int iL=0; iL<LHE_Pt->size();iL++){
      if(LHE_status->at(iL)>0 && abs(LHE_pdgid->at(iL))==23) MC_p4_Z.SetPtEtaPhiE(LHE_Pt->at(iL),LHE_Eta->at(iL),LHE_Phi->at(iL),LHE_E->at(iL));
      }
      LHE_Z_mass=MC_p4_Z.M();
      int N_Barrel=0;
      int N_Endcap=0;
      int N_Gap=0;
      for(unsigned int iL=0; iL<LHE_Pt->size();iL++){
      if(LHE_status->at(iL)>0 && abs(LHE_pdgid->at(iL))==11 && fabs(LHE_Eta->at(iL))<1.4442) N_Barrel++;
      else if(LHE_status->at(iL)>0 && abs(LHE_pdgid->at(iL))==11 && fabs(LHE_Eta->at(iL))<1.566) N_Gap++;
      else if(LHE_status->at(iL)>0 && abs(LHE_pdgid->at(iL))==11 && fabs(LHE_Eta->at(iL))<2.5  ) N_Endcap++;
      }
      if(N_Barrel==2)Z_region=1;
      else if(N_Endcap==2)Z_region=2;
      else if((N_Barrel+N_Endcap)==2)Z_region=3;
      else Z_region=4;
      }
      }
//// clear vector //////////////////////
      vector<float>().swap(trig_DEle33_unseed_eta_out   ); 
      vector<float>().swap(trig_DEle33_unseed_phi_out   );
      vector<float>().swap(trig_DEle33_MW_unseed_eta_out);
      vector<float>().swap(trig_DEle33_MW_unseed_phi_out);
      vector<int>  ().swap(pv_isValid_out         );
      vector<int>  ().swap(pv_ndof_out            );  
      vector<int>  ().swap(pv_nTracks_out         ); 
      vector<int>  ().swap(pv_totTrackSize_out    ); 
      vector<float>().swap(pv_normalizedChi2_out);
      vector<float>().swap(electrons_pt         );
      vector<float>().swap(electrons_eta        );
      vector<float>().swap(electrons_sc_eta     );
      vector<float>().swap(electrons_phi        );
      vector<float>().swap(electrons_sc_phi     );
      vector<int>  ().swap(electrons_charge     );
      vector<int>  ().swap(electrons_tight_ID   );
      vector<float>().swap(electrons_74_pt      );
      vector<float>().swap(electrons_74_eta     );
      vector<float>().swap(electrons_74_sc_eta  );
      vector<float>().swap(electrons_74_phi     );
      vector<float>().swap(electrons_74_sc_phi  );
      vector<int>  ().swap(electrons_74_charge  );
      vector<int>  ().swap(electrons_74_tight_ID);
      vector<float>().swap(heeps_80_et                        );
      vector<float>().swap(heeps_80_eta                       );
      vector<float>().swap(heeps_80_sc_eta                    );
      vector<float>().swap(heeps_80_phi                       );
      vector<float>().swap(heeps_80_sc_phi                    );
      vector<int>  ().swap(heeps_80_charge                    );
      vector<int>  ().swap(heeps_80_isHEEP7                   );
      vector<int>  ().swap(heeps_80_PreSelection              );
      vector<float>().swap(heeps_74_et                        );
      vector<float>().swap(heeps_74_eta                       );
      vector<float>().swap(heeps_74_sc_eta                    );
      vector<float>().swap(heeps_74_phi                       );
      vector<float>().swap(heeps_74_sc_phi                    );
      vector<int>  ().swap(heeps_74_charge                    );
      vector<int>  ().swap(heeps_74_isHEEP7                   );
      vector<int>  ().swap(heeps_74_PreSelection              );
      vector<float>().swap(heeps_74_dPhiIn                    ); 
      vector<float>().swap(heeps_74_Sieie                     ); 
      vector<float>().swap(heeps_74_missingHits               ); 
      vector<float>().swap(heeps_74_dxyFirstPV                ); 
      vector<float>().swap(heeps_74_HOverE                    ); 
      vector<float>().swap(heeps_74_E1x5OverE5x5              ); 
      vector<float>().swap(heeps_74_E2x5OverE5x5              ); 
      vector<float>().swap(heeps_74_isolEMHadDepth1           ); 
      vector<float>().swap(heeps_74_IsolPtTrks                ); 
      vector<float>().swap(heeps_74_EcalDriven                ); 
      vector<float>().swap(heeps_74_dEtaIn                    ); 
      vector<int>  ().swap(heeps_74_match                     );
      vector<float>().swap(heeps_74_B_EnScaleUp_et            );
      vector<float>().swap(heeps_74_B_EnScaleUp_eta           );
      vector<float>().swap(heeps_74_B_EnScaleUp_sc_eta        );
      vector<float>().swap(heeps_74_B_EnScaleUp_phi           );
      vector<float>().swap(heeps_74_B_EnScaleUp_sc_phi        );
      vector<int>  ().swap(heeps_74_B_EnScaleUp_charge        );
      vector<int>  ().swap(heeps_74_B_EnScaleUp_isHEEP7       );
      vector<int>  ().swap(heeps_74_B_EnScaleUp_PreSelection  );
      vector<float>().swap(heeps_74_B_EnScaleDown_et          );
      vector<float>().swap(heeps_74_B_EnScaleDown_eta         );
      vector<float>().swap(heeps_74_B_EnScaleDown_sc_eta      );
      vector<float>().swap(heeps_74_B_EnScaleDown_phi         );
      vector<float>().swap(heeps_74_B_EnScaleDown_sc_phi      );
      vector<int>  ().swap(heeps_74_B_EnScaleDown_charge      );
      vector<int>  ().swap(heeps_74_B_EnScaleDown_isHEEP7     );
      vector<int>  ().swap(heeps_74_B_EnScaleDown_PreSelection);
      vector<float>().swap(heeps_74_E_EnScaleUp_et            );
      vector<float>().swap(heeps_74_E_EnScaleUp_eta           );
      vector<float>().swap(heeps_74_E_EnScaleUp_sc_eta        );
      vector<float>().swap(heeps_74_E_EnScaleUp_phi           );
      vector<float>().swap(heeps_74_E_EnScaleUp_sc_phi        );
      vector<int>  ().swap(heeps_74_E_EnScaleUp_charge        );
      vector<int>  ().swap(heeps_74_E_EnScaleUp_isHEEP7       );
      vector<int>  ().swap(heeps_74_E_EnScaleUp_PreSelection  );
      vector<float>().swap(heeps_74_E_EnScaleDown_et          );
      vector<float>().swap(heeps_74_E_EnScaleDown_eta         );
      vector<float>().swap(heeps_74_E_EnScaleDown_sc_eta      );
      vector<float>().swap(heeps_74_E_EnScaleDown_phi         );
      vector<float>().swap(heeps_74_E_EnScaleDown_sc_phi      );
      vector<int>  ().swap(heeps_74_E_EnScaleDown_charge      );
      vector<int>  ().swap(heeps_74_E_EnScaleDown_isHEEP7     );
      vector<int>  ().swap(heeps_74_E_EnScaleDown_PreSelection);
      vector<float>().swap(muons_pt             );
      vector<float>().swap(muons_pt_rochest     );
      vector<float>().swap(muons_eta            );
      vector<float>().swap(muons_phi            );
      vector<int>  ().swap(muons_charge         );
      vector<int>  ().swap(muons_tight_ID       );
      vector<int>  ().swap(muons_pfIso          );
      vector<int>  ().swap(muons_match          );
      vector<int>  ().swap(muons_trackerLayer   );
      vector<float>().swap(muons_rochester_sf   );
      vector<float>().swap(jets_pt              ); 
      vector<float>().swap(jets_eta             ); 
      vector<float>().swap(jets_phi             ); 
      vector<float>().swap(jets_mass            ); 
      vector<float>().swap(jets_energy          ); 
      vector<float>().swap(jets_CSV             ); 
      vector<int>  ().swap(jets_loose_ID        ); 
      vector<float>().swap(jets_BtagSF_medium           ); 
      vector<float>().swap(jets_BtagSFbcUp_medium       ); 
      vector<float>().swap(jets_BtagSFbcDown_medium     ); 
      vector<float>().swap(jets_BtagSFudsgUp_medium     ); 
      vector<float>().swap(jets_BtagSFudsgDown_medium   ); 
      vector<float>().swap(jets_SmearedJetResUp_pt      ); 
      vector<float>().swap(jets_SmearedJetResUp_energy  ); 
      vector<float>().swap(jets_SmearedJetResDown_pt    ); 
      vector<float>().swap(jets_SmearedJetResDown_energy);
      vector<float>().swap(jets_EnUp_pt                 ); 
      vector<float>().swap(jets_EnUp_energy             ); 
      vector<float>().swap(jets_EnDown_pt               ); 
      vector<float>().swap(jets_EnDown_energy           ); 
      vector<float>().swap(LHE_sys_weight               );
      vector<int>  ().swap(LHE_sys_id                   );
//// clear vector //////////////////////

      ev_event_out            = ev_event                  ;
      ev_run_out              = ev_run                    ;
      ev_luminosityBlock_out  = ev_luminosityBlock        ;
      rho_out                 = ev_fixedGridRhoFastjetAll ;
      trig_Flag_HBHENoiseFilter_out                   = trig_Flag_HBHENoiseFilter_accept                   ; 
      trig_Flag_HBHENoiseIsoFilter_out                = trig_Flag_HBHENoiseIsoFilter_accept                ; 
      trig_Flag_CSCTightHaloFilter_out                = trig_Flag_CSCTightHaloFilter_accept                ; 
      trig_Flag_CSCTightHaloTrkMuUnvetoFilter_out     = trig_Flag_CSCTightHaloTrkMuUnvetoFilter_accept     ; 
      trig_Flag_CSCTightHalo2015Filter_out            = trig_Flag_CSCTightHalo2015Filter_accept            ; 
      trig_Flag_globalTightHalo2016Filter_out         = trig_Flag_globalTightHalo2016Filter_accept         ; 
      trig_Flag_globalSuperTightHalo2016Filter_out    = trig_Flag_globalSuperTightHalo2016Filter_accept    ; 
      trig_Flag_goodVertices_out                      = trig_Flag_goodVertices_accept                      ; 
      trig_Flag_HcalStripHaloFilter_out               = trig_Flag_HcalStripHaloFilter_accept               ; 
      trig_Flag_hcalLaserEventFilter_out              = trig_Flag_hcalLaserEventFilter_accept              ; 
      trig_Flag_EcalDeadCellTriggerPrimitiveFilter_out= trig_Flag_EcalDeadCellTriggerPrimitiveFilter_accept; 
      trig_Flag_EcalDeadCellBoundaryEnergyFilter_out  = trig_Flag_EcalDeadCellBoundaryEnergyFilter_accept  ; 
      trig_Flag_ecalLaserCorrFilter_out               = trig_Flag_ecalLaserCorrFilter_accept               ; 
      trig_Flag_chargedHadronTrackResolutionFilter_out= trig_Flag_chargedHadronTrackResolutionFilter_accept; 
      trig_Flag_muonBadTrackFilter_out                = trig_Flag_muonBadTrackFilter_accept                ; 
      trig_Flag_BadPFMuonFilter_out                   = int(trig_Flag_BadPFMuonFilter_accept          )    ;
      trig_Flag_BadChargedCandidateFilter_out         = int(trig_Flag_BadChargedCandidateFilter_accept)    ;
      trig_Flag_eeBadScFilter_out                     = trig_Flag_eeBadScFilter_accept                     ;
      trig_Flag_trkPOG_manystripclus53X_out           = trig_Flag_trkPOG_manystripclus53X_accept           ; 
      trig_Flag_trkPOG_toomanystripclus53X_out        = trig_Flag_trkPOG_toomanystripclus53X_accept        ; 
      trig_Flag_trkPOG_logErrorTooManyClusters_out    = trig_Flag_trkPOG_logErrorTooManyClusters_accept    ; 
      trig_Flag_METFilters_out                        = trig_Flag_METFilters_accept                        ;    

      event_sign           =mc_w_sign < 0 ? -1 : 1        ;                 
      pv_n_out             =pv_n                          ;
//      std::cout<<"pv_x->size()="<<pv_x->size()<<std::endl;
      for(unsigned int ip=0; ip<pv_x->size();ip++){
//      pv_isValid_out       .push_back(pv_isValid       ->at(ip)) ;
      pv_ndof_out          .push_back(pv_ndof          ->at(ip)) ;
//      pv_nTracks_out       .push_back(pv_nTracks       ->at(ip)) ;
//      pv_totTrackSize_out  .push_back(pv_totTrackSize  ->at(ip)) ;
      pv_normalizedChi2_out.push_back(pv_normalizedChi2->at(ip)) ;
      }

      bool triggerMatch = false ;
      if(true==isData){
        PU_true_out = -1 ;
        w_PU_silver_down_out    = 1 ;
        w_PU_silver_up_out      = 1 ;
        w_PU_combined_out = 1.0 ;
      }
      else{
        int PU = mc_trueNumInteractions ;
        PU_true_out = PU ;
        w_PU_combined_out      = event_sign*PU_reReco_Morind17::MC_pileup_weight(PU,0,"all");
        w_PU_silver_up_out     = event_sign*PU_reReco_Morind17::MC_pileup_weight(PU,1,"all");
        w_PU_silver_down_out   = event_sign*PU_reReco_Morind17::MC_pileup_weight(PU,2,"all");
      }
//#############   For electrons ##########################
      std::vector<electron_candidate*> electrons    ;
      std::vector<electron_candidate*> electrons_74 ;
      std::vector<electron_candidate*> heeps_80 ;
      std::vector<electron_candidate*> heeps_74 ;
      std::vector<electron_candidate*> heeps_74_Barrel_EScale_up   ;
      std::vector<electron_candidate*> heeps_74_Barrel_EScale_down ;
      std::vector<electron_candidate*> heeps_74_Endcap_EScale_up   ;
      std::vector<electron_candidate*> heeps_74_Endcap_EScale_down ;
      for(unsigned int iEl=0 ; iEl<gsf_n ; ++iEl){
        float Et     = gsf80_caloEnergy->at(iEl)*sin( gsf_theta->at(iEl) ) ; 
        float Et_74  = gsf_caloEnergy->at(iEl)*sin( gsf_theta->at(iEl) ) ; 
        float g_pt   = gsf80_pt->at(iEl) ;
        float g_pt_74= gsf_pt->at(iEl) ;
        float sc_eta = gsf_sc_eta->at(iEl); 
        float sc_phi = gsf_sc_phi->at(iEl); 
        float g_eta  = gsf_eta->at(iEl); 
        float g_phi  = gsf_phi->at(iEl); 
        int   charge = gsf_charge->at(iEl) ;
        float gsf_dxy=gsf_dxy_firstPVtx->at(iEl);
        float gsf_dz =gsf_dz_firstPVtx->at(iEl);
        if(do_EnergyCorrect_74==true){
        if(fabs(sc_eta)<1.4442)Et_74 = Et_74*1.0012 ;
        else if(fabs(sc_eta)>1.566 && fabs(sc_eta)<2.5) Et_74 = Et_74*1.0089 ;
        }
        if(do_EnergySmear==true){
        if(fabs(sc_eta)<1.4442)Et_74 = Et_74*rand.Gaus(1,0.0123) ;
        else if(fabs(sc_eta)>1.566 && fabs(sc_eta)<2.5) Et_74 = Et_74*rand.Gaus(1,0.0229) ;
        }
        int gsf_mc_match=0;
//////////////////// MC matching //////////////////
       if(isData==false){
             TLorentzVector gsf_p4(1,0,0,1);
             gsf_p4.SetPtEtaPhiM(1,g_eta,g_phi,1);
             TLorentzVector MC_p4(1,0,0,0);
             /*
             int use_status=1;
             for(unsigned iMC=0 ; iMC<mc_n ; ++iMC){
             if( abs(mc_pdgId->at(iMC)) == 11 && abs(mc_status->at(iMC)) == 23) {use_status=23;break;}
                                                   }
             */
             for(unsigned iMC=0 ; iMC<mc_n ; ++iMC){
             if( abs(mc_pdgId->at(iMC)) != 11 || (abs(mc_status->at(iMC)) !=23 && abs(mc_status->at(iMC)) !=1 )) continue;
             MC_p4.SetPtEtaPhiM(1,mc_eta->at(iMC),mc_phi->at(iMC),1); 
             if(MC_p4.DeltaR(gsf_p4)<0.1){gsf_mc_match=1;break;}
                                                   }
                        }
//////////////////////////////////////////////////////
        electron_candidate* el         = new electron_candidate(Et, g_pt, sc_eta, sc_phi, g_eta, g_phi, charge) ;
        electron_candidate* el_74      = new electron_candidate(Et_74, g_pt_74, sc_eta, sc_phi, g_eta, g_phi, charge) ;
        electron_candidate* heep_80    = new electron_candidate(Et, g_pt, sc_eta, sc_phi, g_eta, g_phi, charge) ;
        electron_candidate* heep_74    = new electron_candidate(Et_74, g_pt_74, sc_eta, sc_phi, g_eta, g_phi, charge) ;
        electron_candidate* heep_74_B_up   = (fabs(sc_eta)<1.4442)                    ? new electron_candidate(1.02*Et_74, g_pt_74, sc_eta, sc_phi, g_eta, g_phi, charge) : new electron_candidate(Et_74, g_pt_74, sc_eta, sc_phi, g_eta, g_phi, charge) ;
        electron_candidate* heep_74_B_down = (fabs(sc_eta)<1.4442)                    ? new electron_candidate(0.98*Et_74, g_pt_74, sc_eta, sc_phi, g_eta, g_phi, charge) : new electron_candidate(Et_74, g_pt_74, sc_eta, sc_phi, g_eta, g_phi, charge) ;
        electron_candidate* heep_74_E_up   = (fabs(sc_eta)>1.566 && fabs(sc_eta)<2.5) ? new electron_candidate(1.01*Et_74, g_pt_74, sc_eta, sc_phi, g_eta, g_phi, charge) : new electron_candidate(Et_74, g_pt_74, sc_eta, sc_phi, g_eta, g_phi, charge) ;
        electron_candidate* heep_74_E_down = (fabs(sc_eta)>1.566 && fabs(sc_eta)<2.5) ? new electron_candidate(0.99*Et_74, g_pt_74, sc_eta, sc_phi, g_eta, g_phi, charge) : new electron_candidate(Et_74, g_pt_74, sc_eta, sc_phi, g_eta, g_phi, charge) ;
///////////////////For TW stduy//////////////////////
        el->pass_VIDTight   = int(gsf80_Tight->at(iEl))  ;//80X
        el_74->pass_VIDTight= int(gsf_VIDTight->at(iEl)) ;//74X
        //bool tw_ele    = (el->pass_VIDTight==1    && el->pt >= 20    && fabs(el->sc_eta)<2.5    && el->region!=2    && ((fabs(sc_eta)<=1.479 && fabs(gsf_dxy)<0.05 && fabs(gsf_dz)<0.1) || (fabs(sc_eta)>1.479 && fabs(gsf_dxy)<0.1 && fabs(gsf_dz)<0.2))) ? true : false ;
        //bool tw_ele_74 = (el_74->pass_VIDTight==1 && el_74->pt >= 20 && fabs(el_74->sc_eta)<2.5 && el_74->region!=2 && ((fabs(sc_eta)<=1.479 && fabs(gsf_dxy)<0.05 && fabs(gsf_dz)<0.1) || (fabs(sc_eta)>1.479 && fabs(gsf_dxy)<0.1 && fabs(gsf_dz)<0.2))) ? true : false ; 
        bool tw_ele    = (el->pass_VIDTight==1    && el->pt >= 20    && fabs(el->eta)<2.4    && el->region!=2    && ((fabs(sc_eta)<=1.479 && fabs(gsf_dxy)<0.05 && fabs(gsf_dz)<0.1) || (fabs(sc_eta)>1.479 && fabs(gsf_dxy)<0.1 && fabs(gsf_dz)<0.2))) ? true : false ;// change to gsf_eta < 2.4
        bool tw_ele_74 = (el_74->pass_VIDTight==1 && el_74->pt >= 20 && fabs(el_74->eta)<2.4 && el_74->region!=2 && ((fabs(sc_eta)<=1.479 && fabs(gsf_dxy)<0.05 && fabs(gsf_dz)<0.1) || (fabs(sc_eta)>1.479 && fabs(gsf_dxy)<0.1 && fabs(gsf_dz)<0.2))) ? true : false ; 
        if(tw_ele    ) electrons.push_back(el) ;
        if(tw_ele_74 ) electrons_74.push_back(el_74) ;
///////////////////For Z' to ee study /////////////////////
        heep_80->apply_ID_value(gsf_deltaPhiSuperClusterTrackAtVtx->at(iEl),
                           gsf_full5x5_sigmaIetaIeta->at(iEl),
                     float(gsf_nLostInnerHits->at(iEl) ),
                      fabs(gsf_dxy_firstPVtx->at(iEl)),
                           gsf80_hadronicOverEm->at(iEl),
                           gsf_sc_energy->at(iEl),
                          (gsf_full5x5_e1x5->at(iEl)/gsf_full5x5_e5x5->at(iEl) ),
                          (gsf_full5x5_e2x5Max->at(iEl)/gsf_full5x5_e5x5->at(iEl) ),
                          (gsf80_dr03EcalRecHitSumEt->at(iEl) + gsf80_dr03HcalDepth1TowerSumEt->at(iEl) ),
                           gsf_dr03TkSumPtHEEP7->at(iEl),
                     float(gsf_ecaldrivenSeed->at(iEl)),
                           gsf_deltaEtaSeedClusterTrackAtVtx->at(iEl),
                           ev_fixedGridRhoFastjetAll) ;
        heep_80->Pass_PreSelection(gsf_full5x5_sigmaIetaIeta->at(iEl), gsf80_hadronicOverEm->at(iEl), float(gsf_nLostInnerHits->at(iEl)) , fabs(gsf_dxy_firstPVtx->at(iEl)) ); 
        heep_74->apply_ID_value(gsf_deltaPhiSuperClusterTrackAtVtx->at(iEl),
                           gsf_full5x5_sigmaIetaIeta->at(iEl),
                     float(gsf_nLostInnerHits->at(iEl) ),
                      fabs(gsf_dxy_firstPVtx->at(iEl)),
                           gsf_hadronicOverEm->at(iEl),
                           gsf_sc_energy->at(iEl),
                          (gsf_full5x5_e1x5->at(iEl)/gsf_full5x5_e5x5->at(iEl) ),
                          (gsf_full5x5_e2x5Max->at(iEl)/gsf_full5x5_e5x5->at(iEl) ),
                          (gsf_dr03EcalRecHitSumEt->at(iEl) + gsf_dr03HcalDepth1TowerSumEt->at(iEl) ),
                           gsf_dr03TkSumPtHEEP7->at(iEl),
                     float(gsf_ecaldrivenSeed->at(iEl) ),
                           gsf_deltaEtaSeedClusterTrackAtVtx->at(iEl),
                           ev_fixedGridRhoFastjetAll) ;
        heep_74->Pass_PreSelection(gsf_full5x5_sigmaIetaIeta->at(iEl), gsf_hadronicOverEm->at(iEl), float(gsf_nLostInnerHits->at(iEl)) , fabs(gsf_dxy_firstPVtx->at(iEl)) ); 
        heep_74->truthmatched =gsf_mc_match;
        if(heep_80->et>35 ) heeps_80.push_back(heep_80) ;
        if(heep_74->et>35 ) heeps_74.push_back(heep_74) ;
//////////////////////////For energy scale///////////////////////////////////
        if(isData==false){
        heep_74_B_up->apply_ID_value(gsf_deltaPhiSuperClusterTrackAtVtx->at(iEl),
                           gsf_full5x5_sigmaIetaIeta->at(iEl),
                     float(gsf_nLostInnerHits->at(iEl) ),
                      fabs(gsf_dxy_firstPVtx->at(iEl)),
                           gsf_hadronicOverEm->at(iEl),
                           gsf_sc_energy->at(iEl),
                          (gsf_full5x5_e1x5->at(iEl)/gsf_full5x5_e5x5->at(iEl) ),
                          (gsf_full5x5_e2x5Max->at(iEl)/gsf_full5x5_e5x5->at(iEl) ),
                          (gsf_dr03EcalRecHitSumEt->at(iEl) + gsf_dr03HcalDepth1TowerSumEt->at(iEl) ),
                           gsf_dr03TkSumPtHEEP7->at(iEl),
                     float(gsf_ecaldrivenSeed->at(iEl) ),
                           gsf_deltaEtaSeedClusterTrackAtVtx->at(iEl),
                           ev_fixedGridRhoFastjetAll) ;
        heep_74_B_up->Pass_PreSelection(gsf_full5x5_sigmaIetaIeta->at(iEl), gsf_hadronicOverEm->at(iEl), float(gsf_nLostInnerHits->at(iEl)) , fabs(gsf_dxy_firstPVtx->at(iEl)) ); 
        heep_74_B_down->apply_ID_value(gsf_deltaPhiSuperClusterTrackAtVtx->at(iEl),
                           gsf_full5x5_sigmaIetaIeta->at(iEl),
                     float(gsf_nLostInnerHits->at(iEl) ),
                      fabs(gsf_dxy_firstPVtx->at(iEl)),
                           gsf_hadronicOverEm->at(iEl),
                           gsf_sc_energy->at(iEl),
                          (gsf_full5x5_e1x5->at(iEl)/gsf_full5x5_e5x5->at(iEl) ),
                          (gsf_full5x5_e2x5Max->at(iEl)/gsf_full5x5_e5x5->at(iEl) ),
                          (gsf_dr03EcalRecHitSumEt->at(iEl) + gsf_dr03HcalDepth1TowerSumEt->at(iEl) ),
                           gsf_dr03TkSumPtHEEP7->at(iEl),
                     float(gsf_ecaldrivenSeed->at(iEl) ),
                           gsf_deltaEtaSeedClusterTrackAtVtx->at(iEl),
                           ev_fixedGridRhoFastjetAll) ;
        heep_74_B_down->Pass_PreSelection(gsf_full5x5_sigmaIetaIeta->at(iEl), gsf_hadronicOverEm->at(iEl), float(gsf_nLostInnerHits->at(iEl)) , fabs(gsf_dxy_firstPVtx->at(iEl)) ); 
        heep_74_E_up->apply_ID_value(gsf_deltaPhiSuperClusterTrackAtVtx->at(iEl),
                           gsf_full5x5_sigmaIetaIeta->at(iEl),
                     float(gsf_nLostInnerHits->at(iEl) ),
                      fabs(gsf_dxy_firstPVtx->at(iEl)),
                           gsf_hadronicOverEm->at(iEl),
                           gsf_sc_energy->at(iEl),
                          (gsf_full5x5_e1x5->at(iEl)/gsf_full5x5_e5x5->at(iEl) ),
                          (gsf_full5x5_e2x5Max->at(iEl)/gsf_full5x5_e5x5->at(iEl) ),
                          (gsf_dr03EcalRecHitSumEt->at(iEl) + gsf_dr03HcalDepth1TowerSumEt->at(iEl) ),
                           gsf_dr03TkSumPtHEEP7->at(iEl),
                     float(gsf_ecaldrivenSeed->at(iEl) ),
                           gsf_deltaEtaSeedClusterTrackAtVtx->at(iEl),
                           ev_fixedGridRhoFastjetAll) ;
        heep_74_E_up->Pass_PreSelection(gsf_full5x5_sigmaIetaIeta->at(iEl), gsf_hadronicOverEm->at(iEl), float(gsf_nLostInnerHits->at(iEl)) , fabs(gsf_dxy_firstPVtx->at(iEl)) ); 
        heep_74_E_down->apply_ID_value(gsf_deltaPhiSuperClusterTrackAtVtx->at(iEl),
                           gsf_full5x5_sigmaIetaIeta->at(iEl),
                     float(gsf_nLostInnerHits->at(iEl) ),
                      fabs(gsf_dxy_firstPVtx->at(iEl)),
                           gsf_hadronicOverEm->at(iEl),
                           gsf_sc_energy->at(iEl),
                          (gsf_full5x5_e1x5->at(iEl)/gsf_full5x5_e5x5->at(iEl) ),
                          (gsf_full5x5_e2x5Max->at(iEl)/gsf_full5x5_e5x5->at(iEl) ),
                          (gsf_dr03EcalRecHitSumEt->at(iEl) + gsf_dr03HcalDepth1TowerSumEt->at(iEl) ),
                           gsf_dr03TkSumPtHEEP7->at(iEl),
                     float(gsf_ecaldrivenSeed->at(iEl) ),
                           gsf_deltaEtaSeedClusterTrackAtVtx->at(iEl),
                           ev_fixedGridRhoFastjetAll) ;
        heep_74_E_down->Pass_PreSelection(gsf_full5x5_sigmaIetaIeta->at(iEl), gsf_hadronicOverEm->at(iEl), float(gsf_nLostInnerHits->at(iEl)) , fabs(gsf_dxy_firstPVtx->at(iEl)) ); 
        if(heep_74_B_up  ->et>35 ) heeps_74_Barrel_EScale_up  .push_back(heep_74_B_up)   ;
        if(heep_74_B_down->et>35 ) heeps_74_Barrel_EScale_down.push_back(heep_74_B_down) ;
        if(heep_74_E_up  ->et>35 ) heeps_74_Endcap_EScale_up  .push_back(heep_74_E_up)   ;
        if(heep_74_E_down->et>35 ) heeps_74_Endcap_EScale_down.push_back(heep_74_E_down) ;
}
/////////////////////////////////////////////////////////////
      }
//#############   For muons ##########################
      std::vector<muon_candidate*> muons ;
      for(unsigned int iMu=0 ; iMu<mu_gt_pt->size() ; ++iMu){
        if(!mu_isGlobalMuon->at(iMu))continue;
        float pt     = mu_gt_pt->at(iMu) ;
        float eta    = mu_gt_eta->at(iMu) ;
        float phi    = mu_gt_phi->at(iMu) ;
        int   charge = mu_gt_charge->at(iMu) ;
        muon_candidate* mu = new muon_candidate(pt, eta, phi, charge) ;
        mu->isTight=int(mu_isTightMuon->at(iMu));
        mu->passIso = (mu_pfIsoDbCorrected04->at(iMu) < 0.15) ? 1 : 0;
        mu->truthmatched=0;
        mu->trackerLayersWithMeasurement=mu_trackerLayersWithMeasurement->at(iMu);
        mu->rochester_sf=1;
        if(tw_study){
        if(isData==false) mu->rochester_sf=mu_rochester_sf->at(iMu);
        else              mu->rochester_sf=rc.kScaleDT(charge, pt, eta, phi, 0, 0);
        }
        if(mu->isTight==1 && mu->passIso==1 && (mu->pt*mu->rochester_sf >=20) && fabs(mu->eta)<2.4 )muons.push_back(mu);
        }
//#############   For Jets ##########################
      std::vector<jet_candidate*> jets ;
     for(unsigned int j=0; j<jet_pt->size() ; j++){
      jet_candidate* jet = new jet_candidate(jet_pt->at(j), jet_eta->at(j), jet_phi->at(j), jet_mass->at(j), jet_energy->at(j)) ;
      jet->CSV=jet_CSVv2->at(j);
      jet->pass_loose_ID = int(jet_isJetIDLoose->at(j)) ;
      if(tw_study && isData==false){
      jet->BtagSF_medium           = jet_BtagSF_medium           ->at(j);
      jet->BtagSFbcUp_medium       = jet_BtagSFbcUp_medium       ->at(j);
      jet->BtagSFbcDown_medium     = jet_BtagSFbcDown_medium     ->at(j);
      jet->BtagSFudsgUp_medium     = jet_BtagSFudsgUp_medium     ->at(j);
      jet->BtagSFudsgDown_medium   = jet_BtagSFudsgDown_medium   ->at(j);
      jet->SmearedJetResUp_pt      = jet_SmearedJetResUp_pt      ->at(j);
      jet->SmearedJetResUp_energy  = jet_SmearedJetResUp_energy  ->at(j);
      jet->SmearedJetResDown_pt    = jet_SmearedJetResDown_pt    ->at(j);
      jet->SmearedJetResDown_energy= jet_SmearedJetResDown_energy->at(j);
      jet->EnUp_pt                 = jet_EnUp_pt                 ->at(j);
      jet->EnUp_energy             = jet_EnUp_energy             ->at(j);
      jet->EnDown_pt               = jet_EnDown_pt               ->at(j);
      jet->EnDown_energy           = jet_EnDown_energy           ->at(j);
      }
      if(jet->pass_loose_ID==1) jets.push_back(jet); 
      } 
//#############   For save event ##########################
      bool for_tw= tw_study && ((electrons.size() + muons.size() >=2) || (electrons_74.size() + muons.size() >=2) ) ? true : false ;
      bool for_Zprime= Zprime_study && (heeps_80.size()>=2 || heeps_74.size()>=2 || heeps_74_Barrel_EScale_up.size()>=2 || heeps_74_Barrel_EScale_down.size()>=2 || heeps_74_Endcap_EScale_up.size()>=2 || heeps_74_Endcap_EScale_down.size()>=2) ? true : false ;
//      if(ev_event==105 || ev_event==19812 || ev_event==20085) std::cout<<"ev:"<<ev_event<<",pass="<<for_Zprime<<"n 74:"<<heeps_74.size()<<"n 80:"<<heeps_80.size()<<"n b up:"<<heeps_74_Barrel_EScale_up.size()<<"n b down:"<<heeps_74_Barrel_EScale_down.size()<<"n e up:"<<heeps_74_Endcap_EScale_up.size()<<"n e down:"<<heeps_74_Endcap_EScale_down.size()<<std::endl;
      if( for_tw || for_Zprime ){

      trig_Ele23_Ele12_out  = int(trig_Ele23_Ele12_fire  );
      trig_DEle33_out       = int(trig_DEle33_fire       );
      trig_DEle33_MW_out    = int(trig_DEle33_MW_fire    );
      trig_DEle33_CaloId_out= int(trig_DEle33_CaloId_fire);
      trig_Ele27_out        = int(trig_Ele27_fire        );
      trig_Mu8_Ele23_out    = int(trig_Mu8_Ele23_fire    );
      trig_Mu23_Ele12_out   = int(trig_Mu23_Ele12_fire   );
      trig_Mu8_Ele23_DZ_out = int(trig_Mu8_Ele23_DZ_fire );
      trig_Mu23_Ele12_DZ_out= int(trig_Mu23_Ele12_DZ_fire);
      trig_Mu30_Ele30_out   = int(trig_Mu30_Ele30_fire   );
      trig_Mu33_Ele33_out   = int(trig_Mu33_Ele33_fire   );
      trig_Mu17_TkMu8_out   = int(trig_Mu17_TkMu8_fire   );
      trig_Mu17_Mu8_out     = int(trig_Mu17_Mu8_fire     );
      trig_Mu17_TkMu8_DZ_out= int(trig_Mu17_TkMu8_DZ_fire);
      trig_Mu17_Mu8_DZ_out  = int(trig_Mu17_Mu8_DZ_fire  );
      trig_Mu30_TkMu11_out  = int(trig_Mu30_TkMu11_fire  );
      trig_IsoMu24_out      = int(trig_IsoMu24_fire      ); 
      trig_IsoTkMu24_out    = int(trig_IsoTkMu24_fire    );
      trig_HLT_PFHT300_PFMET110_out           = int(trig_HLT_PFHT300_PFMET110_fire          ); 
      trig_HLT_MET200_out                     = int(trig_HLT_MET200_fire                    ); 
      trig_HLT_PFMET300_out                   = int(trig_HLT_PFMET300_fire                  ); 
      trig_HLT_PFMET120_PFMHT120_IDTight_out  = int(trig_HLT_PFMET120_PFMHT120_IDTight_fire ); 
      trig_HLT_PFMET170_HBHECleaned_out       = int(trig_HLT_PFMET170_HBHECleaned_fire      ); 
      trig_HLT_MET75_IsoTrk50_out             = int(trig_HLT_MET75_IsoTrk50_fire            ); 

      if(trig_DEle33_fire!=-1){ 
      for(unsigned int j=0; j<trig_DEle33_unseed_eta->size(); j++){
      trig_DEle33_unseed_eta_out.push_back(trig_DEle33_unseed_eta->at(j));
      trig_DEle33_unseed_phi_out.push_back(trig_DEle33_unseed_phi->at(j));
                                                                  }
                              }
      if(trig_DEle33_MW_fire!=-1){
      for(unsigned int j=0; j<trig_DEle33_MW_unseed_eta->size(); j++){
      trig_DEle33_MW_unseed_eta_out.push_back(trig_DEle33_MW_unseed_eta->at(j));
      trig_DEle33_MW_unseed_phi_out.push_back(trig_DEle33_MW_unseed_phi->at(j));
                                                                  }
                                 }
      
      if(LHE_weight_nominal!=-1 && LHE_weight_nominal!=0){
      for(unsigned int j=0; j<LHE_id_sys->size(); j++){
      int tmp_id=atoi(LHE_id_sys->at(j).c_str());
//      std::cout<<"s id="<<LHE_id_sys->at(j)<<", int id="<<tmp_id<<std::endl;
      if(tmp_id>=2001 && tmp_id<=2102){
      LHE_sys_weight.push_back(LHE_weight_sys->at(j)/LHE_weight_nominal);
      LHE_sys_id    .push_back(tmp_id);
                                      }
      }
      }
     

      Met_et_out                  = MET_pfMet_et  ;
      Met_phi_out                 = MET_pfMet_phi ;
      MET_T1Txy_et_out            = MET_T1Txy_et           ; 
      MET_T1Txy_phi_out           = MET_T1Txy_phi          ; 
      MET_T1Txy_significance_out  = MET_T1Txy_significance ; 

      MET_T1JetEnDown_Pt_out      =0;
      MET_T1JetEnDown_phi_out     =0;
      MET_T1JetEnUp_Pt_out        =0;
      MET_T1JetEnUp_phi_out       =0;
      MET_T1JetResDown_Pt_out     =0;
      MET_T1JetResDown_phi_out    =0;
      MET_T1JetResUp_Pt_out       =0;
      MET_T1JetResUp_phi_out      =0;
      MET_T1UnclusteredEnUp_Pt_out  =0; 
      MET_T1UnclusteredEnUp_Px_out  =0; 
      MET_T1UnclusteredEnUp_Py_out  =0; 
      MET_T1UnclusteredEnDown_Pt_out=0; 
      MET_T1UnclusteredEnDown_Px_out=0; 
      MET_T1UnclusteredEnDown_Py_out=0; 
      if(tw_study && isData==false){
      MET_T1JetEnDown_Pt_out      = MET_T1SmearJetEnDown_Pt  ; 
      MET_T1JetEnDown_phi_out     = MET_T1SmearJetEnDown_phi ; 
      MET_T1JetEnUp_Pt_out        = MET_T1SmearJetEnUp_Pt    ; 
      MET_T1JetEnUp_phi_out       = MET_T1SmearJetEnUp_phi   ; 
      MET_T1JetResDown_Pt_out     = MET_T1SmearJetResDown_Pt ;
      MET_T1JetResDown_phi_out    = MET_T1SmearJetResDown_phi;
      MET_T1JetResUp_Pt_out       = MET_T1SmearJetResUp_Pt   ;
      MET_T1JetResUp_phi_out      = MET_T1SmearJetResUp_phi  ;
      MET_T1UnclusteredEnUp_Pt_out  = MET_Type1Unc_Pt->at(10); 
      MET_T1UnclusteredEnUp_Px_out  = MET_Type1Unc_Px->at(10); 
      MET_T1UnclusteredEnUp_Py_out  = MET_Type1Unc_Py->at(10); 
      MET_T1UnclusteredEnDown_Pt_out= MET_Type1Unc_Pt->at(11); 
      MET_T1UnclusteredEnDown_Px_out= MET_Type1Unc_Px->at(11); 
      MET_T1UnclusteredEnDown_Py_out= MET_Type1Unc_Py->at(11); 
                                   }
      for(unsigned int j=0;j<electrons.size();j++){
      electrons_pt      .push_back(electrons.at(j)->pt           ); 
      electrons_eta     .push_back(electrons.at(j)->eta          ); 
      electrons_sc_eta  .push_back(electrons.at(j)->sc_eta       ); 
      electrons_phi     .push_back(electrons.at(j)->phi          ); 
      electrons_sc_phi  .push_back(electrons.at(j)->sc_phi       ); 
      electrons_charge  .push_back(electrons.at(j)->charge       ); 
      electrons_tight_ID.push_back(electrons.at(j)->pass_VIDTight); 
      }
      for(unsigned int j=0;j<electrons_74.size();j++){
      electrons_74_pt      .push_back(electrons_74.at(j)->pt           ); 
      electrons_74_eta     .push_back(electrons_74.at(j)->eta          ); 
      electrons_74_sc_eta  .push_back(electrons_74.at(j)->sc_eta       ); 
      electrons_74_phi     .push_back(electrons_74.at(j)->phi          ); 
      electrons_74_sc_phi  .push_back(electrons_74.at(j)->sc_phi       ); 
      electrons_74_charge  .push_back(electrons_74.at(j)->charge       ); 
      electrons_74_tight_ID.push_back(electrons_74.at(j)->pass_VIDTight); 
      }
      for(unsigned int j=0;j<heeps_80.size();j++){
      heeps_80_et          .push_back(heeps_80.at(j)->et               ); 
      heeps_80_eta         .push_back(heeps_80.at(j)->eta              ); 
      heeps_80_sc_eta      .push_back(heeps_80.at(j)->sc_eta           ); 
      heeps_80_phi         .push_back(heeps_80.at(j)->phi              ); 
      heeps_80_sc_phi      .push_back(heeps_80.at(j)->sc_phi           ); 
      heeps_80_charge      .push_back(heeps_80.at(j)->charge           ); 
      heeps_80_isHEEP7     .push_back(heeps_80.at(j)->pass_HEEP7       ); 
      heeps_80_PreSelection.push_back(heeps_80.at(j)->pass_PreSelection); 
      }
      for(unsigned int j=0;j<heeps_74.size();j++){
      heeps_74_et          .push_back(heeps_74.at(j)->et               ); 
      heeps_74_eta         .push_back(heeps_74.at(j)->eta              ); 
      heeps_74_sc_eta      .push_back(heeps_74.at(j)->sc_eta           ); 
      heeps_74_phi         .push_back(heeps_74.at(j)->phi              ); 
      heeps_74_sc_phi      .push_back(heeps_74.at(j)->sc_phi           ); 
      heeps_74_charge      .push_back(heeps_74.at(j)->charge           ); 
      heeps_74_isHEEP7     .push_back(heeps_74.at(j)->pass_HEEP7       ); 
      heeps_74_PreSelection.push_back(heeps_74.at(j)->pass_PreSelection);
      heeps_74_dPhiIn         .push_back(heeps_74.at(j)->ele_dPhiIn         ); 
      heeps_74_Sieie          .push_back(heeps_74.at(j)->ele_Sieie          ); 
      heeps_74_missingHits    .push_back(heeps_74.at(j)->ele_missingHits    ); 
      heeps_74_dxyFirstPV     .push_back(heeps_74.at(j)->ele_dxyFirstPV     ); 
      heeps_74_HOverE         .push_back(heeps_74.at(j)->ele_HOverE         ); 
      heeps_74_E1x5OverE5x5   .push_back(heeps_74.at(j)->ele_E1x5OverE5x5   ); 
      heeps_74_E2x5OverE5x5   .push_back(heeps_74.at(j)->ele_E2x5OverE5x5   ); 
      heeps_74_isolEMHadDepth1.push_back(heeps_74.at(j)->ele_isolEMHadDepth1); 
      heeps_74_IsolPtTrks     .push_back(heeps_74.at(j)->ele_IsolPtTrks     ); 
      heeps_74_EcalDriven     .push_back(heeps_74.at(j)->ele_EcalDriven     ); 
      heeps_74_dEtaIn         .push_back(heeps_74.at(j)->ele_dEtaIn         ); 
      heeps_74_match          .push_back(heeps_74.at(j)->truthmatched       ); 
      }
      for(unsigned int j=0;j<heeps_74_Barrel_EScale_up.size();j++){
      heeps_74_B_EnScaleUp_et          .push_back(heeps_74_Barrel_EScale_up.at(j)->et               ); 
      heeps_74_B_EnScaleUp_eta         .push_back(heeps_74_Barrel_EScale_up.at(j)->eta              ); 
      heeps_74_B_EnScaleUp_sc_eta      .push_back(heeps_74_Barrel_EScale_up.at(j)->sc_eta           ); 
      heeps_74_B_EnScaleUp_phi         .push_back(heeps_74_Barrel_EScale_up.at(j)->phi              ); 
      heeps_74_B_EnScaleUp_sc_phi      .push_back(heeps_74_Barrel_EScale_up.at(j)->sc_phi           ); 
      heeps_74_B_EnScaleUp_charge      .push_back(heeps_74_Barrel_EScale_up.at(j)->charge           ); 
      heeps_74_B_EnScaleUp_isHEEP7     .push_back(heeps_74_Barrel_EScale_up.at(j)->pass_HEEP7       ); 
      heeps_74_B_EnScaleUp_PreSelection.push_back(heeps_74_Barrel_EScale_up.at(j)->pass_PreSelection); 
      }
      for(unsigned int j=0;j<heeps_74_Barrel_EScale_down.size();j++){
      heeps_74_B_EnScaleDown_et          .push_back(heeps_74_Barrel_EScale_down.at(j)->et               ); 
      heeps_74_B_EnScaleDown_eta         .push_back(heeps_74_Barrel_EScale_down.at(j)->eta              ); 
      heeps_74_B_EnScaleDown_sc_eta      .push_back(heeps_74_Barrel_EScale_down.at(j)->sc_eta           ); 
      heeps_74_B_EnScaleDown_phi         .push_back(heeps_74_Barrel_EScale_down.at(j)->phi              ); 
      heeps_74_B_EnScaleDown_sc_phi      .push_back(heeps_74_Barrel_EScale_down.at(j)->sc_phi           ); 
      heeps_74_B_EnScaleDown_charge      .push_back(heeps_74_Barrel_EScale_down.at(j)->charge           ); 
      heeps_74_B_EnScaleDown_isHEEP7     .push_back(heeps_74_Barrel_EScale_down.at(j)->pass_HEEP7       ); 
      heeps_74_B_EnScaleDown_PreSelection.push_back(heeps_74_Barrel_EScale_down.at(j)->pass_PreSelection); 
      }
      for(unsigned int j=0;j<heeps_74_Endcap_EScale_up.size();j++){
      heeps_74_E_EnScaleUp_et          .push_back(heeps_74_Endcap_EScale_up.at(j)->et               ); 
      heeps_74_E_EnScaleUp_eta         .push_back(heeps_74_Endcap_EScale_up.at(j)->eta              ); 
      heeps_74_E_EnScaleUp_sc_eta      .push_back(heeps_74_Endcap_EScale_up.at(j)->sc_eta           ); 
      heeps_74_E_EnScaleUp_phi         .push_back(heeps_74_Endcap_EScale_up.at(j)->phi              ); 
      heeps_74_E_EnScaleUp_sc_phi      .push_back(heeps_74_Endcap_EScale_up.at(j)->sc_phi           ); 
      heeps_74_E_EnScaleUp_charge      .push_back(heeps_74_Endcap_EScale_up.at(j)->charge           ); 
      heeps_74_E_EnScaleUp_isHEEP7     .push_back(heeps_74_Endcap_EScale_up.at(j)->pass_HEEP7       ); 
      heeps_74_E_EnScaleUp_PreSelection.push_back(heeps_74_Endcap_EScale_up.at(j)->pass_PreSelection); 
      }
      for(unsigned int j=0;j<heeps_74_Endcap_EScale_down.size();j++){
      heeps_74_E_EnScaleDown_et          .push_back(heeps_74_Endcap_EScale_down.at(j)->et               ); 
      heeps_74_E_EnScaleDown_eta         .push_back(heeps_74_Endcap_EScale_down.at(j)->eta              ); 
      heeps_74_E_EnScaleDown_sc_eta      .push_back(heeps_74_Endcap_EScale_down.at(j)->sc_eta           ); 
      heeps_74_E_EnScaleDown_phi         .push_back(heeps_74_Endcap_EScale_down.at(j)->phi              ); 
      heeps_74_E_EnScaleDown_sc_phi      .push_back(heeps_74_Endcap_EScale_down.at(j)->sc_phi           ); 
      heeps_74_E_EnScaleDown_charge      .push_back(heeps_74_Endcap_EScale_down.at(j)->charge           ); 
      heeps_74_E_EnScaleDown_isHEEP7     .push_back(heeps_74_Endcap_EScale_down.at(j)->pass_HEEP7       ); 
      heeps_74_E_EnScaleDown_PreSelection.push_back(heeps_74_Endcap_EScale_down.at(j)->pass_PreSelection); 
      }
      for(unsigned int j=0;j<muons.size();j++){
      muons_pt          .push_back(muons.at(j)->pt     ); 
      muons_pt_rochest  .push_back(muons.at(j)->pt*muons.at(j)->rochester_sf); 
      muons_eta         .push_back(muons.at(j)->eta    ); 
      muons_phi         .push_back(muons.at(j)->phi    ); 
      muons_charge      .push_back(muons.at(j)->charge ); 
      muons_tight_ID    .push_back(muons.at(j)->isTight); 
      muons_pfIso       .push_back(muons.at(j)->passIso); 
      muons_match       .push_back(muons.at(j)->truthmatched); 
      muons_trackerLayer.push_back(muons.at(j)->trackerLayersWithMeasurement); 
      muons_rochester_sf.push_back(muons.at(j)->rochester_sf); 
      }
      for(unsigned int j=0;j<jets.size();j++){
      jets_pt      .push_back(jets.at(j)->pt           ); 
      jets_eta     .push_back(jets.at(j)->eta          ); 
      jets_phi     .push_back(jets.at(j)->phi          ); 
      jets_mass    .push_back(jets.at(j)->mass         ); 
      jets_energy  .push_back(jets.at(j)->energy       );
      jets_CSV     .push_back(jets.at(j)->CSV          );
      jets_loose_ID.push_back(jets.at(j)->pass_loose_ID); 
      jets_BtagSF_medium           .push_back(jets.at(j)->BtagSF_medium           );
      jets_BtagSFbcUp_medium       .push_back(jets.at(j)->BtagSFbcUp_medium       );
      jets_BtagSFbcDown_medium     .push_back(jets.at(j)->BtagSFbcDown_medium     );
      jets_BtagSFudsgUp_medium     .push_back(jets.at(j)->BtagSFudsgUp_medium     );
      jets_BtagSFudsgDown_medium   .push_back(jets.at(j)->BtagSFudsgDown_medium   );
      jets_SmearedJetResUp_pt      .push_back(jets.at(j)->SmearedJetResUp_pt      );
      jets_SmearedJetResUp_energy  .push_back(jets.at(j)->SmearedJetResUp_energy  );
      jets_SmearedJetResDown_pt    .push_back(jets.at(j)->SmearedJetResDown_pt    );
      jets_SmearedJetResDown_energy.push_back(jets.at(j)->SmearedJetResDown_energy);
      jets_EnUp_pt                 .push_back(jets.at(j)->EnUp_pt                 );
      jets_EnUp_energy             .push_back(jets.at(j)->EnUp_energy             );
      jets_EnDown_pt               .push_back(jets.at(j)->EnDown_pt               );
      jets_EnDown_energy           .push_back(jets.at(j)->EnDown_energy           );
      }
      tree_out.Fill() ;
      }
//#############################################
      for (std::vector<electron_candidate*>::iterator it = electrons.begin(); it != electrons.end(); it ++){
      if (NULL != *it){
        delete *it; 
        *it = NULL;
                      }
      }
      electrons.clear() ;
      electrons.swap(electrons);
   
      for (std::vector<electron_candidate*>::iterator it = electrons_74.begin(); it != electrons_74.end(); it ++){
      if (NULL != *it){
        delete *it; 
        *it = NULL;
                      }
      }
      electrons_74.clear() ;
      electrons_74.swap(electrons_74);

      for (std::vector<electron_candidate*>::iterator it = heeps_80.begin(); it != heeps_80.end(); it ++){
      if (NULL != *it){
        delete *it; 
        *it = NULL;
                      }
      }
      heeps_80.clear() ;
      heeps_80.swap(heeps_80);

      for (std::vector<electron_candidate*>::iterator it = heeps_74.begin(); it != heeps_74.end(); it ++){
      if (NULL != *it){
        delete *it; 
        *it = NULL;
                      }
      }
      heeps_74.clear() ;
      heeps_74.swap(heeps_74);

      for (std::vector<electron_candidate*>::iterator it = heeps_74_Barrel_EScale_up.begin(); it != heeps_74_Barrel_EScale_up.end(); it ++){
      if (NULL != *it){
        delete *it; 
        *it = NULL;
                      }
      }
      heeps_74_Barrel_EScale_up.clear() ;
      heeps_74_Barrel_EScale_up.swap(heeps_74_Barrel_EScale_up);

      for (std::vector<electron_candidate*>::iterator it = heeps_74_Barrel_EScale_down.begin(); it != heeps_74_Barrel_EScale_down.end(); it ++){
      if (NULL != *it){
        delete *it; 
        *it = NULL;
                      }
      }
      heeps_74_Barrel_EScale_down.clear() ;
      heeps_74_Barrel_EScale_down.swap(heeps_74_Barrel_EScale_down);

      for (std::vector<electron_candidate*>::iterator it = heeps_74_Endcap_EScale_up.begin(); it != heeps_74_Endcap_EScale_up.end(); it ++){
      if (NULL != *it){
        delete *it; 
        *it = NULL;
                      }
      }
      heeps_74_Endcap_EScale_up.clear() ;
      heeps_74_Endcap_EScale_up.swap(heeps_74_Endcap_EScale_up);

      for (std::vector<electron_candidate*>::iterator it = heeps_74_Endcap_EScale_down.begin(); it != heeps_74_Endcap_EScale_down.end(); it ++){
      if (NULL != *it){
        delete *it; 
        *it = NULL;
                      }
      }
      heeps_74_Endcap_EScale_down.clear() ;
      heeps_74_Endcap_EScale_down.swap(heeps_74_Endcap_EScale_down);

      for (std::vector<muon_candidate*>::iterator it = muons.begin(); it != muons.end(); it ++){
      if (NULL != *it){
        delete *it; 
        *it = NULL;
                      }
      }
      muons.clear() ;
      muons.swap(muons);

      for (std::vector<jet_candidate*>::iterator it = jets.begin(); it != jets.end(); it ++){
      if (NULL != *it){
        delete *it; 
        *it = NULL;
                      }
      }
      jets.clear() ;
      jets.swap(jets);
   }
         
   std::cout << std::endl ;
   std::cout << "Out: " << tree_out.GetEntries() << std::endl ;
   file_out.cd();
   tree_out.Write() ;
   file_out.Close() ;
   
   time_t time_end = time(0) ;
   char* time_end_text = ctime(&time_end) ;
   std::cout << time_end_text << std::endl ;
}
