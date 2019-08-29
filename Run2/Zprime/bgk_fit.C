#include<math.h>
#include<TMath.h>
#include<TH1D.h>
#include<TFile.h>
#include<TROOT.h>
#include "RooChi2Var.h"
#include "RooGenericPdf.h"
#include "RooRealVar.h"
#include "RooAbsReal.h"
#include "RooNumIntConfig.h"
#include "RooDataSet.h"
#include "RooGaussian.h"
#include "RooBreitWigner.h"
#include "RooCBShape.h"
#include "RooFFTConvPdf.h"
#include "RooConstVar.h"
#include "RooPolynomial.h"
#include "RooAddPdf.h"
#include "RooProdPdf.h"
#include "RooFitResult.h"
#include "RooPlot.h"
#include "TCanvas.h"
#include "TAxis.h"
#include "RooTFnBinding.h"
#include "RooCFunction1Binding.h"
#include "TMath.h"
#include<stdio.h>
#include "TProfile.h"
#include <string>
#include <sstream>
#include <TH2.h>
#include <TLatex.h>
#include <TH1.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TPad.h>
#include "TFile.h"
#include "TF1.h"
#include <math.h>
#include <cmath>
#include "TF2.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TH3F.h"
#include "TLorentzVector.h"
#include <time.h>
#include <iostream>
#include <vector>
#include <TROOT.h>
#include <TSystem.h>
#include <TChain.h>
#include <TFile.h>
#include <TPaveText.h>
#include <TText.h>
#include <TLegend.h>
#include <RooDataHist.h>
#include <TString.h>

