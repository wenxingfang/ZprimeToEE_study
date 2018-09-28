#include <TH1.h>
#include <TH1F.h>
#include <TH1D.h>
#include <TH1D.h>
#include <TChain.h>
#include <TFile.h>
#include <TH2.h>
#include <TAxis.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TRandom3.h>
#include <TLorentzVector.h>
#include <TF1.h>
#include <time.h>
#include <iostream>
#include <fstream>
#include <map>
#include "./resolution_cfg.C"
const float PI_F=3.14159265358979;
const float m_el = 0.000511 ;

TString Regress=80;//80 or 74 regression
bool remove_saturated=false;

void fill_cum(TH1D* &hist, float M , double weight);
void Remove_negative_events(TH1D * &h);
int matching(vector<float> *eta, vector<float> *phi, float eta_1, float phi_1);
float sf_weight(float Et, float eta, TString uncert);
int trigger_match(float eta, float phi, vector<float> *filter_eta, vector<float> *filter_phi, int fire);
double calcCosThetaCSAnal(TLorentzVector v_dil, TLorentzVector v_mum, TLorentzVector v_mup) ;
double calcCosThetaCSAnal(double pz_mum, double e_mum, double pz_mup, double e_mup, double pt_dil, double pl_dil, double mass_dil) ;
void fill_hist(TString input_file, TString output_file, bool is_data=false, bool is_ZToEE=false, bool do_fewz=false, bool do_FR_1F=false, bool do_FR_2F=false, TString uncert="");

void select_and_save(TString uncert_s ){
TString input_dir="/user/wenxing/ST_TW_channel/CMSSW_8_0_25/src/ee_channel/reskim_script/reskim_out/gen_info_for_2017/";
TString output_dir="/user/wenxing/ST_TW_channel/CMSSW_9_4_0/src/Zprime/ntuples/sys_saved_hist/20180304_MCGenmassbin/";
bool do_fewz=true;
TString str_fewz=do_fewz?"_fewz":"";
TString str_uncert="";
TString uncertainty="";
//uncertainty="PU_scale_up";
//uncertainty="PU_scale_down";
//uncertainty="Barrel_energy_scale_up";
//uncertainty="Barrel_energy_scale_down";
//uncertainty="Endcap_energy_scale_up";
//uncertainty="Endcap_energy_scale_down";
//fill_hist(input_dir+"RunBCDEFGH.root"   ,output_dir+"hist_data_test.root"     ,true,false,false,false,false,uncertainty);
/*
fill_hist(input_dir+"RunBCDEFGH.root"   ,output_dir+"hist_data_RunBCDEFGH_reMiniAOD.root"     ,true,false,false,false,false,uncertainty);
fill_hist(input_dir+"RunBCDEFGH.root"   ,output_dir+"hist_data_RunBCDEFGH_FR1F_reMiniAOD.root",true,false,false,true ,false,uncertainty);
fill_hist(input_dir+"RunBCDEFGH.root"   ,output_dir+"hist_data_RunBCDEFGH_FR2F_reMiniAOD.root",true,false,false,false ,true,uncertainty);
*/
//fill_hist(input_dir+   "ZToEE_M_50_120.root",output_dir+str_uncert+   "hist_ZToEE_50_120"+str_fewz+".root",false,true,do_fewz,false,false,uncertainty);
vector<TString> v_uncert;
v_uncert.push_back(uncert_s)             ;
//v_uncert.push_back("nominal"              )             ;
//v_uncert.push_back("PU_scale_up"          )             ;
//v_uncert.push_back("PU_scale_down"        )           ;
////v_uncert.push_back("Barrel_energy_scale_up")  ;
////v_uncert.push_back("Barrel_energy_scale_down");
////v_uncert.push_back("Endcap_energy_scale_up")  ;
////v_uncert.push_back("Endcap_energy_scale_down");
//v_uncert.push_back("BB_mass_scale_up"     )  ;
//v_uncert.push_back("BB_mass_scale_down"   );
//v_uncert.push_back("BE_mass_scale_up"     )  ;
//v_uncert.push_back("BE_mass_scale_down"   );
//v_uncert.push_back("Barrel_SF_scale_up"   )  ;
//v_uncert.push_back("Barrel_SF_scale_down" );
//v_uncert.push_back("Endcap_SF_scale_up"   )  ;
//v_uncert.push_back("Endcap_SF_scale_down" );
//v_uncert.push_back("pdf_scale_up"         );
//v_uncert.push_back("pdf_scale_down"       );
for( unsigned int iv=0;iv<v_uncert.size();iv++){
uncertainty = v_uncert.at(iv);
     if (uncertainty=="PU_scale_up") str_uncert="PU_scale_up_";
else if (uncertainty=="PU_scale_down") str_uncert="PU_scale_down_";
else if (uncertainty=="Barrel_energy_scale_up") str_uncert="Barrel_energy_scale_up_";
else if (uncertainty=="Barrel_energy_scale_down") str_uncert="Barrel_energy_scale_down_";
else if (uncertainty=="Endcap_energy_scale_up") str_uncert="Endcap_energy_scale_up_";
else if (uncertainty=="Endcap_energy_scale_down") str_uncert="Endcap_energy_scale_down_";
else if (uncertainty=="BB_mass_scale_up")   str_uncert="BB_mass_scale_up_";
else if (uncertainty=="BB_mass_scale_down") str_uncert="BB_mass_scale_down_";
else if (uncertainty=="BE_mass_scale_up")   str_uncert="BE_mass_scale_up_";
else if (uncertainty=="BE_mass_scale_down") str_uncert="BE_mass_scale_down_";
else if (uncertainty=="Barrel_SF_scale_up")   str_uncert="Barrel_SF_scale_up_";
else if (uncertainty=="Barrel_SF_scale_down") str_uncert="Barrel_SF_scale_down_";
else if (uncertainty=="Endcap_SF_scale_up")   str_uncert="Endcap_SF_scale_up_";
else if (uncertainty=="Endcap_SF_scale_down") str_uncert="Endcap_SF_scale_down_";
else if (uncertainty=="pdf_scale_up")         str_uncert="pdf_scale_up_";
else if (uncertainty=="pdf_scale_down")       str_uncert="pdf_scale_down_";

if(uncertainty!="pdf_scale_up" && uncertainty!="pdf_scale_down"){
fill_hist(input_dir+"WWTo2L2Nu_Mll_200To600.root"                ,output_dir+str_uncert+"hist_WW2L_200_600.root"     ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"WWTo2L2Nu_Mll_600To1200.root"               ,output_dir+str_uncert+"hist_WW2L_600_1200.root"    ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"WWTo2L2Nu_Mll_1200To2500.root"              ,output_dir+str_uncert+"hist_WW2L_1200_2500.root"   ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"WWTo2L2Nu_Mll_2500ToInf.root"               ,output_dir+str_uncert+"hist_WW2L_2500_Inf.root"    ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"TTToLL_M_500To800.root"                     ,output_dir+str_uncert+"hist_TTbar2L_500_800.root"  ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"TTToLL_M_800To1200.root"                    ,output_dir+str_uncert+"hist_TTbar2L_800_1200.root" ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"TTToLL_M_1200To1800.root"                   ,output_dir+str_uncert+"hist_TTbar2L_1200_1800.root",false,false,false,false,false,uncertainty);
fill_hist(input_dir+"TTToLL_M_1800ToInf.root"                    ,output_dir+str_uncert+"hist_TTbar2L_1800_Inf.root" ,false,false,false,false,false,uncertainty);

fill_hist(input_dir+"WWTo2L2Nu_Mll_200To600.root"                ,output_dir+str_uncert+"hist_WW2L_200_600_1F.root"     ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"WWTo2L2Nu_Mll_600To1200.root"               ,output_dir+str_uncert+"hist_WW2L_600_1200_1F.root"    ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"WWTo2L2Nu_Mll_1200To2500.root"              ,output_dir+str_uncert+"hist_WW2L_1200_2500_1F.root"   ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"WWTo2L2Nu_Mll_2500ToInf.root"               ,output_dir+str_uncert+"hist_WW2L_2500_Inf_1F.root"    ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"TTToLL_M_500To800.root"                     ,output_dir+str_uncert+"hist_TTbar2L_500_800_1F.root"  ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"TTToLL_M_800To1200.root"                    ,output_dir+str_uncert+"hist_TTbar2L_800_1200_1F.root" ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"TTToLL_M_1200To1800.root"                   ,output_dir+str_uncert+"hist_TTbar2L_1200_1800_1F.root",false,false,false,true,false,uncertainty);
fill_hist(input_dir+"TTToLL_M_1800ToInf.root"                    ,output_dir+str_uncert+"hist_TTbar2L_1800_Inf_1F.root" ,false,false,false,true,false,uncertainty);
}


}

}

