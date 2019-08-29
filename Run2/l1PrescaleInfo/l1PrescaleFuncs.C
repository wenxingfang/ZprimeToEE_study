#include "PrescaleProvider.h"
namespace l1ps{
  PrescaleProvider psProvider("/user/wenxing/ST_TW_channel/CMSSW_9_4_0/src/l1PrescaleInfo/hltJsons/triggerData2017");
}

void l1ps_(const std::string& l1Seed,const std::string hltPath,int runnr,int lumiSec)
{
   
  std::cout <<"l1 ps "<<l1ps::psProvider.l1Prescale(l1Seed,runnr,lumiSec)<<std::endl;
  std::cout <<"hlt ps "<<l1ps::psProvider.hltPrescale(hltPath,runnr,lumiSec)<<std::endl;
 

}

int getPhoPS(float et,int runnr,int lumiSec)
{
  std::string pathName;
  if(et>=50 && et<75) pathName="HLT_Photon50_v";
  else if(et>=75 && et<90) pathName="HLT_Photon75_v";
  else if(et>=90 && et<120) pathName="HLT_Photon90_v";
  else if(et>=120 && et<175) pathName="HLT_Photon120_v";
  else if(et>=175) pathName="HLT_Photon175_v";
  
  return l1ps::psProvider.hltPrescale(pathName,runnr,lumiSec);

}

float getLowestSingleL1EG(int runnr,int lumiSec)
{
  std::vector<std::pair<std::string,float> > l1SingleEGSeeds={
    {"L1_SingleEG32",32},
    {"L1_SingleEG34",34},
    {"L1_SingleEG36",36},
    {"L1_SingleEG38",38},
    {"L1_SingleEG40",40},
    {"L1_SingleEG45",45}
  };
  for(auto & l1Seed : l1SingleEGSeeds){
    if(l1ps::psProvider.l1Prescale(l1Seed.first,runnr,lumiSec)==1) return l1Seed.second;
  }
  return -1;



}
