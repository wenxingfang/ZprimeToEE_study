#define fill_histograms_simple_cxx
#include "fill_histograms_simple.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <iostream>
#include "MC_pileup_weight.C"
void displayProgress(long current, long max){
  using std::cerr;
  if (max<1000) return;
  if (current%(max/1000)!=0 && current<max-1) return;

  int width = 52; // Hope the terminal is at least that wide.
  int barWidth = width - 2;
  cerr << "\x1B[2K"; // Clear line
  cerr << "\x1B[2000D"; // Cursor left
  cerr << '[';
  for(int i=0 ; i<barWidth ; ++i){ if(i<barWidth*current/max){ cerr << '=' ; }else{ cerr << ' ' ; } }
  cerr << ']';
  cerr << " " << Form("%8d/%8d (%5.2f%%)", (int)current, (int)max, 100.0*current/max) ;
  cerr.flush();
}

void fill_histograms_simple::Loop(TString sampleName){
   std::cout << sampleName << std::endl ;

   TH1::SetDefaultSumw2();
 
   time_t time_start = time(0) ;
   char* time_start_text = ctime(&time_start) ;
   std::cout << time_start_text << std::endl ;
   
   if (fChain == 0) return;
   
   int nHistos = 1 ;
   const int NBinnings   =  2 ; nHistos *= NBinnings   ;
   const int NVars       =  5 ; nHistos *= NVars       ;
   const int NRegions    =  3 ; nHistos *= NRegions    ;
//   const int NCharges    =  3 ; nHistos *= NCharges    ;
//   const int NTagCharges =  3 ; nHistos *= NTagCharges ;
   const int NCharges    =  1 ; nHistos *= NCharges    ;
   const int NTagCharges =  1 ; nHistos *= NTagCharges ;
   const int NHEEP       =  3 ; nHistos *= NHEEP       ;
   const int NOSSS       =  3 ; nHistos *= NOSSS       ;
//   const int NAltCut     =  4 ; nHistos *= NAltCut     ;
   const int NAltCut     =  18 ; nHistos *= NAltCut     ;
//   const int NJson       =  5 ; nHistos *= NJson       ;
   const int NJson       =  3 ; nHistos *= NJson       ;
   const int NPUW        =  4 ; nHistos *= NPUW        ;
   
   TFile* fBase = new TFile("/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/hBase.root","READ") ;
   
   TFile* file_out = new TFile(Form("/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEPScaleFactorStudy/HEEPScaleFactorStudy_80X/ntuples/out/simple/%s_slices.root",sampleName.Data()),"RECREATE") ;
   TH2F* histograms[NBinnings][NVars][NRegions][NCharges][NTagCharges][NOSSS][NAltCut][NJson][NHEEP][NPUW] ;
   
   TString   binningNames[NBinnings  ] = {"cut","fit"} ;
//   TString       varNames[NVars      ] = {"Et","eta","phi","nVtx","Pt","EtAve","nVtxL"} ;
   TString       varNames[NVars      ] = {"Et","eta","phi","nVtx","Pt"} ;
   TString    regionNames[NRegions   ] = {"Barrel","Transition","Endcap"} ;
//   TString    chargeNames[NCharges   ] = {"em","ep","ea"} ;
//   TString tagChargeNames[NTagCharges] = {"tm","tp","ta"} ;
   TString    chargeNames[NCharges   ] = {"ea"} ;
   TString tagChargeNames[NTagCharges] = {"ta"} ;
   TString      HEEPNames[NHEEP      ] = {"probes","pass","fail"} ;
   TString      OSSSNames[NOSSS      ] = {"OS","SS","AS"} ;
   TString    altCutNames[NAltCut    ] = {"nominal","N_1_EcalDriven","N_1_DEtaIn","N_1_DPhiIn","N_1_Shower","N_1_TrkIso","N_1_EMHD1Iso","N_1_MissHit","N_1_Dxy","N_1_HoE","N_2_Isolation","N_3_Trk","N_2_DetaIn_Dxy","ProbeEt_35_50","ProbeEt_50_100","ProbeEt_100_inf","ProbeEt_300_inf","ProbeEt_500_inf"} ;
//   TString      jsonNames[NJson      ] = {"combined","silverDown","silverUp"} ;
   TString      jsonNames[NJson      ] = {"combined","silverUp","silverDown"} ;
//   TString       PUWNames[NPUW       ] = {"PUW","NoPUW"} ;
   TString       PUWNames[NPUW       ] = {"PUW","NoPUW","PUWrunB2F","PUWrunGH"} ;
   
   //file_in->ls() ;
   std::cout << "Making histograms..." << std::endl ;
   Int_t counter = 0 ;
   for(int iBinning=0 ; iBinning<NBinnings ; ++iBinning){
      for(int iVar=0 ; iVar<NVars ; ++iVar){
        for(int iRegion=0 ; iRegion<NRegions ; ++iRegion){
          TString hBaseName = Form("hBase_2D_%s_%s_%s_mee",
            binningNames[iBinning].Data(),
            varNames[iVar].Data(),
            regionNames[iRegion].Data()) ;
            
          TH2F* hBase = (TH2F*)fBase->Get(hBaseName) ;
	  hBase->Sumw2() ;
          for(int iCharge=0 ; iCharge<NCharges ; ++iCharge){
            for(int iTagCharge=0 ; iTagCharge<NTagCharges ; ++iTagCharge){
              for(int iOSSS=0 ; iOSSS<NOSSS ; ++iOSSS){
                for(int iAltCut=0 ; iAltCut<NAltCut ; ++iAltCut){
                  for(int iJson=0 ; iJson<NJson ; ++iJson){
                    for(int iHEEP=0 ; iHEEP<NHEEP ; ++iHEEP){
                      for(int iPUW=0 ; iPUW<NPUW ; ++iPUW){
                        counter++ ;
                        displayProgress(counter,nHistos) ;
                        TString hName = Form("h_%s_%s_%s_%s_%s_%s_%s_%s_%s_%s_%s",
                              binningNames[iBinning].Data(),
                              sampleName.Data(),
                              varNames[iVar].Data(),
                              regionNames[iRegion].Data(),
                              chargeNames[iCharge].Data(),
                              tagChargeNames[iTagCharge].Data(),
                              OSSSNames[iOSSS].Data(),
                              altCutNames[iAltCut].Data(),
                              jsonNames[iJson].Data(),
                              HEEPNames[iHEEP].Data(),
                              PUWNames[iPUW].Data()) ;
                        TH2F* h2D = (TH2F*) hBase->Clone(hName) ;
                        h2D->Scale(0.0) ;
                        if(!h2D){
                          std::cout << hName << std::endl ;
                        }
                        else{
                          histograms[iBinning][iVar][iRegion][iCharge][iTagCharge][iOSSS][iAltCut][iJson][iHEEP][iPUW] = h2D ;
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
   std::cout << "Done!" << std::endl ;
   time_t time_mid = time(0) ;
   char* time_mid_text = ctime(&time_mid) ;
   std::cout << time_mid_text << std::endl ;
   //###########################
   bool is_MC=true;
   //############################
   Long64_t nentries = fChain->GetEntries();
   Long64_t nbytes = 0, nb = 0;
   for (Long64_t jentry=0; jentry<nentries;jentry++) {
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);   nbytes += nb;
      displayProgress(jentry, nentries) ;
      int iRegion = p_region-1 ;
      if(iRegion<0 || iRegion>2) continue ;
//      int iCharge    = (p_charge<0) ? 0 : 1 ;
//      int iTagCharge = (t_charge<0) ? 0 : 1 ;
      int iOSSS      = (OS        ) ? 0 : 1 ;
      
      float var_values[NVars] = {p_Et, p_eta, p_phi, (float)1.0*pv_n, Pt} ;
      for(int iB=0 ; iB<NBinnings ; ++iB){
        for(int iVar=0 ; iVar<NVars ; ++iVar){
          float v = var_values[iVar] ;
//          float Et_threshold = (iVar==0) ? 20.0 : 35.0 ;
          float Et_threshold = 35.0;
          if(p_Et < Et_threshold) continue ;

          for(int iA=0 ; iA<NAltCut ; ++iA){
            bool fill_1HEEP = false ;
            int pass_or_fail = 0 ; // 1 for pass, 2 for fail
            pass_or_fail =(p_ID_nominal    ) ? 1 : 2 ; 
            switch(iA){
case 0: { fill_1HEEP = true ; break;}
case 1: { fill_1HEEP=(p_ID_HOverE && p_ID_showershape && p_ID_Sieie &&                    p_ID_dEtaIn && p_ID_dPhiIn && p_ID_isolEMHadDepth1 && p_ID_IsolPtTrks && p_ID_missingHits && p_ID_dxyFirstPV)  ? true : false ; break;  }  
case 2: { fill_1HEEP=(p_ID_HOverE && p_ID_showershape && p_ID_Sieie && p_ID_EcalDriven &&                p_ID_dPhiIn && p_ID_isolEMHadDepth1 && p_ID_IsolPtTrks && p_ID_missingHits && p_ID_dxyFirstPV)  ? true : false ; break;  }  
case 3: { fill_1HEEP=(p_ID_HOverE && p_ID_showershape && p_ID_Sieie && p_ID_EcalDriven && p_ID_dEtaIn &&                p_ID_isolEMHadDepth1 && p_ID_IsolPtTrks && p_ID_missingHits && p_ID_dxyFirstPV)  ? true : false ; break;  }  
case 4: { fill_1HEEP=(p_ID_HOverE &&                                   p_ID_EcalDriven && p_ID_dEtaIn && p_ID_dPhiIn && p_ID_isolEMHadDepth1 && p_ID_IsolPtTrks && p_ID_missingHits && p_ID_dxyFirstPV)  ? true : false ; break;  }  
case 5: { fill_1HEEP=(p_ID_HOverE && p_ID_showershape && p_ID_Sieie && p_ID_EcalDriven && p_ID_dEtaIn && p_ID_dPhiIn && p_ID_isolEMHadDepth1 &&                    p_ID_missingHits && p_ID_dxyFirstPV)  ? true : false ; break;  }  
case 6: { fill_1HEEP=(p_ID_HOverE && p_ID_showershape && p_ID_Sieie && p_ID_EcalDriven && p_ID_dEtaIn && p_ID_dPhiIn &&                         p_ID_IsolPtTrks && p_ID_missingHits && p_ID_dxyFirstPV)  ? true : false ; break;  }  
case 7: { fill_1HEEP=(p_ID_HOverE && p_ID_showershape && p_ID_Sieie && p_ID_EcalDriven && p_ID_dEtaIn && p_ID_dPhiIn && p_ID_isolEMHadDepth1 && p_ID_IsolPtTrks &&                     p_ID_dxyFirstPV)  ? true : false ; break;  }  
case 8: { fill_1HEEP=(p_ID_HOverE && p_ID_showershape && p_ID_Sieie && p_ID_EcalDriven && p_ID_dEtaIn && p_ID_dPhiIn && p_ID_isolEMHadDepth1 && p_ID_IsolPtTrks && p_ID_missingHits                   )  ? true : false ; break;  }  
case 9: { fill_1HEEP=(               p_ID_showershape && p_ID_Sieie && p_ID_EcalDriven && p_ID_dEtaIn && p_ID_dPhiIn && p_ID_isolEMHadDepth1 && p_ID_IsolPtTrks && p_ID_missingHits && p_ID_dxyFirstPV)  ? true : false ; break;  }  
case 10:{ fill_1HEEP=(p_ID_HOverE && p_ID_showershape && p_ID_Sieie && p_ID_EcalDriven && p_ID_dEtaIn && p_ID_dPhiIn &&                                            p_ID_missingHits && p_ID_dxyFirstPV)  ? true : false ; break;  }  
case 11:{ fill_1HEEP=(p_ID_HOverE && p_ID_showershape && p_ID_Sieie && p_ID_EcalDriven &&                               p_ID_isolEMHadDepth1 && p_ID_IsolPtTrks && p_ID_missingHits                   )  ? true : false ; break;  }  
case 12:{ fill_1HEEP=(p_ID_HOverE && p_ID_showershape && p_ID_Sieie && p_ID_EcalDriven &&                p_ID_dPhiIn && p_ID_isolEMHadDepth1 && p_ID_IsolPtTrks && p_ID_missingHits                   )  ? true : false ; break;  }  

case 13:{ fill_1HEEP=(p_Et>35 && p_Et<50 )  ? true : false; break;}
case 14:{ fill_1HEEP=(p_Et>50 && p_Et<100)  ? true : false; break;}
case 15:{ fill_1HEEP=(p_Et>100           )  ? true : false; break;}
case 16:{ fill_1HEEP=(p_Et>300           )  ? true : false; break;}
case 17:{ fill_1HEEP=(p_Et>500           )  ? true : false; break;}
default:{std::cout<<"Error, out of range"<<std::endl;}
            }

//            int iCharges   [2] = {iCharge   ,2} ;
//            int iTagCharges[2] = {iTagCharge,2} ;
            int iOSSSS     [2] = {iOSSS     ,2} ;
            
//            for(int iC=0 ; iC<2 ; ++iC){
              for(int iO=0 ; iO<2 ; ++iO){
                for(int iJson=0 ; iJson<NJson ; ++iJson){
//                  float w = w_PU[iJson] ;
//                  if(isnan(w)) continue ;
//                  for(int iT=0 ; iT<2 ; ++iT){
                    if(fill_1HEEP){
                      float w=1;
                      float w1=1;
                      float w2=1;
                      if(is_MC){
                     //////////////////////////////////////
                       w=ev_sign*PU_reReco_Morind17::MC_pileup_weight(PU_true,iJson,"all");
                      w1=ev_sign*PU_reReco_Morind17::MC_pileup_weight(PU_true,iJson,"B2F");
                      w2=ev_sign*PU_reReco_Morind17::MC_pileup_weight(PU_true,iJson,"GH");
                      if(isnan(w))   w=1 ;
                      if(isnan(w1)) w1=1 ;
                      if(isnan(w2)) w2=1 ;
                      ////////////
                               }
                             histograms[iB][iVar][iRegion][0][0][iOSSSS[iO]][iA][iJson][0][0]->Fill(v, mee, w) ;
                      if(w>0)histograms[iB][iVar][iRegion][0][0][iOSSSS[iO]][iA][iJson][0][1]->Fill(v, mee,1) ;
                      if(w<0)histograms[iB][iVar][iRegion][0][0][iOSSSS[iO]][iA][iJson][0][1]->Fill(v, mee,-1) ;
                             histograms[iB][iVar][iRegion][0][0][iOSSSS[iO]][iA][iJson][0][2]->Fill(v, mee, w1) ;
                             histograms[iB][iVar][iRegion][0][0][iOSSSS[iO]][iA][iJson][0][3]->Fill(v, mee, w2) ;
                      if(pass_or_fail==1){
                             histograms[iB][iVar][iRegion][0][0][iOSSSS[iO]][iA][iJson][1][0]->Fill(v, mee, w) ;
                      if(w>0)histograms[iB][iVar][iRegion][0][0][iOSSSS[iO]][iA][iJson][1][1]->Fill(v, mee,1) ;
                      if(w<0)histograms[iB][iVar][iRegion][0][0][iOSSSS[iO]][iA][iJson][1][1]->Fill(v, mee,-1) ;
                             histograms[iB][iVar][iRegion][0][0][iOSSSS[iO]][iA][iJson][1][2]->Fill(v, mee, w1) ;
                             histograms[iB][iVar][iRegion][0][0][iOSSSS[iO]][iA][iJson][1][3]->Fill(v, mee, w2) ;
                      }
                      else{
                             histograms[iB][iVar][iRegion][0][0][iOSSSS[iO]][iA][iJson][2][0]->Fill(v, mee, w) ;
                      if(w>0)histograms[iB][iVar][iRegion][0][0][iOSSSS[iO]][iA][iJson][2][1]->Fill(v, mee, 1) ;
                      if(w<0)histograms[iB][iVar][iRegion][0][0][iOSSSS[iO]][iA][iJson][2][1]->Fill(v, mee, -1) ;
                             histograms[iB][iVar][iRegion][0][0][iOSSSS[iO]][iA][iJson][2][2]->Fill(v, mee, w1) ;
                             histograms[iB][iVar][iRegion][0][0][iOSSSS[iO]][iA][iJson][2][3]->Fill(v, mee, w2) ;
                      }
                    }
//                  }
                }
              }  
//            }
          }
        }
      }
   }
   
   std::cout << "Writing histograms..." << std::endl ;
   int nEmpty = 0 ;
   for(int iBinning=0 ; iBinning<NBinnings ; ++iBinning){
      for(int iVar=0 ; iVar<NVars ; ++iVar){
        for(int iRegion=0 ; iRegion<NRegions ; ++iRegion){
          for(int iCharge=0 ; iCharge<NCharges ; ++iCharge){
            for(int iTagCharge=0 ; iTagCharge<NTagCharges ; ++iTagCharge){
              for(int iOSSS=0 ; iOSSS<NOSSS ; ++iOSSS){
                for(int iAltCut=0 ; iAltCut<NAltCut ; ++iAltCut){
                  for(int iJson=0 ; iJson<NJson ; ++iJson){
                    for(int iHEEP=0 ; iHEEP<NHEEP ; ++iHEEP){
                      for(int iPUW=0 ; iPUW<NPUW ; ++iPUW){
                        TH2F* h = histograms[iBinning][iVar][iRegion][iCharge][iTagCharge][iOSSS][iAltCut][iJson][iHEEP][iPUW] ;
                        if(h->GetSumOfWeights()<1e-3){
                          nEmpty++ ;
                        }
                        h->Write() ;
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
   }
   std::cout << nEmpty << " empty histograms of " << nHistos << std::endl ;
   file_out->Close() ;
   
   time_t time_end = time(0) ;
   char* time_end_text = ctime(&time_end) ;
   std::cout << time_end_text << std::endl ;
}