void fill_hist(TString input_file, TString output_file, bool is_data, bool is_ZToEE, bool do_fewz, bool do_FR_1F, bool do_FR_2F, TString uncert){

TH1::SetDefaultSumw2(kTRUE);
TString t_name="LL";
TChain *t = new TChain(t_name);
t->Add(input_file);

   int   pv_n       = 0 ;
   int   event_sign = 0 ;
   int   PU_true    = 0 ;
   float rho        = 0 ;

   int trig_DEle33       =0; 
   int trig_DEle33_MW    =0; 

   vector<float> *trig_DEle33_unseed_eta   =0; 
   vector<float> *trig_DEle33_unseed_phi   =0; 
   vector<float> *trig_DEle33_MW_unseed_eta=0; 
   vector<float> *trig_DEle33_MW_unseed_phi=0; 

   vector<float> *heeps_et          =0; 
   vector<float> *heeps_eta         =0; 
   vector<float> *heeps_sc_eta      =0; 
   vector<float> *heeps_phi         =0; 
   vector<float> *heeps_sc_phi      =0; 
   vector<int>   *heeps_charge      =0; 
   vector<int>   *heeps_isHEEP7     =0; 
   vector<int>   *heeps_PreSelection=0; 
   vector<int>   *heeps_match       =0; 
   vector<int>   *heeps_saturated   =0; 


   vector<float> *heeps_80X_et          =0; 
   vector<float> *heeps_80X_eta         =0; 
   vector<float> *heeps_80X_sc_eta      =0; 
   vector<float> *heeps_80X_phi         =0; 
   vector<float> *heeps_80X_sc_phi      =0; 
   vector<int>   *heeps_80X_charge      =0; 
   vector<int>   *heeps_80X_isHEEP7     =0; 
   vector<int>   *heeps_80X_PreSelection=0; 

   vector<float> *muons_pt          =0; 
   vector<float> *muons_eta         =0; 
   vector<float> *muons_phi         =0; 
   vector<int>   *muons_charge      =0; 
   vector<int>   *muons_tight_ID    =0; 
   vector<int>   *muons_pfIso       =0; 

   vector<float> *jets_pt      =0;
   vector<float> *jets_eta     =0;
   vector<float> *jets_phi     =0;
   vector<float> *jets_mass    =0;
   vector<float> *jets_energy  =0;
   vector<float> *jets_CSV     =0;
   vector<int>   *jets_loose_ID=0;
 
   vector<float> *mc_electron_pt    =0;
   vector<float> *mc_electron_eta   =0;
   vector<float> *mc_electron_phi   =0;
   vector<float> *mc_electron_m     =0;
   vector<int>   *mc_electron_status=0;




   float Met_et                =0; 
   float Met_phi               =0;
   float MET_T1Txy_et          =0; 
   float MET_T1Txy_phi         =0; 
   float MET_T1Txy_significance=0; 

   int trig_Flag_HBHENoiseFilter                   =0; 
   int trig_Flag_HBHENoiseIsoFilter                =0; 
   int trig_Flag_CSCTightHaloFilter                =0; 
   int trig_Flag_CSCTightHaloTrkMuUnvetoFilter     =0; 
   int trig_Flag_CSCTightHalo2015Filter            =0; 
   int trig_Flag_globalTightHalo2016Filter         =0; 
   int trig_Flag_globalSuperTightHalo2016Filter    =0; 
   int trig_Flag_goodVertices                      =0; 
   int trig_Flag_BadPFMuonFilter                   =0; 
   int trig_Flag_BadChargedCandidateFilter         =0; 
   int trig_Flag_eeBadScFilter                     =0; 
   int trig_Flag_HcalStripHaloFilter               =0; 
   int trig_Flag_hcalLaserEventFilter              =0; 
   int trig_Flag_EcalDeadCellTriggerPrimitiveFilter=0; 
   int trig_Flag_EcalDeadCellBoundaryEnergyFilter  =0; 
   int trig_Flag_ecalLaserCorrFilter               =0; 
   int trig_Flag_chargedHadronTrackResolutionFilter=0; 
   int trig_Flag_muonBadTrackFilter                =0; 
   int trig_Flag_trkPOG_manystripclus53X           =0; 
   int trig_Flag_trkPOG_toomanystripclus53X        =0; 
   int trig_Flag_trkPOG_logErrorTooManyClusters    =0; 
   int trig_Flag_METFilters                        =0;

   float LHE_Z_mass       = 0 ;
   float w_PU_combined    = 0 ;
   float w_PU_silver_down = 0 ; 
   float w_PU_silver_up   = 0 ;

   ULong_t ev_run=0;
   ULong_t ev_event=0;
   ULong_t ev_luminosityBlock=0;
 
   t->SetBranchAddress("ev_run"                     , &ev_run                ) ;
   t->SetBranchAddress("ev_event"                   , &ev_event              ) ;
   t->SetBranchAddress("ev_luminosityBlock"         , &ev_luminosityBlock    ) ;
   t->SetBranchAddress("pv_n"                       , &pv_n                  ) ;
   t->SetBranchAddress("PU_true"                    , &PU_true               ) ;
   t->SetBranchAddress("event_sign"                 , &event_sign            ) ;
   t->SetBranchAddress("trig_Flag_HBHENoiseFilter_accept"                   , &trig_Flag_HBHENoiseFilter                     ) ;
   t->SetBranchAddress("trig_Flag_HBHENoiseIsoFilter_accept"                , &trig_Flag_HBHENoiseIsoFilter                  ) ;
   t->SetBranchAddress("trig_Flag_CSCTightHaloFilter_accept"                , &trig_Flag_CSCTightHaloFilter                  ) ;
   t->SetBranchAddress("trig_Flag_CSCTightHaloTrkMuUnvetoFilter_accept"     , &trig_Flag_CSCTightHaloTrkMuUnvetoFilter       ) ;
   t->SetBranchAddress("trig_Flag_CSCTightHalo2015Filter_accept"            , &trig_Flag_CSCTightHalo2015Filter              ) ;
   t->SetBranchAddress("trig_Flag_globalTightHalo2016Filter_accept"         , &trig_Flag_globalTightHalo2016Filter           ) ;
   t->SetBranchAddress("trig_Flag_globalSuperTightHalo2016Filter_accept"    , &trig_Flag_globalSuperTightHalo2016Filter      ) ;
   t->SetBranchAddress("trig_Flag_goodVertices_accept"                      , &trig_Flag_goodVertices                        ) ;
   t->SetBranchAddress("trig_Flag_BadPFMuonFilter_accept"                   , &trig_Flag_BadPFMuonFilter                     ) ;
   t->SetBranchAddress("trig_Flag_BadChargedCandidateFilter_accept"         , &trig_Flag_BadChargedCandidateFilter           ) ;
   t->SetBranchAddress("trig_Flag_eeBadScFilter_accept"                     , &trig_Flag_eeBadScFilter                       ) ;
   t->SetBranchAddress("trig_Flag_HcalStripHaloFilter_accept"               , &trig_Flag_HcalStripHaloFilter                 ) ;
   t->SetBranchAddress("trig_Flag_hcalLaserEventFilter_accept"              , &trig_Flag_hcalLaserEventFilter                ) ;
   t->SetBranchAddress("trig_Flag_EcalDeadCellTriggerPrimitiveFilter_accept", &trig_Flag_EcalDeadCellTriggerPrimitiveFilter  ) ;
   t->SetBranchAddress("trig_Flag_EcalDeadCellBoundaryEnergyFilter_accept"  , &trig_Flag_EcalDeadCellBoundaryEnergyFilter    ) ;
   t->SetBranchAddress("trig_Flag_ecalLaserCorrFilter_accept"               , &trig_Flag_ecalLaserCorrFilter                 ) ;
   t->SetBranchAddress("trig_Flag_chargedHadronTrackResolutionFilter_accept", &trig_Flag_chargedHadronTrackResolutionFilter  ) ;
   t->SetBranchAddress("trig_Flag_muonBadTrackFilter_accept"                , &trig_Flag_muonBadTrackFilter                  ) ;
   t->SetBranchAddress("trig_Flag_trkPOG_manystripclus53X_accept"           , &trig_Flag_trkPOG_manystripclus53X             ) ;
   t->SetBranchAddress("trig_Flag_trkPOG_toomanystripclus53X_accept"        , &trig_Flag_trkPOG_toomanystripclus53X          ) ;
   t->SetBranchAddress("trig_Flag_trkPOG_logErrorTooManyClusters_accept"    , &trig_Flag_trkPOG_logErrorTooManyClusters      ) ;
   t->SetBranchAddress("trig_Flag_METFilters_accept"                        , &trig_Flag_METFilters                          ) ;
   t->SetBranchAddress("rho"        , &rho           ) ;

   t->SetBranchAddress("trig_DEle33"               , &trig_DEle33                   ) ;
   t->SetBranchAddress("trig_DEle33_MW"            , &trig_DEle33_MW                ) ;
   t->SetBranchAddress("trig_DEle33_unseed_eta"    , &trig_DEle33_unseed_eta        ) ;
   t->SetBranchAddress("trig_DEle33_unseed_phi"    , &trig_DEle33_unseed_phi        ) ;
   t->SetBranchAddress("trig_DEle33_MW_unseed_eta" , &trig_DEle33_MW_unseed_eta     ) ;
   t->SetBranchAddress("trig_DEle33_MW_unseed_phi" , &trig_DEle33_MW_unseed_phi     ) ;
////////////////// For 80X check /////////////////////
   t->SetBranchAddress("heeps_80_et"                          , &heeps_80X_et             ) ;
   t->SetBranchAddress("heeps_80_eta"                         , &heeps_80X_eta            ) ;
   t->SetBranchAddress("heeps_80_sc_eta"                      , &heeps_80X_sc_eta         ) ;
   t->SetBranchAddress("heeps_80_phi"                         , &heeps_80X_phi            ) ;
   t->SetBranchAddress("heeps_80_sc_phi"                      , &heeps_80X_sc_phi         ) ;
   t->SetBranchAddress("heeps_80_charge"                      , &heeps_80X_charge         ) ;
   t->SetBranchAddress("heeps_80_isHEEP7"                     , &heeps_80X_isHEEP7        ) ;
   t->SetBranchAddress("heeps_80_PreSelection"                , &heeps_80X_PreSelection   ) ;

//////////////////////////////////////
   if(Regress==80){
   t->SetBranchAddress("heeps_80_et"                          , &heeps_et             ) ;
   t->SetBranchAddress("heeps_80_eta"                         , &heeps_eta            ) ;
   t->SetBranchAddress("heeps_80_sc_eta"                      , &heeps_sc_eta         ) ;
   t->SetBranchAddress("heeps_80_phi"                         , &heeps_phi            ) ;
   t->SetBranchAddress("heeps_80_sc_phi"                      , &heeps_sc_phi         ) ;
   t->SetBranchAddress("heeps_80_charge"                      , &heeps_charge         ) ;
   t->SetBranchAddress("heeps_80_isHEEP7"                     , &heeps_isHEEP7        ) ;
//   t->SetBranchAddress("heeps_80_noEcalDriven"                , &heeps_isHEEP7        ) ;
   t->SetBranchAddress("heeps_80_PreSelection"                , &heeps_PreSelection   ) ;
   t->SetBranchAddress("heeps_80_match"                       , &heeps_match          ) ;
   }
   else if (uncert=="Barrel_energy_scale_up"){        
   t->SetBranchAddress("heeps_74_B_EnScaleUp_et"              , &heeps_et             ) ;
   t->SetBranchAddress("heeps_74_B_EnScaleUp_eta"             , &heeps_eta            ) ;
   t->SetBranchAddress("heeps_74_B_EnScaleUp_sc_eta"          , &heeps_sc_eta         ) ;
   t->SetBranchAddress("heeps_74_B_EnScaleUp_phi"             , &heeps_phi            ) ;
   t->SetBranchAddress("heeps_74_B_EnScaleUp_sc_phi"          , &heeps_sc_phi         ) ;
   t->SetBranchAddress("heeps_74_B_EnScaleUp_charge"          , &heeps_charge         ) ;
   t->SetBranchAddress("heeps_74_B_EnScaleUp_isHEEP7"         , &heeps_isHEEP7        ) ;
   t->SetBranchAddress("heeps_74_B_EnScaleUp_PreSelection"    , &heeps_PreSelection   ) ;
   }
   else if (uncert=="Barrel_energy_scale_down"){        
   t->SetBranchAddress("heeps_74_B_EnScaleDown_et"            , &heeps_et             ) ;
   t->SetBranchAddress("heeps_74_B_EnScaleDown_eta"           , &heeps_eta            ) ;
   t->SetBranchAddress("heeps_74_B_EnScaleDown_sc_eta"        , &heeps_sc_eta         ) ;
   t->SetBranchAddress("heeps_74_B_EnScaleDown_phi"           , &heeps_phi            ) ;
   t->SetBranchAddress("heeps_74_B_EnScaleDown_sc_phi"        , &heeps_sc_phi         ) ;
   t->SetBranchAddress("heeps_74_B_EnScaleDown_charge"        , &heeps_charge         ) ;
   t->SetBranchAddress("heeps_74_B_EnScaleDown_isHEEP7"       , &heeps_isHEEP7        ) ;
   t->SetBranchAddress("heeps_74_B_EnScaleDown_PreSelection"  , &heeps_PreSelection   ) ;
   }
   else if (uncert=="Endcap_energy_scale_up"){        
   t->SetBranchAddress("heeps_74_E_EnScaleUp_et"              , &heeps_et             ) ;
   t->SetBranchAddress("heeps_74_E_EnScaleUp_eta"             , &heeps_eta            ) ;
   t->SetBranchAddress("heeps_74_E_EnScaleUp_sc_eta"          , &heeps_sc_eta         ) ;
   t->SetBranchAddress("heeps_74_E_EnScaleUp_phi"             , &heeps_phi            ) ;
   t->SetBranchAddress("heeps_74_E_EnScaleUp_sc_phi"          , &heeps_sc_phi         ) ;
   t->SetBranchAddress("heeps_74_E_EnScaleUp_charge"          , &heeps_charge         ) ;
   t->SetBranchAddress("heeps_74_E_EnScaleUp_isHEEP7"         , &heeps_isHEEP7        ) ;
   t->SetBranchAddress("heeps_74_E_EnScaleUp_PreSelection"    , &heeps_PreSelection   ) ;
   }
   else if (uncert=="Endcap_energy_scale_down"){        
   t->SetBranchAddress("heeps_74_E_EnScaleDown_et"            , &heeps_et             ) ;
   t->SetBranchAddress("heeps_74_E_EnScaleDown_eta"           , &heeps_eta            ) ;
   t->SetBranchAddress("heeps_74_E_EnScaleDown_sc_eta"        , &heeps_sc_eta         ) ;
   t->SetBranchAddress("heeps_74_E_EnScaleDown_phi"           , &heeps_phi            ) ;
   t->SetBranchAddress("heeps_74_E_EnScaleDown_sc_phi"        , &heeps_sc_phi         ) ;
   t->SetBranchAddress("heeps_74_E_EnScaleDown_charge"        , &heeps_charge         ) ;
   t->SetBranchAddress("heeps_74_E_EnScaleDown_isHEEP7"       , &heeps_isHEEP7        ) ;
   t->SetBranchAddress("heeps_74_E_EnScaleDown_PreSelection"  , &heeps_PreSelection   ) ;
   }
   else{
   t->SetBranchAddress("heeps_74_et"                          , &heeps_et             ) ;
   t->SetBranchAddress("heeps_74_eta"                         , &heeps_eta            ) ;
   t->SetBranchAddress("heeps_74_sc_eta"                      , &heeps_sc_eta         ) ;
   t->SetBranchAddress("heeps_74_phi"                         , &heeps_phi            ) ;
   t->SetBranchAddress("heeps_74_sc_phi"                      , &heeps_sc_phi         ) ;
   t->SetBranchAddress("heeps_74_charge"                      , &heeps_charge         ) ;
   t->SetBranchAddress("heeps_74_isHEEP7"                     , &heeps_isHEEP7        ) ;
   t->SetBranchAddress("heeps_74_PreSelection"                , &heeps_PreSelection   ) ;
   t->SetBranchAddress("heeps_74_match"                       , &heeps_match          ) ;
   t->SetBranchAddress("heeps_74_saturated"                   , &heeps_saturated      ) ;
   }
   t->SetBranchAddress("muons_pt"            , &muons_pt                    ) ;
   t->SetBranchAddress("muons_eta"           , &muons_eta                   ) ;
   t->SetBranchAddress("muons_phi"           , &muons_phi                   ) ;
   t->SetBranchAddress("muons_charge"        , &muons_charge                ) ;
   t->SetBranchAddress("muons_tight_ID"      , &muons_tight_ID              ) ;
   t->SetBranchAddress("muons_pfIso"         , &muons_pfIso                 ) ;
   t->SetBranchAddress("jets_pt"             , &jets_pt                     ) ;
   t->SetBranchAddress("jets_eta"            , &jets_eta                    ) ;
   t->SetBranchAddress("jets_phi"            , &jets_phi                    ) ;
   t->SetBranchAddress("jets_mass"           , &jets_mass                   ) ;
   t->SetBranchAddress("jets_energy"         , &jets_energy                 ) ;
   t->SetBranchAddress("jets_CSV"            , &jets_CSV                    ) ;
   t->SetBranchAddress("jets_loose_ID"       , &jets_loose_ID               ) ;
   t->SetBranchAddress("Met_et"                , &Met_et                 ) ;
   t->SetBranchAddress("Met_phi"               , &Met_phi                ) ;
   t->SetBranchAddress("MET_T1Txy_et"          , &MET_T1Txy_et           ) ;
   t->SetBranchAddress("MET_T1Txy_phi"         , &MET_T1Txy_phi          ) ;
   t->SetBranchAddress("MET_T1Txy_significance", &MET_T1Txy_significance ) ;

   t->SetBranchAddress("LHE_Z_mass"      , &LHE_Z_mass        ) ;

   t->SetBranchAddress("w_PU_combined"   , &w_PU_combined     ) ;
   t->SetBranchAddress("w_PU_silver_up"  , &w_PU_silver_up    ) ;
   t->SetBranchAddress("w_PU_silver_down", &w_PU_silver_down  ) ;

   t->SetBranchAddress("mc_electron_pt"     , &mc_electron_pt      ) ;
   t->SetBranchAddress("mc_electron_eta"    , &mc_electron_eta     );
   t->SetBranchAddress("mc_electron_phi"    , &mc_electron_phi     );
   t->SetBranchAddress("mc_electron_m"      , &mc_electron_m       );
   t->SetBranchAddress("mc_electron_status" , &mc_electron_status  );


///

const int N_mee_bin=111;
float mee_bin_edge[N_mee_bin];
int index=0;
for(int i=50;i<120;i+=5)    {mee_bin_edge[index]=i;index++;}//14
for(int i=120;i<150;i+=5)   {mee_bin_edge[index]=i;index++;}//6
for(int i=150;i<200;i+=10)  {mee_bin_edge[index]=i;index++;}//5
for(int i=200;i<600;i+=20)  {mee_bin_edge[index]=i;index++;}//20
for(int i=600;i<900;i+=30)  {mee_bin_edge[index]=i;index++;}//10
for(int i=900;i<1250;i+=50) {mee_bin_edge[index]=i;index++;}//7
for(int i=1250;i<1600;i+=60){mee_bin_edge[index]=i;index++;}//6
for(int i=1600;i<1900;i+=70){mee_bin_edge[index]=i;index++;}//5   
for(int i=1900;i<4000;i+=80){mee_bin_edge[index]=i;index++;}//27
for(int i=4000;i<5000;i+=100){mee_bin_edge[index]=i;index++;}//10
mee_bin_edge[index]=5000;//1
///

const int N_mee_bin_sin=63;
float mee_bin_edge_sin[N_mee_bin_sin];
int index_sin=0;
for(int i=200;i<600;i+=20)  {mee_bin_edge_sin[index_sin]=i;index_sin++;}//20
for(int i=600;i<900;i+=30)  {mee_bin_edge_sin[index_sin]=i;index_sin++;}//10
for(int i=900;i<1250;i+=50) {mee_bin_edge_sin[index_sin]=i;index_sin++;}//7
for(int i=1250;i<1600;i+=60){mee_bin_edge_sin[index_sin]=i;index_sin++;}//6
for(int i=1600;i<1900;i+=70){mee_bin_edge_sin[index_sin]=i;index_sin++;}//5   
for(int i=1900;i<3000;i+=80){mee_bin_edge_sin[index_sin]=i;index_sin++;}//14
                             mee_bin_edge_sin[index_sin]=3000;//1
//////// For A_FB ///////////////////
const int N_mee_AFB_bin=39;
float mee_AFB_bin_edge[N_mee_AFB_bin];
int index_AFB=0;
for(int i=50;i<120;i+=5)    {mee_AFB_bin_edge[index_AFB]=i;index_AFB++;}//14
for(int i=120;i<150;i+=5)   {mee_AFB_bin_edge[index_AFB]=i;index_AFB++;}//6
for(int i=150;i<200;i+=10)  {mee_AFB_bin_edge[index_AFB]=i;index_AFB++;}//5
for(int i=200;i<400;i+=20)  {mee_AFB_bin_edge[index_AFB]=i;index_AFB++;}//10
mee_AFB_bin_edge[index_AFB]=500;index_AFB++;//1
mee_AFB_bin_edge[index_AFB]=700;index_AFB++;//1
mee_AFB_bin_edge[index_AFB]=1000;index_AFB++;//1
mee_AFB_bin_edge[index_AFB]=3000;index_AFB++;//1
///

float mee_ss_bin[18]={70,75,80,85,90,95,100,200,300,400,500,600,700,800,900,1000,1500,4000};

TH1D *h_mee_all            =new TH1D("h_mee_all",""   ,N_mee_bin-1,mee_bin_edge);
TH1D *h_mee_all_BB         =new TH1D("h_mee_all_BB","",N_mee_bin-1,mee_bin_edge);
TH1D *h_mee_all_BE         =new TH1D("h_mee_all_BE","",N_mee_bin-1,mee_bin_edge);
TH1D *h_mee_all_EE         =new TH1D("h_mee_all_EE","",N_mee_bin-1,mee_bin_edge);
TH1D *h_mee_all_AS         =new TH1D("h_mee_all_AS",""   ,17,mee_ss_bin);
TH1D *h_mee_all_SS         =new TH1D("h_mee_all_SS",""   ,17,mee_ss_bin);
TH1D *h_mee_all_BB_AS      =new TH1D("h_mee_all_BB_AS","",17,mee_ss_bin);
TH1D *h_mee_all_BB_SS      =new TH1D("h_mee_all_BB_SS","",17,mee_ss_bin);
TH1D *h_mee_all_BE_AS      =new TH1D("h_mee_all_BE_AS","",17,mee_ss_bin);
TH1D *h_mee_all_BE_SS      =new TH1D("h_mee_all_BE_SS","",17,mee_ss_bin);
TH1D *h_mee_all_EE_AS      =new TH1D("h_mee_all_EE_AS","",17,mee_ss_bin);
TH1D *h_mee_all_EE_SS      =new TH1D("h_mee_all_EE_SS","",17,mee_ss_bin);
TH1D *h_mee_all_sin        =new TH1D("h_mee_all_sin",""   ,N_mee_bin_sin-1,mee_bin_edge_sin);
TH1D *h_mee_all_BB_sin     =new TH1D("h_mee_all_BB_sin","",N_mee_bin_sin-1,mee_bin_edge_sin);
TH1D *h_mee_all_BE_sin     =new TH1D("h_mee_all_BE_sin","",N_mee_bin_sin-1,mee_bin_edge_sin);
TH1D *h_mee_all_EE_sin     =new TH1D("h_mee_all_EE_sin","",N_mee_bin_sin-1,mee_bin_edge_sin);
TH1D *h_mee_all_cum        =new TH1D("h_mee_all_cumlative",""     ,247,60,5000);
TH1D *h_mee_all_cum_BE     =new TH1D("h_mee_all_cumlative_BE",""  ,247,60,5000);
TH1D *h_mee_all_cum_BB     =new TH1D("h_mee_all_cumlative_BB",""  ,247,60,5000);
TH1D *h_mee_all_cum_EE     =new TH1D("h_mee_all_cumlative_EE",""  ,247,60,5000);
TH1D *h_mee_all_cum_v1     =new TH1D("h_mee_all_cumlative_v1",""    ,N_mee_bin-1,mee_bin_edge );
TH1D *h_mee_all_cum_BE_v1  =new TH1D("h_mee_all_cumlative_BE_v1","" ,N_mee_bin-1,mee_bin_edge );
TH1D *h_mee_all_cum_BB_v1  =new TH1D("h_mee_all_cumlative_BB_v1","" ,N_mee_bin-1,mee_bin_edge );
TH1D *h_mee_all_cum_EE_v1  =new TH1D("h_mee_all_cumlative_EE_v1","" ,N_mee_bin-1,mee_bin_edge );
//////////////////
TH1D *h_mee_cosp           =new TH1D("h_mee_cosp",""   ,N_mee_bin-1,mee_bin_edge);
TH1D *h_mee_cosp_BB        =new TH1D("h_mee_cosp_BB","",N_mee_bin-1,mee_bin_edge);
TH1D *h_mee_cosp_BE        =new TH1D("h_mee_cosp_BE","",N_mee_bin-1,mee_bin_edge);
TH1D *h_mee_cosp_EE        =new TH1D("h_mee_cosp_EE","",N_mee_bin-1,mee_bin_edge);
TH1D *h_mee_cosm           =new TH1D("h_mee_cosm",""   ,N_mee_bin-1,mee_bin_edge);
TH1D *h_mee_cosm_BB        =new TH1D("h_mee_cosm_BB","",N_mee_bin-1,mee_bin_edge);
TH1D *h_mee_cosm_BE        =new TH1D("h_mee_cosm_BE","",N_mee_bin-1,mee_bin_edge);
TH1D *h_mee_cosm_EE        =new TH1D("h_mee_cosm_EE","",N_mee_bin-1,mee_bin_edge);
TH1D *h_cos_all_region     =new TH1D("h_cos_all_region","",100,-1,1);
TH1D *h_cos                =new TH1D("h_cos"           ,"",100,-1,1);
TH1D *h_cos_BB             =new TH1D("h_cos_BB"        ,"",100,-1,1);
TH1D *h_cos_BE             =new TH1D("h_cos_BE"        ,"",100,-1,1);
TH1D *h_cos_EE             =new TH1D("h_cos_EE"        ,"",100,-1,1);
////////////////
TH1D *h_mee_fine           =new TH1D("h_mee_fine","" ,4000,0,4000);
TH1D *h_mee_BB_fine        =new TH1D("h_mee_BB_fine","" ,4000,0,4000);
TH1D *h_mee_BE_fine        =new TH1D("h_mee_BE_fine","" ,4000,0,4000);
TH1D *h_mee_EE_fine        =new TH1D("h_mee_EE_fine","" ,4000,0,4000);
TH1D *h_mee_cosp_all_fine  =new TH1D("h_mee_cosp_all_fine","" ,N_mee_AFB_bin-1,mee_AFB_bin_edge);
TH1D *h_mee_cosp_fine      =new TH1D("h_mee_cosp_fine"    ,"" ,N_mee_AFB_bin-1,mee_AFB_bin_edge);
TH1D *h_mee_cosp_BB_fine   =new TH1D("h_mee_cosp_BB_fine" ,"" ,N_mee_AFB_bin-1,mee_AFB_bin_edge);
TH1D *h_mee_cosp_BE_fine   =new TH1D("h_mee_cosp_BE_fine" ,"" ,N_mee_AFB_bin-1,mee_AFB_bin_edge);
TH1D *h_mee_cosp_EE_fine   =new TH1D("h_mee_cosp_EE_fine" ,"" ,N_mee_AFB_bin-1,mee_AFB_bin_edge);
TH1D *h_mee_cosm_all_fine  =new TH1D("h_mee_cosm_all_fine","" ,N_mee_AFB_bin-1,mee_AFB_bin_edge);
TH1D *h_mee_cosm_fine      =new TH1D("h_mee_cosm_fine"    ,"" ,N_mee_AFB_bin-1,mee_AFB_bin_edge);
TH1D *h_mee_cosm_BB_fine   =new TH1D("h_mee_cosm_BB_fine" ,"" ,N_mee_AFB_bin-1,mee_AFB_bin_edge);
TH1D *h_mee_cosm_BE_fine   =new TH1D("h_mee_cosm_BE_fine" ,"" ,N_mee_AFB_bin-1,mee_AFB_bin_edge);
TH1D *h_mee_cosm_EE_fine   =new TH1D("h_mee_cosm_EE_fine" ,"" ,N_mee_AFB_bin-1,mee_AFB_bin_edge);
TH1D *h_mee_usual          =new TH1D("h_mee_usual"   ,"" ,400,0,4000);
TH1D *h_mee_BB_usual       =new TH1D("h_mee_BB_usual","" ,400,0,4000);
TH1D *h_mee_BE_usual       =new TH1D("h_mee_BE_usual","" ,400,0,4000);
TH1D *h_mee_EE_usual       =new TH1D("h_mee_EE_usual","" ,400,0,4000);
TH1D *h_mee_Zpeak          =new TH1D("h_mee_Zpeak"   ,"",60,60,120);
TH1D *h_mee_Zpeak_BB       =new TH1D("h_mee_Zpeak_BB","",60,60,120);
TH1D *h_mee_Zpeak_BB_v1    =new TH1D("h_mee_Zpeak_BB_v1","",120,60,120);
TH1D *h_mee_Zpeak_BE       =new TH1D("h_mee_Zpeak_BE","",60,60,120);
TH1D *h_mee_Zpeak_BE_v1    =new TH1D("h_mee_Zpeak_BE_v1","",120,60,120);
TH1D *h_mee_Zpeak_EE       =new TH1D("h_mee_Zpeak_EE","",60,60,120);
TH1D *h_mee_cosp_usual     =new TH1D("h_mee_cosp_usual"   ,"" ,400,0,4000);
TH1D *h_mee_cosp_BB_usual  =new TH1D("h_mee_cosp_BB_usual","" ,400,0,4000);
TH1D *h_mee_cosp_BE_usual  =new TH1D("h_mee_cosp_BE_usual","" ,400,0,4000);
TH1D *h_mee_cosp_EE_usual  =new TH1D("h_mee_cosp_EE_usual","" ,400,0,4000);
TH1D *h_mee_cosm_usual     =new TH1D("h_mee_cosm_usual"   ,"" ,400,0,4000);
TH1D *h_mee_cosm_BB_usual  =new TH1D("h_mee_cosm_BB_usual","" ,400,0,4000);
TH1D *h_mee_cosm_BE_usual  =new TH1D("h_mee_cosm_BE_usual","" ,400,0,4000);
TH1D *h_mee_cosm_EE_usual  =new TH1D("h_mee_cosm_EE_usual","" ,400,0,4000);

TH1D *h_mee_fail_MET       =new TH1D("h_mee_fail_MET","",197,60,4000);

TH1D *h_pv_n               =new TH1D("h_pv_n","",100,0,100);
TH1D *h_rho                =new TH1D("h_rho" ,"",80,0,40);
TH1D *h_Ptll               =new TH1D("h_Ptll" ,"",75 ,0,150);
TH1D *h_Etall              =new TH1D("h_Etall","",100,-5,5 );
TH1D *h_Phill              =new TH1D("h_Phill" ,"",80 ,-4,4);
TH1D *h_led_Et             =new TH1D("h_led_Et","",60,35,635);
TH1D *h_led_eta            =new TH1D("h_led_eta","",60,-3,3);
TH1D *h_led_phi            =new TH1D("h_led_phi","",100,-5,5);
TH1D *h_sub_Et             =new TH1D("h_sub_Et","",60,35,635);
TH1D *h_sub_eta            =new TH1D("h_sub_eta","",60,-3,3);
TH1D *h_sub_phi            =new TH1D("h_sub_phi","",100,-5,5);
TH1D *h_MET                =new TH1D("h_MET"     ,"",100,0,300);
TH1D *h_MET_phi            =new TH1D("h_MET_phi" ,"",80 ,-4,4);
TH1D *h_MET_T1Txy          =new TH1D("h_MET_T1Txy" ,"",100,0,300);
TH1D *h_MET_phi_T1Txy      =new TH1D("h_MET_phi_T1Txy","",80 ,-4,4);
TH1D *h_MET_SF_T1Txy       =new TH1D("h_MET_SF_T1Txy","",100 ,0,10);
TH1D *h_MET_Filter         =new TH1D("h_MET_Filter"  ,"",2  ,0,2);
TH1D *h_N_jet              =new TH1D("h_N_jet"       ,"",7  ,0,7);
TH1D *h_N_bjet             =new TH1D("h_N_bjet"      ,"",4  ,0,4);
TH1D *h_Dphi_ll            =new TH1D("h_Dphi_ll"     ,"",40,0,4);
TH1D *h_DR_ll              =new TH1D("h_DR_ll"       ,"",60,0,6);
TH1D *h_Dphi_MET_Z         =new TH1D("h_Dphi_MET_Z"  ,"",40,0,4);
TH1D *h_HT_sys             =new TH1D("h_HT_sys"      ,"",100,0,500);
TH1D *h_Pt_sys             =new TH1D("h_Pt_sys"      ,"",100,0,500);

TH1D *h_MET_Filter_detail  =new TH1D("h_MET_Filter_detail" ,"",10  ,0,10);

TH1D *h_resolution         =new TH1D("h_resolution"    ,"",600  ,-1,2);
TH1D *h_resolution_BB      =new TH1D("h_resolution_BB" ,"",600  ,-1,2);
TH1D *h_resolution_BE      =new TH1D("h_resolution_BE" ,"",600  ,-1,2);

TFile *f_ele_eff = new TFile("/user/wenxing/ST_TW_channel/CMSSW_9_4_0/src/Zprime/scripts/root_eff_ZToEE.root");
TH1F  *h_eff_BB  = (TH1F*)f_ele_eff->Get("h_acceff_ZToEE_eff_BB");
TH1F  *h_eff_BE  = (TH1F*)f_ele_eff->Get("h_acceff_ZToEE_eff_BE");

TRandom3 rand ;

double event_weight=1;

map<int,int> ele_indexs;

std::cout<<"total event="<<t->GetEntries()<<std::endl;

for(int i=0;i<t->GetEntries();i++){
if(i%1000000==0)std::cout<<"processed:"<<100*i/t->GetEntries()<<"%"<<std::endl;
t->GetEntry(i);
ele_indexs.clear();
////////////////////////////////////////////////////// 1F ////////////////////////////
if(do_FR_1F==true){
int dummy=1;
}
///////////////////////////////////////////////////// 2F //////////////////////////////////
else if(do_FR_2F==true){
int dummy=1;
}
///////////////////////////////////////////////////////////// Nonimal ////////////////////////////
else{
float max_sum_et=0;
int index_1=-1;
int index_2=-1;
int N_status_23=0;
for(unsigned int j=0;j<mc_electron_pt->size();j++){
if(mc_electron_status->at(j)==23) N_status_23++;
}
////////////////////////////
if(N_status_23==0){
for(unsigned int j=0;j<mc_electron_pt->size();j++){
if(mc_electron_status->at(j)!=1 || mc_electron_pt->at(j)<35 || (fabs(mc_electron_eta->at(j))>2.5 || (fabs(mc_electron_eta->at(j))>1.4442 && fabs(mc_electron_eta->at(j))<1.566) ) ) continue;
for(unsigned int k=j+1;k<mc_electron_pt->size();k++){
if(mc_electron_status->at(k)!=1 || mc_electron_pt->at(k)<35 || (fabs(mc_electron_eta->at(k))>2.5 || (fabs(mc_electron_eta->at(k))>1.4442 && fabs(mc_electron_eta->at(k))<1.566) ) ) continue;
if((mc_electron_pt->at(j)+mc_electron_pt->at(k))>max_sum_et) {max_sum_et=mc_electron_pt->at(j)+mc_electron_pt->at(k);
                                                              index_1=j;
                                                              index_2=k;}
}
}
}
///////////////
else if(N_status_23==1){
for(unsigned int j=0;j<mc_electron_pt->size();j++){
if(mc_electron_status->at(j)!=23 || mc_electron_pt->at(j)<35 || (fabs(mc_electron_eta->at(j))>2.5 || (fabs(mc_electron_eta->at(j))>1.4442 && fabs(mc_electron_eta->at(j))<1.566) ) ) continue;
for(unsigned int k=0;k<mc_electron_pt->size();k++){
if(k==j || mc_electron_status->at(k)!=1 || mc_electron_pt->at(k)<35 || (fabs(mc_electron_eta->at(k))>2.5 || (fabs(mc_electron_eta->at(k))>1.4442 && fabs(mc_electron_eta->at(k))<1.566) ) ) continue;
if((mc_electron_pt->at(j)+mc_electron_pt->at(k))>max_sum_et) {max_sum_et=mc_electron_pt->at(j)+mc_electron_pt->at(k);
                                                              index_1=j;
                                                              index_2=k;}
}
}
}
///////////////
else{
for(unsigned int j=0;j<mc_electron_pt->size();j++){
if(mc_electron_status->at(j)!=23 || mc_electron_pt->at(j)<35 || (fabs(mc_electron_eta->at(j))>2.5 || (fabs(mc_electron_eta->at(j))>1.4442 && fabs(mc_electron_eta->at(j))<1.566) ) ) continue;
for(unsigned int k=j+1;k<mc_electron_pt->size();k++){
if(mc_electron_status->at(k)!=23 || mc_electron_pt->at(k)<35 || (fabs(mc_electron_eta->at(k))>2.5 || (fabs(mc_electron_eta->at(k))>1.4442 && fabs(mc_electron_eta->at(k))<1.566) ) ) continue;
if((mc_electron_pt->at(j)+mc_electron_pt->at(k))>max_sum_et) {max_sum_et=mc_electron_pt->at(j)+mc_electron_pt->at(k);
                                                              index_1=j;
                                                              index_2=k;}
}
}
}
///////////////
if(index_1!=-1 && index_2!=-1){
ele_indexs.insert(map<int,int>::value_type(index_1, index_2));
}
}//else

//////////////////////// MET Filter //////////


/////////////////////// fill histograms///////////////////////////////////////////////

for(map<int,int>::iterator iter = ele_indexs.begin( ); iter != ele_indexs.end( ); iter++ ){
int e1_index=iter->first;
int e2_index=iter->second;
TLorentzVector e1(0,0,0,0);
TLorentzVector e2(0,0,0,0);
e1.SetPtEtaPhiM(mc_electron_pt->at(e1_index),mc_electron_eta->at(e1_index),mc_electron_phi->at(e1_index),mc_electron_m->at(e1_index));
e2.SetPtEtaPhiM(mc_electron_pt->at(e2_index),mc_electron_eta->at(e2_index),mc_electron_phi->at(e2_index),mc_electron_m->at(e1_index));
TLorentzVector Zee=e1+e2;
float e1_et=mc_electron_pt->at(e1_index);
float e2_et=mc_electron_pt->at(e2_index);
float e1_sc_eta=mc_electron_eta->at(e1_index);
float e2_sc_eta=mc_electron_eta->at(e2_index);
float mee=Zee.M();
////////  efficiency /////////////
TAxis *xaxis_BB = h_eff_BB->GetXaxis();
TAxis *xaxis_BE = h_eff_BE->GetXaxis();
float efficiency=0;
////////  resolution /////////////
bool is_BB=false;
if(fabs(e1_sc_eta)<1.4442 && fabs(e2_sc_eta)<1.4442){ is_BB=true;
                                                     Int_t binx = xaxis_BB->FindBin(mee); 
                                                     efficiency=h_eff_BB->GetBinContent(binx);
                                                    }
else                                                { is_BB=false;
                                                     Int_t binx = xaxis_BE->FindBin(mee); 
                                                     efficiency=h_eff_BE->GetBinContent(binx);
                                                    }
Resolution::dCB.get_value(mee,is_BB);
float sigma=Resolution::dCB.sigma;
float mean =Resolution::dCB.mean ;
//std::cout<<"sigma="<<sigma<<",mean="<<mean<<std::endl;
mee = mee*rand.Gaus(mean+1,sigma) ;
//std::cout<<"mee="<<mee<<std::endl;
///////////// calcCosThetaCSAnal ////////////
double CosThetaCS=0;
int same_sign=0;
//////////////////////// PU ///////////////////////////
///////////////////////////// fake rate ////////////////
///////////////////////// mass scale //////////////////////
////////////////// fewz ////////////////////////////
//////////////// pdf uncertainty //////////////////
//////////////////////////////////////////////////////
event_weight=event_sign*efficiency;
TAxis *xaxis = h_mee_all->GetXaxis();
Int_t binx = xaxis->FindBin(mee);
Float_t bin_width=h_mee_all->GetXaxis()->GetBinWidth(binx);
float cos_mee_cut=200;
int barrel_barrel=0;
int cos_region=0;

if(fabs(e1_sc_eta)>2.5 || fabs(e2_sc_eta)>2.5 || (fabs(e1_sc_eta)>1.4442 && fabs(e1_sc_eta) <1.566) || (fabs(e2_sc_eta)>1.4442 && fabs(e2_sc_eta) <1.566) ) continue;
else if(fabs(e1_sc_eta)>1.566 && fabs(e1_sc_eta)<2.5 && fabs(e2_sc_eta)>1.566 && fabs(e2_sc_eta)<2.5 ) {
h_mee_Zpeak_EE->Fill(mee,event_weight);
h_mee_all_EE->Fill(mee,event_weight/bin_width);
h_mee_all_EE_sin->Fill(mee,event_weight);
h_mee_EE_usual->Fill(  mee,event_weight);   
h_mee_EE_fine ->Fill(  mee,event_weight);   
h_mee_all_EE_AS->Fill(mee,event_weight);
if(same_sign==0){
if(CosThetaCS>0) {h_mee_cosp_EE->Fill(mee,event_weight/bin_width);
                  h_mee_cosp_EE_fine->Fill(mee,event_weight);
                  h_mee_cosp_all_fine->Fill(mee,event_weight);
                  h_mee_cosp_EE_usual->Fill( mee,event_weight);
                 }
else             {h_mee_cosm_EE->Fill(mee,event_weight/bin_width);
                  h_mee_cosm_EE_fine->Fill(mee,event_weight);
                  h_mee_cosm_all_fine->Fill(mee,event_weight);
                  h_mee_cosm_EE_usual->Fill( mee,event_weight);
                 }
if(mee>cos_mee_cut ){h_cos_EE->Fill(CosThetaCS,event_weight);
                     h_cos_all_region->Fill(CosThetaCS,event_weight);//for all region
                    }
}
else{
h_mee_all_EE_SS->Fill(mee,event_weight);
}
fill_cum(h_mee_all_cum_EE   , mee , event_weight);
fill_cum(h_mee_all_cum_EE_v1, mee , event_weight);
continue;
}
else if(fabs(e1_sc_eta)<1.4442 && fabs(e2_sc_eta)<1.4442){
                                               if(uncert=="BB_mass_scale_up")mee=(mee>0) ? 1.02*mee :1.005*mee;
                                               else if(uncert=="BB_mass_scale_down")mee=(mee>0) ? 0.98*mee : 0.995*mee;
                                               barrel_barrel=1;
                                               h_mee_Zpeak_BB->Fill(mee,event_weight);
                                               h_mee_Zpeak_BB_v1->Fill(mee,event_weight);
                                               h_mee_all_BB->Fill(mee,event_weight/bin_width);
                                               h_mee_all_BB_sin->Fill(mee,event_weight);
                                               h_mee_BB_usual->Fill(  mee,event_weight);
                                               h_mee_BB_fine ->Fill(  mee,event_weight);
                                               h_mee_all_BB_AS->Fill(mee,event_weight);
                                               if(same_sign==0){
                                               if(CosThetaCS>0) {h_mee_cosp_BB->Fill(mee,event_weight/bin_width);
                                                                 h_mee_cosp_BB_fine->Fill(mee,event_weight);
                                                                 h_mee_cosp_all_fine->Fill(mee,event_weight);
                                                                 cos_region=1;
                                                                 h_mee_cosp_BB_usual->Fill( mee,event_weight);
                                                                }
                                               else             {h_mee_cosm_BB->Fill(mee,event_weight/bin_width);
                                                                 h_mee_cosm_BB_fine->Fill(mee,event_weight);
                                                                 h_mee_cosm_all_fine->Fill(mee,event_weight);
                                                                 cos_region=2;
                                                                 h_mee_cosm_BB_usual->Fill( mee,event_weight);
                                                                }
                                               if(mee>cos_mee_cut) {h_cos_BB->Fill(CosThetaCS,event_weight);
                                                                    h_cos_all_region->Fill(CosThetaCS,event_weight);//for all region
                                                                   }
                                               }
                                               else{
                                               h_mee_all_BB_SS->Fill(mee,event_weight);
                                               }
                                               fill_cum(h_mee_all_cum_BB   , mee , event_weight);
                                               fill_cum(h_mee_all_cum_BB_v1, mee , event_weight);
                                                         }

else if( (fabs(e1_sc_eta)<1.4442 && (fabs(e2_sc_eta)>1.566 && fabs(e2_sc_eta)<2.5)) || (fabs(e2_sc_eta)<1.4442 && (fabs(e1_sc_eta)>1.566 && fabs(e1_sc_eta)<2.5)) ){
                                                                          if(uncert=="BE_mass_scale_up")mee=(mee>0) ? 1.01*mee: 1.0025*mee ;
                                                                          else if(uncert=="BE_mass_scale_down")mee=(mee>0) ? 0.99*mee: 0.9975*mee;
                                                                          h_mee_Zpeak_BE->Fill(mee,event_weight);
                                                                          h_mee_Zpeak_BE_v1->Fill(mee,event_weight);
                                                                          h_mee_all_BE->Fill(mee,event_weight/bin_width);
                                                                          h_mee_all_BE_sin->Fill(mee,event_weight);
                                                                          h_mee_BE_usual->Fill(  mee,event_weight);
                                                                          h_mee_BE_fine ->Fill(  mee,event_weight);
                                                                          h_mee_all_BE_AS->Fill(mee,event_weight);
                                                                          if(same_sign==0){
                                                                          if(CosThetaCS>0) {h_mee_cosp_BE->Fill(mee,event_weight/bin_width);
                                                                                            h_mee_cosp_BE_fine->Fill(mee,event_weight);
                                                                                            h_mee_cosp_all_fine->Fill(mee,event_weight);
                                                                                            cos_region=3;
                                                                                            h_mee_cosp_BE_usual->Fill( mee,event_weight);
                                                                                           }
                                                                          else             {h_mee_cosm_BE->Fill(mee,event_weight/bin_width);
                                                                                            h_mee_cosm_BE_fine->Fill(mee,event_weight);
                                                                                            h_mee_cosm_all_fine->Fill(mee,event_weight);
                                                                                            cos_region=4;
                                                                                            h_mee_cosm_BE_usual->Fill( mee,event_weight);
                                                                                           }
                                                                          if(mee>cos_mee_cut ){h_cos_BE->Fill(CosThetaCS,event_weight);
                                                                                               h_cos_all_region->Fill(CosThetaCS,event_weight);//for all region
                                                                                              }
                                                                          }
                                                                          else{
                                                                          h_mee_all_BE_SS->Fill(mee,event_weight);
                                                                          } 
                                                                          fill_cum(h_mee_all_cum_BE   , mee , event_weight);
                                                                          fill_cum(h_mee_all_cum_BE_v1, mee , event_weight);
                                                                                                                                                                    }

h_mee_Zpeak->Fill(mee,event_weight);
h_mee_all->Fill(mee,event_weight/bin_width);
h_mee_all_sin->Fill(mee,event_weight);
h_mee_usual->Fill(  mee,event_weight);
h_mee_fine ->Fill(  mee,event_weight);

h_mee_all_AS->Fill(mee,event_weight);
if(same_sign==0){
if(CosThetaCS>0) {h_mee_cosp->Fill(mee,event_weight/bin_width);
                  h_mee_cosp_fine->Fill(mee,event_weight);
                  h_mee_cosp_usual->Fill( mee,event_weight);
                 }
else             {h_mee_cosm->Fill(mee,event_weight/bin_width);
                  h_mee_cosm_fine->Fill(mee,event_weight);
                  h_mee_cosm_usual->Fill( mee,event_weight);
                 }
if(mee>cos_mee_cut)h_cos->Fill(CosThetaCS,event_weight);
}
else{
h_mee_all_SS->Fill(mee,event_weight);
}
fill_cum(h_mee_all_cum   , mee , event_weight);
fill_cum(h_mee_all_cum_v1, mee , event_weight);

if(mee<200) continue;
 
h_Ptll   ->Fill(Zee.Pt() ,event_weight);
h_Etall  ->Fill(Zee.Eta(),event_weight);
h_Phill  ->Fill(Zee.Phi(),event_weight);
h_pv_n   ->Fill(pv_n    ,event_weight);
h_rho    ->Fill(rho     ,event_weight);
if(e1_et>e2_et){
h_led_Et ->Fill(e1.Pt() ,event_weight);
h_led_eta->Fill(e1.Eta(),event_weight);
h_led_phi->Fill(e1.Phi(),event_weight);
h_sub_Et ->Fill(e2.Pt() ,event_weight);
h_sub_eta->Fill(e2.Eta(),event_weight);
h_sub_phi->Fill(e2.Phi(),event_weight);
              }
else{
h_led_Et ->Fill(e2.Pt() ,event_weight);
h_led_eta->Fill(e2.Eta(),event_weight);
h_led_phi->Fill(e2.Phi(),event_weight);
h_sub_Et ->Fill(e1.Pt() ,event_weight);
h_sub_eta->Fill(e1.Eta(),event_weight);
h_sub_phi->Fill(e1.Phi(),event_weight);
    }
float Dphi_ll   =(fabs(e1.Phi()-e2.Phi())<PI_F) ? fabs(e1.Phi()-e2.Phi()) : (2*PI_F-fabs(e1.Phi()-e2.Phi())) ;
float Dphi_MET_Z=(fabs(MET_T1Txy_phi-Zee.Phi())<PI_F) ? fabs(MET_T1Txy_phi-Zee.Phi()) : (2*PI_F-fabs(MET_T1Txy_phi-Zee.Phi())) ; 
h_MET           ->Fill(Met_et                ,event_weight); 
h_MET_phi       ->Fill(Met_phi               ,event_weight); 
h_MET_T1Txy     ->Fill(MET_T1Txy_et          ,event_weight); 
h_MET_phi_T1Txy ->Fill(MET_T1Txy_phi         ,event_weight); 
h_MET_SF_T1Txy  ->Fill(MET_T1Txy_significance,event_weight); 
h_Dphi_ll       ->Fill(Dphi_ll               ,event_weight); 
h_Dphi_MET_Z    ->Fill(Dphi_MET_Z            ,event_weight); 
h_DR_ll         ->Fill(e1.DeltaR(e2)         ,event_weight);
//////////////////////// Jet ////////////////
TLorentzVector tmp_p4(0,0,0,0);
TLorentzVector sum_p4(0,0,0,0);
float HT_sys=0;
int Num_loose_jet=0;
int Num_b_jet=0;
HT_sys=HT_sys+e1.Pt()+e2.Pt();
sum_p4=sum_p4+e1+e2;
////////////////////////////////////////////
h_N_jet     ->Fill(Num_loose_jet         ,event_weight); 
h_N_bjet    ->Fill(Num_b_jet             ,event_weight); 
h_HT_sys    ->Fill(HT_sys                ,event_weight); 
h_Pt_sys    ->Fill(sum_p4.Pt()           ,event_weight); 

}// Fill histrogram


}// Entry
////////////////// Save histogram /////////////////////////////////////
Remove_negative_events( h_mee_all       );
Remove_negative_events( h_mee_all_BB    );
Remove_negative_events( h_mee_all_BE    );
Remove_negative_events( h_mee_all_EE    );
Remove_negative_events( h_mee_all_sin   );
Remove_negative_events( h_mee_all_AS    );
Remove_negative_events( h_mee_all_BB_AS );
Remove_negative_events( h_mee_all_BE_AS );
Remove_negative_events( h_mee_all_EE_AS );
Remove_negative_events( h_mee_all_SS    );
Remove_negative_events( h_mee_all_BB_SS );
Remove_negative_events( h_mee_all_BE_SS );
Remove_negative_events( h_mee_all_EE_SS );
Remove_negative_events( h_mee_all_BB_sin);
Remove_negative_events( h_mee_all_BE_sin);
Remove_negative_events( h_mee_all_EE_sin);
Remove_negative_events( h_mee_all_cum   );
Remove_negative_events( h_mee_all_cum_BB);
Remove_negative_events( h_mee_all_cum_BE);
Remove_negative_events( h_mee_all_cum_EE);
Remove_negative_events( h_mee_all_cum_v1   );
Remove_negative_events( h_mee_all_cum_BB_v1);
Remove_negative_events( h_mee_all_cum_BE_v1);
Remove_negative_events( h_mee_all_cum_EE_v1);
Remove_negative_events( h_mee_usual     );
Remove_negative_events( h_mee_BB_usual  );
Remove_negative_events( h_mee_BE_usual  );
Remove_negative_events( h_mee_EE_usual  );
Remove_negative_events( h_mee_fine      );
Remove_negative_events( h_mee_BB_fine   );
Remove_negative_events( h_mee_BE_fine   );
Remove_negative_events( h_mee_EE_fine   );
Remove_negative_events( h_mee_Zpeak     );
Remove_negative_events( h_mee_Zpeak_BB  );
Remove_negative_events( h_mee_Zpeak_BB_v1);
Remove_negative_events( h_mee_Zpeak_BE  );
Remove_negative_events( h_mee_Zpeak_BE_v1);
Remove_negative_events( h_mee_Zpeak_EE  );
Remove_negative_events( h_mee_cosp      ); 
Remove_negative_events( h_mee_cosp_BB   ); 
Remove_negative_events( h_mee_cosp_BE   ); 
Remove_negative_events( h_mee_cosp_EE   ); 
Remove_negative_events( h_mee_cosm      ); 
Remove_negative_events( h_mee_cosm_BB   ); 
Remove_negative_events( h_mee_cosm_BE   ); 
Remove_negative_events( h_mee_cosm_EE   ); 
Remove_negative_events( h_mee_cosp_fine   );
Remove_negative_events( h_mee_cosp_all_fine);
Remove_negative_events( h_mee_cosp_BB_fine);
Remove_negative_events( h_mee_cosp_BE_fine);
Remove_negative_events( h_mee_cosp_EE_fine);
Remove_negative_events( h_mee_cosm_all_fine);
Remove_negative_events( h_mee_cosm_fine   );
Remove_negative_events( h_mee_cosm_BB_fine);
Remove_negative_events( h_mee_cosm_BE_fine);
Remove_negative_events( h_mee_cosm_EE_fine);
Remove_negative_events( h_mee_cosp_usual   ); 
Remove_negative_events( h_mee_cosp_BB_usual); 
Remove_negative_events( h_mee_cosp_BE_usual); 
Remove_negative_events( h_mee_cosp_EE_usual); 
Remove_negative_events( h_mee_cosm_usual   ); 
Remove_negative_events( h_mee_cosm_BB_usual); 
Remove_negative_events( h_mee_cosm_BE_usual); 
Remove_negative_events( h_mee_cosm_EE_usual); 
Remove_negative_events( h_cos_all_region); 
Remove_negative_events( h_cos           ); 
Remove_negative_events( h_cos_BB        ); 
Remove_negative_events( h_cos_BE        ); 
Remove_negative_events( h_cos_EE        ); 

Remove_negative_events( h_mee_fail_MET  );
Remove_negative_events( h_pv_n          );
Remove_negative_events( h_rho           );
Remove_negative_events( h_Ptll          );
Remove_negative_events( h_Etall         );
Remove_negative_events( h_Phill         );
Remove_negative_events( h_led_Et        );
Remove_negative_events( h_led_eta       );
Remove_negative_events( h_led_phi       );
Remove_negative_events( h_sub_Et        );
Remove_negative_events( h_sub_eta       );
Remove_negative_events( h_sub_phi       );
Remove_negative_events( h_MET           );
Remove_negative_events( h_MET_phi       );
Remove_negative_events( h_MET_T1Txy     );
Remove_negative_events( h_MET_phi_T1Txy );
Remove_negative_events( h_MET_SF_T1Txy  );
Remove_negative_events( h_MET_Filter    );
Remove_negative_events( h_Dphi_ll       );
Remove_negative_events( h_Dphi_MET_Z    );
Remove_negative_events( h_DR_ll         );
Remove_negative_events( h_N_jet         );
Remove_negative_events( h_N_bjet        );
Remove_negative_events( h_HT_sys        );
Remove_negative_events( h_Pt_sys        );
Remove_negative_events( h_MET_Filter_detail);
Remove_negative_events( h_resolution    );
Remove_negative_events( h_resolution_BB );
Remove_negative_events( h_resolution_BE );

TFile *f = new TFile(output_file,"RECREATE");
f->cd();

h_mee_all       ->Write();
h_mee_all_BB    ->Write();
h_mee_all_BE    ->Write();
h_mee_all_EE    ->Write();
h_mee_all_AS    ->Write();
h_mee_all_BB_AS ->Write();
h_mee_all_BE_AS ->Write();
h_mee_all_EE_AS ->Write();
h_mee_all_SS    ->Write();
h_mee_all_BB_SS ->Write();
h_mee_all_BE_SS ->Write();
h_mee_all_EE_SS ->Write();
h_mee_all_sin   ->Write();
h_mee_all_BB_sin->Write();
h_mee_all_BE_sin->Write();
h_mee_all_EE_sin->Write();
h_mee_all_cum   ->Write();
h_mee_all_cum_BB->Write();
h_mee_all_cum_BE->Write();
h_mee_all_cum_EE->Write();
h_mee_all_cum_v1   ->Write();
h_mee_all_cum_BB_v1->Write();
h_mee_all_cum_BE_v1->Write();
h_mee_all_cum_EE_v1->Write();
h_mee_usual     ->Write();
h_mee_BB_usual  ->Write();
h_mee_BE_usual  ->Write();
h_mee_EE_usual  ->Write();
h_mee_fine      ->Write();
h_mee_BB_fine   ->Write();
h_mee_BE_fine   ->Write();
h_mee_EE_fine   ->Write();
h_mee_Zpeak     ->Write();
h_mee_Zpeak_BB  ->Write();
h_mee_Zpeak_BB_v1  ->Write();
h_mee_Zpeak_BE  ->Write();
h_mee_Zpeak_BE_v1  ->Write();
h_mee_Zpeak_EE  ->Write();
h_mee_cosp      ->Write(); 
h_mee_cosp_BB   ->Write(); 
h_mee_cosp_BE   ->Write(); 
h_mee_cosp_EE   ->Write(); 
h_mee_cosm      ->Write(); 
h_mee_cosm_BB   ->Write(); 
h_mee_cosm_BE   ->Write(); 
h_mee_cosm_EE   ->Write(); 
h_mee_cosp_fine   ->Write(); 
h_mee_cosp_all_fine->Write(); 
h_mee_cosp_BB_fine->Write(); 
h_mee_cosp_BE_fine->Write(); 
h_mee_cosp_EE_fine->Write(); 
h_mee_cosm_all_fine->Write(); 
h_mee_cosm_fine   ->Write(); 
h_mee_cosm_BB_fine->Write(); 
h_mee_cosm_BE_fine->Write(); 
h_mee_cosm_EE_fine->Write(); 
h_mee_cosp_usual   ->Write(); 
h_mee_cosp_BB_usual->Write(); 
h_mee_cosp_BE_usual->Write(); 
h_mee_cosp_EE_usual->Write(); 
h_mee_cosm_usual   ->Write(); 
h_mee_cosm_BB_usual->Write(); 
h_mee_cosm_BE_usual->Write(); 
h_mee_cosm_EE_usual->Write(); 
h_cos_all_region->Write(); 
h_cos           ->Write(); 
h_cos_BB        ->Write(); 
h_cos_BE        ->Write(); 
h_cos_EE        ->Write(); 
h_mee_fail_MET  ->Write();
h_pv_n          ->Write();
h_rho           ->Write();
h_Ptll          ->Write();
h_Etall         ->Write();
h_Phill         ->Write();
h_led_Et        ->Write();
h_led_eta       ->Write();
h_led_phi       ->Write();
h_sub_Et        ->Write();
h_sub_eta       ->Write();
h_sub_phi       ->Write();
h_MET           ->Write(); 
h_MET_phi       ->Write(); 
h_MET_T1Txy     ->Write(); 
h_MET_phi_T1Txy ->Write(); 
h_MET_SF_T1Txy  ->Write(); 
h_MET_Filter    ->Write();
h_Dphi_ll       ->Write();
h_Dphi_MET_Z    ->Write();
h_DR_ll         ->Write();
h_N_jet         ->Write();
h_N_bjet        ->Write();
h_HT_sys        ->Write();
h_Pt_sys        ->Write();
h_MET_Filter_detail    ->Write();
h_resolution    ->Write(); 
h_resolution_BB ->Write(); 
h_resolution_BE ->Write(); 

f->Close();

f_ele_eff->Close();

h_mee_all       ->Delete();
h_mee_all_BB    ->Delete();
h_mee_all_BE    ->Delete();
h_mee_all_EE    ->Delete();
h_mee_all_AS    ->Delete();
h_mee_all_BB_AS ->Delete();
h_mee_all_BE_AS ->Delete();
h_mee_all_EE_AS ->Delete();
h_mee_all_SS    ->Delete();
h_mee_all_BB_SS ->Delete();
h_mee_all_BE_SS ->Delete();
h_mee_all_EE_SS ->Delete();
h_mee_all_sin   ->Delete();
h_mee_all_BB_sin->Delete();
h_mee_all_BE_sin->Delete();
h_mee_all_EE_sin->Delete();
h_mee_all_cum   ->Delete();
h_mee_all_cum_BB->Delete();
h_mee_all_cum_BE->Delete();
h_mee_all_cum_EE->Delete();
h_mee_all_cum_v1   ->Delete();
h_mee_all_cum_BB_v1->Delete();
h_mee_all_cum_BE_v1->Delete();
h_mee_all_cum_EE_v1->Delete();
h_mee_usual     ->Delete();
h_mee_BB_usual  ->Delete();
h_mee_BE_usual  ->Delete();
h_mee_EE_usual  ->Delete();
h_mee_fine      ->Delete();
h_mee_BB_fine   ->Delete();
h_mee_BE_fine   ->Delete();
h_mee_EE_fine   ->Delete();
h_mee_Zpeak     ->Delete();
h_mee_Zpeak_BB  ->Delete();
h_mee_Zpeak_BB_v1  ->Delete();
h_mee_Zpeak_BE  ->Delete();
h_mee_Zpeak_BE_v1  ->Delete();
h_mee_Zpeak_EE  ->Delete();
h_mee_cosp      ->Delete(); 
h_mee_cosp_BB   ->Delete(); 
h_mee_cosp_BE   ->Delete(); 
h_mee_cosp_EE   ->Delete(); 
h_mee_cosm      ->Delete(); 
h_mee_cosm_BB   ->Delete(); 
h_mee_cosm_BE   ->Delete(); 
h_mee_cosm_EE   ->Delete(); 
h_mee_cosp_fine   ->Delete(); 
h_mee_cosp_all_fine->Delete(); 
h_mee_cosp_BB_fine->Delete(); 
h_mee_cosp_BE_fine->Delete(); 
h_mee_cosp_EE_fine->Delete(); 
h_mee_cosm_all_fine->Delete(); 
h_mee_cosm_fine   ->Delete(); 
h_mee_cosm_BB_fine->Delete(); 
h_mee_cosm_BE_fine->Delete(); 
h_mee_cosm_EE_fine->Delete(); 
h_mee_cosp_usual   ->Delete(); 
h_mee_cosp_BB_usual->Delete(); 
h_mee_cosp_BE_usual->Delete(); 
h_mee_cosp_EE_usual->Delete(); 
h_mee_cosm_usual   ->Delete(); 
h_mee_cosm_BB_usual->Delete(); 
h_mee_cosm_BE_usual->Delete(); 
h_mee_cosm_EE_usual->Delete(); 
h_cos_all_region->Delete(); 
h_cos           ->Delete(); 
h_cos_BB        ->Delete(); 
h_cos_BE        ->Delete(); 
h_cos_EE        ->Delete(); 
h_mee_fail_MET  ->Delete();
h_pv_n          ->Delete();
h_rho           ->Delete();
h_Ptll          ->Delete();
h_Etall         ->Delete();
h_Phill         ->Delete();
h_led_Et        ->Delete();
h_led_eta       ->Delete();
h_led_phi       ->Delete();
h_sub_Et        ->Delete();
h_sub_eta       ->Delete();
h_sub_phi       ->Delete();
h_MET           ->Delete(); 
h_MET_phi       ->Delete(); 
h_MET_T1Txy     ->Delete(); 
h_MET_phi_T1Txy ->Delete(); 
h_MET_SF_T1Txy  ->Delete(); 
h_MET_Filter    ->Delete(); 
h_Dphi_ll       ->Delete(); 
h_Dphi_MET_Z    ->Delete(); 
h_DR_ll         ->Delete();        
h_N_jet         ->Delete(); 
h_N_bjet        ->Delete(); 
h_HT_sys        ->Delete(); 
h_Pt_sys        ->Delete(); 
h_MET_Filter_detail    ->Delete(); 
h_resolution    ->Delete(); 
h_resolution_BB ->Delete(); 
h_resolution_BE ->Delete(); 


t               ->Delete();
std::cout<<output_file<<" is saved"<<std::endl;
}

