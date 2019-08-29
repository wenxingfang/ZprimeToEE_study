#include "TMath.h"
#include "TRandom3.h"

namespace trigEle33l1{


  TRandom3 randNrGen;
  float turnOnfunction(float Et, float p0, float p1, float p2, float p3, float p4, float p5){
    float eff = 0.0;
    eff = 0.5*p0*(1+erf((Et-p1)/(1.414*p2)))+0.5*p3*(1+erf((Et-p4)/(1.414*p5)));
    return eff;
  }
  
  float turnOn_MW(float scEt,float scEta){
    if (0.0<=fabs(scEta) && fabs(scEta)<=1.4442)
      return turnOnfunction(scEt,0.745, 35.3, 3.33, 0.584, 115, 169);
    else if (1.556<=fabs(scEta) && fabs(scEta)<=2.5)
      return turnOnfunction(scEt,0.875, 35.2, 4.45, 0.086, 41.1, 11.5);
    else
      return 0.0;
  }
  
  bool passTrig(float scEt,float scEta){return turnOn_MW(scEt,scEta)>randNrGen.Uniform(0,1);}

}
  
