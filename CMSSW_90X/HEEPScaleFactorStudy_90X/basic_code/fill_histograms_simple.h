//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Thu Dec 10 13:36:52 2015 by ROOT version 6.02/05
// from TTree tap/Streamlined tag and probe
// found on file: ZToEE.root
//////////////////////////////////////////////////////////

#ifndef fill_histograms_simple_h
#define fill_histograms_simple_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

// Header file for the classes stored in the TTree if any.

class fill_histograms_simple {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

// Fixed size dimensions of array or collections stored in the TTree if any.

   // Declaration of leaf types
   Int_t           ev_run;
   Int_t           ev_sign;
   Int_t           pass_HLT_Ele32_require;
   Int_t           pass_HLT_Ele32_require_v1;
   Int_t           pass_HLT_Ele32_require_v2;
   Int_t           pass_HLT_Ele35_require;
   Float_t         mee;
   Int_t           OS;
   Int_t           pv_n;
   Int_t           PU_true;
   Float_t         w_PU_golden;
   Float_t         w_PU_silver;
   Float_t         w_PU_silver_down;
   Float_t         w_PU_silver_up;
   Float_t         w_PU_combined;
   
   Float_t         p_Et;
   Float_t         Pt;
   Float_t         p_eta;
   Float_t         p_phi;
   Float_t         p_Et35;
   Float_t         p_Et20;
   Int_t           p_charge;
   Int_t           p_region;
   Int_t           p_ID_tag;
   Int_t           p_ID_noEcalDriven;
   Int_t           p_ID_noDPhiIn ; 
   Int_t           p_ID_noShower ; 
   Int_t           p_ID_noTrkIso ; 
   Int_t           p_ID_noEMHD1Iso;
   Int_t           p_ID_noMissHit ;
   Int_t           p_ID_noDxy     ;
   Int_t           p_ID_noHoE     ;
   Int_t           p_ID_noTrk;
   Int_t           p_ID_noDEtaIn;
   Int_t           p_ID_noDEtaIn_barrel;
   Int_t           p_ID_noDEtaIn_endcap;
   Int_t           p_ID_noIsolation;
   Int_t           p_ID_nominal;
   Int_t           p_truthmatched;
   Int_t           p_ID_HOverE        ; 
   Int_t           p_ID_showershape   ; 
   Int_t           p_ID_Sieie         ; 
   Int_t           p_ID_EcalDriven    ; 
   Int_t           p_ID_dEtaIn        ; 
   Int_t           p_ID_dPhiIn        ; 
   Int_t           p_ID_isolEMHadDepth1;
   Int_t           p_ID_IsolPtTrks    ; 
   Int_t           p_ID_missingHits   ; 
   Int_t           p_ID_dxyFirstPV    ; 



   
   Float_t         t_Et;
   Float_t         t_eta;
   Float_t         t_phi;
   Float_t         t_Et35;
   Float_t         t_Et20;
   Int_t           t_charge;
   Int_t           t_region;
   Int_t           t_ID_tag;
   Int_t           t_ID_noDEtaIn;
   Int_t           t_ID_EcalDriven;
   Int_t           t_ID_noIsolation;
   Int_t           t_ID_nominal;
   Int_t           t_truthmatched;
   
   Float_t w_PU[3] ;

   // List of branches
   TBranch        *b_ev_run;   //!
   TBranch        *b_ev_sign;   //!
   TBranch        *b_pass_HLT_Ele32_require;   //!
   TBranch        *b_pass_HLT_Ele32_require_v1;   //!
   TBranch        *b_pass_HLT_Ele32_require_v2;   //!
   TBranch        *b_pass_HLT_Ele35_require;   //!
   TBranch        *b_mee;   //!
   TBranch        *b_Pt;   //!
   TBranch        *b_OS;   //!
   TBranch        *b_pv_n;   //!
   TBranch        *b_PU_true;   //!
   
   TBranch        *b_w_PU_golden;   //!
   TBranch        *b_w_PU_silver;   //!
   TBranch        *b_w_PU_silver_down;   //!
   TBranch        *b_w_PU_silver_up;   //!
   TBranch        *b_w_PU_combined;   //!
   
   TBranch        *b_HLT_Ele27;   //!
   TBranch        *b_p_Et;   //!
   TBranch        *b_p_eta;   //!
   TBranch        *b_p_phi;   //!
   TBranch        *b_p_Et35;   //!
   TBranch        *b_p_Et20;   //!
   TBranch        *b_p_charge;   //!
   TBranch        *b_p_region;   //!
   TBranch        *b_p_ID_tag;   //!
   TBranch        *b_p_ID_noEcalDriven;   //!
   TBranch        *b_p_ID_noDPhiIn ; 
   TBranch        *b_p_ID_noShower ; 
   TBranch        *b_p_ID_noTrkIso ; 
   TBranch        *b_p_ID_noEMHD1Iso;
   TBranch        *b_p_ID_noMissHit ;
   TBranch        *b_p_ID_noDxy     ;
   TBranch        *b_p_ID_noHoE     ;