int trigger_match(float eta, float phi, vector<float> *filter_eta, vector<float> *filter_phi, int fire){
if(fire==0) return 0;
TLorentzVector tmp1;
TLorentzVector tmp2;
tmp1.SetPtEtaPhiM(1,eta,phi,0);
for(unsigned int i=0;i<filter_eta->size();i++){
tmp2.SetPtEtaPhiM(1,filter_eta->at(i),filter_phi->at(i),0);
if(tmp2.DeltaR(tmp1)<0.1){return 1;}
}
return 0;
}

void Remove_negative_events(TH1D * &h){
for(int i=1; i< h->GetNbinsX()+1; i++){
if(h->GetBinContent(i)<0) {h->SetBinContent(i,0);
                           h->SetBinError(i,0);
                          }
}
}

float sf_weight(float Et, float eta, TString uncert){
float weight=1;
if(uncert=="Barrel_SF_scale_up"){if(fabs(eta)<1.4442){if(Et<90)weight=1.01;
                                                      //else if(Et<1000)weight=1.02;
                                                      else if(Et<1000)weight=1+(0.00802+2.198e-5*Et);
                                                      else weight=1.03;
                                                     }
                                }
else if(uncert=="Barrel_SF_scale_down"){if(fabs(eta)<1.4442){if(Et<90)weight=0.99;
                                                      //else if(Et<1000)weight=0.98;
                                                      else if(Et<1000)weight=1-(0.00802+2.198e-5*Et);
                                                      else weight=0.97;
                                                     }
                                }
else if(uncert=="Endcap_SF_scale_up"){if(fabs(eta)>1.566 && fabs(eta)<2.5){if(Et<90)weight=1.01;
                                                      //else if(Et<300)weight=1.02;
                                                      else if(Et<300)weight=1+(-0.00286+1.4e-4*Et);
                                                      else weight=1.04;
                                                     }
                                }
else if(uncert=="Endcap_SF_scale_down"){if(fabs(eta)>1.566 && fabs(eta)<2.5){if(Et<90)weight=0.99;
                                                      //else if(Et<300)weight=0.98;
                                                      else if(Et<300)weight=1-(-0.00286+1.4e-4*Et);
                                                      else weight=0.96;
                                                     }
                                }
return weight;
}

