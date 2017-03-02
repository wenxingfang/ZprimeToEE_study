//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Sun Dec  6 18:36:33 2015 by ROOT version 6.02/05
// from TTree IIHEAnalysis/IIHEAnalysis
// found on file: ../../samples/RunIISpring15DR74/RunIISpring15DR74_ZToEE_50_120_25ns/outfile_1.root
//////////////////////////////////////////////////////////

#ifndef reskim_FR_1F_h
#define reskim_FR_1F_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

// Header file for the classes stored in the TTree if any.
#include "vector"

#include <iostream>

class reskim_FR_1F {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

// Fixed size dimensions of array or collections stored in the TTree if any.

   // Declaration of leaf types
   UInt_t          ev_event;
   UInt_t          ev_run;
   UInt_t          ev_luminosityBlock;
   UInt_t          ev_time;
   UInt_t          ev_time_unixTime;
   UInt_t          ev_time_microsecondOffset;
   Float_t         ev_fixedGridRhoAll;
   Float_t         ev_fixedGridRhoFastjetAll;
   Float_t         ev_rho_kt6PFJetsForIsolation;
   UInt_t          mc_n;
   Float_t         mc_pdfvariables_weight;
   Float_t         mc_w;
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
//   vector<int>     *pv_isValid;
   vector<bool>     *pv_isValid;
   vector<float>   *pv_normalizedChi2;
   vector<int>     *pv_ndof;
   vector<int>     *pv_nTracks;
   vector<int>     *pv_totTrackSize;
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
   vector<bool>    *gsf_ecaldrivenSeed;
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
////////////////////////////////////////////

   vector<vector<int> > *gsf_hitsinfo;
   vector<float>   *gsf_pixelMatch_dPhi1;
   vector<float>   *gsf_pixelMatch_dPhi2;
   vector<float>   *gsf_pixelMatch_dRz1;
   vector<float>   *gsf_pixelMatch_dRz2;
   vector<int>     *gsf_pixelMatch_subDetector1;
   vector<int>     *gsf_pixelMatch_subDetector2;
   vector<float>   *gsf_mc_bestDR;
   vector<int>     *gsf_mc_index;
   vector<float>   *gsf_mc_ERatio;
   Float_t         MET_caloMet_et;
   Float_t         MET_caloMet_phi;
   Float_t         MET_pfMet_et;
   Float_t         MET_pfMet_phi;
   vector<float>   *HEEP_eseffsixix;
   vector<float>   *HEEP_eseffsiyiy;
   vector<float>   *HEEP_eseffsirir;
   vector<float>   *HEEP_preshowerEnergy;
   vector<float>   *HEEP_e1x3;
   vector<float>   *HEEP_eMax;
   vector<float>   *HEEP_e5x5;
   vector<float>   *HEEP_e2x5Right;
   vector<float>   *HEEP_e2x5Left;
   vector<float>   *HEEP_e2x5Top;
   vector<float>   *HEEP_e2x5Bottom;
   vector<float>   *HEEP_eRight;
   vector<float>   *HEEP_eLeft;
   vector<float>   *HEEP_eTop;
   vector<float>   *HEEP_eBottom;
   vector<float>   *HEEP_basicClusterSeedTime;
   vector<int>     *EBHits_rawId;
   vector<int>     *EBHits_iRechit;
   vector<float>   *EBHits_energy;
   vector<int>     *EBHits_ieta;
   vector<int>     *EBHits_iphi;
   vector<int>     *EBHits_RecoFlag;
   vector<bool>     *EBHits_kSaturated;
   vector<bool>     *EBHits_kLeadingEdgeRecovered;
   vector<bool>     *EBHits_kNeighboursRecovered;
   vector<bool>     *EBHits_kWeird;
   vector<int>     *EEHits_rawId;
   vector<int>     *EEHits_iRechit;
   vector<float>   *EEHits_energy;
   vector<int>     *EEHits_ieta;
   vector<int>     *EEHits_iphi;
   vector<int>     *EEHits_RecoFlag;
   vector<bool>     *EEHits_kSaturated;
   vector<bool>     *EEHits_kLeadingEdgeRecovered;
   vector<bool>     *EEHits_kNeighboursRecovered;
   vector<bool>     *EEHits_kWeird;
   vector<vector<float> > *HEEP_crystal_energy;
   vector<vector<float> > *HEEP_crystal_eta;
   vector<vector<float> > *HEEP_eshitsixix;
   vector<vector<float> > *HEEP_eshitsiyiy;
   vector<vector<int> > *HEEP_crystal_ietaorix;
   vector<vector<int> > *HEEP_crystal_iphioriy;
   vector<int>     *HEEP_cutflow60_Et;
   Int_t           HEEP_cutflow60_Et_n;
   Int_t           HEEP_cutflow60_Et_nCumulative;
   vector<float>   *HEEP_cutflow60_Et_value;
   vector<int>     *HEEP_cutflow60_eta;
   Int_t           HEEP_cutflow60_eta_n;
   Int_t           HEEP_cutflow60_eta_nCumulative;
   vector<float>   *HEEP_cutflow60_eta_value;
   vector<int>     *HEEP_cutflow60_acceptance;
   Int_t           HEEP_cutflow60_acceptance_n;
   vector<int>     *HEEP_cutflow60_EcalDriven;
   Int_t           HEEP_cutflow60_EcalDriven_n;
   Int_t           HEEP_cutflow60_EcalDriven_nCumulative;
   vector<float>   *HEEP_cutflow60_EcalDriven_value;
   vector<int>     *HEEP_cutflow60_dEtaIn;
   Int_t           HEEP_cutflow60_dEtaIn_n;
   Int_t           HEEP_cutflow60_dEtaIn_nCumulative;
   vector<float>   *HEEP_cutflow60_dEtaIn_value;
   vector<int>     *HEEP_cutflow60_dPhiIn;
   Int_t           HEEP_cutflow60_dPhiIn_n;
   Int_t           HEEP_cutflow60_dPhiIn_nCumulative;
   vector<float>   *HEEP_cutflow60_dPhiIn_value;
   vector<int>     *HEEP_cutflow60_HOverE;
   Int_t           HEEP_cutflow60_HOverE_n;
   Int_t           HEEP_cutflow60_HOverE_nCumulative;
   vector<float>   *HEEP_cutflow60_HOverE_value;
   vector<int>     *HEEP_cutflow60_SigmaIetaIeta;
   Int_t           HEEP_cutflow60_SigmaIetaIeta_n;
   Int_t           HEEP_cutflow60_SigmaIetaIeta_nCumulative;
   vector<float>   *HEEP_cutflow60_SigmaIetaIeta_value;
   vector<int>     *HEEP_cutflow60_E1x5OverE5x5;
   Int_t           HEEP_cutflow60_E1x5OverE5x5_n;
   Int_t           HEEP_cutflow60_E1x5OverE5x5_nCumulative;
   vector<float>   *HEEP_cutflow60_E1x5OverE5x5_value;
   vector<int>     *HEEP_cutflow60_E2x5OverE5x5;
   Int_t           HEEP_cutflow60_E2x5OverE5x5_n;
   Int_t           HEEP_cutflow60_E2x5OverE5x5_nCumulative;
   vector<float>   *HEEP_cutflow60_E2x5OverE5x5_value;
   vector<int>     *HEEP_cutflow60_missingHits;
   Int_t           HEEP_cutflow60_missingHits_n;
   Int_t           HEEP_cutflow60_missingHits_nCumulative;
   vector<float>   *HEEP_cutflow60_missingHits_value;
   vector<int>     *HEEP_cutflow60_dxyFirstPV;
   Int_t           HEEP_cutflow60_dxyFirstPV_n;
   Int_t           HEEP_cutflow60_dxyFirstPV_nCumulative;
   vector<float>   *HEEP_cutflow60_dxyFirstPV_value;
   vector<int>     *HEEP_cutflow60_ID;
   Int_t           HEEP_cutflow60_ID_n;
   vector<int>     *HEEP_cutflow60_isolEMHadDepth1;
   Int_t           HEEP_cutflow60_isolEMHadDepth1_n;
   Int_t           HEEP_cutflow60_isolEMHadDepth1_nCumulative;
   vector<float>   *HEEP_cutflow60_isolEMHadDepth1_value;
   vector<int>     *HEEP_cutflow60_IsolPtTrks;
   Int_t           HEEP_cutflow60_IsolPtTrks_n;
   Int_t           HEEP_cutflow60_IsolPtTrks_nCumulative;
   vector<float>   *HEEP_cutflow60_IsolPtTrks_value;
   vector<int>     *HEEP_cutflow60_isolation;
   Int_t           HEEP_cutflow60_isolation_n;
   vector<int>     *HEEP_cutflow60_total;
   Int_t           HEEP_cutflow60_total_n;
   Int_t           Zee_n;
   vector<float>   *Zee_mass;
   vector<float>   *Zee_mass_HEEP;
   vector<int>     *Zee_i1;
   vector<int>     *Zee_i2;
   Int_t           Zee_highestMass;
   Int_t           Zmm_n;
   vector<float>   *Zmm_mass;
   vector<int>     *Zmm_i1;
   vector<int>     *Zmm_i2;
   Int_t           Zmm_highestMass;
   Int_t           Zem_n;
   vector<float>   *Zem_mass;
   vector<float>   *Zem_mass_HEEP;
   vector<int>     *Zem_i1;
   vector<int>     *Zem_i2;
   Int_t           Zem_highestMass;
   
