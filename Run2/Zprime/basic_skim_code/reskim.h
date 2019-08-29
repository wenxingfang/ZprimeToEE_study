//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Sun Dec  6 18:36:33 2015 by ROOT version 6.02/05
// from TTree IIHEAnalysis/IIHEAnalysis
// found on file: ../../samples/RunIISpring15DR74/RunIISpring15DR74_ZToEE_50_120_25ns/outfile_1.root
//////////////////////////////////////////////////////////

#ifndef reskim_h
#define reskim_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

// Header file for the classes stored in the TTree if any.
#include "vector"

#include <iostream>

class reskim {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

// Fixed size dimensions of array or collections stored in the TTree if any.

   // Declaration of leaf types
   ULong_t          ev_event;
   ULong_t          ev_run;
   ULong_t          ev_luminosityBlock;
   UInt_t          trig_Flag_HBHENoiseFilter_accept                     =0; 
   UInt_t          trig_Flag_HBHENoiseIsoFilter_accept                  =0; 
   UInt_t          trig_Flag_CSCTightHaloFilter_accept                  =0; 
   UInt_t          trig_Flag_CSCTightHaloTrkMuUnvetoFilter_accept       =0; 
   UInt_t          trig_Flag_CSCTightHalo2015Filter_accept              =0; 
   UInt_t          trig_Flag_globalTightHalo2016Filter_accept           =0; 
   UInt_t          trig_Flag_globalSuperTightHalo2016Filter_accept      =0; 
   UInt_t          trig_Flag_goodVertices_accept                        =0; 
   UInt_t          trig_Flag_HcalStripHaloFilter_accept                 =0; 
   UInt_t          trig_Flag_hcalLaserEventFilter_accept                =0; 
   UInt_t          trig_Flag_EcalDeadCellTriggerPrimitiveFilter_accept  =0; 
   UInt_t          trig_Flag_EcalDeadCellBoundaryEnergyFilter_accept    =0; 
   UInt_t          trig_Flag_ecalLaserCorrFilter_accept                 =0; 
   UInt_t          trig_Flag_chargedHadronTrackResolutionFilter_accept  =0; 
   UInt_t          trig_Flag_muonBadTrackFilter_accept                  =0; 
   Bool_t          trig_Flag_BadPFMuonFilter_accept                     =false; 
   Bool_t          trig_Flag_BadChargedCandidateFilter_accept           =false; 
   UInt_t          trig_Flag_eeBadScFilter_accept                       =0; 
   UInt_t          trig_Flag_trkPOG_manystripclus53X_accept             =0; 
   UInt_t          trig_Flag_trkPOG_toomanystripclus53X_accept          =0; 
   UInt_t          trig_Flag_trkPOG_logErrorTooManyClusters_accept      =0; 
   UInt_t          trig_Flag_METFilters_accept                          =0;
   UInt_t          ev_time;
   UInt_t          ev_time_unixTime;
   UInt_t          ev_time_microsecondOffset;
   Float_t         ev_fixedGridRhoAll;
   Float_t         ev_fixedGridRhoFastjetAll;
   Float_t         ev_rho_kt6PFJetsForIsolation;
   UInt_t          mc_n;
   Float_t         mc_pdfvariables_weight;
   Float_t         mc_w;
   vector<int>     *LHE_pdgid ; 
   vector<int>     *LHE_status;
   vector<float>   *LHE_Pt    ;
   vector<float>   *LHE_Eta   ;
   vector<float>   *LHE_Phi   ;
   vector<float>   *LHE_E    ;
   vector<int>     *mc_index;
   vector<int>     *mc_pdgId;
   vector<int>     *mc_charge;
   vector<int>     *mc_status;
   vector<float>   *mc_mass;
   vector<float>   *mc_px;
   vector<float>   *mc_py;
   vector<float>   *mc_pz;
   vector<float>   *mc_pt;
   vector<float>   *mc_eta;
   vector<float>   *mc_phi;
   vector<float>   *mc_energy;
   vector<unsigned int> *mc_numberOfDaughters;
   vector<unsigned int> *mc_numberOfMothers;
   vector<vector<int> > *mc_mother_index;
   vector<vector<int> > *mc_mother_pdgId;
   vector<vector<float> > *mc_mother_px;
   vector<vector<float> > *mc_mother_py;
   vector<vector<float> > *mc_mother_pz;
   vector<vector<float> > *mc_mother_pt;
   vector<vector<float> > *mc_mother_eta;
   vector<vector<float> > *mc_mother_phi;
   vector<vector<float> > *mc_mother_energy;
   vector<vector<float> > *mc_mother_mass;
   Int_t           mc_trueNumInteractions;
   Int_t           mc_PU_NumInteractions;
   UInt_t          pv_n;
   vector<float>   *pv_x;
   vector<float>   *pv_y;
   vector<float>   *pv_z;
   vector<int>     *pv_isValid;
   vector<float>   *pv_normalizedChi2;
   vector<int>     *pv_ndof;
   vector<int>     *pv_nTracks;
   vector<int>     *pv_totTrackSize;
   UInt_t          jet_n;
   vector<float>   *jet_px                          ;
   vector<float>   *jet_py                          ;
   vector<float>   *jet_pz                          ; 
   vector<float>   *jet_pt                          ; 
   vector<float>   *jet_eta                         ; 
   vector<float>   *jet_phi                         ; 
   vector<float>   *jet_energy                      ; 
   vector<float>   *jet_mass                        ; 
   vector<float>   *jet_neutralHadronEnergyFraction ; 
   vector<float>   *jet_neutralEmEnergyFraction     ; 
   vector<float>   *jet_chargedHadronEnergyFraction ; 
   vector<float>   *jet_chargedEmEnergyFraction     ; 
   vector<float>   *jet_muonEnergyFraction          ; 
   vector<int>     *jet_chargedMultiplicity         ; 
   vector<int>     *jet_neutralMultiplicity         ; 
   vector<float>   *jet_CSVv2                       ;  
   vector<bool>    *jet_isJetIDLoose                ;  

   UInt_t          gsf_n;
   vector<int>     *gsf_classification;
   vector<float>   *gsf_energy;
   vector<float>   *gsf_p;
   vector<float>   *gsf_pt;
   vector<float>   *gsf_full5x5_e5x5         ; 
   vector<float>   *gsf_full5x5_e1x5         ; 
   vector<float>   *gsf_full5x5_e2x5Max      ; 
   vector<float>   *gsf_full5x5_sigmaIetaIeta;
   vector<float>   *gsf_full5x5_hcalOverEcal ;
   vector<float>   *gsf_scE1x5;
   vector<float>   *gsf_scE5x5;
   vector<float>   *gsf_scE2x5Max;
   vector<float>   *gsf_eta;
   vector<float>   *gsf_phi;
   vector<float>   *gsf_theta;
   vector<float>   *gsf_px;
   vector<float>   *gsf_py;
   vector<float>   *gsf_pz;
   vector<float>   *gsf_superClusterEta;
   vector<float>   *gsf_superClusterEnergy;
   vector<float>   *gsf_caloEnergy;
   vector<float>   *gsf_deltaEtaSuperClusterTrackAtVtx;
   vector<float>   *gsf_deltaPhiSuperClusterTrackAtVtx;
   vector<float>   *gsf_hadronicOverEm;
   vector<float>   *gsf_hcalDepth1OverEcal;
   vector<float>   *gsf_hcalDepth2OverEcal;
   vector<float>   *gsf_dr03TkSumPt;
   vector<float>   *gsf_dr03TkSumPtHEEP7;
   vector<float>   *gsf_dr03EcalRecHitSumEt;
   vector<float>   *gsf_dr03HcalDepth1TowerSumEt;
   vector<float>   *gsf_dr03HcalDepth2TowerSumEt;
   vector<int>     *gsf_charge;
   vector<float>   *gsf_sigmaIetaIeta;
   vector<int>     *gsf_ecaldrivenSeed;
   vector<int>    *gsf_VIDHEEP7;
   vector<int>    *gsf_VIDLoose;
   vector<int>    *gsf_VIDTight;
   vector<int>     *gsf_trackerdrivenSeed;
   vector<int>     *gsf_isEB;
   vector<int>     *gsf_isEE;
   vector<float>   *gsf_deltaEtaSeedClusterTrackAtVtx;
   vector<float>   *gsf_deltaEtaSeedClusterTrackAtCalo;
   vector<float>   *gsf_deltaPhiSeedClusterTrackAtCalo;
   vector<float>   *gsf_ecalEnergy;
   vector<float>   *gsf_eSuperClusterOverP;
   vector<float>   *gsf_dxy;
   vector<float>   *gsf_dxy_beamSpot;
   vector<float>   *gsf_dxy_firstPVtx;
   vector<float>   *gsf_dxyError;
   vector<float>   *gsf_dz;
   vector<float>   *gsf_dz_beamSpot;
   vector<float>   *gsf_dz_firstPVtx;
   vector<float>   *gsf_dzError;
   vector<float>   *gsf_vz;
   vector<int>     *gsf_numberOfValidHits;
   vector<int>     *gsf_nLostInnerHits;
   vector<int>     *gsf_nLostOuterHits;
   vector<int>     *gsf_convFlags;
   vector<float>   *gsf_convDist;
   vector<float>   *gsf_convDcot;
   vector<float>   *gsf_convRadius;
   vector<float>   *gsf_fBrem;
   vector<float>   *gsf_e1x5;
   vector<float>   *gsf_e2x5Max;
   vector<float>   *gsf_e5x5;
   vector<float>   *gsf_r9;
////////////////////////////////////
   vector<int>   *gsf_sc_seed_ieta;
   vector<int>   *gsf_sc_seed_iphi;
   vector<int>   *gsf_sc_seed_rawId;          
   vector<float> *gsf_sc_energy;              
   vector<float> *gsf_sc_rawEnergy;           
   vector<float> *gsf_sc_preshowerEnergy;     
   vector<float> *gsf_sc_lazyTools_e2x5Right; 
   vector<float> *gsf_sc_lazyTools_e2x5Left;  
   vector<float> *gsf_sc_lazyTools_e2x5Top;   
   vector<float> *gsf_sc_lazyTools_e2x5Bottom;
   vector<float> *gsf_sc_eta;                 
   vector<float> *gsf_sc_phi;                 
   vector<float> *gsf_sc_theta;                 
   vector<float> *gsf_sc_etaWidth;            
   vector<float> *gsf_sc_phiWidth;            
   vector<float> *gsf_sc_lazyTools_e2x2;      
   vector<float> *gsf_sc_lazyTools_e3x3;      
   vector<float> *gsf_sc_lazyTools_e4x4;      
   vector<float> *gsf_sc_lazyTools_e5x5;      
   vector<float> *gsf_sc_lazyTools_e1x3;      
   vector<float> *gsf_sc_lazyTools_e3x1;      
   vector<float> *gsf_sc_lazyTools_e1x5;      
   vector<float> *gsf_sc_lazyTools_e5x1;      
   vector<float> *gsf_sc_lazyTools_eMax;      
   vector<float> *gsf_sc_lazyTools_e2nd;      
   vector<float> *gsf_sc_lazyTools_eLeft;     
   vector<float> *gsf_sc_lazyTools_eRight;    
   vector<float> *gsf_sc_lazyTools_eTop;      
   vector<float> *gsf_sc_lazyTools_eBottom;   

   vector<int>     *EBHits_kSaturated;
   vector<int>     *EEHits_kSaturated;
   vector<int>     *EBHits_rawId;
   vector<int>     *EEHits_rawId;
//////////// For muons /////////////////////
   UInt_t         mu_ibt_n       ;
   vector<float> *mu_ibt_p       ;
   vector<float> *mu_ibt_pt      ;
   vector<float> *mu_ibt_eta     ;
   vector<float> *mu_ibt_phi     ;
   vector<int>   *mu_ibt_charge  ;
   vector<float> *mu_gt_p       ;
   vector<float> *mu_gt_pt      ;
   vector<float> *mu_gt_eta     ;
   vector<float> *mu_gt_phi     ;
   vector<int>   *mu_gt_charge  ;
   vector<bool>  *mu_isGlobalMuon;
   vector<bool>  *mu_isTightMuon ;
   vector<float> *mu_pfIsoDbCorrected04 ;
   vector<int>   *mu_trackerLayersWithMeasurement  ;