double calcCosThetaCSAnal(TLorentzVector v_dil, TLorentzVector v_mum, TLorentzVector v_mup) {
    //Function to return value of cos(theta*) in Collins-Soper frame
    // takes as input 4-vector of dilepton in lab frame, and 4-vectors of mu+
    // and mu- in dilepton CM frame.
    //debug = false;
    // Get pz and E components of mu+ and mu- in lab frame.
    double pz_mum = v_mum.Pz();
    double e_mum  = v_mum.E();
    double pz_mup = v_mup.Pz();
    double e_mup  = v_mup.E();
 
    // Get mass and pt of dilepton in lab frame
    double pt_dil   = v_dil.Pt();
    double pl_dil   = v_dil.Pz();
    double mass_dil = v_dil.M();
 
      // Calculate cos_theta and return
    double cos_theta_cs = calcCosThetaCSAnal(pz_mum, e_mum, pz_mup, e_mup, pt_dil, pl_dil, mass_dil);
    return cos_theta_cs;
   }
double calcCosThetaCSAnal(double pz_mum, double e_mum, double pz_mup, double e_mup, double pt_dil, double pl_dil, double mass_dil) {
  // Analytical calculation of Collins-Soper cos(theta).  Uses pz, e of mu+
  // and mu-, and pt, pl, and mass of dilepton in lab frame.
  //debug = false;
  
  double mum_minus = (1./sqrt(2.))*(e_mum - pz_mum);
  double mum_plus  = (1./sqrt(2.))*(e_mum + pz_mum);
  double mup_minus = (1./sqrt(2.))*(e_mup - pz_mup);
  double mup_plus  = (1./sqrt(2.))*(e_mup + pz_mup);
  double dil_term  = 2./(mass_dil*sqrt((mass_dil*mass_dil) + (pt_dil*pt_dil)));
  double mu_term   = (mum_plus*mup_minus) - (mum_minus*mup_plus);
  double cos_cs    = dil_term*mu_term;
  
  // The above calculation assumed dilepton pL > 0. Flip the sign of
  // cos_cs if this isn't true.
  if (pl_dil < 0.)cos_cs *= -1.;
  return cos_cs;
  }


int matching(vector<float> *eta, vector<float> *phi, float eta_1, float phi_1){
TLorentzVector tmp_1;
tmp_1.SetPtEtaPhiM(1,eta_1,phi_1,1);
if(eta->size()!=phi->size())std::cout<<"n eta:"<<eta->size()<<",n phi:"<<phi->size()<<std::endl;
for(unsigned int i=0;i<eta->size();i++){
TLorentzVector tmp;
tmp.SetPtEtaPhiM(1,eta->at(i),phi->at(i),1);
if(tmp.DeltaR(tmp_1)<0.001) return i;
}

return -1;
}

void fill_cum(TH1D* &hist, float M , double weight){
if(M<(hist->GetBinLowEdge(hist->GetNbinsX())+hist->GetBinWidth(hist->GetNbinsX()))) hist->Fill(M,weight);
else{hist->Fill(hist->GetBinLowEdge(hist->GetNbinsX())+0.5*hist->GetBinWidth(hist->GetNbinsX()) ,weight);
    }
}