   Int_t trig_DE_fire ;
   Int_t trig_fire_v1 ;
   Int_t trig_fire_v2 ;
   vector<float> *trig_eta_v1 ;
   vector<float> *trig_phi_v1 ;
   vector<float> *trig_eta_v2 ;
   vector<float> *trig_phi_v2 ;
   vector<float> *trig_DE_eta ;
   vector<float> *trig_DE_phi ;
   vector<float> *trig_DE_unseed_eta ;
   vector<float> *trig_DE_unseed_phi ;
   vector<float> *trig_DE_L1_eta_v1 ;
   vector<float> *trig_DE_L1_phi_v1 ;
   vector<float> *trig_DE_L1_eta_v2 ;
   vector<float> *trig_DE_L1_phi_v2 ;
   
   Float_t mc_w_sign ;

   // List of branches
   TBranch        *b_ev_event;   //!
   TBranch        *b_ev_run;   //!
   TBranch        *b_ev_luminosityBlock;   //!
   TBranch        *b_ev_time;   //!
   TBranch        *b_ev_time_unixTime;   //!
   TBranch        *b_ev_time_microsecondOffset;   //!
   TBranch        *b_ev_fixedGridRhoAll;   //!
   TBranch        *b_ev_fixedGridRhoFastjetAll;   //!
   TBranch        *b_ev_rho_kt6PFJetsForIsolation;   //!
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
///////////////////////////////////////

