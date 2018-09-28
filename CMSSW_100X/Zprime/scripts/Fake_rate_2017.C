float frFuncDataNoDEtaInEE(float et,float eta)
{
   if(fabs(eta)<1.5){
     if(et<87.3097) return 0.0346865+-0.000282823*et;
     else if(et>=87.3097 && et<168.981) return 0.0154796+-6.28359e-05*et;
     else return 0.00486146+0*et;
   }else if(fabs(eta)<2.0){
     return 0.0685793+0*et;
   }else if(std::abs(eta)<2.5){
     if(et<148.038) return 0.0978484+0.000351208*et;
     else return 0.149841+0*et;
   }else return 0.;

}

//////////////////
/*
float frFuncData(float et,float eta)
{
   if(std::abs(eta)<1.5){
//    et=et/0.991;
     if(et<76.8269) return 0.0504166+-0.000518216*et;
     else if(et>=76.8269 && et<193.163) return 0.0143937+-4.93329e-05*et;
     else return 0.00486445+0*et;
   }else if(std::abs(eta)<2.0){
//    et=et/0.993;
     if(et<76.6595) return 0.0990428+-0.000771932*et;
     else return 0.0398669+0*et;
   }else if(std::abs(eta)<2.5){
//    et=et/0.993;
     if(et<56.0614) return 0.101048+-0.000819684*et;
     else return 0.0515465+6.33035e-05*et;
   }else return 0.;
}
*/
//new

/*
float frFuncData(float et,float eta)
{
  if(std::abs(eta)<1.5){
    et=et/0.989;
    if(et<87.3097) return 0.0346865+-0.000282823*et;
    else if(et>=87.3097 && et<168.981) return 0.0154796+-6.28359e-05*et;
    else return 0.00486146+0*et;
  }else if(std::abs(eta)<2.0){
    et=et/0.996;
    if(et<78.4565) return 0.0686444+-0.000349687*et;
    else return 0.0412092+0*et;
  }else if(std::abs(eta)<2.5){
    et=et/0.996;
    if(et<83.8057) return 0.0733596+-0.000405637*et;
    else if(et>=83.8057 && et<157.615) return 0.00310642+0.00043265*et;
    else return 0.0712985+0*et;
  }else return 0.;

}
*/

/////////////// 2016 All /////////////////
/*
float frFuncData(float Et,float eta)
{
   if(std::abs(eta)<1.5){
   float et=Et/1.0012;
//   float et=Et;
     if(et<131.424) return
0.105781+-0.00251823*et+2.28326e-05*et*et+-7.21185e-08*et*et*et;
     else if(et>=131.424 && et<355.514) return
0.0137969+-0.000103437*et+3.61974e-07*et*et+-4.25465e-10*et*et*et;
     else return 0.00279259+2.42827e-06*et;
   }else if(std::abs(eta)<2.0){
//   float et=Et;
     float et=Et/1.0089;
     if(et<121.849) return 0.11723+-0.00129615*et+4.67464e-06*et*et;
     else if(et>=121.849 && et<226.175) return 0.034505+-4.76287e-05*et;
     else return 0.0257885+-9.08954e-06*et;
   }else if(std::abs(eta)<2.5){
     float et=Et/1.0089;
//   float et=Et;
     if(et<112.517) return 0.0807503+-0.000341528*et;
     else return 0.0423239;
   }else return 0.;
}
*/
/////////// 2017 For rereco //////////////////




float frFuncData(float Et,float eta)
{
   if(std::abs(eta)<1.5){
   float et=Et;
   if(et<131.6) return    0.14-0.0029*et+2.56e-05*et*et-8.48e-08*et*et*et;
   else if(et>=131.6 && et<359.3) return    0.02-0.00013*et+3.5e-07*et*et-2.9e-10*et*et*et;
   else return 0.00514+4.73e-07*et;
   }else if(std::abs(eta)<2.0){
   float et=Et;
     if(et<125) return 0.1012-0.00094*et+3.37e-06*et*et;
     else if(et>=125 && et<226.3) return 0.0488-11.37e-05*et;
     else return 0.0241-1.24e-06*et;
   }else if(std::abs(eta)<2.5){
   float et=Et;
     if(et<152) return 0.0622-0.00012*et;
     else return 0.0387;
   }else return 0.;
}