   vector<float> *mu_rochester_sf          ;
   vector<float> *jet_BtagSF_medium        ;
   vector<float> *jet_BtagSFbcUp_medium    ;
   vector<float> *jet_BtagSFbcDown_medium  ;
   vector<float> *jet_BtagSFudsgUp_medium  ;
   vector<float> *jet_BtagSFudsgDown_medium;
   vector<float> *jet_SmearedJetResUp_pt      ;
   vector<float> *jet_SmearedJetResUp_energy  ;
   vector<float> *jet_SmearedJetResDown_pt    ;
   vector<float> *jet_SmearedJetResDown_energy;
   vector<float> *jet_EnUp_pt                 ;
   vector<float> *jet_EnUp_energy             ;
   vector<float> *jet_EnDown_pt               ;
   vector<float> *jet_EnDown_energy           ;

/////////////For MET ////////////////////////
   vector<float> *MET_Type1Unc_Pt;
   vector<float> *MET_Type1Unc_Px; 
   vector<float> *MET_Type1Unc_Py;

   Float_t         MET_pfMet_et;
   Float_t         MET_pfMet_phi;
   Float_t         MET_T1Txy_et;
   Float_t         MET_T1Txy_phi;
   Float_t         MET_T1Txy_significance;
   Float_t         MET_T1SmearJetEnDown_Pt     ; 
   Float_t         MET_T1SmearJetEnDown_phi    ; 
   Float_t         MET_T1SmearJetEnUp_Pt       ; 
   Float_t         MET_T1SmearJetEnUp_phi      ; 
   Float_t         MET_T1SmearJetResDown_Pt    ; 
   Float_t         MET_T1SmearJetResDown_phi   ; 
   Float_t         MET_T1SmearJetResUp_Pt      ; 
   Float_t         MET_T1SmearJetResUp_phi     ; 

   Float_t         LHE_weight_nominal ;
   vector<float> *LHE_weight_sys; 
   vector<string> *LHE_id_sys    ; 
   Float_t         ev_prefiringweight;
   Float_t         ev_prefiringweightup;
   Float_t         ev_prefiringweightdown;

////////////////////////////////////////////
   Int_t trig_Ele23_Ele12_fire  ;
   Int_t trig_DEle33_fire       ;
   Int_t trig_DEle33_MW_fire    ;
   Int_t trig_DEle25_MW_fire    ;
   Int_t trig_DEle33_CaloId_fire;
   Int_t trig_Ele27_fire        ;
   Int_t trig_Mu8_Ele23_fire    ; 
   Int_t trig_Mu23_Ele12_fire   ;
   Int_t trig_Mu8_Ele23_DZ_fire ; 
   Int_t trig_Mu23_Ele12_DZ_fire;
   Int_t trig_Mu30_Ele30_fire   ; 
   Int_t trig_Mu33_Ele33_fire   ; 
   Int_t trig_Mu17_TkMu8_fire   ;
   Int_t trig_Mu17_Mu8_fire     ;
   Int_t trig_Mu17_TkMu8_DZ_fire;
   Int_t trig_Mu17_Mu8_DZ_fire  ;
   Int_t trig_Mu30_TkMu11_fire  ;
   Int_t trig_IsoMu24_fire      ; 
   Int_t trig_IsoTkMu24_fire    ; 
   Int_t trig_HLT_PFHT300_PFMET110_fire          ; 
   Int_t trig_HLT_MET200_fire                    ; 
   Int_t trig_HLT_PFMET300_fire                  ; 
   Int_t trig_HLT_PFMET120_PFMHT120_IDTight_fire ; 
   Int_t trig_HLT_PFMET170_HBHECleaned_fire      ; 
   Int_t trig_HLT_MET75_IsoTrk50_fire            ; 




   vector<float> *trig_DEle33_seed_eta     ;
   vector<float> *trig_DEle33_seed_phi     ;
   vector<float> *trig_DEle33_unseed_eta   ;
   vector<float> *trig_DEle33_unseed_phi   ;
   vector<float> *trig_DEle33_MW_seed_eta  ;
   vector<float> *trig_DEle33_MW_seed_phi  ;
   vector<float> *trig_DEle33_MW_unseed_eta;
   vector<float> *trig_DEle33_MW_unseed_phi;
   vector<float> *trig_DEle33_MW_L1_eta;
   vector<float> *trig_DEle33_MW_L1_phi;
   vector<float> *trig_DEle33_MW_L1_et ;
   vector<bool>  *L1_pass_final;
   vector<float> *trig_DEle25_MW_seed_eta  ;
   vector<float> *trig_DEle25_MW_seed_phi  ;
   vector<float> *trig_DEle25_MW_unseed_eta;
   vector<float> *trig_DEle25_MW_unseed_phi;
   vector<float> *trig_DEle25_MW_L1_eta    ;
   vector<float> *trig_DEle25_MW_L1_phi    ;
   vector<float> *trig_DEle25_MW_L1_et     ;


   Float_t mc_w_sign ;

   // List of branches
   TBranch        *b_ev_event;   //!
   TBranch        *b_ev_run;   //!
   TBranch        *b_ev_luminosityBlock;   //!
   TBranch        *b_trig_Flag_HBHENoiseFilter_accept                   ; 
   TBranch        *b_trig_Flag_HBHENoiseIsoFilter_accept                ; 
   TBranch        *b_trig_Flag_CSCTightHaloFilter_accept                ; 
   TBranch        *b_trig_Flag_CSCTightHaloTrkMuUnvetoFilter_accept     ; 
   TBranch        *b_trig_Flag_CSCTightHalo2015Filter_accept            ; 
   TBranch        *b_trig_Flag_globalTightHalo2016Filter_accept         ; 
   TBranch        *b_trig_Flag_globalSuperTightHalo2016Filter_accept    ; 
   TBranch        *b_trig_Flag_goodVertices_accept                      ; 
   TBranch        *b_trig_Flag_HcalStripHaloFilter_accept               ; 
   TBranch        *b_trig_Flag_hcalLaserEventFilter_accept              ; 
   TBranch        *b_trig_Flag_EcalDeadCellTriggerPrimitiveFilter_accept; 
   TBranch        *b_trig_Flag_EcalDeadCellBoundaryEnergyFilter_accept  ; 
   TBranch        *b_trig_Flag_ecalLaserCorrFilter_accept               ; 
   TBranch        *b_trig_Flag_chargedHadronTrackResolutionFilter_accept; 
   TBranch        *b_trig_Flag_muonBadTrackFilter_accept                ; 
   TBranch        *b_trig_Flag_BadPFMuonFilter_accept                   ; 
   TBranch        *b_trig_Flag_BadChargedCandidateFilter_accept         ; 
   TBranch        *b_trig_Flag_eeBadScFilter_accept                     ; 
   TBranch        *b_trig_Flag_trkPOG_manystripclus53X_accept           ; 
   TBranch        *b_trig_Flag_trkPOG_toomanystripclus53X_accept        ; 
   TBranch        *b_trig_Flag_trkPOG_logErrorTooManyClusters_accept    ; 
   TBranch        *b_trig_Flag_METFilters_accept;   //!
   TBranch        *b_ev_particleFlowEGammaGSFixed;   //!
   TBranch        *b_ev_time;   //!
   TBranch        *b_ev_time_unixTime;   //!
   TBranch        *b_ev_time_microsecondOffset;   //!
   TBranch        *b_ev_fixedGridRhoAll;   //!
   TBranch        *b_ev_fixedGridRhoFastjetAll;   //!
   TBranch        *b_ev_rho_kt6PFJetsForIsolation;   //!
   TBranch        *b_LHE_pdgid ;
   TBranch        *b_LHE_status;
   TBranch        *b_LHE_Pt    ;
   TBranch        *b_LHE_Eta   ;
   TBranch        *b_LHE_Phi   ;
   TBranch        *b_LHE_E     ;
   TBranch        *b_mc_n;   //!
   TBranch        *b_mc_pdfvariables_weight;   //!
   TBranch        *b_mc_w;   //!
   TBranch        *b_mc_index;   //!
   TBranch        *b_mc_pdgId;   //!
   TBranch        *b_mc_charge;   //!
   TBranch        *b_mc_status;   //!
   TBranch        *b_mc_mass;   //!
   TBranch        *b_mc_px;   //!
   TBranch        *b_mc_py;   //!
   TBranch        *b_mc_pz;   //!
   TBranch        *b_mc_pt;   //!
   TBranch        *b_mc_eta;   //!
   TBranch        *b_mc_phi;   //!
   TBranch        *b_mc_energy;   //!
   TBranch        *b_mc_numberOfDaughters;   //!
   TBranch        *b_mc_numberOfMothers;   //!
   TBranch        *b_mc_mother_index;   //!
   TBranch        *b_mc_mother_pdgId;   //!
   TBranch        *b_mc_mother_px;   //!
   TBranch        *b_mc_mother_py;   //!
   TBranch        *b_mc_mother_pz;   //!
   TBranch        *b_mc_mother_pt;   //!
   TBranch        *b_mc_mother_eta;   //!
   TBranch        *b_mc_mother_phi;   //!
   TBranch        *b_mc_mother_energy;   //!
   TBranch        *b_mc_mother_mass;   //!
   TBranch        *b_mc_trueNumInteractions;   //!
   TBranch        *b_mc_PU_NumInteractions;   //!
   TBranch        *b_pv_n;   //!
   TBranch        *b_pv_x;   //!
   TBranch        *b_pv_y;   //!
   TBranch        *b_pv_z;   //!
   TBranch        *b_pv_isValid;   //!
   TBranch        *b_pv_normalizedChi2;   //!
   TBranch        *b_pv_ndof;   //!
   TBranch        *b_pv_nTracks;   //!
   TBranch        *b_pv_totTrackSize;   //!
   TBranch        *b_jet_n;   //!
   TBranch        *b_jet_px                         ;
   TBranch        *b_jet_py                         ;
   TBranch        *b_jet_pz                         ;
   TBranch        *b_jet_pt                         ;
   TBranch        *b_jet_eta                        ;
   TBranch        *b_jet_phi                        ;
   TBranch        *b_jet_energy                     ;
   TBranch        *b_jet_mass                       ;
   TBranch        *b_jet_neutralHadronEnergyFraction;
   TBranch        *b_jet_neutralEmEnergyFraction    ;
   TBranch        *b_jet_chargedHadronEnergyFraction;
   TBranch        *b_jet_chargedEmEnergyFraction    ;
   TBranch        *b_jet_muonEnergyFraction         ;
   TBranch        *b_jet_chargedMultiplicity        ;
   TBranch        *b_jet_neutralMultiplicity        ;
   TBranch        *b_jet_CSVv2                      ;
   TBranch        *b_jet_isJetIDLoose               ;