using namespace RooFit ;
void draw( RooRealVar x, RooDataHist hist, TH1D* hh, RooGenericPdf pdf, RooFitResult* result ,TString out_name);
void draw_split( RooRealVar x, RooDataHist hist, TH1D* hh, RooGenericPdf pdf, RooFitResult* result ,TString out_name);
void draw_compare(TH1D* hist, TF1* fun, TString out_name);
void draw_compare_two(TH1D* hist, TF1* fun1, TF1* fun2, TString out_name);
void bgk_fit(){
RooAbsReal::defaultIntegratorConfig()->Print("v") ;
RooAbsReal::defaultIntegratorConfig()->setEpsAbs(1e-10) ;
RooAbsReal::defaultIntegratorConfig()->setEpsRel(1e-10) ;

TH1::SetDefaultSumw2();
gSystem->Load("libRooFit");
gROOT->Reset();
gROOT->SetStyle("Plain");
gROOT->SetBatch(kTRUE);

TFile* f = new TFile("bgk_2016.root","READ");
TH1D* h_BB  = (TH1D*) f->Get("bgk_h_mee_BB_usual");
TH1D* h_BE  = (TH1D*) f->Get("bgk_h_mee_BE_usual");
/*
TH1D* h_cosp_BB  = (TH1D*) f->Get("bgk_h_mee_cosp_BB_usual");
TH1D* h_cosp_BE  = (TH1D*) f->Get("bgk_h_mee_cosp_BE_usual");
TH1D* h_cosm_BB  = (TH1D*) f->Get("bgk_h_mee_cosm_BB_usual");
//TH1D* h_cosm_BE  = (TH1D*) f->Get("bgk_h_mee_cosm_BE_usual");
TH1D* h_cosm_BE_v1  = (TH1D*) f->Get("bgk_h_mee_cosm_BE_usual");
TH1D* h_cosm_BE  = (TH1D*)h_cosm_BE_v1->Rebin(2);
*/

const float fit_low=140;//150
//const float fit_up=4000;// orignal 4000
const float fit_up=4000;// orignal 4000
RooRealVar x("x","x",  fit_low  ,  fit_up );
//###########################  nominal ####################################

RooRealVar Norm_BB  ("Norm_BB"  ,""     ,  3.10        , 2.8     , 3.5   );
RooRealVar a_BB     ("a_BB"     ,""     , -1.0748      ,-1.3     , -0.8  );
RooRealVar b_BB     ("b_BB"     ,""     ,  4.50        , 0.5     , 10.00 );
RooRealVar c_BB     ("c_BB"     ,""     , -1.9388      ,-2.20    , -1.2  );
RooRealVar d_BB     ("d_BB"     ,""     , -3.956       ,-4.2     , -3.6  );
RooGenericPdf pdf_BB("pdf_BB","pdf_BB","10*Norm_BB*exp(1e-3*a_BB*x+1e-8*b_BB*pow(x,2)+1e-11*c_BB*pow(x,3))*pow(x,d_BB)",RooArgSet(x,a_BB,b_BB,c_BB,d_BB,Norm_BB)) ;

RooRealVar Norm_BE  ("Norm_BE"  ,""     ,  2.35        , 2.0     , 2.6   );
RooRealVar a_BE     ("a_BE"     ,""     , -3.85        ,-6.00    , -2.00 );
RooRealVar b_BE     ("b_BE"     ,""     ,  65.55       , 60.00   , 90.00 );
RooRealVar c_BE     ("c_BE"     ,""     , -7.44        ,-10.00   , -6.00 );
RooRealVar d_BE     ("d_BE"     ,""     , -2.90        ,-4.00    , -2.00  );
RooGenericPdf pdf_BE("pdf_BE","pdf_BE","10*Norm_BE*exp(1e-3*a_BE*x+1e-8*b_BE*pow(x,2)+1e-11*c_BE*pow(x,3))*pow(x,d_BE)",RooArgSet(x,a_BE,b_BE,c_BE,d_BE,Norm_BE)) ;
//+++++++++++++++++++++++++++++++ separate ++++++++++++++++++++++++++++++++++
/*
RooRealVar LNorm_BB  ("LNorm_BB"  ,""     ,  31             , 26         , 35    );
RooRealVar La_BB     ("La_BB"     ,""     , -1.0748e-3      ,-1.3e-3     , -0.8e-3  );
RooRealVar Lb_BB     ("Lb_BB"     ,""     ,  4.50e-8        , 0.15e-8    , 10.00e-8 );
RooRealVar Lc_BB     ("Lc_BB"     ,""     , -1.9388e-11     ,-2.20e-11   , -1.2e-11  );
RooRealVar Ld_BB     ("Ld_BB"     ,""     , -3.956          ,-4.2        , -3.6  );
RooRealVar HNorm_BB  ("HNorm_BB"  ,""     ,  31             , 28         , 35    );
RooRealVar Ha_BB     ("Ha_BB"     ,""     , -1.0748e-3      ,-1.3e-3     , -0.8e-3  );
RooRealVar Hb_BB     ("Hb_BB"     ,""     ,  4.50e-8        , 0.5e-8     , 10.00e-8 );
RooRealVar Hc_BB     ("Hc_BB"     ,""     , -1.9388e-11     ,-2.20e-11   , -1.2e-11 );
RooRealVar Hd_BB     ("Hd_BB"     ,""     , -3.956          ,-4.2        , -3.6  );
RooArgSet Var_BB(x,LNorm_BB,La_BB,Lb_BB,Lc_BB,Ld_BB,HNorm_BB,Ha_BB,Hb_BB);
Var_BB.add(RooArgSet(Hc_BB,Hd_BB));
RooGenericPdf PDF_BB("PDF_BB","PDF_BB","(x<=600)*LNorm_BB*exp(La_BB*x+Lb_BB*pow(x,2)+Lc_BB*pow(x,3))*pow(x,Ld_BB)+(x>600)*HNorm_BB*exp(Ha_BB*x+Hb_BB*pow(x,2)+Hc_BB*pow(x,3))*pow(x,Hd_BB)",Var_BB) ;
//RooGenericPdf PDF_BB("PDF_BB","PDF_BB","(@0<=600)*10*@1*exp(1e-3*@2*@0+1e-8*@3*pow(@0,2)+1e-11*@4*pow(@0,3))*pow(@0,@5)+(@0>600)*10*@6*exp(1e-3*@7*@0+1e-8*@8*pow(@0,2)+1e-11*@9*pow(@0,3))*pow(@0,@10)",Var_BB) ;

RooRealVar LNorm_BE  ("LNorm_BE"  ,""     ,  2.35        , 2.0     , 2.6   );
RooRealVar La_BE     ("La_BE"     ,""     , -3.85e-3        ,-6.00e-3    , -2.00e-3 );
RooRealVar Lb_BE     ("Lb_BE"     ,""     ,  65.55e-8       , 60.00e-8   , 90.00e-8 );
RooRealVar Lc_BE     ("Lc_BE"     ,""     , -7.44e-11        ,-10.00e-11   , -6.00e-11 );
RooRealVar Ld_BE     ("Ld_BE"     ,""     , -2.90        ,-4.00    , -2.00  );
RooRealVar HNorm_BE  ("HNorm_BE"  ,""     ,  2.35        , 2.0     , 2.6   );
RooRealVar Ha_BE     ("Ha_BE"     ,""     , -3.85e-3        ,-6.00e-3    , -2.00e-3 );
RooRealVar Hb_BE     ("Hb_BE"     ,""     ,  65.55e-8       , 60.00e-8   , 90.00e-8 );
RooRealVar Hc_BE     ("Hc_BE"     ,""     , -7.44e-11        ,-10.00e-11   , -6.00e-11 );
RooRealVar Hd_BE     ("Hd_BE"     ,""     , -2.90        ,-4.00    , -2.00  );
RooArgSet Var_BE(x,LNorm_BE,La_BE,Lb_BE,Lc_BE,Ld_BE,HNorm_BE,Ha_BE,Hb_BE);
Var_BE.add(RooArgSet(Hc_BE,Hd_BE));
RooGenericPdf PDF_BE("PDF_BE","PDF_BE","(x<=600)*LNorm_BE*exp(La_BE*x+Lb_BE*pow(x,2)+Lc_BE*pow(x,3))*pow(x,Ld_BE)+(x>600)*HNorm_BE*exp(Ha_BE*x+Hb_BE*pow(x,2)+Hc_BE*pow(x,3))*pow(x,Hd_BE)",Var_BE) ;
*/
//+++++++++++++++++++++++++++++++ separate new ++++++++++++++++++++++++++++++++++

RooRealVar LNorm_BB  ("LNorm_BB"  ,""     ,  3.40        , 2.6     , 3.6   );
RooRealVar La_BB     ("La_BB"     ,""     , -1.0748e-3   ,-2.0e-3     , -0.8e-3  );
RooRealVar Lb_BB     ("Lb_BB"     ,""     ,  3.50e-8     , 0.    , 10.00e-8 );
Lb_BB.setVal(0);
Lb_BB.setConstant();
RooRealVar Lc_BB     ("Lc_BB"     ,""     , -1.9388e-11  ,-2.20e-11, -1.2e-11);
RooRealVar Ld_BB     ("Ld_BB"     ,""     , -3.956       ,-4.2     , -3.6  );
RooRealVar HNorm_BB  ("HNorm_BB"  ,""     ,  3.40        , 2.8     , 3.8   );
RooRealVar Ha_BB     ("Ha_BB"     ,""     , -1.0748e-3   ,-1.4e-3  , -0.6e-3);
RooRealVar Hb_BB     ("Hb_BB"     ,""     ,  2.40e-8     , 0.     , 10.00e-8 );
Hb_BB.setVal(0);
Hb_BB.setConstant();
RooRealVar Hc_BB     ("Hc_BB"     ,""     , -1.5388e-11  ,-2.20e-11, -0.1e-11);
RooRealVar Hd_BB     ("Hd_BB"     ,""     , -3.956       ,-4.2     , -3.6  );
RooArgSet Var_BB(x,LNorm_BB,La_BB,Lb_BB,Lc_BB,Ld_BB,HNorm_BB,Ha_BB,Hb_BB);
Var_BB.add(RooArgSet(Hc_BB,Hd_BB));
RooGenericPdf PDF_BB("PDF_BB","PDF_BB","(x<=600)*exp(LNorm_BB+La_BB*x+Lb_BB*pow(x,2)+Lc_BB*pow(x,3))*pow(x,Ld_BB)+(x>600)*exp(HNorm_BB+Ha_BB*x+Hb_BB*pow(x,2)+Hc_BB*pow(x,3))*pow(x,Hd_BB)",Var_BB) ;


RooRealVar LNorm_BE  ("LNorm_BE"  ,""     ,  3.0        , 1.     , 4   );
RooRealVar La_BE     ("La_BE"     ,""     , -4.5e-3     ,-10.00e-3, 0.001e-3 );
RooRealVar Lb_BE     ("Lb_BE"     ,""     ,  65.55e-8   , 0.00   , 90.00e-8 );
Lb_BE.setVal(0);
Lb_BE.setConstant();
RooRealVar Lc_BE     ("Lc_BE"     ,""     , -7.44e-11   ,-25.00e-11, 0.001e-11 );
Lc_BE.setVal(0);
Lc_BE.setConstant();
RooRealVar Ld_BE     ("Ld_BE"     ,""     , -3.10        ,-10.00    , 0.001  );
RooRealVar HNorm_BE  ("HNorm_BE"  ,""     ,  3.55        , 0.     ,  5   );
RooRealVar Ha_BE     ("Ha_BE"     ,""     , -3.85e-3     ,-10.00e-3    , 0.001e-3 );
RooRealVar Hb_BE     ("Hb_BE"     ,""     ,  60.55e-8    , 0.00   , 90.00e-8 );
RooRealVar Hc_BE     ("Hc_BE"     ,""     , -4.55e-11    ,-10.00e-11   , 0.001e-11 );
RooRealVar Hd_BE     ("Hd_BE"     ,""     , -4.10        ,-10.00    , 0.001  );
RooArgSet Var_BE(x,LNorm_BE,La_BE,Lb_BE,Lc_BE,Ld_BE,HNorm_BE,Ha_BE,Hb_BE);
Var_BE.add(RooArgSet(Hc_BE,Hd_BE));
RooGenericPdf PDF_BE("PDF_BE","PDF_BE","(x<=600)*exp(LNorm_BE+La_BE*x+Lb_BE*pow(x,2)+Lc_BE*pow(x,3))*pow(x,Ld_BE)+(x>600)*exp(HNorm_BE+Ha_BE*x+Hb_BE*pow(x,2)+Hc_BE*pow(x,3))*pow(x,Hd_BE)",Var_BE) ;

//###########################  cosp  ####################################
/*
RooRealVar Norm_BB  ("Norm_BB"  ,""     ,  3.20        , 2.8     , 3.6   );
RooRealVar a_BB     ("a_BB"     ,""     , -1.0748      ,-1.3     , -0.8  );
RooRealVar b_BB     ("b_BB"     ,""     ,  4.50        , 0.5     , 10.00 );
RooRealVar c_BB     ("c_BB"     ,""     , -1.9388      ,-2.20    , -1.2  );
RooRealVar d_BB     ("d_BB"     ,""     , -3.956       ,-4.2     , -3.6  );
RooGenericPdf pdf_BB("pdf_BB","pdf_BB","10*Norm_BB*exp(1e-3*a_BB*x+1e-8*b_BB*pow(x,2)+1e-11*c_BB*pow(x,3))*pow(x,d_BB)",RooArgSet(x,a_BB,b_BB,c_BB,d_BB,Norm_BB)) ;

RooRealVar Norm_BE  ("Norm_BE"  ,""     ,  2.35        , 2.0     , 2.6   );
RooRealVar a_BE     ("a_BE"     ,""     , -3.85        ,-6.00    , -2.00 );
RooRealVar b_BE     ("b_BE"     ,""     ,  65.55       , 60.00   , 90.00 );
RooRealVar c_BE     ("c_BE"     ,""     , -7.44        ,-10.00   , -6.00 );
RooRealVar d_BE     ("d_BE"     ,""     , -2.90        ,-4.00    , -2.00  );
RooGenericPdf pdf_BE("pdf_BE","pdf_BE","Norm_BE*exp(1e-3*a_BE*x+1e-8*b_BE*pow(x,2)+1e-11*c_BE*pow(x,3))*pow(x,d_BE)",RooArgSet(x,a_BE,b_BE,c_BE,d_BE,Norm_BE)) ;
*/
//###########################  cosm  ####################################
/*
RooRealVar Norm_BB  ("Norm_BB"  ,""     ,  3.10        , 2.8     , 3.5   );
RooRealVar a_BB     ("a_BB"     ,""     , -1.0748      ,-1.3     , -0.8  );
RooRealVar b_BB     ("b_BB"     ,""     ,  4.50        , 0.5     , 10.00 );
RooRealVar c_BB     ("c_BB"     ,""     , -1.9388      ,-2.20    , -1.2  );
RooRealVar d_BB     ("d_BB"     ,""     , -3.956       ,-4.2     , -3.6  );
RooGenericPdf pdf_BB("pdf_BB","pdf_BB","10*Norm_BB*exp(1e-3*a_BB*x+1e-8*b_BB*pow(x,2)+1e-11*c_BB*pow(x,3))*pow(x,d_BB)",RooArgSet(x,a_BB,b_BB,c_BB,d_BB,Norm_BB)) ;

RooRealVar Norm_BE  ("Norm_BE"  ,""     ,  2.35        , 2.0     , 2.6   );
RooRealVar a_BE     ("a_BE"     ,""     , -3.85        ,-6.00    , -2.00 );
RooRealVar b_BE     ("b_BE"     ,""     ,  65.55       , 60.00   , 90.00 );
RooRealVar c_BE     ("c_BE"     ,""     , -7.44        ,-10.00   , -6.00 );
RooRealVar d_BE     ("d_BE"     ,""     , -2.90        ,-4.00    , -2.00  );
RooGenericPdf pdf_BE("pdf_BE","pdf_BE","Norm_BE*exp(1e-3*a_BE*x+1e-8*b_BE*pow(x,2)+1e-11*c_BE*pow(x,3))*pow(x,d_BE)",RooArgSet(x,a_BE,b_BE,c_BE,d_BE,Norm_BE)) ;
*/
/*
RooRealVar ga_x    ("ga_x","ga_x",  200 ,  800 );
RooRealVar ga_mean ("ga_mean","ga_mean",  91 ,  90,92 );
RooRealVar ga_sigma("ga_sigma","ga_sigma",  2.5 ,  1,3 );
RooGaussian gauss  ("gauss","",ga_x,ga_mean,ga_sigma);
RooRealVar cb_mean ("cb_mean" ,"cb_mean" ,  0  ,  -0.4,0.4 );
RooRealVar cb_sigma("cb_sigma","cb_sigma",  0.01 , 1e-4,1 );
RooRealVar cb_a    ("cb_a"   , "CB Cut"  , 1, 0.1, 50);
RooRealVar cb_n    ("cb_n"   , "CB Power", 2, 0.2, 50);
RooCBShape CB      ("CB","",ga_x,cb_mean,cb_sigma,cb_a,cb_n);
RooFFTConvPdf model("model","model",ga_x,gauss,CB);
*/
RooDataHist dh_BB("dh_BB","dh_BB"   ,x, h_BB);
RooDataHist dh_BE("dh_BE","dh_BE"   ,x, h_BE);
/*
RooDataHist dh_cosp_BB("dh_cosp_BB","dh_cosp_BB"   ,x, h_cosp_BB);
RooDataHist dh_cosp_BE("dh_cosp_BE","dh_cosp_BE"   ,x, h_cosp_BE);
RooDataHist dh_cosm_BB("dh_cosm_BB","dh_cosm_BB"   ,x, h_cosm_BB);
RooDataHist dh_cosm_BE("dh_cosm_BE","dh_cosm_BE"   ,x, h_cosm_BE);
*/
//RooFitResult* result = pdf_BB.fitTo(dh_BB,Range(200,1000),SumW2Error(kTRUE),Save()) ;
//RooFitResult* result = pdf_BB.fitTo(dh_BB,SumW2Error(kTRUE),Save()) ;
//RooFitResult* result = pdf_BB.fitTo(dh_BB,SumW2Error(kTRUE),Save()) ;
//RooFitResult* result = model.fitTo(dh_BB,Range(200,800),SumW2Error(kTRUE),Save()) ;
//############### nominal ################################
/*
RooFitResult* result_BB = pdf_BB.chi2FitTo(dh_BB,Save()) ;
draw( x, dh_BB, h_BB, pdf_BB, result_BB ,"BB_");
*/
/*
RooFitResult* result_BE = pdf_BE.chi2FitTo(dh_BE,Save()) ;
draw( x, dh_BE, h_BE, pdf_BE, result_BE ,"BE_");
*/
//++++++++++++++++ split +++++++++++++++++++++++++++++
/*
RooFitResult* result_BB = PDF_BB.chi2FitTo(dh_BB,Save()) ;
draw_split( x, dh_BB, h_BB, PDF_BB, result_BB ,"BB_");
*/

RooFitResult* result_BE = PDF_BE.chi2FitTo(dh_BE,Save()) ;
draw_split( x, dh_BE, h_BE, PDF_BE, result_BE ,"BE_");

/*
const float x_down=140;
const float x_up=4000;
const float x_down_1=140;
const float x_up_1=600;
const float x_down_2=600;
const float x_up_2=4000;
TF1* f_BB_1 = new TF1("f_BB_1","[0]*30.556116*exp(-1.3e-3*x+5.000603e-9*x*x-2.199982e-11*x*x*x)*pow(x,-3.811980)",x_down_1,x_up_1);
f_BB_1->SetParameter(0,1);
double BB_scale_1=20*h_BB->Integral(h_BB->GetXaxis()->FindBin(x_down_1+1),h_BB->GetXaxis()->FindBin(x_up_1-1))/f_BB_1->Integral(x_down_1,x_up_1);
f_BB_1->SetParameter(0,BB_scale_1);
TF1* f_BB_2 = new TF1("f_BB_2","[0]*34.730069*exp(-1.117221e-3*x+2.887786e-8*x*x-1.268114e-11*x*x*x)*pow(x,-3.819568)",x_down_2,x_up_2);
f_BB_2->SetParameter(0,1);
double BB_scale_2=20*h_BB->Integral(h_BB->GetXaxis()->FindBin(x_down_2+1),h_BB->GetXaxis()->FindBin(x_up_2-1))/f_BB_2->Integral(x_down_2,x_up_2);
f_BB_2->SetParameter(0,BB_scale_2);

TF1* f_BE_1 = new TF1("f_BE_1","[0]*25.999129*exp(-4.501022e-3*x+6.000081e-7*x*x-9.997981e-11*x*x*x)*pow(x,-2.675427)",x_down_1,x_up_1);
f_BE_1->SetParameter(0,1);
double BE_scale_1=20*h_BE->Integral(h_BE->GetXaxis()->FindBin(x_down_1+1),h_BE->GetXaxis()->FindBin(x_up_1-1))/f_BE_1->Integral(x_down_1,x_up_1);
f_BE_1->SetParameter(0,BE_scale_1);
TF1* f_BE_2 = new TF1("f_BE_2","[0]*23.486731*exp(-3.883321e-3*x+6.453821e-7*x*x-7.270135e-11*x*x*x)*pow(x,-2.816375)",x_down_2,x_up_2);
f_BE_2->SetParameter(0,1);
double BE_scale_2=20*h_BE->Integral(h_BE->GetXaxis()->FindBin(x_down_2+1),h_BE->GetXaxis()->FindBin(x_up_2-1))/f_BE_2->Integral(x_down_2,x_up_2);
f_BE_2->SetParameter(0,BE_scale_2);

draw_compare_two(h_BB, f_BB_1, f_BB_2, "BB_check_");
draw_compare_two(h_BE, f_BE_1, f_BE_2, "BE_check_");
*/
//############### cosp  ################################
/*
RooFitResult* result_cosp_BB = pdf_BB.chi2FitTo(dh_cosp_BB,Save()) ;
draw( x, dh_cosp_BB, h_cosp_BB, pdf_BB, result_cosp_BB ,"cosp_BB_");
*/
/*
RooFitResult* result_cosp_BE = pdf_BE.chi2FitTo(dh_cosp_BE,Save()) ;
draw( x, dh_cosp_BE, h_cosp_BE, pdf_BE, result_cosp_BE ,"cosp_BE_");
*/
//############### cosm  ################################
/*
RooFitResult* result_cosm_BB = pdf_BB.chi2FitTo(dh_cosm_BB,Save()) ;
draw( x, dh_cosm_BB, h_cosm_BB, pdf_BB, result_cosm_BB ,"cosm_BB_");
*/
/*
RooFitResult* result_cosm_BE = pdf_BE.chi2FitTo(dh_cosm_BE,Save()) ;
draw( x, dh_cosm_BE, h_cosm_BE, pdf_BE, result_cosm_BE ,"cosm_BE_");
*/
}

