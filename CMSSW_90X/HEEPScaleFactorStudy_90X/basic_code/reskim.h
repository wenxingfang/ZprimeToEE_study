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
   vector<float> *gsf_sc_energy;              
   vector<float> *gsf_sc_eta;                 
   vector<float> *gsf_sc_phi;                 
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
   
   Int_t trig_Ele32_accept ;
   Int_t trig_Ele35_accept ;
   vector<float> *trig_eta ;
   
   vector<float> *trig_Ele32_eta ;
   vector<float> *trig_Ele32_phi ;
   vector<float> *trig_Ele32_L1_eta_v1 ;
   vector<float> *trig_Ele32_L1_phi_v1 ;
   vector<float> *trig_Ele32_L1_eta_v2 ;
   vector<float> *trig_Ele32_L1_phi_v2 ;
   vector<float> *trig_Ele32_L1_eta ;
   vector<float> *trig_Ele32_L1_phi ;
   vector<float> *trig_Ele35_eta ;
   vector<float> *trig_Ele35_phi ;
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

   TBranch *b_gsf_sc_energy;              
   TBranch *b_gsf_sc_eta;                 
   TBranch *b_gsf_sc_phi;                 
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
   
   TBranch        *b_mc_w_sign;   //!
   

   TBranch *b_trig_Ele32_accept  ;
   TBranch *b_trig_Ele35_accept  ;
   TBranch *b_trig_Ele32_eta  ;
   TBranch *b_trig_Ele32_phi  ;
   TBranch *b_trig_Ele32_L1_eta_v1  ;
   TBranch *b_trig_Ele32_L1_phi_v1  ;
   TBranch *b_trig_Ele32_L1_eta_v2  ;
   TBranch *b_trig_Ele32_L1_phi_v2  ;
   TBranch *b_trig_Ele32_L1_eta  ;
   TBranch *b_trig_Ele32_L1_phi  ;
   TBranch *b_trig_Ele35_eta  ;
   TBranch *b_trig_Ele35_phi  ;
   bool isData  ;
   bool isZToTT ;
   bool isZToEE ;
   bool isWJets ;
   string triggerVersion ;
   unsigned int Run_low;
   unsigned int Run_high;   

   float goldenLumi ;
   float silverLumi ;
   float combinedLumi ;

   reskim(TTree *tree=0, bool isData_in=false, bool isZToEE_in=false, bool isZToTT_in=false, bool isWJets_in=false, string triggerVersion_in="", int Run_low_in=0, int Run_high_in=999999);
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
reskim::reskim(TTree *tree, bool isData_in, bool isZToEE_in,  bool isZToTT_in, bool isWJets_in, string triggerVersion_in, int Run_low_in, int Run_high_in) :
fChain(0),
goldenLumi(2040.0), 
silverLumi(351.0), 
combinedLumi(2391.0)
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   isData  = isData_in  ;
   isZToTT = isZToTT_in ;
   isZToEE = isZToEE_in ;
   isWJets = isWJets_in ;
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
   gsf_sc_energy = 0;              
   gsf_sc_eta    = 0;              
/////////////////////
   
   
   trig_Ele32_eta=0; 
   trig_Ele32_phi=0; 
   trig_Ele32_L1_eta_v1=0;
   trig_Ele32_L1_phi_v1=0;
   trig_Ele32_L1_eta_v2=0;
   trig_Ele32_L1_phi_v2=0;
   trig_Ele32_L1_eta=0;
   trig_Ele32_L1_phi=0;
   trig_Ele35_eta=0; 
   trig_Ele35_phi=0; 


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
   fChain->SetBranchAddress("gsf_n", &gsf_n, &b_gsf_n);
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
   fChain->SetBranchAddress("gsf_sc_eta"  , &gsf_sc_eta   , &b_gsf_sc_eta);
   fChain->SetBranchAddress("gsf_sc_energy",&gsf_sc_energy, &b_gsf_sc_energy);

   fChain->SetBranchAddress("trig_HLT_Ele32_WPTight_Gsf_L1DoubleEG_accept", &trig_Ele32_accept, &b_trig_Ele32_accept) ;


   fChain->SetBranchAddress("trig_HLT_Ele32_WPTight_Gsf_L1DoubleEG_hltL1sSingleAndDoubleEGor_eta", &trig_Ele32_L1_eta_v1, &b_trig_Ele32_L1_eta_v1) ;
   fChain->SetBranchAddress("trig_HLT_Ele32_WPTight_Gsf_L1DoubleEG_hltL1sSingleAndDoubleEGor_phi", &trig_Ele32_L1_phi_v1, &b_trig_Ele32_L1_phi_v1) ;
   fChain->SetBranchAddress("trig_HLT_Ele32_WPTight_Gsf_L1DoubleEG_hltEGL1SingleAndDoubleEGOrSingleFilter_eta", &trig_Ele32_L1_eta_v2, &b_trig_Ele32_L1_eta_v2) ;
   fChain->SetBranchAddress("trig_HLT_Ele32_WPTight_Gsf_L1DoubleEG_hltEGL1SingleAndDoubleEGOrSingleFilter_phi", &trig_Ele32_L1_phi_v2, &b_trig_Ele32_L1_phi_v2) ;

   fChain->SetBranchAddress("trig_HLT_Ele32_WPTight_Gsf_L1DoubleEG_hltEG32L1SingleAndDoubleEGEtFilter_eta", &trig_Ele32_L1_eta, &b_trig_Ele32_L1_eta) ;
   fChain->SetBranchAddress("trig_HLT_Ele32_WPTight_Gsf_L1DoubleEG_hltEG32L1SingleAndDoubleEGEtFilter_phi", &trig_Ele32_L1_phi, &b_trig_Ele32_L1_phi) ;
   fChain->SetBranchAddress("trig_HLT_Ele32_WPTight_Gsf_L1DoubleEG_hltEle32L1DoubleEGWPTightGsfTrackIsoFilter_eta", &trig_Ele32_eta, &b_trig_Ele32_eta) ;
   fChain->SetBranchAddress("trig_HLT_Ele32_WPTight_Gsf_L1DoubleEG_hltEle32L1DoubleEGWPTightGsfTrackIsoFilter_phi", &trig_Ele32_phi, &b_trig_Ele32_phi) ;
   fChain->SetBranchAddress("trig_HLT_Ele35_WPTight_Gsf_accept", &trig_Ele35_accept, &b_trig_Ele35_accept) ;
   fChain->SetBranchAddress("trig_HLT_Ele35_WPTight_Gsf_hltEle35noerWPTightGsfTrackIsoFilter_eta", &trig_Ele35_eta, &b_trig_Ele35_eta) ;
   fChain->SetBranchAddress("trig_HLT_Ele35_WPTight_Gsf_hltEle35noerWPTightGsfTrackIsoFilter_phi", &trig_Ele35_phi, &b_trig_Ele35_phi) ;
   
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