   TBranch        *b_gsf_n;   //!
   TBranch        *b_gsf_classification;   //!
   TBranch        *b_gsf_energy;   //!
   TBranch        *b_gsf_p;   //!
   TBranch        *b_gsf_pt;   //!
   TBranch        *b_gsf_full5x5_e5x5         ; 
   TBranch        *b_gsf_full5x5_e1x5         ; 
   TBranch        *b_gsf_full5x5_e2x5Max      ; 
   TBranch        *b_gsf_full5x5_sigmaIetaIeta; 
   TBranch        *b_gsf_full5x5_hcalOverEcal ; 
   TBranch        *b_gsf_scE1x5;   //!
   TBranch        *b_gsf_scE5x5;   //!
   TBranch        *b_gsf_scE2x5Max;   //!
   TBranch        *b_gsf_eta;   //!
   TBranch        *b_gsf_phi;   //!
   TBranch        *b_gsf_theta;   //!
   TBranch        *b_gsf_px;   //!
   TBranch        *b_gsf_py;   //!
   TBranch        *b_gsf_pz;   //!
   TBranch        *b_gsf_superClusterEta;   //!
   TBranch        *b_gsf_superClusterEnergy;   //!
   TBranch        *b_gsf_caloEnergy;   //!
   TBranch        *b_gsf_deltaEtaSuperClusterTrackAtVtx;   //!
   TBranch        *b_gsf_deltaPhiSuperClusterTrackAtVtx;   //!
   TBranch        *b_gsf_hadronicOverEm;   //!
   TBranch        *b_gsf_hcalDepth1OverEcal;   //!
   TBranch        *b_gsf_hcalDepth2OverEcal;   //!
   TBranch        *b_gsf_dr03TkSumPt;   //!
   TBranch        *b_gsf_dr03TkSumPtHEEP7;   //!
   TBranch        *b_gsf_dr03TkSumPtCorrected;   //!
   TBranch        *b_gsf_dr03EcalRecHitSumEt;   //!
   TBranch        *b_gsf_dr03HcalDepth1TowerSumEt;   //!
   TBranch        *b_gsf_dr03HcalDepth2TowerSumEt;   //!
   TBranch        *b_gsf_charge;   //!
   TBranch        *b_gsf_sigmaIetaIeta;   //!
   TBranch        *b_gsf_ecaldrivenSeed;   //!
   TBranch        *b_gsf_VIDHEEP7;   //!
   TBranch        *b_gsf_VIDLoose;   //!
   TBranch        *b_gsf_VIDTight;   //!
   TBranch        *b_gsf_trackerdrivenSeed;   //!
   TBranch        *b_gsf_isEB;   //!
   TBranch        *b_gsf_isEE;   //!
   TBranch        *b_gsf_deltaEtaSeedClusterTrackAtVtx;   //!
   TBranch        *b_gsf_deltaEtaSeedClusterTrackAtCalo;   //!
   TBranch        *b_gsf_deltaPhiSeedClusterTrackAtCalo;   //!
   TBranch        *b_gsf_ecalEnergy;   //!
   TBranch        *b_gsf_eSuperClusterOverP;   //!
   TBranch        *b_gsf_dxy;   //!
   TBranch        *b_gsf_dxy_beamSpot;   //!
   TBranch        *b_gsf_dxy_firstPVtx;   //!
   TBranch        *b_gsf_dxyError;   //!
   TBranch        *b_gsf_dz;   //!
   TBranch        *b_gsf_dz_beamSpot;   //!
   TBranch        *b_gsf_dz_firstPVtx;   //!
   TBranch        *b_gsf_dzError;   //!
   TBranch        *b_gsf_vz;   //!
   TBranch        *b_gsf_numberOfValidHits;   //!
   TBranch        *b_gsf_nLostInnerHits;   //!
   TBranch        *b_gsf_nLostOuterHits;   //!
   TBranch        *b_gsf_convFlags;   //!
   TBranch        *b_gsf_convDist;   //!
   TBranch        *b_gsf_convDcot;   //!
   TBranch        *b_gsf_convRadius;   //!
   TBranch        *b_gsf_fBrem;   //!
   TBranch        *b_gsf_e1x5;   //!
   TBranch        *b_gsf_e2x5Max;   //!
   TBranch        *b_gsf_e5x5;   //!
   TBranch        *b_gsf_r9;   //!
///////////////////////////////////////

   TBranch *b_gsf_sc_seed_ieta;
   TBranch *b_gsf_sc_seed_iphi;
   TBranch *b_gsf_sc_seed_rawId;          
   TBranch *b_gsf_sc_energy;              
   TBranch *b_gsf_sc_rawEnergy;           
   TBranch *b_gsf_sc_preshowerEnergy;     
   TBranch *b_gsf_sc_lazyTools_e2x5Right; 
   TBranch *b_gsf_sc_lazyTools_e2x5Left;  
   TBranch *b_gsf_sc_lazyTools_e2x5Top;   
   TBranch *b_gsf_sc_lazyTools_e2x5Bottom;
   TBranch *b_gsf_sc_eta;                 
   TBranch *b_gsf_sc_phi;                 
   TBranch *b_gsf_sc_theta;                 
   TBranch *b_gsf_sc_etaWidth;            
   TBranch *b_gsf_sc_phiWidth;            
   TBranch *b_gsf_sc_lazyTools_e2x2;      
   TBranch *b_gsf_sc_lazyTools_e3x3;      
   TBranch *b_gsf_sc_lazyTools_e4x4;      
   TBranch *b_gsf_sc_lazyTools_e5x5;      
   TBranch *b_gsf_sc_lazyTools_e1x3;      
   TBranch *b_gsf_sc_lazyTools_e3x1;      
   TBranch *b_gsf_sc_lazyTools_e1x5;      
   TBranch *b_gsf_sc_lazyTools_e5x1;      
   TBranch *b_gsf_sc_lazyTools_eMax;      
   TBranch *b_gsf_sc_lazyTools_e2nd;      
   TBranch *b_gsf_sc_lazyTools_eLeft;     
   TBranch *b_gsf_sc_lazyTools_eRight;    
   TBranch *b_gsf_sc_lazyTools_eTop;      
   TBranch *b_gsf_sc_lazyTools_eBottom;   

   TBranch *b_EEHits_kSaturated ;
   TBranch *b_EEHits_rawId      ;
   TBranch *b_EBHits_kSaturated ;
   TBranch *b_EBHits_rawId      ;
///////////////////////////////////////
   TBranch *b_mu_ibt_n       ;
   TBranch *b_mu_ibt_p       ;
   TBranch *b_mu_ibt_pt      ;
   TBranch *b_mu_ibt_eta     ;
   TBranch *b_mu_ibt_phi     ;
   TBranch *b_mu_ibt_charge  ;
   TBranch *b_mu_gt_p       ;
   TBranch *b_mu_gt_pt      ;
   TBranch *b_mu_gt_eta     ;
   TBranch *b_mu_gt_phi     ;
   TBranch *b_mu_gt_charge  ;
   TBranch *b_mu_isGlobalMuon;
   TBranch *b_mu_isTightMuon ;
   TBranch *b_mu_pfIsoDbCorrected04 ;
   TBranch *b_mu_trackerLayersWithMeasurement  ;

   TBranch *b_mu_rochester_sf          ;
   TBranch *b_jet_BtagSF_medium        ;
   TBranch *b_jet_BtagSFbcUp_medium    ;
   TBranch *b_jet_BtagSFbcDown_medium  ;
   TBranch *b_jet_BtagSFudsgUp_medium  ;
   TBranch *b_jet_BtagSFudsgDown_medium;
   TBranch *b_jet_SmearedJetResUp_pt      ; 
   TBranch *b_jet_SmearedJetResUp_energy  ; 
   TBranch *b_jet_SmearedJetResDown_pt    ; 
   TBranch *b_jet_SmearedJetResDown_energy; 
   TBranch *b_jet_EnUp_pt                 ; 
   TBranch *b_jet_EnUp_energy             ; 
   TBranch *b_jet_EnDown_pt               ; 
   TBranch *b_jet_EnDown_energy           ; 

//////////////////////////////////////   
   TBranch        *b_MET_caloMet_et;   //!
   TBranch        *b_MET_caloMet_phi;   //!
   TBranch        *b_MET_pfMet_et;   //!
   TBranch        *b_MET_pfMet_phi;   //!
   TBranch        *b_MET_T1Txy_et          ;  
   TBranch        *b_MET_T1Txy_phi         ; 
   TBranch        *b_MET_T1Txy_significance; 
 
   TBranch        *b_MET_T1SmearJetEnDown_Pt  ; 
   TBranch        *b_MET_T1SmearJetEnDown_phi ; 
   TBranch        *b_MET_T1SmearJetEnUp_Pt    ; 
   TBranch        *b_MET_T1SmearJetEnUp_phi   ; 
   TBranch        *b_MET_T1SmearJetResDown_Pt ; 
   TBranch        *b_MET_T1SmearJetResDown_phi; 
   TBranch        *b_MET_T1SmearJetResUp_Pt   ; 
   TBranch        *b_MET_T1SmearJetResUp_phi  ; 
   TBranch        *b_MET_Type1Unc_Pt; 
   TBranch        *b_MET_Type1Unc_Px; 
   TBranch        *b_MET_Type1Unc_Py; 

   TBranch        *b_LHE_weight_nominal; 
   TBranch        *b_LHE_weight_sys    ; 
   TBranch        *b_LHE_id_sys        ; 

   TBranch        *b_ev_prefiringweight    ; 
   TBranch        *b_ev_prefiringweightup    ; 
   TBranch        *b_ev_prefiringweightdown    ; 


   TBranch        *b_mc_w_sign;   //!
   
   TBranch *b_trig_Ele23_Ele12_fire  ;
   TBranch *b_trig_DEle33_fire       ;
   TBranch *b_trig_DEle33_MW_fire    ;
   TBranch *b_trig_DEle25_MW_fire    ;
   TBranch *b_trig_DEle33_CaloId_fire;
   TBranch *b_trig_Ele27_fire        ;
   TBranch *b_trig_Mu8_Ele23_fire    ;
   TBranch *b_trig_Mu23_Ele12_fire   ;
   TBranch *b_trig_Mu8_Ele23_DZ_fire ;
   TBranch *b_trig_Mu23_Ele12_DZ_fire;
   TBranch *b_trig_Mu30_Ele30_fire   ; 
   TBranch *b_trig_Mu33_Ele33_fire   ; 
   TBranch *b_trig_Mu17_TkMu8_fire   ;
   TBranch *b_trig_Mu17_Mu8_fire     ;
   TBranch *b_trig_Mu17_TkMu8_DZ_fire;
   TBranch *b_trig_Mu17_Mu8_DZ_fire  ;
   TBranch *b_trig_Mu30_TkMu11_fire  ;
   TBranch *b_trig_IsoMu24_fire      ; 
   TBranch *b_trig_IsoTkMu24_fire    ; 
   TBranch *b_trig_HLT_PFHT300_PFMET110_fire         ; 
   TBranch *b_trig_HLT_MET200_fire                   ; 
   TBranch *b_trig_HLT_PFMET300_fire                 ; 
   TBranch *b_trig_HLT_PFMET120_PFMHT120_IDTight_fire; 
   TBranch *b_trig_HLT_PFMET170_HBHECleaned_fire     ; 
   TBranch *b_trig_HLT_MET75_IsoTrk50_fire           ; 


   TBranch *b_trig_DEle33_seed_eta     ;
   TBranch *b_trig_DEle33_seed_phi     ;
   TBranch *b_trig_DEle33_unseed_eta   ;
   TBranch *b_trig_DEle33_unseed_phi   ;
   TBranch *b_trig_DEle33_MW_seed_eta  ;
   TBranch *b_trig_DEle33_MW_seed_phi  ;
   TBranch *b_trig_DEle33_MW_unseed_eta;
   TBranch *b_trig_DEle33_MW_unseed_phi;
   TBranch *b_trig_DEle33_MW_L1_eta    ;
   TBranch *b_trig_DEle33_MW_L1_phi    ;
   TBranch *b_trig_DEle33_MW_L1_et     ;
   TBranch *b_L1_pass_final            ;
   TBranch *b_trig_DEle25_MW_seed_eta  ;
   TBranch *b_trig_DEle25_MW_seed_phi  ;
   TBranch *b_trig_DEle25_MW_unseed_eta;
   TBranch *b_trig_DEle25_MW_unseed_phi;
   TBranch *b_trig_DEle25_MW_L1_eta    ;
   TBranch *b_trig_DEle25_MW_L1_phi    ;
   TBranch *b_trig_DEle25_MW_L1_et     ;



   bool isData  ;
   bool isZToTT ;
   bool isTTbar ;
   bool isWW ;
//   int triggerVersion ;
   string triggerVersion ;
   unsigned int Run_low;
   unsigned int Run_high;

   float goldenLumi ;
   float silverLumi ;
   float combinedLumi ;

   reskim(TTree *tree=0, bool isData_in=false, bool isTTbar_in=false, bool isZToTT_in=false, bool isWW_in=false, string triggerVersion_in="", int Run_low_in=0, int Run_high_in=999999);
   virtual ~reskim();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop(TString);
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
};

#endif