void draw_split( RooRealVar x, RooDataHist hist, TH1D* hh, RooGenericPdf pdf, RooFitResult* result ,TString out_name){
RooPlot* frame = x.frame();
TCanvas *can = new TCanvas("can","",1000,1000);
can->cd();
TPad *pad1 = new TPad("pad1", "", 0.0, 0.3, 1.0, 1.0, 0);
TPad *pad2 = new TPad("pad2", "", 0.0, 0.0, 1.0, 0.3, 0);
pad1->Draw();
pad2->Draw();
pad1->SetBottomMargin(0.07);
pad2->SetTopMargin(0);
pad2->SetBottomMargin(0.35);
pad1->SetRightMargin(0.07);
pad1->SetLeftMargin(0.13);
pad2->SetRightMargin(0.07);
pad2->SetLeftMargin(0.13);
pad2->SetGridy();
pad1->SetTickx();
pad1->SetTicky();
pad2->SetTickx();
pad2->SetTicky();
pad1->SetLogy();
pad1->cd();
//hist.plotOn(frame);//possion error
hist.plotOn(frame,DataError(RooAbsData::SumW2));
pdf.plotOn(frame);
frame->SetMaximum(5E4);
frame->SetMinimum(1E-4);
//frame->SetMaximum(2E5);
//frame->SetMinimum(1E1);
//frame->SetMaximum(2E5);
//frame->SetMinimum(1E1);
frame->SetTitle("");
frame->SetXTitle("");
frame->SetYTitle("Events / 20 GeV");
frame->GetXaxis()->SetLabelSize(0.055);
frame->GetYaxis()->SetLabelSize(0.055);
frame->GetYaxis()->SetTitleSize(0.055);
frame->Draw();
int nbins=(frame->GetXaxis()->GetXmax()-frame->GetXaxis()->GetXmin())/hh->GetBinWidth(1);
TH1* ph=pdf.createHistogram("ph",x,Binning(nbins));
TH1D *hbgk= new TH1D("hbgk","",nbins,frame->GetXaxis()->GetXmin(),frame->GetXaxis()->GetXmax());
for(int i=1;i<nbins+1;i++){
float mean=hbgk->GetBinLowEdge(i)+0.5*hbgk->GetBinWidth(i);
int bin_x=hh->GetXaxis()->FindBin(mean);
hbgk->SetBinContent(i,hh->GetBinContent(bin_x));
hbgk->SetBinError  (i,hh->GetBinError  (bin_x));
}
//int bin_low=hh->GetXaxis()->FindBin(frame->GetXaxis()->GetXmin());
//int bin_up =hh->GetXaxis()->FindBin(frame->GetXaxis()->GetXmax());
//double scale=hh->Integral(bin_low,bin_up)/ph->Integral();
double scale=hbgk->Integral()/ph->Integral();
std::cout<<"scale:"<<scale<<std::endl;
ph->Scale(scale);
//ph->Draw("same");
//hbgk->Draw("same:hist");
//////// parameters
RooChi2Var chi2 ("chi2", "chi2", pdf, hist);
double chi2_val = chi2.getVal();

double L_p_0      =0;
double L_p_0_error=0;
double L_p_a      =0;
double L_p_a_error=0;
double L_p_b      =0;
double L_p_b_error=0;
double L_p_c      =0;
double L_p_c_error=0;
double L_p_d      =0;
double L_p_d_error=0;
double H_p_0      =0;
double H_p_0_error=0;
double H_p_a      =0;
double H_p_a_error=0;
double H_p_b      =0;
double H_p_b_error=0;
double H_p_c      =0;
double H_p_c_error=0;
double H_p_d      =0;
double H_p_d_error=0;

if(out_name.Contains("BB")){
RooRealVar* L_par0_fitresult = (RooRealVar*) result->floatParsFinal().find("LNorm_BB");
RooRealVar* L_par1_fitresult = (RooRealVar*) result->floatParsFinal().find("La_BB");
//RooRealVar* L_par2_fitresult = (RooRealVar*) result->floatParsFinal().find("Lb_BB");
RooRealVar* L_par3_fitresult = (RooRealVar*) result->floatParsFinal().find("Lc_BB");
RooRealVar* L_par4_fitresult = (RooRealVar*) result->floatParsFinal().find("Ld_BB");
L_p_0      =L_par0_fitresult->getValV()   ;
L_p_0_error=L_par0_fitresult->getError()  ;
L_p_a      =L_par1_fitresult->getValV()   ;
L_p_a_error=L_par1_fitresult->getError()  ;
//L_p_b      =L_par2_fitresult->getValV()   ;
//L_p_b_error=L_par2_fitresult->getError()  ;
L_p_c      =L_par3_fitresult->getValV()   ;
L_p_c_error=L_par3_fitresult->getError()  ;
L_p_d      =L_par4_fitresult->getValV()   ;
L_p_d_error=L_par4_fitresult->getError()  ;
RooRealVar* H_par0_fitresult = (RooRealVar*) result->floatParsFinal().find("HNorm_BB");
RooRealVar* H_par1_fitresult = (RooRealVar*) result->floatParsFinal().find("Ha_BB");
//RooRealVar* H_par2_fitresult = (RooRealVar*) result->floatParsFinal().find("Hb_BB");
RooRealVar* H_par3_fitresult = (RooRealVar*) result->floatParsFinal().find("Hc_BB");
RooRealVar* H_par4_fitresult = (RooRealVar*) result->floatParsFinal().find("Hd_BB");
H_p_0      =H_par0_fitresult->getValV()   ;
H_p_0_error=H_par0_fitresult->getError()  ;
H_p_a      =H_par1_fitresult->getValV()   ;
H_p_a_error=H_par1_fitresult->getError()  ;
//H_p_b      =H_par2_fitresult->getValV()   ;
//H_p_b_error=H_par2_fitresult->getError()  ;
H_p_c      =H_par3_fitresult->getValV()   ;
H_p_c_error=H_par3_fitresult->getError()  ;
H_p_d      =H_par4_fitresult->getValV()   ;
H_p_d_error=H_par4_fitresult->getError()  ;
}
else if(out_name.Contains("BE")){
RooRealVar* L_par0_fitresult = (RooRealVar*) result->floatParsFinal().find("LNorm_BE");
RooRealVar* L_par1_fitresult = (RooRealVar*) result->floatParsFinal().find("La_BE");
//RooRealVar* L_par2_fitresult = (RooRealVar*) result->floatParsFinal().find("Lb_BE");
//RooRealVar* L_par3_fitresult = (RooRealVar*) result->floatParsFinal().find("Lc_BE");
RooRealVar* L_par4_fitresult = (RooRealVar*) result->floatParsFinal().find("Ld_BE");
L_p_0      =L_par0_fitresult->getValV()   ;
L_p_0_error=L_par0_fitresult->getError()  ;
L_p_a      =L_par1_fitresult->getValV()   ;
L_p_a_error=L_par1_fitresult->getError()  ;
//L_p_b      =L_par2_fitresult->getValV()   ;
//L_p_b_error=L_par2_fitresult->getError()  ;
//L_p_c      =L_par3_fitresult->getValV()   ;
//L_p_c_error=L_par3_fitresult->getError()  ;
L_p_d      =  L_par4_fitresult->getValV()   ;
L_p_d_error=  L_par4_fitresult->getError()  ;
RooRealVar* H_par0_fitresult = (RooRealVar*) result->floatParsFinal().find("HNorm_BE");
RooRealVar* H_par1_fitresult = (RooRealVar*) result->floatParsFinal().find("Ha_BE");
RooRealVar* H_par2_fitresult = (RooRealVar*) result->floatParsFinal().find("Hb_BE");
RooRealVar* H_par3_fitresult = (RooRealVar*) result->floatParsFinal().find("Hc_BE");
RooRealVar* H_par4_fitresult = (RooRealVar*) result->floatParsFinal().find("Hd_BE");
H_p_0      =H_par0_fitresult->getValV()   ;
H_p_0_error=H_par0_fitresult->getError()  ;
H_p_a      =H_par1_fitresult->getValV()   ;
H_p_a_error=H_par1_fitresult->getError()  ;
H_p_b      =H_par2_fitresult->getValV()   ;
H_p_b_error=H_par2_fitresult->getError()  ;
H_p_c      =H_par3_fitresult->getValV()   ;
H_p_c_error=H_par3_fitresult->getError()  ;
H_p_d      =H_par4_fitresult->getValV()   ;
H_p_d_error=H_par4_fitresult->getError()  ;
}

TLatex fit_bkg_label ;
fit_bkg_label.SetTextAlign(12) ;
fit_bkg_label.SetTextSize(0.03);
fit_bkg_label.SetNDC(kTRUE);
float y_space=0.04;
TString chi_ndof = Form("#chi^{2}/ndof     %f/%d"    ,chi2_val,nbins-5);
TString prob     = Form("Prob           %f"       ,TMath::Prob(chi2_val, nbins-5));
/*
TString L_P0     = Form("Lp0            %f #pm %f",L_p_0,L_p_0_error);
TString L_P1     = Form("Lp1            %e #pm %f",L_p_a,L_p_a_error);
TString L_P2     = Form("Lp2            %e #pm %e",L_p_b,L_p_b_error);
TString L_P3     = Form("Lp3            %e #pm %e",L_p_c,L_p_c_error);
TString L_P4     = Form("Lp4            %f #pm %f",L_p_d,L_p_d_error);
TString H_P0     = Form("Hp0            %f #pm %f",H_p_0,H_p_0_error);
TString H_P1     = Form("Hp1            %e #pm %f",H_p_a,H_p_a_error);
TString H_P2     = Form("Hp2            %e #pm %e",H_p_b,H_p_b_error);
TString H_P3     = Form("Hp3            %e #pm %e",H_p_c,H_p_c_error);
TString H_P4     = Form("Hp4            %f #pm %f",H_p_d,H_p_d_error);
TString H_Fun1   = "Pdf=(m<=600)*exp(Lp0+Lp1*m+Lp2*m^{2}+Lp3*m^{3})*m^{Lp4}+";
TString H_Fun2   = "    (m>600)*exp(Hp0+Hp1*m+Hp2*m^{2}+Hp3*m^{3})*m^{Hp4}"    ;
*/
TString L_P0     = Form("p0            %f #pm %f",L_p_0,L_p_0_error);
TString L_P1     = Form("p1            %e #pm %f",L_p_a,L_p_a_error);
TString L_P2     = Form("p2            %e #pm %e",L_p_b,L_p_b_error);
TString L_P3     = Form("p3            %e #pm %e",L_p_c,L_p_c_error);
TString L_P4     = Form("p4            %f #pm %f",L_p_d,L_p_d_error);
TString H_P0     = Form("p5            %f #pm %f",H_p_0,H_p_0_error);
TString H_P1     = Form("p6            %e #pm %f",H_p_a,H_p_a_error);
TString H_P2     = Form("p7            %e #pm %e",H_p_b,H_p_b_error);
TString H_P3     = Form("p8            %e #pm %e",H_p_c,H_p_c_error);
TString H_P4     = Form("p9            %f #pm %f",H_p_d,H_p_d_error);
TString H_Fun1   = "(m<=600)exp(p_{0}+p_{1}m+p_{2}m^{2}+p_{3}m^{3})m^{p_{4}}+";
TString H_Fun2   = "(m>600)exp(p_{5}+p_{6}m+p_{7}m^{2}+p_{8}m^{3})m^{p_{9}}"    ;


//TString H_Fun1   = "Pdf=(x<=600)*Lp0*exp(Lp1*x+Lp2*x^{2}+Lp3*x^{3})*x^{Lp4}";
//TString H_Fun2   ="+(x>600)*Hp0*exp(Hp1*x+Hp2*x^{2}+Hp3*x^{3})*x^{Hp4}"    ;
fit_bkg_label.DrawLatex(0.55,0.85          , chi_ndof );
fit_bkg_label.DrawLatex(0.55,0.85-y_space  , prob     );
fit_bkg_label.DrawLatex(0.55,0.85-2*y_space, L_P0     );
fit_bkg_label.DrawLatex(0.55,0.85-3*y_space, L_P1     );
fit_bkg_label.DrawLatex(0.55,0.85-4*y_space, L_P2     );
fit_bkg_label.DrawLatex(0.55,0.85-5*y_space, L_P3     );
fit_bkg_label.DrawLatex(0.55,0.85-6*y_space, L_P4     );
fit_bkg_label.DrawLatex(0.55,0.85-7*y_space, H_P0     );
fit_bkg_label.DrawLatex(0.55,0.85-8*y_space, H_P1     );
fit_bkg_label.DrawLatex(0.55,0.85-9*y_space, H_P2     );
fit_bkg_label.DrawLatex(0.55,0.85-10*y_space,H_P3    );
fit_bkg_label.DrawLatex(0.55,0.85-11*y_space,H_P4    );
TLatex pdf_label ;
pdf_label.SetTextAlign(12) ;
pdf_label.SetTextSize(0.045);
pdf_label.SetTextColor(2);
pdf_label.SetNDC(kTRUE);
pdf_label.DrawLatex(0.16,0.19        ,H_Fun1   );
pdf_label.DrawLatex(0.16,0.19-0.06   ,H_Fun2   );
float label_y=0.91;
TLatex cms_label ;
cms_label.SetTextSize(0.06);
cms_label.SetNDC(kTRUE);
cms_label.SetTextFont(61);
cms_label.DrawLatex(0.135,label_y, "CMS");
TLatex supp_label ;
supp_label.SetTextSize(0.06*0.8);
supp_label.SetNDC(kTRUE);
supp_label.SetTextFont(51);
supp_label.DrawLatex(0.24,label_y , "Simulation Supplementary");
TLatex lumi_label ;
lumi_label.SetTextSize(0.05);
lumi_label.SetNDC(kTRUE);
lumi_label.DrawLatex(0.68,label_y , "35.9 fb^{-1} (13 TeV)");
TLatex region_label ;
region_label.SetTextSize(0.04);
region_label.SetNDC(kTRUE);
TString mass_range = Form("(%.0f-%.0f GeV)",frame->GetXaxis()->GetXmin(),frame->GetXaxis()->GetXmax());
TString mass_low   = Form("%.0f",frame->GetXaxis()->GetXmin());
TString mass_up    = Form("%.0f",frame->GetXaxis()->GetXmax());
TString str_cos="";
if(out_name.Contains("cosp"))str_cos=" (cos#theta*>0)";
else if(out_name.Contains("cosm"))str_cos=" (cos#theta*<0)";
if(out_name.Contains("BB")){
region_label.DrawLatex(0.16,0.8 , "Barrel-Barrel"+str_cos+mass_range);
}
else if(out_name.Contains("BE")){
region_label.DrawLatex(0.16,0.8 , "Barrel-Endcap"+str_cos+mass_range);
}
/////////////////
pad2->cd();
TH2D *dum_bgk_ratio = new TH2D("dummy_bgk_ratio","",1,frame->GetXaxis()->GetXmin(),frame->GetXaxis()->GetXmax(),1,0.5,1.5);
dum_bgk_ratio->SetStats(kFALSE);
dum_bgk_ratio->GetYaxis()->SetTitle("bkg / fit");
dum_bgk_ratio->GetYaxis()->CenterTitle();
dum_bgk_ratio->GetXaxis()->SetTitle("m(ee) [GeV]");
dum_bgk_ratio->GetXaxis()->SetTitleSize(0.14);
dum_bgk_ratio->GetXaxis()->SetTitleOffset(1.1);
dum_bgk_ratio->GetXaxis()->SetLabelSize(0.13);
dum_bgk_ratio->GetXaxis()->SetMoreLogLabels();
dum_bgk_ratio->GetXaxis()->SetNoExponent()  ;
dum_bgk_ratio->GetYaxis()->SetNdivisions(405);
dum_bgk_ratio->GetYaxis()->SetTitleSize(0.14);
dum_bgk_ratio->GetYaxis()->SetLabelSize(0.13);
dum_bgk_ratio->GetYaxis()->SetTitleOffset(0.38);
dum_bgk_ratio->Draw();
TH1D *h_ratio=(TH1D*)hbgk->Clone("ratio");
for(int i=1;i<hbgk->GetNbinsX()+1;i++){
double value= hbgk->GetBinContent(i)/ph->GetBinContent(i)< 10000 ? hbgk->GetBinContent(i)/ph->GetBinContent(i) : 0;
//std::cout<<"bin:"<<i<<",value:"<<value<<std::endl;
double err=hbgk->GetBinError(i)/ph->GetBinContent(i);
h_ratio->SetBinContent(i,value);
h_ratio->SetBinError(  i,err  );
}
h_ratio->SetMarkerStyle(8);
h_ratio->Draw("same:pe");
TF1 *fline = new TF1("line", "[0]");
fline->SetParameters(0,1);
fline->SetLineColor(kBlue);
fline->SetLineWidth(3);
h_ratio->Fit(fline,"","",frame->GetXaxis()->GetXmin(),frame->GetXaxis()->GetXmax());
TLatex h_ratio_label ;
h_ratio_label.SetTextAlign(12) ;
h_ratio_label.SetTextSize(0.07);
h_ratio_label.SetNDC(kTRUE)    ;
TString r_chi_ndof = Form("#chi^{2}/ndof  %f/%d"    ,fline->GetChisquare(),fline->GetNDF());
TString r_Prob     = Form("Prob           %f"       ,fline->GetProb());
TString r_P1       = Form("p0             %f #pm %f",fline->GetParameter(0),fline->GetParError(0));
h_ratio_label.DrawLatex(0.15,0.54,r_chi_ndof); 
h_ratio_label.DrawLatex(0.15,0.47,r_Prob    );
h_ratio_label.DrawLatex(0.15,0.4,r_P1      );

can->Print(out_name+mass_low+"_"+mass_up+"_bgk.png");    
can->Print(out_name+mass_low+"_"+mass_up+"_bgk.pdf");    
can->Print(out_name+mass_low+"_"+mass_up+"_bgk.root");    
can->Delete();

}
void draw( RooRealVar x, RooDataHist hist, TH1D* hh, RooGenericPdf pdf, RooFitResult* result ,TString out_name){
RooPlot* frame = x.frame();
TCanvas *can = new TCanvas("can","",1000,1000);
can->cd();
TPad *pad1 = new TPad("pad1", "", 0.0, 0.3, 1.0, 1.0, 0);
TPad *pad2 = new TPad("pad2", "", 0.0, 0.0, 1.0, 0.3, 0);
pad1->Draw();
pad2->Draw();
pad1->SetBottomMargin(0.07);
pad2->SetTopMargin(0);
pad2->SetBottomMargin(0.35);
pad1->SetRightMargin(0.07);
pad1->SetLeftMargin(0.13);
pad2->SetRightMargin(0.07);
pad2->SetLeftMargin(0.13);
pad2->SetGridy();
pad1->SetTickx();
pad1->SetTicky();
pad2->SetTickx();
pad2->SetTicky();
pad1->SetLogy();
pad1->cd();
//hist.plotOn(frame);//possion error
hist.plotOn(frame,DataError(RooAbsData::SumW2));
pdf.plotOn(frame);
frame->SetMaximum(5E4);
frame->SetMinimum(1E-4);
//frame->SetMaximum(2E5);
//frame->SetMinimum(1E1);
//frame->SetMaximum(2E5);
//frame->SetMinimum(1E1);
frame->SetTitle("");
frame->SetXTitle("");
frame->SetYTitle("Events / 20 GeV");
frame->GetXaxis()->SetLabelSize(0.055);
frame->GetYaxis()->SetLabelSize(0.055);
frame->GetYaxis()->SetTitleSize(0.055);
frame->Draw();
int nbins=(frame->GetXaxis()->GetXmax()-frame->GetXaxis()->GetXmin())/hh->GetBinWidth(1);
TH1* ph=pdf.createHistogram("ph",x,Binning(nbins));
TH1D *hbgk= new TH1D("hbgk","",nbins,frame->GetXaxis()->GetXmin(),frame->GetXaxis()->GetXmax());
for(int i=1;i<nbins+1;i++){
float mean=hbgk->GetBinLowEdge(i)+0.5*hbgk->GetBinWidth(i);
int bin_x=hh->GetXaxis()->FindBin(mean);
hbgk->SetBinContent(i,hh->GetBinContent(bin_x));
hbgk->SetBinError  (i,hh->GetBinError  (bin_x));
}
//int bin_low=hh->GetXaxis()->FindBin(frame->GetXaxis()->GetXmin());
//int bin_up =hh->GetXaxis()->FindBin(frame->GetXaxis()->GetXmax());
//double scale=hh->Integral(bin_low,bin_up)/ph->Integral();
double scale=hbgk->Integral()/ph->Integral();
std::cout<<"scale:"<<scale<<std::endl;
ph->Scale(scale);
//ph->Draw("same");
//hbgk->Draw("same:hist");
//////// parameters
RooChi2Var chi2 ("chi2", "chi2", pdf, hist);
double chi2_val = chi2.getVal();

double p_0      =0;
double p_0_error=0;
double p_a      =0;
double p_a_error=0;
double p_b      =0;
double p_b_error=0;
double p_c      =0;
double p_c_error=0;
double p_d      =0;
double p_d_error=0;

if(out_name.Contains("BB")){
RooRealVar* par0_fitresult = (RooRealVar*) result->floatParsFinal().find("Norm_BB");
RooRealVar* par1_fitresult = (RooRealVar*) result->floatParsFinal().find("a_BB");
RooRealVar* par2_fitresult = (RooRealVar*) result->floatParsFinal().find("b_BB");
RooRealVar* par3_fitresult = (RooRealVar*) result->floatParsFinal().find("c_BB");
RooRealVar* par4_fitresult = (RooRealVar*) result->floatParsFinal().find("d_BB");
p_0      =10*par0_fitresult->getValV()   ;
p_0_error=10*par0_fitresult->getError() ;
p_a      =1e-3*par1_fitresult->getValV()   ;
p_a_error=1e-3*par1_fitresult->getError() ;
p_b      =1e-8*par2_fitresult->getValV()   ;
p_b_error=1e-8*par2_fitresult->getError() ;
p_c      =1e-11*par3_fitresult->getValV()   ;
p_c_error=1e-11*par3_fitresult->getError() ;
p_d      =par4_fitresult->getValV()   ;
p_d_error=par4_fitresult->getError() ;
}
else if(out_name.Contains("BE")){
RooRealVar* par0_fitresult = (RooRealVar*) result->floatParsFinal().find("Norm_BE");
RooRealVar* par1_fitresult = (RooRealVar*) result->floatParsFinal().find("a_BE");
RooRealVar* par2_fitresult = (RooRealVar*) result->floatParsFinal().find("b_BE");
RooRealVar* par3_fitresult = (RooRealVar*) result->floatParsFinal().find("c_BE");
RooRealVar* par4_fitresult = (RooRealVar*) result->floatParsFinal().find("d_BE");
p_0      =10*par0_fitresult->getValV()   ;
p_0_error=10*par0_fitresult->getError() ;
p_a      =1e-3*par1_fitresult->getValV()   ;
p_a_error=1e-3*par1_fitresult->getError() ;
p_b      =1e-8*par2_fitresult->getValV()   ;
p_b_error=1e-8*par2_fitresult->getError() ;
p_c      =1e-11*par3_fitresult->getValV()   ;
p_c_error=1e-11*par3_fitresult->getError() ;
p_d      =par4_fitresult->getValV()   ;
p_d_error=par4_fitresult->getError() ;
}

TLatex fit_bkg_label ;
fit_bkg_label.SetTextAlign(12) ;
fit_bkg_label.SetTextSize(0.04);
fit_bkg_label.SetNDC(kTRUE);
float y_space=0.05;
TString chi_ndof = Form("#chi^{2}/ndof     %f/%d"    ,chi2_val,nbins-5);
TString prob     = Form("Prob           %f"       ,TMath::Prob(chi2_val, nbins-5));
TString P0       = Form("p0             %f #pm %f",p_0,p_0_error);
TString P1       = Form("p1             %e #pm %f",p_a,p_a_error);
TString P2       = Form("p2             %e #pm %e",p_b,p_b_error);
TString P3       = Form("p3             %e #pm %e",p_c,p_c_error);
TString P4       = Form("p4             %f #pm %f",p_d,p_d_error);
fit_bkg_label.DrawLatex(0.4,0.85          , chi_ndof );
fit_bkg_label.DrawLatex(0.4,0.85-y_space  , prob     );
fit_bkg_label.DrawLatex(0.4,0.85-2*y_space, P0       );
fit_bkg_label.DrawLatex(0.4,0.85-3*y_space, P1       );
fit_bkg_label.DrawLatex(0.4,0.85-4*y_space, P2       );
fit_bkg_label.DrawLatex(0.4,0.85-5*y_space, P3       );
fit_bkg_label.DrawLatex(0.4,0.85-6*y_space, P4       );

TLatex lumi_label ;
lumi_label.SetTextSize(0.04);
lumi_label.SetNDC(kTRUE);
lumi_label.DrawLatex(0.2,0.20 , "35.9 fb^{-1}, 13 TeV");
TLatex region_label ;
region_label.SetTextSize(0.04);
region_label.SetNDC(kTRUE);
TString mass_range = Form("(%.0f-%.0f GeV)",frame->GetXaxis()->GetXmin(),frame->GetXaxis()->GetXmax());
TString mass_low   = Form("%.0f",frame->GetXaxis()->GetXmin());
TString mass_up    = Form("%.0f",frame->GetXaxis()->GetXmax());
TString str_cos="";
if(out_name.Contains("cosp"))str_cos=" (cos#theta*>0)";
else if(out_name.Contains("cosm"))str_cos=" (cos#theta*<0)";
if(out_name.Contains("BB")){
region_label.DrawLatex(0.2,0.15 , "Barrel-Barrel"+str_cos+mass_range);
}
else if(out_name.Contains("BE")){
region_label.DrawLatex(0.2,0.15 , "Barrel-Endcap"+str_cos+mass_range);
}
/////////////////
pad2->cd();
TH2D *dum_bgk_ratio = new TH2D("dummy_bgk_ratio","",1,frame->GetXaxis()->GetXmin(),frame->GetXaxis()->GetXmax(),1,0.5,1.5);
dum_bgk_ratio->SetStats(kFALSE);
dum_bgk_ratio->GetYaxis()->SetTitle("bkg / fit");
dum_bgk_ratio->GetYaxis()->CenterTitle();
dum_bgk_ratio->GetXaxis()->SetTitle("m(ee) [GeV]");
dum_bgk_ratio->GetXaxis()->SetTitleSize(0.14);
dum_bgk_ratio->GetXaxis()->SetTitleOffset(1.1);
dum_bgk_ratio->GetXaxis()->SetLabelSize(0.13);
dum_bgk_ratio->GetXaxis()->SetMoreLogLabels();
dum_bgk_ratio->GetXaxis()->SetNoExponent()  ;
dum_bgk_ratio->GetYaxis()->SetNdivisions(405);
dum_bgk_ratio->GetYaxis()->SetTitleSize(0.14);
dum_bgk_ratio->GetYaxis()->SetLabelSize(0.13);
dum_bgk_ratio->GetYaxis()->SetTitleOffset(0.38);
dum_bgk_ratio->Draw();
TH1D *h_ratio=(TH1D*)hbgk->Clone("ratio");
for(int i=1;i<hbgk->GetNbinsX()+1;i++){
double value= hbgk->GetBinContent(i)/ph->GetBinContent(i)< 10000 ? hbgk->GetBinContent(i)/ph->GetBinContent(i) : 0;
//std::cout<<"bin:"<<i<<",value:"<<value<<std::endl;
double err=hbgk->GetBinError(i)/ph->GetBinContent(i);
h_ratio->SetBinContent(i,value);
h_ratio->SetBinError(  i,err  );
}
h_ratio->SetMarkerStyle(8);
h_ratio->Draw("same:pe");
TF1 *fline = new TF1("line", "[0]");
fline->SetParameters(0,1);
fline->SetLineColor(kBlue);
fline->SetLineWidth(3);
h_ratio->Fit(fline,"","",frame->GetXaxis()->GetXmin(),frame->GetXaxis()->GetXmax());
TLatex h_ratio_label ;
h_ratio_label.SetTextAlign(12) ;
h_ratio_label.SetTextSize(0.07);
h_ratio_label.SetNDC(kTRUE)    ;
TString r_chi_ndof = Form("#chi^{2}/ndof  %f/%d"    ,fline->GetChisquare(),fline->GetNDF());
TString r_Prob     = Form("Prob           %f"       ,fline->GetProb());
TString r_P1       = Form("p0             %f #pm %f",fline->GetParameter(0),fline->GetParError(0));
h_ratio_label.DrawLatex(0.15,0.54,r_chi_ndof); 
h_ratio_label.DrawLatex(0.15,0.47,r_Prob    );
h_ratio_label.DrawLatex(0.15,0.4,r_P1      );

can->Print(out_name+mass_low+"_"+mass_up+"_bgk.png");    
can->Delete();

}

