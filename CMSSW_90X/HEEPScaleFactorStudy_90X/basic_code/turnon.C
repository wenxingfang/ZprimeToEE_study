#ifndef DIELESCALEFACTORS_ELE27WPLOOSETRIGTURN_C
#define DIELESCALEFACTORS_ELE27WPLOOSETRIGTURN_C

#include "TMath.h"
#include "TRandom3.h"

namespace trigEle27{
  class TurnOn {
  public:
    class TurnOnFunc {
      float maxEff_,midPoint_,turnOn_;      
    public:
      TurnOnFunc():maxEff_(0),midPoint_(0),turnOn_(0){}
      TurnOnFunc(float maxEff,float midPoint,float turnOn):maxEff_(maxEff),midPoint_(midPoint),turnOn_(turnOn){}
      float operator()(float et)const{
	return 0.5*maxEff_*(1+TMath::Erf((et-midPoint_)/(sqrt(2)*turnOn_)));
      }
    };
    
    class DiTurnOnFunc {
    private:
      TurnOnFunc turnOn1_,turnOn2_;
    public:
      DiTurnOnFunc(){}
      DiTurnOnFunc(const TurnOnFunc& turnOn1,const TurnOnFunc& turnOn2):
	turnOn1_(turnOn1),turnOn2_(turnOn2){}
      float operator()(float et)const{return turnOn1_(et)+turnOn2_(et);}
    };
    
    template<typename T> 
    struct Nop{
      T operator()(const T& val)const{return val;}
    };
    template<typename T> 
    struct Abs{
      T operator()(const T& val)const{return std::abs(val);}
    };

    template<typename T,typename Func=Nop<T>>
    class ValRange {
    private:
      Func manipFunc_;
      T minVal_;
      T maxVal_;
    public:
      ValRange(){}
      ValRange(const T& minVal,const T& maxVal):minVal_(minVal),maxVal_(maxVal){}
      bool operator()(const T& inputVal)const{return manipFunc_(inputVal)>=minVal_ && manipFunc_(inputVal)<maxVal_;}
    };
   
    using ValRangeAbsF = ValRange<float,Abs<float>>;
    
  private:
    std::vector<std::pair<ValRangeAbsF,DiTurnOnFunc>> turnOnData_;
  public:
    TurnOn(){
      turnOnData_.push_back(std::make_pair<ValRangeAbsF,DiTurnOnFunc>({0.0,1.5},
	//{{0.410,29.1,1.88},{0.517,23.7,14.2}}//for 2015
	//{{0.622,27.3,0.597},{0.289,37,5.45}}//for 2016
	//{{0.218,36.8,5.15},{0.725,-15.7,42}}//for 2016
       	//{{0.819,24.3,11.8},{0.142,1.48e-7,84.4}}//for 2016 7p1
       	//{{0.702,22.675,11.149},{0.223,37.622,37.619}}//for 2016 Ele27WPTight
       	{{0.649,23.450,10.901},{0.287,28.056,42.947}}//for 2016 corrected data Ele27WPTight
        ));
      turnOnData_.push_back(std::make_pair<ValRangeAbsF,DiTurnOnFunc>({1.5,2.1},
	{{0.544,28.7,1.16},{0.318,28.5,6.86}}));//for 2015
      turnOnData_.push_back(std::make_pair<ValRangeAbsF,DiTurnOnFunc>({2.1,2.5},
	{{0.,35.4,1.03},{0.,37.6,2.09}}));//for 2015
    }
    float operator()(float et,float eta)const{
      for(const auto& data : turnOnData_){
	if(data.first(eta)) return data.second(et);
      }
      return 0;
    }
	  

  };
  
  TurnOn turnOnData;
  TRandom3 randNrGen;
  
  float turnOn(float scEt,float scEta){return turnOnData(scEt,scEta);}
  
  bool passTrig(float scEt,float scEta){return turnOn(scEt,scEta)>randNrGen.Uniform(0,1);}

}
/*
namespace trigEle33{


  float turnOnfunction(float Et,float Eta){
    float p0=-10.2;
    float p1=-7.03e+08;
    float p2=3.68;
    float p3=11.2;
    float p4=-17.9;
    float p5=24.4;
    float eff = 0.0;
    eff = 0.5*p0*(1+erf((Et-p1)/(1.414*p2)))+0.5*p3*(1+erf((Et-p4)/(1.414*p5)));
    return eff;
  }
}  
*/

#endif
