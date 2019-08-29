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
#include <TString.h>
#include <math.h>
#include <TMath.h>
#include <string>
#include "Fake_rate_2016_2017_2018.C"
#include "turnonDoubleEle_2016_2017_2018.C"
#include "MC_pileup_weight_2016_2017_2018.C"
#include "PU_reWeighting_2018_per_MC.C"
#include "/user/wenxing/ST_TW_channel/CMSSW_10_2_13/src/l1PrescaleInfo/l1PrescaleFuncs.C"
#include "/user/wenxing/ST_TW_channel/CMSSW_10_2_13/src/l1PrescaleInfo/turnonEle33l1.C"
const float PI_F=3.14159265358979;
const float m_el = 0.000511 ;
const float M_Z =  91.2;
const float L1_DeltaR=0.3;
const float SingleL1_threshold=45;

TString Year = "2018" ;

bool applyPreFiringW = true;// be nominal

bool use_Z_mass_suppress=true;// be nominal

bool use_DoubleEle25=false;//only be true for 2018, false is for DoubleEle33 trigger

bool use_L1SingleEG =true;//true for 2017 only

bool LHE_Mass_cut=false;//not used , using DYToEE_pow get 50-120 GeV

bool check_Et=false;// not used 
bool use_gsf_sf=false;// not used
bool match_to_seed_led=false;// match electron to seeded leg of HLT to do a check
bool check_sc_et=false;

bool remove_saturated=false;// check the effect of saturation
bool OnlyFor1TeV=false; // check only for 1 TeV
TString PU_data="";//init

float scale_factor( TH2F* h, float pt, float eta , TString uncert);
void fill_cum(TH1D* &hist, float M , double weight);
void Remove_negative_events(TH1D * &h);
int matching(vector<float> *eta, vector<float> *phi, float eta_1, float phi_1);
float sf_weight(float Et, float eta, TString uncert);
int L1_trigger_match(float eta, float phi, vector<float> *filter_eta, vector<float> *filter_phi, vector<float> *filter_et,int runnr, int lumisec );
int L1_trigger_match_s(float eta, float phi, vector<float> *filter_eta, vector<float> *filter_phi, vector<float> *filter_et);
float L1_trigger_match_Et(float eta, float phi, vector<float> *filter_eta, vector<float> *filter_phi, vector<float> *filter_et);
int trigger_match(float eta, float phi, vector<float> *filter_eta, vector<float> *filter_phi, int fire);
double calcCosThetaCSAnal(TLorentzVector v_dil, TLorentzVector v_mum, TLorentzVector v_mup) ;
double calcCosThetaCSAnal(double pz_mum, double e_mum, double pz_mup, double e_mup, double pt_dil, double pl_dil, double mass_dil) ;
void fill_hist(TString input_file, TString output_file, TString pu_name, bool is_data=false, bool is_ZToEE=false, bool do_fewz=false, bool do_FR_1F=false, bool do_FR_2F=false, TString uncert="");

