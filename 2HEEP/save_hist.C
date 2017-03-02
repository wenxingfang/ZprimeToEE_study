#include <TH1.h>
#include <TH1F.h>
#include <TH1D.h>
#include <TChain.h>
#include <TFile.h>
#include <TH2.h>
#include <TAxis.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TRandom3.h>
#include <TLorentzVector.h>
#include "Fake_rate.C"
#include <TF1.h>
#include <time.h>
#include <iostream>

void fill_hist(TString input_file, TString output_file, bool is_data=false, bool is_ZToEE=false, bool is_fewz=false, bool is_FR_1F=false, bool is_FR_2F=false, TString uncert="");

void save_hist(){
TString input_dir="/user/wenxing/HEEP/CMSSW_7_4_10_patch2/src/HEEP_electron_80/reskim_script/reskim_out/for_plots/";
TString output_dir="./ntuples/sys_saved_hist/";
bool do_fewz=true;
TString str_fewz=do_fewz?"_fewz":"";
TString str_uncert="";
TString uncertainty="";
//uncertainty="PU_scale_up";
//uncertainty="PU_scale_down";
uncertainty="Barrel_energy_scale_up";
//uncertainty="Barrel_energy_scale_down";
//uncertainty="Endcap_energy_scale_up";
//uncertainty="Endcap_energy_scale_down";
     if (uncertainty=="PU_scale_up") str_uncert="PU_scale_up_";
else if (uncertainty=="PU_scale_down") str_uncert="PU_scale_down_";
else if (uncertainty=="Barrel_energy_scale_up") str_uncert="Barrel_energy_scale_up_";
else if (uncertainty=="Barrel_energy_scale_down") str_uncert="Barrel_energy_scale_down_";
else if (uncertainty=="Endcap_energy_scale_up") str_uncert="Endcap_energy_scale_up_";
else if (uncertainty=="Endcap_energy_scale_down") str_uncert="Endcap_energy_scale_down_";

//fill_hist(input_dir+"RunBCDEFGH_reMini_gsf.root"   ,output_dir+"hist_data_RunBCDEFGH_reMiniAOD.root"     ,true,false,false,false,false,uncertainty);
//fill_hist(input_dir+"RunBCDEFGH_reMini_gsf_1F.root",output_dir+"hist_data_RunBCDEFGH_FR1F_reMiniAOD.root",true,false,false,true ,false,uncertainty);
//fill_hist(input_dir+"RunBCDEFGH_reMini_gsf_2F.root",output_dir+"hist_data_RunBCDEFGH_FR2F_reMiniAOD.root",true,false,false,false ,true,uncertainty);

fill_hist(input_dir+   "ZToEE_50_120.root",output_dir+str_uncert+   "hist_ZToEE_50_120"+str_fewz+".root",false,true,do_fewz,false,false,uncertainty);
fill_hist(input_dir+  "ZToEE_120_200.root",output_dir+str_uncert+  "hist_ZToEE_120_200"+str_fewz+".root",false,true,do_fewz,false,false,uncertainty);
fill_hist(input_dir+  "ZToEE_200_400.root",output_dir+str_uncert+  "hist_ZToEE_200_400"+str_fewz+".root",false,true,do_fewz,false,false,uncertainty);
fill_hist(input_dir+  "ZToEE_400_800.root",output_dir+str_uncert+  "hist_ZToEE_400_800"+str_fewz+".root",false,true,do_fewz,false,false,uncertainty);
fill_hist(input_dir+ "ZToEE_800_1400.root",output_dir+str_uncert+ "hist_ZToEE_800_1400"+str_fewz+".root",false,true,do_fewz,false,false,uncertainty);
fill_hist(input_dir+"ZToEE_1400_2300.root",output_dir+str_uncert+"hist_ZToEE_1400_2300"+str_fewz+".root",false,true,do_fewz,false,false,uncertainty);
fill_hist(input_dir+"ZToEE_2300_3500.root",output_dir+str_uncert+"hist_ZToEE_2300_3500"+str_fewz+".root",false,true,do_fewz,false,false,uncertainty);
fill_hist(input_dir+"ZToEE_3500_4500.root",output_dir+str_uncert+"hist_ZToEE_3500_4500"+str_fewz+".root",false,true,do_fewz,false,false,uncertainty);
fill_hist(input_dir+"ZToEE_4500_6000.root",output_dir+str_uncert+"hist_ZToEE_4500_6000"+str_fewz+".root",false,true,do_fewz,false,false,uncertainty);
fill_hist(input_dir+ "ZToEE_6000_Inf.root",output_dir+str_uncert+ "hist_ZToEE_6000_Inf"+str_fewz+".root",false,true,do_fewz,false,false,uncertainty);

fill_hist(input_dir+   "ZToEE_50_120_1F.root",output_dir+str_uncert+   "hist_ZToEE_50_120"+str_fewz+"_1F.root",false,true,do_fewz,true,false,uncertainty);
fill_hist(input_dir+  "ZToEE_120_200_1F.root",output_dir+str_uncert+  "hist_ZToEE_120_200"+str_fewz+"_1F.root",false,true,do_fewz,true,false,uncertainty);
fill_hist(input_dir+  "ZToEE_200_400_1F.root",output_dir+str_uncert+  "hist_ZToEE_200_400"+str_fewz+"_1F.root",false,true,do_fewz,true,false,uncertainty);
fill_hist(input_dir+  "ZToEE_400_800_1F.root",output_dir+str_uncert+  "hist_ZToEE_400_800"+str_fewz+"_1F.root",false,true,do_fewz,true,false,uncertainty);
fill_hist(input_dir+ "ZToEE_800_1400_1F.root",output_dir+str_uncert+ "hist_ZToEE_800_1400"+str_fewz+"_1F.root",false,true,do_fewz,true,false,uncertainty);
fill_hist(input_dir+"ZToEE_1400_2300_1F.root",output_dir+str_uncert+"hist_ZToEE_1400_2300"+str_fewz+"_1F.root",false,true,do_fewz,true,false,uncertainty);
fill_hist(input_dir+"ZToEE_2300_3500_1F.root",output_dir+str_uncert+"hist_ZToEE_2300_3500"+str_fewz+"_1F.root",false,true,do_fewz,true,false,uncertainty);
fill_hist(input_dir+"ZToEE_3500_4500_1F.root",output_dir+str_uncert+"hist_ZToEE_3500_4500"+str_fewz+"_1F.root",false,true,do_fewz,true,false,uncertainty);
fill_hist(input_dir+"ZToEE_4500_6000_1F.root",output_dir+str_uncert+"hist_ZToEE_4500_6000"+str_fewz+"_1F.root",false,true,do_fewz,true,false,uncertainty);
fill_hist(input_dir+ "ZToEE_6000_Inf_1F.root",output_dir+str_uncert+ "hist_ZToEE_6000_Inf"+str_fewz+"_1F.root",false,true,do_fewz,true,false,uncertainty);

fill_hist(input_dir+"DYToLL.root"              ,output_dir+str_uncert+"hist_ZToTT_mad.root"        ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"WZ.root"                  ,output_dir+str_uncert+"hist_WZ.root"               ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"ZZ.root"                  ,output_dir+str_uncert+"hist_ZZ.root"               ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"ST.root"                  ,output_dir+str_uncert+"hist_ST.root"               ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"ST_anti.root"             ,output_dir+str_uncert+"hist_ST_anti.root"          ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"WW_To2L2Nv_200.root"      ,output_dir+str_uncert+"hist_WW2L_200.root"         ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"WW_To2L2Nv_200_600.root"  ,output_dir+str_uncert+"hist_WW2L_200_600.root"     ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"WW_To2L2Nv_600_1200.root" ,output_dir+str_uncert+"hist_WW2L_600_1200.root"    ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"WW_To2L2Nv_1200_2500.root",output_dir+str_uncert+"hist_WW2L_1200_2500.root"   ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"WW_To2L2Nv_2500_Inf.root" ,output_dir+str_uncert+"hist_WW2L_2500_Inf.root"    ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"TT_M_500.root"            ,output_dir+str_uncert+"hist_TTbar2L_500.root"      ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"TT_M_500_800.root"        ,output_dir+str_uncert+"hist_TTbar2L_500_800.root"  ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"TT_M_800_1200.root"       ,output_dir+str_uncert+"hist_TTbar2L_800_1200.root" ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"TT_M_1200_1800.root"      ,output_dir+str_uncert+"hist_TTbar2L_1200_1800.root",false,false,false,false,false,uncertainty);
fill_hist(input_dir+"TT_M_1800_Inf.root"       ,output_dir+str_uncert+"hist_TTbar2L_1800_Inf.root" ,false,false,false,false,false,uncertainty);

fill_hist(input_dir+"DYToLL_1F.root"              ,output_dir+str_uncert+"hist_ZToTT_mad_1F.root"        ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"WZ_1F.root"                  ,output_dir+str_uncert+"hist_WZ_1F.root"               ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"ZZ_1F.root"                  ,output_dir+str_uncert+"hist_ZZ_1F.root"               ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"ST_1F.root"                  ,output_dir+str_uncert+"hist_ST_1F.root"               ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"ST_anti_1F.root"             ,output_dir+str_uncert+"hist_ST_anti_1F.root"          ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"WW_To2L2Nv_200_1F.root"      ,output_dir+str_uncert+"hist_WW2L_200_1F.root"         ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"WW_To2L2Nv_200_600_1F.root"  ,output_dir+str_uncert+"hist_WW2L_200_600_1F.root"     ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"WW_To2L2Nv_600_1200_1F.root" ,output_dir+str_uncert+"hist_WW2L_600_1200_1F.root"    ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"WW_To2L2Nv_1200_2500_1F.root",output_dir+str_uncert+"hist_WW2L_1200_2500_1F.root"   ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"WW_To2L2Nv_2500_Inf_1F.root" ,output_dir+str_uncert+"hist_WW2L_2500_Inf_1F.root"    ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"TT_M_500_1F.root"            ,output_dir+str_uncert+"hist_TTbar2L_500_1F.root"      ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"TT_M_500_800_1F.root"        ,output_dir+str_uncert+"hist_TTbar2L_500_800_1F.root"  ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"TT_M_800_1200_1F.root"       ,output_dir+str_uncert+"hist_TTbar2L_800_1200_1F.root" ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"TT_M_1200_1800_1F.root"      ,output_dir+str_uncert+"hist_TTbar2L_1200_1800_1F.root",false,false,false,true,false,uncertainty);
fill_hist(input_dir+"TT_M_1800_Inf_1F.root"       ,output_dir+str_uncert+"hist_TTbar2L_1800_Inf_1F.root" ,false,false,false,true,false,uncertainty);

////fill_hist(input_dir+"TTTo2L2Nu_ttHtranche3_1F.root",output_dir+"hist_TTbar2L_all_1F.root");
////fill_hist(input_dir+"WJet_mad.root",output_dir+"hist_WJet_mad.root");
////fill_hist(input_dir+"GJ_40_100.root",output_dir+"hist_GJ_40_100.root");
////fill_hist(input_dir+"GJ_100_200.root",output_dir+"hist_GJ_100_200.root");
////fill_hist(input_dir+"GJ_200_400.root",output_dir+"hist_GJ_200_400.root");
////fill_hist(input_dir+"GJ_400_600.root",output_dir+"hist_GJ_400_600.root");
////fill_hist(input_dir+"GJ_600_Inf.root",output_dir+"hist_GJ_600_Inf.root");
////fill_hist(input_dir+"DYToEE_pow.root",output_dir+"hist_DYToEE_pow.root");
////fill_hist(input_dir+"DYToEE_mad.root",output_dir+"hist_DYToEE_mad.root");
////fill_hist(input_dir+"DYToEE_amc.root",output_dir+"hist_DYToEE_amc.root");

}

