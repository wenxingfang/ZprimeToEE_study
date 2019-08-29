#include "TMath.h"
#include "TString.h"
#include "TRandom3.h"
#include "TF1.h"

namespace FR_2016{
/*float frFuncData(float et,float eta)
{
   if(std::abs(eta)<1.5){
   if(et<131.564) return
   0.105833+-0.00250361*et+2.25897e-05*et*et+-7.11117e-08*et*et*et;
   else if(et>=131.564 && et<359.267) return
   0.0139092+-0.000103971*et+3.59764e-07*et*et+-4.12752e-10*et*et*et;
   else return 0.00263727+3.3799e-06*et;
   }else if(std::abs(eta)<2.0){
     if(et<121.849) return 0.11723+-0.00129615*et+4.67464e-06*et*et;
     else if(et>=121.849 && et<226.175) return 0.034505+-4.76287e-05*et;
     else return 0.0257885+-9.08954e-06*et;
   }else if(std::abs(eta)<2.5){
     if(et<112.517) return 0.0807503+-0.000341528*et;
     else return 0.0423239;
   }else return 0.;
}
*/
float frFuncData(float et,float eta)
{
   if(std::abs(eta)<1.5){
   if(et<130) return
   0.060668-0.000830144*et+3.17395e-06*et*et;
   else if(et>=130 && et<300.3) return
   0.0235486-0.000239157*et+9.89383e-07*et*et-1.36279e-09*et*et*et;
   else return 0.00266908+4.18481e-06*et;
   }else if(std::abs(eta)<2.0){
     if(et<125) return 0.119317-0.00129805*et+4.73552e-06*et*et;
     else if(et>=125 && et<220) return 0.0388357-6.19859e-05*et;
     else return 0.0278574-9.76733e-06*et;
   }else if(std::abs(eta)<2.5){
     if(et<112.5) return 0.0888971-0.000414238*et;
     else return 0.0447642;
   }else return 0.;
}
}

namespace FR_2017{
/*float frFuncData(float et,float eta)
{
   if(std::abs(eta)<1.5){
   if(et<131.6) return    0.14-0.0029*et+2.56e-05*et*et-8.48e-08*et*et*et;
   else if(et>=131.6 && et<359.3) return    0.02-0.00013*et+3.5e-07*et*et-2.9e-10*et*et*et;
   else return 0.00514+4.73e-07*et;
   }else if(std::abs(eta)<2.0){
     if(et<125) return 0.1012-0.00094*et+3.37e-06*et*et;
     else if(et>=125 && et<226.3) return 0.0488-11.37e-05*et;
     else return 0.0241-1.24e-06*et;
   }else if(std::abs(eta)<2.5){
     if(et<152) return 0.0622-0.00012*et;
     else return 0.0387;
   }else return 0.;
}
*/
float frFuncData(float et,float eta)
{
   if(std::abs(eta)<1.5){
   if(et<130) return    0.130888-0.00262678*et+2.26808e-05*et*et-7.417e-08*et*et*et;
   else if(et>=130 && et<359.3) return    0.0250652-0.000190867*et+6.11255e-07*et*et-6.45971e-10*et*et*et;
   else return 0.00509181+5.8553e-07*et;
   }else if(std::abs(eta)<2.0){
     if(et<125) return 0.0867558-0.000605761*et+1.56754e-06*et*et;
     else if(et>=125 && et<220) return 0.0481578-0.000111123*et;
     else return 0.0243468;
   }else if(std::abs(eta)<2.5){
     if(et<90) return 0.075785-0.000315158*et;
     else if (et>=90 && et<200) return 0.0561002-8.38524e-05*et;
     else return 0.038503;
   }else return 0.;
}
}


namespace FR_2018{

float lumi_before_HEM = 14.976;
float lumi_total      = 53.551;

TRandom3 randNrGen;

float Before_HEM(float et,float eta)
{
   if(std::abs(eta)<1.5){
   if(et<130)        return    2.02017e-06  * et*et -0.000843135 * et + 0.0876231;
   else if(et<359.3) return    -1.341e-09   * et*et*et + 1.11091e-06  * et*et -0.000311271 * et + 0.0358143;
   else              return    2.18947e-07 * et + 0.00598619;
   }else if(std::abs(eta)<2.0){
     if(et<70)       return  -0.00163634 * et + 0.167095;
     else if(et<155) return -0.000340279 * et + 0.0802441;
     else            return 0.026187;
   }else if(std::abs(eta)<2.5){
     if(et<220)       return 1.34086e-06 * et*et -0.00058487 * et + 0.106484;
     else            return 0.0427328;
   }
   else return 0.;
}


float Contain_HEM(float et,float eta, float phi)
{
   if(eta>-3.0 && eta<-1.3 && phi>-1.57 && phi<-0.87){ //for HEM region
//   if(et<120) return    1.73852e-06 * et*et -0.000604569 * et + 0.0727721;
//   else       return    1.33076e-05 * et + 0.0256443;
   if(std::abs(eta)<1.5){
   if(et<97)                      return    -0.000641136 * et + 0.0681215;
   else                           return   0.0084599;
   }else if(std::abs(eta)<2.0){
     if(et<100)                   return -0.000468076 * et + 0.0663296;
     else                         return 0.0210277;
   }else if(std::abs(eta)<2.5){
                                  return 0.0392853;
   }
   else return 0.;
   }
  ///////// out HEM/////////////
   else{
   if(std::abs(eta)<1.5){
   if(et<130)                     return    1.18124e-06 * et*et - 0.000689288 * et + 0.0801178;
   else if(et<359.3)              return   -8.21182e-10 * et*et*et + 7.09363e-07 * et*et - 0.00020855 * et + 0.0268764;
   else                           return    7.65758e-06 * et + 0.00291191;
   }else if(std::abs(eta)<2.0){
     if(et<160)                   return -0.000360437 * et + 0.0831656;
     else                         return 0.0266372;
   }else if(std::abs(eta)<2.5){
     if(et<220)                   return 1.37424e-06* et*et -0.00056355*et + 0.100376;
     else                         return 0.0419409;
   }
   else return 0.;
   }
}


float frFuncData(float Et,float eta, float phi, unsigned long run, bool isData)
{

    if(isData)
    {
        if(run<319077) return Before_HEM(Et, eta);
        else           return Contain_HEM(Et, eta, phi);
    }
    else
    {   if(randNrGen.Uniform(0,1)<(lumi_before_HEM/lumi_total)) return Before_HEM(Et, eta);
        else                                                    return Contain_HEM(Et, eta, phi);
    }

}
}