void select_and_save(TString year, TString uncert_s ,TString pu_data){
Year = year ;
TString input_dir     ="/user/wenxing/ST_TW_channel/CMSSW_10_2_13/src/Zprime/reskim_script/reskim_out/for_plot/"+Year+"/";
//TString output_dir    ="/user/wenxing/ST_TW_channel/CMSSW_10_2_13/src/Zprime/ntuples/sys_saved_hist/"+Year+"/20190705_EEScale/";// 
TString output_dir    ="/user/wenxing/ST_TW_channel/CMSSW_10_2_13/src/Zprime/ntuples/sys_saved_hist/"+Year+"/20190809_UpdateRunD/"; 
if(Year=="2018") use_DoubleEle25=true;
PU_data=pu_data;
if(PU_data=="Run_all") output_dir=output_dir+"all/";
else if(PU_data=="Run_A") output_dir=output_dir+"Run_A/";
else if(PU_data=="Run_B") output_dir=output_dir+"Run_B/";
else if(PU_data=="Run_C") output_dir=output_dir+"Run_C/";
else if(PU_data=="Run_D") output_dir=output_dir+"Run_D/";
bool do_fewz=true;
TString str_fewz=do_fewz?"_fewz":"";
TString str_uncert="";
TString uncertainty="";
vector<TString> v_uncert;
v_uncert.push_back(uncert_s)             ;
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
else if (uncertainty=="pf_scale_up")          str_uncert="pf_scale_up_";
else if (uncertainty=="pf_scale_down")        str_uncert="pf_scale_down_";

//fill_hist("/user/wenxing/ST_TW_channel/CMSSW_10_1_4/src/Zprime/reskim_script/reskim_out/normal_perone/MiniAOD/EGamma/Syn_Jan.root"   ,output_dir+"hist_data_syn.root"     ,"",true,false,false,false,false,uncertainty);

if(Year=="2018"){
input_dir             ="/user/wenxing/ST_TW_channel/CMSSW_10_1_4/src/Zprime/reskim_script/reskim_out/for_plot/";

//fill_hist(input_dir+"data_Run_ABC.root"   ,output_dir+"hist_data_MiniAOD_RunABC.root"     ,"",true,false,false,false,false,uncertainty);
//fill_hist(input_dir+"Run_D.root"          ,output_dir+"hist_data_MiniAOD_RunD.root"       ,"",true,false,false,false,false,uncertainty);
/*
if(uncertainty=="nominal"){
if(PU_data=="Run_all"){
fill_hist(input_dir+"Run*.root"   ,output_dir+"hist_data_MiniAOD.root"     ,"",true,false,false,false,false,uncertainty);
fill_hist(input_dir+"Run*.root"   ,output_dir+"hist_data_FR1F_MiniAOD.root","",true,false,false,true ,false,uncertainty);
fill_hist(input_dir+"Run*.root"   ,output_dir+"hist_data_FR2F_MiniAOD.root","",true,false,false,false ,true,uncertainty);
}
else if(PU_data=="Run_A"){
fill_hist(input_dir+"Run_A.root"   ,output_dir+"hist_data_MiniAOD.root"     ,"",true,false,false,false,false,uncertainty);
fill_hist(input_dir+"Run_A.root"   ,output_dir+"hist_data_FR1F_MiniAOD.root","",true,false,false,true ,false,uncertainty);
fill_hist(input_dir+"Run_A.root"   ,output_dir+"hist_data_FR2F_MiniAOD.root","",true,false,false,false ,true,uncertainty);
}
else if(PU_data=="Run_B"){
fill_hist(input_dir+"Run_B.root"   ,output_dir+"hist_data_MiniAOD.root"     ,"",true,false,false,false,false,uncertainty);
fill_hist(input_dir+"Run_B.root"   ,output_dir+"hist_data_FR1F_MiniAOD.root","",true,false,false,true ,false,uncertainty);
fill_hist(input_dir+"Run_B.root"   ,output_dir+"hist_data_FR2F_MiniAOD.root","",true,false,false,false ,true,uncertainty);
}
else if(PU_data=="Run_C"){
fill_hist(input_dir+"Run_C.root"   ,output_dir+"hist_data_MiniAOD.root"     ,"",true,false,false,false,false,uncertainty);
fill_hist(input_dir+"Run_C.root"   ,output_dir+"hist_data_FR1F_MiniAOD.root","",true,false,false,true ,false,uncertainty);
fill_hist(input_dir+"Run_C.root"   ,output_dir+"hist_data_FR2F_MiniAOD.root","",true,false,false,false ,true,uncertainty);
}
else if(PU_data=="Run_D"){
fill_hist(input_dir+"Run_D.root"   ,output_dir+"hist_data_MiniAOD.root"     ,"",true,false,false,false,false,uncertainty);
fill_hist(input_dir+"Run_D.root"   ,output_dir+"hist_data_FR1F_MiniAOD.root","",true,false,false,true ,false,uncertainty);
fill_hist(input_dir+"Run_D.root"   ,output_dir+"hist_data_FR2F_MiniAOD.root","",true,false,false,false ,true,uncertainty);
}
}
*/

//fill_hist(input_dir+"DYToLL_mad*.root",output_dir+str_uncert+"hist_DYToLL_mad"+str_fewz+".root"   ,   "DYJetsToLL_M_50_mad",false,true,do_fewz,false,false,uncertainty);
/*
fill_hist(input_dir+   "DYToEE_pow.root"  ,output_dir+str_uncert+   "hist_ZToEE_50_120"+str_fewz+".root"   ,   "DYToEE_pow",false,true,do_fewz,false,false,uncertainty);
fill_hist(input_dir+   "DYToEE_pow.root"  ,output_dir+str_uncert+   "hist_ZToEE_50_120"+str_fewz+"_1F.root",   "DYToEE_pow",false,true,do_fewz,true,false,uncertainty);
*/


fill_hist(input_dir+   "ZToEE_50_120.root",output_dir+str_uncert+   "hist_ZToEE_50_120"+str_fewz+".root"   ,   "ZToEE_50_120",false,true,do_fewz,false,false,uncertainty);
fill_hist(input_dir+  "ZToEE_120_200.root",output_dir+str_uncert+  "hist_ZToEE_120_200"+str_fewz+".root"   ,  "ZToEE_120_200",false,true,do_fewz,false,false,uncertainty);
fill_hist(input_dir+  "ZToEE_200_400.root",output_dir+str_uncert+  "hist_ZToEE_200_400"+str_fewz+".root"   ,  "ZToEE_200_400",false,true,do_fewz,false,false,uncertainty);
fill_hist(input_dir+  "ZToEE_400_800.root",output_dir+str_uncert+  "hist_ZToEE_400_800"+str_fewz+".root"   ,  "ZToEE_400_800",false,true,do_fewz,false,false,uncertainty);
fill_hist(input_dir+ "ZToEE_800_1400.root",output_dir+str_uncert+ "hist_ZToEE_800_1400"+str_fewz+".root"   , "ZToEE_800_1400",false,true,do_fewz,false,false,uncertainty);
fill_hist(input_dir+"ZToEE_1400_2300.root",output_dir+str_uncert+"hist_ZToEE_1400_2300"+str_fewz+".root"   ,"ZToEE_1400_2300",false,true,do_fewz,false,false,uncertainty);
fill_hist(input_dir+"ZToEE_2300_3500.root",output_dir+str_uncert+"hist_ZToEE_2300_3500"+str_fewz+".root"   ,"ZToEE_2300_3500",false,true,do_fewz,false,false,uncertainty);
fill_hist(input_dir+"ZToEE_3500_4500.root",output_dir+str_uncert+"hist_ZToEE_3500_4500"+str_fewz+".root"   ,"ZToEE_3500_4500",false,true,do_fewz,false,false,uncertainty);
fill_hist(input_dir+"ZToEE_4500_6000.root",output_dir+str_uncert+"hist_ZToEE_4500_6000"+str_fewz+".root"   ,"ZToEE_4500_6000",false,true,do_fewz,false,false,uncertainty);
fill_hist(input_dir+ "ZToEE_6000_Inf.root",output_dir+str_uncert+ "hist_ZToEE_6000_Inf"+str_fewz+".root"   , "ZToEE_6000_Inf",false,true,do_fewz,false,false,uncertainty);

fill_hist(input_dir+   "ZToEE_50_120.root",output_dir+str_uncert+   "hist_ZToEE_50_120"+str_fewz+"_1F.root",   "ZToEE_50_120",false,true,do_fewz,true,false,uncertainty);
fill_hist(input_dir+  "ZToEE_120_200.root",output_dir+str_uncert+  "hist_ZToEE_120_200"+str_fewz+"_1F.root",  "ZToEE_120_200",false,true,do_fewz,true,false,uncertainty);
fill_hist(input_dir+  "ZToEE_200_400.root",output_dir+str_uncert+  "hist_ZToEE_200_400"+str_fewz+"_1F.root",  "ZToEE_200_400",false,true,do_fewz,true,false,uncertainty);
fill_hist(input_dir+  "ZToEE_400_800.root",output_dir+str_uncert+  "hist_ZToEE_400_800"+str_fewz+"_1F.root",  "ZToEE_400_800",false,true,do_fewz,true,false,uncertainty);
fill_hist(input_dir+ "ZToEE_800_1400.root",output_dir+str_uncert+ "hist_ZToEE_800_1400"+str_fewz+"_1F.root", "ZToEE_800_1400",false,true,do_fewz,true,false,uncertainty);
fill_hist(input_dir+"ZToEE_1400_2300.root",output_dir+str_uncert+"hist_ZToEE_1400_2300"+str_fewz+"_1F.root","ZToEE_1400_2300",false,true,do_fewz,true,false,uncertainty);
fill_hist(input_dir+"ZToEE_2300_3500.root",output_dir+str_uncert+"hist_ZToEE_2300_3500"+str_fewz+"_1F.root","ZToEE_2300_3500",false,true,do_fewz,true,false,uncertainty);
fill_hist(input_dir+"ZToEE_3500_4500.root",output_dir+str_uncert+"hist_ZToEE_3500_4500"+str_fewz+"_1F.root","ZToEE_3500_4500",false,true,do_fewz,true,false,uncertainty);
fill_hist(input_dir+"ZToEE_4500_6000.root",output_dir+str_uncert+"hist_ZToEE_4500_6000"+str_fewz+"_1F.root","ZToEE_4500_6000",false,true,do_fewz,true,false,uncertainty);
fill_hist(input_dir+ "ZToEE_6000_Inf.root",output_dir+str_uncert+ "hist_ZToEE_6000_Inf"+str_fewz+"_1F.root", "ZToEE_6000_Inf",false,true,do_fewz,true,false,uncertainty);


if(uncertainty!="pdf_scale_up" && uncertainty!="pdf_scale_down"){

fill_hist(input_dir+"DYToTT_amc_*.root"                          ,output_dir+str_uncert+"hist_ZToTT_amc.root"        ,"DYJetsToLL_M_50_amc"  ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"ST.root"                                    ,output_dir+str_uncert+"hist_ST.root"               ,"ST"                   ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"ST_anti.root"                               ,output_dir+str_uncert+"hist_ST_anti.root"          ,"ST_anti"              ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"WZTo2L2Q.root"                              ,output_dir+str_uncert+"hist_WZ_2L2Q.root"          , "WZTo2L2Q"            ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"WZTo3LNu.root"                              ,output_dir+str_uncert+"hist_WZ_3LNu.root"          , "WZTo3LNu"            ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"ZZTo2L2Nu.root"                             ,output_dir+str_uncert+"hist_ZZ_2L2Nu.root"         , "ZZTo2L2Nu"           ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"ZZTo2L2Q.root"                              ,output_dir+str_uncert+"hist_ZZ_2L2Q.root"          , "ZZTo2L2Q"            ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"ZZTo4L.root"                                ,output_dir+str_uncert+"hist_ZZ_4L.root"            , "ZZTo4L"              ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"WWTo2L2Nu_M200.root"                        ,output_dir+str_uncert+"hist_WW2L_200.root"         , "WWTo2L2Nu"           ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"WW_200_600.root"                            ,output_dir+str_uncert+"hist_WW2L_200_600.root"     , "WWTo2L2Nu_200_600"   ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"WW_600_1200.root"                           ,output_dir+str_uncert+"hist_WW2L_600_1200.root"    , "WWTo2L2Nu_600_1200"  ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"WW_1200_2500.root"                          ,output_dir+str_uncert+"hist_WW2L_1200_2500.root"   , "WWTo2L2Nu_1200_2500" ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"WW_2500_Inf.root"                           ,output_dir+str_uncert+"hist_WW2L_2500_Inf.root"    , "WWTo2L2Nu_2500_Inf"  ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"TTTo2L2Nu_M500_*.root"                      ,output_dir+str_uncert+"hist_TTbar2L_500.root"      , "TTTo2L2Nu"           ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"TTTo2L2Nu_500_800.root"                     ,output_dir+str_uncert+"hist_TTbar2L_500_800.root"  , "TTTo2L2Nu_500_800"   ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"TTTo2L2Nu_800_1200.root"                    ,output_dir+str_uncert+"hist_TTbar2L_800_1200.root" , "TTTo2L2Nu_800_1200"  ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"TTTo2L2Nu_1200_1800.root"                   ,output_dir+str_uncert+"hist_TTbar2L_1200_1800.root", "TTTo2L2Nu_1200_1800" ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"TTTo2L2Nu_1800_Inf.root"                    ,output_dir+str_uncert+"hist_TTbar2L_1800_Inf.root" , "TTTo2L2Nu_1800_Inf"  ,false,false,false,false,false,uncertainty);

///////////// 1F ///////////////////////////////

fill_hist(input_dir+"DYToTT_amc_*.root"                          ,output_dir+str_uncert+"hist_ZToTT_amc_1F.root"        ,"DYJetsToLL_M_50_amc"  ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"ST.root"                                    ,output_dir+str_uncert+"hist_ST_1F.root"               ,"ST"                   ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"ST_anti.root"                               ,output_dir+str_uncert+"hist_ST_anti_1F.root"          ,"ST_anti"              ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"WZTo2L2Q.root"                              ,output_dir+str_uncert+"hist_WZ_2L2Q_1F.root"          , "WZTo2L2Q"            ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"WZTo3LNu.root"                              ,output_dir+str_uncert+"hist_WZ_3LNu_1F.root"          , "WZTo3LNu"            ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"ZZTo2L2Nu.root"                             ,output_dir+str_uncert+"hist_ZZ_2L2Nu_1F.root"         , "ZZTo2L2Nu"           ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"ZZTo2L2Q.root"                              ,output_dir+str_uncert+"hist_ZZ_2L2Q_1F.root"          , "ZZTo2L2Q"            ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"ZZTo4L.root"                                ,output_dir+str_uncert+"hist_ZZ_4L_1F.root"            , "ZZTo4L"              ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"WWTo2L2Nu_M200.root"                        ,output_dir+str_uncert+"hist_WW2L_200_1F.root"         , "WWTo2L2Nu"           ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"WW_200_600.root"                            ,output_dir+str_uncert+"hist_WW2L_200_600_1F.root"     , "WWTo2L2Nu_200_600"   ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"WW_600_1200.root"                           ,output_dir+str_uncert+"hist_WW2L_600_1200_1F.root"    , "WWTo2L2Nu_600_1200"  ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"WW_1200_2500.root"                          ,output_dir+str_uncert+"hist_WW2L_1200_2500_1F.root"   , "WWTo2L2Nu_1200_2500" ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"WW_2500_Inf.root"                           ,output_dir+str_uncert+"hist_WW2L_2500_Inf_1F.root"    , "WWTo2L2Nu_2500_Inf"  ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"TTTo2L2Nu_M500_*.root"                      ,output_dir+str_uncert+"hist_TTbar2L_500_1F.root"      , "TTTo2L2Nu"           ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"TTTo2L2Nu_500_800.root"                     ,output_dir+str_uncert+"hist_TTbar2L_500_800_1F.root"  , "TTTo2L2Nu_500_800"   ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"TTTo2L2Nu_800_1200.root"                    ,output_dir+str_uncert+"hist_TTbar2L_800_1200_1F.root" , "TTTo2L2Nu_800_1200"  ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"TTTo2L2Nu_1200_1800.root"                   ,output_dir+str_uncert+"hist_TTbar2L_1200_1800_1F.root", "TTTo2L2Nu_1200_1800" ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"TTTo2L2Nu_1800_Inf.root"                    ,output_dir+str_uncert+"hist_TTbar2L_1800_Inf_1F.root" , "TTTo2L2Nu_1800_Inf"  ,false,false,false,true,false,uncertainty);
}

}//2018
else if(Year=="2017"){
input_dir             ="/user/wenxing/ST_TW_channel/CMSSW_9_4_0/src/Zprime/reskim_script/reskim_out/for_plot/";
fill_hist(input_dir+"RunF.root"   ,output_dir+"hist_test_runF.root"     ,"",true,false,false,false,false,uncertainty);
/*
if(uncertainty=="nominal"){
if(PU_data=="Run_all"){
fill_hist(input_dir+"Run*.root"   ,output_dir+"hist_data_MiniAOD.root"     ,"",true,false,false,false,false,uncertainty);
fill_hist(input_dir+"Run*.root"   ,output_dir+"hist_data_FR1F_MiniAOD.root","",true,false,false,true ,false,uncertainty);
fill_hist(input_dir+"Run*.root"   ,output_dir+"hist_data_FR2F_MiniAOD.root","",true,false,false,false ,true,uncertainty);
}
else if(PU_data=="Run_B"){
fill_hist(input_dir+"Run_B.root"   ,output_dir+"hist_data_MiniAOD.root"     ,"",true,false,false,false,false,uncertainty);
fill_hist(input_dir+"Run_B.root"   ,output_dir+"hist_data_FR1F_MiniAOD.root","",true,false,false,true ,false,uncertainty);
fill_hist(input_dir+"Run_B.root"   ,output_dir+"hist_data_FR2F_MiniAOD.root","",true,false,false,false ,true,uncertainty);
}
else if(PU_data=="Run_C"){
fill_hist(input_dir+"Run_C.root"   ,output_dir+"hist_data_MiniAOD.root"     ,"",true,false,false,false,false,uncertainty);
fill_hist(input_dir+"Run_C.root"   ,output_dir+"hist_data_FR1F_MiniAOD.root","",true,false,false,true ,false,uncertainty);
fill_hist(input_dir+"Run_C.root"   ,output_dir+"hist_data_FR2F_MiniAOD.root","",true,false,false,false ,true,uncertainty);
}
else if(PU_data=="Run_D"){
fill_hist(input_dir+"Run_D.root"   ,output_dir+"hist_data_MiniAOD.root"     ,"",true,false,false,false,false,uncertainty);
fill_hist(input_dir+"Run_D.root"   ,output_dir+"hist_data_FR1F_MiniAOD.root","",true,false,false,true ,false,uncertainty);
fill_hist(input_dir+"Run_D.root"   ,output_dir+"hist_data_FR2F_MiniAOD.root","",true,false,false,false ,true,uncertainty);
}
else if(PU_data=="Run_F"){
fill_hist(input_dir+"Run_F.root"   ,output_dir+"hist_data_MiniAOD.root"     ,"",true,false,false,false,false,uncertainty);
fill_hist(input_dir+"Run_F.root"   ,output_dir+"hist_data_FR1F_MiniAOD.root","",true,false,false,true ,false,uncertainty);
fill_hist(input_dir+"Run_F.root"   ,output_dir+"hist_data_FR2F_MiniAOD.root","",true,false,false,false ,true,uncertainty);
}
}
*/
//fill_hist(MC_102X_Aut18+"DYToLL_mad*.root",output_dir+str_uncert+"hist_DYToLL_mad"+str_fewz+".root"   ,   "DYToLL_mad",false,true,do_fewz,false,false,uncertainty);
/*
fill_hist(input_dir+   "ZToEE_50_120.root",output_dir+str_uncert+   "hist_ZToEE_50_120"+str_fewz+".root"   ,   "ZToEE_50_120",false,true,do_fewz,false,false,uncertainty);
fill_hist(input_dir+  "ZToEE_120_200.root",output_dir+str_uncert+  "hist_ZToEE_120_200"+str_fewz+".root"   ,  "ZToEE_120_200",false,true,do_fewz,false,false,uncertainty);
fill_hist(input_dir+  "ZToEE_200_400.root",output_dir+str_uncert+  "hist_ZToEE_200_400"+str_fewz+".root"   ,  "ZToEE_200_400",false,true,do_fewz,false,false,uncertainty);
fill_hist(input_dir+  "ZToEE_400_800.root",output_dir+str_uncert+  "hist_ZToEE_400_800"+str_fewz+".root"   ,  "ZToEE_400_800",false,true,do_fewz,false,false,uncertainty);
fill_hist(input_dir+ "ZToEE_800_1400.root",output_dir+str_uncert+ "hist_ZToEE_800_1400"+str_fewz+".root"   , "ZToEE_800_1400",false,true,do_fewz,false,false,uncertainty);
fill_hist(input_dir+"ZToEE_1400_2300.root",output_dir+str_uncert+"hist_ZToEE_1400_2300"+str_fewz+".root"   ,"ZToEE_1400_2300",false,true,do_fewz,false,false,uncertainty);
fill_hist(input_dir+"ZToEE_2300_3500.root",output_dir+str_uncert+"hist_ZToEE_2300_3500"+str_fewz+".root"   ,"ZToEE_2300_3500",false,true,do_fewz,false,false,uncertainty);
fill_hist(input_dir+"ZToEE_3500_4500.root",output_dir+str_uncert+"hist_ZToEE_3500_4500"+str_fewz+".root"   ,"ZToEE_3500_4500",false,true,do_fewz,false,false,uncertainty);
fill_hist(input_dir+"ZToEE_4500_6000.root",output_dir+str_uncert+"hist_ZToEE_4500_6000"+str_fewz+".root"   ,"ZToEE_4500_6000",false,true,do_fewz,false,false,uncertainty);
fill_hist(input_dir+ "ZToEE_6000_Inf.root",output_dir+str_uncert+ "hist_ZToEE_6000_Inf"+str_fewz+".root"   , "ZToEE_6000_Inf",false,true,do_fewz,false,false,uncertainty);

fill_hist(input_dir+   "ZToEE_50_120.root",output_dir+str_uncert+   "hist_ZToEE_50_120"+str_fewz+"_1F.root",   "ZToEE_50_120",false,true,do_fewz,true,false,uncertainty);
fill_hist(input_dir+  "ZToEE_120_200.root",output_dir+str_uncert+  "hist_ZToEE_120_200"+str_fewz+"_1F.root",  "ZToEE_120_200",false,true,do_fewz,true,false,uncertainty);
fill_hist(input_dir+  "ZToEE_200_400.root",output_dir+str_uncert+  "hist_ZToEE_200_400"+str_fewz+"_1F.root",  "ZToEE_200_400",false,true,do_fewz,true,false,uncertainty);
fill_hist(input_dir+  "ZToEE_400_800.root",output_dir+str_uncert+  "hist_ZToEE_400_800"+str_fewz+"_1F.root",  "ZToEE_400_800",false,true,do_fewz,true,false,uncertainty);
fill_hist(input_dir+ "ZToEE_800_1400.root",output_dir+str_uncert+ "hist_ZToEE_800_1400"+str_fewz+"_1F.root", "ZToEE_800_1400",false,true,do_fewz,true,false,uncertainty);
fill_hist(input_dir+"ZToEE_1400_2300.root",output_dir+str_uncert+"hist_ZToEE_1400_2300"+str_fewz+"_1F.root","ZToEE_1400_2300",false,true,do_fewz,true,false,uncertainty);
fill_hist(input_dir+"ZToEE_2300_3500.root",output_dir+str_uncert+"hist_ZToEE_2300_3500"+str_fewz+"_1F.root","ZToEE_2300_3500",false,true,do_fewz,true,false,uncertainty);
fill_hist(input_dir+"ZToEE_3500_4500.root",output_dir+str_uncert+"hist_ZToEE_3500_4500"+str_fewz+"_1F.root","ZToEE_3500_4500",false,true,do_fewz,true,false,uncertainty);
fill_hist(input_dir+"ZToEE_4500_6000.root",output_dir+str_uncert+"hist_ZToEE_4500_6000"+str_fewz+"_1F.root","ZToEE_4500_6000",false,true,do_fewz,true,false,uncertainty);
fill_hist(input_dir+ "ZToEE_6000_Inf.root",output_dir+str_uncert+ "hist_ZToEE_6000_Inf"+str_fewz+"_1F.root", "ZToEE_6000_Inf",false,true,do_fewz,true,false,uncertainty);

if(uncertainty!="pdf_scale_up" && uncertainty!="pdf_scale_down"){

fill_hist(input_dir+"DYToTT_amc*.root"                            ,output_dir+str_uncert+"hist_ZToTT.root"            ,"DYJetsToLL_M_50_amc",false,false,false,false,false,uncertainty);
fill_hist(input_dir+"ST.root"                                     ,output_dir+str_uncert+"hist_ST.root"               ,"ST"                 ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"ST_anti.root"                                ,output_dir+str_uncert+"hist_ST_anti.root"          ,"ST_anti"            ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"WZTo2L2Q.root"                               ,output_dir+str_uncert+"hist_WZ_2L2Q.root"          ,"WZTo2L2Q"           ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"WZTo3LNu.root"                               ,output_dir+str_uncert+"hist_WZ_3LNu.root"          ,"WZTo3LNu"           ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"ZZTo2L2Nu.root"                              ,output_dir+str_uncert+"hist_ZZ_2L2Nu.root"         ,"ZZTo2L2Nu"          ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"ZZTo2L2Q.root"                               ,output_dir+str_uncert+"hist_ZZ_2L2Q.root"          ,"ZZTo2L2Q"           ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"ZZTo4L.root"                                 ,output_dir+str_uncert+"hist_ZZ_4L.root"            ,"ZZTo4L"             ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"WW_200.root"                                 ,output_dir+str_uncert+"hist_WW2L_200.root"         ,"WWTo2L2Nu"          ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"WW_200_600.root"                             ,output_dir+str_uncert+"hist_WW2L_200_600.root"     ,"WWTo2L2Nu_200_600"  ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"WW_600_1200.root"                            ,output_dir+str_uncert+"hist_WW2L_600_1200.root"    ,"WWTo2L2Nu_600_1200" ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"WW_1200_2500.root"                           ,output_dir+str_uncert+"hist_WW2L_1200_2500.root"   ,"WWTo2L2Nu_1200_2500",false,false,false,false,false,uncertainty);
fill_hist(input_dir+"WW_2500_Inf.root"                            ,output_dir+str_uncert+"hist_WW2L_2500_Inf.root"    ,"WWTo2L2Nu_2500_Inf" ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"TTTo2L2Nu_500.root"                          ,output_dir+str_uncert+"hist_TTbar2L_500.root"      ,"TTTo2L2Nu"          ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"TTTo2L2Nu_500_800.root"                      ,output_dir+str_uncert+"hist_TTbar2L_500_800.root"  ,"TTTo2L2Nu_500_800"  ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"TTTo2L2Nu_800_1200.root"                     ,output_dir+str_uncert+"hist_TTbar2L_800_1200.root" ,"TTTo2L2Nu_800_1200" ,false,false,false,false,false,uncertainty);
fill_hist(input_dir+"TTTo2L2Nu_1200_1800.root"                    ,output_dir+str_uncert+"hist_TTbar2L_1200_1800.root","TTTo2L2Nu_1200_1800",false,false,false,false,false,uncertainty);
fill_hist(input_dir+"TTTo2L2Nu_1800_Inf.root"                     ,output_dir+str_uncert+"hist_TTbar2L_1800_Inf.root" ,"TTTo2L2Nu_1800_Inf" ,false,false,false,false,false,uncertainty);

///////////// 1F ///////////////////////////////
fill_hist(input_dir+"DYToTT_amc*.root"                            ,output_dir+str_uncert+"hist_ZToTT_1F.root"            ,"DYJetsToLL_M_50_amc",false,false,false,true,false,uncertainty);
fill_hist(input_dir+"ST.root"                                     ,output_dir+str_uncert+"hist_ST_1F.root"               ,"ST"                 ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"ST_anti.root"                                ,output_dir+str_uncert+"hist_ST_anti_1F.root"          ,"ST_anti"            ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"WZTo2L2Q.root"                               ,output_dir+str_uncert+"hist_WZ_2L2Q_1F.root"          ,"WZTo2L2Q"           ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"WZTo3LNu.root"                               ,output_dir+str_uncert+"hist_WZ_3LNu_1F.root"          ,"WZTo3LNu"           ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"ZZTo2L2Nu.root"                              ,output_dir+str_uncert+"hist_ZZ_2L2Nu_1F.root"         ,"ZZTo2L2Nu"          ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"ZZTo2L2Q.root"                               ,output_dir+str_uncert+"hist_ZZ_2L2Q_1F.root"          ,"ZZTo2L2Q"           ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"ZZTo4L.root"                                 ,output_dir+str_uncert+"hist_ZZ_4L_1F.root"            ,"ZZTo4L"             ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"WW_200.root"                                 ,output_dir+str_uncert+"hist_WW2L_200_1F.root"         ,"WWTo2L2Nu"          ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"WW_200_600.root"                             ,output_dir+str_uncert+"hist_WW2L_200_600_1F.root"     ,"WWTo2L2Nu_200_600"  ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"WW_600_1200.root"                            ,output_dir+str_uncert+"hist_WW2L_600_1200_1F.root"    ,"WWTo2L2Nu_600_1200" ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"WW_1200_2500.root"                           ,output_dir+str_uncert+"hist_WW2L_1200_2500_1F.root"   ,"WWTo2L2Nu_1200_2500",false,false,false,true,false,uncertainty);
fill_hist(input_dir+"WW_2500_Inf.root"                            ,output_dir+str_uncert+"hist_WW2L_2500_Inf_1F.root"    ,"WWTo2L2Nu_2500_Inf" ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"TTTo2L2Nu_500.root"                          ,output_dir+str_uncert+"hist_TTbar2L_500_1F.root"      ,"TTTo2L2Nu"          ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"TTTo2L2Nu_500_800.root"                      ,output_dir+str_uncert+"hist_TTbar2L_500_800_1F.root"  ,"TTTo2L2Nu_500_800"  ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"TTTo2L2Nu_800_1200.root"                     ,output_dir+str_uncert+"hist_TTbar2L_800_1200_1F.root" ,"TTTo2L2Nu_800_1200" ,false,false,false,true,false,uncertainty);
fill_hist(input_dir+"TTTo2L2Nu_1200_1800.root"                    ,output_dir+str_uncert+"hist_TTbar2L_1200_1800_1F.root","TTTo2L2Nu_1200_1800",false,false,false,true,false,uncertainty);
fill_hist(input_dir+"TTTo2L2Nu_1800_Inf.root"                     ,output_dir+str_uncert+"hist_TTbar2L_1800_Inf_1F.root" ,"TTTo2L2Nu_1800_Inf" ,false,false,false,true,false,uncertainty);
}
*/
}//2017
else if(Year=="2016"){
//fill_hist(input_dir+"Run*.root"   ,output_dir+"hist_data_MiniAOD.root"     ,"",true,false,false,false,false,uncertainty);

if(uncertainty=="nominal"){
if(PU_data=="Run_all"){
fill_hist(input_dir+"Run*.root"   ,output_dir+"hist_data_MiniAOD.root"     ,"",true,false,false,false,false,uncertainty);
fill_hist(input_dir+"Run*.root"   ,output_dir+"hist_data_FR1F_MiniAOD.root","",true,false,false,true ,false,uncertainty);
fill_hist(input_dir+"Run*.root"   ,output_dir+"hist_data_FR2F_MiniAOD.root","",true,false,false,false ,true,uncertainty);
}
else if(PU_data=="Run_A"){
fill_hist(input_dir+"Run_A.root"   ,output_dir+"hist_data_MiniAOD.root"     ,"",true,false,false,false,false,uncertainty);
fill_hist(input_dir+"Run_A.root"   ,output_dir+"hist_data_FR1F_MiniAOD.root","",true,false,false,true ,false,uncertainty);
fill_hist(input_dir+"Run_A.root"   ,output_dir+"hist_data_FR2F_MiniAOD.root","",true,false,false,false ,true,uncertainty);
}
else if(PU_data=="Run_B"){
fill_hist(input_dir+"Run_B.root"   ,output_dir+"hist_data_MiniAOD.root"     ,"",true,false,false,false,false,uncertainty);
fill_hist(input_dir+"Run_B.root"   ,output_dir+"hist_data_FR1F_MiniAOD.root","",true,false,false,true ,false,uncertainty);
fill_hist(input_dir+"Run_B.root"   ,output_dir+"hist_data_FR2F_MiniAOD.root","",true,false,false,false ,true,uncertainty);
}
else if(PU_data=="Run_C"){
fill_hist(input_dir+"Run_C.root"   ,output_dir+"hist_data_MiniAOD.root"     ,"",true,false,false,false,false,uncertainty);
fill_hist(input_dir+"Run_C.root"   ,output_dir+"hist_data_FR1F_MiniAOD.root","",true,false,false,true ,false,uncertainty);
fill_hist(input_dir+"Run_C.root"   ,output_dir+"hist_data_FR2F_MiniAOD.root","",true,false,false,false ,true,uncertainty);
}
else if(PU_data=="Run_D"){
fill_hist(input_dir+"Run_D.root"   ,output_dir+"hist_data_MiniAOD.root"     ,"",true,false,false,false,false,uncertainty);
fill_hist(input_dir+"Run_D.root"   ,output_dir+"hist_data_FR1F_MiniAOD.root","",true,false,false,true ,false,uncertainty);
fill_hist(input_dir+"Run_D.root"   ,output_dir+"hist_data_FR2F_MiniAOD.root","",true,false,false,false ,true,uncertainty);
}
}

//fill_hist(MC_102X_Aut18+"DYToLL_mad*.root",output_dir+str_uncert+"hist_DYToLL_mad"+str_fewz+".root"   ,   "DYToLL_mad",false,true,do_fewz,false,false,uncertainty);



fill_hist(input_dir+   "ZToEE_50_120.root",output_dir+str_uncert+   "hist_ZToEE_50_120"+str_fewz+".root"   ,"",false,true,do_fewz,false,false,uncertainty);
fill_hist(input_dir+  "ZToEE_120_200.root",output_dir+str_uncert+  "hist_ZToEE_120_200"+str_fewz+".root"   ,"",false,true,do_fewz,false,false,uncertainty);
fill_hist(input_dir+  "ZToEE_200_400.root",output_dir+str_uncert+  "hist_ZToEE_200_400"+str_fewz+".root"   ,"",false,true,do_fewz,false,false,uncertainty);
fill_hist(input_dir+  "ZToEE_400_800.root",output_dir+str_uncert+  "hist_ZToEE_400_800"+str_fewz+".root"   ,"",false,true,do_fewz,false,false,uncertainty);
fill_hist(input_dir+ "ZToEE_800_1400.root",output_dir+str_uncert+ "hist_ZToEE_800_1400"+str_fewz+".root"   ,"",false,true,do_fewz,false,false,uncertainty);
fill_hist(input_dir+"ZToEE_1400_2300.root",output_dir+str_uncert+"hist_ZToEE_1400_2300"+str_fewz+".root"   ,"",false,true,do_fewz,false,false,uncertainty);
fill_hist(input_dir+"ZToEE_2300_3500.root",output_dir+str_uncert+"hist_ZToEE_2300_3500"+str_fewz+".root"   ,"",false,true,do_fewz,false,false,uncertainty);
fill_hist(input_dir+"ZToEE_3500_4500.root",output_dir+str_uncert+"hist_ZToEE_3500_4500"+str_fewz+".root"   ,"",false,true,do_fewz,false,false,uncertainty);
fill_hist(input_dir+"ZToEE_4500_6000.root",output_dir+str_uncert+"hist_ZToEE_4500_6000"+str_fewz+".root"   ,"",false,true,do_fewz,false,false,uncertainty);
fill_hist(input_dir+ "ZToEE_6000_Inf.root",output_dir+str_uncert+ "hist_ZToEE_6000_Inf"+str_fewz+".root"   ,"",false,true,do_fewz,false,false,uncertainty);

fill_hist(input_dir+   "ZToEE_50_120.root",output_dir+str_uncert+   "hist_ZToEE_50_120"+str_fewz+"_1F.root","",false,true,do_fewz,true,false,uncertainty);
fill_hist(input_dir+  "ZToEE_120_200.root",output_dir+str_uncert+  "hist_ZToEE_120_200"+str_fewz+"_1F.root","",false,true,do_fewz,true,false,uncertainty);
fill_hist(input_dir+  "ZToEE_200_400.root",output_dir+str_uncert+  "hist_ZToEE_200_400"+str_fewz+"_1F.root","",false,true,do_fewz,true,false,uncertainty);
fill_hist(input_dir+  "ZToEE_400_800.root",output_dir+str_uncert+  "hist_ZToEE_400_800"+str_fewz+"_1F.root","",false,true,do_fewz,true,false,uncertainty);
fill_hist(input_dir+ "ZToEE_800_1400.root",output_dir+str_uncert+ "hist_ZToEE_800_1400"+str_fewz+"_1F.root","",false,true,do_fewz,true,false,uncertainty);
fill_hist(input_dir+"ZToEE_1400_2300.root",output_dir+str_uncert+"hist_ZToEE_1400_2300"+str_fewz+"_1F.root","",false,true,do_fewz,true,false,uncertainty);
fill_hist(input_dir+"ZToEE_2300_3500.root",output_dir+str_uncert+"hist_ZToEE_2300_3500"+str_fewz+"_1F.root","",false,true,do_fewz,true,false,uncertainty);
fill_hist(input_dir+"ZToEE_3500_4500.root",output_dir+str_uncert+"hist_ZToEE_3500_4500"+str_fewz+"_1F.root","",false,true,do_fewz,true,false,uncertainty);
fill_hist(input_dir+"ZToEE_4500_6000.root",output_dir+str_uncert+"hist_ZToEE_4500_6000"+str_fewz+"_1F.root","",false,true,do_fewz,true,false,uncertainty);
fill_hist(input_dir+ "ZToEE_6000_Inf.root",output_dir+str_uncert+ "hist_ZToEE_6000_Inf"+str_fewz+"_1F.root","",false,true,do_fewz,true,false,uncertainty);


if(uncertainty!="pdf_scale_up" && uncertainty!="pdf_scale_down"){

fill_hist(input_dir+"DYToTT_amc.root"                             ,output_dir+str_uncert+"hist_ZToTT.root"            ,"",false,false,false,false,false,uncertainty);
fill_hist(input_dir+"ST.root"                                     ,output_dir+str_uncert+"hist_ST.root"               ,"",false,false,false,false,false,uncertainty);
fill_hist(input_dir+"ST_anti.root"                                ,output_dir+str_uncert+"hist_ST_anti.root"          ,"",false,false,false,false,false,uncertainty);
fill_hist(input_dir+"WZTo2L2Q.root"                               ,output_dir+str_uncert+"hist_WZ_2L2Q.root"          ,"",false,false,false,false,false,uncertainty);
fill_hist(input_dir+"WZTo3LNu.root"                               ,output_dir+str_uncert+"hist_WZ_3LNu.root"          ,"",false,false,false,false,false,uncertainty);
fill_hist(input_dir+"ZZTo2L2Nu.root"                              ,output_dir+str_uncert+"hist_ZZ_2L2Nu.root"         ,"",false,false,false,false,false,uncertainty);
fill_hist(input_dir+"ZZTo2L2Q.root"                               ,output_dir+str_uncert+"hist_ZZ_2L2Q.root"          ,"",false,false,false,false,false,uncertainty);
fill_hist(input_dir+"ZZTo4L.root"                                 ,output_dir+str_uncert+"hist_ZZ_4L.root"            ,"",false,false,false,false,false,uncertainty);
fill_hist(input_dir+"WW2L2Nu_200.root"                            ,output_dir+str_uncert+"hist_WW2L_200.root"         ,"",false,false,false,false,false,uncertainty);
fill_hist(input_dir+"WW2L2Nu_200_600.root"                        ,output_dir+str_uncert+"hist_WW2L_200_600.root"     ,"",false,false,false,false,false,uncertainty);
fill_hist(input_dir+"WW2L2Nu_600_1200.root"                       ,output_dir+str_uncert+"hist_WW2L_600_1200.root"    ,"",false,false,false,false,false,uncertainty);
fill_hist(input_dir+"WW2L2Nu_1200_2500.root"                      ,output_dir+str_uncert+"hist_WW2L_1200_2500.root"   ,"",false,false,false,false,false,uncertainty);
fill_hist(input_dir+"WW2L2Nu_2500_Inf.root"                       ,output_dir+str_uncert+"hist_WW2L_2500_Inf.root"    ,"",false,false,false,false,false,uncertainty);
fill_hist(input_dir+"TTTo2L2Nu_500.root"                          ,output_dir+str_uncert+"hist_TTbar2L_500.root"      ,"",false,false,false,false,false,uncertainty);
fill_hist(input_dir+"TTTo2L2Nu_500_800.root"                      ,output_dir+str_uncert+"hist_TTbar2L_500_800.root"  ,"",false,false,false,false,false,uncertainty);
fill_hist(input_dir+"TTTo2L2Nu_800_1200.root"                     ,output_dir+str_uncert+"hist_TTbar2L_800_1200.root" ,"",false,false,false,false,false,uncertainty);
fill_hist(input_dir+"TTTo2L2Nu_1200_1800.root"                    ,output_dir+str_uncert+"hist_TTbar2L_1200_1800.root","",false,false,false,false,false,uncertainty);
fill_hist(input_dir+"TTTo2L2Nu_1800_Inf.root"                     ,output_dir+str_uncert+"hist_TTbar2L_1800_Inf.root" ,"",false,false,false,false,false,uncertainty);

///////////// 1F ///////////////////////////////

fill_hist(input_dir+"DYToTT_amc.root"                             ,output_dir+str_uncert+"hist_ZToTT_1F.root"            ,"",false,false,false,true,false,uncertainty);
fill_hist(input_dir+"ST.root"                                     ,output_dir+str_uncert+"hist_ST_1F.root"               ,"",false,false,false,true,false,uncertainty);
fill_hist(input_dir+"ST_anti.root"                                ,output_dir+str_uncert+"hist_ST_anti_1F.root"          ,"",false,false,false,true,false,uncertainty);
fill_hist(input_dir+"WZTo2L2Q.root"                               ,output_dir+str_uncert+"hist_WZ_2L2Q_1F.root"          ,"",false,false,false,true,false,uncertainty);
fill_hist(input_dir+"WZTo3LNu.root"                               ,output_dir+str_uncert+"hist_WZ_3LNu_1F.root"          ,"",false,false,false,true,false,uncertainty);
fill_hist(input_dir+"ZZTo2L2Nu.root"                              ,output_dir+str_uncert+"hist_ZZ_2L2Nu_1F.root"         ,"",false,false,false,true,false,uncertainty);
fill_hist(input_dir+"ZZTo2L2Q.root"                               ,output_dir+str_uncert+"hist_ZZ_2L2Q_1F.root"          ,"",false,false,false,true,false,uncertainty);
fill_hist(input_dir+"ZZTo4L.root"                                 ,output_dir+str_uncert+"hist_ZZ_4L_1F.root"            ,"",false,false,false,true,false,uncertainty);
fill_hist(input_dir+"WW2L2Nu_200.root"                            ,output_dir+str_uncert+"hist_WW2L_200_1F.root"         ,"",false,false,false,true,false,uncertainty);
fill_hist(input_dir+"WW2L2Nu_200_600.root"                        ,output_dir+str_uncert+"hist_WW2L_200_600_1F.root"     ,"",false,false,false,true,false,uncertainty);
fill_hist(input_dir+"WW2L2Nu_600_1200.root"                       ,output_dir+str_uncert+"hist_WW2L_600_1200_1F.root"    ,"",false,false,false,true,false,uncertainty);
fill_hist(input_dir+"WW2L2Nu_1200_2500.root"                      ,output_dir+str_uncert+"hist_WW2L_1200_2500_1F.root"   ,"",false,false,false,true,false,uncertainty);
fill_hist(input_dir+"WW2L2Nu_2500_Inf.root"                       ,output_dir+str_uncert+"hist_WW2L_2500_Inf_1F.root"    ,"",false,false,false,true,false,uncertainty);
fill_hist(input_dir+"TTTo2L2Nu_500.root"                          ,output_dir+str_uncert+"hist_TTbar2L_500_1F.root"      ,"",false,false,false,true,false,uncertainty);
fill_hist(input_dir+"TTTo2L2Nu_500_800.root"                      ,output_dir+str_uncert+"hist_TTbar2L_500_800_1F.root"  ,"",false,false,false,true,false,uncertainty);
fill_hist(input_dir+"TTTo2L2Nu_800_1200.root"                     ,output_dir+str_uncert+"hist_TTbar2L_800_1200_1F.root" ,"",false,false,false,true,false,uncertainty);
fill_hist(input_dir+"TTTo2L2Nu_1200_1800.root"                    ,output_dir+str_uncert+"hist_TTbar2L_1200_1800_1F.root","",false,false,false,true,false,uncertainty);
fill_hist(input_dir+"TTTo2L2Nu_1800_Inf.root"                     ,output_dir+str_uncert+"hist_TTbar2L_1800_Inf_1F.root" ,"",false,false,false,true,false,uncertainty);
}

}//2016
}
}

