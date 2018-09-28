#ifndef DIELESCALEFACTORS_ELE27WPLOOSETRIGTURN_C
#define DIELESCALEFACTORS_ELE27WPLOOSETRIGTURN_C

#include "TMath.h"
#include "TRandom3.h"

namespace trigEle33{


  TRandom3 randNrGen;
  float turnOnfunction(float Et, float p0, float p1, float p2, float p3, float p4, float p5){
    float eff = 0.0;
    eff = 0.5*p0*(1+erf((Et-p1)/(1.414*p2)))+0.5*p3*(1+erf((Et-p4)/(1.414*p5)));
    return eff;
  }
/*  
  float turnOn(float scEt,float scEta){
    if (0.0<=fabs(scEta) && fabs(scEta)<0.79)
      return turnOnfunction(scEt,0.146, 32.425, 1.534, 0.834, 32.583, 0.547);
    else if (0.79<=fabs(scEta) && fabs(scEta)<1.1)
      return turnOnfunction(scEt,0.130, 32.844, 1.686, 0.854, 32.759, 0.670);
    else if (1.1<=fabs(scEta) && fabs(scEta)<1.4442)
      return turnOnfunction(scEt,0.287, 32.820, 1.361, 0.702, 32.887, 0.631);
    else if (1.566<=fabs(scEta) && fabs(scEta)<1.70)
      return turnOnfunction(scEt,0.074, 31.730, 4.372, 0.919, 32.530, 0.853);
    else if (1.70<=fabs(scEta) && fabs(scEta)<2.1)
      return turnOnfunction(scEt,0.221, 32.816, 1.889, 0.776, 32.729, 0.805);
    else if (2.1<=fabs(scEta) && fabs(scEta)<2.5)
      return turnOnfunction(scEt,0.541, 33.711, 1.571, 0.456, 33.523, 0.876);
    else
      return -1.0;
  }
*/
  float turnOn(float scEt,float scEta){
    if (0.0<=fabs(scEta) && fabs(scEta)<0.79)
      return turnOnfunction(scEt,0.9054, 33.71, 0.4502, 0.07426, 34.04, 1.791);
    else if (0.79<=fabs(scEta) && fabs(scEta)<1.1)
      return turnOnfunction(scEt,0.8727, 33.81, 0.5074, 0.1111, 33.99, 1.924);
    else if (1.1<=fabs(scEta) && fabs(scEta)<1.4442)
      return turnOnfunction(scEt,0.8573, 33.96, 0.6658, 0.128, 33.85, 2.043);
    else if (1.566<=fabs(scEta) && fabs(scEta)<1.70)
      return turnOnfunction(scEt,0.8539, 33.58, 0.7439, 0.1341, 33.57, 2.659);
    else if (1.70<=fabs(scEta) && fabs(scEta)<2.1)
      return turnOnfunction(scEt,0.6968, 33.68, 0.6542, 0.2913, 34.1, 1.611);
    else if (2.1<=fabs(scEta) && fabs(scEta)<2.5)
      return turnOnfunction(scEt,0.6204, 34.15, 0.927, 0.3651, 35.44, 1.99);
    else
      return -1.0;
  }
  float turnOn_MW(float scEt,float scEta){
    if (0.0<=fabs(scEta) && fabs(scEta)<0.79)
      return turnOnfunction(scEt,0.103, 32.535, 1.923, 0.890, 32.642, 0.640);
    else if (0.79<=fabs(scEta) && fabs(scEta)<1.1)
      return turnOnfunction(scEt,0.177, 32.936, 1.655, 0.818, 32.829, 0.685);
    else if (1.1<=fabs(scEta) && fabs(scEta)<1.4442)
      return turnOnfunction(scEt,0.220, 32.968, 1.542, 0.774, 32.954, 0.732);
    else if (1.566<=fabs(scEta) && fabs(scEta)<1.70)
      return turnOnfunction(scEt,0.086, 31.774, 4.446, 0.906, 32.675, 0.931);
    else if (1.70<=fabs(scEta) && fabs(scEta)<2.1)
      return turnOnfunction(scEt,0.801, 32.985, 1.009, 0.193, 33.412, 2.040);
    else if (2.1<=fabs(scEta) && fabs(scEta)<2.5)
      return turnOnfunction(scEt,0.491, 34.609, 1.889, 0.505, 33.979, 1.161);
    else
      return -1.0;
  }
  
  //bool passTrig(float scEt,float scEta){return (11.021/36.459)*turnOn(scEt,scEta)+(25.438/36.459)*turnOn_MW(scEt,scEta)>randNrGen.Uniform(0,1);}
  bool passTrig(float scEt,float scEta){return turnOn(scEt,scEta)>randNrGen.Uniform(0,1);}

}
  


#endif
