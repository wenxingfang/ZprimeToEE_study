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

#include<stdio.h>
#include "TProfile.h"
#include <string>
#include <sstream>
#include <TH2.h>
#include <TLatex.h>
#include <TH1.h>
#include <TF1.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TPad.h>
#include "TFile.h"
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
void draw( RooRealVar x, RooDataHist hist, TH1D* hh, RooGenericPdf pdf, RooFitResult* result, TString out_name);
void bgk_fit(){
RooAbsReal::defaultIntegratorConfig()->Print("v") ;
RooAbsReal::defaultIntegratorConfig()->setEpsAbs(1e-10) ;
RooAbsReal::defaultIntegratorConfig()->setEpsRel(1e-10) ;

TH1::SetDefaultSumw2();
gSystem->Load("libRooFit");
gROOT->Reset();
gROOT->SetStyle("Plain");

TFile* f = new TFile("bgk.root","READ");
TH1D* h_BB  = (TH1D*) f->Get("bgk_h_mee_BB_usual");
TH1D* h_BE  = (TH1D*) f->Get("bgk_h_mee_BE_usual");
TH1D* h_BE_v1=(TH1D*)h_BE->Rebin(2,"bgk_h_mee_BE_usual_v1");
const float fit_low=200;//200
const float fit_up=4000;//4000
RooRealVar x("x","x",  fit_low  ,  fit_up );

RooRealVar Norm_BB  ("Norm_BB"  ,""     ,  3.10        , 2.8     , 3.5   );
RooRealVar a_BB     ("a_BB"     ,""     , -1.0748      ,-1.3     , -0.8  );
RooRealVar b_BB     ("b_BB"     ,""     ,  4.50        , 0.5     , 10.00 );
RooRealVar c_BB     ("c_BB"     ,""     , -1.9388      ,-2.20    , -1.2  );
RooRealVar d_BB     ("d_BB"     ,""     , -3.956       ,-4.2     , -3.6  );
RooGenericPdf pdf_BB("pdf_BB","pdf_BB","10*Norm_BB*exp(1e-3*a_BB*x+1e-8*b_BB*pow(x,2)+1e-11*c_BB*pow(x,3))*pow(x,d_BB)",RooArgSet(x,a_BB,b_BB,c_BB,d_BB,Norm_BB)) ;

/*
RooRealVar Norm_BB  ("Norm_BB"  ,""     ,  21.00       , 20      , 25   );
RooRealVar a_BB     ("a_BB"     ,""     , -1.70        ,-3.00    , -1.00 );
RooRealVar b_BB     ("b_BB"     ,""     , -1e-3        ,-1e-1    , -1e-4 );
RooRealVar c_BB     ("c_BB"     ,""     , -2e-5        ,-5e-5    , -1e-5 );
RooRealVar d_BB     ("d_BB"     ,""     , -0.0016      ,-0.003   , -0.001 );
RooGenericPdf pdf_BB("pdf_BB","pdf_BB","Norm_BB*pow(x,a_BB+b_BB*log(x)+c_BB*pow(log(x),2)+d_BB*pow(log(x),3))",RooArgSet(x,a_BB,b_BB,c_BB,d_BB,Norm_BB)) ;
*/
//std::cout<<"test="<<log(2.718)<<std::endl;

RooRealVar Norm_BE  ("Norm_BE"  ,""     ,  2.35        , 2.0     , 2.6   );
RooRealVar a_BE     ("a_BE"     ,""     , -3.85        ,-6.00    , -2.00 );
RooRealVar b_BE     ("b_BE"     ,""     ,  65.55       , 60.00   , 90.00 );
RooRealVar c_BE     ("c_BE"     ,""     , -7.44        ,-10.00   , -6.00 );
RooRealVar d_BE     ("d_BE"     ,""     , -2.90        ,-4.00    , -2.00  );
RooGenericPdf pdf_BE("pdf_BE","pdf_BE","Norm_BE*exp(1e-3*a_BE*x+1e-8*b_BE*pow(x,2)+1e-11*c_BE*pow(x,3))*pow(x,d_BE)",RooArgSet(x,a_BE,b_BE,c_BE,d_BE,Norm_BE)) ;

/*
RooRealVar Norm_BE  ("Norm_BE"  ,""     ,  2.5        , 2.2     , 2.6   );
RooRealVar a_BE     ("a_BE"     ,""     , -3.70        ,-6.00    , -2.00 );
RooRealVar b_BE     ("b_BE"     ,""     ,  80.30       , 60.00   , 90.00 );
RooRealVar c_BE     ("c_BE"     ,""     , -9.12        ,-10.00   , -6.00 );
RooRealVar d_BE     ("d_BE"     ,""     , -3.02        ,-4.00    , -2.00 );
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
RooDataHist dh_BE_v1("dh_BE_v1","dh_BE_v1"   ,x, h_BE_v1);

//RooFitResult* result = pdf_BB.fitTo(dh_BB,Range(200,1000),SumW2Error(kTRUE),Save()) ;
//RooFitResult* result = pdf_BB.fitTo(dh_BB,SumW2Error(kTRUE),Save()) ;
//RooFitResult* result = pdf_BB.fitTo(dh_BB,SumW2Error(kTRUE),Save()) ;
//RooFitResult* result = model.fitTo(dh_BB,Range(200,800),SumW2Error(kTRUE),Save()) ;

/*
RooFitResult* result_BB = pdf_BB.chi2FitTo(dh_BB,Save()) ;
draw( x, dh_BB, h_BB, pdf_BB, result_BB ,"BB_");
*/

RooFitResult* result_BE = pdf_BE.chi2FitTo(dh_BE,Save()) ;
draw( x, dh_BE, h_BE, pdf_BE, result_BE ,"BE_");

/*
RooFitResult* result_BE = pdf_BE.chi2FitTo(dh_BE_v1,Save()) ;
draw( x, dh_BE_v1, h_BE_v1, pdf_BE, result_BE ,"BE_");
*/
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
if(out_name.Contains("BB")){
region_label.DrawLatex(0.2,0.15 , "Barrel-Barrel");
}
else if(out_name.Contains("BE")){
region_label.DrawLatex(0.2,0.15 , "Barrel-Endcap");
}
/////////////////
pad2->cd();
TH2D *dum_bgk_ratio = new TH2D("dummy_bgk_ratio","",1,frame->GetXaxis()->GetXmin(),frame->GetXaxis()->GetXmax(),1,0.5,1.5);
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

can->Print(out_name+"_bgk.png");    
can->Delete();

}