#ifdef reskim_cxx
reskim::reskim(TTree *tree, bool isData_in, bool isTTbar_in,  bool isZToTT_in, bool isWW_in, string triggerVersion_in, int Run_low_in, int Run_high_in) :
fChain(0),
goldenLumi(2040.0), 
silverLumi(351.0), 
combinedLumi(2391.0)
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
      //TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("../../samples/RunIISpring15DR74/RunIISpring15DR74_ZToEE_50_120_25ns/outfile_1.root");
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("../../data2015/skims/25ns_golden/SingleElectron_2015D_v4_run258159_10.root");
      if (!f || !f->IsOpen()) {
         f = new TFile("../../samples/RunIISpring15DR74/RunIISpring15DR74_ZToEE_50_120_25ns/outfile_1.root");
         f = new TFile("../../data2015/skims/25ns_golden/SingleElectron_2015D_v4_run258159_10.root");
      }
      f->GetObject("IIHEAnalysis",tree);

   }
   isData  = isData_in  ;
   isZToTT = isZToTT_in ;
   isTTbar = isTTbar_in ;
   isWW = isWW_in ;
   triggerVersion = triggerVersion_in ;
   Run_low=Run_low_in;
   Run_high=Run_high_in;
   Init(tree);
}

reskim::~reskim()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t reskim::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t reskim::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void reskim::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set object pointer
   //
   LHE_pdgid =0;
   LHE_status=0;
   LHE_Pt    =0;
   LHE_Eta   =0;
   LHE_Phi   =0;
   LHE_E     =0;
   mc_w_sign=1;
   mc_index = 0;
   mc_pdgId = 0;
   mc_charge = 0;
   mc_status = 0;
   mc_mass = 0;
   mc_px = 0;
   mc_py = 0;
   mc_pz = 0;
   mc_pt = 0;
   mc_eta = 0;
   mc_phi = 0;
   mc_energy = 0;
   mc_numberOfDaughters = 0;
   mc_numberOfMothers = 0;
   mc_mother_index = 0;
   mc_mother_pdgId = 0;
   mc_mother_px = 0;
   mc_mother_py = 0;
   mc_mother_pz = 0;
   mc_mother_pt = 0;
   mc_mother_eta = 0;
   mc_mother_phi = 0;
   mc_mother_energy = 0;
   mc_mother_mass = 0;
   pv_x = 0;
   pv_y = 0;
   pv_z = 0;
   pv_isValid = 0;
   pv_normalizedChi2 = 0;
   pv_ndof = 0;
   pv_nTracks = 0;
   pv_totTrackSize = 0;
   jet_px                          =0;
   jet_py                          =0;
   jet_pz                          =0;
   jet_pt                          =0;
   jet_eta                         =0;
   jet_phi                         =0;
   jet_energy                      =0;
   jet_mass                        =0;
   jet_neutralHadronEnergyFraction =0;
   jet_neutralEmEnergyFraction     =0;
   jet_chargedHadronEnergyFraction =0;
   jet_chargedEmEnergyFraction     =0;
   jet_muonEnergyFraction          =0;
   jet_chargedMultiplicity         =0;
   jet_neutralMultiplicity         =0;
   jet_CSVv2                       =0;
   jet_isJetIDLoose                =0;

   gsf_classification = 0;
   gsf_energy = 0;
   gsf_p = 0;
   gsf_pt = 0;
   gsf_full5x5_e5x5         =0; 
   gsf_full5x5_e1x5         =0; 
   gsf_full5x5_e2x5Max      =0; 
   gsf_full5x5_sigmaIetaIeta=0; 
   gsf_full5x5_hcalOverEcal =0; 
   gsf_scE1x5 = 0;
   gsf_scE5x5 = 0;
   gsf_scE2x5Max = 0;
   gsf_eta = 0;
   gsf_phi = 0;
   gsf_theta = 0;
   gsf_px = 0;
   gsf_py = 0;
   gsf_pz = 0;
   gsf_superClusterEta = 0;
   gsf_superClusterEnergy = 0;
   gsf_caloEnergy = 0;
   gsf_deltaEtaSuperClusterTrackAtVtx = 0;
   gsf_deltaPhiSuperClusterTrackAtVtx = 0;
   gsf_hadronicOverEm = 0;
   gsf_hcalDepth1OverEcal = 0;
   gsf_hcalDepth2OverEcal = 0;
   gsf_dr03TkSumPt = 0;
   gsf_dr03TkSumPtHEEP7 = 0;
   gsf_dr03EcalRecHitSumEt = 0;
   gsf_dr03HcalDepth1TowerSumEt = 0;
   gsf_dr03HcalDepth2TowerSumEt = 0;
   gsf_charge = 0;
   gsf_sigmaIetaIeta = 0;
   gsf_ecaldrivenSeed = 0;
   gsf_VIDHEEP7 = 0;
   gsf_VIDLoose = 0;
   gsf_VIDTight = 0;
   gsf_trackerdrivenSeed = 0;
   gsf_isEB = 0;
   gsf_isEE = 0;
   gsf_deltaEtaSeedClusterTrackAtVtx  = 0;
   gsf_deltaEtaSeedClusterTrackAtCalo = 0;
   gsf_deltaPhiSeedClusterTrackAtCalo = 0;
   gsf_ecalEnergy = 0;
   gsf_eSuperClusterOverP = 0;
   gsf_dxy = 0;
   gsf_dxy_beamSpot = 0;
   gsf_dxy_firstPVtx = 0;
   gsf_dxyError = 0;
   gsf_dz = 0;
   gsf_dz_beamSpot = 0;
   gsf_dz_firstPVtx = 0;
   gsf_dzError = 0;
   gsf_vz = 0;
   gsf_numberOfValidHits = 0;
   gsf_nLostInnerHits = 0;
   gsf_nLostOuterHits = 0;
   gsf_convFlags = 0;
   gsf_convDist = 0;
   gsf_convDcot = 0;
   gsf_convRadius = 0;
   gsf_fBrem = 0;
   gsf_e1x5 = 0;
   gsf_e2x5Max = 0;
   gsf_e5x5 = 0;
   gsf_r9 = 0;
////////////////////////
   gsf_sc_seed_ieta = 0;
   gsf_sc_seed_iphi = 0;
   gsf_sc_seed_rawId = 0;          
   gsf_sc_energy = 0;              
   gsf_sc_rawEnergy = 0;           
   gsf_sc_preshowerEnergy = 0;     
   gsf_sc_lazyTools_e2x5Right = 0; 
   gsf_sc_lazyTools_e2x5Left = 0;  
   gsf_sc_lazyTools_e2x5Top = 0;   
   gsf_sc_lazyTools_e2x5Bottom = 0;
   gsf_sc_eta = 0;                 
   gsf_sc_phi = 0;                 
   gsf_sc_theta = 0;                 
   gsf_sc_etaWidth = 0;            
   gsf_sc_phiWidth = 0;            
   gsf_sc_lazyTools_e2x2 = 0;      
   gsf_sc_lazyTools_e3x3 = 0;      
   gsf_sc_lazyTools_e4x4 = 0;      
   gsf_sc_lazyTools_e5x5 = 0;      
   gsf_sc_lazyTools_e1x3 = 0;      
   gsf_sc_lazyTools_e3x1 = 0;      
   gsf_sc_lazyTools_e1x5 = 0;      
   gsf_sc_lazyTools_e5x1 = 0;      
   gsf_sc_lazyTools_eMax = 0;      
   gsf_sc_lazyTools_e2nd = 0;      
   gsf_sc_lazyTools_eLeft = 0;     
   gsf_sc_lazyTools_eRight = 0;    
   gsf_sc_lazyTools_eTop = 0;      
   gsf_sc_lazyTools_eBottom = 0;   

   EBHits_kSaturated =0 ;
   EEHits_kSaturated =0 ;
   EBHits_rawId      =0 ;
   EEHits_rawId      =0 ;
////////For Muon /////////////
   mu_ibt_p       =0;
   mu_ibt_pt      =0;
   mu_ibt_eta     =0;
   mu_ibt_phi     =0;
   mu_ibt_charge  =0;
   mu_gt_p       =0;
   mu_gt_pt      =0;
   mu_gt_eta     =0;
   mu_gt_phi     =0;
   mu_gt_charge  =0;
   mu_isGlobalMuon=0;
   mu_isTightMuon =0;
   mu_pfIsoDbCorrected04 =0;
   mu_trackerLayersWithMeasurement  =0;

   mu_rochester_sf          =0;
   jet_BtagSF_medium        =0;
   jet_BtagSFbcUp_medium    =0;
   jet_BtagSFbcDown_medium  =0;
   jet_BtagSFudsgUp_medium  =0;
   jet_BtagSFudsgDown_medium=0;
   jet_SmearedJetResUp_pt      =0;
   jet_SmearedJetResUp_energy  =0;
   jet_SmearedJetResDown_pt    =0;
   jet_SmearedJetResDown_energy=0;
   jet_EnUp_pt                 =0;
   jet_EnUp_energy             =0;
   jet_EnDown_pt               =0;
   jet_EnDown_energy           =0;

   MET_Type1Unc_Pt             =0;
   MET_Type1Unc_Px             =0;
   MET_Type1Unc_Py             =0;

   LHE_weight_sys              =0; 
   LHE_id_sys                  =0; 
   ev_prefiringweight          =0;
   ev_prefiringweightup        =0;
   ev_prefiringweightdown      =0;

