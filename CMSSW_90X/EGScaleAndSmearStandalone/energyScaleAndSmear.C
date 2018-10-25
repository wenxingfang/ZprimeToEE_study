#include "EnergyScaleCorrection_class.cc"

#include "TRandom3.h"
#include <memory>

namespace egamma{
  
  float eMCSmearCorr(const EnergyScaleCorrection_class& eScaler,
		     const int runnr,const float et,const float etaSC,const float r9,const int gain){
    static TRandom3 randNrGen;
    const bool isEBEle = std::abs(etaSC)<1.5;
    float smearSigma = eScaler.getSmearingSigma(runnr, isEBEle, r9, etaSC, et, gain, 0, 0);
    return randNrGen.Gaus(1,smearSigma);
  }

  float eDataScaleCorr(const EnergyScaleCorrection_class& eScaler,
		       const int runnr,const float et,const float etaSC,const float r9,const int gain){
    const bool isEBEle = std::abs(etaSC)<1.5;
    float scale = eScaler.ScaleCorrection(runnr, isEBEle, r9, etaSC, et, gain);
    return scale;
  }

  //the main TTree::Draw callable function
  float eCorr(const int runnr,const float et,const float etaSC,const float r9,const int gain,const bool isMC)
  {  
    static std::unique_ptr<EnergyScaleCorrection_class> eScaler;
    if(eScaler==nullptr){
      //adjust this to whereever you put the .dat files
      eScaler = std::make_unique<EnergyScaleCorrection_class>("/user/wenxing/ST_TW_channel/CMSSW_9_4_0/src/EGScaleAndSmearStandalone/ScalesSmearings/Run2017_17Nov2017_v1_ele_unc");
      eScaler->doScale=true;
      eScaler->doSmearings=true;
    }
    if(isMC) return eMCSmearCorr(*eScaler,runnr,et,etaSC,r9,gain);
    else return eDataScaleCorr(*eScaler,runnr,et,etaSC,r9,gain);
  }

}
