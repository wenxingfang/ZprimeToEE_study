#ifndef DIELESCALEFACTORS_ELE27WPLOOSETRIGTURN_C
#define DIELESCALEFACTORS_ELE27WPLOOSETRIGTURN_C

#include "TMath.h"
#include <iostream>
#include "TString.h"
#include "TRandom3.h"

namespace trigEle33{


  TRandom3 randNrGen;
  float turnOnfunction(float Et, float p0, float p1, float p2, float p3, float p4, float p5){
    float eff = 0.0;
    eff = 0.5*p0*(1+erf((Et-p1)/(1.414*p2)))+0.5*p3*(1+erf((Et-p4)/(1.414*p5)));
    return eff;
  }
  float turnOn_MW(float scEt,float scEta, TString run){
    if(run=="Rereco_B"){
    if (0.0<=fabs(scEta) && fabs(scEta)<0.79)
      return turnOnfunction(scEt,0.8412, 33.78, 0.4251, 0.115, 34.89, 2.151);//rereco all
    else if (0.79<=fabs(scEta) && fabs(scEta)<1.1)
      return turnOnfunction(scEt,0.8147, 33.9, 0.4882, 0.1466, 34.87, 2.191);//rereco all
    else if (1.1<=fabs(scEta) && fabs(scEta)<1.4442)
      return turnOnfunction(scEt,0.8457, 34.11, 0.6876, 0.1337, 34.42, 2.475);//rereco all
    else if (1.566<=fabs(scEta) && fabs(scEta)<1.70)
      return turnOnfunction(scEt,0.6784, 34.02, 0.926, 0.3102, 33.5, 2.092);//rereco all
    else if (1.70<=fabs(scEta) && fabs(scEta)<2.1)
      return turnOnfunction(scEt,0.6402, 34.32, 0.7727, 0.3287, 34.87, 2.039);//rereco all
    else if (2.1<=fabs(scEta) && fabs(scEta)<2.5)
      return turnOnfunction(scEt,0.8073, 35.25, 1.172, 0.1491, 39.66, 1.604);//rereco all
    else
      return -1.0;
    }
    else if(run=="Rereco_C"){
    if (0.0<=fabs(scEta) && fabs(scEta)<0.79)
      return turnOnfunction(scEt,0.8847, 33.85, 0.4371, 0.1003, 34.51, 2.02);//rereco all
    else if (0.79<=fabs(scEta) && fabs(scEta)<1.1)
      return turnOnfunction(scEt,0.8701, 34.01, 0.5326, 0.1186, 34.56, 2.209);//rereco all
    else if (1.1<=fabs(scEta) && fabs(scEta)<1.4442)
      return turnOnfunction(scEt,0.9097, 34.3, 0.7043, 0.0812, 33.97, 2.595);//rereco all
    else if (1.566<=fabs(scEta) && fabs(scEta)<1.70)
      return turnOnfunction(scEt,0.9027, 33.77, 0.788, 0.092, 34.31, 2.915);//rereco all
    else if (1.70<=fabs(scEta) && fabs(scEta)<2.1)
      return turnOnfunction(scEt,0.8214, 34.2, 0.8137, 0.1746, 34.54, 1.934);//rereco all
    else if (2.1<=fabs(scEta) && fabs(scEta)<2.5)
      return turnOnfunction(scEt,0.9192, 34.57, 1.314, 0.07611, 37.66, 1.08);//rereco all
    else
      return -1.0;
    }
    else if(run=="Rereco_D"){
    if (0.0<=fabs(scEta) && fabs(scEta)<0.79)
      return turnOnfunction(scEt,0.9124, 33.84, 0.3908, 0.06999, 34.77, 2.501);//rereco all
    else if (0.79<=fabs(scEta) && fabs(scEta)<1.1)
      return turnOnfunction(scEt,0.837, 34.02, 0.6225, 0.1464, 33.87, 0.009738);//rereco all
    else if (1.1<=fabs(scEta) && fabs(scEta)<1.4442)
      return turnOnfunction(scEt,0.9189, 34.32, 0.6685, 0.06196, 33.49, 2.52);//rereco all
    else if (1.566<=fabs(scEta) && fabs(scEta)<1.70)
      return turnOnfunction(scEt,0.8676, 33.82, 0.6439, 0.1096, 34.23, 2.722);//rereco all
    else if (1.70<=fabs(scEta) && fabs(scEta)<2.1)
      return turnOnfunction(scEt,0.8802, 34.11, 0.6133, 0.1068, 34.48, 2.036);//rereco all
    else if (2.1<=fabs(scEta) && fabs(scEta)<2.5)
      return turnOnfunction(scEt,0.8867, 34.23, 0.9265, 0.1007, 35.04, 2.382);//rereco all
    else
      return -1.0;
    }
    else if(run=="Rereco_E"){
    if (0.0<=fabs(scEta) && fabs(scEta)<0.79)
      return turnOnfunction(scEt,0.845, 34.07, 0.4258, 0.1341, 35.24, 2.032);//rereco all
    else if (0.79<=fabs(scEta) && fabs(scEta)<1.1)
      return turnOnfunction(scEt,0.8963, 34.27, 0.5536, 0.08795, 35.11, 2.709);//rereco all
    else if (1.1<=fabs(scEta) && fabs(scEta)<1.4442)
      return turnOnfunction(scEt,0.8835, 34.7, 0.6991, 0.09436, 34.43, 2.414);//rereco all
    else if (1.566<=fabs(scEta) && fabs(scEta)<1.70)
      return turnOnfunction(scEt,0.7445, 34.11, 0.6534, 0.2244, 34.75, 2.109);//rereco all
    else if (1.70<=fabs(scEta) && fabs(scEta)<2.1)
      return turnOnfunction(scEt,0.7018, 34.52, 0.6805, 0.2802, 35.14, 1.649);//rereco all
    else if (2.1<=fabs(scEta) && fabs(scEta)<2.5)
      return turnOnfunction(scEt,0.4691, 34.45, 0.7297, 0.5083, 35.56, 1.756);//rereco all
    else
      return -1.0;
    }
    else if(run=="Rereco_F"){
    if (0.0<=fabs(scEta) && fabs(scEta)<0.79)
      return turnOnfunction(scEt,0.95, 34.21, 0.629, -8.418e4, -25.96, -6.682);//rereco all
    else if (0.79<=fabs(scEta) && fabs(scEta)<1.1)
      return turnOnfunction(scEt,0.9523, 34.33, 0.7422, 0.2658, -32.72, -1.049);//rereco all
    else if (1.1<=fabs(scEta) && fabs(scEta)<1.4442)
      return turnOnfunction(scEt,0.925, 34.69, 0.8889, 0.3132, 79.43, 25.85);//rereco all
    else if (1.566<=fabs(scEta) && fabs(scEta)<1.70)
      return turnOnfunction(scEt,0.5188, 65.71, 15.44, 0.8989, 35.84, 1.44);//rereco all
    else if (1.70<=fabs(scEta) && fabs(scEta)<2.1)
      return turnOnfunction(scEt,0.5039, 35.77, 1.198, 0.4509, 36.52, 1.986);//rereco all
    else if (2.1<=fabs(scEta) && fabs(scEta)<2.5)
      return turnOnfunction(scEt,0.8513, 37.35, 2.156, 0.09232, 35.44, 0.84);//rereco all
    else
      return -1.0;
    }
    else if(run=="Rereco_all"){
    if (0.0<=fabs(scEta) && fabs(scEta)<0.79)
      return turnOnfunction(scEt,0.8415, 33.96, 0.4561, 0.1291, 35.01, 2.05);//rereco all
    else if (0.79<=fabs(scEta) && fabs(scEta)<1.1)
      return turnOnfunction(scEt,0.8908, 34.14, 0.5844, 0.08305, 34.83, 2.675);//rereco all
    else if (1.1<=fabs(scEta) && fabs(scEta)<1.4442)
      return turnOnfunction(scEt,0.8832, 34.47, 0.7515, 0.09064, 34.29, 2.597);//rereco all
    else if (1.566<=fabs(scEta) && fabs(scEta)<1.70)
      return turnOnfunction(scEt,0.4776, 35.02, 1.989, 0.4916, 33.96, 0.6667);//rereco all
    else if (1.70<=fabs(scEta) && fabs(scEta)<2.1)
      return turnOnfunction(scEt,0.5414, 34.35, 0.7203, 0.4353, 35.51, 1.885);//rereco all
    else if (2.1<=fabs(scEta) && fabs(scEta)<2.5)
      return turnOnfunction(scEt,0.5271, 34.6, 1.013, 0.4449, 36.49, 2.33);//rereco all
    else
      return -1.0;
       }
   else{std::cout<<"wrong run name"<<std::endl;return 1;}
   }
  bool passTrig(float scEt,float scEta, TString run){return turnOn_MW(scEt,scEta,run)>randNrGen.Uniform(0,1);}

}
  


#endif