////////////////////////////////   
   trig_DEle33_seed_eta     =0;
   trig_DEle33_seed_phi     =0;
   trig_DEle33_unseed_eta   =0;
   trig_DEle33_unseed_phi   =0;
   trig_DEle33_MW_seed_eta  =0;
   trig_DEle33_MW_seed_phi  =0;
   trig_DEle33_MW_unseed_eta=0;
   trig_DEle33_MW_unseed_phi=0;
   trig_DEle33_MW_L1_eta    =0;
   trig_DEle33_MW_L1_phi    =0;
   trig_DEle33_MW_L1_et     =0;
   L1_pass_final            =0;
   trig_DEle25_MW_seed_eta  =0;
   trig_DEle25_MW_seed_phi  =0;
   trig_DEle25_MW_unseed_eta=0;
   trig_DEle25_MW_unseed_phi=0;
   trig_DEle25_MW_L1_eta    =0;
   trig_DEle25_MW_L1_phi    =0;
   trig_DEle25_MW_L1_et     =0;

 
   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);
   
   

   

   fChain->SetBranchAddress("ev_event", &ev_event, &b_ev_event);
   fChain->SetBranchAddress("ev_run", &ev_run, &b_ev_run);
   fChain->SetBranchAddress("ev_luminosityBlock", &ev_luminosityBlock, &b_ev_luminosityBlock);
   fChain->SetBranchAddress("ev_time", &ev_time, &b_ev_time);
   fChain->SetBranchAddress("ev_time_unixTime", &ev_time_unixTime, &b_ev_time_unixTime);
   fChain->SetBranchAddress("ev_time_microsecondOffset", &ev_time_microsecondOffset, &b_ev_time_microsecondOffset);
   fChain->SetBranchAddress("ev_fixedGridRhoAll", &ev_fixedGridRhoAll, &b_ev_fixedGridRhoAll);
   fChain->SetBranchAddress("ev_fixedGridRhoFastjetAll", &ev_fixedGridRhoFastjetAll, &b_ev_fixedGridRhoFastjetAll);
   if(isData==false){
       fChain->SetBranchAddress("LHE_pdgid" , &LHE_pdgid , &b_LHE_pdgid );
       fChain->SetBranchAddress("LHE_status", &LHE_status, &b_LHE_status);
       fChain->SetBranchAddress("LHE_Pt"    , &LHE_Pt    , &b_LHE_Pt    );
       fChain->SetBranchAddress("LHE_Eta"   , &LHE_Eta   , &b_LHE_Eta   );
       fChain->SetBranchAddress("LHE_Phi"   , &LHE_Phi   , &b_LHE_Phi   );
       fChain->SetBranchAddress("LHE_E"     , &LHE_E     , &b_LHE_E     );
       fChain->SetBranchAddress("mc_n", &mc_n, &b_mc_n);
       fChain->SetBranchAddress("mc_w_sign", &mc_w_sign, &b_mc_w_sign);
       fChain->SetBranchAddress("mc_index", &mc_index, &b_mc_index);
       fChain->SetBranchAddress("mc_pdgId", &mc_pdgId, &b_mc_pdgId);
       fChain->SetBranchAddress("mc_charge", &mc_charge, &b_mc_charge);
       fChain->SetBranchAddress("mc_status", &mc_status, &b_mc_status);
       fChain->SetBranchAddress("mc_mass", &mc_mass, &b_mc_mass);
       fChain->SetBranchAddress("mc_px", &mc_px, &b_mc_px);
       fChain->SetBranchAddress("mc_py", &mc_py, &b_mc_py);
       fChain->SetBranchAddress("mc_pz", &mc_pz, &b_mc_pz);
       fChain->SetBranchAddress("mc_pt", &mc_pt, &b_mc_pt);
       fChain->SetBranchAddress("mc_eta", &mc_eta, &b_mc_eta);
       fChain->SetBranchAddress("mc_phi", &mc_phi, &b_mc_phi);
       fChain->SetBranchAddress("mc_energy", &mc_energy, &b_mc_energy);
       fChain->SetBranchAddress("mc_numberOfDaughters", &mc_numberOfDaughters, &b_mc_numberOfDaughters);
       fChain->SetBranchAddress("mc_numberOfMothers", &mc_numberOfMothers, &b_mc_numberOfMothers);
       fChain->SetBranchAddress("mc_mother_index", &mc_mother_index, &b_mc_mother_index);
       fChain->SetBranchAddress("mc_mother_pdgId", &mc_mother_pdgId, &b_mc_mother_pdgId);
       fChain->SetBranchAddress("mc_mother_px", &mc_mother_px, &b_mc_mother_px);
       fChain->SetBranchAddress("mc_mother_py", &mc_mother_py, &b_mc_mother_py);
       fChain->SetBranchAddress("mc_mother_pz", &mc_mother_pz, &b_mc_mother_pz);
       fChain->SetBranchAddress("mc_mother_pt", &mc_mother_pt, &b_mc_mother_pt);
       fChain->SetBranchAddress("mc_mother_eta", &mc_mother_eta, &b_mc_mother_eta);
       fChain->SetBranchAddress("mc_mother_phi", &mc_mother_phi, &b_mc_mother_phi);
       fChain->SetBranchAddress("mc_mother_energy", &mc_mother_energy, &b_mc_mother_energy);
       fChain->SetBranchAddress("mc_mother_mass", &mc_mother_mass, &b_mc_mother_mass);
       fChain->SetBranchAddress("mc_trueNumInteractions", &mc_trueNumInteractions, &b_mc_trueNumInteractions);
       fChain->SetBranchAddress("mc_PU_NumInteractions", &mc_PU_NumInteractions, &b_mc_PU_NumInteractions);
//       fChain->SetBranchAddress("MET_T1Smear_Pt"    ,&MET_pfMet_et , &b_MET_pfMet_et );
//       fChain->SetBranchAddress("MET_T1Smear_phi"   ,&MET_pfMet_phi, &b_MET_pfMet_phi);
       fChain->SetBranchAddress("jet_Smeared_pt"    ,&jet_pt       , &b_jet_pt       );
       fChain->SetBranchAddress("jet_Smeared_energy",&jet_energy   , &b_jet_energy   );
//       fChain->SetBranchAddress("mu_rochester_sf"             ,&mu_rochester_sf             ,&b_mu_rochester_sf              );
//       fChain->SetBranchAddress("jet_BtagSF_loose"            ,&jet_BtagSF_loose            ,&b_jet_BtagSF_loose             );
//       fChain->SetBranchAddress("jet_BtagSFbcUp_loose"        ,&jet_BtagSFbcUp_loose        ,&b_jet_BtagSFbcUp_loose         );
//       fChain->SetBranchAddress("jet_BtagSFbcDown_loose"      ,&jet_BtagSFbcDown_loose      ,&b_jet_BtagSFbcDown_loose       );
//       fChain->SetBranchAddress("jet_BtagSFudsgUp_loose"      ,&jet_BtagSFudsgUp_loose      ,&b_jet_BtagSFudsgUp_loose       );
//       fChain->SetBranchAddress("jet_BtagSFudsgDown_loose"    ,&jet_BtagSFudsgDown_loose    ,&b_jet_BtagSFudsgDown_loose     );
//       fChain->SetBranchAddress("jet_BtagSF_medium"           ,&jet_BtagSF_medium           ,&b_jet_BtagSF_medium            );
//       fChain->SetBranchAddress("jet_BtagSFbcUp_medium"       ,&jet_BtagSFbcUp_medium       ,&b_jet_BtagSFbcUp_medium        );
//       fChain->SetBranchAddress("jet_BtagSFbcDown_medium"     ,&jet_BtagSFbcDown_medium     ,&b_jet_BtagSFbcDown_medium      );
//       fChain->SetBranchAddress("jet_BtagSFudsgUp_medium"     ,&jet_BtagSFudsgUp_medium     ,&b_jet_BtagSFudsgUp_medium      );
//       fChain->SetBranchAddress("jet_BtagSFudsgDown_medium"   ,&jet_BtagSFudsgDown_medium   ,&b_jet_BtagSFudsgDown_medium    );
//       fChain->SetBranchAddress("jet_SmearedJetResUp_pt"      ,&jet_SmearedJetResUp_pt      ,&b_jet_SmearedJetResUp_pt       );
//       fChain->SetBranchAddress("jet_SmearedJetResUp_energy"  ,&jet_SmearedJetResUp_energy  ,&b_jet_SmearedJetResUp_energy   );
//       fChain->SetBranchAddress("jet_SmearedJetResDown_pt"    ,&jet_SmearedJetResDown_pt    ,&b_jet_SmearedJetResDown_pt     );
//       fChain->SetBranchAddress("jet_SmearedJetResDown_energy",&jet_SmearedJetResDown_energy,&b_jet_SmearedJetResDown_energy );
//       fChain->SetBranchAddress("jet_EnUp_pt"                 ,&jet_EnUp_pt                 ,&b_jet_EnUp_pt                  );
//       fChain->SetBranchAddress("jet_EnUp_energy"             ,&jet_EnUp_energy             ,&b_jet_EnUp_energy              );
//       fChain->SetBranchAddress("jet_EnDown_pt"               ,&jet_EnDown_pt               ,&b_jet_EnDown_pt                );
//       fChain->SetBranchAddress("jet_EnDown_energy"           ,&jet_EnDown_energy           ,&b_jet_EnDown_energy            );
//       fChain->SetBranchAddress("MET_T1SmearJetEnDown_Pt"     ,&MET_T1SmearJetEnDown_Pt     ,&b_MET_T1SmearJetEnDown_Pt      );
//       fChain->SetBranchAddress("MET_T1SmearJetEnDown_phi"    ,&MET_T1SmearJetEnDown_phi    ,&b_MET_T1SmearJetEnDown_phi     );
//       fChain->SetBranchAddress("MET_T1SmearJetEnUp_Pt"       ,&MET_T1SmearJetEnUp_Pt       ,&b_MET_T1SmearJetEnUp_Pt        );
//       fChain->SetBranchAddress("MET_T1SmearJetEnUp_phi"      ,&MET_T1SmearJetEnUp_phi      ,&b_MET_T1SmearJetEnUp_phi       );
//       fChain->SetBranchAddress("MET_T1SmearJetResDown_Pt"    ,&MET_T1SmearJetResDown_Pt    ,&b_MET_T1SmearJetResDown_Pt     );
//       fChain->SetBranchAddress("MET_T1SmearJetResDown_phi"   ,&MET_T1SmearJetResDown_phi   ,&b_MET_T1SmearJetResDown_phi    );
//       fChain->SetBranchAddress("MET_T1SmearJetResUp_Pt"      ,&MET_T1SmearJetResUp_Pt      ,&b_MET_T1SmearJetResUp_Pt       );
//       fChain->SetBranchAddress("MET_T1SmearJetResUp_phi"     ,&MET_T1SmearJetResUp_phi     ,&b_MET_T1SmearJetResUp_phi      );
//       fChain->SetBranchAddress("MET_Type1Unc_Pt"             ,&MET_Type1Unc_Pt    ,&b_MET_Type1Unc_Pt     );
//       fChain->SetBranchAddress("MET_Type1Unc_Px"             ,&MET_Type1Unc_Px    ,&b_MET_Type1Unc_Px     );
//       fChain->SetBranchAddress("MET_Type1Unc_Py"             ,&MET_Type1Unc_Py    ,&b_MET_Type1Unc_Py     );
       //################# LHE weight for PDF uncertainty ########################################################
       fChain->SetBranchAddress("LHE_weight_nominal"          ,&LHE_weight_nominal    ,&b_LHE_weight_nominal     );
       fChain->SetBranchAddress("LHE_weight_sys"              ,&LHE_weight_sys        ,&b_LHE_weight_sys         );
       fChain->SetBranchAddress("LHE_id_sys"                  ,&LHE_id_sys            ,&b_LHE_id_sys             );

       //################# weight for Prefiring ########################################################
       fChain->SetBranchAddress("ev_prefiringweight"          ,&ev_prefiringweight    ,&b_ev_prefiringweight     );
       fChain->SetBranchAddress("ev_prefiringweightup"        ,&ev_prefiringweightup  ,&b_ev_prefiringweightup   );
       fChain->SetBranchAddress("ev_prefiringweightdown"      ,&ev_prefiringweightdown,&b_ev_prefiringweightdown );

   }
   else{
//       fChain->SetBranchAddress("MET_pfMetMuEGClean_et" ,&MET_pfMet_et  , &b_MET_pfMet_et );
//       fChain->SetBranchAddress("MET_pfMetMuEGClean_phi",&MET_pfMet_phi , &b_MET_pfMet_phi);
       fChain->SetBranchAddress("jet_pt"                ,&jet_pt        , &b_jet_pt       );
       fChain->SetBranchAddress("jet_energy"            ,&jet_energy    , &b_jet_energy   );
   }
   fChain->SetBranchAddress("trig_Flag_HBHENoiseFilter_accept"                   ,&trig_Flag_HBHENoiseFilter_accept                      ,&b_trig_Flag_HBHENoiseFilter_accept                    );
   fChain->SetBranchAddress("trig_Flag_HBHENoiseIsoFilter_accept"                ,&trig_Flag_HBHENoiseIsoFilter_accept                   ,&b_trig_Flag_HBHENoiseIsoFilter_accept                 );
   fChain->SetBranchAddress("trig_Flag_CSCTightHaloFilter_accept"                ,&trig_Flag_CSCTightHaloFilter_accept                   ,&b_trig_Flag_CSCTightHaloFilter_accept                 );
   fChain->SetBranchAddress("trig_Flag_CSCTightHaloTrkMuUnvetoFilter_accept"     ,&trig_Flag_CSCTightHaloTrkMuUnvetoFilter_accept        ,&b_trig_Flag_CSCTightHaloTrkMuUnvetoFilter_accept      );
   fChain->SetBranchAddress("trig_Flag_CSCTightHalo2015Filter_accept"            ,&trig_Flag_CSCTightHalo2015Filter_accept               ,&b_trig_Flag_CSCTightHalo2015Filter_accept             );
   fChain->SetBranchAddress("trig_Flag_globalTightHalo2016Filter_accept"         ,&trig_Flag_globalTightHalo2016Filter_accept            ,&b_trig_Flag_globalTightHalo2016Filter_accept          );
   fChain->SetBranchAddress("trig_Flag_globalSuperTightHalo2016Filter_accept"    ,&trig_Flag_globalSuperTightHalo2016Filter_accept       ,&b_trig_Flag_globalSuperTightHalo2016Filter_accept     );
   fChain->SetBranchAddress("trig_Flag_goodVertices_accept"                      ,&trig_Flag_goodVertices_accept                         ,&b_trig_Flag_goodVertices_accept                       );
   fChain->SetBranchAddress("trig_Flag_HcalStripHaloFilter_accept"               ,&trig_Flag_HcalStripHaloFilter_accept                  ,&b_trig_Flag_HcalStripHaloFilter_accept                );
   fChain->SetBranchAddress("trig_Flag_hcalLaserEventFilter_accept"              ,&trig_Flag_hcalLaserEventFilter_accept                 ,&b_trig_Flag_hcalLaserEventFilter_accept               );
   fChain->SetBranchAddress("trig_Flag_EcalDeadCellTriggerPrimitiveFilter_accept",&trig_Flag_EcalDeadCellTriggerPrimitiveFilter_accept   ,&b_trig_Flag_EcalDeadCellTriggerPrimitiveFilter_accept );
   fChain->SetBranchAddress("trig_Flag_EcalDeadCellBoundaryEnergyFilter_accept"  ,&trig_Flag_EcalDeadCellBoundaryEnergyFilter_accept     ,&b_trig_Flag_EcalDeadCellBoundaryEnergyFilter_accept   );
   fChain->SetBranchAddress("trig_Flag_ecalLaserCorrFilter_accept"               ,&trig_Flag_ecalLaserCorrFilter_accept                  ,&b_trig_Flag_ecalLaserCorrFilter_accept                );
   fChain->SetBranchAddress("trig_Flag_chargedHadronTrackResolutionFilter_accept",&trig_Flag_chargedHadronTrackResolutionFilter_accept   ,&b_trig_Flag_chargedHadronTrackResolutionFilter_accept );
   fChain->SetBranchAddress("trig_Flag_muonBadTrackFilter_accept"                ,&trig_Flag_muonBadTrackFilter_accept                   ,&b_trig_Flag_muonBadTrackFilter_accept                 );
   fChain->SetBranchAddress("trig_Flag_BadPFMuonFilter_accept"                   ,&trig_Flag_BadPFMuonFilter_accept                      ,&b_trig_Flag_BadPFMuonFilter_accept                    );
   fChain->SetBranchAddress("trig_Flag_BadChargedCandidateFilter_accept"         ,&trig_Flag_BadChargedCandidateFilter_accept            ,&b_trig_Flag_BadChargedCandidateFilter_accept          );
   fChain->SetBranchAddress("trig_Flag_eeBadScFilter_accept"                     ,&trig_Flag_eeBadScFilter_accept                        ,&b_trig_Flag_eeBadScFilter_accept                      );
   fChain->SetBranchAddress("trig_Flag_trkPOG_manystripclus53X_accept"           ,&trig_Flag_trkPOG_manystripclus53X_accept              ,&b_trig_Flag_trkPOG_manystripclus53X_accept            );
   fChain->SetBranchAddress("trig_Flag_trkPOG_toomanystripclus53X_accept"        ,&trig_Flag_trkPOG_toomanystripclus53X_accept           ,&b_trig_Flag_trkPOG_toomanystripclus53X_accept         );
   fChain->SetBranchAddress("trig_Flag_trkPOG_logErrorTooManyClusters_accept"    ,&trig_Flag_trkPOG_logErrorTooManyClusters_accept       ,&b_trig_Flag_trkPOG_logErrorTooManyClusters_accept     );
   fChain->SetBranchAddress("trig_Flag_METFilters_accept"                        ,&trig_Flag_METFilters_accept                           ,&b_trig_Flag_METFilters_accept                         );
   fChain->SetBranchAddress("pv_n"             , &pv_n             , &b_pv_n             );
   fChain->SetBranchAddress("pv_x"             , &pv_x             , &b_pv_x             );
   fChain->SetBranchAddress("pv_y"             , &pv_y             , &b_pv_y             );
   fChain->SetBranchAddress("pv_z"             , &pv_z             , &b_pv_z             );
   fChain->SetBranchAddress("pv_isValid"       , &pv_isValid       , &b_pv_isValid       );
   fChain->SetBranchAddress("pv_normalizedChi2", &pv_normalizedChi2, &b_pv_normalizedChi2);
   fChain->SetBranchAddress("pv_ndof"          , &pv_ndof          , &b_pv_ndof          );