void fill_hist(TString input_file, TString output_file, TString pu_name, bool is_data, bool is_ZToEE, bool do_fewz, bool do_FR_1F, bool do_FR_2F, TString uncert){

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
   int L1_pass_final    =0; 

   vector<float> *trig_DEle33_unseed_eta   =0; 
   vector<float> *trig_DEle33_unseed_phi   =0; 
   vector<float> *trig_DEle33_MW_unseed_eta=0; 
   vector<float> *trig_DEle33_MW_unseed_phi=0; 
   vector<float> *trig_DEle33_MW_L1_eta    =0; 
   vector<float> *trig_DEle33_MW_L1_phi    =0; 
   vector<float> *trig_DEle33_MW_L1_et     =0; 

   vector<float> *heeps_E           =0; 
   vector<float> *heeps_et          =0; 
   vector<float> *heeps_sc_et       =0; 
   vector<float> *heeps_sc_et_corr  =0; 
   vector<float> *heeps_eta         =0; 
   vector<float> *heeps_sc_eta      =0; 
   vector<float> *heeps_phi         =0; 
   vector<float> *heeps_sc_phi      =0; 
   vector<int>   *heeps_charge      =0; 
   vector<int>   *heeps_isHEEP7     =0; 
   vector<int>   *heeps_PreSelection=0; 
   vector<int>   *heeps_match       =0; 
   vector<int>   *heeps_saturated   =0; 
   vector<int>   *heeps_VIDHEEP7    =0; 
   vector<float> *heeps_dPhiIn         =0;
   vector<float> *heeps_Sieie          =0;
   vector<float> *heeps_missingHits    =0;
   vector<float> *heeps_dxyFirstPV     =0;
   vector<float> *heeps_HOverE         =0;
   vector<float> *heeps_E1x5OverE5x5   =0;
   vector<float> *heeps_E2x5OverE5x5   =0;
   vector<float> *heeps_isolEMHadDepth1=0;
   vector<float> *heeps_IsolPtTrks     =0;
   vector<float> *heeps_EcalDriven     =0;
   vector<float> *heeps_dEtaIn         =0;


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
   float Gen_Z_mass       = 0 ;
   float Gen_Led_Et       = 0 ;
   float Gen_Sub_Et       = 0 ;
   float w_PU_combined    = 0 ;
   float w_PU_silver_down = 0 ; 
   float w_PU_silver_up   = 0 ;

   ULong_t ev_run=0;
   ULong_t ev_event=0;
   ULong_t ev_luminosityBlock=0;
   float prefiringweight     = 0 ;
   float prefiringweightup   = 0 ;
   float prefiringweightdown = 0 ;
 
   t->SetBranchAddress("ev_run"                     , &ev_run                ) ;
   t->SetBranchAddress("ev_event"                   , &ev_event              ) ;
   t->SetBranchAddress("ev_luminosityBlock"         , &ev_luminosityBlock    ) ;
   if(Year=="2016"){
   t->SetBranchAddress("ev_prefiringweight"         , &prefiringweight       ) ;
   t->SetBranchAddress("ev_prefiringweightup"       , &prefiringweightup     ) ;
   t->SetBranchAddress("ev_prefiringweightdown"     , &prefiringweightdown   ) ;
   }
   else if (Year=="2017"){
   t->SetBranchAddress("prefiringweight"            , &prefiringweight       ) ;
   t->SetBranchAddress("prefiringweightup"          , &prefiringweightup     ) ;
   t->SetBranchAddress("prefiringweightdown"        , &prefiringweightdown   ) ;
   }
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
   t->SetBranchAddress("trig_DEle33_unseed_eta"    , &trig_DEle33_unseed_eta        ) ;
   t->SetBranchAddress("trig_DEle33_unseed_phi"    , &trig_DEle33_unseed_phi        ) ;
   if(use_DoubleEle25){
   t->SetBranchAddress("trig_DEle25_MW"            , &trig_DEle33_MW                ) ;
   if(match_to_seed_led){
   t->SetBranchAddress("trig_DEle25_MW_seed_eta" , &trig_DEle33_MW_unseed_eta     ) ;
   t->SetBranchAddress("trig_DEle25_MW_seed_phi" , &trig_DEle33_MW_unseed_phi     ) ;
   }
   else{
   t->SetBranchAddress("trig_DEle25_MW_unseed_eta" , &trig_DEle33_MW_unseed_eta     ) ;
   t->SetBranchAddress("trig_DEle25_MW_unseed_phi" , &trig_DEle33_MW_unseed_phi     ) ;
   }
   t->SetBranchAddress("trig_DEle25_MW_L1_eta"     , &trig_DEle33_MW_L1_eta         ) ;
   t->SetBranchAddress("trig_DEle25_MW_L1_phi"     , &trig_DEle33_MW_L1_phi         ) ;
   t->SetBranchAddress("trig_DEle25_MW_L1_et"      , &trig_DEle33_MW_L1_et          ) ;
   }////
   else{
   t->SetBranchAddress("trig_DEle33_MW"            , &trig_DEle33_MW                ) ;
   if(match_to_seed_led){
   t->SetBranchAddress("trig_DEle33_MW_seed_eta" , &trig_DEle33_MW_unseed_eta     ) ;
   t->SetBranchAddress("trig_DEle33_MW_seed_phi" , &trig_DEle33_MW_unseed_phi     ) ;
   }
   else{
   t->SetBranchAddress("trig_DEle33_MW_unseed_eta" , &trig_DEle33_MW_unseed_eta     ) ;
   t->SetBranchAddress("trig_DEle33_MW_unseed_phi" , &trig_DEle33_MW_unseed_phi     ) ;
   }
   t->SetBranchAddress("trig_DEle33_MW_L1_eta"     , &trig_DEle33_MW_L1_eta         ) ;
   t->SetBranchAddress("trig_DEle33_MW_L1_phi"     , &trig_DEle33_MW_L1_phi         ) ;
   t->SetBranchAddress("trig_DEle33_MW_L1_et"      , &trig_DEle33_MW_L1_et          ) ;
   }
   t->SetBranchAddress("L1_pass_final"             , &L1_pass_final         ) ;
//////////////////////////////////////
   t->SetBranchAddress("heeps_E"                           , &heeps_E              ) ;
   t->SetBranchAddress("heeps_et"                          , &heeps_et             ) ;
   t->SetBranchAddress("heeps_sc_et"                       , &heeps_sc_et          ) ;
   t->SetBranchAddress("heeps_sc_et_corr"                  , &heeps_sc_et_corr     ) ;
   t->SetBranchAddress("heeps_eta"                         , &heeps_eta            ) ;
   t->SetBranchAddress("heeps_sc_eta"                      , &heeps_sc_eta         ) ;
   t->SetBranchAddress("heeps_phi"                         , &heeps_phi            ) ;
   t->SetBranchAddress("heeps_sc_phi"                      , &heeps_sc_phi         ) ;
   t->SetBranchAddress("heeps_charge"                      , &heeps_charge         ) ;
   t->SetBranchAddress("heeps_PreSelection"                , &heeps_PreSelection   ) ;
   t->SetBranchAddress("heeps_match"                       , &heeps_match          ) ;
   t->SetBranchAddress("heeps_saturated"                   , &heeps_saturated      ) ;
   t->SetBranchAddress("heeps_VIDHEEP7"                    , &heeps_VIDHEEP7       ) ;
   t->SetBranchAddress("heeps_isHEEP7"                     , &heeps_isHEEP7        ) ;
   t->SetBranchAddress("heeps_dPhiIn"                      , &heeps_dPhiIn         ) ;
   t->SetBranchAddress("heeps_Sieie"                       , &heeps_Sieie          ) ;
   t->SetBranchAddress("heeps_missingHits"                 , &heeps_missingHits    ) ;
   t->SetBranchAddress("heeps_dxyFirstPV"                  , &heeps_dxyFirstPV     ) ;
   t->SetBranchAddress("heeps_HOverE"                      , &heeps_HOverE         ) ;
   t->SetBranchAddress("heeps_E1x5OverE5x5"                , &heeps_E1x5OverE5x5   ) ;
   t->SetBranchAddress("heeps_E2x5OverE5x5"                , &heeps_E2x5OverE5x5   ) ;
   t->SetBranchAddress("heeps_isolEMHadDepth1"             , &heeps_isolEMHadDepth1) ;
   t->SetBranchAddress("heeps_IsolPtTrks"                  , &heeps_IsolPtTrks     ) ;
   t->SetBranchAddress("heeps_EcalDriven"                  , &heeps_EcalDriven     ) ;
   t->SetBranchAddress("heeps_dEtaIn"                      , &heeps_dEtaIn         ) ;

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
   t->SetBranchAddress("Gen_Z_mass"      , &Gen_Z_mass        ) ;
   t->SetBranchAddress("Gen_Led_Et"      , &Gen_Led_Et        ) ;
   t->SetBranchAddress("Gen_Sub_Et"      , &Gen_Sub_Et        ) ;


///

const int N_mee_bin=120;
float mee_bin_edge[N_mee_bin];
int index=0;
for(int i=50;i<120;i+=5)    {mee_bin_edge[index]=i;index++;}//14
for(int i=120;i<150;i+=5)   {mee_bin_edge[index]=i;index++;}//6
for(int i=150;i<200;i+=10)  {mee_bin_edge[index]=i;index++;}//5
for(int i=200;i<600;i+=20)  {mee_bin_edge[index]=i;index++;}//20
for(int i=600;i<900;i+=30)  {mee_bin_edge[index]=i;index++;}//10
for(int i=900;i<1250;i+=50) {mee_bin_edge[index]=i;index++;}//7
for(int i=1250;i<1610;i+=60){mee_bin_edge[index]=i;index++;}//6
for(int i=1610;i<1890;i+=70){mee_bin_edge[index]=i;index++;}//4   
for(int i=1890;i<3970;i+=80){mee_bin_edge[index]=i;index++;}//26
for(int i=3970;i<6070;i+=100){mee_bin_edge[index]=i;index++;}//21
mee_bin_edge[index]=6070;//1

///

const int N_mee_bin_sin=76;
float mee_bin_edge_sin[N_mee_bin_sin];
int index_sin=0;
for(int i=200;i<600;i+=20)  {mee_bin_edge_sin[index_sin]=i;index_sin++;}//20
for(int i=600;i<900;i+=30)  {mee_bin_edge_sin[index_sin]=i;index_sin++;}//10
for(int i=900;i<1250;i+=50) {mee_bin_edge_sin[index_sin]=i;index_sin++;}//7
for(int i=1250;i<1600;i+=60){mee_bin_edge_sin[index_sin]=i;index_sin++;}//6
for(int i=1600;i<1900;i+=70){mee_bin_edge_sin[index_sin]=i;index_sin++;}//5   
for(int i=1900;i<4000;i+=80){mee_bin_edge_sin[index_sin]=i;index_sin++;}//27
                             mee_bin_edge_sin[index_sin]=4000;//1
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
TH1D *h_mee_all_SS         =new TH1D("h_mee_all_SS",""   ,17,mee_ss_bin);
TH1D *h_mee_all_BB_SS      =new TH1D("h_mee_all_BB_SS","",17,mee_ss_bin);
TH1D *h_mee_all_BE_SS      =new TH1D("h_mee_all_BE_SS","",17,mee_ss_bin);
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
TH1D *h_mee_fine           =new TH1D("h_mee_fine",""    ,6000,0,6000);
TH1D *h_mee_BB_fine        =new TH1D("h_mee_BB_fine","" ,6000,0,6000);
TH1D *h_mee_BE_fine        =new TH1D("h_mee_BE_fine","" ,6000,0,6000);
TH1D *h_mee_EE_fine        =new TH1D("h_mee_EE_fine","" ,6000,0,6000);
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
TH1D *h_mee_usual          =new TH1D("h_mee_usual"   ,"" ,600,0,6000);
TH1D *h_mee_BB_usual       =new TH1D("h_mee_BB_usual","" ,600,0,6000);
TH1D *h_mee_BE_usual       =new TH1D("h_mee_BE_usual","" ,600,0,6000);
TH1D *h_mee_EE_usual       =new TH1D("h_mee_EE_usual","" ,600,0,6000);
TH1D *h_mee_Zpeak          =new TH1D("h_mee_Zpeak"   ,"",60,60,120);
TH1D *h_mee_Zpeak_BB       =new TH1D("h_mee_Zpeak_BB","",60,60,120);
TH1D *h_mee_Zpeak_BE       =new TH1D("h_mee_Zpeak_BE","",60,60,120);
TH1D *h_mee_Zpeak_EE       =new TH1D("h_mee_Zpeak_EE","",60,60,120);
TH1D *h_mee_Zpeak_EE_pp    =new TH1D("h_mee_Zpeak_EE_pp","",60,60,120);
TH1D *h_mee_Zpeak_EE_pm    =new TH1D("h_mee_Zpeak_EE_pm","",60,60,120);
TH1D *h_mee_Zpeak_EE_mm    =new TH1D("h_mee_Zpeak_EE_mm","",60,60,120);
TH1D *h_mee_Zpeak_EE_Heta  =new TH1D("h_mee_Zpeak_EE_Heta","",60,60,120);
TH1D *h_mee_Zpeak_EE_Leta  =new TH1D("h_mee_Zpeak_EE_Leta","",60,60,120);
TH1D *h_mee_Zpeak_EE_HLeta =new TH1D("h_mee_Zpeak_EE_HLeta","",60,60,120);
TH1D *h_mee_Zpeak_v1       =new TH1D("h_mee_Zpeak_v1"   ,"",120,60,120);
TH1D *h_mee_Zpeak_BB_v1    =new TH1D("h_mee_Zpeak_BB_v1","",120,60,120);
TH1D *h_mee_Zpeak_BE_v1    =new TH1D("h_mee_Zpeak_BE_v1","",120,60,120);
TH1D *h_mee_Zpeak_EE_v1    =new TH1D("h_mee_Zpeak_EE_v1","",120,60,120);

TH1D *h_mee_fail_MET       =new TH1D("h_mee_fail_MET","",197,60,4000);

TH1D *h_pv_n               =new TH1D("h_pv_n","",100,0,100);
TH1D *h_rho                =new TH1D("h_rho" ,"",80,0,40);
TH1D *h_rho_BB             =new TH1D("h_rho_BB" ,"",80,0,40);
TH1D *h_rho_BE             =new TH1D("h_rho_BE" ,"",80,0,40);
TH1D *h_rho_EE             =new TH1D("h_rho_EE" ,"",80,0,40);
TH1D *h_Ptll               =new TH1D("h_Ptll" ,"",75 ,0,150);
TH1D *h_Etall              =new TH1D("h_Etall","",100,-5,5 );
TH1D *h_Phill              =new TH1D("h_Phill" ,"",80 ,-4,4);
TH1D *h_led_Et             =new TH1D("h_led_Et","",60,35,635);
TH1D *h_led_eta            =new TH1D("h_led_eta","",60,-3,3);
TH1D *h_led_phi            =new TH1D("h_led_phi","",100,-5,5);
TH1D *h_sub_Et             =new TH1D("h_sub_Et","",60,35,635);
TH1D *h_sub_eta            =new TH1D("h_sub_eta","",60,-3,3);
TH1D *h_sub_phi            =new TH1D("h_sub_phi","",100,-5,5);
TH1D *h_led_Et_v1          =new TH1D("h_led_Et_v1","",50,35,1535);
TH1D *h_led_eta_v1         =new TH1D("h_led_eta_v1","",30,-3,3);
TH1D *h_led_phi_v1         =new TH1D("h_led_phi_v1","",50,-5,5);
TH1D *h_sub_Et_v1          =new TH1D("h_sub_Et_v1","",50,35,1535);
TH1D *h_sub_eta_v1         =new TH1D("h_sub_eta_v1","",30,-3,3);
TH1D *h_sub_phi_v1         =new TH1D("h_sub_phi_v1","",50,-5,5);
TH1D *h_led_Et_AM          =new TH1D("h_led_Et_AM","",60,35,635);
TH1D *h_led_eta_AM         =new TH1D("h_led_eta_AM","",60,-3,3);
TH1D *h_led_phi_AM         =new TH1D("h_led_phi_AM","",100,-5,5);
TH1D *h_sub_Et_AM          =new TH1D("h_sub_Et_AM","",60,35,635);
TH1D *h_sub_eta_AM         =new TH1D("h_sub_eta_AM","",60,-3,3);
TH1D *h_sub_phi_AM         =new TH1D("h_sub_phi_AM","",100,-5,5);
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

TH1D *h_dPhiIn             =new TH1D("h_dPhiIn"         ,"",40,0,0.08 );
TH1D *h_Sieie              =new TH1D("h_Sieie"          ,"",30,0,0.03 );
TH1D *h_missingHits        =new TH1D("h_missingHits"    ,"",6 ,0,3    );
TH1D *h_dxyFirstPV         =new TH1D("h_dxyFirstPV"     ,"",10,0,0.05 );
TH1D *h_HOverE             =new TH1D("h_HOverE"         ,"",20,0,0.2  );
TH1D *h_E1x5OverE5x5       =new TH1D("h_E1x5OverE5x5"   ,"",100,0,1   );
TH1D *h_E2x5OverE5x5       =new TH1D("h_E2x5OverE5x5"   ,"",100,0,1   );
TH1D *h_isolEMHadDepth1    =new TH1D("h_isolEMHadDepth1","",100,0,10  );
TH1D *h_IsolPtTrks         =new TH1D("h_IsolPtTrks"     ,"",60,0,6    );
TH1D *h_EcalDriven         =new TH1D("h_EcalDriven"     ,"",4,0,2     );
TH1D *h_dEtaIn             =new TH1D("h_dEtaIn"         ,"",70,0,0.007);


TH1D *h_L1Et          =new TH1D("h_L1Et"   ,"" ,20,0,100);
TH1D *h_L1Et_BB       =new TH1D("h_L1Et_BB","" ,20,0,100);
TH1D *h_L1Et_BE       =new TH1D("h_L1Et_BE","" ,20,0,100);


TH2D *h_led_Et_Mee_BB      =new TH2D("h_led_Et_Mee_BB"     ,"",3000,0,3000,60,60,120);//for energy scale check
TH2D *h_led_E_Mee_BB       =new TH2D("h_led_E_Mee_BB"      ,"",3000,0,3000,60,60,120);//for energy scale check
TH2D *h_endcap_Et_Mee_BE   =new TH2D("h_endcap_Et_Mee_BE"  ,"",3000,0,3000,60,60,120);//for energy scale check
TH2D *h_endcap_E_Mee_BE    =new TH2D("h_endcap_E_Mee_BE"   ,"",3000,0,3000,60,60,120);//for energy scale check
TH2D *h_endcap_eta_Mee_BE  =new TH2D("h_endcap_eta_Mee_BE" ,"",600,-3,3   ,60,60,120);//for  energy scale vs eta check
TH2D *h_float_eta_Mee_BB   =new TH2D("h_float_eta_Mee_BB"  ,"",600,-3,3   ,60,60,120);//for  energy scale vs eta check
TH2D *h_limit_eta_Mee_BB   =new TH2D("h_limit_eta_Mee_BB"  ,"",600,-3,3   ,60,60,120);//for  energy scale vs eta check
TH2D *h_led_Et_Mee_EE      =new TH2D("h_led_Et_Mee_EE"     ,"",3000,0,3000,60,60,120);//for energy scale check
TH2D *h_led_E_Mee_EE       =new TH2D("h_led_E_Mee_EE"      ,"",3000,0,3000,60,60,120);//for energy scale check




TH1D *h_resolution         =new TH1D("h_resolution"    ,"",600  ,-1,2);// for energy scale and resolution check vs mass
TH1D *h_resolution_BB      =new TH1D("h_resolution_BB" ,"",600  ,-1,2);// for energy scale and resolution check vs mass
TH1D *h_resolution_BE      =new TH1D("h_resolution_BE" ,"",600  ,-1,2);// for energy scale and resolution check vs mass
//############ gsf reco sf ################
//TFile *f_Ele_Reco_Map_BCDEF = new TFile("/user/wenxing/ST_TW_channel/CMSSW_9_4_0/src/Zprime/scripts/gsf_reco_SF/egammaEffi.txt_EGM2D_runBCDEF_passingRECO.root");
//TH2F  *sf_Ele_Reco_Map_BCDEF= (TH2F*)f_Ele_Reco_Map_BCDEF->Get("EGamma_SF2D");
//TFile *f_Ele_Reco_Map_B     = new TFile("/user/wenxing/ST_TW_channel/CMSSW_9_4_0/src/Zprime/scripts/gsf_reco_SF/egammaEffi.txt_EGM2D_runB_passingRECO.root");
//TH2F  *sf_Ele_Reco_Map_B    = (TH2F*)f_Ele_Reco_Map_B    ->Get("EGamma_SF2D");
//TFile *f_Ele_Reco_Map_C     = new TFile("/user/wenxing/ST_TW_channel/CMSSW_9_4_0/src/Zprime/scripts/gsf_reco_SF/egammaEffi.txt_EGM2D_runC_passingRECO.root");
//TH2F  *sf_Ele_Reco_Map_C    = (TH2F*)f_Ele_Reco_Map_C    ->Get("EGamma_SF2D");
//TFile *f_Ele_Reco_Map_D     = new TFile("/user/wenxing/ST_TW_channel/CMSSW_9_4_0/src/Zprime/scripts/gsf_reco_SF/egammaEffi.txt_EGM2D_runD_passingRECO.root");
//TH2F  *sf_Ele_Reco_Map_D    = (TH2F*)f_Ele_Reco_Map_D    ->Get("EGamma_SF2D");
//TFile *f_Ele_Reco_Map_E     = new TFile("/user/wenxing/ST_TW_channel/CMSSW_9_4_0/src/Zprime/scripts/gsf_reco_SF/egammaEffi.txt_EGM2D_runE_passingRECO.root");
//TH2F  *sf_Ele_Reco_Map_E    = (TH2F*)f_Ele_Reco_Map_E    ->Get("EGamma_SF2D");
//TFile *f_Ele_Reco_Map_F     = new TFile("/user/wenxing/ST_TW_channel/CMSSW_9_4_0/src/Zprime/scripts/gsf_reco_SF/egammaEffi.txt_EGM2D_runF_passingRECO.root");
//TH2F  *sf_Ele_Reco_Map_F    = (TH2F*)f_Ele_Reco_Map_F    ->Get("EGamma_SF2D");
//############### NNPDF ratio histogram for ttbar###########################
TFile *f_NNPDF = new TFile("/user/wenxing/ST_TW_channel/CMSSW_10_2_13/src/Zprime/xgao_ttbar_ratio.root","read");
TH1D  *h_tt_BB = (TH1D*)f_NNPDF->Get("gen_M_emu_BB_log");
TH1D  *h_tt_BE = (TH1D*)f_NNPDF->Get("gen_M_emu_BE_log");
TH1D  *h_tt_EE = (TH1D*)f_NNPDF->Get("gen_M_emu_EE_log");
TAxis *tt_BB_axis = h_tt_BB->GetXaxis();
TAxis *tt_BE_axis = h_tt_BE->GetXaxis();
TAxis *tt_EE_axis = h_tt_EE->GetXaxis();
float tt_BB_axis_min = tt_BB_axis->GetXmin();
float tt_BB_axis_max = tt_BB_axis->GetXmax();
float tt_BE_axis_min = tt_BE_axis->GetXmin();
float tt_BE_axis_max = tt_BE_axis->GetXmax();
float tt_EE_axis_min = tt_EE_axis->GetXmin();
float tt_EE_axis_max = tt_EE_axis->GetXmax();
int do_tt_reweight=false;
if(pu_name.Contains("TTTo2L2Nu") && (Year=="2017" || Year=="2018") ){do_tt_reweight=true;std::cout<<"do tt reweight"<<std::endl;}

TH2D *h_pass_L1_BB           =new TH2D("h_pass_L1_BB"    ,"", 60,60,120,4,0,2);// for L1 check
TH2D *h_pass_L1_BE           =new TH2D("h_pass_L1_BE"    ,"", 60,60,120,4,0,2);// for L1 check
TH2D *h_pass_L1_EE           =new TH2D("h_pass_L1_EE"    ,"", 60,60,120,4,0,2);// for L1 check
TH1D *h_diff_et_barrel       =new TH1D("h_diff_et_barrel"    ,"",300  ,-1,2);// sc-et/et
TH1D *h_diff_et_endcap       =new TH1D("h_diff_et_endcap"    ,"",300  ,-1,2);// sc-et/et
TH1D *h_N_saturated_BB       =new TH1D("h_N_saturated_BB"    ,"",6  ,0,3);// saturated check
TH1D *h_N_saturated_BE       =new TH1D("h_N_saturated_BE"    ,"",6  ,0,3);// saturated check


bool MET_detail=false;//check the MET
bool do_match  =true;//check match, be nominal

double event_weight=1;
float  fake_rate=1;
bool do_PU_weight=true; 
double fewz_weight=1;
bool do_fewz_weight=false;
if(is_ZToEE && do_fewz) do_fewz_weight=true;
if(is_data==true){
                  do_PU_weight=false;
                  do_fewz_weight=false;
                 }

map<int,int> ele_indexs;
//const int trig_Calo_trID_run_low=9999999;
//const int trig_Calo_trID_run_up =0;
const int trig_Calo_trID_run_low=276454;
const int trig_Calo_trID_run_up =278822;

TString event_out="event_list_"+Year;
TString add_out="Add_info_"+Year;
if(is_data) {event_out=event_out+"_data";add_out=add_out+"_data";}
if(do_FR_1F){event_out=event_out+"_1F"  ;add_out=add_out+"_1F";  }
if(do_FR_2F){event_out=event_out+"_2F"  ;add_out=add_out+"_2F";  }
add_out  =add_out  +".txt"; 
event_out=event_out+".txt"; 
ofstream fout(event_out);
ofstream f_add_out(add_out);
ofstream fout_MET("Wx_data_MET.txt");
ofstream fout_match("ZtoEE_match_v1.txt");
long long N_total=t->GetEntries();
std::cout<<"total event="<<N_total<<std::endl;
//for(int i=0;i<100;i++){
for(long long i=0;i<t->GetEntries();i++){
if(i%1000000==0)std::cout<<"processed:"<<100*i/N_total<<"%"<<",event:"<<i<<std::endl;
t->GetEntry(i);
//if(ev_event!=499191292)continue;
int Region=-1;
ele_indexs.clear();
int is_pass_L1=0;
//////////////////////// MET Filter //////////
int MET_Filter=0;//temp
//int MET_Filter=(trig_Flag_HBHENoiseFilter==0 || trig_Flag_HBHENoiseIsoFilter==0 || trig_Flag_globalTightHalo2016Filter==0 || trig_Flag_goodVertices==0 || trig_Flag_EcalDeadCellTriggerPrimitiveFilter==0 || trig_Flag_BadChargedCandidateFilter==0 || trig_Flag_BadPFMuonFilter==0 || (is_data && trig_Flag_eeBadScFilter==0)) ? 0 : 1 ;
////////////////////////////////////////////////////// 1F ////////////////////////////
if(do_FR_1F==true){
for(unsigned int j=0;j<heeps_et->size();j++){
int e1_pass_trigger=0;
if(is_data){ if(ev_run>=trig_Calo_trID_run_low && ev_run<=trig_Calo_trID_run_up) e1_pass_trigger=trigger_match(heeps_sc_eta->at(j),heeps_sc_phi->at(j),trig_DEle33_unseed_eta,trig_DEle33_unseed_phi,trig_DEle33);
             else e1_pass_trigger=trigger_match(heeps_sc_eta->at(j),heeps_sc_phi->at(j),trig_DEle33_MW_unseed_eta,trig_DEle33_MW_unseed_phi,trig_DEle33_MW);
           }
else{
if     (Year=="2016")e1_pass_trigger=trigEle_2016::passTrig(heeps_et->at(j), heeps_sc_eta->at(j)) ;
else if(Year=="2017")e1_pass_trigger=trigEle_2017::passTrig(heeps_et->at(j), heeps_sc_eta->at(j)) ;
else if(Year=="2018")e1_pass_trigger=trigEle_2018::passTrig(heeps_et->at(j), heeps_sc_eta->at(j), PU_data, use_DoubleEle25) ;

    }
if(e1_pass_trigger==0 || heeps_isHEEP7->at(j)==0 || (fabs(heeps_sc_eta->at(j))>1.4442 && fabs(heeps_sc_eta->at(j))<1.566) || fabs(heeps_sc_eta->at(j))>2.5) continue;
for(unsigned int k=0;k<heeps_et->size();k++){
int e2_pass_trigger=0;
if(is_data){ if(ev_run>=trig_Calo_trID_run_low && ev_run<=trig_Calo_trID_run_up) e2_pass_trigger=trigger_match(heeps_sc_eta->at(k),heeps_sc_phi->at(k),trig_DEle33_unseed_eta,trig_DEle33_unseed_phi,trig_DEle33);
             else e2_pass_trigger=trigger_match(heeps_sc_eta->at(k),heeps_sc_phi->at(k),trig_DEle33_MW_unseed_eta,trig_DEle33_MW_unseed_phi,trig_DEle33_MW);
           }
else{
if     (Year=="2016")e2_pass_trigger=trigEle_2016::passTrig(heeps_et->at(k), heeps_sc_eta->at(k)) ;
else if(Year=="2017")e2_pass_trigger=trigEle_2017::passTrig(heeps_et->at(k), heeps_sc_eta->at(k)) ;
else if(Year=="2018")e2_pass_trigger=trigEle_2018::passTrig(heeps_et->at(k), heeps_sc_eta->at(k), PU_data, use_DoubleEle25) ;
    }
if(e2_pass_trigger==0 || heeps_PreSelection->at(k)==0 || heeps_isHEEP7->at(k)==1 || (fabs(heeps_sc_eta->at(k))>1.4442 && fabs(heeps_sc_eta->at(k))<1.566) || fabs(heeps_sc_eta->at(k))>2.5 ) continue;

ele_indexs.insert(map<int,int>::value_type(j, k));
                                              }//for k
                                            }// for j
}
///////////////////////////////////////////////////// 2F //////////////////////////////////
else if(do_FR_2F==true){
for(unsigned int j=0;j<heeps_et->size();j++){
int e1_pass_trigger=0;
if(is_data){ if(ev_run>=trig_Calo_trID_run_low && ev_run<=trig_Calo_trID_run_up) e1_pass_trigger=trigger_match(heeps_sc_eta->at(j),heeps_sc_phi->at(j),trig_DEle33_unseed_eta,trig_DEle33_unseed_phi,trig_DEle33);
             else e1_pass_trigger=trigger_match(heeps_sc_eta->at(j),heeps_sc_phi->at(j),trig_DEle33_MW_unseed_eta,trig_DEle33_MW_unseed_phi,trig_DEle33_MW);
           }
else{
if     (Year=="2016")e1_pass_trigger=trigEle_2016::passTrig(heeps_et->at(j), heeps_sc_eta->at(j)) ;
else if(Year=="2017")e1_pass_trigger=trigEle_2017::passTrig(heeps_et->at(j), heeps_sc_eta->at(j)) ;
else if(Year=="2018")e1_pass_trigger=trigEle_2018::passTrig(heeps_et->at(j), heeps_sc_eta->at(j), PU_data, use_DoubleEle25) ;
    }
if(e1_pass_trigger==0 || heeps_PreSelection->at(j)==0 || heeps_isHEEP7->at(j)==1 || (fabs(heeps_sc_eta->at(j))>1.4442 && fabs(heeps_sc_eta->at(j))<1.566) || fabs(heeps_sc_eta->at(j))>2.5 ) continue;
for(unsigned int k=j+1;k<heeps_et->size();k++){
int e2_pass_trigger=0;
if(is_data){ if(ev_run>=trig_Calo_trID_run_low && ev_run<=trig_Calo_trID_run_up) e2_pass_trigger=trigger_match(heeps_sc_eta->at(k),heeps_sc_phi->at(k),trig_DEle33_unseed_eta,trig_DEle33_unseed_phi,trig_DEle33);
             else e2_pass_trigger=trigger_match(heeps_sc_eta->at(k),heeps_sc_phi->at(k),trig_DEle33_MW_unseed_eta,trig_DEle33_MW_unseed_phi,trig_DEle33_MW);
           }
else{
if     (Year=="2016")e2_pass_trigger=trigEle_2016::passTrig(heeps_et->at(k), heeps_sc_eta->at(k)) ;
else if(Year=="2017")e2_pass_trigger=trigEle_2017::passTrig(heeps_et->at(k), heeps_sc_eta->at(k)) ;
else if(Year=="2018")e2_pass_trigger=trigEle_2018::passTrig(heeps_et->at(k), heeps_sc_eta->at(k), PU_data, use_DoubleEle25) ;
    }
if(e2_pass_trigger==0 || heeps_PreSelection->at(k)==0 || heeps_isHEEP7->at(k)==1 || (fabs(heeps_sc_eta->at(k))>1.4442 && fabs(heeps_sc_eta->at(k))<1.566) || fabs(heeps_sc_eta->at(k))>2.5 ) continue;

ele_indexs.insert(map<int,int>::value_type(j, k));
                                              }//for k
                                            }// for j

}
///////////////////////////////////////////////////////////// Nonimal ////////////////////////////
else{
float min_diff=999;
TLorentzVector tmp_e1(0,0,0,0);
TLorentzVector tmp_e2(0,0,0,0);
TLorentzVector tmp_Zee;
float max_sum_et=0;
int index_1=-1;
int index_2=-1;
int index_Z1=-1;
int index_Z2=-1;
for(unsigned int j=0;j<heeps_et->size();j++){
if(is_data && heeps_saturated->at(j)==1) f_add_out<<"Saturated "<<ev_run<<" "<<ev_luminosityBlock<<" "<<ev_event<<" VID:"<<heeps_VIDHEEP7->at(j)<<" HEEP:"<<heeps_isHEEP7->at(j)<<" Et:"<<heeps_et->at(j)<<" sc_eta:"<<heeps_sc_eta->at(j)<<" phi:"<<heeps_phi->at(j)<<" MET:"<<MET_Filter<<"\n";
int e1_pass_trigger=0;
int e1_match_L1    =1;
if(is_data){ if(ev_run>=trig_Calo_trID_run_low && ev_run<=trig_Calo_trID_run_up) e1_pass_trigger=trigger_match(heeps_sc_eta->at(j),heeps_sc_phi->at(j),trig_DEle33_unseed_eta,trig_DEle33_unseed_phi,trig_DEle33);
             else e1_pass_trigger=trigger_match(heeps_sc_eta->at(j),heeps_sc_phi->at(j),trig_DEle33_MW_unseed_eta,trig_DEle33_MW_unseed_phi,trig_DEle33_MW);
             if(Year=="2017") e1_match_L1      =L1_trigger_match(heeps_sc_eta->at(j),heeps_sc_phi->at(j),trig_DEle33_MW_L1_eta,trig_DEle33_MW_L1_phi,trig_DEle33_MW_L1_et,int(ev_run), int(ev_luminosityBlock));
           }
else{
if     (Year=="2016")e1_pass_trigger=trigEle_2016::passTrig(heeps_et->at(j), heeps_sc_eta->at(j)) ;
else if(Year=="2017")e1_pass_trigger=trigEle_2017::passTrig(heeps_et->at(j), heeps_sc_eta->at(j)) ;
else if(Year=="2018")e1_pass_trigger=trigEle_2018::passTrig(heeps_et->at(j), heeps_sc_eta->at(j), PU_data, use_DoubleEle25) ;
     if(Year=="2017")e1_match_L1    = trigEle33l1::passTrig(heeps_sc_et->at(j),heeps_sc_eta->at(j),PU_data, false) ;
    }
if(e1_pass_trigger==0 || heeps_isHEEP7->at(j)==0 || (fabs(heeps_sc_eta->at(j))>1.4442 && fabs(heeps_sc_eta->at(j))<1.566) || fabs(heeps_sc_eta->at(j))>2.5) continue;
//std::cout<<"event="<<i<<"e1="<<j<<std::endl;
for(unsigned int k=j+1;k<heeps_et->size();k++){
int e2_pass_trigger=0;
int e2_match_L1    =1;
if(is_data){ if(ev_run>=trig_Calo_trID_run_low && ev_run<=trig_Calo_trID_run_up) e2_pass_trigger=trigger_match(heeps_sc_eta->at(k),heeps_sc_phi->at(k),trig_DEle33_unseed_eta,trig_DEle33_unseed_phi,trig_DEle33);
             else e2_pass_trigger=trigger_match(heeps_sc_eta->at(k),heeps_sc_phi->at(k),trig_DEle33_MW_unseed_eta,trig_DEle33_MW_unseed_phi,trig_DEle33_MW);
             if(Year=="2017") e2_match_L1      =L1_trigger_match(heeps_sc_eta->at(k),heeps_sc_phi->at(k),trig_DEle33_MW_L1_eta,trig_DEle33_MW_L1_phi,trig_DEle33_MW_L1_et,int(ev_run), int(ev_luminosityBlock));
           }
else{
if     (Year=="2016")e2_pass_trigger=trigEle_2016::passTrig(heeps_et->at(k), heeps_sc_eta->at(k)) ;
else if(Year=="2017")e2_pass_trigger=trigEle_2017::passTrig(heeps_et->at(k), heeps_sc_eta->at(k)) ;
else if(Year=="2018")e2_pass_trigger=trigEle_2018::passTrig(heeps_et->at(k), heeps_sc_eta->at(k), PU_data, use_DoubleEle25) ;
     if(Year=="2017")e2_match_L1    = trigEle33l1::passTrig(heeps_sc_et->at(k),heeps_sc_eta->at(k),PU_data, false) ;
    }
if(e2_pass_trigger==0 || heeps_isHEEP7->at(k)==0 || (fabs(heeps_sc_eta->at(k))>1.4442 && fabs(heeps_sc_eta->at(k))<1.566) || fabs(heeps_sc_eta->at(k))>2.5) continue;
//std::cout<<"event="<<i<<"e2="<<k<<std::endl;
/////////////////////////// check L1 ///////////////////////////////////////////////

if(use_L1SingleEG && Year == "2017") {if(e1_match_L1==0 && e2_match_L1==0) continue;}//for L1 SingleEG matching
//std::cout<<"pass L1"<<std::endl;
//if(use_L1DoubleEG) {if(L1_pass_final==0) continue;}//for L1 DoubleEG matching

if((heeps_et->at(j)+heeps_et->at(k))>max_sum_et) {max_sum_et=heeps_et->at(j)+heeps_et->at(k);
                                                  index_1=j;
                                                  index_2=k;
                                                  is_pass_L1=(e1_match_L1==0 && e2_match_L1==0)?0:1;
                                                 }
if(use_Z_mass_suppress){
tmp_e1.SetPtEtaPhiM(heeps_et->at(j),heeps_eta->at(j),heeps_phi->at(j),m_el);
tmp_e2.SetPtEtaPhiM(heeps_et->at(k),heeps_eta->at(k),heeps_phi->at(k),m_el);
tmp_Zee=tmp_e1+tmp_e2;
if(fabs(tmp_Zee.M()-M_Z)<min_diff){min_diff=fabs(tmp_Zee.M()-M_Z);
                                   index_Z1=j;
                                   index_Z2=k;
                                  }

}// Z mass suppress
                                              }//for k
                                            }// for j
if(index_1!=-1 && index_2!=-1){
if(use_Z_mass_suppress && min_diff<=20 && index_Z1!=-1 && index_Z2!=-1) ele_indexs.insert(map<int,int>::value_type(index_Z1, index_Z2));
else ele_indexs.insert(map<int,int>::value_type(index_1, index_2));
}
//std::cout<<"pass event="<<i<<",e1="<<index_1<<",e2="<<index_2<<std::endl;
}//else



/////////////////////// fill histograms///////////////////////////////////////////////

for(map<int,int>::iterator iter = ele_indexs.begin( ); iter != ele_indexs.end( ); iter++ ){
int e1_index=iter->first;
int e2_index=iter->second;
TLorentzVector e1(0,0,0,0);
TLorentzVector e2(0,0,0,0);
e1.SetPtEtaPhiM(heeps_et->at(e1_index),heeps_eta->at(e1_index),heeps_phi->at(e1_index),m_el);
e2.SetPtEtaPhiM(heeps_et->at(e2_index),heeps_eta->at(e2_index),heeps_phi->at(e2_index),m_el);
TLorentzVector Zee=e1+e2;
float e1_E=heeps_E->at(e1_index);
float e2_E=heeps_E->at(e2_index);
float e1_et=heeps_et->at(e1_index);
float e2_et=heeps_et->at(e2_index);
float e1_sc_eta=heeps_sc_eta->at(e1_index);
float e2_sc_eta=heeps_sc_eta->at(e2_index);
float e1_eta   =heeps_eta->at(e1_index);
float e2_eta   =heeps_eta->at(e2_index);
float e1_phi   =heeps_phi->at(e1_index);
float e2_phi   =heeps_phi->at(e2_index);
int e1_saturated=remove_saturated ? heeps_saturated->at(e1_index) : 0;
int e2_saturated=remove_saturated ? heeps_saturated->at(e2_index) : 0;
float mee=Zee.M();
float led_et=(e1_et > e2_et) ? e1_et : e2_et;
float sub_et=(e1_et > e2_et) ? e2_et : e1_et;
float led_E =(e1_E > e2_E) ? e1_E : e2_E;
float sub_E =(e1_E > e2_E) ? e2_E : e1_E;
int region=0;
if(fabs(e1_eta)<1.4442 && fabs(e2_eta)<1.4442)region=1;
else if ((fabs(e1_eta)>1.566 && fabs(e2_eta)<1.4442) || (fabs(e1_eta)<1.4442 && fabs(e2_eta)>1.566))region=2;
else if(fabs(e1_eta)>1.566 && fabs(e2_eta)>1.566)region=3;
if(OnlyFor1TeV && mee <1000)continue;
/*
if(check_sc_et){
float e1_sc_et=heeps_sc_et->at(e1_index);
float e2_sc_et=heeps_sc_et->at(e2_index);
if(e1_sc_et<50){
if(fabs(e1_sc_eta)<1.4442){h_diff_et_barrel->Fill((e1_sc_et-e1_et)/e1_et);}
else{h_diff_et_endcap->Fill((e1_sc_et-e1_et)/e1_et);}
}
if(e2_sc_et<50){
if(fabs(e2_sc_eta)<1.4442){h_diff_et_barrel->Fill((e2_sc_et-e2_et)/e2_et);}
else{h_diff_et_endcap->Fill((e2_sc_et-e2_et)/e2_et);}
}
}
if(check_Et) if(e1_et<45 || e2_et<45)continue;//check >45, >45
*/
float e1_L1_Et    = 0;// not used
float e2_L1_Et    = 0;// not used
//float e1_L1_Et    = use_DoubleEle25 == false ? L1_trigger_match_Et(heeps_sc_eta->at(e1_index),heeps_sc_phi->at(e1_index),trig_DEle33_MW_L1_eta,trig_DEle33_MW_L1_phi,trig_DEle33_MW_L1_et) : 0;// check the Et of the matched L1 object
//float e2_L1_Et    = use_DoubleEle25 == false ? L1_trigger_match_Et(heeps_sc_eta->at(e2_index),heeps_sc_phi->at(e2_index),trig_DEle33_MW_L1_eta,trig_DEle33_MW_L1_phi,trig_DEle33_MW_L1_et) : 0;
//////////////for gen match //////////////////
if(do_match && is_data==false){ if(heeps_match->at(e1_index)==0 || heeps_match->at(e2_index)==0) continue;
                                if(LHE_Mass_cut && LHE_Z_mass>120)continue;//for select DY < 120 GeV
                              }//for match check


//if(mee>=1500) f_add_out<<"m>=1500 "<<ev_run<<" "<<ev_luminosityBlock<<" "<<ev_event<<" "<<mee<<" "<<e1.Pt()<<" "<<e1.Eta()<<" "<<e1.Phi()<<" "<<heeps_charge->at(e1_index)<<" "<<e2.Pt()<<" "<<e2.Eta()<<" "<<e2.Phi()<<" "<<heeps_charge->at(e2_index)<<"\n";
if(mee>=1000) f_add_out<<"Run:"<<ev_run<<",LS:"<<ev_luminosityBlock<<",Event:"<<ev_event<<",M:"<<mee<<",e1_Et:"<<e1.Pt()<<",e1_eta:"<<e1.Eta()<<",e1_sc_eta:"<<e1_sc_eta<<",e1_phi:"<<e1.Phi()<<",e1_c:"<<heeps_charge->at(e1_index)<<",e2_Et:"<<e2.Pt()<<",e2_eta:"<<e2.Eta()<<",e2_sc_eta:"<<e2_sc_eta<<",e2_phi:"<<e2.Phi()<<",e2_c:"<<heeps_charge->at(e2_index)<<",e1_dPhi:"<<heeps_dPhiIn->at(e1_index)<<",e1_Sieie:"<<heeps_Sieie->at(e1_index)<<",e1_missHit:"<<heeps_missingHits->at(e1_index)<<",e1_dxy:"<<heeps_dxyFirstPV->at(e1_index)<<",e1_HoE:"<<heeps_HOverE->at(e1_index)<<",e1_E1X5:"<<heeps_E1x5OverE5x5->at(e1_index)<<",e1_E2X5:"<<heeps_E2x5OverE5x5->at(e1_index)<<",e1_EMHD1:"<<heeps_isolEMHadDepth1->at(e1_index)<<",e1_trkiso:"<<heeps_IsolPtTrks->at(e1_index)<<",e1_ECAL:"<<heeps_EcalDriven->at(e1_index)<<",e1_dEta:"<<heeps_dEtaIn->at(e1_index)<<",e2_dPhi:"<<heeps_dPhiIn->at(e2_index)<<",e2_Sieie:"<<heeps_Sieie->at(e2_index)<<",e2_missHit:"<<heeps_missingHits->at(e2_index)<<",e2_dxy:"<<heeps_dxyFirstPV->at(e2_index)<<",e2_HoE:"<<heeps_HOverE->at(e2_index)<<",e2_E1X5:"<<heeps_E1x5OverE5x5->at(e2_index)<<",e2_E2X5:"<<heeps_E2x5OverE5x5->at(e2_index)<<",e2_EMHD1:"<<heeps_isolEMHadDepth1->at(e2_index)<<",e2_trkiso:"<<heeps_IsolPtTrks->at(e2_index)<<",e2_ECAL:"<<heeps_EcalDriven->at(e2_index)<<",e2_dEta:"<<heeps_dEtaIn->at(e2_index)<<"\n";
///////////// calcCosThetaCSAnal ////////////
double CosThetaCS=0;
int same_sign=0;
if(heeps_charge->at(e1_index)*heeps_charge->at(e2_index) < 0){
                                                              if(heeps_charge->at(e1_index)<0) CosThetaCS= calcCosThetaCSAnal(Zee, e1, e2);
                                                              else CosThetaCS= calcCosThetaCSAnal(Zee, e2, e1);
                                                             }
else{same_sign=1;//skip
     CosThetaCS= calcCosThetaCSAnal(Zee, e1, e2);
    }
//////////////////////// PU ///////////////////////////
if(do_PU_weight==true) {
                        if(Year=="2016"){
                                                         event_weight=event_sign*PU_2016::MC_pileup_weight(PU_true,0,"all");
                        if(uncert=="PU_scale_up")        event_weight=event_sign*PU_2016::MC_pileup_weight(PU_true,1,"all");
                        else if(uncert=="PU_scale_down") event_weight=event_sign*PU_2016::MC_pileup_weight(PU_true,2,"all");
                                        }
                        else if(Year=="2017"){
                        // weight sample by sample in 2017 
                                                         event_weight=event_sign*PU_2017::MC_pileup_weight(PU_true,pu_name,"Rereco_all"); 
                        if(uncert=="PU_scale_up")        event_weight=event_sign*PU_2017::MC_pileup_weight(PU_true,pu_name,"Rereco_all_scaleUp");
                        else if(uncert=="PU_scale_down") event_weight=event_sign*PU_2017::MC_pileup_weight(PU_true,pu_name,"Rereco_all_scaleDown");
                                        }
                        else if(Year=="2018"){
                        // due to use 2017 TT and WW mass bin sample
                        if(true) {                       event_weight=event_sign*PU_2018_PerMC::MC_pileup_weight(PU_true,pu_name,"Run_all"          );
                        if(uncert=="PU_scale_up")        event_weight=event_sign*PU_2018_PerMC::MC_pileup_weight(PU_true,pu_name,"Run_all_scaleUp"  );
                        else if(uncert=="PU_scale_down") event_weight=event_sign*PU_2018_PerMC::MC_pileup_weight(PU_true,pu_name,"Run_all_scaleDown");
                                 }

                        else{
                                                         event_weight=event_sign*PU_2018::MC_pileup_weight(PU_true,0,"all");
                        if(uncert=="PU_scale_up")        event_weight=event_sign*PU_2018::MC_pileup_weight(PU_true,1,"all");
                        else if(uncert=="PU_scale_down") event_weight=event_sign*PU_2018::MC_pileup_weight(PU_true,2,"all");
                            }
                                        }
                       }
else event_weight=event_sign;
///////////////////////////// fake rate ////////////////
if(Year=="2016"){
     if(do_FR_1F==true) fake_rate=FR_2016::frFuncData(e2_et, e2_sc_eta)/(1-FR_2016::frFuncData(e2_et, e2_sc_eta));
else if(do_FR_2F==true)fake_rate=(FR_2016::frFuncData(e1_et, e1_sc_eta)/(1-FR_2016::frFuncData(e1_et, e1_sc_eta)))*(FR_2016::frFuncData(e2_et, e2_sc_eta)/(1-FR_2016::frFuncData(e2_et, e2_sc_eta)) );
else fake_rate=1;
}
else if(Year=="2017"){
     if(do_FR_1F==true) fake_rate=FR_2017::frFuncData(e2_et, e2_sc_eta)/(1-FR_2017::frFuncData(e2_et, e2_sc_eta));
else if(do_FR_2F==true)fake_rate=(FR_2017::frFuncData(e1_et, e1_sc_eta)/(1-FR_2017::frFuncData(e1_et, e1_sc_eta)))*(FR_2017::frFuncData(e2_et, e2_sc_eta)/(1-FR_2017::frFuncData(e2_et, e2_sc_eta)) );
else fake_rate=1;
}
else if(Year=="2018"){
     if(do_FR_1F==true) fake_rate=FR_2018::frFuncData(e2_et, e2_sc_eta, e2_phi, ev_run, is_data)/(1-FR_2018::frFuncData(e2_et, e2_sc_eta, e2_phi, ev_run, is_data));
else if(do_FR_2F==true)fake_rate=(FR_2018::frFuncData(e1_et, e1_sc_eta, e1_phi, ev_run, is_data)/(1-FR_2018::frFuncData(e1_et, e1_sc_eta, e1_phi, ev_run, is_data)))*(FR_2018::frFuncData(e2_et, e2_sc_eta, e2_phi, ev_run, is_data)/(1-FR_2018::frFuncData(e2_et, e2_sc_eta, e2_phi, ev_run, is_data)) );
else fake_rate=1;
}

////////////////// NNPDF30/NNPDF31 ////////////////////////////
/*
if(do_NNPDF30_weight) {
                    if(mee>120)NNPDF30_weight = 0.9803 - 1.068e-04*mee + 1.142e-07*mee*mee - 2.013e-11*mee*mee*mee-5.904*pow(mee,4)+1.634e-18*pow(mee,5); //from muon
                    else NNPDF30_weight=1;
                   }
else NNPDF30_weight=1;
*/
//////////////// In Z peak: NNPDF3.1 to NNPDF3.0 weight using leading Et //////////////////
float NNPDF_weight=1;
if(is_ZToEE  && (Year=="2017" || Year=="2018") ){
if(Gen_Z_mass<120){
if(region==1)      NNPDF_weight=(Gen_Led_Et<150) ? 3.596-0.2076 *Gen_Led_Et+0.005795*pow(Gen_Led_Et,2)-7.421e-05*pow(Gen_Led_Et,3)+4.447e-07*pow(Gen_Led_Et,4)-1.008e-9 *pow(Gen_Led_Et,5) : 0.969125;
else if(region==2) NNPDF_weight=(Gen_Led_Et<150) ? 2.066-0.09495*Gen_Led_Et+0.002664*pow(Gen_Led_Et,2)-3.242e-05*pow(Gen_Led_Et,3)+1.755e-07*pow(Gen_Led_Et,4)-3.424e-10*pow(Gen_Led_Et,5) : 1.191875;
else if(region==3) NNPDF_weight=(Gen_Led_Et<150) ? 2.865-0.1443 *Gen_Led_Et+0.003799*pow(Gen_Led_Et,2)-4.482e-05*pow(Gen_Led_Et,3)+2.429e-07*pow(Gen_Led_Et,4)-4.93e-10 *pow(Gen_Led_Et,5) : 0.9609375;
}
else{
if(region==1)      NNPDF_weight=(Gen_Z_mass<5000) ? 0.8934+0.0002193 *Gen_Z_mass-1.961e-7*pow(Gen_Z_mass,2)+8.704e-11*pow(Gen_Z_mass,3)-1.551e-14*pow(Gen_Z_mass,4)+1.112e-18*pow(Gen_Z_mass,5) : 1.74865;
else if(region==2) NNPDF_weight=(Gen_Z_mass<5000) ? 0.8989+0.000182  *Gen_Z_mass-1.839e-7*pow(Gen_Z_mass,2)+1.026e-10*pow(Gen_Z_mass,3)-2.361e-14*pow(Gen_Z_mass,4)+1.927e-18*pow(Gen_Z_mass,5) : 1.302025;
else if(region==3) NNPDF_weight=(Gen_Z_mass<5000) ? 0.9328-7.23e-6   *Gen_Z_mass+3.904e-9*pow(Gen_Z_mass,2)+2.454e-11*pow(Gen_Z_mass,3)-1.038e-14*pow(Gen_Z_mass,4)+1.543e-18*pow(Gen_Z_mass,5) : 2.396125;
}
}
float tt_weight=1;
if(do_tt_reweight && Gen_Z_mass>500){
if(region==1){
Int_t bin_tt = tt_BB_axis->FindBin(Gen_Z_mass);
if(Gen_Z_mass > tt_BB_axis_max)      bin_tt=tt_BB_axis->FindBin(tt_BB_axis_max-0.01);
else if(Gen_Z_mass < tt_BB_axis_min) bin_tt=tt_BB_axis->FindBin(tt_BB_axis_min+0.01);
tt_weight = h_tt_BB->GetBinContent(bin_tt);// get the ratio of NNPDF3.0 to NNPDF3.1
}
else if(region==2){
Int_t bin_tt = tt_BE_axis->FindBin(Gen_Z_mass);
if(Gen_Z_mass > tt_BE_axis_max)      bin_tt=tt_BE_axis->FindBin(tt_BE_axis_max-0.01);
else if(Gen_Z_mass < tt_BE_axis_min) bin_tt=tt_BE_axis->FindBin(tt_BE_axis_min+0.01);
tt_weight = h_tt_BE->GetBinContent(bin_tt);// get the ratio of NNPDF3.0 to NNPDF3.1
}
/*
else if(region==3){
Int_t bin_tt = tt_EE_axis->FindBin(Gen_Z_mass);
if(Gen_Z_mass > tt_EE_axis_max)      bin_tt=tt_EE_axis->FindBin(tt_EE_axis_max-0.01);
else if(Gen_Z_mass < tt_EE_axis_min) bin_tt=tt_EE_axis->FindBin(tt_EE_axis_min+0.01);
tt_weight = h_tt_EE->GetBinContent(bin_tt);// get the ratio of NNPDF3.0 to NNPDF3.1
}
*/
}

/*
Int_t bin_NNPDF = NNPDF_axis->FindBin(led_et);
if(led_et > NNPDF_axis_max)      bin_NNPDF=NNPDF_axis->FindBin(NNPDF_axis_max-0.01);
else if(led_et < NNPDF_axis_min) bin_NNPDF=NNPDF_axis->FindBin(NNPDF_axis_min+0.01);
NNPDF_weight = h_NNPDF->GetBinContent(bin_NNPDF);// get the ratio of NNPDF3.0 to NNPDF3.1
*/
//std::cout<<"tt_weight="<<tt_weight<<",region="<<region<<",M gen="<<Gen_Z_mass<<std::endl;
////////////////// fewz ////////////////////////////
if(do_fewz_weight) {
                    //if(mee>120)fewz_weight = 1.06780 - 1.20666e-04*mee + 3.22646e-08*mee*mee - 3.94886e-12*mee*mee*mee;
                    if(Gen_Z_mass>120)fewz_weight = 1.06780 - 1.20666e-04*Gen_Z_mass + 3.22646e-08*Gen_Z_mass*Gen_Z_mass - 3.94886e-12*Gen_Z_mass*Gen_Z_mass*Gen_Z_mass;
                    else fewz_weight=1;
                   }
else fewz_weight=1;
//////////////// pdf uncertainty //////////////////
float pdf_weight=1;
if(is_ZToEE && uncert=="pdf_scale_up" && Gen_Z_mass>120){
   //double pdf_uncert=1.25509-0.000131645*mee+1.28426e-06*pow(mee,2)-5.32126e-10*pow(mee,3)+7.62146e-14*pow(mee,4);
   //double pdf_uncert=0.43305-0.00329146*mee-2.15864e-06*pow(mee,2)+9.0436e-10*pow(mee,3)-1.80655e-13*pow(mee,4)+1.51031e-17*pow(mee,5);
   double pdf_uncert=0.43305-0.00329146*Gen_Z_mass-2.15864e-06*pow(Gen_Z_mass,2)+9.0436e-10*pow(Gen_Z_mass,3)-1.80655e-13*pow(Gen_Z_mass,4)+1.51031e-17*pow(Gen_Z_mass,5);
   pdf_weight=1+(pdf_uncert/100);
   }
else if(is_ZToEE && uncert=="pdf_scale_down" && Gen_Z_mass>120){
   //double pdf_uncert=1.25509-0.000131645*mee+1.28426e-06*pow(mee,2)-5.32126e-10*pow(mee,3)+7.62146e-14*pow(mee,4);
   //double pdf_uncert=0.43305-0.00329146*mee-2.15864e-06*pow(mee,2)+9.0436e-10*pow(mee,3)-1.80655e-13*pow(mee,4)+1.51031e-17*pow(mee,5);
   double pdf_uncert=0.43305-0.00329146*Gen_Z_mass-2.15864e-06*pow(Gen_Z_mass,2)+9.0436e-10*pow(Gen_Z_mass,3)-1.80655e-13*pow(Gen_Z_mass,4)+1.51031e-17*pow(Gen_Z_mass,5);
   pdf_weight=1-(pdf_uncert/100);
   }
else pdf_weight=1;
//std::cout<<"gen_m="<<Gen_Z_mass<<",pdf_weight="<<std::endl;
/////////////////////////gsf sf/////////////////////////////
float sf_gsf_weight=1;
/*
if(use_gsf_sf && is_data==false){
     if(PU_data=="Rereco_all") sf_gsf_weight =scale_factor(sf_Ele_Reco_Map_BCDEF ,e1_et,e1_sc_eta,"")*scale_factor(sf_Ele_Reco_Map_BCDEF ,e2_et ,e2_sc_eta,"");
else if(PU_data=="Rereco_B")   sf_gsf_weight =scale_factor(sf_Ele_Reco_Map_B     ,e1_et,e1_sc_eta,"")*scale_factor(sf_Ele_Reco_Map_B     ,e2_et ,e2_sc_eta,"");
else if(PU_data=="Rereco_C")   sf_gsf_weight =scale_factor(sf_Ele_Reco_Map_C     ,e1_et,e1_sc_eta,"")*scale_factor(sf_Ele_Reco_Map_C     ,e2_et ,e2_sc_eta,"");
else if(PU_data=="Rereco_D")   sf_gsf_weight =scale_factor(sf_Ele_Reco_Map_D     ,e1_et,e1_sc_eta,"")*scale_factor(sf_Ele_Reco_Map_D     ,e2_et ,e2_sc_eta,"");
else if(PU_data=="Rereco_E")   sf_gsf_weight =scale_factor(sf_Ele_Reco_Map_E     ,e1_et,e1_sc_eta,"")*scale_factor(sf_Ele_Reco_Map_E     ,e2_et ,e2_sc_eta,"");
else if(PU_data=="Rereco_F")   sf_gsf_weight =scale_factor(sf_Ele_Reco_Map_F     ,e1_et,e1_sc_eta,"")*scale_factor(sf_Ele_Reco_Map_F     ,e2_et ,e2_sc_eta,"");
}
*/
/////////////////// PreFiring weight /////////////////////////////////
float pfweight=1;
if(applyPreFiringW && is_data==false && (Year=="2016" || Year=="2017") ){
                                 pfweight=prefiringweight;
     if(uncert=="pf_scale_up"  ) pfweight=prefiringweightup;
else if(uncert=="pf_scale_down") pfweight=prefiringweightdown;
}
//std::cout<<"weight="<<event_weight<<",fr="<<fake_rate<<",fz="<<fewz_weight<<",sf1="<<sf_weight(e1_et, e1_sc_eta,uncert)<<",sf2="<<sf_weight(e2_et, e2_sc_eta,uncert)<<",pdf="<<pdf_weight<<",gsf="<<sf_gsf_weight<<",pf="<<pfweight<<"NNPDF="<<NNPDF_weight<<std::endl;
//event_weight=event_weight*fake_rate*fewz_weight*sf_weight(e1_et, e1_sc_eta,uncert)*sf_weight(e2_et, e2_sc_eta,uncert)*pdf_weight*sf_gsf_weight*pfweight;
//event_weight=event_weight*fake_rate*fewz_weight*sf_weight(e1_et, e1_sc_eta,uncert)*sf_weight(e2_et, e2_sc_eta,uncert)*pdf_weight*sf_gsf_weight*pfweight*NNPDF_weight;
event_weight=event_weight*fake_rate*fewz_weight*sf_weight(e1_et, e1_sc_eta,uncert)*sf_weight(e2_et, e2_sc_eta,uncert)*pdf_weight*sf_gsf_weight*pfweight*NNPDF_weight*tt_weight;
TAxis *xaxis = h_mee_all->GetXaxis();
Int_t binx = xaxis->FindBin(mee);
Float_t bin_width=h_mee_all->GetXaxis()->GetBinWidth(binx);
float cos_mee_cut=200;
int barrel_barrel=0;

if(fabs(e1_sc_eta)>2.5 || fabs(e2_sc_eta)>2.5 || (fabs(e1_sc_eta)>1.4442 && fabs(e1_sc_eta) <1.566) || (fabs(e2_sc_eta)>1.4442 && fabs(e2_sc_eta) <1.566) ) continue;//nominal

else if(fabs(e1_sc_eta)>1.566 && fabs(e1_sc_eta)<2.5 && fabs(e2_sc_eta)>1.566 && fabs(e2_sc_eta)<2.5 ) {
h_mee_Zpeak_EE->Fill(mee,event_weight);
h_mee_Zpeak_EE_v1->Fill(mee,event_weight);
h_mee_all_EE->Fill(mee,event_weight/bin_width);
h_mee_all_EE_sin->Fill(mee,event_weight);
h_mee_EE_usual->Fill(  mee,event_weight);   
h_mee_EE_fine ->Fill(  mee,event_weight); 

if(e1_sc_eta>1.566 && e2_sc_eta>1.566) h_mee_Zpeak_EE_pp->Fill(mee,event_weight);
else if(e1_sc_eta<-1.566 && e2_sc_eta<-1.566) h_mee_Zpeak_EE_mm->Fill(mee,event_weight);
else h_mee_Zpeak_EE_pm->Fill(mee,event_weight);
if(fabs(e1_sc_eta)>2.0 && fabs(e2_sc_eta)>2.0) h_mee_Zpeak_EE_Heta->Fill(mee,event_weight);
else if(fabs(e1_sc_eta)<2.0 && fabs(e2_sc_eta)<2.0) h_mee_Zpeak_EE_Leta->Fill(mee,event_weight);
else h_mee_Zpeak_EE_HLeta->Fill(mee,event_weight);

if(same_sign==0){
if(CosThetaCS>0) {h_mee_cosp_EE->Fill(mee,event_weight/bin_width);
                  h_mee_cosp_EE_fine->Fill(mee,event_weight);
                  h_mee_cosp_all_fine->Fill(mee,event_weight);
                 }
else             {h_mee_cosm_EE->Fill(mee,event_weight/bin_width);
                  h_mee_cosm_EE_fine->Fill(mee,event_weight);
                  h_mee_cosm_all_fine->Fill(mee,event_weight);
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
h_pass_L1_EE->Fill(mee,is_pass_L1);
h_rho_EE ->Fill(rho     ,event_weight);
Region=2;
if(is_data && do_FR_1F==false && do_FR_2F==false)fout<<ev_run<<" "<<ev_luminosityBlock<<" "<<ev_event<<" "<<mee<<" "<<Region<<"\n";
h_led_Et_Mee_EE->Fill(led_et,mee);
h_led_E_Mee_EE->Fill(led_E,mee);
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
                                               if(same_sign==0){
                                               if(CosThetaCS>0) {h_mee_cosp_BB->Fill(mee,event_weight/bin_width);
                                                                 h_mee_cosp_BB_fine->Fill(mee,event_weight);
                                                                 h_mee_cosp_all_fine->Fill(mee,event_weight);
                                                                }
                                               else             {h_mee_cosm_BB->Fill(mee,event_weight/bin_width);
                                                                 h_mee_cosm_BB_fine->Fill(mee,event_weight);
                                                                 h_mee_cosm_all_fine->Fill(mee,event_weight);
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
                                               h_led_Et_Mee_BB->Fill(led_et,mee);
                                               h_led_E_Mee_BB->Fill(led_E,mee);
                                               if (fabs(e1_eta)<0.5){h_limit_eta_Mee_BB->Fill(e1_eta,mee);h_float_eta_Mee_BB->Fill(e2_eta,mee);}
                                               else if (fabs(e2_eta)<0.5){h_limit_eta_Mee_BB->Fill(e2_eta,mee);h_float_eta_Mee_BB->Fill(e1_eta,mee);}
                                               //if(LHE_Z_mass<5000){if(e1_saturated==0 && e2_saturated==0) h_resolution_BB->Fill((mee-LHE_Z_mass)/LHE_Z_mass); 
                                               if(Gen_Z_mass<5000){if(e1_saturated==0 && e2_saturated==0) h_resolution_BB->Fill((mee-Gen_Z_mass)/Gen_Z_mass); 
                                                                   h_N_saturated_BB->Fill(e1_saturated+e2_saturated); 
                                                                  }
                                               h_pass_L1_BB->Fill(mee,is_pass_L1);
                                               //### for L1 Et check #################
                                               h_L1Et_BB->Fill(e1_L1_Et,event_weight);
                                               h_L1Et_BB->Fill(e2_L1_Et,event_weight);
                                               h_rho_BB ->Fill(rho     ,event_weight);
                                               Region=0;
                                                         }

else if( (fabs(e1_sc_eta)<1.4442 && (fabs(e2_sc_eta)>1.566 && fabs(e2_sc_eta)<2.5)) || (fabs(e2_sc_eta)<1.4442 && (fabs(e1_sc_eta)>1.566 && fabs(e1_sc_eta)<2.5)) ){
                                                                          if(uncert=="BE_mass_scale_up")mee=(mee>0) ? 1.014*mee: 1.0025*mee ;
                                                                          else if(uncert=="BE_mass_scale_down")mee=(mee>0) ? 0.986*mee: 0.9975*mee;
                                                                          //if(uncert=="BE_mass_scale_up")mee=(mee>0) ? 1.05*mee: 1.0025*mee ;
                                                                          //else if(uncert=="BE_mass_scale_down")mee=(mee>0) ? 0.95*mee: 0.9975*mee;
                                                                          h_mee_Zpeak_BE->Fill(mee,event_weight);
                                                                          h_mee_Zpeak_BE_v1->Fill(mee,event_weight);
                                                                          h_mee_all_BE->Fill(mee,event_weight/bin_width);
                                                                          h_mee_all_BE_sin->Fill(mee,event_weight);
                                                                          h_mee_BE_usual->Fill(  mee,event_weight);
                                                                          h_mee_BE_fine ->Fill(  mee,event_weight);
                                                                          if(same_sign==0){
                                                                          if(CosThetaCS>0) {h_mee_cosp_BE->Fill(mee,event_weight/bin_width);
                                                                                            h_mee_cosp_BE_fine->Fill(mee,event_weight);
                                                                                            h_mee_cosp_all_fine->Fill(mee,event_weight);
                                                                                           }
                                                                          else             {h_mee_cosm_BE->Fill(mee,event_weight/bin_width);
                                                                                            h_mee_cosm_BE_fine->Fill(mee,event_weight);
                                                                                            h_mee_cosm_all_fine->Fill(mee,event_weight);
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
                                                                          h_endcap_Et_Mee_BE->Fill(fabs(e1_sc_eta)<1.4442 ? e2_et  : e1_et ,mee);
                                                                          h_endcap_E_Mee_BE ->Fill(fabs(e1_sc_eta)<1.4442 ? e2_E   : e1_E  ,mee);
                                                                          if(fabs(e1_eta)<0.5)     {h_endcap_eta_Mee_BE->Fill(e2_eta,mee);}
                                                                          else if(fabs(e2_eta)<0.5){h_endcap_eta_Mee_BE->Fill(e1_eta,mee);}
                                                                          //if(LHE_Z_mass<5000){if(e1_saturated==0 && e2_saturated==0) h_resolution_BE->Fill((mee-LHE_Z_mass)/LHE_Z_mass);
                                                                          if(Gen_Z_mass<5000){if(e1_saturated==0 && e2_saturated==0) h_resolution_BE->Fill((mee-Gen_Z_mass)/Gen_Z_mass);
                                                                                              h_N_saturated_BE->Fill(e1_saturated+e2_saturated); 
                                                                                             }
                                                                          h_pass_L1_BE->Fill(mee,is_pass_L1);
                                                                          //### for L1 Et check #################
                                                                          h_L1Et_BE->Fill(e1_L1_Et,event_weight);
                                                                          h_L1Et_BE->Fill(e2_L1_Et,event_weight);
                                                                          h_rho_BE ->Fill(rho     ,event_weight);
                                                                          Region=1;
                                                                                      }
//if(is_data && do_FR_1F==false && do_FR_2F==false)fout<<ev_run<<" "<<ev_luminosityBlock<<" "<<ev_event<<" "<<mee<<" "<<barrel_barrel<<"\n";
if(is_data && do_FR_1F==false && do_FR_2F==false)fout<<ev_run<<" "<<ev_luminosityBlock<<" "<<ev_event<<" "<<mee<<" "<<Region<<"\n";


h_mee_Zpeak->Fill(mee,event_weight);
h_mee_Zpeak_v1->Fill(mee,event_weight);
h_mee_all->Fill(mee,event_weight/bin_width);
h_mee_all_sin->Fill(mee,event_weight);
h_mee_usual->Fill(  mee,event_weight);
h_mee_fine ->Fill(  mee,event_weight);

if(same_sign==0){
if(CosThetaCS>0) {h_mee_cosp->Fill(mee,event_weight/bin_width);
                  h_mee_cosp_fine->Fill(mee,event_weight);
                 }
else             {h_mee_cosm->Fill(mee,event_weight/bin_width);
                  h_mee_cosm_fine->Fill(mee,event_weight);
                 }
if(mee>cos_mee_cut)h_cos->Fill(CosThetaCS,event_weight);
}
else{
h_mee_all_SS->Fill(mee,event_weight);
}
fill_cum(h_mee_all_cum   , mee , event_weight);
fill_cum(h_mee_all_cum_v1, mee , event_weight);
//if(LHE_Z_mass<5000){if(e1_saturated==0 && e2_saturated==0) h_resolution->Fill((mee-LHE_Z_mass)/LHE_Z_mass);}
if(Gen_Z_mass<5000){if(e1_saturated==0 && e2_saturated==0) h_resolution->Fill((mee-Gen_Z_mass)/Gen_Z_mass);}

/*
if(MET_Filter==0) h_mee_fail_MET->Fill(mee ,event_weight);
if(MET_detail && is_data){
if(trig_Flag_HBHENoiseFilter                   ==0 ){h_MET_Filter_detail->Fill("HBHENoiseFilter"                   ,1);if(is_data && do_FR_1F==false && do_FR_2F==false)fout_MET<<"HBHENoiseFilter"                   <<" "<<ev_run<<" "<<ev_luminosityBlock<<" "<<ev_event<<" "<<mee<<" "<<barrel_barrel<<"\n"; } 
if(trig_Flag_HBHENoiseIsoFilter                ==0 ){h_MET_Filter_detail->Fill("HBHENoiseIsoFilter"                ,1);if(is_data && do_FR_1F==false && do_FR_2F==false)fout_MET<<"HBHENoiseIsoFilter"                <<" "<<ev_run<<" "<<ev_luminosityBlock<<" "<<ev_event<<" "<<mee<<" "<<barrel_barrel<<"\n"; } 
if(trig_Flag_globalTightHalo2016Filter         ==0 ){h_MET_Filter_detail->Fill("globalTightHalo2016Filter"         ,1);if(is_data && do_FR_1F==false && do_FR_2F==false)fout_MET<<"globalTightHalo2016Filter"         <<" "<<ev_run<<" "<<ev_luminosityBlock<<" "<<ev_event<<" "<<mee<<" "<<barrel_barrel<<"\n"; }
if(trig_Flag_goodVertices                      ==0 ){h_MET_Filter_detail->Fill("goodVertices"                      ,1);if(is_data && do_FR_1F==false && do_FR_2F==false)fout_MET<<"goodVertices"                      <<" "<<ev_run<<" "<<ev_luminosityBlock<<" "<<ev_event<<" "<<mee<<" "<<barrel_barrel<<"\n"; } 
if(trig_Flag_EcalDeadCellTriggerPrimitiveFilter==0 ){h_MET_Filter_detail->Fill("EcalDeadCellTriggerPrimitiveFilter",1);if(is_data && do_FR_1F==false && do_FR_2F==false)fout_MET<<"EcalDeadCellTriggerPrimitiveFilter"<<" "<<ev_run<<" "<<ev_luminosityBlock<<" "<<ev_event<<" "<<mee<<" "<<barrel_barrel<<"\n"; }
if(trig_Flag_BadChargedCandidateFilter         ==0 ){h_MET_Filter_detail->Fill("BadChargedCandidateFilter"         ,1);if(is_data && do_FR_1F==false && do_FR_2F==false)fout_MET<<"BadChargedCandidateFilter"         <<" "<<ev_run<<" "<<ev_luminosityBlock<<" "<<ev_event<<" "<<mee<<" "<<barrel_barrel<<"\n"; } 
if(trig_Flag_BadPFMuonFilter                   ==0 ){h_MET_Filter_detail->Fill("BadPFMuonFilter"                   ,1);if(is_data && do_FR_1F==false && do_FR_2F==false)fout_MET<<"BadPFMuonFilter"                   <<" "<<ev_run<<" "<<ev_luminosityBlock<<" "<<ev_event<<" "<<mee<<" "<<barrel_barrel<<"\n"; } 
if((is_data && trig_Flag_eeBadScFilter         ==0)){h_MET_Filter_detail->Fill("eeBadScFilter"                     ,1);if(is_data && do_FR_1F==false && do_FR_2F==false)fout_MET<<"eeBadScFilter"                     <<" "<<ev_run<<" "<<ev_luminosityBlock<<" "<<ev_event<<" "<<mee<<" "<<barrel_barrel<<"\n"; }
}
*/

//####################### for HEEP variables ########################################
h_dPhiIn          ->Fill(heeps_dPhiIn         ->at(e1_index),event_weight); 
h_Sieie           ->Fill(heeps_Sieie          ->at(e1_index),event_weight); 
h_missingHits     ->Fill(heeps_missingHits    ->at(e1_index),event_weight); 
h_dxyFirstPV      ->Fill(heeps_dxyFirstPV     ->at(e1_index),event_weight); 
h_HOverE          ->Fill(heeps_HOverE         ->at(e1_index),event_weight); 
h_E1x5OverE5x5    ->Fill(heeps_E1x5OverE5x5   ->at(e1_index),event_weight); 
h_E2x5OverE5x5    ->Fill(heeps_E2x5OverE5x5   ->at(e1_index),event_weight); 
h_isolEMHadDepth1 ->Fill(heeps_isolEMHadDepth1->at(e1_index),event_weight); 
h_IsolPtTrks      ->Fill(heeps_IsolPtTrks     ->at(e1_index),event_weight); 
h_EcalDriven      ->Fill(heeps_EcalDriven     ->at(e1_index),event_weight); 
h_dEtaIn          ->Fill(heeps_dEtaIn         ->at(e1_index),event_weight); 

h_dPhiIn          ->Fill(heeps_dPhiIn         ->at(e2_index),event_weight); 
h_Sieie           ->Fill(heeps_Sieie          ->at(e2_index),event_weight); 
h_missingHits     ->Fill(heeps_missingHits    ->at(e2_index),event_weight); 
h_dxyFirstPV      ->Fill(heeps_dxyFirstPV     ->at(e2_index),event_weight); 
h_HOverE          ->Fill(heeps_HOverE         ->at(e2_index),event_weight); 
h_E1x5OverE5x5    ->Fill(heeps_E1x5OverE5x5   ->at(e2_index),event_weight); 
h_E2x5OverE5x5    ->Fill(heeps_E2x5OverE5x5   ->at(e2_index),event_weight); 
h_isolEMHadDepth1 ->Fill(heeps_isolEMHadDepth1->at(e2_index),event_weight); 
h_IsolPtTrks      ->Fill(heeps_IsolPtTrks     ->at(e2_index),event_weight); 
h_EcalDriven      ->Fill(heeps_EcalDriven     ->at(e2_index),event_weight); 
h_dEtaIn          ->Fill(heeps_dEtaIn         ->at(e2_index),event_weight); 
//std::cout<<"e1--dPhiIn:"<<heeps_dPhiIn->at(e1_index)<<",Sieie:"<<heeps_Sieie->at(e1_index)<<",missingHits:"<<heeps_missingHits->at(e1_index)<<",dxy:"<<heeps_dxyFirstPV->at(e1_index)<<",H/E:"<<heeps_HOverE->at(e1_index)<<",E1X5/E5X5:"<<heeps_E1x5OverE5x5->at(e1_index)<<",E2X5/E5X5:"<<heeps_E2x5OverE5x5->at(e1_index)<<",EM+HD1:"<<heeps_isolEMHadDepth1->at(e1_index)<<",trkiso:"<<heeps_IsolPtTrks->at(e1_index)<<",ECALDriven:"<<heeps_EcalDriven->at(e1_index)<<",detain:"<<heeps_dEtaIn->at(e1_index)<<std::endl;
//std::cout<<"e2--dPhiIn:"<<heeps_dPhiIn->at(e2_index)<<",Sieie:"<<heeps_Sieie->at(e2_index)<<",missingHits:"<<heeps_missingHits->at(e2_index)<<",dxy:"<<heeps_dxyFirstPV->at(e2_index)<<",H/E:"<<heeps_HOverE->at(e2_index)<<",E1X5/E5X5:"<<heeps_E1x5OverE5x5->at(e2_index)<<",E2X5/E5X5:"<<heeps_E2x5OverE5x5->at(e2_index)<<",EM+HD1:"<<heeps_isolEMHadDepth1->at(e2_index)<<",trkiso:"<<heeps_IsolPtTrks->at(e2_index)<<",ECALDriven:"<<heeps_EcalDriven->at(e2_index)<<",detain:"<<heeps_dEtaIn->at(e2_index)<<std::endl;
//### for L1 Et check #################
h_L1Et->Fill(e1_L1_Et,event_weight);
h_L1Et->Fill(e2_L1_Et,event_weight);

h_rho    ->Fill(rho     ,event_weight);
h_pv_n   ->Fill(pv_n    ,event_weight);

if(e1_et>e2_et){
h_led_Et_AM ->Fill(e1.Pt() ,event_weight);
h_led_eta_AM->Fill(e1.Eta(),event_weight);
h_led_phi_AM->Fill(e1.Phi(),event_weight);
h_sub_Et_AM ->Fill(e2.Pt() ,event_weight);
h_sub_eta_AM->Fill(e2.Eta(),event_weight);
h_sub_phi_AM->Fill(e2.Phi(),event_weight);
              }
else{
h_led_Et_AM ->Fill(e2.Pt() ,event_weight);
h_led_eta_AM->Fill(e2.Eta(),event_weight);
h_led_phi_AM->Fill(e2.Phi(),event_weight);
h_sub_Et_AM ->Fill(e1.Pt() ,event_weight);
h_sub_eta_AM->Fill(e1.Eta(),event_weight);
h_sub_phi_AM->Fill(e1.Phi(),event_weight);
    }
//####################### for m > 200 ########################################
if(mee<200) continue;
//if(mee<1000) continue;
 
h_Ptll   ->Fill(Zee.Pt() ,event_weight);
h_Etall  ->Fill(Zee.Eta(),event_weight);
h_Phill  ->Fill(Zee.Phi(),event_weight);
if(e1_et>e2_et){
h_led_Et ->Fill(e1.Pt() ,event_weight);
h_led_eta->Fill(e1.Eta(),event_weight);
h_led_phi->Fill(e1.Phi(),event_weight);
h_sub_Et ->Fill(e2.Pt() ,event_weight);
h_sub_eta->Fill(e2.Eta(),event_weight);
h_sub_phi->Fill(e2.Phi(),event_weight);
h_led_Et_v1 ->Fill(e1.Pt() ,event_weight);
h_led_eta_v1->Fill(e1.Eta(),event_weight);
h_led_phi_v1->Fill(e1.Phi(),event_weight);
h_sub_Et_v1 ->Fill(e2.Pt() ,event_weight);
h_sub_eta_v1->Fill(e2.Eta(),event_weight);
h_sub_phi_v1->Fill(e2.Phi(),event_weight);
              }
else{
h_led_Et ->Fill(e2.Pt() ,event_weight);
h_led_eta->Fill(e2.Eta(),event_weight);
h_led_phi->Fill(e2.Phi(),event_weight);
h_sub_Et ->Fill(e1.Pt() ,event_weight);
h_sub_eta->Fill(e1.Eta(),event_weight);
h_sub_phi->Fill(e1.Phi(),event_weight);
h_led_Et_v1 ->Fill(e2.Pt() ,event_weight);
h_led_eta_v1->Fill(e2.Eta(),event_weight);
h_led_phi_v1->Fill(e2.Phi(),event_weight);
h_sub_Et_v1 ->Fill(e1.Pt() ,event_weight);
h_sub_eta_v1->Fill(e1.Eta(),event_weight);
h_sub_phi_v1->Fill(e1.Phi(),event_weight);
    }
float Dphi_ll   =(fabs(e1.Phi()-e2.Phi())<PI_F) ? fabs(e1.Phi()-e2.Phi()) : (2*PI_F-fabs(e1.Phi()-e2.Phi())) ;
float Dphi_MET_Z=(fabs(MET_T1Txy_phi-Zee.Phi())<PI_F) ? fabs(MET_T1Txy_phi-Zee.Phi()) : (2*PI_F-fabs(MET_T1Txy_phi-Zee.Phi())) ; 
h_MET           ->Fill(Met_et                ,event_weight); 
h_MET_phi       ->Fill(Met_phi               ,event_weight); 
h_MET_T1Txy     ->Fill(MET_T1Txy_et          ,event_weight); 
h_MET_phi_T1Txy ->Fill(MET_T1Txy_phi         ,event_weight); 
h_MET_SF_T1Txy  ->Fill(MET_T1Txy_significance,event_weight); 
h_MET_Filter    ->Fill(MET_Filter            ,event_weight); 
h_Dphi_ll       ->Fill(Dphi_ll               ,event_weight); 
h_Dphi_MET_Z    ->Fill(Dphi_MET_Z            ,event_weight); 
h_DR_ll         ->Fill(e1.DeltaR(e2)         ,event_weight);
/*
//////////////////////// Jet ////////////////
TLorentzVector tmp_p4(0,0,0,0);
TLorentzVector sum_p4(0,0,0,0);
float HT_sys=0;
int Num_loose_jet=0;
int Num_b_jet=0;
for(unsigned int ij=0;ij<jets_pt->size();ij++){
tmp_p4.SetPtEtaPhiM(jets_pt->at(ij), jets_eta->at(ij), jets_phi->at(ij), jets_mass->at(ij));
if(tmp_p4.DeltaR(e1)<0.4 || tmp_p4.DeltaR(e2)<0.4) continue;
if(fabs(jets_eta->at(ij))<2.4 && jets_pt->at(ij) > 30 && jets_loose_ID->at(ij)==1) {Num_loose_jet++;
                                                                                    HT_sys=HT_sys+jets_pt->at(ij);
                                                                                    sum_p4=sum_p4+tmp_p4;
                                                                                   }
if(fabs(jets_eta->at(ij))<2.4 && jets_pt->at(ij) > 30 && jets_loose_ID->at(ij)==1 && jets_CSV->at(ij)>0.8484) Num_b_jet++;
}
HT_sys=HT_sys+e1.Pt()+e2.Pt();
sum_p4=sum_p4+e1+e2;
////////////////////////////////////////////
h_N_jet     ->Fill(Num_loose_jet         ,event_weight); 
h_N_bjet    ->Fill(Num_b_jet             ,event_weight); 
h_HT_sys    ->Fill(HT_sys                ,event_weight); 
h_Pt_sys    ->Fill(sum_p4.Pt()           ,event_weight); 
*/
}// Fill histrogram


}// Entry
fout << flush;
fout.close();
//f_add_out << flush;
//f_add_out.close();
//fout_MET << flush;
//fout_MET.close();
//fout_match << flush;
//fout_match.close();
////////////////// Save histogram /////////////////////////////////////
Remove_negative_events( h_mee_all       );
Remove_negative_events( h_mee_all_BB    );
Remove_negative_events( h_mee_all_BE    );
Remove_negative_events( h_mee_all_EE    );
Remove_negative_events( h_mee_all_SS    );  
Remove_negative_events( h_mee_all_BB_SS ); 
Remove_negative_events( h_mee_all_BE_SS ); 
Remove_negative_events( h_mee_all_EE_SS ); 
Remove_negative_events( h_mee_all_sin   );
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
Remove_negative_events( h_mee_Zpeak_BE  );
Remove_negative_events( h_mee_Zpeak_EE  );
Remove_negative_events( h_mee_Zpeak_EE_pp);
Remove_negative_events( h_mee_Zpeak_EE_pm);
Remove_negative_events( h_mee_Zpeak_EE_mm);
Remove_negative_events( h_mee_Zpeak_EE_Heta);
Remove_negative_events( h_mee_Zpeak_EE_Leta);
Remove_negative_events( h_mee_Zpeak_EE_HLeta);
Remove_negative_events( h_mee_Zpeak_v1     );
Remove_negative_events( h_mee_Zpeak_BB_v1  );
Remove_negative_events( h_mee_Zpeak_BE_v1  );
Remove_negative_events( h_mee_Zpeak_EE_v1  );
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

Remove_negative_events( h_cos_all_region); 
Remove_negative_events( h_cos           ); 
Remove_negative_events( h_cos_BB        ); 
Remove_negative_events( h_cos_BE        ); 
Remove_negative_events( h_cos_EE        ); 

Remove_negative_events( h_mee_fail_MET  );
Remove_negative_events( h_pv_n          );
Remove_negative_events( h_rho           );
Remove_negative_events( h_rho_BB        );
Remove_negative_events( h_rho_BE        );
Remove_negative_events( h_rho_EE        );
Remove_negative_events( h_Ptll          );
Remove_negative_events( h_Etall         );
Remove_negative_events( h_Phill         );
Remove_negative_events( h_led_Et        );
Remove_negative_events( h_led_eta       );
Remove_negative_events( h_led_phi       );
Remove_negative_events( h_sub_Et        );
Remove_negative_events( h_sub_eta       );
Remove_negative_events( h_sub_phi       );
Remove_negative_events( h_led_Et_v1        );
Remove_negative_events( h_led_eta_v1       );
Remove_negative_events( h_led_phi_v1       );
Remove_negative_events( h_sub_Et_v1        );
Remove_negative_events( h_sub_eta_v1       );
Remove_negative_events( h_sub_phi_v1       );
Remove_negative_events( h_led_Et_AM     );
Remove_negative_events( h_led_eta_AM    );
Remove_negative_events( h_led_phi_AM    );
Remove_negative_events( h_sub_Et_AM     );
Remove_negative_events( h_sub_eta_AM    );
Remove_negative_events( h_sub_phi_AM    );
Remove_negative_events( h_dPhiIn         );
Remove_negative_events( h_Sieie          );
Remove_negative_events( h_missingHits    );
Remove_negative_events( h_dxyFirstPV     );
Remove_negative_events( h_HOverE         );
Remove_negative_events( h_E1x5OverE5x5   );
Remove_negative_events( h_E2x5OverE5x5   );
Remove_negative_events( h_isolEMHadDepth1);
Remove_negative_events( h_IsolPtTrks     );
Remove_negative_events( h_EcalDriven     );
Remove_negative_events( h_dEtaIn         );

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
Remove_negative_events( h_MET_Filter_detail    );

Remove_negative_events( h_L1Et           ); 
Remove_negative_events( h_L1Et_BB        ); 
Remove_negative_events( h_L1Et_BE        ); 

TFile *f = new TFile(output_file,"RECREATE");
f->cd();

h_mee_all       ->Write();
h_mee_all_BB    ->Write();
h_mee_all_BE    ->Write();
h_mee_all_EE    ->Write();
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
h_mee_Zpeak_BE  ->Write();
h_mee_Zpeak_EE  ->Write();
h_mee_Zpeak_EE_pp->Write();
h_mee_Zpeak_EE_pm->Write();
h_mee_Zpeak_EE_mm->Write();
h_mee_Zpeak_EE_Heta  ->Write();
h_mee_Zpeak_EE_Leta  ->Write();
h_mee_Zpeak_EE_HLeta ->Write();
h_mee_Zpeak_v1     ->Write();
h_mee_Zpeak_BB_v1  ->Write();
h_mee_Zpeak_BE_v1  ->Write();
h_mee_Zpeak_EE_v1  ->Write();
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
h_cos_all_region->Write(); 
h_cos           ->Write(); 
h_cos_BB        ->Write(); 
h_cos_BE        ->Write(); 
h_cos_EE        ->Write(); 
h_led_Et_Mee_BB ->Write(); 
h_led_E_Mee_BB  ->Write(); 
h_led_Et_Mee_EE ->Write(); 
h_led_E_Mee_EE  ->Write(); 
h_endcap_Et_Mee_BE->Write();
h_endcap_E_Mee_BE ->Write();
h_endcap_eta_Mee_BE->Write(); 
h_float_eta_Mee_BB ->Write(); 
h_limit_eta_Mee_BB ->Write(); 
h_resolution       ->Write(); 
h_resolution_BB    ->Write(); 
h_resolution_BE    ->Write(); 
h_pass_L1_BB       ->Write(); 
h_pass_L1_BE       ->Write(); 
h_pass_L1_EE       ->Write(); 
h_diff_et_barrel   ->Write(); 
h_diff_et_endcap   ->Write(); 
h_N_saturated_BB   ->Write(); 
h_N_saturated_BE   ->Write(); 


h_mee_fail_MET  ->Write();
h_pv_n          ->Write();
h_rho           ->Write();
h_rho_BB        ->Write();
h_rho_BE        ->Write();
h_rho_EE        ->Write();
h_Ptll          ->Write();
h_Etall         ->Write();
h_Phill         ->Write();
h_led_Et        ->Write();
h_led_eta       ->Write();
h_led_phi       ->Write();
h_sub_Et        ->Write();
h_sub_eta       ->Write();
h_sub_phi       ->Write();
h_led_Et_v1        ->Write();
h_led_eta_v1       ->Write();
h_led_phi_v1       ->Write();
h_sub_Et_v1        ->Write();
h_sub_eta_v1       ->Write();
h_sub_phi_v1       ->Write();
h_led_Et_AM     ->Write();
h_led_eta_AM    ->Write();
h_led_phi_AM    ->Write();
h_sub_Et_AM     ->Write();
h_sub_eta_AM    ->Write();
h_sub_phi_AM    ->Write();
h_dPhiIn         ->Write(); 
h_Sieie          ->Write(); 
h_missingHits    ->Write(); 
h_dxyFirstPV     ->Write(); 
h_HOverE         ->Write(); 
h_E1x5OverE5x5   ->Write(); 
h_E2x5OverE5x5   ->Write(); 
h_isolEMHadDepth1->Write(); 
h_IsolPtTrks     ->Write(); 
h_EcalDriven     ->Write(); 
h_dEtaIn         ->Write(); 

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

h_L1Et     ->Write();
h_L1Et_BB  ->Write();
h_L1Et_BE  ->Write();

f->Close();
//f_NNPDF->Close();//can't do Close here, otherwise will give an error 
h_mee_all       ->Delete();
h_mee_all_BB    ->Delete();
h_mee_all_BE    ->Delete();
h_mee_all_EE    ->Delete();
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
h_mee_Zpeak_BE  ->Delete();
h_mee_Zpeak_EE  ->Delete();
h_mee_Zpeak_EE_pp->Delete();
h_mee_Zpeak_EE_pm->Delete();
h_mee_Zpeak_EE_mm->Delete();
h_mee_Zpeak_EE_Heta  ->Delete();
h_mee_Zpeak_EE_Leta  ->Delete();
h_mee_Zpeak_EE_HLeta ->Delete();
h_mee_Zpeak_v1     ->Delete();
h_mee_Zpeak_BB_v1  ->Delete();
h_mee_Zpeak_BE_v1  ->Delete();
h_mee_Zpeak_EE_v1  ->Delete();
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
h_cos_all_region->Delete(); 
h_cos           ->Delete(); 
h_cos_BB        ->Delete(); 
h_cos_BE        ->Delete(); 
h_cos_EE        ->Delete(); 
h_led_Et_Mee_BB ->Delete(); 
h_led_E_Mee_BB  ->Delete(); 
h_led_Et_Mee_EE ->Delete(); 
h_led_E_Mee_EE  ->Delete(); 
h_endcap_Et_Mee_BE->Delete();
h_endcap_E_Mee_BE ->Delete();
h_endcap_eta_Mee_BE->Delete(); 
h_float_eta_Mee_BB ->Delete(); 
h_limit_eta_Mee_BB ->Delete(); 
h_resolution       ->Delete(); 
h_resolution_BB    ->Delete(); 
h_resolution_BE    ->Delete(); 
h_pass_L1_BB       ->Delete(); 
h_pass_L1_BE       ->Delete(); 
h_pass_L1_EE       ->Delete(); 
h_diff_et_barrel   ->Delete(); 
h_diff_et_endcap   ->Delete(); 
h_N_saturated_BB   ->Delete(); 
h_N_saturated_BE   ->Delete(); 


h_mee_fail_MET  ->Delete();
h_pv_n          ->Delete();
h_rho           ->Delete();
h_rho_BB        ->Delete();
h_rho_BE        ->Delete();
h_rho_EE        ->Delete();
h_Ptll          ->Delete();
h_Etall         ->Delete();
h_Phill         ->Delete();
h_led_Et        ->Delete();
h_led_eta       ->Delete();
h_led_phi       ->Delete();
h_sub_Et        ->Delete();
h_sub_eta       ->Delete();
h_sub_phi       ->Delete();
h_led_Et_v1        ->Delete();
h_led_eta_v1       ->Delete();
h_led_phi_v1       ->Delete();
h_sub_Et_v1        ->Delete();
h_sub_eta_v1       ->Delete();
h_sub_phi_v1       ->Delete();
h_led_Et_AM     ->Delete();
h_led_eta_AM    ->Delete();
h_led_phi_AM    ->Delete();
h_sub_Et_AM     ->Delete();
h_sub_eta_AM    ->Delete();
h_sub_phi_AM    ->Delete();
h_dPhiIn         ->Delete(); 
h_Sieie          ->Delete(); 
h_missingHits    ->Delete(); 
h_dxyFirstPV     ->Delete(); 
h_HOverE         ->Delete(); 
h_E1x5OverE5x5   ->Delete(); 
h_E2x5OverE5x5   ->Delete(); 
h_isolEMHadDepth1->Delete(); 
h_IsolPtTrks     ->Delete(); 
h_EcalDriven     ->Delete(); 
h_dEtaIn         ->Delete(); 


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

h_L1Et      ->Delete(); 
h_L1Et_BB   ->Delete(); 
h_L1Et_BE   ->Delete(); 

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

int L1_trigger_match_s(float eta, float phi, vector<float> *filter_eta, vector<float> *filter_phi, vector<float> *filter_et){
TLorentzVector tmp1;
TLorentzVector tmp2;
tmp1.SetPtEtaPhiM(1,eta,phi,0);
for(unsigned int i=0;i<filter_eta->size();i++){
tmp2.SetPtEtaPhiM(1,filter_eta->at(i),filter_phi->at(i),0);
if(tmp2.DeltaR(tmp1)<L1_DeltaR){if(filter_et->at(i)>=SingleL1_threshold) return 1;}
}
return 0;
}

float L1_trigger_match_Et(float eta, float phi, vector<float> *filter_eta, vector<float> *filter_phi, vector<float> *filter_et){
TLorentzVector tmp1;
TLorentzVector tmp2;
tmp1.SetPtEtaPhiM(1,eta,phi,0);
for(unsigned int i=0;i<filter_eta->size();i++){
tmp2.SetPtEtaPhiM(1,filter_eta->at(i),filter_phi->at(i),0);
if(tmp2.DeltaR(tmp1)<L1_DeltaR){ return filter_et->at(i);}
}
return -1;
}

int L1_trigger_match(float eta, float phi, vector<float> *filter_eta, vector<float> *filter_phi, vector<float> *filter_et,int runnr, int lumisec ){
TLorentzVector tmp1;
TLorentzVector tmp2;
tmp1.SetPtEtaPhiM(1,eta,phi,0);
for(unsigned int i=0;i<filter_eta->size();i++){
tmp2.SetPtEtaPhiM(1,filter_eta->at(i),filter_phi->at(i),0);
//std::cout<<"ele_eta="<<eta<<",ele_phi="<<phi<<",L1_eta="<<filter_eta->at(i)<<",L1_phi="<<filter_phi->at(i)<<",L1_et="<<filter_et->at(i)<<", run="<<runnr<<", LS="<<lumisec<<", L1 threshold="<<float(getLowestSingleL1EG(runnr,lumisec))<<std::endl;
if(tmp2.DeltaR(tmp1)<L1_DeltaR){if(filter_et->at(i)>=float(getLowestSingleL1EG(runnr,lumisec))) return 1;}
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
if(Year=="2016"){
if(uncert=="Barrel_SF_scale_up"){if(fabs(eta)<1.4442){if(Et<90)weight=1.01;
                                                      else if(Et<1000)weight=1+(0.00802+2.198e-5*Et);
                                                      else weight=1.03;
                                                     }
                                }
else if(uncert=="Barrel_SF_scale_down"){if(fabs(eta)<1.4442){if(Et<90)weight=0.99;
                                                      else if(Et<1000)weight=1-(0.00802+2.198e-5*Et);
                                                      else weight=0.97;
                                                     }
                                }
else if(uncert=="Endcap_SF_scale_up"){if(fabs(eta)>1.566 && fabs(eta)<2.5){if(Et<90)weight=1.01;
                                                      else if(Et<300)weight=1+(-0.00286+1.4e-4*Et);
                                                      else weight=1.04;
                                                     }
                                }
else if(uncert=="Endcap_SF_scale_down"){if(fabs(eta)>1.566 && fabs(eta)<2.5){if(Et<90)weight=0.99;
                                                      else if(Et<300)weight=1-(-0.00286+1.4e-4*Et);
                                                      else weight=0.96;
                                                     }
                                }
}
else{
if(uncert=="Barrel_SF_scale_up"){if(fabs(eta)<1.4442){if(Et<90)weight=1.01;
                                                      else if(Et<500)weight=0.99561+4.878e-5*Et;
                                                      else weight=1.03;
                                                     }
                                }
else if(uncert=="Barrel_SF_scale_down"){if(fabs(eta)<1.4442){if(Et<90)weight=0.99;
                                                      else if(Et<500)weight=0.9944-4.878e-5*Et;
                                                      else weight=0.97;
                                                     }
                                }
else if(uncert=="Endcap_SF_scale_up"){if(fabs(eta)>1.566 && fabs(eta)<2.5){if(Et<90)weight=1.02;
                                                      else if(Et<300)weight=1.007143+1.4286e-4*Et;
                                                      else weight=1.05;
                                                     }
                                }
else if(uncert=="Endcap_SF_scale_down"){if(fabs(eta)>1.566 && fabs(eta)<2.5){if(Et<90)weight=0.98;
                                                      else if(Et<300)weight=0.99286-1.4286e-4*Et;
                                                      else weight=0.95;
                                                     }
                                }
}//else
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

float scale_factor( TH2F* h, float pt, float eta , TString uncert){
int NbinsX=h->GetXaxis()->GetNbins();
int NbinsY=h->GetYaxis()->GetNbins();
float x_min=h->GetXaxis()->GetBinLowEdge(1);
float x_max=h->GetXaxis()->GetBinLowEdge(NbinsX)+h->GetXaxis()->GetBinWidth(NbinsX);
float y_min=h->GetYaxis()->GetBinLowEdge(1);
float y_max=h->GetYaxis()->GetBinLowEdge(NbinsY)+h->GetYaxis()->GetBinWidth(NbinsY);
TAxis *Xaxis = h->GetXaxis();
TAxis *Yaxis = h->GetYaxis();
Int_t binx=1;
Int_t biny=1;
if(x_min < eta && eta < x_max) binx = Xaxis->FindBin(eta);
else binx= (eta<=x_min) ? 1 : NbinsX ;
if(y_min < pt && pt < y_max) biny = Yaxis->FindBin(pt);
else biny= (pt<=y_min) ? 1 : NbinsY ;
//std::cout<<"pt="<<pt<<",eta="<<eta<<",xmin="<<x_min<<",xmax="<<x_max<<",ymin="<<y_min<<",ymax="<<y_max<<",sf="<<h->GetBinContent(binx, biny)<<std::endl;
     if(uncert=="EleSFReco_up"   )return (h->GetBinContent(binx, biny)+h->GetBinError(binx, biny));
else if(uncert=="EleSFReco_down" )return (h->GetBinContent(binx, biny)-h->GetBinError(binx, biny));
else                              return  h->GetBinContent(binx, biny);
}