void fill_hist(TString input_file, TString output_file, bool is_data, bool is_ZToEE, bool is_fewz, bool is_FR_1F, bool is_FR_2F, TString uncert){

TH1::SetDefaultSumw2(kTRUE);
TString t_name="Ele";
if(is_data==false){
if (uncert=="Barrel_energy_scale_up")        t_name="Ele_Barrel_scale_up";
else if (uncert=="Barrel_energy_scale_down") t_name="Ele_Barrel_scale_down";
else if (uncert=="Endcap_energy_scale_up")   t_name="Ele_Endcap_scale_up";
else if (uncert=="Endcap_energy_scale_down") t_name="Ele_Endcap_scale_down";}
TChain *t = new TChain(t_name);
t->Add(input_file);

int   pv_n     = 0 ;
int   PU_true  = 0 ;
int   event_sign = 0 ;

float rho        = 0 ;

float OS      = 0 ;
float mee     = 0 ;
float Pt      = 0 ;
float e1_Et   = 0 ;
float e1_eta  = 0 ;
float e1_phi  = 0 ;
float e2_Et   = 0 ;
float e2_eta  = 0 ;
float e2_phi  = 0 ;

float w_PU_combined    = 0 ;
float w_PU_golden      = 0 ; 
float w_PU_silver      = 0 ;
float w_PU_silver_down = 0 ; 
float w_PU_silver_up   = 0 ;

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

t->SetBranchAddress("PU_true"   , &PU_true         ) ;
t->SetBranchAddress("event_sign", &event_sign      ) ;
t->SetBranchAddress("mee_gsf"   , &mee             ) ;
t->SetBranchAddress("e1_Et"     , &e1_Et        ) ;
t->SetBranchAddress("e1_eta"    , &e1_eta       ) ;
t->SetBranchAddress("e1_phi"    , &e1_phi       ) ;
t->SetBranchAddress("e2_Et"     , &e2_Et        ) ;
t->SetBranchAddress("e2_eta"    , &e2_eta       ) ;
t->SetBranchAddress("e2_phi"    , &e2_phi       ) ;
t->SetBranchAddress("w_PU_combined"   , &w_PU_combined        ) ;
if(t_name=="Ele"){
t->SetBranchAddress("pv_n"      , &pv_n            ) ;
t->SetBranchAddress("rho"       , &rho             ) ;
t->SetBranchAddress("OS"        , &OS              ) ;
t->SetBranchAddress("Pt"        , &Pt              ) ;
t->SetBranchAddress("e1_dPhiIn"          , &e1_dPhiIn                 ) ;
t->SetBranchAddress("e1_Sieie"           , &e1_Sieie                  ) ;
t->SetBranchAddress("e1_missingHits"     , &e1_missingHits            ) ;
t->SetBranchAddress("e1_dxyFirstPV"      , &e1_dxyFirstPV             ) ;
t->SetBranchAddress("e1_HOverE"          , &e1_HOverE                 ) ;
t->SetBranchAddress("e1_E1x5OverE5x5"    , &e1_E1x5OverE5x5           ) ;
t->SetBranchAddress("e1_E2x5OverE5x5"    , &e1_E2x5OverE5x5           ) ;
t->SetBranchAddress("e1_isolEMHadDepth1" , &e1_isolEMHadDepth1        ) ;
t->SetBranchAddress("e1_IsolPtTrks"      , &e1_IsolPtTrks             ) ;
t->SetBranchAddress("e1_EcalDriven"      , &e1_EcalDriven             ) ;
t->SetBranchAddress("e1_dEtaIn"          , &e1_dEtaIn                 ) ;
t->SetBranchAddress("e2_dPhiIn"          , &e2_dPhiIn                 ) ;
t->SetBranchAddress("e2_Sieie"           , &e2_Sieie                  ) ;
t->SetBranchAddress("e2_missingHits"     , &e2_missingHits            ) ;
t->SetBranchAddress("e2_dxyFirstPV"      , &e2_dxyFirstPV             ) ;
t->SetBranchAddress("e2_HOverE"          , &e2_HOverE                 ) ;
t->SetBranchAddress("e2_E1x5OverE5x5"    , &e2_E1x5OverE5x5           ) ;
t->SetBranchAddress("e2_E2x5OverE5x5"    , &e2_E2x5OverE5x5           ) ;
t->SetBranchAddress("e2_isolEMHadDepth1" , &e2_isolEMHadDepth1        ) ;
t->SetBranchAddress("e2_IsolPtTrks"      , &e2_IsolPtTrks             ) ;
t->SetBranchAddress("e2_EcalDriven"      , &e2_EcalDriven             ) ;
t->SetBranchAddress("e2_dEtaIn"          , &e2_dEtaIn                 ) ;
t->SetBranchAddress("w_PU_golden"     , &w_PU_golden          ) ;
t->SetBranchAddress("w_PU_silver"     , &w_PU_silver          ) ;
t->SetBranchAddress("w_PU_silver_down", &w_PU_silver_down     ) ;
t->SetBranchAddress("w_PU_silver_up"  , &w_PU_silver_up       ) ;
}
///
const int N_mee_bin=101;
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
mee_bin_edge[index]=4000;//1
///
float mee_bin_edge_EE[57];
int index_EE=0;
for(int i=50;i<120;i+=5)    {mee_bin_edge_EE[index_EE]=i;index_EE++;}//14
for(int i=120;i<150;i+=5)   {mee_bin_edge_EE[index_EE]=i;index_EE++;}//6
for(int i=150;i<200;i+=10)  {mee_bin_edge_EE[index_EE]=i;index_EE++;}//5
for(int i=200;i<600;i+=40)  {mee_bin_edge_EE[index_EE]=i;index_EE++;}//10
for(int i=600;i<900;i+=60)  {mee_bin_edge_EE[index_EE]=i;index_EE++;}//5
for(int i=900;i<1250;i+=80) {mee_bin_edge_EE[index_EE]=i;index_EE++;}//5
for(int i=1250;i<1600;i+=100){mee_bin_edge_EE[index_EE]=i;index_EE++;}//4
for(int i=1600;i<1900;i+=120){mee_bin_edge_EE[index_EE]=i;index_EE++;}//3   
for(int i=1900;i<2500;i+=160){mee_bin_edge_EE[index_EE]=i;index_EE++;}//4
mee_bin_edge_EE[index_EE]=2500;//1

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

const int N_mee_bin_big=61;
float mee_bin_edge_big[N_mee_bin_big];
int index_big=0;
for(int i=50;i<120;i+=5)     {mee_bin_edge_big[index_big]=i;index_big++;}//14
for(int i=120;i<150;i+=5)    {mee_bin_edge_big[index_big]=i;index_big++;}//6
for(int i=150;i<200;i+=10)   {mee_bin_edge_big[index_big]=i;index_big++;}//5
for(int i=200;i<600;i+=20)   {mee_bin_edge_big[index_big]=i;index_big++;}//20
for(int i=600;i<1000;i+=80)  {mee_bin_edge_big[index_big]=i;index_big++;}//5
for(int i=1000;i<2500;i+=160){mee_bin_edge_big[index_big]=i;index_big++;}//10
                              mee_bin_edge_big[index_big]=2500;//1


///
TH1F *h_pv_n               =new TH1F("h_pv_n","",40,0,40);
TH1F *h_rho                =new TH1F("h_rho" ,"",80,0,40);
TH1F *h_OS                 =new TH1F("h_OS"  ,"",20,0, 2);

TH1F *h_mee_all            =new TH1F("h_mee_all",""   ,N_mee_bin-1,mee_bin_edge);
TH1F *h_mee_all_BB         =new TH1F("h_mee_all_BB","",N_mee_bin-1,mee_bin_edge);
TH1F *h_mee_all_BE         =new TH1F("h_mee_all_BE","",N_mee_bin-1,mee_bin_edge);
TH1F *h_mee_all_EE         =new TH1F("h_mee_all_EE","",N_mee_bin-1,mee_bin_edge);
TH1F *h_mee_all_EE_v1      =new TH1F("h_mee_all_EE_v1","",56,mee_bin_edge_EE);
TH1F *h_mee_all_big        =new TH1F("h_mee_all_big",""    ,N_mee_bin_big-1,mee_bin_edge_big);
TH1F *h_mee_all_BB_big      =new TH1F("h_mee_all_BB_big","",N_mee_bin_big-1,mee_bin_edge_big);
TH1F *h_mee_all_BE_big      =new TH1F("h_mee_all_BE_big","",N_mee_bin_big-1,mee_bin_edge_big);
TH1F *h_mee_all_EE_big      =new TH1F("h_mee_all_EE_big","",N_mee_bin_big-1,mee_bin_edge_big);
TH1F *h_mee_all_sin        =new TH1F("h_mee_all_sin",""   ,N_mee_bin_sin-1,mee_bin_edge_sin);
TH1F *h_mee_all_BB_sin     =new TH1F("h_mee_all_BB_sin","",N_mee_bin_sin-1,mee_bin_edge_sin);
TH1F *h_mee_all_BE_sin     =new TH1F("h_mee_all_BE_sin","",N_mee_bin_sin-1,mee_bin_edge_sin);
TH1F *h_mee_all_EE_sin     =new TH1F("h_mee_all_EE_sin","",N_mee_bin_sin-1,mee_bin_edge_sin);
/*
TH1F *h_mee_all_sin        =new TH1F("h_mee_all_sin",""   ,31,Bin_mee_sin_all);
TH1F *h_mee_all_BB_sin     =new TH1F("h_mee_all_BB_sin","",27,Bin_mee_sin_BB_all);
TH1F *h_mee_all_BE_sin     =new TH1F("h_mee_all_BE_sin","",27,Bin_mee_sin_BE_all);
TH1F *h_mee_all_EE_sin     =new TH1F("h_mee_all_EE_sin","",24,Bin_mee_sin_EE_all);
*/
TH1F *h_mee_all_cum        =new TH1F("h_mee_all_cumlative",""     ,197,60,4000);
TH1F *h_mee_all_cum_BE     =new TH1F("h_mee_all_cumlative_BE",""  ,197,60,4000);
TH1F *h_mee_all_cum_BB     =new TH1F("h_mee_all_cumlative_BB",""  ,197,60,4000);
TH1F *h_mee_all_cum_EE     =new TH1F("h_mee_all_cumlative_EE",""  ,197,60,4000);

h_mee_all_cum   ->Sumw2(kFALSE); 
h_mee_all_cum_BE->Sumw2(kFALSE); 
h_mee_all_cum_BB->Sumw2(kFALSE); 
h_mee_all_cum_EE->Sumw2(kFALSE); 


TH1F *h_mee_usual      =new TH1F("h_mee_usual","" ,400,0,4000);
TH1F *h_mee_BB_usual   =new TH1F("h_mee_BB_usual","" ,400,0,4000);
TH1F *h_mee_BE_usual   =new TH1F("h_mee_BE_usual","" ,400,0,4000);
TH1F *h_mee_EE_usual   =new TH1F("h_mee_EE_usual","" ,400,0,4000);
TH1F *h_mee_high           =new TH1F("h_mee_high","" ,120,300,1500);
TH1F *h_mee_Zpeak          =new TH1F("h_mee_Zpeak","",60,60,120);
TH1F *h_mee_Zpeak_BB       =new TH1F("h_mee_Zpeak_BB","",60,60,120);
TH1F *h_mee_Zpeak_BE       =new TH1F("h_mee_Zpeak_BE","",60,60,120);
TH1F *h_mee_Zpeak_EE       =new TH1F("h_mee_Zpeak_EE","",60,60,120);
TH1F *h_mee_cail           =new TH1F("h_mee_cail","" ,40,70,110);

TH1F *h_Pt                 =new TH1F("h_Pt"   ,"",75 ,0,150);
TH1F *h_e1_Et              =new TH1F("h_e1_Et","",12,30,630);
TH1F *h_e1_eta             =new TH1F("h_e1_eta","",60,-3,3);
TH1F *h_e1_phi             =new TH1F("h_e1_phi","",100,-5,5);
TH1F *h_e2_Et              =new TH1F("h_e2_Et","",12,30,630);
TH1F *h_e2_eta             =new TH1F("h_e2_eta","",60,-3,3);
TH1F *h_e2_phi             =new TH1F("h_e2_phi","",100,-5,5);
TH1F *h_e_Et_B             =new TH1F("h_e_Et_Barrel","",20,30,1030);
TH1F *h_e_Et_E             =new TH1F("h_e_Et_Endcap","",20,30,1030);

TH1F *e1_dPhiIn_B          =new TH1F("h_e1_dPhiIn_Barrel","",7,0,0.07); 
TH1F *e1_dPhiIn_E          =new TH1F("h_e1_dPhiIn_Endcap","",7,0,0.07); 
TH1F *e1_Sieie_B           =new TH1F("h_e1_Sieie_Barrel","",40,0,0.04); 
TH1F *e1_Sieie_E           =new TH1F("h_e1_Sieie_Endcap","",40,0,0.04); 
TH1F *e1_missingHits_B     =new TH1F("h_e1_missingHits_Barrel","",20,0,2);   
TH1F *e1_missingHits_E     =new TH1F("h_e1_missingHits_Endcap","",20,0,2);   
TH1F *e1_dxyFirstPV_B      =new TH1F("h_e1_dxyFirstPV_Barrel","",50,0,0.05);     
TH1F *e1_dxyFirstPV_E      =new TH1F("h_e1_dxyFirstPV_Endcap","",50,0,0.05);     
TH1F *e1_HOverE_B          =new TH1F("h_e1_HOverE_Barrel","",20,0,0.2); 
TH1F *e1_HOverE_E          =new TH1F("h_e1_HOverE_Endcap","",20,0,0.2); 
TH1F *e1_E1x5OverE5x5_B    =new TH1F("h_e1_E1x5OverE5x5_Barrel","",100,0,1);
TH1F *e1_E1x5OverE5x5_E    =new TH1F("h_e1_E1x5OverE5x5_Endcap","",100,0,1);
TH1F *e1_E2x5OverE5x5_B    =new TH1F("h_e1_E2x5OverE5x5_Barrel","",100,0,1);    
TH1F *e1_E2x5OverE5x5_E    =new TH1F("h_e1_E2x5OverE5x5_Endcap","",100,0,1);    
TH1F *e1_isolEMHadDepth1_B =new TH1F("h_e1_isolEMHadDepth1_Barrel","",100,0,10);
TH1F *e1_isolEMHadDepth1_E =new TH1F("h_e1_isolEMHadDepth1_Endcap","",100,0,10);
TH1F *e1_IsolPtTrks_B      =new TH1F("h_e1_IsolPtTrks_Barrel","",50,0,5); 
TH1F *e1_IsolPtTrks_E      =new TH1F("h_e1_IsolPtTrks_Endcap","",50,0,5); 
TH1F *e1_dEtaIn_B          =new TH1F("h_e1_dEtaIn_Barrel","",7,0,0.007);         
TH1F *e1_dEtaIn_B_er       =new TH1F("h_e1_dEtaIn_Barrel_er","",7,0,0.007);         
TH1F *e1_dEtaIn_E          =new TH1F("h_e1_dEtaIn_Endcap","",7,0,0.007);         

TH1F *e2_dPhiIn_B          =new TH1F("h_e2_dPhiIn_Barrel","",7,0,0.07); 
TH1F *e2_dPhiIn_E          =new TH1F("h_e2_dPhiIn_Endcap","",7,0,0.07); 
TH1F *e2_Sieie_B           =new TH1F("h_e2_Sieie_Barrel","",40,0,0.04); 
TH1F *e2_Sieie_E           =new TH1F("h_e2_Sieie_Endcap","",40,0,0.04); 
TH1F *e2_missingHits_B     =new TH1F("h_e2_missingHits_Barrel","",20,0,2);   
TH1F *e2_missingHits_E     =new TH1F("h_e2_missingHits_Endcap","",20,0,2);   
TH1F *e2_dxyFirstPV_B      =new TH1F("h_e2_dxyFirstPV_Barrel","",50,0,0.05);     
TH1F *e2_dxyFirstPV_E      =new TH1F("h_e2_dxyFirstPV_Endcap","",50,0,0.05);     
TH1F *e2_HOverE_B          =new TH1F("h_e2_HOverE_Barrel","",20,0,0.2); 
TH1F *e2_HOverE_E          =new TH1F("h_e2_HOverE_Endcap","",20,0,0.2); 
TH1F *e2_E1x5OverE5x5_B    =new TH1F("h_e2_E1x5OverE5x5_Barrel","",100,0,1);
TH1F *e2_E1x5OverE5x5_E    =new TH1F("h_e2_E1x5OverE5x5_Endcap","",100,0,1);
TH1F *e2_E2x5OverE5x5_B    =new TH1F("h_e2_E2x5OverE5x5_Barrel","",100,0,1);    
TH1F *e2_E2x5OverE5x5_E    =new TH1F("h_e2_E2x5OverE5x5_Endcap","",100,0,1);    
TH1F *e2_isolEMHadDepth1_B =new TH1F("h_e2_isolEMHadDepth1_Barrel","",100,0,10);
TH1F *e2_isolEMHadDepth1_E =new TH1F("h_e2_isolEMHadDepth1_Endcap","",100,0,10);
TH1F *e2_IsolPtTrks_B      =new TH1F("h_e2_IsolPtTrks_Barrel","",50,0,5); 
TH1F *e2_IsolPtTrks_E      =new TH1F("h_e2_IsolPtTrks_Endcap","",50,0,5); 
TH1F *e2_dEtaIn_B          =new TH1F("h_e2_dEtaIn_Barrel","",7,0,0.007);         
TH1F *e2_dEtaIn_B_er       =new TH1F("h_e2_dEtaIn_Barrel_er","",7,0,0.007);         
TH1F *e2_dEtaIn_E          =new TH1F("h_e2_dEtaIn_Endcap","",7,0,0.007);        

TH1F *e_dPhiIn_B          =new TH1F("h_e_dPhiIn_Barrel","",7,0,0.07); 
TH1F *e_dPhiIn_E          =new TH1F("h_e_dPhiIn_Endcap","",7,0,0.07); 
TH1F *e_Sieie_B           =new TH1F("h_e_Sieie_Barrel","",40,0,0.04); 
TH1F *e_Sieie_E           =new TH1F("h_e_Sieie_Endcap","",40,0,0.04); 
TH1F *e_missingHits_B     =new TH1F("h_e_missingHits_Barrel","",20,0,2);   
TH1F *e_missingHits_E     =new TH1F("h_e_missingHits_Endcap","",20,0,2);   
TH1F *e_dxyFirstPV_B      =new TH1F("h_e_dxyFirstPV_Barrel","",50,0,0.05);     
TH1F *e_dxyFirstPV_E      =new TH1F("h_e_dxyFirstPV_Endcap","",50,0,0.05);     
TH1F *e_HOverE_B          =new TH1F("h_e_HOverE_Barrel","",20,0,0.2); 
TH1F *e_HOverE_E          =new TH1F("h_e_HOverE_Endcap","",20,0,0.2); 
TH1F *e_E1x5OverE5x5_B    =new TH1F("h_e_E1x5OverE5x5_Barrel","",100,0,1);
TH1F *e_E1x5OverE5x5_E    =new TH1F("h_e_E1x5OverE5x5_Endcap","",100,0,1);
TH1F *e_E2x5OverE5x5_B    =new TH1F("h_e_E2x5OverE5x5_Barrel","",100,0,1);    
TH1F *e_E2x5OverE5x5_E    =new TH1F("h_e_E2x5OverE5x5_Endcap","",100,0,1);    
TH1F *e_isolEMHadDepth1_B =new TH1F("h_e_isolEMHadDepth1_Barrel","",100,0,10);
TH1F *e_isolEMHadDepth1_E =new TH1F("h_e_isolEMHadDepth1_Endcap","",100,0,10);
TH1F *e_IsolPtTrks_B      =new TH1F("h_e_IsolPtTrks_Barrel","",50,0,5); 
TH1F *e_IsolPtTrks_E      =new TH1F("h_e_IsolPtTrks_Endcap","",50,0,5); 
TH1F *e_dEtaIn_B          =new TH1F("h_e_dEtaIn_Barrel","",7,0,0.007);         
TH1F *e_dEtaIn_B_er       =new TH1F("h_e_dEtaIn_Barrel_er","",7,0,0.007);         
TH1F *e_dEtaIn_E          =new TH1F("h_e_dEtaIn_Endcap","",7,0,0.007);         


double event_weight=1;
float fake_rate=1;
float L1_weight=1;
double fewz_weight=1;
bool do_PU_weight=true; 
bool do_L1_weight=false;//don't use
bool do_data_mass_scale=false;
bool do_FR_1F =false;
bool do_FR_2F =false;
bool do_fewz_weight=false;
if(is_FR_1F) do_FR_1F=true;
if(is_FR_2F) do_FR_2F=true;
if(is_ZToEE && is_fewz) do_fewz_weight=true;
if(is_data==true){do_L1_weight=false;
                  do_PU_weight=false;
                  do_fewz_weight=false;
                 }
if(is_data==false)do_data_mass_scale=false;
///// fewz /////
//TF1 *fewzKFactor = new TF1("fit","pol3",120,6000);
//fewzKFactor->SetParameters(1.06780e+00,-1.20666e-04,3.22646e-08,-3.94886e-12);
////////
TFile *f_L1Map= new TFile("l1EGJet200EffMapAllMC.root");
TH2D *h_L1Map = (TH2D*)f_L1Map->Get("l1EGJet200EffMapHist");
for(int i=0;i<t->GetEntries();i++){
t->GetEntry(i);

if(do_PU_weight==true) {event_weight=w_PU_combined;
                        if(uncert=="PU_scale_up") event_weight=w_PU_silver_up;
                        else if(uncert=="PU_scale_down") event_weight=w_PU_silver_down;
                       }
else event_weight=event_sign;

if(do_L1_weight==true){

if(e1_Et<4000 && e2_Et<4000 && fabs(e1_eta)<2.5 && fabs(e2_eta)<2.5){
float e1_weight=1;
float e2_weight=1;
TAxis *Xaxis = h_L1Map->GetXaxis();
TAxis *Yaxis = h_L1Map->GetYaxis();
Int_t binx_e1 = Xaxis->FindBin(e1_eta);
Int_t biny_e1 = Yaxis->FindBin(e1_Et);
Int_t binx_e2 = Xaxis->FindBin(e2_eta);
Int_t biny_e2 = Yaxis->FindBin(e2_Et);
if(fabs(e1_eta)<1.5 || e1_Et>50) e1_weight= h_L1Map->GetBinContent(binx_e1,biny_e1) ==0 ? 1 : h_L1Map->GetBinContent(binx_e1,biny_e1);
else e1_weight =  0.5*0.997*(1+TMath::Erf((e1_Et+22.8)/(sqrt(2)*27.4)));
if(fabs(e2_eta)<1.5 || e2_Et>50) e2_weight= h_L1Map->GetBinContent(binx_e2,biny_e2) ==0 ? 1 : h_L1Map->GetBinContent(binx_e2,biny_e2);
else e2_weight =  0.5*0.997*(1+TMath::Erf((e2_Et+22.8)/(sqrt(2)*27.4)));

L1_weight=e1_weight*e2_weight;
}

else L1_weight=1;
}
else L1_weight=1;

if(do_FR_1F==true) fake_rate=frFuncData(e2_Et, e2_eta)/(1-frFuncData(e2_Et, e2_eta));
else if(do_FR_2F==true)fake_rate=(frFuncData(e1_Et, e1_eta)/(1-frFuncData(e1_Et, e1_eta)))*(frFuncData(e2_Et, e2_eta)/(1-frFuncData(e2_Et, e2_eta)));
else fake_rate=1;

if(do_fewz_weight) {
                    //fewz_weight = 1.01696-7.73522E-5*mee+6.69239E-9*mee*mee;
                    //if(fewz_weight>1) fewz_weight=1;
                    if(mee>120)fewz_weight = 1.06780 - 1.20666e-04*mee + 3.22646e-08*mee*mee - 3.94886e-12*mee*mee*mee;
                    else fewz_weight=1;
                   }
else fewz_weight=1;
event_weight=fake_rate*event_weight*L1_weight*fewz_weight;

///////////// mass scale

float mee_tmp=mee;
if(do_data_mass_scale==true){
if(fabs(e1_eta)>1.566 && fabs(e1_eta)<2.5 && fabs(e2_eta)>1.566 && fabs(e2_eta)<2.5 ) {mee_tmp=1.003*mee;}
else if(fabs(e1_eta)<1.4442 && fabs(e2_eta)<1.4442){mee_tmp=1.017*mee;}
else if(fabs(e1_eta)<1.4442 && (fabs(e2_eta)>1.566 && fabs(e2_eta)<2.5) ){mee_tmp=1.010*mee;}
else if(fabs(e2_eta)<1.4442 && (fabs(e1_eta)>1.566 && fabs(e1_eta)<2.5) ){mee_tmp=1.010*mee;}
}
/////////////
TAxis *xaxis = h_mee_all->GetXaxis();
Int_t binx = xaxis->FindBin(mee_tmp);
Float_t bin_width=h_mee_all->GetXaxis()->GetBinWidth(binx);

TAxis *xaxis_EE = h_mee_all_EE_v1->GetXaxis();
Int_t binx_EE = xaxis_EE->FindBin(mee_tmp);
Float_t bin_width_EE=h_mee_all_EE_v1->GetXaxis()->GetBinWidth(binx_EE);

TAxis *xaxis_sin = h_mee_all_sin->GetXaxis();
Int_t binx_sin = xaxis_sin->FindBin(mee_tmp);
Float_t bin_width_sin=h_mee_all_sin->GetXaxis()->GetBinWidth(binx_sin);

TAxis *xaxis_big = h_mee_all_big->GetXaxis();
Int_t binx_big = xaxis_big->FindBin(mee_tmp);
Float_t bin_width_big=h_mee_all_big->GetXaxis()->GetBinWidth(binx_big);


if(fabs(e1_eta)>1.566 && fabs(e1_eta)<2.5 && fabs(e2_eta)>1.566 && fabs(e2_eta)<2.5 ) {
h_mee_Zpeak_EE->Fill(mee_tmp,event_weight);
h_mee_all_EE->Fill(mee_tmp,event_weight/bin_width);
h_mee_all_EE_big->Fill(mee_tmp,event_weight/bin_width_big);
h_mee_all_EE_v1->Fill(mee_tmp,event_weight/bin_width_EE);
h_mee_all_EE_sin->Fill(mee_tmp,event_weight);
if(mee_tmp<=4000) h_mee_all_cum_EE->Fill(mee_tmp,event_weight);
else              h_mee_all_cum_EE->Fill(3999   ,event_weight);
if(mee_tmp<=4000) h_mee_EE_usual->Fill(mee_tmp,event_weight);
else              h_mee_EE_usual->Fill(3999   ,event_weight);

continue;
}
if(fabs(e1_eta)>2.5 && fabs(e2_eta)>2.5) continue;
//if(mee_tmp > 1700) std::cout<<"mass="<<mee_tmp<<std::endl;
if(fabs(e1_eta)<1.4442 && fabs(e2_eta)<1.4442){h_mee_Zpeak_BB->Fill(mee_tmp,event_weight);
                                               h_mee_all_BB->Fill(mee_tmp,event_weight/bin_width);
                                               h_mee_all_BB_big->Fill(mee_tmp,event_weight/bin_width_big);
                                               h_mee_all_BB_sin->Fill(mee_tmp,event_weight);
                                               if(mee_tmp<=4000) h_mee_all_cum_BB->Fill(mee_tmp,event_weight);
                                               else              h_mee_all_cum_BB->Fill(3999   ,event_weight);
                                               if(mee_tmp<=4000) h_mee_BB_usual->Fill(mee_tmp,event_weight);
                                               else              h_mee_BB_usual->Fill(3999   ,event_weight);
                                              }
else if(fabs(e1_eta)<1.4442 && (fabs(e2_eta)>1.566 && fabs(e2_eta)<2.5) ){h_mee_Zpeak_BE->Fill(mee_tmp,event_weight);
                                                                          h_mee_all_BE->Fill(mee_tmp,event_weight/bin_width);
                                                                          h_mee_all_BE_big->Fill(mee_tmp,event_weight/bin_width_big);
                                                                          h_mee_all_BE_sin->Fill(mee_tmp,event_weight);
                                                                          if(mee_tmp<=4000) h_mee_all_cum_BE->Fill(mee_tmp,event_weight);
                                                                          else              h_mee_all_cum_BE->Fill(3999   ,event_weight);
                                                                          if(mee_tmp<=4000) h_mee_BE_usual->Fill(mee_tmp,event_weight);
                                                                          else              h_mee_BE_usual->Fill(3999   ,event_weight);
                                                                         }
else if(fabs(e2_eta)<1.4442 && (fabs(e1_eta)>1.566 && fabs(e1_eta)<2.5) ){h_mee_Zpeak_BE->Fill(mee_tmp,event_weight);
                                                                          h_mee_all_BE->Fill(mee_tmp,event_weight/bin_width);
                                                                          h_mee_all_BE_big->Fill(mee_tmp,event_weight/bin_width_big);
                                                                          h_mee_all_BE_sin->Fill(mee_tmp,event_weight);
                                                                          if(mee_tmp<=4000) h_mee_all_cum_BE->Fill(mee_tmp,event_weight);
                                                                          else              h_mee_all_cum_BE->Fill(3999   ,event_weight);
                                                                          if(mee_tmp<=4000) h_mee_BE_usual->Fill(mee_tmp,event_weight);
                                                                          else              h_mee_BE_usual->Fill(3999   ,event_weight);
                                                                         }
 
h_mee_all->Fill(mee_tmp,event_weight/bin_width);
h_mee_all_big->Fill(mee_tmp,event_weight/bin_width_big);
h_mee_all_sin->Fill(mee_tmp,event_weight);
if(mee_tmp<=4000) h_mee_all_cum->Fill(mee_tmp,event_weight);
else              h_mee_all_cum->Fill(3999   ,event_weight);
if(mee_tmp<=4000)h_mee_usual->Fill(mee_tmp,event_weight);
else             h_mee_usual->Fill(3999   ,event_weight);
h_mee_high->Fill(mee_tmp,event_weight);
h_mee_Zpeak->Fill(mee_tmp,event_weight);
h_mee_cail->Fill(mee_tmp,event_weight);

h_Pt->Fill(Pt,event_weight);
h_pv_n->Fill(pv_n,event_weight);
h_rho->Fill(rho,event_weight);
h_OS->Fill(OS,event_weight);
h_e1_Et->Fill(e1_Et,event_weight);
h_e1_eta->Fill(e1_eta,event_weight);
h_e1_phi->Fill(e1_phi,event_weight);
h_e2_Et->Fill(e2_Et,event_weight);
h_e2_eta->Fill(e2_eta,event_weight);
h_e2_phi->Fill(e2_phi,event_weight);

if(fabs(e1_eta)<1.4442){
h_e_Et_B->Fill(e1_Et, event_weight);
e1_dPhiIn_B->Fill(e1_dPhiIn,event_weight);         
e1_Sieie_B->Fill(e1_Sieie,event_weight);          
e1_missingHits_B->Fill(e1_missingHits,event_weight);    
e1_dxyFirstPV_B->Fill(e1_dxyFirstPV,event_weight);     
e1_HOverE_B->Fill(e1_HOverE,event_weight);         
e1_E1x5OverE5x5_B->Fill(e1_E1x5OverE5x5,event_weight);   
e1_E2x5OverE5x5_B->Fill(e1_E2x5OverE5x5,event_weight);   
e1_isolEMHadDepth1_B->Fill(e1_isolEMHadDepth1,event_weight);
e1_IsolPtTrks_B->Fill(e1_IsolPtTrks,event_weight);     
e1_dEtaIn_B->Fill(e1_dEtaIn,event_weight);         
if(fabs(e1_eta)<0.5) e1_dEtaIn_B_er->Fill(e1_dEtaIn,event_weight);         
}
else if(fabs(e1_eta)>1.566 && fabs(e1_eta)<2.5){
h_e_Et_E->Fill(e1_Et, event_weight);
e1_dPhiIn_E->Fill(e1_dPhiIn,event_weight);         
e1_Sieie_E->Fill(e1_Sieie,event_weight);          
e1_missingHits_E->Fill(e1_missingHits,event_weight);    
e1_dxyFirstPV_E->Fill(e1_dxyFirstPV,event_weight);     
e1_HOverE_E->Fill(e1_HOverE,event_weight);         
e1_E1x5OverE5x5_E->Fill(e1_E1x5OverE5x5,event_weight);   
e1_E2x5OverE5x5_E->Fill(e1_E2x5OverE5x5,event_weight);   
e1_isolEMHadDepth1_E->Fill(e1_isolEMHadDepth1,event_weight);
e1_IsolPtTrks_E->Fill(e1_IsolPtTrks,event_weight);     
e1_dEtaIn_E->Fill(e1_dEtaIn,event_weight);         
}
else{int a=1;}

if(fabs(e2_eta)<1.4442){
h_e_Et_B->Fill(e2_Et, event_weight);
e2_dPhiIn_B->Fill(e2_dPhiIn,event_weight);         
e2_Sieie_B->Fill(e2_Sieie,event_weight);          
e2_missingHits_B->Fill(e2_missingHits,event_weight);    
e2_dxyFirstPV_B->Fill(e2_dxyFirstPV,event_weight);     
e2_HOverE_B->Fill(e2_HOverE,event_weight);         
e2_E1x5OverE5x5_B->Fill(e2_E1x5OverE5x5,event_weight);   
e2_E2x5OverE5x5_B->Fill(e2_E2x5OverE5x5,event_weight);   
e2_isolEMHadDepth1_B->Fill(e2_isolEMHadDepth1,event_weight);
e2_IsolPtTrks_B->Fill(e2_IsolPtTrks,event_weight);     
e2_dEtaIn_B->Fill(e2_dEtaIn,event_weight);         
if(fabs(e1_eta)<0.5) e2_dEtaIn_B_er->Fill(e2_dEtaIn,event_weight);         
}
else if(fabs(e2_eta)>1.566 && fabs(e2_eta)<2.5){
h_e_Et_E->Fill(e2_Et, event_weight);
e2_dPhiIn_E->Fill(e2_dPhiIn,event_weight);         
e2_Sieie_E->Fill(e2_Sieie,event_weight);          
e2_missingHits_E->Fill(e2_missingHits,event_weight);    
e2_dxyFirstPV_E->Fill(e2_dxyFirstPV,event_weight);     
e2_HOverE_E->Fill(e2_HOverE,event_weight);         
e2_E1x5OverE5x5_E->Fill(e2_E1x5OverE5x5,event_weight);   
e2_E2x5OverE5x5_E->Fill(e2_E2x5OverE5x5,event_weight);   
e2_isolEMHadDepth1_E->Fill(e2_isolEMHadDepth1,event_weight);
e2_IsolPtTrks_E->Fill(e2_IsolPtTrks,event_weight);     
e2_dEtaIn_E->Fill(e2_dEtaIn,event_weight);         
}
else{int a=1;}

}
///////////////////////
e_dPhiIn_B          ->Add(e1_dPhiIn_B,e2_dPhiIn_B,1,1);
e_dPhiIn_E          ->Add(e1_dPhiIn_E,e2_dPhiIn_E,1,1);
e_Sieie_B           ->Add(e1_Sieie_B,e2_Sieie_B,1,1);
e_Sieie_E           ->Add(e1_Sieie_E,e2_Sieie_E,1,1);
e_missingHits_B     ->Add(e1_missingHits_B,e2_missingHits_B,1,1);
e_missingHits_E     ->Add(e1_missingHits_E,e2_missingHits_E,1,1);
e_dxyFirstPV_B      ->Add(e1_dxyFirstPV_B,e2_dxyFirstPV_B,1,1);
e_dxyFirstPV_E      ->Add(e1_dxyFirstPV_E,e2_dxyFirstPV_E,1,1);
e_HOverE_B          ->Add(e1_HOverE_B,e2_HOverE_B,1,1);
e_HOverE_E          ->Add(e1_HOverE_E,e2_HOverE_E,1,1);
e_E1x5OverE5x5_B    ->Add(e1_E1x5OverE5x5_B,e2_E1x5OverE5x5_B,1,1);
e_E1x5OverE5x5_E    ->Add(e1_E1x5OverE5x5_E,e2_E1x5OverE5x5_E,1,1);
e_E2x5OverE5x5_B    ->Add(e1_E2x5OverE5x5_B,e2_E2x5OverE5x5_B,1,1);
e_E2x5OverE5x5_E    ->Add(e1_E2x5OverE5x5_E,e2_E2x5OverE5x5_E,1,1);
e_isolEMHadDepth1_B ->Add(e1_isolEMHadDepth1_B,e2_isolEMHadDepth1_B,1,1);
e_isolEMHadDepth1_E ->Add(e1_isolEMHadDepth1_E,e2_isolEMHadDepth1_E,1,1);
e_IsolPtTrks_B      ->Add(e1_IsolPtTrks_B,e2_IsolPtTrks_B,1,1);
e_IsolPtTrks_E      ->Add(e1_IsolPtTrks_E,e2_IsolPtTrks_E,1,1);
e_dEtaIn_B          ->Add(e1_dEtaIn_B,e2_dEtaIn_B,1,1);
e_dEtaIn_B_er       ->Add(e1_dEtaIn_B_er,e2_dEtaIn_B_er,1,1);
e_dEtaIn_E          ->Add(e1_dEtaIn_E,e2_dEtaIn_E,1,1);
/////////////////////

//TH1 *H_mee_all_cum = h_mee_all_cum->GetCumulative(kFALSE,"");
//TH1 *H_mee_all_cum_BB = h_mee_all_cum_BB->GetCumulative(kFALSE,"");
//TH1 *H_mee_all_cum_EE = h_mee_all_cum_EE->GetCumulative(kFALSE,"");
//TH1 *H_mee_all_cum_BE = h_mee_all_cum_BE->GetCumulative(kFALSE,"");

//////////rebin signal region plot/////////////////////
if(false){

std::cout<<"bining for sin_all"<<std::endl;
int low=1;
for(int i=1; i<=h_mee_all_sin->GetNbinsX();i++){
int high=i;
if(h_mee_all_sin->Integral(low,high)>10){
//std::cout<<"bin="<<i<<",low="<<h_mee_all_sin->GetXaxis()->GetBinLowEdge(low)<<",high="<<h_mee_all_sin->GetXaxis()->GetBinLowEdge(high)+h_mee_all_sin->GetXaxis()->GetBinWidth(high)<<std::endl;
std::cout<<"Bin_mee_sin_all["<<i-1<<"]="<<h_mee_all_sin->GetXaxis()->GetBinLowEdge(low)<<std::endl;
low=high+1;}
if(i==h_mee_all_sin->GetNbinsX()){std::cout<<"last bin="<<i<<",low="<<h_mee_all_sin->GetXaxis()->GetBinLowEdge(low)<<",high="<<h_mee_all_sin->GetXaxis()->GetBinLowEdge(high)+h_mee_all_sin->GetXaxis()->GetBinWidth(high)<<",event="<<h_mee_all_sin->Integral(low,high)<<std::endl;}
}

std::cout<<"bining for sin_BB_all"<<std::endl;
low=1;
for(int i=1; i<=h_mee_all_BB_sin->GetNbinsX();i++){
int high=i;
if(h_mee_all_BB_sin->Integral(low,high)>10){
std::cout<<"Bin_mee_sin_BB_all["<<i-1<<"]="<<h_mee_all_BB_sin->GetXaxis()->GetBinLowEdge(low)<<std::endl;
low=high+1;}
if(i==h_mee_all_BB_sin->GetNbinsX()){std::cout<<"last bin="<<i<<",low="<<h_mee_all_BB_sin->GetXaxis()->GetBinLowEdge(low)<<",high="<<h_mee_all_BB_sin->GetXaxis()->GetBinLowEdge(high)+h_mee_all_BB_sin->GetXaxis()->GetBinWidth(high)<<",event="<<h_mee_all_BB_sin->Integral(low,high)<<std::endl;}
}

std::cout<<"bining for sin_BE_all"<<std::endl;
low=1;
for(int i=1; i<=h_mee_all_BE_sin->GetNbinsX();i++){
int high=i;
if(h_mee_all_BE_sin->Integral(low,high)>10){
std::cout<<"Bin_mee_sin_BE_all["<<i-1<<"]="<<h_mee_all_BE_sin->GetXaxis()->GetBinLowEdge(low)<<std::endl;
low=high+1;}
if(i==h_mee_all_BE_sin->GetNbinsX()){std::cout<<"last bin="<<i<<",low="<<h_mee_all_BE_sin->GetXaxis()->GetBinLowEdge(low)<<",high="<<h_mee_all_BE_sin->GetXaxis()->GetBinLowEdge(high)+h_mee_all_BE_sin->GetXaxis()->GetBinWidth(high)<<",event="<<h_mee_all_BE_sin->Integral(low,high)<<std::endl;}
}

std::cout<<"bining for sin_EE_all"<<std::endl;
low=1;
for(int i=1; i<=h_mee_all_EE_sin->GetNbinsX();i++){
int high=i;
if(h_mee_all_EE_sin->Integral(low,high)>10){
std::cout<<"Bin_mee_sin_EE_all["<<i-1<<"]="<<h_mee_all_EE_sin->GetXaxis()->GetBinLowEdge(low)<<std::endl;
low=high+1;}
if(i==h_mee_all_EE_sin->GetNbinsX()){std::cout<<"last bin="<<i<<",low="<<h_mee_all_EE_sin->GetXaxis()->GetBinLowEdge(low)<<",high="<<h_mee_all_EE_sin->GetXaxis()->GetBinLowEdge(high)+h_mee_all_EE_sin->GetXaxis()->GetBinWidth(high)<<",event="<<h_mee_all_EE_sin->Integral(low,high)<<std::endl;}
}

}
///////////////////////////////////////////////////////

TFile *f = new TFile(output_file,"RECREATE");
f->cd();

h_pv_n->Write();
h_rho->Write();
h_OS->Write();
                      
h_mee_all->Write();
h_mee_all_BB->Write();
h_mee_all_EE->Write();
h_mee_all_EE_v1->Write();
h_mee_all_BE->Write();
h_mee_all_sin->Write();
h_mee_all_BB_sin->Write();
h_mee_all_EE_sin->Write();
h_mee_all_BE_sin->Write();
h_mee_all_big->Write();
h_mee_all_BB_big->Write();
h_mee_all_EE_big->Write();
h_mee_all_BE_big->Write();
//H_mee_all_cum->Write();
//H_mee_all_cum_BB->Write();
//H_mee_all_cum_EE->Write();
//H_mee_all_cum_BE->Write();
h_mee_all_cum->Write();
h_mee_all_cum_BB->Write();
h_mee_all_cum_EE->Write();
h_mee_all_cum_BE->Write();
h_mee_usual->Write();
h_mee_BB_usual->Write();
h_mee_BE_usual->Write();
h_mee_EE_usual->Write();
h_mee_high->Write();
h_mee_Zpeak->Write();
h_mee_Zpeak_BB->Write();
h_mee_Zpeak_EE->Write();
h_mee_Zpeak_BE->Write();
h_mee_cail->Write();
                      
h_Pt->Write();
h_e1_Et->Write();
h_e1_eta->Write();
h_e1_phi->Write();
h_e2_Et->Write();
h_e2_eta->Write();
h_e2_phi->Write();
h_e_Et_B->Write();                      
h_e_Et_E->Write();                      
e1_dPhiIn_B->Write();
e1_dPhiIn_E->Write();
e1_Sieie_B->Write();
e1_Sieie_E->Write();
e1_missingHits_B->Write();
e1_missingHits_E->Write();
e1_dxyFirstPV_B->Write();
e1_dxyFirstPV_E->Write();
e1_HOverE_B->Write();
e1_HOverE_E->Write();
e1_E1x5OverE5x5_B->Write();
e1_E1x5OverE5x5_E->Write();
e1_E2x5OverE5x5_B->Write();
e1_E2x5OverE5x5_E->Write();
e1_isolEMHadDepth1_B->Write();
e1_isolEMHadDepth1_E->Write();
e1_IsolPtTrks_B->Write();
e1_IsolPtTrks_E->Write();
e1_dEtaIn_B->Write();
e1_dEtaIn_E->Write();

e2_dPhiIn_B->Write();
e2_dPhiIn_E->Write();
e2_Sieie_B->Write();
e2_Sieie_E->Write();
e2_missingHits_B->Write();
e2_missingHits_E->Write();
e2_dxyFirstPV_B->Write();
e2_dxyFirstPV_E->Write();
e2_HOverE_B->Write();
e2_HOverE_E->Write();
e2_E1x5OverE5x5_B->Write();
e2_E1x5OverE5x5_E->Write();
e2_E2x5OverE5x5_B->Write();
e2_E2x5OverE5x5_E->Write();
e2_isolEMHadDepth1_B->Write();
e2_isolEMHadDepth1_E->Write();
e2_IsolPtTrks_B->Write();
e2_IsolPtTrks_E->Write();
e2_dEtaIn_B->Write();
e2_dEtaIn_E->Write();

e_dPhiIn_B->Write();
e_dPhiIn_E->Write();
e_Sieie_B->Write();
e_Sieie_E->Write();
e_missingHits_B->Write();
e_missingHits_E->Write();
e_dxyFirstPV_B->Write();
e_dxyFirstPV_E->Write();
e_HOverE_B->Write();
e_HOverE_E->Write();
e_E1x5OverE5x5_B->Write();
e_E1x5OverE5x5_E->Write();
e_E2x5OverE5x5_B->Write();
e_E2x5OverE5x5_E->Write();
e_isolEMHadDepth1_B->Write();
e_isolEMHadDepth1_E->Write();
e_IsolPtTrks_B->Write();
e_IsolPtTrks_E->Write();
e_dEtaIn_B->Write();
e_dEtaIn_B_er->Write();
e_dEtaIn_E->Write();
f->Close();
//f_L1Map->Close();
h_pv_n->Delete();
h_rho->Delete();
h_OS->Delete();
                      
h_mee_all->Delete();
h_mee_all_BB->Delete();
h_mee_all_EE->Delete();
h_mee_all_EE_v1->Delete();
h_mee_all_BE->Delete();
h_mee_all_sin->Delete();
h_mee_all_BB_sin->Delete();
h_mee_all_EE_sin->Delete();
h_mee_all_BE_sin->Delete();
h_mee_all_big->Delete();
h_mee_all_BB_big->Delete();
h_mee_all_EE_big->Delete();
h_mee_all_BE_big->Delete();
h_mee_all_cum->Delete();
h_mee_all_cum_BB->Delete();
h_mee_all_cum_EE->Delete();
h_mee_all_cum_BE->Delete();
//H_mee_all_cum->Delete();
//H_mee_all_cum_BB->Delete();
//H_mee_all_cum_EE->Delete();
//H_mee_all_cum_BE->Delete();
h_mee_usual->Delete();
h_mee_BB_usual->Delete();
h_mee_BE_usual->Delete();
h_mee_EE_usual->Delete();
h_mee_high->Delete();
h_mee_Zpeak->Delete();
h_mee_Zpeak_BB->Delete();
h_mee_Zpeak_EE->Delete();
h_mee_Zpeak_BE->Delete();
h_mee_cail->Delete();
                      
h_Pt->Delete();
h_e1_Et->Delete();
h_e1_eta->Delete();
h_e1_phi->Delete();
h_e2_Et->Delete();
h_e2_eta->Delete();
h_e2_phi->Delete();
h_e_Et_B->Delete();                      
h_e_Et_E->Delete();                      
                      
e1_dPhiIn_B->Delete();
e1_dPhiIn_E->Delete();
e1_Sieie_B->Delete();
e1_Sieie_E->Delete();
e1_missingHits_B->Delete();
e1_missingHits_E->Delete();
e1_dxyFirstPV_B->Delete();
e1_dxyFirstPV_E->Delete();
e1_HOverE_B->Delete();
e1_HOverE_E->Delete();
e1_E1x5OverE5x5_B->Delete();
e1_E1x5OverE5x5_E->Delete();
e1_E2x5OverE5x5_B->Delete();
e1_E2x5OverE5x5_E->Delete();
e1_isolEMHadDepth1_B->Delete();
e1_isolEMHadDepth1_E->Delete();
e1_IsolPtTrks_B->Delete();
e1_IsolPtTrks_E->Delete();
e1_dEtaIn_B->Delete();
e1_dEtaIn_B_er->Delete();
e1_dEtaIn_E->Delete();

e2_dPhiIn_B->Delete();
e2_dPhiIn_E->Delete();
e2_Sieie_B->Delete();
e2_Sieie_E->Delete();
e2_missingHits_B->Delete();
e2_missingHits_E->Delete();
e2_dxyFirstPV_B->Delete();
e2_dxyFirstPV_E->Delete();
e2_HOverE_B->Delete();
e2_HOverE_E->Delete();
e2_E1x5OverE5x5_B->Delete();
e2_E1x5OverE5x5_E->Delete();
e2_E2x5OverE5x5_B->Delete();
e2_E2x5OverE5x5_E->Delete();
e2_isolEMHadDepth1_B->Delete();
e2_isolEMHadDepth1_E->Delete();
e2_IsolPtTrks_B->Delete();
e2_IsolPtTrks_E->Delete();
e2_dEtaIn_B->Delete();
e2_dEtaIn_B_er->Delete();
e2_dEtaIn_E->Delete();

e_dPhiIn_B->Delete();
e_dPhiIn_E->Delete();
e_Sieie_B->Delete();
e_Sieie_E->Delete();
e_missingHits_B->Delete();
e_missingHits_E->Delete();
e_dxyFirstPV_B->Delete();
e_dxyFirstPV_E->Delete();
e_HOverE_B->Delete();
e_HOverE_E->Delete();
e_E1x5OverE5x5_B->Delete();
e_E1x5OverE5x5_E->Delete();
e_E2x5OverE5x5_B->Delete();
e_E2x5OverE5x5_E->Delete();
e_isolEMHadDepth1_B->Delete();
e_isolEMHadDepth1_E->Delete();
e_IsolPtTrks_B->Delete();
e_IsolPtTrks_E->Delete();
e_dEtaIn_B->Delete();
e_dEtaIn_B_er->Delete();
e_dEtaIn_E->Delete();
std::cout<<output_file<<" is saved"<<std::endl;
}