//   fChain->SetBranchAddress("pv_nTracks"       , &pv_nTracks       , &b_pv_nTracks       );
//   fChain->SetBranchAddress("pv_totTrackSize"  , &pv_totTrackSize  , &b_pv_totTrackSize  );
   fChain->SetBranchAddress("jet_n"                          ,&jet_n                          , &b_jet_n                          );
   fChain->SetBranchAddress("jet_px"                         ,&jet_px                         , &b_jet_px                         );
   fChain->SetBranchAddress("jet_py"                         ,&jet_py                         , &b_jet_py                         );
   fChain->SetBranchAddress("jet_pz"                         ,&jet_pz                         , &b_jet_pz                         );
   fChain->SetBranchAddress("jet_eta"                        ,&jet_eta                        , &b_jet_eta                        );
   fChain->SetBranchAddress("jet_phi"                        ,&jet_phi                        , &b_jet_phi                        );
   fChain->SetBranchAddress("jet_mass"                       ,&jet_mass                       , &b_jet_mass                       );
   fChain->SetBranchAddress("jet_neutralHadronEnergyFraction",&jet_neutralHadronEnergyFraction, &b_jet_neutralHadronEnergyFraction);
   fChain->SetBranchAddress("jet_neutralEmEnergyFraction"    ,&jet_neutralEmEnergyFraction    , &b_jet_neutralEmEnergyFraction    );
   fChain->SetBranchAddress("jet_chargedHadronEnergyFraction",&jet_chargedHadronEnergyFraction, &b_jet_chargedHadronEnergyFraction);
   fChain->SetBranchAddress("jet_chargedEmEnergyFraction"    ,&jet_chargedEmEnergyFraction    , &b_jet_chargedEmEnergyFraction    );
   fChain->SetBranchAddress("jet_muonEnergyFraction"         ,&jet_muonEnergyFraction         , &b_jet_muonEnergyFraction         );
   fChain->SetBranchAddress("jet_chargedMultiplicity"        ,&jet_chargedMultiplicity        , &b_jet_chargedMultiplicity        );
   fChain->SetBranchAddress("jet_neutralMultiplicity"        ,&jet_neutralMultiplicity        , &b_jet_neutralMultiplicity        );
   fChain->SetBranchAddress("jet_CSVv2"                      ,&jet_CSVv2                      , &b_jet_CSVv2                      );
   fChain->SetBranchAddress("jet_isJetIDLoose"               ,&jet_isJetIDLoose               , &b_jet_isJetIDLoose               );
//   fChain->SetBranchAddress("MET_T1Txy_Pt"                   ,&MET_T1Txy_et                   , &b_MET_T1Txy_et                   );
//   fChain->SetBranchAddress("MET_T1Txy_phi"                  ,&MET_T1Txy_phi                  , &b_MET_T1Txy_phi                  );
//   fChain->SetBranchAddress("MET_T1Txy_significance"         ,&MET_T1Txy_significance         , &b_MET_T1Txy_significance         );
//################################## gsf ##############################################################################################

   fChain->SetBranchAddress("gsf_n", &gsf_n, &b_gsf_n);
   fChain->SetBranchAddress("gsf_classification", &gsf_classification, &b_gsf_classification);
   fChain->SetBranchAddress("gsf_energy", &gsf_energy, &b_gsf_energy);
   fChain->SetBranchAddress("gsf_p", &gsf_p, &b_gsf_p);
   fChain->SetBranchAddress("gsf_pt", &gsf_pt, &b_gsf_pt);
   fChain->SetBranchAddress("gsf_full5x5_e5x5"         , &gsf_full5x5_e5x5         , &b_gsf_full5x5_e5x5         );
   fChain->SetBranchAddress("gsf_full5x5_e1x5"         , &gsf_full5x5_e1x5         , &b_gsf_full5x5_e1x5         );
   fChain->SetBranchAddress("gsf_full5x5_e2x5Max"      , &gsf_full5x5_e2x5Max      , &b_gsf_full5x5_e2x5Max      );
   fChain->SetBranchAddress("gsf_full5x5_sigmaIetaIeta", &gsf_full5x5_sigmaIetaIeta, &b_gsf_full5x5_sigmaIetaIeta);
   fChain->SetBranchAddress("gsf_full5x5_hcalOverEcal" , &gsf_full5x5_hcalOverEcal , &b_gsf_full5x5_hcalOverEcal );
   fChain->SetBranchAddress("gsf_scE1x5", &gsf_scE1x5, &b_gsf_scE1x5);
   fChain->SetBranchAddress("gsf_scE5x5", &gsf_scE5x5, &b_gsf_scE5x5);
   fChain->SetBranchAddress("gsf_scE2x5Max", &gsf_scE2x5Max, &b_gsf_scE2x5Max);
   fChain->SetBranchAddress("gsf_eta", &gsf_eta, &b_gsf_eta);
   fChain->SetBranchAddress("gsf_phi", &gsf_phi, &b_gsf_phi);
   fChain->SetBranchAddress("gsf_theta", &gsf_theta, &b_gsf_theta);
   fChain->SetBranchAddress("gsf_px", &gsf_px, &b_gsf_px);
   fChain->SetBranchAddress("gsf_py", &gsf_py, &b_gsf_py);
   fChain->SetBranchAddress("gsf_pz", &gsf_pz, &b_gsf_pz);
   fChain->SetBranchAddress("gsf_ecalEnergyPostCorr", &gsf_caloEnergy, &b_gsf_caloEnergy);
//   fChain->SetBranchAddress("gsf_caloEnergy", &gsf_caloEnergy, &b_gsf_caloEnergy);
   fChain->SetBranchAddress("gsf_deltaEtaSuperClusterTrackAtVtx", &gsf_deltaEtaSuperClusterTrackAtVtx, &b_gsf_deltaEtaSuperClusterTrackAtVtx);
   fChain->SetBranchAddress("gsf_deltaPhiSuperClusterTrackAtVtx", &gsf_deltaPhiSuperClusterTrackAtVtx, &b_gsf_deltaPhiSuperClusterTrackAtVtx);
   fChain->SetBranchAddress("gsf_hadronicOverEm", &gsf_hadronicOverEm, &b_gsf_hadronicOverEm);
   fChain->SetBranchAddress("gsf_hcalDepth1OverEcal", &gsf_hcalDepth1OverEcal, &b_gsf_hcalDepth1OverEcal);
   fChain->SetBranchAddress("gsf_hcalDepth2OverEcal", &gsf_hcalDepth2OverEcal, &b_gsf_hcalDepth2OverEcal);
//   fChain->SetBranchAddress("gsf_dr03TkSumPt", &gsf_dr03TkSumPtHEEP7, &b_gsf_dr03TkSumPtHEEP7);
   fChain->SetBranchAddress("gsf_heepTrkPtIso", &gsf_dr03TkSumPtHEEP7, &b_gsf_dr03TkSumPtHEEP7);
   fChain->SetBranchAddress("gsf_dr03EcalRecHitSumEt", &gsf_dr03EcalRecHitSumEt, &b_gsf_dr03EcalRecHitSumEt);
   fChain->SetBranchAddress("gsf_dr03HcalDepth1TowerSumEt", &gsf_dr03HcalDepth1TowerSumEt, &b_gsf_dr03HcalDepth1TowerSumEt);
   fChain->SetBranchAddress("gsf_dr03HcalDepth2TowerSumEt", &gsf_dr03HcalDepth2TowerSumEt, &b_gsf_dr03HcalDepth2TowerSumEt);
   fChain->SetBranchAddress("gsf_charge", &gsf_charge, &b_gsf_charge);
   fChain->SetBranchAddress("gsf_sigmaIetaIeta", &gsf_sigmaIetaIeta, &b_gsf_sigmaIetaIeta);
   fChain->SetBranchAddress("gsf_ecaldrivenSeed", &gsf_ecaldrivenSeed, &b_gsf_ecaldrivenSeed);
