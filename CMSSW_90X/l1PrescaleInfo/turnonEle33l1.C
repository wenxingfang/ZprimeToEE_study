#include "TMath.h"
#include "TRandom3.h"

namespace trigEle33l1{


  TRandom3 randNrGen;
  float turnOnfunction(float Et, float p0, float p1, float p2, float p3, float p4, float p5){
    float eff = 0.0;
    eff = 0.5*p0*(1+erf((Et-p1)/(1.414*p2)))+0.5*p3*(1+erf((Et-p4)/(1.414*p5)));
    return eff;
  }
  
  float turnOn_MW(float scEt,float scEta, TString data, bool isScaled_sc_Et){
    if(isScaled_sc_Et==false){
    if(data=="Rereco_all"){
    if (0.0<=fabs(scEta) && fabs(scEta)<=1.4442)
      return turnOnfunction(scEt,0.862, 35.4, 3.43, 0.615, 168, 111);
    else if (1.556<=fabs(scEta) && fabs(scEta)<=2.5)
      return turnOnfunction(scEt,0.832, 35.7, 4.21, 0.125, 40.1, 8.93);
    else
      return 0.0;
  }
  else if(data=="Rereco_B"){
    if (0.0<=fabs(scEta) && fabs(scEta)<=1.4442)
      return turnOnfunction(scEt,0.775, 34.5, 2.62, 0.225, 0.00441, 51.3);
    else if (1.556<=fabs(scEta) && fabs(scEta)<=2.5)
      return turnOnfunction(scEt,0.0386, 36, 0.368, 0.917, 34.4, 4);
    else
      return 0.0;
  }
  else if(data=="Rereco_C"){
    if (0.0<=fabs(scEta) && fabs(scEta)<=1.4442)
      return turnOnfunction(scEt,0.894, 34.2, 2.87, 0.434, 125, 64);
    else if (1.556<=fabs(scEta) && fabs(scEta)<=2.5)
      return turnOnfunction(scEt,0.943, 35, 3.74, 0.0148, 50.1, 3.05);
    else
      return 0.0;
  }
  else if(data=="Rereco_D"){
    if (0.0<=fabs(scEta) && fabs(scEta)<=1.4442)
      return turnOnfunction(scEt,0.914, 33.9, 2.87, 0.395, 119, 53.4);
    else if (1.556<=fabs(scEta) && fabs(scEta)<=2.5)
      return turnOnfunction(scEt,0.946, 34.8, 3.64, 0.287, 83.7, 16.2);
    else
      return 0.0;
  }
  else if(data=="Rereco_E"){
    if (0.0<=fabs(scEta) && fabs(scEta)<=1.4442)
      return turnOnfunction(scEt,0.93, 35.7, 3.59, 0.477, 105, 30.8);
    else if (1.556<=fabs(scEta) && fabs(scEta)<=2.5)
      return turnOnfunction(scEt,0.556, 36.2, 3.41, 0.397, 38.1, 6.82);
    else
      return 0.0;
  }
  else if(data=="Rereco_F"){
    if (0.0<=fabs(scEta) && fabs(scEta)<=1.4442)
      return turnOnfunction(scEt,0.835, 37.2, 3.1, 0.765, 222, 164);
    else if (1.556<=fabs(scEta) && fabs(scEta)<=2.5)
      return turnOnfunction(scEt,0.92, 37.8, 4.81, 10.3, 121, 22.6);
    else
      return 0.0;
  }
  else return 0;
  }//if false
  else{
    if(data=="Rereco_all"){
    if (0.0<=fabs(scEta) && fabs(scEta)<=1.4442)
      return turnOnfunction(scEt,0.765, 35.1, 3.4, 0.525, 108, 153);
    else if (1.556<=fabs(scEta) && fabs(scEta)<=2.5)
      return turnOnfunction(scEt,0.841, 35.6, 4.33, 0.114, 40.0, 8.35);
    else
      return 0.0;
    }
    else return 0;
  }
  }//turnOn_MW
  
  bool passTrig(float scEt,float scEta, TString data, bool sc_et_scaled){return turnOn_MW(scEt,scEta, data, sc_et_scaled)>randNrGen.Uniform(0,1);}

}
  