   TBranch        *b_gsf_hitsinfo;   //!
   TBranch        *b_gsf_pixelMatch_dPhi1;   //!
   TBranch        *b_gsf_pixelMatch_dPhi2;   //!
   TBranch        *b_gsf_pixelMatch_dRz1;   //!
   TBranch        *b_gsf_pixelMatch_dRz2;   //!
   TBranch        *b_gsf_pixelMatch_subDetector1;   //!
   TBranch        *b_gsf_pixelMatch_subDetector2;   //!
   TBranch        *b_gsf_mc_bestDR;   //!
   TBranch        *b_gsf_mc_index;   //!
   TBranch        *b_gsf_mc_ERatio;   //!
   TBranch        *b_MET_caloMet_et;   //!
   TBranch        *b_MET_caloMet_phi;   //!
   TBranch        *b_MET_pfMet_et;   //!
   TBranch        *b_MET_pfMet_phi;   //!
   TBranch        *b_HEEP_eseffsixix;   //!
   TBranch        *b_HEEP_eseffsiyiy;   //!
   TBranch        *b_HEEP_eseffsirir;   //!
   TBranch        *b_HEEP_preshowerEnergy;   //!
   TBranch        *b_HEEP_e1x3;   //!
   TBranch        *b_HEEP_eMax;   //!
   TBranch        *b_HEEP_e5x5;   //!
   TBranch        *b_HEEP_e2x5Right;   //!
   TBranch        *b_HEEP_e2x5Left;   //!
   TBranch        *b_HEEP_e2x5Top;   //!
   TBranch        *b_HEEP_e2x5Bottom;   //!
   TBranch        *b_HEEP_eRight;   //!
   TBranch        *b_HEEP_eLeft;   //!
   TBranch        *b_HEEP_eTop;   //!
   TBranch        *b_HEEP_eBottom;   //!
   TBranch        *b_HEEP_basicClusterSeedTime;   //!
   TBranch        *b_EBHits_rawId;   //!
   TBranch        *b_EBHits_iRechit;   //!
   TBranch        *b_EBHits_energy;   //!
   TBranch        *b_EBHits_ieta;   //!
   TBranch        *b_EBHits_iphi;   //!
   TBranch        *b_EBHits_RecoFlag;   //!
   TBranch        *b_EBHits_kSaturated;   //!
   TBranch        *b_EBHits_kLeadingEdgeRecovered;   //!
   TBranch        *b_EBHits_kNeighboursRecovered;   //!
   TBranch        *b_EBHits_kWeird;   //!
   TBranch        *b_EEHits_rawId;   //!
   TBranch        *b_EEHits_iRechit;   //!
   TBranch        *b_EEHits_energy;   //!
   TBranch        *b_EEHits_ieta;   //!
   TBranch        *b_EEHits_iphi;   //!
   TBranch        *b_EEHits_RecoFlag;   //!
   TBranch        *b_EEHits_kSaturated;   //!
   TBranch        *b_EEHits_kLeadingEdgeRecovered;   //!
   TBranch        *b_EEHits_kNeighboursRecovered;   //!
   TBranch        *b_EEHits_kWeird;   //!
   TBranch        *b_HEEP_crystal_energy;   //!
   TBranch        *b_HEEP_crystal_eta;   //!
   TBranch        *b_HEEP_eshitsixix;   //!
   TBranch        *b_HEEP_eshitsiyiy;   //!
   TBranch        *b_HEEP_crystal_ietaorix;   //!
   TBranch        *b_HEEP_crystal_iphioriy;   //!
   TBranch        *b_HEEP_cutflow60_Et;   //!
   TBranch        *b_HEEP_cutflow60_Et_n;   //!
   TBranch        *b_HEEP_cutflow60_Et_nCumulative;   //!
   TBranch        *b_HEEP_cutflow60_Et_value;   //!
   TBranch        *b_HEEP_cutflow60_eta;   //!
   TBranch        *b_HEEP_cutflow60_eta_n;   //!
   TBranch        *b_HEEP_cutflow60_eta_nCumulative;   //!
   TBranch        *b_HEEP_cutflow60_eta_value;   //!
   TBranch        *b_HEEP_cutflow60_acceptance;   //!
   TBranch        *b_HEEP_cutflow60_acceptance_n;   //!
   TBranch        *b_HEEP_cutflow60_EcalDriven;   //!
   TBranch        *b_HEEP_cutflow60_EcalDriven_n;   //!
   TBranch        *b_HEEP_cutflow60_EcalDriven_nCumulative;   //!
   TBranch        *b_HEEP_cutflow60_EcalDriven_value;   //!
   TBranch        *b_HEEP_cutflow60_dEtaIn;   //!
   TBranch        *b_HEEP_cutflow60_dEtaIn_n;   //!
   TBranch        *b_HEEP_cutflow60_dEtaIn_nCumulative;   //!
   TBranch        *b_HEEP_cutflow60_dEtaIn_value;   //!
   TBranch        *b_HEEP_cutflow60_dPhiIn;   //!
   TBranch        *b_HEEP_cutflow60_dPhiIn_n;   //!
   TBranch        *b_HEEP_cutflow60_dPhiIn_nCumulative;   //!
   TBranch        *b_HEEP_cutflow60_dPhiIn_value;   //!
   TBranch        *b_HEEP_cutflow60_HOverE;   //!
   TBranch        *b_HEEP_cutflow60_HOverE_n;   //!
   TBranch        *b_HEEP_cutflow60_HOverE_nCumulative;   //!
   TBranch        *b_HEEP_cutflow60_HOverE_value;   //!
   TBranch        *b_HEEP_cutflow60_SigmaIetaIeta;   //!
   TBranch        *b_HEEP_cutflow60_SigmaIetaIeta_n;   //!
   TBranch        *b_HEEP_cutflow60_SigmaIetaIeta_nCumulative;   //!
   TBranch        *b_HEEP_cutflow60_SigmaIetaIeta_value;   //!
   TBranch        *b_HEEP_cutflow60_E1x5OverE5x5;   //!
   TBranch        *b_HEEP_cutflow60_E1x5OverE5x5_n;   //!
   TBranch        *b_HEEP_cutflow60_E1x5OverE5x5_nCumulative;   //!
   TBranch        *b_HEEP_cutflow60_E1x5OverE5x5_value;   //!
   TBranch        *b_HEEP_cutflow60_E2x5OverE5x5;   //!
   TBranch        *b_HEEP_cutflow60_E2x5OverE5x5_n;   //!
   TBranch        *b_HEEP_cutflow60_E2x5OverE5x5_nCumulative;   //!
   TBranch        *b_HEEP_cutflow60_E2x5OverE5x5_value;   //!
   TBranch        *b_HEEP_cutflow60_missingHits;   //!
   TBranch        *b_HEEP_cutflow60_missingHits_n;   //!
   TBranch        *b_HEEP_cutflow60_missingHits_nCumulative;   //!
   TBranch        *b_HEEP_cutflow60_missingHits_value;   //!
   TBranch        *b_HEEP_cutflow60_dxyFirstPV;   //!
   TBranch        *b_HEEP_cutflow60_dxyFirstPV_n;   //!
   TBranch        *b_HEEP_cutflow60_dxyFirstPV_nCumulative;   //!
   TBranch        *b_HEEP_cutflow60_dxyFirstPV_value;   //!
   TBranch        *b_HEEP_cutflow60_ID;   //!
   TBranch        *b_HEEP_cutflow60_ID_n;   //!
   TBranch        *b_HEEP_cutflow60_isolEMHadDepth1;   //!
   TBranch        *b_HEEP_cutflow60_isolEMHadDepth1_n;   //!
   TBranch        *b_HEEP_cutflow60_isolEMHadDepth1_nCumulative;   //!
   TBranch        *b_HEEP_cutflow60_isolEMHadDepth1_value;   //!
   TBranch        *b_HEEP_cutflow60_IsolPtTrks;   //!
   TBranch        *b_HEEP_cutflow60_IsolPtTrks_n;   //!
   TBranch        *b_HEEP_cutflow60_IsolPtTrks_nCumulative;   //!
   TBranch        *b_HEEP_cutflow60_IsolPtTrks_value;   //!
   TBranch        *b_HEEP_cutflow60_isolation;   //!
   TBranch        *b_HEEP_cutflow60_isolation_n;   //!
   TBranch        *b_HEEP_cutflow60_total;   //!
   TBranch        *b_HEEP_cutflow60_total_n;   //!
   TBranch        *b_Zee_n;   //!
   TBranch        *b_Zee_mass;   //!
   TBranch        *b_Zee_mass_HEEP;   //!
   TBranch        *b_Zee_i1;   //!
   TBranch        *b_Zee_i2;   //!
   TBranch        *b_Zee_highestMass;   //!
   TBranch        *b_Zmm_n;   //!
   TBranch        *b_Zmm_mass;   //!
   TBranch        *b_Zmm_i1;   //!
   TBranch        *b_Zmm_i2;   //!
   TBranch        *b_Zmm_highestMass;   //!
   TBranch        *b_Zem_n;   //!
   TBranch        *b_Zem_mass;   //!
   TBranch        *b_Zem_mass_HEEP;   //!
   TBranch        *b_Zem_i1;   //!
   TBranch        *b_Zem_i2;   //!
   TBranch        *b_Zem_highestMass;   //!
   
   TBranch        *b_mc_w_sign;   //!
   
   TBranch *b_trig_DE_fire ;
   TBranch *b_trig_DE_eta ;
   TBranch *b_trig_DE_phi ;
   TBranch *b_trig_DE_unseed_eta ;
   TBranch *b_trig_DE_unseed_phi ;
   TBranch *b_trig_DE_L1_eta_v1 ;
   TBranch *b_trig_DE_L1_phi_v1 ;
   TBranch *b_trig_DE_L1_eta_v2 ;
   TBranch *b_trig_DE_L1_phi_v2 ;
   TBranch *b_trig_fire_v1 ;
   TBranch *b_trig_fire_v2 ;
   TBranch *b_trig_eta_v1  ;
   TBranch *b_trig_phi_v1  ;
   TBranch *b_trig_eta_v2  ;
   TBranch *b_trig_phi_v2  ;

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

   reskim_FR_1F(TTree *tree=0, bool isData_in=false, bool isTTbar_in=false, bool isZToTT_in=false, bool isWW_in=false, string triggerVersion_in="", int Run_low_in=0, int Run_high_in=999999);
   virtual ~reskim_FR_1F();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop(TString);
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
};

#endif

#ifdef reskim_FR_1F_cxx
reskim_FR_1F::reskim_FR_1F(TTree *tree, bool isData_in, bool isTTbar_in,  bool isZToTT_in, bool isWW_in, string triggerVersion_in, int Run_low_in, int Run_high_in) :
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