//   fChain->SetBranchAddress("gsf_VIDHEEP7"      , &gsf_VIDHEEP7      , &b_gsf_VIDHEEP7);
   fChain->SetBranchAddress("gsf_VID_heepElectronID_HEEPV70"      , &gsf_VIDHEEP7      , &b_gsf_VIDHEEP7);
   fChain->SetBranchAddress("gsf_VIDLoose"      , &gsf_VIDLoose      , &b_gsf_VIDLoose);
   fChain->SetBranchAddress("gsf_VIDTight"      , &gsf_VIDTight      , &b_gsf_VIDTight);
   fChain->SetBranchAddress("gsf_trackerdrivenSeed", &gsf_trackerdrivenSeed, &b_gsf_trackerdrivenSeed);
   fChain->SetBranchAddress("gsf_deltaEtaSeedClusterTrackAtVtx",  &gsf_deltaEtaSeedClusterTrackAtVtx,  &b_gsf_deltaEtaSeedClusterTrackAtVtx);
   fChain->SetBranchAddress("gsf_deltaEtaSeedClusterTrackAtCalo", &gsf_deltaEtaSeedClusterTrackAtCalo, &b_gsf_deltaEtaSeedClusterTrackAtCalo);
   fChain->SetBranchAddress("gsf_deltaPhiSeedClusterTrackAtCalo", &gsf_deltaPhiSeedClusterTrackAtCalo, &b_gsf_deltaPhiSeedClusterTrackAtCalo);
   fChain->SetBranchAddress("gsf_ecalEnergy", &gsf_ecalEnergy, &b_gsf_ecalEnergy);
   fChain->SetBranchAddress("gsf_eSuperClusterOverP", &gsf_eSuperClusterOverP, &b_gsf_eSuperClusterOverP);
   fChain->SetBranchAddress("gsf_dxy", &gsf_dxy, &b_gsf_dxy);
   fChain->SetBranchAddress("gsf_dxy_beamSpot", &gsf_dxy_beamSpot, &b_gsf_dxy_beamSpot);
   fChain->SetBranchAddress("gsf_dxy_firstPVtx", &gsf_dxy_firstPVtx, &b_gsf_dxy_firstPVtx);
   fChain->SetBranchAddress("gsf_dxyError", &gsf_dxyError, &b_gsf_dxyError);
   fChain->SetBranchAddress("gsf_dz", &gsf_dz, &b_gsf_dz);
   fChain->SetBranchAddress("gsf_dz_beamSpot", &gsf_dz_beamSpot, &b_gsf_dz_beamSpot);
   fChain->SetBranchAddress("gsf_dz_firstPVtx", &gsf_dz_firstPVtx, &b_gsf_dz_firstPVtx);
   fChain->SetBranchAddress("gsf_dzError", &gsf_dzError, &b_gsf_dzError);
   fChain->SetBranchAddress("gsf_vz", &gsf_vz, &b_gsf_vz);
   fChain->SetBranchAddress("gsf_numberOfValidHits", &gsf_numberOfValidHits, &b_gsf_numberOfValidHits);
   fChain->SetBranchAddress("gsf_nLostInnerHits", &gsf_nLostInnerHits, &b_gsf_nLostInnerHits);
   fChain->SetBranchAddress("gsf_nLostOuterHits", &gsf_nLostOuterHits, &b_gsf_nLostOuterHits);
   fChain->SetBranchAddress("gsf_convFlags", &gsf_convFlags, &b_gsf_convFlags);
   fChain->SetBranchAddress("gsf_convDist", &gsf_convDist, &b_gsf_convDist);
   fChain->SetBranchAddress("gsf_convDcot", &gsf_convDcot, &b_gsf_convDcot);
   fChain->SetBranchAddress("gsf_convRadius", &gsf_convRadius, &b_gsf_convRadius);
   fChain->SetBranchAddress("gsf_fBrem", &gsf_fBrem, &b_gsf_fBrem);
   fChain->SetBranchAddress("gsf_e1x5", &gsf_e1x5, &b_gsf_e1x5);
   fChain->SetBranchAddress("gsf_e2x5Max", &gsf_e2x5Max, &b_gsf_e2x5Max);
   fChain->SetBranchAddress("gsf_e5x5", &gsf_e5x5, &b_gsf_e5x5);
   fChain->SetBranchAddress("gsf_r9", &gsf_r9, &b_gsf_r9);
//########################################### Saturation study #########################################
   fChain->SetBranchAddress("gsf_sc_energy",               &gsf_sc_energy, &b_gsf_sc_energy);
   fChain->SetBranchAddress("gsf_sc_seed_rawId",           &gsf_sc_seed_rawId, &b_gsf_sc_seed_rawId);
   fChain->SetBranchAddress("gsf_sc_seed_ieta",            &gsf_sc_seed_ieta, &b_gsf_sc_seed_ieta);
   fChain->SetBranchAddress("gsf_sc_seed_iphi",            &gsf_sc_seed_iphi, &b_gsf_sc_seed_iphi);
   fChain->SetBranchAddress("gsf_sc_rawEnergy",            &gsf_sc_rawEnergy, &b_gsf_sc_rawEnergy);
   fChain->SetBranchAddress("gsf_sc_preshowerEnergy",      &gsf_sc_preshowerEnergy, &b_gsf_sc_preshowerEnergy);
   fChain->SetBranchAddress("gsf_sc_lazyTools_e2x5Right",  &gsf_sc_lazyTools_e2x5Right, &b_gsf_sc_lazyTools_e2x5Right);
   fChain->SetBranchAddress("gsf_sc_lazyTools_e2x5Left",   &gsf_sc_lazyTools_e2x5Left, &b_gsf_sc_lazyTools_e2x5Left);
   fChain->SetBranchAddress("gsf_sc_lazyTools_e2x5Top",    &gsf_sc_lazyTools_e2x5Top, &b_gsf_sc_lazyTools_e2x5Top);
   fChain->SetBranchAddress("gsf_sc_lazyTools_e2x5Bottom", &gsf_sc_lazyTools_e2x5Bottom, &b_gsf_sc_lazyTools_e2x5Bottom);
   fChain->SetBranchAddress("gsf_sc_eta",                  &gsf_sc_eta, &b_gsf_sc_eta);
   fChain->SetBranchAddress("gsf_sc_phi",                  &gsf_sc_phi, &b_gsf_sc_phi);
   fChain->SetBranchAddress("gsf_sc_theta",                &gsf_sc_theta, &b_gsf_sc_theta);
   fChain->SetBranchAddress("gsf_sc_etaWidth",             &gsf_sc_etaWidth, &b_gsf_sc_etaWidth);
   fChain->SetBranchAddress("gsf_sc_phiWidth",             &gsf_sc_phiWidth, &b_gsf_sc_phiWidth);
   fChain->SetBranchAddress("gsf_sc_lazyTools_e2x2",       &gsf_sc_lazyTools_e2x2, &b_gsf_sc_lazyTools_e2x2);
   fChain->SetBranchAddress("gsf_sc_lazyTools_e3x3",       &gsf_sc_lazyTools_e3x3, &b_gsf_sc_lazyTools_e3x3);
   fChain->SetBranchAddress("gsf_sc_lazyTools_e4x4",       &gsf_sc_lazyTools_e4x4, &b_gsf_sc_lazyTools_e4x4);
   fChain->SetBranchAddress("gsf_sc_lazyTools_e5x5",       &gsf_sc_lazyTools_e5x5, &b_gsf_sc_lazyTools_e5x5);
   fChain->SetBranchAddress("gsf_sc_lazyTools_e1x3",       &gsf_sc_lazyTools_e1x3, &b_gsf_sc_lazyTools_e1x3);
   fChain->SetBranchAddress("gsf_sc_lazyTools_e3x1",       &gsf_sc_lazyTools_e3x1, &b_gsf_sc_lazyTools_e3x1);
   fChain->SetBranchAddress("gsf_sc_lazyTools_e1x5",       &gsf_sc_lazyTools_e1x5, &b_gsf_sc_lazyTools_e1x5);
   fChain->SetBranchAddress("gsf_sc_lazyTools_e5x1",       &gsf_sc_lazyTools_e5x1, &b_gsf_sc_lazyTools_e5x1);
   fChain->SetBranchAddress("gsf_sc_lazyTools_eMax",       &gsf_sc_lazyTools_eMax, &b_gsf_sc_lazyTools_eMax);
   fChain->SetBranchAddress("gsf_sc_lazyTools_e2nd",       &gsf_sc_lazyTools_e2nd, &b_gsf_sc_lazyTools_e2nd);
   fChain->SetBranchAddress("gsf_sc_lazyTools_eLeft",      &gsf_sc_lazyTools_eLeft, &b_gsf_sc_lazyTools_eLeft);
   fChain->SetBranchAddress("gsf_sc_lazyTools_eRight",     &gsf_sc_lazyTools_eRight, &b_gsf_sc_lazyTools_eRight);
   fChain->SetBranchAddress("gsf_sc_lazyTools_eTop",       &gsf_sc_lazyTools_eTop, &b_gsf_sc_lazyTools_eTop);
   fChain->SetBranchAddress("gsf_sc_lazyTools_eBottom",    &gsf_sc_lazyTools_eBottom, &b_gsf_sc_lazyTools_eBottom);
//########################################### Hits #########################################
   fChain->SetBranchAddress("EEHits_kSaturated"           , &EEHits_kSaturated, &b_EEHits_kSaturated);
   fChain->SetBranchAddress("EEHits_rawId"                , &EEHits_rawId     , &b_EEHits_rawId     );
   fChain->SetBranchAddress("EBHits_kSaturated"           , &EBHits_kSaturated, &b_EBHits_kSaturated);
   fChain->SetBranchAddress("EBHits_rawId"                , &EBHits_rawId     , &b_EBHits_rawId     );
//####################For Muon############################################################################
//   fChain->SetBranchAddress("mu_ibt_n"       , &mu_ibt_n       , &b_mu_ibt_n       );
   fChain->SetBranchAddress("mu_ibt_p"       , &mu_ibt_p       , &b_mu_ibt_p       );
   fChain->SetBranchAddress("mu_ibt_pt"      , &mu_ibt_pt      , &b_mu_ibt_pt      );
   fChain->SetBranchAddress("mu_ibt_eta"     , &mu_ibt_eta     , &b_mu_ibt_eta     );
   fChain->SetBranchAddress("mu_ibt_phi"     , &mu_ibt_phi     , &b_mu_ibt_phi     );
   fChain->SetBranchAddress("mu_ibt_charge"  , &mu_ibt_charge  , &b_mu_ibt_charge  );
   fChain->SetBranchAddress("mu_gt_p"        , &mu_gt_p        , &b_mu_gt_p       );
   fChain->SetBranchAddress("mu_gt_pt"       , &mu_gt_pt       , &b_mu_gt_pt      );
   fChain->SetBranchAddress("mu_gt_eta"      , &mu_gt_eta      , &b_mu_gt_eta     );
   fChain->SetBranchAddress("mu_gt_phi"      , &mu_gt_phi      , &b_mu_gt_phi     );
   fChain->SetBranchAddress("mu_gt_charge"   , &mu_gt_charge   , &b_mu_gt_charge  );
   fChain->SetBranchAddress("mu_isGlobalMuon", &mu_isGlobalMuon, &b_mu_isGlobalMuon);
   fChain->SetBranchAddress("mu_isTightMuon" , &mu_isTightMuon , &b_mu_isTightMuon );
   fChain->SetBranchAddress("mu_pfIsoDbCorrected04" , &mu_pfIsoDbCorrected04 , &b_mu_pfIsoDbCorrected04 );
   fChain->SetBranchAddress("mu_trackerLayersWithMeasurement" , &mu_trackerLayersWithMeasurement , &b_mu_trackerLayersWithMeasurement );
//############### For trigger ##############################################################################
//   fChain->SetBranchAddress("trig_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_accept"         , &trig_Ele23_Ele12_fire  ,  &b_trig_Ele23_Ele12_fire   ) ;
   fChain->SetBranchAddress("trig_HLT_DoubleEle33_CaloIdL_GsfTrkIdVL_accept"                , &trig_DEle33_fire       ,  &b_trig_DEle33_fire        ) ;
   fChain->SetBranchAddress("trig_HLT_DoubleEle33_CaloIdL_MW_accept"                        , &trig_DEle33_MW_fire    ,  &b_trig_DEle33_MW_fire     ) ;
   fChain->SetBranchAddress("trig_HLT_DoubleEle25_CaloIdL_MW_accept"                        , &trig_DEle25_MW_fire    ,  &b_trig_DEle25_MW_fire     ) ;