   TBranch        *b_p_ID_noTrk;   //!
   TBranch        *b_p_ID_noDEtaIn;   //!
   TBranch        *b_p_ID_noDEtaIn_barrel;   //!
   TBranch        *b_p_ID_noDEtaIn_endcap;   //!
   TBranch        *b_p_ID_noIsolation;   //!
   TBranch        *b_p_ID_nominal;   //!
   TBranch        *b_p_truthmatched;   //!
  
   TBranch        *b_p_ID_HOverE        ; 
   TBranch        *b_p_ID_showershape   ; 
   TBranch        *b_p_ID_Sieie         ; 
   TBranch        *b_p_ID_EcalDriven    ; 
   TBranch        *b_p_ID_dEtaIn        ; 
   TBranch        *b_p_ID_dPhiIn        ; 
   TBranch        *b_p_ID_isolEMHadDepth1;
   TBranch        *b_p_ID_IsolPtTrks    ; 
   TBranch        *b_p_ID_missingHits   ; 
   TBranch        *b_p_ID_dxyFirstPV    ; 



 
   TBranch        *b_t_Et;   //!
   TBranch        *b_t_eta;   //!
   TBranch        *b_t_phi;   //!
   TBranch        *b_t_Et35;   //!
   TBranch        *b_t_Et20;   //!
   TBranch        *b_t_charge;   //!
   TBranch        *b_t_region;   //!
   TBranch        *b_t_ID_tag;   //!
   TBranch        *b_t_ID_noDEtaIn;   //!
   TBranch        *b_t_ID_EcalDriven;   //!
   TBranch        *b_t_ID_noIsolation;   //!
   TBranch        *b_t_ID_nominal;   //!
   TBranch        *b_t_truthmatched;   //!

   fill_histograms_simple(TTree *tree=0);
   virtual ~fill_histograms_simple();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop(TString);
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
};

#endif

#ifdef fill_histograms_simple_cxx
fill_histograms_simple::fill_histograms_simple(TTree *tree) : fChain(0) 
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
/*
   if (tree == 0) {
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("ZToEE.root");
      if (!f || !f->IsOpen()) {
         f = new TFile("ZToEE.root");
      }
      f->GetObject("tap",tree);

   }
*/
   Init(tree);
}

fill_histograms_simple::~fill_histograms_simple()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t fill_histograms_simple::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t fill_histograms_simple::LoadTree(Long64_t entry)
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