reskim_FR_1F::~reskim_FR_1F()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t reskim_FR_1F::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t reskim_FR_1F::LoadTree(Long64_t entry)
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

void reskim_FR_1F::Init(TTree *tree)
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

/////////////////////
   gsf_hitsinfo = 0;
   gsf_pixelMatch_dPhi1 = 0;
   gsf_pixelMatch_dPhi2 = 0;
   gsf_pixelMatch_dRz1 = 0;
   gsf_pixelMatch_dRz2 = 0;
   gsf_pixelMatch_subDetector1 = 0;
   gsf_pixelMatch_subDetector2 = 0;
   gsf_mc_bestDR = 0;
   gsf_mc_index = 0;
   gsf_mc_ERatio = 0;
   HEEP_eseffsixix = 0;
   HEEP_eseffsiyiy = 0;
   HEEP_eseffsirir = 0;
   HEEP_preshowerEnergy = 0;
   HEEP_e1x3 = 0;
   HEEP_eMax = 0;
   HEEP_e5x5 = 0;
   HEEP_e2x5Right = 0;
   HEEP_e2x5Left = 0;
   HEEP_e2x5Top = 0;
   HEEP_e2x5Bottom = 0;
   HEEP_eRight = 0;
   HEEP_eLeft = 0;
   HEEP_eTop = 0;
   HEEP_eBottom = 0;
   HEEP_basicClusterSeedTime = 0;
   EBHits_rawId = 0;
   EBHits_iRechit = 0;
   EBHits_energy = 0;
   EBHits_ieta = 0;
   EBHits_iphi = 0;
   EBHits_RecoFlag = 0;
   EBHits_kSaturated = 0;
   EBHits_kLeadingEdgeRecovered = 0;
   EBHits_kNeighboursRecovered = 0;
   EBHits_kWeird = 0;
   EEHits_rawId = 0;
   EEHits_iRechit = 0;
   EEHits_energy = 0;
   EEHits_ieta = 0;
   EEHits_iphi = 0;
   EEHits_RecoFlag = 0;
   EEHits_kSaturated = 0;
   EEHits_kLeadingEdgeRecovered = 0;
   EEHits_kNeighboursRecovered = 0;
   EEHits_kWeird = 0;
   HEEP_crystal_energy = 0;
   HEEP_crystal_eta = 0;
   HEEP_eshitsixix = 0;
   HEEP_eshitsiyiy = 0;
   HEEP_crystal_ietaorix = 0;
   HEEP_crystal_iphioriy = 0;
   HEEP_cutflow60_Et = 0;
   HEEP_cutflow60_Et_value = 0;
   HEEP_cutflow60_eta = 0;
   HEEP_cutflow60_eta_value = 0;
   HEEP_cutflow60_acceptance = 0;
   HEEP_cutflow60_EcalDriven = 0;
   HEEP_cutflow60_EcalDriven_value = 0;
   HEEP_cutflow60_dEtaIn = 0;
   HEEP_cutflow60_dEtaIn_value = 0;
   HEEP_cutflow60_dPhiIn = 0;
   HEEP_cutflow60_dPhiIn_value = 0;
   HEEP_cutflow60_HOverE = 0;
   HEEP_cutflow60_HOverE_value = 0;
   HEEP_cutflow60_SigmaIetaIeta = 0;
   HEEP_cutflow60_SigmaIetaIeta_value = 0;
   HEEP_cutflow60_E1x5OverE5x5 = 0;
   HEEP_cutflow60_E1x5OverE5x5_value = 0;
   HEEP_cutflow60_E2x5OverE5x5 = 0;
   HEEP_cutflow60_E2x5OverE5x5_value = 0;
   HEEP_cutflow60_missingHits = 0;
   HEEP_cutflow60_missingHits_value = 0;
   HEEP_cutflow60_dxyFirstPV = 0;
   HEEP_cutflow60_dxyFirstPV_value = 0;
   HEEP_cutflow60_ID = 0;
   HEEP_cutflow60_isolEMHadDepth1 = 0;
   HEEP_cutflow60_isolEMHadDepth1_value = 0;
   HEEP_cutflow60_IsolPtTrks = 0;
   HEEP_cutflow60_IsolPtTrks_value = 0;
   HEEP_cutflow60_isolation = 0;
   HEEP_cutflow60_total = 0;
   Zee_mass = 0;
   Zee_mass_HEEP = 0;
   Zee_i1 = 0;
   Zee_i2 = 0;
   Zmm_mass = 0;
   Zmm_i1 = 0;
   Zmm_i2 = 0;
   Zem_mass = 0;
   Zem_mass_HEEP = 0;
   Zem_i1 = 0;
   Zem_i2 = 0;
   
   trig_eta_v1 = 0 ;
   trig_phi_v1 = 0 ;
   trig_eta_v2 = 0 ;
   trig_phi_v2 = 0 ;
   trig_DE_eta = 0 ;
   trig_DE_phi = 0 ;
   trig_DE_unseed_eta = 0 ;
   trig_DE_unseed_phi = 0 ;
   trig_DE_L1_eta_v1 = 0 ;
   trig_DE_L1_phi_v1 = 0 ;
   trig_DE_L1_eta_v2 = 0 ;
   trig_DE_L1_phi_v2 = 0 ;
   
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
//   fChain->SetBranchAddress("ev_rho_kt6PFJetsForIsolation", &ev_rho_kt6PFJetsForIsolation, &b_ev_rho_kt6PFJetsForIsolation);#MinAOD
   if(isData==false){
       fChain->SetBranchAddress("mc_n", &mc_n, &b_mc_n);
//       fChain->SetBranchAddress("mc_pdfvariables_weight", &mc_pdfvariables_weight, &b_mc_pdfvariables_weight);
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
   }
   fChain->SetBranchAddress("pv_n", &pv_n, &b_pv_n);
   fChain->SetBranchAddress("pv_x", &pv_x, &b_pv_x);
   fChain->SetBranchAddress("pv_y", &pv_y, &b_pv_y);
   fChain->SetBranchAddress("pv_z", &pv_z, &b_pv_z);