//   fChain->SetBranchAddress("trig_HLT_DoubleEle33_CaloIdL_accept"                           , &trig_DEle33_CaloId_fire,  &b_trig_DEle33_CaloId_fire ) ;
//   fChain->SetBranchAddress("trig_HLT_Ele27_WPTight_Gsf_accept"                             , &trig_Ele27_fire        ,  &b_trig_Ele27_fire         ) ;
//   fChain->SetBranchAddress("trig_HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_accept"    , &trig_Mu8_Ele23_fire    ,  &b_trig_Mu8_Ele23_fire     ) ;
//   fChain->SetBranchAddress("trig_HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_accept"   , &trig_Mu23_Ele12_fire   ,  &b_trig_Mu23_Ele12_fire    ) ;
//   fChain->SetBranchAddress("trig_HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_accept" , &trig_Mu8_Ele23_DZ_fire ,  &b_trig_Mu8_Ele23_DZ_fire  ) ;
//   fChain->SetBranchAddress("trig_HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_accept", &trig_Mu23_Ele12_DZ_fire,  &b_trig_Mu23_Ele12_DZ_fire ) ;
//   fChain->SetBranchAddress("trig_HLT_Mu30_Ele30_CaloIdL_GsfTrkIdVL_accept"                 , &trig_Mu30_Ele30_fire   ,  &b_trig_Mu30_Ele30_fire    ) ;
//   fChain->SetBranchAddress("trig_HLT_Mu33_Ele33_CaloIdL_GsfTrkIdVL_accept"                 , &trig_Mu33_Ele33_fire   ,  &b_trig_Mu33_Ele33_fire    ) ;
//   fChain->SetBranchAddress("trig_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_accept"                , &trig_Mu17_TkMu8_fire   ,  &b_trig_Mu17_TkMu8_fire    ) ;
//   fChain->SetBranchAddress("trig_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_accept"                  , &trig_Mu17_Mu8_fire     ,  &b_trig_Mu17_Mu8_fire      ) ;
//   fChain->SetBranchAddress("trig_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_accept"             , &trig_Mu17_TkMu8_DZ_fire,  &b_trig_Mu17_TkMu8_DZ_fire ) ;
//   fChain->SetBranchAddress("trig_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_accept"               , &trig_Mu17_Mu8_DZ_fire  ,  &b_trig_Mu17_Mu8_DZ_fire   ) ;
//   fChain->SetBranchAddress("trig_HLT_Mu30_TkMu11_accept"                                   , &trig_Mu30_TkMu11_fire  ,  &b_trig_Mu30_TkMu11_fire   ) ;
//   fChain->SetBranchAddress("trig_HLT_IsoMu24_accept"                                       , &trig_IsoMu24_fire      ,  &b_trig_IsoMu24_fire       ) ;
//   fChain->SetBranchAddress("trig_HLT_IsoTkMu24_accept"                                     , &trig_IsoTkMu24_fire    ,  &b_trig_IsoTkMu24_fire     ) ;
//##################################### For MET trigger###########################################################################
//   fChain->SetBranchAddress("trig_HLT_PFHT300_PFMET110_accept"                              , &trig_HLT_PFHT300_PFMET110_fire                     ,  &b_trig_HLT_PFHT300_PFMET110_fire           ) ;
//   fChain->SetBranchAddress("trig_HLT_MET200_accept"                                        , &trig_HLT_MET200_fire                               ,  &b_trig_HLT_MET200_fire                     ) ;
//   fChain->SetBranchAddress("trig_HLT_PFMET300_accept"                                      , &trig_HLT_PFMET300_fire                             ,  &b_trig_HLT_PFMET300_fire                   ) ;
//   fChain->SetBranchAddress("trig_HLT_PFMET120_PFMHT120_IDTight_accept"                     , &trig_HLT_PFMET120_PFMHT120_IDTight_fire            ,  &b_trig_HLT_PFMET120_PFMHT120_IDTight_fire  ) ;
//   fChain->SetBranchAddress("trig_HLT_PFMET170_HBHECleaned_accept"                          , &trig_HLT_PFMET170_HBHECleaned_fire                 ,  &b_trig_HLT_PFMET170_HBHECleaned_fire       ) ;
//   fChain->SetBranchAddress("trig_HLT_MET75_IsoTrk50_accept"                                , &trig_HLT_MET75_IsoTrk50_fire                       ,  &b_trig_HLT_MET75_IsoTrk50_fire             ) ;
//############################################################# For Zprime ###########################################################   
   fChain->SetBranchAddress("trig_HLT_DoubleEle33_CaloIdL_GsfTrkIdVL_hltEle33CaloIdLGsfTrkIdVLDPhiFilter_eta"          , &trig_DEle33_seed_eta     , &b_trig_DEle33_seed_eta     ) ;
   fChain->SetBranchAddress("trig_HLT_DoubleEle33_CaloIdL_GsfTrkIdVL_hltEle33CaloIdLGsfTrkIdVLDPhiFilter_phi"          , &trig_DEle33_seed_phi     , &b_trig_DEle33_seed_phi     ) ;
   fChain->SetBranchAddress("trig_HLT_DoubleEle33_CaloIdL_GsfTrkIdVL_hltDiEle33CaloIdLGsfTrkIdVLDPhiUnseededFilter_eta", &trig_DEle33_unseed_eta   , &b_trig_DEle33_unseed_eta   ) ;
   fChain->SetBranchAddress("trig_HLT_DoubleEle33_CaloIdL_GsfTrkIdVL_hltDiEle33CaloIdLGsfTrkIdVLDPhiUnseededFilter_phi", &trig_DEle33_unseed_phi   , &b_trig_DEle33_unseed_phi   ) ;

   if(fChain->GetBranchStatus("trig_HLT_DoubleEle33_CaloIdL_MW_hltEle33CaloIdLMWPMS2Filter_eta")!=false){
   fChain->SetBranchAddress("trig_HLT_DoubleEle33_CaloIdL_MW_hltEle33CaloIdLMWPMS2Filter_eta"                          , &trig_DEle33_MW_seed_eta  , &b_trig_DEle33_MW_seed_eta  ) ;
   fChain->SetBranchAddress("trig_HLT_DoubleEle33_CaloIdL_MW_hltEle33CaloIdLMWPMS2Filter_phi"                          , &trig_DEle33_MW_seed_phi  , &b_trig_DEle33_MW_seed_phi  ) ;
   }
   else{
   fChain->SetBranchAddress("trig_HLT_DoubleEle33_CaloIdL_MW_hltEG33CaloIdLMWPMS2Filter_eta"                          , &trig_DEle33_MW_seed_eta  , &b_trig_DEle33_MW_seed_eta  ) ;
   fChain->SetBranchAddress("trig_HLT_DoubleEle33_CaloIdL_MW_hltEG33CaloIdLMWPMS2Filter_phi"                          , &trig_DEle33_MW_seed_phi  , &b_trig_DEle33_MW_seed_phi  ) ;
   }

   fChain->SetBranchAddress("trig_HLT_DoubleEle33_CaloIdL_MW_hltDiEle33CaloIdLMWPMS2UnseededFilter_eta"                , &trig_DEle33_MW_unseed_eta, &b_trig_DEle33_MW_unseed_eta) ;
   fChain->SetBranchAddress("trig_HLT_DoubleEle33_CaloIdL_MW_hltDiEle33CaloIdLMWPMS2UnseededFilter_phi"                , &trig_DEle33_MW_unseed_phi, &b_trig_DEle33_MW_unseed_phi) ;

   if(fChain->GetBranchStatus("trig_HLT_DoubleEle33_CaloIdL_MW_hltEGL1SingleAndDoubleEGNonIsoOrWithEG26WithJetAndTauFilter_eta")!=false){
   fChain->SetBranchAddress("trig_HLT_DoubleEle33_CaloIdL_MW_hltEGL1SingleAndDoubleEGNonIsoOrWithEG26WithJetAndTauFilter_eta", &trig_DEle33_MW_L1_eta, &b_trig_DEle33_MW_L1_eta  ) ;
   fChain->SetBranchAddress("trig_HLT_DoubleEle33_CaloIdL_MW_hltEGL1SingleAndDoubleEGNonIsoOrWithEG26WithJetAndTauFilter_phi", &trig_DEle33_MW_L1_phi, &b_trig_DEle33_MW_L1_phi  ) ;
   fChain->SetBranchAddress("trig_HLT_DoubleEle33_CaloIdL_MW_hltEGL1SingleAndDoubleEGNonIsoOrWithEG26WithJetAndTauFilter_et" , &trig_DEle33_MW_L1_et , &b_trig_DEle33_MW_L1_et   ) ;
   }
   else if (fChain->GetBranchStatus("trig_HLT_DoubleEle33_CaloIdL_MW_hltEGL1SingleEG40OR30OR26ORDoubleEG2210OR2417ORSingleJet200Filter_eta")!=false){
   fChain->SetBranchAddress("trig_HLT_DoubleEle33_CaloIdL_MW_hltEGL1SingleEG40OR30OR26ORDoubleEG2210OR2417ORSingleJet200Filter_eta", &trig_DEle33_MW_L1_eta, &b_trig_DEle33_MW_L1_eta  ) ;
   fChain->SetBranchAddress("trig_HLT_DoubleEle33_CaloIdL_MW_hltEGL1SingleEG40OR30OR26ORDoubleEG2210OR2417ORSingleJet200Filter_phi", &trig_DEle33_MW_L1_phi, &b_trig_DEle33_MW_L1_phi  ) ;
   fChain->SetBranchAddress("trig_HLT_DoubleEle33_CaloIdL_MW_hltEGL1SingleEG40OR30OR26ORDoubleEG2210OR2417ORSingleJet200Filter_et" , &trig_DEle33_MW_L1_et , &b_trig_DEle33_MW_L1_et   ) ;
   }
   else{
   fChain->SetBranchAddress("trig_HLT_DoubleEle33_CaloIdL_MW_hltEGL1SingleEG40OR30OR26ORDoubleEG2210OR2417ORL1EGHighPtSeedsFilter_eta", &trig_DEle33_MW_L1_eta, &b_trig_DEle33_MW_L1_eta  ) ;
   fChain->SetBranchAddress("trig_HLT_DoubleEle33_CaloIdL_MW_hltEGL1SingleEG40OR30OR26ORDoubleEG2210OR2417ORL1EGHighPtSeedsFilter_phi", &trig_DEle33_MW_L1_phi, &b_trig_DEle33_MW_L1_phi  ) ;
   fChain->SetBranchAddress("trig_HLT_DoubleEle33_CaloIdL_MW_hltEGL1SingleEG40OR30OR26ORDoubleEG2210OR2417ORL1EGHighPtSeedsFilter_et" , &trig_DEle33_MW_L1_et , &b_trig_DEle33_MW_L1_et   ) ;
   }

//   fChain->SetBranchAddress("L1_pass_final" , &L1_pass_final , &b_L1_pass_final   ) ;
   fChain->SetBranchAddress("trig_HLT_DoubleEle25_CaloIdL_MW_hltEle25CaloIdLMWPMS2Filter_eta"                                , &trig_DEle25_MW_seed_eta  , &b_trig_DEle25_MW_seed_eta  ) ;
   fChain->SetBranchAddress("trig_HLT_DoubleEle25_CaloIdL_MW_hltEle25CaloIdLMWPMS2Filter_phi"                                , &trig_DEle25_MW_seed_phi  , &b_trig_DEle25_MW_seed_phi  ) ;
   fChain->SetBranchAddress("trig_HLT_DoubleEle25_CaloIdL_MW_hltDiEle25CaloIdLMWPMS2UnseededFilter_eta"                      , &trig_DEle25_MW_unseed_eta, &b_trig_DEle25_MW_unseed_eta) ;
   fChain->SetBranchAddress("trig_HLT_DoubleEle25_CaloIdL_MW_hltDiEle25CaloIdLMWPMS2UnseededFilter_phi"                      , &trig_DEle25_MW_unseed_phi, &b_trig_DEle25_MW_unseed_phi) ;
   fChain->SetBranchAddress("trig_HLT_DoubleEle25_CaloIdL_MW_hltEGL1SingleAndDoubleEGNonIsoOrWithEG26WithJetAndTauFilter_eta", &trig_DEle25_MW_L1_eta    , &b_trig_DEle25_MW_L1_eta    ) ;
   fChain->SetBranchAddress("trig_HLT_DoubleEle25_CaloIdL_MW_hltEGL1SingleAndDoubleEGNonIsoOrWithEG26WithJetAndTauFilter_phi", &trig_DEle25_MW_L1_phi    , &b_trig_DEle25_MW_L1_phi    ) ;
   fChain->SetBranchAddress("trig_HLT_DoubleEle25_CaloIdL_MW_hltEGL1SingleAndDoubleEGNonIsoOrWithEG26WithJetAndTauFilter_et" , &trig_DEle25_MW_L1_et     , &b_trig_DEle25_MW_L1_et     ) ;
   Notify();
}

Bool_t reskim::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void reskim::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t reskim::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
#endif // #ifdef reskim_cxx