void draw_compare(TH1D* hist, TF1* fun, TString out_name){
TCanvas *can = new TCanvas("can","",1000,1000);
can->cd();
TPad *pad1 = new TPad("pad1", "", 0.0, 0.3, 1.0, 1.0, 0);
TPad *pad2 = new TPad("pad2", "", 0.0, 0.0, 1.0, 0.3, 0);
pad1->Draw();
pad2->Draw();
pad1->SetBottomMargin(0.07);
pad2->SetTopMargin(0);
pad2->SetBottomMargin(0.35);
pad1->SetRightMargin(0.07);
pad1->SetLeftMargin(0.13);
pad2->SetRightMargin(0.07);
pad2->SetLeftMargin(0.13);
pad2->SetGridy();
pad1->SetTickx();
pad1->SetTicky();
pad2->SetTickx();
pad2->SetTicky();
pad1->SetLogy();
pad1->cd();
double x_min=100;
double x_max=4000;
double y_min=1e-4;
double y_max=5e4;
TH2D *dum_bgk = new TH2D("dummy_bgk_ratio","",1,x_min,x_max,1,y_min,y_max);
dum_bgk->SetStats(kFALSE);
dum_bgk->GetYaxis()->SetTitle("Events / 20 GeV");
dum_bgk->GetXaxis()->SetTitle("m(ee) [GeV]");
dum_bgk->GetXaxis()->SetLabelSize(0.055);
dum_bgk->GetYaxis()->SetLabelSize(0.055);
dum_bgk->GetYaxis()->SetTitleSize(0.055);
dum_bgk->GetXaxis()->SetTitleSize(0);
dum_bgk->GetXaxis()->SetMoreLogLabels();
dum_bgk->GetXaxis()->SetNoExponent()  ;
dum_bgk->GetYaxis()->SetNdivisions(405);
dum_bgk->Draw();
hist->Draw("same:pe");
std::cout<<"500="<<fun->Eval(500)<<std::endl;
fun->Draw("same");
pad2->cd();
TH2D *dum_bgk_ratio = new TH2D("dummy_bgk_ratio","",1,x_min,x_max,1,0.5,1.5);
dum_bgk_ratio->SetStats(kFALSE);
dum_bgk_ratio->GetYaxis()->SetTitle("bkg / fit");
dum_bgk_ratio->GetYaxis()->CenterTitle();
dum_bgk_ratio->GetXaxis()->SetTitle("m(ee) [GeV]");
dum_bgk_ratio->GetXaxis()->SetTitleSize(0.14);
dum_bgk_ratio->GetXaxis()->SetTitleOffset(1.1);
dum_bgk_ratio->GetXaxis()->SetLabelSize(0.13);
dum_bgk_ratio->GetXaxis()->SetMoreLogLabels();
dum_bgk_ratio->GetXaxis()->SetNoExponent()  ;
dum_bgk_ratio->GetYaxis()->SetNdivisions(405);
dum_bgk_ratio->GetYaxis()->SetTitleSize(0.14);
dum_bgk_ratio->GetYaxis()->SetLabelSize(0.13);
dum_bgk_ratio->GetYaxis()->SetTitleOffset(0.38);
dum_bgk_ratio->Draw();

TH1D *h_ratio=(TH1D*)hist->Clone("ratio");
for(int i=1;i<hist->GetNbinsX()+1;i++){
double mean=hist->GetBinLowEdge(i)+0.5*hist->GetBinWidth(i);
double value= hist->GetBinContent(i)/fun->Eval(mean);
double err=hist->GetBinError(i)/fun->Eval(mean);
h_ratio->SetBinContent(i,value);
h_ratio->SetBinError  (i,err  );
}
h_ratio->SetMarkerStyle(8);
h_ratio->Draw("same:pe");

can->Print(out_name+"_bgk.png");    
can->Delete();
}

