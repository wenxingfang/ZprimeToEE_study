import ROOT
import os
fout=open("PU_reWeighting.C","w")
#Dir="./data_mc_pu/"
#Dir="./mc_pu_2017/"
Dir="./mc_pu_2017SF/"
#Dir="./mc_pu_2018/"
file_list=[]
files = os.listdir(Dir)
for ifile in files:
    file_list.append("%s"%(ifile))
print file_list

str_head='''
#include <map>
#include <TString.h>
#include <iostream>
namespace PU_2017_Rereco{
'''
str_end='''
double MC_pileup_weight(int NumTrueInteraction, TString mc, TString data_scale){
if (NumTrueInteraction < 0 || NumTrueInteraction > 120 ) return 1;
map<TString,double*>::const_iterator iter_mc   = map_pu.find(mc);
map<TString,double*>::const_iterator iter_data = map_pu.find(data_scale);
if(iter_mc != map_pu.end() && iter_data != map_pu.end()) {return iter_mc->second[NumTrueInteraction]!=0 ? double(iter_data->second[NumTrueInteraction]/iter_mc->second[NumTrueInteraction]) : 1 ;}
else {if(iter_mc == map_pu.end())  std::cout<<"no "<<mc        <<std::endl;
      if(iter_data == map_pu.end())std::cout<<"no "<<data_scale<<std::endl;
      return  1;}
}
}
'''
README='''
/*
.L PU_reWeighting.C+
PU_2017_Rereco::MC_pileup_weight(int NumTrueInteraction, TString mc, TString data_scale)
Possible TString mc and TString data_scale list below:
'''
sep=","
fout.write(README)
for ifile in files:
    tmp_name=ifile.split(".root")[0]
    fout.write(tmp_name+"|")
fout.write("\n")
fout.write("*/\n")
fout.write(str_head+"\n")
for ifile in file_list:
    file_tmp=ROOT.TFile(Dir+ifile,"read")
    h_tmp=file_tmp.Get("pileup")
    h_tmp.Scale(1/h_tmp.GetSumOfWeights())
    tmp_name=ifile.split(".root")[0]
    fout.write("double %s[%d]={\n"%(tmp_name,h_tmp.GetNbinsX()))
    for ibin in range(1,h_tmp.GetNbinsX()+1):
        if ibin == h_tmp.GetNbinsX():
            fout.write("%e\n"%(h_tmp.GetBinContent(ibin)))
        else:
            fout.write("%e,\n"%(h_tmp.GetBinContent(ibin)))
    fout.write("};\n")
    file_tmp.Close()
fout.write("const std::map<TString,double*>::value_type init_value[] ={\n")
for ifile in file_list:
    tmp_name=ifile.split(".root")[0]
    if ifile!=file_list[-1]:
        fout.write('std::map<TString,double*>::value_type( "%s", %s),\n'%(tmp_name,tmp_name))
    else:
        fout.write('std::map<TString,double*>::value_type( "%s", %s)\n'%(tmp_name,tmp_name))
fout.write("};\n")
fout.write("const static std::map<TString,double*> map_pu(init_value, init_value+%d);\n"%(len(file_list)))
fout.write(str_end+"\n")
fout.close()
print "done"