//   fChain->SetBranchAddress("pv_isValid", &pv_isValid, &b_pv_isValid);
//   fChain->SetBranchAddress("pv_normalizedChi2", &pv_normalizedChi2, &b_pv_normalizedChi2);
//   fChain->SetBranchAddress("pv_ndof", &pv_ndof, &b_pv_ndof);
//   fChain->SetBranchAddress("pv_nTracks", &pv_nTracks, &b_pv_nTracks);
//   fChain->SetBranchAddress("pv_totTrackSize", &pv_totTrackSize, &b_pv_totTrackSize);
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
   fChain->SetBranchAddress("gsf_superClusterEta", &gsf_superClusterEta, &b_gsf_superClusterEta);
   fChain->SetBranchAddress("gsf_superClusterEnergy", &gsf_superClusterEnergy, &b_gsf_superClusterEnergy);
   fChain->SetBranchAddress("gsf_caloEnergy", &gsf_caloEnergy, &b_gsf_caloEnergy);
   fChain->SetBranchAddress("gsf_deltaEtaSuperClusterTrackAtVtx", &gsf_deltaEtaSuperClusterTrackAtVtx, &b_gsf_deltaEtaSuperClusterTrackAtVtx);
   fChain->SetBranchAddress("gsf_deltaPhiSuperClusterTrackAtVtx", &gsf_deltaPhiSuperClusterTrackAtVtx, &b_gsf_deltaPhiSuperClusterTrackAtVtx);
   fChain->SetBranchAddress("gsf_hadronicOverEm", &gsf_hadronicOverEm, &b_gsf_hadronicOverEm);
   fChain->SetBranchAddress("gsf_hcalDepth1OverEcal", &gsf_hcalDepth1OverEcal, &b_gsf_hcalDepth1OverEcal);
   fChain->SetBranchAddress("gsf_hcalDepth2OverEcal", &gsf_hcalDepth2OverEcal, &b_gsf_hcalDepth2OverEcal);
   fChain->SetBranchAddress("gsf_dr03TkSumPt", &gsf_dr03TkSumPt, &b_gsf_dr03TkSumPt);
   fChain->SetBranchAddress("gsf_dr03TkSumPtHEEP7", &gsf_dr03TkSumPtHEEP7, &b_gsf_dr03TkSumPtHEEP7);
   fChain->SetBranchAddress("gsf_dr03EcalRecHitSumEt", &gsf_dr03EcalRecHitSumEt, &b_gsf_dr03EcalRecHitSumEt);
   fChain->SetBranchAddress("gsf_dr03HcalDepth1TowerSumEt", &gsf_dr03HcalDepth1TowerSumEt, &b_gsf_dr03HcalDepth1TowerSumEt);
   fChain->SetBranchAddress("gsf_dr03HcalDepth2TowerSumEt", &gsf_dr03HcalDepth2TowerSumEt, &b_gsf_dr03HcalDepth2TowerSumEt);
   fChain->SetBranchAddress("gsf_charge", &gsf_charge, &b_gsf_charge);
   fChain->SetBranchAddress("gsf_sigmaIetaIeta", &gsf_sigmaIetaIeta, &b_gsf_sigmaIetaIeta);
   fChain->SetBranchAddress("gsf_ecaldrivenSeed", &gsf_ecaldrivenSeed, &b_gsf_ecaldrivenSeed);
   fChain->SetBranchAddress("gsf_trackerdrivenSeed", &gsf_trackerdrivenSeed, &b_gsf_trackerdrivenSeed);
//   fChain->SetBranchAddress("gsf_isEB", &gsf_isEB, &b_gsf_isEB);
//   fChain->SetBranchAddress("gsf_isEE", &gsf_isEE, &b_gsf_isEE);
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
   fChain->SetBranchAddress("gsf_sc_seed_ieta",           &gsf_sc_seed_ieta, &b_gsf_sc_seed_ieta);
   fChain->SetBranchAddress("gsf_sc_seed_iphi",           &gsf_sc_seed_iphi, &b_gsf_sc_seed_iphi);
   fChain->SetBranchAddress("gsf_sc_rawEnergy",            &gsf_sc_rawEnergy, &b_gsf_sc_rawEnergy);
   fChain->SetBranchAddress("gsf_sc_preshowerEnergy",      &gsf_sc_preshowerEnergy, &b_gsf_sc_preshowerEnergy);
   fChain->SetBranchAddress("gsf_sc_lazyTools_e2x5Right",  &gsf_sc_lazyTools_e2x5Right, &b_gsf_sc_lazyTools_e2x5Right);
   fChain->SetBranchAddress("gsf_sc_lazyTools_e2x5Left",   &gsf_sc_lazyTools_e2x5Left, &b_gsf_sc_lazyTools_e2x5Left);
   fChain->SetBranchAddress("gsf_sc_lazyTools_e2x5Top",    &gsf_sc_lazyTools_e2x5Top, &b_gsf_sc_lazyTools_e2x5Top);
   fChain->SetBranchAddress("gsf_sc_lazyTools_e2x5Bottom", &gsf_sc_lazyTools_e2x5Bottom, &b_gsf_sc_lazyTools_e2x5Bottom);
   fChain->SetBranchAddress("gsf_sc_eta",                  &gsf_sc_eta, &b_gsf_sc_eta);
   fChain->SetBranchAddress("gsf_sc_phi",                  &gsf_sc_phi, &b_gsf_sc_phi);
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
//################################################################################################

   fChain->SetBranchAddress("gsf_hitsinfo", &gsf_hitsinfo, &b_gsf_hitsinfo);
   fChain->SetBranchAddress("gsf_pixelMatch_dPhi1", &gsf_pixelMatch_dPhi1, &b_gsf_pixelMatch_dPhi1);
   fChain->SetBranchAddress("gsf_pixelMatch_dPhi2", &gsf_pixelMatch_dPhi2, &b_gsf_pixelMatch_dPhi2);
   fChain->SetBranchAddress("gsf_pixelMatch_dRz1", &gsf_pixelMatch_dRz1, &b_gsf_pixelMatch_dRz1);
   fChain->SetBranchAddress("gsf_pixelMatch_dRz2", &gsf_pixelMatch_dRz2, &b_gsf_pixelMatch_dRz2);
   fChain->SetBranchAddress("gsf_pixelMatch_subDetector1", &gsf_pixelMatch_subDetector1, &b_gsf_pixelMatch_subDetector1);
   fChain->SetBranchAddress("gsf_pixelMatch_subDetector2", &gsf_pixelMatch_subDetector2, &b_gsf_pixelMatch_subDetector2);
   fChain->SetBranchAddress("gsf_mc_bestDR", &gsf_mc_bestDR, &b_gsf_mc_bestDR);
   fChain->SetBranchAddress("gsf_mc_index", &gsf_mc_index, &b_gsf_mc_index);
   fChain->SetBranchAddress("gsf_mc_ERatio", &gsf_mc_ERatio, &b_gsf_mc_ERatio);
//   fChain->SetBranchAddress("MET_caloMet_et", &MET_caloMet_et, &b_MET_caloMet_et);#MinAOD
//   fChain->SetBranchAddress("MET_caloMet_phi", &MET_caloMet_phi, &b_MET_caloMet_phi);#MinAOD
   fChain->SetBranchAddress("MET_pfMet_et", &MET_pfMet_et, &b_MET_pfMet_et);