void draw_compare_two(TH1D* hist, TF1* fun1, TF1* fun2, TString out_name){
TCanvas *can = new TCanvas("can","",1000,1000);
can->cd();
TPad *pad1 = new TPad("pad1", "", 0.0, 0.3, 1.0, 1.0, 0);
TPad *pad2 = new TPad("pad2", "", 0.0, 0.0, 1.0, 0.3, 0);
pad1->Draw();
pad2->Draw();
pad1->SetBottomMargin(0.07);
pad2->SetTopMargin(0);
pad2->SetBottomMargin(0.35);
pad1->SetRightMargin(0.07);
pad1->SetLeftMargin(0.13);
pad2->SetRightMargin(0.07);
pad2->SetLeftMargin(0.13);
pad2->SetGridy();
pad1->SetTickx();
pad1->SetTicky();
pad2->SetTickx();
pad2->SetTicky();
pad1->SetLogy();
pad1->cd();
double x_min=140;
double x_max=4000;
double y_min=1e-4;
double y_max=5e4;
//double y_min=1e1;
//double y_max=1e2;
TH2D *dum_bgk = new TH2D("dummy_bgk_ratio","",1,x_min,x_max,1,y_min,y_max);
dum_bgk->SetStats(kFALSE);
dum_bgk->GetYaxis()->SetTitle("Events / 20 GeV");
dum_bgk->GetXaxis()->SetTitle("m(ee) [GeV]");
dum_bgk->GetXaxis()->SetLabelSize(0.055);
dum_bgk->GetYaxis()->SetLabelSize(0.055);
dum_bgk->GetYaxis()->SetTitleSize(0.055);
dum_bgk->GetXaxis()->SetTitleSize(0);
dum_bgk->GetXaxis()->SetMoreLogLabels();
dum_bgk->GetXaxis()->SetNoExponent()  ;
dum_bgk->GetYaxis()->SetNdivisions(405);
dum_bgk->Draw();
hist->Draw("same:pe");
fun1->SetLineColor(2);
fun2->SetLineColor(4);
//fun1->Draw("same");
//fun2->Draw("same");
fun1->DrawF1(140,600,"same");
fun2->DrawF1(580,4000,"same");
pad2->cd();
TH2D *dum_bgk_ratio = new TH2D("dummy_bgk_ratio","",1,x_min,x_max,1,0.5,1.5);
dum_bgk_ratio->SetStats(kFALSE);
dum_bgk_ratio->GetYaxis()->SetTitle("bgk / fit");
dum_bgk_ratio->GetYaxis()->CenterTitle();
dum_bgk_ratio->GetXaxis()->SetTitle("m(ee) [GeV]");
dum_bgk_ratio->GetXaxis()->SetTitleSize(0.14);
dum_bgk_ratio->GetXaxis()->SetTitleOffset(1.1);
dum_bgk_ratio->GetXaxis()->SetLabelSize(0.13);
dum_bgk_ratio->GetXaxis()->SetMoreLogLabels();
dum_bgk_ratio->GetXaxis()->SetNoExponent()  ;
dum_bgk_ratio->GetYaxis()->SetNdivisions(405);
dum_bgk_ratio->GetYaxis()->SetTitleSize(0.14);
dum_bgk_ratio->GetYaxis()->SetLabelSize(0.13);
dum_bgk_ratio->GetYaxis()->SetTitleOffset(0.38);
dum_bgk_ratio->Draw();

TH1D *h_ratio=(TH1D*)hist->Clone("ratio");
for(int i=1;i<hist->GetNbinsX()+1;i++){
double mean=hist->GetBinLowEdge(i)+0.5*hist->GetBinWidth(i);
double value= mean<fun1->GetXmax()? hist->GetBinContent(i)/fun1->Eval(mean) : hist->GetBinContent(i)/fun2->Eval(mean);
double err= mean<fun1->GetXmax()  ? hist->GetBinError(i)/fun1->Eval(mean) : hist->GetBinError(i)/fun2->Eval(mean)    ;
h_ratio->SetBinContent(i,value);
h_ratio->SetBinError  (i,err  );
}
h_ratio->SetMarkerStyle(8);
h_ratio->Draw("same:pe");

can->Print(out_name+"_bgk.png");    
can->Delete();
}