void fill_histograms_simple::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("ev_run" , &ev_run , &b_ev_run );
   fChain->SetBranchAddress("ev_sign", &ev_sign, &b_ev_sign );
   fChain->SetBranchAddress("pass_HLT_Ele32_require", &pass_HLT_Ele32_require, &b_pass_HLT_Ele32_require );
   fChain->SetBranchAddress("pass_HLT_Ele32_require_v1", &pass_HLT_Ele32_require_v1, &b_pass_HLT_Ele32_require_v1 );
   fChain->SetBranchAddress("pass_HLT_Ele32_require_v2", &pass_HLT_Ele32_require_v2, &b_pass_HLT_Ele32_require_v2 );
   fChain->SetBranchAddress("pass_HLT_Ele35_require", &pass_HLT_Ele35_require, &b_pass_HLT_Ele35_require );
   fChain->SetBranchAddress("mee"    , &mee    , &b_mee    );
   fChain->SetBranchAddress("Pt"     , &Pt     , &b_Pt    );
   fChain->SetBranchAddress("OS"     , &OS     , &b_OS     );
   fChain->SetBranchAddress("pv_n"   , &pv_n   , &b_pv_n   );
   fChain->SetBranchAddress("PU_true", &PU_true, &b_PU_true);
   fChain->SetBranchAddress("w_PU_combined"   , &w_PU[0], &b_w_PU_combined   );
   fChain->SetBranchAddress("w_PU_silver_down", &w_PU[1], &b_w_PU_silver_down);
   fChain->SetBranchAddress("w_PU_silver_up"  , &w_PU[2], &b_w_PU_silver_up  );
   
   
   fChain->SetBranchAddress("p_Et"             , &p_Et             , &b_p_Et             );
   fChain->SetBranchAddress("p_eta"            , &p_eta            , &b_p_eta            );
   fChain->SetBranchAddress("p_phi"            , &p_phi            , &b_p_phi            );
   fChain->SetBranchAddress("p_Et35"           , &p_Et35           , &b_p_Et35           );
   fChain->SetBranchAddress("p_Et20"           , &p_Et20           , &b_p_Et20           );
   fChain->SetBranchAddress("p_charge"         , &p_charge         , &b_p_charge         );
   fChain->SetBranchAddress("p_region"         , &p_region         , &b_p_region         );
   fChain->SetBranchAddress("p_ID_tag"         , &p_ID_tag         , &b_p_ID_tag         );
   fChain->SetBranchAddress("p_ID_noEcalDriven", &p_ID_noEcalDriven, &b_p_ID_noEcalDriven);
   fChain->SetBranchAddress("p_ID_noDPhiIn"    , &p_ID_noDPhiIn    , &b_p_ID_noDPhiIn    );
   fChain->SetBranchAddress("p_ID_noShower"    , &p_ID_noShower    , &b_p_ID_noShower    );
   fChain->SetBranchAddress("p_ID_noTrkIso"    , &p_ID_noTrkIso    , &b_p_ID_noTrkIso    );
   fChain->SetBranchAddress("p_ID_noEMHD1Iso"  , &p_ID_noEMHD1Iso  , &b_p_ID_noEMHD1Iso  );
   fChain->SetBranchAddress("p_ID_noMissHit"   , &p_ID_noMissHit   , &b_p_ID_noMissHit   );
   fChain->SetBranchAddress("p_ID_noDxy"       , &p_ID_noDxy       , &b_p_ID_noDxy       );
   fChain->SetBranchAddress("p_ID_noHoE"       , &p_ID_noHoE       , &b_p_ID_noHoE       );
   fChain->SetBranchAddress("p_ID_noDEtaIn"    , &p_ID_noDEtaIn    , &b_p_ID_noDEtaIn    );
   fChain->SetBranchAddress("p_ID_noTrk"       , &p_ID_noTrk       , &b_p_ID_noTrk       );
   fChain->SetBranchAddress("p_ID_noIsolation" , &p_ID_noIsolation , &b_p_ID_noIsolation );
   fChain->SetBranchAddress("p_ID_nominal"     , &p_ID_nominal     , &b_p_ID_nominal     );
   fChain->SetBranchAddress("p_HOverE"         , &p_ID_HOverE          , &b_p_ID_HOverE         );
   fChain->SetBranchAddress("p_showershape"    , &p_ID_showershape     , &b_p_ID_showershape    );
   fChain->SetBranchAddress("p_Sieie"          , &p_ID_Sieie           , &b_p_ID_Sieie          );
   fChain->SetBranchAddress("p_EcalDriven"     , &p_ID_EcalDriven      , &b_p_ID_EcalDriven     );
   fChain->SetBranchAddress("p_dEtaIn"         , &p_ID_dEtaIn          , &b_p_ID_dEtaIn         );
   fChain->SetBranchAddress("p_dPhiIn"         , &p_ID_dPhiIn          , &b_p_ID_dPhiIn         );
   fChain->SetBranchAddress("p_isolEMHadDepth1", &p_ID_isolEMHadDepth1 , &b_p_ID_isolEMHadDepth1);
   fChain->SetBranchAddress("p_IsolPtTrks"     , &p_ID_IsolPtTrks      , &b_p_ID_IsolPtTrks     );
   fChain->SetBranchAddress("p_missingHits"    , &p_ID_missingHits     , &b_p_ID_missingHits    );
   fChain->SetBranchAddress("p_dxyFirstPV"     , &p_ID_dxyFirstPV      , &b_p_ID_dxyFirstPV     );
   
   fChain->SetBranchAddress("t_Et"     , &t_Et     , &b_t_Et     );
   fChain->SetBranchAddress("t_eta"    , &t_eta    , &b_t_eta    );
   fChain->SetBranchAddress("t_phi"    , &t_phi    , &b_t_phi    );
   fChain->SetBranchAddress("t_Et35"   , &t_Et35   , &b_t_Et35   );
   fChain->SetBranchAddress("t_Et20"   , &t_Et20   , &b_t_Et20   );
   fChain->SetBranchAddress("t_charge" , &t_charge , &b_t_charge );
   fChain->SetBranchAddress("t_region" , &t_region , &b_t_region );
   fChain->SetBranchAddress("t_ID_tag" , &t_ID_tag , &b_t_ID_tag );
   fChain->SetBranchAddress("t_ID_nominal"    , &t_ID_nominal    , &b_t_ID_nominal    );
   
   Notify();
}

Bool_t fill_histograms_simple::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void fill_histograms_simple::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t fill_histograms_simple::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
#endif // #ifdef fill_histograms_simple_cxx
