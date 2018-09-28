#ifndef DIELESCALEFACTORS_ELE27WPLOOSETRIGTURN_C
#define DIELESCALEFACTORS_ELE27WPLOOSETRIGTURN_C

#include "TMath.h"
#include <iostream>
#include "TString.h"
#include "TRandom3.h"

namespace trigEle25{


  TRandom3 randNrGen;
  float turnOnfunction(float Et, float p0, float p1, float p2, float p3, float p4, float p5){
    float eff = 0.0;
    eff = 0.5*p0*(1+erf((Et-p1)/(1.414*p2)))+0.5*p3*(1+erf((Et-p4)/(1.414*p5)));
    return eff;
  }
  float turnOn_MW(float scEt,float scEta, TString run){
    if(run=="Rereco_B"){
    if (0.0<=fabs(scEta) && fabs(scEta)<0.79)
      return turnOnfunction(scEt,0.8734, 33.58, 0.4597, 0.08289, 34.62, 2.323);
    else if (0.79<=fabs(scEta) && fabs(scEta)<1.1)
      return turnOnfunction(scEt,0.8363, 33.68, 0.52, 0.1251, 34.64, 2.275);
    else if (1.1<=fabs(scEta) && fabs(scEta)<1.4442)
      return turnOnfunction(scEt,0.1104, 33.92, 2.565, 0.8681, 33.83, 0.7143);
    else if (1.566<=fabs(scEta) && fabs(scEta)<1.70)
      return turnOnfunction(scEt,0.759, 34.41, 0.9982, 0.2302, 33.91, 2.368);
    else if (1.70<=fabs(scEta) && fabs(scEta)<2.1)
      return turnOnfunction(scEt,0.6415, 34.61, 0.7622, 0.3277, 35.18, 2.016);
    else if (2.1<=fabs(scEta) && fabs(scEta)<2.5)
      return turnOnfunction(scEt,0.7947, 35.0, 1.165, 0.16, 39.38, 1.666);
    else
      return -1.0;
    }
    else if(run=="Rereco_C"){
    if (0.0<=fabs(scEta) && fabs(scEta)<0.79)
      return turnOnfunction(scEt,0.8983, 33.68, 0.4539, 0.08661, 34.31, 2.081);
    else if (0.79<=fabs(scEta) && fabs(scEta)<1.1)
      return turnOnfunction(scEt,0.8547, 33.85, 0.5308, 0.134, 34.41, 2.068);
    else if (1.1<=fabs(scEta) && fabs(scEta)<1.4442)
      return turnOnfunction(scEt,0.07665, 33.72, 2.551, 0.9142, 34.14, 0.7229);
    else if (1.566<=fabs(scEta) && fabs(scEta)<1.70)
      return turnOnfunction(scEt,0.9075, 34.17, 0.8147, 0.08738, 34.82, 3.026);
    else if (1.70<=fabs(scEta) && fabs(scEta)<2.1)
      return turnOnfunction(scEt,0.8803,34.49,0.8688, 0.116, 34.85, 2.235);
    else if (2.1<=fabs(scEta) && fabs(scEta)<2.5)
      return turnOnfunction(scEt,0.8673, 34.32, 1.218, 0.1283, 37.06, 1.22);
    else
      return -1.0;
    }
    else if(run=="Rereco_D"){
    if (0.0<=fabs(scEta) && fabs(scEta)<0.79)
      return turnOnfunction(scEt,0.9139, 33.68, 0.4031, 0.06823, 34.65, 2.454);
    else if (0.79<=fabs(scEta) && fabs(scEta)<1.1)
      return turnOnfunction(scEt,1.056, 33.91, 0.5862, -0.07221, 34.5, 0.01876);
    else if (1.1<=fabs(scEta) && fabs(scEta)<1.4442)
      return turnOnfunction(scEt,0.9141,34.21,0.6963,0.06704,33.64,2.526);
    else if (1.566<=fabs(scEta) && fabs(scEta)<1.70)
      return turnOnfunction(scEt,0.8747,34.21,0.7027,0.103,34.68,2.89);
    else if (1.70<=fabs(scEta) && fabs(scEta)<2.1)
      return turnOnfunction(scEt,0.9014,34.37,0.6862,0.08579,34.84,2.284);
    else if (2.1<=fabs(scEta) && fabs(scEta)<2.5)
      return turnOnfunction(scEt,0.8517,34.07,0.8997,0.1356,34.89,2.129);
    else
      return -1.0;
    }
    else if(run=="Rereco_E"){
    if (0.0<=fabs(scEta) && fabs(scEta)<0.79)
      return turnOnfunction(scEt,0.8696, 33.91, 0.4352, 0.1096, 35.12, 2.166);
    else if (0.79<=fabs(scEta) && fabs(scEta)<1.1)
      return turnOnfunction(scEt,0.864, 34.12, 0.5379, 0.12, 35.05, 2.385);
    else if (1.1<=fabs(scEta) && fabs(scEta)<1.4442)
      return turnOnfunction(scEt,0.8829,34.59,0.7185,0.09504,34.37,2.462);
    else if (1.566<=fabs(scEta) && fabs(scEta)<1.70)
      return turnOnfunction(scEt,0.7627, 34.52, 0.6991,0.2064,35.28,2.245);
    else if (1.70<=fabs(scEta) && fabs(scEta)<2.1)
      return turnOnfunction(scEt,0.7458,34.82,0.7367,0.236,35.49,1.759 );
    else if (2.1<=fabs(scEta) && fabs(scEta)<2.5)
      return turnOnfunction(scEt,0.4963,34.27,0.7626,0.4808,35.48,1.797);
    else
      return -1.0;
    }
    else if(run=="Rereco_F"){
    if (0.0<=fabs(scEta) && fabs(scEta)<0.79)
      return turnOnfunction(scEt, 0.9498, 34.23, 0.6193, 0.2754, -40.14, -0.5894);
    else if (0.79<=fabs(scEta) && fabs(scEta)<1.1)
      return turnOnfunction(scEt, 0.8981, 34.35, 0.6632, 0.05487, 34.72, 3.03);
    else if (1.1<=fabs(scEta) && fabs(scEta)<1.4442)
      return turnOnfunction(scEt, 0.9488, 34.75, 1.007, 0.08113, 58.3, 2.783);
    else if (1.566<=fabs(scEta) && fabs(scEta)<1.70)
      return turnOnfunction(scEt, 1.268, 75.92, 17.29, 0.898, 36.3, 1.484);
    else if (1.70<=fabs(scEta) && fabs(scEta)<2.1)
      return turnOnfunction(scEt, 0.4659, 36.07, 1.204, 0.4884, 36.81, 1.947);
    else if (2.1<=fabs(scEta) && fabs(scEta)<2.5)
      return turnOnfunction(scEt, 0.828, 37.28, 2.164, 0.116, 35.4, 0.9914);
    else
      return -1.0;
    }
/*
    else if(run=="Run_all"){
    if (0.0<=fabs(scEta) && fabs(scEta)<0.79)
      return turnOnfunction(scEt,0.8987, 33.88, 0.3972, 0.06919, 34.61, 2.495);
    else if (0.79<=fabs(scEta) && fabs(scEta)<1.1)
      return turnOnfunction(scEt,0.8796, 33.89, 0.4511, 0.08773, 34.27, 2.466);
    else if (1.1<=fabs(scEta) && fabs(scEta)<1.4442)
      return turnOnfunction(scEt,0.09263, 33.7, 2.426, 0.873, 34.06, 0.6335);
    else if (1.566<=fabs(scEta) && fabs(scEta)<1.70)
      return turnOnfunction(scEt,0.7733, 33.71, 0.6949, 0.1912, 33.73, 2.222);
    else if (1.70<=fabs(scEta) && fabs(scEta)<2.1)
      return turnOnfunction(scEt,0.7765, 33.9, 0.6375, 0.2082, 33.77, 1.698);
    else if (2.1<=fabs(scEta) && fabs(scEta)<2.5)
      return turnOnfunction(scEt,0.7771, 34.81, 0.9298, 0.2008, 35.29, 1.808);
    else
      return -1.0;
       }
*/
    else if(run=="Run_all"){
    if (0.0<=fabs(scEta) && fabs(scEta)<0.79)
      return turnOnfunction(scEt,0.9338, 25.84, 0.3994, 0.0413, 26.44, 3.255);
    else if (0.79<=fabs(scEta) && fabs(scEta)<1.1)
      return turnOnfunction(scEt,0.9246, 25.82, 0.4528, 0.05142, 25.74, 3.223);
    else if (1.1<=fabs(scEta) && fabs(scEta)<1.4442)
      return turnOnfunction(scEt,0.918, 26.01, 0.6092, 0.05179, 25.38, 2.58);
    else if (1.566<=fabs(scEta) && fabs(scEta)<1.70)
      return turnOnfunction(scEt,0.8709, 25.59, 0.7184, 0.09799, 25.98, 3.905);
    else if (1.70<=fabs(scEta) && fabs(scEta)<2.1)
      return turnOnfunction(scEt,0.8866, 25.82, 0.6621, 0.09917, 26.03, 2.3);
    else if (2.1<=fabs(scEta) && fabs(scEta)<2.5)
      return turnOnfunction(scEt,0.6169, 26.7, 0.7517, 0.3611, 27.34, 1.473);
    else
      return -1.0;
       }
   else{std::cout<<"wrong run name"<<std::endl;return 1;}
   }
  bool passTrig(float scEt,float scEta, TString run){return turnOn_MW(scEt,scEta,run)>randNrGen.Uniform(0,1);}

}
  


#endif