//   fChain->SetBranchAddress("MET_pfMet_phi", &MET_pfMet_phi, &b_MET_pfMet_phi);#MinAOD
//   fChain->SetBranchAddress("HEEP_eseffsixix", &HEEP_eseffsixix, &b_HEEP_eseffsixix);
//   fChain->SetBranchAddress("HEEP_eseffsiyiy", &HEEP_eseffsiyiy, &b_HEEP_eseffsiyiy);
//   fChain->SetBranchAddress("HEEP_eseffsirir", &HEEP_eseffsirir, &b_HEEP_eseffsirir);
//   fChain->SetBranchAddress("HEEP_preshowerEnergy", &HEEP_preshowerEnergy, &b_HEEP_preshowerEnergy);
//   fChain->SetBranchAddress("HEEP_e1x3", &HEEP_e1x3, &b_HEEP_e1x3);
//   fChain->SetBranchAddress("HEEP_eMax", &HEEP_eMax, &b_HEEP_eMax);
//   fChain->SetBranchAddress("HEEP_e5x5", &HEEP_e5x5, &b_HEEP_e5x5);
//   fChain->SetBranchAddress("HEEP_e2x5Right", &HEEP_e2x5Right, &b_HEEP_e2x5Right);
//   fChain->SetBranchAddress("HEEP_e2x5Left", &HEEP_e2x5Left, &b_HEEP_e2x5Left);
//   fChain->SetBranchAddress("HEEP_e2x5Top", &HEEP_e2x5Top, &b_HEEP_e2x5Top);
//   fChain->SetBranchAddress("HEEP_e2x5Bottom", &HEEP_e2x5Bottom, &b_HEEP_e2x5Bottom);
//   fChain->SetBranchAddress("HEEP_eRight", &HEEP_eRight, &b_HEEP_eRight);
//   fChain->SetBranchAddress("HEEP_eLeft", &HEEP_eLeft, &b_HEEP_eLeft);
//   fChain->SetBranchAddress("HEEP_eTop", &HEEP_eTop, &b_HEEP_eTop);
//   fChain->SetBranchAddress("HEEP_eBottom", &HEEP_eBottom, &b_HEEP_eBottom);
//   fChain->SetBranchAddress("HEEP_basicClusterSeedTime", &HEEP_basicClusterSeedTime, &b_HEEP_basicClusterSeedTime);
//   fChain->SetBranchAddress("EBHits_rawId", &EBHits_rawId, &b_EBHits_rawId);
//   fChain->SetBranchAddress("EBHits_iRechit", &EBHits_iRechit, &b_EBHits_iRechit);
//   fChain->SetBranchAddress("EBHits_energy", &EBHits_energy, &b_EBHits_energy);
//   fChain->SetBranchAddress("EBHits_ieta", &EBHits_ieta, &b_EBHits_ieta);
//   fChain->SetBranchAddress("EBHits_iphi", &EBHits_iphi, &b_EBHits_iphi);
//   fChain->SetBranchAddress("EBHits_RecoFlag", &EBHits_RecoFlag, &b_EBHits_RecoFlag);
//   fChain->SetBranchAddress("EBHits_kSaturated", &EBHits_kSaturated, &b_EBHits_kSaturated);
//   fChain->SetBranchAddress("EBHits_kLeadingEdgeRecovered", &EBHits_kLeadingEdgeRecovered, &b_EBHits_kLeadingEdgeRecovered);
//   fChain->SetBranchAddress("EBHits_kNeighboursRecovered", &EBHits_kNeighboursRecovered, &b_EBHits_kNeighboursRecovered);
//   fChain->SetBranchAddress("EBHits_kWeird", &EBHits_kWeird, &b_EBHits_kWeird);
//   fChain->SetBranchAddress("EEHits_rawId", &EEHits_rawId, &b_EEHits_rawId);
//   fChain->SetBranchAddress("EEHits_iRechit", &EEHits_iRechit, &b_EEHits_iRechit);
//   fChain->SetBranchAddress("EEHits_energy", &EEHits_energy, &b_EEHits_energy);
//   fChain->SetBranchAddress("EEHits_ieta", &EEHits_ieta, &b_EEHits_ieta);
//   fChain->SetBranchAddress("EEHits_iphi", &EEHits_iphi, &b_EEHits_iphi);
//   fChain->SetBranchAddress("EEHits_RecoFlag", &EEHits_RecoFlag, &b_EEHits_RecoFlag);
//   fChain->SetBranchAddress("EEHits_kSaturated", &EEHits_kSaturated, &b_EEHits_kSaturated);
//   fChain->SetBranchAddress("EEHits_kLeadingEdgeRecovered", &EEHits_kLeadingEdgeRecovered, &b_EEHits_kLeadingEdgeRecovered);
//   fChain->SetBranchAddress("EEHits_kNeighboursRecovered", &EEHits_kNeighboursRecovered, &b_EEHits_kNeighboursRecovered);
//   fChain->SetBranchAddress("EEHits_kWeird", &EEHits_kWeird, &b_EEHits_kWeird);
////   fChain->SetBranchAddress("HEEP_crystal_energy", &HEEP_crystal_energy, &b_HEEP_crystal_energy);
////   fChain->SetBranchAddress("HEEP_crystal_eta", &HEEP_crystal_eta, &b_HEEP_crystal_eta);
////   fChain->SetBranchAddress("HEEP_eshitsixix", &HEEP_eshitsixix, &b_HEEP_eshitsixix);
////   fChain->SetBranchAddress("HEEP_eshitsiyiy", &HEEP_eshitsiyiy, &b_HEEP_eshitsiyiy);
////   fChain->SetBranchAddress("HEEP_crystal_ietaorix", &HEEP_crystal_ietaorix, &b_HEEP_crystal_ietaorix);
////   fChain->SetBranchAddress("HEEP_crystal_iphioriy", &HEEP_crystal_iphioriy, &b_HEEP_crystal_iphioriy);
//   fChain->SetBranchAddress("HEEP_cutflow60_Et", &HEEP_cutflow60_Et, &b_HEEP_cutflow60_Et);
//   fChain->SetBranchAddress("HEEP_cutflow60_Et_n", &HEEP_cutflow60_Et_n, &b_HEEP_cutflow60_Et_n);
//   fChain->SetBranchAddress("HEEP_cutflow60_Et_nCumulative", &HEEP_cutflow60_Et_nCumulative, &b_HEEP_cutflow60_Et_nCumulative);
//   fChain->SetBranchAddress("HEEP_cutflow60_Et_value", &HEEP_cutflow60_Et_value, &b_HEEP_cutflow60_Et_value);
//   fChain->SetBranchAddress("HEEP_cutflow60_eta", &HEEP_cutflow60_eta, &b_HEEP_cutflow60_eta);
//   fChain->SetBranchAddress("HEEP_cutflow60_eta_n", &HEEP_cutflow60_eta_n, &b_HEEP_cutflow60_eta_n);
//   fChain->SetBranchAddress("HEEP_cutflow60_eta_nCumulative", &HEEP_cutflow60_eta_nCumulative, &b_HEEP_cutflow60_eta_nCumulative);
//   fChain->SetBranchAddress("HEEP_cutflow60_eta_value", &HEEP_cutflow60_eta_value, &b_HEEP_cutflow60_eta_value);
//   fChain->SetBranchAddress("HEEP_cutflow60_acceptance", &HEEP_cutflow60_acceptance, &b_HEEP_cutflow60_acceptance);
//   fChain->SetBranchAddress("HEEP_cutflow60_acceptance_n", &HEEP_cutflow60_acceptance_n, &b_HEEP_cutflow60_acceptance_n);
//   fChain->SetBranchAddress("HEEP_cutflow60_EcalDriven", &HEEP_cutflow60_EcalDriven, &b_HEEP_cutflow60_EcalDriven);
//   fChain->SetBranchAddress("HEEP_cutflow60_EcalDriven_n", &HEEP_cutflow60_EcalDriven_n, &b_HEEP_cutflow60_EcalDriven_n);
//   fChain->SetBranchAddress("HEEP_cutflow60_EcalDriven_nCumulative", &HEEP_cutflow60_EcalDriven_nCumulative, &b_HEEP_cutflow60_EcalDriven_nCumulative);
//   fChain->SetBranchAddress("HEEP_cutflow60_EcalDriven_value", &HEEP_cutflow60_EcalDriven_value, &b_HEEP_cutflow60_EcalDriven_value);
//   fChain->SetBranchAddress("HEEP_cutflow60_dEtaIn", &HEEP_cutflow60_dEtaIn, &b_HEEP_cutflow60_dEtaIn);
//   fChain->SetBranchAddress("HEEP_cutflow60_dEtaIn_n", &HEEP_cutflow60_dEtaIn_n, &b_HEEP_cutflow60_dEtaIn_n);
//   fChain->SetBranchAddress("HEEP_cutflow60_dEtaIn_nCumulative", &HEEP_cutflow60_dEtaIn_nCumulative, &b_HEEP_cutflow60_dEtaIn_nCumulative);
//   fChain->SetBranchAddress("HEEP_cutflow60_dEtaIn_value", &HEEP_cutflow60_dEtaIn_value, &b_HEEP_cutflow60_dEtaIn_value);
//   fChain->SetBranchAddress("HEEP_cutflow60_dPhiIn", &HEEP_cutflow60_dPhiIn, &b_HEEP_cutflow60_dPhiIn);
//   fChain->SetBranchAddress("HEEP_cutflow60_dPhiIn_n", &HEEP_cutflow60_dPhiIn_n, &b_HEEP_cutflow60_dPhiIn_n);
//   fChain->SetBranchAddress("HEEP_cutflow60_dPhiIn_nCumulative", &HEEP_cutflow60_dPhiIn_nCumulative, &b_HEEP_cutflow60_dPhiIn_nCumulative);
//   fChain->SetBranchAddress("HEEP_cutflow60_dPhiIn_value", &HEEP_cutflow60_dPhiIn_value, &b_HEEP_cutflow60_dPhiIn_value);
//   fChain->SetBranchAddress("HEEP_cutflow60_HOverE", &HEEP_cutflow60_HOverE, &b_HEEP_cutflow60_HOverE);
//   fChain->SetBranchAddress("HEEP_cutflow60_HOverE_n", &HEEP_cutflow60_HOverE_n, &b_HEEP_cutflow60_HOverE_n);
//   fChain->SetBranchAddress("HEEP_cutflow60_HOverE_nCumulative", &HEEP_cutflow60_HOverE_nCumulative, &b_HEEP_cutflow60_HOverE_nCumulative);
//   fChain->SetBranchAddress("HEEP_cutflow60_HOverE_value", &HEEP_cutflow60_HOverE_value, &b_HEEP_cutflow60_HOverE_value);
//   fChain->SetBranchAddress("HEEP_cutflow60_SigmaIetaIeta", &HEEP_cutflow60_SigmaIetaIeta, &b_HEEP_cutflow60_SigmaIetaIeta);
//   fChain->SetBranchAddress("HEEP_cutflow60_SigmaIetaIeta_n", &HEEP_cutflow60_SigmaIetaIeta_n, &b_HEEP_cutflow60_SigmaIetaIeta_n);
//   fChain->SetBranchAddress("HEEP_cutflow60_SigmaIetaIeta_nCumulative", &HEEP_cutflow60_SigmaIetaIeta_nCumulative, &b_HEEP_cutflow60_SigmaIetaIeta_nCumulative);
//   fChain->SetBranchAddress("HEEP_cutflow60_SigmaIetaIeta_value", &HEEP_cutflow60_SigmaIetaIeta_value, &b_HEEP_cutflow60_SigmaIetaIeta_value);
//   fChain->SetBranchAddress("HEEP_cutflow60_E1x5OverE5x5", &HEEP_cutflow60_E1x5OverE5x5, &b_HEEP_cutflow60_E1x5OverE5x5);
//   fChain->SetBranchAddress("HEEP_cutflow60_E1x5OverE5x5_n", &HEEP_cutflow60_E1x5OverE5x5_n, &b_HEEP_cutflow60_E1x5OverE5x5_n);
//   fChain->SetBranchAddress("HEEP_cutflow60_E1x5OverE5x5_nCumulative", &HEEP_cutflow60_E1x5OverE5x5_nCumulative, &b_HEEP_cutflow60_E1x5OverE5x5_nCumulative);
//   fChain->SetBranchAddress("HEEP_cutflow60_E1x5OverE5x5_value", &HEEP_cutflow60_E1x5OverE5x5_value, &b_HEEP_cutflow60_E1x5OverE5x5_value);
//   fChain->SetBranchAddress("HEEP_cutflow60_E2x5OverE5x5", &HEEP_cutflow60_E2x5OverE5x5, &b_HEEP_cutflow60_E2x5OverE5x5);
//   fChain->SetBranchAddress("HEEP_cutflow60_E2x5OverE5x5_n", &HEEP_cutflow60_E2x5OverE5x5_n, &b_HEEP_cutflow60_E2x5OverE5x5_n);
//   fChain->SetBranchAddress("HEEP_cutflow60_E2x5OverE5x5_nCumulative", &HEEP_cutflow60_E2x5OverE5x5_nCumulative, &b_HEEP_cutflow60_E2x5OverE5x5_nCumulative);
//   fChain->SetBranchAddress("HEEP_cutflow60_E2x5OverE5x5_value", &HEEP_cutflow60_E2x5OverE5x5_value, &b_HEEP_cutflow60_E2x5OverE5x5_value);
//   fChain->SetBranchAddress("HEEP_cutflow60_missingHits", &HEEP_cutflow60_missingHits, &b_HEEP_cutflow60_missingHits);
//   fChain->SetBranchAddress("HEEP_cutflow60_missingHits_n", &HEEP_cutflow60_missingHits_n, &b_HEEP_cutflow60_missingHits_n);
//   fChain->SetBranchAddress("HEEP_cutflow60_missingHits_nCumulative", &HEEP_cutflow60_missingHits_nCumulative, &b_HEEP_cutflow60_missingHits_nCumulative);
//   fChain->SetBranchAddress("HEEP_cutflow60_missingHits_value", &HEEP_cutflow60_missingHits_value, &b_HEEP_cutflow60_missingHits_value);
//   fChain->SetBranchAddress("HEEP_cutflow60_dxyFirstPV", &HEEP_cutflow60_dxyFirstPV, &b_HEEP_cutflow60_dxyFirstPV);
//   fChain->SetBranchAddress("HEEP_cutflow60_dxyFirstPV_n", &HEEP_cutflow60_dxyFirstPV_n, &b_HEEP_cutflow60_dxyFirstPV_n);
//   fChain->SetBranchAddress("HEEP_cutflow60_dxyFirstPV_nCumulative", &HEEP_cutflow60_dxyFirstPV_nCumulative, &b_HEEP_cutflow60_dxyFirstPV_nCumulative);
//   fChain->SetBranchAddress("HEEP_cutflow60_dxyFirstPV_value", &HEEP_cutflow60_dxyFirstPV_value, &b_HEEP_cutflow60_dxyFirstPV_value);
//   fChain->SetBranchAddress("HEEP_cutflow60_ID", &HEEP_cutflow60_ID, &b_HEEP_cutflow60_ID);
//   fChain->SetBranchAddress("HEEP_cutflow60_ID_n", &HEEP_cutflow60_ID_n, &b_HEEP_cutflow60_ID_n);
//   fChain->SetBranchAddress("HEEP_cutflow60_isolEMHadDepth1", &HEEP_cutflow60_isolEMHadDepth1, &b_HEEP_cutflow60_isolEMHadDepth1);
//   fChain->SetBranchAddress("HEEP_cutflow60_isolEMHadDepth1_n", &HEEP_cutflow60_isolEMHadDepth1_n, &b_HEEP_cutflow60_isolEMHadDepth1_n);
//   fChain->SetBranchAddress("HEEP_cutflow60_isolEMHadDepth1_nCumulative", &HEEP_cutflow60_isolEMHadDepth1_nCumulative, &b_HEEP_cutflow60_isolEMHadDepth1_nCumulative);
//   fChain->SetBranchAddress("HEEP_cutflow60_isolEMHadDepth1_value", &HEEP_cutflow60_isolEMHadDepth1_value, &b_HEEP_cutflow60_isolEMHadDepth1_value);
//   fChain->SetBranchAddress("HEEP_cutflow60_IsolPtTrks", &HEEP_cutflow60_IsolPtTrks, &b_HEEP_cutflow60_IsolPtTrks);
//   fChain->SetBranchAddress("HEEP_cutflow60_IsolPtTrks_n", &HEEP_cutflow60_IsolPtTrks_n, &b_HEEP_cutflow60_IsolPtTrks_n);
//   fChain->SetBranchAddress("HEEP_cutflow60_IsolPtTrks_nCumulative", &HEEP_cutflow60_IsolPtTrks_nCumulative, &b_HEEP_cutflow60_IsolPtTrks_nCumulative);
//   fChain->SetBranchAddress("HEEP_cutflow60_IsolPtTrks_value", &HEEP_cutflow60_IsolPtTrks_value, &b_HEEP_cutflow60_IsolPtTrks_value);
//   fChain->SetBranchAddress("HEEP_cutflow60_isolation", &HEEP_cutflow60_isolation, &b_HEEP_cutflow60_isolation);
//   fChain->SetBranchAddress("HEEP_cutflow60_isolation_n", &HEEP_cutflow60_isolation_n, &b_HEEP_cutflow60_isolation_n);
//   fChain->SetBranchAddress("HEEP_cutflow60_total", &HEEP_cutflow60_total, &b_HEEP_cutflow60_total);
//   fChain->SetBranchAddress("HEEP_cutflow60_total_n", &HEEP_cutflow60_total_n, &b_HEEP_cutflow60_total_n);
   fChain->SetBranchAddress("Zee_n", &Zee_n, &b_Zee_n);
   fChain->SetBranchAddress("Zee_mass", &Zee_mass, &b_Zee_mass);
   fChain->SetBranchAddress("Zee_mass_HEEP", &Zee_mass_HEEP, &b_Zee_mass_HEEP);
   fChain->SetBranchAddress("Zee_i1", &Zee_i1, &b_Zee_i1);
   fChain->SetBranchAddress("Zee_i2", &Zee_i2, &b_Zee_i2);
   fChain->SetBranchAddress("Zee_highestMass", &Zee_highestMass, &b_Zee_highestMass);
   fChain->SetBranchAddress("Zmm_n", &Zmm_n, &b_Zmm_n);
   fChain->SetBranchAddress("Zmm_mass", &Zmm_mass, &b_Zmm_mass);
   fChain->SetBranchAddress("Zmm_i1", &Zmm_i1, &b_Zmm_i1);
   fChain->SetBranchAddress("Zmm_i2", &Zmm_i2, &b_Zmm_i2);
   fChain->SetBranchAddress("Zmm_highestMass", &Zmm_highestMass, &b_Zmm_highestMass);
   fChain->SetBranchAddress("Zem_n", &Zem_n, &b_Zem_n);
   fChain->SetBranchAddress("Zem_mass", &Zem_mass, &b_Zem_mass);
   fChain->SetBranchAddress("Zem_mass_HEEP", &Zem_mass_HEEP, &b_Zem_mass_HEEP);
   fChain->SetBranchAddress("Zem_i1", &Zem_i1, &b_Zem_i1);
   fChain->SetBranchAddress("Zem_i2", &Zem_i2, &b_Zem_i2);
   fChain->SetBranchAddress("Zem_highestMass", &Zem_highestMass, &b_Zem_highestMass);

   
   if(true==isData){
     if(triggerVersion.find("DoubleEle33_CaloIdL_GsfTrkIdVL")!=string::npos){
       fChain->SetBranchAddress("trig_HLT_DoubleEle33_CaloIdL_GsfTrkIdVL_accept", &trig_DE_fire, &b_trig_DE_fire) ;
       fChain->SetBranchAddress("trig_HLT_DoubleEle33_CaloIdL_GsfTrkIdVL_hltEle33CaloIdLGsfTrkIdVLDPhiFilter_eta", &trig_DE_eta, &b_trig_DE_eta) ;
       fChain->SetBranchAddress("trig_HLT_DoubleEle33_CaloIdL_GsfTrkIdVL_hltEle33CaloIdLGsfTrkIdVLDPhiFilter_phi", &trig_DE_phi, &b_trig_DE_phi) ;
       fChain->SetBranchAddress("trig_HLT_DoubleEle33_CaloIdL_GsfTrkIdVL_hltDiEle33CaloIdLGsfTrkIdVLDPhiUnseededFilter_eta", &trig_DE_unseed_eta, &b_trig_DE_unseed_eta) ;
       fChain->SetBranchAddress("trig_HLT_DoubleEle33_CaloIdL_GsfTrkIdVL_hltDiEle33CaloIdLGsfTrkIdVLDPhiUnseededFilter_phi", &trig_DE_unseed_phi, &b_trig_DE_unseed_phi) ;
       
                          }

     else if(triggerVersion.find("DoubleEle33_CaloIdL_MW")!=string::npos){
       fChain->SetBranchAddress("trig_HLT_DoubleEle33_CaloIdL_MW_accept", &trig_DE_fire, &b_trig_DE_fire) ;
       fChain->SetBranchAddress("trig_HLT_DoubleEle33_CaloIdL_MW_hltEG33CaloIdLMWPMS2Filter_eta", &trig_DE_eta, &b_trig_DE_eta) ;
       fChain->SetBranchAddress("trig_HLT_DoubleEle33_CaloIdL_MW_hltEG33CaloIdLMWPMS2Filter_phi", &trig_DE_phi, &b_trig_DE_phi) ;
       fChain->SetBranchAddress("trig_HLT_DoubleEle33_CaloIdL_MW_hltDiEle33CaloIdLMWPMS2UnseededFilter_eta", &trig_DE_unseed_eta, &b_trig_DE_unseed_eta) ;
       fChain->SetBranchAddress("trig_HLT_DoubleEle33_CaloIdL_MW_hltDiEle33CaloIdLMWPMS2UnseededFilter_phi", &trig_DE_unseed_phi, &b_trig_DE_unseed_phi) ;
                          }



   }
   
   Notify();
}

Bool_t reskim_FR_1F::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void reskim_FR_1F::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t reskim_FR_1F::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
#endif // #ifdef reskim_FR_1F_cxx
